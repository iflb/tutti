from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler import paths, common
from handler.handler_output import handler_output, CommandError
#from handler.redis_resource import WorkerHelper

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.mturk = manager.load_helper_module('helper_mturk')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        #async with await self.mturk.get_client_async(event.session.redis) as client:
        #    command = event.data["Command"]
        #    output.set("Command", command)

        #    if command=="List":
        #        pn = event.data["ProjectName"]
        #        wids = await WorkerHelper.get_amt_wids_for_pn(event.session.redis, pn)
        #        output.set("ProjectName", pn)
        #        output.set("WorkerIds", wids)
        pass
