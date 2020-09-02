import os
import asyncio
from asyncio.subprocess import PIPE

import handler.paths as path

def get_projects():
    return [name for name in os.listdir(path.projects()) if os.path.isdir(path.project(name)) and not name.startswith(".")]

def get_templates(project_name):
    return [name for name in os.listdir(path.templates(project_name)) if os.path.isdir(path.template(project_name, name)) and not name.startswith(".")]
