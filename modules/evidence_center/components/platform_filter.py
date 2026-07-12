import streamlit as st

from modules.evidence_center.domain import EvidenceItem


def _format_value(value):
    """
    將 Evidence 欄位安全轉成可顯示文字。
    """

    if value is None:
        return "未知"

    if hasattr(value, "value"):
        return str(value.value)

    clean_value = str(value).strip()

    if not clean_value:
        return "未知"

    return clean_value


def render_platform_filter(
    evidence_items: list[EvidenceItem],
) -> str:
    """
    Platform Filter

    Evidence Center 平台篩選元件。

    GM-06 Final Product Audit：
    - 不新增功能
    - 不改變 Architecture
    - 保留既有平台篩選責任
    - 強化中文產品語言與可讀性
    """

    evidence_items = evidence_items or []

    platforms = sorted(
        {
            _format_value(item.platform)
            for item in evidence_items
        }
    )

    options = ["全部", *platforms]

    return st.selectbox(
        "資料來源",
        options,
        index=0,
        help="選擇欲檢視的公開資料來源。",
    )