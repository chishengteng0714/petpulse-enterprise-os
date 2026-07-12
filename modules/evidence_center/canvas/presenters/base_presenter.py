class BaseCanvasPresenter:
    """
    Base Canvas Presenter

    Presenter 是 Canvas Presentation Layer 的資料轉換層。

    原則：
    - 不保存 Runtime State
    - 不做 Intelligence Logic
    - 不直接操作 Evidence Engine
    - 只把 Intelligence Context 轉成 UI 好讀的 View Model
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def _safe_call(self, method_name, default=None):
        if not self.runtime:
            return default

        if not hasattr(self.runtime, method_name):
            return default

        try:
            return getattr(self.runtime, method_name)()
        except Exception:
            return default

    def _get_object_title(self, item):
        if not item:
            return "Untitled"

        return (
            item.get("title")
            or item.get("label")
            or item.get("name")
            or item.get("summary")
            or item.get("id")
            or item.get("evidence_id")
            or item.get("action_id")
            or item.get("flow_id")
            or "Untitled"
        )

    def _get_object_id(self, item):
        if not item:
            return None

        return (
            item.get("id")
            or item.get("evidence_id")
            or item.get("action_id")
            or item.get("flow_id")
        )