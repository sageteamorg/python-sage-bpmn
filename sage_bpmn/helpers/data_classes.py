from typing import List

from dataclasses import dataclass

from sage_bpmn.helpers.enums import EventType, GatewayType, TaskType


@dataclass(frozen=True)
class BPMNGateway:
    """Immutable dataclass representing a BPMN Gateway."""

    gateway_id: str
    name: str
    gateway_type: GatewayType

    def __post_init__(self):
        """Validate that gateway_type is a GatewayType enum value."""
        if not isinstance(self.gateway_type, GatewayType):
            raise TypeError(
                f"gateway_type must be a GatewayType, got {type(self.gateway_type).__name__}"
            )


@dataclass(frozen=True)
class BPMNTask:
    """Immutable dataclass representing a BPMN Task."""

    task_id: str
    name: str
    task_type: TaskType

    def __post_init__(self):
        """Validate that task_type is a TaskType enum value."""
        if not isinstance(self.task_type, TaskType):
            raise TypeError(
                f"task_type must be a TaskType, got {type(self.task_type).__name__}"
            )

    def __repr__(self):
        return f"<{self.task_type.name} Task id={self.task_id} name={self.name}>"


@dataclass(frozen=True)
class BPMNSequenceFlow:
    """Represents a BPMN Sequence Flow between elements."""

    flow_id: str
    source_ref: str
    target_ref: str


@dataclass(frozen=True)
class BPMNEvent:
    """Represents a BPMN Event (Start, End, Intermediate)."""

    event_id: str
    name: str
    event_type: EventType

@dataclass(frozen=True)
class BPMNProcess:
    """Represents a BPMN Process, including subprocesses."""

    process_id: str
    name: str
    is_executable: bool
    parent_process_id: str = None  # None if it's a top-level process
    elements: List[str] = None  # List of element IDs (tasks, gateways, etc.)

    def __post_init__(self):
        """Ensure elements is always a list."""
        if self.elements is None:
            object.__setattr__(self, "elements", [])
