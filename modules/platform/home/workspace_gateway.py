import html
import streamlit as st


def render_workspace_gateway(experience):
    """
    Workspace Gateway

    GM-11 Enterprise Product Identity
    - Presentation Layer Only
    - Design System Only
    """

    workspaces = getattr(experience, "workspaces", []) or []

    _render_section_header(len(workspaces))

    if not workspaces:
        _render_empty_state()
        return

    st.markdown('<section class="pp-grid pp-grid-3">', unsafe_allow_html=True)

    for index, workspace in enumerate(workspaces, start=1):
        _render_workspace_card(index, workspace)

    st.markdown("</section>", unsafe_allow_html=True)


def _render_section_header(total_count):
    st.markdown(f"""
<section class="pp-section-header pp-enterprise-section-header">
<div class="pp-section-icon pp-enterprise-section-icon">行</div>
<div class="pp-section-copy">
<div class="pp-card-kicker">下一步行動</div>
<div class="pp-section-title">今日建議進入的工作區</div>
<div class="pp-section-subtitle">將今日判斷轉換為可立即執行的工作入口，協助團隊快速推進。</div>
</div>
<div class="pp-badge gold">{total_count} 個入口</div>
</section>
""", unsafe_allow_html=True)


def _render_empty_state():
    st.markdown("""
<section class="pp-callout">
<div class="pp-card-top"><div class="pp-card-index">行</div><div class="pp-badge info">等待指派</div></div>
<div class="pp-card-kicker">工作入口</div>
<div class="pp-card-title">今日暫無建議工作入口</div>
<div class="pp-card-desc">目前沒有需要立即切換的工作區，請先完成今日決策判斷。</div>
</section>
""", unsafe_allow_html=True)


def _render_workspace_card(index, workspace):
    title=_safe_text(_get_value(workspace,"title",f"工作區 {index}"))
    description=_safe_text(_get_value(workspace,"description","目前沒有補充說明。"))
    status=_safe_text(_get_value(workspace,"status","可進入"))
    target=_safe_text(_get_value(workspace,"target","未指定"))
    st.markdown(f"""
<article class="pp-card pp-enterprise-card is-priority">
<div class="pp-card-top">
<div class="pp-card-index">{index:02d}</div>
<div class="pp-badge {_status_class(status)}">{status}</div>
</div>
<div class="pp-card-kicker">決策執行入口</div>
<div class="pp-card-title">{title}</div>
<div class="pp-card-desc">{description}</div>
<div class="pp-card-meta"><strong>目標工作區</strong><br>{target}</div>
</article>
""", unsafe_allow_html=True)


def _get_value(item,key,default=None):
    if item is None:return default
    if isinstance(item,dict): return item.get(key,default)
    return getattr(item,key,default)

def _safe_text(value):
    if value is None:return ""
    if hasattr(value,"value"): value=value.value
    return html.escape(str(value))

def _status_class(status):
    if any(w in status for w in ["可用","可進入","啟用","完成"]): return "success"
    if any(w in status for w in ["建置","準備","待確認","規劃"]): return "gold"
    if any(w in status for w in ["暫停","停用","不可用"]): return "danger"
    return "info"
