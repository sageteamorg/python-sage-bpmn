from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExtensionProperty:
    name: str
    value: str


@dataclass
class ExecutionListener:
    event_type: str  # e.g., "start", "end"
    listener_type: str  # class, expression, delegateExpression
    retries: Optional[str] = None


@dataclass
class ZeebeFormDefinition:
    formKey: str
    binding: Optional[str] = None
    version: Optional[str] = None


@dataclass
class ZeebeAssignment:
    assignee: Optional[str] = None
    candidateGroups: Optional[str] = None
    candidateUsers: Optional[str] = None
    dueDate: Optional[str] = None
    followUpDate: Optional[str] = None
    priority: Optional[str] = None


@dataclass
class ZeebeInput:
    source: str
    target: str


@dataclass
class ZeebeOutput:
    source: str
    target: str


@dataclass
class ZeebeHeader:
    key: str
    value: str