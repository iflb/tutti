from datetime import datetime
import os
import asyncio
import shutil

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output

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
        project_name = event.data[0]
        template_names = event.data[1:]
        
        for tn in template_names:
            if not os.path.exists(self.path.template(project_name, tn)):
                logger.debug(self.path.template(project_name, tn))
                raise Exception("template '{}' for project '{}' does not exist".format(tn, project_name))

        spacedPaths = " ".join([str(self.path.template(project_name, tn)) for tn in template_names])

        process = await asyncio.create_subprocess_shell("rm -rf {}".format(spacedPaths), shell=True)
        retcode = await process.wait()

        output.set("Templates", template_names)
