from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================
# Studio Core Models
# ============================================================

@dataclass
class StudioEvidenceRef:
    evidence_id: str
    title: str
    platform: str = "Unknown"
    topic: str = "Unknown"
    sentiment: str = "Unknown"
    engagement: int = 0
    content_preview: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StudioGraphNode:
    node_id: str
    label: str
    node_type: str = "evidence"
    evidence_id: str | None = None
    size: int = 24
    score: float = 0.0
    group: str = "default"
    color_hint: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StudioGraphEdge:
    edge_id: str
    source: str
    target: str
    relationship: str = "related"
    weight: float = 1.0
    label: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StudioGraph:
    nodes: list[StudioGraphNode] = field(default_factory=list)
    edges: list[StudioGraphEdge] = field(default_factory=list)
    selected_node_id: str | None = None
    focus_node_id: str | None = None
    active_relationship: str | None = None
    active_group: str | None = None


# ============================================================
# Studio Workspace Models
# ============================================================

@dataclass
class StudioBasketItem:
    evidence_id: str
    title: str
    reason: str = ""
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class StudioNote:
    note_id: str
    title: str
    body: str
    evidence_id: str | None = None
    node_id: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class StudioCase:
    case_id: str
    title: str
    description: str = ""
    status: str = "Open"
    evidence_ids: list[str] = field(default_factory=list)
    notes: list[StudioNote] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class InvestigationStudioRuntime:
    evidence_refs: list[StudioEvidenceRef] = field(default_factory=list)
    graph: StudioGraph = field(default_factory=StudioGraph)
    basket: list[StudioBasketItem] = field(default_factory=list)
    active_case: StudioCase | None = None
    selected_evidence_id: str | None = None
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())