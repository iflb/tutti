from datetime import datetime
import os
import asyncio

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

#import db

@config_callback
def config(loader):
    loader.add_attr('root_path', os.getcwd(), help='')
    loader.add_attr('root_path_project', 'projects/{project_name}', help='')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('プロジェクトを削除します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]
        
        root_path_project = os.path.join(self.conf.root_path, self.conf.root_path_project.format(project_name=project_name))

        if not os.path.exists(root_path_project):
            return "Error: project '{}' does not exist".format(project_name)

        #client = MySQLClient(connection_name="dummy",user="root",password="root",database=project_name,host="127.0.0.1",port=3306)
        #await client.db_delete()
        process = await asyncio.create_subprocess_shell("rm -rf {}".format(root_path_project), shell=True)
        retcode = await process.wait()

        return "Success: deleted project '{}'".format(project_name)
