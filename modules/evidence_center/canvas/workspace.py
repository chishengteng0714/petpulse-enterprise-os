import importlib

import streamlit as st

from modules.evidence_center.canvas.engine.canvas_runtime import CanvasRuntime


def render_evidence_canvas_workspace(evidence_items=None, evidence_runtime=None):
    """
    證據總覽

    RC Final Product Finish.
    Presentation Layer only.
    將原本工程導向 Canvas 頁面調整為主管可閱讀的證據總覽。
    """

    runtime = _get_or_create_canvas_runtime(evidence_runtime)

    st.markdown("## 證據總覽")
    st.caption("從關係、時間、脈絡與決策角度，快速理解證據背後的意義。")

    _render_canvas_summary(evidence_items)

    tab_graph, tab_timeline, tab_insight = st.tabs(
        [
            "關係圖",
            "時間軸",
            "決策脈絡",
        ]
    )

    with tab_graph:
        _safe_render("modules.evidence_center.canvas.toolbar", runtime)
        _safe_render("modules.evidence_center.canvas.graph_layer", runtime)
        _safe_render("modules.evidence_center.canvas.statusbar", runtime)

    with tab_timeline:
        _safe_render("modules.evidence_center.canvas.timeline_layer", runtime)

    with tab_insight:
        col1, col2 = st.columns(2)

        with col1:
            _safe_render("modules.evidence_center.canvas.inspector_layer", runtime)
            _safe_render("modules.evidence_center.canvas.relationship_map", runtime)

        with col2:
            _safe_render("modules.evidence_center.canvas.ai_copilot", runtime)
            _safe_render("modules.evidence_center.canvas.decision_queue", runtime)

        _safe_render("modules.evidence_center.canvas.notebook_layer", runtime)


def render_canvas_workspace(evidence_runtime=None):
    """
    Canvas Workspace 相容入口。

    保留既有呼叫方式，畫面統一導向證據總覽。
    """

    render_evidence_canvas_workspace(evidence_runtime=evidence_runtime)


def render(evidence_runtime=None):
    render_canvas_workspace(evidence_runtime=evidence_runtime)


def _render_canvas_summary(evidence_items):
    evidence_items = evidence_items or []

    total_count = len(evidence_items)
    platform_count = len(
        {
            _format_value(_safe_get(item, "platform", "未知來源"))
            for item in evidence_items
        }
    )
    topic_count = len(
        {
            _format_value(_safe_get(item, "topic", "未分類議題"))
            for item in evidence_items
        }
    )
    risk_count = len(
        [
            item
            for item in evidence_items
            if _format_value(_safe_get(item, "sentiment", "")).lower()
            in ["negative", "負面"]
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.caption("今日證據")
            st.metric("可檢視證據", total_count)

    with col2:
        with st.container(border=True):
            st.caption("來源範圍")
            st.metric("資料來源", platform_count)

    with col3:
        with st.container(border=True):
            st.caption("討論範圍")
            st.metric("議題數", topic_count)

    with col4:
        with st.container(border=True):
            st.caption("需關注")
            st.metric("風險訊號", risk_count)

    st.markdown("")


def _get_or_create_canvas_runtime(evidence_runtime=None):
    if "canvas_runtime" not in st.session_state:
        st.session_state["canvas_runtime"] = CanvasRuntime(
            evidence_runtime=evidence_runtime,
        )

    runtime = st.session_state["canvas_runtime"]

    if evidence_runtime is not None:
        runtime.evidence_runtime = evidence_runtime

    return runtime


def _safe_render(module_path, runtime):
    try:
        module = importlib.import_module(module_path)

        if not hasattr(module, "render"):
            st.caption("此區塊目前尚未開放顯示。")
            return

        module.render(runtime)

    except Exception:
        st.warning("此區塊暫時無法顯示，請稍後再查看。")


def _safe_get(item, key, default=None):
    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def _format_value(value):
    if value is None:
        return "未知"

    if hasattr(value, "value"):
        return str(value.value)

    return str(value)