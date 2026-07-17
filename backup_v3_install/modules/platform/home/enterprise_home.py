import streamlit as st
from html import escape
from pathlib import Path

from modules.platform.home.product_experience import build_enterprise_home_experience


def render_enterprise_home(runtime=None):
    _load_css()
    x = build_enterprise_home_experience()
    decisions = _items(x, "decisions"); risks = _items(x, "risks"); opportunities = _items(x, "opportunities"); workspaces = _items(x, "workspaces")
    health = _health(x); status = _safe(getattr(x, "operating_status", None), "穩定"); confidence = _safe(getattr(x, "confidence_level", None), "高")
    summary = _safe(getattr(x, "briefing_summary", None), getattr(x, "greeting", None) or "系統已整理今日品牌狀態與待辦事項。")
    statement = f"今日品牌狀態為{status}，有 {len(risks)} 項訊號值得優先確認。" if risks else f"今日品牌狀態為{status}，目前沒有需要立即升級的重大風險。"
    html = ['<main class="pp-page">', _hero(health,status,confidence,summary,statement,decisions,risks,opportunities), _kpis(health,decisions,risks,opportunities), _priority(decisions), _decision_queue(decisions), _signals(risks,opportunities), _workspaces(workspaces), '</main>']
    st.markdown(''.join(html), unsafe_allow_html=True)


def _load_css():
    path = Path(__file__).resolve().parents[3] / "assets" / "enterprise.css"
    if path.exists(): st.markdown(f"<style>{path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

def _safe(value, fallback=""):
    text = str(value).strip() if value is not None else ""
    return escape(text or str(fallback))

def _items(x, name): return getattr(x, name, []) or []

def _health(x):
    signals = _items(x, "health_signals")
    return _safe(getattr(signals[0], "value", None), "—") if signals else "—"

def _head(kicker,title,desc): return f'''<header class="pp-section-head"><div><div class="pp-kicker">{_safe(kicker)}</div><h2 class="pp-section-title">{_safe(title)}</h2><div class="pp-section-desc">{_safe(desc)}</div></div></header>'''

def _hero(health,status,confidence,summary,statement,decisions,risks,opportunities):
    return f'''<section class="pp-hero"><div><div class="pp-kicker">EXECUTIVE MORNING BRIEF</div><h1>今天品牌狀況</h1><div class="pp-hero-lead">{statement}</div><div class="pp-hero-copy">{summary}</div><div class="pp-hero-chips"><span class="pp-chip">營運狀態 {status}</span><span class="pp-chip">資料可信度 {confidence}</span></div></div><aside class="pp-hero-aside"><div class="pp-hero-aside-label">品牌健康</div><div class="pp-hero-score">{health}</div><div class="pp-hero-status">今日狀態</div><div class="pp-hero-meta-grid"><div><span>待決策</span><strong>{len(decisions)}</strong></div><div><span>風險</span><strong>{len(risks)}</strong></div><div><span>機會</span><strong>{len(opportunities)}</strong></div><div><span>信心</span><strong>{confidence}</strong></div></div></aside></section>'''

def _kpis(health,decisions,risks,opportunities):
    cards=[("品牌健康",health,"整體品牌狀態"),("待決策",len(decisions),"需要主管確認"),("風險訊號",len(risks),"建議優先查核"),("成長機會",len(opportunities),"值得安排下一步")]
    return '<div class="pp-kpi-grid">'+''.join(f'<article class="pp-kpi"><div class="pp-kpi-label">{a}</div><div class="pp-kpi-value">{b}</div><div class="pp-kpi-note">{c}</div></article>' for a,b,c in cards)+'</div>'

def _priority(decisions):
    if not decisions: title="目前沒有需要立即介入的決策"; copy="持續監測品牌狀態，並維持例行查核節奏。"; next_step="維持監測"
    else:
        item=decisions[0]; title=_safe(getattr(item,"title",None),"待決策事項"); copy=_safe(getattr(item,"description",None),"需要主管確認後安排下一步。"); next_step=_safe(getattr(item,"next_step",None),"確認影響範圍並安排處理窗口。")
    return f'''<section class="pp-section">{_head("TODAY'S PRIORITY","今天最重要的一件事","先處理最影響推進速度的判斷，再查看其餘訊號。")}<article class="pp-priority"><div><div class="pp-kicker">PRIORITY 01</div><div class="pp-priority-title">{title}</div><div class="pp-priority-copy">{copy}</div></div><aside class="pp-priority-action"><span>建議下一步</span><strong>{next_step}</strong></aside></article></section>'''

def _decision_queue(decisions):
    rest=decisions[1:4]
    if not rest: body='<div class="pp-empty">目前沒有其他待決策事項。</div>'
    else:
        rows=[]
        for i,item in enumerate(rest,start=2):
            rows.append(f'''<article class="pp-list-item"><div class="pp-list-index">{i:02d}</div><div><div class="pp-list-title">{_safe(getattr(item,'title',None),'待確認事項')}</div><div class="pp-list-copy">{_safe(getattr(item,'description',None),'確認影響與下一步。')}</div></div></article>''')
        body='<div class="pp-list">'+''.join(rows)+'</div>'
    return f'''<section class="pp-section">{_head("DECISION QUEUE","其餘待決策事項","依優先順序閱讀，不讓所有事情同時搶走注意力。")} {body}</section>'''

def _feed(items,title,empty,cls=""):
    if not items: return f'<article class="pp-card {cls}"><div class="pp-kicker">{title}</div><div class="pp-card-copy">{empty}</div></article>'
    rows=[]
    for item in items[:4]: rows.append(f'<article class="pp-list-item"><div class="pp-list-index">•</div><div><div class="pp-list-title">{_safe(getattr(item,"title",None),"情報訊號")}</div><div class="pp-list-copy">{_safe(getattr(item,"description",None),"持續追蹤後續變化。")}</div></div></article>')
    return f'<article class="pp-card {cls}"><div class="pp-kicker">{title}</div><div class="pp-list" style="margin-top:14px">{"".join(rows)}</div></article>'

def _signals(risks,opportunities): return f'''<section class="pp-section">{_head("SIGNALS","風險與機會","兩種訊號並列，避免決策只剩危機或只剩樂觀。")}<div class="pp-grid-2">{_feed(risks,"風險訊號","目前沒有重大風險。")}{_feed(opportunities,"成長機會","目前沒有新的機會訊號。")}</div></section>'''

def _workspaces(items):
    cards=[]
    for i,item in enumerate(items[:3],start=1): cards.append(f'''<article class="pp-card"><div class="pp-kicker">WORKSPACE {i:02d}</div><div class="pp-card-title">{_safe(getattr(item,'title',None),'工作入口')}</div><div class="pp-card-copy">{_safe(getattr(item,'description',None),'查看詳細資料並安排下一步。')}</div><div class="pp-card-meta"><span>{_safe(getattr(item,'status',None),'可使用')}</span></div></article>''')
    body='<div class="pp-grid-3">'+''.join(cards)+'</div>' if cards else '<div class="pp-empty">目前沒有可用工作入口。</div>'
    return f'''<section class="pp-section">{_head("NEXT STEP","去哪裡處理","從今日判斷直接前往對應工作區。")} {body}</section>'''
