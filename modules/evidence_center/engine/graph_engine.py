from modules.evidence_center.engine.models import (
    EngineEdge,
    EngineGraph,
    EngineNode,
)


class EvidenceGraphEngine:
    """
    Evidence Graph Engine

    Engine Runtime 的 Graph 管理核心。

    職責：
    - 持有唯一 EngineGraph
    - 對外提供穩定 Graph API
    - UI 不直接操作 graph.nodes / graph.edges
    - 不建立第二套 Graph
    """

    def __init__(self, graph=None):
        self.graph = graph or EngineGraph()

    # =========================
    # Graph API
    # =========================

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph or EngineGraph()
        return self.graph

    def clear_graph(self):
        self.graph = EngineGraph()
        return self.graph

    # =========================
    # Node API
    # =========================

    def get_nodes(self):
        nodes = getattr(self.graph, "nodes", [])

        if isinstance(nodes, dict):
            return list(nodes.values())

        return nodes or []

    def get_node_ids(self):
        return [self._node_id(node) for node in self.get_nodes()]

    def get_node_by_id(self, node_id):
        for node in self.get_nodes():
            if self._node_id(node) == node_id:
                return node

        return None

    def add_node(self, node):
        if node is None:
            return None

        node_id = self._node_id(node)

        if not node_id:
            return None

        if isinstance(getattr(self.graph, "nodes", None), dict):
            self.graph.nodes[node_id] = node
            return node

        nodes = self.get_nodes()

        existing_node = self.get_node_by_id(node_id)

        if existing_node is not None:
            self.update_node(node_id, node)
            return node

        nodes.append(node)
        self.graph.nodes = nodes

        return node

    def create_node(
        self,
        node_id,
        title,
        node_type="Evidence",
        summary="",
        evidence_ids=None,
        metadata=None,
    ):
        node = EngineNode(
            node_id=node_id,
            title=title,
            node_type=node_type,
            summary=summary,
            evidence_ids=evidence_ids or [],
            metadata=metadata or {},
        )

        return self.add_node(node)

    def update_node(self, node_id, updates):
        node = self.get_node_by_id(node_id)

        if node is None:
            return None

        if isinstance(updates, dict):
            for key, value in updates.items():
                self._set_value(node, key, value)
        else:
            replacement_id = self._node_id(updates)

            if replacement_id == node_id:
                self.remove_node(node_id)
                self.add_node(updates)
                return updates

        return node

    def remove_node(self, node_id):
        node = self.get_node_by_id(node_id)

        if node is None:
            return None

        if isinstance(getattr(self.graph, "nodes", None), dict):
            self.graph.nodes.pop(node_id, None)
        else:
            self.graph.nodes = [
                current_node
                for current_node in self.get_nodes()
                if self._node_id(current_node) != node_id
            ]

        self.graph.edges = [
            edge
            for edge in self.get_edges()
            if self._edge_source(edge) != node_id and self._edge_target(edge) != node_id
        ]

        return node

    # =========================
    # Edge API
    # =========================

    def get_edges(self):
        edges = getattr(self.graph, "edges", [])

        if isinstance(edges, dict):
            return list(edges.values())

        return edges or []

    def get_edge_ids(self):
        return [self._edge_id(edge) for edge in self.get_edges()]

    def get_edge_by_id(self, edge_id):
        for edge in self.get_edges():
            if self._edge_id(edge) == edge_id:
                return edge

        return None

    def add_edge(self, edge):
        if edge is None:
            return None

        edge_id = self._edge_id(edge)

        if not edge_id:
            return None

        if isinstance(getattr(self.graph, "edges", None), dict):
            self.graph.edges[edge_id] = edge
            return edge

        edges = self.get_edges()

        existing_edge = self.get_edge_by_id(edge_id)

        if existing_edge is not None:
            self.update_edge(edge_id, edge)
            return edge

        edges.append(edge)
        self.graph.edges = edges

        return edge

    def create_edge(
        self,
        edge_id,
        source,
        target,
        edge_type="relates_to",
        label=None,
        metadata=None,
    ):
        edge = EngineEdge(
            edge_id=edge_id,
            source=source,
            target=target,
            edge_type=edge_type,
            label=label or edge_type,
            metadata=metadata or {},
        )

        return self.add_edge(edge)

    def connect(
        self,
        source,
        target,
        edge_type="relates_to",
        label=None,
        metadata=None,
    ):
        edge_id = f"{source}__{edge_type}__{target}"

        return self.create_edge(
            edge_id=edge_id,
            source=source,
            target=target,
            edge_type=edge_type,
            label=label or edge_type,
            metadata=metadata or {},
        )

    def update_edge(self, edge_id, updates):
        edge = self.get_edge_by_id(edge_id)

        if edge is None:
            return None

        if isinstance(updates, dict):
            for key, value in updates.items():
                self._set_value(edge, key, value)
        else:
            replacement_id = self._edge_id(updates)

            if replacement_id == edge_id:
                self.remove_edge(edge_id)
                self.add_edge(updates)
                return updates

        return edge

    def remove_edge(self, edge_id):
        edge = self.get_edge_by_id(edge_id)

        if edge is None:
            return None

        if isinstance(getattr(self.graph, "edges", None), dict):
            self.graph.edges.pop(edge_id, None)
        else:
            self.graph.edges = [
                current_edge
                for current_edge in self.get_edges()
                if self._edge_id(current_edge) != edge_id
            ]

        return edge

    def disconnect(self, source, target, edge_type=None):
        removed_edges = []

        for edge in list(self.get_edges()):
            is_same_pair = (
                self._edge_source(edge) == source
                and self._edge_target(edge) == target
            )

            is_same_type = (
                edge_type is None
                or self._edge_type(edge) == edge_type
                or self._edge_label(edge) == edge_type
            )

            if is_same_pair and is_same_type:
                removed_edge = self.remove_edge(self._edge_id(edge))
                if removed_edge is not None:
                    removed_edges.append(removed_edge)

        return removed_edges

    # =========================
    # Query API
    # =========================

    def get_neighbors(self, node_id):
        neighbors = []

        for edge in self.get_edges():
            source = self._edge_source(edge)
            target = self._edge_target(edge)

            if source == node_id:
                target_node = self.get_node_by_id(target)
                if target_node is not None:
                    neighbors.append(target_node)

            if target == node_id:
                source_node = self.get_node_by_id(source)
                if source_node is not None:
                    neighbors.append(source_node)

        return neighbors

    def get_edges_for_node(self, node_id):
        return [
            edge
            for edge in self.get_edges()
            if self._edge_source(edge) == node_id or self._edge_target(edge) == node_id
        ]

    def get_node_count(self):
        return len(self.get_nodes())

    def get_edge_count(self):
        return len(self.get_edges())

    def get_summary(self):
        return {
            "node_count": self.get_node_count(),
            "edge_count": self.get_edge_count(),
            "node_ids": self.get_node_ids(),
            "edge_ids": self.get_edge_ids(),
        }

    # =========================
    # Internal Helpers
    # =========================

    def _node_id(self, node):
        if isinstance(node, dict):
            return (
                node.get("node_id")
                or node.get("id")
                or node.get("evidence_id")
            )

        return (
            getattr(node, "node_id", None)
            or getattr(node, "id", None)
            or getattr(node, "evidence_id", None)
        )

    def _edge_id(self, edge):
        if isinstance(edge, dict):
            return (
                edge.get("edge_id")
                or edge.get("id")
                or self._build_edge_id(edge)
            )

        return (
            getattr(edge, "edge_id", None)
            or getattr(edge, "id", None)
            or self._build_edge_id(edge)
        )

    def _edge_source(self, edge):
        if isinstance(edge, dict):
            return edge.get("source") or edge.get("source_id")

        return getattr(edge, "source", None) or getattr(edge, "source_id", None)

    def _edge_target(self, edge):
        if isinstance(edge, dict):
            return edge.get("target") or edge.get("target_id")

        return getattr(edge, "target", None) or getattr(edge, "target_id", None)

    def _edge_type(self, edge):
        if isinstance(edge, dict):
            return edge.get("edge_type") or edge.get("type")

        return getattr(edge, "edge_type", None) or getattr(edge, "type", None)

    def _edge_label(self, edge):
        if isinstance(edge, dict):
            return edge.get("label") or edge.get("relation")

        return getattr(edge, "label", None) or getattr(edge, "relation", None)

    def _build_edge_id(self, edge):
        source = self._edge_source(edge)
        target = self._edge_target(edge)
        edge_type = self._edge_type(edge) or self._edge_label(edge) or "relates_to"

        if source and target:
            return f"{source}__{edge_type}__{target}"

        return None

    def _set_value(self, obj, key, value):
        if isinstance(obj, dict):
            obj[key] = value
            return

        setattr(obj, key, value)