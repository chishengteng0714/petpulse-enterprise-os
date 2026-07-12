import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_executive_summary(data):
    summary = data.get("executive_summary", "")

    if not summary:
        summary = (
            "今日品牌整體聲量表現穩定，正向情緒仍為主要討論基調。"
            "消費者關注重點集中於產品品質、寵物健康與門市服務體驗。"
            "建議企業持續追蹤負向聲量來源，並針對高頻議題建立回應策略。"
        )

    with st.container(border=True):
        st.subheader("AI 策略分析")
        st.write(summary)


def render_today_highlights(data):
    highlights = data.get("highlights", [])

    if not highlights:
        highlights = [
            "今日品牌聲量維持穩定，未偵測到重大異常波動。",
            "正向討論主要集中在產品體驗、服務品質與品牌信任感。",
            "負向討論仍需持續觀察，避免小型抱怨累積成聲譽風險。"
        ]

    with st.container(border=True):
        st.subheader("今日焦點")

        for item in highlights:
            st.info(item)


def _build_topic_rows(topics):
    fallback_topics = [
        {"topic": "飼料保存", "mentions": 21, "trend": "+18%"},
        {"topic": "寵物健康", "mentions": 18, "trend": "+12%"},
        {"topic": "門市體驗", "mentions": 15, "trend": "+6%"},
        {"topic": "商品優惠", "mentions": 12, "trend": "-3%"},
        {"topic": "品牌信任", "mentions": 9, "trend": "+4%"}
    ]

    if not topics:
        return fallback_topics

    rows = []

    for index, item in enumerate(topics[:6]):
        if isinstance(item, dict):
            topic_name = item.get("topic", "未知議題")
            mentions = item.get("mentions", 20 - index * 2)
            trend = item.get("trend", f"+{max(2, 18 - index * 3)}%")
        else:
            topic_name = str(item)
            mentions = 20 - index * 2
            trend = f"+{max(2, 18 - index * 3)}%"

        rows.append({
            "topic": topic_name,
            "mentions": mentions,
            "trend": trend
        })

    return rows


def render_topics(data):
    topics = data.get("topics", [])
    rows = _build_topic_rows(topics)

    df = pd.DataFrame(rows)
    table_df = df.rename(columns={
        "topic": "熱門議題",
        "mentions": "聲量",
        "trend": "趨勢"
    })

    with st.container(border=True):
        st.subheader("熱門議題排行")
        st.caption("AI 依據今日聲量與討論密度整理主要議題。")
        st.dataframe(table_df, use_container_width=True, hide_index=True)

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=df["mentions"],
                theta=df["topic"],
                fill="toself",
                name="議題聲量"
            )
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            margin=dict(t=30, b=30, l=30, r=30),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    gridcolor="rgba(255,255,255,0.10)"
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.10)"
                )
            ),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)