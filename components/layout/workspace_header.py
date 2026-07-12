import streamlit as st


def render_workspace_header(workspace):
    """
    Workspace Header

    GM-09 Enterprise UI Polish:
    - 全中文化首頁第一屏
    - 強化 Enterprise OS 產品定位
    - 統一 KPI 語意
    - 不改 Runtime Behavior / Architecture
    """

    with st.container(border=True):
        st.caption("企業工作台")
        st.markdown(f"# {workspace.platform_name}")
        st.write(workspace.workspace_message)
        st.caption(
            f"{workspace.engine_name} · 最後產生時間 {workspace.generated_at}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "品牌健康度",
            workspace.health,
            workspace.health_delta,
        )

    with col2:
        st.metric(
            "今日焦點",
            workspace.today_focus,
        )

    with col3:
        st.metric(
            "優先層級",
            workspace.today_focus_priority,
        )