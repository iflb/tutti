import os
from pathlib import Path

from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr_path('root', Path().absolute(), help='Absolute path to backend folder')
    loader.add_attr_path('projects', 'projects', help='relative path to projects folder')
    loader.add_attr_path('templates', 'templates', help='relative path to templates folder')
    loader.add_attr_path('default_project', '.defaultproject', help='default project filename')
    loader.add_attr_path('project_profile', 'profile.json', help='project profile filename')
    loader.add_attr_path('template_presets', '.presets', help='template presets dirname')

cf = configure_module(config)

def projects():
    return cf.root / cf.projects

def default_project():
    return projects() / cf.default_project

def default_project_templates():
    return default_project() / cf.templates

def project(project_name):
    return projects() / Path(project_name)

def project_profile(project_name):
    return project(project_name) / cf.project_profile

def template_presets(project_name=None):
    if project_name:
        return templates(project_name) / cf.template_presets
    else:
        return default_project_templates() / cf.template_presets

def templates(project_name):
    return project(project_name) / cf.templates

def template(project_name, template_name):
    return templates(project_name) / Path(template_name)

def preset_envs(env_name, project_name=None):
    return template_presets(project_name) / Path(env_name)

def preset_template(env_name, tmpl_name, project_name=None):
    return template_presets(project_name) / Path(env_name) / Path(tmpl_name)
