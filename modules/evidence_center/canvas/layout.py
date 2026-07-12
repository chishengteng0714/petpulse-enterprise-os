import streamlit as st

from modules.evidence_center.canvas.graph_layer import render_graph_layer
from modules.evidence_center.canvas.timeline_layer import render_timeline_layer
from modules.evidence_center.canvas.inspector_layer import render_inspector_layer
from modules.evidence_center.canvas.notebook_layer import render_notebook_layer
from modules.evidence_center.canvas.decision_queue import render_decision_queue
from modules.evidence_center.canvas.ai_copilot import render_ai_copilot
from modules.evidence_center.canvas.event_log_layer import render_event_log_layer
from modules.evidence_center.canvas.relationship_map import render_relationship_map
from modules.evidence_center.canvas.toolbar import render_toolbar
from modules.evidence_center.canvas.statusbar import render_statusbar


def _is_panel_open(canvas_runtime, panel_name):
    panel_state = canvas_runtime.get_panel_state()
    return panel_state.get(panel_name, True)


def _render_closed_panel_notice(panel_name):
    st.info(f"{panel_name} panel is currently closed from Canvas Toolbar.")


def _render_graph_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "graph"):
        render_graph_layer(canvas_runtime)
    else:
        _render_closed_panel_notice("Graph")


def _render_timeline_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "timeline"):
        render_timeline_layer(canvas_runtime)
    else:
        _render_closed_panel_notice("Timeline")


def _render_inspector_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "inspector"):
        render_inspector_layer(canvas_runtime)
    else:
        _render_closed_panel_notice("Inspector")


def _render_notebook_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "notebook"):
        render_notebook_layer(canvas_runtime)
    else:
        _render_closed_panel_notice("Notebook")


def _render_decision_queue_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "decision_queue"):
        render_decision_queue(canvas_runtime)
    else:
        _render_closed_panel_notice("Decision Queue")


def _render_ai_copilot_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "ai_copilot"):
        render_ai_copilot(canvas_runtime)
    else:
        _render_closed_panel_notice("AI Copilot")


def _render_event_log_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "event_log"):
        render_event_log_layer(canvas_runtime)
    else:
        _render_closed_panel_notice("Event Log")


def _render_relationship_map_panel(canvas_runtime):
    if _is_panel_open(canvas_runtime, "relationship_map"):
        render_relationship_map(canvas_runtime)
    else:
        _render_closed_panel_notice("Relationship Map")


def _render_default_layout(canvas_runtime):
    left_col, center_col, right_col = st.columns([1.2, 2.2, 1.3])

    with left_col:
        _render_timeline_panel(canvas_runtime)
        st.divider()
        _render_decision_queue_panel(canvas_runtime)

    with center_col:
        _render_graph_panel(canvas_runtime)
        st.divider()
        _render_relationship_map_panel(canvas_runtime)

    with right_col:
        _render_inspector_panel(canvas_runtime)
        st.divider()
        _render_notebook_panel(canvas_runtime)
        st.divider()
        _render_ai_copilot_panel(canvas_runtime)


def _render_focus_layout(canvas_runtime):
    main_col, side_col = st.columns([3, 1.3])

    with main_col:
        _render_graph_panel(canvas_runtime)
        st.divider()
        _render_relationship_map_panel(canvas_runtime)

    with side_col:
        _render_inspector_panel(canvas_runtime)
        st.divider()
        _render_ai_copilot_panel(canvas_runtime)


def _render_split_layout(canvas_runtime):
    left_col, right_col = st.columns(2)

    with left_col:
        _render_graph_panel(canvas_runtime)
        st.divider()
        _render_timeline_panel(canvas_runtime)

    with right_col:
        _render_relationship_map_panel(canvas_runtime)
        st.divider()
        _render_inspector_panel(canvas_runtime)
        st.divider()
        _render_notebook_panel(canvas_runtime)
        st.divider()
        _render_decision_queue_panel(canvas_runtime)


def _render_analysis_layout(canvas_runtime):
    top_col1, top_col2 = st.columns([2, 1])

    with top_col1:
        _render_graph_panel(canvas_runtime)
        st.divider()
        _render_relationship_map_panel(canvas_runtime)

    with top_col2:
        _render_inspector_panel(canvas_runtime)

    st.divider()

    bottom_col1, bottom_col2 = st.columns(2)

    with bottom_col1:
        _render_notebook_panel(canvas_runtime)

    with bottom_col2:
        _render_ai_copilot_panel(canvas_runtime)


def _render_executive_layout(canvas_runtime):
    top_col1, top_col2 = st.columns([1.5, 1])

    with top_col1:
        _render_decision_queue_panel(canvas_runtime)

    with top_col2:
        _render_ai_copilot_panel(canvas_runtime)

    st.divider()

    _render_graph_panel(canvas_runtime)
    st.divider()
    _render_relationship_map_panel(canvas_runtime)


def _render_audit_layout(canvas_runtime):
    top_col1, top_col2 = st.columns([2, 1])

    with top_col1:
        _render_event_log_panel(canvas_runtime)

    with top_col2:
        _render_inspector_panel(canvas_runtime)
        st.divider()
        _render_ai_copilot_panel(canvas_runtime)


def render_canvas_layout(canvas_runtime):
    """
    Canvas Layout

    Step 21：
    Layout 接上 Relationship Map Layer。
    """

    render_toolbar(canvas_runtime)

    st.divider()

    layout_mode = canvas_runtime.get_layout_mode()

    if layout_mode == "focus":
        _render_focus_layout(canvas_runtime)
    elif layout_mode == "split":
        _render_split_layout(canvas_runtime)
    elif layout_mode == "analysis":
        _render_analysis_layout(canvas_runtime)
    elif layout_mode == "executive":
        _render_executive_layout(canvas_runtime)
    elif layout_mode == "audit":
        _render_audit_layout(canvas_runtime)
    else:
        _render_default_layout(canvas_runtime)

    render_statusbar(canvas_runtime)