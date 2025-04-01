"""
BPMN 2.0 Data Model (Python @dataclass-based)

This module defines a BPMN 2.0-compliant data structure hierarchy using Python dataclasses.
It mirrors the XML structure used in the BPMN 2.0 standard.

Element Hierarchy:
------------------

Definitions
├── Process (List[Process])
│   ├── flowElements (List of):
│   │   ├── StartEvent
│   │   ├── EndEvent
│   │   ├── IntermediateCatchEvent
│   │   ├── IntermediateThrowEvent
│   │   ├── BoundaryEvent
│   │   ├── Task (base class)
│   │   │   ├── UserTask
│   │   │   ├── ServiceTask
│   │   │   ├── ScriptTask
│   │   │   └── SubProcess (contains its own flowElements)
│   │   ├── Gateway (base class)
│   │   │   ├── ExclusiveGateway
│   │   │   ├── ParallelGateway
│   │   │   ├── InclusiveGateway
│   │   │   └── EventBasedGateway
│   │   └── SequenceFlow
│   ├── laneSets (List[LaneSet])
│   │   └── Lane (contains flowNodeRefs)
│   └── artifacts (List of):
│       ├── TextAnnotation
│       └── Association
│
├── BPMNDiagram (List[BPMNDiagram])
│   └── BPMNPlane
│       ├── BPMNShape (one per FlowNode)
│       └── BPMNEdge (one per SequenceFlow)
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .properties_panel import (
    ExecutionListener,
    ExtensionProperty,
    ZeebeAssignment,
    ZeebeFormDefinition,
    ZeebeHeader,
    ZeebeInput,
    ZeebeOutput,
    ZeebeTaskDefinition,
)


@dataclass
class AtomicFlowElement:
    id: str
    name: Optional[str] = None
    documentation: Optional[str] = None
    extensionProperties: List[ExtensionProperty] = field(default_factory=list)
    executionListeners: List[ExecutionListener] = field(default_factory=list)


@dataclass
class SequenceFlow(AtomicFlowElement):
    """
    Represents a BPMN Sequence Flow that connects two flow nodes.

    XML Example:
    ------------
    <sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="UserTask_1" />

    Attributes:
    -----------
    id : str
        Unique identifier of the sequence flow.
    sourceRef : str
        ID of the source element (e.g., task, gateway).
    targetRef : str
        ID of the target element.
    name : Optional[str]
        Optional display name of the sequence flow.
    """

    sourceRef: str = ""
    targetRef: str = ""


# --- Base Event Class and Subclasses ---


@dataclass
class Event(AtomicFlowElement):
    pass


@dataclass
class StartEvent(Event):
    """
    Represents a BPMN StartEvent, which marks the beginning of a process flow.

    XML Example:
    ------------
    <startEvent id="StartEvent_1" name="Start" />
    """

    pass


@dataclass
class EndEvent(Event):
    """
    Represents a BPMN EndEvent, which marks the end of a process flow.

    XML Example:
    ------------
    <endEvent id="EndEvent_1" name="End" />
    """

    pass


@dataclass
class IntermediateCatchEvent(Event):
    """
    Represents an Intermediate Catch Event, which waits for a trigger.

    XML Example:
    ------------
    <intermediateCatchEvent id="CatchEvent_1" name="Wait for signal" />
    """

    pass


@dataclass
class IntermediateThrowEvent(Event):
    """
    Represents an Intermediate Throw Event, which emits a trigger.

    XML Example:
    ------------
    <intermediateThrowEvent id="ThrowEvent_1" name="Send signal" />
    """

    pass


@dataclass
class BoundaryEvent(Event):
    """
    Represents a Boundary Event attached to the boundary of an activity.

    XML Example:
    ------------
    <boundaryEvent id="BoundaryEvent_1" attachedToRef="UserTask_1" />

    Attributes:
    -----------
    attachedToRef : str
        ID of the activity (usually a task) this event is attached to.
    """

    attachedToRef: str = ""


# --- Gateway Base and Variants ---


@dataclass
class Gateway(AtomicFlowElement):
    """
    Base class for all BPMN gateways.

    Attributes:
    -----------
    id : str
        Unique identifier of the gateway.
    name : Optional[str]
        Display name of the gateway.
    """

    id: str
    name: Optional[str] = None


@dataclass
class ExclusiveGateway(Gateway):
    """
    Represents an Exclusive Gateway (XOR), which routes to exactly one path.

    XML Example:
    ------------
    <exclusiveGateway id="Gateway_1" name="Decision Point" />
    """

    pass


@dataclass
class ParallelGateway(Gateway):
    """
    Represents a Parallel Gateway (AND), which splits or joins all paths simultaneously.

    XML Example:
    ------------
    <parallelGateway id="Parallel_1" name="Fork" />
    """

    pass


@dataclass
class InclusiveGateway(Gateway):
    """
    Represents an Inclusive Gateway (OR), which can take one or more paths.

    XML Example:
    ------------
    <inclusiveGateway id="Inclusive_1" name="Evaluate Options" />
    """

    pass


@dataclass
class EventBasedGateway(Gateway):
    """
    Represents an Event-Based Gateway, which routes based on event occurrence.

    XML Example:
    ------------
    <eventBasedGateway id="EventBased_1" name="Wait for Response" />
    """

    pass


# --- Task Base and Variants ---


@dataclass
class Task(AtomicFlowElement):
    """
    Base class for BPMN tasks.

    Attributes:
    -----------
    id : str
        Unique identifier of the task.
    name : Optional[str]
        Display name for the task.
    """

    pass


@dataclass
class UserTask(Task):
    """
    Represents a BPMN UserTask, performed by a human user.

    XML Example:
    ------------
    <userTask id="UserTask_1" name="Review Request" />
    """

    assignment: Optional[ZeebeAssignment] = None
    form: Optional[ZeebeFormDefinition] = None
    inputs: List[ZeebeInput] = field(default_factory=list)
    outputs: List[ZeebeOutput] = field(default_factory=list)
    headers: List[ZeebeHeader] = field(default_factory=list)


@dataclass
class ServiceTask(Task):
    """
    Represents a BPMN ServiceTask, performed by an automated service.

    XML Example:
    ------------
    <serviceTask id="ServiceTask_1" name="Call API" />
    """

    taskDefinition: Optional[ZeebeTaskDefinition] = None
    inputs: List[ZeebeInput] = field(default_factory=list)
    outputs: List[ZeebeOutput] = field(default_factory=list)
    headers: List[ZeebeHeader] = field(default_factory=list)


@dataclass
class ScriptTask(Task):
    """
    Represents a BPMN ScriptTask, which runs a script internally.

    XML Example:
    ------------
    <scriptTask id="ScriptTask_1" name="Run Script">
        <script>console.log("Hello BPMN")</script>
    </scriptTask>

    Attributes:
    -----------
    script : Optional[str]
        The script content to be executed by this task.
    """

    script: Optional[str] = None


@dataclass
class SubProcess(Task):
    """
    Represents a BPMN SubProcess, which contains its own nested flow elements.

    XML Example:
    ------------
    <subProcess id="SubProcess_1" name="Nested Flow">
        <!-- nested flowElements go here -->
    </subProcess>
    """

    flowElements: List[AtomicFlowElement] = field(default_factory=list)
