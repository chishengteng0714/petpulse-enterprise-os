import streamlit as st

from components.base import BaseBadge, BaseCard


def ActionItem(
    title: str,
    description: str,
    owner: str = "Marketing Team",
    priority: str = "Medium",
    variant: str = "default",
):
    """
    PetPulse Business Component - ActionItem v2

    Enterprise Platform 2.0 原則：
    - 使用 BaseCard v2
    - 不使用 HTML
    - 用 Streamlit Native 呈現任務資訊
    """

    with BaseCard(
        eyebrow="Action Item",
        title=title,
        subtitle=description,
        variant=variant,
    ):
        col1, col2 = st.columns(2)

        with col1:
            st.caption("OWNER")
            st.write(owner)

        with col2:
            st.caption("PRIORITY")
            BaseBadge(priority, variant=variant)