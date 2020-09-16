from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler import common

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        project_name = event.data[0]

        ans = {}
        try:
            ans["Templates"] = common.get_templates(project_name)
            ans["Project"] = project_name
            ans["Status"] = "success"
        except Exception as e:
            ans["Status"] = "error"
            ans["Reason"] = str(e)
        return ans
