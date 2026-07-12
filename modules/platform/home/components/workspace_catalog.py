import streamlit as st


def render_workspace_catalog(summary):
    st.markdown("## 下一步去哪裡")
    st.caption("從今日企業營運中心進入對應工作區，接續完成證據檢視、調查、主管決策與平台觀測。")

    for index, workspace in enumerate(summary["workspaces"], start=1):
        _render_workspace_card(workspace, index)

    st.divider()


def _render_workspace_card(workspace, index):
    with st.container(border=True):
        name_col, status_col, action_col = st.columns([2.5, 1.2, 0.8])

        with name_col:
            if index == 1:
                st.caption("Recommended")
            else:
                st.caption("Workspace")

            st.markdown(f"### {workspace['name']}")
            st.write(workspace["purpose"])
            st.caption(f"下一步：{workspace['activity']}")

        with status_col:
            _render_status(workspace["status"])
            st.caption(f"Updated {workspace['last_updated']}")

        with action_col:
            st.button(
                workspace["action"],
                key=f"workspace_{workspace['id']}",
                use_container_width=True,
            )


def _render_status(status):
    if status == "Healthy":
        st.success("健康")
    elif status == "Active":
        st.info("進行中")
    elif status == "Ready":
        st.info("已就緒")
    elif status == "Needs Review":
        st.warning("需確認")
    else:
        st.caption(status)