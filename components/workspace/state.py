"""
Enterprise Workspace Store

WorkspaceStore 是 UI 與 Workspace Engine 之間的唯一狀態入口。

UI 不直接理解 analysis data。
UI 不直接理解 workspace_context。
UI 永遠只理解 WorkspaceStore。
"""


class WorkspaceStore:

    def __init__(self, context: dict):
        self.context = context if isinstance(context, dict) else {}

    @property
    def meta(self):
        return self.context.get("meta", {})

    @property
    def raw(self):
        return self.context.get("raw", {})

    @property
    def status(self):
        return self.context.get("workspace_status", {})

    @property
    def focus(self):
        return self.context.get("focus", {})

    @property
    def ai_inbox(self):
        return self.context.get("ai_inbox", [])

    @property
    def priority_queue(self):
        return self.context.get("priority_queue", [])

    @property
    def recent_signals(self):
        return self.context.get("recent_signals", [])

    @property
    def action_queue(self):
        return self.context.get("action_queue", [])

    @property
    def competitor_feed(self):
        return self.context.get("competitor_feed", [])

    @property
    def platform_name(self):
        return self.meta.get(
            "platform",
            "PetPulse Enterprise Intelligence Platform",
        )

    @property
    def engine_name(self):
        return self.meta.get(
            "engine",
            "Enterprise Context Engine",
        )

    @property
    def generated_at(self):
        return self.meta.get("generated_at", "-")

    @property
    def workspace_status(self):
        return self.status.get("status", "Unknown")

    @property
    def workspace_tone(self):
        return self.status.get("tone", "default")

    @property
    def workspace_message(self):
        return self.status.get(
            "message",
            "目前尚未取得品牌狀態。",
        )

    @property
    def health(self):
        return self.status.get("health", 0)

    @property
    def health_delta(self):
        return self.status.get("delta", 0)

    @property
    def today_focus(self):
        return self.focus.get(
            "title",
            "今日重點尚未產生",
        )

    @property
    def today_focus_description(self):
        return self.focus.get(
            "description",
            "目前尚未取得今日重點說明。",
        )

    @property
    def today_focus_priority(self):
        return self.focus.get("priority", "Low")

    @property
    def inbox_count(self):
        return len(self.ai_inbox)

    @property
    def high_priority_count(self):
        return len(
            [
                item
                for item in self.ai_inbox
                if item.get("priority") == "High"
            ]
        )

    @property
    def pending_action_count(self):
        return len(self.action_queue)

    @property
    def signal_count(self):
        return len(self.recent_signals)

    @property
    def competitor_count(self):
        return len(self.competitor_feed)

    def to_debug_dict(self):
        return {
            "meta": self.meta,
            "workspace": {
                "status": self.workspace_status,
                "tone": self.workspace_tone,
                "message": self.workspace_message,
                "health": self.health,
                "health_delta": self.health_delta,
            },
            "focus": {
                "title": self.today_focus,
                "description": self.today_focus_description,
                "priority": self.today_focus_priority,
            },
            "counts": {
                "ai_inbox": self.inbox_count,
                "high_priority": self.high_priority_count,
                "pending_actions": self.pending_action_count,
                "recent_signals": self.signal_count,
                "competitors": self.competitor_count,
            },
            "raw": self.raw,
        }


WorkspaceState = WorkspaceStore