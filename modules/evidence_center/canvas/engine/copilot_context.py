# modules/evidence_center/canvas/engine/copilot_context.py

class CopilotContextBuilder:
    """
    AI Copilot Context Builder

    將 Canvas Intelligence Brief 轉換成 AI Copilot 可理解的任務上下文。

    這一層不產生 UI。
    這一層負責建立：
    - User Focus
    - Investigation Context
    - Evidence Context
    - Relationship Context
    - Suggested Copilot Prompts
    """

    def __init__(self, canvas_runtime, summary_builder=None):
        self.canvas_runtime = canvas_runtime
        self.summary_builder = summary_builder

    def build(self):
        summary = self.summary_builder.build() if self.summary_builder else {}
        selected_object = summary.get("selected_object")
        relationship_summary = summary.get("relationship_summary", {})

        return {
            "title": "Copilot Intelligence Context",
            "purpose": "Assist user investigation based on current Canvas Intelligence.",
            "mode": self._build_mode(selected_object),
            "user_focus": summary.get("focus"),
            "selected_object": selected_object,
            "selected_object_type": summary.get("selected_object_type"),
            "evidence_context": self._build_evidence_context(selected_object),
            "relationship_context": self._build_relationship_context(relationship_summary),
            "runtime_context": self._build_runtime_context(summary),
            "risk_context": self._build_risk_context(summary),
            "recommended_prompts": self._build_recommended_prompts(
                selected_object=selected_object,
                relationship_summary=relationship_summary,
            ),
            "next_best_question": self._build_next_best_question(
                selected_object=selected_object,
                relationship_summary=relationship_summary,
            ),
        }

    # =========================
    # Context Sections
    # =========================

    def _build_mode(self, selected_object):
        if not selected_object:
            return "idle"

        object_type = selected_object.get("_canvas_object_type")

        if object_type in ["node", "evidence"]:
            return "evidence_investigation"

        if object_type == "action":
            return "action_planning"

        if object_type == "flow":
            return "flow_analysis"

        return "canvas_analysis"

    def _build_evidence_context(self, selected_object):
        if not selected_object:
            return {
                "available": False,
                "message": "尚未選取 Evidence 或 Canvas 物件。",
            }

        return {
            "available": True,
            "id": self._get_object_id(selected_object),
            "content": self._get_object_content(selected_object),
            "topic": selected_object.get("topic"),
            "platform": selected_object.get("platform"),
            "source": selected_object.get("source"),
            "sentiment": selected_object.get("sentiment"),
            "priority": selected_object.get("priority"),
            "ai_summary": (
                selected_object.get("ai_summary")
                or selected_object.get("description")
                or selected_object.get("content")
            ),
            "original_url": selected_object.get("original_url"),
        }

    def _build_relationship_context(self, relationship_summary):
        relationships = relationship_summary.get("relationships", [])
        total = relationship_summary.get("total", 0)

        return {
            "available": total > 0,
            "total": total,
            "relationships": relationships,
            "message": self._build_relationship_message(total),
        }

    def _build_runtime_context(self, summary):
        return {
            "canvas_state": summary.get("canvas_state", {}),
            "runtime_counts": summary.get("runtime_counts", {}),
            "latest_event": summary.get("latest_event"),
        }

    def _build_risk_context(self, summary):
        return {
            "risk_note": summary.get("risk_note"),
            "next_step": summary.get("next_step"),
        }

    # =========================
    # Prompt Intelligence
    # =========================

    def _build_recommended_prompts(self, selected_object, relationship_summary):
        if not selected_object:
            return [
                "請先選取一個 Evidence，讓我協助你整理重點。",
                "我可以幫你從目前 Canvas 找出值得優先追蹤的訊號。",
                "請選擇 Graph 上的節點，我可以幫你分析關聯脈絡。",
            ]

        object_type = selected_object.get("_canvas_object_type")
        total_relationships = relationship_summary.get("total", 0)

        prompts = [
            "請幫我整理這個物件的核心洞察。",
            "這個訊號代表什麼商業風險或機會？",
            "下一步我應該採取什麼行動？",
        ]

        if object_type in ["node", "evidence"]:
            prompts.append("請幫我把相關 Evidence 整理成決策摘要。")

        if total_relationships > 0:
            prompts.append("請分析這些關聯訊號之間可能形成的議題脈絡。")

        if object_type == "action":
            prompts.append("請幫我評估這個 Action 是否值得優先執行。")

        if object_type == "flow":
            prompts.append("請幫我檢查這個 Flow 是否有缺漏步驟。")

        return prompts

    def _build_next_best_question(self, selected_object, relationship_summary):
        if not selected_object:
            return "你想先分析哪一個 Evidence 或 Canvas 節點？"

        total_relationships = relationship_summary.get("total", 0)

        if total_relationships > 0:
            return "你要我先幫你分析關聯脈絡，還是直接整理成決策建議？"

        return "你要我先幫你整理這個物件的重點、風險，還是下一步行動？"

    # =========================
    # Text Helpers
    # =========================

    def _build_relationship_message(self, total):
        if total <= 0:
            return "目前尚未偵測到明確關聯。"

        return f"目前偵測到 {total} 個相關情報關聯。"

    def _get_object_id(self, item):
        if not item:
            return None

        return (
            item.get("id")
            or item.get("evidence_id")
            or item.get("action_id")
            or item.get("flow_id")
        )

    def _get_object_content(self, item):
        if not item:
            return "Unknown"

        return (
            item.get("content")
            or item.get("label")
            or item.get("name")
            or item.get("id")
            or item.get("evidence_id")
            or "Untitled Object"
        )

    def _get_object_title(self, item):
        if not item:
            return "Unknown"

        return (
            item.get("title")
            or item.get("label")
            or item.get("name")
            or item.get("id")
            or item.get("evidence_id")
            or "Untitled Object"
        )