from dataclasses import dataclass
from typing import List


@dataclass
class ExecutiveDecision:
    title: str
    description: str
    owner: str
    urgency: str
    next_step: str


@dataclass
class HealthSignal:
    label: str
    value: str
    status: str
    detail: str


@dataclass
class RiskSignal:
    title: str
    description: str
    severity: str
    action: str


@dataclass
class OpportunitySignal:
    title: str
    description: str
    potential: str
    recommendation: str


@dataclass
class WorkspaceEntry:
    title: str
    description: str
    status: str
    target: str


@dataclass
class EnterpriseHomeExperience:
    greeting: str
    briefing_title: str
    briefing_summary: str
    operating_status: str
    confidence_level: str
    decisions: List[ExecutiveDecision]
    health_signals: List[HealthSignal]
    risks: List[RiskSignal]
    opportunities: List[OpportunitySignal]
    workspaces: List[WorkspaceEntry]


def build_enterprise_home_experience() -> EnterpriseHomeExperience:
    """
    Enterprise Home Product Experience

    建立企業首頁所需的展示資料。

    首頁只回答：
    - 今日營運狀態是否穩定
    - 哪些決策需要主管確認
    - 哪些風險與機會需要行動
    - 下一步應該前往哪個工作區處理

    GM-07 Final Product Audit：
    - 統一主管閱讀語言
    - 強化首頁決策脈絡
    - 維持既有資料結構
    - 不改變 Runtime Behavior
    """

    return EnterpriseHomeExperience(
        greeting="今日營運狀態穩定，建議主管確認 3 項決策。",
        briefing_title="今日判斷",
        briefing_summary=(
            "目前品牌聲量、會員互動與活動表現維持健康。"
            "今日建議優先確認會員成長活動、負面討論處理方式，"
            "以及成長機會的負責窗口，避免執行節奏延遲。"
        ),
        operating_status="健康",
        confidence_level="高",
        decisions=[
            ExecutiveDecision(
                title="會員成長活動是否加碼",
                description="會員互動維持正向，可評估加碼素材與預算。",
                owner="行銷團隊",
                urgency="今日確認",
                next_step="確認預算、素材窗口與上線節奏。",
            ),
            ExecutiveDecision(
                title="負面討論是否提前處理",
                description="服務體驗與商品期待出現落差，建議先建立回應口徑。",
                owner="品牌團隊",
                urgency="優先處理",
                next_step="前往證據中心確認來源、脈絡與影響範圍。",
            ),
            ExecutiveDecision(
                title="成長機會是否轉成任務",
                description="保健與會員經營議題具備短期測試價值。",
                owner="專案窗口",
                urgency="本日安排",
                next_step="指定負責人，拆解任務並確認完成時間。",
            ),
        ],
        health_signals=[
            HealthSignal(
                label="企業健康度",
                value="96 分",
                status="健康",
                detail="整體營運穩定。",
            ),
            HealthSignal(
                label="待決策事項",
                value="3 項",
                status="今日處理",
                detail="需主管確認。",
            ),
            HealthSignal(
                label="風險訊號",
                value="3 項",
                status="可控",
                detail="建議提前管理。",
            ),
            HealthSignal(
                label="成長機會",
                value="3 項",
                status="可投入",
                detail="具短期測試價值。",
            ),
        ],
        risks=[
            RiskSignal(
                title="服務體驗討論升溫",
                description="部分顧客對服務流程與商品期待有落差。",
                severity="中",
                action="確認討論來源，建立客服與社群回應口徑。",
            ),
            RiskSignal(
                title="活動訊息理解不一致",
                description="促銷內容若溝通不清，可能造成期待落差。",
                severity="中",
                action="統一活動說明、限制條件與門市溝通版本。",
            ),
            RiskSignal(
                title="成長議題缺少負責窗口",
                description="部分機會尚未分派窗口，容易在執行階段流失。",
                severity="低",
                action="指定負責人與完成時間。",
            ),
        ],
        opportunities=[
            OpportunitySignal(
                title="會員經營內容加碼",
                description="會員互動穩定，適合推出情境內容與回購誘因。",
                potential="高",
                recommendation="安排會員專屬內容，測試互動與轉換。",
            ),
            OpportunitySignal(
                title="寵物保健議題延伸",
                description="保健、食安與季節照護具備高討論度。",
                potential="高",
                recommendation="建立保健內容企劃，串接商品、社群與門市。",
            ),
            OpportunitySignal(
                title="門市體驗轉成社群素材",
                description="實體門市互動可轉化為更有溫度的品牌內容。",
                potential="中",
                recommendation="挑選門市情境，產出短影音與圖文測試素材。",
            ),
        ],
        workspaces=[
            WorkspaceEntry(
                title="企業工作區",
                description="分派任務、確認窗口，追蹤今日決策後續執行。",
                status="使用中",
                target="決策執行",
            ),
            WorkspaceEntry(
                title="證據中心",
                description="查看訊號來源、討論脈絡與決策依據。",
                status="使用中",
                target="證據確認",
            ),
            WorkspaceEntry(
                title="深入調查室",
                description="追查複雜風險、異常訊號與形成原因。",
                status="使用中",
                target="深入調查",
            ),
        ],
    )