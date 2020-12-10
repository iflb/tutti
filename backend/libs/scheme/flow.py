from enum import Enum


class Statement(Enum):
    NONE = 0
    IF = 1
    WHILE = 2
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class UnskippableNodeException(Exception):
    pass

class SessionEndException(Exception):
    pass

class Flow:
    def __init__(self, pn, root_node):
        self.pn = pn
        self.begin_node = BeginNode()
        self.end_node = EndNode()

        self.begin_node.next = self.end_node.prev = self.root_node = root_node
        self.root_node.prev = self.begin_node
        self.root_node.next = self.end_node

        self.nodes = self.register_nodes(root_node)

    def register_nodes(self, node):
        ret = {}
        ret[node.name] = node
        if isinstance(node, BatchNode):
            for child in node.children:
                ret.update(self.register_nodes(child))
        return ret

    def get_begin_node(self):
        return self.begin_node

    def get_node_by_name(self, name):
        return self.nodes[name]

    def get_all_node_names(self):
        return self.nodes.keys()

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
        
    def eval_cond(self, wkr_client, ws_client):
        if callable(self.condition):
            print("calling self.condition")
            return self.condition(wkr_client, ws_client)
        else:
            print("skipping self.condition", self.condition)
            return True
        ## TODO
        #import random
        #ret = random.choice([True, False])
        #print(f"random choice for '{node.name}': {ret}")
        #return ret

    def forward(self, wkr_client, ws_client):
        def check_node_exec_or_skip(node):
            if node.statement in (Statement.IF, Statement.WHILE):
                if node.eval_cond(wkr_client, ws_client):
                    return node
                else:
                    if node.is_skippable:  return None
                    else:  raise UnskippableNodeException(f"unskippable node '{node.name}'")
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
                if _parent.eval_cond(wkr_client, ws_client):
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
    #def __init__(self, on_submit=None, **kwargs):
    #    self.on_submit = on_submit

    #def _on_submit(self, ws_client, ans, gt):
    #    wkr.cnt[self.name] += 1
    #    for key,val in ans_gt.items():
    #        if ans_wkr[key]==ans_gt[key]:  wkr.correct_cnt[self.name][key]
    #        wkr.acc[self.name][key] = wkr.correct_cnt[self.name][key] / wkr.cnt[self.name]

    #    ws.cnt[self.name] += 1
    #    for key,val in ans_gt.items():
    #        if ans_wkr[key]==ans_gt[key]:  ws.correct_cnt[self.name][key]
    #        ws.acc[self.name][key] = ws.correct_cnt[self.name][key] / ws.cnt[self.name]

    #    self.on_submit(ws_client, ans, gt)
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
