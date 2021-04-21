import json
import msgpack
import pickle

from handler.redis_resource import (NodeSessionResource, WorkerResource)

class ContextBase:
    def __init__(self, redis, resource, id, pn):
        self._new_attrs = {}
        self._new_attrs_obj = {}
        self._cnt = {}

        self.redis = redis
        self.resource = resource
        self.id = id
        self.pn = pn

        self._path_attrs = f"{self.resource}Context/{pn}/{self.id}/Attributes"
        self.r_ns = NodeSessionResource(redis)

    async def _load_for_read(self, flow):
        await self._load_cnt(flow)
        #await self._load_members()
        await self._load_attrs()
        return self

    async def _load_cnt(self, flow):
        pass

    async def _load_attrs(self):
        attrs = {}
        key = ""
        for i,val in enumerate(await self.redis.execute("HGETALL", self._path_attrs)):
            if i%2==0:
                key = val.decode()
                attrs[val] = None
            else:
                attrs[key] = val
        self.attrs = attrs

    async def _register_new_attrs_to_redis(self):
        for (fmt,attrs) in [ (msgpack, self._new_attrs), (pickle, self._new_attrs_obj) ]:
            if attrs.keys():
                for name,values in attrs.items():
                    await self.redis.execute("HSET", self._path_attrs, name, fmt.dumps(values))
                    self.attrs[name] = fmt.dumps(values)

    def get_id(self):
        return int(self.id[-8:])

    def cnt(self, node_name):
        return self._cnt[node_name]

    def set_attr(self, name, value):
        if name not in self._new_attrs:  self._new_attrs[name] = []
        self._new_attrs[name].append(value)

    def set_attr_obj(self, name, value):
        if name not in self._new_attrs_obj:  self._new_attrs_obj[name] = []
        self._new_attrs_obj[name].append(value)

    def get_attr(self, name):
        return msgpack.loads(self.attrs[name])[0] if name in self.attrs else None

    def get_attr_obj(self, name):
        return pickle.loads(self.attrs[name])[0] if name in self.attrs else None

class WorkerContext(ContextBase):
    def __init__(self, redis, id, pn):
        super().__init__(redis, "Worker", id, pn)
        self.r_wkr = WorkerResource(redis)

    async def _load_cnt(self, flow):
        nns = flow.get_all_node_names()
        self._cnt = {nn: await self.r_ns.get_length_for_pn_nn_wid(self.pn, nn, self.id) for nn in nns}

    async def _load_for_read(self, flow):
        await super()._load_for_read(flow)
        self.prj_id = await self.r_wkr.get_prj_id(self.pn, self.id)
        return self

    def get_prj_id(self):
        return self.prj_id

class WorkSessionContext(ContextBase):
    def __init__(self, redis, id, pn):
        super().__init__(redis, "WorkSession", id, pn)

    async def _load_cnt(self, flow):
        nns = flow.get_all_node_names()
        self._cnt = {nn: await self.r_ns.get_length_for_pn_nn_wsid(self.pn, nn, self.id) for nn in nns}
