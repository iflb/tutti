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
        self.evt_list_templates = manager.get_handler_for(manager.key_ids["LIST_TEMPLATES"])[1]

        handler_spec.set_description('Creates a project.')
        handler_spec.set_as_responsive()
        return handler_spec

    def is_valid_template_name(self, name):
        return name in self.templates

    @handler_output
    async def handle(self, event, output):
        ret = await self.evt_project_scheme.get_project_scheme(**event.data)

        self.templates = await self.evt_list_templates.list_templates(event.data["ProjectName"])

        if isinstance(ret, Exception):
            raise ret
        else:
            scheme = ret
            output.set("Config", self.get_config_dict(scheme))
            if scheme.flow:
                output.set("Flow", self.get_batch_info_dict(scheme.flow.root_node))
            else:
                output.set("Flow", None)

    def get_batch_info_dict(self, child):
        if child.is_template():
            if not self.is_valid_template_name(child.name):
                raise Exception(f"'{child.name}' is not registered as a template name")
            ret = {
                "is_skippable": child.is_skippable,
                "name": child.name
            }
        else:
            _info = []
            for c in child.children:
                _info.append(self.get_batch_info_dict(c))
            ret = {
                "name": child.name,
                "is_skippable": child.is_skippable,
                "children": _info
            }

        if child.condition:
            ret.update({
                "statement": child.condition.statement.value,
                "condition": child.condition.print() if child.condition else None
            })

        return ret


    def get_config_dict(self, scheme):
        return {
            "Title": scheme.title,
            "AssignmentOrder": scheme.assignment_order,
            "SortOrder": scheme.sort_order,
            "ShowTitle": scheme.show_title,
            "PageNavigation": scheme.page_navigation,
            "PushInstruction": scheme.push_instruction,
            "InstructionBtn": scheme.instruction_btn,
            "AllowParallelSessions": scheme.allow_parallel_sessions,
            "Anonymous": scheme.anonymous,
            "Preview": scheme.preview,
            "CompletionAlert": scheme.completion_alert,
        }
