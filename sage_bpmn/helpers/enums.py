from enum import StrEnum

class GatewayType(StrEnum):
    """Enum for BPMN Gateway types."""
    EXCLUSIVE = "exclusiveGateway"
    PARALLEL = "parallelGateway"
    INCLUSIVE = "inclusiveGateway"
    EVENT_BASED = "eventBasedGateway"
