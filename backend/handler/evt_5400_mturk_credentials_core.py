from datetime import datetime

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from botocore.exceptions import NoCredentialsError

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler.handler_output import handler_output
from handler.redis_resource import MTurkResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.hits = []

    def setup(self, handler_spec, manager):
        self.mturk = manager.load_helper_module('helper_mturk')
        self.redis = manager.redis
        self.r_mt = MTurkResource(manager.redis)
        self.manager = manager
        handler_spec.set_description('Core event for boto3 credentials')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        pass

    async def get(self):
        mturk_api_core = self.manager.get_handler_for(self.manager.key_ids["MTURK_API_CORE"])[1]

        [access_key_id, secret_access_key, sandbox] = await self.r_mt.get_credentials()
        async with await self.mturk.get_client_async(self.redis) as client:
            try:
                ret = await mturk_api_core.exec_boto3("get_account_balance")  # here throws error if credentials are invalid
                return {
                    "AccessKeyId": access_key_id,
                    "SecretAccessKey": secret_access_key,
                    "Sandbox": sandbox,
                    "AccountBalance": ret
                }
            except NoCredentialsError:
                return None

    async def set(self, AccessKeyId, SecretAccessKey, Sandbox=True):
        await self.r_mt.set_credentials(AccessKeyId, SecretAccessKey, Sandbox)
        return await self.get()

    async def set_sandbox(self, Enabled):
        await self.r_mt.set_is_sandbox(Enabled)
        return await self.get()

    async def clear(self):
        await self.r_mt.remove_credentials()
