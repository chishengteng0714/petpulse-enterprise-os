import streamlit as st


def render(runtime):
    render_event_log_layer(runtime)


def render_event_log_layer(runtime):
    """
    Canvas Event Log Layer

    顯示 Canvas Runtime Event Bus 的事件紀錄。
    """

    st.markdown("### Canvas Event Log")
    st.caption("顯示 Canvas Runtime 事件，用於 Debug 與 Timeline Intelligence。")

    events = _safe_call(runtime, "get_events", [])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.metric("Events", len(events))

    with col2:
        if st.button("Clear Events", width="stretch"):
            if runtime and hasattr(runtime, "clear_events"):
                runtime.clear_events()
                st.rerun()

    if not events:
        st.caption("目前尚未有事件紀錄。")
        return

    for event in reversed(events[-20:]):
        _render_event(event)


def _render_event(event):
    event_type = event.get("type") or event.get("event_type", "event")
    payload = event.get("payload", {})
    timestamp = event.get("timestamp")

    with st.expander(f"{event_type}｜{timestamp or 'No timestamp'}"):
        st.json(payload)


def _safe_call(runtime, method_name, default=None):
    if not runtime:
        return default

    if not hasattr(runtime, method_name):
        return default

    try:
        return getattr(runtime, method_name)()
    except Exception:
        return default