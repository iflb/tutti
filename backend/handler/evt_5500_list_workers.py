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
        self.evt_project = manager.get_handler_for(manager.key_ids["PROJECT_CORE"])[1]

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if event.data is None:  event.data = {}
        output.set("Workers", await self.list_workers(**event.data))

    async def list_workers(self, Platform=None, ProjectName=None):
        wids = []
        if ProjectName:  pns = [ProjectName]
        else:            pns = [prj["name"] for prj in await self.evt_project.list_projects()]

        wkr_prjs = {}
        for pn in pns:
            wids = await self.r_wkr.get_ids_for_pn(pn)
            for wid in wids:
                if wid not in wkr_prjs:  wkr_prjs[wid] = []
                wkr_prjs[wid].append(pn)

        [wids.extend(await self.r_wkr.get_ids_for_pn(pn)) for pn in pns]

        tasks = [self.r_wkr.get(wid) for wid in wids]
        workers = dict(zip(wids, await asyncio.gather(*tasks)))
        for wid in workers:
            workers[wid]["Projects"] = wkr_prjs[wid]
        if Platform:  workers = {wid:wkr for wid,wkr in workers.items() if wkr["Platform"]==Platform}
        return workers
