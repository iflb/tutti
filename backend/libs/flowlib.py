import copy

import logging
logger = logging.getLogger(__name__)


def is_batch(node):
    return isinstance(node, BatchNode)

def is_template(node):
    return isinstance(node, TemplateNode)


class Node:
    def __init__(self, tag, cond_if=None, cond_while=None, is_skippable=True):
        self.tag = tag
        self.cond_if = cond_if
        self.cond_while = cond_while

        # FIXME
        self.acc = 0
        self.cnt = 0
        self.scores = []

        # TODO
        self.is_skippable = is_skippable
        
    def set_if(self, cond):
        self.cond_if = cond

    def set_while(self, cond):
        self.cond_while = cond

    def score(self, drange="all", num=1, stat="mean"):
        if drange=="all":      _scores = self.scores
        elif drange=="first":  _scores = self.scores[:num]
        elif drange=="last":   _scores = self.scores[-num:]

        if len(_scores)==1:
            return _scores[0]
        else:
            #if stat=="mean":  return sum(_scores) / len(_scores)
            return sum(_scores) / len(_scores)

class TemplateNode(Node):
    def __init__(self, tag, template=None, **kwargs):
        super().__init__(tag, **kwargs)
        self.template = template if template else tag

class BatchNode(Node):
    def __init__(self, tag, children=None, child_order="natural", **kwargs):
        super().__init__(tag, **kwargs)
        self.children = self._propagate(children) if children else []

        # TODO
        self.child_order = child_order

    def _propagate(self, node):
        if type(node)==list:
            return [self._propagate(e) for e in node]
        else:
            node.cond_if = self.cond_if if not node.cond_if else node.cond_if
            #node.cond_while = self.cond_while if not node.cond_while else node.cond_while
        return node

    def append(self, node):
        if type(node)==list:
            self.children.extend(self._propagate(node))
        else:
            self.children.append(self._propagate(node))

    def retrieve(self):
        ### ここは最下位のbatchまで
        for node in self.children:
            if not node.cond_if or eval(node.cond_if)(node):
                _cnt = 0
                _cond_while = eval(node.cond_while) if node.cond_while else (lambda node: _cnt==0)

                while _cond_while(node):
                    yield node
                    if is_batch(node): yield from node.retrieve()
                    node.cnt += 1
                    _cnt += 1


class Engine:
    def __init__(self, project_name, root_batch):
        self.project_name = project_name
        self.root = copy.deepcopy(root_batch)
        self.root_gen = self.root.retrieve()

    def test_generator(self):
        _root = copy.deepcopy(self.root)
        yield from _root.retrieve()

    def _get_next_template(self):
        while True:
            n = self.root_gen.__next__()
            if is_template(n): return n

    def get_next_template(self):
        return self._get_next_template().tag
        #return self._get_next_template()

