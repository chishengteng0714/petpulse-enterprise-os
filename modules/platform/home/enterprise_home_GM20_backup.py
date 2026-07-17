import streamlit as st
from html import escape
from pathlib import Path

from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_enterprise_home(runtime=None):
    """
    PetPulse Enterprise OS v1.2 Executive Edition

    GM-20 Executive Home Premium：
    - Presentation Layer Only
    - 不修改 Runtime
    - 不修改 Engine
    - 不修改 Registry
    - 不修改 State
    - 不修改 Business Logic
    - 不修改 Data Schema
    - 僅重構首頁資訊層級、HTML 與視覺語言
    """

    _load_enterprise_css()
    experience = build_enterprise_home_experience()

    html = (
        _render_hero(experience)
        + _render_executive_brief(experience)
        + _render_decisions(experience)
        + _render_health(experience)
        + _render_risks(experience)
        + _render_opportunities(experience)
        + _render_workspaces(experience)
    )

    _render_html(html)


def _load_enterprise_css():
    css_path = (
        Path(__file__).resolve().parents[3]
        / "assets"
        / "enterprise.css"
    )

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )


def _render_html(markup):
    st.markdown(
        _compact_html(markup),
        unsafe_allow_html=True,
    )


def _compact_html(markup):
    if not markup:
        return ""

    return "".join(
        line.strip()
        for line in str(markup).splitlines()
        if line.strip()
    )


def _safe(value, fallback=""):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()

    if not text:
        return escape(str(fallback))

    if "<" in text or ">" in text:
        return escape(str(fallback))

    return escape(text)


def _items(experience, field_name):
    return getattr(experience, field_name, []) or []


def _section(icon, eyebrow, title, subtitle):
    return f"""
    <section class="pp-section-header pp-enterprise-section-header">
        <div class="pp-section-icon pp-enterprise-section-icon">
            {icon}
        </div>

        <div class="pp-section-copy">
            <div class="pp-section-kicker">{eyebrow}</div>
            <div class="pp-section-title">{title}</div>
            <div class="pp-section-subtitle">{subtitle}</div>
        </div>
    </section>
    """


def _empty_state(title, description):
    return f"""
    <article class="pp-card pp-card-highlight pp-empty-state">
        <div class="pp-card-kicker">今日狀態</div>
        <div class="pp-card-title">{title}</div>
        <div class="pp-card-desc">{description}</div>
    </article>
    """


def _render_hero(experience):
    title = _safe(
        getattr(experience, "briefing_title", None),
        "今日營運判斷",
    )
    summary = _safe(
        getattr(experience, "briefing_summary", None),
        (
            "今天品牌整體維持健康。"
            "目前真正需要主管確認的，是待決策事項、風險處理方式與成長機會的負責窗口。"
        ),
    )
    greeting = _safe(
        getattr(experience, "greeting", None),
        "主管決策首頁",
    )
    operating_status = _safe(
        getattr(experience, "operating_status", None),
        "穩定",
    )
    confidence_level = _safe(
        getattr(experience, "confidence_level", None),
        "高",
    )

    health_count = len(_items(experience, "health_signals"))
    decision_count = len(_items(experience, "decisions"))
    risk_count = len(_items(experience, "risks"))
    opportunity_count = len(_items(experience, "opportunities"))

    return f"""
    <section class="pp-hero pp-executive-hero pp-hero-gm20">
        <div class="pp-hero-content">
            <div class="pp-product-signature">
                PetPulse Enterprise OS v1.2 Executive Edition
            </div>

            <div class="pp-hero-kicker">
                {greeting}
            </div>

            <h1 class="pp-hero-title">
                {title}
            </h1>

            <div class="pp-hero-summary">
                {summary}
            </div>

            <div class="pp-hero-meta">
                <div class="pp-badge brand">營運狀態：{operating_status}</div>
                <div class="pp-badge brand">判斷信心：{confidence_level}</div>
                <div class="pp-badge brand">今日 {decision_count} 項待決策</div>
            </div>

            <div class="pp-hero-metrics">
                <article class="pp-hero-metric">
                    <div class="pp-hero-metric-number">{health_count:02d}</div>
                    <div class="pp-hero-metric-label">健康訊號</div>
                    <div class="pp-hero-metric-note">確認今日營運是否穩定</div>
                </article>

                <article class="pp-hero-metric pp-hero-metric-primary">
                    <div class="pp-hero-metric-number">{decision_count:02d}</div>
                    <div class="pp-hero-metric-label">主管待決策</div>
                    <div class="pp-hero-metric-note">需要確認、拍板與推進</div>
                </article>

                <article class="pp-hero-metric">
                    <div class="pp-hero-metric-number">{risk_count + opportunity_count:02d}</div>
                    <div class="pp-hero-metric-label">風險與機會</div>
                    <div class="pp-hero-metric-note">掌握需要留意與驗證的訊號</div>
                </article>
            </div>
        </div>
    </section>
    """


def _render_executive_brief(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")

    top_decision = (
        _safe(getattr(decisions[0], "title", None), "今日暫無待決策事項")
        if decisions
        else "今日暫無待決策事項"
    )
    top_risk = (
        _safe(getattr(risks[0], "title", None), "目前未發現重大風險")
        if risks
        else "目前未發現重大風險"
    )
    top_opportunity = (
        _safe(getattr(opportunities[0], "title", None), "持續觀察市場機會")
        if opportunities
        else "持續觀察市場機會"
    )

    return f"""
    <section class="pp-executive-narrative pp-executive-brief-gm20">
        <div class="pp-executive-narrative-label">
            今日主管摘要
        </div>

        <div class="pp-executive-narrative-title">
            今天最重要的，不是看完所有資料，而是先完成正確判斷。
        </div>

        <div class="pp-executive-narrative-copy">
            PetPulse 已整理今日營運訊號、待決策事項、風險與成長機會，
            讓管理團隊直接掌握優先順序與下一步。
        </div>

        <div class="pp-brief-grid">
            <article class="pp-brief-card pp-brief-card-priority">
                <div class="pp-brief-index">01</div>
                <div class="pp-card-kicker">第一優先</div>
                <div class="pp-card-title">{top_decision}</div>
                <div class="pp-card-desc">
                    需要主管先判斷，避免工作等待與資源延誤。
                </div>
            </article>

            <article class="pp-brief-card pp-brief-card-watch">
                <div class="pp-brief-index">02</div>
                <div class="pp-card-kicker">需要留意</div>
                <div class="pp-card-title">{top_risk}</div>
                <div class="pp-card-desc">
                    確認是否需要提前介入，或維持持續觀察。
                </div>
            </article>

            <article class="pp-brief-card pp-brief-card-verify">
                <div class="pp-brief-index">03</div>
                <div class="pp-card-kicker">值得驗證</div>
                <div class="pp-card-title">{top_opportunity}</div>
                <div class="pp-card-desc">
                    評估是否能轉化為會員、內容或營運任務。
                </div>
            </article>
        </div>
    </section>
    """


def _render_decisions(experience):
    items = _items(experience, "decisions")

    if not items:
        cards = _empty_state(
            "今日暫無待決策事項",
            "目前沒有需要主管立即拍板的事項。",
        )
    else:
        cards = ""

        tone_classes = [
            "pp-decision-priority",
            "pp-decision-attention",
            "pp-decision-action",
        ]

        for index, item in enumerate(items, start=1):
            urgency = _safe(getattr(item, "urgency", None), "今日處理")
            title = _safe(getattr(item, "title", None), "待決策事項")
            description = _safe(
                getattr(item, "description", None),
                "需要主管確認後才能繼續推進。",
            )
            owner = _safe(getattr(item, "owner", None), "未指定")
            next_step = _safe(
                getattr(item, "next_step", None),
                "確認後安排下一步。",
            )

            tone_class = tone_classes[(index - 1) % len(tone_classes)]

            cards += f"""
            <article class="pp-decision-card {tone_class}">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge warning">{urgency}</div>
                </div>

                <div class="pp-decision-question">{title}</div>
                <div class="pp-card-desc">{description}</div>

                <div class="pp-decision-reason">
                    <div class="pp-decision-label">負責窗口</div>
                    <div class="pp-decision-text">{owner}</div>
                </div>

                <div class="pp-decision-next">
                    <div class="pp-decision-label">AI 建議下一步</div>
                    <div class="pp-decision-text">{next_step}</div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "決",
        "主管判斷",
        "今日需要決策",
        "只保留今天真正需要主管確認、拍板與推進的事項。",
    )}

    <section class="pp-grid pp-grid-3 pp-decision-grid">
        {cards}
    </section>
    """


def _render_health(experience):
    items = _items(experience, "health_signals")

    if not items:
        cards = _empty_state(
            "今日暫無企業健康訊號",
            "目前沒有需要主管立即介入的健康指標。",
        )
    else:
        cards = ""

        for index, item in enumerate(items, start=1):
            status = _safe(getattr(item, "status", None), "穩定")
            value = _safe(getattr(item, "value", None), "觀察中")
            label = _safe(getattr(item, "label", None), "關鍵指標")
            detail = _safe(
                getattr(item, "detail", None),
                "目前狀態穩定。",
            )

            feature_class = (
                "pp-health-card-featured"
                if index == 1
                else "pp-health-card-secondary"
            )

            cards += f"""
            <article class="pp-card pp-health-card {feature_class}">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge success">{status}</div>
                </div>

                <div class="pp-card-kicker">營運健康訊號</div>
                <div class="pp-card-value">{value}</div>
                <div class="pp-card-title">{label}</div>
                <div class="pp-card-desc">{detail}</div>
            </article>
            """

    return f"""
    {_section(
        "況",
        "營運概況",
        "今日品牌與營運狀態",
        "用最少資訊確認今天是否健康、是否需要介入，以及判斷依據。",
    )}

    <section class="pp-grid pp-grid-4 pp-health-grid">
        {cards}
    </section>
    """


def _render_risks(experience):
    items = _items(experience, "risks")

    if not items:
        cards = _empty_state(
            "今天沒有需要立即升級處理的風險",
            "目前狀況穩定，可持續觀察。",
        )
    else:
        cards = ""

        for index, item in enumerate(items, start=1):
            severity = _safe(
                getattr(item, "severity", None),
                "持續觀察",
            )
            title = _safe(getattr(item, "title", None), "風險訊號")
            description = _safe(
                getattr(item, "description", None),
                "需要持續追蹤。",
            )
            action = _safe(
                getattr(item, "action", None),
                "安排後續確認。",
            )

            cards += f"""
            <article class="pp-card pp-risk-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge danger">{severity}</div>
                </div>

                <div class="pp-card-kicker">今日需留意</div>
                <div class="pp-card-title">{title}</div>
                <div class="pp-card-desc">{description}</div>

                <div class="pp-card-detail">
                    <div class="pp-decision-label">建議處理</div>
                    <div class="pp-decision-text">{action}</div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "風",
        "風險判讀",
        "今天需要留意",
        "提前辨識可能影響品牌聲量、會員體驗與營運節奏的異常訊號。",
    )}

    <section class="pp-grid pp-grid-3 pp-risk-grid">
        {cards}
    </section>
    """


def _render_opportunities(experience):
    items = _items(experience, "opportunities")

    if not items:
        cards = _empty_state(
            "今天暫無需要立即投入的成長機會",
            "可持續觀察市場與會員訊號。",
        )
    else:
        cards = ""

        for index, item in enumerate(items, start=1):
            potential = _safe(
                getattr(item, "potential", None),
                "可驗證",
            )
            title = _safe(getattr(item, "title", None), "成長機會")
            description = _safe(
                getattr(item, "description", None),
                "具備進一步驗證價值。",
            )
            recommendation = _safe(
                getattr(item, "recommendation", None),
                "建議安排小規模測試。",
            )

            cards += f"""
            <article class="pp-card pp-opportunity-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge success">{potential}</div>
                </div>

                <div class="pp-card-kicker">成長契機</div>
                <div class="pp-card-title">{title}</div>
                <div class="pp-card-desc">{description}</div>

                <div class="pp-card-detail">
                    <div class="pp-decision-label">建議驗證</div>
                    <div class="pp-decision-text">{recommendation}</div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "機",
        "成長判讀",
        "值得投入驗證",
        "把市場、會員與門市訊號轉化為可測試、可追蹤的成長選項。",
    )}

    <section class="pp-grid pp-grid-3 pp-opportunity-grid">
        {cards}
    </section>
    """


def _render_workspaces(experience):
    items = _items(experience, "workspaces")

    if not items:
        cards = _empty_state(
            "目前暫無可用工作入口",
            "請稍後再確認企業工作區狀態。",
        )
    else:
        cards = ""

        for index, item in enumerate(items, start=1):
            status = _safe(getattr(item, "status", None), "使用中")
            title = _safe(getattr(item, "title", None), "工作入口")
            description = _safe(
                getattr(item, "description", None),
                "查看相關資訊並安排下一步。",
            )

            cards += f"""
            <article class="pp-card pp-launcher-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge brand">{status}</div>
                </div>

                <div class="pp-card-kicker">工作入口</div>
                <div class="pp-card-title">{title}</div>
                <div class="pp-card-desc">{description}</div>

                <div class="pp-feed-action">
                    進入工作區 →
                </div>
            </article>
            """

    return f"""
    {_section(
        "行",
        "執行路徑",
        "下一步行動",
        "完成判斷後，直接進入對應工作區，安排負責窗口與後續追蹤。",
    )}

    <section class="pp-grid pp-grid-3 pp-workspace-grid">
        {cards}
    </section>
    """


__all__ = [
    "render_enterprise_home",
]
