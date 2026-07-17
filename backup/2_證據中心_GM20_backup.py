import streamlit as st
from html import escape
from pathlib import Path

from modules.evidence_center.service import EvidenceService


st.set_page_config(
    page_title="證據中心｜PetPulse 企業決策系統",
    page_icon="📌",
    layout="wide",
)


def main():
    """
    PetPulse Enterprise OS v1.0 Golden Master

    GM-14 Evidence Center Premium：
    - Presentation Layer Only
    - 不修改 Evidence Schema
    - 不修改 Service / Repository / Query Engine
    - 不修改篩選與查詢邏輯
    - 強化 Hero、Query Panel、Evidence Table 與主管判讀
    """

    _load_enterprise_css()
    _inject_evidence_center_css()

    service = EvidenceService()
    evidence_items = service.get_all_evidence()

    _render_hero(evidence_items)
    filtered_items = _render_query_tools(evidence_items)
    _render_evidence_command_strip(filtered_items)
    _render_evidence_table(filtered_items)
    _render_decision_hint(filtered_items)


def _load_enterprise_css():
    current = Path(__file__).resolve()

    for parent in current.parents:
        css_path = parent / "assets" / "enterprise.css"

        if css_path.exists():
            css = css_path.read_text(encoding="utf-8")
            st.markdown(
                f"<style>{css}</style>",
                unsafe_allow_html=True,
            )
            return


def _inject_evidence_center_css():
    """GM-14 Evidence Center Final Visual Pass。"""

    _render_html("""
<style>
    .pp-evidence-page-hero .pp-hero-title { max-width: 780px; }
    .pp-evidence-page-hero .pp-hero-summary { max-width: 790px; }

    .pp-evidence-query-shell {
        position: relative;
        overflow: hidden;
        margin-top: 0.1rem;
        padding: 1.15rem;
        border: 1px solid rgba(0, 62, 51, 0.10);
        border-radius: 24px;
        background:
            radial-gradient(circle at 96% 0%, rgba(216, 183, 106, 0.12), transparent 30%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(250, 248, 242, 0.96));
        box-shadow:
            0 20px 52px rgba(0, 62, 51, 0.07),
            inset 0 1px 0 rgba(255, 255, 255, 0.88);
    }

    .pp-evidence-query-shell::before {
        content: "";
        position: absolute;
        top: 0;
        left: 1.4rem;
        right: 1.4rem;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(123, 170, 60, 0.42), rgba(216, 183, 106, 0.34), transparent);
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp-evidence-toolbar-marker) {
        margin-top: -0.15rem;
        padding: 0.15rem !important;
        border: 0 !important;
        border-radius: 22px !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp-evidence-toolbar-marker) > div {
        padding: 0 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp-evidence-toolbar-marker) [data-testid="stHorizontalBlock"] {
        gap: 0.72rem;
    }

    .pp-evidence-command-main { min-height: 100%; }
    .pp-evidence-command-main .pp-card-title { max-width: 680px; font-size: 1.44rem; }
    .pp-evidence-command-main .pp-card-desc { max-width: 720px; }
    .pp-evidence-command-side { height: 100%; }
    .pp-evidence-command-side .pp-card-summary { min-height: calc(50% - 0.5rem); }

    .pp-evidence-table-shell { padding: 1.4rem; border-radius: 28px; }

    .pp-evidence-table-scroll {
        margin-top: 1rem;
        overflow-x: auto;
        overflow-y: hidden;
        border: 1px solid rgba(0, 62, 51, 0.09);
        border-radius: 20px;
        background: #FFFFFF;
        box-shadow:
            0 14px 34px rgba(0, 62, 51, 0.045),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    .pp-evidence-table { border: 0 !important; border-radius: 0 !important; box-shadow: none !important; }

    .pp-evidence-table tbody tr:hover {
        background: linear-gradient(90deg, rgba(123, 170, 60, 0.075), rgba(216, 183, 106, 0.035)) !important;
        box-shadow: inset 4px 0 0 #7BAA3C, 0 8px 18px rgba(0, 62, 51, 0.025);
    }

    .pp-evidence-table tbody td { transition: background 160ms ease, color 160ms ease; }
    .pp-evidence-title-cell { max-width: 340px; color: #173C31; font-weight: 760; }

    .pp-evidence-link-disabled {
        border-color: rgba(0, 62, 51, 0.08) !important;
        background: #F3F3EF !important;
        color: #9AA29D !important;
        pointer-events: none;
        box-shadow: none !important;
    }

    .pp-evidence-decision-card .pp-card-title { max-width: 720px; font-size: 1.48rem; }

    .pp-evidence-decision-steps {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.72rem;
        margin-top: 1rem;
    }

    .pp-evidence-decision-step {
        padding: 0.92rem;
        border: 1px solid rgba(255, 255, 255, 0.13);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.075);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    .pp-evidence-decision-step span {
        display: block;
        color: rgba(255, 255, 255, 0.55);
        font-size: 0.67rem;
        font-weight: 820;
        letter-spacing: 0.1em;
    }

    .pp-evidence-decision-step strong {
        display: block;
        margin-top: 0.34rem;
        color: #FFFFFF;
        font-size: 0.92rem;
        line-height: 1.45;
        font-weight: 820;
    }

    .pp-evidence-empty {
        padding: 2.8rem 2rem;
        border: 1px solid rgba(0, 62, 51, 0.10);
        border-radius: 24px;
        background: radial-gradient(circle at 50% 0%, rgba(123, 170, 60, 0.10), transparent 34%), #FFFFFF;
        box-shadow: 0 18px 44px rgba(0, 62, 51, 0.055);
        text-align: center;
    }

    .pp-evidence-empty-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 54px;
        height: 54px;
        margin: 0 auto 1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #003E33 0%, #7BAA3C 145%);
        color: #FFFFFF;
        font-size: 0.92rem;
        font-weight: 900;
        box-shadow: 0 14px 30px rgba(0, 62, 51, 0.17);
    }

    .pp-evidence-empty-title { color: #003E33; font-size: 1.08rem; font-weight: 880; }
    .pp-evidence-empty-desc { margin-top: 0.5rem; color: #6B7871; font-size: 0.86rem; line-height: 1.7; }

    @media (max-width: 980px) {
        .pp-evidence-decision-steps { grid-template-columns: 1fr; }
    }

    @media (max-width: 820px) {
        .pp-evidence-query-shell { padding: 0.96rem; border-radius: 20px; }
        .pp-evidence-table-shell { padding: 1rem; border-radius: 22px; }
        .pp-evidence-command-main .pp-card-title,
        .pp-evidence-decision-card .pp-card-title { font-size: 1.28rem; }
    }
</style>
    """)


def _compact_html(markup):
    if not markup:
        return ""

    return "".join(
        line.strip()
        for line in str(markup).splitlines()
        if line.strip()
    )


def _render_html(markup):
    st.markdown(
        _compact_html(markup),
        unsafe_allow_html=True,
    )


def _safe(value, fallback=""):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()

    if not text:
        return escape(str(fallback))

    return escape(text)


def _get_item_value(item, *keys, fallback=""):
    for key in keys:
        if isinstance(item, dict):
            value = item.get(key)
        else:
            value = getattr(item, key, None)

        if value not in (None, ""):
            if hasattr(value, "value"):
                value = value.value

            return value

    return fallback


def _section(icon, eyebrow, title, subtitle, count=None, count_label="筆"):
    count_html = ""

    if count is not None:
        count_html = f'<div class="pp-badge gold">{count} {count_label}</div>'

    _render_html(f"""
<section class="pp-section-header pp-enterprise-section-header">
    <div class="pp-section-icon pp-enterprise-section-icon">{_safe(icon)}</div>
    <div class="pp-section-copy">
        <div class="pp-card-kicker">{_safe(eyebrow)}</div>
        <div class="pp-section-title">{_safe(title)}</div>
        <div class="pp-section-subtitle">{_safe(subtitle)}</div>
    </div>
    {count_html}
</section>
    """)


def _render_hero(evidence_items):
    total_count = len(evidence_items)
    platform_count = len({str(_get_item_value(item, "platform", fallback="")).strip() for item in evidence_items if str(_get_item_value(item, "platform", fallback="")).strip()})
    negative_count = _count_sentiment(evidence_items, "negative")
    positive_count = _count_sentiment(evidence_items, "positive")

    status_text = "需要優先查核" if negative_count > 0 else "證據狀態穩定"
    top_platform = _top_value(evidence_items, "platform", "尚無來源")
    top_topic = _top_value(evidence_items, "topic", "尚無議題")

    _render_html(f"""
<section class="pp-hero pp-enterprise-hero pp-evidence-page-hero">
    <div class="pp-hero-dashboard">
        <div class="pp-hero-main">
            <div class="pp-product-signature">PetPulse 企業證據作業中心</div>
            <div class="pp-hero-kicker">今日證據判讀台</div>
            <h1 class="pp-hero-title">從公開訊號，建立可追溯的決策依據</h1>
            <div class="pp-hero-summary">彙整跨平台公開來源、討論脈絡與原始連結，讓主管在做出判斷之前，快速看見證據分布、異常訊號與需要優先查核的事項。</div>
            <div class="pp-hero-meta">
                <div class="pp-badge dark">公開來源查核</div>
                <div class="pp-badge dark">討論脈絡比對</div>
                <div class="pp-badge dark">原始連結追溯</div>
            </div>
            <div class="pp-executive-strip">
                <div class="pp-executive-strip-item"><span class="pp-executive-strip-label">證據總量</span><strong>{total_count} 筆</strong></div>
                <div class="pp-executive-strip-item"><span class="pp-executive-strip-label">公開來源</span><strong>{platform_count} 個</strong></div>
                <div class="pp-executive-strip-item"><span class="pp-executive-strip-label">情緒分布</span><strong>{negative_count} 負向・{positive_count} 正向</strong></div>
            </div>
        </div>
        <aside class="pp-hero-side">
            <div class="pp-hero-signal"><div class="pp-hero-signal-label">目前狀態</div><div class="pp-hero-signal-value">{status_text}</div><div class="pp-hero-signal-note">以負向訊號與原始來源作為優先查核依據。</div></div>
            <div class="pp-hero-signal"><div class="pp-hero-signal-label">主要來源</div><div class="pp-hero-signal-value">{_safe(top_platform)}</div><div class="pp-hero-signal-note">目前證據量最高的公開平台。</div></div>
            <div class="pp-hero-signal"><div class="pp-hero-signal-label">主要議題</div><div class="pp-hero-signal-value">{_safe(top_topic)}</div><div class="pp-hero-signal-note">目前討論集中度最高的議題。</div></div>
        </aside>
    </div>
</section>
    """)


def _render_query_tools(evidence_items):
    _section(
        "查",
        "證據查詢",
        "查詢與縮小範圍",
        "依照資料來源、討論議題、情緒狀態與關鍵字，快速鎖定需要檢視的證據。",
    )

    platforms = ["全部"] + sorted({str(_get_item_value(item, "platform", fallback="未知")) for item in evidence_items})
    topics = ["全部"] + sorted({str(_get_item_value(item, "topic", fallback="未分類")) for item in evidence_items})
    sentiments = ["全部"] + sorted({str(_get_item_value(item, "sentiment", fallback="未知")) for item in evidence_items})

    _render_html("""
<section class="pp-evidence-query-shell">
    <div class="pp-evidence-query-intro">
        <div class="pp-card-top">
            <div><div class="pp-evidence-query-eyebrow">證據範圍</div><div class="pp-evidence-query-title">建立今日查核條件</div></div>
            <div class="pp-badge success">即時更新</div>
        </div>
        <div class="pp-evidence-query-desc">選擇來源、議題與情緒狀態，或輸入關鍵字。下方證據結果與主管判讀將同步更新。</div>
    </div>
    <div class="pp-evidence-toolbar-marker"></div>
</section>
    """)

    with st.container(border=True):
        _render_html('<div class="pp-evidence-toolbar-marker"></div>')
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.45])

        with col1:
            selected_platform = st.selectbox("資料來源", platforms, key="evidence_platform_filter")
        with col2:
            selected_topic = st.selectbox("討論議題", topics, key="evidence_topic_filter")
        with col3:
            selected_sentiment = st.selectbox("情緒狀態", sentiments, key="evidence_sentiment_filter", format_func=_sentiment_display)
        with col4:
            keyword = st.text_input("關鍵字", placeholder="輸入內容、議題或發布者", key="evidence_keyword_filter")

    normalized_keyword = keyword.strip().lower()
    filtered_items = []

    for item in evidence_items:
        platform = str(_get_item_value(item, "platform", fallback="未知"))
        topic = str(_get_item_value(item, "topic", fallback="未分類"))
        sentiment = str(_get_item_value(item, "sentiment", fallback="未知"))
        title = str(_get_item_value(item, "title", fallback=""))
        content = str(_get_item_value(item, "content", fallback=""))
        author = str(_get_item_value(item, "author", fallback=""))

        if selected_platform != "全部" and platform != selected_platform:
            continue
        if selected_topic != "全部" and topic != selected_topic:
            continue
        if selected_sentiment != "全部" and sentiment != selected_sentiment:
            continue
        if normalized_keyword and normalized_keyword not in f"{title} {content} {author}".lower():
            continue

        filtered_items.append(item)

    return filtered_items


def _render_evidence_command_strip(evidence_items):
    total_count = len(evidence_items)
    negative_count = _count_sentiment(evidence_items, "negative")
    positive_count = _count_sentiment(evidence_items, "positive")
    neutral_count = _count_sentiment(evidence_items, "neutral")
    platform_count = len({str(_get_item_value(item, "platform", fallback="未知")) for item in evidence_items})
    signal_text = "優先查核" if negative_count > 0 else "持續觀察"
    signal_class = "danger" if negative_count > 0 else "success"

    _render_html(f"""
<section class="pp-grid pp-grid-8-4">
    <article class="pp-card-highlight pp-evidence-command-main">
        <div class="pp-card-top"><div><div class="pp-card-kicker">目前查核結果</div><div class="pp-card-title">{total_count} 筆證據符合目前條件</div></div><div class="pp-badge {signal_class}">{signal_text}</div></div>
        <div class="pp-card-desc">本次結果涵蓋 {platform_count} 個公開來源，其中包含 {negative_count} 筆負向、{neutral_count} 筆中立與 {positive_count} 筆正向訊號。</div>
        <div class="pp-card-meta"><strong>建議閱讀順序</strong><br>先檢視負向內容與原始連結，再確認發布者、互動量與完整討論脈絡。</div>
    </article>
    <div class="pp-stack pp-evidence-command-side">
        <article class="pp-card-summary"><div class="pp-card-kicker">負向訊號</div><div class="pp-card-value">{negative_count}</div><div class="pp-card-title">需要優先確認</div></article>
        <article class="pp-card-summary"><div class="pp-card-kicker">來源分布</div><div class="pp-card-value">{platform_count}</div><div class="pp-card-title">公開平台</div></article>
    </div>
</section>
    """)


def _render_evidence_table(evidence_items):
    _section(
        "證",
        "公開證據",
        "證據結果",
        "檢視符合條件的來源、議題、情緒、發布者、互動量與原始連結。",
        len(evidence_items),
        "筆",
    )

    if not evidence_items:
        _render_html("""
<section class="pp-evidence-empty">
    <div class="pp-evidence-empty-icon">證</div>
    <div class="pp-evidence-empty-title">目前沒有符合條件的證據</div>
    <div class="pp-evidence-empty-desc">請調整查詢條件，或將篩選條件切換回「全部」重新檢視。</div>
</section>
        """)
        return

    rows_html = "".join(_build_evidence_row(item) for item in evidence_items)

    _render_html(f"""
<section class="pp-card-large pp-evidence-table-shell">
    <div class="pp-card-top">
        <div><div class="pp-card-kicker">公開來源明細</div><div class="pp-card-title">可追溯證據清單</div><div class="pp-card-desc">每一筆資料均保留來源、時間、發布者與原始連結。</div></div>
        <div class="pp-badge success">共 {len(evidence_items)} 筆</div>
    </div>
    <div class="pp-evidence-table-scroll">
        <table class="pp-evidence-table">
            <colgroup>
                <col style="width: 110px;"><col style="width: 130px;"><col style="width: 105px;"><col style="width: 320px;"><col style="width: 130px;"><col style="width: 90px;"><col style="width: 150px;"><col style="width: 105px;">
            </colgroup>
            <thead><tr><th>資料來源</th><th>討論議題</th><th>情緒狀態</th><th>證據內容</th><th>發布者</th><th>互動量</th><th>發布時間</th><th>原始連結</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
</section>
    """)


def _build_evidence_row(item):
    platform_raw = str(_get_item_value(item, "platform", fallback="未知"))
    topic_raw = str(_get_item_value(item, "topic", fallback="未分類"))
    sentiment_raw = str(_get_item_value(item, "sentiment", fallback="未知"))

    platform = _safe(platform_raw, "未知")
    topic = _safe(topic_raw, "未分類")
    sentiment = _safe(_sentiment_display(sentiment_raw), "未知")
    title = _safe(_get_item_value(item, "title", "content", fallback="未提供證據內容"), "未提供證據內容")
    author = _safe(_get_item_value(item, "author", fallback="未提供"), "未提供")
    engagement = _safe(_get_item_value(item, "engagement", fallback="—"), "—")
    published_time = _safe(_get_item_value(item, "published_time", fallback="未提供"), "未提供")
    original_url = str(_get_item_value(item, "original_url", "url", fallback="")).strip()

    sentiment_class = _sentiment_class(sentiment_raw)
    platform_class = _platform_class(platform_raw)
    link_html = _render_original_link(original_url)

    return f"""
<tr>
    <td><span class="pp-evidence-badge pp-evidence-badge-platform {platform_class}">{platform}</span></td>
    <td><span class="pp-evidence-badge pp-evidence-badge-topic">{topic}</span></td>
    <td><span class="pp-evidence-badge {sentiment_class}">{sentiment}</span></td>
    <td><div class="pp-evidence-title-cell">{title}</div></td>
    <td><div class="pp-evidence-author">{author}</div></td>
    <td><div class="pp-evidence-engagement">{engagement}</div></td>
    <td><div class="pp-evidence-date">{published_time}</div></td>
    <td>{link_html}</td>
</tr>
    """


def _render_original_link(original_url):
    if not original_url:
        return '<span class="pp-evidence-link pp-evidence-link-disabled">無連結</span>'

    safe_url = escape(original_url, quote=True)
    return f'<a class="pp-evidence-link" href="{safe_url}" target="_blank" rel="noopener noreferrer">查看來源</a>'


def _sentiment_display(sentiment):
    normalized = str(sentiment).strip().lower()

    if normalized == "全部":
        return "全部"
    if "正" in normalized or "positive" in normalized:
        return "正向"
    if "負" in normalized or "negative" in normalized:
        return "負向"
    if "中" in normalized or "neutral" in normalized:
        return "中立"

    return str(sentiment).strip() or "未知"


def _platform_class(platform):
    normalized = str(platform).strip().lower()
    platform_map = {
        "facebook": "pp-platform-facebook",
        "instagram": "pp-platform-instagram",
        "threads": "pp-platform-threads",
        "dcard": "pp-platform-dcard",
        "ptt": "pp-platform-ptt",
        "forum": "pp-platform-forum",
        "google review": "pp-platform-google-review",
        "youtube": "pp-platform-youtube",
        "mobile01": "pp-platform-mobile01",
        "news": "pp-platform-news",
        "blog": "pp-platform-blog",
    }
    return platform_map.get(normalized, "pp-platform-default")


def _sentiment_class(sentiment):
    normalized = str(sentiment).strip().lower()

    if "正" in normalized or "positive" in normalized:
        return "pp-evidence-badge-positive"
    if "負" in normalized or "negative" in normalized:
        return "pp-evidence-badge-negative"
    if "中" in normalized or "neutral" in normalized:
        return "pp-evidence-badge-neutral"

    return "pp-evidence-badge-unknown"


def _count_sentiment(evidence_items, target):
    count = 0

    for item in evidence_items:
        sentiment = str(_get_item_value(item, "sentiment", fallback="")).strip().lower()

        if target == "positive" and ("正" in sentiment or "positive" in sentiment):
            count += 1
        if target == "negative" and ("負" in sentiment or "negative" in sentiment):
            count += 1
        if target == "neutral" and ("中" in sentiment or "neutral" in sentiment):
            count += 1

    return count


def _top_value(evidence_items, key, fallback):
    counts = {}

    for item in evidence_items:
        value = str(_get_item_value(item, key, fallback="")).strip()

        if not value:
            continue

        counts[value] = counts.get(value, 0) + 1

    if not counts:
        return fallback

    return max(counts, key=counts.get)


def _render_decision_hint(evidence_items):
    negative_count = _count_sentiment(evidence_items, "negative")

    if negative_count > 0:
        badge_text = f"{negative_count} 筆負向訊號"
        badge_class = "warning"
        basis_title = "優先查核"
        basis_desc = "目前篩選結果含有需要主管優先確認的負向討論。"
    else:
        badge_text = "證據狀態穩定"
        badge_class = "success"
        basis_title = "持續觀察"
        basis_desc = "目前篩選結果未出現需要立即處理的負向訊號。"

    _section(
        "判",
        "主管判讀",
        "證據決策提示",
        "將目前證據狀態轉換為可立即執行的查核順序與行動建議。",
    )

    _render_html(f"""
<section class="pp-grid pp-grid-8-4">
    <article class="pp-card-highlight pp-evidence-decision-card">
        <div class="pp-card-top"><div class="pp-card-index">判</div><div class="pp-badge {badge_class}">{_safe(badge_text)}</div></div>
        <div class="pp-card-kicker">主管優先確認事項</div>
        <div class="pp-card-title">先確認來源，再決定是否需要回應或升級處理</div>
        <div class="pp-card-desc">證據中心的目的不是增加資訊量，而是協助主管快速判斷：哪一筆值得追、哪一筆需要回應、哪一筆可以持續觀察。</div>
        <div class="pp-evidence-decision-steps">
            <div class="pp-evidence-decision-step"><span>步驟 01</span><strong>確認原始來源與討論脈絡</strong></div>
            <div class="pp-evidence-decision-step"><span>步驟 02</span><strong>評估品牌、會員與營運影響</strong></div>
            <div class="pp-evidence-decision-step"><span>步驟 03</span><strong>安排品牌、客服或專案窗口</strong></div>
        </div>
    </article>
    <div class="pp-stack">
        <article class="pp-card-summary"><div class="pp-card-kicker">判讀結果</div><div class="pp-card-value">{negative_count}</div><div class="pp-card-title">{basis_title}</div><div class="pp-card-desc">{_safe(basis_desc)}</div></article>
        <article class="pp-card-summary"><div class="pp-card-kicker">執行原則</div><div class="pp-card-title">依據先於結論</div><div class="pp-card-desc">任何回應、澄清或任務指派，都應回到原始證據與實際脈絡。</div></article>
    </div>
</section>
    """)


if __name__ == "__main__":
    main()
