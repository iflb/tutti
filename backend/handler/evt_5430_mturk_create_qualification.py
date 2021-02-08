from ducts.spi import EventHandler, Event
from ifconf import configure_module, config_callback

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_boto3_mturk = manager.get_handler_for(manager.key_ids["BOTO3_MTURK"])[1]
        handler_spec.set_description('Creates a QualificationType.')
        handler_spec.set_as_responsive()

        return handler_spec

    @handler_output
    async def handle(self, event, output):
        output.set("QualificationType", await self.evt_boto3_mturk.exec_boto3("create_qualification_type", event.data))
