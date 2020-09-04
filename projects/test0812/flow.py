from libs.flowlib import TemplateNode, BatchNode

class TaskFlow:
    def __init__(self):
        self.batch_all = None

    def define(self):
        batch_pre = BatchNode("pre", is_skippable=False, cond_if="lambda b: b.cnt==0")
        batch_pre.append([
            TemplateNode("pre1"),
            TemplateNode("pre2")
        ])
        
        batch_main = BatchNode("main", cond_while="lambda b: b.cnt<3")
        batch_main.append([
            TemplateNode("main1"),
            TemplateNode("main2")
        ])

        self.batch_all = BatchNode("all", children=[batch_pre, batch_main, TemplateNode("post")])
