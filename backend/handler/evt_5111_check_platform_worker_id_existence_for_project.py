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
        self.evt_worker = manager.get_handler_for(manager.key_ids["WORKER_CORE"])[1]

        handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("Exists", await self.evt_worker.check_platform_worker_id_existence_for_project(**event.data))
