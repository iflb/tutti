import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

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
        project_name = event.data[0]
        
        path_prj = self.path.project(project_name)
        root_path_default_project = self.path.default_project()

        if not os.path.exists(root_path_default_project):
            raise Exception("Error: no default project src is found")
        if os.path.exists(path_prj):
            raise Exception("Error: project '{}' already exists".format(project_name))

        process = await asyncio.create_subprocess_shell("mkdir -p {} && cp -r {}/* {}".format(path_prj, root_path_default_project, path_prj), shell=True)
        retcode = await process.wait()

        output.set("Project", project_name)
