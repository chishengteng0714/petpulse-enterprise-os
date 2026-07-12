import streamlit as st

from modules.evidence_center.canvas.presenters import TimelinePresenter


def render(runtime):
    render_timeline_layer(runtime)


def render_timeline_layer(runtime):
    """
    時間軸

    GM-08 Enterprise Design System v2：
    - 移除 HTML Event Card
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native Components
    - 保持 Runtime Behavior 不變
    """

    view_model = TimelinePresenter(runtime).present()

    st.markdown("### 時間軸")
    st.caption("依時間順序查看證據與操作紀錄，協助理解事件發展。")

    _render_summary(view_model)
    _render_events(view_model)


def _render_summary(view_model):
    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("事件數", view_model.get("total_events", 0))

    with col2:
        st.info(view_model.get("message", "目前尚未累積事件紀錄。"))


def _render_events(view_model):
    events = view_model.get("events", [])

    if not events:
        st.caption("目前尚未有事件紀錄。")
        return

    for event in reversed(events[-8:]):
        _render_event_card(event)


def _render_event_card(event):
    event_type = event.get("type", "事件")
    payload = event.get("payload", {})
    timestamp = event.get("timestamp") or "尚未記錄時間"

    with st.container(border=True):
        st.markdown(f"#### {_format_event_type(event_type)}")
        st.caption(timestamp)
        st.write(payload)


def _format_event_type(value):
    return {
        "event": "事件",
        "selection": "選取紀錄",
        "node_selected": "已選取關聯項目",
    }.get(str(value), str(value))