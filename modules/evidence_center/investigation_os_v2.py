from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ============================================================
# Investigation OS v2
# Golden Master Kernel
# ============================================================


@dataclass
class GraphNode:
    node_id: str
    label: str
    node_type: str = "evidence"
    description: str = ""
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    is_focus: bool = False
    is_selected: bool = False
    is_filtered: bool = False


@dataclass
class GraphEdge:
    edge_id: str
    source: str
    target: str
    relationship: str = "related"
    weight: float = 1.0
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    is_highlighted: bool = False


@dataclass
class GraphCanvasState:
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)

    focus_node_id: str | None = None
    selected_node_id: str | None = None
    active_relationship: str | None = None
    active_node_type: str | None = None

    def get_node(self, node_id: str) -> GraphNode | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node

        return None

    def get_connected_node_ids(self, node_id: str) -> set[str]:
        connected_node_ids = set()

        for edge in self.edges:
            if edge.source == node_id:
                connected_node_ids.add(edge.target)

            if edge.target == node_id:
                connected_node_ids.add(edge.source)

        return connected_node_ids

    def focus_node(self, node_id: str):
        self.focus_node_id = node_id
        self.selected_node_id = node_id

        connected_node_ids = self.get_connected_node_ids(node_id)
        visible_node_ids = connected_node_ids | {node_id}

        for node in self.nodes:
            node.is_focus = node.node_id == node_id
            node.is_selected = node.node_id == node_id
            node.is_filtered = node.node_id not in visible_node_ids

        for edge in self.edges:
            edge.is_highlighted = (
                edge.source == node_id
                or edge.target == node_id
            )

    def filter_by_node_type(self, node_type: str | None):
        self.active_node_type = node_type

        for node in self.nodes:
            if node_type is None:
                node.is_filtered = False
            else:
                node.is_filtered = node.node_type != node_type

    def highlight_relationship(self, relationship: str | None):
        self.active_relationship = relationship

        for edge in self.edges:
            if relationship is None:
                edge.is_highlighted = False
            else:
                edge.is_highlighted = edge.relationship == relationship

    def visible_nodes(self) -> list[GraphNode]:
        return [
            node
            for node in self.nodes
            if not node.is_filtered
        ]

    def visible_edges(self) -> list[GraphEdge]:
        visible_node_ids = {
            node.node_id
            for node in self.visible_nodes()
        }

        return [
            edge
            for edge in self.edges
            if edge.source in visible_node_ids
            and edge.target in visible_node_ids
        ]


@dataclass
class InvestigationAction:
    action_id: str
    title: str
    description: str
    action_type: str = "inspect"
    priority: str = "Medium"
    target_node_id: str | None = None
    target_evidence_id: str | None = None
    status: str = "Ready"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    action_id: str
    status: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    executed_at: str = field(default_factory=lambda: datetime.now().isoformat())


class InvestigationActionSystem:
    """
    Investigation Action System

    根據目前調查畫布狀態，建立可供使用者執行的下一步行動。

    GM-07 Final Product Audit：
    - 保留既有 action_type 與 status，避免影響 Runtime 行為
    - 只調整主管可閱讀文字
    - 不新增任何功能或 Architecture
    """

    def build_actions(
        self,
        graph_state: GraphCanvasState,
    ) -> list[InvestigationAction]:
        actions: list[InvestigationAction] = []

        focus_node_id = graph_state.focus_node_id

        if focus_node_id:
            focus_node = graph_state.get_node(focus_node_id)

            if focus_node:
                actions.append(
                    InvestigationAction(
                        action_id="inspect_focus_node",
                        title="檢視焦點證據",
                        description=f"深入檢視目前焦點證據：{focus_node.label}",
                        action_type="open_evidence",
                        priority="High",
                        target_node_id=focus_node.node_id,
                        target_evidence_id=focus_node.metadata.get("evidence_id"),
                    )
                )

                actions.append(
                    InvestigationAction(
                        action_id="filter_focus_subgraph",
                        title="聚焦關聯脈絡",
                        description="只保留與目前焦點證據直接相關的內容與關係。",
                        action_type="filter_subgraph",
                        priority="High",
                        target_node_id=focus_node.node_id,
                    )
                )

        if graph_state.edges:
            relationship_counts: dict[str, int] = {}

            for edge in graph_state.edges:
                relationship_counts[edge.relationship] = (
                    relationship_counts.get(edge.relationship, 0) + 1
                )

            strongest_relationship = max(
                relationship_counts,
                key=relationship_counts.get,
            )

            actions.append(
                InvestigationAction(
                    action_id="highlight_strongest_relationship",
                    title="標示主要關聯",
                    description=f"目前最常出現的關聯類型是：{strongest_relationship}",
                    action_type="highlight_relationship",
                    priority="Medium",
                    payload={"relationship": strongest_relationship},
                )
            )

        actions.append(
            InvestigationAction(
                action_id="generate_investigation_flow",
                title="建立調查路徑",
                description="根據目前調查畫布狀態，整理下一輪建議檢查順序。",
                action_type="generate_flow",
                priority="Medium",
            )
        )

        return actions

    def execute(
        self,
        action: InvestigationAction,
        graph_state: GraphCanvasState,
    ) -> ActionResult:
        if action.action_type == "focus_node" and action.target_node_id:
            graph_state.focus_node(action.target_node_id)

            return ActionResult(
                action_id=action.action_id,
                status="Success",
                message="已切換焦點證據。",
                data={"focus_node_id": action.target_node_id},
            )

        if action.action_type == "filter_subgraph" and action.target_node_id:
            graph_state.focus_node(action.target_node_id)

            return ActionResult(
                action_id=action.action_id,
                status="Success",
                message="已聚焦焦點證據的關聯脈絡。",
                data={"focus_node_id": action.target_node_id},
            )

        if action.action_type == "highlight_relationship":
            relationship = action.payload.get("relationship")
            graph_state.highlight_relationship(relationship)

            return ActionResult(
                action_id=action.action_id,
                status="Success",
                message=f"已標示關聯類型：{relationship}",
                data={"relationship": relationship},
            )

        if action.action_type == "generate_flow":
            return ActionResult(
                action_id=action.action_id,
                status="Success",
                message="已準備建立調查路徑。",
            )

        if action.action_type == "open_evidence":
            return ActionResult(
                action_id=action.action_id,
                status="Pending",
                message="此動作將由介面開啟證據詳情。",
                data={
                    "target_node_id": action.target_node_id,
                    "target_evidence_id": action.target_evidence_id,
                },
            )

        if action.action_type == "compare_evidence":
            return ActionResult(
                action_id=action.action_id,
                status="Pending",
                message="此動作將由介面開啟證據比對。",
                data={
                    "target_node_id": action.target_node_id,
                    "target_evidence_id": action.target_evidence_id,
                },
            )

        return ActionResult(
            action_id=action.action_id,
            status="Failed",
            message=f"尚未支援的行動類型：{action.action_type}",
        )


@dataclass
class InvestigationFlowStep:
    step_id: str
    title: str
    description: str
    node_id: str | None = None
    action_type: str = "inspect"
    priority: str = "Medium"
    status: str = "Todo"


@dataclass
class InvestigationFlow:
    flow_id: str
    title: str
    description: str
    steps: list[InvestigationFlowStep] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class InvestigationFlowEngine:
    """
    Investigation Flow Engine

    根據目前調查畫布狀態，整理建議檢查順序。

    GM-07 Final Product Audit：
    - 保留既有流程產生邏輯
    - 只調整主管可閱讀文字
    - 不改變 Runtime Behavior
    """

    def generate(self, graph_state: GraphCanvasState) -> InvestigationFlow:
        steps: list[InvestigationFlowStep] = []

        anomaly_nodes = [
            node
            for node in graph_state.nodes
            if node.node_type in ["anomaly", "risk"]
        ]

        high_score_nodes = sorted(
            graph_state.nodes,
            key=lambda node: node.score,
            reverse=True,
        )

        cluster_nodes = [
            node
            for node in graph_state.nodes
            if node.node_type in ["cluster", "storyline"]
        ]

        for index, node in enumerate(anomaly_nodes[:3], start=1):
            steps.append(
                InvestigationFlowStep(
                    step_id=f"anomaly_{index}",
                    title=f"優先確認異常訊號：{node.label}",
                    description=(
                        node.description
                        or "此內容可能代表異常、風險或突發討論。"
                    ),
                    node_id=node.node_id,
                    action_type="focus_node",
                    priority="High",
                )
            )

        existing_node_ids = {
            step.node_id
            for step in steps
        }

        for index, node in enumerate(high_score_nodes[:5], start=1):
            if node.node_id in existing_node_ids:
                continue

            steps.append(
                InvestigationFlowStep(
                    step_id=f"high_score_{index}",
                    title=f"檢查高影響證據：{node.label}",
                    description=(
                        node.description
                        or "此證據具有較高影響分數，建議進一步檢查。"
                    ),
                    node_id=node.node_id,
                    action_type="open_evidence",
                    priority="Medium",
                )
            )

            existing_node_ids.add(node.node_id)

        for index, node in enumerate(cluster_nodes[:3], start=1):
            if node.node_id in existing_node_ids:
                continue

            steps.append(
                InvestigationFlowStep(
                    step_id=f"cluster_{index}",
                    title=f"梳理討論脈絡：{node.label}",
                    description=(
                        node.description
                        or "此內容可能代表一組相關討論或故事線，建議整體檢視。"
                    ),
                    node_id=node.node_id,
                    action_type="filter_subgraph",
                    priority="Medium",
                )
            )

            existing_node_ids.add(node.node_id)

        if not steps:
            steps.append(
                InvestigationFlowStep(
                    step_id="empty_graph_review",
                    title="建立第一輪調查視角",
                    description="目前尚無明確異常或高影響證據，建議先選擇一筆焦點證據進行檢視。",
                    action_type="open_evidence",
                    priority="Low",
                )
            )

        return InvestigationFlow(
            flow_id="investigation_flow_auto",
            title="建議調查路徑",
            description="根據目前調查畫布狀態整理出的建議檢查順序。",
            steps=steps,
        )


class InvestigationGraphBuilder:
    """
    Investigation Graph Builder

    將 Evidence 資料轉換為調查畫布可使用的節點與關聯。

    GM-06 Final Schema Consistency Audit：
    - Evidence 讀取來源對齊 content / ai_summary / original_url
    - Graph Domain 保留 label / title / description 語意

    GM-07 Final Product Audit：
    - 保留既有資料結構與關聯建立邏輯
    - 統一 fallback 文字
    - 不新增任何 Runtime 行為
    """

    def build_from_evidence(
        self,
        evidence_items: list[Any],
    ) -> GraphCanvasState:
        nodes: list[GraphNode] = []
        edges: list[GraphEdge] = []

        for index, item in enumerate(evidence_items):
            evidence_id = self._safe_get(item, "evidence_id", None)
            fallback_id = self._safe_get(item, "id", f"evidence_{index + 1}")
            node_id = str(evidence_id or fallback_id)

            content = self._safe_get(item, "content", "")
            ai_summary = self._safe_get(item, "ai_summary", "")

            node_label = self._build_node_label(
                content=content,
                evidence_id=evidence_id or node_id,
            )
            node_description = self._build_node_description(
                content=content,
                ai_summary=ai_summary,
            )

            platform = self._safe_get(item, "platform", "未標示")
            topic = self._safe_get(item, "topic", "未標示")
            sentiment = self._safe_get(item, "sentiment", "未標示")
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
                GraphNode(
                    node_id=node_id,
                    label=node_label,
                    node_type="evidence",
                    description=node_description,
                    score=score,
                    metadata={
                        "evidence_id": evidence_id,
                        "platform": self._format_value(platform),
                        "topic": self._format_value(topic),
                        "sentiment": self._format_value(sentiment),
                        "engagement": engagement,
                        "ai_summary": ai_summary,
                        "original_url": original_url,
                        "published_time": published_time,
                    },
                )
            )

        edges.extend(self._build_topic_edges(nodes))
        edges.extend(self._build_platform_edges(nodes))
        edges.extend(self._build_sentiment_edges(nodes))

        return GraphCanvasState(
            nodes=nodes,
            edges=edges,
        )

    def _build_topic_edges(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        edges: list[GraphEdge] = []

        for index, source in enumerate(nodes):
            for target in nodes[index + 1:]:
                if source.metadata.get("topic") == target.metadata.get("topic"):
                    topic = source.metadata.get("topic")

                    edges.append(
                        GraphEdge(
                            edge_id=f"topic_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_topic",
                            weight=1.2,
                            description=f"同屬議題：{topic}",
                            metadata={"topic": topic},
                        )
                    )

        return edges

    def _build_platform_edges(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        edges: list[GraphEdge] = []

        for index, source in enumerate(nodes):
            for target in nodes[index + 1:]:
                if (
                    source.metadata.get("platform")
                    == target.metadata.get("platform")
                ):
                    platform = source.metadata.get("platform")

                    edges.append(
                        GraphEdge(
                            edge_id=f"platform_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_platform",
                            weight=0.8,
                            description=f"同一來源平台：{platform}",
                            metadata={"platform": platform},
                        )
                    )

        return edges

    def _build_sentiment_edges(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        edges: list[GraphEdge] = []

        for index, source in enumerate(nodes):
            for target in nodes[index + 1:]:
                if (
                    source.metadata.get("sentiment")
                    == target.metadata.get("sentiment")
                ):
                    sentiment = source.metadata.get("sentiment")

                    edges.append(
                        GraphEdge(
                            edge_id=f"sentiment_{source.node_id}_{target.node_id}",
                            source=source.node_id,
                            target=target.node_id,
                            relationship="same_sentiment",
                            weight=0.6,
                            description=f"同一情緒傾向：{sentiment}",
                            metadata={"sentiment": sentiment},
                        )
                    )

        return edges

    def _build_node_label(self, content: Any, evidence_id: Any) -> str:
        content_text = str(content or "").strip()

        if not content_text:
            return str(evidence_id or "未命名證據")

        if len(content_text) <= 48:
            return content_text

        return f"{content_text[:48]}..."

    def _build_node_description(self, content: Any, ai_summary: Any) -> str:
        summary_text = str(ai_summary or "").strip()
        content_text = str(content or "").strip()

        description = summary_text or content_text

        return description[:140]

    def _calculate_score(self, engagement: int, sentiment: Any) -> float:
        score = float(engagement)

        sentiment_text = self._format_value(sentiment).lower()

        if sentiment_text in ["negative", "負面", "負向"]:
            score *= 1.35

        if sentiment_text in ["positive", "正面", "正向"]:
            score *= 1.05

        return score

    def _safe_get(
        self,
        item: Any,
        key: str,
        default: Any = None,
    ) -> Any:
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
            return "未標示"

        if hasattr(value, "value"):
            return str(value.value)

        return str(value)


@dataclass
class InvestigationOSV2Runtime:
    graph_state: GraphCanvasState
    actions: list[InvestigationAction]
    flow: InvestigationFlow
    last_action_result: ActionResult | None = None
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class InvestigationOSV2Kernel:
    """
    Investigation OS v2 Kernel

    調查畫布、建議行動與調查路徑的協調入口。

    GM-07 Final Product Audit：
    - 不新增 Runtime / Engine / Layer / Domain
    - 保留既有公開方法
    - 僅做語言、docstring 與可讀性整理
    """

    def __init__(self):
        self.graph_builder = InvestigationGraphBuilder()
        self.action_system = InvestigationActionSystem()
        self.flow_engine = InvestigationFlowEngine()

    def boot(self, evidence_items: list[Any]) -> InvestigationOSV2Runtime:
        graph_state = self.graph_builder.build_from_evidence(evidence_items)
        actions = self.action_system.build_actions(graph_state)
        flow = self.flow_engine.generate(graph_state)

        return InvestigationOSV2Runtime(
            graph_state=graph_state,
            actions=actions,
            flow=flow,
        )

    def cycle(
        self,
        runtime: InvestigationOSV2Runtime,
    ) -> InvestigationOSV2Runtime:
        runtime.actions = self.action_system.build_actions(runtime.graph_state)
        runtime.flow = self.flow_engine.generate(runtime.graph_state)
        runtime.updated_at = datetime.now().isoformat()

        return runtime

    def execute_action(
        self,
        runtime: InvestigationOSV2Runtime,
        action_id: str,
    ) -> InvestigationOSV2Runtime:
        action = self._find_action(runtime.actions, action_id)

        if action is None:
            runtime.last_action_result = ActionResult(
                action_id=action_id,
                status="Failed",
                message="找不到指定行動。",
            )
            return runtime

        result = self.action_system.execute(
            action=action,
            graph_state=runtime.graph_state,
        )

        runtime.last_action_result = result
        runtime = self.cycle(runtime)

        return runtime

    def focus_node(
        self,
        runtime: InvestigationOSV2Runtime,
        node_id: str,
    ) -> InvestigationOSV2Runtime:
        runtime.graph_state.focus_node(node_id)
        runtime = self.cycle(runtime)

        return runtime

    def filter_by_node_type(
        self,
        runtime: InvestigationOSV2Runtime,
        node_type: str | None,
    ) -> InvestigationOSV2Runtime:
        runtime.graph_state.filter_by_node_type(node_type)
        runtime = self.cycle(runtime)

        return runtime

    def highlight_relationship(
        self,
        runtime: InvestigationOSV2Runtime,
        relationship: str | None,
    ) -> InvestigationOSV2Runtime:
        runtime.graph_state.highlight_relationship(relationship)
        runtime = self.cycle(runtime)

        return runtime

    def _find_action(
        self,
        actions: list[InvestigationAction],
        action_id: str,
    ) -> InvestigationAction | None:
        for action in actions:
            if action.action_id == action_id:
                return action

        return None


def create_investigation_os_v2() -> InvestigationOSV2Kernel:
    return InvestigationOSV2Kernel()