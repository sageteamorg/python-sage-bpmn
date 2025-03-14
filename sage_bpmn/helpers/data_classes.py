from dataclasses import dataclass
from sage_bpmn.helpers.enums import GatewayType

@dataclass(frozen=True)
class BPMNGateway:
    """Immutable dataclass representing a BPMN Gateway."""
    gateway_id: str
    name: str
    gateway_type: GatewayType
