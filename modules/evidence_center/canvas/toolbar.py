import streamlit as st


def render(runtime):
    render_toolbar(runtime)


def render_toolbar(runtime):
    """
    查詢工具列
    """

    st.markdown("### 查詢條件")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("查看關係圖", use_container_width=True):
            _set_view_mode(runtime, "graph")

    with col2:
        if st.button("查看時間軸", use_container_width=True):
            _set_view_mode(runtime, "timeline")

    with col3:
        if st.button("重整版面", use_container_width=True):
            _set_layout_mode(runtime, "default")

    with col4:
        if st.button("清除選取", use_container_width=True):
            _clear_selection(runtime)

    _render_current_state(runtime)


def _render_current_state(runtime):
    if not runtime:
        st.caption("證據總覽尚未準備完成。")
        return

    view_mode = _safe_call(runtime, "get_view_mode", "graph")
    layout_mode = _safe_call(runtime, "get_layout_mode", "default")

    st.caption(f"目前檢視：{_format_view_mode(view_mode)}｜版面：{_format_layout_mode(layout_mode)}")


def _set_view_mode(runtime, view_mode):
    if runtime and hasattr(runtime, "set_view_mode"):
        runtime.set_view_mode(view_mode)


def _set_layout_mode(runtime, layout_mode):
    if runtime and hasattr(runtime, "set_layout_mode"):
        runtime.set_layout_mode(layout_mode)


def _clear_selection(runtime):
    if runtime and hasattr(runtime, "clear_selection"):
        runtime.clear_selection()


def _safe_call(runtime, method_name, default=None):
    if not runtime or not hasattr(runtime, method_name):
        return default

    try:
        return getattr(runtime, method_name)()
    except Exception:
        return default


def _format_view_mode(value):
    return {
        "graph": "關係圖",
        "timeline": "時間軸",
    }.get(str(value), str(value))


def _format_layout_mode(value):
    return {
        "default": "標準",
    }.get(str(value), str(value))