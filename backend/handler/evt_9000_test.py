import asyncio
import aioredis
from ducts.event import EventHandler

import handler.redis_index as ri

class Handler(EventHandler):
    async def setup(self, handler_spec, manager):
        #pn = "test0812"
        #tn = "main4"
        #wid = "fff"
        #redis = manager.redis
        #while True:
        #    await redis.execute("WATCH", ri.key_completed_nids_for_pn_tn(pn,tn))
        #    await redis.execute("MULTI")
        #    await redis.execute("ZUNIONSTORE",
        #                             ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), 3,
        #                             ri.key_nids_for_pn_tn(pn,tn),
        #                             ri.key_completed_nids_for_pn_tn(pn,tn),
        #                             ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid),
        #                             "WEIGHTS", 1, 0, 0, "AGGREGATE", "MIN")
        #    await redis.execute_str("ZRANGEBYSCORE",
        #                                   ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid),
        #                                   1, "+inf", "LIMIT", 0, 1)
        #    print("sleeping")
        #    await asyncio.sleep(5)
        #    ret = await redis.execute("EXEC")
        #    if type(ret[1])==aioredis.WatchVariableError:
        #        print("watchvariableerror")
        #        continue
        #    else:
        #        break
        #print(ret)
        pass

    async def handle(self, event, output):
        pass
