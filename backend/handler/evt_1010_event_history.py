import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output

import redis
r = redis.Redis(host="localhost", port=6379, db=0)

import logging
logger = logging.getLogger(__name__)


class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        #handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        history_size = 10
        if len(event.data)>1:   # update 
            eid = event.data[0]
            args = event.data[1:]

            event_key = self.namespace_redis.key_event_query(eid)

            count = r.zcount(event_key, 1, history_size)
            if count==history_size:
                r.zpopmin(event_key)
                keys = r.zrange(event_key, 0, -1)
                for key in keys:  r.zincrby(event_key, -1, key)
            d = {}
            d[" ".join(args)] = min(count+1, history_size)
            ret = r.zadd(event_key, d)

            output.set("EventId", eid)
            output.set("History", [h.decode() for h in r.zrange(event_key, 0, -1)])
        else:  # get all
            event_keys = r.keys(self.namespace_redis.key_event_query("*"))
            output.set("AllHistory", {ekey.split("/")[1]:[h.decode() for h in r.zrange(ekey, 0, -1)] for ekey in event_keys})
