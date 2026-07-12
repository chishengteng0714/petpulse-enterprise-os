import streamlit as st


def render_ai_summary(runtime=None):
    """
    AI Summary Golden Master

    呈現今日企業摘要，協助主管快速掌握重點。

    GM-07 Final Product Audit：
    - 統一主管閱讀語言
    - 強化資訊閱讀順序
    - 維持 Presentation Only
    - 不改變 Runtime Behavior
    """

    summary = _get_ai_summary(runtime)

    st.markdown("## AI 今日摘要")
    st.caption("將今日企業訊號整理為可快速閱讀的決策摘要。")

    _render_micro_gap()

    with st.container(border=True):
        header_col, status_col = st.columns([3, 1])

        with header_col:
            st.caption("今日判讀")
            st.markdown("### 今日企業狀態穩定，建議聚焦 3 項決策。")
            st.write(summary["headline"])

        with status_col:
            st.caption("判斷信心")
            st.markdown("### 高")

    _render_micro_gap()

    left_col, right_col = st.columns([1.4, 1])

    with left_col:
        with st.container(border=True):
            st.caption("關鍵觀察")

            for index, takeaway in enumerate(summary["takeaways"], start=1):
                st.markdown(f"**{index}. {takeaway}**")

    with right_col:
        with st.container(border=True):
            st.caption("今日建議聚焦")
            st.write(summary["recommended_focus"])


def _get_ai_summary(runtime=None):
    """
    取得 AI 今日摘要。

    若 Runtime 提供摘要資料則優先使用，
    否則使用 Golden Master Demo 資料。

    不改變 Runtime Behavior。
    """

    fallback = _get_fallback_ai_summary()

    if runtime is None:
        return fallback

    if hasattr(runtime, "get_summary"):
        try:
            runtime_summary = runtime.get_summary()

            return {
                "headline": runtime_summary.get(
                    "ai_headline",
                    fallback["headline"],
                ),
                "takeaways": runtime_summary.get(
                    "ai_takeaways",
                    fallback["takeaways"],
                ),
                "recommended_focus": runtime_summary.get(
                    "ai_recommended_focus",
                    fallback["recommended_focus"],
                ),
            }
        except Exception:
            return fallback

    return fallback


def _get_fallback_ai_summary():
    """
    Golden Master Demo AI 摘要。
    """

    return {
        "headline": (
            "目前企業營運維持健康，品牌聲量、會員互動與活動表現皆保持穩定。"
            "今日建議優先確認會員成長活動、風險回應策略與成長機會的任務分派。"
        ),
        "takeaways": [
            "會員互動維持正向，具備活動加碼與內容測試條件。",
            "部分服務體驗討論需要提前管理，降低品牌風險。",
            "寵物保健與門市體驗具備短期成長潛力，適合轉成追蹤任務。",
        ],
        "recommended_focus": (
            "建議先完成今日決策，再依任務性質前往企業工作區、"
            "證據中心或深入調查室持續處理。"
        ),
    }


def _render_micro_gap():
    st.markdown("")