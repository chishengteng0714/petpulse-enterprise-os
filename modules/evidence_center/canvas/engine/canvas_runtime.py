from .canvas_event_bus import CanvasEventBus
from .canvas_selection import CanvasSelection
from .intelligence_runtime import CanvasIntelligenceRuntime


class CanvasRuntime:
    """
    Canvas Runtime

    Lightweight Runtime Gateway。

    負責：
    - Runtime State
    - Selection State
    - View Mode
    - Layout Mode
    - Panel State
    - Event Dispatch
    - Session-level API Delegation

    不負責 Intelligence Logic。
    """

    def __init__(self, evidence_runtime=None):
        self.evidence_runtime = evidence_runtime

        self.selection = CanvasSelection()
        self.event_bus = CanvasEventBus()

        self.view_mode = "graph"
        self.layout_mode = "default"

        self.panel_state = {
            "inspector": True,
            "notebook": True,
            "copilot": True,
            "decision_queue": True,
            "relationship_map": True,
            "timeline": True,
            "event_log": False,
        }

        self.intelligence_runtime = CanvasIntelligenceRuntime(
            canvas_runtime=self,
        )

    # =========================
    # Evidence Runtime Delegation
    # =========================

    def get_nodes(self):
        if self.evidence_runtime and hasattr(self.evidence_runtime, "get_nodes"):
            return self.evidence_runtime.get_nodes()

        return []

    def get_edges(self):
        if self.evidence_runtime and hasattr(self.evidence_runtime, "get_edges"):
            return self.evidence_runtime.get_edges()

        return []

    def get_actions(self):
        if self.evidence_runtime and hasattr(self.evidence_runtime, "get_actions"):
            return self.evidence_runtime.get_actions()

        return []

    def get_flows(self):
        if self.evidence_runtime and hasattr(self.evidence_runtime, "get_flows"):
            return self.evidence_runtime.get_flows()

        return []

    # =========================
    # Selection API
    # =========================

    def select_node(self, node_id):
        self._set_selection("node", node_id)
        self.dispatch_event(
            event_type="selection_changed",
            payload={
                "object_type": "node",
                "object_id": node_id,
            },
        )

    def select_action(self, action_id):
        self._set_selection("action", action_id)
        self.dispatch_event(
            event_type="selection_changed",
            payload={
                "object_type": "action",
                "object_id": action_id,
            },
        )

    def select_flow(self, flow_id):
        self._set_selection("flow", flow_id)
        self.dispatch_event(
            event_type="selection_changed",
            payload={
                "object_type": "flow",
                "object_id": flow_id,
            },
        )

    def select_evidence(self, evidence_id):
        self._set_selection("evidence", evidence_id)
        self.dispatch_event(
            event_type="selection_changed",
            payload={
                "object_type": "evidence",
                "object_id": evidence_id,
            },
        )

    def clear_selection(self):
        if hasattr(self.selection, "clear"):
            self.selection.clear()
        else:
            self.selection.selected_type = None
            self.selection.selected_id = None

        self.dispatch_event(
            event_type="selection_cleared",
            payload={},
        )

    def get_selected_object(self):
        selected_type = self._get_selected_type()
        selected_id = self._get_selected_id()

        if not selected_type or not selected_id:
            return None

        collections = {
            "node": self.get_nodes(),
            "evidence": self.get_nodes(),
            "action": self.get_actions(),
            "flow": self.get_flows(),
        }

        for item in collections.get(selected_type, []):
            item_id = (
                item.get("id")
                or item.get("evidence_id")
                or item.get("action_id")
                or item.get("flow_id")
            )

            if item_id == selected_id:
                return {
                    **item,
                    "_canvas_object_type": selected_type,
                    "_canvas_object_id": selected_id,
                }

        return {
            "id": selected_id,
            "_canvas_object_type": selected_type,
            "_canvas_object_id": selected_id,
        }

    def _set_selection(self, selected_type, selected_id):
        if hasattr(self.selection, "select"):
            self.selection.select(selected_type, selected_id)
            return

        if hasattr(self.selection, "set_selection"):
            self.selection.set_selection(selected_type, selected_id)
            return

        self.selection.selected_type = selected_type
        self.selection.selected_id = selected_id

    def _get_selected_type(self):
        if hasattr(self.selection, "get_selected_type"):
            return self.selection.get_selected_type()

        if hasattr(self.selection, "selected_type"):
            return self.selection.selected_type

        if hasattr(self.selection, "type"):
            return self.selection.type

        return None

    def _get_selected_id(self):
        if hasattr(self.selection, "get_selected_id"):
            return self.selection.get_selected_id()

        if hasattr(self.selection, "selected_id"):
            return self.selection.selected_id

        if hasattr(self.selection, "id"):
            return self.selection.id

        return None

    # =========================
    # View Mode API
    # =========================

    def set_view_mode(self, view_mode):
        self.view_mode = view_mode
        self.dispatch_event(
            event_type="view_mode_changed",
            payload={"view_mode": view_mode},
        )

    def get_view_mode(self):
        return self.view_mode

    # =========================
    # Layout Mode API
    # =========================

    def set_layout_mode(self, layout_mode):
        self.layout_mode = layout_mode
        self.dispatch_event(
            event_type="layout_mode_changed",
            payload={"layout_mode": layout_mode},
        )

    def get_layout_mode(self):
        return self.layout_mode

    # =========================
    # Panel State API
    # =========================

    def set_panel_state(self, panel_name, is_open):
        self.panel_state[panel_name] = is_open
        self.dispatch_event(
            event_type="panel_state_changed",
            payload={
                "panel_name": panel_name,
                "is_open": is_open,
            },
        )

    def toggle_panel(self, panel_name):
        current = self.panel_state.get(panel_name, False)
        self.set_panel_state(panel_name, not current)

    def get_panel_state(self):
        return self.panel_state

    def is_panel_open(self, panel_name):
        return self.panel_state.get(panel_name, False)

    # =========================
    # Event Bus API
    # =========================

    def dispatch_event(self, event_type, payload=None):
        payload = payload or {}

        if hasattr(self.event_bus, "dispatch"):
            self.event_bus.dispatch(event_type, payload)
            return

        if hasattr(self.event_bus, "emit"):
            self.event_bus.emit(event_type, payload)
            return

    def get_events(self):
        if hasattr(self.event_bus, "get_events"):
            return self.event_bus.get_events()

        if hasattr(self.event_bus, "events"):
            return self.event_bus.events

        return []

    def get_latest_event(self):
        if hasattr(self.event_bus, "get_latest_event"):
            return self.event_bus.get_latest_event()

        events = self.get_events()
        return events[-1] if events else None

    def get_events_by_type(self, event_type):
        if hasattr(self.event_bus, "get_events_by_type"):
            return self.event_bus.get_events_by_type(event_type)

        return [
            event
            for event in self.get_events()
            if event.get("type") == event_type
            or event.get("event_type") == event_type
        ]

    def clear_events(self):
        if hasattr(self.event_bus, "clear"):
            self.event_bus.clear()
            return

        if hasattr(self.event_bus, "clear_events"):
            self.event_bus.clear_events()
            return

        if hasattr(self.event_bus, "events"):
            self.event_bus.events = []

    # =========================
    # Intelligence Delegation API
    # =========================

    def get_selected_relationships(self):
        return self.intelligence_runtime.get_selected_relationships()

    def get_relationship_summary(self):
        return self.intelligence_runtime.get_relationship_summary()

    def get_summary(self):
        return self.intelligence_runtime.get_summary()

    def get_canvas_brief(self):
        return self.intelligence_runtime.get_canvas_brief()

    def get_copilot_context(self):
        return self.intelligence_runtime.get_copilot_context()

    def get_ai_context(self):
        return self.intelligence_runtime.get_ai_context()

    def get_decision_context(self):
        return self.intelligence_runtime.get_decision_context()

    def get_timeline_context(self):
        return self.intelligence_runtime.get_timeline_context()