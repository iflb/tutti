from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output

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
        next_token = None
        quals = []
        while True:
            kwargs = {
                "MustBeRequestable": False,
                "MustBeOwnedByCaller": True
            }
            if next_token:  kwargs["NextToken"] = next_token

            res = await self.evt_boto3_mturk.exec_boto3("list_qualification_types", kwargs)
            quals[:0] = res["QualificationTypes"][::-1]

            if "NextToken" in res:
                next_token = res["NextToken"]
                continue
            else:
                break
        output.set("QualificationTypes", quals)
