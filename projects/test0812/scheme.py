from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.pagination = False
        
    def define_flow(self):
        t_pre = TemplateNode("pre1")

        t_main1 = TemplateNode("main4")
        t_main2 = TemplateNode("main2")
        b_main = BatchNode("main",
                           [t_main1, t_main2],
                           statement=Statement.WHILE,
                           #cond=("cnt", "<", 3)
                           )

        return BatchNode("all", children=[t_pre, b_main, TemplateNode("post2", is_skippable=False)])

    def batch1_if(self, some_session):
        # write some rules
        return True
