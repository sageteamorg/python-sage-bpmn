from abc import ABC, abstractmethod
from typing import Dict
from sage_bpmn.helpers.data_classes import BPMNGateway

class IBPMNRepository(ABC):
    """Abstract base class for BPMN data storage."""

    @abstractmethod
    def add_gateway(self, gateway: BPMNGateway):
        """Adds a BPMN gateway to storage."""
        pass

    @abstractmethod
    def get_gateways(self) -> Dict[str, BPMNGateway]:
        """Returns all stored BPMN gateways."""
        pass
