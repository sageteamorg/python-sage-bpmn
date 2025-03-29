from dataclasses import dataclass, field
from typing import List

from .diagrams import BPMNDiagram
from .process import Process


@dataclass
class Definitions:
    """
    Root element of a BPMN 2.0 model. It serves as the container for processes,
    collaborations, choreographies, and their visual representations.

    This is the entry point when serializing or parsing a BPMN XML document.

    XML Example:
    ------------
    <definitions id="Defs_1" targetNamespace="http://example.com/bpmn">
        <process id="Process_1" isExecutable="true">
            <!-- Flow elements go here -->
        </process>
        <bpmndi:BPMNDiagram id="Diagram_1">
            <!-- Diagram shapes and edges -->
        </bpmndi:BPMNDiagram>
    </definitions>

    Attributes:
    -----------
    id : str
        Unique identifier for the definitions container.
    targetNamespace : str
        The XML namespace for the contained BPMN elements (e.g., your company or model URI).
    processes : List[Process]
        A list of executable or non-executable processes.
    diagrams : List[BPMNDiagram]
        Graphical representation (BPMN DI) elements for the processes.
    """

    id: str
    targetNamespace: str
    processes: List[Process] = field(default_factory=list)
    diagrams: List[BPMNDiagram] = field(default_factory=list)
