from contextlib import contextmanager

import streamlit as st


@contextmanager
def BaseCard(
    title: str | None = None,
    subtitle: str | None = None,
    eyebrow: str | None = None,
    footer: str | None = None,
    variant: str = "default",
):
    """
    PetPulse Enterprise Design System

    BaseCard

    GM-09 Enterprise UI Polish:
    - 統一卡片資訊層級
    - 強化卡片閱讀節奏
    - 保留 variant 參數，不改 Runtime Behavior
    - Streamlit Native Only
    """

    with st.container(border=True):
        if eyebrow:
            st.caption(eyebrow)

        if title:
            st.markdown(f"### {title}")

        if subtitle:
            st.caption(subtitle)

        st.markdown("")

        yield

        if footer:
            st.divider()
            st.caption(footer)