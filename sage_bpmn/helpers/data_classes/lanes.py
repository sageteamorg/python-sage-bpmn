from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Lane:
    """
    Represents a BPMN Lane, which groups flow nodes (e.g., tasks, events) by role or responsibility.
    Lanes appear within a pool and visually separate process logic.

    XML Example:
    ------------
    <lane id="Lane_1" name="Customer Service">
        <flowNodeRef>UserTask_1</flowNodeRef>
        <flowNodeRef>EndEvent_1</flowNodeRef>
    </lane>

    Attributes:
    -----------
    id : str
        Unique identifier for the lane.
    name : Optional[str]
        Human-readable name, usually representing a role or department.
    flowNodeRefs : List[str]
        List of BPMN element IDs (e.g., tasks, events) that belong to this lane.
    """

    id: str
    name: Optional[str] = None
    flowNodeRefs: List[str] = field(default_factory=list)


@dataclass
class LaneSet:
    """
    A collection of BPMN lanes, usually contained within a pool or subprocess.
    LaneSets organize lanes logically and are used to manage participant roles.

    XML Example:
    ------------
    <laneSet id="LaneSet_1">
        <lane id="Lane_1" name="Sales" />
        <lane id="Lane_2" name="Support" />
    </laneSet>

    Attributes:
    -----------
    id : str
        Unique identifier for the lane set.
    lanes : List[Lane]
        List of lanes grouped in this set.
    """

    id: str
    lanes: List[Lane] = field(default_factory=list)
