import plotly.graph_objects as go
import streamlit as st


def render_voice_funnel(data):
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    total = positive + neutral + negative
    meaningful = positive + negative
    advocacy = positive
    content_ready = round(positive * 0.65)

    with st.container(border=True):
        st.subheader("品牌聲量漏斗")
        st.caption("AI 將今日聲量拆解為可追蹤、可判讀、可行動的品牌資產。")

        fig = go.Figure(
            go.Funnel(
                y=[
                    "總聲量",
                    "有效討論",
                    "正向口碑",
                    "可轉換內容"
                ],
                x=[
                    total,
                    meaningful,
                    advocacy,
                    content_ready
                ],
                textinfo="value+percent initial"
            )
        )

        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(fig, use_container_width=True)