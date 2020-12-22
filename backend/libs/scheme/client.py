import json
from handler.redis_resource import NodeSessionResource

class ClientBase:
    def __init__(self, redis, resource, id, pn):
        self.id = id
        self.redis = redis
        self.new_members = {}
        self.resource = resource
        self.pn = pn
        self.members = {}
        self._cnt = {}
        self._path_member_names = f"{self.resource}Client/{self.id}/ClientMeta/MemberNames"
        self.r_ns = NodeSessionResource(redis)

    def _path_member(self, name):  return f"{self.resource}Client/{self.id}/ClientMeta/Members/{name}"

    async def _load_for_read(self, flow):
        await self._load_cnt(flow)
        await self._load_members()
        return self

    async def _load_cnt(self, flow):
        pass

    async def _load_members(self):
        member_names = await self.redis.execute_str("SMEMBERS", self._path_member_names)
        self.members = {name: await self.redis.execute_str("LRANGE", self._path_member(name), 0, -1) for name in member_names}

    def _get_new_members(self):
        return self.new_members

    async def _register_new_members_to_redis(self):
        if self.new_members.keys():
            await self.redis.execute("SADD", self._path_member_names, *self.new_members.keys())
            for name,values in self.new_members.items():  await self.redis.execute("RPUSH", self._path_member(name), *values)




    def get_member(self, name):
        return self.members[name] if name in self.members else []

    def cnt(self, node_name):
        return self._cnt[node_name]

    def add_member(self, name, value):
        if name not in self.new_members:  self.new_members[name] = []
        self.new_members[name].append(value)

class WorkerClient(ClientBase):
    def __init__(self, redis, id, pn):
        super().__init__(redis, "Worker", id, pn)

    async def _load_cnt(self, flow):
        nns = flow.get_all_node_names()
        self._cnt = {nn: await self.r_ns.get_length_for_pn_nn_wid(self.pn, nn, self.id) for nn in nns}

class WorkSessionClient(ClientBase):
    def __init__(self, redis, id, pn):
        super().__init__(redis, "WorkSession", id, pn)

    async def _load_cnt(self, flow):
        nns = flow.get_all_node_names()
        self._cnt = {nn: await self.r_ns.get_length_for_pn_nn_wsid(self.pn, nn, self.id) for nn in nns}
