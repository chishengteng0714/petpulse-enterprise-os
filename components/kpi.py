import streamlit as st

from components.base import BaseCard, BaseMetric


def _safe_delta(current: int | float, previous: int | float) -> str:
    """
    計算 KPI 與前一期的差異。
    """
    delta = current - previous

    if delta > 0:
        return f"+{delta}"
    if delta < 0:
        return str(delta)

    return "0"


def render_kpi_dashboard(data: dict, history):
    """
    PetPulse KPI Dashboard

    使用 PetPulse Design System：
    - BaseCard
    - BaseMetric
    - Streamlit Native columns
    """

    brand_health = data.get("brand_health", 0)
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    if history is not None and len(history) >= 2:
        previous_health = history.iloc[-2]["health"]
        health_delta = _safe_delta(brand_health, previous_health)
    else:
        health_delta = "0"

    total_mentions = positive + neutral + negative

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with BaseCard(
            eyebrow="Brand Health",
            title="品牌健康度",
            subtitle="AI 綜合判斷目前品牌聲量與情緒狀態。",
            variant="info",
        ):
            BaseMetric(
                label="Health Score",
                value=f"{brand_health}",
                delta=health_delta,
                help_text="根據近期正負聲量與 AI 風險判斷產生。",
            )

    with col2:
        with BaseCard(
            eyebrow="Positive",
            title="正向聲量",
            subtitle="代表市場中較有利的品牌討論。",
            variant="success",
        ):
            BaseMetric(
                label="Positive Mentions",
                value=positive,
                help_text="近期 AI 判定為正向的聲量數。",
            )

    with col3:
        with BaseCard(
            eyebrow="Neutral",
            title="中性聲量",
            subtitle="代表一般資訊、詢問或未明顯傾向的討論。",
            variant="default",
        ):
            BaseMetric(
                label="Neutral Mentions",
                value=neutral,
                help_text="近期 AI 判定為中性的聲量數。",
            )

    with col4:
        with BaseCard(
            eyebrow="Risk",
            title="負向聲量",
            subtitle="代表需要關注的抱怨、風險或潛在危機。",
            variant="danger",
        ):
            BaseMetric(
                label="Negative Mentions",
                value=negative,
                help_text="近期 AI 判定為負向的聲量數。",
            )

    with BaseCard(
        eyebrow="Total Signal",
        title="總聲量觀測",
        subtitle="所有正向、中性與負向訊號的總和。",
        variant="purple",
        footer="PetPulse AI 會持續追蹤聲量變化，協助判斷是否出現異常波動。",
    ):
        BaseMetric(
            label="Total Mentions",
            value=total_mentions,
            help_text="Positive + Neutral + Negative 的總和。",
        )