import pandas as pd
import streamlit as st


def render_action_center(data):
    positive = data.get("positive", 0)
    negative = data.get("negative", 0)
    neutral = data.get("neutral", 0)

    total = positive + negative + neutral

    if total == 0:
        positive_rate = 0
        negative_rate = 0
    else:
        positive_rate = round((positive / total) * 100, 1)
        negative_rate = round((negative / total) * 100, 1)

    actions = []

    if positive_rate >= 40:
        actions.append({
            "優先級": "高",
            "建議行動": "放大正向口碑內容",
            "負責單位": "社群行銷",
            "預期效果": "提升互動率與品牌信任感"
        })

    if negative_rate >= 15:
        actions.append({
            "優先級": "高",
            "建議行動": "建立客服快速回覆腳本",
            "負責單位": "客服 / 社群",
            "預期效果": "降低負向聲量擴散"
        })

    actions.append({
        "優先級": "中",
        "建議行動": "規劃夏季毛孩照護貼文",
        "負責單位": "內容行銷",
        "預期效果": "承接熱門議題，提高內容相關性"
    })

    actions.append({
        "優先級": "中",
        "建議行動": "整理熱門議題週報",
        "負責單位": "品牌 / PM",
        "預期效果": "提供商品與活動規劃依據"
    })

    df = pd.DataFrame(actions)

    with st.container(border=True):
        st.subheader("AI 行動建議中心")
        st.caption("AI 將聲量訊號轉換為今日可執行的品牌營運任務。")
        st.dataframe(df, use_container_width=True, hide_index=True)