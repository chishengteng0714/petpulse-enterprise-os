from contextlib import contextmanager

import streamlit as st


@contextmanager
def BaseSection(
    title: str,
    description: str | None = None,
    eyebrow: str | None = None,
):
    """
    PetPulse Enterprise Design System

    BaseSection

    GM-09 Enterprise UI Polish

    Responsibilities
    ----------------
    - 統一全站 Section Header
    - 建立 Enterprise Information Hierarchy
    - 建立一致的閱讀節奏
    - 不改變 Runtime Behavior
    """

    st.container()

    if eyebrow:
        st.caption(eyebrow)

    st.markdown(f"## {title}")

    if description:
        st.caption(description)

    st.markdown("")

    yield

    st.divider()

    st.markdown("")