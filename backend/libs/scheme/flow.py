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

class FlowNode:
    def __init__(self, name, parent=None, prev=None, next=None, statement=Statement.NONE, condition=None, is_skippable=False, on_enter=None, on_exit=None):
        self.name = name
        self.parent = parent
        self.prev = prev
        self.next = next
        self.statement = statement
        self.condition = condition
        self.is_skippable = is_skippable
        self.on_enter = on_enter
        self.on_exit = on_exit

    def is_template(self):
        return isinstance(self, TemplateNode)
        
    def eval_cond(self, wkr_ctxt, ws_ctxt):
        if callable(self.condition):
            return self.condition(wkr_ctxt, ws_ctxt)
        else:
            print("skipping self.condition", self.condition)
            return True

    def forward(self, wkr_ctxt, ws_ctxt, try_skip=False):
        def _invoke_on_enter(node):
            if callable(self.on_enter):
                node.on_enter(wkr_ctxt, ws_ctxt)
            return node

        def _invoke_on_exit(node):
            if callable(node.on_exit):
                node.on_exit(wkr_ctxt, ws_ctxt)
            return node

        def check_node_exec_or_skip(node, try_skip=False):
            if node.statement in (Statement.IF, Statement.WHILE):
                if node.eval_cond(wkr_ctxt, ws_ctxt) and try_skip==False:
                    return node
                else:
                    if node.is_skippable:  return None
                    else:  raise UnskippableNodeException(f"unskippable node '{node.name}'")
            else:
                if try_skip:
                    if node.is_skippable:  return None
                    else:  raise UnskippableNodeException(f"unskippable node '{node.name}'")
                else:
                    return node


        ### main part starts here ###

        # try to get the first available children in the batch
        if isinstance(self, BatchNode):
            for child in self.children:
                node = check_node_exec_or_skip(child)
                if node:  return _invoke_on_enter(node)
                else: continue
            # reaches here if no children is available

        # reaches here if it's a BatchNode w/o available children OR a TemplateNode

        _invoke_on_exit(self)

        _node = self
        while True:
            if try_skip:
                check_node_exec_or_skip(_node, try_skip=True)

                # checking only whether the node is skippable
                # so, reaches here only if the node *is_skippable*, and go search the next node below
                # (if above would return something, it's always None, so ignore the return value)
            else:
                if _node.statement==Statement.WHILE:
                    if _node.eval_cond(wkr_ctxt, ws_ctxt):
                        return _invoke_on_enter(_node)

            _next = _node
            while (_next := _next.next):
                node = check_node_exec_or_skip(_next, try_skip=try_skip)
                if node: return _invoke_on_enter(node)
                else:    continue

            # reaches here when no executable next nodes are found

            if not (_node := _node.parent):  return None

class TerminalNode(FlowNode):
    def __init__(self, name):
        super().__init__(name)

class BeginNode(TerminalNode):
    def __init__(self):
        super().__init__("__begin__")

class EndNode(TerminalNode):
    def __init__(self):
        super().__init__("__end__")


class TemplateNode(FlowNode):
    def __init__(self, name, statement=Statement.NONE, condition=None, is_skippable=False, on_enter=None, on_exit=None, on_submit=None):
        super().__init__(name,
                         statement=statement,
                         condition=condition,
                         is_skippable=is_skippable,
                         on_enter=on_enter,
                         on_exit=on_exit)
        self.on_submit = on_submit

class BatchNode(FlowNode):
    def __init__(self, name, children=None, statement=Statement.NONE, condition=None, is_skippable=False, on_enter=None, on_exit=None):
        super().__init__(name,
                         statement=statement,
                         condition=condition,
                         is_skippable=is_skippable,
                         on_enter=on_enter,
                         on_exit=on_exit)
        self.children = children if children else []
        self.scan_children()

    def scan_children(self):
        c_prev = None
        for i,c in enumerate(self.children):
            c.parent = self
            c.prev = c_prev
            c.next = self.children[i+1] if i<len(self.children)-1 else None
            c_prev = c
