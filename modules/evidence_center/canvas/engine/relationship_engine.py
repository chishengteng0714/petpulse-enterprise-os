class RelationshipEngine:
    """
    Canvas Relationship Intelligence Engine

    負責整理 Canvas 內的關聯情報。
    不回頭呼叫 Canvas Runtime 的 get_selected_relationships，
    避免 Intelligence Runtime 與 Canvas Runtime 互相遞迴。
    """

    def __init__(self, canvas_runtime):
        self.canvas_runtime = canvas_runtime

    def get_selected_relationships(self):
        selected_object = self._get_selected_object()

        if not selected_object:
            return []

        selected_id = selected_object.get("id") or selected_object.get("evidence_id")

        if not selected_id:
            return []

        edges = self._get_edges()
        nodes = self._get_nodes()

        node_lookup = {}
        for node in nodes:
            node_id = node.get("id") or node.get("evidence_id")
            if node_id:
                node_lookup[node_id] = node

        relationships = []

        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")

            if selected_id not in [source, target]:
                continue

            related_id = target if source == selected_id else source

            relationships.append(
                {
                    "source": source,
                    "target": target,
                    "type": edge.get("type", "related"),
                    "label": edge.get("label", "Related"),
                    "strength": edge.get("strength", "Medium"),
                    "related_object": node_lookup.get(related_id, {}),
                    "edge": edge,
                }
            )

        return relationships

    def get_relationship_summary(self):
        relationships = self.get_selected_relationships()

        return {
            "total": len(relationships),
            "relationships": relationships,
        }

    def _get_selected_object(self):
        if not self.canvas_runtime:
            return None

        if hasattr(self.canvas_runtime, "get_selected_object"):
            return self.canvas_runtime.get_selected_object()

        return None

    def _get_nodes(self):
        if not self.canvas_runtime:
            return []

        if hasattr(self.canvas_runtime, "get_nodes"):
            return self.canvas_runtime.get_nodes()

        return []

    def _get_edges(self):
        if not self.canvas_runtime:
            return []

        if hasattr(self.canvas_runtime, "get_edges"):
            return self.canvas_runtime.get_edges()

        return []