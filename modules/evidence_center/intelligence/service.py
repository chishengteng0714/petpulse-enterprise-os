from __future__ import annotations

from typing import Any

from modules.evidence_center.intelligence.models import (
    EnterpriseIntelligenceDomain,
    EnterpriseIntelligenceHubState,
    EnterpriseIntelligenceSignal,
    EnterpriseIntelligenceSummary,
)


class EnterpriseIntelligenceService:
    """
    Enterprise Intelligence Service

    Sprint D 的平台級 Intelligence Core。

    這不是 Dashboard。
    這是未來所有 Enterprise Intelligence 能力的共同入口：

    - Executive Briefing
    - Strategy Planning
    - Enterprise AI Intelligence
    - Risk Analysis
    - Opportunity Discovery
    - Cross Workspace Intelligence
    - Enterprise Agent Runtime
    """

    def __init__(
        self,
        evidence_runtime: Any | None = None,
        canvas_runtime: Any | None = None,
        canvas_intelligence_runtime: Any | None = None,
        observability_service: Any | None = None,
    ):
        self.evidence_runtime = evidence_runtime
        self.canvas_runtime = canvas_runtime
        self.canvas_intelligence_runtime = canvas_intelligence_runtime
        self.observability_service = observability_service

    def get_hub_state(self) -> EnterpriseIntelligenceHubState:
        runtime_context = self._build_runtime_context()
        signals = self._build_foundation_signals(runtime_context)
        summary = self._build_summary(runtime_context, signals)

        return EnterpriseIntelligenceHubState(
            status="Ready",
            layer_name="Enterprise Intelligence Hub",
            description=(
                "The shared Enterprise Intelligence Layer for executive briefing, "
                "strategy planning, enterprise AI, risk analysis, opportunity discovery, "
                "cross-workspace intelligence, and future agent runtime."
            ),
            domains=list(EnterpriseIntelligenceDomain),
            signals=signals,
            summary=summary,
            runtime_context=runtime_context,
        )

    def get_signals(self) -> list[EnterpriseIntelligenceSignal]:
        return self.get_hub_state().signals

    def get_summary(self) -> EnterpriseIntelligenceSummary:
        return self.get_hub_state().summary

    def get_domains(self) -> list[EnterpriseIntelligenceDomain]:
        return list(EnterpriseIntelligenceDomain)

    def _build_runtime_context(self) -> dict[str, Any]:
        return {
            "evidence_runtime": self._inspect_runtime(
                self.evidence_runtime,
                expected_methods=[
                    "get_nodes",
                    "get_edges",
                    "get_actions",
                    "get_flows",
                    "get_summary",
                ],
            ),
            "canvas_runtime": self._inspect_runtime(
                self.canvas_runtime,
                expected_methods=[
                    "get_selected_object",
                    "get_event_log",
                    "get_view_mode",
                    "get_layout_mode",
                ],
            ),
            "canvas_intelligence_runtime": self._inspect_runtime(
                self.canvas_intelligence_runtime,
                expected_methods=[
                    "get_relationships",
                    "get_summary",
                    "get_copilot_context",
                    "get_decision_context",
                    "get_timeline_context",
                ],
            ),
            "observability_service": self._inspect_runtime(
                self.observability_service,
                expected_methods=[
                    "get_enterprise_snapshot",
                    "get_health_summary",
                    "get_technical_debt",
                ],
            ),
        }

    def _inspect_runtime(
        self,
        runtime: Any | None,
        expected_methods: list[str],
    ) -> dict[str, Any]:
        if runtime is None:
            return {
                "connected": False,
                "available_methods": [],
                "missing_methods": expected_methods,
            }

        available_methods = [
            method for method in expected_methods if hasattr(runtime, method)
        ]

        missing_methods = [
            method for method in expected_methods if not hasattr(runtime, method)
        ]

        return {
            "connected": True,
            "runtime_type": runtime.__class__.__name__,
            "available_methods": available_methods,
            "missing_methods": missing_methods,
        }

    def _build_foundation_signals(
        self,
        runtime_context: dict[str, Any],
    ) -> list[EnterpriseIntelligenceSignal]:
        connected_layers = [
            name
            for name, state in runtime_context.items()
            if state.get("connected") is True
        ]

        signals = [
            EnterpriseIntelligenceSignal(
                signal_id="ei-foundation-001",
                title="Enterprise Intelligence Layer initialized",
                description=(
                    "Enterprise Intelligence Hub is now available as the shared "
                    "foundation for future executive, strategy, AI, risk, and opportunity modules."
                ),
                domain=EnterpriseIntelligenceDomain.CROSS_WORKSPACE,
                priority="High",
                metadata={
                    "connected_layers": connected_layers,
                    "layer_count": len(connected_layers),
                },
            ),
            EnterpriseIntelligenceSignal(
                signal_id="ei-foundation-002",
                title="Executive Briefing foundation ready",
                description=(
                    "The hub can now provide a single summary contract for future "
                    "executive briefing modules."
                ),
                domain=EnterpriseIntelligenceDomain.EXECUTIVE_BRIEFING,
                priority="High",
            ),
            EnterpriseIntelligenceSignal(
                signal_id="ei-foundation-003",
                title="Strategy Planning foundation ready",
                description=(
                    "The hub establishes the shared domain model required for future "
                    "strategy planning and decision orchestration."
                ),
                domain=EnterpriseIntelligenceDomain.STRATEGY_PLANNING,
                priority="Medium",
            ),
            EnterpriseIntelligenceSignal(
                signal_id="ei-foundation-004",
                title="Enterprise AI foundation ready",
                description=(
                    "The hub creates a clean service boundary for future copilot, "
                    "multi-agent, and enterprise AI workflows."
                ),
                domain=EnterpriseIntelligenceDomain.ENTERPRISE_AI,
                priority="Medium",
            ),
        ]

        return signals

    def _build_summary(
        self,
        runtime_context: dict[str, Any],
        signals: list[EnterpriseIntelligenceSignal],
    ) -> EnterpriseIntelligenceSummary:
        connected_count = sum(
            1 for state in runtime_context.values() if state.get("connected") is True
        )

        return EnterpriseIntelligenceSummary(
            title="Enterprise Intelligence Hub Foundation",
            narrative=(
                "Sprint D Step 1 establishes the Enterprise Intelligence Hub as the "
                "single shared intelligence layer above Evidence Runtime, Canvas Runtime, "
                "Canvas Intelligence, and Enterprise Observability. This foundation is "
                "designed to support executive briefing, strategy planning, enterprise AI, "
                "risk analysis, opportunity discovery, cross-workspace intelligence, and "
                "future agent runtime."
            ),
            key_points=[
                "Enterprise Intelligence Hub folder and service boundary created.",
                "Shared intelligence domain model created.",
                "Hub state, signals, and summary contracts created.",
                f"{connected_count} upstream runtime layer(s) currently connected.",
                f"{len(signals)} foundation signal(s) available.",
            ],
            risks=[
                "No UI surface has been connected yet.",
                "No executive briefing renderer exists yet.",
                "No strategy planning workflow exists yet.",
            ],
            opportunities=[
                "Executive Briefing can now be built on top of a stable hub contract.",
                "Strategy Planning can reuse the same intelligence state.",
                "Enterprise AI and Agent Runtime can share the same service boundary.",
            ],
            recommended_actions=[
                "Build Enterprise Intelligence Hub workspace entry.",
                "Add Executive Briefing module.",
                "Add Strategy Planning module.",
                "Connect Observability snapshot into Enterprise Intelligence summary.",
            ],
        )


def create_enterprise_intelligence_service(
    evidence_runtime: Any | None = None,
    canvas_runtime: Any | None = None,
    canvas_intelligence_runtime: Any | None = None,
    observability_service: Any | None = None,
) -> EnterpriseIntelligenceService:
    return EnterpriseIntelligenceService(
        evidence_runtime=evidence_runtime,
        canvas_runtime=canvas_runtime,
        canvas_intelligence_runtime=canvas_intelligence_runtime,
        observability_service=observability_service,
    )