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
ENTERPRISE_CSS_FILE = PROJECT_ROOT / "assets" / "enterprise.css"

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
_ICON_OPPORTUNITY = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="9"/><path d="M12 8v8"/><path d="M8 12h8"/>'
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
    """PetPulse Enterprise OS v4.0 — Presentation Layer Only."""

    _load_enterprise_css()
    _render_utility_bar()

    experience = build_enterprise_home_experience()

    html = (
        '<div class="pp4-page">'
        + _render_executive_hero(experience)
        + _render_decision_queue(experience)
        + _render_signal_intelligence(experience)
        + _render_action_workspace(experience)
        + "</div>"
    )

    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _load_enterprise_css() -> None:
    if not ENTERPRISE_CSS_FILE.exists():
        return

    try:
        css = ENTERPRISE_CSS_FILE.read_text(encoding="utf-8")
    except OSError:
        return

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _render_utility_bar() -> None:
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

    left, right = st.columns([4.6, 1], vertical_alignment="center")

    with left:
        st.markdown(
            (
                '<div class="pp4-utility">'
                f'<span class="pp4-utility-icon pp4-icon">{_ICON_SYNC}</span>'
                '<div class="pp4-utility-copy">'
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


def _render_executive_hero(experience):
    title = _safe(getattr(experience, "briefing_title", None), "今日品牌情報判斷")
    summary = _brief_summary(
        getattr(experience, "briefing_summary", None),
        "今日品牌目前穩定。目前未發現重大負向事件，但有幾項決策值得今天完成。",
    )
    status = _safe(getattr(experience, "operating_status", None), "穩定")
    confidence = _safe(getattr(experience, "confidence_level", None), "高")
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")
    snapshot = _load_analysis_snapshot()
    health_value = _health_value(experience)

    tags = [
        f'<span class="pp4-tag is-brand">品牌健康 {health_value}</span>',
        f'<span class="pp4-tag">營運 {status}</span>',
        f'<span class="pp4-tag">可信度 {confidence}</span>',
        f'<span class="pp4-tag">待決策 {len(decisions)}</span>',
    ]

    return f"""
<section class="pp4-hero">
<div class="pp4-hero-main">
<div class="pp4-eyebrow">主管晨間簡報</div>
<h1 class="pp4-hero-title">{title}</h1>
<p class="pp4-hero-summary">{summary}</p>
<div class="pp4-hero-tags">{"".join(tags)}</div>
</div>
<aside class="pp4-kpi-matrix">
{_kpi_matrix_cell(_ICON_HEALTH, "品牌健康度", health_value, "")}
{_kpi_matrix_cell(_ICON_SIGNAL, "有效訊號", snapshot["total"], "筆")}
{_kpi_matrix_cell(_ICON_NEGATIVE, "負向訊號", snapshot["negative"], "筆")}
{_kpi_matrix_cell(_ICON_RISK, "高風險", snapshot["high_risk"], "筆")}
</aside>
</section>
"""


def _render_decision_queue(experience):
    items = _items(experience, "decisions")

    if not items:
        return """
<section class="pp4-section">
<div class="pp4-section-head">
<div><div class="pp4-eyebrow">決策佇列</div>
<h2 class="pp4-section-title">今日待決策</h2>
<p class="pp4-section-desc">主管應優先確認的品牌情報。</p></div>
<span class="pp4-count">0 項</span></div>
<div class="pp4-empty">目前沒有需要主管立即拍板的事項。</div>
</section>
"""

    primary = items[0]
    title = _safe(getattr(primary, "title", None), "待決策事項")
    description = _truncate_text(
        getattr(primary, "description", None) or "需要主管確認後才能繼續推進。",
        120,
    )
    urgency = _safe(getattr(primary, "urgency", None), "今天完成")
    owner = _safe(getattr(primary, "owner", None), "待主管指定")
    next_step = _truncate_text(
        getattr(primary, "next_step", None)
        or "確認負責人、完成期限與是否立即執行。",
        80,
    )

    secondary = ""
    for index, item in enumerate(items[1:3], start=2):
        item_title = _safe(getattr(item, "title", None), "待決策事項")
        item_reason = _truncate_text(
            getattr(item, "description", None) or "需要主管確認。",
            90,
        )
        item_action = _truncate_text(
            getattr(item, "next_step", None) or "確認負責人與期限。",
            60,
        )
        item_status = _safe(getattr(item, "urgency", None), "待確認")
        secondary += f"""
<article class="pp4-decision-secondary">
<div class="pp4-decision-secondary-head">
<span class="pp4-decision-index">優先事項 {index:02d}</span>
<span class="pp4-decision-status">{item_status}</span>
</div>
<h4>{item_title}</h4>
<p>{escape(item_reason)}</p>
<div class="pp4-decision-action">建議：{escape(item_action)}</div>
</article>
"""

    return f"""
<section class="pp4-section">
<div class="pp4-section-head">
<div><div class="pp4-eyebrow">決策佇列</div>
<h2 class="pp4-section-title">今日待決策</h2>
<p class="pp4-section-desc">先完成影響最大的決策。</p></div>
<span class="pp4-count">{len(items)} 項</span></div>
<div class="pp4-decision-grid">
<article class="pp4-decision-primary">
<div>
<div class="pp4-eyebrow">最高優先</div>
<h3>{title}</h3>
<p>{escape(description)}</p>
</div>
<aside class="pp4-decision-meta">
<div><span>負責單位</span><strong>{owner}</strong></div>
<div><span>建議行動</span><strong>{escape(next_step)}</strong></div>
<div><span>執行狀態</span><strong>{urgency}</strong></div>
</aside>
</article>
{secondary}
</div>
</section>
"""


def _render_signal_intelligence(experience):
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")

    risk_rows = _signal_rows(risks[:3], _ICON_RISK, "risk")
    opp_rows = _signal_rows(opportunities[:3], _ICON_OPPORTUNITY, "opportunity")

    return f"""
<section class="pp4-section">
<div class="pp4-section-head">
<div><div class="pp4-eyebrow">訊號情報</div>
<h2 class="pp4-section-title">今天要留意</h2>
<p class="pp4-section-desc">風險防守與值得投入的訊號。</p></div>
<span class="pp4-count">6 項精選</span></div>
<div class="pp4-signal-split">
<div>
<div class="pp4-signal-col-title is-risk">風險訊號</div>
{risk_rows}
</div>
<div>
<div class="pp4-signal-col-title is-opportunity">值得投入</div>
{opp_rows}
</div>
</div>
</section>
"""


def _render_action_workspace(experience):
    items = _items(experience, "workspaces")
    health_value = _health_value(experience)
    operating_status = _safe(getattr(experience, "operating_status", None), "穩定")
    confidence_level = _safe(getattr(experience, "confidence_level", None), "高")
    health_number, health_unit = _kpi_parts(health_value, "")

    cards = ""
    for index, item in enumerate(items[:3], start=1):
        is_disabled = index == 3
        card_class = "is-disabled" if is_disabled else "is-active"
        item_status = (
            "規劃中"
            if is_disabled
            else _safe(getattr(item, "status", None), "可用")
        )
        cta = (
            ""
            if is_disabled
            else '<span class="pp4-workspace-cta">進入 →</span>'
        )
        cards += f"""
<article class="pp4-workspace-card {card_class}">
<span class="pp4-workspace-eyebrow">{_workspace_label(index)}</span>
<span class="pp4-workspace-icon pp4-icon">{_workspace_icon(index)}</span>
<h4>{_safe(getattr(item, "title", None), "工作入口")}</h4>
<p>{_safe(getattr(item, "description", None), "建立負責人、安排時程並追蹤結果。")}</p>
<div class="pp4-workspace-footer">
<span class="pp4-workspace-status">{item_status}</span>
{cta}
</div>
</article>
"""

    health_card = f"""
<article class="pp4-workspace-card is-health">
<span class="pp4-workspace-eyebrow">企業健康</span>
<div class="pp4-health-value">{health_number}<small>{health_unit}</small></div>
<div class="pp4-health-meta">
<span>營運狀態 {operating_status}</span>
<span>資料可信度 {confidence_level}</span>
</div>
</article>
"""

    return f"""
<section class="pp4-section">
<div class="pp4-section-head">
<div><div class="pp4-eyebrow">執行入口</div>
<h2 class="pp4-section-title">開始執行</h2>
<p class="pp4-section-desc">完成決策後進入工作入口。</p></div>
</div>
<div class="pp4-workspace-grid">{cards}{health_card}</div>
</section>
"""


def _signal_rows(items, icon, kind):
    if not items:
        empty = "目前沒有風險訊號。" if kind == "risk" else "目前沒有機會訊號。"
        return f'<div class="pp4-empty">{empty}</div>'

    rows = ""
    for item in items:
        title = _safe(getattr(item, "title", None), "訊號")
        summary = _short_signal(
            getattr(item, "description", None),
            "AI 初判，請至證據中心確認來源。",
        )
        action_key = "action" if kind == "risk" else "recommendation"
        action = _truncate_text(
            getattr(item, action_key, None) or "安排後續確認。",
            48,
        )
        rows += f"""
<div class="pp4-signal-item">
<span class="pp4-signal-icon pp4-icon">{icon}</span>
<div>
<strong>{title}</strong>
<p>{summary}</p>
<small>建議：{escape(action)}</small>
</div>
</div>
"""
    return rows


def _kpi_matrix_cell(icon, label, value, unit_default):
    number, unit = _kpi_parts(value, unit_default)
    unit_html = f'<span class="pp4-kpi-cell-unit">{unit}</span>' if unit else ""
    return f"""
<div class="pp4-kpi-cell">
<div class="pp4-kpi-cell-top">
<span class="pp4-kpi-cell-icon pp4-icon">{icon}</span>
</div>
<span class="pp4-kpi-cell-label">{label}</span>
<div class="pp4-kpi-cell-value"><strong>{number}</strong>{unit_html}</div>
</div>
"""


def _workspace_label(index):
    return {
        1: "企業工作區",
        2: "證據中心",
        3: "深入調查室",
    }.get(index, "工作入口")


def _workspace_icon(index):
    return {
        1: _ICON_CLIPBOARD,
        2: _ICON_FILE_CHECK,
        3: _ICON_LAYERS,
    }.get(index, _ICON_CLIPBOARD)


def _load_evidence_status() -> tuple[int, str]:
    if not EVIDENCE_FILE.exists():
        return 0, "尚未建立資料"

    try:
        with EVIDENCE_FILE.open("r", encoding="utf-8") as file:
            evidence_data = json.load(file)

        evidence_count = _count_evidence_items(evidence_data)
        modified_datetime = datetime.fromtimestamp(EVIDENCE_FILE.stat().st_mtime)
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


def _resolve_update_status(evidence_count: int, last_updated: str) -> tuple[str, str]:
    if last_updated == "資料讀取異常":
        return ("資料狀態異常", "目前無法讀取資料檔案，請重新執行更新。")

    if evidence_count <= 0:
        return ("尚未載入品牌情報", f"最後狀態：{last_updated}")

    return (
        "品牌情報已同步",
        f"最後更新 {last_updated}",
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
            "total": data.get("evidence_count") or data.get("brand_signal_count") or 0,
            "positive": data.get("positive", 0),
            "negative": data.get("negative", 0),
            "high_risk": data.get("high_risk_count", 0),
        }

    return {"total": 0, "positive": 0, "negative": 0, "high_risk": 0}


def _compact_html(markup):
    return "".join(line.strip() for line in str(markup).splitlines() if line.strip())


def _safe(value, fallback=""):
    text = str(value).strip() if value is not None else ""
    return escape(text or str(fallback))


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


def _brief_summary(value, fallback):
    text = str(value).strip() if value is not None else ""
    if not text:
        text = fallback

    sentences = re.split(r"(?<=[。！？!?])\s*", text)
    concise = "".join(sentence for sentence in sentences[:2] if sentence).strip()
    return escape(_truncate_text(concise, 150))


def _truncate_text(value, max_chars):
    text = str(value).strip() if value is not None else ""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip("，、；： ") + "…"


def _short_signal(value, fallback):
    text = str(value).strip() if value is not None else ""
    if not text:
        text = fallback

    boilerplate = "此風險由最新 AI 品牌情報分析辨識，仍應回到原始證據確認細節。"
    if boilerplate in text:
        return escape("AI 初判，請至證據中心確認來源。")

    return escape(_truncate_text(text, 56))


__all__ = ["render_enterprise_home"]
