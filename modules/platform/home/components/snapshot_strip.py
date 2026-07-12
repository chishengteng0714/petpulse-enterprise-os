import streamlit as st


def render_snapshot_strip(summary):
    st.markdown("## 今日企業概況")
    st.caption("將今日訊號、決策、風險、成長機會與 AI 信心值整理成主管可快速判讀的營運概況。")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("今日訊號", summary["signals_today"], summary["signals_delta"])
        st.caption("Signals")

    with col2:
        st.metric("待決策", summary["decision_count"])
        st.caption("Decisions")

    with col3:
        st.metric("高風險", summary["high_risk_count"])
        st.caption("High Risk")

    with col4:
        st.metric("成長機會", summary["growth_count"])
        st.caption("Growth")

    with col5:
        st.metric("AI 信心值", summary["operating_confidence"])
        st.caption("Confidence")

    st.divider()