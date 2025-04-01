from typing import List
from dataclasses import dataclass, field
from .core import AtomicFlowElement, SequenceFlow

@dataclass
class FlowEdge:
    sequence_flow: SequenceFlow
    target: "FlowNode"


@dataclass
class FlowNode:
    id: str
    element: AtomicFlowElement
    outgoing: List[FlowEdge] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id)


@dataclass
class Token:
    current_node: FlowNode
    path: List[FlowNode]
