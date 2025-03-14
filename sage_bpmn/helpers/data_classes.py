from dataclasses import dataclass

from sage_bpmn.helpers.enums import GatewayType, TaskType


@dataclass(frozen=True)
class BPMNGateway:
    """Immutable dataclass representing a BPMN Gateway."""

    gateway_id: str
    name: str
    gateway_type: GatewayType

    def __post_init__(self):
        """Validate that gateway_type is a GatewayType enum value."""
        if not isinstance(self.gateway_type, GatewayType):
            raise TypeError(f"gateway_type must be a GatewayType, got {type(self.gateway_type).__name__}")


@dataclass(frozen=True)
class BPMNTask:
    """Immutable dataclass representing a BPMN Task."""

    task_id: str
    name: str
    task_type: TaskType

    def __post_init__(self):
        """Validate that task_type is a TaskType enum value."""
        if not isinstance(self.task_type, TaskType):
            raise TypeError(f"task_type must be a TaskType, got {type(self.task_type).__name__}")

    def __repr__(self):
        return f"<{self.task_type.name} Task id={self.task_id} name={self.name}>"
