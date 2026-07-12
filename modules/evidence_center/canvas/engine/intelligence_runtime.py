from .relationship_engine import RelationshipEngine
from .summary_builder import CanvasSummaryBuilder
from .copilot_context import CopilotContextBuilder
from .decision_context import DecisionContextBuilder
from .timeline_context import TimelineContextBuilder


class CanvasIntelligenceRuntime:
    """
    Canvas Intelligence Runtime

    PetPulse 第二顆核心引擎。

    負責 Canvas 層 Intelligence Orchestration。
    """

    def __init__(self, canvas_runtime):
        self.canvas_runtime = canvas_runtime

        self.relationship_engine = RelationshipEngine(
            canvas_runtime=canvas_runtime,
        )

        self.summary_builder = CanvasSummaryBuilder(
            canvas_runtime=canvas_runtime,
            relationship_engine=self.relationship_engine,
        )

        self.copilot_context_builder = CopilotContextBuilder(
            canvas_runtime=canvas_runtime,
            summary_builder=self.summary_builder,
        )

        self.decision_context_builder = DecisionContextBuilder(
            canvas_runtime=canvas_runtime,
            summary_builder=self.summary_builder,
        )

        self.timeline_context_builder = TimelineContextBuilder(
            canvas_runtime=canvas_runtime,
        )

    # =========================
    # Relationship Intelligence
    # =========================

    def get_relationships(self):
        return self.relationship_engine.get_selected_relationships()

    def get_selected_relationships(self):
        return self.relationship_engine.get_selected_relationships()

    def get_relationship_summary(self):
        return self.relationship_engine.get_relationship_summary()

    # =========================
    # Summary Intelligence
    # =========================

    def get_summary(self):
        return self.summary_builder.build()

    def get_canvas_brief(self):
        return self.summary_builder.build()

    # =========================
    # Copilot Intelligence
    # =========================

    def get_copilot_context(self):
        return self.copilot_context_builder.build()

    def get_ai_context(self):
        return self.copilot_context_builder.build()

    # =========================
    # Decision Intelligence
    # =========================

    def get_decision_context(self):
        return self.decision_context_builder.build()

    # =========================
    # Timeline Intelligence
    # =========================

    def get_timeline_context(self):
        return self.timeline_context_builder.build()