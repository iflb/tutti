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
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        pns = common.get_projects()
        prj_paths = [self.path.project(pn) for pn in pns]
        projects = [{"name": p[0], "path": str(p[1])} for p in zip(pns, prj_paths)]
        output.set("Projects", projects)
