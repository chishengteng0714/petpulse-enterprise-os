# modules/evidence_center/knowledge_memory_graph.py

class KnowledgeMemoryGraph:
    """
    Cross-Investigation Knowledge Graph

    負責保存跨 Investigation 的長期知識圖譜。

    GM-06 Final Schema Consistency Audit：
    - 使用 Golden Master Evidence Schema
    - Graph Domain 保持不變
    """

    def __init__(self):
        self.global_nodes = {}
        self.global_edges = []

    def ingest(self, evidences: list):
        for evidence in evidences:
            node_id = (
                evidence.get("evidence_id")
                or evidence.get("id")
            )

            self.global_nodes[node_id] = {
                "content": evidence.get("content"),
                "topic": evidence.get("topic"),
                "platform": evidence.get("platform"),
            }

        self._build_links()

    def _build_links(self):
        self.global_edges = []

        nodes = list(self.global_nodes.items())

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                node1_id, node1 = nodes[i]
                node2_id, node2 = nodes[j]

                if node1["topic"] == node2["topic"]:
                    self.global_edges.append(
                        (node1_id, node2_id)
                    )

                elif node1["platform"] == node2["platform"]:
                    self.global_edges.append(
                        (node1_id, node2_id)
                    )

    def get_graph_summary(self):
        return {
            "nodes": len(self.global_nodes),
            "edges": len(self.global_edges),
            "clusters": self._count_clusters(),
        }

    def _count_clusters(self):
        topics = {}

        for node in self.global_nodes.values():
            topic = node.get("topic", "unknown")
            topics[topic] = topics.get(topic, 0) + 1

        return topics