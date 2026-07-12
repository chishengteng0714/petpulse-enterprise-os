import streamlit as st


def render_alert_center(data):
    positive = data.get("positive", 0)
    negative = data.get("negative", 0)
    neutral = data.get("neutral", 0)

    total = positive + negative + neutral

    if total == 0:
        negative_rate = 0
        positive_rate = 0
    else:
        negative_rate = round((negative / total) * 100, 1)
        positive_rate = round((positive / total) * 100, 1)

    alerts = []

    if negative_rate >= 30:
        alerts.append({
            "level": "high",
            "title": "負向聲量偏高",
            "message": f"目前負向聲量占比 {negative_rate}%，建議立即檢查客服、價格與缺貨相關討論。",
        })
    elif negative_rate >= 15:
        alerts.append({
            "level": "medium",
            "title": "負向討論需觀察",
            "message": f"目前負向聲量占比 {negative_rate}%，仍在可控範圍，但建議持續追蹤。",
        })
    else:
        alerts.append({
            "level": "low",
            "title": "品牌風險穩定",
            "message": f"目前負向聲量占比 {negative_rate}%，尚未偵測到明顯危機訊號。",
        })

    if positive_rate >= 45:
        alerts.append({
            "level": "opportunity",
            "title": "正向口碑可放大",
            "message": f"正向聲量占比 {positive_rate}%，建議擷取好評內容作為社群與會員溝通素材。",
        })

    alerts.append({
        "level": "medium",
        "title": "熱門議題需持續追蹤",
        "message": "飼料保存、寵物健康與門市體驗為今日主要討論議題，建議納入內容規劃與客服腳本。",
    })

    with st.container(border=True):
        st.subheader("風險預警中心")
        st.caption("AI 根據今日聲量結構與議題變化，整理需要關注的品牌訊號。")

        for alert in alerts:
            title = alert["title"]
            message = alert["message"]
            level = alert["level"]

            if level == "high":
                st.error(f"🔴 {title}｜{message}")
            elif level == "medium":
                st.warning(f"🟡 {title}｜{message}")
            elif level == "opportunity":
                st.success(f"🟢 {title}｜{message}")
            else:
                st.info(f"🔵 {title}｜{message}")