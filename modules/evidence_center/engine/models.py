from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================
# Evidence Reference
# ============================================================

@dataclass
class EngineEvidence:
    evidence_id: str
    title: str
    content: str = ""

    platform: str = "Unknown"
    topic: str = "Unknown"
    sentiment: str = "Unknown"
    engagement: int = 0

    source_url: str = ""
    created_time: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================
# Unified Graph Models
# ============================================================

@dataclass
class EngineNode:
    node_id: str
    label: str
    node_type: str = "evidence"

    evidence_id: str | None = None
    description: str = ""

    platform: str = "Unknown"
    topic: str = "Unknown"
    sentiment: str = "Unknown"

    score: float = 0.0
    size: int = 24
    group: str = "default"

    metadata: dict[str, Any] = field(default_factory=dict)

    is_focus: bool = False
    is_selected: bool = False
    is_hidden: bool = False


@dataclass
class EngineEdge:
    edge_id: str
    source: str
    target: str

    relationship: str = "related"
    label: str = ""
    description: str = ""

    weight: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    is_highlighted: bool = False
    is_hidden: bool = False


@dataclass
class EngineGraph:
    nodes: list[EngineNode] = field(default_factory=list)
    edges: list[EngineEdge] = field(default_factory=list)

    focus_node_id: str | None = None
    selected_node_id: str | None = None
    active_relationship: str | None = None
    active_node_type: str | None = None
    active_group: str | None = None

    def get_node(self, node_id: str) -> EngineNode | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_edge(self, edge_id: str) -> EngineEdge | None:
        for edge in self.edges:
            if edge.edge_id == edge_id:
                return edge
        return None

    def visible_nodes(self) -> list[EngineNode]:
        return [node for node in self.nodes if not node.is_hidden]

    def visible_edges(self) -> list[EngineEdge]:
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
class EngineAction:
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
class EngineActionResult:
    action_id: str
    status: str
    message: str

    data: dict[str, Any] = field(default_factory=dict)
    executed_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# Flow Models
# ============================================================

@dataclass
class EngineFlowStep:
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
class EngineFlow:
    flow_id: str
    title: str
    description: str

    steps: list[EngineFlowStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# Case / Basket / Note Models
# ============================================================

@dataclass
class EngineBasketItem:
    evidence_id: str
    title: str
    reason: str = ""
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EngineNote:
    note_id: str
    title: str
    body: str

    evidence_id: str | None = None
    node_id: str | None = None

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EngineCase:
    case_id: str
    title: str
    description: str = ""
    status: str = "Open"

    evidence_ids: list[str] = field(default_factory=list)
    notes: list[EngineNote] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# Runtime
# ============================================================

@dataclass
class EngineRuntime:
    evidence: list[EngineEvidence] = field(default_factory=list)
    graph: EngineGraph = field(default_factory=EngineGraph)
    actions: list[EngineAction] = field(default_factory=list)
    flow: EngineFlow | None = None

    basket: list[EngineBasketItem] = field(default_factory=list)
    active_case: EngineCase | None = None

    selected_evidence_id: str | None = None
    selected_evidence_id_2: str | None = None

    last_action_result: EngineActionResult | None = None

    cycle_count: int = 0
    status: str = "Ready"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())