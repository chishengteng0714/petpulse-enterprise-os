import streamlit as st

from components.workspace.engine import build_workspace_context
from components.workspace.state import WorkspaceStore
from components.layout.workspace_header import render_workspace_header
from components.layout.today_focus import render_today_focus
from components.workspace.ai_inbox import render_ai_inbox
from components.workspace.priority_queue import render_priority_queue
from components.workspace.recent_signals import render_recent_signals
from components.workspace.action_queue import render_action_queue
from components.workspace.competitor_feed import render_competitor_feed
from components.workspace.source_feed import render_source_feed


def render_workspace_context_debug(workspace):
    """
    Workspace Store Debug

    保留既有 Debug 能力。
    GM-09 不改 Runtime Behavior。
    """

    with st.expander("Workspace Store Debug", expanded=False):
        st.json(workspace.to_debug_dict())


def render_overview_workspace(data, history):
    """
    Enterprise Overview Workspace

    GM-09 Enterprise UI Polish:
    - 不改資料流
    - 不改元件責任
    - 不新增功能
    - 只優化首頁閱讀節奏與資訊層級
    """

    workspace_context = build_workspace_context(
        data=data,
        history=history,
    )

    workspace = WorkspaceStore(workspace_context)

    render_workspace_header(workspace)

    render_workspace_context_debug(workspace)

    st.divider()

    render_today_focus(workspace)

    st.divider()

    render_ai_inbox(workspace)

    st.divider()

    render_priority_queue(workspace)

    st.divider()

    render_recent_signals(workspace)

    st.divider()

    render_source_feed(workspace)

    st.divider()

    render_action_queue(workspace_context)

    st.divider()

    render_competitor_feed(workspace_context)