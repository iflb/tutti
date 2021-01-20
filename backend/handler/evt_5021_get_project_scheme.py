import os
import asyncio
import inspect

from ducts.spi import EventHandler
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.evt_project_scheme = manager.get_handler_for(manager.key_ids["PROJECT_SCHEME_CORE"])[1]

        handler_spec.set_description('Creates a project.')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        scheme = await self.evt_project_scheme.get_project_scheme(**event.data)
        output.set("Config", self.get_config_dict(scheme))
        output.set("Flow", self.get_batch_info_dict(scheme.flow.root_node))

    def get_batch_info_dict(self, child):
        if child.is_template():
            return {
                "statement": child.statement.value,
                "condition": inspect.getsource(child.condition) if child.condition else None,
                "is_skippable": child.is_skippable,
                "name": child.name
            }
        else:
            _info = []
            for c in child.children:
                _info.append(self.get_batch_info_dict(c))
            return {
                "name": child.name,
                "statement": child.statement.value,
                "condition": inspect.getsource(child.condition) if child.condition else None,
                "is_skippable": child.is_skippable,
                "children": _info
            }

    def get_config_dict(self, scheme):
        return {
            "Title": scheme.title,
            "AssignmentOrder": scheme.assignment_order,
            "SortOrder": scheme.sort_order,
            "Pagination": scheme.pagination,
            "Instruction": scheme.instruction,
            "ShowTitle": scheme.show_title
        }
