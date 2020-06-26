from datetime import datetime
import os
import asyncio
from asyncio.subprocess import PIPE

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr('root_path', os.getcwd(), help='')
    loader.add_attr('root_path_templates', 'projects/{project_name}/templates/', help='')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]

        root_path_templates = os.path.join(self.conf.root_path, self.conf.root_path_templates)

        process = await asyncio.create_subprocess_shell("ls {}".format(root_path_templates.format(project_name=project_name)), stdout=PIPE, shell=True)
        val = await process.communicate()

        return val[0].decode().split("\n")[:-1]
