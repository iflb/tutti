from enum import Enum
import datetime
import random
import string
import time
import pickle

import redis
r = redis.Redis(host="localhost", port=6379, db=0)

from libs.node import Statement

import handler.helper_redis_namespace as namespace_redis

class SessionStatus(Enum):
    ACTIVE = 1
    FINISHED = 2
    EXPIRED = 3

class Session:
    def __init__(self, time_created=None):
        self.status = SessionStatus.ACTIVE
        if time_created and type(time_created)==datetime.datetime:
            self.time_created = time_created
        else:
            self.time_created = datetime.datetime.now()
        self.time_finished = None

        self.id = self._generate_id()

    def _generate_id(self):
        return "{}.".format("".join([c for c in self.__class__.__name__ if c.isupper()]))+''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

    def finish(self, time=None):
        if time is None:
            time = datetime.datetime.now()
        self.time_finished = time
        self.status = SessionStatus.FINISHED

class NodeSession(Session):
    def __init__(self, ws, node, parent, prev):
        super().__init__()
        self.ws = ws
        self.node = node
        self.prev = prev
        self.next = None
        self.parent = parent
        self.node_lcnts = {}   # { node.name: int }
        self.nid = None
        self.answers = None

        self.cnt = ws.node_cnts[node.name] if node.name in ws.node_cnts else 0
        self.lcnt = parent.node_lcnts[node.name] if parent and (node.name in parent.node_lcnts) else 0
        self.score = 0
        self.prev_ans = None
        #print("started NodeSession({}) for node '{}' (statement={}, cond={}, cnt={})".format(self.id, self.node.name, self.node.statement, self.node.cond, self.cnt))

    def increase_node_lcnt(self, node):
        if node.name not in self.node_lcnts:
            self.node_lcnts[node.name] = 0
        self.node_lcnts[node.name] += 1

    def update_attr(self, attr_name, val):
        setattr(self, attr_name, val)
        self.save_to_redis()

    def save_to_redis(self):
        r.set(namespace_redis.key_for_node_session_by_id(self.id), pickle.dumps(self))

    def finish(self):
        super().finish()
        self.ws.increase_node_cnt(self.node)
        if self.parent:
            self.parent.increase_node_lcnt(self.node)
        #print("finished NodeSession({}) for node '{}'".format(self.id, self.node.name))

class WorkSession(Session):
    def __init__(self, wid, pid, root_node, expiration=None):
        super().__init__()
        self.wid = wid
        self.pid = pid
        self.ns_factory = NodeSessionFactory(self)
        self.root_node = root_node
        self.root_ns = None
        self._set_expiration(expiration)
        self.node_cnts = {}   # { node.name: int }

        self.nsessions = {}

        r.sadd(namespace_redis.key_for_work_session_ids_by_project_name(pid), self.id)
        r.sadd(namespace_redis.key_for_work_session_ids_by_worker_id(wid), self.id)

    def increase_node_cnt(self, node):
        if node.name not in self.node_cnts:
            self.node_cnts[node.name] = 0
        self.node_cnts[node.name] += 1

    def _set_expiration(self, exp):
        if type(exp) is int:
            self.expires_at = self.time_created + datetime.timedelta(seconds=exp)
        elif type(exp) is datetime.datetime:
            self.expires_at = exp
        elif exp is None:
            self.expires_at = None
        else:
            raise Exception("unknown expiration type")

    def _get_next_node_session(self, ns):
        def _exit_node_and_find_next(ns, prev=None):
            if prev is None:  prev = ns

            ns.finish()  # exit current node

            next_ns = None
            if ns.node.statement==Statement.WHILE:
                next_ns = self.ns_factory.create_if_executable(ns.node, parent=ns.parent, prev=prev)

            if next_ns is None:
                if ns.node.next:
                    next_ns = self.ns_factory.create_if_executable(ns.node.next, parent=ns.parent, prev=prev)
                elif ns.node.parent:
                    next_ns = _exit_node_and_find_next(ns.parent, prev=prev)
                else:  # = currently end of root batch
                    next_ns = None

            return next_ns

        def _enter_batch_and_find_next(ns):
            for child in ns.node.children:
                if (next_ns := self.ns_factory.create_if_executable(child, parent=ns, prev=ns)):
                    return next_ns
                elif child.skippable==False:
                    return None

            # only if batch has no executable child
            return _exit_node_and_find_next(ns)

        ### main ##########

        if ns is None:
            if (next_ns := self.ns_factory.create_if_executable(self.root_node)):
                self.root_ns = next_ns
            else:
                raise Exception("root node is not executable")
        else:
            if ns.node.is_batch():
                next_ns = _enter_batch_and_find_next(ns)
            else:
                next_ns = _exit_node_and_find_next(ns)

        if next_ns:
            r.sadd(namespace_redis.key_for_node_session_ids_by_node_id(next_ns.node.id), next_ns.id)
            r.sadd(namespace_redis.key_for_node_session_ids_by_work_session_id(self.id), next_ns.id)
            next_ns.save_to_redis()

        return next_ns


    def create_next_template_node_session(self, ns=None):
        while (ns := self._get_next_node_session(ns)):
            if ns.node.is_template():
                return ns 

        return None

    def get_existing_node_session(self, nsid):
        if nsid in self.nsessions:  return self.nsessions[nsid]
        else: return None


class NodeSessionFactory:
    def __init__(self, ws):
        self.ws = ws

    def create_if_executable(self, node, parent=None, prev=None):
        if node.statement==Statement.NONE \
           or node.eval_cond(Statement.IF, self.ws, parent, prev) \
           or node.eval_cond(Statement.WHILE, self.ws, parent, prev):

            ns = NodeSession(self.ws, node, parent=parent, prev=prev)
            if prev:
                prev.next = ns
            self.ws.nsessions[ns.id] = ns
            return ns

        else:
            return None
