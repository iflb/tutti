import csv
import os

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from bson.objectid import ObjectId

from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.path = manager.load_helper_module('paths')
        self.mongo = self.namespace_mongo.get_db()

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        [command, pn, tn] = event.data
        output.set("Command", command)
        output.set("Project", pn)
        output.set("Template", tn)

        nids = await self.namespace_redis.get_nanotask_ids_for_project_name_template_name(event.session.redis, pn, tn)

        if command=="NANOTASKS":
            data = self.mongo[self.namespace_mongo.CLCT_NAME_NANOTASK].find(filter={"_id":{"$in":self.namespace_mongo.wrap_obj_id(nids)}})
            output.set("Nanotasks", self.namespace_mongo.unwrap_obj_id(list(data)))
        elif command=="COUNT":
            output.set("Count", len(nids))
