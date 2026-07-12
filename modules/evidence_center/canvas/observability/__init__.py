"""
Canvas Observability Module

Enterprise Observability Platform for Canvas Runtime.

此模組集中管理 Canvas Runtime 的可觀測能力：

- Overview
- Snapshot
- Runtime
- Session
- Context
- Timeline
- Presenter
- API
- Contracts
- Performance
- Health Summary
- Technical Debt
- Observability Service
- Architecture Map

設計原則：
- 每個 Panel 單一責任
- Runtime Debug Center 僅作為 Assembler
- Observability 不改變 Runtime 狀態
- 所有讀取皆採安全容錯
- Panel 透過 Service 取得 Enterprise Snapshot
"""

from modules.evidence_center.canvas.observability.api_panel import (
    render_api_panel,
)
from modules.evidence_center.canvas.observability.architecture import (
    get_observability_architecture_diagram,
    get_observability_architecture_map,
    get_observability_folder_tree,
)
from modules.evidence_center.canvas.observability.context_panel import (
    render_context_panel,
)
from modules.evidence_center.canvas.observability.contract_panel import (
    render_contract_panel,
)
from modules.evidence_center.canvas.observability.health_summary import (
    build_observability_health_summary,
)
from modules.evidence_center.canvas.observability.models import (
    DebtSeverity,
    HealthDetail,
    HealthStatus,
    HealthSummary,
    PerformanceCheckResult,
    RuntimeMetrics,
    TechnicalDebtItem,
    TechnicalDebtRegistry,
    build_technical_debt_registry_from_items,
)
from modules.evidence_center.canvas.observability.overview_panel import (
    render_overview_panel,
)
from modules.evidence_center.canvas.observability.performance_panel import (
    render_performance_panel,
)
from modules.evidence_center.canvas.observability.presenter_panel import (
    render_presenter_panel,
)
from modules.evidence_center.canvas.observability.runtime_debug_center import (
    render_runtime_debug_center,
)
from modules.evidence_center.canvas.observability.runtime_panel import (
    render_runtime_panel,
)
from modules.evidence_center.canvas.observability.service import (
    ObservabilityService,
    create_observability_service,
)
from modules.evidence_center.canvas.observability.session_panel import (
    render_session_panel,
)
from modules.evidence_center.canvas.observability.snapshot_panel import (
    render_snapshot_panel,
)
from modules.evidence_center.canvas.observability.technical_debt import (
    build_technical_debt_registry,
)
from modules.evidence_center.canvas.observability.timeline_panel import (
    render_timeline_panel,
)


__all__ = [
    "DebtSeverity",
    "HealthDetail",
    "HealthStatus",
    "HealthSummary",
    "ObservabilityService",
    "PerformanceCheckResult",
    "RuntimeMetrics",
    "TechnicalDebtItem",
    "TechnicalDebtRegistry",
    "build_observability_health_summary",
    "build_technical_debt_registry",
    "build_technical_debt_registry_from_items",
    "create_observability_service",
    "get_observability_architecture_diagram",
    "get_observability_architecture_map",
    "get_observability_folder_tree",
    "render_api_panel",
    "render_context_panel",
    "render_contract_panel",
    "render_overview_panel",
    "render_performance_panel",
    "render_presenter_panel",
    "render_runtime_debug_center",
    "render_runtime_panel",
    "render_session_panel",
    "render_snapshot_panel",
    "render_timeline_panel",
]