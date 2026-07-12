from modules.evidence_center.engine.models import EngineFlow


class EvidenceFlowEngine:
    """
    Evidence Flow Engine

    Engine Runtime 的 Flow 管理核心。

    職責：
    - 持有唯一 Flow Queue
    - 對外提供穩定 Flow API
    - UI 不直接操作 flows 內部結構
    - 不建立第二套 Flow Engine
    """

    def __init__(self, flows=None):
        self.flows = flows or []

    # =========================
    # Flow API
    # =========================

    def get_flows(self):
        if isinstance(self.flows, dict):
            return list(self.flows.values())

        return self.flows or []

    def set_flows(self, flows):
        self.flows = flows or []
        return self.get_flows()

    def clear_flows(self):
        self.flows = []
        return self.flows

    def get_flow_ids(self):
        return [self._flow_id(flow) for flow in self.get_flows()]

    def get_flow_by_id(self, flow_id):
        for flow in self.get_flows():
            if self._flow_id(flow) == flow_id:
                return flow

        return None

    def add_flow(self, flow):
        if flow is None:
            return None

        flow_id = self._flow_id(flow)

        if not flow_id:
            return None

        if isinstance(self.flows, dict):
            self.flows[flow_id] = flow
            return flow

        existing_flow = self.get_flow_by_id(flow_id)

        if existing_flow is not None:
            self.update_flow(flow_id, flow)
            return flow

        self.flows.append(flow)
        return flow

    def create_flow(
        self,
        flow_id,
        title,
        description="",
        flow_type="Flow",
        status="Ready",
        steps=None,
        source=None,
        evidence_id=None,
        metadata=None,
    ):
        flow = EngineFlow(
            flow_id=flow_id,
            title=title,
            description=description,
            flow_type=flow_type,
            status=status,
            steps=steps or [],
            source=source or evidence_id or "Evidence Engine",
            evidence_id=evidence_id,
            metadata=metadata or {},
        )

        return self.add_flow(flow)

    def update_flow(self, flow_id, updates):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return None

        if isinstance(updates, dict):
            for key, value in updates.items():
                self._set_value(flow, key, value)
        else:
            replacement_id = self._flow_id(updates)

            if replacement_id == flow_id:
                self.remove_flow(flow_id)
                self.add_flow(updates)
                return updates

        return flow

    def remove_flow(self, flow_id):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return None

        if isinstance(self.flows, dict):
            self.flows.pop(flow_id, None)
        else:
            self.flows = [
                current_flow
                for current_flow in self.get_flows()
                if self._flow_id(current_flow) != flow_id
            ]

        return flow

    # =========================
    # Status API
    # =========================

    def set_status(self, flow_id, status):
        return self.update_flow(flow_id, {"status": status})

    def mark_ready(self, flow_id):
        return self.set_status(flow_id, "Ready")

    def mark_running(self, flow_id):
        return self.set_status(flow_id, "Running")

    def mark_completed(self, flow_id):
        return self.set_status(flow_id, "Completed")

    def mark_failed(self, flow_id):
        return self.set_status(flow_id, "Failed")

    # =========================
    # Step API
    # =========================

    def get_steps(self, flow_id):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return []

        steps = self._flow_steps(flow)

        if isinstance(steps, dict):
            return list(steps.values())

        return steps or []

    def add_step(self, flow_id, step):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return None

        steps = self.get_steps(flow_id)
        steps.append(step)

        self._set_value(flow, "steps", steps)

        return step

    def update_step(self, flow_id, step_index, updates):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return None

        steps = self.get_steps(flow_id)

        if step_index < 0 or step_index >= len(steps):
            return None

        step = steps[step_index]

        if isinstance(updates, dict):
            for key, value in updates.items():
                self._set_value(step, key, value)
        else:
            steps[step_index] = updates
            step = updates

        self._set_value(flow, "steps", steps)

        return step

    def remove_step(self, flow_id, step_index):
        flow = self.get_flow_by_id(flow_id)

        if flow is None:
            return None

        steps = self.get_steps(flow_id)

        if step_index < 0 or step_index >= len(steps):
            return None

        removed_step = steps.pop(step_index)

        self._set_value(flow, "steps", steps)

        return removed_step

    # =========================
    # Query API
    # =========================

    def get_ready_flows(self):
        return [
            flow
            for flow in self.get_flows()
            if str(self._flow_status(flow)).lower()
            in ["ready", "pending", "todo", "open"]
        ]

    def get_running_flows(self):
        return [
            flow
            for flow in self.get_flows()
            if str(self._flow_status(flow)).lower()
            in ["running", "active", "in_progress"]
        ]

    def get_completed_flows(self):
        return [
            flow
            for flow in self.get_flows()
            if str(self._flow_status(flow)).lower()
            in ["completed", "complete", "done", "resolved"]
        ]

    def get_flows_by_type(self, flow_type):
        return [
            flow
            for flow in self.get_flows()
            if str(self._flow_type(flow)).lower() == str(flow_type).lower()
        ]

    def get_flows_by_evidence_id(self, evidence_id):
        return [
            flow
            for flow in self.get_flows()
            if self._flow_evidence_id(flow) == evidence_id
        ]

    def get_flow_count(self):
        return len(self.get_flows())

    def get_summary(self):
        flows = self.get_flows()

        return {
            "flow_count": len(flows),
            "ready_count": len(self.get_ready_flows()),
            "running_count": len(self.get_running_flows()),
            "completed_count": len(self.get_completed_flows()),
            "flow_ids": self.get_flow_ids(),
        }

    # =========================
    # Internal Helpers
    # =========================

    def _flow_id(self, flow):
        if isinstance(flow, dict):
            return (
                flow.get("flow_id")
                or flow.get("id")
                or flow.get("key")
            )

        return (
            getattr(flow, "flow_id", None)
            or getattr(flow, "id", None)
            or getattr(flow, "key", None)
        )

    def _flow_status(self, flow):
        if isinstance(flow, dict):
            return flow.get("status") or flow.get("state") or "Ready"

        return (
            getattr(flow, "status", None)
            or getattr(flow, "state", None)
            or "Ready"
        )

    def _flow_type(self, flow):
        if isinstance(flow, dict):
            return (
                flow.get("flow_type")
                or flow.get("type")
                or flow.get("category")
                or "Flow"
            )

        return (
            getattr(flow, "flow_type", None)
            or getattr(flow, "type", None)
            or getattr(flow, "category", None)
            or "Flow"
        )

    def _flow_steps(self, flow):
        if isinstance(flow, dict):
            return (
                flow.get("steps")
                or flow.get("nodes")
                or flow.get("tasks")
                or []
            )

        return (
            getattr(flow, "steps", None)
            or getattr(flow, "nodes", None)
            or getattr(flow, "tasks", None)
            or []
        )

    def _flow_evidence_id(self, flow):
        if isinstance(flow, dict):
            return flow.get("evidence_id") or flow.get("source_id")

        return (
            getattr(flow, "evidence_id", None)
            or getattr(flow, "source_id", None)
        )

    def _set_value(self, obj, key, value):
        if isinstance(obj, dict):
            obj[key] = value
            return

        setattr(obj, key, value)