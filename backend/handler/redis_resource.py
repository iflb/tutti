import json
import handler.redis_index as ri
from datetime import datetime
import aioredis

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

    async def next_count(self):
        return await self.redis.execute("INCR", self.key_counter)

    async def add(self, data):
        cnt = await self.next_count()
        id = self.id(cnt=cnt)
        data["Timestamp"] = datetime.now().timestamp()
        res = await self.redis.execute("JSON.SET", self.key(id=id), ".", json.dumps(data))
        await self._on_add(id, data)
        return id

    async def update(self, id, data):
        await self.redis.execute("JSON.SET", self.key(id=id), ".", json.dumps(data))
        await self._on_update(id, data)

    async def get(self, id):
        data = await self.redis.execute("JSON.GET", self.key(id=id))
        return json.loads(data) if data else None

    async def _delete(self, id):
        data = await self.get(id)
        await self.redis.execute("JSON.DEL", self.key(id=id))
        return data

    async def delete(self, id):
        data = await self._delete(id)
        await self._on_delete(id, data)

    async def delete_multi(self, ids):
        data = [await self._delete(id) for id in ids]
        await self._on_delete_multi(ids, data)

    async def _get_by_json_path(self, id, path):
        data = await self.redis.execute("JSON.GET", self.key(id=id), path)
        return json.loads(data) if data else None

    async def _on_add(self, id, data):
        pass

    async def _on_update(self, id, data):
        pass

    async def _on_delete(self, id, data):
        pass

    async def _on_delete_multi(self, ids, data):
        pass

class NanotaskResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Nanotask", "NT")

    @classmethod
    def create_instance(cls, pn, tn, tag, num_assignable, priority, gt, props):
        return {
            "ProjectName": pn,
            "TemplateName": tn,
            "Tag": tag,
            "NumAssignable": num_assignable,
            "Priority": priority,
            "GroundTruths": gt,
            "Props": props
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        tn = data["TemplateName"]
        priority = data["Priority"]

        await self.add_id_for_pn_tn(pn, tn, priority, id)

    async def _on_delete(self, id, data):
        pn = data["ProjectName"]
        tn = data["TemplateName"]

        await self.delete_ids_for_pn_tn(pn, tn, id)

    async def _on_delete_multi(self, ids, data):
        pn = data[0]["ProjectName"]
        tn = data[0]["TemplateName"]

        await self.delete_ids_for_pn_tn(pn, tn, *ids)
        
    async def add_id_for_pn_tn(self, pn, tn, priority, id):
        await self.redis.execute("ZADD", ri.key_nids_for_pn_tn(pn,tn), priority, id)

    async def delete_ids_for_pn_tn(self, pn, tn, *ids):
        await self.redis.execute("ZREM", ri.key_nids_for_pn_tn(pn,tn), *ids)

    async def check_id_exists_for_pn_tn(self, pn, tn):
        return (await self.redis.execute("EXISTS", ri.key_nids_for_pn_tn(pn,tn)))==1

    async def get_ids_for_pn_tn(self, pn, tn):
        return await self.redis.execute_str("ZRANGE", ri.key_nids_for_pn_tn(pn,tn), 0, -1)

    async def get_first_id_for_pn_tn_wid(self, pn, tn, wid, assignment_order="bfs", sort_order="natural"):
        while True:
            await self.redis.execute("WATCH", ri.key_completed_nids_for_pn_tn(pn,tn))
            await self.redis.execute("MULTI")
            await self.redis.execute("ZUNIONSTORE",
                                     ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), 3,
                                     ri.key_nids_for_pn_tn(pn,tn),
                                     ri.key_completed_nids_for_pn_tn(pn,tn),
                                     ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid),
                                     "WEIGHTS", 1, 0, 0, "AGGREGATE", "MIN")
            get_first_bfs = '''
                local ret = redis.call('ZRANGEBYSCORE', KEYS[1], 1, '+inf', 'WITHSCORES', 'LIMIT', 0, 1)
                local item = ret[1]
                local score = ret[2]

            '''
            
            get_first_dfs = '''
                local ret = redis.call('ZRANGEBYSCORE', KEYS[1], 1, '+inf', 'WITHSCORES', 'LIMIT', 0, 1)
                local _item = ret[1]
                local _score = ret[2]
                _score = math.floor(_score)
                
                local ret = redis.call('ZREVRANGEBYSCORE', KEYS[1], '('..(_score+1), _score, 'WITHSCORES', 'LIMIT', 0, 1)
                local item = ret[1]
                local score = ret[2]

            '''
            
            get_first_common = '''
                local num = redis.call('ZCOUNT', KEYS[1], score, score)
                if num > 1 then
                    local offset = 0
                    if ARGV[2] == 'random' then
                        math.randomseed(ARGV[1])
                        offset = math.random(0, num-1)
                    end
                    local ret = redis.call('ZRANGEBYSCORE', KEYS[1], score, score, 'LIMIT', offset, 1)
                    item = ret[1]
                end

                redis.call('ZINCRBY', KEYS[2], 0.000001, item)
                return item
            '''
            
            if assignment_order=="bfs":
                get_first = get_first_bfs+get_first_common
            elif assignment_order=="dfs":
                get_first = get_first_dfs+get_first_common
            
            await self.redis.execute("EVAL", get_first, 2, ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), ri.key_nids_for_pn_tn(pn,tn), datetime.now().timestamp()+random.randint(0, random.randint(1, 100)), sort_order)

            ret = await self.redis.execute_str("EXEC")

            if type(ret[1])==aioredis.WatchVariableError:  continue
            else:  break
        return ret[1].decode() if ret[1] else None


class WorkSessionResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "WorkSession", "WS")

    @classmethod
    def create_instance(cls, pn, wid, ct):
        return {
            "ProjectName": pn,
            "WorkerId": wid,
            "ClientToken": ct
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        wid = data["WorkerId"]
        ct = data["ClientToken"]
        await self.set_id_for_pn_wid_ct(pn, wid, ct, id)
        await self.add_wid_for_pn(pn, wid)

    async def set_id_for_pn_wid_ct(self, pn, wid, ct, id):
        await self.redis.execute("SET", ri.key_wsids_for_pn_wid_ct(pn,wid,ct), id)
    async def get_id_for_pn_wid_ct(self, pn, wid, ct):
        return await self.redis.execute_str("GET", ri.key_wsids_for_pn_wid_ct(pn,wid,ct))

    async def add_wid_for_pn(self, pn, wid):
        await self.redis.execute("SADD", ri.key_wids_for_pn(pn), wid)

class NodeSessionResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "NodeSession", "NS")

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
        }

    async def _on_add(self, id, data):
        await self.add_id_for_wsid(data["WorkSessionId"], id)
        await self.add_id_for_pn_nn_wid(data["ProjectName"], data["NodeName"], data["WorkerId"], id)
        await self.add_id_for_pn_nn_wsid(data["ProjectName"], data["NodeName"], data["WorkSessionId"], id)

    async def add_id_for_wsid(self, wsid, id):
        await self.redis.execute("RPUSH", ri.key_nsids_for_wsid(wsid), id)
    async def add_id_for_pn_nn_wid(self, pn, nn, wid, id):
        await self.redis.execute("RPUSH", ri.key_nsids_for_pn_nn_wid(pn,nn,wid), id)
    async def add_id_for_pn_nn_wsid(self, pn, nn, wsid, id):
        await self.redis.execute("RPUSH", ri.key_nsids_for_pn_nn_wsid(pn,nn,wsid), id)

    async def get_ids_for_wsid(self, wsid):
        return await self.redis.execute_str("LRANGE", ri.key_nsids_for_wsid(wsid), 0, -1)
    async def get_ids_for_pn_nn_wid(self, pn, nn, wid):
        return await self.redis.execute_str("LRANGE", ri.key_nsids_for_pn_nn_wid(pn,nn,wid), 0, -1)
    async def get_ids_for_pn_nn_wsid(self, pn, nn, wsid):
        return await self.redis.execute_str("LRANGE", ri.key_nsids_for_pn_nn_wsid(pn,nn,wsid), 0, -1)

    async def get_id_for_wsid_by_index(self, wsid, idx):
        return await self.redis.execute_str("LINDEX", ri.key_nsids_for_wsid(wsid), idx)

    async def get_length_for_wsid(self, wsid):
        return await self.redis.execute("LLEN", ri.key_nsids_for_wsid(wsid))
    async def get_length_for_pn_nn_wid(self, pn, nn, wid):
        return await self.redis.execute("LLEN", ri.key_nsids_for_pn_nn_wid(pn,nn,wid))
    async def get_length_for_pn_nn_wsid(self, pn, nn, wsid):
        return await self.redis.execute("LLEN", ri.key_nsids_for_pn_nn_wsid(pn,nn,wsid))


    async def set_next_id(self, id, next_id):
        await self.redis.execute("JSON.SET", self.key(id=id), "NextId", next_id)

    async def get_prev_id(self, id):
        return await self._get_by_json_path(id, "PrevId")
    async def get_next_id(self, id):
        return await self._get_by_json_path(id, "NextId")

class AnswerResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Answer", "NS")
        self.key_counter = None
        self.res_nt = NanotaskResource(redis)
        self.res_ns = NodeSessionResource(redis)

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
        res = await self.redis.execute("JSON.SET", self.key(nsid), ".", json.dumps(data))
        await self._on_add(nsid, data)

    async def _on_add(self, nsid, data):
        ns = await self.res_ns.get(nsid)
        wid = ns["WorkerId"]
        pn = ns["ProjectName"]
        tn = ns["NodeName"]
        wsid = ns["WorkSessionId"]
        nid = ns["NanotaskId"]
        if nid: await self.add_id_for_nid(nid, nsid)
        else:   await self.add_id_for_pn_tn(pn, tn, nsid)

        if nid:
            nt = await self.res_nt.get(nid)
            num_assignable = nt["NumAssignable"]
            answers = await self.get_ids_for_nid(nid)
            await self.add_completed_nid_for_pn_tn_wid(pn, tn, wid, nid)
            if num_assignable<=len(answers):
                await self.add_completed_nid_for_pn_tn(pn, tn, nid)
        
    async def add_completed_nid_for_pn_tn_wid(self, pn, tn, wid, nid):
        await self.redis.execute("SADD", ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid), nid)

    async def add_completed_nid_for_pn_tn(self, pn, tn, nid):
        await self.redis.execute("SADD", ri.key_completed_nids_for_pn_tn(pn,tn), nid)

    async def add_id_for_nid(self, nid, id):
        await self.redis.execute("SADD", ri.key_aids_for_nid(nid), id)

    async def add_id_for_pn_tn(self, pn, tn, id):
        await self.redis.execute("SADD", ri.key_aids_for_pn_tn(pn,tn), id)

    async def get_ids_for_nid(self, nid):
        return await self.redis.execute_str("SMEMBERS", ri.key_aids_for_nid(nid))

    async def get_ids_for_pn_tn(self, pn, tn):
        return await self.redis.execute_str("SMEMBERS", ri.key_aids_for_pn_tn(pn,tn))

class MTurkResource:
    def __init__(self, redis):
        self.redis = redis

    @classmethod
    def key_access_key_id(cls):
        return f"Platform/AMT/AccessKeyId"
    @classmethod
    def key_secret_access_key(cls):
        return f"Platform/AMT/SecretAccessKey"
    @classmethod
    def key_is_sandbox(cls):
        return f"Platform/AMT/IsSandbox"

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
        data = await self.redis.execute("JSON.GET", await self.key_hit_type_params_for_htid(htid))
        return json.loads(data) if data else None

    async def set_hit_type_params_for_htid(self, htid, params):
        timestamp = datetime.now().timestamp()
        data = {
            "Timestamp": timestamp,
            "Params": params
        }
        await self.redis.execute("SADD", await self.key_hit_type_ids(), htid)
        await self.redis.execute("JSON.SET", await self.key_hit_type_params_for_htid(htid), ".", json.dumps(params))

    async def get_hits(self):
        data = await self.redis.execute("JSON.GET", await self.key_hits())
        return json.loads(data) if data else None
        
    async def set_hits(self, hits):
        await self.redis.execute("JSON.SET", await self.key_hits(), ".", json.dumps(hits))

class WorkerHelper:
    @classmethod
    async def get_wids_for_pn(cls, redis, pn):
        return await redis.execute_str("SMEMBERS", ri.key_wids_for_pn(pn))

    @classmethod
    async def get_amt_wids_for_pn(cls, redis, pn):
        wids = await redis.execute_str("SMEMBERS", ri.key_wids_for_pn(pn))
        return [wid for wid in wids if wid.startswith("A") and wid.isupper()]
