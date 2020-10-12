import boto3
import json
import datetime

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
        client = self.mturk.get_client()
        
        output.set("AccountBalance", client.get_account_balance())
