import streamlit as st

from components.base import BaseSection, BaseCard, BaseBadge


def render_priority_queue(workspace):
    """
    Decision Priority Queue

    GM-09 Enterprise UI Polish:
    - 全中文化
    - 強化主管決策排序語意
    - 不改 Runtime Behavior / Architecture
    """

    queue = workspace.priority_queue

    with BaseSection(
        eyebrow="決策排序",
        title="決策優先佇列",
        description="依據 AI 評估結果排序，協助主管先處理最值得確認的決策事項。",
    ):
        if not queue:
            st.info("目前沒有需要優先處理的決策。")
            return

        for index, item in enumerate(queue, start=1):
            with BaseCard(
                eyebrow=f"優先事項 #{index}",
                title=item.get("title", "未命名決策"),
                subtitle=item.get("description", ""),
                variant=item.get("variant", "default"),
            ):
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.caption("優先層級")
                    BaseBadge(
                        item.get("priority", "低"),
                        variant=item.get("variant", "default"),
                    )

                with col2:
                    st.caption("決策狀態")
                    st.write("等待確認")