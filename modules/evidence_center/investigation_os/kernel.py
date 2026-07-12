from datetime import datetime
from typing import Any

from modules.evidence_center.investigation_os.action_engine import (
    InvestigationActionEngine,
)
from modules.evidence_center.investigation_os.flow_engine import (
    InvestigationFlowEngine,
)
from modules.evidence_center.investigation_os.graph_engine import (
    InvestigationGraphEngine,
)
from modules.evidence_center.investigation_os.models import (
    InvestigationAction,
    InvestigationActionResult,
    InvestigationRuntime,
)


class InvestigationOSKernel:
    """
    Investigation OS Kernel

    負責統一調度：
    - Graph Engine
    - Action Engine
    - Flow Engine
    - Runtime Cycle
    """

    def __init__(self):
        self.graph_engine = InvestigationGraphEngine()
        self.action_engine = InvestigationActionEngine()
        self.flow_engine = InvestigationFlowEngine()

    def boot(self, evidence_items: list[Any]) -> InvestigationRuntime:
        graph = self.graph_engine.build(evidence_items)
        actions = self.action_engine.build_actions(graph)
        flow = self.flow_engine.generate(graph)

        return InvestigationRuntime(
            graph=graph,
            actions=actions,
            flow=flow,
            cycle_count=1,
            status="Running",
            updated_at=datetime.now().isoformat(),
        )

    def cycle(self, runtime: InvestigationRuntime) -> InvestigationRuntime:
        runtime.actions = self.action_engine.build_actions(runtime.graph)
        runtime.flow = self.flow_engine.generate(runtime.graph)
        runtime.cycle_count += 1
        runtime.status = "Running"
        runtime.updated_at = datetime.now().isoformat()

        return runtime

    def execute_action(
        self,
        runtime: InvestigationRuntime,
        action_id: str,
    ) -> InvestigationRuntime:
        action = self._find_action(runtime.actions, action_id)

        if action is None:
            runtime.last_action_result = InvestigationActionResult(
                action_id=action_id,
                status="Failed",
                message="找不到指定 Action。",
            )
            return runtime

        graph, result = self.action_engine.execute(
            action=action,
            graph_engine=self.graph_engine,
            graph=runtime.graph,
        )

        runtime.graph = graph
        runtime.last_action_result = result
        runtime = self.cycle(runtime)

        return runtime

    def focus_node(
        self,
        runtime: InvestigationRuntime,
        node_id: str,
    ) -> InvestigationRuntime:
        runtime.graph = self.graph_engine.focus_node(
            runtime.graph,
            node_id,
        )
        runtime.last_action_result = InvestigationActionResult(
            action_id="manual_focus_node",
            status="Success",
            message=f"已手動聚焦節點：{node_id}",
            data={
                "node_id": node_id,
            },
        )

        return self.cycle(runtime)

    def reset_focus(
        self,
        runtime: InvestigationRuntime,
    ) -> InvestigationRuntime:
        runtime.graph = self.graph_engine.reset_focus(runtime.graph)
        runtime.last_action_result = InvestigationActionResult(
            action_id="manual_reset_focus",
            status="Success",
            message="已重置 Graph Focus。",
        )

        return self.cycle(runtime)

    def filter_by_node_type(
        self,
        runtime: InvestigationRuntime,
        node_type: str | None,
    ) -> InvestigationRuntime:
        runtime.graph = self.graph_engine.filter_by_node_type(
            runtime.graph,
            node_type,
        )
        runtime.last_action_result = InvestigationActionResult(
            action_id="manual_filter_node_type",
            status="Success",
            message=f"已篩選 Node Type：{node_type or 'All'}",
            data={
                "node_type": node_type,
            },
        )

        return self.cycle(runtime)

    def highlight_relationship(
        self,
        runtime: InvestigationRuntime,
        relationship: str | None,
    ) -> InvestigationRuntime:
        runtime.graph = self.graph_engine.highlight_relationship(
            runtime.graph,
            relationship,
        )
        runtime.last_action_result = InvestigationActionResult(
            action_id="manual_highlight_relationship",
            status="Success",
            message=f"已高亮 Relationship：{relationship or 'None'}",
            data={
                "relationship": relationship,
            },
        )

        return self.cycle(runtime)

    def generate_flow(
        self,
        runtime: InvestigationRuntime,
    ) -> InvestigationRuntime:
        runtime.flow = self.flow_engine.generate(runtime.graph)
        runtime.last_action_result = InvestigationActionResult(
            action_id="manual_generate_flow",
            status="Success",
            message="已重新生成 Investigation Flow。",
        )
        runtime.updated_at = datetime.now().isoformat()

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


def create_investigation_os_kernel() -> InvestigationOSKernel:
    return InvestigationOSKernel()