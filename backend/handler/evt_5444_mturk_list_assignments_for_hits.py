import asyncio
from datetime import datetime

from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler import paths, common
from handler.handler_output import handler_output, CommandError
from handler.redis_resource import (WorkSessionResource,
                                    WorkerResource)

sem_limit = 10

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]
        self.evt_mturk_api_hit_core = manager.get_handler_for(manager.key_ids["MTURK_API_HIT_CORE"])[1]
        self.r_ws = WorkSessionResource(manager.redis)
        self.r_wkr = WorkerResource(manager.redis)
        handler_spec.set_description('Creates a QualificationType.')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("Assignments", await self.list_assignments_for_hits(**event.data))

    async def list_assignments_for_hits(self, HITIds):
        #if Cached and (assignments := await self.evt_mturk_api_core.cache_get_assignments_list()):
        #    return assignments

        #else:
            sem = asyncio.Semaphore(sem_limit)
            async def _list_assignments_for_hit(hit_id):
                async with sem:
                    return await self.evt_mturk_api_core.exec_boto3("list_assignments_for_hit", { "HITId": hit_id })

            #hits = await self.evt_mturk_api_hit_core.list_hits(Cached)
            res = await asyncio.gather(*[_list_assignments_for_hit(hit_id) for hit_id in HITIds])

            ret_keys = ("AcceptTime","AssignmentId","AssignmentStatus","AutoApprovalTime","SubmitTime","WorkerId")
            assignments = [{k:r["Assignments"][0][k] for k in ret_keys} for r in res if len(r["Assignments"])==1]

            for asmt in assignments:
                asmt["PlatformWorkerId"] = asmt["WorkerId"]
                asmt["WorkerId"] = await self.r_wkr.get_id_for_platform("MTurk", asmt["PlatformWorkerId"])

            return assignments
