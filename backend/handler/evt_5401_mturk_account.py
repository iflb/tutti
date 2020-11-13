import boto3
import json
import datetime

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

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
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        key_mturk_access_key_id = self.namespace_redis.key_mturk_access_key_id()
        key_mturk_secret_access_key = self.namespace_redis.key_mturk_secret_access_key()
        command = event.data[0]
        if command=="get":
            pass
        elif command=="set":
            access_key_id = event.data[1]
            secret_access_key = event.data[2]
            await event.session.redis.execute("SET", key_mturk_access_key_id, access_key_id)
            await event.session.redis.execute("SET", key_mturk_secret_access_key, secret_access_key)
        elif command=="remove":
            await event.session.redis.execute("DEL", key_mturk_access_key_id)
            await event.session.redis.execute("DEL", key_mturk_secret_access_key)
        else:
            raise CommandError(command)

        try:    access_key_id = await event.session.redis.execute_str("GET", key_mturk_access_key_id)
        except: access_key_id = None
        try:    secret_access_key = await event.session.redis.execute_str("GET", key_mturk_secret_access_key)
        except: secret_access_key = None

        output.set("AccessKeyId", access_key_id)
        output.set("SecretAccessKey", secret_access_key)
