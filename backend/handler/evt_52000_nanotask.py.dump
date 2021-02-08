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
        command = event.data["Command"]
        pn = event.data["ProjectName"]
        tn = event.data["TemplateName"]
        output.set("Command", command)
        output.set("ProjectName", pn)
        output.set("TemplateName", tn)

        if command=="Upload":
            tag = event.data["Data"]["Settings"]["TagName"]
            num_assignable = event.data["Data"]["Settings"]["NumAssignable"]
            priority = event.data["Data"]["Settings"]["Priority"]
            nanotasks = event.data["Data"]["Nanotasks"]
            for nt in nanotasks:
                _num_assignable = nt["NumAssignable"] if "NumAssignable" in nt else num_assignable
                _priority = nt["Priority"] if "Priority" in nt else priority
                _props = nt["Props"] if "Props" in nt else None
                _gt = nt["GroundTruths"] if "GroundTruths" in nt else None
                await self.r_nt.add(NanotaskResource.create_instance(pn=pn,
                                                                     tn=tn,
                                                                     tag=tag,
                                                                     num_assignable=_num_assignable,
                                                                     priority=_priority,
                                                                     gt=_gt,
                                                                     props=_props))
            output.set("NumInserted", len(nanotasks))

        elif command=="Get":
            nids = await self.r_nt.get_ids_for_pn_tn(pn, tn)
            data = [dict(NanotaskId=nid, **(await self.r_nt.get(nid))) for nid in nids]
            output.set("Nanotasks", data)
            output.set("Count", len(nids))

        elif command=="Delete":
            nids = event.data["NanotaskIds"]
            await self.r_nt.delete_multi(nids)
