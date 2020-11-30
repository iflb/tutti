from enum import Enum
from IPython import embed

class Statement(Enum):
    NONE = 0
    IF = 1
    WHILE = 2
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class UnSkippableNodeException(Exception):
    pass

class Node:
    def __init__(self, name, parent=None, prev=None, next=None, **kwargs):
        self.name = name
        self.parent = parent
        self.prev = prev
        self.next = next

        self.statement    = kwargs["statement"]    if "statement"    in kwargs else Statement.NONE
        self.condition    = kwargs["condition"]    if "condition"    in kwargs else None
        self.is_skippable = kwargs["is_skippable"] if "is_skippable" in kwargs else False
        
    def eval_cond(self, node, ws, fs, ns):
        # TODO
        import random
        ret = random.choice([True, False])
        print(f"random choice for '{node.name}': {ret}")
        return ret

    def forward(self, ws, fs, ns):
        def check_node_exec_or_skip(node):
            if node.statement in (Statement.IF, Statement.WHILE):
                if node.eval_cond(node, ws, fs, ns):
                    return node
                else:
                    if node.is_skippable:  return None
                    else:  raise UnSkippableNodeException(f"unskippable node '{node.name}'")
            else:
                return node


        if isinstance(self, BatchNode):
            for child in self.children:
                node = check_node_exec_or_skip(child)
                if node: return node
                else:    continue

        _parent = self
        while True:
            if _parent.statement==Statement.WHILE:
                if _parent.eval_cond(_parent, ws, fs, ns):
                    return _parent

            _next = _parent
            while (_next := _next.next):
                node = check_node_exec_or_skip(_next)
                if node: return node
                else:    continue

            if not (_parent := _parent.parent):  break

        return _parent

class TerminalNode(Node):
    def __init__(self, name, prev=None, next=None):
        super().__init__(name, prev=prev, next=next)

class BeginNode(TerminalNode):
    def __init__(self, next=None):
        super().__init__(name="__begin__", next=next)

class EndNode(TerminalNode):
    def __init__(self, prev=None):
        super().__init__(name="__end__", prev=prev)


class TemplateNode(Node):
    pass

class BatchNode(Node):
    def __init__(self, name, children=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.children = children if children else []
        self.scan_children()

    def scan_children(self):
        c_prev = None
        for i,c in enumerate(self.children):
            c.parent = self
            c.prev = c_prev
            c.next = self.children[i+1] if i<len(self.children)-1 else None
            c_prev = c

    
class BaseFlow:
    def __init__(self):
        self.begin_node = BeginNode()
        self.end_node = EndNode()
        self.root_node = None

    def set_root(self, node):
        self.begin_node.next = self.end_node.prev = self.root_node = node
        self.root_node.prev = self.begin_node
        self.root_node.next = self.end_node

    def initiate(self):
        return self.begin_node.forward(None, None, None)

    
class Flow(BaseFlow):
    def __init__(self):
        super().__init__()
        tmp1 = TemplateNode("tmp1")
        tmp2 = TemplateNode("tmp2")
        batch1 = BatchNode("batch1", children=[tmp1, tmp2], statement=Statement.IF)
        tmp3 = TemplateNode("tmp3")
        tmp4 = TemplateNode("tmp4")
        tmp5 = TemplateNode("tmp5")
        batch2 = BatchNode("batch2", children=[tmp3, tmp4, tmp5], statement=Statement.IF, is_skippable=True)
        batch = BatchNode("batch", children=[batch1, batch2], statement=Statement.WHILE)
        self.set_root(batch)


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

class ProjectScheme(ProjectSchemeBase):
    def config_params(self):
        self.pagination = False
        
    def flow(self):
        tmp1 = TemplateNode("tmp1")
        tmp2 = TemplateNode("tmp2")
        batch1 = BatchNode("batch1", children=[tmp1, tmp2], statement=Statement.IF, cond_func=self.batch1_if)

        tmp3 = TemplateNode("tmp3")
        tmp4 = TemplateNode("tmp4")
        tmp5 = TemplateNode("tmp5")
        batch2 = BatchNode("batch2", children=[tmp3, tmp4, tmp5], statement=Statement.IF, is_skippable=True)

        return BatchNode("batch", children=[batch1, batch2], statement=Statement.WHILE)

    def batch1_if(self, some_session):
        # write some rules
        return True

if __name__=="__main__":
    flow = Flow()
    next_node = flow.begin_node
    while (next_node := next_node.forward(None, None, None)):
        print(f"--> {next_node.__class__.__name__} {next_node.name}")
        print("===")
        if isinstance(next_node, EndNode):
            break
