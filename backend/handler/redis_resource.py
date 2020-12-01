import json
import handler.redis_index as ri

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
        res = await self.redis.execute("JSON.SET", self.key(id=id), ".", json.dumps(data))
        await self._on_add(id, data)
        return id

    async def get(self, id):
        data = await self.redis.execute("JSON.GET", self.key(id=id))
        return json.loads(data) if data else None

    async def _get_by_json_path(self, id, path):
        data = await self.redis.execute("JSON.GET", self.key(id=id), path)
        return json.loads(data) if data else None

    async def _on_add(self, id, data):
        pass

class NanotaskResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "Nanotask", "NT")

    @classmethod
    def create_instance(cls, pn, tn, tag, num_assignable, priority, props):
        return {
            "ProjectName": pn,
            "TemplateName": tn,
            "Tag": tag,
            "NumAssignable": num_assignable,
            "Priority": priority,
            "Props": props
        }

    async def _on_add(self, id, data):
        pn = data["ProjectName"]
        tn = data["TemplateName"]

        await self.add_id_for_pn_tn(pn, tn, id)
        
    async def add_id_for_pn_tn(self, pn, tn, priority, id):
        await self.redis.execute("ZADD", ri.key_nids_for_pn_tn(pn,tn), priority, id)

    async def get_ids_for_pn_tn(self, pn, tn):
        return await self.redis.execute_str("ZRANGE", ri.key_nids_for_pn_tn(pn,tn), 0, -1)

    async def get_first_id_for_pn_tn_wid(self, pn, tn, wid):
        await self.redis.execute("ZUNIONSTORE",
                                 ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), 3,
                                 ri.key_nids_for_pn_tn(pn,tn),
                                 ri.key_completed_nids_for_pn_tn(pn,tn),
                                 ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid),
                                 "WEIGHTS", 1, 0, 0, "AGGREGATE", "MIN")
        ret = await self.redis.execute_str("ZRANGEBYSCORE",
                                       ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid),
                                       1, "+inf", "LIMIT", 0, 1)
        return ret


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

    async def set_id_for_pn_wid_ct(self, pn, wid, ct, id):
        await self.redis.execute("SET", ri.key_wsid_for_pn_wid_ct(pn,wid,ct), id)

    async def get_id_for_pn_wid_ct(self, pn, wid, ct):
        return await self.redis.execute_str("GET", ri.key_wsid_for_pn_wid_ct(pn,wid,ct))

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
        wsid = data["WorkSessionId"]
        await self.add_id_for_wsid(wsid, id)

    async def add_id_for_wsid(self, wsid, id):
        await self.redis.execute("RPUSH", ri.key_nsid_list_for_wsid(wsid), id)
    async def get_id_for_wsid_by_index(self, wsid, idx):
        return await self.redis.execute_str("LINDEX", ri.key_nsid_list_for_wsid(wsid), idx)
    async def get_length_for_wsid(self, wsid):
        return await self.redis.execute("LLEN", ri.key_nsid_list_for_wsid(wsid))
    async def get_ids_for_wsid(self, wsid):
        return json.loads(await self.redis.execute("LRANGE", ri.key_nsid_list_for_wsid(wsid), 0, -1))
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
    def create_instance(cls, answer):
        return answer

    def key(self, id=None):
        return f"{self.base_path}/{id}"

    async def next_count(self):
        pass

    async def add(self, nsid, data):
        res = await self.redis.execute("JSON.SET", self.key(nsid), ".", json.dumps(data))
        await self._on_add(nsid, data)

    async def _on_add(self, nsid, data):
        ns = await self.res_ns.get(nsid)
        wid = ns["WorkerId"]
        pn = ns["ProjectName"]
        tn = ns["NodeName"]
        nid = ns["NanotaskId"]
        if nid:  await self.add_id_for_nid(nid, nsid)
        else:    await self.add_id_for_tn(tn, nsid)

        if nid:
            nt = await self.res_nt.get(nid)
            num_assignable = nt["NumAssignable"]
            answers = await self.get_ids_for_nid(nid)
            await self.add_completed_nid_for_pn_tn_wid(pn, tn, wid, nid)
            if num_assignable<=len(answers):
                await self.add_completed_nid_for_pn_tn(pn, tn, nid)
        
    async def add_completed_nid_for_pn_tn_wid(self, pn, tn, wid, nid):
        await redis.execute("SADD", ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid), nid)

    async def add_completed_nid_for_pn_tn(self, pn, tn, nid):
        await redis.execute("SADD", ri.key_completed_nids_for_pn_tn(pn,tn), nid)

    async def add_id_for_nid(self, nid, id):
        await self.redis.execute("SADD", ri.key_aids_for_nid(nid), id)

    async def add_id_for_tn(self, tn, id):
        await self.redis.execute("SADD", ri.key_aids_for_tn(tn), id)

    async def get_ids_for_nid(self, nid):
        return await self.redis.execute_str("SMEMBERS", ri.key_aids_for_nid(nid))

    async def get_ids_for_tn(self, tn):
        return await self.redis.execute_str("SMEMBERS", ri.key_aids_for_tn(tn))
