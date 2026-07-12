import streamlit as st


def render_workspace_launcher(experience):
    """
    Workspace Launcher Golden Master

    呈現決策完成後的工作路徑導引。

    GM-07 Final Product Audit：
    - 強化主管閱讀語言
    - 統一卡片版型
    - 維持 Streamlit Native First
    - 不改變 Runtime Behavior
    """

    workspaces = getattr(experience, "workspaces", [])

    if not workspaces:
        _render_empty_workspace_state()
        return

    _render_decision_route(workspaces)
    _render_demo_route_note()


def _render_decision_route(workspaces):
    """
    呈現決策後的工作區導引。
    """

    st.markdown("### 決策後的工作路徑")
    st.caption("根據任務性質，選擇最適合的工作區繼續確認、分派與追蹤。")

    _render_micro_gap()

    columns = st.columns(len(workspaces))

    for index, workspace in enumerate(workspaces):
        with columns[index]:
            _render_route_card(index, workspace)


def _render_route_card(index, workspace):
    """
    呈現單一工作區導引卡片。
    """

    with st.container(border=True):
        st.caption(_get_step_label(index))
        st.markdown(f"#### {workspace.title}")

        target = getattr(workspace, "target", None)
        status = getattr(workspace, "status", None)
        description = getattr(workspace, "description", None)

        if description:
            st.write(description)

        if target:
            st.caption("適合處理")
            st.markdown(f"**{target}**")

        if status:
            st.caption("目前狀態")
            st.markdown(f"**{status}**")


def _render_demo_route_note():
    """
    呈現 Demo 工作路徑說明。
    """

    st.info(
        "首頁負責說清楚今日狀態與今日決策；後續執行由企業工作區、"
        "證據中心與深入調查室承接。"
    )


def _render_empty_workspace_state():
    """
    呈現沒有工作區資料時的空狀態。
    """

    st.info("目前尚未取得可顯示的工作區資料。")
    st.caption("請確認工作區設定是否已完成。")


def _get_step_label(index):
    """
    回傳工作路徑步驟標籤。
    """

    labels = [
        "步驟 1",
        "步驟 2",
        "步驟 3",
        "步驟 4",
    ]

    if index < len(labels):
        return labels[index]

    return f"步驟 {index + 1}"


def _render_micro_gap():
    st.markdown("")