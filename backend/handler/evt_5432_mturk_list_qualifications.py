from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        quals = await self.list_qualification_types(**event.data)
        output.set("QualificationTypes", quals)

    async def list_qualification_types(self, TuttiQuals=True):
        next_token = None
        quals = []
        while True:
            kwargs = {
                "MustBeRequestable": False,
                "MustBeOwnedByCaller": True
            }
            if next_token:  kwargs["NextToken"] = next_token

            res = await self.evt_mturk_api_core.exec_boto3("list_qualification_types", kwargs)
            qtypes = [qt for qt in res["QualificationTypes"] if TuttiQuals is True or not qt["Name"].startswith("TUTTI_HITTYPE_QUALIFICATION")]
            #quals[:0] = res["QualificationTypes"][::-1]
            quals.extend(qtypes)

            if "NextToken" in res:
                next_token = res["NextToken"]
                continue
            else:
                break
        return quals
