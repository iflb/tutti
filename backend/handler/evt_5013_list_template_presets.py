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
        presets = []
        env_names = common.get_preset_env_names()
        for en in env_names:
            for tn in common.get_preset_template_names(en):
                presets.append([en, tn])
        output.set("Presets", presets)
