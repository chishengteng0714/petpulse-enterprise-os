import streamlit as st

from components.base import BaseSection, BaseCard, BaseBadge


def render_recent_signals(workspace):
    """
    Recent Signals

    GM-09 Enterprise UI Polish:
    - 全中文化
    - 強化市場觀察語意
    - 不改 Runtime Behavior / Architecture
    """

    signals = workspace.recent_signals

    with BaseSection(
        eyebrow="近期觀察",
        title=f"近期訊號：{workspace.signal_count} 個新觀察",
        description="整理近期由 AI 偵測到的市場、品牌與消費者討論主題，協助團隊判斷是否需要追蹤。",
    ):
        if not signals:
            st.info("目前沒有新的市場訊號。")
            return

        for signal in signals[:6]:
            with BaseCard(
                eyebrow=signal.get("source", "訊號來源"),
                title=signal.get("title", "未命名訊號"),
                subtitle=signal.get("description", "尚無訊號說明。"),
                variant="default",
            ):
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.caption("訊號狀態")
                    BaseBadge(
                        signal.get("status", "新訊號"),
                        variant="default",
                    )

                with col2:
                    st.caption("建議處理方式")
                    st.write("持續觀察此訊號是否轉變為風險、決策事項或成長機會。")