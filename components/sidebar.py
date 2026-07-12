import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.title("🐶 PetPulse AI")
        st.caption("企業級社群聲量智慧平台")

        st.divider()

        st.subheader("指揮中心")
        st.markdown("**總覽戰情室**")
        st.markdown("AI 決策中心")
        st.markdown("聲量分析")
        st.markdown("市場情報")
        st.markdown("風險預警")

        st.divider()

        st.subheader("系統狀態")
        st.success("爬蟲系統｜正常")
        st.success("AI 分析｜正常")
        st.success("資料庫｜正常")

        st.divider()
        st.caption("Enterprise Edition v2")