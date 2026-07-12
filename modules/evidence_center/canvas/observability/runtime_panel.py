import streamlit as st

from .session_panel import render_session_panel
from .ui_helpers import render_health_section, render_json_card


def render_runtime_panel(report):
    """
    Runtime Panel

    Canvas Runtime / Intelligence Runtime / Session 的觀測入口。
    """

    st.markdown("## Runtime Monitor")
    st.caption("Runtime, engine, session, and state visibility.")

    runtime_tab, engine_tab, session_tab = st.tabs(
        [
            "Canvas Runtime",
            "Intelligence Runtime",
            "Session",
        ]
    )

    with runtime_tab:
        render_health_section("Canvas Runtime Monitor", report.runtime_health)
        render_json_card("Runtime Snapshot", report.session_snapshot.get("runtime"))

    with engine_tab:
        render_health_section("Intelligence Runtime Monitor", report.engine_health)
        render_json_card("Context Snapshot", report.context_snapshot)

    with session_tab:
        render_session_panel(report)