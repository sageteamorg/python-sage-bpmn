import datetime
from typing import Dict, List

from networkx import DiGraph

from sage_bpmn.design.interfaces import ExecutionObserver
from sage_bpmn.models import Token


class ConsoleObserver(ExecutionObserver):
    ICONS = {
        "StartEvent": "🟢",
        "EndEvent": "🔴",
        "Task": "✅",
        "UserTask": "👤",
        "ReceiveTask": "📨",
        "ServiceTask": "⚙️",
        "ScriptTask": "📜",
        "SendTask": "✉",
        "ExclusiveGateway": "🔀",
        "ParallelGateway": "⏸️",
        "InclusiveGateway": "➕",
        "SubProcess": "📦",
        "CallActivity": "📞",
    }

    def __init__(self, graph: DiGraph):
        self.graph = graph
        self.token_history = {}  # token_id → list of timestamps
        self.tokens: Dict[str, Token] = {}  # activity_id → Token

    def on_step(
        self,
        active_nodes: List[str],
        visited_nodes: List[str],
        metadata: Dict[str, dict],
    ):
        print("\n🧭 BPMN Execution Step\n" + "=" * 60)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for node_id in active_nodes:
            el = self.graph.nodes[node_id]["element"]
            meta = metadata.get(node_id, {})

            # Create or update Token
            if node_id not in self.tokens:
                token = Token.from_metadata(node_id, meta, is_active=True)
                self.tokens[node_id] = token
            else:
                token = self.tokens[node_id]
                token.is_active = True
                token.is_concurrent = meta.get("isConcurrent", False)
                token.is_completed = meta.get("isCompleted", False)

            self.token_history.setdefault(token.id, []).append(timestamp)

            el_type = el.__class__.__name__
            el_name = el.name or el.id
            icon = self.ICONS.get(el_type, "🔸")

            # Log
            print(f"{icon} Token **{token.id}** entered {el_type}: *{el_name}*")
            print(f"   🆔 Activity ID: {token.activity_id}")
            print(f"   🕒 Timestamp: {timestamp}")

            for pred in self.graph.predecessors(node_id):
                flow = self.graph.edges[pred, node_id].get("flow")
                if flow:
                    print(f"   🔄 From: {flow.sourceRef} ➡ {flow.targetRef}")

            for succ in self.graph.successors(node_id):
                flow = self.graph.edges.get((node_id, succ), {}).get("flow")
                if flow:
                    print(f"   🔁 To:   {flow.sourceRef} ➡ {flow.targetRef}")

            print("   🧩 Token State:")
            print(f"      • isActive     : {'✅' if token.is_active else '❌'}")
            print(
                f"      • isConcurrent : {'🧵 Yes' if token.is_concurrent else '— No'}"
            )
            print(
                f"      • isCompleted  : {'✔️ Done' if token.is_completed else '… Pending'}"
            )
            print(f"      • isScope      : {'🌐 Yes' if token.is_scope else '— No'}")

            if len(self.token_history[token.id]) > 1:
                print(f"   📚 Token History: {self.token_history[token.id]}")

            print("-" * 60)
