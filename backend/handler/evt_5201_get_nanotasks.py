from ducts.event import EventHandler
from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

from handler.redis_resource import NanotaskResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_nt = NanotaskResource(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        [command, pn, tn] = event.data
        output.set("Command", command)
        output.set("Project", pn)
        output.set("Template", tn)

        nids = await self.r_nt.get_ids_for_pn_tn(pn, tn)

        if command=="NANOTASKS":
            data = [await self.r_nt.get(nid) for nid in nids]
            output.set("Nanotasks", data)

        elif command=="COUNT":
            output.set("Count", len(nids))
