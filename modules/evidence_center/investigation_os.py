class InvestigationOS:
    """
    Investigation Operating System Core
    """

    def __init__(self, modules: dict):
        self.modules = modules

    def run_cycle(self, data: list, state: dict):

        result = {
            "loop": None,
            "agent": None,
            "graph": None,
            "evolution": None,
            "memory": None,
        }

        # =========================
        # LOOP ENGINE
        # =========================
        if "loop" in self.modules:
            result["loop"] = self.modules["loop"].run_loop(data)

        # =========================
        # AGENT
        # =========================
        if "agent" in self.modules:
            result["agent"] = self.modules["agent"].next_best_evidence(
                data,
                state.get("selected")
            )

        # =========================
        # EVOLUTION
        # =========================
        if "evolution" in self.modules:
            self.modules["evolution"].learn(result.get("loop"), data)
            result["evolution"] = self.modules["evolution"].evolve_weights(data)

        # =========================
        # GRAPH
        # =========================
        if "graph" in self.modules:
            result["graph"] = self.modules["graph"].cluster(data)

        # =========================
        # MEMORY (optional hook)
        # =========================
        if "memory" in self.modules:
            self.modules["memory"].add_selection(state.get("selected"))

        return result