import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from sage_bpmn.models import (
    AtomicFlowElement,
    Process,
    SequenceFlow,
    SubProcess,
)


class BPMNDAGBuilder:
    def __init__(self, process: Process):
        self.process = process
        self.graph = nx.DiGraph()
        self._id_to_element = {
            el.id: el for el in self._flatten_elements(process.flowElements)
        }

    def _flatten_elements(self, elements):
        flat = []
        for el in elements:
            flat.append(el)
            if isinstance(el, SubProcess):
                flat.extend(self._flatten_elements(el.flowElements))
        return flat

    def build(self):
        for element in self._id_to_element.values():
            self.graph.add_node(element.id, element=element)

        for element in self._id_to_element.values():
            if isinstance(element, SequenceFlow):
                self.graph.add_edge(element.sourceRef, element.targetRef, flow=element)

        return self.graph


class DAGVisualizer:
    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self._filtered_nodes = [
            n
            for n in graph.nodes
            if not isinstance(graph.nodes[n]["element"], SequenceFlow)
        ]

    def draw(self, with_labels=True, figsize=(12, 8)):
        pos = graphviz_layout(self.graph.subgraph(self._filtered_nodes), prog="dot")
        labels = {n: self._label(n) for n in self._filtered_nodes}

        plt.figure(figsize=figsize)
        nx.draw(
            self.graph.subgraph(self._filtered_nodes),
            pos,
            with_labels=with_labels,
            labels=labels,
            node_size=2500,
            node_color="lightblue",
            font_size=10,
        )
        plt.title("BPMN Process DAG (Flow Elements only)")
        plt.show()

    def _label(self, node_id):
        element: AtomicFlowElement = self.graph.nodes[node_id].get("element")
        return f"{element.__class__.__name__}\n{element.name or element.id}"

    def print_tree_view(self, start_node=None, prefix=""):
        roots = (
            [n for n in self._filtered_nodes if self.graph.in_degree(n) == 0]
            if start_node is None
            else [start_node]
        )

        for r in roots:
            self._print_tree_recursive(r, prefix)

    def _print_tree_recursive(self, node_id, prefix):
        element = self.graph.nodes[node_id]["element"]
        label = f"{element.__class__.__name__} ({element.name or element.id})"
        print(prefix + "├── " + label)

        successors = [
            succ
            for succ in self.graph.successors(node_id)
            if succ in self._filtered_nodes
        ]

        for i, succ in enumerate(successors):
            next_prefix = prefix + ("│   " if i < len(successors) - 1 else "    ")
            self._print_tree_recursive(succ, next_prefix)
