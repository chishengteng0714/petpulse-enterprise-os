import streamlit as st


def render_topics(data):
    """
    Topics

    GM-08 Enterprise Design System v2：
    - 移除 HTML Card
    - 移除 Topic Pill HTML
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native Components
    - 保持 Runtime Behavior 不變
    """

    topics = data.get("topics", [])

    if not topics:
        topics = [
            "飼料保存",
            "寵物健康",
            "門市體驗",
            "商品優惠",
            "品牌信任",
        ]

    with st.container(border=True):
        st.caption("Hot Topics")
        st.markdown("### 熱門議題")
        st.caption("High-frequency discussion clusters detected by AI analyzer.")

        for topic in topics:
            if isinstance(topic, dict):
                topic_name = topic.get("topic", "Unknown")
            else:
                topic_name = str(topic)

            st.write(f"• #{topic_name}")