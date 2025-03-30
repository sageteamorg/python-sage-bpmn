from typing import List, Optional, Union
from sage_bpmn_v2.helpers.data_classes import AtomicFlowElement, SequenceFlow, StartEvent
from sage_bpmn_v2.repository import BPMNQuery


class ExecutionPathResolver:
    """
    Resolves the linear execution order of BPMN flow elements starting from StartEvent.
    Handles basic linear flows (no gateway branching or merging).
    """

    def __init__(self, query: BPMNQuery):
        self.query = query
        self.visited = set()

    def resolve(self, include_sequence_flows: bool = False) -> List[Union[AtomicFlowElement, SequenceFlow]]:
        """
        Returns the ordered list of flow elements starting from the StartEvent,
        following connected SequenceFlows.

        Parameters:
        -----------
        include_sequence_flows : bool
            If True, include SequenceFlow elements between flow nodes in the path.

        Returns:
        --------
        List[Union[AtomicFlowElement, SequenceFlow]]
        """
        start_events = self.query.find_by_type(StartEvent)
        if not start_events:
            raise ValueError("No StartEvent found in the process.")

        start_node = start_events[0]  # Assuming one start event
        return self._walk(start_node, include_sequence_flows)

    def _walk(
        self,
        node: AtomicFlowElement,
        include_sequence_flows: bool
    ) -> List[Union[AtomicFlowElement, SequenceFlow]]:
        """
        Walks the flow from the given node using outgoing SequenceFlows.
        """
        if node.id in self.visited:
            return []

        self.visited.add(node.id)
        ordered_path: List[Union[AtomicFlowElement, SequenceFlow]] = [node]

        next_sequence_flows = self.query.filter_by_attributes(
            SequenceFlow, sourceRef=node.id
        )

        for flow in next_sequence_flows:
            target_node = self.query.find_by_id(flow.targetRef)
            if not target_node or target_node.id in self.visited:
                continue

            if include_sequence_flows:
                ordered_path.append(flow)

            ordered_path.extend(self._walk(target_node, include_sequence_flows))

        return ordered_path
