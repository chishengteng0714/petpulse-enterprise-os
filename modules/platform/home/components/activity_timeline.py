import streamlit as st


def render_activity_timeline(summary):
    st.markdown("## 近期更新")
    st.caption("最近 24 小時的重要系統與情報更新，協助主管理解今日判讀依據如何被整理與推進。")

    for item in summary["activities"]:
        with st.container(border=True):
            time_col, content_col = st.columns([0.7, 4])

            with time_col:
                st.caption(item["time"])

            with content_col:
                st.markdown(f"### {item['title']}")
                st.write(item["detail"])