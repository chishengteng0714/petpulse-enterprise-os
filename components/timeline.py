import streamlit as st
from datetime import datetime


def render_ai_timeline(data):
    positive = data.get("positive", 0)
    neutral = data.get("neutral", 0)
    negative = data.get("negative", 0)

    total = positive + neutral + negative

    with st.container(border=True):
        st.subheader("AI 趨勢摘要時間線")
        st.caption("AI 將今日聲量變化整理成主管可快速閱讀的事件脈絡。")

        timeline = [
            {
                "time": "09:00",
                "title": "品牌聲量開始累積",
                "desc": f"今日累積監測聲量 {total} 筆，整體討論量維持穩定。"
            },
            {
                "time": "11:30",
                "title": "正向討論形成主軸",
                "desc": f"正向聲量目前為 {positive} 筆，主要集中於產品體驗與門市服務。"
            },
            {
                "time": "14:00",
                "title": "負向議題進入觀察",
                "desc": f"負向聲量目前為 {negative} 筆，建議持續追蹤價格、缺貨與客服相關討論。"
            },
            {
                "time": datetime.now().strftime("%H:%M"),
                "title": "AI 完成今日初步判讀",
                "desc": "建議優先放大正向口碑，同步建立客服快速回覆腳本。"
            }
        ]

        for item in timeline:
            st.markdown(f"**{item['time']}｜{item['title']}**")
            st.write(item["desc"])
            st.divider()