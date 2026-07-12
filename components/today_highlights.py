import streamlit as st


def render_today_highlights(data):
    """
    Today Highlights

    GM-08 Enterprise Design System v2：
    - 移除 HTML Card
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native
    - 保持 Runtime Behavior 不變
    """

    highlights = data.get("highlights", [])

    if not highlights:
        highlights = [
            "今日品牌聲量維持穩定，未偵測到重大異常波動。",
            "正向討論主要集中在產品體驗、服務品質與品牌信任感。",
            "負向討論仍需持續觀察，避免小型抱怨累積成聲譽風險。",
        ]

    with st.container(border=True):
        st.caption("Today Highlights")
        st.markdown("### 今日重點")

        for item in highlights:
            st.write(f"- {item}")