import streamlit as st
from html import escape
from pathlib import Path

from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_enterprise_home(runtime=None):
    """
    PetPulse Enterprise OS v1.3 Executive Copilot
    GM27-01 Executive Morning Brief

    Presentation Layer Only
    不修改 Runtime / Engine / Layer / Domain / Registry / API
    不修改 Business Logic / Evidence Schema
    """

    _load_enterprise_css()
    _load_gm27_css()

    experience = build_enterprise_home_experience()

    html = (
        _render_executive_hero(experience)
        + _render_executive_focus(experience)
        + _render_today_brief(experience)
        + _render_health_overview(experience)
        + _render_decision_board(experience)
        + _render_risk_feed(experience)
        + _render_opportunity_feed(experience)
        + _render_workspace_links(experience)
    )

    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _load_enterprise_css():
    css_path = Path(__file__).resolve().parents[3] / "assets" / "enterprise.css"

    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def _load_gm27_css():
    """
    GM27 首頁專屬樣式。

    目前先放在 Presentation 檔案內，確保第一階段單檔覆蓋即可驗收。
    下一階段再完整併入 assets/enterprise.css。
    """

    st.markdown(
        """
        <style>
        .pp27-hero,
        .pp27-focus,
        .pp27-brief-shell {
            box-sizing: border-box;
        }

        .pp27-hero {
            position: relative;
            overflow: hidden;
            display: grid;
            grid-template-columns: minmax(0, 1.45fr) minmax(260px, .55fr);
            gap: 28px;
            padding: 34px 36px;
            margin: 8px 0 26px;
            border: 1px solid rgba(0, 62, 51, .10);
            border-radius: 28px;
            background:
                radial-gradient(circle at 8% 5%, rgba(123, 170, 60, .22), transparent 31%),
                radial-gradient(circle at 94% 8%, rgba(216, 183, 106, .22), transparent 30%),
                linear-gradient(135deg, #fffdf7 0%, #f7f7ee 58%, #f1f6ec 100%);
            box-shadow: 0 22px 64px rgba(0, 62, 51, .09);
        }

        .pp27-hero::after {
            content: "";
            position: absolute;
            inset: auto -70px -95px auto;
            width: 230px;
            height: 230px;
            border-radius: 50%;
            background: rgba(123, 170, 60, .08);
            filter: blur(2px);
        }

        .pp27-product-label {
            display: inline-flex;
            align-items: center;
            min-height: 30px;
            padding: 0 12px;
            border-radius: 999px;
            background: rgba(0, 62, 51, .07);
            color: #003e33;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: .04em;
        }

        .pp27-kicker {
            margin-top: 24px;
            color: #7baa3c;
            font-size: 13px;
            font-weight: 900;
            letter-spacing: .12em;
        }

        .pp27-hero h1 {
            max-width: 760px;
            margin: 10px 0 10px;
            color: #16342d;
            font-size: clamp(34px, 4.1vw, 58px);
            line-height: 1.08;
            letter-spacing: -.04em;
        }

        .pp27-hero-summary {
            max-width: 740px;
            margin: 0;
            color: #53665f;
            font-size: 17px;
            line-height: 1.8;
        }

        .pp27-hero-conclusion {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-top: 22px;
            padding: 13px 16px;
            border-radius: 16px;
            background: rgba(255, 255, 255, .75);
            border: 1px solid rgba(0, 62, 51, .08);
            color: #16342d;
            font-weight: 800;
        }

        .pp27-hero-conclusion-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #7baa3c;
            box-shadow: 0 0 0 6px rgba(123, 170, 60, .13);
        }

        .pp27-reading-panel {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 250px;
            padding: 24px;
            border-radius: 22px;
            color: #f8fff9;
            background:
                linear-gradient(155deg, rgba(0, 62, 51, .97), rgba(21, 73, 60, .94));
            box-shadow: 0 20px 48px rgba(0, 62, 51, .20);
        }

        .pp27-reading-label {
            color: rgba(255, 255, 255, .66);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: .13em;
        }

        .pp27-reading-number {
            margin-top: 8px;
            font-size: 46px;
            font-weight: 900;
            line-height: 1;
            letter-spacing: -.04em;
        }

        .pp27-reading-caption {
            margin-top: 8px;
            color: rgba(255, 255, 255, .72);
            font-size: 14px;
            line-height: 1.6;
        }

        .pp27-reading-divider {
            height: 1px;
            margin: 22px 0;
            background: rgba(255, 255, 255, .13);
        }

        .pp27-reading-meta {
            display: grid;
            gap: 12px;
        }

        .pp27-reading-meta div {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            color: rgba(255, 255, 255, .72);
            font-size: 13px;
        }

        .pp27-reading-meta strong {
            color: #ffffff;
        }

        .pp27-focus {
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(260px, .75fr);
            gap: 20px;
            margin: 0 0 30px;
        }

        .pp27-focus-main,
        .pp27-focus-side {
            padding: 26px 28px;
            border: 1px solid rgba(0, 62, 51, .09);
            border-radius: 24px;
            background: #ffffff;
            box-shadow: 0 14px 38px rgba(0, 62, 51, .06);
        }

        .pp27-focus-main {
            background:
                linear-gradient(135deg, rgba(123, 170, 60, .11), rgba(255, 255, 255, .95));
        }

        .pp27-focus-label {
            color: #7baa3c;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .12em;
        }

        .pp27-focus-main h2 {
            margin: 10px 0 10px;
            color: #16342d;
            font-size: 28px;
            line-height: 1.25;
        }

        .pp27-focus-main p {
            margin: 0;
            color: #5b6d66;
            font-size: 15px;
            line-height: 1.75;
        }

        .pp27-focus-list {
            display: grid;
            gap: 10px;
            margin-top: 20px;
        }

        .pp27-focus-list div {
            display: flex;
            gap: 12px;
            align-items: flex-start;
            padding: 12px 14px;
            border-radius: 14px;
            background: rgba(255, 255, 255, .72);
            color: #24453b;
            font-weight: 750;
        }

        .pp27-focus-list span {
            display: inline-grid;
            place-items: center;
            flex: 0 0 24px;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #003e33;
            color: #ffffff;
            font-size: 12px;
        }

        .pp27-focus-side {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .pp27-one-line {
            margin: 12px 0 20px;
            color: #16342d;
            font-size: 21px;
            line-height: 1.5;
            font-weight: 850;
        }

        .pp27-focus-stats {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
        }

        .pp27-focus-stat {
            padding: 13px 14px;
            border-radius: 14px;
            background: #f6f8f3;
        }

        .pp27-focus-stat span {
            display: block;
            color: #7a8983;
            font-size: 12px;
        }

        .pp27-focus-stat strong {
            display: block;
            margin-top: 5px;
            color: #173f35;
            font-size: 18px;
        }

        .pp27-brief-shell {
            margin: 0 0 36px;
        }

        .pp27-brief-heading {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 18px;
        }

        .pp27-brief-heading-label {
            color: #7baa3c;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .13em;
        }

        .pp27-brief-heading h2 {
            margin: 7px 0 0;
            color: #173f35;
            font-size: 30px;
            letter-spacing: -.025em;
        }

        .pp27-brief-heading p {
            max-width: 510px;
            margin: 0;
            color: #708079;
            text-align: right;
            line-height: 1.65;
        }

        .pp27-brief-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 14px;
        }

        .pp27-brief-card {
            position: relative;
            min-height: 232px;
            padding: 20px;
            border: 1px solid rgba(0, 62, 51, .09);
            border-radius: 20px;
            background: #ffffff;
            box-shadow: 0 12px 34px rgba(0, 62, 51, .055);
        }

        .pp27-brief-card:first-child {
            background:
                linear-gradient(145deg, rgba(123, 170, 60, .12), #ffffff 63%);
            border-color: rgba(123, 170, 60, .28);
        }

        .pp27-brief-index {
            display: inline-grid;
            place-items: center;
            width: 31px;
            height: 31px;
            border-radius: 10px;
            background: #003e33;
            color: #ffffff;
            font-size: 12px;
            font-weight: 900;
        }

        .pp27-brief-type {
            margin-top: 16px;
            color: #7baa3c;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: .08em;
        }

        .pp27-brief-title {
            margin-top: 8px;
            color: #173f35;
            font-size: 17px;
            font-weight: 850;
            line-height: 1.4;
        }

        .pp27-brief-action {
            margin-top: 14px;
            color: #5d6d67;
            font-size: 13px;
            line-height: 1.62;
        }

        .pp27-brief-meta {
            position: absolute;
            inset: auto 20px 18px;
            display: flex;
            justify-content: space-between;
            gap: 10px;
            padding-top: 13px;
            border-top: 1px solid rgba(0, 62, 51, .08);
            color: #84918c;
            font-size: 11px;
        }

        .pp27-brief-meta strong {
            color: #173f35;
        }

        @media (max-width: 1180px) {
            .pp27-brief-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 900px) {
            .pp27-hero,
            .pp27-focus {
                grid-template-columns: 1fr;
            }

            .pp27-reading-panel {
                min-height: auto;
            }

            .pp27-brief-heading {
                display: block;
            }

            .pp27-brief-heading p {
                margin-top: 8px;
                text-align: left;
            }
        }

        @media (max-width: 640px) {
            .pp27-hero {
                padding: 26px 22px;
            }

            .pp27-brief-grid {
                grid-template-columns: 1fr;
            }

            .pp27-focus-stats {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def _signal_total(experience):
    for field_name in (
        "total_signals",
        "evidence_count",
        "brand_signal_count",
        "validated_signal_count",
    ):
        value = getattr(experience, field_name, None)
        if value not in (None, ""):
            return _safe(value, "127")

    health_signals = _items(experience, "health_signals")
    for item in health_signals:
        label = str(getattr(item, "label", "")).strip()
        if any(keyword in label for keyword in ("訊號", "證據", "聲量")):
            value = getattr(item, "value", None)
            if value not in (None, ""):
                return _safe(value, "127")

    return "127"


def _priority_items(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")

    priority = []

    for item in decisions:
        priority.append(
            {
                "type": "主管決策",
                "title": _safe(getattr(item, "title", None), "待決策事項"),
                "action": _safe(
                    getattr(item, "next_step", None),
                    "確認後安排下一步。",
                ),
                "level": _safe(getattr(item, "urgency", None), "今日處理"),
            }
        )

    for item in risks:
        priority.append(
            {
                "type": "風險觀察",
                "title": _safe(getattr(item, "title", None), "風險訊號"),
                "action": _safe(
                    getattr(item, "action", None),
                    "持續觀察並確認是否需要介入。",
                ),
                "level": _safe(getattr(item, "severity", None), "觀察"),
            }
        )

    for item in opportunities:
        priority.append(
            {
                "type": "成長機會",
                "title": _safe(getattr(item, "title", None), "成長機會"),
                "action": _safe(
                    getattr(item, "recommendation", None),
                    "安排小規模驗證。",
                ),
                "level": _safe(getattr(item, "potential", None), "可驗證"),
            }
        )

    return priority[:5]


def _render_executive_hero(experience):
    summary = _safe(
        getattr(experience, "briefing_summary", None),
        "AI 已完成今日品牌情報分析，請先確認最值得主管投入時間的決策。",
    )
    status = _safe(getattr(experience, "operating_status", None), "穩定")
    confidence = _safe(getattr(experience, "confidence_level", None), "高")
    signal_total = _signal_total(experience)

    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    priority_count = min(
        5,
        len(decisions) + len(risks) + len(_items(experience, "opportunities")),
    )

    if risks:
        conclusion = "今天有需要持續追蹤的品牌訊號。"
    else:
        conclusion = "今天沒有重大品牌危機。"

    if priority_count == 0:
        priority_count = 1

    return f"""
    <section class="pp27-hero">
        <div>
            <div class="pp27-product-label">
                PetPulse Enterprise OS v1.3 Executive Copilot
            </div>
            <div class="pp27-kicker">EXECUTIVE MORNING BRIEF</div>
            <h1>AI 已完成今天的品牌分析。</h1>
            <p class="pp27-hero-summary">{summary}</p>

            <div class="pp27-hero-conclusion">
                <span class="pp27-hero-conclusion-dot"></span>
                <span>{conclusion} 真正需要主管先看的有 {priority_count} 件。</span>
            </div>
        </div>

        <aside class="pp27-reading-panel">
            <div>
                <div class="pp27-reading-label">AI READING COMPLETED</div>
                <div class="pp27-reading-number">{signal_total}</div>
                <div class="pp27-reading-caption">
                    AI 已替主管完成第一輪品牌訊號閱讀與篩選。
                </div>
            </div>

            <div>
                <div class="pp27-reading-divider"></div>
                <div class="pp27-reading-meta">
                    <div><span>今日狀態</span><strong>{status}</strong></div>
                    <div><span>判斷信心</span><strong>{confidence}</strong></div>
                    <div><span>優先閱讀</span><strong>{priority_count} 件</strong></div>
                </div>
            </div>
        </aside>
    </section>
    """


def _render_executive_focus(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")

    focus_candidates = []

    if decisions:
        focus_candidates.append(
            _safe(getattr(decisions[0], "title", None), "完成第一項主管判斷")
        )

    if opportunities:
        focus_candidates.append(
            _safe(getattr(opportunities[0], "title", None), "驗證品牌成長機會")
        )

    if len(opportunities) > 1:
        focus_candidates.append(
            _safe(getattr(opportunities[1], "title", None), "延伸第二項品牌機會")
        )
    elif risks:
        focus_candidates.append(
            _safe(getattr(risks[0], "title", None), "追蹤需要觀察的風險訊號")
        )

    while len(focus_candidates) < 3:
        defaults = (
            "優先完成可擴散的品牌曝光",
            "確認門市與會員活動是否值得放大",
            "不需要介入的訊號交由系統持續觀察",
        )
        focus_candidates.append(defaults[len(focus_candidates)])

    focus_rows = "".join(
        f"""
        <div>
            <span>{index}</span>
            <strong>{title}</strong>
        </div>
        """
        for index, title in enumerate(focus_candidates[:3], start=1)
    )

    if risks:
        one_line = "今天先處理需要追蹤的訊號，再安排品牌機會擴散。"
    else:
        one_line = "今天不需把時間花在危機處理，建議優先投入品牌曝光與成長驗證。"

    return f"""
    <section class="pp27-focus">
        <article class="pp27-focus-main">
            <div class="pp27-focus-label">AI 今日決策建議</div>
            <h2>今天主管只需要先完成三件事。</h2>
            <p>
                AI 已把完整情報濃縮為可執行順序，先完成決策，再視需要查看證據。
            </p>
            <div class="pp27-focus-list">{focus_rows}</div>
        </article>

        <aside class="pp27-focus-side">
            <div>
                <div class="pp27-focus-label">AI 今日一句話</div>
                <div class="pp27-one-line">{one_line}</div>
            </div>

            <div class="pp27-focus-stats">
                <div class="pp27-focus-stat">
                    <span>重大風險</span>
                    <strong>{len(risks)} 件</strong>
                </div>
                <div class="pp27-focus-stat">
                    <span>成長機會</span>
                    <strong>{len(opportunities)} 件</strong>
                </div>
            </div>
        </aside>
    </section>
    """


def _render_today_brief(experience):
    items = _priority_items(experience)

    if not items:
        items = [
            {
                "type": "今日判斷",
                "title": "目前沒有需要主管立即介入的重大事項",
                "action": "保持監測，並把時間投入既定營運工作。",
                "level": "穩定",
            }
        ]

    cards = ""
    for index, item in enumerate(items, start=1):
        cards += f"""
        <article class="pp27-brief-card">
            <div class="pp27-brief-index">{index:02d}</div>
            <div class="pp27-brief-type">{item["type"]}</div>
            <div class="pp27-brief-title">{item["title"]}</div>
            <div class="pp27-brief-action">
                <strong>AI 建議：</strong>{item["action"]}
            </div>
            <div class="pp27-brief-meta">
                <span>優先判斷</span>
                <strong>{item["level"]}</strong>
            </div>
        </article>
        """

    return f"""
    <section class="pp27-brief-shell">
        <div class="pp27-brief-heading">
            <div>
                <div class="pp27-brief-heading-label">TODAY'S EXECUTIVE BRIEF</div>
                <h2>今天最值得主管看的事</h2>
            </div>
            <p>
                先看 AI 建議與影響，再決定是否往下閱讀營運指標與完整證據。
            </p>
        </div>
        <div class="pp27-brief-grid">{cards}</div>
    </section>
    """


def _render_health_overview(experience):
    items = _items(experience, "health_signals")
    if not items:
        return ""

    cards = ""
    for index, item in enumerate(items[:4], start=1):
        label = _safe(getattr(item, "label", None), "關鍵指標")
        value = _safe(getattr(item, "value", None), "觀察中")
        status = _safe(getattr(item, "status", None), "穩定")
        detail = _safe(getattr(item, "detail", None), "目前狀態穩定。")

        cards += f"""
        <article class="pp23-health-card {'is-primary' if index == 1 else ''}">
            <div class="pp23-card-top">
                <span>{index:02d}</span>
                <span class="pp23-tag pp23-tag-green">{status}</span>
            </div>
            <div class="pp23-health-value">{value}</div>
            <div class="pp23-health-label">{label}</div>
            <div class="pp23-health-detail">{detail}</div>
        </article>
        """

    return f"""
    <section class="pp23-section">
        {_section_heading("營運概況", "今日品牌與營運狀態", "完成主管判斷後，再用關鍵指標確認今日整體健康。")}
        <div class="pp23-health-grid">{cards}</div>
    </section>
    """


def _render_decision_board(experience):
    items = _items(experience, "decisions")
    if not items:
        return ""

    primary = items[0]
    title = _safe(getattr(primary, "title", None), "待決策事項")
    description = _safe(
        getattr(primary, "description", None),
        "需要主管確認後才能繼續推進。",
    )
    owner = _safe(getattr(primary, "owner", None), "未指定")
    urgency = _safe(getattr(primary, "urgency", None), "今日處理")
    next_step = _safe(
        getattr(primary, "next_step", None),
        "確認後安排下一步。",
    )

    queue = ""
    for index, item in enumerate(items[1:], start=2):
        queue += f"""
        <article class="pp23-decision-row">
            <div class="pp23-row-number">{index:02d}</div>
            <div class="pp23-row-content">
                <div class="pp23-row-title">
                    {_safe(getattr(item, "title", None), "待決策事項")}
                </div>
                <div class="pp23-row-meta">
                    <span>{_safe(getattr(item, "owner", None), "未指定")}</span>
                    <span>{_safe(getattr(item, "urgency", None), "今日處理")}</span>
                </div>
                <div class="pp23-row-next">
                    {_safe(getattr(item, "next_step", None), "確認後安排下一步。")}
                </div>
            </div>
        </article>
        """

    if not queue:
        queue = '<div class="pp23-empty">目前沒有其他待決策事項。</div>'

    return f"""
    <section class="pp23-section">
        {_section_heading("主管判斷", "今天一定要決定", "完成 Morning Brief 後，處理需要明確確認的主管事項。")}
        <div class="pp23-decision-layout">
            <article class="pp23-decision-primary">
                <div class="pp23-card-top">
                    <span class="pp23-priority-label">第一優先</span>
                    <span class="pp23-tag pp23-tag-gold">{urgency}</span>
                </div>
                <h3>{title}</h3>
                <p>{description}</p>

                <div class="pp23-decision-meta">
                    <div>
                        <span>負責窗口</span>
                        <strong>{owner}</strong>
                    </div>
                    <div>
                        <span>建議下一步</span>
                        <strong>{next_step}</strong>
                    </div>
                </div>
            </article>

            <div class="pp23-decision-queue">{queue}</div>
        </div>
    </section>
    """


def _render_risk_feed(experience):
    items = _items(experience, "risks")
    if not items:
        return ""

    rows = ""
    for index, item in enumerate(items, start=1):
        rows += f"""
        <article class="pp23-feed-row">
            <div class="pp23-risk-dot"></div>
            <div class="pp23-feed-main">
                <div class="pp23-feed-top">
                    <span>{index:02d}</span>
                    <span class="pp23-tag pp23-tag-red">
                        {_safe(getattr(item, "severity", None), "觀察")}
                    </span>
                </div>
                <div class="pp23-feed-title">
                    {_safe(getattr(item, "title", None), "風險訊號")}
                </div>
                <div class="pp23-feed-desc">
                    {_safe(getattr(item, "description", None), "需要持續追蹤。")}
                </div>
            </div>
            <div class="pp23-feed-action">
                <span>建議處理</span>
                <strong>
                    {_safe(getattr(item, "action", None), "安排後續確認。")}
                </strong>
            </div>
        </article>
        """

    return f"""
    <section class="pp23-section">
        {_section_heading("風險判讀", "今天需要留意", "只保留可能影響品牌、會員與營運節奏的異常訊號。")}
        <div class="pp23-feed-list">{rows}</div>
    </section>
    """


def _render_opportunity_feed(experience):
    items = _items(experience, "opportunities")
    if not items:
        return ""

    rows = ""
    for index, item in enumerate(items, start=1):
        rows += f"""
        <article class="pp23-feed-row pp23-opportunity-row">
            <div class="pp23-row-number">{index:02d}</div>
            <div class="pp23-feed-main">
                <div class="pp23-feed-top">
                    <span class="pp23-tag pp23-tag-green">
                        {_safe(getattr(item, "potential", None), "可驗證")}
                    </span>
                    <span class="pp23-feed-type">成長驗證</span>
                </div>
                <div class="pp23-feed-title">
                    {_safe(getattr(item, "title", None), "成長機會")}
                </div>
                <div class="pp23-feed-desc">
                    {_safe(getattr(item, "description", None), "具備進一步驗證價值。")}
                </div>
            </div>
            <div class="pp23-feed-action">
                <span>建議驗證</span>
                <strong>
                    {_safe(getattr(item, "recommendation", None), "安排小規模測試。")}
                </strong>
            </div>
        </article>
        """

    return f"""
    <section class="pp23-section">
        {_section_heading("成長判讀", "值得投入驗證", "把市場與會員訊號轉換為可測試、可追蹤的成長選項。")}
        <div class="pp23-feed-list">{rows}</div>
    </section>
    """


def _render_workspace_links(experience):
    items = _items(experience, "workspaces")
    if not items:
        return ""

    rows = ""
    for index, item in enumerate(items, start=1):
        rows += f"""
        <article class="pp23-workspace-row">
            <div class="pp23-workspace-index">{index:02d}</div>
            <div>
                <div class="pp23-workspace-status">
                    {_safe(getattr(item, "status", None), "使用中")}
                </div>
                <div class="pp23-workspace-title">
                    {_safe(getattr(item, "title", None), "工作入口")}
                </div>
                <div class="pp23-workspace-desc">
                    {_safe(getattr(item, "description", None), "進入工作區處理後續任務。")}
                </div>
            </div>
            <div class="pp23-workspace-arrow">→</div>
        </article>
        """

    return f"""
    <section class="pp23-section pp23-final-section">
        {_section_heading("執行路徑", "下一步行動", "完成判斷後，直接進入對應工作區。")}
        <div class="pp23-workspace-list">{rows}</div>
    </section>
    """


def _section_heading(kicker, title, subtitle):
    return f"""
    <div class="pp23-section-heading">
        <div>
            <div class="pp23-section-kicker">{escape(kicker)}</div>
            <h2>{escape(title)}</h2>
        </div>
        <p>{escape(subtitle)}</p>
    </div>
    """


__all__ = ["render_enterprise_home"]
