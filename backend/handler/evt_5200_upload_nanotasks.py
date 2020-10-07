import csv

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        pn = event.data["projectName"]
        tn = event.data["templateName"]
        output.set("Project", pn)
        output.set("Template", tn)

        data = {
            "tag": event.data["tag"],
            "num_assignable": event.data["numAssignable"],
            "priority": event.data["priority"]
        }
        dn = self.namespace_mongo.db_name_for_nanotasks()
        cn = self.namespace_mongo.collection_name_for_nanotasks(pn,tn)
        res = self.db[dn][cn].insert_many([dict(data, **{"props": props}) for props in event.data["props"]])
        inserted_ids = res.inserted_ids
        output.set("NumInserted", len(inserted_ids))
