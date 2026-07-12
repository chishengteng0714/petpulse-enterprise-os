import streamlit as st


def render_evidence_explorer(evidence_items):
    """
    Evidence Explorer

    GM-11 Enterprise Investigation Identity：
    - Presentation Layer Only
    - 不修改 Evidence Schema
    - 不修改 Runtime / Engine / Service / Repository
    - 不修改 Session State
    - 保留原本篩選、選取與比較邏輯
    - 保留原本 Master / Detail 組裝方式
    - 統一使用 Enterprise Design System
    - 改為 Enterprise Investigation Case Explorer
    """

    evidence_items = evidence_items or []

    _render_explorer_header(evidence_items)
    _render_micro_gap()

    _render_explorer_summary(evidence_items)
    _render_micro_gap()

    filtered_items = _render_filters(evidence_items)
    _render_micro_gap()

    col1, col2 = st.columns([1.25, 1])

    with col1:
        _render_evidence_list(filtered_items)

    with col2:
        _render_evidence_detail(evidence_items)


def _render_explorer_header(evidence_items):
    evidence_count = len(evidence_items)

    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                查
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    調查案件總覽
                </div>

                <div class="pp-section-subtitle">
                    從公開訊號中篩選案件、建立主要證據，
                    並將相關內容加入交叉比對。
                </div>
            </div>

            <div class="pp-badge gold">
                {evidence_count} 筆案件
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_explorer_summary(evidence_items):
    platforms = {
        _format_value(
            _safe_get(
                item,
                "platform",
                "未知來源",
            )
        )
        for item in evidence_items
    }

    topics = {
        _format_value(
            _safe_get(
                item,
                "topic",
                "未分類議題",
            )
        )
        for item in evidence_items
    }

    risk_count = len(
        [
            item
            for item in evidence_items
            if _normalize_sentiment(
                _safe_get(
                    item,
                    "sentiment",
                    "",
                )
            )
            == "負向"
        ]
    )

    selected_primary = st.session_state.get("selected_evidence")
    selected_compare = st.session_state.get("selected_evidence_2")

    selected_count = sum(
        [
            selected_primary is not None,
            selected_compare is not None,
        ]
    )

    st.markdown(
        f"""
        <section class="pp-executive-strip">
            <div class="pp-executive-strip-item">
                <div class="pp-executive-strip-label">
                    可調查案件
                </div>

                <div class="pp-executive-strip-value">
                    {len(evidence_items)}
                </div>

                <div class="pp-executive-strip-note">
                    目前可檢視的公開證據
                </div>
            </div>

            <div class="pp-executive-strip-item">
                <div class="pp-executive-strip-label">
                    資料來源
                </div>

                <div class="pp-executive-strip-value">
                    {len(platforms)}
                </div>

                <div class="pp-executive-strip-note">
                    已納入調查的平台數
                </div>
            </div>

            <div class="pp-executive-strip-item">
                <div class="pp-executive-strip-label">
                    重要議題
                </div>

                <div class="pp-executive-strip-value">
                    {len(topics)}
                </div>

                <div class="pp-executive-strip-note">
                    目前辨識的議題數
                </div>
            </div>

            <div class="pp-executive-strip-item">
                <div class="pp-executive-strip-label">
                    負向訊號
                </div>

                <div class="pp-executive-strip-value">
                    {risk_count}
                </div>

                <div class="pp-executive-strip-note">
                    建議優先查核的案件
                </div>
            </div>

            <div class="pp-executive-strip-item">
                <div class="pp-executive-strip-label">
                    已選案件
                </div>

                <div class="pp-executive-strip-value">
                    {selected_count}
                </div>

                <div class="pp-executive-strip-note">
                    主要案件與比較案件
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_filters(evidence_items):
    st.markdown(
        """
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                篩
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    案件查詢條件
                </div>

                <div class="pp-section-subtitle">
                    依照平台、議題、情緒與關鍵字縮小調查範圍。
                </div>
            </div>

            <div class="pp-badge info">
                調查工具
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    platforms = sorted(
        {
            _format_value(
                _safe_get(
                    item,
                    "platform",
                    "未知來源",
                )
            )
            for item in evidence_items
        }
    )

    topics = sorted(
        {
            _format_value(
                _safe_get(
                    item,
                    "topic",
                    "未分類議題",
                )
            )
            for item in evidence_items
        }
    )

    sentiments = sorted(
        {
            _format_value(
                _safe_get(
                    item,
                    "sentiment",
                    "未知情緒",
                )
            )
            for item in evidence_items
        }
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        platform_filter = st.selectbox(
            "資料平台",
            options=["全部"] + platforms,
            key="evidence_explorer_platform_filter",
        )

    with col2:
        topic_filter = st.selectbox(
            "討論議題",
            options=["全部"] + topics,
            key="evidence_explorer_topic_filter",
        )

    with col3:
        sentiment_filter = st.selectbox(
            "情緒方向",
            options=["全部"] + sentiments,
            key="evidence_explorer_sentiment_filter",
        )

    with col4:
        keyword = st.text_input(
            "案件關鍵字",
            value="",
            key="evidence_explorer_keyword_filter",
            placeholder="輸入品牌、商品、門市、服務或競品",
        )

    filtered_items = []

    for item in evidence_items:
        platform = _format_value(
            _safe_get(
                item,
                "platform",
                "未知來源",
            )
        )

        topic = _format_value(
            _safe_get(
                item,
                "topic",
                "未分類議題",
            )
        )

        sentiment = _format_value(
            _safe_get(
                item,
                "sentiment",
                "未知情緒",
            )
        )

        title = _format_value(
            _safe_get(
                item,
                "title",
                "",
            )
        )

        content = _format_value(
            _safe_get(
                item,
                "content",
                "",
            )
        )

        ai_summary = _format_value(
            _safe_get(
                item,
                "ai_summary",
                _safe_get(
                    item,
                    "summary",
                    "",
                ),
            )
        )

        if (
            platform_filter != "全部"
            and platform != platform_filter
        ):
            continue

        if (
            topic_filter != "全部"
            and topic != topic_filter
        ):
            continue

        if (
            sentiment_filter != "全部"
            and sentiment != sentiment_filter
        ):
            continue

        if keyword:
            search_text = (
                f"{title} "
                f"{content} "
                f"{ai_summary} "
                f"{platform} "
                f"{topic}"
            ).lower()

            if keyword.lower() not in search_text:
                continue

        filtered_items.append(item)

    result_class = (
        "success"
        if filtered_items
        else "danger"
    )

    st.markdown(
        f"""
        <div class="pp-card-top">
            <div class="pp-card-meta">
                查詢結果已依目前條件更新
            </div>

            <div class="pp-badge {result_class}">
                顯示 {len(filtered_items)} / {len(evidence_items)} 筆
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return filtered_items


def _render_evidence_list(evidence_items):
    st.markdown(
        """
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                卷
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    調查案件清單
                </div>

                <div class="pp-section-subtitle">
                    依互動量排序，優先呈現影響程度較高的公開訊號。
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if not evidence_items:
        st.markdown(
            """
            <section class="pp-callout">
                <div class="pp-card-top">
                    <div class="pp-card-index">
                        空
                    </div>

                    <div class="pp-badge info">
                        無符合案件
                    </div>
                </div>

                <div class="pp-card-kicker">
                    調查案件清單
                </div>

                <div class="pp-card-title">
                    目前沒有符合條件的證據
                </div>

                <div class="pp-card-desc">
                    請調整平台、議題、情緒或關鍵字，
                    重新建立調查範圍。
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    sorted_items = sorted(
        evidence_items,
        key=lambda item: _safe_number(
            _safe_get(
                item,
                "engagement",
                0,
            )
        ),
        reverse=True,
    )

    for index, item in enumerate(
        sorted_items,
        start=1,
    ):
        _render_evidence_card(
            index,
            item,
        )


def _render_evidence_card(index, item):
    evidence_id = _get_evidence_id(item)

    title = _format_value(
        _safe_get(
            item,
            "title",
            "未命名證據",
        )
    )

    content = _format_value(
        _safe_get(
            item,
            "content",
            _safe_get(
                item,
                "description",
                "",
            ),
        )
    )

    platform = _format_platform(
        _safe_get(
            item,
            "platform",
            "未知來源",
        )
    )

    topic = _format_value(
        _safe_get(
            item,
            "topic",
            "未分類議題",
        )
    )

    sentiment = _normalize_sentiment(
        _safe_get(
            item,
            "sentiment",
            "未知情緒",
        )
    )

    engagement = _safe_number(
        _safe_get(
            item,
            "engagement",
            0,
        )
    )

    selected_primary = (
        st.session_state.get("selected_evidence")
        == evidence_id
    )

    selected_compare = (
        st.session_state.get("selected_evidence_2")
        == evidence_id
    )

    if selected_primary:
        status_text = "主要案件"
        status_class = "success"
    elif selected_compare:
        status_text = "比較案件"
        status_class = "gold"
    else:
        status_text = "待檢視"
        status_class = "info"

    sentiment_class = _sentiment_class(sentiment)
    platform_class = _platform_class(platform)

    summary = content[:220]

    if len(content) > 220:
        summary = f"{summary}…"

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card">
            <div class="pp-card-top">
                <div class="pp-card-index">
                    {index:02d}
                </div>

                <div class="pp-badge {status_class}">
                    {status_text}
                </div>
            </div>

            <div class="pp-card-kicker">
                案件編號｜{evidence_id}
            </div>

            <div class="pp-card-title">
                {title}
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

            <div class="pp-card-desc">
                {summary or "目前沒有可顯示的案件內容。"}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-top">
                <div class="pp-card-meta">
                    互動量｜{engagement}
                </div>

                <div class="pp-card-meta">
                    公開來源案件
                </div>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button(
            "開啟案件",
            key=f"explorer_open_{evidence_id}",
            use_container_width=True,
        ):
            _select_evidence_a(evidence_id)
            st.rerun()

    with action_col2:
        if st.button(
            "設為主要案件",
            key=f"explorer_compare_a_{evidence_id}",
            use_container_width=True,
        ):
            _select_evidence_a(evidence_id)
            st.rerun()

    with action_col3:
        if st.button(
            "加入交叉比對",
            key=f"explorer_compare_b_{evidence_id}",
            use_container_width=True,
        ):
            _select_evidence_b(evidence_id)
            st.rerun()

    _render_micro_gap()


def _render_evidence_detail(evidence_items):
    st.markdown(
        """
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">
                案
            </div>

            <div class="pp-section-copy">
                <div class="pp-section-title">
                    主要調查案件
                </div>

                <div class="pp-section-subtitle">
                    檢視目前選取案件的核心內容與調查識別資訊。
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    selected_id = st.session_state.get(
        "selected_evidence"
    )

    if not selected_id:
        st.markdown(
            """
            <section class="pp-callout">
                <div class="pp-card-top">
                    <div class="pp-card-index">
                        案
                    </div>

                    <div class="pp-badge info">
                        等待選取
                    </div>
                </div>

                <div class="pp-card-kicker">
                    主要調查案件
                </div>

                <div class="pp-card-title">
                    尚未指定主要案件
                </div>

                <div class="pp-card-desc">
                    請從左側案件清單選擇一筆證據，
                    建立目前調查工作的主要案件。
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    evidence = _find_evidence(
        evidence_items,
        selected_id,
    )

    if not evidence:
        st.markdown(
            """
            <section class="pp-callout">
                <div class="pp-card-top">
                    <div class="pp-card-index">
                        異
                    </div>

                    <div class="pp-badge danger">
                        案件不存在
                    </div>
                </div>

                <div class="pp-card-kicker">
                    調查資料異常
                </div>

                <div class="pp-card-title">
                    找不到已選取的案件
                </div>

                <div class="pp-card-desc">
                    目前的選取紀錄已無法對應案件資料。
                    請重新從案件清單建立主要案件。
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    evidence_id = _get_evidence_id(evidence)

    title = _format_value(
        _safe_get(
            evidence,
            "title",
            "未命名證據",
        )
    )

    content = _format_value(
        _safe_get(
            evidence,
            "content",
            _safe_get(
                evidence,
                "description",
                "目前沒有內容。",
            ),
        )
    )

    ai_summary = _format_value(
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

    platform = _format_platform(
        _safe_get(
            evidence,
            "platform",
            "未知來源",
        )
    )

    topic = _format_value(
        _safe_get(
            evidence,
            "topic",
            "未分類議題",
        )
    )

    sentiment = _normalize_sentiment(
        _safe_get(
            evidence,
            "sentiment",
            "未知情緒",
        )
    )

    engagement = _safe_number(
        _safe_get(
            evidence,
            "engagement",
            0,
        )
    )

    sentiment_class = _sentiment_class(sentiment)
    platform_class = _platform_class(platform)

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card">
            <div class="pp-card-top">
                <div class="pp-card-index">
                    案
                </div>

                <div class="pp-badge success">
                    主要案件
                </div>
            </div>

            <div class="pp-card-kicker">
                案件編號｜{evidence_id}
            </div>

            <div class="pp-card-title">
                {title}
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
                AI 摘要
            </div>

            <div class="pp-card-desc">
                {ai_summary}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-kicker">
                原始證據內容
            </div>

            <div class="pp-card-desc">
                {content}
            </div>

            <div class="pp-divider"></div>

            <div class="pp-card-top">
                <div class="pp-card-meta">
                    互動量｜{engagement}
                </div>

                <div class="pp-card-meta">
                    資料來源｜{platform}
                </div>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button(
            "加入交叉比對",
            key=f"explorer_detail_compare_{evidence_id}",
            use_container_width=True,
        ):
            _select_evidence_b(
                _get_evidence_id(evidence)
            )
            st.rerun()

    with action_col2:
        if st.button(
            "清除主要案件",
            key=f"explorer_detail_clear_{evidence_id}",
            use_container_width=True,
        ):
            st.session_state["selected_evidence"] = None
            st.rerun()


def _select_evidence_a(evidence_id):
    st.session_state["selected_evidence"] = evidence_id

    history = st.session_state.get(
        "selection_history",
        [],
    )

    history.append(evidence_id)

    st.session_state["selection_history"] = (
        history[-20:]
    )


def _select_evidence_b(evidence_id):
    st.session_state["selected_evidence_2"] = evidence_id

    history = st.session_state.get(
        "compare_history",
        [],
    )

    history.append(evidence_id)

    st.session_state["compare_history"] = (
        history[-20:]
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
        return item.get(
            key,
            default,
        )

    return getattr(
        item,
        key,
        default,
    )


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


def _format_platform(value):
    value = _format_value(value)

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
        value,
        value,
    )


def _normalize_sentiment(value):
    value = _format_value(value)

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
        value,
        value,
    )


def _sentiment_class(sentiment):
    if sentiment == "正向":
        return "success"

    if sentiment == "負向":
        return "danger"

    if sentiment == "中立":
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


def _render_micro_gap():
    st.markdown("")