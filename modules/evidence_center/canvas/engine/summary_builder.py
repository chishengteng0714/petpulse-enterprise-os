class CanvasSummaryBuilder:
    """
    Canvas Intelligence Summary Builder

    將 Canvas Runtime 狀態整理成 Enterprise Canvas Brief。

    這不是 UI 摘要。
    這是未來 AI Copilot、Decision Intelligence、
    Executive Briefing、Strategy Planning 共用的情報摘要。
    """

    def __init__(self, canvas_runtime, relationship_engine=None):
        self.canvas_runtime = canvas_runtime
        self.relationship_engine = relationship_engine

    def build(self):
        selected_object = self._get_selected_object()
        relationship_summary = self._get_relationship_summary()
        canvas_state = self._get_canvas_state()
        runtime_counts = self._get_runtime_counts()
        latest_event = self._get_latest_event()

        return {
            "title": "Canvas Intelligence Brief",
            "status": self._build_status(selected_object),
            "selected_object": selected_object,
            "selected_object_type": self._get_selected_object_type(selected_object),
            "relationship_summary": relationship_summary,
            "runtime_counts": runtime_counts,
            "canvas_state": canvas_state,
            "latest_event": latest_event,
            "focus": self._build_focus(selected_object, relationship_summary),
            "risk_note": self._build_risk_note(selected_object, relationship_summary),
            "next_step": self._build_next_step(selected_object, relationship_summary),
        }

    # =========================
    # Brief Intelligence
    # =========================

    def _build_status(self, selected_object):
        if not selected_object:
            return "No Selection"

        object_type = self._get_selected_object_type(selected_object)

        if object_type:
            return f"Selected {object_type.title()}"

        return "Selected Object"

    def _build_focus(self, selected_object, relationship_summary):
        if not selected_object:
            return "尚未選取 Canvas 物件，請先從 Graph、Timeline 或 Queue 選擇一個分析目標。"

        title = self._get_object_title(selected_object)
        total_relationships = relationship_summary.get("total", 0)

        if total_relationships <= 0:
            return f"目前焦點為「{title}」，尚未找到明確關聯物件。"

        return f"目前焦點為「{title}」，已偵測到 {total_relationships} 個相關情報關聯。"

    def _build_risk_note(self, selected_object, relationship_summary):
        if not selected_object:
            return "目前沒有足夠上下文判斷風險。"

        sentiment = str(selected_object.get("sentiment", "")).lower()
        priority = str(selected_object.get("priority", "")).lower()
        total_relationships = relationship_summary.get("total", 0)

        if "negative" in sentiment or "high" in priority:
            return "此物件可能具有較高風險，建議優先檢查來源證據與後續行動。"

        if total_relationships >= 3:
            return "此物件已連結多個相關訊號，可能代表議題正在形成脈絡。"

        return "目前未偵測到明顯高風險訊號。"

    def _build_next_step(self, selected_object, relationship_summary):
        if not selected_object:
            return "請先選取一個 Evidence、Node、Action 或 Flow。"

        total_relationships = relationship_summary.get("total", 0)

        if total_relationships <= 0:
            return "建議補充更多 Evidence 或檢查是否需要建立關聯。"

        return "建議檢查 Relationship Map，確認是否需要加入 Decision Queue 或建立 Action。"

    # =========================
    # Data Access
    # =========================

    def _get_selected_object(self):
        if not self.canvas_runtime:
            return None

        if hasattr(self.canvas_runtime, "get_selected_object"):
            return self.canvas_runtime.get_selected_object()

        return None

    def _get_relationship_summary(self):
        if self.relationship_engine:
            return self.relationship_engine.get_relationship_summary()

        return {
            "total": 0,
            "relationships": [],
        }

    def _get_canvas_state(self):
        if not self.canvas_runtime:
            return {}

        return {
            "view_mode": self._safe_call("get_view_mode", default="graph"),
            "layout_mode": self._safe_call("get_layout_mode", default="default"),
            "panel_state": self._safe_call("get_panel_state", default={}),
        }

    def _get_runtime_counts(self):
        return {
            "nodes": len(self._safe_call("get_nodes", default=[])),
            "edges": len(self._safe_call("get_edges", default=[])),
            "actions": len(self._safe_call("get_actions", default=[])),
            "flows": len(self._safe_call("get_flows", default=[])),
            "events": len(self._safe_call("get_events", default=[])),
        }

    def _get_latest_event(self):
        return self._safe_call("get_latest_event", default=None)

    def _safe_call(self, method_name, default=None):
        if not self.canvas_runtime:
            return default

        if not hasattr(self.canvas_runtime, method_name):
            return default

        try:
            return getattr(self.canvas_runtime, method_name)()
        except Exception:
            return default

    # =========================
    # Object Helpers
    # =========================

    def _get_selected_object_type(self, selected_object):
        if not selected_object:
            return None

        return (
            selected_object.get("_canvas_object_type")
            or selected_object.get("type")
            or selected_object.get("object_type")
            or "object"
        )

    def _get_object_title(self, selected_object):
        if not selected_object:
            return "Unknown"

        return (
            selected_object.get("title")
            or selected_object.get("label")
            or selected_object.get("name")
            or selected_object.get("summary")
            or selected_object.get("id")
            or selected_object.get("evidence_id")
            or "Untitled Object"
        )