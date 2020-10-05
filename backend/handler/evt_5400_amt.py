import boto3

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
        self.boto_client = boto3.client('mturk',
                                        aws_access_key_id = "AKIAJRUGUST5H75E255Q",
                                        aws_secret_access_key = "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",
                                        region_name = "us-east-1",
                                        endpoint_url = endpoint_url)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        command = event.data[0]
        project_name = event.data[1]
        options = event.data[2:]

        ans = {}
        ans["Command"] = command
        ans["Status"] = "success"
        try:
            if command=="create_hits":
                num = options[0]
                is_prod_mode = (options[1]=="production")


        except Exception as e:
            ans["Status"] = "error"
            ans["Reason"] = e.args

        return ans
