import streamlit as st

from modules.evidence_center.canvas.presenters import InspectorPresenter


def render(runtime):
    render_inspector_layer(runtime)


def render_inspector_layer(runtime):
    """
    內容檢視
    """

    view_model = InspectorPresenter(runtime).present()

    st.markdown("### 內容檢視")
    st.caption("查看目前選取項目的內容、風險與建議下一步。")

    _render_status(view_model)
    _render_focus(view_model)
    _render_selected_object(view_model)
    _render_risk_and_next_step(view_model)
    _render_counts(view_model)


def _render_status(view_model):
    col1, col2 = st.columns(2)

    with col1:
        st.metric("狀態", _format_status(view_model.get("status", "No Selection")))

    with col2:
        st.metric("選取類型", _format_type(view_model.get("selected_type", "None")))


def _render_focus(view_model):
    st.markdown("#### 目前焦點")
    st.info(view_model.get("focus", "尚未選取分析目標。"))


def _render_selected_object(view_model):
    selected_object = view_model.get("selected_object")

    st.markdown("#### 選取內容")

    if not selected_object:
        st.caption("目前尚未選取任何內容。")
        return

    st.write(f"**標題：** {view_model.get('selected_title', '未命名內容')}")
    st.write(f"**編號：** {_get_object_id(selected_object)}")

    fields = [
        ("資料來源", selected_object.get("platform")),
        ("議題", selected_object.get("topic")),
        ("情緒傾向", selected_object.get("sentiment")),
        ("優先度", selected_object.get("priority")),
    ]

    for label, value in fields:
        if value:
            st.write(f"**{label}：** {value}")

    description = (
        selected_object.get("summary")
        or selected_object.get("description")
        or selected_object.get("content")
    )

    if description:
        st.caption(description)


def _render_risk_and_next_step(view_model):
    st.markdown("#### 風險與下一步")

    st.warning(view_model.get("risk_note", "目前沒有足夠上下文判斷風險。"))
    st.success(view_model.get("next_step", "請先選取一個內容。"))


def _render_counts(view_model):
    counts = view_model.get("runtime_counts", {})

    st.markdown("#### 目前證據概況")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("關聯項目", counts.get("nodes", 0))

    with col2:
        st.metric("關聯線索", counts.get("edges", 0))

    with col3:
        st.metric("建議行動", counts.get("actions", 0))

    with col4:
        st.metric("流程紀錄", counts.get("flows", 0))


def _get_object_id(item):
    if not item:
        return "未知"

    return (
        item.get("id")
        or item.get("evidence_id")
        or item.get("action_id")
        or item.get("flow_id")
        or "未知"
    )


def _format_status(value):
    return {
        "No Selection": "尚未選取",
        "None": "尚未選取",
    }.get(str(value), str(value))


def _format_type(value):
    return {
        "None": "未選取",
        "node": "關聯項目",
        "evidence": "證據",
        "action": "行動",
        "flow": "流程",
    }.get(str(value), str(value))