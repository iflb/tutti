from enum import Enum

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

    def is_template(self):
        return isinstance(self, TemplateNode)
        
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
