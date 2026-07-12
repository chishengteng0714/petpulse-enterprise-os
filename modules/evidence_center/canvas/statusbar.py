import streamlit as st


def render(runtime):
    render_statusbar(runtime)


def render_statusbar(runtime):
    """
    證據總覽狀態列
    """

    st.markdown("---")

    summary = _safe_call(runtime, "get_summary", {})
    counts = summary.get("runtime_counts", {})
    selected_type = summary.get("selected_object_type") or "未選取"
    status = summary.get("status", "尚未選取")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("狀態", _format_status(status))

    with col2:
        st.metric("選取類型", _format_selected_type(selected_type))

    with col3:
        st.metric("關聯項目", counts.get("nodes", 0))

    with col4:
        st.metric("建議行動", counts.get("actions", 0))

    with col5:
        st.metric("事件紀錄", counts.get("events", 0))


def _safe_call(runtime, method_name, default=None):
    if not runtime or not hasattr(runtime, method_name):
        return default

    try:
        return getattr(runtime, method_name)()
    except Exception:
        return default


def _format_status(value):
    return {
        "No Selection": "尚未選取",
        "None": "尚未選取",
    }.get(str(value), str(value))


def _format_selected_type(value):
    return {
        "None": "未選取",
        "node": "關聯項目",
        "evidence": "證據",
        "action": "行動",
        "flow": "流程",
    }.get(str(value), str(value))