from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path
import subprocess
import sys
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


st.set_page_config(
    page_title="證據中心｜PetPulse Enterprise OS",
    page_icon="📌",
    layout="wide",
)


def main() -> None:
    _load_enterprise_css()

    service = EvidenceService()
    evidence_items = _get_evidence_items(service)

    render_shared_sidebar_brand_and_navigation(
        active_page="evidence",
        runtime=None,
        workspace_registry=None,
        experience=None,
    )

    _render_update_control(evidence_items)

    filtered_items = _render_evidence_experience(
        evidence_items
    )

    _render_evidence_results(filtered_items)


def _load_enterprise_css() -> None:
    if not ENTERPRISE_CSS_FILE.exists():
        return

    try:
        css = ENTERPRISE_CSS_FILE.read_text(
            encoding="utf-8"
        )
    except OSError:
        return

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def _get_evidence_items(
    service: EvidenceService,
) -> list[Any]:
    methods = (
        "get_all_evidence",
        "list_all",
        "get_all",
        "list_evidence",
    )

    for method_name in methods:
        method = getattr(
            service,
            method_name,
            None,
        )

        if not callable(method):
            continue

        try:
            result = method()
        except Exception:
            continue

        return _normalise_items(result)

    return []


def _normalise_items(
    value: Any,
) -> list[Any]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, dict):
        for key in (
            "items",
            "evidence_items",
            "results",
            "data",
        ):
            nested = value.get(key)
            if isinstance(nested, list):
                return nested

        return list(value.values())

    try:
        return list(value)
    except TypeError:
        return []


def _render_update_control(
    evidence_items: list[Any],
) -> None:
    if st.session_state.pop("evidence_update_success", False):
        st.success("品牌情報資料已更新。")

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
                '<strong>品牌情報資料已同步</strong>'
                f'<span>目前可查閱 {len(evidence_items)} 筆證據，'
                '可隨時重新整理最新資料。</span>'
                '</div>'
                '</div>'
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


def _render_evidence_experience(
    evidence_items: list[Any],
) -> list[Any]:
    summary = _summarise(evidence_items)

    hero_html = (
        '<div class="pp32-evidence-page">'
        '<section class="pp32-evidence-command-hero">'
        '<div class="pp32-evidence-command-main">'
        '<div class="pp32-hero-eyebrow">Evidence Intelligence</div>'
        '<h1 class="pp32-evidence-title">證據中心</h1>'
        '<p class="pp32-evidence-summary">'
        '集中檢視品牌訊號、AI 判讀、可信度與建議行動。'
        '每筆證據保留原始來源，讓主管能從結論一路追溯到證據。'
        '</p>'
        '<div class="pp32-evidence-tags">'
        f'<span class="pp32-tag">有效訊號 {summary["total"]}</span>'
        f'<span class="pp32-tag">平均可信度 {summary["average_confidence"]}%</span>'
        f'<span class="pp32-tag">平台涵蓋 {summary["platforms"]}</span>'
        '</div>'
        '</div>'
        '<aside class="pp32-evidence-kpi-cluster">'
        f'<div class="pp32-evidence-kpi-cell"><span>有效品牌訊號</span><strong>{summary["total"]}</strong><small>可直接查閱</small></div>'
        f'<div class="pp32-evidence-kpi-cell"><span>正向訊號</span><strong>{summary["positive"]}</strong><small>品牌動能</small></div>'
        f'<div class="pp32-evidence-kpi-cell"><span>負向訊號</span><strong>{summary["negative"]}</strong><small>優先判讀</small></div>'
        f'<div class="pp32-evidence-kpi-cell"><span>高風險</span><strong>{summary["high_risk"]}</strong><small>主管關注</small></div>'
        '</aside>'
        '</section>'
        '</div>'
    )

    st.markdown(
        _compact_html(hero_html),
        unsafe_allow_html=True,
    )

    platform_options = sorted(
        {
            _text(_get(item, "platform"), "")
            for item in evidence_items
            if _text(_get(item, "platform"), "")
        }
    )

    sentiment_options = sorted(
        {
            _sentiment_label(item)
            for item in evidence_items
        }
    )

    risk_options = sorted(
        {
            _risk_label(item)
            for item in evidence_items
        }
    )

    with st.container():
        search_col, platform_col, sentiment_col, risk_col = st.columns(
            [2.4, 1, 1, 1]
        )

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

    filtered = [
        item
        for item in evidence_items
        if _matches_query(item, query)
        and _matches_value(
            _text(_get(item, "platform"), ""),
            platform_filter,
        )
        and _matches_value(
            _sentiment_label(item),
            sentiment_filter,
        )
        and _matches_value(
            _risk_label(item),
            risk_filter,
        )
    ]

    st.markdown(
        _compact_html(
            (
                '<section class="pp32-section">'
                '<div class="pp32-section-head">'
                '<div>'
                '<div class="pp32-section-eyebrow">AI Verified Evidence</div>'
                '<div class="pp32-section-title">品牌情報結果</div>'
                '<div class="pp32-section-desc">'
                '依目前篩選條件顯示，可從 AI 摘要快速判讀，再開啟原始來源。'
                '</div>'
                '</div>'
                f'<span class="pp32-section-count">{len(filtered)} 筆</span>'
                '</div>'
                '</section>'
            )
        ),
        unsafe_allow_html=True,
    )

    return filtered


def _render_evidence_results(
    evidence_items: list[Any],
) -> None:
    if not evidence_items:
        st.markdown(
            '<div class="pp32-empty">'
            '目前沒有符合條件的證據，請調整搜尋或篩選條件。'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    cards = "".join(
        _render_evidence_card(item, index)
        for index, item in enumerate(
            evidence_items,
            start=1,
        )
    )

    st.markdown(
        _compact_html(
            f'<div class="pp32-evidence-list">{cards}</div>'
        ),
        unsafe_allow_html=True,
    )


def _render_evidence_card(
    item: Any,
    index: int,
) -> str:
    platform = _text(
        _get(item, "platform"),
        "未知平台",
    )
    sentiment = _sentiment_label(item)
    sentiment_class = _sentiment_class(sentiment)
    impact = _impact_label(item)
    impact_class = _impact_class(item)
    confidence = _confidence_value(item)
    confidence_label = _confidence_label(confidence)
    published_at = _published_time(item)
    risk_label = _risk_label(item)

    headline = _text(
        _first(
            item,
            "title",
            "executive_summary",
            "summary",
        ),
        "尚未產生主管摘要。",
    )

    summary = _text(
        _first(
            item,
            "executive_summary",
            "summary",
            "title",
        ),
        "尚未產生主管摘要。",
    )

    recommendation = _text(
        _first(
            item,
            "recommended_action",
            "recommendation",
            "action",
        ),
        "持續監測後續討論與情緒變化。",
    )

    publisher = _text(
        _first(
            item,
            "publisher",
            "source",
            "author",
        ),
        platform,
    )

    url = _text(
        _first(
            item,
            "url",
            "source_url",
            "link",
            "original_url",
        ),
        "",
    )

    source_link = (
        f'<a class="pp32-cta-executive" href="{escape(url)}" '
        'target="_blank" rel="noopener noreferrer">'
        f'<span>查看原始來源</span><span class="pp32-icon">{_ICON_ARROW}</span>'
        '</a>'
        if url
        else '<span class="pp32-evidence-badge neutral">無原始連結</span>'
    )

    return f"""
<article class="pp32-evidence-card">
<div class="pp32-evidence-card-top">
<div class="pp32-evidence-badges">
<span class="pp32-evidence-badge platform">{escape(platform)}</span>
<span class="pp32-evidence-badge {sentiment_class}">{escape(sentiment)}</span>
<span class="pp32-evidence-badge {impact_class}">{escape(impact)}</span>
<span class="pp32-evidence-badge confidence">{escape(confidence_label)}</span>
</div>
<span class="pp32-evidence-time">{escape(published_at)}</span>
</div>

<h3 class="pp32-evidence-headline">{escape(headline)}</h3>

<div class="pp32-evidence-meta-rail">
<span><em>來源</em>{escape(publisher)}</span>
<span><em>可信度</em>{confidence}%</span>
<span><em>序號</em>{index:03d}</span>
<span class="pp32-evidence-confidence-inline"><em>信心</em><span class="pp32-evidence-confidence-bar"><i style="width:{confidence}%"></i></span></span>
</div>

<div class="pp32-evidence-inset summary">
<span>AI Summary</span>
<p>{escape(summary)}</p>
</div>
<div class="pp32-evidence-inset action">
<span>Recommendation</span>
<p>{escape(recommendation)}</p>
</div>

<div class="pp32-evidence-footer">
<div class="pp32-evidence-platform">
{escape(platform)} · {escape(risk_label)}
</div>
{source_link}
</div>
</article>
"""


def _summarise(
    evidence_items: list[Any],
) -> dict[str, int]:
    total = len(evidence_items)

    confidence_values = [
        _confidence_value(item)
        for item in evidence_items
    ]

    average_confidence = (
        round(
            sum(confidence_values)
            / len(confidence_values)
        )
        if confidence_values
        else 0
    )

    positive = sum(
        1
        for item in evidence_items
        if _sentiment_label(item) == "正向"
    )

    negative = sum(
        1
        for item in evidence_items
        if _sentiment_label(item) == "負向"
    )

    high_risk = sum(
        1
        for item in evidence_items
        if _risk_label(item) == "高風險"
    )

    platforms = len(
        {
            _text(_get(item, "platform"), "")
            for item in evidence_items
            if _text(_get(item, "platform"), "")
        }
    )

    return {
        "total": total,
        "average_confidence": average_confidence,
        "positive": positive,
        "negative": negative,
        "high_risk": high_risk,
        "platforms": platforms,
    }


def _matches_query(
    item: Any,
    query: str,
) -> bool:
    normalized = query.strip().lower()

    if not normalized:
        return True

    haystack = " ".join(
        _text(
            _first(item, key),
            "",
        )
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


def _matches_value(
    value: str,
    selected: str,
) -> bool:
    return selected == "全部" or value == selected


def _sentiment_label(
    item: Any,
) -> str:
    value = _text(
        _first(
            item,
            "sentiment",
            "sentiment_label",
        ),
        "中立",
    ).lower()

    if value in {
        "positive",
        "正向",
        "正面",
    }:
        return "正向"

    if value in {
        "negative",
        "負向",
        "負面",
    }:
        return "負向"

    return "中立"


def _sentiment_class(
    sentiment: str,
) -> str:
    if sentiment == "正向":
        return "positive"

    if sentiment == "負向":
        return "negative"

    return "neutral"


def _impact_class(
    item: Any,
) -> str:
    impact = _impact_label(item).lower()

    if "機會" in impact or "opportunity" in impact:
        return "opportunity"

    if impact in {
        "高影響",
        "高",
        "高風險",
        "重大",
    }:
        return "warning"

    return "neutral"


def _risk_label(
    item: Any,
) -> str:
    is_high_risk = _first(
        item,
        "is_high_risk",
        "high_risk",
    )

    if isinstance(is_high_risk, bool):
        return (
            "高風險"
            if is_high_risk
            else "一般"
        )

    impact = _impact_label(item).lower()

    if impact in {
        "high",
        "高",
        "高風險",
        "重大",
    }:
        return "高風險"

    return "一般"


def _impact_label(
    item: Any,
) -> str:
    value = _text(
        _first(
            item,
            "impact_level",
            "impact",
            "risk_level",
        ),
        "一般",
    )

    mappings = {
        "high": "高影響",
        "medium": "中影響",
        "low": "一般",
        "positive opportunity": "正向機會",
    }

    return mappings.get(
        value.lower(),
        value,
    )


def _confidence_value(
    item: Any,
) -> int:
    raw = _first(
        item,
        "brand_confidence",
        "confidence",
        "confidence_score",
        "raw_brand_confidence",
    )

    try:
        value = float(raw)
    except (TypeError, ValueError):
        return 0

    if 0 <= value <= 1:
        value *= 100

    return max(
        0,
        min(100, round(value)),
    )


def _confidence_label(
    confidence: int,
) -> str:
    if confidence >= 90:
        return "極高信心"

    if confidence >= 75:
        return "高信心"

    if confidence >= 60:
        return "中等信心"

    return "需人工確認"


def _published_time(
    item: Any,
) -> str:
    raw = _first(
        item,
        "published_at",
        "published_time",
        "date",
        "created_at",
        "timestamp",
    )

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


def _first(
    item: Any,
    *keys: str,
) -> Any:
    for key in keys:
        value = _get(item, key)

        if value not in (
            None,
            "",
            [],
            {},
        ):
            return value

    return None


def _get(
    item: Any,
    key: str,
    default: Any = None,
) -> Any:
    if item is None:
        return default

    if isinstance(item, dict):
        return item.get(
            key,
            default,
        )

    return getattr(
        item,
        key,
        default,
    )


def _text(
    value: Any,
    fallback: str = "",
) -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text or fallback


def _compact_html(
    markup: str,
) -> str:
    return "".join(
        line.strip()
        for line in str(markup).splitlines()
        if line.strip()
    )


if __name__ == "__main__":
    main()
