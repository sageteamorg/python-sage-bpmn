from typing import Dict
from sage_bpmn.helpers.data_classes import BPMNGateway
from sage_bpmn.design.interface import IBPMNRepository


class InMemoryIBPMNRepository(IBPMNRepository):
    """Stores BPMN gateways in memory."""

    def __init__(self):
        self._gateways: Dict[str, BPMNGateway] = {}

    def add_gateway(self, gateway: BPMNGateway):
        """Adds a BPMN gateway to storage."""
        self._gateways[gateway.gateway_id] = gateway

    def get_gateways(self) -> Dict[str, BPMNGateway]:
        """Returns all stored BPMN gateways."""
        return self._gateways
