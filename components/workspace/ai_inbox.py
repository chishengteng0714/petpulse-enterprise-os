import streamlit as st

from components.base import BaseSection, BaseCard, BaseBadge


def render_ai_inbox(workspace):
    """
    AI Inbox

    GM-09 Enterprise UI Polish:
    - 全中文化
    - 強化決策收件匣語意
    - 統一 KPI 命名
    - 不改 Runtime Behavior / Architecture
    """

    inbox_items = workspace.ai_inbox

    with BaseSection(
        eyebrow="決策收件匣",
        title=f"AI 收件匣：{workspace.inbox_count} 個待確認訊號",
        description=(
            "將風險、建議與洞察整理成主管可快速判讀的決策收件匣，"
            "協助團隊優先處理真正需要確認的訊號。"
        ),
    ):
        if not inbox_items:
            st.info("目前沒有待確認的 AI 訊號。")
            return

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("訊號總數", workspace.inbox_count)

        with col2:
            st.metric("高優先訊號", workspace.high_priority_count)

        with col3:
            st.metric("待處理行動", workspace.pending_action_count)

        st.divider()

        for item in inbox_items[:5]:
            with BaseCard(
                eyebrow=item.get("type", "訊號"),
                title=item.get("title", "未命名訊號"),
                subtitle=item.get("description", "尚無訊號說明。"),
                variant=item.get("variant", "default"),
            ):
                col_a, col_b, col_c = st.columns([1, 1, 2])

                with col_a:
                    st.caption("優先層級")
                    BaseBadge(
                        item.get("priority", "低"),
                        variant=item.get("variant", "default"),
                    )

                with col_b:
                    st.caption("來源")
                    st.write(item.get("source", "AI 分析引擎"))

                with col_c:
                    st.caption("建議下一步")
                    st.write("確認內容後，決定是否加入行動佇列。")