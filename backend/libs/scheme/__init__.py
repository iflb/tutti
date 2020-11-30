from libs.scheme.flow import BeginNode, EndNode

class ProjectSchemeBase:
    def __init__(self):
        self.config_params()
        self._set_flow_root()

    def _set_flow_root(self):
        root_node = self.flow()
        self.flow_nodes = {
            "begin": BeginNode(),
            "root": root_node
            "end": EndNode()
        }
        self.flow_nodes["begin"].next = root_node
        self.flow_nodes["end"].prev = root_node
        self.flow_nodes["root"].prev = self.flow_nodes["begin"]
        self.flow_nodes["root"].next = self.flow_nodes["end"]
