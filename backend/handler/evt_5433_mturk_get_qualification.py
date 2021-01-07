from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.evt_boto3_mturk = manager.get_handler_for(manager.key_ids["BOTO3_MTURK"])[1]
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("Results", await self.get_qualification_type(**event.data))

    async def get_qualification_type(self, QualificationTypeId):
        return await self.evt_boto3_mturk.exec_boto3("get_qualification_type", {"QualificationTypeId": QualificationTypeId})
