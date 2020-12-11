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
            for (props,gt) in zip(event.data["Props"],event.data["GroundTruths"]):
                await self.r_nt.add(NanotaskResource.create_instance(pn=pn,
                                                                     tn=tn,
                                                                     tag=event.data["Tag"],
                                                                     num_assignable=event.data["NumAssignable"],
                                                                     priority=event.data["Priority"],
                                                                     gt=gt,
                                                                     props=props))
            output.set("NumInserted", len(event.data["Props"]))
        elif command=="Get":
            nids = await self.r_nt.get_ids_for_pn_tn(pn, tn)
            data = [await self.r_nt.get(nid) for nid in nids]
            output.set("Nanotasks", data)
            output.set("Count", len(nids))
