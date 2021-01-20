import os
import asyncio
import importlib.util
from importlib import reload

from ducts.spi import EventHandler
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    async def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')

        handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()

        await self._load_all_project_schemes()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        pass

    async def _load_all_project_schemes(self):
        self.schemes = {}
        for project_name in common.get_projects():
            await self.get_project_scheme(ProjectName=project_name, Cached=False)

    async def get_project_scheme(self, ProjectName, Cached=True):
        if Cached:
            return self.schemes[ProjectName]
        else:
            module = "projects.{}.scheme".format(ProjectName)
            mod_flow = importlib.import_module(module)
            importlib.reload(mod_flow)
            scheme = mod_flow.ProjectScheme()
            self.schemes[ProjectName] = scheme
            return scheme
