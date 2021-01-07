import asyncio
from inspect import signature
from typing import List

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
        #handler_spec.params = [(k,v.annotation) for k,v in signature(self.delete_qualification_types).parameters.items()]

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if isinstance(event.data, dict):
            output.set("Results", await self.delete_qualification_types(**event.data))
        else:
            raise Exception("data needs to be JSON format")

    async def delete_qualification_types(self, QualificationTypeIds: List[str]):
        if isinstance(QualificationTypeIds, list):
            tasks = [self.evt_boto3_mturk.exec_boto3("delete_qualification_type", {"QualificationTypeId":qid}) for qid in QualificationTypeIds]
            return await asyncio.gather(*tasks)
        else:
            raise Exception("QualificationTypeIds needs to be a list")
