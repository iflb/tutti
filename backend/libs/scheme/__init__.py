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
        self.pagination = False
        self.instruction = True
        self.show_title = True
        self.allow_parallel_sessions = True

        self.config_params()

    @abstractmethod
    def config_params(self):
        pass

    @abstractmethod
    def define_flow(self):
        pass
