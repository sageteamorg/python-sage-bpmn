from abc import ABC, abstractmethod
from typing import Dict

from sage_bpmn.helpers.data_classes import BPMNGateway, BPMNProcess, BPMNTask


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

    @abstractmethod
    def add_process(self, process: BPMNProcess):
        pass

    @abstractmethod
    def get_processes(self) -> Dict[str, BPMNProcess]:
        pass
