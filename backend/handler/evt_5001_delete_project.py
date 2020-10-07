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
        handler_spec.set_description('プロジェクトを削除します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        project_name = event.data[0]
        
        path_prj = self.path.project(project_name)

        if not os.path.exists(path_prj):
            raise Exception("Error: project '{}' does not exist".format(project_name))

        process = await asyncio.create_subprocess_shell("rm -rf {}".format(path_prj), shell=True)
        retcode = await process.wait()

        output.set("Project", project_name)
