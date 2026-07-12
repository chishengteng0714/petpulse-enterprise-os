import streamlit as st


def BaseBadge(
    label: str,
    variant: str = "default",
):
    """
    PetPulse Enterprise Design System

    BaseBadge

    GM-09 Enterprise UI Polish:
    - 移除過重的 st.status 視覺重量
    - 改為輕量級 Streamlit Native Badge
    - 保持 API 不變
    - 不改 Runtime Behavior / Architecture
    """

    icon_map = {
        "default": "🏷️",
        "info": "🔎",
        "success": "✅",
        "warning": "⚠️",
        "danger": "🚨",
        "purple": "🟣",
    }

    icon = icon_map.get(variant, "🏷️")

    st.caption(f"{icon} {label}")