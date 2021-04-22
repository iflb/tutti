import os
import aiohttp

from ducts.event import EventHandler

from handler.handler_output import handler_output
class Handler(EventHandler):

    def setup(self, handler_spec, manager):
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        has_diff = await self.check_project_diff(**event.data)
        output.set("HasDiff", has_diff)

    async def check_project_diff(self, ProjectName):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{os.getenv('TUTTI_WEBAPI_HOST')}/{ProjectName}") as resp:
                res = int(await resp.text())
                if res==-1:  raise Exception(f"ProjectName '{ProjectName}' does not exist")
                return res==1
