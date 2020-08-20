from datetime import datetime
import os
import asyncio
import shutil

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr('root_path', os.getcwd(), help='')
    loader.add_attr('root_path_project', 'projects/{project_name}', help='')
    loader.add_attr('dir_presets', 'templates', help='')
    loader.add_attr('preset_default', '.presets/Default.vue', help='')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレートを作成します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]
        template_names = event.data[1:]
        
        root_path_templates = os.path.join(self.conf.root_path, self.conf.root_path_project.format(project_name=project_name), self.conf.dir_presets)
        src = os.path.join(root_path_templates, self.conf.preset_default)

        if not os.path.exists(src):
            return "Error: default preset does not exist ({})".format(src)

        templates_success = []
        for template_name in template_names:
            dst = os.path.join(root_path_templates, f"{template_name}/Main.vue")
    
            if os.path.exists(dst):
                return "Error: template '{}' already exists (Successful for templates: {})".format(template_name, templates_success)
    
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                templates_success.append(template_name)
            except Exception as e:
                return "Error for '{}': {} (Successful for templates: {})".format(template_name, e, templates_success)
        return "Success: created template '{}'".format(templates_success)
