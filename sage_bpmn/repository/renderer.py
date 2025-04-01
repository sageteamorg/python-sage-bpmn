import uuid
from typing import List

from networkx import DiGraph


class TokenMetadata:
    def __init__(
        self,
        activity_id: str,
        is_scope: bool = False,
        is_active: bool = True,
        is_concurrent: bool = False,
        is_completed: bool = False,
    ):
        self.id = f"T{str(uuid.uuid4())[:4]}"  # Short token ID
        self.activity_id = activity_id
        self.is_scope = is_scope
        self.is_active = is_active
        self.is_concurrent = is_concurrent
        self.is_completed = is_completed

    def format_flags(self):
        flags = []
        if self.is_scope:
            flags.append("scope")
        if self.is_active:
            flags.append("active")
        if self.is_concurrent:
            flags.append("concurrent")
        if self.is_completed:
            flags.append("completed")
        return flags


class TokenLogger:
    def __init__(self, graph: DiGraph):
        self.graph = graph

    def log(
        self,
        active_tokens: List[TokenMetadata],
        current_flows: List[str],
        next_flows: List[str],
    ):
        print("📍 Execution DAG (Token Trace):")
        roots = [n for n in self.graph.nodes if self.graph.in_degree(n) == 0]
        for root in roots:
            self._print_dag_recursive(root, "", active_tokens)

        print("\n🧭 Token Metadata:")
        for token in active_tokens:
            if token.is_active:
                element = self.graph.nodes[token.activity_id]["element"]
                print(
                    f"• {token.id} → {element.__class__.__name__} ({element.name or element.id})"
                )
                print(f"   - isScope     : {token.is_scope}")
                print(f"   - isActive    : {token.is_active}")
                print(f"   - isConcurrent: {token.is_concurrent}")
                print(f"   - isCompleted : {token.is_completed}")

        print()
        for token in active_tokens:
            if token.is_active:
                element = self.graph.nodes[token.activity_id]["element"]
                print(
                    f"🟢 Executing: {element.__class__.__name__} ({element.name or element.id}) [{', '.join(token.format_flags())}]"
                )
                for flow in current_flows:
                    print(f"➡️  Flow: {flow}")
                for flow in next_flows:
                    print(f"➡️  Next: {flow}")
                print()

        print("⏭️ Press Enter to proceed...")
        print("************************")
        print("************************")
        print("************************")

    def _print_dag_recursive(
        self, node_id: str, prefix: str, tokens: List[TokenMetadata]
    ):
        element = self.graph.nodes[node_id]["element"]
        token_here = [t for t in tokens if t.activity_id == node_id and t.is_active]
        token_display = ""
        if token_here:
            flags = token_here[0].format_flags()
            token_display = f"   🟢 Token: {token_here[0].id} [{', '.join(flags)}]"

        print(
            prefix
            + "├── "
            + f"{element.__class__.__name__} ({element.name or element.id})"
            + token_display
        )

        successors = list(self.graph.successors(node_id))
        for i, succ in enumerate(successors):
            new_prefix = prefix + ("│   " if i < len(successors) - 1 else "    ")
            self._print_dag_recursive(succ, new_prefix, tokens)

    def on_step(
        self, active_nodes: List[str], visited_nodes: List[str], metadata: dict
    ):
        print("🧭 [TokenLogger] Step executed.")
        print("Active nodes:")
        for node in active_nodes:
            element = self.graph.nodes[node]["element"]
            print(f"• {element.__class__.__name__} ({element.name or element.id})")
        print()
