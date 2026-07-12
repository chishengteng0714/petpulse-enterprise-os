import streamlit as st


def render_news_feed(news_df):
    st.subheader("📰 Latest News Feed")

    if news_df.empty:
        st.info("目前沒有新聞資料。")
        return

    display_columns = []

    for col in ["title", "source", "publisher", "published_at", "competitors", "url"]:
        if col in news_df.columns:
            display_columns.append(col)

    df = news_df[display_columns].head(50)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )