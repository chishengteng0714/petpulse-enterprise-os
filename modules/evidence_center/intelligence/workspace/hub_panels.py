import streamlit as st

from modules.evidence_center.intelligence.models import (
    EnterpriseIntelligenceHubState,
    EnterpriseIntelligenceSignal,
    EnterpriseIntelligenceSummary,
)


def render_hub_overview_panel(hub_state: EnterpriseIntelligenceHubState):
    """
    Hub Overview

    RC Final Demo Freeze:
    將平台狀態轉譯成主管可理解的企業情報概覽。
    """

    st.markdown("## 今日企業情報總覽")

    recommended_actions = getattr(
        hub_state.summary,
        "recommended_actions",
        [],
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("今日狀態", _format_status(hub_state.status))

    with col2:
        st.metric("觀察領域", len(hub_state.domains))

    with col3:
        st.metric("重要訊號", len(hub_state.signals))

    with col4:
        st.metric("建議決策", len(recommended_actions))

    st.info(
        "AI 已彙整今日企業情報，協助主管快速掌握品牌狀態、重要變化、"
        "潛在風險與下一步決策方向。"
    )


def render_hub_summary_panel(summary: EnterpriseIntelligenceSummary):
    """
    今日 AI 摘要
    """

    st.markdown("## 今日 AI 摘要")

    st.markdown(f"### {summary.title}")
    st.write(summary.narrative)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 主管今日必看")
        _render_list(
            summary.key_points,
            empty_text="目前沒有需要主管立即關注的重點。",
        )

        st.markdown("#### 需要留意的風險")
        _render_list(
            summary.risks,
            empty_text="目前沒有明顯升溫的企業風險。",
        )

    with col2:
        st.markdown("#### 可掌握的機會")
        _render_list(
            summary.opportunities,
            empty_text="目前尚未偵測到明確成長機會。",
        )

        st.markdown("#### 建議優先行動")
        _render_list(
            summary.recommended_actions,
            empty_text="目前沒有需要立即執行的建議行動。",
        )


def render_hub_signals_panel(signals: list[EnterpriseIntelligenceSignal]):
    """
    重要企業訊號
    """

    st.markdown("## 重要企業訊號")

    if not signals:
        st.success("目前沒有需要特別處理的企業訊號。")
        return

    for signal in signals:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {signal.title}")
                st.caption(
                    f"{_format_domain(signal.domain)}｜來源：{signal.source}"
                )
                st.write(signal.description)

            with col2:
                st.metric("優先度", signal.priority)

            if signal.evidence_refs:
                st.markdown("#### 可追溯依據")
                _render_list(signal.evidence_refs)


def render_hub_decision_panel(summary: EnterpriseIntelligenceSummary):
    """
    今日建議決策
    """

    st.markdown("## 今日建議決策")

    actions = summary.recommended_actions

    if not actions:
        st.success("目前沒有需要立即決策的事項。")
        return

    st.caption("以下為 AI 根據今日企業情報整理出的建議決策順序。")

    for index, action in enumerate(actions, start=1):
        with st.container(border=True):
            st.markdown(f"### {index}. {action}")
            st.write(_build_decision_note(index))


def render_hub_observation_panel(hub_state: EnterpriseIntelligenceHubState):
    """
    企業觀察
    """

    summary = hub_state.summary

    st.markdown("## 企業觀察")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 市場與品牌狀態")
        _render_observation_card(
            "整體狀態",
            "今日企業情報已完成彙整，可作為主管會議與行動排程的判斷基礎。",
        )
        _render_observation_card(
            "品牌風險",
            _build_risk_observation(summary.risks),
        )

    with col2:
        st.markdown("#### 成長與行動方向")
        _render_observation_card(
            "成長機會",
            _build_opportunity_observation(summary.opportunities),
        )
        _render_observation_card(
            "下一步",
            _build_next_step_observation(summary.recommended_actions),
        )


def _render_observation_card(title: str, description: str):
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(description)


def _render_list(items, empty_text="目前沒有資料。"):
    if not items:
        st.caption(empty_text)
        return

    for item in items:
        st.markdown(f"- {item}")


def _format_status(status):
    status_text = str(status).strip()

    status_map = {
        "active": "正常",
        "ready": "正常",
        "healthy": "正常",
        "connected": "正常",
        "stable": "穩定",
        "warning": "需關注",
        "risk": "需處理",
    }

    return status_map.get(status_text.lower(), status_text)


def _format_domain(domain):
    value = getattr(domain, "value", domain)
    text = str(value)

    domain_map = {
        "brand": "品牌",
        "market": "市場",
        "risk": "風險",
        "opportunity": "機會",
        "customer": "消費者",
        "competitor": "競品",
        "operation": "營運",
    }

    return domain_map.get(text.lower(), text)


def _build_decision_note(index: int) -> str:
    notes = {
        1: "建議列為今日優先討論事項，確認負責窗口與完成時間。",
        2: "建議安排相關團隊追蹤，避免訊號延遲擴大。",
        3: "建議納入本週行動清單，視後續聲量變化調整優先順序。",
    }

    return notes.get(
        index,
        "建議持續觀察，並在下一次主管同步時確認是否需要升級處理。",
    )


def _build_risk_observation(risks) -> str:
    if not risks:
        return "目前沒有明顯升溫的品牌或營運風險，可維持既有監測節奏。"

    return "今日已有需要留意的風險訊號，建議先確認影響範圍與回應窗口。"


def _build_opportunity_observation(opportunities) -> str:
    if not opportunities:
        return "目前尚未出現明確成長機會，建議持續觀察市場討論與消費者需求變化。"

    return "今日已出現可延伸的成長訊號，適合評估內容、活動或銷售行動。"


def _build_next_step_observation(actions) -> str:
    if not actions:
        return "目前不需要立即新增行動，建議維持例行追蹤。"

    return "建議先處理第一順位行動，並於今日完成決策與任務指派。"