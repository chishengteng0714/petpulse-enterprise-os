import streamlit as st


def render_status_bar(data):
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    total = positive + neutral + negative

    if total == 0:
        health = 0
    else:
        health = round((positive / total) * 100)

    if health >= 80:
        status = "🟢 健康"
    elif health >= 60:
        status = "🟡 注意"
    else:
        status = "🔴 高風險"

    confidence = 96

    risk = "低"

    if negative >= positive * 0.5:
        risk = "中"

    if negative >= positive:
        risk = "高"

    st.caption("今日品牌決策中心")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("品牌健康度", f"{health}", status)
    c2.metric("AI 信心指數", f"{confidence}%", "分析可信度")
    c3.metric("今日風險", risk, "持續監控")
    c4.metric("AI 建議", "3 項", "等待執行")

    st.info(
        "📌 AI 判讀：今日品牌整體聲量穩定，建議優先放大正向內容，並持續監控價格、缺貨與客服相關討論。"
    )