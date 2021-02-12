from ducts.event import EventHandler

from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

from handler.redis_resource import NodeSessionResource, WorkSessionResource, NanotaskResource, ResponseResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_ws = WorkSessionResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)
        self.r_nt = NanotaskResource(manager.redis)
        self.r_resp = ResponseResource(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        await self.unassign_abandoned_nanotasks_for_project(**event.data)

    async def unassign_abandoned_nanotasks_for_project(self, ProjectName):
        wsids = await self.r_ws.get_ids_for_pn(ProjectName)
        nsids = []
        [nsids.extend(await self.r_ns.get_ids_for_wsid(wsid)) for wsid in wsids]
        for nsid in nsids:
            ns = await self.r_ns.get(nsid)
            if ns["NanotaskId"]:
                if not (response := await self.r_resp.get(nsid)):  await self.r_nt.unassign(ProjectName,ns["NodeName"],ns["WorkerId"],ns["NanotaskId"])
            else:
                continue
