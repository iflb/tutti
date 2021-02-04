from ducts.event import EventHandler
import asyncio

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
        pass

    async def upload_nanotasks(self, ProjectName, TemplateName, Nanotasks, TagName=None, NumAssignable=None, Priority=None):
        tasks = []
        for nt in Nanotasks:
            _num_assignable = nt["NumAssignable"] if "NumAssignable" in nt else NumAssignable
            _priority = nt["Priority"] if "Priority" in nt else Priority
            _props = nt["Props"] if "Props" in nt else None
            _gt = nt["GroundTruths"] if "GroundTruths" in nt else None
            params = {
                "pn": ProjectName,
                "tn": TemplateName,
                "tag": TagName, 
                "num_assignable": _num_assignable,
                "priority": _priority,
                "gt": _gt,
                "props": _props
            }
            tasks.append(self.r_nt.add(NanotaskResource.create_instance(**params)))
        await asyncio.gather(*tasks)

    async def get_nanotasks(self, ProjectName, TemplateName):
        nids = await self.r_nt.get_ids_for_pn_tn(ProjectName, TemplateName)
        ret = await asyncio.gather(*[self.r_nt.get(nid) for nid in nids])
        return [dict(NanotaskId=nid, **r) for (nid,r) in zip(nids, ret)]

    async def delete_nanotasks(self, NanotaskIds):
        await self.r_nt.delete_multi(NanotaskIds)

    async def update_nanotask_num_assignable(self, NanotaskId, NumAssignable):
        nt = await self.r_nt.get(NanotaskId)
        nt["NumAssignable"] = NumAssignable
        await self.r_nt.update(NanotaskId, nt)

    async def update_nanotask_assignability_status(self, NanotaskId):
        await self.r_nt.update_nanotask_assignability(NanotaskId)
