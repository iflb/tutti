import asyncio

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
        self.r_mt = MTurkResource(manager.redis)
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        qual_ids = event.data["QualificationTypeIds"]
        async with await self.mturk.get_client_async(event.session.redis) as client:
            tasks = [client.delete_qualification_type(QualificationTypeId=qual_id) for qual_id in qual_ids]
            ret = await asyncio.gather(*tasks)
            output.set("Results", ret)
