import os
import asyncio
import importlib.util
from importlib import reload

from ducts.spi import EventHandler
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output
from handler.redis_resource import WorkerResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    async def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')
        self.r_wkr = WorkerResource(manager.redis)

        handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        pass

    async def check_platform_worker_id_existence_for_project(self, ProjectName, Platform, PlatformWorkerId):
        wid = await self.r_wkr.get_id_for_platform(Platform, PlatformWorkerId)
        wids = await self.r_wkr.get_ids_for_pn(ProjectName)
        return wid in wids
        
