# modules/evidence_center/intelligence_graph.py

class IntelligenceGraph:
    """
    Evidence Intelligence Graph

    - Clustering
    - Relationship Mapping
    - Storyline Building

    GM-06 Final Schema Consistency Audit：
    使用 Golden Master Evidence Schema。
    """

    def build_clusters(self, evidences: list) -> dict:
        clusters = {}

        for evidence in evidences:
            topic = evidence.get("topic", "unknown")

            if topic not in clusters:
                clusters[topic] = []

            clusters[topic].append(
                {
                    "id": evidence.get("evidence_id")
                    or evidence.get("id"),
                    "content": evidence.get("content"),
                    "platform": evidence.get("platform"),
                }
            )

        return clusters

    def build_platform_map(self, evidences: list) -> dict:
        platform_map = {}

        for evidence in evidences:
            platform = evidence.get("platform", "unknown")

            if platform not in platform_map:
                platform_map[platform] = 0

            platform_map[platform] += 1

        return platform_map

    def generate_storyline(self, evidences: list) -> list:
        storyline = []

        if len(evidences) > 1:
            storyline.append("事件開始於多平台訊號出現")

        if len({e.get("topic") for e in evidences}) > 1:
            storyline.append("議題開始跨主題擴散")

        if sum(e.get("engagement", 0) for e in evidences) > 1000:
            storyline.append("事件進入高擴散階段")

        return storyline