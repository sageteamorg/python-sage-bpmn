from dataclasses import dataclass
from typing import Union

from sage_bpmn_v2.helpers.data_classes.core import Event, Gateway, SequenceFlow, Task

#: FlowElement is a generic type representing any major flow node,
#: including tasks, gateways, events, or sequence flows.
FlowElement = Union[Task, Gateway, Event, SequenceFlow]
