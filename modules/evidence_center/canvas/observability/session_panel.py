import streamlit as st

from .ui_helpers import format_bool, render_json_card


def render_session_panel(report):
    """
    Session Panel

    Runtime State Map:
    - Runtime
    - Session
    - State
    - Selection
    - Panel
    - Modes
    """

    st.markdown("## Session Inspector")
    st.caption("Runtime state map: Runtime / Session / State / Selection / Panel / Modes.")

    snapshot = report.session_snapshot

    runtime_tab, session_tab, state_tab, selection_tab, panel_tab, modes_tab, raw_tab = st.tabs(
        [
            "Runtime",
            "Session",
            "State",
            "Selection",
            "Panel",
            "Modes",
            "Raw",
        ]
    )

    with runtime_tab:
        _render_runtime_state(snapshot)

    with session_tab:
        _render_session_state(snapshot)

    with state_tab:
        _render_state(snapshot)

    with selection_tab:
        _render_selection_state(snapshot)

    with panel_tab:
        _render_panel_state(snapshot)

    with modes_tab:
        _render_modes(snapshot)

    with raw_tab:
        render_json_card("Raw Session Snapshot", snapshot)


def _render_runtime_state(snapshot):
    runtime_snapshot = snapshot.get("runtime", {})

    st.metric("Runtime Type", runtime_snapshot.get("runtime_type", "Unknown"))

    with st.expander("Runtime Attributes", expanded=False):
        st.json(runtime_snapshot.get("attributes", []))


def _render_session_state(snapshot):
    session_snapshot = snapshot.get("session", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Has Session", format_bool(session_snapshot.get("has_session")))

    with col2:
        st.metric("Session Type", session_snapshot.get("session_type") or "None")

    render_json_card("Session Snapshot", session_snapshot.get("snapshot"))


def _render_state(snapshot):
    state_snapshot = snapshot.get("state", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Has State", format_bool(state_snapshot.get("has_state")))

    with col2:
        st.metric("State Type", state_snapshot.get("state_type") or "None")

    render_json_card("State Snapshot", state_snapshot.get("snapshot"))


def _render_selection_state(snapshot):
    selection_snapshot = snapshot.get("selection", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Has Selection",
            format_bool(selection_snapshot.get("has_selection_state")),
        )

    with col2:
        st.metric(
            "Selection Type",
            selection_snapshot.get("selection_type") or "None",
        )

    render_json_card("Selection Snapshot", selection_snapshot.get("snapshot"))


def _render_panel_state(snapshot):
    panel_snapshot = snapshot.get("panel", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Has Panel State", format_bool(panel_snapshot.get("has_panel_state")))

    with col2:
        st.metric("Panel State Type", panel_snapshot.get("panel_state_type") or "None")

    render_json_card("Panel Snapshot", panel_snapshot.get("snapshot"))


def _render_modes(snapshot):
    modes_snapshot = snapshot.get("modes", {})

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Layout Mode", modes_snapshot.get("layout_mode") or "None")

    with col2:
        st.metric("View Mode", modes_snapshot.get("view_mode") or "None")

    render_json_card("Modes Snapshot", modes_snapshot)