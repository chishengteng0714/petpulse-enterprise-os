import streamlit as st
from html import escape
from pathlib import Path

from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_enterprise_home(runtime=None):
    """
    PetPulse Enterprise OS v1.0 Golden Master

    GM-13 Phase 2：
    - Presentation Layer Only
    - 不修改 Runtime / Registry / State / Schema
    - 不修改 Business Logic
    - Hero Dashboard 2.0
    - 非對稱主管決策首頁
    - 全中文企業資訊架構
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

    st.markdown(html, unsafe_allow_html=True)


def _load_enterprise_css():
    css_path = Path(__file__).resolve().parents[3] / "assets" / "enterprise.css"

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _safe(value, fallback=""):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()

    if not text:
        return escape(str(fallback))

    return escape(text)


def _items(experience, name):
    return getattr(experience, name, []) or []


def _section(icon, eyebrow, title, subtitle, count=None, count_label="項"):
    count_html = ""

    if count is not None:
        count_html = f"""
        <div class="pp-badge gold">{count} {count_label}</div>
        """

    return f"""
<section class="pp-section-header pp-enterprise-section-header">
    <div class="pp-section-icon pp-enterprise-section-icon">{icon}</div>

    <div class="pp-section-copy">
        <div class="pp-card-kicker">{eyebrow}</div>
        <div class="pp-section-title">{title}</div>
        <div class="pp-section-subtitle">{subtitle}</div>
    </div>

    {count_html}
</section>
"""


def _empty_state(icon, kicker, title, description, badge="目前穩定"):
    return f"""
<section class="pp-callout">
    <div class="pp-card-top">
        <div class="pp-card-index">{icon}</div>
        <div class="pp-badge success">{badge}</div>
    </div>

    <div class="pp-card-kicker">{kicker}</div>
    <div class="pp-card-title">{title}</div>
    <div class="pp-card-desc">{description}</div>
</section>
"""


def _severity_level(value):
    text = str(value or "").strip().lower()

    if any(token in text for token in ("重大", "嚴重", "高", "critical", "high")):
        return "高", 92, "critical"

    if any(token in text for token in ("中", "medium")):
        return "中", 64, ""

    if any(token in text for token in ("低", "low")):
        return "低", 36, ""

    return str(value or "觀察"), 48, ""


def _render_hero(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    opportunities = _items(experience, "opportunities")
    health_signals = _items(experience, "health_signals")

    title = _safe(
        getattr(experience, "briefing_title", None),
        "今日企業決策總覽",
    )
    summary = _safe(
        getattr(experience, "briefing_summary", None),
        "整合今日營運狀態、待決策事項、風險訊號與成長機會，協助主管快速完成判斷。",
    )
    greeting = _safe(
        getattr(experience, "greeting", None),
        "今日企業首頁",
    )
    operating_status = _safe(
        getattr(experience, "operating_status", None),
        "營運穩定",
    )
    confidence_level = _safe(
        getattr(experience, "confidence_level", None),
        "高信心",
    )

    primary_health = "尚待更新"
    primary_health_label = "企業健康"

    if health_signals:
        primary_health = _safe(
            getattr(health_signals[0], "value", None),
            "觀察中",
        )
        primary_health_label = _safe(
            getattr(health_signals[0], "label", None),
            "企業健康",
        )

    top_decision = (
        _safe(getattr(decisions[0], "title", None), "今日暫無待決策事項")
        if decisions
        else "今日暫無待決策事項"
    )

    top_risk = (
        _safe(getattr(risks[0], "title", None), "目前沒有重大風險")
        if risks
        else "目前沒有重大風險"
    )

    top_opportunity = (
        _safe(getattr(opportunities[0], "title", None), "持續觀察成長訊號")
        if opportunities
        else "持續觀察成長訊號"
    )

    return f"""
<section class="pp-hero pp-enterprise-hero">
    <div class="pp-hero-dashboard">
        <div class="pp-hero-main">
            <div class="pp-product-signature">PetPulse 企業決策作業系統</div>
            <div class="pp-hero-kicker">今日主管決策台</div>

            <h1 class="pp-hero-title">{title}</h1>

            <div class="pp-hero-summary">
                {summary}
            </div>

            <div class="pp-hero-meta">
                <div class="pp-badge dark">{greeting}</div>
                <div class="pp-badge dark">營運狀態：{operating_status}</div>
                <div class="pp-badge dark">判斷信心：{confidence_level}</div>
            </div>

            <div class="pp-executive-strip">
                <div class="pp-executive-strip-item">
                    <span class="pp-executive-strip-label">{primary_health_label}</span>
                    <strong>{primary_health}</strong>
                </div>

                <div class="pp-executive-strip-item">
                    <span class="pp-executive-strip-label">今日待決策</span>
                    <strong>{len(decisions)} 項</strong>
                </div>

                <div class="pp-executive-strip-item">
                    <span class="pp-executive-strip-label">風險與機會</span>
                    <strong>{len(risks)} 項風險・{len(opportunities)} 項機會</strong>
                </div>
            </div>
        </div>

        <aside class="pp-hero-side">
            <div class="pp-hero-signal">
                <div class="pp-hero-signal-label">今日首要決策</div>
                <div class="pp-hero-signal-value">{top_decision}</div>
                <div class="pp-hero-signal-note">
                    優先確認後，讓團隊能立即往下執行。
                </div>
            </div>

            <div class="pp-hero-signal">
                <div class="pp-hero-signal-label">最高風險</div>
                <div class="pp-hero-signal-value">{top_risk}</div>
                <div class="pp-hero-signal-note">
                    先看影響範圍，再判斷是否需要主管介入。
                </div>
            </div>

            <div class="pp-hero-signal">
                <div class="pp-hero-signal-label">優先成長機會</div>
                <div class="pp-hero-signal-value">{top_opportunity}</div>
                <div class="pp-hero-signal-note">
                    以小規模、短週期方式降低驗證成本。
                </div>
            </div>
        </aside>
    </div>
</section>
"""


def _render_health(experience):
    items = _items(experience, "health_signals")

    if not items:
        return (
            _section(
                "衡",
                "營運總覽",
                "企業健康",
                "用核心指標與輔助訊號，判斷今日營運是否需要主管介入。",
                0,
                "項",
            )
            + _empty_state(
                "衡",
                "健康訊號",
                "目前沒有可顯示的營運訊號",
                "健康資料尚未提供，請稍後再確認企業營運狀態。",
                "等待資料",
            )
        )

    feature = items[0]
    supporting = items[1:4]

    support_html = ""

    for item in supporting:
        support_html += f"""
<article class="pp-card-compact">
    <div class="pp-card-top">
        <div class="pp-card-kicker">輔助營運訊號</div>
        <div class="pp-health">
            {_safe(getattr(item, "status", None), "穩定")}
        </div>
    </div>

    <div class="pp-card-value">
        {_safe(getattr(item, "value", None), "觀察中")}
    </div>

    <div class="pp-card-title">
        {_safe(getattr(item, "label", None), "關鍵指標")}
    </div>

    <div class="pp-card-desc">
        {_safe(getattr(item, "detail", None), "目前狀態穩定。")}
    </div>
</article>
"""

    if not support_html:
        support_html = """
<article class="pp-card-compact">
    <div class="pp-card-kicker">輔助營運訊號</div>
    <div class="pp-card-title">核心訊號集中</div>
    <div class="pp-card-desc">
        今日主要判斷已集中於左側核心健康指標。
    </div>
</article>
"""

    return f"""
{_section(
    "衡",
    "營運總覽",
    "企業健康",
    "以一個主指標搭配輔助訊號，快速確認今日是否需要主管介入。",
    len(items),
    "項",
)}

<section class="pp-grid pp-grid-large-small">
    <article class="pp-card-large">
        <div class="pp-card-top">
            <div>
                <div class="pp-card-kicker">核心健康指標</div>
                <div class="pp-card-title">
                    {_safe(getattr(feature, "label", None), "企業健康度")}
                </div>
            </div>

            <div class="pp-health">
                {_safe(getattr(feature, "status", None), "穩定")}
            </div>
        </div>

        <div class="pp-card-value">
            {_safe(getattr(feature, "value", None), "觀察中")}
        </div>

        <div class="pp-card-desc">
            {_safe(getattr(feature, "detail", None), "目前企業營運狀態穩定。")}
        </div>

        <div class="pp-card-meta">
            <strong>主管判讀</strong><br>
            優先檢查是否出現偏離日常營運基準的異常訊號。
        </div>
    </article>

    <div class="pp-stack">
        {support_html}
    </div>
</section>
"""


def _render_decisions(experience):
    items = _items(experience, "decisions")

    if not items:
        return (
            _section(
                "決",
                "今日優先",
                "決策中樞",
                "聚焦需要主管拍板的事項，避免重要工作因等待判斷而停滯。",
                0,
                "項",
            )
            + _empty_state(
                "決",
                "決策狀態",
                "今日暫無待決策事項",
                "目前沒有需要主管立即確認的事項，可依序檢視企業健康與風險訊號。",
                "決策清空",
            )
        )

    feature = items[0]
    supporting = items[1:]

    supporting_html = ""

    for index, item in enumerate(supporting, start=2):
        supporting_html += f"""
<article class="pp-card-summary">
    <div class="pp-card-top">
        <div class="pp-card-index">{index:02d}</div>
        <div class="pp-priority">
            {_safe(getattr(item, "urgency", None), "今日處理")}
        </div>
    </div>

    <div class="pp-card-title">
        {_safe(getattr(item, "title", None), "待決策事項")}
    </div>

    <div class="pp-card-desc">
        {_safe(getattr(item, "description", None), "需要主管確認後才能繼續推進。")}
    </div>

    <div class="pp-card-meta">
        <strong>負責窗口</strong><br>
        {_safe(getattr(item, "owner", None), "未指定")}
        <br><br>
        <strong>建議下一步</strong><br>
        {_safe(getattr(item, "next_step", None), "確認後安排下一步。")}
    </div>
</article>
"""

    if not supporting_html:
        supporting_html = """
<article class="pp-card-summary">
    <div class="pp-card-kicker">決策佇列</div>
    <div class="pp-card-title">今日焦點集中</div>
    <div class="pp-card-desc">
        今日唯一待決策事項已提升為主要決策卡。
    </div>
</article>
"""

    return f"""
{_section(
    "決",
    "今日優先",
    "決策中樞",
    "以一項主要決策搭配輔助決策佇列，建立清楚的主管拍板順序。",
    len(items),
    "項",
)}

<section class="pp-grid pp-grid-8-4">
    <article class="pp-card-highlight">
        <div class="pp-card-top">
            <div class="pp-card-index">01</div>
            <div class="pp-priority">
                {_safe(getattr(feature, "urgency", None), "今日確認")}
            </div>
        </div>

        <div class="pp-card-kicker">今日主要決策</div>

        <div class="pp-card-title">
            {_safe(getattr(feature, "title", None), "待決策事項")}
        </div>

        <div class="pp-card-desc">
            {_safe(getattr(feature, "description", None), "需要主管確認後才能繼續推進。")}
        </div>

        <div class="pp-card-meta">
            <strong>負責窗口</strong><br>
            {_safe(getattr(feature, "owner", None), "未指定")}
            <br><br>
            <strong>建議下一步</strong><br>
            {_safe(getattr(feature, "next_step", None), "確認後安排下一步。")}
        </div>
    </article>

    <div class="pp-stack">
        {supporting_html}
    </div>
</section>
"""


def _render_risks(experience):
    items = _items(experience, "risks")

    if not items:
        return (
            _section(
                "警",
                "風險排序",
                "企業風險觀測",
                "依照風險強度排列異常訊號，讓主管先處理影響最大的事項。",
                0,
                "項",
            )
            + _empty_state(
                "警",
                "風險狀態",
                "今日暫無明顯風險訊號",
                "目前沒有需要主管立即介入的異常訊號，建議持續觀察關鍵指標。",
                "風險穩定",
            )
        )

    feature = items[0]
    secondary = items[1:]

    feature_level, feature_weight, feature_class = _severity_level(
        getattr(feature, "severity", None)
    )

    secondary_html = ""

    for index, item in enumerate(secondary, start=2):
        level, weight, critical_class = _severity_level(
            getattr(item, "severity", None)
        )

        secondary_html += f"""
<article class="pp-risk-card {critical_class}">
    <div class="pp-card-top">
        <div class="pp-card-index">{index:02d}</div>
        <div class="pp-severity">{_safe(level)}風險</div>
    </div>

    <div class="pp-card-title">
        {_safe(getattr(item, "title", None), "風險訊號")}
    </div>

    <div class="pp-card-desc">
        {_safe(getattr(item, "description", None), "需要持續追蹤。")}
    </div>

    <div class="pp-risk-priority">
        <div class="pp-risk-bar">
            <span style="width: {weight}%"></span>
        </div>
        <div class="pp-risk-weight">{weight}%</div>
    </div>

    <div class="pp-card-meta">
        <strong>建議處理</strong><br>
        {_safe(getattr(item, "action", None), "安排後續確認。")}
    </div>
</article>
"""

    if not secondary_html:
        secondary_html = """
<article class="pp-card-summary">
    <div class="pp-card-kicker">次要風險</div>
    <div class="pp-card-title">目前沒有其他高權重風險</div>
    <div class="pp-card-desc">
        今日風險焦點已集中於左側主要風險。
    </div>
</article>
"""

    return f"""
{_section(
    "警",
    "風險排序",
    "企業風險觀測",
    "先處理最高權重風險，再依序檢視次要異常訊號。",
    len(items),
    "項",
)}

<section class="pp-grid pp-grid-7-5">
    <article class="pp-risk-card {feature_class}">
        <div class="pp-card-top">
            <div class="pp-card-index">01</div>
            <div class="pp-severity">{_safe(feature_level)}風險</div>
        </div>

        <div class="pp-card-kicker">最高權重風險</div>

        <div class="pp-card-title">
            {_safe(getattr(feature, "title", None), "風險訊號")}
        </div>

        <div class="pp-card-desc">
            {_safe(getattr(feature, "description", None), "需要持續追蹤。")}
        </div>

        <div class="pp-risk-priority">
            <div class="pp-risk-bar">
                <span style="width: {feature_weight}%"></span>
            </div>
            <div class="pp-risk-weight">{feature_weight}%</div>
        </div>

        <div class="pp-card-meta">
            <strong>主管行動</strong><br>
            {_safe(getattr(feature, "action", None), "安排後續確認。")}
        </div>
    </article>

    <div class="pp-stack">
        {secondary_html}
    </div>
</section>
"""


def _render_opportunities(experience):
    items = _items(experience, "opportunities")

    if not items:
        return (
            _section(
                "增",
                "策略選項",
                "企業成長機會",
                "用潛力、投入方式與驗證節奏，辨識值得測試的成長選項。",
                0,
                "項",
            )
            + _empty_state(
                "增",
                "成長訊號",
                "今日暫無明顯成長機會",
                "目前沒有需要立即安排驗證或資源投入的機會訊號。",
                "持續觀察",
            )
        )

    feature = items[0]
    secondary = items[1:]

    feature_potential = _safe(
        getattr(feature, "potential", None),
        "可驗證",
    )

    secondary_html = ""

    for index, item in enumerate(secondary, start=2):
        potential = _safe(getattr(item, "potential", None), "可驗證")

        secondary_html += f"""
<article class="pp-opportunity-card">
    <div class="pp-card-top">
        <div class="pp-card-index">{index:02d}</div>
        <div class="pp-roi">{potential}</div>
    </div>

    <div class="pp-card-title">
        {_safe(getattr(item, "title", None), "成長機會")}
    </div>

    <div class="pp-card-desc">
        {_safe(getattr(item, "description", None), "具備進一步驗證價值。")}
    </div>

    <div class="pp-opportunity-metrics">
        <div class="pp-opportunity-metric">
            <span>成長潛力</span>
            <strong>{potential}</strong>
        </div>

        <div class="pp-opportunity-metric">
            <span>投入方式</span>
            <strong>小規模</strong>
        </div>

        <div class="pp-opportunity-metric">
            <span>驗證節奏</span>
            <strong>短週期</strong>
        </div>
    </div>

    <div class="pp-card-meta">
        <strong>建議行動</strong><br>
        {_safe(getattr(item, "recommendation", None), "建議安排小規模測試。")}
    </div>
</article>
"""

    if not secondary_html:
        secondary_html = """
<article class="pp-card-summary">
    <div class="pp-card-kicker">次要機會</div>
    <div class="pp-card-title">今日成長焦點集中</div>
    <div class="pp-card-desc">
        目前最值得驗證的機會已提升為左側主要策略卡。
    </div>
</article>
"""

    return f"""
{_section(
    "增",
    "策略選項",
    "企業成長機會",
    "先驗證最高潛力機會，再依投入成本與週期安排後續測試。",
    len(items),
    "項",
)}

<section class="pp-grid pp-grid-8-4">
    <article class="pp-card-large pp-opportunity-card">
        <div class="pp-card-top">
            <div class="pp-card-index">01</div>
            <div class="pp-roi">{feature_potential}</div>
        </div>

        <div class="pp-card-kicker">優先成長機會</div>

        <div class="pp-card-title">
            {_safe(getattr(feature, "title", None), "成長機會")}
        </div>

        <div class="pp-card-desc">
            {_safe(getattr(feature, "description", None), "具備進一步驗證價值。")}
        </div>

        <div class="pp-opportunity-metrics">
            <div class="pp-opportunity-metric">
                <span>成長潛力</span>
                <strong>{feature_potential}</strong>
            </div>

            <div class="pp-opportunity-metric">
                <span>投入方式</span>
                <strong>小規模</strong>
            </div>

            <div class="pp-opportunity-metric">
                <span>驗證節奏</span>
                <strong>短週期</strong>
            </div>
        </div>

        <div class="pp-card-meta">
            <strong>主管建議</strong><br>
            {_safe(getattr(feature, "recommendation", None), "建議安排小規模測試。")}
        </div>
    </article>

    <div class="pp-stack">
        {secondary_html}
    </div>
</section>
"""


def _workspace_icon(index, title):
    """
    僅依既有標題選擇呈現符號，不改變 Workspace 資料與行為。
    """

    text = str(title or "")

    if "證據" in text:
        return "證"

    if "調查" in text or "深入" in text:
        return "研"

    if "工作" in text or "執行" in text:
        return "行"

    return f"{index:02d}"


def _render_workspaces(experience):
    items = _items(experience, "workspaces")

    if not items:
        return (
            _section(
                "行",
                "執行入口",
                "企業工作區",
                "把今日判斷轉換成可立即推進的執行路徑。",
                0,
                "個入口",
            )
            + _empty_state(
                "行",
                "工作入口",
                "今日暫無建議工作入口",
                "目前沒有需要立即切換的工作區，請先完成今日決策判斷。",
                "等待指派",
            )
        )

    primary = items[0]
    secondary = items[1:]

    primary_title = _safe(
        getattr(primary, "title", None),
        "企業工作區",
    )
    primary_description = _safe(
        getattr(primary, "description", None),
        "承接今日決策並安排後續執行。",
    )
    primary_status = _safe(
        getattr(primary, "status", None),
        "可使用",
    )
    primary_target = _safe(
        getattr(primary, "target", None),
        "工作區",
    )
    primary_icon = _workspace_icon(
        1,
        getattr(primary, "title", None),
    )

    secondary_html = ""

    for index, item in enumerate(secondary, start=2):
        title = _safe(
            getattr(item, "title", None),
            "工作入口",
        )
        description = _safe(
            getattr(item, "description", None),
            "查看相關資訊並安排下一步。",
        )
        status = _safe(
            getattr(item, "status", None),
            "可使用",
        )
        target = _safe(
            getattr(item, "target", None),
            "工作區",
        )
        icon = _workspace_icon(
            index,
            getattr(item, "title", None),
        )

        secondary_html += f"""
<article class="pp-launcher-row">
    <div class="pp-launcher-row-icon">{icon}</div>

    <div class="pp-launcher-row-copy">
        <div class="pp-launcher-row-head">
            <div class="pp-launcher-row-title">{title}</div>
            <div class="pp-launcher-row-status">{status}</div>
        </div>

        <div class="pp-launcher-row-desc">
            {description}
        </div>

        <div class="pp-launcher-row-foot">
            <span>目標位置</span>
            <strong>{target}</strong>
        </div>
    </div>

    <div class="pp-launcher-row-arrow">→</div>
</article>
"""

    if not secondary_html:
        secondary_html = """
<article class="pp-launcher-row">
    <div class="pp-launcher-row-icon">候</div>

    <div class="pp-launcher-row-copy">
        <div class="pp-launcher-row-head">
            <div class="pp-launcher-row-title">其他工作入口待命</div>
            <div class="pp-launcher-row-status">穩定</div>
        </div>

        <div class="pp-launcher-row-desc">
            今日執行焦點已集中於左側主要工作區。
        </div>

        <div class="pp-launcher-row-foot">
            <span>目前狀態</span>
            <strong>無需切換</strong>
        </div>
    </div>
</article>
"""

    return f"""
{_section(
    "行",
    "執行入口",
    "企業工作區",
    "以一個主要入口承接今日決策，其餘工作區依任務順序快速切換。",
    len(items),
    "個入口",
)}

<style>
.pp-enterprise-launcher {{
    display: grid;
    grid-template-columns: minmax(0, 1.38fr) minmax(360px, 0.82fr);
    gap: 1rem;
    align-items: stretch;
}}

.pp-launcher-feature {{
    position: relative;
    isolation: isolate;
    overflow: hidden;
    min-height: 330px;
    padding: 1.9rem;
    border-radius: 30px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background:
        radial-gradient(
            circle at 88% 10%,
            rgba(216, 183, 106, 0.24),
            transparent 30%
        ),
        radial-gradient(
            circle at 8% 100%,
            rgba(123, 170, 60, 0.18),
            transparent 34%
        ),
        linear-gradient(
            135deg,
            #001f1a 0%,
            #003e33 72%,
            #0a5247 100%
        );
    box-shadow:
        0 34px 84px rgba(0, 38, 31, 0.23),
        inset 0 1px 0 rgba(255, 255, 255, 0.10);
    color: #ffffff;
}}

.pp-launcher-feature::after {{
    content: "";
    position: absolute;
    right: -76px;
    bottom: -76px;
    z-index: -1;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow:
        0 0 0 42px rgba(255, 255, 255, 0.025),
        0 0 0 88px rgba(255, 255, 255, 0.014);
}}

.pp-launcher-feature-top {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}}

.pp-launcher-feature-icon {{
    width: 58px;
    height: 58px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.11);
    border: 1px solid rgba(255, 255, 255, 0.16);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.12),
        0 16px 34px rgba(0, 0, 0, 0.15);
    color: #ffffff;
    font-size: 1rem;
    font-weight: 930;
}}

.pp-launcher-feature-status {{
    display: inline-flex;
    align-items: center;
    gap: 0.38rem;
    padding: 0.48rem 0.72rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: rgba(255, 255, 255, 0.82);
    font-size: 0.72rem;
    font-weight: 820;
}}

.pp-launcher-feature-status::before {{
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #91bc55;
    box-shadow: 0 0 0 4px rgba(145, 188, 85, 0.12);
}}

.pp-launcher-feature-kicker {{
    margin-top: 2.1rem;
    color: rgba(216, 183, 106, 0.92);
    font-size: 0.72rem;
    font-weight: 860;
    letter-spacing: 0.13em;
}}

.pp-launcher-feature-title {{
    max-width: 620px;
    margin-top: 0.42rem;
    color: #ffffff;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    line-height: 1.08;
    font-weight: 930;
    letter-spacing: -0.045em;
}}

.pp-launcher-feature-desc {{
    max-width: 680px;
    margin-top: 0.9rem;
    color: rgba(255, 255, 255, 0.72);
    font-size: 0.94rem;
    line-height: 1.78;
}}

.pp-launcher-feature-foot {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.11);
}}

.pp-launcher-feature-target span {{
    display: block;
    color: rgba(255, 255, 255, 0.48);
    font-size: 0.66rem;
    font-weight: 760;
    letter-spacing: 0.08em;
}}

.pp-launcher-feature-target strong {{
    display: block;
    margin-top: 0.24rem;
    color: #ffffff;
    font-size: 0.92rem;
    font-weight: 860;
}}

.pp-launcher-feature-arrow {{
    width: 46px;
    height: 46px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.11);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: #ffffff;
    font-size: 1.12rem;
    font-weight: 850;
}}

.pp-launcher-list {{
    display: grid;
    gap: 0.78rem;
}}

.pp-launcher-row {{
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 0.8rem;
    align-items: center;
    min-height: 132px;
    padding: 1rem;
    border-radius: 21px;
    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(123, 170, 60, 0.10),
            transparent 34%
        ),
        linear-gradient(
            180deg,
            #ffffff 0%,
            #faf8f2 100%
        );
    border: 1px solid rgba(0, 62, 51, 0.10);
    box-shadow: 0 15px 34px rgba(0, 62, 51, 0.065);
    transition:
        transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
        border-color 220ms ease,
        box-shadow 220ms ease;
}}

.pp-launcher-row:hover {{
    transform: translateY(-3px);
    border-color: rgba(123, 170, 60, 0.30);
    box-shadow: 0 24px 54px rgba(0, 62, 51, 0.10);
}}

.pp-launcher-row-icon {{
    width: 46px;
    height: 46px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background:
        linear-gradient(
            145deg,
            #edf4e4 0%,
            #ffffff 100%
        );
    border: 1px solid rgba(123, 170, 60, 0.25);
    color: #003e33;
    font-size: 0.76rem;
    font-weight: 920;
}}

.pp-launcher-row-copy {{
    min-width: 0;
}}

.pp-launcher-row-head {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.7rem;
}}

.pp-launcher-row-title {{
    color: #003e33;
    font-size: 1rem;
    line-height: 1.35;
    font-weight: 900;
    letter-spacing: -0.025em;
}}

.pp-launcher-row-status {{
    flex: 0 0 auto;
    padding: 0.34rem 0.55rem;
    border-radius: 999px;
    background: #fff6df;
    border: 1px solid rgba(216, 183, 106, 0.32);
    color: #8e6d27;
    font-size: 0.66rem;
    font-weight: 800;
}}

.pp-launcher-row-desc {{
    margin-top: 0.3rem;
    color: #6f7d75;
    font-size: 0.82rem;
    line-height: 1.58;
}}

.pp-launcher-row-foot {{
    display: flex;
    gap: 0.38rem;
    margin-top: 0.56rem;
    color: #87928c;
    font-size: 0.68rem;
}}

.pp-launcher-row-foot strong {{
    color: #315247;
    font-weight: 820;
}}

.pp-launcher-row-arrow {{
    width: 34px;
    height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: #f3f6ef;
    border: 1px solid rgba(0, 62, 51, 0.09);
    color: #003e33;
    font-size: 0.92rem;
    font-weight: 850;
}}

@media (max-width: 1100px) {{
    .pp-enterprise-launcher {{
        grid-template-columns: 1fr;
    }}

    .pp-launcher-feature {{
        min-height: 280px;
    }}
}}

@media (max-width: 680px) {{
    .pp-launcher-feature {{
        min-height: auto;
        padding: 1.35rem;
        border-radius: 24px;
    }}

    .pp-launcher-feature-title {{
        font-size: 1.8rem;
    }}

    .pp-launcher-feature-foot {{
        align-items: flex-end;
    }}

    .pp-launcher-row {{
        grid-template-columns: auto minmax(0, 1fr);
    }}

    .pp-launcher-row-arrow {{
        display: none;
    }}
}}
</style>

<section class="pp-enterprise-launcher">
    <article class="pp-launcher-feature">
        <div class="pp-launcher-feature-top">
            <div class="pp-launcher-feature-icon">
                {primary_icon}
            </div>

            <div class="pp-launcher-feature-status">
                {primary_status}
            </div>
        </div>

        <div class="pp-launcher-feature-kicker">
            主要執行入口
        </div>

        <div class="pp-launcher-feature-title">
            {primary_title}
        </div>

        <div class="pp-launcher-feature-desc">
            {primary_description}
        </div>

        <div class="pp-launcher-feature-foot">
            <div class="pp-launcher-feature-target">
                <span>目標位置</span>
                <strong>{primary_target}</strong>
            </div>

            <div class="pp-launcher-feature-arrow">→</div>
        </div>
    </article>

    <div class="pp-launcher-list">
        {secondary_html}
    </div>
</section>
"""


__all__ = ["render_enterprise_home"]
