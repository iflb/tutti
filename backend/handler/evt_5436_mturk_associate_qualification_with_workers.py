import asyncio

from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if isinstance(event.data, dict):
            output.set("Results", await self.associate_qualification_with_workers(**event.data))
        else:
            raise Exception("data needs to be JSON format")

    async def associate_qualification_with_workers(self, QualificationTypeId, WorkerIds, IntegerValue=1, SendNotification=True):
        if isinstance(WorkerIds, list):
            tasks = [self.evt_mturk_api_core.exec_boto3("associate_qualification_with_worker", {
                "QualificationTypeId":QualificationTypeId,
                "WorkerId": wid,
                "IntegerValue": IntegerValue,
                "SendNotification": SendNotification
            }) for wid in WorkerIds]
            return await asyncio.gather(*tasks)
        else:
            raise Exception("WorkerIds needs to be a list")
