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
        await self.delete_templates(**event.data)

    async def delete_templates(self, ProjectName, TemplateNames):
        for tn in TemplateNames:
            if not os.path.exists(self.path.template(ProjectName, tn)):
                logger.debug(self.path.template(ProjectName, tn))
                raise Exception("template '{}' for project '{}' does not exist".format(tn, ProjectName))

        spacedPaths = " ".join([str(self.path.template(ProjectName, tn)) for tn in TemplateNames])

        process = await asyncio.create_subprocess_shell("rm -rf {}".format(spacedPaths), shell=True)
        retcode = await process.wait()
