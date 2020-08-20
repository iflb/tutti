from libs.flowlib import TaskNode, BatchNode

class TaskFlow:
    def __init__(self):
        self.batch_all = None

    def define(self):
        batch_pre = BatchNode("pre", cond_if=lambda b: b.acc>=0)
        batch_pre.append([
            TaskNode("pre1"),
            TaskNode("pre2"),
            TaskNode("pre3"),
        ])
        
        batch_main = BatchNode("main", cond_while=lambda b: b.cnt<2)
        batch_main.append([
            TaskNode("main1"),
            TaskNode("main2")
        ])
        batch_post = BatchNode("post",
                               #cond_if=lambda n: n.acc>=0.8
                     )
        batch_post.append([
            TaskNode("post1"),
            TaskNode("post2")
        ])
        batch_postq = BatchNode("post-qual", elms=[batch_main, batch_post])

        self.batch_all = BatchNode("all", elms=[batch_pre, batch_postq])
