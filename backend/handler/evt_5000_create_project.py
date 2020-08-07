from datetime import datetime
import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

#import db

import logging

@config_callback
def config(loader):
    loader.add_attr('root_path', os.getcwd(), help='')
    loader.add_attr('root_path_project', 'projects/{project_name}', help='')
    loader.add_attr('root_path_default_project', 'projects/.defaultproject', help='')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]
        
        root_path_project = os.path.join(self.conf.root_path, self.conf.root_path_project.format(project_name=project_name))
        root_path_default_project = os.path.join(self.conf.root_path, self.conf.root_path_default_project)

        if not os.path.exists(root_path_default_project):
            return "Error: no default project src is found"
        if os.path.exists(root_path_project):
            return "Error: project '{}' already exists".format(project_name)

        #await db.migrate_project_db(project_name)
        process = await asyncio.create_subprocess_shell("mkdir -p {} && cp -r {}/* {}".format(root_path_project, root_path_default_project, root_path_project), shell=True)
        retcode = await process.wait()

        return "Success: created project '{}'".format(project_name)
