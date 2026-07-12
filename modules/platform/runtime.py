from modules.platform.workspace_registry import create_workspace_registry


class PlatformRuntime:
    """
    Platform Runtime Golden Master

    提供 PetPulse Enterprise OS 平台層所需的基礎資料。

    負責提供：
    - Workspace Registry
    - Platform Summary
    - Navigation Context

    GM-07 Final Product Audit：
    - 維持既有 Runtime 行為
    - 不新增 Runtime / Engine / Layer / Domain / Registry / API
    - 僅整理 Docstring 與可讀性
    """

    def __init__(self):
        self.workspace_registry = create_workspace_registry()

    def get_workspace_registry(self):
        """
        取得 Workspace Registry。
        """

        return self.workspace_registry

    def get_workspaces(self):
        """
        取得目前可用的工作區清單。
        """

        return self.workspace_registry.get_workspaces()

    def get_summary(self):
        """
        取得 Enterprise Home 可安全渲染的基礎摘要資料。
        """

        return {
            "enterprise_health": "Stable",
            "health_delta": "Operational",
            "health_score": 0.78,
            "health_description": (
                "PetPulse Enterprise OS 目前運作穩定，"
                "品牌聲量、風險訊號與 Evidence Coverage 皆可正常追蹤。"
            ),
            "active_signals": 12,
            "signal_delta": "+3 today",
            "open_risks": 2,
            "risk_delta": "Watching",
            "decision_queue": 4,
            "decision_delta": "Pending",
            "briefing_message": (
                "今日重點：品牌討論維持穩定，但部分高互動負面訊號需要追蹤。"
                "建議優先檢查 Evidence Center，並將高風險議題加入 Investigation Studio。"
            ),
            "health_signals": [
                {
                    "label": "Brand Signal",
                    "description": "品牌討論維持正常區間，互動量略有上升。",
                },
                {
                    "label": "Risk Signal",
                    "description": "目前存在少數待追蹤風險，建議持續觀察負面高互動內容。",
                },
                {
                    "label": "Evidence Coverage",
                    "description": "Evidence Center 可支援主要洞察回溯至原始證據。",
                },
            ],
        }


def create_platform_runtime():
    """
    建立 Platform Runtime。
    """

    return PlatformRuntime()