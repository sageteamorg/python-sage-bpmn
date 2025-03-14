from typing import List, Optional
from sage_bpmn.helpers.enums import GatewayType
from sage_bpmn.design.interface import IBPMNRepository
from sage_bpmn.helpers.data_classes import BPMNGateway


class BPMNQueryEngine:
    """Handles searching and filtering of BPMN Gateways."""

    def __init__(self, repository: IBPMNRepository):
        self.repository = repository

    def get_gateway_by_id(self, gateway_id: str) -> Optional[BPMNGateway]:
        """Finds a BPMN gateway by its ID."""
        return self.repository.get_gateways().get(gateway_id, None)

    def get_gateways_by_type(self, gateway_type: GatewayType) -> List[BPMNGateway]:
        """Filters and returns BPMN gateways of a specific type."""
        return [gw for gw in self.repository.get_gateways().values() if gw.gateway_type == gateway_type]

    def search_gateways_by_name(self, name_query: str, exact_match: bool = False) -> List[BPMNGateway]:
        """Searches for BPMN gateways by name."""
        if exact_match:
            return [gw for gw in self.repository.get_gateways().values() if gw.name == name_query]
        return [gw for gw in self.repository.get_gateways().values() if name_query.lower() in gw.name.lower()]
