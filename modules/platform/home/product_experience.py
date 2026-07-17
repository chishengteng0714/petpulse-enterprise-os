import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


# =========================
# 首頁展示資料模型
# =========================

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


# =========================
# 資料路徑
# =========================

CURRENT_FILE = Path(__file__).resolve()

DASHBOARD_DIR = CURRENT_FILE.parents[3]
PROJECT_ROOT = CURRENT_FILE.parents[4]

PROJECT_ANALYSIS_PATH = (
    PROJECT_ROOT
    / "data"
    / "analysis.json"
)

DASHBOARD_ANALYSIS_PATH = (
    DASHBOARD_DIR
    / "data"
    / "analysis.json"
)


# =========================
# 共用安全工具
# =========================

def _safe_int(
    value: Any,
    default: int = 0,
) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def _safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_text(
    value: Any,
    default: str = "",
) -> str:
    if value is None:
        return default

    text = str(value).strip()

    return text or default


def _safe_list(
    value: Any,
) -> List[Any]:
    if isinstance(value, list):
        return value

    return []


def _clamp(
    value: int,
    minimum: int,
    maximum: int,
) -> int:
    return max(
        minimum,
        min(value, maximum),
    )


# =========================
# analysis.json 載入
# =========================

def _resolve_analysis_path() -> Path:
    """
    優先讀取專案根目錄的最新 analysis.json。

    Analyzer 正式輸出位置：
    AI-Social-Listening/data/analysis.json

    同時保留 dashboard/data/analysis.json 相容能力，
    避免舊環境中斷。
    """
    candidate_paths = [
        PROJECT_ANALYSIS_PATH,
        DASHBOARD_ANALYSIS_PATH,
    ]

    for path in candidate_paths:
        if path.exists():
            return path

    return PROJECT_ANALYSIS_PATH


def _load_analysis_data() -> Dict[str, Any]:
    """
    安全讀取 GM24 Analyzer 輸出。

    檔案不存在或 JSON 損壞時，
    回傳安全空白資料，首頁仍可正常啟動。
    """
    analysis_path = _resolve_analysis_path()

    if not analysis_path.exists():
        return _build_empty_analysis()

    try:
        with open(
            analysis_path,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return _build_empty_analysis()

        return data

    except (
        OSError,
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        return _build_empty_analysis()


def _build_empty_analysis() -> Dict[str, Any]:
    return {
        "brand_health": 0,
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "summary": (
            "目前尚未取得最新品牌情報，"
            "請先執行資料更新與 AI 分析。"
        ),
        "topics": [],
        "risks": [],
        "suggestions": [],
        "competitors": [],
        "brand_signal_count": 0,
        "competitor_signal_count": 0,
        "brand_confidence_average": 0.0,
        "negative_ratio": 0.0,
        "high_risk_count": 0,
        "data_quality": "資料不足",
        "raw_crawler_signal_count": 0,
        "filtered_signal_count": 0,
    }


# =========================
# 營運狀態判斷
# =========================

def _build_operating_status(
    brand_health: int,
    negative_ratio: float,
    high_risk_count: int,
    data_quality: str,
) -> str:
    if data_quality == "資料不足":
        return "待更新"

    if (
        brand_health >= 80
        and negative_ratio < 10
        and high_risk_count <= 1
    ):
        return "健康"

    if (
        brand_health >= 65
        and negative_ratio < 20
        and high_risk_count <= 3
    ):
        return "穩定"

    if (
        brand_health >= 50
        and negative_ratio < 30
    ):
        return "需關注"

    return "需處理"


def _build_confidence_level(
    average_confidence: float,
    data_quality: str,
) -> str:
    if data_quality == "資料不足":
        return "資料不足"

    if average_confidence >= 90:
        return "極高"

    if average_confidence >= 75:
        return "高"

    if average_confidence >= 60:
        return "中"

    return "偏低"


def _build_greeting(
    operating_status: str,
    high_risk_count: int,
    decision_count: int,
) -> str:
    if operating_status == "待更新":
        return "目前尚無最新品牌情報，請先執行資料更新。"

    if operating_status == "健康":
        if decision_count > 0:
            return (
                "今日品牌營運狀態健康，"
                f"建議主管確認 {decision_count} 項行動。"
            )

        return "今日品牌營運狀態健康，暫無重大待決策事項。"

    if operating_status == "穩定":
        return (
            "今日品牌營運維持穩定，"
            f"目前辨識到 {high_risk_count} 項風險訊號。"
        )

    if operating_status == "需關注":
        return (
            "今日品牌情報出現需關注訊號，"
            "建議主管優先確認風險來源與處理窗口。"
        )

    return (
        "今日品牌情報出現較高風險，"
        "建議立即進入證據中心確認來源與影響範圍。"
    )


# =========================
# 決策資料
# =========================

def _build_decisions(
    analysis: Dict[str, Any],
) -> List[ExecutiveDecision]:
    suggestions = _safe_list(
        analysis.get("suggestions")
    )

    risks = _safe_list(
        analysis.get("risks")
    )

    topics = _safe_list(
        analysis.get("topics")
    )

    decisions: List[ExecutiveDecision] = []

    owners = [
        "品牌行銷團隊",
        "社群與客服團隊",
        "專案負責窗口",
    ]

    urgency_labels = [
        "今日確認",
        "優先處理",
        "本週安排",
    ]

    for index, suggestion in enumerate(
        suggestions[:3]
    ):
        suggestion_text = _safe_text(
            suggestion,
            "確認後續行動與負責窗口。",
        )

        related_risk = ""

        if index < len(risks):
            related_risk = _safe_text(
                risks[index]
            )

        related_topic = ""

        if index < len(topics):
            topic = topics[index]

            if isinstance(topic, dict):
                related_topic = _safe_text(
                    topic.get("title")
                )
            else:
                related_topic = _safe_text(topic)

        if related_risk:
            description = (
                f"根據最新品牌情報，"
                f"需留意「{related_risk}」。"
            )
        elif related_topic:
            description = (
                f"目前「{related_topic}」具備管理與行動價值。"
            )
        else:
            description = (
                "根據最新分析結果，"
                "此項目具備後續執行價值。"
            )

        decisions.append(
            ExecutiveDecision(
                title=suggestion_text,
                description=description,
                owner=owners[
                    min(index, len(owners) - 1)
                ],
                urgency=urgency_labels[
                    min(
                        index,
                        len(urgency_labels) - 1,
                    )
                ],
                next_step=(
                    "確認負責窗口、完成時間與執行方式。"
                    if index != 1
                    else (
                        "前往證據中心確認來源、"
                        "脈絡與影響範圍。"
                    )
                ),
            )
        )

    if decisions:
        return decisions

    return [
        ExecutiveDecision(
            title="確認最新品牌情報",
            description=(
                "目前尚無足夠的 AI 行動建議，"
                "建議先確認資料是否已完成更新。"
            ),
            owner="品牌行銷團隊",
            urgency="今日確認",
            next_step=(
                "執行資料更新後，"
                "重新檢視首頁與證據中心。"
            ),
        )
    ]


# =========================
# 健康 KPI
# =========================

def _build_health_signals(
    analysis: Dict[str, Any],
    decision_count: int,
) -> List[HealthSignal]:
    brand_health = _clamp(
        _safe_int(
            analysis.get("brand_health")
        ),
        0,
        100,
    )

    brand_signal_count = max(
        0,
        _safe_int(
            analysis.get(
                "brand_signal_count",
                analysis.get(
                    "evidence_count",
                    0,
                ),
            )
        ),
    )

    high_risk_count = max(
        0,
        _safe_int(
            analysis.get("high_risk_count")
        ),
    )

    average_confidence = max(
        0.0,
        min(
            _safe_float(
                analysis.get(
                    "brand_confidence_average"
                )
            ),
            100.0,
        ),
    )

    negative_ratio = max(
        0.0,
        min(
            _safe_float(
                analysis.get("negative_ratio")
            ),
            100.0,
        ),
    )

    data_quality = _safe_text(
        analysis.get("data_quality"),
        "資料不足",
    )

    health_status = (
        "健康"
        if brand_health >= 80
        else "穩定"
        if brand_health >= 65
        else "需關注"
        if brand_health >= 50
        else "需處理"
    )

    risk_status = (
        "低風險"
        if high_risk_count <= 1
        else "可控"
        if high_risk_count <= 3
        else "需處理"
    )

    confidence_status = (
        "高可信"
        if average_confidence >= 75
        else "中可信"
        if average_confidence >= 60
        else "待確認"
    )

    return [
        HealthSignal(
            label="品牌健康度",
            value=f"{brand_health} 分",
            status=health_status,
            detail=(
                "依最新品牌情緒、風險與 AI 分析即時計算。"
            ),
        ),
        HealthSignal(
            label="有效品牌訊號",
            value=f"{brand_signal_count} 筆",
            status=data_quality,
            detail=(
                f"平均品牌可信度 "
                f"{average_confidence:.1f}%。"
            ),
        ),
        HealthSignal(
            label="高風險事件",
            value=f"{high_risk_count} 項",
            status=risk_status,
            detail=(
                f"目前負向訊號比例 "
                f"{negative_ratio:.1f}%。"
            ),
        ),
        HealthSignal(
            label="待確認行動",
            value=f"{decision_count} 項",
            status=confidence_status,
            detail=(
                "由最新 AI 建議與風險訊號整理。"
            ),
        ),
    ]


# =========================
# 風險資料
# =========================

def _build_risks(
    analysis: Dict[str, Any],
) -> List[RiskSignal]:
    risk_items = _safe_list(
        analysis.get("risks")
    )

    negative_ratio = _safe_float(
        analysis.get("negative_ratio")
    )

    risks: List[RiskSignal] = []

    for index, item in enumerate(
        risk_items[:5]
    ):
        title = _safe_text(
            item,
            "未命名風險訊號",
        )

        if (
            negative_ratio >= 20
            or index == 0
            and negative_ratio >= 10
        ):
            severity = "高"
        elif index <= 2:
            severity = "中"
        else:
            severity = "低"

        if index == 0:
            action = (
                "前往證據中心確認來源、"
                "討論脈絡與影響範圍。"
            )
        elif index == 1:
            action = (
                "建立統一回應口徑，"
                "確認品牌與客服處理方式。"
            )
        else:
            action = (
                "指定負責窗口，"
                "持續追蹤訊號變化。"
            )

        risks.append(
            RiskSignal(
                title=title,
                description=(
                    "此風險由最新 AI 品牌情報分析辨識，"
                    "仍應回到原始證據確認細節。"
                ),
                severity=severity,
                action=action,
            )
        )

    if risks:
        return risks

    return [
        RiskSignal(
            title="目前沒有明確高風險事件",
            description=(
                "最新分析未辨識出需要立即處理的重大風險。"
            ),
            severity="低",
            action=(
                "持續監測品牌聲量、"
                "負向比例與來源變化。"
            ),
        )
    ]


# =========================
# 成長機會
# =========================

def _build_opportunities(
    analysis: Dict[str, Any],
) -> List[OpportunitySignal]:
    topics = _safe_list(
        analysis.get("topics")
    )

    suggestions = _safe_list(
        analysis.get("suggestions")
    )

    opportunities: List[OpportunitySignal] = []

    for index, topic in enumerate(
        topics[:3]
    ):
        if isinstance(topic, dict):
            title = _safe_text(
                topic.get("title"),
                f"品牌議題 {index + 1}",
            )

            description = _safe_text(
                topic.get("description"),
                "此議題在最新品牌情報中具有較高討論價值。",
            )
        else:
            title = _safe_text(
                topic,
                f"品牌議題 {index + 1}",
            )

            description = (
                "此議題在最新品牌情報中具有較高討論價值。"
            )

        recommendation = (
            _safe_text(
                suggestions[index]
            )
            if index < len(suggestions)
            else (
                "安排小規模內容或營運測試，"
                "再依成效決定是否擴大投入。"
            )
        )

        opportunities.append(
            OpportunitySignal(
                title=title,
                description=description,
                potential=(
                    "高"
                    if index <= 1
                    else "中"
                ),
                recommendation=recommendation,
            )
        )

    if opportunities:
        return opportunities

    return [
        OpportunitySignal(
            title="等待更多有效品牌訊號",
            description=(
                "目前資料不足以形成具體成長機會判斷。"
            ),
            potential="待評估",
            recommendation=(
                "完成最新資料更新後，"
                "重新執行 AI 分析。"
            ),
        )
    ]


# =========================
# 工作入口
# =========================

def _build_workspaces() -> List[WorkspaceEntry]:
    return [
        WorkspaceEntry(
            title="企業工作區",
            description=(
                "分派任務、確認窗口，"
                "追蹤今日決策後續執行。"
            ),
            status="使用中",
            target="決策執行",
        ),
        WorkspaceEntry(
            title="證據中心",
            description=(
                "查看訊號來源、討論脈絡、"
                "品牌可信度與決策依據。"
            ),
            status="使用中",
            target="證據確認",
        ),
        WorkspaceEntry(
            title="深入調查室",
            description=(
                "追查複雜風險、異常訊號"
                "與議題形成原因。"
            ),
            status="使用中",
            target="深入調查",
        ),
    ]


# =========================
# 首頁 Experience 組裝
# =========================

def build_enterprise_home_experience() -> EnterpriseHomeExperience:
    """
    PetPulse Enterprise OS
    GM24 Brand Intelligence

    保留既有 EnterpriseHomeExperience Schema，
    不修改 Runtime、Registry、Router 或首頁組裝方式。

    本檔只負責：
    - 讀取 analysis.json
    - 將即時分析轉為首頁 Presentation Data
    - 移除寫死的 96 分、3 項與固定高可信度
    """
    analysis = _load_analysis_data()

    brand_health = _clamp(
        _safe_int(
            analysis.get("brand_health")
        ),
        0,
        100,
    )

    negative_ratio = max(
        0.0,
        min(
            _safe_float(
                analysis.get("negative_ratio")
            ),
            100.0,
        ),
    )

    high_risk_count = max(
        0,
        _safe_int(
            analysis.get("high_risk_count")
        ),
    )

    average_confidence = max(
        0.0,
        min(
            _safe_float(
                analysis.get(
                    "brand_confidence_average"
                )
            ),
            100.0,
        ),
    )

    data_quality = _safe_text(
        analysis.get("data_quality"),
        "資料不足",
    )

    decisions = _build_decisions(
        analysis
    )

    operating_status = (
        _build_operating_status(
            brand_health=brand_health,
            negative_ratio=negative_ratio,
            high_risk_count=high_risk_count,
            data_quality=data_quality,
        )
    )

    confidence_level = (
        _build_confidence_level(
            average_confidence=average_confidence,
            data_quality=data_quality,
        )
    )

    briefing_summary = _safe_text(
        analysis.get("summary"),
        (
            "目前尚未取得最新品牌情報摘要，"
            "請先執行資料更新與 AI 分析。"
        ),
    )

    return EnterpriseHomeExperience(
        greeting=_build_greeting(
            operating_status=operating_status,
            high_risk_count=high_risk_count,
            decision_count=len(decisions),
        ),
        briefing_title="今日品牌情報判斷",
        briefing_summary=briefing_summary,
        operating_status=operating_status,
        confidence_level=confidence_level,
        decisions=decisions,
        health_signals=_build_health_signals(
            analysis=analysis,
            decision_count=len(decisions),
        ),
        risks=_build_risks(
            analysis
        ),
        opportunities=_build_opportunities(
            analysis
        ),
        workspaces=_build_workspaces(),
    )