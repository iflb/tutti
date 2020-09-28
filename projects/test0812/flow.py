from libs.node import TemplateNode, BatchNode, Statement

class TaskFlow:
    def __init__(self):
        t_pre1 = TemplateNode("pre1")
        t_pre2 = TemplateNode("pre2")
        b_pre = BatchNode("pre",
                          [t_pre1, t_pre2],
                          statement=Statement.IF,
                          cond=("cnt", "==", 0),
                          skippable=False)

        t_main1 = TemplateNode("main1")
        t_main2 = TemplateNode("main2")
        b_main = BatchNode("main",
                           [t_main1, t_main2],
                           statement=Statement.WHILE,
                           cond=("cnt", "<", 3))

        self.root = BatchNode("all", children=[b_pre, b_main, TemplateNode("post")])
