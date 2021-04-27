from datetime import datetime
import os
import asyncio
import shutil
from pathlib import Path

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
        templates_success = await self.create_templates(**event.data)
        output.set("Templates", templates_success)

    async def create_templates(self, ProjectName, TemplateNames, PresetEnvName, PresetTemplateName):
        preset = self.path.preset_template(PresetEnvName, PresetTemplateName, ProjectName)

        if not os.path.exists(preset):
            raise Exception("default preset does not exist ({})".format(preset))

        templates_success = []
        for tn in TemplateNames:
            dst = self.path.template(ProjectName, tn)
    
            if os.path.exists(dst):
                raise Exception("template '{}' already exists (Successful for templates: {})".format(tn, templates_success))
    
            try:
                shutil.copytree(preset, dst)
                open(dst/Path(".dummy"),"w").close()
                templates_success.append(tn)
            except Exception as e:
                raise Exception("Error for '{}': {} (Successful for templates: {})".format(tn, e, templates_success))
        return templates_success
