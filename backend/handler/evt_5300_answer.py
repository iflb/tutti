import time
import os

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

from handler.redis_resource import NanotaskResource, NodeSessionResource, AnswerResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_ans = AnswerResource(manager.redis)
        self.r_nt = NanotaskResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        command = event.data["Command"]
        output.set("Command", command)

        if command=="Get":
            pn = event.data["ProjectName"]
            tn = event.data["TemplateName"]
            aids = await self.r_ans.get_ids_for_pn_tn(pn, tn)
            nids = await self.r_nt.get_ids_for_pn_tn(pn, tn)
            if nids:  [aids.extend(await self.r_ans.get_ids_for_nid(nid)) for nid in nids]

            answers = [await self.r_ans.get(aid) for aid in aids]
            print(answers)
            output.set("Answers", answers)

        elif command=="Set":
            if not event.data["NodeSessionId"]:  raise Exception(f"node session ID cannot be null")

            wsid = event.data["WorkSessionId"]
            nsid = event.data["NodeSessionId"]

            ns = await self.r_ns.get(nsid)
            wid = ns["WorkerId"]
            nid = ns["NanotaskId"]

            answer = AnswerResource.create_instance(wsid, wid, nid, event.data["Answer"])
            await self.r_ans.add(nsid, answer)
            output.set("SentAnswer", answer)

        else:
            raise Exception("unknown command '{}'".format(command))
