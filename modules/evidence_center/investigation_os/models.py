from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================
# Core Graph Models
# ============================================================

@dataclass
class InvestigationNode:
    node_id: str
    label: str
    node_type: str = "evidence"
    description: str = ""
    score: float = 0.0

    platform: str = "Unknown"
    topic: str = "Unknown"
    sentiment: str = "Unknown"

    evidence_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    is_focus: bool = False
    is_selected: bool = False
    is_hidden: bool = False


@dataclass
class InvestigationEdge:
    edge_id: str
    source: str
    target: str
    relationship: str = "related"
    weight: float = 1.0
    description: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    is_highlighted: bool = False
    is_hidden: bool = False


@dataclass
class InvestigationGraph:
    nodes: list[InvestigationNode] = field(default_factory=list)
    edges: list[InvestigationEdge] = field(default_factory=list)

    focus_node_id: str | None = None
    selected_node_id: str | None = None
    active_relationship: str | None = None
    active_node_type: str | None = None

    def get_node(self, node_id: str) -> InvestigationNode | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_edge(self, edge_id: str) -> InvestigationEdge | None:
        for edge in self.edges:
            if edge.edge_id == edge_id:
                return edge
        return None

    def visible_nodes(self) -> list[InvestigationNode]:
        return [node for node in self.nodes if not node.is_hidden]

    def visible_edges(self) -> list[InvestigationEdge]:
        visible_node_ids = {node.node_id for node in self.visible_nodes()}

        return [
            edge
            for edge in self.edges
            if not edge.is_hidden
            and edge.source in visible_node_ids
            and edge.target in visible_node_ids
        ]

    def connected_node_ids(self, node_id: str) -> set[str]:
        connected = set()

        for edge in self.edges:
            if edge.source == node_id:
                connected.add(edge.target)

            if edge.target == node_id:
                connected.add(edge.source)

        return connected


# ============================================================
# Action Models
# ============================================================

@dataclass
class InvestigationAction:
    action_id: str
    title: str
    description: str

    action_type: str = "inspect"
    priority: str = "Medium"
    status: str = "Ready"

    target_node_id: str | None = None
    target_evidence_id: str | None = None

    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class InvestigationActionResult:
    action_id: str
    status: str
    message: str

    data: dict[str, Any] = field(default_factory=dict)
    executed_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# Flow Models
# ============================================================

@dataclass
class InvestigationFlowStep:
    step_id: str
    title: str
    description: str

    action_type: str = "inspect"
    priority: str = "Medium"
    status: str = "Todo"

    node_id: str | None = None
    evidence_id: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class InvestigationFlow:
    flow_id: str
    title: str
    description: str

    steps: list[InvestigationFlowStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# Runtime Model
# ============================================================

@dataclass
class InvestigationRuntime:
    graph: InvestigationGraph
    actions: list[InvestigationAction] = field(default_factory=list)
    flow: InvestigationFlow | None = None

    last_action_result: InvestigationActionResult | None = None

    cycle_count: int = 0
    status: str = "Ready"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())