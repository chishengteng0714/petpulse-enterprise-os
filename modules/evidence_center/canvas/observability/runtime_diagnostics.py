from dataclasses import dataclass, field
from datetime import datetime
import importlib
from typing import Any

from .runtime_contracts import RuntimeContractReport, RuntimeContractTester


@dataclass
class RuntimeHealthCheck:
    name: str
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeDiagnosticsReport:
    generated_at: str
    runtime_health: list[RuntimeHealthCheck]
    engine_health: list[RuntimeHealthCheck]
    presenter_health: list[RuntimeHealthCheck]
    api_health: list[RuntimeHealthCheck]
    session_snapshot: dict[str, Any]
    context_snapshot: dict[str, Any]
    event_snapshot: dict[str, Any]
    performance_snapshot: dict[str, Any]
    presenter_snapshot: dict[str, Any]
    contract_report: RuntimeContractReport


PRESENTER_MODULES = [
    {
        "name": "BaseCanvasPresenter",
        "module": "modules.evidence_center.canvas.presenters.base_canvas_presenter",
        "class_name": "BaseCanvasPresenter",
    },
    {
        "name": "CopilotPresenter",
        "module": "modules.evidence_center.canvas.presenters.copilot_presenter",
        "class_name": "CopilotPresenter",
    },
    {
        "name": "DecisionPresenter",
        "module": "modules.evidence_center.canvas.presenters.decision_presenter",
        "class_name": "DecisionPresenter",
    },
    {
        "name": "RelationshipPresenter",
        "module": "modules.evidence_center.canvas.presenters.relationship_presenter",
        "class_name": "RelationshipPresenter",
    },
    {
        "name": "TimelinePresenter",
        "module": "modules.evidence_center.canvas.presenters.timeline_presenter",
        "class_name": "TimelinePresenter",
    },
    {
        "name": "InspectorPresenter",
        "module": "modules.evidence_center.canvas.presenters.inspector_presenter",
        "class_name": "InspectorPresenter",
    },
]


def _safe_call(target: Any, method_name: str, default: Any = None):
    try:
        method = getattr(target, method_name, None)

        if not callable(method):
            return default

        return method()
    except Exception as error:
        return {
            "error": str(error),
            "method": method_name,
        }


def _safe_len(value: Any) -> int:
    try:
        if value is None:
            return 0

        return len(value)
    except Exception:
        return 0


def _safe_value(value: Any):
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool, list, tuple, dict)):
        return value

    if hasattr(value, "value"):
        return value.value

    if hasattr(value, "__dict__"):
        return {
            key: _safe_value(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }

    return str(value)


def _snapshot_object(target: Any) -> dict[str, Any]:
    if target is None:
        return {
            "available": False,
            "type": None,
            "values": {},
        }

    values = {}

    if hasattr(target, "__dict__"):
        for key, value in vars(target).items():
            if key.startswith("_"):
                continue

            values[key] = _safe_value(value)

    return {
        "available": True,
        "type": type(target).__name__,
        "values": values,
    }


def _status_from_error(value: Any) -> str:
    if isinstance(value, dict) and value.get("error"):
        return "Error"

    return "Healthy"


def _build_health_check(name: str, value: Any, success_message: str) -> RuntimeHealthCheck:
    status = _status_from_error(value)

    if status == "Error":
        return RuntimeHealthCheck(
            name=name,
            status="Error",
            message=value.get("error", "Unknown runtime error"),
            details=value,
        )

    return RuntimeHealthCheck(
        name=name,
        status="Healthy",
        message=success_message,
        details={
            "type": type(value).__name__,
            "count": _safe_len(value),
        },
    )


class RuntimeDiagnosticsCollector:
    """
    Enterprise Runtime Diagnostics Collector

    負責將 Canvas Runtime / Intelligence Runtime / Presenter Layer / API Contract
    轉換成可觀測、可測試、可擴充的 Runtime Diagnostics Report。
    """

    def __init__(self, runtime: Any):
        self.runtime = runtime

    def collect(self) -> RuntimeDiagnosticsReport:
        selected_object = _safe_call(
            self.runtime,
            "get_selected_object",
            default=None,
        )

        summary = _safe_call(
            self.runtime,
            "get_summary",
            default={},
        )

        events = _safe_call(
            self.runtime,
            "get_events",
            default=[],
        )

        latest_event = _safe_call(
            self.runtime,
            "get_latest_event",
            default=None,
        )

        relationships = _safe_call(
            self.runtime,
            "get_selected_relationships",
            default=[],
        )

        presenter_health, presenter_snapshot = self._collect_presenter_diagnostics()
        contract_report = RuntimeContractTester(self.runtime).run()

        runtime_health = [
            _build_health_check(
                name="Canvas Runtime",
                value=self.runtime,
                success_message="Canvas Runtime instance is available.",
            ),
            _build_health_check(
                name="Selected Object API",
                value=selected_object,
                success_message="Unified Selected Object API is reachable.",
            ),
            _build_health_check(
                name="Runtime Summary API",
                value=summary,
                success_message="Runtime Summary API is reachable.",
            ),
        ]

        engine_health = [
            _build_health_check(
                name="Relationship Engine",
                value=relationships,
                success_message="Relationship context is available.",
            ),
            _build_health_check(
                name="Event Bus",
                value=events,
                success_message="Runtime Event Bus is available.",
            ),
        ]

        api_health = [
            RuntimeHealthCheck(
                name="get_selected_object()",
                status=_status_from_error(selected_object),
                message="Unified selected object endpoint checked.",
                details={
                    "result_type": type(selected_object).__name__,
                    "has_value": selected_object is not None,
                },
            ),
            RuntimeHealthCheck(
                name="get_events()",
                status=_status_from_error(events),
                message="Event stream endpoint checked.",
                details={
                    "event_count": _safe_len(events),
                },
            ),
            RuntimeHealthCheck(
                name="get_latest_event()",
                status=_status_from_error(latest_event),
                message="Latest event endpoint checked.",
                details={
                    "has_latest_event": latest_event is not None,
                    "result_type": type(latest_event).__name__,
                },
            ),
            RuntimeHealthCheck(
                name="get_selected_relationships()",
                status=_status_from_error(relationships),
                message="Relationship endpoint checked.",
                details={
                    "relationship_count": _safe_len(relationships),
                },
            ),
            RuntimeHealthCheck(
                name="get_summary()",
                status=_status_from_error(summary),
                message="Summary endpoint checked.",
                details={
                    "summary_type": type(summary).__name__,
                    "summary_keys": list(summary.keys()) if isinstance(summary, dict) else [],
                },
            ),
        ]

        event_snapshot = self._collect_event_snapshot(
            events=events,
            latest_event=latest_event,
        )

        session_snapshot = self._collect_session_snapshot()
        context_snapshot = self._collect_context_snapshot(
            selected_object=selected_object,
            summary=summary,
            relationships=relationships,
        )
        performance_snapshot = self._collect_performance_snapshot(
            events=events,
            relationships=relationships,
            summary=summary,
            presenter_snapshot=presenter_snapshot,
            contract_report=contract_report,
            event_snapshot=event_snapshot,
            context_snapshot=context_snapshot,
        )

        return RuntimeDiagnosticsReport(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            runtime_health=runtime_health,
            engine_health=engine_health,
            presenter_health=presenter_health,
            api_health=api_health,
            session_snapshot=session_snapshot,
            context_snapshot=context_snapshot,
            event_snapshot=event_snapshot,
            performance_snapshot=performance_snapshot,
            presenter_snapshot=presenter_snapshot,
            contract_report=contract_report,
        )

    def _collect_presenter_diagnostics(self):
        checks = []
        modules = []

        for presenter in PRESENTER_MODULES:
            module_path = presenter["module"]
            class_name = presenter["class_name"]
            display_name = presenter["name"]

            try:
                module = importlib.import_module(module_path)
                presenter_class = getattr(module, class_name, None)

                if presenter_class is None:
                    checks.append(
                        RuntimeHealthCheck(
                            name=display_name,
                            status="Error",
                            message="Presenter class was not found.",
                            details={
                                "module": module_path,
                                "class_name": class_name,
                            },
                        )
                    )

                    modules.append(
                        {
                            "name": display_name,
                            "module": module_path,
                            "class_name": class_name,
                            "status": "Error",
                            "reason": "Class not found",
                        }
                    )

                    continue

                checks.append(
                    RuntimeHealthCheck(
                        name=display_name,
                        status="Healthy",
                        message="Presenter module and class are available.",
                        details={
                            "module": module_path,
                            "class_name": class_name,
                            "class_type": type(presenter_class).__name__,
                        },
                    )
                )

                modules.append(
                    {
                        "name": display_name,
                        "module": module_path,
                        "class_name": class_name,
                        "status": "Healthy",
                    }
                )

            except Exception as error:
                checks.append(
                    RuntimeHealthCheck(
                        name=display_name,
                        status="Error",
                        message=str(error),
                        details={
                            "module": module_path,
                            "class_name": class_name,
                            "error": str(error),
                        },
                    )
                )

                modules.append(
                    {
                        "name": display_name,
                        "module": module_path,
                        "class_name": class_name,
                        "status": "Error",
                        "reason": str(error),
                    }
                )

        healthy_count = len([item for item in modules if item.get("status") == "Healthy"])
        error_count = len([item for item in modules if item.get("status") == "Error"])

        snapshot = {
            "presenter_count": len(modules),
            "healthy_count": healthy_count,
            "error_count": error_count,
            "presenters": modules,
        }

        return checks, snapshot

    def _collect_session_snapshot(self) -> dict[str, Any]:
        session = getattr(self.runtime, "session", None)
        state = getattr(self.runtime, "state", None)

        selection_state = getattr(self.runtime, "selection", None)
        panel_state = getattr(self.runtime, "panel_state", None)
        layout_mode = getattr(self.runtime, "layout_mode", None)
        view_mode = getattr(self.runtime, "view_mode", None)

        return {
            "runtime": {
                "runtime_type": type(self.runtime).__name__,
                "attributes": sorted(
                    [
                        key
                        for key in dir(self.runtime)
                        if not key.startswith("_")
                    ]
                ),
            },
            "session": {
                "has_session": session is not None,
                "session_type": type(session).__name__ if session is not None else None,
                "snapshot": _snapshot_object(session),
            },
            "state": {
                "has_state": state is not None,
                "state_type": type(state).__name__ if state is not None else None,
                "snapshot": _snapshot_object(state),
            },
            "selection": {
                "has_selection_state": selection_state is not None,
                "selection_type": type(selection_state).__name__ if selection_state is not None else None,
                "snapshot": _snapshot_object(selection_state),
            },
            "panel": {
                "has_panel_state": panel_state is not None,
                "panel_state_type": type(panel_state).__name__ if panel_state is not None else None,
                "snapshot": _snapshot_object(panel_state),
            },
            "modes": {
                "layout_mode": _safe_value(layout_mode),
                "view_mode": _safe_value(view_mode),
            },
        }

    def _collect_context_snapshot(
        self,
        selected_object: Any,
        summary: Any,
        relationships: Any,
    ) -> dict[str, Any]:
        safe_summary = summary if isinstance(summary, dict) else {}
        safe_relationships = relationships if isinstance(relationships, list) else []

        selected_diagnostics = self._build_selected_object_diagnostics(selected_object)
        summary_diagnostics = self._build_summary_diagnostics(safe_summary)
        relationship_diagnostics = self._build_relationship_diagnostics(safe_relationships)

        return {
            "selected_object": selected_object,
            "summary": summary,
            "relationships": safe_relationships,
            "relationship_count": len(safe_relationships),
            "selected_diagnostics": selected_diagnostics,
            "summary_diagnostics": summary_diagnostics,
            "relationship_diagnostics": relationship_diagnostics,
        }

    def _build_selected_object_diagnostics(self, selected_object: Any) -> dict[str, Any]:
        selected_type = None
        selected_id = None
        selected_title = None

        if isinstance(selected_object, dict):
            selected_type = (
                selected_object.get("type")
                or selected_object.get("object_type")
                or selected_object.get("kind")
            )
            selected_id = (
                selected_object.get("id")
                or selected_object.get("node_id")
                or selected_object.get("evidence_id")
                or selected_object.get("action_id")
                or selected_object.get("flow_id")
            )
            selected_title = (
                selected_object.get("title")
                or selected_object.get("label")
                or selected_object.get("name")
            )

        elif selected_object is not None:
            selected_type = getattr(selected_object, "type", None) or type(selected_object).__name__
            selected_id = (
                getattr(selected_object, "id", None)
                or getattr(selected_object, "node_id", None)
                or getattr(selected_object, "evidence_id", None)
                or getattr(selected_object, "action_id", None)
                or getattr(selected_object, "flow_id", None)
            )
            selected_title = (
                getattr(selected_object, "title", None)
                or getattr(selected_object, "label", None)
                or getattr(selected_object, "name", None)
            )

        return {
            "has_selected_object": selected_object is not None,
            "selected_type": _safe_value(selected_type),
            "selected_id": _safe_value(selected_id),
            "selected_title": _safe_value(selected_title),
            "payload_type": type(selected_object).__name__,
            "payload_size": _safe_len(selected_object) if selected_object is not None else 0,
        }

    def _build_summary_diagnostics(self, summary: dict[str, Any]) -> dict[str, Any]:
        return {
            "has_summary": bool(summary),
            "summary_type": type(summary).__name__,
            "summary_key_count": len(summary.keys()),
            "summary_keys": list(summary.keys()),
            "has_title": "title" in summary,
            "has_brief": "brief" in summary,
            "has_recommendations": "recommendations" in summary,
            "has_risks": "risks" in summary,
            "has_actions": "actions" in summary,
        }

    def _build_relationship_diagnostics(self, relationships: list[Any]) -> dict[str, Any]:
        relationship_types = {}

        for relationship in relationships:
            relationship_type = self._extract_relationship_type(relationship)
            relationship_types[relationship_type] = relationship_types.get(relationship_type, 0) + 1

        return {
            "has_relationships": len(relationships) > 0,
            "relationship_count": len(relationships),
            "relationship_types": dict(
                sorted(
                    relationship_types.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ),
            "unique_relationship_types": len(relationship_types),
        }

    def _extract_relationship_type(self, relationship: Any) -> str:
        if isinstance(relationship, dict):
            return (
                relationship.get("type")
                or relationship.get("relationship_type")
                or relationship.get("kind")
                or "unknown"
            )

        if hasattr(relationship, "type"):
            return str(getattr(relationship, "type"))

        if hasattr(relationship, "relationship_type"):
            return str(getattr(relationship, "relationship_type"))

        if hasattr(relationship, "kind"):
            return str(getattr(relationship, "kind"))

        return "unknown"

    def _collect_event_snapshot(
        self,
        events: Any,
        latest_event: Any,
    ) -> dict[str, Any]:
        safe_events = events if isinstance(events, list) else []
        event_types = self._count_event_types(safe_events)
        event_stream = self._build_event_stream(safe_events)

        return {
            "events": safe_events,
            "event_count": len(safe_events),
            "latest_event": latest_event,
            "event_types": event_types,
            "unique_event_types": len(event_types),
            "event_stream": event_stream,
        }

    def _count_event_types(self, events: list[Any]) -> dict[str, int]:
        result = {}

        for event in events:
            event_type = self._extract_event_type(event)
            result[event_type] = result.get(event_type, 0) + 1

        return dict(
            sorted(
                result.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

    def _build_event_stream(self, events: list[Any]) -> list[dict[str, Any]]:
        stream = []

        for index, event in enumerate(events, start=1):
            event_type = self._extract_event_type(event)

            stream.append(
                {
                    "index": index,
                    "type": event_type,
                    "payload_type": type(event).__name__,
                    "payload": _safe_value(event),
                }
            )

        return stream

    def _extract_event_type(self, event: Any) -> str:
        if isinstance(event, dict):
            return (
                event.get("type")
                or event.get("event_type")
                or event.get("name")
                or "unknown"
            )

        if hasattr(event, "type"):
            return str(getattr(event, "type"))

        if hasattr(event, "event_type"):
            return str(getattr(event, "event_type"))

        if hasattr(event, "name"):
            return str(getattr(event, "name"))

        return "unknown"

    def _collect_performance_snapshot(
        self,
        events: Any,
        relationships: Any,
        summary: Any,
        presenter_snapshot: dict[str, Any],
        contract_report: RuntimeContractReport,
        event_snapshot: dict[str, Any],
        context_snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        summary_diagnostics = context_snapshot.get("summary_diagnostics", {})
        selected_diagnostics = context_snapshot.get("selected_diagnostics", {})

        return {
            "event_count": _safe_len(events),
            "unique_event_types": event_snapshot.get("unique_event_types", 0),
            "relationship_count": _safe_len(relationships),
            "summary_size": summary_diagnostics.get("summary_key_count", 0),
            "has_selected_object": selected_diagnostics.get("has_selected_object", False),
            "presenter_count": presenter_snapshot.get("presenter_count", 0),
            "healthy_presenters": presenter_snapshot.get("healthy_count", 0),
            "contract_total": contract_report.total,
            "contract_passed": contract_report.passed,
            "contract_failed": contract_report.failed,
            "runtime_object_type": type(self.runtime).__name__,
        }