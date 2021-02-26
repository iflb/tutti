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
        output.set("Results", await self.notify_workers(**event.data))

    async def notify_workers(self, Subject, MessageText, SendEmailWorkerIds):
        wids = [SendEmailWorkerIds[i:i+100] for i in range(0, len(SendEmailWorkerIds), 100)]
        tasks = [self.evt_mturk_api_core.exec_boto3("notify_workers", {"Subject":Subject, "MessageText": MessageText, "WorkerIds":_wids}) for _wids in wids]
        return await asyncio.gather(*tasks)
