import random, string
import json
import copy
import importlib.util
from importlib import reload
import heapq
import inspect
import pickle
import sys
import os

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import common
from libs.session import WorkSession

import redis
r = redis.Redis(host="localhost", port=6379, db=0)

from pymongo import MongoClient
from datetime import datetime

class Nanotask:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def get(self, attr):
        return getattr(self, attr)

class PriorityNanotaskSet:
    def __init__(self):
        self._heap = []
        self._set = set()

    def __repr__(self):
        return "<PriorityNanotaskSet {}>".format(str(self._heap))

    def add(self, item, priority):
        if not item in self._set:
            heapq.heappush(self._heap, (priority, item))
            self._set.add(item)

    def pop(self):
        priority, item = heapq.heappop(self._heap)
        self._set.remove(item)
        return item 

class DCStruct:   # lame
    def __init__(self):
        self.data_all = {}

    def __repr__(self):
        return "<DCStruct {}>".format(json.dumps(self.data_all, indent=4, default=lambda o: repr(o)))

    def exists(self, project_name=None, template_name=None, nanotask_id=None):
        if not template_name:
            return project_name in self.data_all
        if not nanotask_id:
            return (project_name in self.data_all) and (template_name in self.data_all[project_name])

        return (project_name in self.data_all) and (template_name in self.data_all[project_name]) and (nanotask_id in self.data_all[project_name][template_name])

    def add(self, data, project_name, template_name=None, nanotask_id=None):
        pn, tn, nid = project_name, template_name, nanotask_id
        if tn==None:
            self.data_all[pn] = data
            return
        else:
            if pn not in self.data_all:  self.data_all[pn] = {}
            if nid==None:
                self.data_all[pn][tn] = data
                return
            else:
                if tn not in self.data_all[pn]:  self.data_all[pn][tn] = {}
                self.data_all[pn][tn][nid] = data
                
    def get(self, project_name=None, template_name=None, nanotask_id=None):
        pn, tn, nid = project_name, template_name, nanotask_id
        try:
            if nid:   return self.data_all[pn][tn][nid]
            elif tn:  return self.data_all[pn][tn]
            elif pn:  return self.data_all[pn]
            else:     return self.data_all
        except KeyError:
            return None

    def delete(self, project_name=None, template_name=None, nanotask_id=None):
        pn, tn, nid = project_name, template_name, nanotask_id
        if nid:   del self.data_all[pn][tn][nid]
        elif tn:  del self.data_all[pn][tn]
        elif pn:  del self.data_all[pn]
        else:     del self.data_all

    def project_names(self):
        return self.data_all.keys()

    def template_names(self, project_name):
        return self.data_all[project_name].keys()

    def nanotask_ids(self, project_name, template_name):
        return self.data_all[project_name][template_name].keys()


class TaskSession:
    def __init__(self, worker_id, engine=None):
        self.id = self._generate_id()
        self.worker_id = worker_id
        self.engine = engine

    def _generate_id(self):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])

    def get_engine(self):
        return self.engine

from typing import Dict, Set

class DCModel:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def list_projects(self):
        return self.projects.keys()

    def add_project(self, project):
        self.projects[project.name] = project
        return project

    def get_project(self, name):
        return self.projects[name] if (name in self.projects) else None

class Project:
    def __init__(self, name):
        self.name = name
        self.templates: Dict[str, Template] = {}

    def list_templates(self):
        return self.templates.keys()

    def add_template(self, template):
        self.templates[template.name] = template
        return template

    def get_template(self, name):
        return self.templates[name] if (name in self.templates) else None
            

class Template:
    def __init__(self, name):
        self.name = name
        self.nids = set()

    def has_nanotasks(self):
        return len(self.nids)>0

    def add_nanotask_ids(self, nids: Set[str]):
        self.nids = self.nids | nids
        return self.nids


class TaskQueue:
    def __init__(self):
        self.queue_all = {}  # wid -> project_name -> template_name -> heapq

    def get_queue(self, wid, pn, tn):
        try:
            return self.queue_all[wid][pn][tn]
        except:
            try: self.queue_all[wid]
            except: self.queue_all[wid] = {}

            try: self.queue_all[wid][pn]
            except: self.queue_all[wid][pn] = {}

            try: self.queue_all[wid][pn][tn]
            except:
                self.queue_all[wid][pn][tn] = []
                heapq.heapify(self.queue_all[wid][pn][tn])
            
            return self.queue_all[wid][pn][tn]

    def push(self, queue, nid, priority):
        heapq.heappush(queue, (priority, nid))

    def get_first(self, queue):
        try:    return queue[0][1]
        except: return None

    def pop(self, queue):
        try:    return heapq.heappop(queue)[1]
        except: return None


class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.flows = self.load_flows()   # {project_name: TaskFlow}
        self.wsessions = {}               # {session_id: iterator}
        self.db = MongoClient()

        self.dcmodel = DCModel()
        self.nt_memory = {}                     # { nid: Nanotask }
        self.g_assignable = set()               # set(nid)
        self.tqueue = TaskQueue()
        self.w_submitted = {}                   # worker_id -> set(nanotask_id)

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        self.create_nanotask_memory()

        return handler_spec

    def create_nanotask_memory(self):
        self.cache_nanotasks()
        self.update_assignability()

    def cache_nanotasks(self):
        nt_memory = self.nt_memory
        g_assignable = self.g_assignable

        for pn in common.get_projects():
            prj = self.dcmodel.add_project(Project(pn))
            for tn in common.get_templates(pn):
                prj.add_template(Template(tn))

        _db = self.db["nanotasks"]
        for cn in _db.list_collection_names(filter=None):
            [pn, tn] = [project_name, template_name] = cn.split(".")

            nids = set()
            for nt in _db[cn].find():
                nid = nt["_id"] = str(nt["_id"])
                nids.add(nid)
                nt["project_name"] = pn
                nt["template_name"] = tn
                nt["num_remaining"] = nt["num_assignable"]
                nt_memory[nid] = Nanotask(**nt)
                g_assignable.add(nid)
            self.dcmodel.get_project(pn).get_template(tn).add_nanotask_ids(nids)

    def create_task_queue_for_worker(self, wid):
        _w_assignable = self.g_assignable - self.w_submitted[wid]
        for nid in _w_assignable:
            nt = self.nt_memory[nid]
            pn = nt.get("project_name")
            tn = nt.get("template_name")
            q = self.tqueue.get_queue(wid, pn, tn)
            self.tqueue.push(q, nid, nt.priority)

    def update_assignability(self):
        nt_memory = self.nt_memory
        g_assignable = self.g_assignable
        w_submitted = self.w_submitted
        tqueue = self.tqueue

        _db = self.db["answers"]
        for cn in _db.list_collection_names(filter=None):
            #try:
            #    [pn, tn, nid] = [project_name, template_name, nanotask_id] = cn.split(".")
            #except ValueError: 
            #    [pn, tn] = [project_name, template_name] = cn.split(".")
            #    nid = None
            nsid = cn
            ns_bin = r.get(self.namespace_redis.key_for_node_session_by_id(nsid))
            ns = pickle.loads(ns_bin)
            pn = ns.ws.pid
            tn = ns.node.name
            nid = ns.nid

            _n_answers = _db[cn].find()
            prj = self.dcmodel.get_project(pn)
            if prj is not None:
                tmpl = prj.get_template(tn)
                if tmpl is None:
                    logger.error("template '{}' in project '{}' is not found in memory".format(tn, pn))
                elif tmpl.has_nanotasks():
                    nt = nt_memory[nid]
                    nt.num_remaining -= _n_answers.count()
                    if nt.num_remaining<=0:  g_assignable.remove(nid)

                for a in _n_answers:
                    wid = a["WorkerId"]
                    if wid not in w_submitted:  w_submitted[wid] = set()
                    if nid: w_submitted[wid].add(nid)
            else:
                logger.error("project '{}' is not found in memory".format(pn))

        for wid in w_submitted.keys():
            self.create_task_queue_for_worker(wid)

    def get_flow(self, project_name):
        mod_flow = importlib.import_module("projects.{}.flow".format(project_name))
        importlib.reload(mod_flow)
        flow = mod_flow.TaskFlow()
        return flow

    def load_flows(self):
        flows = {}
        for project_name in common.get_projects():
            try:
                flows[project_name] = self.get_flow(project_name)
            except Exception as e:
                logger.error("could not load flow for {}, {}".format("projects.{}.flow".format(project_name), str(e)))
                continue   
        return flows

    def get_batch_info(self, child):
        if child.is_batch():
            _info = []
            for c in child.children:
                _info.append(self.get_batch_info(c))
            return {
                "name": child.name,
                "statement": child.statement.value,
                "cond": child.cond,
                "skippable": child.skippable,
                "children": _info
            }
        elif child.is_template():
            return {
                "statement": child.statement.value,
                "cond": child.cond,
                "skippable": child.skippable,
                "name": child.name
            }

    async def handle(self, event):

        command = event.data[0]
        ans = {}
        ans["Command"] = command
        ans["Status"] = "success"

        try:
            if command=="GET_FLOWS":
                pn = event.data[1]

                flow = self.get_flow(pn)
                info = self.get_batch_info(flow.root)
                ans["Flow"] = info


            elif command=="LOAD_FLOW":
                pn = event.data[1]

                flow = self.get_flow(pn)
                info = self.get_batch_info(flow.root)
                ans["Flow"] = info

                self.flows[pn] = flow


            elif command=="CREATE_SESSION":    # フローをワーカーが開始するごとに作成
                [pn, wid] = event.data[1:]

                if wid not in self.w_submitted:
                    self.w_submitted[wid] = set()
                    self.create_task_queue_for_worker(wid)

                flow = self.flows[pn]
                flow.root.scan()
                ws = self.wsessions[ws.id] = WorkSession(wid, pn, flow.root)
                ans["WorkSessionId"] = ws.id
                

            elif command=="GET":
                def get_neighboring_template_node_session(ns, direction):
                    while out_ns := getattr(ns, direction):
                        if out_ns.node.is_template():
                            return out_ns
                        else:
                            ns = out_ns
                    return None
                
                [target, wsid, nsid] = event.data[1:]

                if wsid not in self.wsessions:  raise Exception("No session found")

                ws = self.wsessions[wsid]
                wid = ws.wid
                pn = ws.pid

                ns = None
                if len(nsid)>0 and not (ns := ws.get_existing_node_session(nsid)):
                    raise Exception(f"Invalid node session ID: {nsid}")

                if ns:
                    [name, id] = [ns.node.name, ns.id]
                    [p_name, p_id] = [ns.prev.node.name, ns.prev.id]
                    [n_name, n_id] = [ns.next.node.name, ns.next.id] if ns.next else [None, None]
                    logger.info(f"IN:: {name}({id}), prev={p_name}({p_id}), next={n_name}({n_id})")

                if target=="NEXT":
                    if ns is not None and (out_ns := get_neighboring_template_node_session(ns, "next")):  # if next node session exists
                        if out_ns != ws.get_existing_node_session(out_ns.id):
                            raise Exception("Broken consistency of node sessions in work session")
                        ans["NodeSessionId"] = out_ns.id
                        ans["Template"] = tn = out_ns.node.name
                        ans["Answers"] = out_ns.answers
                        ans["NanotaskId"] = out_ns.nid
                        if out_ns.nid is not None:
                            ans["Props"] = self.nt_memory[out_ns.nid].props
                    else:   # create new next node session
                        try:
                            if not (out_ns := ws.create_next_template_node_session(ns)):
                                raise StopIteration()
                            ans["NodeSessionId"] = out_ns.id
                            ans["Template"] = tn = out_ns.node.name
                            tmpl = self.dcmodel.get_project(pn).get_template(tn)
                            if tmpl.has_nanotasks():
                                q = self.tqueue.get_queue(wid, pn, tn)
                                if len(q)>0:
                                    nid = self.tqueue.pop(q)
                                    out_ns.update_attr("nid", nid)
                                    nt = self.nt_memory[nid]
                                    ans["IsStatic"] = False
                                    ans["NanotaskId"] = nid
                                    ans["Props"] = nt.props
                                else:
                                    ans["NanotaskId"] = None
                            else:
                                ans["IsStatic"] = True

                        except StopIteration as e:
                            ans["NextTemplate"] = None

                elif target=="PREV":
                    out_ns = get_neighboring_template_node_session(ns, "prev")
                    if out_ns != ws.get_existing_node_session(out_ns.id):
                        raise Exception("Broken consistency of node sessions in work session")
                    
                    ans["NodeSessionId"] = out_ns.id
                    ans["Template"] = tn = out_ns.node.name
                    ans["Answers"] = out_ns.answers
                    if (nid := out_ns.nid):
                        ans["IsStatic"] = False
                        ans["Props"] = self.nt_memory[nid].props
                    else:
                        ans["IsStatic"] = True
                    ans["NanotaskId"] = nid

                if out_ns:
                    [name, id] = [out_ns.node.name, out_ns.id]
                    [p_name, p_id] = [out_ns.prev.node.name, out_ns.prev.id]
                    [n_name, n_id] = [out_ns.next.node.name, out_ns.next.id] if out_ns.next else [None, None]
                    logger.info(f"OUT:: {name}({id}), prev={p_name}({p_id}), next={n_name}({n_id})")

                    ans["HasPrevTemplate"] = (get_neighboring_template_node_session(out_ns, "prev") is not None)
                    ans["HasNextTemplate"] = (get_neighboring_template_node_session(out_ns, "next") is not None)

                        
            elif command=="ANSWER":
                [wsid, nsid] = event.data[1:3]

                ### FIXME
                answers = json.loads(" ".join(event.data[3:]))

                ws = self.wsessions[wsid]
                wid = ws.wid
                pn = ws.pid

                if nsid=="":
                    raise Exception(f"node session ID cannot be null")

                ns = ws.get_existing_node_session(nsid)
                tn = ns.node.name
                nid = ns.nid

                ns.answers = answers

                self.w_submitted[wid].add(nid)
                ans_json = {
                    "WorkSessionId": wsid,
                    "NodeSessionId": nsid,
                    "WorkerId": wid,
                    "Answers": answers,
                    "Timestamp": datetime.now()
                }
                if nid!="null":  ans_json["NanotaskId"] = nid
                self.db["answers"][nsid].insert_one(ans_json)
                ans["SentAnswer"] = answers


            else:
                raise Exception("unknown command '{}'".format(command))


        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ans["Status"] = "error"
            ans["Reason"] = f"{str(e)} [{fname} (line {exc_tb.tb_lineno})]"
            
        return ans
