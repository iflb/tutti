from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        if isinstance(event.data, dict):
            output.set("QualificationTypeId", event.data["QualificationTypeId"])
            output.set("Results", await self.list_workers_with_qualification_type(**event.data))
        else:
            raise Exception("data needs to be JSON format")

    async def list_workers_with_qualification_type(self, QualificationTypeId, Status="Granted"):
        next_token = None
        quals = []
        while True:
            kwargs = {
                "QualificationTypeId": QualificationTypeId,
                "Status": Status
            }
            if next_token:  kwargs["NextToken"] = next_token

            res = await self.evt_mturk_api_core.exec_boto3("list_workers_with_qualification_type", kwargs)
            quals.extend(res["Qualifications"])

            if "NextToken" in res:
                next_token = res["NextToken"]
                continue
            else:
                break
        return quals
