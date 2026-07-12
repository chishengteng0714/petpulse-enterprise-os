from modules.evidence_center.investigation_os.models import (
    InvestigationFlow,
    InvestigationFlowStep,
    InvestigationGraph,
)


class InvestigationFlowEngine:
    """
    Investigation Flow Engine

    依據目前 Graph 狀態，自動生成調查路徑。

    調查順序：
    1. 高影響負面訊號
    2. 高互動訊號
    3. 被多條 edge 連接的樞紐節點
    4. 目前焦點節點周邊
    5. 補充缺口檢查
    """

    def generate(
        self,
        graph: InvestigationGraph,
    ) -> InvestigationFlow:
        steps: list[InvestigationFlowStep] = []

        steps.extend(self._build_negative_signal_steps(graph))
        steps.extend(self._build_high_engagement_steps(graph))
        steps.extend(self._build_hub_node_steps(graph))
        steps.extend(self._build_focus_neighbor_steps(graph))
        steps.extend(self._build_gap_check_steps(graph, steps))

        if not steps:
            steps.append(
                InvestigationFlowStep(
                    step_id="empty_graph_start",
                    title="建立第一個調查入口",
                    description="目前沒有足夠 Graph 訊號，請先從 Evidence Explorer 選擇一則證據作為起點。",
                    action_type="open_evidence",
                    priority="Low",
                    status="Todo",
                )
            )

        return InvestigationFlow(
            flow_id="auto_investigation_flow",
            title="Auto Investigation Flow",
            description="由 Investigation OS 根據目前 Graph 狀態自動生成的調查路徑。",
            steps=steps,
        )

    def _build_negative_signal_steps(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationFlowStep]:
        steps: list[InvestigationFlowStep] = []

        negative_nodes = [
            node
            for node in graph.nodes
            if node.sentiment.lower() in ["negative", "負面"]
        ]

        negative_nodes = sorted(
            negative_nodes,
            key=lambda node: node.score,
            reverse=True,
        )

        for index, node in enumerate(negative_nodes[:3], start=1):
            steps.append(
                InvestigationFlowStep(
                    step_id=f"negative_signal_{index}",
                    title=f"優先檢查負面訊號：{node.label}",
                    description=(
                        node.description
                        or "此節點帶有負面情緒，且可能影響品牌風險判斷。"
                    ),
                    action_type="focus_node",
                    priority="High",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "negative_signal",
                        "score": node.score,
                        "sentiment": node.sentiment,
                    },
                )
            )

        return steps

    def _build_high_engagement_steps(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationFlowStep]:
        steps: list[InvestigationFlowStep] = []

        high_engagement_nodes = [
            node
            for node in graph.nodes
            if node.metadata.get("engagement", 0) >= 500
        ]

        high_engagement_nodes = sorted(
            high_engagement_nodes,
            key=lambda node: node.metadata.get("engagement", 0),
            reverse=True,
        )

        for index, node in enumerate(high_engagement_nodes[:3], start=1):
            steps.append(
                InvestigationFlowStep(
                    step_id=f"high_engagement_{index}",
                    title=f"檢查高互動證據：{node.label}",
                    description=(
                        node.description
                        or "此節點具有較高互動量，可能代表值得追蹤的公開討論。"
                    ),
                    action_type="open_evidence",
                    priority="Medium",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "high_engagement",
                        "engagement": node.metadata.get("engagement", 0),
                    },
                )
            )

        return steps

    def _build_hub_node_steps(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationFlowStep]:
        steps: list[InvestigationFlowStep] = []

        degree_map: dict[str, int] = {}

        for edge in graph.edges:
            degree_map[edge.source] = degree_map.get(edge.source, 0) + 1
            degree_map[edge.target] = degree_map.get(edge.target, 0) + 1

        hub_nodes = sorted(
            graph.nodes,
            key=lambda node: degree_map.get(node.node_id, 0),
            reverse=True,
        )

        for index, node in enumerate(hub_nodes[:3], start=1):
            degree = degree_map.get(node.node_id, 0)

            if degree <= 0:
                continue

            steps.append(
                InvestigationFlowStep(
                    step_id=f"hub_node_{index}",
                    title=f"梳理樞紐節點：{node.label}",
                    description=(
                        f"此節點連接 {degree} 條關係，可能是議題群聚的中心。"
                    ),
                    action_type="focus_node",
                    priority="Medium",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "hub_node",
                        "degree": degree,
                    },
                )
            )

        return steps

    def _build_focus_neighbor_steps(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationFlowStep]:
        steps: list[InvestigationFlowStep] = []

        if not graph.focus_node_id:
            return steps

        connected_ids = graph.connected_node_ids(graph.focus_node_id)

        connected_nodes = [
            node
            for node in graph.nodes
            if node.node_id in connected_ids
        ]

        connected_nodes = sorted(
            connected_nodes,
            key=lambda node: node.score,
            reverse=True,
        )

        for index, node in enumerate(connected_nodes[:3], start=1):
            steps.append(
                InvestigationFlowStep(
                    step_id=f"focus_neighbor_{index}",
                    title=f"延伸檢查關聯節點：{node.label}",
                    description=(
                        node.description
                        or "此節點與目前焦點節點直接相連，適合做下一層追查。"
                    ),
                    action_type="focus_node",
                    priority="Medium",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "focus_neighbor",
                        "focus_node_id": graph.focus_node_id,
                    },
                )
            )

        return steps

    def _build_gap_check_steps(
        self,
        graph: InvestigationGraph,
        existing_steps: list[InvestigationFlowStep],
    ) -> list[InvestigationFlowStep]:
        steps: list[InvestigationFlowStep] = []

        used_node_ids = {
            step.node_id
            for step in existing_steps
            if step.node_id
        }

        unvisited_nodes = [
            node
            for node in graph.nodes
            if node.node_id not in used_node_ids
        ]

        if not unvisited_nodes:
            return steps

        unknown_topic_nodes = [
            node
            for node in unvisited_nodes
            if node.topic == "Unknown"
        ]

        if unknown_topic_nodes:
            node = unknown_topic_nodes[0]

            steps.append(
                InvestigationFlowStep(
                    step_id="gap_unknown_topic",
                    title=f"補齊未知議題：{node.label}",
                    description="此證據尚未被歸入明確 topic，建議人工檢查是否需要補標籤。",
                    action_type="open_evidence",
                    priority="Low",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "gap_unknown_topic",
                    },
                )
            )

        disconnected_nodes = self._find_disconnected_nodes(graph)

        if disconnected_nodes:
            node = disconnected_nodes[0]

            steps.append(
                InvestigationFlowStep(
                    step_id="gap_disconnected_node",
                    title=f"檢查孤立證據：{node.label}",
                    description="此證據目前沒有任何 Graph 關聯，可能需要補充關係或重新分類。",
                    action_type="open_evidence",
                    priority="Low",
                    status="Todo",
                    node_id=node.node_id,
                    evidence_id=node.evidence_id,
                    metadata={
                        "reason": "gap_disconnected_node",
                    },
                )
            )

        return steps

    def _find_disconnected_nodes(
        self,
        graph: InvestigationGraph,
    ):
        connected_ids = set()

        for edge in graph.edges:
            connected_ids.add(edge.source)
            connected_ids.add(edge.target)

        return [
            node
            for node in graph.nodes
            if node.node_id not in connected_ids
        ]