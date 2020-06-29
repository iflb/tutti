from datetime import datetime
import os
import asyncio
from asyncio.subprocess import PIPE
import random, string

from tortoise.backends.mysql.client import MySQLClient

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

#@config_callback
#def config(loader):
#    loader.add_attr('root_path', os.getcwd(), help='')
#    loader.add_attr('root_path_templates', 'projects/{project_name}/templates/', help='')

templates = [
    {
        "name": "first",
        "repeat_times": 2,
    },
    {
        "name": "main",
        "repeat_times": 10,
    },
    {
        "name": "last",
        "repeat_times": 1
    }
]

class NanotaskSessionManager():
    def __init__(self):
        self.state_machines = {}
        self.sessions = {}

    def register_state_machine(self, project_name, sm):
        self.state_machines[project_name] = sm

    def create_session(self, project_name, session_id=None):
        if not session_id:
            session_id = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
        if session_id in self.sessions:
            raise ValueError(f"duplicate session id '{session_id}'")

        self.set_session(project_name, session_id)
        return session_id, self.get_session(session_id)

    def get_session(self, session_id):
        return self.sessions[session_id]

    def set_session(self, project_name, session_id):
        try:
            self.sessions[session_id] = self.state_machines[project_name]
        except Exception as e:
            raise ValueError(f"state machine for project name '{project_name}' is not registered")

class NanotaskSessionStateMachine():
    def __init__(self):
        self.batches = []
        self.total_finished_nanotasks = 0
        self.status_getter = self._next_status_generator()

    def add_batch(self, batch):
        self.batches.append(batch)

    def _next_status_generator(self):
        for b in self.batches:
            for i in range(b.repeat_times):
                yield f'{b.template_name} {i}'

    def get_next_status(self):
        return self.status_getter.__next__()

    def refresh_generator(self, batch):
        self.__init__()
        

# TODO:: ultimately needs to be moved to some other data structure
class NanotaskSessionState():
    def __init__(self, template_name, repeat_times):
        self.template_name = template_name
        self.repeat_times = repeat_times


class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        #self.conf = configure_module(config)
        self.session_manager = NanotaskSessionManager()

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        command = event.data[0]
        project_name = event.data[1]
        if command=="REGISTER_SM":
            try:
                sm = NanotaskSessionStateMachine()
                sm.add_batch(NanotaskSessionState("first", 2))
                sm.add_batch(NanotaskSessionState("main", 10))
                sm.add_batch(NanotaskSessionState("last", 1))
                self.session_manager.register_state_machine(project_name, sm)
                return "successfully registered a state machine"
            except Exception as e:
                return str(e)
        elif command=="CREATE_SESSION":
            try:
                session_id, session = self.session_manager.create_session(project_name)
                return session_id
            except Exception as e:
                return str(e)
        elif command=="GET":
            try:
                ### FIXME:: project_name -> session_id
                session_id = project_name
                return self.session_manager.get_session(session_id).get_next_status()
            except:
                return "Session already terminated"
