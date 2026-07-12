import streamlit as st

from modules.evidence_center.investigation_state import create_default_state
from modules.evidence_center.service import EvidenceService

try:
    from modules.evidence_center.components.investigation_toolbar import (
        render_investigation_toolbar,
    )
except ImportError:
    render_investigation_toolbar = None

try:
    from modules.evidence_center.components.evidence_explorer import (
        render_evidence_explorer,
    )
except ImportError:
    render_evidence_explorer = None

try:
    from modules.evidence_center.components.evidence_table import (
        render_evidence_table,
    )
except ImportError:
    render_evidence_table = None

try:
    from modules.evidence_center.components.evidence_detail import (
        render_evidence_detail,
    )
except ImportError:
    render_evidence_detail = None


def _render_component_fallback(component_name):
    st.info(f"{component_name} 元件尚未完成連接。")


def _get_display_value(value):
    label_map = {
        "All": "全部",
        "Positive": "正向",
        "Neutral": "中立",
        "Negative": "負向",
        "Latest": "最新優先",
        "Oldest": "最舊優先",
        "Relevance": "相關性優先",
    }

    if value is None:
        return "全部"

    return label_map.get(value, value)


def _render_state_debug_panel(state, evidence_items):
    """
    RC Final Demo Freeze:
    Debug Panel 不在正式 Demo 畫面顯示。
    保留函式避免影響既有結構，但不輸出 UI。
    """
    return


def _render_evidence_summary(state, evidence_items):
    """
    Evidence Summary

    RC Final Product Polish:
    - 中文化摘要指標
    - 僅呈現主管 Demo 需要的資訊
    - 不顯示技術字詞
    """

    st.markdown("### 證據摘要")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("證據數量", len(evidence_items))

    with col2:
        st.metric("資料來源", _get_display_value(state.platform))

    with col3:
        st.metric("情緒傾向", _get_display_value(state.sentiment))

    with col4:
        st.metric("排序方式", _get_display_value(state.sort_by))


def _render_first_evidence_detail(evidence_items):
    """
    Workspace Detail Area

    顯示第一筆證據作為細節預覽。
    """

    if not evidence_items:
        st.info("目前沒有可顯示的證據細節。")
        return

    if render_evidence_detail:
        render_evidence_detail(
            item=evidence_items[0],
            index=0,
        )
    else:
        _render_component_fallback("證據細節")


def render_evidence_workspace():
    """
    Evidence Workspace

    RC Final Demo Freeze:
    - 只保留新的 Investigation Toolbar 作為唯一查詢入口
    - 移除 Legacy Platform Filter
    - 全面中文化 Presentation Copy
    - 不新增 Runtime / Engine / Layer / Domain / Registry / Service Architecture
    """

    st.markdown("## 證據中心")
    st.caption("整合查詢、證據列表與細節檢視，協助快速完成深入調查。")

    st.divider()

    state = create_default_state()

    with st.container():
        if render_investigation_toolbar:
            state = render_investigation_toolbar()
        else:
            st.markdown("### 深入調查工具列")
            _render_component_fallback("深入調查工具列")

    service = EvidenceService()
    evidence_items = service.query_by_state(state)

    _render_state_debug_panel(state, evidence_items)

    with st.container():
        _render_evidence_summary(state, evidence_items)

    with st.container():
        left_col, right_col = st.columns([2, 1])

        with left_col:
            with st.container(border=True):
                st.markdown("### 證據列表")

                if render_evidence_explorer:
                    render_evidence_explorer(evidence_items)
                else:
                    _render_component_fallback("證據列表")

            with st.container(border=True):
                st.markdown("### 證據表格")

                if render_evidence_table:
                    render_evidence_table(evidence_items)
                else:
                    _render_component_fallback("證據表格")

        with right_col:
            with st.container(border=True):
                st.markdown("### 證據細節")
                _render_first_evidence_detail(evidence_items)