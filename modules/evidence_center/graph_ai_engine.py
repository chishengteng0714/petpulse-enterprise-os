class GraphAIEngine:
    """
    Graph Intelligence v2
    - clustering
    - anomaly detection
    - investigation path suggestion
    """

    def cluster(self, evidences: list) -> dict:

        clusters = {}

        for e in evidences:

            key = e.get("topic", "unknown")

            if key not in clusters:
                clusters[key] = []

            clusters[key].append(e)

        return clusters

    def detect_anomalies(self, evidences: list) -> list:

        anomalies = []

        for e in evidences:

            # low engagement anomaly
            if e.get("engagement", 0) < 5:
                anomalies.append({
                    "id": e.get("evidence_id") or e.get("id"),
                    "reason": "low engagement signal"
                })

            # missing topic anomaly
            if not e.get("topic"):
                anomalies.append({
                    "id": e.get("evidence_id") or e.get("id"),
                    "reason": "missing topic"
                })

        return anomalies

    def suggest_path(self, evidences: list) -> list:

        path = []

        sorted_ev = sorted(
            evidences,
            key=lambda x: x.get("engagement", 0),
            reverse=True
        )

        if sorted_ev:
            path.append(sorted_ev[0])

        if len(sorted_ev) > 1:
            path.append(sorted_ev[1])

        return path