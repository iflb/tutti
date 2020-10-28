from libs.node import TemplateNode, BatchNode

class TaskFlow:
    def __init__(self):
        tmpl = TemplateNode("default")
        self.root = BatchNode("all", children=[tmpl])
