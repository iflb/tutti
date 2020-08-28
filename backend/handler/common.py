import os
import asyncio
from asyncio.subprocess import PIPE

import handler.paths as paths

def get_projects():
    return [name for name in os.listdir(paths.projects) if os.path.isdir(paths.project_dirpath(name)) and not name.startswith(".")]

def get_templates(project_name):
    return [name for name in os.listdir(paths.templates_dirpath(project_name)) if os.path.isdir(paths.template_dirpath(project_name, name)) and not name.startswith(".")]
