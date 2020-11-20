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
        command = event.data["Command"]
        params = event.data["Params"] if "Params" in event.data else {}
        output.set("Command", command)

        if command=="Create":
            project_name = params["ProjectName"]
            template_names = params["TemplateNames"]
            preset_env_name = params["PresetEnvName"]
            preset_tmpl_name = params["PresetTemplateName"]
                
            preset = self.path.preset_template(preset_env_name, preset_tmpl_name, project_name)

            if not os.path.exists(preset):
                raise Exception("default preset does not exist ({})".format(preset))

            templates_success = []
            for template_name in template_names:
                dst = self.path.template(project_name, template_name)
    
                if os.path.exists(dst):
                    raise Exception("template '{}' already exists (Successful for templates: {})".format(template_name, templates_success))
    
                try:
                    #os.makedirs(os.path.dirname(dst), exist_ok=True)
                    print(preset, dst)
                    shutil.copytree(preset, dst)
                    templates_success.append(template_name)
                except Exception as e:
                    raise Exception("Error for '{}': {} (Successful for templates: {})".format(template_name, e, templates_success))
            output.set("Templates", templates_success)

        elif command=="Delete":
            project_name = params["ProjectName"]
            template_names = params["TemplateNames"]

            for tn in template_names:
                if not os.path.exists(self.path.template(project_name, tn)):
                    logger.debug(self.path.template(project_name, tn))
                    raise Exception("template '{}' for project '{}' does not exist".format(tn, project_name))

            spacedPaths = " ".join([str(self.path.template(project_name, tn)) for tn in template_names])

            process = await asyncio.create_subprocess_shell("rm -rf {}".format(spacedPaths), shell=True)
            retcode = await process.wait()

            output.set("Templates", template_names)

        elif command=="List":
            project_name = params["ProjectName"]

            output.set("Templates", common.get_templates(project_name))
            output.set("Project", project_name)

        elif command=="ListPresets":
            presets = []
            env_names = common.get_preset_env_names()
            for en in env_names:
                for tn in common.get_preset_template_names(en):
                    presets.append([en, tn])
            output.set("Presets", presets)
