from libs.scheme.flow import Flow
from abc import ABC, abstractmethod
import os
import sys

class ProjectSchemeBase(ABC):
    def __init__(self):
        pn = sys.modules[self.__class__.__module__].__file__.split("/")[-2]
        self.flow = Flow(pn, self.define_flow())

        self.title = None
        self.assignment_order = "bfs"
        self.sort_order = "natural"
        self.show_title = True
        self.page_navigation = False
        self.push_instruction = True
        self.instruction_btn = True
        self.allow_parallel_sessions = True
        self.anonymous = False
        self.preview = True
        self.completion_alert = False

        self.config_params()

    @abstractmethod
    def config_params(self):
        pass

    @abstractmethod
    def define_flow(self):
        pass
