import copy

import logging
logger = logging.getLogger(__name__)


def is_batch(elm):
    return isinstance(elm, BatchNode)

def is_node(elm):
    return isinstance(elm, TaskNode)


class Node:
    def __init__(self, tag, cond_if=None, cond_while=None):
        self.tag = tag
        self.cond_if = cond_if
        self.cond_while = cond_while
        self.acc = 0
        self.cnt = 0
        
    def set_if(self, cond):
        self.cond_if = cond

    def set_while(self, cond):
        self.cond_while = cond

class TaskNode(Node):
    def __init__(self, tag, template=None, **kwargs):
        super().__init__(tag, **kwargs)
        self.template = template if template else tag

class BatchNode(Node):
    def __init__(self, tag, elms=None, **kwargs):
        super().__init__(tag, **kwargs)
        self.elms = self._propagate(elms) if elms else []

    def _propagate(self, elm):
        if type(elm)==list:
            return [self._propagate(e) for e in elm]
        else:
            elm.cond_if = self.cond_if if not elm.cond_if else elm.cond_if
            #elm.cond_while = self.cond_while if not elm.cond_while else elm.cond_while
        return elm

    def append(self, elm):
        if type(elm)==list:
            self.elms.extend(self._propagate(elm))
        else:
            self.elms.append(self._propagate(elm))

    def retrieve(self, skip_while=False):
        ### ここは最下位のbatchまで
        for elm in self.elms:
            if not elm.cond_if or elm.cond_if(elm):
                _cnt = 0
                if not elm.cond_while:  _cond_while = lambda elm: _cnt==0
                else:                   _cond_while = elm.cond_while
                while _cond_while(elm):
                    yield elm
                    if is_batch(elm): yield from elm.retrieve(skip_while=skip_while)
                    if skip_while: break
                    elm.cnt += 1
                    _cnt += 1


class Engine:
    def __init__(self, root_batch):
        self.root = copy.deepcopy(root_batch)
        self.root_gen = self.root.retrieve()

    def test_generator(self):
        _root = copy.deepcopy(self.root)
        yield from _root.retrieve()

    def _get_next_template(self):
        while True:
            elm = self.root_gen.__next__()
            if is_node(elm): return elm

    def get_next_template(self):
        return self._get_next_template().tag
        #return self._get_next_template()

