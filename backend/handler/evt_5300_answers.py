import time

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()

    def setup(self, handler_spec, manager):
        self.namespace_mongo = manager.load_helper_module('helper_mongo_namespace')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        [command, pn, tn] = event.data

        output.set("Command", command)

        dn = self.namespace_mongo.db_name_for_answers()
        cn = self.namespace_mongo.collection_name_for_answers(pn, tn)

        if command=="get":
            _names = self.db[dn].list_collection_names()
            names = [name for name in _names if name.startswith(cn)]
            answers = []
            for name in names:
                answer = self.db[dn][name].find({})
                for a in answer:
                    a["_id"] = str(a["_id"])
                    if "Timestamp" in a:
                        a["Timestamp"] = time.mktime(a["Timestamp"].timetuple())
                    answers.append(a)
            output.set("Answers", answers)
