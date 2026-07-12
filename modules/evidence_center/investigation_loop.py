class InvestigationLoopEngine:

    def run_loop(self, evidences: list) -> dict:

        if not evidences:
            return {
                "status": "empty",
                "next_action": "collect initial evidence"
            }

        platforms = set(e.get("platform") for e in evidences)
        topics = set(e.get("topic") for e in evidences)

        gaps = []

        if len(platforms) < 2:
            gaps.append("Need cross-platform evidence expansion")

        if len(topics) < 2:
            gaps.append("Need topic diversification")

        avg_eng = sum(e.get("engagement", 0) for e in evidences) / len(evidences)

        if avg_eng < 20:
            gaps.append("Low engagement signals")

        if gaps:
            return {
                "status": "expand",
                "gaps": gaps,
                "next_action": "expand evidence coverage"
            }

        return {
            "status": "stable",
            "next_action": "learn & refine"
        }

    def refine_hypothesis(self, old: list, new_evidence: list) -> list:

        updated = old.copy() if old else []

        if len(new_evidence) > 3:
            updated.append("Cross-source reinforcement detected")

        return updated