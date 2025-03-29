from dataclasses import dataclass, field
from typing import List


@dataclass
class BPMNShape:
    """
    Represents a graphical shape in a BPMN diagram, typically corresponding to a task,
    event, gateway, or subprocess.

    XML Example:
    ------------
    <bpmndi:BPMNShape id="Shape_1" bpmnElement="UserTask_1" />

    Attributes:
    -----------
    id : str
        Unique identifier of the shape element.
    bpmnElement : str
        The ID of the BPMN element (e.g., task or event) this shape visualizes.
    """

    id: str
    bpmnElement: str


@dataclass
class BPMNEdge:
    """
    Represents a graphical connector (line) between BPMN elements in a diagram.
    Typically corresponds to a sequence flow, message flow, or association.

    XML Example:
    ------------
    <bpmndi:BPMNEdge id="Edge_1" bpmnElement="Flow_1" />

    Attributes:
    -----------
    id : str
        Unique identifier of the edge element.
    bpmnElement : str
        The ID of the BPMN element (e.g., SequenceFlow) this edge visualizes.
    """

    id: str
    bpmnElement: str


@dataclass
class BPMNPlane:
    """
    Container for all visual elements (shapes and edges) in a BPMN diagram.
    It is associated with a specific BPMN process or collaboration.

    XML Example:
    ------------
    <bpmndi:BPMNPlane id="Plane_1" bpmnElement="Process_1">
        <!-- Shapes and edges go here -->
    </bpmndi:BPMNPlane>

    Attributes:
    -----------
    id : str
        Unique identifier for the BPMN plane.
    bpmnElement : str
        ID of the BPMN element (typically a process) represented on this plane.
    shapes : List[BPMNShape]
        Visual boxes for BPMN flow nodes (e.g., tasks, events).
    edges : List[BPMNEdge]
        Visual lines for BPMN connections (e.g., sequence flows).
    """

    id: str
    bpmnElement: str
    shapes: List[BPMNShape] = field(default_factory=list)
    edges: List[BPMNEdge] = field(default_factory=list)


@dataclass
class BPMNDiagram:
    """
    Represents an entire BPMN diagram, including its visual plane.

    XML Example:
    ------------
    <bpmndi:BPMNDiagram id="Diagram_1">
        <bpmndi:BPMNPlane id="Plane_1" bpmnElement="Process_1">
            <!-- shapes and edges -->
        </bpmndi:BPMNPlane>
    </bpmndi:BPMNDiagram>

    Attributes:
    -----------
    id : str
        Unique identifier of the diagram.
    plane : BPMNPlane
        The visual container holding BPMN shapes and edges.
    """

    id: str
    plane: BPMNPlane
