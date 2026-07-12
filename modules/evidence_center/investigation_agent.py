class InvestigationAgent:
    """
    Autonomous Investigation Agent
    - suggests next step
    - ranks evidence priority
    - runs investigation loop logic
    """

    def score_evidence(self, evidences: list) -> list:

        scored = []

        for e in evidences:

            score = 0

            # engagement weight
            score += e.get("engagement", 0) * 0.6

            # topic richness
            if e.get("topic"):
                score += 10

            # platform diversity bonus
            if e.get("platform") in ["FB", "IG", "PTT"]:
                score += 5

            scored.append({
                "evidence": e,
                "score": score
            })

        return sorted(scored, key=lambda x: x["score"], reverse=True)

    def next_best_evidence(self, evidences: list, selected: dict) -> dict:

        if not evidences:
            return None

        ranked = self.score_evidence(evidences)

        for item in ranked:

            e = item["evidence"]

            if selected and (
                e.get("id") == selected.get("id")
                or e.get("evidence_id") == selected.get("evidence_id")
            ):
                continue

            return e

        return ranked[0]["evidence"]

    def investigation_loop_hint(self, evidences: list) -> str:

        if len(evidences) < 2:
            return "Need more data for investigation loop"

        high_eng = sum(1 for e in evidences if e.get("engagement", 0) > 50)

        if high_eng > 2:
            return "High engagement cluster detected → explore propagation path"

        return "Continue expanding evidence coverage"