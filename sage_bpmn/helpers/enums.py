from enum import StrEnum


class GatewayType(StrEnum):
    """Enum for BPMN Gateway types."""

    EXCLUSIVE = "exclusiveGateway"
    PARALLEL = "parallelGateway"
    INCLUSIVE = "inclusiveGateway"
    EVENT_BASED = "eventBasedGateway"


class TaskType(StrEnum):
    """Enum for BPMN Task types."""

    GENERIC = "task"
    USER = "userTask"
    MANUAL = "manualTask"
    SERVICE = "serviceTask"
    SCRIPT = "scriptTask"
    BUSINESS_RULE = "businessRuleTask"
    SEND = "sendTask"
    RECEIVE = "receiveTask"
