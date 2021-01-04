from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.title = ""
        # self.assignment_order = "bfs"
        # self.sort_order = "natural"
        # self.pagination = False
        # self.instruction = True
        # self.show_title = True
        
    def define_flow(self):
        # define your task flow here
