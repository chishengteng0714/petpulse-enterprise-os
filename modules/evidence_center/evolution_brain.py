class EvolutionBrain:
    """
    Self-Evolving Investigation Brain
    - learns from past loops
    - adjusts evidence weights
    - evolves hypotheses
    """

    def __init__(self):
        self.success_patterns = []
        self.failed_patterns = []

    def learn(self, loop_result: dict, evidences: list):

        if loop_result.get("status") == "stable":

            pattern = {
                "topics": [e.get("topic") for e in evidences],
                "platforms": [e.get("platform") for e in evidences],
            }

            self.success_patterns.append(pattern)

        elif loop_result.get("status") == "expand":

            self.failed_patterns.append({
                "gaps": loop_result.get("gaps", [])
            })

    def evolve_weights(self, evidences: list) -> list:

        evolved = []

        for e in evidences:

            weight = 0

            # base engagement
            weight += e.get("engagement", 0)

            # learned boost
            for p in self.success_patterns:

                if e.get("topic") in p["topics"]:
                    weight += 10

            evolved.append({
                "evidence": e,
                "weight": weight
            })

        return sorted(evolved, key=lambda x: x["weight"], reverse=True)

    def evolve_hypothesis(self, old: list, new_data: list) -> list:

        updated = old.copy() if old else []

        for e in new_data:

            if e.get("sentiment") == "negative":
                updated.append("Negative cluster reinforcement detected")

            if e.get("engagement", 0) > 100:
                updated.append("High impact signal strengthening hypothesis")

        return list(set(updated))