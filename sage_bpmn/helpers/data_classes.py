from dataclasses import dataclass
from sage_bpmn.helpers.enums import GatewayType, TaskType


@dataclass(frozen=True)
class BPMNGateway:
    """Immutable dataclass representing a BPMN Gateway."""
    gateway_id: str
    name: str
    gateway_type: GatewayType


@dataclass(frozen=True)
class BPMNTask:
    """Immutable dataclass representing a BPMN Task."""
    task_id: str
    name: str
    task_type: TaskType

    def __repr__(self):
        return f"<{self.task_type.name} Task id={self.task_id} name={self.name}>"
