import time
import os

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mongo = self.namespace_mongo.get_db()

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        [command, pn, tn] = event.data

        output.set("Command", command)

        if command=="get":
            aids = await self.namespace_redis.get_answer_ids_for_project_name_template_name(event.session.redis, pn, tn)
            answers = self.mongo[self.namespace_mongo.CLCT_NAME_ANSWER].find(filter={"_id":{"$in":self.namespace_mongo.wrap_obj_id(aids)}})
            answers = self.namespace_mongo.unwrap_obj_id(list(answers))
            [a.update({"Timestamp": time.mktime(a["Timestamp"].timetuple())}) for a in answers]
            output.set("Answers", answers)
