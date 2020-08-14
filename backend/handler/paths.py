import os
from pathlib import Path

root = Path(os.getcwd())
projects = root / 'projects'

def project_profile_path(project_name):
    return projects / project_name / "profile.json"
