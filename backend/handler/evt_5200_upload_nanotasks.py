import csv
import os
import json

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

from handler.redis_resource import NanotaskResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mongo = self.namespace_mongo.get_db()
        self.res_nanotask = NanotaskResource(manager.redis)

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
            "ProjectName": pn,
            "TemplateName": tn,
            "Tag": event.data["tag"],
            "num_assignable": event.data["numAssignable"],
            "priority": event.data["priority"]
        }

        #res = self.mongo[self.namespace_mongo.CLCT_NAME_NANOTASK].insert_many([dict(data, **{"props": props}) for props in event.data["props"]])
        #inserted_ids = res.inserted_ids

        for props in event.data["props"]:
            await self.res_nanotask.add(dict(data, **{"props": props}))
        output.set("NumInserted", len(event.data["props"]))
