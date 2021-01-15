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
        pass

    async def create_project(self, ProjectName):
        path_prj = self.path.project(ProjectName)
        root_path_default_prj = self.path.default_project()

        if not os.path.exists(root_path_default_prj):
            raise Exception("Error: no default project src is found")
        if os.path.exists(path_prj):
            raise Exception("Error: project '{}' already exists".format(ProjectName))

        process = await asyncio.create_subprocess_shell("mkdir -p {} && cp -r {}/* {}".format(path_prj, root_path_default_prj, path_prj), shell=True)
        return await process.wait()

    async def delete_project(self, ProjectName):
        path_prj = self.path.project(ProjectName)

        if not os.path.exists(path_prj):
            raise Exception("Error: project '{}' does not exist".format(ProjectName))

        process = await asyncio.create_subprocess_shell("rm -rf {}".format(path_prj), shell=True)
        return await process.wait()

    async def list_projects(self):
        pns = common.get_projects()
        prj_paths = [self.path.project(pn) for pn in pns]
        projects = [{"name": p[0], "path": str(p[1])} for p in zip(pns, prj_paths)]
        return projects
