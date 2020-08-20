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

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from libs.flowlib import Engine, is_batch, is_node

class MyIterator():
    def __init__(self, profile):
        self.profile = profile
        self._tidx = 0
        self._ridx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._tidx==len(self.profile):  raise StopIteration()

        template = self.profile[self._tidx]
        self._ridx += 1
        if self._ridx==self.profile[self._tidx]["repeat_times"]:
            self._tidx += 1
            self._ridx = 0
        return template

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.profiles = {}    # {project_name: profile}
        self.sessions = {}    # {session_id: iterator}
        self.flows = self.load_flows()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    def get_existing_profiles(self):
        for project_name in common.get_projects():
            profile_path = paths.project_profile_path(project_name)
            if os.path.exists(profile_path):
                with open(profile_path, "r") as f:
                    profile = f.read()
                    profile_json = json.loads(profile)
                    self.profiles[project_name] = profile_json

    def load_flows(self):
        flows = {}
        for project_name in common.get_projects():
            try:
                mod_flow = importlib.import_module("projects.{}.flow".format(project_name))
                flow = mod_flow.TaskFlow()
                flow.define()
                flows[project_name] = flow.batch_all
            except Exception as e:
                #logger.debug("{}, {}".format("projects.{}.flow".format(project_name), str(e)))
                continue   
        return flows

    async def handle(self, event):

        command = event.data[0]
        ans = {}
        ans["Command"] = command

        if len(self.profiles.keys())==0:  self.get_existing_profiles()

        if command=="REGISTER_SM":    # ナノタスクフローの定義。ワーカー数によらず１回のみでよい
            project_name = event.data[1]
            profile = event.data[2]
            
            try:
                profile_json = json.loads(profile)
                with open(paths.project_profile_path(project_name), "w") as f:
                    f.write(json.dumps(profile_json, indent=4))
                self.profiles[project_name] = profile_json
                ans["Status"] = "success"
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)





        elif command=="GET_FLOWS":
            project_name = event.data[1]
            try:
                flow = self.flows[project_name]
                engine = Engine(flow)
                log = ""
                for elm in engine.test_generator():
                    if is_batch(elm):   log += "entering batch {}\n".format(elm.tag)
                    elif is_node(elm):  log += "--> executing node {}\n".format(elm.tag)
                ans["Status"] = "success"
                ans["Flow"] = log
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)







        elif command=="GET_SM_PROFILE":
            project_name = event.data[1]

            try:
                profile = self.profiles[project_name]
                ans["Status"] = "success"
                ans["Profile"] = profile
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)

        elif command=="CREATE_SESSION":    # フローをワーカーが開始するごとに作成
            project_name = event.data[1]



            try:
                session_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
                self.sessions[session_id] = Engine(self.flows[project_name])
                ans["Status"] = "success"
                ans["SessionId"] = session_id
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)
                

            ## TODO:: what if duplicate?
            #try:
            #    session_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
            #    self.sessions[session_id] = iterator
            #    ans["Status"] = "success"
            #    ans["SessionId"] = session_id
            #except Exception as e:
            #    ans["Status"] = "error"
            #    ans["Reason"] = str(e)

        elif command=="GET":
            session_id = event.data[1]

            try:
                if session_id in self.sessions:
                    session = self.sessions[session_id]
                    ans["NextTemplate"] = session.get_next_template()
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
