import html
import streamlit as st


def render_opportunity_radar(experience):
    """
    Opportunity Radar

    GM-11 Enterprise Product Identity：
    - Presentation Layer Only
    - 不修改 Experience Schema
    - 不修改首頁組裝
    - 統一使用 Enterprise Design System
    """

    opportunities = getattr(experience, "opportunities", []) or []

    _render_section_header(len(opportunities))

    if not opportunities:
        _render_empty_state()
        return

    st.markdown('<section class="pp-grid pp-grid-2">', unsafe_allow_html=True)

    for index, opportunity in enumerate(opportunities, start=1):
        _render_opportunity_card(index, opportunity)

    st.markdown("</section>", unsafe_allow_html=True)


def _render_section_header(total_count):
    st.markdown(
        f"""
        <section class="pp-section-header pp-enterprise-section-header">
            <div class="pp-section-icon pp-enterprise-section-icon">增</div>

            <div class="pp-section-copy">
                <div class="pp-card-kicker">企業成長雷達</div>
                <div class="pp-section-title">今日值得投入的成長機會</div>
                <div class="pp-section-subtitle">
                    彙整具備成長潛力的公開訊號與營運切入點，
                    協助主管判斷是否安排驗證、資源投入或後續行動。
                </div>
            </div>

            <div class="pp-badge success">
                {total_count} 項成長機會
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
                <div class="pp-card-index">增</div>
                <div class="pp-badge info">持續觀察</div>
            </div>

            <div class="pp-card-kicker">企業成長狀態</div>
            <div class="pp-card-title">今日暫無明顯成長機會</div>

            <div class="pp-card-desc">
                目前沒有需要立即安排驗證或資源投入的機會訊號，
                請持續觀察市場、會員與營運變化。
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _render_opportunity_card(index, opportunity):
    title = _safe_text(
        _get_value(
            opportunity,
            "title",
            f"成長機會 {index}",
        )
    )
    description = _safe_text(
        _get_value(
            opportunity,
            "description",
            "目前沒有補充說明。",
        )
    )
    potential = _safe_text(
        _get_value(
            opportunity,
            "potential",
            "待確認",
        )
    )
    recommendation = _safe_text(
        _get_value(
            opportunity,
            "recommendation",
            "建議持續觀察並等待更多證據。",
        )
    )

    potential_class = _potential_class(potential)

    st.markdown(
        f"""
        <article class="pp-card pp-enterprise-card is-opportunity">
            <div class="pp-card-top">
                <div class="pp-card-index">{index:02d}</div>

                <div class="pp-badge {potential_class}">
                    {potential}
                </div>
            </div>

            <div class="pp-card-kicker">企業成長機會</div>

            <div class="pp-card-title">
                {title}
            </div>

            <div class="pp-card-desc">
                {description}
            </div>

            <div class="pp-card-meta">
                <strong>建議行動</strong><br>
                {recommendation}
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


def _potential_class(potential):
    if any(word in potential for word in ["高", "強", "明顯", "立即"]):
        return "success"

    if any(word in potential for word in ["中", "觀察", "可驗證"]):
        return "gold"

    if any(word in potential for word in ["低", "輕微", "初步"]):
        return "info"

    return "info"
