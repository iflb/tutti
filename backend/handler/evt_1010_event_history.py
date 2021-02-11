import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output

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
        self.redis = event.session.redis

        history_size = 10
        if event.data and len(event.data)>1:   # update 
            eid = event.data[0]
            args = event.data[1:]

            event_key = self.namespace_redis.key_event_query(eid)
            query = " ".join(args)

            if query!="" and query!="null":
                cnt = await self.redis.execute("LLEN", event_key)
                lremcnt = await self.redis.execute("LREM", event_key, 1, query)
                if cnt==history_size:  await self.redis.execute("LPOP", event_key)
                await self.redis.execute("RPUSH", event_key, query)

            output.set("EventId", eid)
            output.set("History", [h.decode() for h in await self.redis.execute("LRANGE", event_key, 0, -1)])
        else:  # get all
            event_keys = await self.redis.execute("KEYS", self.namespace_redis.key_event_query("*"))
            output.set("AllHistory", {ekey.decode().split("/")[1]:[h.decode() for h in await self.redis.execute("LRANGE", ekey, 0, -1)] for ekey in event_keys})
