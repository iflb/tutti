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
        handler_spec.set_description('Creates a QualificationType.')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if event.data is None:  event.data = {}
        output.set("Assignments", await self.get_assignments(**event.data))

    async def get_assignments(self, AssignmentIds):
        sem = asyncio.Semaphore(sem_limit)
        async def _get_assignment(assignment_id):
            async with sem:
                return await self.evt_mturk_api_core.exec_boto3("get_assignment", { "AssignmentId": assignment_id })

        tasks = [asyncio.ensure_future(_get_assignment(assignment_id)) for assignment_id in AssignmentIds]
        return await asyncio.gather(*tasks)
