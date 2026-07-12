from .base_presenter import BaseCanvasPresenter


class DecisionPresenter(BaseCanvasPresenter):
    """
    Decision Presenter

    將 Decision Intelligence Context 轉成 Decision Queue UI View Model。
    """

    def present(self):
        context = self._safe_call("get_decision_context", default={})
        selected_object = context.get("selected_object")
        relationship_summary = context.get("relationship_summary", {})

        return {
            "title": "Decision Intelligence",
            "selected_title": self._get_object_title(selected_object)
            if selected_object
            else "尚未選取物件",
            "selected_object": selected_object,
            "relationship_total": relationship_summary.get("total", 0),
            "recommended_focus": context.get(
                "recommended_focus",
                "請先選取一個 Evidence、Action 或 Flow。",
            ),
            "decision_cards": self._build_decision_cards(
                selected_object=selected_object,
                relationship_summary=relationship_summary,
            ),
        }

    def _build_decision_cards(self, selected_object, relationship_summary):
        if not selected_object:
            return [
                {
                    "title": "等待分析目標",
                    "status": "Idle",
                    "description": "請先從 Canvas 選取一個物件，Decision Intelligence 會整理下一步。",
                }
            ]

        cards = [
            {
                "title": "確認核心證據",
                "status": "Ready",
                "description": "檢查此物件是否有足夠來源證據支撐決策。",
            },
            {
                "title": "評估商業影響",
                "status": "Ready",
                "description": "判斷此訊號是否影響品牌、通路、競品或消費者信任。",
            },
        ]

        if relationship_summary.get("total", 0) > 0:
            cards.append(
                {
                    "title": "檢查關聯脈絡",
                    "status": "Recommended",
                    "description": "此物件已有相關情報，建議優先檢查 Relationship Map。",
                }
            )

        return cards