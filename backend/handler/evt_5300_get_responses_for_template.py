import time
import os

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

from handler.redis_resource import NanotaskResource, NodeSessionResource, ResponseResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_resp = ResponseResource(manager.redis)
        self.r_nt = NanotaskResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("Responses", await self.get_responses_for_template(**event.data))

    async def get_responses_for_template(self, ProjectName, TemplateName):
        aids = await self.r_resp.get_ids_for_pn_tn(ProjectName, TemplateName)
        nids = await self.r_nt.get_ids_for_pn_tn(ProjectName, TemplateName)
        if nids:  [aids.extend(await self.r_resp.get_ids_for_nid(nid)) for nid in nids]

        return [await self.r_resp.get(aid) for aid in aids]
