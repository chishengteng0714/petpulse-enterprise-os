
import html
import streamlit as st


def render_risk_radar(experience):
    """
    Risk Radar

    GM-11 Enterprise Product Identity
    - Presentation Layer Only
    - Design System Only
    """

    risks = getattr(experience, "risks", []) or []

    _render_section_header(len(risks))

    if not risks:
        _render_empty_state()
        return

    st.markdown('<section class="pp-grid pp-grid-2">', unsafe_allow_html=True)

    for index, risk in enumerate(risks, start=1):
        _render_risk_card(index, risk)

    st.markdown("</section>", unsafe_allow_html=True)


def _render_section_header(total_count):
    st.markdown(f"""
<section class="pp-section-header pp-enterprise-section-header">
<div class="pp-section-icon pp-enterprise-section-icon">警</div>
<div class="pp-section-copy">
<div class="pp-card-kicker">企業風險觀測</div>
<div class="pp-section-title">今日需要注意的風險訊號</div>
<div class="pp-section-subtitle">彙整可能影響品牌、營運與顧客體驗的重要風險，協助主管安排優先處理順序。</div>
</div>
<div class="pp-badge danger">{total_count} 項風險訊號</div>
</section>
""", unsafe_allow_html=True)


def _render_empty_state():
    st.markdown("""
<section class="pp-callout">
<div class="pp-card-top"><div class="pp-card-index">警</div><div class="pp-badge success">目前穩定</div></div>
<div class="pp-card-kicker">企業風險狀態</div>
<div class="pp-card-title">今日暫無明顯風險</div>
<div class="pp-card-desc">目前沒有需要立即升級處理的風險訊號，請持續觀察公開討論變化。</div>
</section>
""", unsafe_allow_html=True)


def _render_risk_card(index, risk):
    title=_safe_text(_get_value(risk,"title",f"風險訊號 {index}"))
    desc=_safe_text(_get_value(risk,"description","目前沒有補充說明。"))
    sev=_safe_text(_get_value(risk,"severity","觀察中"))
    act=_safe_text(_get_value(risk,"action","持續觀察並等待更多證據。"))
    st.markdown(f"""
<article class="pp-card pp-enterprise-card is-risk">
<div class="pp-card-top">
<div class="pp-card-index">{index:02d}</div>
<div class="pp-badge {_severity_class(sev)}">{sev}</div>
</div>
<div class="pp-card-kicker">企業風險訊號</div>
<div class="pp-card-title">{title}</div>
<div class="pp-card-desc">{desc}</div>
<div class="pp-card-meta"><strong>建議處理</strong><br>{act}</div>
</article>
""", unsafe_allow_html=True)


def _get_value(item,key,default=None):
    if item is None:
        return default
    if isinstance(item,dict):
        return item.get(key,default)
    return getattr(item,key,default)


def _safe_text(value):
    if value is None:
        return ""
    if hasattr(value,"value"):
        value=value.value
    return html.escape(str(value))


def _severity_class(severity):
    if any(w in severity for w in ["高","嚴重","立即","緊急"]):
        return "danger"
    if any(w in severity for w in ["中","注意","觀察"]):
        return "gold"
    if any(w in severity for w in ["低","輕微","穩定"]):
        return "success"
    return "info"
