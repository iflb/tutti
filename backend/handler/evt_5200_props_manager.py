from datetime import datetime
import os
import sys
import asyncio
from asyncio.subprocess import PIPE
import random, string
import json
import csv
import copy
import itertools
import glob
import importlib.util

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

from handler import paths, common

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()["nanotasks"]

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    def save_nanotasks(self, iterable, project_name, template_name, **meta):
        def add_meta(props):
            return {
                "tag": meta["tag"],
                "#assignable": meta["num_assignments"],
                "priority": meta["priority"],
                "props": props
            }

        res = self.db.get_collection("{}.{}".format(project_name, template_name)).insert_many([add_meta(props) for props in iterable])
        return res.inserted_ids

    async def handle(self, event):
        command = event.data[0]
        project_name = event.data[1]
        template_name = event.data[2]
        tag = event.data[3]

        ans = {}

        if command=="add_csv":
            with open(paths.template_dirpath(project_name, template_name) / (tag+".csv"), "r") as f:
                try:
                    inserted_ids = self.save_nanotasks(csv.DictReader(f), project_name, template_name, tag=tag, num_assignments=3, priority=0)
                    ans["Status"] = "success"
                    ans["NumInserted"] = len(inserted_ids)
                except Exception as e:
                    ans["Status"] = "error"
                    ans["Reason"] = str(e)
            return ans
