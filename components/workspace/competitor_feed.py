import streamlit as st

from components.base import BaseCard, BaseSection, BaseBadge


def _build_competitor_feed(data):
    """
    Build Competitor Feed

    GM-09 Enterprise UI Polish:
    - 全中文化顯示語意
    - 不改 Runtime Behavior / Architecture
    """

    competitors = data.get("competitors", [])

    feed = []

    for index, competitor in enumerate(competitors[:5], start=1):
        feed.append(
            {
                "title": f"競品訊號 {index}",
                "description": str(competitor),
                "source": "競品監測",
                "impact": "中" if index <= 2 else "低",
                "variant": "purple" if index <= 2 else "info",
            }
        )

    if not feed:
        feed.append(
            {
                "title": "尚無重大競品訊號",
                "description": "目前 AI 尚未偵測到需要立即追蹤的競品動態。",
                "source": "PetPulse AI",
                "impact": "低",
                "variant": "success",
            }
        )

    return feed


def render_competitor_feed(data):
    """
    Competitor Feed

    GM-09 Enterprise UI Polish:
    - 強化競品觀察語意
    - 統一中文欄位
    - 不改 Runtime Behavior / Architecture
    """

    feed = _build_competitor_feed(data)

    with BaseSection(
        eyebrow="競品觀察",
        title="競品動態摘要",
        description="整理近期值得追蹤的競品訊號，協助判斷是否需要調整行銷、客服或通路應對策略。",
    ):
        for item in feed:
            with BaseCard(
                eyebrow=item["source"],
                title=item["title"],
                subtitle=item["description"],
                variant=item["variant"],
            ):
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    st.caption("影響層級")
                    BaseBadge(
                        item["impact"],
                        variant=item["variant"],
                    )

                with col2:
                    st.caption("訊號來源")
                    st.write(item["source"])

                with col3:
                    st.caption("建議觀察")
                    st.write("持續追蹤競品活動是否造成品牌聲量、情緒或門市討論變化。")