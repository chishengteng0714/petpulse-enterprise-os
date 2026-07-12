import html
import streamlit as st


def render_enterprise_health(experience):
    """
    Enterprise Health

    GM-11 Enterprise Product Identity：
    - Presentation Layer Only
    - 不修改 Experience Schema
    - 不修改首頁組裝
    - 統一使用 Enterprise Design System
    """

    health_signals = getattr(experience, "health_signals", []) or []

    _render_section_header(len(health_signals))

    if not health_signals:
        _render_empty_state()
        return

    st.markdown('<section class="pp-grid pp-grid-4">', unsafe_allow_html=True)

    for index, signal in enumerate(health_signals[:4], start=1):
        _render_health_card(index, signal)

    st.markdown("</section>", unsafe_allow_html=True)


def _render_section_header(total_count):
    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">衡</div>

            <div class="pp-section-copy">
                <div class="pp-card-kicker">企業健康總覽</div>
                <div class="pp-section-title">今日企業營運健康</div>
                <div class="pp-section-subtitle">
                    快速掌握今日最重要的營運訊號，
                    協助主管判斷是否需要立即介入。
                </div>
            </div>

            <div class="pp-badge gold">
                {total_count} 項核心指標
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
                <div class="pp-card-index">衡</div>
                <div class="pp-badge success">目前穩定</div>
            </div>

            <div class="pp-card-kicker">企業健康狀態</div>
            <div class="pp-card-title">今日暫無關鍵指標</div>

            <div class="pp-card-desc">
                目前沒有需要立即檢視的營運指標，
                請持續觀察後續資料與企業健康訊號。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_health_card(index, signal):
    label = _safe_text(
        _get_value(
            signal,
            "label",
            f"指標 {index}",
        )
    )
    value = _safe_text(
        _get_value(
            signal,
            "value",
            "未提供",
        )
    )
    status = _safe_text(
        _get_value(
            signal,
            "status",
            "觀察中",
        )
    )
    detail = _safe_text(
        _get_value(
            signal,
            "detail",
            "目前沒有補充說明。",
        )
    )

    status_class = _status_class(status)
    card_class = _card_class(status)

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card {card_class}">
            <div class="pp-card-top">
                <div class="pp-card-index">{index:02d}</div>

                <div class="pp-badge {status_class}">
                    {status}
                </div>
            </div>

            <div class="pp-card-kicker">企業健康訊號</div>

            <div class="pp-card-value">
                {value}
            </div>

            <div class="pp-card-title">
                {label}
            </div>

            <div class="pp-card-desc">
                {detail}
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


def _status_class(status):
    if any(word in status for word in ["正常", "穩定", "良好", "正向"]):
        return "success"

    if any(word in status for word in ["注意", "觀察", "待確認"]):
        return "gold"

    if any(word in status for word in ["風險", "異常", "下降", "負向"]):
        return "danger"

    return "info"


def _card_class(status):
    if any(word in status for word in ["風險", "異常", "下降", "負向"]):
        return "is-risk"

    if any(word in status for word in ["正常", "穩定", "良好", "正向"]):
        return "is-opportunity"

    return "is-neutral"
