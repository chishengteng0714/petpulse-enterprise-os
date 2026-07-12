from .base_presenter import BaseCanvasPresenter


class TimelinePresenter(BaseCanvasPresenter):
    """
    Timeline Presenter

    將 Timeline Intelligence Context 轉成 Timeline UI View Model。
    """

    def present(self):
        context = self._safe_call(
            "get_timeline_context",
            default={
                "events": [],
                "latest_event": None,
                "total_events": 0,
            },
        )

        return {
            "title": "Timeline Intelligence",
            "total_events": context.get("total_events", 0),
            "latest_event": context.get("latest_event"),
            "events": self._present_events(context.get("events", [])),
            "message": self._build_message(context.get("total_events", 0)),
        }

    def _build_message(self, total):
        if total <= 0:
            return "目前尚未累積 Canvas 事件。"

        return f"目前已累積 {total} 筆 Canvas 操作事件。"

    def _present_events(self, events):
        view_items = []

        for event in events:
            view_items.append(
                {
                    "type": event.get("type") or event.get("event_type", "event"),
                    "payload": event.get("payload", {}),
                    "timestamp": event.get("timestamp"),
                    "raw": event,
                }
            )

        return view_items