from ducts.event import EventHandler
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.manager = manager

        handler_spec.set_description('Get registered boto3 credentials')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        mturk_crd_core = self.manager.get_handler_for(self.manager.key_ids["MTURK_CREDENTIALS_CORE"])[1]
        output.set("Results", await mturk_crd_core.get())
