from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler import common

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('プロジェクト一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        return common.get_projects()
