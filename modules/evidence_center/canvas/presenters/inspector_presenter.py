from .base_presenter import BaseCanvasPresenter


class InspectorPresenter(BaseCanvasPresenter):
    """
    Inspector Presenter

    將 Canvas Brief 轉成 Inspector UI View Model。
    """

    def present(self):
        brief = self._safe_call("get_canvas_brief", default={})

        selected_object = brief.get("selected_object")

        return {
            "title": "Inspector Intelligence",
            "status": brief.get("status", "No Selection"),
            "selected_object": selected_object,
            "selected_type": brief.get("selected_object_type") or "None",
            "selected_title": self._get_object_title(selected_object)
            if selected_object
            else "尚未選取物件",
            "focus": brief.get("focus", "尚未選取分析目標。"),
            "risk_note": brief.get("risk_note", "目前沒有足夠上下文判斷風險。"),
            "next_step": brief.get("next_step", "請先選取一個 Canvas 物件。"),
            "runtime_counts": brief.get("runtime_counts", {}),
            "canvas_state": brief.get("canvas_state", {}),
            "latest_event": brief.get("latest_event"),
        }