import streamlit as st

from modules.evidence_center.service import EvidenceService
from modules.evidence_center.components.evidence_explorer import (
    render_evidence_explorer,
)
from modules.evidence_center.canvas.workspace import (
    render_evidence_canvas_workspace,
)
from modules.evidence_center.intelligence.workspace import (
    render_enterprise_intelligence_hub_tab,
    is_enterprise_intelligence_hub_available,
)


def render_evidence_workspace():
    """
    證據中心

    RC Final Product Finish.
    Presentation Layer only.
    """

    service = EvidenceService()
    evidence_items = service.get_all_evidence()

    _render_evidence_hero()

    if not evidence_items:
        st.info("目前尚未取得可顯示的證據資料。")
        return

    tab_labels = [
        "證據總覽",
        "證據清單",
    ]

    if is_enterprise_intelligence_hub_available():
        tab_labels.append("AI 決策摘要")

    tabs = st.tabs(tab_labels)

    with tabs[0]:
        render_evidence_canvas_workspace(evidence_items)

    with tabs[1]:
        render_evidence_explorer(evidence_items)

    if is_enterprise_intelligence_hub_available() and len(tabs) >= 3:
        with tabs[2]:
            render_enterprise_intelligence_hub_tab()


def _render_evidence_hero():
    st.caption("PETPULSE EVIDENCE CENTER｜決策證據中心")
    st.markdown("# 證據中心")
    st.markdown("### 每一個決策，都應該能追溯到可驗證的證據。")
    st.write(
        "證據中心彙整社群訊號、顧客回饋、品牌聲量與公開來源，"
        "協助團隊確認討論脈絡、判斷風險影響，並支援今日企業決策。"
    )

    st.markdown("")

    col_signal, col_source, col_context = st.columns(3)

    with col_signal:
        with st.container(border=True):
            st.caption("用途一")
            st.markdown("### 看見訊號")
            st.write("快速掌握品牌、商品、服務與競品相關討論。")

    with col_source:
        with st.container(border=True):
            st.caption("用途二")
            st.markdown("### 確認來源")
            st.write("追溯訊號來自哪些平台、內容與互動情境。")

    with col_context:
        with st.container(border=True):
            st.caption("用途三")
            st.markdown("### 支援決策")
            st.write("將證據轉化為主管可採用的決策依據。")

    st.markdown("")


def render():
    render_evidence_workspace()