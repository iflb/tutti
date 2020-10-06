import csv

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()["Nanotasks"]

    def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        command = event.data[0]
        project_name = event.data[1]
        template_name = event.data[2]
        ans = {}
        ans["Command"] = command
        ans["Project"] = project_name
        ans["Template"] = template_name
        try:
            if command=="NANOTASKS":
                data = []
                for d in self.db["{}.{}".format(project_name, template_name)].find():
                    d["_id"] = str(d["_id"])
                    data.append(d)
                ans["Nanotasks"] = data
            elif command=="COUNT":
                count = self.db["{}.{}".format(project_name, template_name)].count()
                ans["Count"] = count
            ans["Status"] = "success"
        except Exception as e:
            ans["Status"] = "error"
            ans["Reason"] = str(e)

        return ans
