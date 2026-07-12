import streamlit as st

from modules.evidence_center.intelligence.workspace.hub_workspace import (
    render_enterprise_intelligence_hub,
)


def render_enterprise_intelligence_hub_tab(
    evidence_runtime=None,
    canvas_runtime=None,
    canvas_intelligence_runtime=None,
    observability_service=None,
):
    """
    Enterprise Intelligence Hub Tab Integration

    這是 Evidence Workspace 與 Enterprise Intelligence Hub 之間的橋接層。

    設計目的：
    - 不讓 evidence_workspace.py 直接知道 Hub 內部細節
    - 保持 Workspace Layer 乾淨
    - 未來 Executive Briefing / Strategy Planning / Enterprise AI 都從這裡進入
    """

    st.markdown("## Enterprise Intelligence Hub")
    st.caption(
        "Enterprise Intelligence Layer integration point for Evidence Workspace."
    )

    render_enterprise_intelligence_hub(
        evidence_runtime=evidence_runtime,
        canvas_runtime=canvas_runtime,
        canvas_intelligence_runtime=canvas_intelligence_runtime,
        observability_service=observability_service,
    )


def get_enterprise_intelligence_tab_label():
    """
    Evidence Workspace Tab Label

    統一管理 Tab 名稱，避免散落在各處。
    """

    return "Enterprise Intelligence"


def is_enterprise_intelligence_hub_available():
    """
    Hub Availability Guard

    目前 Sprint D Step 3 預設可用。
    未來可以在這裡加入 feature flag、runtime health check 或權限判斷。
    """

    return True