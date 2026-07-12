from dataclasses import dataclass


@dataclass(frozen=True)
class WorkspaceRoute:
    key: str
    label: str
    description: str
    icon: str
    target: str
    status: str = "available"


class WorkspaceRegistry:
    """
    Workspace Registry

    GM-10 Final Polish：
    - 全中文展示
    - 保留舊接口 list_enabled()
    - 不改架構
    """

    def __init__(self):
        self._routes = [
            WorkspaceRoute(
                key="enterprise_home",
                label="今日企業首頁",
                description="掌握今日狀態、待決策事項與下一步行動。",
                icon="🏠",
                target="enterprise_home",
                status="available",
            ),
            WorkspaceRoute(
                key="evidence_center",
                label="證據中心",
                description="檢視公開訊號、原始證據與決策依據。",
                icon="📌",
                target="evidence_center",
                status="available",
            ),
            WorkspaceRoute(
                key="decision_center",
                label="決策中心",
                description="整理今日需要主管確認的判斷與行動。",
                icon="🎯",
                target="decision_center",
                status="available",
            ),
            WorkspaceRoute(
                key="risk_radar",
                label="風險雷達",
                description="追蹤需要提前處理的營運與品牌風險。",
                icon="⚠️",
                target="risk_radar",
                status="available",
            ),
            WorkspaceRoute(
                key="growth_opportunity",
                label="成長機會",
                description="彙整具備驗證價值的市場機會。",
                icon="🌱",
                target="growth_opportunity",
                status="available",
            ),
        ]

    def list_routes(self):
        return list(self._routes)

    def list_available_routes(self):
        return [route for route in self._routes if route.status == "available"]

    def list_enabled(self):
        """
        舊版 Platform Frame 使用的接口。
        必須保留，避免 AttributeError。
        """

        return self.list_available_routes()

    def get_route(self, key: str):
        for route in self._routes:
            if route.key == key:
                return route
        return None


def create_workspace_registry():
    return WorkspaceRegistry()