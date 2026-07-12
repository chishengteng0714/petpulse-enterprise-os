# modules/evidence_center/canvas/presenters/copilot_presenter.py

from .base_presenter import BaseCanvasPresenter


class CopilotPresenter(BaseCanvasPresenter):
    """
    Copilot Presenter

    將 Copilot Intelligence Context 轉成 AI Copilot UI View Model。
    """

    def present(self):
        context = self._safe_call("get_copilot_context", default={})

        evidence_context = context.get("evidence_context", {})
        relationship_context = context.get("relationship_context", {})
        risk_context = context.get("risk_context", {})

        return {
            "title": context.get("title", "Copilot Intelligence Context"),
            "mode": context.get("mode", "idle"),
            "selected_type": context.get("selected_object_type") or "None",
            "focus": context.get("user_focus") or "尚未選取分析目標。",
            "evidence": {
                "available": evidence_context.get("available", False),
                "message": evidence_context.get("message"),
                "content": evidence_context.get("content", "Untitled"),
                "platform": evidence_context.get("platform", "Unknown"),
                "topic": evidence_context.get("topic", "Unknown"),
                "sentiment": evidence_context.get("sentiment", "Unknown"),
                "priority": evidence_context.get("priority", "Unknown"),
                "ai_summary": evidence_context.get("ai_summary"),
            },
            "relationships": {
                "available": relationship_context.get("available", False),
                "total": relationship_context.get("total", 0),
                "message": relationship_context.get(
                    "message",
                    "目前尚未偵測到明確關聯。",
                ),
                "items": self._present_relationships(
                    relationship_context.get("relationships", [])
                ),
            },
            "risk": {
                "risk_note": risk_context.get(
                    "risk_note",
                    "目前沒有足夠上下文判斷風險。",
                ),
                "next_step": risk_context.get(
                    "next_step",
                    "請先選取一個分析目標。",
                ),
            },
            "recommended_prompts": context.get("recommended_prompts", []),
            "next_best_question": context.get(
                "next_best_question",
                "你想先分析哪一個 Evidence 或 Canvas 節點？",
            ),
        }

    def _present_relationships(self, relationships):
        view_items = []

        for relationship in relationships:
            related_object = relationship.get("related_object", {})

            view_items.append(
                {
                    "content": self._get_object_title(related_object)
                    or relationship.get("label", "Related Object"),
                    "type": relationship.get("type", "related"),
                    "strength": relationship.get("strength", "Medium"),
                    "source": relationship.get("source"),
                    "target": relationship.get("target"),
                }
            )

        return view_items