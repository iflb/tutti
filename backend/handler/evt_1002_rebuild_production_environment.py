import os
import aiohttp
import asyncio

from ducts.event import EventHandler

from handler.handler_output import handler_output
class Handler(EventHandler):

    def setup(self, handler_spec, manager):
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        await self.rebuild_production_environment(**event.data)
        output.set("Success", True)

    async def rebuild_production_environment(self, ProjectName):
        #await asyncio.sleep(3)
        #return
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://{os.getenv('TUTTI_WEBAPI_HOST')}/{ProjectName}") as resp:
                await resp.text()
                return
