import csv
import os
import json

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mongo = self.namespace_mongo.get_db()

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
            "project_name": pn,
            "template_name": tn,
            "tag": event.data["tag"],
            "num_assignable": event.data["numAssignable"],
            "priority": event.data["priority"]
        }
        res = self.mongo[self.namespace_mongo.CLCT_NAME_NANOTASK].insert_many([dict(data, **{"props": props}) for props in event.data["props"]])
        inserted_ids = res.inserted_ids

        for i,props in enumerate(event.data["props"]):
            await event.session.redis.execute("SET", self.namespace_redis.key_nano_props(i), json.dumps(props))
        await self.namespace_redis.add_nanotask_ids(event.session.redis, pn, tn, self.namespace_mongo.unwrap_obj_id(inserted_ids))
        output.set("NumInserted", len(inserted_ids))
