import streamlit as st

from components.base import BaseSection
from components.business import DecisionCard


def render_ai_insights(data: dict):
    """
    PetPulse AI Command Center

    將 AI 分析結果轉換成企業可讀的 Decision Signals。
    """

    summary = data.get("summary", "目前尚未取得 AI 分析摘要。")
    insights = data.get("insights", [])
    recommendations = data.get("recommendations", [])
    risks = data.get("risks", [])

    with BaseSection(
        eyebrow="AI Command Center",
        title="AI 決策中心",
        description="將即時輿情、品牌風險與行動建議整合成可判讀的企業決策訊號。",
    ):
        DecisionCard(
            title="今日品牌總結",
            description=summary,
            status="AI Summary",
            action="請優先檢查今日聲量是否出現異常波動，並確認是否需要更新社群回應策略。",
            variant="purple",
            footer="由 OpenAI Analyzer 根據最新 analysis.json 產生。",
        )

        col1, col2 = st.columns(2)

        with col1:
            if insights:
                for insight in insights[:3]:
                    DecisionCard(
                        title="關鍵洞察",
                        description=str(insight),
                        status="Insight",
                        action="可作為今日社群內容、客服溝通或品牌觀察的參考依據。",
                        variant="info",
                    )
            else:
                DecisionCard(
                    title="尚未偵測到明確洞察",
                    description="目前資料量不足，AI 尚未產生可判讀的關鍵洞察。",
                    status="No Signal",
                    action="請持續累積新聞與社群資料後再進行觀察。",
                    variant="default",
                )

        with col2:
            if risks:
                for risk in risks[:3]:
                    DecisionCard(
                        title="潛在風險",
                        description=str(risk),
                        status="Risk",
                        action="建議確認是否需要啟動客服回應、門市溝通或品牌聲明準備。",
                        variant="danger",
                    )
            else:
                DecisionCard(
                    title="目前未偵測高風險訊號",
                    description="AI 尚未發現需要立即處理的負面風險。",
                    status="Stable",
                    action="維持例行監測即可。",
                    variant="success",
                )

        if recommendations:
            st.markdown("")

            for recommendation in recommendations[:3]:
                DecisionCard(
                    title="AI 建議行動",
                    description=str(recommendation),
                    status="Recommended",
                    action="請評估是否轉換為今日社群任務或內部追蹤項目。",
                    variant="warning",
                )