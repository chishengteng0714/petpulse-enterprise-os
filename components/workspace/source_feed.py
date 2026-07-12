import streamlit as st

from components.base import BaseSection, BaseCard, BaseBadge
from components.workspace.mappers import map_sources_to_intelligence_items


def _load_mock_sources():
    """
    Source Intelligence Raw Data

    目前先使用 mock data 模擬未來外部資料來源。
    注意：這裡是 raw data，不是 UI model。
    """

    return [
        {
            "platform": "Threads",
            "title": "網友討論寵物公園近期保健品活動",
            "summary": "多位飼主討論指定品牌買一送一活動，主要關注關節保健、腸胃保健與適口性。",
            "topic": "寵物保健品",
            "sentiment": "Positive",
            "engagement": 128,
            "published_at": "2026-07-03",
            "url": "https://www.threads.net/",
        },
        {
            "platform": "Facebook",
            "title": "社團分享寵物公園門市購物心得",
            "summary": "貼文提到門市人員推薦保健品組合，留言區出現價格、品牌與成分比較討論。",
            "topic": "門市體驗",
            "sentiment": "Neutral",
            "engagement": 86,
            "published_at": "2026-07-02",
            "url": "https://www.facebook.com/",
        },
        {
            "platform": "Instagram",
            "title": "飼主限動開箱寵物公園活動商品",
            "summary": "使用者分享購買保健品與零食的開箱照片，內容偏向生活化與推薦型曝光。",
            "topic": "開箱分享",
            "sentiment": "Positive",
            "engagement": 214,
            "published_at": "2026-07-02",
            "url": "https://www.instagram.com/",
        },
        {
            "platform": "PTT / Forum",
            "title": "論壇討論寵物保健品價格與通路差異",
            "summary": "討論集中在寵物公園、電商平台與其他連鎖通路的價格比較。",
            "topic": "價格比較",
            "sentiment": "Neutral",
            "engagement": 45,
            "published_at": "2026-07-01",
            "url": "https://www.ptt.cc/",
        },
        {
            "platform": "Dcard",
            "title": "新手飼主詢問寵物公園推薦商品",
            "summary": "留言中多數建議先從腸胃、皮膚與關節保健品開始挑選，並比較不同品牌評價。",
            "topic": "新手飼主",
            "sentiment": "Positive",
            "engagement": 73,
            "published_at": "2026-06-30",
            "url": "https://www.dcard.tw/",
        },
    ]


def render_source_feed(workspace):
    """
    Source Intelligence Feed

    GM-09 Enterprise UI Polish:
    - 強化證據來源語意
    - 統一欄位中文化
    - 不改 Runtime Behavior / Architecture
    """

    raw_sources = _load_mock_sources()
    source_items = map_sources_to_intelligence_items(raw_sources)

    with BaseSection(
        eyebrow="來源情報",
        title="來源情報清單",
        description="彙整 Facebook、Instagram、Threads、PTT、論壇等公開來源訊號，讓每個洞察都能回到原始證據。",
    ):
        for item in source_items:
            with BaseCard(
                eyebrow=item["platform"],
                title=item["title"],
                subtitle=item["description"],
                variant=item["variant"],
            ):
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1.4])

                with col1:
                    st.caption("主題")
                    st.write(item["topic"])

                with col2:
                    st.caption("情緒")
                    BaseBadge(item["sentiment"], variant=item["variant"])

                with col3:
                    st.caption("互動量")
                    st.write(item["engagement_label"])

                with col4:
                    st.caption("發布時間")
                    st.write(item["published_at"])

                if item["url"]:
                    st.link_button("開啟原始連結", item["url"])
                else:
                    st.caption("尚未提供原始連結")