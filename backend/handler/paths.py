import os
from pathlib import Path

root = Path(os.getcwd())
projects = root / 'projects'

def project_dirpath(project_name):
    return projects / project_name

def project_profile_filepath(project_name):
    return project_dirpath(project_name) / "profile.json"

def templates_dirpath(project_name):
    return project_dirpath(project_name) / "templates"

def template_dirpath(project_name, template_name):
    return templates_dirpath(project_name) / template_name
