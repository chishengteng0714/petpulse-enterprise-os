import streamlit as st


def render_footer():
    """
    Footer

    GM-08 Enterprise Design System v2：
    - 移除 HTML Footer
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native
    - 保持 Runtime Behavior 不變
    """

    st.divider()

    st.caption(
        "PetPulse AI｜Enterprise-grade AI Social Listening Platform｜"
        "Built for portfolio-ready product demonstration."
    )