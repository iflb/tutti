import boto3
import json
from pprint import pprint

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import redis
r = redis.Redis(host="localhost", port=6379, db=0)

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mturk = manager.load_helper_module('helper_mturk')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        client = self.mturk.get_client(sandbox=False)

        command = event.data[0]

        if command=="list":
            next_token = None
            quals = []
            while True:
                kwargs = {
                    "MustBeRequestable": False,
                    "MustBeOwnedByCaller": True
                }
                if next_token:  kwargs["NextToken"] = next_token
                res = client.list_qualification_types(**kwargs)

                quals.extend([self.mturk.datetime_to_unixtime(q) for q in res["QualificationTypes"]])
                if "NextToken" in res:
                    next_token = res["NextToken"]
                    continue
                else:
                    break
            output.set("QualificationTypes", quals)

        elif command=="create":
            params = json.loads(event.data[1])
            res = client.create_qualification_type(**params)
            output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

        elif command=="update":
            params = json.loads(event.data[1])
            res = client.update_qualification_type(**params)
            output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

        elif command=="get":
            qid = event.data[1]
            res = client.get_qualification_type(QualificationTypeId=qid)
            output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

        elif command=="delete":
            qid = event.data[1]
            client.delete_qualification_type(QualificationTypeId=qid)
