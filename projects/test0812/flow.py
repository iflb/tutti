from libs.flowlib import TemplateNode, BatchNode

class TaskFlow:
    def __init__(self):
        self.batch_all = None

    def define(self):
        self.batch_all = BatchNode("all", children=[TemplateNode("pre1", cond_while=lambda t: t.cnt<6)])
        #batch_pre = BatchNode("pre", cond_if=lambda b: b.acc>=0)
        #batch_pre.append([
        #    TemplateNode("pre1"),
        #    TemplateNode("pre2"),
        #    TemplateNode("pre3"),
        #])
        #
        #batch_main = BatchNode("main", cond_while=lambda b: b.cnt<2)
        #batch_main.append([
        #    TemplateNode("main1"),
        #    TemplateNode("main2")
        #])
        #batch_post = BatchNode("post",
        #                       #cond_if=lambda n: n.acc>=0.8
        #             )
        #batch_post.append([
        #    TemplateNode("post1"),
        #    TemplateNode("post2")
        #])
        #batch_postq = BatchNode("post-qual", children=[batch_main, batch_post])

        #self.batch_all = BatchNode("all", children=[batch_pre, batch_postq])
