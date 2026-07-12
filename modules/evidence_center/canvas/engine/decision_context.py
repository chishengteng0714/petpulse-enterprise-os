class DecisionContextBuilder:
    """
    Decision Intelligence Context Builder

    負責建立 Decision Queue、Action Queue、Strategy Planning 使用的決策上下文。
    """

    def __init__(self, canvas_runtime, summary_builder=None):
        self.canvas_runtime = canvas_runtime
        self.summary_builder = summary_builder

    def build(self):
        summary = self.summary_builder.build() if self.summary_builder else {}

        return {
            "selected_object": summary.get("selected_object"),
            "relationship_summary": summary.get("relationship_summary"),
            "recommended_focus": self._build_recommended_focus(summary),
        }

    def _build_recommended_focus(self, summary):
        selected_object = summary.get("selected_object")

        if not selected_object:
            return "尚未選取 Canvas 物件。"

        return "根據目前選取物件，檢查相關證據、關聯節點與下一步行動。"