from libs.scheme.flow import Flow
from abc import ABC, abstractmethod
import os
import sys

class ProjectSchemeBase(ABC):
    def __init__(self):
        self.config_params()
        pn = sys.modules[self.__class__.__module__].__file__.split("/")[-2]
        self.flow = Flow(pn, self.define_flow())

    @abstractmethod
    def config_params(self):
        pass

    @abstractmethod
    def define_flow(self):
        pass
