from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EnterpriseRuntimeLayer(str, Enum):
    ENTERPRISE_WORKSPACE = "Enterprise Workspace"
    EVIDENCE_RUNTIME = "Evidence Runtime"
    CANVAS_RUNTIME = "Canvas Runtime"
    CANVAS_INTELLIGENCE = "Canvas Intelligence"
    ENTERPRISE_OBSERVABILITY = "Enterprise Observability"
    ENTERPRISE_INTELLIGENCE = "Enterprise Intelligence"


class EnterpriseRuntimeStatus(str, Enum):
    READY = "Ready"
    DEGRADED = "Degraded"
    NOT_CONNECTED = "Not Connected"


@dataclass
class EnterpriseRuntimeSnapshot:
    layer: EnterpriseRuntimeLayer
    status: EnterpriseRuntimeStatus
    runtime_type: str = "Unknown"
    available_methods: list[str] = field(default_factory=list)
    missing_methods: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EnterpriseRuntimeContext:
    status: EnterpriseRuntimeStatus
    title: str
    description: str
    snapshots: list[EnterpriseRuntimeSnapshot]
    summary: dict[str, Any] = field(default_factory=dict)