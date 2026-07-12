import streamlit as st

from modules.evidence_center.investigation_state import InvestigationState


def render_investigation_toolbar(
    platforms: list[str],
    topics: list[str],
    sentiments: list[str],
) -> InvestigationState:
    """
    Investigation Toolbar

    GM-10 Enterprise Presentation Rewrite：
    - Presentation Layer Only
    - 不修改 InvestigationState
    - 不修改查詢邏輯
    - 保留既有回傳格式
    - 改為 Enterprise Filter Bar
    """

    _inject_toolbar_style()
    _render_toolbar_header()

    with st.container():
        st.markdown('<section class="pp-investigation-toolbar">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1.1, 1.1, 1.1, 1.7])

        with col1:
            platform = st.selectbox(
                "資料平台",
                _normalize_options(platforms),
                index=0,
                key="investigation_platform",
            )

        with col2:
            topic = st.selectbox(
                "討論議題",
                _normalize_options(topics),
                index=0,
                key="investigation_topic",
            )

        with col3:
            sentiment = st.selectbox(
                "情緒狀態",
                _normalize_options(sentiments),
                index=0,
                key="investigation_sentiment",
            )

        with col4:
            keyword = st.text_input(
                "關鍵字搜尋",
                value="",
                placeholder="輸入品牌、議題、留言內容或作者",
                key="investigation_keyword",
            )

        sort_by = st.selectbox(
            "排序方式",
            ["最新優先", "互動最高", "情緒風險優先"],
            index=0,
            key="investigation_sort_by",
        )

        st.markdown("</section>", unsafe_allow_html=True)

    _render_toolbar_summary(platform, topic, sentiment, keyword, sort_by)

    return InvestigationState(
        platform=platform,
        topic=topic,
        sentiment=sentiment,
        keyword=keyword,
        sort_by=sort_by,
    )


def _render_toolbar_header():
    st.markdown(
        """
        <section class="pp-investigation-header">
            <div class="pp-investigation-header-icon">
                <span>查</span>
            </div>
            <div>
                <div class="pp-investigation-eyebrow">查詢工具</div>
                <h2>篩選公開證據</h2>
                <p>
                    依平台、議題、情緒與關鍵字快速收斂證據範圍，
                    讓主管能在最短時間完成判斷與追溯。
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_toolbar_summary(platform, topic, sentiment, keyword, sort_by):
    keyword_text = keyword.strip() if keyword else "未輸入"

    st.markdown(
        f"""
        <section class="pp-investigation-summary">
            <div class="pp-investigation-chip">
                <span>平台</span>
                <strong>{_safe_text(platform)}</strong>
            </div>
            <div class="pp-investigation-chip">
                <span>議題</span>
                <strong>{_safe_text(topic)}</strong>
            </div>
            <div class="pp-investigation-chip">
                <span>情緒</span>
                <strong>{_safe_text(sentiment)}</strong>
            </div>
            <div class="pp-investigation-chip">
                <span>關鍵字</span>
                <strong>{_safe_text(keyword_text)}</strong>
            </div>
            <div class="pp-investigation-chip">
                <span>排序</span>
                <strong>{_safe_text(sort_by)}</strong>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _normalize_options(options: list[str]) -> list[str]:
    normalized = ["全部"]

    for option in options or []:
        if option is None:
            continue

        value = _format_option(option)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


def _format_option(value):
    if hasattr(value, "value"):
        value = value.value

    text = str(value)

    option_map = {
        "Facebook": "Facebook",
        "Instagram": "Instagram",
        "Threads": "Threads",
        "PTT": "PTT",
        "Dcard": "Dcard",
        "Forum": "論壇",
        "Google Review": "Google 評論",
        "News": "新聞",
        "Blog": "部落格",
        "Positive": "正向",
        "Neutral": "中立",
        "Negative": "負向",
        "positive": "正向",
        "neutral": "中立",
        "negative": "負向",
    }

    return option_map.get(text, text)


def _safe_text(value):
    if value is None:
        return ""

    if hasattr(value, "value"):
        value = value.value

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _inject_toolbar_style():
    st.markdown(
        """
        <style>
            .pp-investigation-header {
                display: flex;
                align-items: center;
                gap: 18px;
                padding: 24px 26px;
                margin: 12px 0 18px 0;
                background:
                    radial-gradient(circle at top left, rgba(194, 168, 111, 0.16), transparent 34%),
                    linear-gradient(135deg, #FFFFFF 0%, #FBF8F1 100%);
                border: 1px solid rgba(31, 60, 46, 0.10);
                border-radius: 26px;
                box-shadow: 0 18px 46px rgba(31, 60, 46, 0.07);
            }

            .pp-investigation-header-icon {
                width: 54px;
                height: 54px;
                border-radius: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #1F3C2E 0%, #6F8F72 100%);
                color: #FFFFFF;
                box-shadow: 0 14px 30px rgba(31, 60, 46, 0.18);
                flex: 0 0 auto;
            }

            .pp-investigation-header-icon span {
                font-size: 18px;
                font-weight: 900;
                letter-spacing: 0.08em;
            }

            .pp-investigation-eyebrow {
                margin-bottom: 5px;
                color: #8A7442;
                font-size: 12px;
                font-weight: 850;
                letter-spacing: 0.16em;
            }

            .pp-investigation-header h2 {
                margin: 0;
                color: #1F3C2E;
                font-size: 25px;
                font-weight: 850;
                letter-spacing: -0.03em;
            }

            .pp-investigation-header p {
                max-width: 760px;
                margin: 8px 0 0 0;
                color: #5F6F63;
                font-size: 14px;
                line-height: 1.75;
            }

            .pp-investigation-toolbar {
                padding: 22px 24px;
                margin: 0 0 14px 0;
                background: #FFFFFF;
                border: 1px solid rgba(31, 60, 46, 0.10);
                border-radius: 24px;
                box-shadow: 0 14px 34px rgba(31, 60, 46, 0.055);
            }

            .pp-investigation-toolbar label {
                color: #1F3C2E !important;
                font-size: 13px !important;
                font-weight: 850 !important;
            }

            .pp-investigation-toolbar [data-baseweb="select"] > div,
            .pp-investigation-toolbar [data-baseweb="input"] > div {
                min-height: 44px;
                border-radius: 15px !important;
                border-color: rgba(31, 60, 46, 0.14) !important;
                background: #FBFAF6 !important;
                box-shadow: none !important;
            }

            .pp-investigation-toolbar [data-baseweb="select"] > div:hover,
            .pp-investigation-toolbar [data-baseweb="input"] > div:hover {
                border-color: rgba(111, 143, 114, 0.42) !important;
                background: #FFFFFF !important;
            }

            .pp-investigation-toolbar input {
                color: #1F3C2E !important;
                font-size: 14px !important;
            }

            .pp-investigation-summary {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 0 0 24px 0;
            }

            .pp-investigation-chip {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 11px;
                border-radius: 999px;
                background: #FFFFFF;
                border: 1px solid rgba(31, 60, 46, 0.09);
                box-shadow: 0 8px 20px rgba(31, 60, 46, 0.04);
            }

            .pp-investigation-chip span {
                color: #8B947F;
                font-size: 11px;
                font-weight: 850;
                letter-spacing: 0.08em;
            }

            .pp-investigation-chip strong {
                color: #1F3C2E;
                font-size: 12px;
                font-weight: 900;
            }

            @media (max-width: 860px) {
                .pp-investigation-header {
                    align-items: flex-start;
                    flex-direction: column;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )