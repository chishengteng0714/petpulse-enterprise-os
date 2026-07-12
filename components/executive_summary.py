import streamlit as st


def render_executive_summary(data):
    """
    Executive Summary

    GM-08 Enterprise Design System v2：
    - 移除 HTML Card
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native
    - 保持 Runtime Behavior 不變
    """

    summary = data.get("executive_summary", "")

    if not summary:
        summary = (
            "今日品牌整體聲量表現穩定，正向情緒仍為主要討論基調。"
            "消費者關注重點集中於產品品質、寵物健康與門市服務體驗。"
            "建議企業持續追蹤負向聲量來源，並針對高頻議題建立回應策略。"
        )

    with st.container(border=True):
        st.caption("Strategic Intelligence Brief")
        st.markdown("### 策略摘要")
        st.write(summary)