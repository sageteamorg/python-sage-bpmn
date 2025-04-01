from typing import Dict, List, Set

from sage_bpmn_v2.design.interfaces import ExecutionObserver
from sage_bpmn_v2.helpers.data_classes import (
    AtomicFlowElement,
    EndEvent,
    ExclusiveGateway,
    ParallelGateway,
    Process,
    StartEvent,
)
from sage_bpmn_v2.repository import BPMNDAGBuilder


class BPMNExecutor:
    def __init__(self, process: Process):
        self.process = process
        self.graph = BPMNDAGBuilder(process).build()

        self.visited_nodes: Set[str] = set()
        self.current_executions: List[str] = self._find_start_nodes()
        self.execution_metadata: Dict[str, dict] = {
            node_id: {
                "isScope": False,
                "isConcurrent": False,
                "isCompleted": False,
                "executionId": f"exec_{node_id}",
            }
            for node_id in self.graph.nodes
        }

        self.observers: List[ExecutionObserver] = []

    def add_observer(self, observer: ExecutionObserver):
        self.observers.append(observer)

    def _find_start_nodes(self) -> List[str]:
        return [
            node
            for node in self.graph.nodes
            if isinstance(self.graph.nodes[node]["element"], StartEvent)
        ]

    def step(self) -> bool:
        if not self.current_executions:
            return False

        next_executions: List[str] = []

        for node_id in self.current_executions:
            element: AtomicFlowElement = self.graph.nodes[node_id]["element"]
            self.visited_nodes.add(node_id)
            self.execution_metadata[node_id]["isCompleted"] = True

            successors = list(self.graph.successors(node_id))

            # Simulate branching logic
            if isinstance(element, EndEvent):
                continue
            elif isinstance(element, ExclusiveGateway):
                if successors:
                    next_executions.append(successors[0])
            elif isinstance(element, ParallelGateway):
                for succ in successors:
                    self.execution_metadata[succ]["isConcurrent"] = True
                    next_executions.append(succ)
            else:
                next_executions.extend(successors)

        self.current_executions = next_executions

        # Notify observers
        for observer in self.observers:
            observer.on_step(
                self.current_executions,
                list(self.visited_nodes),
                self.execution_metadata,
            )

        return bool(self.current_executions)
