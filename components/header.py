import streamlit as st
from datetime import datetime


def render_header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    left, right = st.columns([4, 1.2], gap="large")

    with left:
        st.caption("企業級 AI 社群聲量指揮中心")
        st.title("🐶 PetPulse AI")
        st.write("以 AI 即時掌握品牌聲量、風險預警與決策洞察")

    with right:
        st.success("● 即時監測中")
        st.caption(f"最後更新：{now}")

    st.divider()