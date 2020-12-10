from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.title = "My test project"
        self.pagination = False
        
    def define_flow(self):
        t_pre = TemplateNode("pre1")

        #t_main1 = TemplateNode("main4", on_submit=self.t_main1_on_submit)
        t_main1 = TemplateNode("main4")
        t_main2 = TemplateNode("main2", statement=Statement.IF, condition=self.t_main2_cond, is_skippable=True)
        b_main = BatchNode("main",
                           [t_main1, t_main2],
                           statement=Statement.WHILE,
                           condition=self.b_main_cond
                           )

        return BatchNode("all", children=[t_pre, b_main, TemplateNode("post2")])

    def b_main_cond(self, wkr_client, ws_client):
        print(wkr_client._cnt, ws_client._cnt)
        return ws_client.cnt("main")<5

    def t_main2_cond(self, wkr_client, ws_client): 
        return ws_client.cnt("main2")<3
