import streamlit as st

from components.base import BaseCard, BaseBadge


def FocusCard(
    title: str,
    status: str,
    summary: str,
    alert: str,
    action: str,
    confidence: int = 94,
    health_value: int | float = 84,
    negative_rate: int | float = 0,
    variant: str = "default",
):
    with BaseCard(
        eyebrow="AI Decision Layer",
        title=title,
        subtitle=summary,
        variant=variant,
    ):
        col1, col2, col3 = st.columns([1.2, 1, 1])

        with col1:
            BaseBadge(status, variant=variant)
            st.markdown("### 今日判斷")
            st.write(alert)

        with col2:
            st.metric("品牌健康度", health_value)
            st.metric("負向聲量", f"{negative_rate}%")

        with col3:
            st.metric("AI Confidence", f"{confidence}%")
            st.markdown("### 建議行動")
            st.write(action)