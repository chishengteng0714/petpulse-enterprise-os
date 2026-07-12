# modules/evidence_center/investigation_os/graph_engine.py

from typing import Any

from modules.evidence_center.investigation_os.models import (
    InvestigationEdge,
    InvestigationGraph,
    InvestigationNode,
)


class InvestigationGraphEngine:
    """
    Investigation Graph Engine

    負責將 Evidence Items 轉換成 Investigation Graph。

    GM-06 Final Schema Consistency Audit：
    - Evidence 讀取來源對齊 Golden Master Schema
    - Graph Domain 保留 label / node / edge 語意
    - 不改變 Graph Architecture
    """

    def build(self, evidence_items: list[Any]) -> InvestigationGraph:
        nodes = self._build_nodes(evidence_items)
        edges = self._build_edges(nodes)

        return InvestigationGraph(
            nodes=nodes,
            edges=edges,
        )

    def focus_node(
        self,
        graph: InvestigationGraph,
        node_id: str,
    ) -> InvestigationGraph:
        graph.focus_node_id = node_id
        graph.selected_node_id = node_id

        connected_ids = graph.connected_node_ids(node_id)
        visible_ids = connected_ids | {node_id}

        for node in graph.nodes:
            node.is_focus = node.node_id == node_id
            node.is_selected = node.node_id == node_id
            node.is_hidden = node.node_id not in visible_ids

        for edge in graph.edges:
            edge.is_highlighted = (
                edge.source == node_id or edge.target == node_id
            )
            edge.is_hidden = not edge.is_highlighted

        return graph

    def reset_focus(self, graph: InvestigationGraph) -> InvestigationGraph:
        graph.focus_node_id = None
        graph.selected_node_id = None

        for node in graph.nodes:
            node.is_focus = False
            node.is_selected = False
            node.is_hidden = False

        for edge in graph.edges:
            edge.is_highlighted = False
            edge.is_hidden = False

        return graph

    def filter_by_node_type(
        self,
        graph: InvestigationGraph,
        node_type: str | None,
    ) -> InvestigationGraph:
        graph.active_node_type = node_type

        for node in graph.nodes:
            if node_type is None:
                node.is_hidden = False
            else:
                node.is_hidden = node.node_type != node_type

        return graph

    def highlight_relationship(
        self,
        graph: InvestigationGraph,
        relationship: str | None,
    ) -> InvestigationGraph:
        graph.active_relationship = relationship

        for edge in graph.edges:
            if relationship is None:
                edge.is_highlighted = False
            else:
                edge.is_highlighted = edge.relationship == relationship

        return graph

    def _build_nodes(self, evidence_items: list[Any]) -> list[InvestigationNode]:
        nodes: list[InvestigationNode] = []

        for index, item in enumerate(evidence_items):
            evidence_id = self._safe_get(item, "evidence_id", None)
            fallback_id = self._safe_get(item, "id", f"evidence_{index + 1}")

            node_id = str(evidence_id or fallback_id)

            content = self._safe_get(
                item,
                "content",
                f"Evidence {index + 1}",
            )
            ai_summary = self._safe_get(item, "ai_summary", "")
            node_label = self._build_node_label(
                content=content,
                evidence_id=evidence_id or node_id,
            )
            node_description = self._build_node_description(
                content=content,
                ai_summary=ai_summary,
            )

            platform = self._format_value(
                self._safe_get(item, "platform", "Unknown")
            )
            topic = self._format_value(
                self._safe_get(item, "topic", "Unknown")
            )
            sentiment = self._format_value(
                self._safe_get(item, "sentiment", "Unknown")
            )
            engagement = self._safe_number(
                self._safe_get(item, "engagement", 0)
            )

            original_url = self._safe_get(item, "original_url", "")
            published_time = self._safe_get(item, "published_time", "")

            score = self._calculate_score(
                engagement=engagement,
                sentiment=sentiment,
            )

            nodes.append(
                InvestigationNode(
                    node_id=node_id,
                    label=node_label,
                    node_type="evidence",
                    description=node_description,
                    score=score,
                    platform=platform,
                    topic=topic,
                    sentiment=sentiment,
                    evidence_id=str(evidence_id or node_id),
                    metadata={
                        "engagement": engagement,
                        "raw_index": index,
                        "ai_summary": ai_summary,
                        "original_url": original_url,
                        "published_time": published_time,
                    },
                )
            )

        return nodes

    def _build_edges(
        self,
        nodes: list[InvestigationNode],
    ) -> list[InvestigationEdge]:
        edges: list[InvestigationEdge] = []

        edges.extend(self._build_same_topic_edges(nodes))
        edges.extend(self._build_same_platform_edges(nodes))
        edges.extend(self._build_same_sentiment_edges(nodes))
        edges.extend(self._build_high_engagement_edges(nodes))

        return edges

    def _build_same_topic_edges(
        self,
        nodes: list[InvestigationNode],
    ) -> list[InvestigationEdge]:
        edges: list[InvestigationEdge] = []

        for i, source in enumerate(nodes):
            for target in nodes[i + 1:]:
                if source.topic == "Unknown":
                    continue

                if source.topic == target.topic:
                    edges.append(
                        InvestigationEdge(
                            edge_id=f"same_topic_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_topic",
                            weight=1.3,
                            description=f"同屬議題：{source.topic}",
                            metadata={
                                "topic": source.topic,
                            },
                        )
                    )

        return edges

    def _build_same_platform_edges(
        self,
        nodes: list[InvestigationNode],
    ) -> list[InvestigationEdge]:
        edges: list[InvestigationEdge] = []

        for i, source in enumerate(nodes):
            for target in nodes[i + 1:]:
                if source.platform == "Unknown":
                    continue

                if source.platform == target.platform:
                    edges.append(
                        InvestigationEdge(
                            edge_id=f"same_platform_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_platform",
                            weight=0.8,
                            description=f"同一來源平台：{source.platform}",
                            metadata={
                                "platform": source.platform,
                            },
                        )
                    )

        return edges

    def _build_same_sentiment_edges(
        self,
        nodes: list[InvestigationNode],
    ) -> list[InvestigationEdge]:
        edges: list[InvestigationEdge] = []

        for i, source in enumerate(nodes):
            for target in nodes[i + 1:]:
                if source.sentiment == "Unknown":
                    continue

                if source.sentiment == target.sentiment:
                    edges.append(
                        InvestigationEdge(
                            edge_id=f"same_sentiment_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_sentiment",
                            weight=0.6,
                            description=f"同一情緒傾向：{source.sentiment}",
                            metadata={
                                "sentiment": source.sentiment,
                            },
                        )
                    )

        return edges

    def _build_high_engagement_edges(
        self,
        nodes: list[InvestigationNode],
    ) -> list[InvestigationEdge]:
        edges: list[InvestigationEdge] = []

        high_engagement_nodes = [
            node
            for node in nodes
            if node.metadata.get("engagement", 0) >= 500
        ]

        for i, source in enumerate(high_engagement_nodes):
            for target in high_engagement_nodes[i + 1:]:
                edges.append(
                    InvestigationEdge(
                        edge_id=f"high_engagement_{source.node_id}_{target.node_id}",
                        source=source.node_id,
                        target=target.node_id,
                        relationship="high_engagement_cluster",
                        weight=1.5,
                        description="同屬高互動聲量群集。",
                        metadata={
                            "source_engagement": source.metadata.get(
                                "engagement", 0
                            ),
                            "target_engagement": target.metadata.get(
                                "engagement", 0
                            ),
                        },
                    )
                )

        return edges

    def _build_node_label(self, content: Any, evidence_id: Any) -> str:
        content_text = str(content or "").strip()

        if not content_text:
            return str(evidence_id or "Evidence")

        if len(content_text) <= 48:
            return content_text

        return f"{content_text[:48]}..."

    def _build_node_description(
        self,
        content: Any,
        ai_summary: Any,
    ) -> str:
        summary_text = str(ai_summary or "").strip()
        content_text = str(content or "").strip()

        description = summary_text or content_text

        return description[:180]

    def _calculate_score(self, engagement: int, sentiment: str) -> float:
        score = float(engagement)

        sentiment_text = sentiment.lower()

        if sentiment_text in ["negative", "負面", "負向"]:
            score *= 1.4

        if sentiment_text in ["positive", "正面", "正向"]:
            score *= 1.05

        return score

    def _safe_get(self, item: Any, key: str, default: Any = None) -> Any:
        if isinstance(item, dict):
            return item.get(key, default)

        return getattr(item, key, default)

    def _safe_number(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def _format_value(self, value: Any) -> str:
        if value is None:
            return "Unknown"

        if hasattr(value, "value"):
            return str(value.value)

        return str(value)