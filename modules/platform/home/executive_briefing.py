import html
import streamlit as st


def render_executive_briefing(experience):
    """
    Executive Briefing

    GM-11 Enterprise Product Identity：
    - Presentation Layer Only
    - 不修改 Experience Schema
    - 不修改首頁組裝
    - 統一使用 Enterprise Design System
    """

    decisions = getattr(experience, "decisions", []) or []

    _render_section_header(len(decisions))

    if not decisions:
        _render_empty_state()
        return

    st.markdown('<section class="pp-grid pp-grid-3">', unsafe_allow_html=True)

    for index, decision in enumerate(decisions, start=1):
        _render_decision_card(index, decision)

    st.markdown("</section>", unsafe_allow_html=True)


def _render_section_header(total_count):
    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">決</div>

            <div class="pp-section-copy">
                <div class="pp-card-kicker">主管決策中樞</div>
                <div class="pp-section-title">今日待決策</div>
                <div class="pp-section-subtitle">
                    彙整今日需要主管確認的關鍵事項，
                    讓團隊快速取得判斷並繼續推進。
                </div>
            </div>

            <div class="pp-badge gold">
                {total_count} 項待確認
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
                <div class="pp-card-index">決</div>
                <div class="pp-badge success">目前穩定</div>
            </div>

            <div class="pp-card-kicker">今日決策狀態</div>
            <div class="pp-card-title">今日暫無待決策事項</div>

            <div class="pp-card-desc">
                目前沒有需要主管立即確認的決策，
                請持續觀察關鍵指標、風險訊號與後續行動。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_decision_card(index, decision):
    title = _safe_text(
        _get_value(
            decision,
            "title",
            f"決策事項 {index}",
        )
    )
    description = _safe_text(
        _get_value(
            decision,
            "description",
            "目前沒有補充說明。",
        )
    )
    owner = _safe_text(
        _get_value(
            decision,
            "owner",
            "未指定",
        )
    )
    urgency = _safe_text(
        _get_value(
            decision,
            "urgency",
            "待確認",
        )
    )
    next_step = _safe_text(
        _get_value(
            decision,
            "next_step",
            "等待主管確認。",
        )
    )

    urgency_class = _urgency_class(urgency)

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card is-priority">
            <div class="pp-card-top">
                <div class="pp-card-index">{index:02d}</div>

                <div class="pp-badge {urgency_class}">
                    {urgency}
                </div>
            </div>

            <div class="pp-card-kicker">主管判斷事項</div>

            <div class="pp-card-title">
                {title}
            </div>

            <div class="pp-card-desc">
                {description}
            </div>

            <div class="pp-card-meta">
                <strong>負責窗口</strong><br>
                {owner}
            </div>

            <div class="pp-card-meta">
                <strong>優先程度</strong><br>
                {urgency}
            </div>

            <div class="pp-card-meta">
                <strong>建議下一步</strong><br>
                {next_step}
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


def _urgency_class(urgency):
    if any(word in urgency for word in ["高", "立即", "緊急", "重要"]):
        return "danger"

    if any(word in urgency for word in ["中", "今日", "觀察"]):
        return "gold"

    if any(word in urgency for word in ["低", "稍後", "一般"]):
        return "success"

    return "info"
