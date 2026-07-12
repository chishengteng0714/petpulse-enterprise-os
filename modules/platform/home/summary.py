"""
Enterprise Home Summary

Golden Master Compatibility Summary Provider.

Presentation Layer Only.

Architecture Frozen:
- 不新增 Runtime
- 不新增 Engine
- 不新增 Layer
- 不新增 Domain
- 不新增 Folder Structure
- 不新增 API
- 不新增 Registry
- 不新增 State

此檔案目的：
- 保留舊版 Home Presentation Component 相容性
- 避免舊元件讀取既有欄位時產生 KeyError
- 不作為 Enterprise Home 主資料來源
- Enterprise Home 主資料來源已改為 EnterpriseHomeExperience
"""


def build_enterprise_home_summary(runtime=None):
    """
    建立 Enterprise Home Summary。

    runtime:
    - 保留參數以相容舊版呼叫端
    - Golden Master Presentation Layer 不使用 runtime
    """

    return {
        "today_label": "今日",
        "mission_title": "今日企業狀態健康，建議先完成 3 項管理決策。",
        "mission_context": (
            "PetPulse Enterprise OS 已整理今日營運訊號。"
            "目前品牌聲量與會員互動維持健康，"
            "建議先確認會員經營、品牌回應與競品促銷三項決策。"
        ),
        "primary_action": "查看今日決策",
        "mission_next_step": "建議先進入今日企業首頁，完成管理方向確認。",
        "enterprise_health": "96 分",
        "health_delta": "+2",
        "attention_level": "健康",
        "brief_updated": "今日 16:30",
        "last_updated": "今日 16:30",
        "signals_today": 28,
        "signals_delta": "+6",
        "decision_count": 3,
        "high_risk_count": 0,
        "growth_count": 3,
        "operating_confidence": "高",
        "status_label": "狀態健康",
        "status_detail": "目前企業營運可持續推進，建議先完成今日管理決策。",
        "risk_summary": "目前未達高衝擊危機，但服務體驗與競品促銷仍需觀察。",
        "opportunity_summary": "會員教育、健康品類與出遊情境具備成長空間。",
        "decisions": [
            {
                "id": "D1",
                "priority": "P1",
                "level": "今日確認",
                "title": "會員互動成長是否加碼",
                "description": "會員互動維持正向，可提高內容投放與會員經營節奏。",
                "signal": "會員互動維持正向",
                "owner": "會員經營",
                "due": "今日確認",
                "workspace": "Enterprise Workspace",
                "action": "確認本週會員溝通主軸與負責窗口。",
            },
            {
                "id": "D2",
                "priority": "P2",
                "level": "需關注",
                "title": "服務體驗討論是否回應",
                "description": "部分討論集中於服務流程與消費體驗，建議先統一品牌回應口徑。",
                "signal": "服務體驗討論升溫",
                "owner": "品牌行銷",
                "due": "今日關注",
                "workspace": "Evidence Center",
                "action": "整理主要討論來源與建議回應方向。",
            },
            {
                "id": "D3",
                "priority": "P3",
                "level": "本週評估",
                "title": "競品促銷是否需要跟進",
                "description": "競品短期促銷力道提高，可能影響會員回購與轉換。",
                "signal": "競品促銷壓力提高",
                "owner": "商務團隊",
                "due": "本週評估",
                "workspace": "Competitor Feed",
                "action": "比對促銷區間、主打品類與會員反應。",
            },
        ],
        "opportunities": [
            {
                "id": "OP1",
                "title": "會員教育內容",
                "description": "食安、保健與日常照護主題具備高互動與收藏潛力。",
                "signal": "會員教育內容互動潛力高。",
                "impact": "高",
                "confidence": "高",
                "window": "7 天",
                "owner": "會員 / 行銷團隊",
                "workspace": "Enterprise Workspace",
                "action": "規劃一組專家型內容。",
            },
            {
                "id": "OP2",
                "title": "寵物健康品類",
                "description": "消費者對營養、保健與日常照護討論度提高。",
                "signal": "健康品類討論度提高。",
                "impact": "高",
                "confidence": "高",
                "window": "14 天",
                "owner": "品牌 / 內容團隊",
                "workspace": "Enterprise Workspace",
                "action": "作為本週主要溝通主軸。",
            },
            {
                "id": "OP3",
                "title": "毛孩出遊情境",
                "description": "出遊、陪伴與照護情境具備社群分享力。",
                "signal": "毛孩出遊情境具備分享力。",
                "impact": "中",
                "confidence": "中",
                "window": "30 天",
                "owner": "品牌 / 社群團隊",
                "workspace": "Enterprise Workspace",
                "action": "設計輕量互動內容。",
            },
        ],
        "workspaces": [
            {
                "id": "enterprise_home",
                "name": "Enterprise Home",
                "title": "今日企業首頁",
                "icon": "🏠",
                "description": "掌握今日企業營運狀態、風險、機會與管理結論。",
                "recommended": True,
                "status": "Ready",
                "badge": "Recommended",
                "route": "enterprise_home",
                "target": "今日管理結論",
                "action": "查看",
            },
            {
                "id": "enterprise_workspace",
                "name": "Enterprise Workspace",
                "title": "企業工作區",
                "icon": "📊",
                "description": "處理今日優先事項、決策佇列與行動追蹤。",
                "recommended": True,
                "status": "Ready",
                "badge": "Workspace",
                "route": "workspace",
                "target": "今日營運工作台",
                "action": "進入",
            },
            {
                "id": "evidence_center",
                "name": "Evidence Center",
                "title": "證據中心",
                "icon": "📄",
                "description": "追溯決策背後的證據、訊號來源與可信度。",
                "recommended": True,
                "status": "Ready",
                "badge": "Evidence",
                "route": "evidence_center",
                "target": "證據中心",
                "action": "進入",
            },
            {
                "id": "investigation_os",
                "name": "Investigation OS",
                "title": "深入調查室",
                "icon": "🔎",
                "description": "針對高關注議題進行深度分析與後續追蹤。",
                "recommended": False,
                "status": "Ready",
                "badge": "Investigation",
                "route": "investigation",
                "target": "調查工作區",
                "action": "開啟",
            },
        ],
        "executive_takeaway": (
            "今日企業狀態健康。建議先完成會員經營、品牌回應與競品促銷三項管理決策，"
            "再交由企業工作區與證據中心承接後續執行。"
        ),
        "recommended_flow": [
            "今日企業首頁",
            "企業工作區",
            "證據中心",
            "深入調查室",
        ],
    }


def get_enterprise_home_summary(runtime=None):
    """
    取得 Enterprise Home Summary。

    保留 runtime 參數，避免舊版呼叫端傳入 runtime 時發生 TypeError。
    """

    return build_enterprise_home_summary(runtime)


def get_home_summary(runtime=None):
    """
    取得 Legacy Home Summary。

    舊版 Home Workspace 仍會呼叫：

        get_home_summary(runtime)

    因此此函式必須保留 runtime=None。
    """

    return build_enterprise_home_summary(runtime)