import streamlit as st
from html import escape
from pathlib import Path

from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_enterprise_home(runtime=None):
    """
    Enterprise Home

    GM-12 Luxury Polish Final：
    - Presentation Layer Only
    - 不修改 Runtime
    - 不修改 Experience Schema
    - 不修改 Business Logic
    - 不修改首頁組裝順序
    - 精修 Hero、KPI、Icon、Card 與資訊層級
    """

    _load_enterprise_css()

    experience = build_enterprise_home_experience()

    html = (
        _render_hero(experience)
        + _render_health(experience)
        + _render_decisions(experience)
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


def _section(
    icon,
    eyebrow,
    title,
    subtitle,
):
    return f"""
    <section class="pp-section-header pp-enterprise-section-header">
        <div class="pp-section-icon pp-enterprise-section-icon">
            {icon}
        </div>

        <div class="pp-section-copy">
            <div class="pp-card-kicker">
                {eyebrow}
            </div>

            <div class="pp-section-title">
                {title}
            </div>

            <div class="pp-section-subtitle">
                {subtitle}
            </div>
        </div>
    </section>
    """


def _empty_state(
    title,
    description,
):
    return f"""
    <article class="pp-card-summary pp-empty-state">
        <div class="pp-card-kicker">
            今日狀態
        </div>

        <div class="pp-card-title">
            {title}
        </div>

        <div class="pp-card-desc">
            {description}
        </div>
    </article>
    """


def _render_hero(experience):
    title = _safe(
        getattr(experience, "briefing_title", None),
        "今日企業決策總覽",
    )

    summary = _safe(
        getattr(experience, "briefing_summary", None),
        (
            "整合今日營運狀態、待決策事項、風險訊號與下一步行動，"
            "協助主管快速完成判斷。"
        ),
    )

    greeting = _safe(
        getattr(experience, "greeting", None),
        "今日企業首頁",
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
    risk_opportunity_count = risk_count + opportunity_count

    return f"""
    <section class="pp-hero pp-enterprise-hero">
        <div class="pp-hero-dashboard">
            <div class="pp-hero-main">
                <div class="pp-product-signature">
                    企業決策作業系統
                </div>

                <div class="pp-hero-kicker">
                    PetPulse Enterprise OS｜主管決策首頁
                </div>

                <h1 class="pp-hero-title">
                    {title}
                </h1>

                <div class="pp-hero-summary">
                    {summary}
                </div>

                <div class="pp-hero-meta">
                    <div class="pp-badge dark">決策視角</div>
                    <div class="pp-badge dark">營運判讀</div>
                    <div class="pp-badge dark">行動排序</div>
                </div>

                <div class="pp-executive-strip">
                    <div class="pp-executive-strip-item">
                        <strong>{health_count}</strong>
                        <span class="pp-executive-strip-label">健康訊號</span>
                    </div>

                    <div class="pp-executive-strip-item">
                        <strong>{decision_count}</strong>
                        <span class="pp-executive-strip-label">今日待決策</span>
                    </div>

                    <div class="pp-executive-strip-item">
                        <strong>{risk_opportunity_count}</strong>
                        <span class="pp-executive-strip-label">風險與機會</span>
                    </div>
                </div>
            </div>

            <aside class="pp-hero-side">
                <div class="pp-hero-signal pp-hero-signal-featured">
                    <div class="pp-hero-signal-label">
                        今日主管焦點
                    </div>

                    <div class="pp-hero-signal-value">
                        {greeting}
                    </div>

                    <div class="pp-hero-signal-note">
                        聚焦今日需要優先判斷、確認與推進的企業事項。
                    </div>
                </div>

                <div class="pp-hero-signal">
                    <div class="pp-hero-signal-label">
                        企業營運狀態
                    </div>

                    <div class="pp-hero-signal-value">
                        {operating_status}
                    </div>

                    <div class="pp-hero-signal-note">
                        依目前訊號整合結果呈現今日營運狀態。
                    </div>
                </div>

                <div class="pp-hero-signal">
                    <div class="pp-hero-signal-label">
                        決策判斷信心
                    </div>

                    <div class="pp-hero-signal-value">
                        {confidence_level}
                    </div>

                    <div class="pp-hero-signal-note">
                        反映今日判斷所依據資訊的完整程度。
                    </div>
                </div>
            </aside>
        </div>
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

            cards += f"""
            <article class="pp-card pp-enterprise-card pp-health-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge success">{status}</div>
                </div>

                <div class="pp-card-body">
                    <div class="pp-card-kicker">企業健康訊號</div>
                    <div class="pp-card-value">{value}</div>
                    <div class="pp-card-title">{label}</div>
                    <div class="pp-card-desc">{detail}</div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "◎",
        "營運概況",
        "企業營運健康",
        "以主管視角掌握今日最重要的核心營運訊號，快速確認是否需要介入。",
    )}

    <section class="pp-grid pp-grid-4">
        {cards}
    </section>
    """


def _render_decisions(experience):
    items = _items(experience, "decisions")

    if not items:
        cards = _empty_state(
            "今日暫無待決策事項",
            "目前沒有需要主管立即拍板的企業事項。",
        )
    else:
        cards = ""

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

            cards += f"""
            <article class="pp-card pp-enterprise-card is-priority pp-decision-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge gold">{urgency}</div>
                </div>

                <div class="pp-card-body">
                    <div class="pp-card-kicker">主管決策事項</div>
                    <div class="pp-card-title">{title}</div>
                    <div class="pp-card-desc">{description}</div>
                </div>

                <div class="pp-card-footer">
                    <div class="pp-card-meta">
                        <strong>負責窗口</strong><br>
                        {owner}
                        <br><br>
                        <strong>建議下一步</strong><br>
                        {next_step}
                    </div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "◆",
        "主管判斷",
        "今日決策中樞",
        "聚焦今日需要主管拍板的事項，避免重要工作因等待判斷而停滯。",
    )}

    <section class="pp-grid pp-grid-3">
        {cards}
    </section>
    """


def _render_risks(experience):
    items = _items(experience, "risks")

    if not items:
        cards = _empty_state(
            "今日暫無明顯風險訊號",
            "目前沒有需要立即升級處理的企業風險。",
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
            <article class="pp-card pp-enterprise-card is-risk pp-risk-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge danger">{severity}</div>
                </div>

                <div class="pp-card-body">
                    <div class="pp-card-kicker">企業風險訊號</div>
                    <div class="pp-card-title">{title}</div>
                    <div class="pp-card-desc">{description}</div>
                </div>

                <div class="pp-card-footer">
                    <div class="pp-card-meta">
                        <strong>建議處理</strong><br>
                        {action}
                    </div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "▲",
        "異常監測",
        "企業風險觀測",
        "提前辨識可能影響品牌聲量、營運節奏與會員體驗的異常訊號。",
    )}

    <section class="pp-grid pp-grid-3">
        {cards}
    </section>
    """


def _render_opportunities(experience):
    items = _items(experience, "opportunities")

    if not items:
        cards = _empty_state(
            "今日暫無明顯成長機會",
            "目前沒有需要立即投入驗證的成長訊號。",
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
            <article class="pp-card pp-enterprise-card is-opportunity pp-opportunity-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge success">{potential}</div>
                </div>

                <div class="pp-card-body">
                    <div class="pp-card-kicker">成長驗證機會</div>
                    <div class="pp-card-title">{title}</div>
                    <div class="pp-card-desc">{description}</div>
                </div>

                <div class="pp-card-footer">
                    <div class="pp-card-meta">
                        <strong>建議行動</strong><br>
                        {recommendation}
                    </div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "✦",
        "成長探索",
        "企業成長機會",
        "找出今日值得投入驗證的市場、會員與營運機會，將訊號轉化為成長選項。",
    )}

    <section class="pp-grid pp-grid-3">
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
            <article class="pp-card pp-enterprise-card is-priority pp-workspace-card">
                <div class="pp-card-top">
                    <div class="pp-card-index">{index:02d}</div>
                    <div class="pp-badge gold">{status}</div>
                </div>

                <div class="pp-card-body">
                    <div class="pp-card-kicker">決策執行入口</div>
                    <div class="pp-card-title">{title}</div>
                    <div class="pp-card-desc">{description}</div>
                </div>

                <div class="pp-card-footer">
                    <div class="pp-card-meta">
                        <strong>執行原則</strong><br>
                        完成初步判斷後，安排負責窗口、執行節點與後續追蹤。
                    </div>
                </div>
            </article>
            """

    return f"""
    {_section(
        "→",
        "執行路徑",
        "下一步行動入口",
        "把今日企業判斷轉換為可立即推進的執行路徑，讓決策真正開始運作。",
    )}

    <section class="pp-grid pp-grid-3">
        {cards}
    </section>
    """


__all__ = [
    "render_enterprise_home",
]
