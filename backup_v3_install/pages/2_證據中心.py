import streamlit as st
from html import escape
from pathlib import Path

from modules.evidence_center.service import EvidenceService

from app import (
    _render_quick_update_control,
)

from modules.platform.platform_frame import (
    render_shared_sidebar_brand_and_navigation,
)


st.set_page_config(
    page_title="證據中心｜PetPulse Enterprise OS",
    page_icon="📌",
    layout="wide",
)


def main():
    """
    PetPulse Enterprise OS v1.2 Executive Edition
    GM28 Enterprise Design Polish

    Presentation Layer Only
    不修改 Runtime / Engine / Domain / Repository / Query Engine
    品牌證據中心 僅呈現 Analyzer 驗證後的品牌情報
    """

    render_shared_sidebar_brand_and_navigation()
    _render_quick_update_control()

    _load_enterprise_css()
    _inject_gm25_evidence_css()
    _inject_v2_evidence_override()
    _inject_v21_unified_refinement()

    service = EvidenceService()
    evidence_items = service.get_all_evidence()
    kpi_summary = service.get_kpi_summary()

    _render_hero(
        evidence_items=evidence_items,
        kpi_summary=kpi_summary,
    )

    filtered_items = _render_query_tools(
        evidence_items
    )

    _render_evidence_overview(
        evidence_items=filtered_items,
        kpi_summary=kpi_summary,
    )

    _render_evidence_table(
        filtered_items
    )

    _render_decision_hint(
        filtered_items
    )


def _load_enterprise_css():
    current = Path(__file__).resolve()

    for parent in current.parents:
        css_path = (
            parent
            / "assets"
            / "enterprise.css"
        )

        if css_path.exists():
            st.markdown(
                (
                    "<style>"
                    f"{css_path.read_text(encoding='utf-8')}"
                    "</style>"
                ),
                unsafe_allow_html=True,
            )
            return


def _inject_gm25_evidence_css():
    _render_html(
        """
<style>
/* ================================================================
   GM27 Unified Sidebar + GM28 Enterprise Design Polish
   ================================================================ */

/* 證據中心頁面目前選取狀態 */
[data-testid="stSidebar"] [data-testid="stPageLink"] a[href*="2_"] {
    background: rgba(255, 255, 255, 0.94) !important;
    border-color: rgba(255, 255, 255, 0.70) !important;
    box-shadow: 0 12px 26px rgba(0, 62, 51, 0.12) !important;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a[href*="app.py"] {
    background: transparent !important;
    border-color: transparent !important;
    box-shadow: none !important;
}


.pp25e-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.65fr);
    gap: 1rem;
    padding: clamp(2rem, 3.4vw, 3.5rem);
    border: 1px solid rgba(123, 170, 60, 0.20);
    border-radius: 30px;
    background:
        radial-gradient(circle at 95% 0%, rgba(216, 183, 106, 0.15), transparent 27%),
        radial-gradient(circle at 0% 100%, rgba(123, 170, 60, 0.10), transparent 30%),
        linear-gradient(135deg, #FFFDF8 0%, #F7F8F2 64%, #EEF4E7 100%);
    box-shadow: 0 18px 48px rgba(0, 48, 39, 0.055);
}

.pp25e-product {
    display: inline-flex;
    align-items: center;
    padding: 0.44rem 0.72rem;
    border: 1px solid rgba(123, 170, 60, 0.24);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.78);
    color: #557D27;
    font-size: 0.7rem;
    font-weight: 820;
    letter-spacing: 0.06em;
}

.pp25e-product::before {
    content: "";
    width: 7px;
    height: 7px;
    margin-right: 0.42rem;
    border-radius: 50%;
    background: #7BAA3C;
    box-shadow: 0 0 0 4px rgba(123, 170, 60, 0.12);
}

.pp25e-eyebrow,
.pp25e-section-kicker,
.pp25e-side-label,
.pp25e-card-kicker {
    color: #557D27;
    font-size: 0.72rem;
    font-weight: 840;
    letter-spacing: 0.07em;
}

.pp25e-eyebrow {
    margin-top: 1rem;
}

.pp25e-title {
    max-width: 900px;
    margin: 0.45rem 0 0;
    color: #003E33;
    font-size: clamp(3rem, 5vw, 5rem);
    font-weight: 860;
    line-height: 0.99;
    letter-spacing: -0.065em;
}

.pp25e-summary {
    max-width: 820px;
    margin-top: 1rem;
    color: #6C7C75;
    font-size: 1rem;
    line-height: 1.78;
}

.pp25e-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.48rem;
    margin-top: 1.2rem;
}

.pp25e-chip {
    padding: 0.43rem 0.66rem;
    border: 1px solid rgba(0, 62, 51, 0.09);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.74);
    color: #2E443C;
    font-size: 0.72rem;
    font-weight: 740;
}

.pp25e-side {
    overflow: hidden;
    align-self: center;
    border: 1px solid rgba(0, 62, 51, 0.09);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.82);
}

.pp25e-side-item {
    padding: 1rem 1.1rem;
    border-bottom: 1px solid rgba(0, 62, 51, 0.08);
}

.pp25e-side-item:last-child {
    border-bottom: 0;
}

.pp25e-side-value {
    margin-top: 0.23rem;
    color: #003E33;
    font-size: 1.08rem;
    font-weight: 820;
}

.pp25e-side-note {
    margin-top: 0.22rem;
    color: #6C7C75;
    font-size: 0.76rem;
    line-height: 1.5;
}

.pp25e-section {
    margin-top: 3.8rem;
}

.pp25e-section-heading {
    display: flex;
    align-items: end;
    justify-content: space-between;
    gap: 2rem;
    margin-bottom: 1.1rem;
}

.pp25e-section-title {
    margin-top: 0.28rem;
    color: #003E33;
    font-size: clamp(2rem, 3vw, 3rem);
    font-weight: 850;
    line-height: 1.05;
    letter-spacing: -0.045em;
}

.pp25e-section-desc {
    max-width: 610px;
    color: #6C7C75;
    font-size: 0.9rem;
    line-height: 1.65;
}

.pp25e-query-intro {
    margin-bottom: 0.9rem;
    padding: 1.1rem 1.2rem;
    border: 1px solid rgba(0, 62, 51, 0.09);
    border-radius: 20px;
    background:
        radial-gradient(circle at 100% 0%, rgba(216, 183, 106, 0.11), transparent 28%),
        #FFFFFF;
    box-shadow: 0 8px 24px rgba(0, 48, 39, 0.04);
}

.pp25e-query-title {
    margin-top: 0.28rem;
    color: #003E33;
    font-size: 1.05rem;
    font-weight: 800;
}

.pp25e-query-desc {
    margin-top: 0.3rem;
    color: #6C7C75;
    font-size: 0.83rem;
    line-height: 1.55;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp25e-toolbar-marker) {
    padding: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp25e-toolbar-marker) > div {
    padding: 0 !important;
}

.pp25e-overview {
    display: grid;
    grid-template-columns: minmax(0, 1.4fr) repeat(3, minmax(170px, 0.4fr));
    gap: 0.9rem;
}

.pp25e-overview-main,
.pp25e-overview-card,
.pp25e-table-shell,
.pp25e-decision-main,
.pp25e-decision-side {
    border: 1px solid rgba(0, 62, 51, 0.09);
    border-radius: 22px;
    background: #FFFFFF;
    box-shadow: 0 8px 24px rgba(0, 48, 39, 0.04);
}

.pp25e-overview-main {
    padding: 1.45rem;
    background:
        radial-gradient(circle at 100% 0%, rgba(123, 170, 60, 0.09), transparent 30%),
        linear-gradient(145deg, #FFFDF8 0%, #F3F7EE 100%);
}

.pp25e-overview-count {
    margin-top: 0.55rem;
    color: #003E33;
    font-size: clamp(2rem, 3vw, 3.1rem);
    font-weight: 860;
    line-height: 1;
    letter-spacing: -0.05em;
}

.pp25e-overview-copy {
    margin-top: 0.62rem;
    color: #6C7C75;
    font-size: 0.88rem;
    line-height: 1.65;
}

.pp25e-overview-card {
    padding: 1.25rem;
}

.pp25e-metric {
    margin-top: 0.55rem;
    color: #003E33;
    font-size: 2.7rem;
    font-weight: 860;
    line-height: 0.95;
    letter-spacing: -0.05em;
}

.pp25e-metric-label {
    margin-top: 0.5rem;
    color: #003E33;
    font-size: 0.98rem;
    font-weight: 800;
}

.pp25e-table-shell {
    padding: 1.2rem;
}

.pp25e-table-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}

.pp25e-table-title {
    margin-top: 0.25rem;
    color: #003E33;
    font-size: 1.18rem;
    font-weight: 820;
}

.pp25e-table-desc {
    margin-top: 0.28rem;
    color: #6C7C75;
    font-size: 0.8rem;
    line-height: 1.55;
}

.pp25e-count-pill {
    flex: 0 0 auto;
    padding: 0.38rem 0.65rem;
    border: 1px solid rgba(67, 129, 79, 0.17);
    border-radius: 999px;
    background: #EDF7EF;
    color: #43814F;
    font-size: 0.7rem;
    font-weight: 780;
}

.pp25e-table-scroll {
    margin-top: 0.95rem;
    overflow-x: auto;
    border: 1px solid rgba(0, 62, 51, 0.08);
    border-radius: 17px;
}

.pp25e-table {
    width: 100%;
    min-width: 1320px;
    border-collapse: collapse;
    background: #FFFFFF;
}

.pp25e-table th {
    padding: 0.88rem;
    background: #F3F6F0;
    color: #003E33;
    font-size: 0.7rem;
    font-weight: 820;
    text-align: left;
    white-space: nowrap;
}

.pp25e-table td {
    padding: 0.9rem;
    border-top: 1px solid rgba(0, 62, 51, 0.075);
    color: #2E443C;
    font-size: 0.79rem;
    line-height: 1.55;
    vertical-align: top;
}

.pp25e-table tbody tr {
    transition: background 150ms ease, box-shadow 150ms ease;
}

.pp25e-table tbody tr:hover {
    background:
        linear-gradient(
            90deg,
            rgba(123, 170, 60, 0.065),
            rgba(216, 183, 106, 0.025)
        );
    box-shadow: inset 4px 0 0 #7BAA3C;
}

.pp25e-table tbody tr.pp25e-risk-row {
    background:
        linear-gradient(
            90deg,
            rgba(163, 71, 63, 0.055),
            rgba(255, 255, 255, 0)
        );
}

.pp25e-table tbody tr.pp25e-risk-row:hover {
    box-shadow: inset 4px 0 0 #A3473F;
}

.pp25e-content-cell {
    max-width: 460px;
    color: #003E33;
    font-weight: 740;
}

.pp26e-summary-cell {
    min-width: 420px;
}

.pp26e-summary-text {
    color: #003E33;
    font-size: 0.82rem;
    font-weight: 760;
    line-height: 1.65;
}

.pp26e-action {
    max-width: 300px;
    color: #5F6F68;
    font-size: 0.76rem;
    line-height: 1.6;
}

.pp26e-impact {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.58rem;
    border-radius: 999px;
    font-size: 0.67rem;
    font-weight: 800;
    white-space: nowrap;
}

.pp26e-impact-high {
    background: #FCEDEA;
    color: #A3473F;
}

.pp26e-impact-medium {
    background: #FFF3E7;
    color: #A86A2C;
}

.pp26e-impact-opportunity {
    background: #EDF7EF;
    color: #43814F;
}

.pp26e-impact-review {
    background: #FFF7E2;
    color: #8A6B22;
}

.pp26e-impact-normal {
    background: #F2F4F2;
    color: #65736D;
}

.pp25e-evidence-title-link {
    display: block;
    color: #003E33 !important;
    text-decoration: none !important;
}

.pp25e-evidence-title {
    display: block;
    color: #003E33;
    font-weight: 780;
    line-height: 1.58;
}

.pp25e-source-action {
    display: inline-flex;
    align-items: center;
    margin-top: 0.42rem;
    padding: 0.27rem 0.52rem;
    border: 1px solid rgba(123, 170, 60, 0.22);
    border-radius: 999px;
    background: #F3F8ED;
    color: #557D27;
    font-size: 0.66rem;
    font-weight: 800;
    transition:
        background 150ms ease,
        border-color 150ms ease,
        transform 150ms ease;
}

.pp25e-evidence-title-link:hover .pp25e-source-action {
    transform: translateX(2px);
    border-color: rgba(123, 170, 60, 0.42);
    background: #EAF3E0;
}

.pp25e-evidence-title-link:hover .pp25e-evidence-title {
    color: #557D27;
}

.pp25e-source-missing {
    margin-top: 0.4rem;
    color: #A2AAA6;
    font-size: 0.65rem;
    font-weight: 680;
}

.pp25e-badge,
.pp25e-confidence-badge,
.pp25e-risk-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.28rem 0.55rem;
    border-radius: 999px;
    font-size: 0.67rem;
    font-weight: 760;
    white-space: nowrap;
}

.pp25e-badge-neutral {
    background: #F2F4F2;
    color: #65736D;
}

.pp25e-badge-positive {
    background: #EDF7EF;
    color: #43814F;
}

.pp25e-badge-negative {
    background: #FCEDEA;
    color: #A3473F;
}

.pp25e-confidence-score {
    color: #003E33;
    font-size: 1.05rem;
    font-weight: 850;
}

.pp25e-confidence-extreme {
    background: #EAF4E1;
    color: #557D27;
}

.pp25e-confidence-high {
    background: #EDF7EF;
    color: #43814F;
}

.pp25e-confidence-medium {
    background: #FFF7E2;
    color: #8A6B22;
}

.pp25e-confidence-normal {
    background: #F2F4F2;
    color: #65736D;
}

.pp25e-risk-yes {
    background: #FCEDEA;
    color: #A3473F;
}

.pp25e-risk-no {
    background: #F2F4F2;
    color: #7A8781;
}

.pp25e-empty {
    padding: 2.5rem;
    border: 1px solid rgba(0, 62, 51, 0.09);
    border-radius: 22px;
    background: #FFFFFF;
    color: #6C7C75;
    text-align: center;
}

.pp25e-decision-layout {
    display: grid;
    grid-template-columns: minmax(0, 1.3fr) minmax(300px, 0.7fr);
    gap: 0.9rem;
}

.pp25e-decision-main {
    padding: 1.5rem;
    background:
        radial-gradient(circle at 100% 0%, rgba(123, 170, 60, 0.09), transparent 30%),
        linear-gradient(145deg, #FFFDF8 0%, #F3F7EE 100%);
}

.pp25e-decision-title {
    margin-top: 0.65rem;
    color: #003E33;
    font-size: clamp(1.5rem, 2.4vw, 2.3rem);
    font-weight: 840;
    line-height: 1.2;
    letter-spacing: -0.035em;
}

.pp25e-decision-copy {
    margin-top: 0.7rem;
    color: #6C7C75;
    font-size: 0.88rem;
    line-height: 1.65;
}

.pp25e-steps {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.65rem;
    margin-top: 1.2rem;
}

.pp25e-step {
    padding: 0.9rem;
    border: 1px solid rgba(0, 62, 51, 0.08);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.72);
}

.pp25e-step span {
    display: block;
    color: #99A49F;
    font-size: 0.66rem;
    font-weight: 800;
}

.pp25e-step strong {
    display: block;
    margin-top: 0.28rem;
    color: #003E33;
    font-size: 0.82rem;
    line-height: 1.45;
}

.pp25e-decision-side {
    overflow: hidden;
}

.pp25e-side-block {
    padding: 1.2rem;
    border-bottom: 1px solid rgba(0, 62, 51, 0.08);
}

.pp25e-side-block:last-child {
    border-bottom: 0;
}

.pp25e-side-number {
    margin-top: 0.45rem;
    color: #003E33;
    font-size: 2.6rem;
    font-weight: 860;
    line-height: 0.95;
}

.pp25e-side-title {
    margin-top: 0.45rem;
    color: #003E33;
    font-size: 1rem;
    font-weight: 800;
}

.pp25e-side-copy {
    margin-top: 0.3rem;
    color: #6C7C75;
    font-size: 0.77rem;
    line-height: 1.55;
}

@media (max-width: 1180px) {
    .pp25e-overview {
        grid-template-columns: 1fr 1fr;
    }

    .pp25e-overview-main {
        grid-column: 1 / -1;
    }
}

@media (max-width: 1100px) {
    .pp25e-hero,
    .pp25e-decision-layout {
        grid-template-columns: 1fr;
    }
}


/* ================================================================
   GM28 Premium Evidence Overrides
   ================================================================ */

.stApp {
    background:
        radial-gradient(circle at 12% 0%, rgba(123, 170, 60, 0.055), transparent 25%),
        linear-gradient(180deg, #FBFAF6 0%, #F7F8F4 100%) !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1480px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

.pp25e-hero {
    gap: 1.25rem;
    padding: clamp(2rem, 3vw, 3rem);
    border-color: rgba(0, 62, 51, 0.09);
    border-radius: 26px;
    background:
        radial-gradient(circle at 92% 4%, rgba(216, 183, 106, 0.12), transparent 28%),
        radial-gradient(circle at 0% 100%, rgba(123, 170, 60, 0.08), transparent 28%),
        linear-gradient(135deg, #FFFDF9 0%, #F8FAF5 70%, #EFF5E9 100%);
    box-shadow: 0 16px 40px rgba(0, 48, 39, 0.045);
}

.pp25e-product {
    padding: .38rem .65rem;
    background: rgba(255,255,255,.88);
    border-color: rgba(123,170,60,.18);
    font-size: .67rem;
}

.pp25e-title {
    max-width: 820px;
    margin-top: .65rem;
    font-size: clamp(2.65rem, 4.25vw, 4.35rem);
    line-height: 1.01;
    letter-spacing: -.055em;
}

.pp25e-summary {
    max-width: 760px;
    margin-top: 1.1rem;
    color: #62736B;
    font-size: .95rem;
    line-height: 1.72;
}

.pp25e-side {
    border-color: rgba(0,62,51,.08);
    border-radius: 20px;
    box-shadow: 0 10px 26px rgba(0,48,39,.035);
}

.pp25e-side-item { padding: 1rem 1.05rem; }
.pp25e-section { margin-top: 3.1rem; }
.pp25e-section-title { font-size: clamp(1.8rem, 2.7vw, 2.55rem); }
.pp25e-section-desc { font-size: .85rem; }

.pp25e-query-intro,
.pp25e-overview-main,
.pp25e-overview-card,
.pp25e-table-shell,
.pp25e-decision-main,
.pp25e-decision-side {
    border-color: rgba(0,62,51,.075);
    border-radius: 19px;
    box-shadow: 0 8px 22px rgba(0,48,39,.032);
}

.pp25e-query-intro { padding: 1rem 1.1rem; }
.pp25e-overview { gap: .75rem; }
.pp25e-overview-main { padding: 1.25rem; }
.pp25e-overview-card { padding: 1.1rem; }
.pp25e-metric { font-size: 2.35rem; }
.pp25e-table-shell { padding: 1.05rem; }
.pp25e-table-scroll { border-radius: 14px; }
.pp25e-table th { padding: .8rem .85rem; background: #F4F7F1; }
.pp25e-table td { padding: .82rem .85rem; }
.pp25e-table tbody tr:hover { box-shadow: inset 3px 0 0 #7BAA3C; }

.pp25e-chip,
.pp25e-count-pill,
.pp25e-confidence-badge,
.pp25e-badge,
.pp26e-impact {
    font-weight: 780;
}

.pp25e-decision-main { padding: 1.35rem; }
.pp25e-step { border-radius: 12px; }

/* 原生輸入元件一起收斂 */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] input {
    border-color: rgba(0,62,51,.10) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,.92) !important;
}

@media (max-width: 820px) {
    .pp25e-hero {
        padding: 1.45rem;
        border-radius: 24px;
    }

    .pp25e-title {
        font-size: clamp(2.5rem, 12vw, 4rem);
    }

    .pp25e-section-heading {
        display: block;
    }

    .pp25e-section-desc {
        margin-top: 0.5rem;
    }

    .pp25e-overview,
    .pp25e-steps {
        grid-template-columns: 1fr;
    }

    .pp25e-overview-main {
        grid-column: auto;
    }
}
</style>
        """
    )



def _inject_v2_evidence_override():
    _render_html(
        """
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 88% -8%, rgba(212,179,99,.08), transparent 24rem),
        linear-gradient(180deg,#fafaf7 0%,#f7f8f4 100%) !important;
}

[data-testid="stMainBlockContainer"], .block-container {
    max-width: 1360px !important;
    padding-top: 1.1rem !important;
    padding-bottom: 5rem !important;
}

.ppv2e-header {
    display: grid;
    grid-template-columns: minmax(0,1fr) minmax(520px,.85fr);
    gap: 28px;
    align-items: end;
    padding: 28px 30px;
    border: 1px solid rgba(7,61,52,.10);
    border-radius: 24px;
    background:
        radial-gradient(circle at 100% 0%, rgba(212,179,99,.10), transparent 28%),
        linear-gradient(135deg,#fff 0%,#fbfaf6 100%);
    box-shadow: 0 18px 48px rgba(7,61,52,.05);
}

.ppv2e-kicker {
    color: #5f8c2e;
    font-size: 11px;
    font-weight: 850;
    letter-spacing: .11em;
}

.ppv2e-header h1 {
    margin: 9px 0 0;
    color: #073d34;
    font-size: clamp(2.2rem,4vw,4rem);
    font-weight: 900;
    line-height: 1.02;
    letter-spacing: -.06em;
}

.ppv2e-header p {
    max-width: 680px;
    margin: 12px 0 0;
    color: #6a7b74;
    font-size: 14px;
    line-height: 1.7;
}

.ppv2e-summary-grid {
    display: grid;
    grid-template-columns: 1.2fr repeat(3,1fr);
    overflow: hidden;
    border: 1px solid rgba(7,61,52,.09);
    border-radius: 18px;
    background: rgba(255,255,255,.84);
}

.ppv2e-summary-grid > div {
    min-height: 112px;
    padding: 16px;
    border-right: 1px solid rgba(7,61,52,.08);
}
.ppv2e-summary-grid > div:last-child { border-right: 0; }
.ppv2e-summary-grid span,
.ppv2e-summary-grid strong,
.ppv2e-summary-grid small { display: block; }
.ppv2e-summary-grid span {
    color: #75867f;
    font-size: 10px;
    font-weight: 800;
}
.ppv2e-summary-grid strong {
    margin-top: 10px;
    color: #073d34;
    font-size: 27px;
    font-weight: 900;
    line-height: 1;
}
.ppv2e-summary-grid small {
    margin-top: 8px;
    color: #5f8c2e;
    font-size: 10px;
    font-weight: 800;
}
.ppv2e-summary-primary {
    background: linear-gradient(145deg,#f4f8ed 0%,#fff 100%);
}

.pp25e-section { margin-top: 48px !important; }
.pp25e-section-title {
    font-size: clamp(1.8rem,3vw,2.8rem) !important;
}
.pp25e-query-intro { display: none !important; }
.pp25e-overview { display: none !important; }
.pp25e-decision-layout { margin-bottom: 24px; }
.pp25e-table-shell,
.pp25e-decision-main,
.pp25e-decision-side {
    border-radius: 20px !important;
    box-shadow: 0 9px 28px rgba(7,61,52,.035) !important;
}
.pp25e-table-shell { padding: 1rem !important; }
.pp25e-table-scroll { border-radius: 14px !important; }
.pp25e-table th { background: #f3f6f0 !important; }

[data-testid="stSidebar"] [data-testid="stPageLink"] a[href*="2_"] {
    background: rgba(255,255,255,.94) !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[href*="app.py"] {
    background: transparent !important;
    box-shadow: none !important;
}

@media (max-width: 1100px) {
    .ppv2e-header { grid-template-columns: 1fr; }
}
@media (max-width: 760px) {
    .ppv2e-header { padding: 22px; border-radius: 20px; }
    .ppv2e-summary-grid { grid-template-columns: repeat(2,1fr); }
    .ppv2e-summary-grid > div { border-bottom: 1px solid rgba(7,61,52,.08); }
}
</style>
        """
    )


def _inject_v21_unified_refinement():
    _render_html("""
<style>
/* =========================================================
   PetPulse v2.1 Evidence Refinement
   ========================================================= */

[data-testid="stAppViewContainer"] {
    background: #F4F6F1 !important;
}

[data-testid="stMainBlockContainer"],
.block-container {
    width: calc(100% - 40px) !important;
    max-width: 1280px !important;
    margin: 18px auto 32px !important;
    padding: 28px 30px 36px !important;
    border: 1px solid rgba(7, 61, 52, .10) !important;
    border-radius: 24px !important;
    background:
        radial-gradient(
            circle at 96% 0%,
            rgba(216, 183, 106, .07),
            transparent 22rem
        ),
        #FFFFFF !important;
    box-shadow:
        0 18px 46px rgba(7, 61, 52, .055),
        inset 0 1px 0 rgba(255, 255, 255, .95) !important;
}

.ppv2e-header {
    padding: 26px 28px !important;
    border-radius: 18px !important;
    border: 1px solid rgba(7, 61, 52, .10) !important;
    box-shadow: 0 9px 24px rgba(7, 61, 52, .035) !important;
}

.ppv2e-header h1 {
    font-size: clamp(2rem, 3.4vw, 3.1rem) !important;
    line-height: 1.05 !important;
}

.ppv2e-header p {
    font-size: 12.5px !important;
    line-height: 1.65 !important;
}

.ppv2e-summary-grid > div {
    min-height: 82px !important;
    padding: 12px 13px !important;
}

.ppv2e-summary-grid strong {
    font-size: 22px !important;
}

.pp25e-section {
    margin-top: 30px !important;
}

.pp25e-section-heading {
    margin-bottom: 12px !important;
}

.pp25e-section-title {
    font-size: clamp(1.65rem, 2.5vw, 2.25rem) !important;
}

.pp25e-section-desc {
    font-size: 12.5px !important;
    line-height: 1.58 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.pp25e-toolbar-marker) {
    padding: 16px !important;
    border-radius: 15px !important;
    border: 1px solid rgba(7, 61, 52, .09) !important;
    background: #FAFBF8 !important;
    box-shadow: none !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label {
    color: #4E625A !important;
    font-size: 11.5px !important;
    font-weight: 760 !important;
}

[data-baseweb="select"] > div,
[data-testid="stTextInput"] input {
    min-height: 42px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(7, 61, 52, .13) !important;
    background: #FFFFFF !important;
    color: #173F35 !important;
    box-shadow: none !important;
}

.pp25e-table-shell {
    padding: 16px !important;
    border-radius: 16px !important;
    box-shadow: 0 7px 20px rgba(7, 61, 52, .032) !important;
}

.pp25e-table-scroll {
    margin-top: 12px !important;
    border-radius: 11px !important;
}

.pp25e-table th {
    padding: 10px 11px !important;
    font-size: 10.5px !important;
}

.pp25e-table td {
    padding: 12px 11px !important;
    font-size: 11.5px !important;
    line-height: 1.52 !important;
}

.pp25e-decision-layout {
    gap: 12px !important;
}

.pp25e-decision-main,
.pp25e-decision-side {
    border-radius: 16px !important;
    box-shadow: 0 7px 20px rgba(7, 61, 52, .032) !important;
}

.pp25e-decision-main {
    padding: 20px !important;
}

.pp25e-decision-title {
    font-size: clamp(1.35rem, 2vw, 1.8rem) !important;
}

/* 英文小標降噪 */
.pp25e-card-kicker,
.pp25e-section-kicker,
.ppv2e-kicker {
    color: #668D33 !important;
    font-size: 9.5px !important;
    letter-spacing: .11em !important;
}

@media (max-width: 980px) {
    [data-testid="stMainBlockContainer"],
    .block-container {
        width: calc(100% - 24px) !important;
        padding: 20px !important;
    }
}
</style>
""")


def _compact_html(markup):
    if not markup:
        return ""

    return "".join(
        line.strip()
        for line in str(markup).splitlines()
        if line.strip()
    )


def _render_html(markup):
    st.markdown(
        _compact_html(markup),
        unsafe_allow_html=True,
    )


def _safe(
    value,
    fallback="",
):
    if value is None:
        return escape(
            str(fallback)
        )

    text = str(
        value
    ).strip()

    if not text:
        return escape(
            str(fallback)
        )

    return escape(
        text
    )


def _get_item_value(
    item,
    *keys,
    fallback="",
):
    for key in keys:
        if isinstance(
            item,
            dict,
        ):
            value = item.get(
                key
            )
        else:
            value = getattr(
                item,
                key,
                None,
            )

        if value not in (
            None,
            "",
        ):
            if hasattr(
                value,
                "value",
            ):
                value = value.value

            return value

    return fallback


def _section(
    kicker,
    title,
    description,
):
    _render_html(
        f"""
<section class="pp25e-section-heading">
    <div>
        <div class="pp25e-section-kicker">{_safe(kicker)}</div>
        <div class="pp25e-section-title">{_safe(title)}</div>
    </div>
    <div class="pp25e-section-desc">{_safe(description)}</div>
</section>
        """
    )


def _render_hero(
    evidence_items,
    kpi_summary,
):
    total_count = int(
        kpi_summary.get(
            "evidence_count",
            len(evidence_items),
        )
    )
    high_risk_count = int(
        kpi_summary.get(
            "high_risk_count",
            _count_high_risk(evidence_items),
        )
    )
    negative_count = int(
        kpi_summary.get(
            "negative",
            _count_sentiment(evidence_items, "negative"),
        )
    )
    average_confidence = kpi_summary.get(
        "brand_confidence_average",
        _average_confidence(evidence_items),
    )

    status_text = "需要優先查核" if high_risk_count > 0 else "目前無重大風險"

    _render_html(
        f"""
<section class="ppv2e-header">
    <div>
        <div class="ppv2e-kicker">EVIDENCE CENTER</div>
        <h1>品牌證據</h1>
        <p>
            主管摘要、可信度、影響程度與原始來源集中於此。
            先縮小查核範圍，再決定是否開啟原文。
        </p>
    </div>

    <div class="ppv2e-summary-grid">
        <div class="ppv2e-summary-primary">
            <span>有效情報</span>
            <strong>{total_count}</strong>
            <small>{_safe(status_text)}</small>
        </div>
        <div><span>高風險</span><strong>{high_risk_count}</strong></div>
        <div><span>負向</span><strong>{negative_count}</strong></div>
        <div><span>平均可信度</span><strong>{average_confidence}%</strong></div>
    </div>
</section>
        """
    )


def _render_query_tools(
    evidence_items,
):
    _render_html(
        '<section class="pp25e-section">'
    )

    _section(
        "智慧篩選",
        "縮小主管查核範圍",
        (
            "依可信度、風險、情緒、來源與關鍵字快速收斂，"
            "讓最需要處理的品牌情報優先浮出水面。"
        ),
    )

    _render_html(
        """
<div class="pp25e-query-intro">
    <div class="pp25e-card-kicker">證據情報 Filter</div>
    <div class="pp25e-query-title">建立今日主管查核條件</div>
    <div class="pp25e-query-desc">
        預設採 GM25 智慧排序：高風險與負向置頂，
        再依 Brand Confidence 與發布時間排序。
    </div>
</div>
        """
    )

    platforms = [
        "全部"
    ] + sorted(
        {
            str(
                _get_item_value(
                    item,
                    "platform",
                    fallback="未知",
                )
            )
            for item
            in evidence_items
        }
    )

    sentiments = [
        "全部",
        "負向",
        "中立",
        "正向",
    ]

    confidence_levels = [
        "全部",
        "極高",
        "高",
        "中",
        "一般",
    ]

    risk_filters = [
        "全部",
        "僅品牌訊號",
        "僅高風險",
    ]

    with st.container(
        border=True
    ):
        _render_html(
            '<div class="pp25e-toolbar-marker"></div>'
        )

        row1_col1, row1_col2, row1_col3 = st.columns(
            [1, 1, 1]
        )

        with row1_col1:
            selected_confidence = st.selectbox(
                "可信度等級",
                confidence_levels,
                key="gm25_confidence_filter",
            )

        with row1_col2:
            selected_risk = st.selectbox(
                "情報範圍",
                risk_filters,
                key="gm25_risk_filter",
            )

        with row1_col3:
            selected_sentiment = st.selectbox(
                "情緒狀態",
                sentiments,
                key="gm25_sentiment_filter",
            )

        row2_col1, row2_col2 = st.columns(
            [1, 1.8]
        )

        with row2_col1:
            selected_platform = st.selectbox(
                "資料來源",
                platforms,
                key="gm25_platform_filter",
            )

        with row2_col2:
            keyword = st.text_input(
                "關鍵字",
                placeholder=(
                    "輸入標題、內容、發布者或來源"
                ),
                key="gm25_keyword_filter",
            )

    normalized_keyword = (
        keyword.strip().lower()
    )

    filtered_items = []

    for item in evidence_items:
        platform = str(
            _get_item_value(
                item,
                "platform",
                fallback="未知",
            )
        )

        sentiment = str(
            _get_item_value(
                item,
                "sentiment",
                fallback="未知",
            )
        )

        confidence_level = str(
            _get_item_value(
                item,
                "confidence_level",
                fallback="一般",
            )
        )

        is_brand_signal = bool(
            _get_item_value(
                item,
                "is_brand_signal",
                fallback=True,
            )
        )

        is_high_risk = bool(
            _get_item_value(
                item,
                "is_high_risk",
                fallback=False,
            )
        )

        title = str(
            _get_item_value(
                item,
                "title",
                "content",
                fallback="",
            )
        )

        content = str(
            _get_item_value(
                item,
                "content",
                "snippet",
                fallback="",
            )
        )

        author = str(
            _get_item_value(
                item,
                "author",
                "publisher",
                fallback="",
            )
        )

        source = str(
            _get_item_value(
                item,
                "source",
                fallback="",
            )
        )

        if (
            selected_confidence != "全部"
            and confidence_level
            != selected_confidence
        ):
            continue

        if (
            selected_risk
            == "僅品牌訊號"
            and not is_brand_signal
        ):
            continue

        if (
            selected_risk
            == "僅高風險"
            and not is_high_risk
        ):
            continue

        if selected_platform != "全部":
            if platform != selected_platform:
                continue

        if selected_sentiment != "全部":
            if (
                _sentiment_display(
                    sentiment
                )
                != selected_sentiment
            ):
                continue

        if normalized_keyword:
            searchable_text = (
                f"{title} "
                f"{content} "
                f"{author} "
                f"{source}"
            ).lower()

            if (
                normalized_keyword
                not in searchable_text
            ):
                continue

        filtered_items.append(
            item
        )

    filtered_items = sorted(
        filtered_items,
        key=lambda item: (
            int(
                bool(
                    _get_item_value(
                        item,
                        "is_high_risk",
                        fallback=False,
                    )
                )
            ),
            int(
                _sentiment_display(
                    _get_item_value(
                        item,
                        "sentiment",
                        fallback="",
                    )
                )
                == "負向"
            ),
            _safe_int(
                _get_item_value(
                    item,
                    "brand_confidence",
                    fallback=0,
                )
            ),
            str(
                _get_item_value(
                    item,
                    "published_at",
                    "published_time",
                    fallback="",
                )
            ),
        ),
        reverse=True,
    )

    _render_html(
        "</section>"
    )

    return filtered_items


def _render_evidence_overview(
    evidence_items,
    kpi_summary,
):
    total_count = len(
        evidence_items
    )

    high_risk_count = (
        _count_high_risk(
            evidence_items
        )
    )

    negative_count = (
        _count_sentiment(
            evidence_items,
            "negative",
        )
    )

    average_confidence = (
        _average_confidence(
            evidence_items
        )
    )

    all_count = int(
        kpi_summary.get(
            "evidence_count",
            total_count,
        )
    )

    _render_html(
        f"""
<section class="pp25e-section">
    <div class="pp25e-overview">
        <article class="pp25e-overview-main">
            <div class="pp25e-card-kicker">目前查核結果</div>
            <div class="pp25e-overview-count">{total_count} 筆品牌情報符合條件</div>
            <div class="pp25e-overview-copy">
                全部 Analyzer 驗證證據共 {all_count} 筆。
                目前篩選結果含 {high_risk_count} 筆高風險、
                {negative_count} 筆負向訊號，平均可信度為
                {average_confidence}%。
            </div>
        </article>

        <article class="pp25e-overview-card">
            <div class="pp25e-card-kicker">高風險</div>
            <div class="pp25e-metric">{high_risk_count}</div>
            <div class="pp25e-metric-label">優先查核</div>
        </article>

        <article class="pp25e-overview-card">
            <div class="pp25e-card-kicker">負向訊號</div>
            <div class="pp25e-metric">{negative_count}</div>
            <div class="pp25e-metric-label">固定置頂</div>
        </article>

        <article class="pp25e-overview-card">
            <div class="pp25e-card-kicker">平均可信度</div>
            <div class="pp25e-metric">{average_confidence}%</div>
            <div class="pp25e-metric-label">Brand Confidence</div>
        </article>
    </div>
</section>
        """
    )


def _render_evidence_table(
    evidence_items,
):
    _render_html(
        '<section class="pp25e-section">'
    )

    _section(
        "AI 驗證證據",
        "品牌情報結果",
        (
            "每一筆均已通過 Analyzer 品牌驗證，"
            "並保留可信度、風險、情緒、來源與原始連結。"
        ),
    )

    if not evidence_items:
        _render_html(
            """
<div class="pp25e-empty">
    目前沒有符合條件的品牌情報。
    請調整篩選條件，或將條件切換回「全部」。
</div>
</section>
            """
        )
        return

    rows = "".join(
        _build_evidence_row(
            item
        )
        for item
        in evidence_items
    )

    _render_html(
        f"""
<div class="pp25e-table-shell">
    <div class="pp25e-table-header">
        <div>
            <div class="pp25e-card-kicker">證據情報 List</div>
            <div class="pp25e-table-title">AI 驗證品牌情報清單</div>
            <div class="pp25e-table-desc">
                預設排序為：高風險、負向、可信度、發布時間。主管可先讀摘要與建議行動，再決定是否開啟原文。
            </div>
        </div>
        <div class="pp25e-count-pill">共 {len(evidence_items)} 筆</div>
    </div>

    <div class="pp25e-table-scroll">
        <table class="pp25e-table">
            <thead>
                <tr>
                    <th>可信度</th>
                    <th>影響程度</th>
                    <th>情緒</th>
                    <th>主管摘要</th>
                    <th>建議行動</th>
                    <th>資料來源</th>
                    <th>發布時間</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
</div>
</section>
        """
    )


def _build_evidence_row(
    item,
):
    confidence = _safe_int(
        _get_item_value(
            item,
            "brand_confidence",
            fallback=0,
        )
    )

    confidence_level_raw = str(
        _get_item_value(
            item,
            "confidence_level",
            fallback="一般",
        )
    )

    confidence_level = _safe(
        confidence_level_raw
    )

    confidence_class = (
        _confidence_class(
            confidence_level_raw
        )
    )

    sentiment_raw = str(
        _get_item_value(
            item,
            "sentiment",
            fallback="未知",
        )
    )

    sentiment = _safe(
        _sentiment_display(
            sentiment_raw
        )
    )

    sentiment_class = (
        _sentiment_class(
            sentiment_raw
        )
    )

    impact_level_raw = str(
        _get_item_value(
            item,
            "impact_level",
            fallback="一般",
        )
    ).strip()

    impact_level = _safe(
        impact_level_raw
    )

    impact_class = (
        _impact_class(
            impact_level_raw
        )
    )

    executive_summary = _safe(
        _get_item_value(
            item,
            "executive_summary",
            "ai_summary",
            "title",
            "content",
            fallback="目前沒有足夠內容可供主管判讀。",
        )
    )

    recommended_action = _safe(
        _get_item_value(
            item,
            "recommended_action",
            fallback="持續監測後續討論量與情緒變化。",
        )
    )

    platform = _safe(
        _get_item_value(
            item,
            "platform",
            "source",
            fallback="未知",
        )
    )

    published_time = _safe(
        _get_item_value(
            item,
            "published_at",
            "published_time",
            fallback="未提供",
        )
    )

    original_url = str(
        _get_item_value(
            item,
            "original_url",
            "source_url",
            "article_url",
            "link",
            "url",
            fallback="",
        )
    ).strip()

    summary_html = (
        _render_clickable_evidence_content(
            content=executive_summary,
            original_url=original_url,
        )
    )

    is_high_risk = bool(
        _get_item_value(
            item,
            "is_high_risk",
            fallback=False,
        )
    )

    row_class = (
        "pp25e-risk-row"
        if is_high_risk
        else ""
    )

    return f"""
<tr class="{row_class}">
    <td>
        <span class="pp25e-confidence-score">{confidence}</span>
        <div style="margin-top:0.35rem;">
            <span class="pp25e-confidence-badge {confidence_class}">
                {confidence_level}
            </span>
        </div>
    </td>
    <td>
        <span class="pp26e-impact {impact_class}">
            {impact_level}
        </span>
    </td>
    <td>
        <span class="pp25e-badge {sentiment_class}">
            {sentiment}
        </span>
    </td>
    <td>
        <div class="pp25e-content-cell pp26e-summary-cell">
            <div class="pp26e-summary-text">{summary_html}</div>
        </div>
    </td>
    <td>
        <div class="pp26e-action">{recommended_action}</div>
    </td>
    <td>{platform}</td>
    <td>{published_time}</td>
</tr>
    """

def _render_clickable_evidence_content(
    content,
    original_url,
):
    if not original_url:
        return (
            f'<div class="pp25e-evidence-title">{content}</div>'
            '<div class="pp25e-source-missing">目前無原始連結</div>'
        )

    safe_url = escape(
        original_url,
        quote=True,
    )

    return (
        f'<a class="pp25e-evidence-title-link" '
        f'href="{safe_url}" '
        'target="_blank" '
        'rel="noopener noreferrer">'
        f'<span class="pp25e-evidence-title">{content}</span>'
        '<span class="pp25e-source-action">開啟原始來源 ↗</span>'
        '</a>'
    )


def _render_decision_hint(
    evidence_items,
):
    high_risk_count = (
        _count_high_risk(
            evidence_items
        )
    )

    negative_count = (
        _count_sentiment(
            evidence_items,
            "negative",
        )
    )

    extreme_count = sum(
        1
        for item
        in evidence_items
        if str(
            _get_item_value(
                item,
                "confidence_level",
                fallback="",
            )
        ).strip()
        == "極高"
    )

    if high_risk_count > 0:
        status_title = (
            "立即查核"
        )
        status_copy = (
            "目前篩選結果含有 Analyzer 標記的高風險事件，"
            "建議優先確認原始來源、影響範圍與負責窗口。"
        )
    elif negative_count > 0:
        status_title = (
            "優先判讀"
        )
        status_copy = (
            "目前未出現高風險標記，"
            "但仍有負向訊號需要確認完整脈絡。"
        )
    else:
        status_title = (
            "持續監測"
        )
        status_copy = (
            "目前篩選結果未出現高風險或負向品牌事件。"
        )

    _render_html(
        '<section class="pp25e-section">'
    )

    _section(
        "主管決策",
        "品牌證據行動提示",
        (
            "將 AI 驗證後的品牌證據轉換為"
            "可立即執行的查核順序與責任分派。"
        ),
    )

    _render_html(
        f"""
<div class="pp25e-decision-layout">
    <article class="pp25e-decision-main">
        <div class="pp25e-card-kicker">主管優先確認事項</div>
        <div class="pp25e-decision-title">
            先讀主管摘要，再決定是否升級處理
        </div>
        <div class="pp25e-decision-copy">
            GM25 不再讓主管從大量原始新聞自行判斷。
            系統已先完成品牌驗證、可信度評分與風險排序，
            主管只需要確認證據、判斷影響，再指派處理窗口。
        </div>

        <div class="pp25e-steps">
            <div class="pp25e-step">
                <span>步驟 01</span>
                <strong>先閱讀主管摘要與影響程度</strong>
            </div>
            <div class="pp25e-step">
                <span>步驟 02</span>
                <strong>確認建議行動是否需要執行</strong>
            </div>
            <div class="pp25e-step">
                <span>步驟 03</span>
                <strong>必要時再開原文並指派窗口</strong>
            </div>
        </div>
    </article>

    <aside class="pp25e-decision-side">
        <div class="pp25e-side-block">
            <div class="pp25e-card-kicker">目前判讀結果</div>
            <div class="pp25e-side-number">{high_risk_count}</div>
            <div class="pp25e-side-title">{_safe(status_title)}</div>
            <div class="pp25e-side-copy">{_safe(status_copy)}</div>
        </div>
        <div class="pp25e-side-block">
            <div class="pp25e-card-kicker">高可信情報</div>
            <div class="pp25e-side-number">{extreme_count}</div>
            <div class="pp25e-side-title">極高可信度</div>
            <div class="pp25e-side-copy">
                建議優先閱讀極高可信度且同時為負向的品牌事件。
            </div>
        </div>
    </aside>
</div>
</section>
        """
    )


def _sentiment_display(
    sentiment,
):
    normalized = str(
        sentiment
    ).strip().lower()

    if normalized == "全部":
        return "全部"

    if (
        "正" in normalized
        or "positive" in normalized
    ):
        return "正向"

    if (
        "負" in normalized
        or "negative" in normalized
    ):
        return "負向"

    if (
        "中" in normalized
        or "neutral" in normalized
    ):
        return "中立"

    return (
        str(sentiment).strip()
        or "未知"
    )


def _sentiment_class(
    sentiment,
):
    normalized = str(
        sentiment
    ).strip().lower()

    if (
        "正" in normalized
        or "positive" in normalized
    ):
        return (
            "pp25e-badge-positive"
        )

    if (
        "負" in normalized
        or "negative" in normalized
    ):
        return (
            "pp25e-badge-negative"
        )

    return (
        "pp25e-badge-neutral"
    )


def _confidence_class(
    confidence_level,
):
    normalized = str(
        confidence_level
    ).strip()

    if normalized == "極高":
        return (
            "pp25e-confidence-extreme"
        )

    if normalized == "高":
        return (
            "pp25e-confidence-high"
        )

    if normalized == "中":
        return (
            "pp25e-confidence-medium"
        )

    return (
        "pp25e-confidence-normal"
    )


def _impact_class(
    impact_level,
):
    normalized = str(
        impact_level
    ).strip()

    if normalized == "高影響":
        return "pp26e-impact-high"

    if normalized == "中影響":
        return "pp26e-impact-medium"

    if normalized == "正向機會":
        return "pp26e-impact-opportunity"

    if normalized == "待確認":
        return "pp26e-impact-review"

    return "pp26e-impact-normal"



def _count_sentiment(
    evidence_items,
    target,
):
    count = 0

    for item in evidence_items:
        sentiment = str(
            _get_item_value(
                item,
                "sentiment",
                fallback="",
            )
        ).strip().lower()

        if (
            target == "positive"
            and (
                "正" in sentiment
                or "positive" in sentiment
            )
        ):
            count += 1

        elif (
            target == "negative"
            and (
                "負" in sentiment
                or "negative" in sentiment
            )
        ):
            count += 1

        elif (
            target == "neutral"
            and (
                "中" in sentiment
                or "neutral" in sentiment
            )
        ):
            count += 1

    return count


def _count_high_risk(
    evidence_items,
):
    return sum(
        1
        for item
        in evidence_items
        if bool(
            _get_item_value(
                item,
                "is_high_risk",
                fallback=False,
            )
        )
    )


def _average_confidence(
    evidence_items,
):
    scores = [
        _safe_int(
            _get_item_value(
                item,
                "brand_confidence",
                fallback=0,
            )
        )
        for item
        in evidence_items
    ]

    if not scores:
        return 0.0

    return round(
        sum(scores)
        / len(scores),
        1,
    )


def _safe_int(
    value,
):
    try:
        return int(
            round(
                float(value)
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        return 0


if __name__ == "__main__":
    main()
