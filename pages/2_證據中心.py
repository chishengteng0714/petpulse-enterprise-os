from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import streamlit as st

from modules.evidence_center.service import EvidenceService
from modules.platform.platform_frame import (
    render_shared_sidebar_brand_and_navigation,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENTERPRISE_CSS_FILE = PROJECT_ROOT / "assets" / "enterprise.css"
UPDATE_SCRIPT = PROJECT_ROOT / "update_evidence.py"

_ICON_ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>'
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

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0000FE00-\U0000FE0F"
    "\U0001F900-\U0001F9FF"
    "]+",
    flags=re.UNICODE,
)


st.set_page_config(
    page_title="證據中心｜PetPulse Enterprise OS",
    page_icon="📌",
    layout="wide",
)


def main() -> None:
    _load_enterprise_css()

    service = EvidenceService()
    evidence_items = _get_evidence_items(service)
    kpi_summary = _get_kpi_summary(service, evidence_items)

    render_shared_sidebar_brand_and_navigation(
        active_page="evidence",
        runtime=None,
        workspace_registry=None,
        experience=None,
    )

    _render_update_control(evidence_items)
    _render_evidence_header(evidence_items, kpi_summary)
    filtered_items = _render_filter_bar(evidence_items)
    _render_result_header(filtered_items)
    _render_evidence_results(filtered_items)


def _load_enterprise_css() -> None:
    if not ENTERPRISE_CSS_FILE.exists():
        return

    try:
        css = ENTERPRISE_CSS_FILE.read_text(encoding="utf-8")
    except OSError:
        return

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _get_evidence_items(service: EvidenceService) -> list[Any]:
    methods = ("get_all_evidence", "list_all", "get_all", "list_evidence")

    for method_name in methods:
        method = getattr(service, method_name, None)
        if not callable(method):
            continue
        try:
            result = method()
        except Exception:
            continue
        return _normalise_items(result)

    return []


def _normalise_items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict):
        for key in ("items", "evidence_items", "results", "data"):
            nested = value.get(key)
            if isinstance(nested, list):
                return nested
        return list(value.values())
    try:
        return list(value)
    except TypeError:
        return []


def _get_kpi_summary(
    service: EvidenceService,
    evidence_items: list[Any],
) -> dict[str, Any]:
    method = getattr(service, "get_kpi_summary", None)

    if callable(method):
        try:
            result = method()
            if isinstance(result, dict):
                summary = dict(result)
                summary["platforms"] = _platform_count(evidence_items)
                return summary
        except Exception:
            pass

    fallback = _summarise(evidence_items)
    return {
        "brand_health": 0,
        "brand_signal_count": fallback["total"],
        "evidence_count": fallback["total"],
        "high_risk_count": fallback["high_risk"],
        "brand_confidence_average": fallback["average_confidence"],
        "data_quality": "待確認",
        "positive": fallback["positive"],
        "neutral": max(
            0,
            fallback["total"] - fallback["positive"] - fallback["negative"],
        ),
        "negative": fallback["negative"],
        "platforms": fallback["platforms"],
    }


def _platform_count(evidence_items: list[Any]) -> int:
    return len(
        {
            _text(_get(item, "platform"), "")
            for item in evidence_items
            if _text(_get(item, "platform"), "")
        }
    )


def _render_update_control(evidence_items: list[Any]) -> None:
    if st.session_state.pop("evidence_update_success", False):
        st.success("品牌情報資料已更新。")

    left, right = st.columns([4.6, 1], vertical_alignment="center")

    with left:
        st.markdown(
            (
                '<div class="pp4-utility">'
                f'<span class="pp4-utility-icon pp4-icon">{_ICON_SYNC}</span>'
                '<div class="pp4-utility-copy">'
                "<strong>品牌情報已同步</strong>"
                f"<span>目前可查閱 {len(evidence_items)} 筆證據</span>"
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
            key="gm29_update_evidence",
        ):
            _run_update()


def _run_update() -> None:
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

    st.session_state["evidence_update_success"] = True
    st.rerun()


def _render_evidence_header(
    evidence_items: list[Any],
    summary: dict[str, Any],
) -> None:
    total = _safe_int(
        summary.get(
            "brand_signal_count",
            summary.get("evidence_count", len(evidence_items)),
        )
    )
    average_confidence = _safe_float(
        summary.get("brand_confidence_average", 0)
    )
    positive = _safe_int(summary.get("positive", 0))
    negative = _safe_int(summary.get("negative", 0))
    high_risk = _safe_int(summary.get("high_risk_count", 0))
    platforms = _safe_int(
        summary.get("platforms", _platform_count(evidence_items))
    )

    html = f"""
<div class="pp4-evidence-page">
<section class="pp4-evidence-header">
<div>
<div class="pp4-eyebrow">證據情報</div>
<h1>證據中心</h1>
<p>集中檢視品牌訊號、AI 判讀與建議行動。每筆證據保留原始來源。</p>
<div class="pp4-evidence-meta">
<span class="pp4-tag">有效訊號 {total}</span>
<span class="pp4-tag">平均可信度 {average_confidence:.0f}%</span>
<span class="pp4-tag">平台 {platforms}</span>
</div>
</div>
<aside class="pp4-evidence-kpis">
<div class="pp4-evidence-kpi"><span>有效訊號</span><strong>{total}</strong></div>
<div class="pp4-evidence-kpi"><span>正向</span><strong>{positive}</strong></div>
<div class="pp4-evidence-kpi"><span>負向</span><strong>{negative}</strong></div>
<div class="pp4-evidence-kpi"><span>高風險</span><strong>{high_risk}</strong></div>
</aside>
</section>
</div>
"""

    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _render_filter_bar(evidence_items: list[Any]) -> list[Any]:
    platform_options = sorted(
        {_text(_get(item, "platform"), "") for item in evidence_items if _text(_get(item, "platform"), "")}
    )
    sentiment_options = sorted({_sentiment_label(item) for item in evidence_items})
    risk_options = sorted({_risk_label(item) for item in evidence_items})

    search_col, platform_col, sentiment_col, risk_col = st.columns([2.4, 1, 1, 1])

    with search_col:
        query = st.text_input(
            "搜尋內容",
            placeholder="搜尋摘要、標題、建議行動或來源",
            key="gm29_evidence_query",
        )

    with platform_col:
        platform_filter = st.selectbox(
            "平台",
            ["全部", *platform_options],
            key="gm29_platform_filter",
        )

    with sentiment_col:
        sentiment_filter = st.selectbox(
            "情緒",
            ["全部", *sentiment_options],
            key="gm29_sentiment_filter",
        )

    with risk_col:
        risk_filter = st.selectbox(
            "風險",
            ["全部", *risk_options],
            key="gm29_risk_filter",
        )

    return [
        item
        for item in evidence_items
        if _matches_query(item, query)
        and _matches_value(_text(_get(item, "platform"), ""), platform_filter)
        and _matches_value(_sentiment_label(item), sentiment_filter)
        and _matches_value(_risk_label(item), risk_filter)
    ]


def _render_result_header(filtered_items: list[Any]) -> None:
    html = f"""
<section class="pp4-section">
<div class="pp4-section-head">
<div>
<div class="pp4-eyebrow">AI 驗證證據</div>
<h2 class="pp4-section-title">品牌情報結果</h2>
<p class="pp4-section-desc">依目前篩選條件顯示，可開啟原始來源確認細節。</p>
</div>
<span class="pp4-count">{len(filtered_items)} 筆</span>
</div>
</section>
"""
    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _render_evidence_results(evidence_items: list[Any]) -> None:
    if not evidence_items:
        st.markdown(
            '<div class="pp4-empty">目前沒有符合條件的證據，請調整搜尋或篩選條件。</div>',
            unsafe_allow_html=True,
        )
        return

    cards = "".join(
        _render_evidence_card(item, index)
        for index, item in enumerate(evidence_items, start=1)
    )

    st.markdown(
        _compact_html(f'<div class="pp4-evidence-list">{cards}</div>'),
        unsafe_allow_html=True,
    )


def _render_evidence_card(item: Any, index: int) -> str:
    platform = _text(_get(item, "platform"), "未知平台")
    sentiment = _sentiment_label(item)
    sentiment_class = _sentiment_class(sentiment)
    impact = _impact_label(item)
    impact_class = _impact_class(item)
    confidence = _confidence_value(item)
    confidence_label = _confidence_label(confidence)
    published_at = _published_time(item)
    risk_label = _risk_label(item)

    raw_title = _text(
        _first(item, "title", "executive_summary", "summary"),
        "尚未產生主管摘要。",
    )
    raw_summary = _text(
        _first(item, "executive_summary", "summary", "title"),
        "尚未產生主管摘要。",
    )
    raw_recommendation = _text(
        _first(item, "recommended_action", "recommendation", "action"),
        "持續監測後續討論與情緒變化。",
    )

    title = escape(_clean_display_title(raw_title))
    summary = escape(_clean_summary(raw_summary))
    recommendation = escape(_truncate_text(raw_recommendation, 90))

    publisher = _text(
        _first(item, "publisher", "source", "author"),
        platform,
    )

    url = _text(
        _first(item, "url", "source_url", "link", "original_url"),
        "",
    )

    source_link = (
        f'<a class="pp4-cta" href="{escape(url)}" target="_blank" rel="noopener noreferrer">'
        "<span>查看原始來源</span>"
        "</a>"
        if url
        else '<span class="pp4-badge">無原始連結</span>'
    )

    return f"""
<article class="pp4-evidence-card">
<div class="pp4-evidence-card-top">
<div class="pp4-evidence-badges">
<span class="pp4-badge">{escape(platform)}</span>
<span class="pp4-badge {sentiment_class}">{escape(sentiment)}</span>
<span class="pp4-badge {impact_class}">{escape(impact)}</span>
<span class="pp4-badge is-info">{escape(confidence_label)}</span>
</div>
<span class="pp4-evidence-date">{escape(published_at)}</span>
</div>
<h3 class="pp4-evidence-title">{title}</h3>
<div class="pp4-evidence-compact-meta">
<span><em>來源</em>{escape(publisher)}</span>
<span><em>可信度</em>{confidence}%</span>
<span><em>序號</em>{index:03d}</span>
</div>
<div class="pp4-evidence-summary">
<span>AI 摘要</span>
<p>{summary}</p>
</div>
<div class="pp4-evidence-recommendation">
<em>建議行動｜</em>{recommendation}
</div>
<div class="pp4-evidence-footer">
<span class="pp4-evidence-risk">風險：{escape(risk_label)}</span>
{source_link}
</div>
</article>
"""


def _truncate_text(text: str, max_chars: int) -> str:
    value = str(text or "").strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 1].rstrip("，、；： #") + "…"


def _clean_display_title(text: str) -> str:
    value = re.sub(r"\s+", " ", str(text or "").strip())

    seen_tags: set[str] = set()
    words: list[str] = []
    for word in value.split():
        if word.startswith("#") or word.startswith("＃"):
            key = word.lower()
            if key in seen_tags:
                continue
            seen_tags.add(key)
        words.append(word)
    value = " ".join(words)

    value = re.sub(r"[!！]{2,}", "!", value)
    value = re.sub(r"[#＃]{2,}", "#", value)
    value = re.sub(r"[%％]{2,}", "%", value)
    value = re.sub(r"([🔥💥✨🎉⭐🌟💯]+)\s*\1+", r"\1", value)

    emoji_count = 0

    def _limit_emoji(match: re.Match[str]) -> str:
        nonlocal emoji_count
        emoji_count += 1
        return match.group(0) if emoji_count <= 1 else ""

    value = _EMOJI_PATTERN.sub(_limit_emoji, value)
    value = re.sub(r"\s+", " ", value).strip()
    return _truncate_text(value, 72)


def _clean_summary(text: str) -> str:
    value = re.sub(r"\s+", " ", str(text or "").strip())
    return _truncate_text(value, 120)


def _summarise(evidence_items: list[Any]) -> dict[str, int]:
    total = len(evidence_items)
    confidence_values = [_confidence_value(item) for item in evidence_items]
    average_confidence = (
        round(sum(confidence_values) / len(confidence_values))
        if confidence_values
        else 0
    )
    positive = sum(1 for item in evidence_items if _sentiment_label(item) == "正向")
    negative = sum(1 for item in evidence_items if _sentiment_label(item) == "負向")
    high_risk = sum(1 for item in evidence_items if _risk_label(item) == "高風險")
    platforms = len(
        {_text(_get(item, "platform"), "") for item in evidence_items if _text(_get(item, "platform"), "")}
    )

    return {
        "total": total,
        "average_confidence": average_confidence,
        "positive": positive,
        "negative": negative,
        "high_risk": high_risk,
        "platforms": platforms,
    }


def _matches_query(item: Any, query: str) -> bool:
    normalized = query.strip().lower()
    if not normalized:
        return True

    haystack = " ".join(
        _text(_first(item, key), "")
        for key in (
            "executive_summary",
            "summary",
            "title",
            "content",
            "description",
            "snippet",
            "recommended_action",
            "recommendation",
            "publisher",
            "source",
            "platform",
        )
    ).lower()

    return normalized in haystack


def _matches_value(value: str, selected: str) -> bool:
    return selected == "全部" or value == selected


def _sentiment_label(item: Any) -> str:
    value = _text(_first(item, "sentiment", "sentiment_label"), "中立").lower()

    if value in {"positive", "正向", "正面"}:
        return "正向"
    if value in {"negative", "負向", "負面"}:
        return "負向"
    return "中立"


def _sentiment_class(sentiment: str) -> str:
    if sentiment == "正向":
        return "is-positive"
    if sentiment == "負向":
        return "is-negative"
    return ""


def _impact_class(item: Any) -> str:
    impact = _impact_label(item).lower()
    if "機會" in impact or "opportunity" in impact:
        return "is-positive"
    if impact in {"高影響", "高", "高風險", "重大"}:
        return "is-warning"
    return ""


def _risk_label(item: Any) -> str:
    is_high_risk = _first(item, "is_high_risk", "high_risk")
    if isinstance(is_high_risk, bool):
        return "高風險" if is_high_risk else "一般"

    impact = _impact_label(item).lower()
    if impact in {"high", "高", "高風險", "重大"}:
        return "高風險"
    return "一般"


def _impact_label(item: Any) -> str:
    value = _text(_first(item, "impact_level", "impact", "risk_level"), "一般")
    mappings = {
        "high": "高影響",
        "medium": "中影響",
        "low": "一般",
        "positive opportunity": "正向機會",
    }
    return mappings.get(value.lower(), value)


def _confidence_value(item: Any) -> int:
    raw = _first(item, "brand_confidence", "confidence", "confidence_score", "raw_brand_confidence")
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return 0
    if 0 <= value <= 1:
        value *= 100
    return max(0, min(100, round(value)))


def _confidence_label(confidence: int) -> str:
    if confidence >= 90:
        return "極高信心"
    if confidence >= 75:
        return "高信心"
    if confidence >= 60:
        return "中等信心"
    return "需人工確認"


def _published_time(item: Any) -> str:
    raw = _first(item, "published_at", "published_time", "date", "created_at", "timestamp")

    if raw in (None, ""):
        return "時間未提供"

    taipei = ZoneInfo("Asia/Taipei")

    if isinstance(raw, datetime):
        if raw.tzinfo is None:
            raw = raw.replace(tzinfo=taipei)
        else:
            raw = raw.astimezone(taipei)
        return raw.strftime("%Y/%m/%d %H:%M")

    if isinstance(raw, (int, float)):
        try:
            timestamp = float(raw)
            if timestamp > 1_000_000_000_000:
                timestamp /= 1000
            parsed = datetime.fromtimestamp(timestamp, tz=taipei)
            return parsed.strftime("%Y/%m/%d %H:%M")
        except (OSError, OverflowError, ValueError):
            return "時間未提供"

    text = str(raw).strip()
    if not text:
        return "時間未提供"

    try:
        parsed = parsedate_to_datetime(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
        return parsed.astimezone(taipei).strftime("%Y/%m/%d %H:%M")
    except (TypeError, ValueError, OverflowError):
        pass

    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=taipei)
        else:
            parsed = parsed.astimezone(taipei)
        return parsed.strftime("%Y/%m/%d %H:%M")
    except ValueError:
        pass

    return "時間未提供"


def _first(item: Any, *keys: str) -> Any:
    for key in keys:
        value = _get(item, key)
        if value not in (None, "", [], {}):
            return value
    return None


def _get(item: Any, key: str, default: Any = None) -> Any:
    if item is None:
        return default
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text or fallback


def _safe_int(value: Any, fallback: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback


def _safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _compact_html(markup: str) -> str:
    return "".join(line.strip() for line in str(markup).splitlines() if line.strip())


if __name__ == "__main__":
    main()
