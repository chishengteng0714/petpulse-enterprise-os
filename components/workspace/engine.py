from datetime import datetime

from components.workspace.mappers import (
    map_topic_to_signal,
    map_competitor_to_feed_item,
)


def _safe_get(data, key, default=None):
    if not isinstance(data, dict):
        return default

    return data.get(key, default)


def _safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _get_latest_health(history, fallback=0):
    try:
        if history is None or history.empty:
            return fallback

        if "health" not in history.columns:
            return fallback

        return _safe_number(history.iloc[-1]["health"], fallback)

    except Exception:
        return fallback


def _get_previous_health(history, fallback=0):
    try:
        if history is None or history.empty or len(history) < 2:
            return fallback

        if "health" not in history.columns:
            return fallback

        return _safe_number(history.iloc[-2]["health"], fallback)

    except Exception:
        return fallback


def _calculate_health_delta(current_health, previous_health):
    return round(current_health - previous_health, 1)


def _build_workspace_status(current_health, health_delta):
    if current_health >= 80:
        status = "Healthy"
        tone = "positive"
        message = "品牌健康度維持在良好區間，適合推進成長型任務。"
    elif current_health >= 60:
        status = "Watch"
        tone = "warning"
        message = "品牌狀態需要觀察，建議優先處理負面訊號與高風險議題。"
    else:
        status = "Critical"
        tone = "danger"
        message = "品牌健康度偏低，需要立即啟動修復與回應流程。"

    return {
        "status": status,
        "tone": tone,
        "message": message,
        "health": current_health,
        "delta": health_delta,
    }


def _build_focus(workspace_status, data):
    risks = _safe_get(data, "risks", [])
    recommendations = _safe_get(data, "recommendations", [])
    insights = _safe_get(data, "insights", [])

    if workspace_status["status"] == "Critical":
        title = "優先處理品牌風險"
        description = "目前品牌健康度偏低，建議先檢查負面聲量、顧客抱怨與高風險議題。"
        priority = "High"
    elif risks:
        title = "確認高風險訊號"
        description = "AI 偵測到潛在風險，建議先完成人工確認，再決定是否加入 Action Queue。"
        priority = "High"
    elif recommendations:
        title = "推進 AI 建議行動"
        description = "目前已有可執行建議，適合轉換成下一步行銷或營運任務。"
        priority = "Medium"
    elif insights:
        title = "檢視最新市場洞察"
        description = "目前品牌狀態穩定，建議從洞察中尋找成長機會。"
        priority = "Medium"
    else:
        title = "維持品牌監控"
        description = "目前尚未偵測到明確風險或機會，建議持續觀察每日訊號。"
        priority = "Low"

    return {
        "title": title,
        "description": description,
        "priority": priority,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def _build_ai_inbox(data):
    inbox_items = []

    for risk in _safe_get(data, "risks", []):
        inbox_items.append(
            {
                "type": "Risk",
                "title": risk,
                "description": "AI 偵測到可能影響品牌信任的風險訊號。",
                "priority": "High",
                "variant": "danger",
                "source": "Risk Engine",
            }
        )

    for recommendation in _safe_get(data, "recommendations", []):
        inbox_items.append(
            {
                "type": "Recommendation",
                "title": recommendation,
                "description": "AI 建議可轉換成行銷、營運或客服任務。",
                "priority": "Medium",
                "variant": "warning",
                "source": "Recommendation Engine",
            }
        )

    for insight in _safe_get(data, "insights", []):
        inbox_items.append(
            {
                "type": "Insight",
                "title": insight,
                "description": "AI 整理出的市場或消費者洞察。",
                "priority": "Low",
                "variant": "default",
                "source": "Insight Engine",
            }
        )

    return inbox_items


def _build_priority_queue(ai_inbox):
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    return sorted(
        ai_inbox,
        key=lambda item: priority_order.get(item.get("priority"), 99),
    )


def _build_recent_signals(data):
    topics = _safe_get(data, "topics", [])

    return [
        map_topic_to_signal(topic)
        for topic in topics
    ]


def _build_action_queue(ai_inbox):
    actions = []

    for item in ai_inbox:
        if item.get("priority") in ["High", "Medium"]:
            actions.append(
                {
                    "title": item.get("title", "未命名任務"),
                    "description": "建議人工確認後，轉換成可執行任務。",
                    "priority": item.get("priority", "Medium"),
                    "status": "Pending Review",
                    "source": item.get("source", "AI Engine"),
                }
            )

    return actions


def _build_competitor_feed(data):
    competitors = _safe_get(data, "competitors", [])

    return [
        map_competitor_to_feed_item(competitor)
        for competitor in competitors
    ]


def build_workspace_context(data, history=None):
    data = data if isinstance(data, dict) else {}

    fallback_health = _safe_number(_safe_get(data, "brand_health", 0), 0)

    current_health = _get_latest_health(
        history=history,
        fallback=fallback_health,
    )

    previous_health = _get_previous_health(
        history=history,
        fallback=current_health,
    )

    health_delta = _calculate_health_delta(
        current_health=current_health,
        previous_health=previous_health,
    )

    workspace_status = _build_workspace_status(
        current_health=current_health,
        health_delta=health_delta,
    )

    focus = _build_focus(
        workspace_status=workspace_status,
        data=data,
    )

    ai_inbox = _build_ai_inbox(data)
    priority_queue = _build_priority_queue(ai_inbox)
    recent_signals = _build_recent_signals(data)
    action_queue = _build_action_queue(ai_inbox)
    competitor_feed = _build_competitor_feed(data)

    return {
        "meta": {
            "platform": "PetPulse Enterprise Intelligence Platform",
            "engine": "Enterprise Context Engine v2",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        "workspace_status": workspace_status,
        "focus": focus,
        "ai_inbox": ai_inbox,
        "priority_queue": priority_queue,
        "recent_signals": recent_signals,
        "action_queue": action_queue,
        "competitor_feed": competitor_feed,
        "raw": {
            "data": data,
            "history_available": history is not None,
        },
    }