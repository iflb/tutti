from datetime import datetime
import os
import sys
import asyncio
from asyncio.subprocess import PIPE
import random, string
import json
import copy
import itertools
import glob
import importlib.util
import heapq

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from libs.flowlib import Engine, is_batch, is_node


from pymongo import MongoClient

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
        if nid:   return self.data_all[pn][tn][nid]
        elif tn:  return self.data_all[pn][tn]
        elif pn:  return self.data_all[pn]
        else:     return self.data_all

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


class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.flows = self.load_flows()   # {project_name: Engine}
        self.sessions = {}               # {session_id: iterator}
        self.db = MongoClient()

        self.nt_memory = DCStruct()             # DCStruct(project_name -> template_name -> nanotask_id) -> {nanotask}
        self.assignables_priority = DCStruct()  # DCStruct(project_name -> template_name -> nanotask_id) -> int(priority)
        self.w_assignables = {}                 # worker_id -> DCStruct(project_name -> template_name) -> PriorityNanotaskSet({nanotask_id})

        self.create_nanotask_memory()    

    def create_nanotask_memory(self):
        self.cache_nanotasks()
        self.update_assignability()

        logger.debug(self.w_assignables)

    def cache_nanotasks(self):
        nt_memory = self.nt_memory
        assignables_priority = self.assignables_priority

        _db = self.db["nanotasks"]
        for cn in _db.list_collection_names(filter=None):
            [pn, tn] = [project_name, template_name] = cn.split(".")

            for nt in _db[cn].find():
                nid = nanotask_id = str(nt["_id"])
                nt["#remaining"] = nt["#assignable"]
                nt_memory.add(nt, pn, tn, nid)
                assignables_priority.add(nt_memory.get(pn,tn,nid)["priority"], pn, tn, nid)

    def update_assignability(self):
        nt_memory = self.nt_memory
        assignables_priority = self.assignables_priority
        submitted_nids = {}

        _db = self.db["answers"]
        for cn in _db.list_collection_names(filter=None):
            [pn, tn, nid] = [project_name, template_name, nanotask_id] = cn.split(".")
            _n_answers = _db[cn].find()

            try:     mem = nt_memory.get(pn, tn, nid)
            except:  logger.debug("{}.{}.{} was not found in nanotask memory".format(pn, tn, nid))

            mem["#remaining"] -= _n_answers.count()
            if mem["#remaining"]<=0:  assignables_priority.delete(pn, tn, nid)

            for a in _n_answers:
                #wid = a["workerId"]
                wid = a["sessionId"]
                if wid not in submitted_nids:
                    submitted_nids[wid] = DCStruct()
                    submitted_nids[wid].add(set(), pn, tn)
                submitted_nids[wid].get(pn, tn).add(nid)

        w_assignables = self.w_assignables
        for wid in submitted_nids.keys():
            for pn in submitted_nids[wid].project_names():
                for tn in submitted_nids[wid].template_names(pn):
                    _t_assignables_priority = copy.copy(assignables_priority.get(pn,tn))
                    for nid in submitted_nids[wid].get(pn, tn):
                        del _t_assignables_priority[nid]

                    if wid not in w_assignables:  w_assignables[wid] = DCStruct()
                    _set = PriorityNanotaskSet()
                    for nid, pr in _t_assignables_priority.items():  _set.add(nid, pr)
                    w_assignables[wid].add(_set, pn, tn)


    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    def load_flows(self):
        flows = {}
        for project_name in common.get_projects():
            try:
                mod_flow = importlib.import_module("projects.{}.flow".format(project_name))
                flow = mod_flow.TaskFlow()
                flow.define()
                flows[project_name] = flow.batch_all
            except Exception as e:
                logger.debug("{}, {}".format("projects.{}.flow".format(project_name), str(e)))
                continue   
        return flows

    async def handle(self, event):

        command = event.data[0]
        ans = {}
        ans["Command"] = command

        if command=="GET_FLOWS":
            project_name = event.data[1]
            try:
                flow = self.flows[project_name]
                engine = Engine(project_name, flow)
                log = ""
                for elm in engine.test_generator():
                    if is_batch(elm):   log += "entering batch {}\n".format(elm.tag)
                    elif is_node(elm):  log += "--> executing node {}\n".format(elm.tag)
                ans["Status"] = "success"
                ans["Flow"] = log
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)

        elif command=="CREATE_SESSION":    # フローをワーカーが開始するごとに作成
            project_name = event.data[1]
            try:
                session_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
                self.sessions[session_id] = Engine(project_name, self.flows[project_name])
                ans["Status"] = "success"
                ans["SessionId"] = session_id
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)
                
        elif command=="GET":
            session_id = event.data[1]

            try:
                if session_id in self.sessions:
                    session = self.sessions[session_id]
                    template_name = session.get_next_template()
                    ans["NextTemplate"] = template_name
                    nanotask = self.db["nanotasks"].get_collection("{}.{}".format(session.project_name, template_name)).find_one()
                    self.db["answers"].get_collection("{}.{}.{}".format(session.project_name, template_name, nanotask["_id"])).insert_one({"sessionId": session_id, "answers": None})
                    ans["Props"] = nanotask["props"]
                    ans["Status"] = "success"
                else:
                    ans["Status"] = "error"
                    ans["Reason"] = "No session found"
            except StopIteration as e:
                ans["Status"] = "success"
                ans["NextTemplate"] = None
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)

        else:
            ans["Status"] = "error"
            ans["Reason"] = "unknown command '{}'".format(command)
        return ans
