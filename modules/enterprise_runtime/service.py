from __future__ import annotations

from typing import Any

from modules.enterprise_runtime.models import (
    EnterpriseRuntimeContext,
    EnterpriseRuntimeLayer,
    EnterpriseRuntimeSnapshot,
    EnterpriseRuntimeStatus,
)


class EnterpriseRuntimeService:
    """
    Enterprise Runtime Service

    PetPulse Enterprise Intelligence Platform 的頂層 Runtime。

    目的：
    - 統一接管 Evidence Runtime
    - 統一接管 Canvas Runtime
    - 統一接管 Canvas Intelligence
    - 統一接管 Enterprise Observability
    - 提供 Enterprise Intelligence Hub 單一上游 Context
    """

    def __init__(
        self,
        enterprise_workspace: Any | None = None,
        evidence_runtime: Any | None = None,
        canvas_runtime: Any | None = None,
        canvas_intelligence: Any | None = None,
        enterprise_observability: Any | None = None,
        enterprise_intelligence: Any | None = None,
    ):
        self.enterprise_workspace = enterprise_workspace
        self.evidence_runtime = evidence_runtime
        self.canvas_runtime = canvas_runtime
        self.canvas_intelligence = canvas_intelligence
        self.enterprise_observability = enterprise_observability
        self.enterprise_intelligence = enterprise_intelligence

    def get_context(self) -> EnterpriseRuntimeContext:
        snapshots = [
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.ENTERPRISE_WORKSPACE,
                runtime=self.enterprise_workspace,
                expected_methods=[
                    "get_workspace_context",
                    "get_focus",
                    "get_ai_inbox",
                    "get_priority_queue",
                    "get_recent_signals",
                    "get_action_queue",
                ],
            ),
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.EVIDENCE_RUNTIME,
                runtime=self.evidence_runtime,
                expected_methods=[
                    "get_nodes",
                    "get_edges",
                    "get_actions",
                    "get_flows",
                    "get_summary",
                ],
            ),
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.CANVAS_RUNTIME,
                runtime=self.canvas_runtime,
                expected_methods=[
                    "get_selected_object",
                    "get_event_log",
                    "get_view_mode",
                    "get_layout_mode",
                    "get_panel_state",
                ],
            ),
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.CANVAS_INTELLIGENCE,
                runtime=self.canvas_intelligence,
                expected_methods=[
                    "get_relationships",
                    "get_summary",
                    "get_copilot_context",
                    "get_decision_context",
                    "get_timeline_context",
                ],
            ),
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.ENTERPRISE_OBSERVABILITY,
                runtime=self.enterprise_observability,
                expected_methods=[
                    "get_enterprise_snapshot",
                    "get_health_summary",
                    "get_technical_debt",
                ],
            ),
            self._inspect_layer(
                layer=EnterpriseRuntimeLayer.ENTERPRISE_INTELLIGENCE,
                runtime=self.enterprise_intelligence,
                expected_methods=[
                    "get_hub_state",
                    "get_summary",
                    "get_signals",
                    "get_domains",
                ],
            ),
        ]

        summary = self._build_summary(snapshots)

        return EnterpriseRuntimeContext(
            status=summary["status"],
            title="Enterprise Runtime",
            description=(
                "The top-level runtime context for PetPulse Enterprise Intelligence "
                "Platform v1.0. It normalizes workspace, evidence, canvas, "
                "observability, and intelligence layers into one shared enterprise context."
            ),
            snapshots=snapshots,
            summary=summary,
        )

    def get_snapshots(self) -> list[EnterpriseRuntimeSnapshot]:
        return self.get_context().snapshots

    def get_summary(self) -> dict[str, Any]:
        return self.get_context().summary

    def _inspect_layer(
        self,
        layer: EnterpriseRuntimeLayer,
        runtime: Any | None,
        expected_methods: list[str],
    ) -> EnterpriseRuntimeSnapshot:
        if runtime is None:
            return EnterpriseRuntimeSnapshot(
                layer=layer,
                status=EnterpriseRuntimeStatus.NOT_CONNECTED,
                runtime_type="None",
                available_methods=[],
                missing_methods=expected_methods,
            )

        available_methods = [
            method for method in expected_methods if hasattr(runtime, method)
        ]

        missing_methods = [
            method for method in expected_methods if not hasattr(runtime, method)
        ]

        status = (
            EnterpriseRuntimeStatus.READY
            if not missing_methods
            else EnterpriseRuntimeStatus.DEGRADED
        )

        return EnterpriseRuntimeSnapshot(
            layer=layer,
            status=status,
            runtime_type=runtime.__class__.__name__,
            available_methods=available_methods,
            missing_methods=missing_methods,
        )

    def _build_summary(
        self,
        snapshots: list[EnterpriseRuntimeSnapshot],
    ) -> dict[str, Any]:
        total_layers = len(snapshots)
        ready_layers = len(
            [
                snapshot
                for snapshot in snapshots
                if snapshot.status == EnterpriseRuntimeStatus.READY
            ]
        )
        degraded_layers = len(
            [
                snapshot
                for snapshot in snapshots
                if snapshot.status == EnterpriseRuntimeStatus.DEGRADED
            ]
        )
        not_connected_layers = len(
            [
                snapshot
                for snapshot in snapshots
                if snapshot.status == EnterpriseRuntimeStatus.NOT_CONNECTED
            ]
        )

        if ready_layers == total_layers:
            status = EnterpriseRuntimeStatus.READY
        elif ready_layers > 0 or degraded_layers > 0:
            status = EnterpriseRuntimeStatus.DEGRADED
        else:
            status = EnterpriseRuntimeStatus.NOT_CONNECTED

        return {
            "status": status,
            "total_layers": total_layers,
            "ready_layers": ready_layers,
            "degraded_layers": degraded_layers,
            "not_connected_layers": not_connected_layers,
        }


def create_enterprise_runtime_service(
    enterprise_workspace: Any | None = None,
    evidence_runtime: Any | None = None,
    canvas_runtime: Any | None = None,
    canvas_intelligence: Any | None = None,
    enterprise_observability: Any | None = None,
    enterprise_intelligence: Any | None = None,
) -> EnterpriseRuntimeService:
    return EnterpriseRuntimeService(
        enterprise_workspace=enterprise_workspace,
        evidence_runtime=evidence_runtime,
        canvas_runtime=canvas_runtime,
        canvas_intelligence=canvas_intelligence,
        enterprise_observability=enterprise_observability,
        enterprise_intelligence=enterprise_intelligence,
    )