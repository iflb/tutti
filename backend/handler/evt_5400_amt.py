from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from botocore.exceptions import NoCredentialsError

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler.handler_output import handler_output
from handler.redis_index import *
from handler.redis_resource import MTurkResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.hits = []

    def setup(self, handler_spec, manager):
        self.mturk = manager.load_helper_module('helper_mturk')
        self.r_mt = MTurkResource(manager.redis)
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        command = event.data["Command"]
        output.set("Command", command)

        if command=="SetCredentials":
            aki = event.data["AccessKeyId"]
            sak = event.data["SecretAccessKey"]
            if "IsSandbox" not in event.data:  sandbox = True

            async with await self.mturk.get_client_async(event.session.redis, access_key_id=aki, secret_access_key=sak, sandbox=sandbox) as client:
                ret = await client.get_account_balance()  # here throws error if credentials are invalid
                await self.r_mt.set_credentials(aki, sak, sandbox)

                output.set("AccessKeyId", aki)
                output.set("SecretAccessKey", sak)
                output.set("IsSandbox", sandbox)
                output.set("AccountBalance", ret)

        elif command=="GetCredentials":
            [aki, sak, sandbox] = await self.r_mt.get_credentials()
            output.set("AccessKeyId", aki)
            output.set("SecretAccessKey", sak)
            output.set("IsSandbox", sandbox)

            async with await self.mturk.get_client_async(event.session.redis) as client:
                try:
                    ret = await client.get_account_balance()
                    output.set("AccountBalance", ret)
                except NoCredentialsError:
                    return

        elif command=="SetSandboxMode":
            is_sandbox = event.data["Enabled"]
            await self.r_mt.set_is_sandbox(is_sandbox)
            output.set("IsSandbox", is_sandbox)
    
        elif command=="ResetAuthorization":
            await self.r_mt.remove_credentials()
