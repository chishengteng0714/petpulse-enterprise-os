from modules.evidence_center.canvas.presenters import (
    CopilotPresenter,
    DecisionPresenter,
    RelationshipPresenter,
    TimelinePresenter,
    InspectorPresenter,
)


class CanvasPresentationSmokeTest:
    """
    Canvas Presentation Runtime Smoke Test

    用來確認所有 Presenter 都能正常從 Runtime 取得 View Model。
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def run(self):
        results = {
            "copilot": self._test_presenter(CopilotPresenter),
            "decision": self._test_presenter(DecisionPresenter),
            "relationship": self._test_presenter(RelationshipPresenter),
            "timeline": self._test_presenter(TimelinePresenter),
            "inspector": self._test_presenter(InspectorPresenter),
        }

        return {
            "passed": all(item["passed"] for item in results.values()),
            "results": results,
        }

    def _test_presenter(self, presenter_class):
        try:
            view_model = presenter_class(self.runtime).present()

            return {
                "passed": isinstance(view_model, dict),
                "presenter": presenter_class.__name__,
                "keys": list(view_model.keys()) if isinstance(view_model, dict) else [],
                "error": None,
            }

        except Exception as error:
            return {
                "passed": False,
                "presenter": presenter_class.__name__,
                "keys": [],
                "error": str(error),
            }