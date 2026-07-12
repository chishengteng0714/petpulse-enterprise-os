import html
import pandas as pd
import streamlit as st


def render_evidence_table(evidence_items):
    """
    Evidence Table

    GM-11 Enterprise Investigation Identity：
    - Presentation Layer Only
    - 不修改資料來源
    - 不修改 Service / Repository / Schema
    - 保留 Evidence Card List
    - 統一使用 Enterprise Design System
    """

    evidence_items = evidence_items or []

    _render_evidence_list_header(evidence_items)

    if not evidence_items:
        _render_empty_state()
        return

    for index, item in enumerate(evidence_items, start=1):
        _render_evidence_card(index, item)


def _render_evidence_list_header(evidence_items):
    total_count = len(evidence_items or [])

    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">證</div>

            <div class="pp-section-copy">
                <div class="pp-card-kicker">企業調查卷宗</div>
                <div class="pp-section-title">可追溯的公開討論證據</div>
                <div class="pp-section-subtitle">
                    彙整社群、論壇、評論與新聞來源的公開訊號，
                    協助主管快速檢視脈絡、確認風險並回到原始內容驗證。
                </div>
            </div>

            <div class="pp-badge gold">
                {total_count} 筆證據
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_empty_state():
    st.markdown(
        """
        <section class="pp-callout">
            <div class="pp-card-top">
                <div class="pp-card-index">證</div>
                <div class="pp-badge info">查無結果</div>
            </div>

            <div class="pp-card-kicker">企業調查卷宗</div>
            <div class="pp-card-title">目前沒有符合條件的證據</div>

            <div class="pp-card-desc">
                請調整平台、議題、情緒或關鍵字條件後再次查詢。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_evidence_card(index, item):
    title = _safe_text(
        _get_value(
            item,
            "title",
            f"證據 {index:03d}",
        )
    )

    summary = _safe_text(
        _get_value(
            item,
            "summary",
            _get_value(
                item,
                "content",
                _get_value(
                    item,
                    "description",
                    "目前沒有摘要內容。",
                ),
            ),
        )
    )

    platform = _safe_text(
        _format_platform(
            _get_value(
                item,
                "platform",
                "未知平台",
            )
        )
    )

    sentiment = _safe_text(
        _format_sentiment(
            _get_value(
                item,
                "sentiment",
                "未知情緒",
            )
        )
    )

    topic = _safe_text(
        _get_value(
            item,
            "topic",
            "未分類議題",
        )
    )

    author = _safe_text(
        _get_value(
            item,
            "author",
            "未知作者",
        )
    )

    published_time = _safe_text(
        _format_time(
            _get_value(
                item,
                "published_time",
                _get_value(
                    item,
                    "time",
                    _get_value(
                        item,
                        "created_at",
                        "未知時間",
                    ),
                ),
            )
        )
    )

    engagement = _safe_text(
        _get_value(
            item,
            "engagement",
            "未提供",
        )
    )

    url = _safe_url(
        _get_value(
            item,
            "url",
            "",
        )
    )

    sentiment_class = _sentiment_class(sentiment)
    platform_class = _platform_class(platform)

    action_html = (
        f"""
        <a
            class="pp-badge gold"
            href="{url}"
            target="_blank"
            rel="noopener noreferrer"
            style="text-decoration:none;"
        >
            查看原始內容
        </a>
        """
        if url
        else """
        <div class="pp-badge info">
            尚未提供原始連結
        </div>
        """
    )

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card">
            <div class="pp-card-top">
                <div class="pp-card-index">{index:03d}</div>

                <div style="display:flex; flex-wrap:wrap; gap:0.5rem; justify-content:flex-end;">
                    <div class="pp-badge {platform_class}">
                        {platform}
                    </div>

                    <div class="pp-badge {sentiment_class}">
                        {sentiment}
                    </div>
                </div>
            </div>

            <div class="pp-card-kicker">企業證據卷宗</div>

            <div class="pp-card-title">
                {title}
            </div>

            <div class="pp-card-desc">
                {summary}
            </div>

            <div class="pp-card-meta">
                <strong>證據來源</strong><br>
                {platform}
                <br><br>

                <strong>討論議題</strong><br>
                {topic}
            </div>

            <div class="pp-card-meta">
                <strong>發布者</strong><br>
                {author}
                <br><br>

                <strong>發布時間</strong><br>
                {published_time}
            </div>

            <div class="pp-card-meta">
                <strong>互動量</strong><br>
                {engagement}
                <br><br>

                <strong>情緒判讀</strong><br>
                {sentiment}
            </div>

            <div class="pp-divider"></div>

            <div style="display:flex; flex-wrap:wrap; gap:0.55rem; align-items:center; justify-content:space-between;">
                <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
                    <div class="pp-badge {platform_class}">
                        {platform}
                    </div>

                    <div class="pp-badge info">
                        {topic}
                    </div>

                    <div class="pp-badge {sentiment_class}">
                        {sentiment}
                    </div>
                </div>

                {action_html}
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def _get_value(item, key, default=None):
    if item is None:
        return default

    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def _safe_text(value):
    if value is None:
        return ""

    if hasattr(value, "value"):
        value = value.value

    return html.escape(str(value))


def _safe_url(value):
    if not value:
        return ""

    if hasattr(value, "value"):
        value = value.value

    value = str(value).strip()

    if not value.startswith(("http://", "https://")):
        return ""

    return html.escape(value, quote=True)


def _format_platform(value):
    platform_map = {
        "Facebook": "Facebook",
        "Instagram": "Instagram",
        "Threads": "Threads",
        "PTT": "PTT",
        "Dcard": "Dcard",
        "Forum": "論壇",
        "Google Review": "Google 評論",
        "News": "新聞",
        "Blog": "部落格",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "threads": "Threads",
        "ptt": "PTT",
        "dcard": "Dcard",
        "forum": "論壇",
        "google_review": "Google 評論",
        "news": "新聞",
        "blog": "部落格",
    }

    if hasattr(value, "value"):
        value = value.value

    return platform_map.get(str(value), str(value))


def _format_sentiment(value):
    sentiment_map = {
        "Positive": "正向",
        "Neutral": "中立",
        "Negative": "負向",
        "positive": "正向",
        "neutral": "中立",
        "negative": "負向",
        "正向": "正向",
        "中立": "中立",
        "負向": "負向",
    }

    if hasattr(value, "value"):
        value = value.value

    return sentiment_map.get(str(value), str(value))


def _format_time(value):
    if value is None:
        return "未知時間"

    if hasattr(value, "value"):
        value = value.value

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y/%m/%d %H:%M")

    return str(value)


def _sentiment_class(sentiment):
    if "正向" in sentiment:
        return "success"

    if "負向" in sentiment:
        return "danger"

    if "中立" in sentiment:
        return "gold"

    return "info"


def _platform_class(platform):
    normalized = platform.lower()

    if "facebook" in normalized:
        return "info"

    if "instagram" in normalized:
        return "gold"

    if "threads" in normalized:
        return "info"

    if "ptt" in normalized:
        return "info"

    if "dcard" in normalized:
        return "gold"

    if "google" in normalized:
        return "success"

    if "新聞" in platform:
        return "danger"

    if "論壇" in platform:
        return "info"

    return "info"
