from libs.scheme import ProjectSchemeBase
from libs.scheme.flow import BatchNode, TemplateNode, Statement

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.title = "My test project"
        self.assignment_order = "bfs"
        self.sort_order = "random"
        self.pagination = True
        self.instruction = False
        self.show_title = False
        
    def define_flow(self):
        t_pre = TemplateNode("preliminary")

        #t_main4 = TemplateNode("main4", on_submit=self.t_main4_on_submit)
        #t_main2 = TemplateNode("main2", statement=Statement.IF, condition=self.t_main2_cond, is_skippable=True)
        #b_main = BatchNode("main", [t_main4, t_main2],
        #                   statement=Statement.WHILE, condition=self.b_main_cond, is_skippable=True)
        t_main4 = TemplateNode("main1")
        t_main2 = TemplateNode("main2")
        b_main = BatchNode("main", [t_main4, t_main2],
                           statement=Statement.WHILE, condition=self.b_main_cond, is_skippable=True)

        t_post = TemplateNode("post")

        return BatchNode("all", children=[t_pre, b_main, t_post])

    #def t_main4_on_submit(self, wkr_client, ws_client, ans, gt):
    #    choice_correct = 1 if ans["choice"]==gt["choice"] else 0
    #    wkr_client.add_member("choice_correct", choice_correct)

    def b_main_cond(self, wkr_client, ws_client): 
        return ws_client.cnt("main2")<5

    #def b_main_cond(self, wkr_client, ws_client):
    #    if wkr_client.cnt("main")>=10: return False

    #    return True
    #    #if (cc := ws_client.get_member("choice_correct")): accuracy = cc.count("1") / len(cc)
    #    #return (not cc) or accuracy >= 0.8
