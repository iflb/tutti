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
        self.evt_nanotask = manager.get_handler_for(manager.key_ids["NANOTASK_CORE"])[1]

        handler_spec.set_description('Gets uploaded nanotasks.')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        kwargs1 = {k:event.data[k] for k in ["ProjectName", "TemplateName", "NanotaskId", "NumAssignable"] if k in event.data}
        await self.evt_nanotask.update_nanotask_num_assignable(**kwargs1)

        kwargs2 = {k:event.data[k] for k in ["NanotaskId"] if k in event.data}
        await self.evt_nanotask.update_nanotask_assignability_status(**kwargs2)
        output.set("ProjectName", event.data["ProjectName"])
        output.set("TemplateName", event.data["TemplateName"])
