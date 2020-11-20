from libs.node import TemplateNode, BatchNode, Statement

class TaskFlow:
    def __init__(self):
        t_pre = TemplateNode("pre1")

        t_main1 = TemplateNode("main3")
        t_main2 = TemplateNode("main2")
        b_main = BatchNode("main",
                           [t_main1, t_main2],
                           statement=Statement.WHILE,
                           cond=("cnt", "<", 3))

        self.root = BatchNode("all", children=[t_pre, b_main, TemplateNode("post2")])
