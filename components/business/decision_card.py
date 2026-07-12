import streamlit as st

from components.base import BaseBadge, BaseCard


def DecisionCard(
    title: str,
    description: str,
    status: str = "AI Decision",
    action: str | None = None,
    variant: str = "default",
    footer: str | None = None,
):
    """
    PetPulse Business Component - DecisionCard v2

    Enterprise Platform 2.0 原則：
    - 使用 BaseCard v2
    - 不使用 HTML action block
    - 全部改為 Streamlit Native
    """

    with BaseCard(
        eyebrow="Decision Signal",
        title=title,
        subtitle=description,
        variant=variant,
        footer=footer,
    ):
        BaseBadge(status, variant=variant)

        if action:
            st.write("")
            st.caption("RECOMMENDED ACTION")
            st.success(action)