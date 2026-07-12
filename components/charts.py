import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_charts(data, history):
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    sentiment_df = pd.DataFrame({
        "情緒類型": ["正向", "中立", "負向"],
        "聲量": [positive, neutral, negative]
    })

    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("聲量情緒分布")
            st.caption("AI 依據今日社群內容判讀品牌討論情緒結構。")

            fig = px.pie(
                sentiment_df,
                names="情緒類型",
                values="聲量",
                hole=0.55
            )

            fig.update_layout(
                height=360,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E5E7EB"),
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.18,
                    xanchor="center",
                    x=0.5
                )
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container(border=True):
            st.subheader("品牌健康度趨勢")
            st.caption("透過每日健康度與 7 日平均線，觀察品牌聲量是否穩定成長。")

            if len(history) > 0 and {"date", "health"}.issubset(history.columns):
                chart_df = history.copy()
                chart_df["七日平均"] = (
                    chart_df["health"]
                    .rolling(window=7, min_periods=1)
                    .mean()
                    .round(1)
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=chart_df["date"],
                        y=chart_df["health"],
                        mode="lines+markers",
                        name="每日品牌健康度"
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=chart_df["date"],
                        y=chart_df["七日平均"],
                        mode="lines",
                        name="7 日平均線"
                    )
                )

                fig.update_layout(
                    height=360,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#E5E7EB"),
                    margin=dict(t=20, b=20, l=20, r=20),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.22,
                        xanchor="center",
                        x=0.5
                    ),
                    xaxis=dict(
                        title="日期",
                        gridcolor="rgba(255,255,255,0.08)"
                    ),
                    yaxis=dict(
                        title="品牌健康度",
                        gridcolor="rgba(255,255,255,0.08)"
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("目前尚無品牌健康度歷史資料。")