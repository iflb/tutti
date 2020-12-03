from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler.handler_output import handler_output
from handler.redis_index import *

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.hits = []

    def setup(self, handler_spec, manager):
        self.mturk = manager.load_helper_module('helper_mturk')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        command = event.data["Command"]
        output.set("Command", command)

        if command=="SetCredentials":
            access_key_id = event.data["AccessKeyId"]
            secret_access_key = event.data["SecretAccessKey"]
            if not (is_sandbox := event.data["IsSandbox"]):
                is_sandbox = 1

            async with await self.mturk.get_client_async(event.session.redis, access_key_id=access_key_id, secret_access_key=secret_access_key, sandbox=is_sandbox) as client:
                ret = await client.get_account_balance()
                await event.session.redis.execute("SET", key_mturk_access_key_id(), access_key_id)
                await event.session.redis.execute("SET", key_mturk_secret_access_key(), secret_access_key)
                await event.session.redis.execute("SET", key_mturk_is_sandbox(), is_sandbox)
                output.set("AccessKeyId", access_key_id)
                output.set("SecretAccessKey", secret_access_key)
                output.set("IsSandbox", is_sandbox)
                output.set("AccountBalance", ret)

        elif command=="GetCredentials":
            output.set("AccessKeyId", await event.session.redis.execute("GET", key_mturk_access_key_id()))
            output.set("SecretAccessKey", await event.session.redis.execute("GET", key_mturk_secret_access_key()))
            output.set("IsSandbox", await event.session.redis.execute("GET", key_mturk_is_sandbox()))
            async with await self.mturk.get_client_async(event.session.redis) as client:
                ret = await client.get_account_balance()
                output.set("AccountBalance", ret)

        elif command=="SetSandboxMode":
            is_sandbox = event.data["Enabled"]
            if is_sandbox:  is_sandbox = 1
            await event.session.redis.execute("SET", key_mturk_is_sandbox(), is_sandbox)
            output.set("IsSandbox", is_sandbox)

        elif command=="ResetAuthorization":
            await event.session.redis.execute("DEL", key_mturk_access_key_id())
            await event.session.redis.execute("DEL", key_mturk_secret_access_key())
            await event.session.redis.execute("DEL", key_mturk_is_sandbox())
