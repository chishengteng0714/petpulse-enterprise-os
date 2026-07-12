import streamlit as st

from components.workspace.engine import build_workspace_context
from components.layout.workspace_header import render_workspace_header
from components.layout.today_focus import render_today_focus
from components.workspace import (
    render_ai_inbox,
    render_priority_queue,
    render_recent_signals,
    render_action_queue,
    render_competitor_feed,
)


def render_overview_workspace(data, history, health_metrics, sentiment_metrics):
    """
    PetPulse Enterprise Workspace

    單一 Workspace 入口。
    app.py 只負責載入資料與呼叫這個函式；
    Workspace 的產品邏輯、模組順序與資料脈絡都從這裡開始。
    """

    workspace_context = build_workspace_context(data)

    render_workspace_header(health_metrics, sentiment_metrics, data)

    with st.expander("Workspace Context Debug", expanded=False):
        st.json(workspace_context)

    st.write("")

    render_today_focus(workspace_context)

    st.write("")

    col1, col2 = st.columns([1, 1])

    with col1:
        render_ai_inbox(data)

    with col2:
        render_priority_queue(data)

    st.write("")

    col3, col4 = st.columns([1, 1])

    with col3:
        render_recent_signals(data)

    with col4:
        render_action_queue(data)

    st.write("")

    render_competitor_feed(data)