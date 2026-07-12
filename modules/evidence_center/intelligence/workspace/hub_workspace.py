import streamlit as st

from modules.evidence_center.intelligence.service import (
    create_enterprise_intelligence_service,
)
from modules.evidence_center.intelligence.workspace.hub_panels import (
    render_hub_decision_panel,
    render_hub_observation_panel,
    render_hub_overview_panel,
    render_hub_signals_panel,
    render_hub_summary_panel,
)


def render_enterprise_intelligence_hub(
    evidence_runtime=None,
    canvas_runtime=None,
    canvas_intelligence_runtime=None,
    observability_service=None,
):
    """
    Enterprise Intelligence Hub

    RC Final Demo Freeze:
    將 Enterprise Intelligence Hub 從工程導向入口，
    調整為主管可閱讀、可決策的企業情報工作區。

    Presentation Layer only.
    不新增 Runtime / Engine / Layer / Domain / API / Registry / State。
    """

    service = create_enterprise_intelligence_service(
        evidence_runtime=evidence_runtime,
        canvas_runtime=canvas_runtime,
        canvas_intelligence_runtime=canvas_intelligence_runtime,
        observability_service=observability_service,
    )

    hub_state = service.get_hub_state()

    st.markdown("# Enterprise Intelligence Hub")
    st.caption(
        "AI 今日企業情報中心｜整理市場訊號、品牌風險、成長機會與建議決策。"
    )

    render_hub_overview_panel(hub_state)

    tab_summary, tab_signals, tab_decisions, tab_observation = st.tabs(
        [
            "今日 AI 摘要",
            "重要企業訊號",
            "今日建議決策",
            "企業觀察",
        ]
    )

    with tab_summary:
        render_hub_summary_panel(hub_state.summary)

    with tab_signals:
        render_hub_signals_panel(hub_state.signals)

    with tab_decisions:
        render_hub_decision_panel(hub_state.summary)

    with tab_observation:
        render_hub_observation_panel(hub_state)