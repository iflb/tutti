import random
import asyncio
import aioredis
from datetime import datetime
from ducts.event import EventHandler

import handler.redis_index as ri

class Handler(EventHandler):
    async def setup(self, handler_spec, manager):
        return


        redis = manager.redis
        pn = "test0812"
        tn = "main4"
        wid = "fff"
        assignment_order = "dfs"
        sort_order = "random"

        for i in range(10):
            await redis.execute("WATCH", ri.key_completed_nids_for_pn_tn(pn,tn))
            await redis.execute("MULTI")
            await redis.execute("ZUNIONSTORE",
                                     ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), 3,
                                     ri.key_nids_for_pn_tn(pn,tn),
                                     ri.key_completed_nids_for_pn_tn(pn,tn),
                                     ri.key_completed_nids_for_pn_tn_wid(pn,tn,wid),
                                     "WEIGHTS", 1, 0, 0, "AGGREGATE", "MIN")
            print("sleeping")
            await asyncio.sleep(10)
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
                if num == 1 then
                    return item
                else
                    local offset = 0
                    if ARGV[2] == 'random' then
                        math.randomseed(ARGV[1])
                        offset = math.random(0, num-1)
                    end
                    local ret = redis.call('ZRANGEBYSCORE', KEYS[1], score, score, 'LIMIT', offset, 1)
                    return ret[1]
                end
            '''
            
            if assignment_order=="bfs":
                get_first = get_first_bfs+get_first_common
            elif assignment_order=="dfs":
                get_first = get_first_dfs+get_first_common
            
            await redis.execute("EVAL", get_first, 1, ri.key_assignable_nids_for_pn_tn_wid(pn,tn,wid), datetime.now().timestamp()+random.randint(0, random.randint(1, 100)), sort_order)
            ret = await redis.execute_str("EXEC")

            print(ret)  

    async def handle(self, event, output):
        pass
