import os
import asyncio

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from libs.scheme.flow import Statement
#from libs.session import SessionStatus

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        #self.path = manager.load_helper_module('paths')
        #handler_spec.set_description('プロジェクトを作ります。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):

        wsd = {"enums": {}}
        #enum_classes = [ Statement, SessionStatus ]
        enum_classes = [ Statement ]
        for ec in enum_classes:
            wsd["enums"][ec.__name__] = { name:member.value for name, member in ec.__members__.items() }

        return wsd
