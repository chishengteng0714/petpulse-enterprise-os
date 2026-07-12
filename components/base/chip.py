import streamlit as st


def BaseChip(
    label: str,
    variant: str = "default",
):
    """
    PetPulse Enterprise Design System

    BaseChip

    GM-09 Enterprise UI Polish

    Responsibilities
    ----------------
    - 提供輕量級資訊標籤
    - 保持與 BaseBadge 一致的設計語言
    - 保留 variant API
    - 不改變 Runtime Behavior
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