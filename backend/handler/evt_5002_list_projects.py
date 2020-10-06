from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.path = manager.load_helper_module('paths')
        handler_spec.set_description('プロジェクト一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        project_names = common.get_projects()
        project_paths = [self.path.project(pn) for pn in project_names]
        projects = [{"name": p[0], "path": str(p[1])} for p in zip(project_names, project_paths)]
        output.set("Projects", projects)
