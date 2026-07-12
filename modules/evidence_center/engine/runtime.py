class EvidenceCenterRuntimeEngine:
    """
    Evidence Center Runtime Engine

    Single Source of Truth for Evidence Center.

    Runtime 負責統一管理：
    - Evidence
    - Graph
    - Actions
    - Flows
    - Selection State

    UI 不應該直接猜 Runtime 內部資料結構，
    而是透過 Runtime API 取得資料。
    """

    def __init__(
        self,
        evidence_items=None,
        graph_engine=None,
        action_engine=None,
        flow_engine=None,
    ):
        self.name = "Evidence Center Runtime"
        self.version = "Engine Runtime"
        self.status = "Active"

        self.evidence_items = evidence_items or []

        self.graph_engine = graph_engine
        self.action_engine = action_engine
        self.flow_engine = flow_engine

        self.selected_node_id = None
        self.selected_edge_id = None
        self.selected_evidence_id = None

        self.metadata = {
            "source": "Evidence Center Engine",
            "single_source_of_truth": True,
            "runtime_owner": "EvidenceCenterRuntimeEngine",
        }

    # =========================
    # Evidence API
    # =========================

    def get_evidence_items(self):
        return self.evidence_items or []

    def set_evidence_items(self, evidence_items):
        self.evidence_items = evidence_items or []
        return self.evidence_items

    def get_evidence_count(self):
        return len(self.get_evidence_items())

    # =========================
    # Graph API
    # =========================

    def get_graph(self):
        if self.graph_engine is None:
            return None

        if hasattr(self.graph_engine, "get_graph"):
            return self.graph_engine.get_graph()

        return getattr(self.graph_engine, "graph", None)

    def get_nodes(self):
        if self.graph_engine is None:
            return []

        if hasattr(self.graph_engine, "get_nodes"):
            return self.graph_engine.get_nodes()

        graph = self.get_graph()

        if graph is None:
            return []

        nodes = getattr(graph, "nodes", [])

        if isinstance(nodes, dict):
            return list(nodes.values())

        return nodes or []

    def get_edges(self):
        if self.graph_engine is None:
            return []

        if hasattr(self.graph_engine, "get_edges"):
            return self.graph_engine.get_edges()

        graph = self.get_graph()

        if graph is None:
            return []

        edges = getattr(graph, "edges", [])

        if isinstance(edges, dict):
            return list(edges.values())

        return edges or []

    def get_node_by_id(self, node_id):
        for node in self.get_nodes():
            current_id = (
                getattr(node, "node_id", None)
                or getattr(node, "id", None)
                or getattr(node, "evidence_id", None)
            )

            if current_id == node_id:
                return node

        return None

    def get_edge_by_id(self, edge_id):
        for edge in self.get_edges():
            current_id = (
                getattr(edge, "edge_id", None)
                or getattr(edge, "id", None)
            )

            if current_id == edge_id:
                return edge

        return None

    # =========================
    # Action API
    # =========================

    def get_actions(self):
        if self.action_engine is None:
            return []

        if hasattr(self.action_engine, "get_actions"):
            return self.action_engine.get_actions()

        actions = getattr(self.action_engine, "actions", [])

        if isinstance(actions, dict):
            return list(actions.values())

        return actions or []

    def get_action_by_id(self, action_id):
        for action in self.get_actions():
            current_id = (
                getattr(action, "action_id", None)
                or getattr(action, "id", None)
                or getattr(action, "key", None)
            )

            if current_id == action_id:
                return action

        return None

    # =========================
    # Flow API
    # =========================

    def get_flows(self):
        if self.flow_engine is None:
            return []

        if hasattr(self.flow_engine, "get_flows"):
            return self.flow_engine.get_flows()

        flows = getattr(self.flow_engine, "flows", [])

        if isinstance(flows, dict):
            return list(flows.values())

        return flows or []

    def get_flow_by_id(self, flow_id):
        for flow in self.get_flows():
            current_id = (
                getattr(flow, "flow_id", None)
                or getattr(flow, "id", None)
                or getattr(flow, "key", None)
            )

            if current_id == flow_id:
                return flow

        return None

    # =========================
    # Selection API
    # =========================

    def select_node(self, node_id):
        self.selected_node_id = node_id
        self.selected_edge_id = None
        return self.get_selected_node()

    def select_edge(self, edge_id):
        self.selected_edge_id = edge_id
        self.selected_node_id = None
        return self.get_selected_edge()

    def select_evidence(self, evidence_id):
        self.selected_evidence_id = evidence_id
        return self.get_selected_evidence()

    def clear_selection(self):
        self.selected_node_id = None
        self.selected_edge_id = None
        self.selected_evidence_id = None

    def get_selected_node(self):
        if self.selected_node_id is None:
            return None

        return self.get_node_by_id(self.selected_node_id)

    def get_selected_edge(self):
        if self.selected_edge_id is None:
            return None

        return self.get_edge_by_id(self.selected_edge_id)

    def get_selected_evidence(self):
        if self.selected_evidence_id is None:
            return None

        for item in self.get_evidence_items():
            current_id = (
                getattr(item, "evidence_id", None)
                or getattr(item, "id", None)
            )

            if isinstance(item, dict):
                current_id = item.get("evidence_id") or item.get("id")

            if current_id == self.selected_evidence_id:
                return item

        return None

    # =========================
    # Runtime Summary API
    # =========================

    def get_summary(self):
        return {
            "runtime": self.name,
            "version": self.version,
            "status": self.status,
            "evidence_count": self.get_evidence_count(),
            "node_count": len(self.get_nodes()),
            "edge_count": len(self.get_edges()),
            "action_count": len(self.get_actions()),
            "flow_count": len(self.get_flows()),
            "selected_node_id": self.selected_node_id,
            "selected_edge_id": self.selected_edge_id,
            "selected_evidence_id": self.selected_evidence_id,
        }

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "summary": self.get_summary(),
            "metadata": self.metadata,
        }