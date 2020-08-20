import os
import asyncio
from asyncio.subprocess import PIPE

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler import paths, common

import logging
logger = logging.getLogger(__name__)

@config_callback
def config(loader):
    loader.add_attr('root_path', os.getcwd(), help='')
    loader.add_attr('root_path_projects', 'projects/', help='')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('プロジェクト一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        return common.get_projects()
