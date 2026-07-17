import json
import re
import subprocess
import sys
from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st

from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPDATE_SCRIPT = PROJECT_ROOT / "update_evidence.py"
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence.json"

_ICON_HEALTH = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 21s-7-4.35-7-10a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 5.65-7 10-7 10z"/>'
    "</svg>"
)
_ICON_SIGNAL = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M4 19h16"/><path d="M7 15V9"/><path d="M12 15V5"/>'
    '<path d="M17 15v-7"/>'
    "</svg>"
)
_ICON_NEGATIVE = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 9v4"/><path d="M12 17h.01"/>'
    '<circle cx="12" cy="12" r="9"/>'
    "</svg>"
)
_ICON_RISK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
    '<path d="M12 9v4"/><path d="M12 17h.01"/>'
    "</svg>"
)
_ICON_DECISION = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'
    "</svg>"
)
_ICON_OPPORTUNITY = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/>'
    "</svg>"
)
_ICON_WORKSPACE = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3" y="3" width="7" height="7" rx="1"/>'
    '<rect x="14" y="3" width="7" height="7" rx="1"/>'
    '<rect x="3" y="14" width="7" height="7" rx="1"/>'
    '<rect x="14" y="14" width="7" height="7" rx="1"/>'
    "</svg>"
)
_ICON_CLIPBOARD = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M9 5h6a2 2 0 0 1 2 2v1H7V7a2 2 0 0 1 2-2z"/>'
    '<rect x="5" y="8" width="14" height="13" rx="2"/>'
    "</svg>"
)
_ICON_FILE_CHECK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7z"/>'
    '<path d="M14 2v5h5"/><path d="m9 15 2 2 4-4"/>'
    "</svg>"
)
_ICON_LAYERS = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 2 2 7l10 5 10-5-10-5z"/>'
    '<path d="m2 12 10 5 10-5"/>'
    '<path d="m2 17 10 5 10-5"/>'
    "</svg>"
)
_ICON_SYNC = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
    '<path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>'
    '<path d="M16 16h5v5"/>'
    "</svg>"
)
_ICON_ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>'
    "</svg>"
)


def render_enterprise_home(runtime=None):
    """
    PetPulse Enterprise OS v3.0 GM33 Executive Art Direction

    Presentation Layer Only
    """

    _load_enterprise_css()

    _render_update_control()

    experience = build_enterprise_home_experience()

    html = (
        '<div class="pp32-page">'
        + _render_hero(experience)
        + _render_decision_queue(experience)
        + _render_metrics_rail(experience)
        + _render_signal_intelligence(experience)
        + _render_workspace_gateway(experience)
        + "</div>"
    )

    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _render_update_control() -> None:
    evidence_count, last_updated = _load_evidence_status()

    if st.session_state.pop("evidence_update_success", False):
        updated_count = st.session_state.pop(
            "evidence_update_count",
            evidence_count,
        )
        st.success(
            f"資料更新完成，目前已載入 {updated_count} 筆品牌情報。"
        )

    status_title, status_meta = _resolve_update_status(
        evidence_count,
        last_updated,
    )

    left, right = st.columns(
        [4.6, 1],
        vertical_alignment="center",
    )

    with left:
        st.markdown(
            (
                '<div class="pp32-update-bar">'
                f'<span class="pp32-update-icon pp32-icon">{_ICON_SYNC}</span>'
                '<div class="pp32-update-copy">'
                f"<strong>{escape(status_title)}</strong>"
                f"<span>{escape(status_meta)} · {evidence_count} 筆情報</span>"
                "</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    with right:
        if st.button(
            "立即更新資料",
            type="primary",
            use_container_width=True,
            key="petpulse_home_update",
        ):
            _run_evidence_update()


def _load_evidence_status() -> tuple[int, str]:
    if not EVIDENCE_FILE.exists():
        return 0, "尚未建立資料"

    try:
        with EVIDENCE_FILE.open("r", encoding="utf-8") as file:
            evidence_data = json.load(file)

        evidence_count = _count_evidence_items(evidence_data)
        modified_datetime = datetime.fromtimestamp(
            EVIDENCE_FILE.stat().st_mtime
        )
        last_updated = modified_datetime.strftime("%Y/%m/%d %H:%M")

        return evidence_count, last_updated
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 0, "資料讀取異常"


def _count_evidence_items(evidence_data: object) -> int:
    if isinstance(evidence_data, list):
        return len(evidence_data)

    if not isinstance(evidence_data, dict):
        return 0

    possible_items = (
        evidence_data.get("evidence_items")
        or evidence_data.get("evidence")
        or evidence_data.get("items")
        or evidence_data.get("articles")
        or evidence_data.get("data")
        or []
    )

    return len(possible_items) if isinstance(possible_items, list) else 0


def _run_evidence_update() -> None:
    if not UPDATE_SCRIPT.exists():
        st.error("找不到 update_evidence.py。")
        return

    try:
        with st.spinner("正在同步最新品牌情報…"):
            completed = subprocess.run(
                [sys.executable, str(UPDATE_SCRIPT)],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                check=False,
            )
    except Exception as exc:
        st.error(f"更新失敗：{exc}")
        return

    if completed.returncode != 0:
        message = (
            completed.stderr.strip()
            or completed.stdout.strip()
            or "更新程序回傳錯誤。"
        )
        st.error(message)
        return

    new_count, _ = _load_evidence_status()
    st.session_state["evidence_update_success"] = True
    st.session_state["evidence_update_count"] = new_count
    st.rerun()


def _resolve_update_status(
    evidence_count: int,
    last_updated: str,
) -> tuple[str, str]:
    if last_updated == "資料讀取異常":
        return (
            "資料狀態異常",
            "目前無法讀取資料檔案，請重新執行更新。",
        )

    if evidence_count <= 0:
        return (
            "尚未載入品牌情報",
            f"最後狀態：{last_updated}",
        )

    return (
        "品牌情報資料已同步",
        f"最後更新 {last_updated} · 系統目前可供決策查閱",
    )


def _load_enterprise_css():
    css_path = Path(__file__).resolve().parents[3] / "assets" / "enterprise.css"

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def _load_analysis_snapshot():
    candidates = (
        PROJECT_ROOT.parent / "data" / "analysis.json",
        PROJECT_ROOT / "data" / "analysis.json",
    )

    for path in candidates:
        if not path.exists():
            continue

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            continue

        return {
            "total": data.get("evidence_count")
            or data.get("brand_signal_count")
            or 0,
            "positive": data.get("positive", 0),
            "negative": data.get("negative", 0),
            "high_risk": data.get("high_risk_count", 0),
        }

    return {
        "total": 0,
        "positive": 0,
        "negative": 0,
        "high_risk": 0,
    }


def _compact_html(markup):
    return "".join(
        line.strip()
        for line in str(markup).splitlines()
        if line.strip()
    )


def _safe(value, fallback=""):
    text = str(value).strip() if value is not None else ""
    if not text:
        text = str(fallback)
    return escape(text)


def _items(experience, field_name):
    return getattr(experience, field_name, []) or []


def _health_value(experience):
    items = _items(experience, "health_signals")
    if items:
        return _safe(getattr(items[0], "value", None), "待確認")
    return "待確認"


def _kpi_parts(value, default_unit=""):
    text = str(value).strip() if value is not None else ""
    if not text:
        return escape("0"), escape(default_unit)

    match = re.match(r"^([\d.,]+)\s*(.*)$", text)
    if match:
        number = match.group(1)
        unit = match.group(2).strip() or default_unit
        return escape(number), escape(unit)

    return escape(text), escape(default_unit)


def _kpi_cell(cell_class, icon, status, label, value, unit_default=""):
    number, unit = _kpi_parts(value, unit_default)
    unit_html = (
        f'<span class="pp32-kpi-cell-unit">{unit}</span>'
        if unit
        else ""
    )
    return f"""
<div class="pp32-kpi-cell {cell_class}">
<div class="pp32-kpi-cell-top">
<span class="pp32-kpi-cell-icon pp32-icon">{icon}</span>
<span class="pp32-kpi-cell-tag">{status}</span>
</div>
<span class="pp32-kpi-cell-label">{label}</span>
<div class="pp32-kpi-cell-value"><strong>{number}</strong>{unit_html}</div>
</div>
"""


def _short_signal_copy(value, fallback, max_len=72):
    text = str(value).strip() if value is not None else ""
    if not text:
        text = fallback

    boilerplate = "此風險由最新 AI 品牌情報分析辨識，仍應回到原始證據確認細節。"
    if boilerplate in text:
        return escape("AI 初判，請至證據中心確認來源。")

    if len(text) > max_len:
        text = text[: max_len - 1].rstrip("，、；： ") + "…"

    return escape(text)


def _workspace_icon(index):
    icons = {
        1: _ICON_CLIPBOARD,
        2: _ICON_FILE_CHECK,
        3: _ICON_LAYERS,
    }
    return icons.get(index, _ICON_CLIPBOARD)


def _executive_summary(value, fallback):
    text = str(value).strip() if value is not None else ""
    if not text:
        text = fallback

    sentences = re.split(r"(?<=[。！？!?])\s*", text)
    concise = "".join(sentence for sentence in sentences[:2] if sentence).strip()

    if len(concise) > 180:
        concise = concise[:177].rstrip("，、；： ") + "…"

    return escape(concise)


def _render_hero(experience):
    title = _safe(getattr(experience, "briefing_title", None), "今日品牌情報判斷")
    summary = _executive_summary(
        getattr(experience, "briefing_summary", None),
        "今日品牌目前穩定。目前未發現重大負向事件，但有幾項決策值得今天完成。建議先確認促銷策略與執行責任，避免短期成長影響長期品牌價值。",
    )
    status = _safe(getattr(experience, "operating_status", None), "穩定")
    confidence = _safe(getattr(experience, "confidence_level", None), "高")

    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")
    snapshot = _load_analysis_snapshot()
    health_value = _health_value(experience)

    return f"""
<section class="pp32-hero">
<div class="pp32-hero-main">
<div class="pp32-hero-eyebrow">Executive Brief</div>
<h1 class="pp32-hero-title">{title}</h1>
<p class="pp32-hero-summary">{summary}</p>
<div class="pp32-hero-tags">
<span class="pp32-tag green">品牌健康 {health_value}</span>
<span class="pp32-tag">營運狀態 {status}</span>
<span class="pp32-tag">資料可信度 {confidence}</span>
<span class="pp32-tag gold">待決策 {len(decisions)} 項</span>
<span class="pp32-tag">風險 {len(risks)} · 機會 {len(opportunities)}</span>
</div>
</div>
<aside class="pp32-kpi-cluster">
{_kpi_cell("health", _ICON_HEALTH, "品牌", "品牌健康度", health_value, "")}
{_kpi_cell("signals", _ICON_SIGNAL, "訊號", "有效品牌訊號", snapshot["total"], "筆")}
{_kpi_cell("negative", _ICON_NEGATIVE, "負向", "負向訊號", snapshot["negative"], "筆")}
{_kpi_cell("risk", _ICON_RISK, "風險", "高風險訊號", snapshot["high_risk"], "筆")}
</aside>
</section>
"""


def _render_metrics_rail(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")
    health_value = _health_value(experience)

    health_display = escape(str(health_value).strip() if health_value else "—")

    return f"""
<section class="pp32-section">
<div class="pp32-section-head">
<div>
<div class="pp32-section-eyebrow">Enterprise Metrics</div>
<div class="pp32-section-title">今日企業指標</div>
<div class="pp32-section-desc">以既有資料呈現品牌健康、決策負載與訊號分布。</div>
</div>
</div>
<div class="pp32-data-rail">
<article class="pp32-data-rail-item">
<span class="pp32-data-rail-label">品牌健康</span>
<strong class="pp32-data-rail-value">{health_display}</strong>
<small class="pp32-data-rail-sub">目前整體品牌狀態</small>
</article>
<article class="pp32-data-rail-item">
<span class="pp32-data-rail-label">今日待決策</span>
<strong class="pp32-data-rail-value">{len(decisions)}</strong>
<small class="pp32-data-rail-sub">今天需要主管確認</small>
</article>
<article class="pp32-data-rail-item">
<span class="pp32-data-rail-label">風險訊號</span>
<strong class="pp32-data-rail-value">{len(risks)}</strong>
<small class="pp32-data-rail-sub">確認影響與來源</small>
</article>
<article class="pp32-data-rail-item">
<span class="pp32-data-rail-label">值得投入</span>
<strong class="pp32-data-rail-value">{len(opportunities)}</strong>
<small class="pp32-data-rail-sub">安排小規模驗證</small>
</article>
</div>
</section>
"""


def _render_decision_queue(experience):
    items = _items(experience, "decisions")

    if not items:
        return """
<section class="pp32-section">
<div class="pp32-section-head">
<div><div class="pp32-section-eyebrow">Decision Queue</div>
<div class="pp32-section-title">今日待決策</div>
<div class="pp32-section-desc">主管應優先確認的品牌情報。</div></div>
<span class="pp32-section-count">0 項</span></div>
<div class="pp32-empty">目前沒有需要主管立即拍板的事項。</div>
</section>
"""

    primary = items[0]
    title = _safe(getattr(primary, "title", None), "待決策事項")
    description = _safe(
        getattr(primary, "description", None),
        "需要主管確認後才能繼續推進。",
    )
    urgency = _safe(getattr(primary, "urgency", None), "今天完成")
    owner = _safe(getattr(primary, "owner", None), "待主管指定")
    next_step = _safe(
        getattr(primary, "next_step", None),
        "確認負責人、完成期限與是否立即執行。",
    )

    queue = ""
    for index, item in enumerate(items[1:3], start=2):
        card_class = "opportunity" if index == 2 else "neutral"
        item_title = _safe(getattr(item, "title", None), "待決策事項")
        item_reason = _safe(
            getattr(item, "description", None),
            "需要主管確認後才能繼續推進。",
        )
        item_action = _safe(
            getattr(item, "next_step", None),
            "確認負責人、完成期限與是否立即執行。",
        )
        item_status = _safe(getattr(item, "urgency", None), "待確認")
        queue += f"""
<article class="pp32-priority-card secondary {card_class}">
<div class="pp32-priority-card-head">
<span class="pp32-priority-index">{index:02d}</span>
<span class="pp32-priority-status">{item_status}</span>
</div>
<h4 class="pp32-clamp-2">{item_title}</h4>
<p class="pp32-clamp-3">{item_reason}</p>
<div class="pp32-priority-card-meta pp32-clamp-2">建議行動：{item_action}</div>
</article>
"""

    if not queue:
        queue = ""

    return f"""
<section class="pp32-section">
<div class="pp32-section-head">
<div><div class="pp32-section-eyebrow">Decision Queue</div>
<div class="pp32-section-title">今日待決策</div>
<div class="pp32-section-desc">主管應優先確認的品牌情報，先完成影響最大的決策。</div></div>
<span class="pp32-section-count">{len(items)} 項</span></div>
<div class="pp32-decision-grid">
<article class="pp32-priority-executive">
<div class="pp32-priority-executive-inner">
<div class="pp32-priority-main">
<div class="pp32-priority-top">
<span class="pp32-priority-badge">Top Priority</span>
<span class="pp32-tag gold">{urgency}</span>
</div>
<h3 class="pp32-priority-title pp32-clamp-2">{title}</h3>
<p class="pp32-priority-reason pp32-clamp-3">{description}</p>
</div>
<aside class="pp32-priority-executive-meta">
<div><span>Owner</span><strong>{owner}</strong></div>
<div><span>Recommended Action</span><strong>{next_step}</strong></div>
<div><span>Status</span><strong>{urgency}</strong></div>
</aside>
</div>
</article>
{queue}
</div>
</section>
"""


def _render_signal_intelligence(experience):
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")

    risk_rows = ""
    for item in risks[:3]:
        risk_title = _safe(getattr(item, "title", None), "風險訊號")
        risk_summary = _short_signal_copy(
            getattr(item, "description", None),
            "需要持續追蹤。",
        )
        risk_action = _safe(getattr(item, "action", None), "安排後續確認。")
        risk_rows += f"""
<div class="pp32-signal-item">
<span class="pp32-signal-mark danger pp32-icon">{_ICON_RISK}</span>
<div><strong class="pp32-clamp-2 pp32-clamp-title">{risk_title}</strong>
<p class="pp32-clamp-3 pp32-clamp-summary">{risk_summary}</p>
<small class="pp32-clamp-2 pp32-clamp-action">今天建議：{risk_action}</small></div>
</div>
"""
    if not risk_rows:
        risk_rows = '<div class="pp32-empty">目前沒有重大風險訊號。</div>'

    opportunity_rows = ""
    for item in opportunities[:3]:
        opp_title = _safe(getattr(item, "title", None), "值得投入")
        opp_summary = _short_signal_copy(
            getattr(item, "description", None),
            "具備進一步驗證價值。",
        )
        opp_action = _safe(getattr(item, "recommendation", None), "安排小規模測試。")
        opportunity_rows += f"""
<div class="pp32-signal-item">
<span class="pp32-signal-mark opportunity pp32-icon">{_ICON_OPPORTUNITY}</span>
<div><strong class="pp32-clamp-2 pp32-clamp-title">{opp_title}</strong>
<p class="pp32-clamp-3 pp32-clamp-summary">{opp_summary}</p>
<small class="pp32-clamp-2 pp32-clamp-action">值得投入：{opp_action}</small></div>
</div>
"""
    if not opportunity_rows:
        opportunity_rows = '<div class="pp32-empty">目前沒有需要立即投入的機會。</div>'

    return f"""
<section class="pp32-section">
<div class="pp32-section-head">
<div><div class="pp32-section-eyebrow">Signal Intelligence</div>
<div class="pp32-section-title">今天要留意</div>
<div class="pp32-section-desc">將需要防守與值得投入的訊號放在同一個決策視窗。</div></div>
<span class="pp32-section-count">{len(risks) + len(opportunities)} 項</span></div>
<div class="pp32-intel-split">
<article class="pp32-intel-panel risk">
<div class="pp32-intel-head"><span class="pp32-intel-badge risk">Risk Intelligence</span></div>
<div class="pp32-intel-list">{risk_rows}</div>
</article>
<article class="pp32-intel-panel opportunity">
<div class="pp32-intel-head"><span class="pp32-intel-badge opportunity">Opportunity Intelligence</span></div>
<div class="pp32-intel-list">{opportunity_rows}</div>
</article>
</div>
</section>
"""


def _workspace_category(index):
    labels = {
        1: "Task Assignment",
        2: "Evidence Review",
        3: "Deep Dive",
    }
    return labels.get(index, "Executive Workspace")


def _render_workspace_gateway(experience):
    items = _items(experience, "workspaces")
    health_value = _health_value(experience)
    operating_status = _safe(getattr(experience, "operating_status", None), "穩定")
    confidence_level = _safe(getattr(experience, "confidence_level", None), "高")
    health_number, health_unit = _kpi_parts(health_value, "")

    cards = ""
    for index, item in enumerate(items, start=1):
        is_disabled = index == 3
        card_class = " is-disabled" if is_disabled else " is-active"
        item_status = (
            "規劃中"
            if is_disabled
            else _safe(getattr(item, "status", None), "使用中")
        )
        arrow_html = (
            ""
            if is_disabled
            else f'<span class="pp32-workspace-arrow pp32-icon">{_ICON_ARROW}</span>'
        )
        cards += f"""
<article class="pp32-workspace-card{card_class}">
<span class="pp32-workspace-eyebrow">{_workspace_category(index)}</span>
<span class="pp32-workspace-icon pp32-icon">{_workspace_icon(index)}</span>
<h4>{_safe(getattr(item, "title", None), "工作入口")}</h4>
<p>{_safe(getattr(item, "description", None), "建立負責人、安排時程並追蹤結果。")}</p>
<div class="pp32-workspace-footer">
<span class="pp32-workspace-status">{item_status}</span>
{arrow_html}
</div>
</article>
"""

    if not cards:
        cards = '<div class="pp32-empty">目前沒有可用工作入口。</div>'

    return f"""
<section class="pp32-section">
<div class="pp32-section-head">
<div><div class="pp32-section-eyebrow">Next Step</div>
<div class="pp32-section-title">開始執行</div>
<div class="pp32-section-desc">完成決策後，直接建立任務、安排時程並追蹤結果。</div></div>
<span class="pp32-section-count">{len(items)} 個</span></div>
<div class="pp32-workspace-layout">
<div class="pp32-workspace-grid">{cards}</div>
<aside class="pp32-health-summary">
<span class="pp32-health-summary-label">Enterprise Health</span>
<strong class="pp32-health-summary-value">{health_number}<small>{health_unit}</small></strong>
<div class="pp32-health-summary-meta">
<span>營運狀態 {operating_status}</span>
<span>資料可信度 {confidence_level}</span>
</div>
</aside>
</div>
</section>
"""


__all__ = [
    "render_enterprise_home",
]
