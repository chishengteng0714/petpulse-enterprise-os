import streamlit as st


def render_decision_list(summary):
    st.markdown("## 今日決策清單")
    st.caption("系統已依照風險急迫性與行動價值排序，主管可由上而下完成今日最重要的三項決策。")

    for index, item in enumerate(summary["decisions"][:3], start=1):
        _render_decision_item(item, index)

    st.divider()


def _render_decision_item(item, index):
    with st.container(border=True):
        level_col, content_col, action_col = st.columns([0.8, 3.2, 0.9])

        with level_col:
            st.markdown(f"### P{index}")
            _render_level(item["level"])

        with content_col:
            st.markdown(f"### {item['title']}")
            st.write(item["signal"])
            st.caption(f"Owner：{item['owner']} · Due：{item['due']}")

        with action_col:
            st.button(
                item["action"],
                key=f"decision_{item['id']}",
                use_container_width=True,
            )


def _render_level(level):
    if level == "High":
        st.error("高優先")
    elif level == "Medium":
        st.warning("中優先")
    else:
        st.info("一般")