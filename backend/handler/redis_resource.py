import json
from datetime import datetime
import asyncio
import aioredis
import random
from collections import defaultdict
import traceback

import logging
logger = logging.getLogger(__name__)

class RedisResource:
    def __init__(self, redis, base_path, id_prefix):
        self.redis = redis
        self.base_path = base_path
        self.id_prefix = id_prefix
        self.key_counter = f"{base_path}/Counter"

    @classmethod
    def create_instance(cls):
        pass

    def id(self, cnt):
        return f"{self.id_prefix}:{cnt:08}"

    def key(self, cnt=None, id=None):
        if cnt:   return f"{self.base_path}/{self.id(cnt)}"
        elif id: return f"{self.base_path}/{id}"

    async def get_counter(self):
        return int(await self.redis.execute_str("GET", self.key_counter))

    async def next_count(self):
        return await self.redis.execute("INCR", self.key_counter)

    async def add(self, data):
        cnt = await self.next_count()
        id = self.id(cnt=cnt)
        data["Timestamp"] = datetime.now().timestamp()
        res = await self.redis.execute("SET", self.key(id=id), json.dumps(data))
        await self._on_add(id, data)
        return id

    async def update(self, id, data):
        await self.redis.execute("SET", self.key(id=id), json.dumps(data))
        await self._on_update(id, data)

    async def get(self, id):
        data = await self.redis.execute("GET", self.key(id=id))
        return json.loads(data) if data else None

    async def _delete(self, id):
        data = await self.get(id)
        await self.redis.execute("DEL", self.key(id=id))
        return data

    async def delete(self, id):
        data = await self._delete(id)
        await self._on_delete(id, data)

    async def delete_multi(self, ids):
        data = [await self._delete(id) for id in ids]
        await self._on_delete_multi(ids, data)

    async def _on_add(self, id, data):
        pass

    async def _on_update(self, id, data):
        pass

    async def _on_delete(self, id, data):
        pass

    async def _on_delete_multi(self, ids, data):
        pass


class WorkerResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Worker", "WKR")

    def key_ids_for_pn(self,pn):                   return f"WorkerIds/PRJ:{pn}"
    def key_ids_assigned_for_nid(self,nid):        return f"WorkerIdsAssigned/{nid}"
    def key_ids_map_for_platform(self, platform):  return f"WorkerIdsMap/{platform}"
    def key_prj_ids(self,pn):                      return f"ProjectWorkerIds/PRJ:{pn}"
    def key_prj_id_counter(self,pn):               return f"ProjectWorkerIds/PRJ:{pn}/Counter"
        
    @classmethod
    def create_instance(cls, platform_wid, platform):
        return {
            "PlatformWorkerId": platform_wid,
            "Platform": platform
        }

    async def _on_add(self, id, data):
        platform_wid = data["PlatformWorkerId"]
        platform = data["Platform"]
        await self.add_id_map_for_platform(platform, platform_wid, id)

    async def get_ids_for_pn(self, pn):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_for_pn(pn))

    async def add_id_map_for_platform(self, platform, platform_wid, id):
        await self.redis.execute("HSET", self.key_ids_map_for_platform(platform), platform_wid, id)

    async def get_id_for_platform(self, platform, platform_wid):
        return await self.redis.execute_str("HGET", self.key_ids_map_for_platform(platform), platform_wid)

    async def add_id_for_pn(self, pn, id):
        await self.redis.execute("SADD", self.key_ids_for_pn(pn), id)

    async def add_id_assigned_for_nid(self, nid, id):
        return await self.redis.execute("SADD", self.key_ids_assigned_for_nid(nid), id)

    async def delete_id_assigned_for_nid(self, nid, id):
        return await self.redis.execute("SREM", self.key_ids_assigned_for_nid(nid), id)

    async def get_ids_assigned_for_nid(self, nid):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_assigned_for_nid(nid))

    async def add_prj_id(self, pn, id):
        if not (prj_id := await self.get_prj_id(pn, id)):
            next_prj_id = await self.redis.execute("INCR", self.key_prj_id_counter(pn))
            return await self.redis.execute("HSET", self.key_prj_ids(pn), id, next_prj_id)

    async def get_prj_id(self, pn, id):
        try:
            return int(await self.redis.execute_str("HGET", self.key_prj_ids(pn), id))
        except:
            return None

class NanotaskResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Nanotask", "NT")
        self.r_wkr = WorkerResource(redis)
        self.weight_for_assignment = 100000

        self.reserve_nanotask_lock = asyncio.Condition()

        self.pool = None

    def key_ids_for_pn_tn(self,pn,tn):                     return f"NanotaskIds/PRJ:{pn}/TMPL:{tn}"
    def key_ids_occupied_for_pn_tn(self,pn,tn):            return f"NanotaskIdsOccupied/PRJ:{pn}/TMPL:{tn}"
    #def key_ids_completed_for_pn_tn(self,pn,tn):           return f"NanotaskIdsCompleted/PRJ:{pn}/TMPL:{tn}"
    def key_ids_assigned_for_pn_tn_wid(self,pn,tn,wid):    return f"NanotaskIdsAssigned/PRJ:{pn}/TMPL:{tn}/{wid}"
    def key_ids_completed_for_pn_tn_wid(self,pn,tn,wid):   return f"NanotaskIdsCompleted/PRJ:{pn}/TMPL:{tn}/{wid}"
    def key_ids_assignable_for_pn_tn_wid(self,pn,tn,wid):  return f"NanotaskIdsAssignable/PRJ:{pn}/TMPL:{tn}/{wid}"

    @classmethod
    def create_instance(cls, pn, tn, tag, num_assignable, priority, ref, props):
        return {
            "ProjectName": pn,
            "TemplateName": tn,
            "Tag": tag,
            "NumAssignable": num_assignable,
            "Priority": priority,
            "ReferenceAnswers": ref,
            "Props": props
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        tn = data["TemplateName"]
        priority = data["Priority"]

        await self.add_id_for_pn_tn(pn, tn, priority*self.weight_for_assignment, id)

    async def _on_delete(self, id, data):
        pn = data["ProjectName"]
        tn = data["TemplateName"]

        await self.delete_ids_for_pn_tn(pn, tn, id)

    async def _on_delete_multi(self, ids, data):
        pn = data[0]["ProjectName"]
        tn = data[0]["TemplateName"]

        await self.delete_ids_for_pn_tn(pn, tn, *ids)
        

    async def assign(self, pn, tn, wid, id):
        nt = await self.get(id)
        num_assignable = nt["NumAssignable"]
        num_assigned = len(await self.r_wkr.get_ids_assigned_for_nid(id))

        await self.add_id_assigned_for_pn_tn_wid(pn, tn, wid, id)
        await self.r_wkr.add_id_assigned_for_nid(id, wid)
        await self.add_id_occupied_for_pn_tn(pn, tn, id) if num_assignable<=num_assigned else None

    async def unassign(self, pn, tn, wid, id):
        await self.delete_id_occupied_for_pn_tn(pn,tn,id)
        await self.delete_id_assigned_for_pn_tn_wid(pn,tn,wid,id)
        await self.r_wkr.delete_id_assigned_for_nid(id,wid)
        await self.decrement_assignment_weight_for_pn_tn(pn,tn,id)

    async def decrement_assignment_weight_for_pn_tn(self, pn, tn, id):
        await self.redis.execute("ZINCRBY", self.key_ids_for_pn_tn(pn,tn), -1, id)

    async def add_id_for_pn_tn(self, pn, tn, priority, id):
        await self.redis.execute("ZADD", self.key_ids_for_pn_tn(pn,tn), priority, id)

    async def add_id_occupied_for_pn_tn(self, pn, tn, id):
        return await self.redis.execute("SADD", self.key_ids_occupied_for_pn_tn(pn,tn), id)

    async def add_id_assigned_for_pn_tn_wid(self, pn, tn, wid, id):
        return await self.redis.execute("SADD", self.key_ids_assigned_for_pn_tn_wid(pn,tn,wid), id)

    #async def add_id_completed_for_pn_tn(self, pn, tn, id):
    #    await self.redis.execute("SADD", self.key_ids_completed_for_pn_tn(pn,tn), id)

    async def add_id_completed_for_pn_tn_wid(self, pn, tn, wid, id):
        await self.redis.execute("SADD", self.key_ids_completed_for_pn_tn_wid(pn,tn,wid), id)


    async def delete_ids_for_pn_tn(self, pn, tn, *ids):
        await self.redis.execute("ZREM", self.key_ids_for_pn_tn(pn,tn), *ids)

    async def delete_id_assigned_for_pn_tn_wid(self, pn, tn, wid, id):
        return await self.redis.execute("SREM", self.key_ids_assigned_for_pn_tn_wid(pn,tn,wid), id)

    async def delete_id_occupied_for_pn_tn(self, pn, tn, id):
        return await self.redis.execute("SREM", self.key_ids_occupied_for_pn_tn(pn,tn), id)


    async def get_ids_for_pn_tn(self, pn, tn):
        return await self.redis.execute_str("ZRANGE", self.key_ids_for_pn_tn(pn,tn), 0, -1)

    async def get_ids_assigned_for_pn_tn_wid(self, pn, tn, wid):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_assigned_for_pn_tn_wid(pn,tn,wid))

    async def get_ids_occupied_for_pn_tn_wid(self, pn, tn):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_occupied_for_pn_tn(pn,tn))

    async def get_first_id_for_pn_tn_wid(self, pn, tn, wid, assignment_order="bfs", sort_order="natural"):
        try:
            async with self.reserve_nanotask_lock:
                self.pool = self.pool if self.pool is not None else await self.redis.connect_for_blocking(3,10)
            while True:
                key_occupied = self.key_ids_occupied_for_pn_tn(pn,tn)

                with await self.pool as conn:
                    try:

                        tasks = []

                        # watch changes in ID set of occupied nanotasks for the template
                        tasks.append(asyncio.ensure_future(conn.execute("WATCH", key_occupied)))
                        tasks.append(asyncio.ensure_future(conn.execute("MULTI")))
                        # create *ID set of assignable nanotasks for the template and the worker* by
                        # (all nanotask IDs for the template) - (unavailable nanotask IDs for the template) - (already-assigned nanotask IDs for the template and the worker)
                        tasks.append(asyncio.ensure_future(conn.execute("ZUNIONSTORE",
                                                 self.key_ids_assignable_for_pn_tn_wid(pn,tn,wid), 3,
                                                 self.key_ids_for_pn_tn(pn,tn),
                                                 key_occupied,
                                                 self.key_ids_assigned_for_pn_tn_wid(pn,tn,wid),
                                                 "WEIGHTS", 1, 0, 0, "AGGREGATE", "MIN")))

                        # get the most prioritized (with top priority but LEAST # of assigned workers) nanotask ID(s) from the obtained ID set
                        get_first_bfs = '''
                            local ret = redis.call('ZRANGEBYSCORE', '{key_nids_assignable_for_pn_tn_wid}', 1, '+inf', 'WITHSCORES', 'LIMIT', 0, 1)
                            local nid = ret[1]
                            local priority = ret[2]
                            if nid == nil then
                                return nil
                            end
                        '''
                        # get the most prioritized (with top priority and most # of assigned workers) nanotask ID(s) from the obtained ID set
                        get_first_dfs = '''
                            local ret = redis.call('ZRANGEBYSCORE', '{key_nids_assignable_for_pn_tn_wid}', 1, '+inf', 'WITHSCORES', 'LIMIT', 0, 1)
                            local nid = ret[1]
                            local _priority = ret[2]
                            if nid == nil then
                                return nil
                            end

                            _priority = math.floor(_priority)
                            local ret = redis.call('ZREVRANGEBYSCORE', '{key_nids_assignable_for_pn_tn_wid}', '('..(_priority+1), _priority, 'WITHSCORES', 'LIMIT', 0, 1)
                            local nid = ret[1]
                            local priority = ret[2]

                        '''
                        # if there are more than one ID, get one of them randomly or in natural order
                        # count up # of assigned workers for the nanotask
                        # compare # of assignable workers and assigned workers;
                        # if no more workers can be assigned, mark the nanotask as unavailable
                        get_first_common = '''
                            local num_nids = redis.call('ZCOUNT', '{key_nids_assignable_for_pn_tn_wid}', priority, priority)
                            if num_nids > 1 then
                                local idx = 0
                                if '{sort_order}' == 'random' then
                                    math.randomseed({random_seed})
                                    idx = math.random(0, num_nids-1)
                                end
                                local ret = redis.call('ZRANGEBYSCORE', '{key_nids_assignable_for_pn_tn_wid}', priority, priority, 'LIMIT', idx, 1)
                                nid = ret[1]
                            end

                            redis.call('ZINCRBY', '{key_nids_for_pn_tn}', 1, nid)

                            local key_nt = string.gsub('{key_nt}', '%[%[nid%]%]', nid)
                            local key_wids_assigned_for_nid = string.gsub('{key_wids_assigned_for_nid}', '%[%[nid%]%]', nid)
                            local nt = redis.call('GET', key_nt)
                            local num_assignable = cjson.decode(nt)['NumAssignable']

                            -- self.add_id_assigned_for_pn_tn_wid
                            redis.call('SADD', '{key_nids_assigned_for_pn_tn_wid}', nid)
                            -- self.r_wkr.add_id_assigned_for_nid
                            redis.call('SADD', key_wids_assigned_for_nid, '{wid}')

                            local num_assigned = redis.call('SCARD', key_wids_assigned_for_nid)

                            if num_assignable <= num_assigned then
                                -- self.add_id_occupied_for_pn_tn
                                redis.call('SADD', '{key_nids_occupied_for_pn_tn}', nid)
                            end
                            
                            return nid
                        '''
                        
                        if assignment_order=="bfs":    get_first = get_first_bfs+get_first_common
                        elif assignment_order=="dfs":  get_first = get_first_dfs+get_first_common

                        get_first = get_first.format(wid=wid,
                                                     key_nids_assignable_for_pn_tn_wid=self.key_ids_assignable_for_pn_tn_wid(pn,tn,wid),
                                                     key_nids_for_pn_tn=self.key_ids_for_pn_tn(pn,tn),
                                                     key_nids_assigned_for_pn_tn_wid=self.key_ids_assigned_for_pn_tn_wid(pn,tn,wid),
                                                     key_nt=self.key(id="[[nid]]"),
                                                     key_wids_assigned_for_nid=self.r_wkr.key_ids_assigned_for_nid("[[nid]]"),
                                                     key_nids_occupied_for_pn_tn=self.key_ids_occupied_for_pn_tn(pn,tn),
                                                     random_seed=datetime.now().timestamp()+random.randint(0, random.randint(1, 100)),
                                                     sort_order=sort_order)

                        tasks.append(asyncio.ensure_future(conn.execute("EVAL", get_first, 0)))

                        tasks.append(asyncio.ensure_future(conn.execute("EXEC")))

                        ret = await asyncio.gather(*tasks)
                        ret = ret[-1]

                    except Exception as e:
                        logger.error("nanotask reservation failed", e)

                        try:     logger.error(ret)
                        except:  pass

                        await self.redis.execute("DISCARD")
                        return None

                    else:
                        if type(ret[1])==aioredis.WatchVariableError:
                            logger.warning("WatchVariableError: retrying nanotask reservation")
                            continue
                        else:
                            return ret[1]

        except Exception as e:
            logger.error("unexpected error happened for nanotask reservation", e)
            return None


    async def update_nanotask_assignability(self, id):
        nt = await self.get(id=id)
        pn = nt["ProjectName"]
        tn = nt["TemplateName"]
        query = '''
            local nt = redis.call('GET', '{key_nt}')
            local num_assignable = cjson.decode(nt)['NumAssignable']
            local num_assigned = redis.call('SCARD', '{key_wids_assigned_for_nid}')

            if num_assignable <= num_assigned then
                -- self.add_id_occupied_for_pn_tn
                redis.call('SADD', '{key_nids_occupied_for_pn_tn}', '{nid}')
            else
                -- self.delete_id_occupied_for_pn_tn
                redis.call('SREM', '{key_nids_occupied_for_pn_tn}', '{nid}')
            end
            
            return '{nid}'
        '''.format(nid=id,
                   key_nt=self.key(id=id),
                   key_wids_assigned_for_nid=self.r_wkr.key_ids_assigned_for_nid(id),
                   key_nids_occupied_for_pn_tn=self.key_ids_occupied_for_pn_tn(pn,tn))

        await self.redis.execute("EVAL", query, 0)

    async def check_id_exists_for_pn_tn(self, pn, tn):
        return (await self.redis.execute("EXISTS", self.key_ids_for_pn_tn(pn,tn)))==1


class WorkSessionResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "WorkSession", "WS")
        self.r_wkr = WorkerResource(redis)

    def key_id_for_pn_wid_ct(self,pn,wid,ct):  return f"WorkSessionId/PRJ:{pn}/{wid}/CT:{ct}"
    def key_ids_for_pn(self,pn):               return f"WorkSessionIds/PRJ:{pn}"

    @classmethod
    def create_instance(cls, pn, wid, ct, platform):
        return {
            "ProjectName": pn,
            "WorkerId": wid,
            "ClientToken": ct,
            "Platform": platform
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        wid = data["WorkerId"]
        ct = data["ClientToken"]
        await self.set_id_for_pn_wid_ct(pn, wid, ct, id)
        await self.add_id_for_pn(pn, id)
        await self.r_wkr.add_id_for_pn(pn, wid)

    async def add_id_for_pn(self, pn, id):
        await self.redis.execute("SADD", self.key_ids_for_pn(pn), id)

    async def get_ids_for_pn(self, pn):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_for_pn(pn))

    async def set_id_for_pn_wid_ct(self, pn, wid, ct, id):
        await self.redis.execute("SET", self.key_id_for_pn_wid_ct(pn,wid,ct), id)

    async def get_id_for_pn_wid_ct(self, pn, wid, ct):
        return await self.redis.execute_str("GET", self.key_id_for_pn_wid_ct(pn,wid,ct))


class NodeSessionResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "NodeSession", "NS")
        self.r_nt = NanotaskResource(redis)

    def key_ids_for_wsid(self,wsid):              return f"NodeSessionIds/{wsid}"
    def key_ids_for_pn_nn_wid(self,pn,nn,wid):    return f"NodeSessionIds/PRJ:{pn}/NODE:{nn}/{wid}"
    def key_ids_for_pn_nn_wsid(self,pn,nn,wsid):  return f"NodeSessionIds/PRJ:{pn}/NODE:{nn}/{wsid}"
    def key_ids_history_for_wsid(self,wsid):      return f"NodeSessionIdsHistory/{wsid}"

    @classmethod
    def create_instance(cls, pn, name, wid, wsid, prev_id, is_template, nid):
        return {
            "WorkerId": wid,
            "ProjectName": pn,
            "NodeName": name,
            "IsTemplateNode": is_template,
            "WorkSessionId": wsid,
            "NanotaskId": nid,
            "PrevId": prev_id,
            "NextId": None,
            "Expired": 0
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        nn = data["NodeName"]
        wid = data["WorkerId"]
        wsid = data["WorkSessionId"]
        await self.add_id_for_wsid(wsid, id)
        await self.add_id_for_pn_nn_wid(pn, nn, wid, id)
        await self.add_id_for_pn_nn_wsid(pn, nn, wsid, id)

        #if (nid := data["NanotaskId"]):  await self.r_nt.assign(pn, nn, wid, nid)

    async def add_id_for_wsid(self, wsid, id):
        await self.redis.execute("RPUSH", self.key_ids_for_wsid(wsid), id)
    async def add_id_to_history_for_wsid(self, wsid, id):
        await self.redis.execute("XADD", self.key_ids_history_for_wsid(wsid), "*", "NodeSessionId", id)
    async def add_id_for_pn_nn_wid(self, pn, nn, wid, id):
        await self.redis.execute("RPUSH", self.key_ids_for_pn_nn_wid(pn,nn,wid), id)
    async def add_id_for_pn_nn_wsid(self, pn, nn, wsid, id):
        await self.redis.execute("RPUSH", self.key_ids_for_pn_nn_wsid(pn,nn,wsid), id)

    async def get_ids_for_wsid(self, wsid):
        return await self.redis.execute_str("LRANGE", self.key_ids_for_wsid(wsid), 0, -1)
    async def get_ids_for_pn_nn_wid(self, pn, nn, wid):
        return await self.redis.execute_str("LRANGE", self.key_ids_for_pn_nn_wid(pn,nn,wid), 0, -1)
    async def get_ids_for_pn_nn_wsid(self, pn, nn, wsid):
        return await self.redis.execute_str("LRANGE", self.key_ids_for_pn_nn_wsid(pn,nn,wsid), 0, -1)

    async def get_id_for_wsid_by_index(self, wsid, idx):
        return await self.redis.execute_str("LINDEX", self.key_ids_for_wsid(wsid), idx)

    async def get_length_for_wsid(self, wsid):
        return await self.redis.execute("LLEN", self.key_ids_for_wsid(wsid))
    async def get_length_for_pn_nn_wid(self, pn, nn, wid):
        return await self.redis.execute("LLEN", self.key_ids_for_pn_nn_wid(pn,nn,wid))
    async def get_length_for_pn_nn_wsid(self, pn, nn, wsid):
        return await self.redis.execute("LLEN", self.key_ids_for_pn_nn_wsid(pn,nn,wsid))


    async def set_next_id(self, id, next_id):
        ns = await self.get(id)
        ns["NextId"] = next_id
        await self.update(id, ns)

    async def get_prev_id(self, id):
        ns = await self.get(id)
        return ns["PrevId"] if ns["PrevId"] else None
    async def get_next_id(self, id):
        ns = await self.get(id)
        return ns["NextId"] if ns["NextId"] else None

    async def set_expired(self, id):
        ns = await self.get(id)
        ns["Expired"] = 1
        await self.update(id, ns)

class ResponseResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Response", "NS")
        self.key_counter = None
        self.r_nt = NanotaskResource(redis)
        self.res_ns = NodeSessionResource(redis)

    def key_ids_for_nid(self,nid):      return f"ResponseIds/{nid}"
    def key_ids_for_pn_tn(self,pn,tn):  return f"ResponseIds/PRJ:{pn}/TMPL:{tn}"

    @classmethod
    def create_instance(cls, wsid, wid, nid, answer):
        return {
            "WorkSessionId": wsid,
            "WorkerId": wid,
            "NanotaskId": nid,
            "Answers": answer
        }

    def key(self, id=None):
        return f"{self.base_path}/{id}"

    async def next_count(self):
        pass

    async def add(self, nsid, data):
        data["Timestamp"] = datetime.now().timestamp()
        res = await self.redis.execute("SET", self.key(nsid), json.dumps(data))
        await self._on_add(nsid, data)

    async def _on_add(self, nsid, data):
        ns = await self.res_ns.get(nsid)
        wid = ns["WorkerId"]
        pn = ns["ProjectName"]
        tn = ns["NodeName"]
        wsid = ns["WorkSessionId"]
        nid = ns["NanotaskId"]
        if nid:
            await self.add_id_for_nid(nid, nsid)
            await self.r_nt.add_id_completed_for_pn_tn_wid(pn, tn, wid, nid)
        else:
            await self.add_id_for_pn_tn(pn, tn, nsid)
        
    async def add_id_for_nid(self, nid, id):
        await self.redis.execute("SADD", self.key_ids_for_nid(nid), id)

    async def add_id_for_pn_tn(self, pn, tn, id):
        await self.redis.execute("SADD", self.key_ids_for_pn_tn(pn,tn), id)

    async def get_ids_for_nid(self, nid):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_for_nid(nid))

    async def get_ids_for_pn_tn(self, pn, tn):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_for_pn_tn(pn,tn))

class MTurkResource:
    def __init__(self, redis):
        self.redis = redis

    def key_access_key_id(cls):      return "Platform/AMT/AccessKeyId"
    def key_secret_access_key(cls):  return "Platform/AMT/SecretAccessKey"
    def key_is_sandbox(cls):         return "Platform/AMT/IsSandbox"

    async def key_base(self):
        [aki, sak, sandbox] = await self.get_credentials()
        sandbox_str = "Sandbox" if sandbox==1 else "Production"
        return f"Platform/AMT/{aki}/{sandbox_str}"
    async def key_hits(self):
        return "{}/HITs".format(await self.key_base())
    async def key_hit_type_ids(self):
        return "{}/HITTypeIds".format(await self.key_base())
    async def key_hit_type_params_for_htid(self, htid):
        return "{}/HITTypeParams/{}".format(await self.key_base(), htid)
    async def key_hit_type_qualification_type_id_for_htid(self, htid):
        return "{}/QualificationTypeId/{}".format(await self.key_base(), htid)
    async def key_assignments(self):
        return "{}/Assignments".format(await self.key_base())
    async def key_hits_for_htid(self, HITTypeId):
        return "{}/HITsForHITType/{}".format(await self.key_base(), HITTypeId)

    async def get_access_key_id(self):
        return await self.redis.execute_str("GET", self.key_access_key_id())
    async def set_access_key_id(self, aki):
        return await self.redis.execute("SET", self.key_access_key_id(), aki)
    async def remove_access_key_id(self):
        return await self.redis.execute("DEL", self.key_access_key_id())
    async def get_secret_access_key(self):
        return await self.redis.execute_str("GET", self.key_secret_access_key())
    async def set_secret_access_key(self, sak):
        return await self.redis.execute("SET", self.key_secret_access_key(), sak)
    async def remove_secret_access_key(self):
        return await self.redis.execute("DEL", self.key_secret_access_key())
    async def get_is_sandbox(self):
        ret = await self.redis.execute_str("GET", self.key_is_sandbox())
        return ret=="1"
    async def set_is_sandbox(self, sandbox):
        val = 1 if sandbox==True else 0
        await self.redis.execute_str("SET", self.key_is_sandbox(), val)
    async def remove_is_sandbox(self):
        ret = await self.redis.execute("DEL", self.key_is_sandbox())
    async def get_credentials(self):
        return [
            await self.get_access_key_id(),
            await self.get_secret_access_key(),
            await self.get_is_sandbox()
        ]
    async def set_credentials(self, aki, sak, sandbox):
        await self.set_access_key_id(aki)
        await self.set_secret_access_key(sak)
        await self.set_is_sandbox(sandbox)
    async def remove_credentials(self):
        await self.remove_access_key_id()
        await self.remove_secret_access_key()
        await self.remove_is_sandbox()

    async def get_hit_type_ids(self):
        return await self.redis.execute_str("SMEMBERS", await self.key_hit_type_ids())

    async def get_hit_type_params_for_htid(self, htid):
        data = await self.redis.execute("GET", await self.key_hit_type_params_for_htid(htid))
        return json.loads(data) if data else None

    async def set_hit_type_params_for_htid(self, htid, params):
        timestamp = datetime.now().timestamp()
        data = {
            "Timestamp": timestamp,
            "Params": params
        }
        await self.redis.execute("SADD", await self.key_hit_type_ids(), htid)
        await self.redis.execute("SET", await self.key_hit_type_params_for_htid(htid), json.dumps(params))

    async def set_hit_type_qualification_type_id_for_htid(self, htid, qtid):
        await self.redis.execute("SET", await self.key_hit_type_qualification_type_id_for_htid(htid), qtid)

    async def get_hit_type_qualification_type_id_for_htid(self, htid):
        return await self.redis.execute_str("GET", await self.key_hit_type_qualification_type_id_for_htid(htid))

    async def get_hits(self):
        data = await self.redis.execute("GET", await self.key_hits())
        return json.loads(data) if data else None
        
    async def set_hits(self, hits):
        await self.redis.execute("SET", await self.key_hits(), json.dumps(hits))

    async def get_assignments(self):
        data = await self.redis.execute("GET", await self.key_assignments())
        return json.loads(data) if data else None
        
    async def set_assignments(self, data):
        await self.redis.execute("SET", await self.key_assignments(), json.dumps(data))

    async def get_hits_for_htid(self, HITTypeId):
        data = await self.redis.execute("GET", await self.key_hits_for_htid(HITTypeId))
        return json.loads(data) if data else None
    async def set_hits_for_htid(self, HITTypeId, HITs):
        await self.redis.execute("SET", await self.key_hits_for_htid(HITTypeId), json.dumps(HITs))
