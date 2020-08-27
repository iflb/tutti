import os
from pathlib import Path

root = Path(os.getcwd())
projects = root / 'projects'

def project_dirpath(project_name):
    return projects / project_name

def template_dirpath(project_name, template_name):
    return projects / project_name / "templates" / template_name

def project_profile_filepath(project_name):
    return project_path(project_name) / "profile.json"
