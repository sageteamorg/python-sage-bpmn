from dataclasses import dataclass, field
from typing import List, Optional, Union

from .artifacts import Association, TextAnnotation
from .core import AtomicFlowElement
from .lanes import LaneSet
from .properties_panel import ExecutionListener, ExtensionProperty


@dataclass
class Process:
    """
    Represents a BPMN Process, the main container for defining business process behavior.
    A process holds tasks, events, gateways, sequence flows, lanes, and other elements
    that describe the flow logic.

    XML Example:
    ------------
    <process id="Process_1" isExecutable="true">
        <startEvent id="StartEvent_1" />
        <userTask id="UserTask_1" name="Handle Request" />
        <exclusiveGateway id="Gateway_1" />
        <sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="UserTask_1" />
        <laneSet id="LaneSet_1">
            <lane id="Lane_1" name="Support Agent">
                <flowNodeRef>UserTask_1</flowNodeRef>
            </lane>
        </laneSet>
        <textAnnotation id="Note_1">
            <text>Handle this task promptly.</text>
        </textAnnotation>
        <association id="Assoc_1" sourceRef="Note_1" targetRef="UserTask_1" />
    </process>

    Attributes:
    -----------
    id : str
        Unique identifier of the process.
    isExecutable : bool
        Indicates whether the process is intended to be executed (e.g., by a BPM engine).
    flowElements : List[AtomicFlowElement]
        The main BPMN elements inside the process: events, tasks, gateways, flows, etc.
    laneSets : List[LaneSet]
        Optional grouping of lanes that partition the process by roles or responsibilities.
    artifacts : List[Union[TextAnnotation, Association]]
        Optional visual or documentation-related elements (notes, connectors).
    """

    id: str
    isExecutable: bool = True
    documentation: Optional[str] = None
    versionTag: Optional[str] = None
    flowElements: List[AtomicFlowElement] = field(default_factory=list)
    laneSets: List[LaneSet] = field(default_factory=list)
    artifacts: List[Union[TextAnnotation, Association]] = field(default_factory=list)
    extensionProperties: List[ExtensionProperty] = field(default_factory=list)
    executionListeners: List[ExecutionListener] = field(default_factory=list)
