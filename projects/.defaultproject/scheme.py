from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.pagination = False
        
    def flow(self):
        tmp1 = TemplateNode("tmp1")
        tmp2 = TemplateNode("tmp2")
        batch1 = BatchNode("batch1", children=[tmp1, tmp2], statement=Statement.IF, condition=self.batch1_if)

        tmp3 = TemplateNode("tmp3")
        tmp4 = TemplateNode("tmp4")
        tmp5 = TemplateNode("tmp5")
        batch2 = BatchNode("batch2", children=[tmp3, tmp4, tmp5], statement=Statement.IF, is_skippable=True)

        return BatchNode("batch", children=[batch1, batch2], statement=Statement.WHILE)

    def batch1_if(self, some_session):
        # write some rules
        return True
