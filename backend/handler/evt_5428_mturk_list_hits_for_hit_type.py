import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output
from handler.redis_resource import MTurkResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_mturk_api_hit_core = manager.get_handler_for(manager.key_ids["MTURK_API_HIT_CORE"])[1]
        self.r_mt = MTurkResource(manager.redis)
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if event.data and "HITTypeId" in event.data:
            htids = [event.data["HITTypeId"]]
        else:
            htids = await self.r_mt.get_hit_type_ids()
        tasks = [self.evt_mturk_api_hit_core.list_hits_for_hit_type(htid) for htid in htids]
        results = await asyncio.gather(*tasks)

        ret = {}
        for result in results:  ret = ret | result

        output.set("Results", { "HITTypes": ret })
