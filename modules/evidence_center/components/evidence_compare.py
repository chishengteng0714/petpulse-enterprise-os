import html
import streamlit as st


def render_evidence_compare(evidence_items):
    """
    Evidence Compare

    GM-11 Enterprise Investigation Identity：
    - Presentation Layer Only
    - 不修改 Evidence Schema
    - 不修改 Runtime / Service / Repository
    - 不修改 Session State
    - 保留原本 Compare A / Compare B 選取邏輯
    - 保留原本證據查找與比較責任
    - 統一使用 Enterprise Design System
    - 改為 Enterprise Investigation Comparison File
    """

    evidence_items = evidence_items or []

    selected_evidence_a = st.session_state.get("selected_evidence")
    selected_evidence_b = st.session_state.get("selected_evidence_2")

    evidence_a = _find_evidence(
        evidence_items,
        selected_evidence_a,
    )
    evidence_b = _find_evidence(
        evidence_items,
        selected_evidence_b,
    )

    _render_compare_header(
        evidence_a=evidence_a,
        evidence_b=evidence_b,
    )

    if not evidence_a and not evidence_b:
        _render_empty_compare()
        return

    compare_col_a, compare_col_b = st.columns(2)

    with compare_col_a:
        _render_compare_card(
            "案件 A",
            evidence_a,
        )

    with compare_col_b:
        _render_compare_card(
            "案件 B",
            evidence_b,
        )

    _render_compare_summary(
        evidence_a,
        evidence_b,
    )


def _render_compare_header(evidence_a, evidence_b):
    selected_count = sum(
        evidence is not None
        for evidence in [evidence_a, evidence_b]
    )

    status_text = (
        "已完成雙案選取"
        if selected_count == 2
        else f"已選取 {selected_count} 筆案件"
    )

    status_class = (
        "success"
        if selected_count == 2
        else "gold"
    )

    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                比
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    證據交叉比對
                </div>

                <div class="pp-section-subtitle">
                    將兩筆公開證據放入同一份調查卷宗，
                    比較來源背景、事件敘述與訊號差異。
                </div>
            </div>

            <div class="pp-badge {status_class}">
                {status_text}
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_empty_compare():
    st.markdown(
        """
        <section class="pp-callout">
            <div class="pp-card-top">
                <div class="pp-card-index">
                    比
                </div>

                <div class="pp-badge info">
                    等待案件
                </div>
            </div>

            <div class="pp-card-kicker">
                企業調查交叉比對
            </div>

            <div class="pp-card-title">
                尚未選取需要比對的證據
            </div>

            <div class="pp-card-desc">
                請先從證據清單選擇主要案件與比較案件。
                完成選取後，系統將在此呈現兩筆證據的來源、
                議題、情緒、事件資訊與主要差異。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_compare_card(title, evidence):
    if not evidence:
        _render_missing_compare_card(title)
        return

    evidence_id = _safe_text(
        _get_evidence_id(evidence)
    )

    evidence_title = _safe_text(
        _safe_get(
            evidence,
            "title",
            "未命名證據",
        )
    )

    content = _safe_text(
        _safe_get(
            evidence,
            "content",
            _safe_get(
                evidence,
                "description",
                "目前沒有證據內容。",
            ),
        )
    )

    ai_summary = _safe_text(
        _safe_get(
            evidence,
            "ai_summary",
            _safe_get(
                evidence,
                "summary",
                content,
            ),
        )
    )

    platform = _safe_text(
        _format_platform(
            _safe_get(
                evidence,
                "platform",
                "未知來源",
            )
        )
    )

    topic = _safe_text(
        _safe_get(
            evidence,
            "topic",
            "未分類議題",
        )
    )

    sentiment = _safe_text(
        _format_sentiment(
            _safe_get(
                evidence,
                "sentiment",
                "未知情緒",
            )
        )
    )

    author = _safe_text(
        _safe_get(
            evidence,
            "author",
            "未知作者",
        )
    )

    published_time = _safe_text(
        _safe_get(
            evidence,
            "published_time",
            _safe_get(
                evidence,
                "time",
                _safe_get(
                    evidence,
                    "created_at",
                    "未知時間",
                ),
            ),
        )
    )

    engagement = _safe_text(
        _safe_get(
            evidence,
            "engagement",
            "未提供",
        )
    )

    original_url = _safe_url(
        _safe_get(
            evidence,
            "original_url",
            _safe_get(
                evidence,
                "url",
                _safe_get(
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
            href="{original_url}"
            target="_blank"
            rel="noopener noreferrer"
        >
            查看原始內容 →
        </a>
        """
        if original_url
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
                    {title[-1]}
                </div>

                <div class="pp-badge gold">
                    {title}｜{evidence_id}
                </div>
            </div>

            <div class="pp-card-kicker">
                案件識別
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
                {evidence_title}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                AI 摘要
            </div>

            <div class="pp-card-desc">
                {ai_summary}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                核心敘述
            </div>

            <div class="pp-card-desc">
                {content}
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

            <div class="pp-card-top">
                <div class="pp-card-meta">
                    公開來源案件卷宗
                </div>

                {source_action}
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def _render_missing_compare_card(title):
    st.markdown(
        f"""
        <section class="pp-callout">
            <div class="pp-card-top">
                <div class="pp-card-index">
                    {title[-1]}
                </div>

                <div class="pp-badge info">
                    尚未選取
                </div>
            </div>

            <div class="pp-card-kicker">
                {title}
            </div>

            <div class="pp-card-title">
                等待加入比較案件
            </div>

            <div class="pp-card-desc">
                請從證據清單選擇一筆案件加入此位置，
                以建立完整的雙案交叉比對。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_compare_summary(evidence_a, evidence_b):
    st.markdown(
        """
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                判
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    比對判讀摘要
                </div>

                <div class="pp-section-subtitle">
                    整理兩筆案件的共同訊號、主要差異與主管查核方向。
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if not evidence_a or not evidence_b:
        st.markdown(
            """
            <section class="pp-callout">
                <div class="pp-card-top">
                    <div class="pp-card-index">
                        判
                    </div>

                    <div class="pp-badge gold">
                        尚未完成
                    </div>
                </div>

                <div class="pp-card-kicker">
                    比對狀態
                </div>

                <div class="pp-card-title">
                    需要兩筆案件才能產生完整判讀
                </div>

                <div class="pp-card-desc">
                    目前案件選取尚未完成。請補上另一筆證據後，
                    再檢視共同來源、議題關聯、情緒差異與互動表現。
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    platform_a = _format_value(
        _safe_get(
            evidence_a,
            "platform",
            "未知來源",
        )
    )
    platform_b = _format_value(
        _safe_get(
            evidence_b,
            "platform",
            "未知來源",
        )
    )

    topic_a = _format_value(
        _safe_get(
            evidence_a,
            "topic",
            "未分類議題",
        )
    )
    topic_b = _format_value(
        _safe_get(
            evidence_b,
            "topic",
            "未分類議題",
        )
    )

    sentiment_a = _format_sentiment(
        _safe_get(
            evidence_a,
            "sentiment",
            "未知情緒",
        )
    )
    sentiment_b = _format_sentiment(
        _safe_get(
            evidence_b,
            "sentiment",
            "未知情緒",
        )
    )

    engagement_a = _safe_number(
        _safe_get(
            evidence_a,
            "engagement",
            0,
        )
    )
    engagement_b = _safe_number(
        _safe_get(
            evidence_b,
            "engagement",
            0,
        )
    )

    same_platform = platform_a == platform_b
    same_topic = topic_a == topic_b
    same_sentiment = sentiment_a == sentiment_b

    common_signals = []

    if same_platform:
        common_signals.append(
            f"兩筆案件皆來自「{platform_a}」，"
            "可視為相同平台環境下的訊號。"
        )

    if same_topic:
        common_signals.append(
            f"兩筆案件皆涉及「{topic_a}」，"
            "具有直接議題關聯。"
        )

    if same_sentiment:
        common_signals.append(
            f"兩筆案件皆呈現「{sentiment_a}」情緒，"
            "訊號方向一致。"
        )

    if not common_signals:
        common_signals.append(
            "兩筆案件在平台、議題與情緒上沒有完全相同的分類，"
            "建議從內容語境與事件時間進一步確認是否存在間接關聯。"
        )

    differences = []

    if not same_platform:
        differences.append(
            f"資料來源不同：案件 A 為「{platform_a}」，"
            f"案件 B 為「{platform_b}」。"
        )

    if not same_topic:
        differences.append(
            f"討論議題不同：案件 A 為「{topic_a}」，"
            f"案件 B 為「{topic_b}」。"
        )

    if not same_sentiment:
        differences.append(
            f"情緒方向不同：案件 A 為「{sentiment_a}」，"
            f"案件 B 為「{sentiment_b}」。"
        )

    if engagement_a > engagement_b:
        engagement_difference = engagement_a - engagement_b
        differences.append(
            f"案件 A 的互動量較高，高出案件 B "
            f"{engagement_difference} 次互動。"
        )
    elif engagement_b > engagement_a:
        engagement_difference = engagement_b - engagement_a
        differences.append(
            f"案件 B 的互動量較高，高出案件 A "
            f"{engagement_difference} 次互動。"
        )
    else:
        differences.append(
            "兩筆案件目前記錄的互動量相同。"
        )

    common_signal_html = "".join(
        f"""
        <div class="pp-card-meta">
            • {_safe_text(item)}
        </div>
        """
        for item in common_signals
    )

    difference_html = "".join(
        f"""
        <div class="pp-card-meta">
            • {_safe_text(item)}
        </div>
        """
        for item in differences
    )

    recommendation = _build_recommendation(
        same_platform=same_platform,
        same_topic=same_topic,
        same_sentiment=same_sentiment,
        engagement_a=engagement_a,
        engagement_b=engagement_b,
    )

    shared_count = sum(
        [
            same_platform,
            same_topic,
            same_sentiment,
        ]
    )

    relation_badge = (
        "高度相關"
        if shared_count >= 2
        else "部分相關"
        if shared_count == 1
        else "需要進一步查核"
    )

    relation_class = (
        "danger"
        if (
            same_topic
            and sentiment_a == "負向"
            and sentiment_b == "負向"
        )
        else "success"
        if shared_count >= 2
        else "gold"
    )

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card">
            <div class="pp-card-top">
                <div class="pp-card-index">
                    判
                </div>

                <div class="pp-badge {relation_class}">
                    {relation_badge}
                </div>
            </div>

            <div class="pp-card-kicker">
                交叉比對結論
            </div>

            <div class="pp-card-title">
                兩筆案件的調查關聯
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                共同訊號
            </div>

            {common_signal_html}

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                主要差異
            </div>

            {difference_html}

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                主管判讀建議
            </div>

            <div class="pp-card-desc">
                {_safe_text(recommendation)}
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def _build_recommendation(
    same_platform,
    same_topic,
    same_sentiment,
    engagement_a,
    engagement_b,
):
    if same_topic and same_sentiment:
        if engagement_a != engagement_b:
            return (
                "兩筆案件的議題與情緒方向一致，但互動表現不同。"
                "建議優先檢查互動量較高的案件，確認其內容是否正在擴散，"
                "並核對另一筆案件是否形成相同敘事或支持訊號。"
            )

        return (
            "兩筆案件的議題、情緒與互動表現高度接近。"
            "建議回到原始內容確認是否來自相同事件、轉載脈絡或重複討論，"
            "避免將相同訊號誤判為多個獨立事件。"
        )

    if same_topic and not same_sentiment:
        return (
            "兩筆案件討論相同議題，但情緒方向不同。"
            "建議比較作者立場、發布時間與內容語境，"
            "確認此議題是否出現評價分歧，並判斷哪一種觀點正在擴大。"
        )

    if same_platform and not same_topic:
        return (
            "兩筆案件來自相同平台，但討論議題不同。"
            "建議確認是否為同一群使用者、同一事件延伸討論，"
            "或只是平台內同時出現的獨立訊號。"
        )

    if same_sentiment and not same_topic:
        return (
            "兩筆案件情緒方向一致，但涉及不同議題。"
            "建議確認是否反映更廣泛的品牌態度、服務體驗或消費者期待，"
            "而不只是單一事件造成的局部反應。"
        )

    return (
        "兩筆案件目前沒有明顯一致的分類訊號。"
        "建議將發布時間、作者背景、原始內容與其他關聯證據一起檢視，"
        "確認兩者是否具有實際調查價值，避免僅因表面關鍵字而建立關聯。"
    )


def _find_evidence(evidence_items, evidence_id):
    if evidence_id is None:
        return None

    evidence_id = str(evidence_id)

    for item in evidence_items:
        if _get_evidence_id(item) == evidence_id:
            return item

    return None


def _get_evidence_id(item):
    evidence_id = _safe_get(
        item,
        "evidence_id",
        None,
    )

    if evidence_id is None:
        evidence_id = _safe_get(
            item,
            "id",
            None,
        )

    if evidence_id is None:
        evidence_id = _safe_get(
            item,
            "title",
            "unknown_evidence",
        )

    return str(evidence_id)


def _safe_get(item, key, default=None):
    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def _safe_number(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _format_value(value):
    if value is None:
        return "未知"

    if hasattr(value, "value"):
        return str(value.value)

    return str(value)


def _safe_text(value):
    if value is None:
        return ""

    if hasattr(value, "value"):
        value = value.value

    return html.escape(
        str(value)
    )


def _safe_url(value):
    if not value:
        return ""

    if hasattr(value, "value"):
        value = value.value

    value = str(value).strip()

    if not value.startswith(
        (
            "http://",
            "https://",
        )
    ):
        return ""

    return html.escape(
        value,
        quote=True,
    )


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

    return platform_map.get(
        str(value),
        str(value),
    )


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
        "正面": "正向",
        "中性": "中立",
        "負面": "負向",
        "正向": "正向",
        "中立": "中立",
        "負向": "負向",
    }

    return sentiment_map.get(
        str(value),
        str(value),
    )


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