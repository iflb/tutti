import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

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
        if event.data is None:  event.data = {}
        output.set("Results", await self.associate_qualifications_with_workers(**event.data))

    async def associate_qualifications_with_workers(self, QualificationTypeId, WorkerIds, IntegerValue, SendNotification):
        tasks = [self.evt_mturk_api_core.exec_boto3("associate_qualification_with_worker", {"QualificationTypeId":QualificationTypeId, "WorkerId": wid, "IntegerValue": IntegerValue, "SendNotification": SendNotification}) for wid in WorkerIds]
        return await asyncio.gather(*tasks)
