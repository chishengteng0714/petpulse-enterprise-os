from modules.evidence_center.investigation_os.models import (
    InvestigationAction,
    InvestigationActionResult,
    InvestigationGraph,
)


class InvestigationActionEngine:
    """
    Investigation Action Engine

    Agent v1：只提出建議。
    Action Engine v2：產生可執行操作。

    支援 action_type：
    - focus_node
    - reset_focus
    - filter_node_type
    - highlight_relationship
    - open_evidence
    - compare_evidence
    - generate_flow
    """

    def build_actions(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationAction]:
        actions: list[InvestigationAction] = []

        actions.extend(self._build_focus_actions(graph))
        actions.extend(self._build_relationship_actions(graph))
        actions.extend(self._build_global_actions(graph))

        return actions

    def execute(
        self,
        action: InvestigationAction,
        graph_engine,
        graph: InvestigationGraph,
    ) -> tuple[InvestigationGraph, InvestigationActionResult]:
        if action.action_type == "focus_node" and action.target_node_id:
            graph = graph_engine.focus_node(graph, action.target_node_id)

            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Success",
                message=f"已聚焦節點：{action.target_node_id}",
                data={
                    "target_node_id": action.target_node_id,
                },
            )

        if action.action_type == "reset_focus":
            graph = graph_engine.reset_focus(graph)

            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Success",
                message="已重置 Graph Canvas。",
            )

        if action.action_type == "filter_node_type":
            node_type = action.payload.get("node_type")
            graph = graph_engine.filter_by_node_type(graph, node_type)

            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Success",
                message=f"已篩選 Node Type：{node_type or 'All'}",
                data={
                    "node_type": node_type,
                },
            )

        if action.action_type == "highlight_relationship":
            relationship = action.payload.get("relationship")
            graph = graph_engine.highlight_relationship(graph, relationship)

            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Success",
                message=f"已高亮 Relationship：{relationship or 'None'}",
                data={
                    "relationship": relationship,
                },
            )

        if action.action_type == "open_evidence":
            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Pending",
                message="請交由 Workspace UI 開啟 Evidence Detail。",
                data={
                    "target_node_id": action.target_node_id,
                    "target_evidence_id": action.target_evidence_id,
                },
            )

        if action.action_type == "compare_evidence":
            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Pending",
                message="請交由 Workspace UI 啟動 Compare Mode。",
                data={
                    "target_node_id": action.target_node_id,
                    "target_evidence_id": action.target_evidence_id,
                },
            )

        if action.action_type == "generate_flow":
            return graph, InvestigationActionResult(
                action_id=action.action_id,
                status="Pending",
                message="請交由 Flow Engine 重新生成調查路徑。",
            )

        return graph, InvestigationActionResult(
            action_id=action.action_id,
            status="Failed",
            message=f"不支援的 action_type：{action.action_type}",
        )

    def _build_focus_actions(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationAction]:
        actions: list[InvestigationAction] = []

        focus_node = (
            graph.get_node(graph.focus_node_id)
            if graph.focus_node_id
            else None
        )

        if focus_node:
            actions.append(
                InvestigationAction(
                    action_id="open_focus_evidence",
                    title="開啟焦點證據",
                    description=f"查看目前焦點節點的原始證據：{focus_node.label}",
                    action_type="open_evidence",
                    priority="High",
                    target_node_id=focus_node.node_id,
                    target_evidence_id=focus_node.evidence_id,
                )
            )

            actions.append(
                InvestigationAction(
                    action_id="compare_focus_evidence",
                    title="加入 Compare Mode",
                    description="將目前焦點證據加入 A/B 比較，用來對照另一則證據。",
                    action_type="compare_evidence",
                    priority="Medium",
                    target_node_id=focus_node.node_id,
                    target_evidence_id=focus_node.evidence_id,
                )
            )

            actions.append(
                InvestigationAction(
                    action_id="reset_focus",
                    title="重置 Graph Focus",
                    description="返回完整 Graph Canvas。",
                    action_type="reset_focus",
                    priority="Low",
                )
            )

        else:
            top_nodes = sorted(
                graph.nodes,
                key=lambda node: node.score,
                reverse=True,
            )

            for index, node in enumerate(top_nodes[:3], start=1):
                actions.append(
                    InvestigationAction(
                        action_id=f"focus_top_node_{index}",
                        title=f"聚焦高影響節點：{node.label}",
                        description="此節點分數較高，適合作為下一輪調查入口。",
                        action_type="focus_node",
                        priority="High" if index == 1 else "Medium",
                        target_node_id=node.node_id,
                        target_evidence_id=node.evidence_id,
                    )
                )

        return actions

    def _build_relationship_actions(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationAction]:
        actions: list[InvestigationAction] = []

        relationship_counts: dict[str, int] = {}

        for edge in graph.edges:
            relationship_counts[edge.relationship] = (
                relationship_counts.get(edge.relationship, 0) + 1
            )

        sorted_relationships = sorted(
            relationship_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for relationship, count in sorted_relationships[:3]:
            actions.append(
                InvestigationAction(
                    action_id=f"highlight_{relationship}",
                    title=f"高亮關係：{relationship}",
                    description=f"此關係目前出現 {count} 次，可用來觀察證據群聚。",
                    action_type="highlight_relationship",
                    priority="Medium",
                    payload={
                        "relationship": relationship,
                    },
                )
            )

        return actions

    def _build_global_actions(
        self,
        graph: InvestigationGraph,
    ) -> list[InvestigationAction]:
        actions: list[InvestigationAction] = []

        node_types = sorted(
            {
                node.node_type
                for node in graph.nodes
                if node.node_type
            }
        )

        for node_type in node_types:
            actions.append(
                InvestigationAction(
                    action_id=f"filter_node_type_{node_type}",
                    title=f"篩選 Node Type：{node_type}",
                    description=f"只顯示 {node_type} 類型節點。",
                    action_type="filter_node_type",
                    priority="Low",
                    payload={
                        "node_type": node_type,
                    },
                )
            )

        actions.append(
            InvestigationAction(
                action_id="show_all_node_types",
                title="顯示全部 Node",
                description="清除 Node Type Filter，回到完整 Graph。",
                action_type="filter_node_type",
                priority="Low",
                payload={
                    "node_type": None,
                },
            )
        )

        actions.append(
            InvestigationAction(
                action_id="generate_flow",
                title="重新生成調查路徑",
                description="根據目前 Graph Canvas 狀態重新產生 Investigation Flow。",
                action_type="generate_flow",
                priority="Medium",
            )
        )

        return actions