import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('プロジェクトを削除します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]
        
        path_prj = self.path.project(project_name)

        if not os.path.exists(path_prj):
            return "Error: project '{}' does not exist".format(project_name)

        process = await asyncio.create_subprocess_shell("rm -rf {}".format(path_prj), shell=True)
        retcode = await process.wait()

        return "Success: deleted project '{}'".format(project_name)
