from typing import Dict, List

from networkx import DiGraph

from sage_bpmn_v2.design.interfaces import ExecutionObserver


class CodeExecutionLogger(ExecutionObserver):
    def __init__(self, graph: DiGraph):
        self.graph = graph

    def on_step(
        self,
        active_nodes: List[str],
        visited_nodes: List[str],
        metadata: Dict[str, dict],
    ):
        for node_id in active_nodes:
            el = self.graph.nodes[node_id]["element"]
            meta = metadata.get(node_id, {})
            print(f"🟢 Executing: {el.__class__.__name__} ({el.name or el.id})")

            # Log incoming flows
            for pred in self.graph.predecessors(node_id):
                flow = self.graph.edges[pred, node_id].get("flow")
                if flow:
                    print(f"➡️  Flow: {flow.sourceRef} → {flow.targetRef}")

            # Log outgoing flows
            for succ in self.graph.successors(node_id):
                flow = self.graph.edges.get((node_id, succ), {}).get("flow")
                if flow:
                    print(f"➡️  Next: {flow.sourceRef} → {flow.targetRef}")

            # Log execution context flags
            flags = []
            if meta.get("isScope"):
                flags.append("isScope")
            if meta.get("isConcurrent"):
                flags.append("isConcurrent")
            if meta.get("isCompleted"):
                flags.append("isCompleted")
            if flags:
                print(f"📌 Context: {', '.join(flags)}")

            print("")  # spacing
