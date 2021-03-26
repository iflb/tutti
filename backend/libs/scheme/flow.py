from copy import deepcopy
from enum import Enum
import inspect
import io
import tokenize
import numbers

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Statement(Enum):
    NONE = 0
    IF = 1
    WHILE = 2
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Condition:
    def __init__(self, statement, func, **kwargs):
        self.statement = statement
        self.func = func
        self.func_params = kwargs

        self.print_func = self._get_print_func()

    def eval(self, wkr_ctxt, ws_ctxt):
        return self.func(wkr_ctxt, ws_ctxt, **self.func_params)

    def _get_print_func(self):
        result = []
        for n,v,_,_,_ in tokenize.generate_tokens(io.StringIO(inspect.getsource(self.func)).readline):
            if n==tokenize.NAME and (v in self.func_params.keys()):
                if isinstance(self.func_params[v], numbers.Number):
                    result.append((tokenize.NUMBER, str(self.func_params[v])))
                elif isinstance(self.func_params[v], str):
                    result.append((tokenize.STRING, self.func_params[v]))
            else:
                result.append((n,v))
        result_str = tokenize.untokenize(result)
        result_str = result_str.replace(" ,",", ").replace(" (","(").replace(" )",")").replace(" .",".")
        return result_str

    def print(self):
        return self.print_func

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
    def __init__(self, name, parent=None, prev=None, next=None, condition=None, is_skippable=False, on_enter=None, on_exit=None):
        self.name = name
        self.parent = parent
        self.prev = prev
        self.next = next
        self.condition = condition
        self.is_skippable = is_skippable
        self.on_enter = on_enter
        self.on_exit = on_exit

    def is_template(self):
        return isinstance(self, TemplateNode)
        
    def eval_cond(self, wkr_ctxt, ws_ctxt):
        if self.condition:
            return self.condition.eval(wkr_ctxt, ws_ctxt)
        else:
            return True

    async def forward(self, wkr_ctxt, ws_ctxt, try_skip=False):
        async def _invoke_on_enter(node):
            logger.debug(f"trying {node.name} on_enter")
            if callable(self.on_enter):
                logger.debug(f"{node.name} on_enter")
                node.on_enter(wkr_ctxt, ws_ctxt)
                await wkr_ctxt._register_new_members_to_redis()
                await ws_ctxt._register_new_members_to_redis()
            return node

        async def _invoke_on_exit(node, unskippable=False, no_nanotask=False):
            logger.debug(f"trying {node.name} on_exit")
            if callable(node.on_exit):
                logger.debug(f"{node.name} on_exit")

                node.on_exit(wkr_ctxt, ws_ctxt, unskippable, no_nanotask)

                await wkr_ctxt._register_new_members_to_redis()
                await ws_ctxt._register_new_members_to_redis()
            return node

        async def _exit_all_and_raise_exception(node, exception):
            while (node := node.parent):
                await _invoke_on_exit(node, unskippable=True)
            raise exception

        async def check_node_exec_or_skip(node, try_skip=False):
            logger.debug(f"trying {node.name}")
            if node.condition and node.condition.statement in (Statement.IF, Statement.WHILE):
                if node.eval_cond(wkr_ctxt, ws_ctxt) and try_skip==False:
                    return node
                else:
                    if node.is_skippable:  return None
                    else:  await _exit_all_and_raise_exception(node, UnskippableNodeException(f"unskippable node '{node.name}'"))
            else:
                if try_skip:
                    if node.is_skippable:  return None
                    else:  await _exit_all_and_raise_exception(node, UnskippableNodeException(f"unskippable node '{node.name}'"))
                else:
                    return node


        ### main part starts here ###

        # try to get the first available children in the batch
        if isinstance(self, BatchNode):
            logger.debug(f"searching children of {self.name}")
            for child in self.children:
                node = await check_node_exec_or_skip(child)
                if node:  return await _invoke_on_enter(node)
                else: continue
            # reaches here if no children is available
            logger.debug("no executable child was found")

        # reaches here if it's a BatchNode w/o available children OR a TemplateNode

        _node = self
        while True:
            await _invoke_on_exit(_node, no_nanotask=try_skip)
            if try_skip:
                await check_node_exec_or_skip(_node, try_skip=True)

                logger.debug(f"skipping {_node.name}")
                # checking only whether the node is skippable
                # so, reaches here only if the node *is_skippable*, and go search the next node below
                # (if above would return something, it's always None, so ignore the return value)
            else:
                if _node.condition and _node.condition.statement==Statement.WHILE:
                    logger.debug(f"trying loop for {_node.name}")
                    if _node.eval_cond(wkr_ctxt, ws_ctxt):
                        logger.debug(f"looping {_node.name}")
                        return await _invoke_on_enter(_node)

            _next = deepcopy(_node)
            logger.debug(f"next node for {_node.name}: {_node.next.name if _node.next else 'None'}")
            while (_next := _next.next):
                if ( node := await check_node_exec_or_skip(_next, try_skip=try_skip)):
                    return await _invoke_on_enter(node)

            # reaches here when no executable next nodes are found

            if not (_node := _node.parent):  return None

            logger.debug(f"back to parent: {_node.name}")

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
    def __init__(self, name, condition=None, is_skippable=False, on_enter=None, on_exit=None, on_submit=None):
        super().__init__(name,
                         condition=condition,
                         is_skippable=is_skippable,
                         on_enter=on_enter,
                         on_exit=on_exit)
        self.on_submit = on_submit

class BatchNode(FlowNode):
    def __init__(self, name, children=None, condition=None, is_skippable=False, on_enter=None, on_exit=None):
        super().__init__(name,
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
