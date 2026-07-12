"""
Canvas Observability Architecture Map

集中記錄 Sprint C2 Enterprise Observability Platform 的架構狀態。
此檔案不負責 UI，只負責提供架構資訊與 Definition of Done。
"""


def get_observability_architecture_map():
    return {
        "module": "Canvas Observability",
        "sprint": "Sprint C2",
        "status": "Completed",
        "goal": "Enterprise Observability Platform for Canvas Runtime",
        "principles": [
            "Maintainability",
            "Observability",
            "Testability",
            "Scalability",
        ],
        "layers": {
            "Assembler": [
                "runtime_debug_center.py",
            ],
            "Service": [
                "service.py",
            ],
            "Models": [
                "models.py",
            ],
            "Builders": [
                "health_summary.py",
                "technical_debt.py",
            ],
            "Panels": [
                "overview_panel.py",
                "snapshot_panel.py",
                "runtime_panel.py",
                "session_panel.py",
                "context_panel.py",
                "timeline_panel.py",
                "presenter_panel.py",
                "api_panel.py",
                "contract_panel.py",
                "performance_panel.py",
            ],
            "Helpers": [
                "ui_helpers.py",
            ],
        },
        "runtime_debug_center_role": (
            "Assembler only. It owns tab composition and safe rendering, "
            "but does not own diagnostics or business logic."
        ),
        "service_role": (
            "Single application-service entry point for health summary, "
            "technical debt registry and enterprise observability snapshot."
        ),
        "definition_of_done": [
            "Runtime Debug Center is modularized.",
            "Every Observability Panel has a single responsibility.",
            "Overview Panel uses ObservabilityService.",
            "Snapshot Panel exposes Enterprise Observability Snapshot.",
            "Health Summary is centralized.",
            "Technical Debt Registry is centralized.",
            "Observability Models are defined.",
            "Service fallback prevents Observability from crashing the app.",
            "Architecture map is available for future Sprint planning.",
        ],
        "next_roadmap": [
            {
                "sprint": "Sprint D",
                "name": "Enterprise Intelligence Hub",
                "goal": "Turn Canvas Intelligence and Observability into a cross-platform intelligence command layer.",
            },
            {
                "sprint": "Sprint E",
                "name": "Executive Briefing",
                "goal": "Generate leadership-ready insight summaries from Evidence, Runtime, Canvas and Observability snapshots.",
            },
            {
                "sprint": "Sprint F",
                "name": "Strategy Planning Center",
                "goal": "Transform signals and evidence into strategic plans, priorities and action scenarios.",
            },
            {
                "sprint": "Sprint G",
                "name": "Enterprise Multi-Agent Runtime",
                "goal": "Introduce specialized agents for evidence, strategy, risk, competitor and executive briefing workflows.",
            },
        ],
    }


def get_observability_folder_tree():
    return """
canvas/observability/

├── __init__.py
├── architecture.py
├── ui_helpers.py
│
├── models.py
├── service.py
│
├── health_summary.py
├── technical_debt.py
│
├── overview_panel.py
├── snapshot_panel.py
├── runtime_panel.py
├── session_panel.py
├── context_panel.py
├── timeline_panel.py
├── presenter_panel.py
├── api_panel.py
├── contract_panel.py
├── performance_panel.py
│
└── runtime_debug_center.py
""".strip()


def get_observability_architecture_diagram():
    return """
Enterprise Observability Platform

Runtime Debug Center
        │
        ▼
Observability Panel Registry
        │
        ├── Overview Panel
        ├── Snapshot Panel
        ├── Runtime Panel
        ├── Session Panel
        ├── Context Panel
        ├── Timeline Panel
        ├── Presenter Panel
        ├── API Panel
        ├── Contract Panel
        └── Performance Panel
        │
        ▼
Observability Service
        │
        ├── Health Summary Builder
        ├── Technical Debt Registry
        └── Enterprise Snapshot
        │
        ▼
Observability Models
        │
        ├── HealthStatus
        ├── DebtSeverity
        ├── RuntimeMetrics
        ├── HealthDetail
        ├── HealthSummary
        ├── PerformanceCheckResult
        ├── TechnicalDebtItem
        └── TechnicalDebtRegistry
""".strip()