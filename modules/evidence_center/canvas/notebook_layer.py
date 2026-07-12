import streamlit as st


def render(runtime):
    render_notebook_layer(runtime)


def render_notebook_layer(runtime):
    """
    調查筆記
    """

    st.markdown("### 調查筆記")
    st.caption("記錄目前調查過程中的觀察、假設與下一步問題。")

    if "canvas_notebook_notes" not in st.session_state:
        st.session_state["canvas_notebook_notes"] = ""

    brief = _safe_call(runtime, "get_canvas_brief", {})
    focus = brief.get("focus", "尚未選取分析目標。")

    st.info(f"目前焦點：{focus}")

    st.session_state["canvas_notebook_notes"] = st.text_area(
        "筆記內容",
        value=st.session_state["canvas_notebook_notes"],
        height=180,
        placeholder="記錄你的調查假設、觀察、下一步問題……",
    )


def _safe_call(runtime, method_name, default=None):
    if not runtime or not hasattr(runtime, method_name):
        return default

    try:
        return getattr(runtime, method_name)()
    except Exception:
        return default