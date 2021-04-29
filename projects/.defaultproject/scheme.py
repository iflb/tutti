from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Condition, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.title = ""
        #self.assignment_order = "bfs"
        #self.sort_order = "natural"
        #self.show_title = True
        #self.page_navigation = False
        #self.push_instruction = True
        #self.instruction_btn = True
        #self.allow_parallel_sessions = True
        #self.anonymous = False
        #self.preview = True
        #self.completion_alert = False

    def define_flow(self):
        # define your task flow here
        return TemplateNode("hello-world")
