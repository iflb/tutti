from libs.scheme.flow import Flow
from abc import ABC, abstractmethod

class ProjectSchemeBase(ABC):
    def __init__(self):
        self.config_params()
        self.flow = Flow(self.define_flow())

    @abstractmethod
    def config_params(self):
        pass

    @abstractmethod
    def define_flow(self):
        pass
