from datetime import datetime
import os
import asyncio
from asyncio.subprocess import PIPE
import random, string
import json
import copy
import itertools
import glob

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common

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
        self.profiles = {}    # project_name: profile
        self.sessions = {}    # session_id: iterator

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def get_existing_profiles(self):
        for project_name in await common.get_projects():
            profile_path = paths.project_profile_path(project_name)
            if os.path.exists(profile_path):
                with open(profile_path, "r") as f:
                    profile = f.read()
                    profile_json = json.loads(profile)
                    self.profiles[project_name] = profile_json

    async def handle(self, event):

        command = event.data[0]
        ans = {}
        ans["Command"] = command

        if len(self.profiles.keys())==0:  await self.get_existing_profiles()

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

            # TODO:: what if duplicate?
            try:
                session_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
                iterator = MyIterator(self.profiles[project_name])
                self.sessions[session_id] = iterator
                ans["Status"] = "success"
                ans["SessionId"] = session_id
            except Exception as e:
                ans["Status"] = "error"
                ans["Reason"] = str(e)

        elif command=="GET":
            session_id = event.data[1]

            try:
                if session_id in self.sessions:
                    ans["NextTemplate"] = next(self.sessions[session_id])
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
