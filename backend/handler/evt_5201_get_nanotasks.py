import csv

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()["nanotasks"]

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
        ans["Project"] = project_name
        ans["Template"] = template_name
        ans["Status"] = "success"
        ans["Command"] = command
        ans["Count"] = 10
        return ans
    
        try:
            project_name = event.data["projectName"]
            template_name = event.data["templateName"]
            data = {
                "tag": event.data["tag"],
                "num_assignable": event.data["numAssignable"],
                "priority": event.data["priority"]
            }
            res = self.db.get_collection("{}.{}".format(project_name, template_name)).insert_many([dict(data, **{"props": props}) for props in event.data["props"]])
            inserted_ids = res.inserted_ids
            ans["Status"] = "success"
            ans["NumInserted"] = len(inserted_ids)
        except Exception as e:
            ans["Status"] = "error"
            ans["Reason"] = str(e)

        return ans
