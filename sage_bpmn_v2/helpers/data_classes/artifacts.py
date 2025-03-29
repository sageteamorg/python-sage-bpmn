from dataclasses import dataclass


@dataclass
class TextAnnotation:
    """
    Represents a BPMN TextAnnotation artifact, used to add notes or comments to a diagram.
    It has no effect on the execution semantics of the process.

    XML Example:
    ------------
    <textAnnotation id="TextAnnotation_1">
        <text>This is a helpful comment.</text>
    </textAnnotation>

    Attributes:
    -----------
    id : str
        Unique identifier of the text annotation.
    text : str
        The content of the annotation (visible comment).
    """

    id: str
    text: str


@dataclass
class Association:
    """
    Represents a BPMN Association, which visually connects artifacts (like TextAnnotations)
    to BPMN elements. Associations do not affect execution.

    XML Example:
    ------------
    <association id="Association_1" sourceRef="TextAnnotation_1" targetRef="Task_1" />

    Attributes:
    -----------
    id : str
        Unique identifier of the association.
    sourceRef : str
        ID of the source element (e.g., TextAnnotation).
    targetRef : str
        ID of the target BPMN element (e.g., Task, Event).
    """

    id: str
    sourceRef: str
    targetRef: str
