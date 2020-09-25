from enum import Enum
import datetime
import json
import random
import string
import time
from IPython import embed

import pprint
import redis
r = redis.Redis(host="localhost", port=6379, db=0)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Statement):
            return obj.value
        elif isinstance(obj, BatchNode):
            return str(obj)
        elif isinstance(obj, TemplateNode):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)

class Statement(Enum):
    NONE = 0
    IF = 1
    WHILE = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Node:
    def __init__(self, name, statement, cond, skippable=True):
        self.name = name
        self.statement = statement
        self.cond = cond
        self.skippable = skippable
        self.prev = None
        self.next = None
        self.parent = None

    def is_batch(self):
        return isinstance(self, BatchNode)
    
    def is_template(self):
        return isinstance(self, TemplateNode)

    def get_children(self):
        if self.is_template(): return None
        else: return self.children

    def scan(self):
        if (children := self.get_children()):
            n_prev = None
            for i, child in enumerate(children):
                try:    n_next = children[i+1]
                except: n_next = None
                child.prev = n_prev
                child.next = n_next
                child.parent = self

                child.scan()
                n_prev = child

    def is_last(self):
        return (self.parent is not None) and (self.parent.children[-1]==self)

    def eval_cond(self, ws):
        if len(self.cond)==3:
            [attr, comparator, cmp_right] = self.cond
            try:
                cmp_left = eval(f"ws.node_{attr}s[self.name]")
            except:
                if attr=="cnt":
                    ws.node_cnts[self.name] = 0
                    cmp_left = 0
                # TODO
                #elif attr=="score":
                #    ws.node_scores[self.name] = 0
                #    cmp_left = 0
                else:
                    raise("invalid attribute in condition")

            cond = "{}{}{}".format(cmp_left, comparator, cmp_right)
            #print(cond, ns.cnt, eval(cond))
            return eval(cond)
        else:
            return False

    def do_if(self, ws):
        return self.statement==Statement.IF and self.eval_cond(ws)

    def do_while(self, ws):
        return self.statement==Statement.WHILE and self.eval_cond(ws)


class TemplateNode(Node):
    def __init__(self, name, statement=Statement.NONE, cond=()):
        super().__init__(name, statement, cond)
        self.id = self._generate_id()

    def _generate_id(self):
        return "TN."+''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

    def __str__(self):
        return f"<TemplateNode name={self.name}>"

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "statement": self.statement.name,
            "cond": " ".join(map(str,self.cond)),
            "prev": self.prev,
            "next": self.next,
            "parent": self.parent,
        }, indent=2, cls=JSONEncoder)

class BatchNode(Node):
    def __init__(self, name, children, statement=Statement.NONE, cond=()):
        super().__init__(name, statement, cond)
        self.children = children
        self.id = self._generate_id()

    def _generate_id(self):
        return "BN."+''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

    def __str__(self):
        return f"<BatchNode name={self.name}>"

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "statement": self.statement.name,
            "cond": " ".join(map(str,self.cond)),
            "prev": self.prev,
            "next": self.next,
            "parent": self.parent,
            "children": [vars(c) for c in self.children]
        }, indent=2, cls=JSONEncoder)

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

#class WorkSession(Session):
#    def __init__(self, wid, pid, root_batch, expiration=None):
#        super().__init__()
#        self.wid = wid
#        self.pid = pid
#        self.nsessions = []
#
#        self.root = root_batch
#
#        self.time_created = datetime.datetime.now()
#        self._set_expiration(expiration)
#
#        self.id = self._generate_id()
#
#    def _generate_id(self):
#        return "WS."+''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
#
#    def _set_expiration(self, exp):
#        if type(exp) is int:
#            self.expires_at = self.time_created + datetime.timedelta(seconds=exp)
#        elif type(exp) is datetime.datetime:
#            self.expires_at = exp
#        elif exp is None:
#            self.expires_at = None
#        else:
#            raise("unknown expiration type")
#
#    def get_last_active_node_session(self):
#        if len(self.nsessions)>0 and self.status==SessionStatus.ACTIVE:
#            nsession = self.nsessions[-1]
#            if nsession.status==SessionStatus.ACTIVE:  return nsession
#
#        return None

class NodeSessionFactory:
    def __init__(self, ws):
        self.ws = ws

    def create_if_executable(self, node, parent=None, prev=None):
        if node.statement==Statement.NONE or node.do_if(self.ws) or node.do_while(self.ws):
            ns = NodeSession(self.ws, node, parent=parent, prev=prev)
            if prev:
                prev.next = ns
                print(ns.node.name, prev.node.name)
            #self.ws.nsessions[ns.id] = ns
            self.ws.nsessions.append(ns)
            return ns
        else:
            return None

class NodeSession(Session):
    def __init__(self, ws, node, parent, prev):
        super().__init__()
        self.ws = ws
        self.node = node
        self.prev = prev
        self.next = None
        self.parent = parent
        self.nid = None

        self.cnt = ws.node_cnts[node.name] if node.name in ws.node_cnts else 0
        self.score = 0
        self.prev_ans = None
        #print("started NodeSession({}) for node '{}' (statement={}, cond={}, cnt={})".format(self.id, self.node.name, self.node.statement, self.node.cond, self.cnt))

    def finish(self):
        super().finish()
        if self.node.name not in self.ws.node_cnts:
            self.ws.node_cnts[self.node.name] = 0
        self.ws.node_cnts[self.node.name] += 1
        #print("finished NodeSession({}) for node '{}'".format(self.id, self.node.name))

class SessionManager:
    def __init__(self):
        self.latest_sessions = {}    # { worker_id: Session }

    def _get_last_active_work_session(self, wid):
        if (wid in self.latest_sessions) \
            and (wsession := self.latest_sessions[wid]) \
            and (wsession.status==SessionStatus.ACTIVE):
            return wsession
        else:
            return None

    def _conv_expiration_time(self, exp, now=None):
        if now is None:  now = datetime.datetime.now()
        if type(exp) is int:
            return now + datetime.timedelta(seconds=exp)
        elif (type(exp) is datetime.datetime) or (exp is None):
            return exp
        else:
            raise("unknown expiration type")
        
    def get_alive_work_session(self, wid):
        wsession = self._get_last_active_work_session(wid)
        if (wsession is not None) and (wsession.expires_at <= datetime.datetime.now()):
            del self.latest_wsessions[wid]
            wsession = None
        return wsession

    def on_start_work_session(self, wid, project_name, expiration):
        now = datetime.datetime.now()
        expires_at = self._conv_expiration_time(expiration, now)
        wsession_id = WorkSession(wid, project_name, None).id
        wsession_start = {
            "wid": wid,
            "prj": project_name,
            "time": now.timestamp(),
            "expires_at": expires_at.timestamp(),
            "is_available": 1
        }
        for key,val in wsession_start.items():  r.hset(f"{wsession_id}/START", key, val)

        return wsession_id

    def on_start_node_session(self, wsession_id, node, parent_nsid, nid=None):
        now = datetime.datetime.now()

        nsession_id = NodeSession(node).id
        nsession_start = {
            "ndid": node.id,
            "nid": nid,
            "parent_ns": parent_nsid,
            "time": now.timestamp()
        }

        r.rpush(f"{wsession_id}/NSID/START", nsession_id)
        for key,val in nsession_start.items():  r.hset(f"{wsession_id}/NODE/START/{nsession_id}", key, val)

        return nsession_id
        
    def on_finish_node_session(self, wsession_id, nsession_id, ans):
        ndid = r.hget(f"{wsession_id}/NODE/START/{nsession_id}", "ndid")

        nsids = r.lrange(f"{wsession_id}/NSID/FINISH", 0,-1)
        cnt = 0
        for nsid in reversed(nsids):
            nsid = nsid.decode()
            _ndid = r.hget(f"{wsession_id}/NODE/FINISH/{nsid}", "ndid")
            if ndid==_ndid:
                cnt = int(r.hget(f"{wsession_id}/NODE/FINISH/{nsid}", "cnt").decode())

                break

        nsession_finish = {
            "ndid": ndid,
            "cnt": cnt+1,
            "time": datetime.datetime.now().timestamp()
        }
        r.rpush(f"{wsession_id}/NSID/FINISH", nsession_id)
        for key,val in ans.items():  r.hset(f"{wsession_id}/NODE/ANSWER/{nsession_id}", key, val)
        for key,val in nsession_finish.items():  r.hset(f"{wsession_id}/NODE/FINISH/{nsession_id}", key, val)

    def on_finish_work_session(self, wsession_id):
        time = datetime.datetime.now()
        wsession_finish = {
            "time": datetime.datetime.now().timestamp()
        }
        for key,val in wsession_finish.items():  r.hset(f"{wsession_id}/FINISH", key, val)

    #def get_next_template(parent_nsid, tnode):
    #    if tnode._next:
    #        nsid = on_start_node_session(wsid, tnode._next, parent_nsid)
    #        return tnode._next, nsid
    #    else:
    #        while (node := tnode._parent):
    #            on_finish_node_session(wsid, node, 
    #    nsid = on_start_node_session(wsid, node, parent_nsid)
    #    if node.is_batch():
    #        for child in node.children:
    #            self.get_next_template(nsid, child)
    #    elif node.is_template():
    #        return 


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

        #self.nsessions = {}
        self.nsessions = []

    def _set_expiration(self, exp):
        if type(exp) is int:
            self.expires_at = self.time_created + datetime.timedelta(seconds=exp)
        elif type(exp) is datetime.datetime:
            self.expires_at = exp
        elif exp is None:
            self.expires_at = None
        else:
            raise("unknown expiration type")

    def _get_next_node_session(self, ns):
        def _fetch_next(ns, prev=None):
            if prev is None:  prev = ns

            if ns.node.next:
                next_ns = self.ns_factory.create_if_executable(ns.node.next, parent=ns.parent, prev=prev)
            else:
                if ns.node.parent:
                    next_ns = _exit_node_and_find_next(ns.parent, prev=prev)
                else:  # = currently end of root batch
                    next_ns = None

            return next_ns

        def _enter_batch_and_find_next(ns):
            #if len(ns.node.children)==0:
            #    raise Exception("error: batch does not have children")

            for child in ns.node.children:
                if (next_ns := self.ns_factory.create_if_executable(child, parent=ns, prev=ns)):
                    return next_ns
                elif child.skippable==False:
                    return None

            # current batch had no executable children, then finish it
            ns.finish()
            # and go find next batch
            return _fetch_next(ns)

        def _exit_node_and_find_next(ns, prev=None):
            ns.finish()  # exit current node

            if prev is None:  prev = ns

            next_ns = None
            if ns.node.statement==Statement.WHILE:
                next_ns = self.ns_factory.create_if_executable(ns.node, parent=ns.parent, prev=prev)

            if next_ns is None:
                next_ns = _fetch_next(ns, prev=prev)
            return next_ns
            


        if ns is None:
            if (next_ns := self.ns_factory.create_if_executable(self.root_node)):
                self.root_ns = next_ns
                #print("-> {}({})".format(next_ns.node.name, next_ns.id))
        else:
            if ns.node.is_batch():
                next_ns = _enter_batch_and_find_next(ns)
            else:
                next_ns = _exit_node_and_find_next(ns)

            if next_ns:
                pass
                #print("{}({}) -> {}({})".format(ns.node.name, ns.id, next_ns.node.name, next_ns.id))
        return next_ns


    def get_next_template_node_session(self, ns=None):
        while (ns := self._get_next_node_session(ns)):
            if ns.node.is_template():
                return ns 

        return None


if __name__=="__main__":
    t11 = TemplateNode("template11", statement=Statement.IF, cond=("cnt","<",2))
    t12 = TemplateNode("template12")
    b1 = BatchNode("batch1", [t11, t12], statement=Statement.WHILE, cond=("cnt","<",3))
    t21 = TemplateNode("template21", statement=Statement.IF, cond=("cnt","<",5))
    t22 = TemplateNode("template22")
    b2 = BatchNode("batch2", [t21, t22])
    b3 = BatchNode("batch3", [b1, b2])
    b3.scan()
    #print(vars(b3))

    ws = WorkSession("worker", "project", b3)
    ws.root_node = b3
    ns = None
    while (ns := ws.get_next_template_node_session(ns)):
        print("######", ns.node.name)
        time.sleep(0.1)
    else:
        ws.finish()

    ns = ws.root_ns
    while ns:
        print(ns.id, ns.node.name)
        ns = ns.next
