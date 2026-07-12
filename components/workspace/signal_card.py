import streamlit as st

from components.base import BaseBadge, BaseCard


def render_signal_card(
    eyebrow: str,
    title: str,
    description: str,
    badge_text: str,
    status: str,
    source: str,
    next_step: str,
    variant: str = "default",
):
    with BaseCard(
        eyebrow=eyebrow,
        title=title,
        subtitle=description,
        variant=variant,
    ):
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            BaseBadge(badge_text, variant=variant)

        with col2:
            st.caption("狀態")
            st.write(status)

        with col3:
            st.caption("建議下一步")
            st.write(next_step)

        st.caption(f"來源：{source}")