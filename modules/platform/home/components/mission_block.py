from datetime import datetime

import streamlit as st


def render_mission_block(summary):
    current_time = datetime.now().strftime("%H:%M")

    st.markdown("# 今日企業營運中心")
    st.caption("Enterprise Mission｜今日任務、決策、機會與工作入口。")

    st.divider()

    top_col, status_col = st.columns([2.5, 1])

    with top_col:
        st.caption(f"今日任務 · {summary['today_label']} · {current_time}")
        st.markdown(f"## {summary['mission_title']}")
        st.write(summary["mission_context"])

        action_col, note_col = st.columns([1, 2])

        with action_col:
            st.button(
                summary["primary_action"],
                key="mission_primary_action",
                use_container_width=True,
            )

        with note_col:
            st.caption(f"下一步：{summary['mission_next_step']}")

    with status_col:
        st.metric(
            "Enterprise Health",
            summary["enterprise_health"],
            summary["health_delta"],
        )

        _render_attention(summary["attention_level"])

        st.caption(f"Brief updated {summary['last_updated']}")

    st.divider()


def _render_attention(level):
    if level == "Action Required":
        st.error("需要行動")
    elif level == "Review":
        st.warning("需要確認")
    else:
        st.success("狀態穩定")