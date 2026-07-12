import streamlit as st

from components.base import BaseCard, BaseSection, BaseBadge


def _build_action_queue(data):
    """
    Build Action Queue

    GM-09 Enterprise UI Polish:
    - 保持 Runtime Behavior 不變
    - 僅調整顯示文字
    """

    actions = data.get("actions", [])

    queue = []

    for index, action in enumerate(actions[:4], start=1):
        queue.append(
            {
                "title": f"建議任務 {index}",
                "description": str(action),
                "owner": "行銷團隊",
                "status": "待執行",
                "priority": "高" if index == 1 else "中",
                "variant": "warning" if index == 1 else "info",
            }
        )

    if not queue:
        queue.append(
            {
                "title": "維持例行監測",
                "description": (
                    "目前尚未偵測到需要立即執行的行動，"
                    "建議持續觀察品牌聲量與負向情緒變化。"
                ),
                "owner": "PetPulse AI",
                "status": "觀察中",
                "priority": "低",
                "variant": "success",
            }
        )

    return queue


def render_action_queue(data):
    """
    Action Queue

    GM-09 Enterprise UI Polish:
    - 全中文化
    - 強化主管執行管理語意
    - 不改 Runtime Behavior / Architecture
    """

    queue = _build_action_queue(data)

    with BaseSection(
        eyebrow="今日行動",
        title="今日行動佇列",
        description="將 AI 建議轉換為可追蹤、可分派與可執行的工作項目，協助團隊快速推進後續行動。",
    ):
        for item in queue:
            with BaseCard(
                eyebrow=item["status"],
                title=item["title"],
                subtitle=item["description"],
                variant=item["variant"],
            ):
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    st.caption("優先層級")
                    BaseBadge(
                        item["priority"],
                        variant=item["variant"],
                    )

                with col2:
                    st.caption("負責單位")
                    st.write(item["owner"])

                with col3:
                    st.caption("建議下一步")
                    st.write("確認內容後，安排任務分派或交由相關團隊執行。")