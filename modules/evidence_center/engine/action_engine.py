from modules.evidence_center.engine.models import EngineAction


class EvidenceActionEngine:
    """
    Evidence Action Engine

    Engine Runtime 的 Action 管理核心。

    職責：
    - 持有唯一 Action Queue
    - 對外提供穩定 Action API
    - UI 不直接操作 actions 內部結構
    - 不建立第二套 Action Engine
    """

    def __init__(self, actions=None):
        self.actions = actions or []

    # =========================
    # Action API
    # =========================

    def get_actions(self):
        if isinstance(self.actions, dict):
            return list(self.actions.values())

        return self.actions or []

    def set_actions(self, actions):
        self.actions = actions or []
        return self.get_actions()

    def clear_actions(self):
        self.actions = []
        return self.actions

    def get_action_ids(self):
        return [self._action_id(action) for action in self.get_actions()]

    def get_action_by_id(self, action_id):
        for action in self.get_actions():
            if self._action_id(action) == action_id:
                return action

        return None

    def add_action(self, action):
        if action is None:
            return None

        action_id = self._action_id(action)

        if not action_id:
            return None

        if isinstance(self.actions, dict):
            self.actions[action_id] = action
            return action

        existing_action = self.get_action_by_id(action_id)

        if existing_action is not None:
            self.update_action(action_id, action)
            return action

        self.actions.append(action)
        return action

    def create_action(
        self,
        action_id,
        title,
        description="",
        action_type="Action",
        priority="Normal",
        status="Pending",
        source=None,
        evidence_id=None,
        metadata=None,
    ):
        action = EngineAction(
            action_id=action_id,
            title=title,
            description=description,
            action_type=action_type,
            priority=priority,
            status=status,
            source=source or evidence_id or "Evidence Engine",
            evidence_id=evidence_id,
            metadata=metadata or {},
        )

        return self.add_action(action)

    def update_action(self, action_id, updates):
        action = self.get_action_by_id(action_id)

        if action is None:
            return None

        if isinstance(updates, dict):
            for key, value in updates.items():
                self._set_value(action, key, value)
        else:
            replacement_id = self._action_id(updates)

            if replacement_id == action_id:
                self.remove_action(action_id)
                self.add_action(updates)
                return updates

        return action

    def remove_action(self, action_id):
        action = self.get_action_by_id(action_id)

        if action is None:
            return None

        if isinstance(self.actions, dict):
            self.actions.pop(action_id, None)
        else:
            self.actions = [
                current_action
                for current_action in self.get_actions()
                if self._action_id(current_action) != action_id
            ]

        return action

    # =========================
    # Status API
    # =========================

    def set_status(self, action_id, status):
        return self.update_action(action_id, {"status": status})

    def mark_pending(self, action_id):
        return self.set_status(action_id, "Pending")

    def mark_running(self, action_id):
        return self.set_status(action_id, "Running")

    def mark_completed(self, action_id):
        return self.set_status(action_id, "Completed")

    def mark_failed(self, action_id):
        return self.set_status(action_id, "Failed")

    # =========================
    # Query API
    # =========================

    def get_pending_actions(self):
        return [
            action
            for action in self.get_actions()
            if str(self._action_status(action)).lower()
            in ["pending", "todo", "ready", "open"]
        ]

    def get_running_actions(self):
        return [
            action
            for action in self.get_actions()
            if str(self._action_status(action)).lower()
            in ["running", "active", "in_progress"]
        ]

    def get_completed_actions(self):
        return [
            action
            for action in self.get_actions()
            if str(self._action_status(action)).lower()
            in ["completed", "complete", "done", "resolved"]
        ]

    def get_actions_by_priority(self, priority):
        return [
            action
            for action in self.get_actions()
            if str(self._action_priority(action)).lower() == str(priority).lower()
        ]

    def get_actions_by_type(self, action_type):
        return [
            action
            for action in self.get_actions()
            if str(self._action_type(action)).lower() == str(action_type).lower()
        ]

    def get_actions_by_evidence_id(self, evidence_id):
        return [
            action
            for action in self.get_actions()
            if self._action_evidence_id(action) == evidence_id
        ]

    def get_action_count(self):
        return len(self.get_actions())

    def get_summary(self):
        actions = self.get_actions()

        return {
            "action_count": len(actions),
            "pending_count": len(self.get_pending_actions()),
            "running_count": len(self.get_running_actions()),
            "completed_count": len(self.get_completed_actions()),
            "action_ids": self.get_action_ids(),
        }

    # =========================
    # Internal Helpers
    # =========================

    def _action_id(self, action):
        if isinstance(action, dict):
            return (
                action.get("action_id")
                or action.get("id")
                or action.get("key")
            )

        return (
            getattr(action, "action_id", None)
            or getattr(action, "id", None)
            or getattr(action, "key", None)
        )

    def _action_status(self, action):
        if isinstance(action, dict):
            return action.get("status") or action.get("state") or "Pending"

        return (
            getattr(action, "status", None)
            or getattr(action, "state", None)
            or "Pending"
        )

    def _action_priority(self, action):
        if isinstance(action, dict):
            return action.get("priority") or action.get("severity") or "Normal"

        return (
            getattr(action, "priority", None)
            or getattr(action, "severity", None)
            or "Normal"
        )

    def _action_type(self, action):
        if isinstance(action, dict):
            return (
                action.get("action_type")
                or action.get("type")
                or action.get("category")
                or "Action"
            )

        return (
            getattr(action, "action_type", None)
            or getattr(action, "type", None)
            or getattr(action, "category", None)
            or "Action"
        )

    def _action_evidence_id(self, action):
        if isinstance(action, dict):
            return action.get("evidence_id") or action.get("source_id")

        return (
            getattr(action, "evidence_id", None)
            or getattr(action, "source_id", None)
        )

    def _set_value(self, obj, key, value):
        if isinstance(obj, dict):
            obj[key] = value
            return

        setattr(obj, key, value)