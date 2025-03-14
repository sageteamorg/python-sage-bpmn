from abc import ABC, abstractmethod
from typing import Dict
from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNTask


class IBPMNRepository(ABC):
    """Abstract base class for BPMN data storage."""

    @abstractmethod
    def add_gateway(self, gateway: BPMNGateway):
        pass

    @abstractmethod
    def get_gateways(self) -> Dict[str, BPMNGateway]:
        pass

    @abstractmethod
    def add_task(self, task: BPMNTask):
        pass

    @abstractmethod
    def get_tasks(self) -> Dict[str, BPMNTask]:
        pass
