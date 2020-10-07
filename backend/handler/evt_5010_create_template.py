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
        template_names = event.data[1:-1]
        preset_name = event.data[-1]
        
        preset = self.path.template_preset(preset_name, project_name)

        if not os.path.exists(preset):
            raise Exception("default preset does not exist ({})".format(preset))

        templates_success = []
        for template_name in template_names:
            dst = self.path.template_main(project_name, template_name)
    
            if os.path.exists(dst):
                raise Exception("template '{}' already exists (Successful for templates: {})".format(template_name, templates_success))
    
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(preset, dst)
                templates_success.append(template_name)
            except Exception as e:
                raise Exception("Error for '{}': {} (Successful for templates: {})".format(template_name, e, templates_success))
        output.set("Templates", templates_success)
