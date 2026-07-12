import streamlit as st


def BaseMetric(
    label: str,
    value: str | int | float,
    delta: str | int | float | None = None,
    help_text: str | None = None,
):
    """
    PetPulse Enterprise Design System

    BaseMetric

    GM-09 Enterprise UI Polish

    Responsibilities
    ----------------
    - 統一全站 KPI 元件
    - 封裝 Streamlit Native st.metric
    - 保持一致 API
    - 不加入任何商業邏輯
    - 不改變 Runtime Behavior
    """

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text,
    )