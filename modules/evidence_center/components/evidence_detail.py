import html
import streamlit as st


def render_evidence_detail(evidence):
    """
    Evidence Detail

    GM-11 Enterprise Investigation Identity：
    - Presentation Layer Only
    - 不修改 Evidence Schema
    - 不修改 Service / Repository / Query Engine
    - 保留原本單筆 Evidence 呈現責任
    - 移除 Component Private CSS
    - 統一使用 Enterprise Design System
    - 改為 Enterprise Investigation Case File
    """

    if not evidence:
        _render_empty_detail()
        return

    _render_detail_card(evidence)


def _render_empty_detail():
    st.markdown(
        """
        <section class="pp-callout">
            <div class="pp-card-top">
                <div class="pp-card-index">卷</div>
                <div class="pp-badge info">等待選取</div>
            </div>

            <div class="pp-card-kicker">
                企業調查工作區
            </div>

            <div class="pp-card-title">
                尚未選取調查案件
            </div>

            <div class="pp-card-desc">
                請從左側證據清單選擇一筆案件，
                查看完整證據脈絡、事件資訊與原始資料來源。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_detail_card(evidence):
    evidence_id = _safe_text(
        _get_value(
            evidence,
            "evidence_id",
            _get_value(
                evidence,
                "id",
                "未編號",
            ),
        )
    )

    title = _safe_text(
        _get_value(
            evidence,
            "title",
            "未命名證據",
        )
    )

    summary = _safe_text(
        _get_value(
            evidence,
            "summary",
            _get_value(
                evidence,
                "ai_summary",
                _get_value(
                    evidence,
                    "content",
                    _get_value(
                        evidence,
                        "description",
                        "目前沒有摘要內容。",
                    ),
                ),
            ),
        )
    )

    platform = _safe_text(
        _format_platform(
            _get_value(
                evidence,
                "platform",
                "未知平台",
            )
        )
    )

    topic = _safe_text(
        _get_value(
            evidence,
            "topic",
            "未分類議題",
        )
    )

    sentiment = _safe_text(
        _format_sentiment(
            _get_value(
                evidence,
                "sentiment",
                "未知情緒",
            )
        )
    )

    author = _safe_text(
        _get_value(
            evidence,
            "author",
            "未知作者",
        )
    )

    published_time = _safe_text(
        _get_value(
            evidence,
            "published_time",
            _get_value(
                evidence,
                "time",
                _get_value(
                    evidence,
                    "created_at",
                    "未知時間",
                ),
            ),
        )
    )

    engagement = _safe_text(
        _get_value(
            evidence,
            "engagement",
            "未提供",
        )
    )

    url = _safe_url(
        _get_value(
            evidence,
            "url",
            _get_value(
                evidence,
                "original_url",
                _get_value(
                    evidence,
                    "source_url",
                    "",
                ),
            ),
        )
    )

    sentiment_class = _sentiment_class(sentiment)
    platform_class = _platform_class(platform)

    source_action = (
        f"""
        <a
            class="pp-badge gold"
            href="{url}"
            target="_blank"
            rel="noopener noreferrer"
        >
            查看原始內容 →
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
                <div class="pp-card-index">
                    案
                </div>

                <div class="pp-badge gold">
                    案件編號｜{evidence_id}
                </div>
            </div>

            <div class="pp-card-kicker">
                企業調查案件卷宗
            </div>

            <div class="pp-card-meta">
                <div class="pp-badge {platform_class}">
                    {platform}
                </div>

                <div class="pp-badge {sentiment_class}">
                    {sentiment}
                </div>

                <div class="pp-badge info">
                    {topic}
                </div>
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                證據標題
            </div>

            <div class="pp-card-title">
                {title}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                AI 摘要
            </div>

            <div class="pp-card-desc">
                {summary}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                事件資訊
            </div>

            <div class="pp-card-meta">
                <strong>發布時間</strong><br>
                {published_time}
            </div>

            <div class="pp-card-meta">
                <strong>作者</strong><br>
                {author}
            </div>

            <div class="pp-card-meta">
                <strong>互動量</strong><br>
                {engagement}
            </div>

            <div class="pp-card-meta">
                <strong>資料來源</strong><br>
                {platform}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                主管判讀建議
            </div>

            <div class="pp-card-desc">
                建議將此案件與相同議題、平台及情緒的其他公開訊號交叉檢視，
                確認事件是否持續擴散、是否具有代表性，以及是否需要安排後續回應。
                正式決策前，請回到原始內容核對完整語境與來源可信度。
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-top">
                <div class="pp-card-meta">
                    調查案件內容已整理完成，可進一步核對原始公開資料。
                </div>

                {source_action}
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
    if hasattr(value, "value"):
        value = value.value

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

    return platform_map.get(str(value), str(value))


def _format_sentiment(value):
    if hasattr(value, "value"):
        value = value.value

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

    return sentiment_map.get(str(value), str(value))


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