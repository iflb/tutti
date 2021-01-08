from datetime import datetime
import os
import asyncio
import shutil

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output
from handler import common

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('テンプレートを作成します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("Templates", await self.list_templates(**event.data))
        output.set("Project", event.data["ProjectName"])

    async def list_templates(self, ProjectName):
        return common.get_templates(ProjectName)
