from .base_presenter import BaseCanvasPresenter


class RelationshipPresenter(BaseCanvasPresenter):
    """
    Relationship Presenter

    將 Relationship Intelligence 轉成 Relationship Map UI View Model。
    """

    def present(self):
        relationship_summary = self._safe_call(
            "get_relationship_summary",
            default={
                "total": 0,
                "relationships": [],
            },
        )

        relationships = relationship_summary.get("relationships", [])

        return {
            "title": "Relationship Intelligence",
            "total": relationship_summary.get("total", 0),
            "message": self._build_message(relationship_summary.get("total", 0)),
            "relationships": self._present_relationships(relationships),
        }

    def _build_message(self, total):
        if total <= 0:
            return "目前尚未偵測到與選取物件直接相關的情報關聯。"

        return f"目前偵測到 {total} 個相關情報關聯。"

    def _present_relationships(self, relationships):
        view_items = []

        for relationship in relationships:
            related_object = relationship.get("related_object", {})

            view_items.append(
                {
                    "title": self._get_object_title(related_object),
                    "type": relationship.get("type", "related"),
                    "label": relationship.get("label", "Related"),
                    "strength": relationship.get("strength", "Medium"),
                    "source": relationship.get("source"),
                    "target": relationship.get("target"),
                    "related_object": related_object,
                }
            )

        return view_items