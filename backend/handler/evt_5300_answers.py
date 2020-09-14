import time

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

from handler import paths, common

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        command = event.data[0]
        project_name = event.data[1]
        template_name = event.data[2]

        ans = {}
        ans["Command"] = command
        ans["Status"] = "success"
        try:
            if command=="get":
                names = self.db.answers.list_collection_names()
                names = [name for name in names if name.startswith("{}.{}".format(project_name, template_name))]
                answers = []
                for name in names:
                    answer = self.db.answers[name].find({})
                    for a in answer:
                        a["_id"] = str(a["_id"])
                        if "timestamp" in a:
                            a["timestamp"] = time.mktime(a["timestamp"].timetuple())
                        answers.append(a)
                    logger.debug(answers)
                ans["Answers"] = answers
                logger.debug(answers)

        except Exception as e:
            ans["Status"] = "error"
            ans["Reason"] = e.args

        return ans
