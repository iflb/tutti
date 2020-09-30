import heapq
from typing import Dict, Set

class DCModel:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def list_projects(self):
        return self.projects.keys()

    def add_project(self, project):
        self.projects[project.name] = project
        return project

    def get_project(self, name):
        return self.projects[name] if (name in self.projects) else None

class Project:
    def __init__(self, name):
        self.name = name
        self.templates: Dict[str, Template] = {}

    def list_templates(self):
        return self.templates.keys()

    def add_template(self, template):
        self.templates[template.name] = template
        return template

    def get_template(self, name):
        return self.templates[name] if (name in self.templates) else None

class Template:
    def __init__(self, name):
        self.name = name
        self.nids = set()

    def has_nanotasks(self):
        return len(self.nids)>0

    def add_nanotask_ids(self, nids: Set[str]):
        self.nids = self.nids | nids
        return self.nids

class TaskQueue:
    def __init__(self):
        self.queue_all = {}  # wid -> project_name -> template_name -> heapq

    def get_queue(self, wid, pn, tn):
        try:
            return self.queue_all[wid][pn][tn]
        except:
            try: self.queue_all[wid]
            except: self.queue_all[wid] = {}

            try: self.queue_all[wid][pn]
            except: self.queue_all[wid][pn] = {}

            try: self.queue_all[wid][pn][tn]
            except:
                self.queue_all[wid][pn][tn] = []
                heapq.heapify(self.queue_all[wid][pn][tn])
            
            return self.queue_all[wid][pn][tn]

    def push(self, queue, nid, priority):
        heapq.heappush(queue, (priority, nid))

    def get_first(self, queue):
        try:    return queue[0][1]
        except: return None

    def pop(self, queue):
        try:    return heapq.heappop(queue)[1]
        except: return None

class Nanotask:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def get(self, attr):
        return getattr(self, attr)
