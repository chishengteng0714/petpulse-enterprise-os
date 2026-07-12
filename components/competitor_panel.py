import pandas as pd
import streamlit as st


def render_competitor_panel(data):
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    own_mentions = positive + neutral + negative

    competitors = pd.DataFrame([
        {
            "品牌": "PetPulse AI",
            "今日聲量": own_mentions,
            "品牌健康度": 84,
            "市場位置": "自有品牌"
        },
        {
            "品牌": "競品 A",
            "今日聲量": max(18, round(own_mentions * 0.82)),
            "品牌健康度": 78,
            "市場位置": "主要競品"
        },
        {
            "品牌": "競品 B",
            "今日聲量": max(14, round(own_mentions * 0.64)),
            "品牌健康度": 72,
            "市場位置": "成長競品"
        },
        {
            "品牌": "競品 C",
            "今日聲量": max(10, round(own_mentions * 0.48)),
            "品牌健康度": 69,
            "市場位置": "觀察名單"
        }
    ])

    with st.container(border=True):
        st.subheader("競品觀察面板")
        st.caption("AI 模擬市場聲量位置，用於作品集展示企業級競品監測架構。")
        st.dataframe(competitors, use_container_width=True, hide_index=True)

        leader = competitors.sort_values("今日聲量", ascending=False).iloc[0]["品牌"]

        if leader == "PetPulse AI":
            st.success("🟢 今日自有品牌聲量位居市場前段，具備內容放大機會。")
        else:
            st.warning(f"🟡 今日 {leader} 聲量較高，建議觀察其活動、促銷或社群內容。")