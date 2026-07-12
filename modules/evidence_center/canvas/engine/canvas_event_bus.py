from datetime import datetime


class CanvasEventBus:
    """
    Canvas Event Bus

    Canvas Runtime 的事件中心。

    職責：
    - 接收 Runtime Events
    - 保存 Event Log
    - 提供最新事件
    - 提供事件查詢
    - 支援未來 Audit Trail / Decision Replay / Copilot Memory
    """

    def __init__(self):
        self.events = []

    def emit(self, event_type, payload=None):
        """
        發送事件並寫入 Event Log。
        """

        event = {
            "event_type": event_type,
            "payload": payload or {},
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }

        self.events.append(event)

        return event

    def get_events(self):
        """
        取得所有事件。
        """

        return self.events

    def get_latest_event(self):
        """
        取得最新事件。
        """

        if not self.events:
            return None

        return self.events[-1]

    def get_events_by_type(self, event_type):
        """
        依事件類型查詢事件。
        """

        return [
            event
            for event in self.events
            if event.get("event_type") == event_type
        ]

    def clear_events(self):
        """
        清空 Event Log。
        """

        self.events = []

    def get_summary(self):
        """
        取得 Event Bus Summary。
        """

        latest_event = self.get_latest_event()

        return {
            "event_count": len(self.events),
            "latest_event_type": (
                latest_event.get("event_type")
                if latest_event
                else None
            ),
            "latest_event_timestamp": (
                latest_event.get("timestamp")
                if latest_event
                else None
            ),
        }