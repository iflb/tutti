import os
import asyncio

from ducts.spi import EventHandler
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_project = manager.get_handler_for(manager.key_ids["PROJECT_CORE"])[1]

        handler_spec.set_description('Deletes a project.')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        await self.evt_project.delete_project(**event.data)
        output.set("ProjectName", event.data["ProjectName"])
