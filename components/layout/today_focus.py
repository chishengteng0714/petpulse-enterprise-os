import streamlit as st


def render_today_focus(workspace):
    """
    Today Focus

    GM-09 Enterprise UI Polish:
    - 全中文化
    - 強化資訊層級
    - 保持 Runtime Behavior 不變
    """

    st.subheader("🎯 今日焦點")

    priority = workspace.today_focus_priority

    priority_map = {
        "High": ("高", st.error),
        "Medium": ("中", st.warning),
        "Low": ("低", st.success),
    }

    priority_text, renderer = priority_map.get(
        priority,
        (priority, st.info),
    )

    renderer(f"優先層級：{priority_text}")

    st.markdown(f"### {workspace.today_focus}")

    st.write(workspace.today_focus_description)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "工作台狀態",
            workspace.workspace_status,
        )

    with col2:
        st.metric(
            "品牌健康度",
            workspace.health,
            workspace.health_delta,
        )