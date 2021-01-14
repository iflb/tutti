import time
import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

from handler.redis_resource import WorkerResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.r_wkr = WorkerResource(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if event.data is None:  event.data = {}
        output.set("Workers", await self.list_workers(**event.data))

    async def list_workers(self, Platform=None, ProjectName=None):
        if ProjectName:
            wids = await self.r_wkr.get_ids_for_pn(ProjectName)
        else:
            wkr_cnt = await self.r_wkr.get_counter()
            wids = [self.r_wkr.id(i) for i in range(1, wkr_cnt+1)]

        tasks = [self.r_wkr.get(wid) for wid in wids]
        workers = dict(zip(wids, await asyncio.gather(*tasks)))
        if Platform:  workers = {wid:wkr for wid,wkr in workers.items() if wkr["Platform"]==Platform}
        return workers
