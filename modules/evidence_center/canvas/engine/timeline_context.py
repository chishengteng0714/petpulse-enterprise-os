class TimelineContextBuilder:
    """
    Timeline Intelligence Context Builder

    負責整理時間線上下文，未來可接：
    - Evidence evolution
    - Event sequence
    - Investigation history
    """

    def __init__(self, canvas_runtime):
        self.canvas_runtime = canvas_runtime

    def build(self):
        events = self._get_events()

        return {
            "events": events,
            "latest_event": events[-1] if events else None,
            "total_events": len(events),
        }

    def _get_events(self):
        if not self.canvas_runtime:
            return []

        if hasattr(self.canvas_runtime, "get_events"):
            return self.canvas_runtime.get_events()

        return []