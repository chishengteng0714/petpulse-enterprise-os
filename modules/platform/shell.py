import streamlit as st
from html import escape

from modules.platform.runtime import create_platform_runtime
from modules.platform.home.enterprise_home import render_enterprise_home
from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)
from modules.platform.workspace_registry import create_workspace_registry
from modules.platform.theme import apply_petpulse_enterprise_theme


def render_platform():
    """
    PetPulse Enterprise OS Platform Shell

    GM-14 Premium Sidebar Final Pass：
    - 不修改 Runtime
    - 不修改 Registry
    - 不修改首頁組裝方式
    - 不修改 Router / Navigation
    - 僅升級 Sidebar Presentation
    """

    apply_petpulse_enterprise_theme()

    runtime = create_platform_runtime()
    workspace_registry = create_workspace_registry()
    experience = build_enterprise_home_experience()

    _render_platform_sidebar(
        runtime=runtime,
        workspace_registry=workspace_registry,
        experience=experience,
    )

    render_enterprise_home(runtime)


def _render_platform_sidebar(
    runtime,
    workspace_registry,
    experience,
):
    """
    Platform Sidebar

    保留既有平台側邊資訊責任，
    僅將既有企業狀態與 Workspace Registry
    轉換為高資訊密度的 Premium Sidebar。
    """

    workspaces = _get_registered_workspaces(
        workspace_registry
    )

    health_signals = _safe_list(
        _safe_get(
            experience,
            "health_signals",
            [],
        )
    )
    decisions = _safe_list(
        _safe_get(
            experience,
            "decisions",
            [],
        )
    )
    risks = _safe_list(
        _safe_get(
            experience,
            "risks",
            [],
        )
    )

    operating_status = _safe_text(
        _safe_get(
            experience,
            "operating_status",
            "營運穩定",
        ),
        "營運穩定",
    )

    confidence_level = _safe_text(
        _safe_get(
            experience,
            "confidence_level",
            "高",
        ),
        "高",
    )

    health_value = "觀察中"
    health_label = "企業健康"

    if health_signals:
        primary_health = health_signals[0]

        health_value = _safe_text(
            _safe_get(
                primary_health,
                "value",
                "觀察中",
            ),
            "觀察中",
        )

        health_label = _safe_text(
            _safe_get(
                primary_health,
                "label",
                "企業健康",
            ),
            "企業健康",
        )

    decision_value = (
        f"{len(decisions)} 項"
        if decisions
        else "清空"
    )
    risk_value = (
        f"{len(risks)} 項"
        if risks
        else "穩定"
    )
    workspace_value = (
        f"{len(workspaces)} 個"
        if workspaces
        else "待命"
    )

    with st.sidebar:
        st.html(
            f"""
<section class="pp-shell-sidebar-brand pp-shell-sidebar-brand-logo">
    <div class="pp-shell-brand-logo-wrap">
        <img
            class="pp-shell-brand-logo"
            src="data:image/png;base64,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"
            alt="寵物公園"
        >
    </div>

    <div class="pp-shell-brand-meta">
        <div class="pp-shell-brand-system">企業決策作業系統</div>
        <div class="pp-shell-brand-product">PetPulse Enterprise OS</div>
    </div>

    <div class="pp-shell-live-dot" title="系統運作中"></div>
</section>

<section class="pp-shell-status-panel">
    <div class="pp-shell-status-head">
        <div>
            <div class="pp-shell-eyebrow">今日企業狀態</div>
            <div class="pp-shell-status-title">
                {operating_status}
            </div>
        </div>

        <div class="pp-shell-status-chip">即時</div>
    </div>

    <div class="pp-shell-health-row">
        <div>
            <span>{health_label}</span>
            <strong>{health_value}</strong>
        </div>

        <div class="pp-shell-health-orbit">
            <span></span>
        </div>
    </div>

    <div class="pp-shell-status-grid">
        <div class="pp-shell-status-item">
            <span>今日待決策</span>
            <strong>{decision_value}</strong>
        </div>

        <div class="pp-shell-status-item">
            <span>風險訊號</span>
            <strong>{risk_value}</strong>
        </div>

        <div class="pp-shell-status-item">
            <span>判斷信心</span>
            <strong>{confidence_level}</strong>
        </div>

        <div class="pp-shell-status-item">
            <span>工作入口</span>
            <strong>{workspace_value}</strong>
        </div>
    </div>
</section>

<section class="pp-shell-ai-panel">
    <div class="pp-shell-ai-icon">智</div>

    <div>
        <div class="pp-shell-ai-title">智慧判讀正常</div>
        <div class="pp-shell-ai-desc">
            今日狀態、決策與風險摘要已完成整理。
        </div>
    </div>
</section>
"""
        )

        _render_workspace_registry(
            workspaces
        )

        st.html(
            """
<section class="pp-shell-footer">
    <div class="pp-shell-footer-mark">P</div>

    <div>
        <div class="pp-shell-footer-title">Golden Master</div>
        <div class="pp-shell-footer-desc">
            企業展示版本・系統運作正常
        </div>
    </div>
</section>
"""
        )

        _inject_sidebar_style()


def _render_workspace_registry(
    workspaces,
):
    """
    顯示既有 Workspace Registry 內容。

    不改變 Registry，
    不新增按鈕或導航行為。
    """

    if not workspaces:
        st.html(
            """
<section class="pp-shell-workspace-panel">
    <div class="pp-shell-workspace-label">主要工作區</div>

    <div class="pp-shell-empty-workspace">
        <div class="pp-shell-empty-icon">候</div>

        <div>
            <div class="pp-shell-workspace-title">
                目前沒有可用的工作區
            </div>

            <div class="pp-shell-workspace-desc">
                系統仍可顯示今日企業首頁。
            </div>
        </div>
    </div>
</section>
"""
        )
        return

    cards = []

    for index, workspace in enumerate(
        workspaces,
        start=1,
    ):
        title = _safe_text(
            _safe_get(
                workspace,
                "title",
                _safe_get(
                    workspace,
                    "name",
                    "工作區",
                ),
            ),
            "工作區",
        )

        description = _safe_text(
            _safe_get(
                workspace,
                "description",
                _safe_get(
                    workspace,
                    "purpose",
                    "查看相關企業資訊。",
                ),
            ),
            "查看相關企業資訊。",
        )

        status = _safe_text(
            _safe_get(
                workspace,
                "status",
                "可使用",
            ),
            "可使用",
        )

        card_class = (
            "pp-shell-workspace-card-primary"
            if index == 1
            else ""
        )

        cards.append(
            f"""
<div class="pp-shell-workspace-card {card_class}">
    <div class="pp-shell-workspace-icon">
        {index:02d}
    </div>

    <div class="pp-shell-workspace-copy">
        <div class="pp-shell-workspace-card-head">
            <div class="pp-shell-workspace-title">
                {title}
            </div>

            <div class="pp-shell-workspace-status">
                {status}
            </div>
        </div>

        <div class="pp-shell-workspace-desc">
            {description}
        </div>
    </div>
</div>
"""
        )

    st.html(
        f"""
<section class="pp-shell-workspace-panel">
    <div class="pp-shell-workspace-label">主要工作區</div>
    {''.join(cards)}
</section>
"""
    )


def _inject_sidebar_style():
    st.html(
        """
<style>
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.1rem;
}

.pp-shell-sidebar-brand {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    align-items: center;
    gap: 0.72rem;
    margin-bottom: 0.82rem;
    padding: 0.88rem;
    border-radius: 20px;
    background:
        linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.11),
            rgba(255, 255, 255, 0.045)
        );
    border: 1px solid rgba(255, 255, 255, 0.10);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.08),
        0 18px 38px rgba(0, 0, 0, 0.11);
}

.pp-shell-brand-mark {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background:
        radial-gradient(
            circle at 78% 18%,
            rgba(216, 183, 106, 0.28),
            transparent 34%
        ),
        linear-gradient(
            135deg,
            #0a5247 0%,
            #7baa3c 150%
        );
    border: 1px solid rgba(255, 255, 255, 0.13);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.15),
        0 14px 30px rgba(0, 0, 0, 0.16);
    color: #ffffff !important;
    font-size: 0.9rem;
    font-weight: 930;
}


.pp-shell-sidebar-brand-logo {
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-areas:
        "logo live"
        "meta live";
    row-gap: 0.62rem;
    padding: 1rem;
}

.pp-shell-brand-logo-wrap {
    grid-area: logo;
    min-width: 0;
    overflow: hidden;
    padding: 0.7rem 0.82rem;
    border-radius: 17px;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.86),
        0 14px 30px rgba(0, 0, 0, 0.13);
}

.pp-shell-brand-logo {
    display: block;
    width: 100%;
    max-width: 220px;
    height: auto;
    object-fit: contain;
    object-position: left center;
}

.pp-shell-brand-meta {
    grid-area: meta;
    min-width: 0;
    padding-left: 0.12rem;
}

.pp-shell-brand-system {
    color: rgba(255, 255, 255, 0.92) !important;
    font-size: 0.78rem;
    line-height: 1.35;
    font-weight: 860;
    letter-spacing: 0.01em;
}

.pp-shell-brand-product {
    margin-top: 0.18rem;
    color: rgba(255, 255, 255, 0.43) !important;
    font-size: 0.56rem;
    line-height: 1.35;
    font-weight: 700;
    letter-spacing: 0.07em;
}

.pp-shell-sidebar-brand-logo .pp-shell-live-dot {
    grid-area: live;
    align-self: center;
    justify-self: end;
    margin-left: 0.3rem;
}

.pp-shell-brand-copy {
    min-width: 0;
}

.pp-shell-brand-title {
    color: #ffffff !important;
    font-size: 1.02rem;
    line-height: 1.1;
    font-weight: 920;
    letter-spacing: -0.03em;
}

.pp-shell-brand-subtitle {
    margin-top: 0.22rem;
    color: rgba(255, 255, 255, 0.57) !important;
    font-size: 0.69rem;
    line-height: 1.35;
    font-weight: 700;
}

.pp-shell-live-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #91bc55;
    box-shadow:
        0 0 0 5px rgba(145, 188, 85, 0.11),
        0 0 18px rgba(145, 188, 85, 0.38);
}

.pp-shell-status-panel {
    position: relative;
    overflow: hidden;
    margin-bottom: 0.72rem;
    padding: 0.92rem;
    border-radius: 22px;
    background:
        radial-gradient(
            circle at 96% 4%,
            rgba(216, 183, 106, 0.17),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.105),
            rgba(255, 255, 255, 0.04)
        );
    border: 1px solid rgba(255, 255, 255, 0.10);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.08),
        0 18px 38px rgba(0, 0, 0, 0.10);
}

.pp-shell-status-panel::after {
    content: "";
    position: absolute;
    right: -40px;
    bottom: -40px;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background:
        radial-gradient(
            circle,
            rgba(123, 170, 60, 0.15),
            transparent 70%
        );
    pointer-events: none;
}

.pp-shell-status-head {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.7rem;
}

.pp-shell-eyebrow {
    color: rgba(255, 255, 255, 0.48) !important;
    font-size: 0.61rem;
    font-weight: 820;
    letter-spacing: 0.13em;
}

.pp-shell-status-title {
    margin-top: 0.25rem;
    color: #ffffff !important;
    font-size: 1rem;
    font-weight: 900;
    letter-spacing: -0.025em;
}

.pp-shell-status-chip {
    padding: 0.3rem 0.5rem;
    border-radius: 999px;
    background: rgba(123, 170, 60, 0.16);
    border: 1px solid rgba(145, 188, 85, 0.24);
    color: #d8ebbd !important;
    font-size: 0.56rem;
    line-height: 1;
    font-weight: 820;
    letter-spacing: 0.08em;
}

.pp-shell-health-row {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-top: 0.78rem;
    padding: 0.76rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.07);
}

.pp-shell-health-row span {
    display: block;
    color: rgba(255, 255, 255, 0.50) !important;
    font-size: 0.61rem;
    font-weight: 750;
    letter-spacing: 0.08em;
}

.pp-shell-health-row strong {
    display: block;
    margin-top: 0.18rem;
    color: #ffffff !important;
    font-size: 1.12rem;
    font-weight: 930;
    letter-spacing: -0.04em;
}

.pp-shell-health-orbit {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    border: 1px solid rgba(145, 188, 85, 0.28);
    box-shadow:
        0 0 0 6px rgba(123, 170, 60, 0.06),
        inset 0 0 18px rgba(123, 170, 60, 0.07);
}

.pp-shell-health-orbit span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #91bc55;
    box-shadow:
        0 0 16px rgba(145, 188, 85, 0.48);
}

.pp-shell-status-grid {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.42rem;
    margin-top: 0.48rem;
}

.pp-shell-status-item {
    padding: 0.62rem;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.052);
    border: 1px solid rgba(255, 255, 255, 0.065);
}

.pp-shell-status-item span {
    display: block;
    color: rgba(255, 255, 255, 0.45) !important;
    font-size: 0.58rem;
    font-weight: 750;
    letter-spacing: 0.07em;
}

.pp-shell-status-item strong {
    display: block;
    margin-top: 0.23rem;
    color: #ffffff !important;
    font-size: 0.78rem;
    font-weight: 880;
}

.pp-shell-ai-panel {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: 0.62rem;
    align-items: center;
    margin-bottom: 0.72rem;
    padding: 0.68rem 0.72rem;
    border-radius: 16px;
    background:
        linear-gradient(
            90deg,
            rgba(123, 170, 60, 0.12),
            rgba(216, 183, 106, 0.07)
        );
    border: 1px solid rgba(123, 170, 60, 0.19);
}

.pp-shell-ai-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: rgba(145, 188, 85, 0.14);
    border: 1px solid rgba(145, 188, 85, 0.22);
    color: #d8ebbd !important;
    font-size: 0.67rem;
    font-weight: 900;
}

.pp-shell-ai-title {
    color: #ffffff !important;
    font-size: 0.7rem;
    font-weight: 850;
}

.pp-shell-ai-desc {
    margin-top: 0.14rem;
    color: rgba(255, 255, 255, 0.46) !important;
    font-size: 0.58rem;
    line-height: 1.45;
}

.pp-shell-workspace-panel {
    margin-bottom: 0.72rem;
    padding: 0.78rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.042);
    border: 1px solid rgba(255, 255, 255, 0.073);
}

.pp-shell-workspace-label {
    margin: 0 0 0.62rem 0.12rem;
    color: rgba(216, 183, 106, 0.88) !important;
    font-size: 0.61rem;
    font-weight: 860;
    letter-spacing: 0.14em;
}

.pp-shell-workspace-card,
.pp-shell-empty-workspace {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    align-items: start;
    gap: 0.62rem;
    padding: 0.68rem;
    margin-bottom: 0.48rem;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.063);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

.pp-shell-workspace-card:last-child {
    margin-bottom: 0;
}

.pp-shell-workspace-card-primary {
    background:
        linear-gradient(
            90deg,
            rgba(123, 170, 60, 0.14),
            rgba(255, 255, 255, 0.045)
        );
    border-color: rgba(123, 170, 60, 0.18);
}

.pp-shell-workspace-icon,
.pp-shell-empty-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: rgba(123, 170, 60, 0.13);
    border: 1px solid rgba(145, 188, 85, 0.19);
    color: #ffffff !important;
    font-size: 0.64rem;
    font-weight: 900;
}

.pp-shell-workspace-copy {
    min-width: 0;
}

.pp-shell-workspace-card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.45rem;
}

.pp-shell-workspace-title {
    color: #ffffff !important;
    font-size: 0.72rem;
    font-weight: 860;
    line-height: 1.35;
}

.pp-shell-workspace-status {
    flex: 0 0 auto;
    padding: 0.22rem 0.38rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.07);
    color: rgba(255, 255, 255, 0.55) !important;
    font-size: 0.52rem;
    font-weight: 760;
}

.pp-shell-workspace-desc {
    margin-top: 0.2rem;
    color: rgba(255, 255, 255, 0.45) !important;
    font-size: 0.58rem;
    line-height: 1.45;
    font-weight: 620;
}

.pp-shell-footer {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    align-items: center;
    gap: 0.56rem;
    padding: 0.64rem;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
}

.pp-shell-footer-mark {
    width: 29px;
    height: 29px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.075);
    color: rgba(255, 255, 255, 0.72) !important;
    font-size: 0.61rem;
    font-weight: 900;
}

.pp-shell-footer-title {
    color: rgba(255, 255, 255, 0.72) !important;
    font-size: 0.61rem;
    font-weight: 820;
}

.pp-shell-footer-desc {
    margin-top: 0.1rem;
    color: rgba(255, 255, 255, 0.34) !important;
    font-size: 0.52rem;
    line-height: 1.4;
}


/* =========================================================
   GM-14 Premium Sidebar Final Pass
   Presentation Layer Only
   ========================================================= */

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.76rem;
}

.pp-shell-sidebar-brand,
.pp-shell-status-panel,
.pp-shell-ai-panel,
.pp-shell-workspace-panel {
    backdrop-filter: blur(12px);
}

/* Brand */
.pp-shell-sidebar-brand {
    margin-bottom: 0.58rem;
    border-radius: 18px;
}

.pp-shell-sidebar-brand-logo {
    row-gap: 0.42rem;
    padding: 0.76rem;
}

.pp-shell-brand-logo-wrap {
    padding: 0.48rem 0.66rem;
    border-radius: 14px;
}

.pp-shell-brand-logo {
    max-width: 184px;
}

.pp-shell-brand-meta {
    padding-left: 0.06rem;
}

.pp-shell-brand-system {
    font-size: 0.72rem;
    line-height: 1.28;
}

.pp-shell-brand-product {
    margin-top: 0.12rem;
    font-size: 0.52rem;
    letter-spacing: 0.055em;
}

.pp-shell-live-dot {
    width: 8px;
    height: 8px;
    box-shadow:
        0 0 0 4px rgba(145, 188, 85, 0.10),
        0 0 14px rgba(145, 188, 85, 0.32);
}

/* Status */
.pp-shell-status-panel {
    margin-bottom: 0.54rem;
    padding: 0.76rem;
    border-radius: 19px;
}

.pp-shell-eyebrow {
    font-size: 0.56rem;
}

.pp-shell-status-title {
    margin-top: 0.18rem;
    font-size: 0.92rem;
}

.pp-shell-status-chip {
    padding: 0.26rem 0.44rem;
    font-size: 0.52rem;
}

.pp-shell-health-row {
    margin-top: 0.58rem;
    padding: 0.62rem;
    border-radius: 14px;
}

.pp-shell-health-row span {
    font-size: 0.56rem;
}

.pp-shell-health-row strong {
    margin-top: 0.13rem;
    font-size: 1rem;
}

.pp-shell-health-orbit {
    width: 31px;
    height: 31px;
    box-shadow:
        0 0 0 5px rgba(123, 170, 60, 0.05),
        inset 0 0 14px rgba(123, 170, 60, 0.06);
}

.pp-shell-health-orbit span {
    width: 8px;
    height: 8px;
}

.pp-shell-status-grid {
    gap: 0.34rem;
    margin-top: 0.38rem;
}

.pp-shell-status-item {
    padding: 0.5rem;
    border-radius: 12px;
}

.pp-shell-status-item span {
    font-size: 0.53rem;
}

.pp-shell-status-item strong {
    margin-top: 0.18rem;
    font-size: 0.72rem;
}

/* AI */
.pp-shell-ai-panel {
    gap: 0.5rem;
    margin-bottom: 0.54rem;
    padding: 0.56rem 0.62rem;
    border-radius: 14px;
}

.pp-shell-ai-icon {
    width: 28px;
    height: 28px;
    border-radius: 9px;
    font-size: 0.6rem;
}

.pp-shell-ai-title {
    font-size: 0.65rem;
}

.pp-shell-ai-desc {
    margin-top: 0.1rem;
    font-size: 0.53rem;
    line-height: 1.38;
}

/* Workspace */
.pp-shell-workspace-panel {
    margin-bottom: 0.54rem;
    padding: 0.64rem;
    border-radius: 17px;
}

.pp-shell-workspace-label {
    margin: 0 0 0.48rem 0.08rem;
    font-size: 0.56rem;
}

.pp-shell-workspace-card,
.pp-shell-empty-workspace {
    gap: 0.5rem;
    padding: 0.54rem;
    margin-bottom: 0.36rem;
    border-radius: 13px;
}

.pp-shell-workspace-icon,
.pp-shell-empty-icon {
    width: 29px;
    height: 29px;
    border-radius: 9px;
    font-size: 0.56rem;
}

.pp-shell-workspace-card-head {
    gap: 0.34rem;
}

.pp-shell-workspace-title {
    font-size: 0.66rem;
    line-height: 1.3;
}

.pp-shell-workspace-status {
    padding: 0.18rem 0.32rem;
    font-size: 0.47rem;
}

.pp-shell-workspace-desc {
    margin-top: 0.14rem;
    font-size: 0.53rem;
    line-height: 1.38;
}

/* Footer */
.pp-shell-footer {
    gap: 0.46rem;
    padding: 0.48rem 0.56rem 0.64rem;
}

.pp-shell-footer-mark {
    width: 25px;
    height: 25px;
    border-radius: 8px;
    font-size: 0.55rem;
}

.pp-shell-footer-title {
    font-size: 0.56rem;
}

.pp-shell-footer-desc {
    margin-top: 0.06rem;
    font-size: 0.48rem;
}

/* Lower visual weight */
.pp-shell-sidebar-brand,
.pp-shell-status-panel {
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.07),
        0 12px 28px rgba(0, 0, 0, 0.075);
}

.pp-shell-ai-panel,
.pp-shell-workspace-panel {
    background-color: rgba(255, 255, 255, 0.025);
}

@media (max-height: 820px) {
    .pp-shell-sidebar-brand-logo {
        padding: 0.66rem;
    }

    .pp-shell-brand-logo {
        max-width: 170px;
    }

    .pp-shell-status-panel {
        padding: 0.68rem;
    }

    .pp-shell-health-row {
        margin-top: 0.48rem;
        padding: 0.56rem;
    }

    .pp-shell-status-item {
        padding: 0.44rem;
    }

    .pp-shell-workspace-card,
    .pp-shell-empty-workspace {
        padding: 0.48rem;
    }
}

</style>
"""
    )


def _get_registered_workspaces(
    workspace_registry,
):
    """
    相容既有 Workspace Registry 公開資料結構。
    """

    if workspace_registry is None:
        return []

    if isinstance(workspace_registry, dict):
        return list(
            workspace_registry.values()
        )

    if isinstance(workspace_registry, list):
        return workspace_registry

    if hasattr(
        workspace_registry,
        "list_workspaces",
    ):
        return (
            workspace_registry.list_workspaces()
            or []
        )

    if hasattr(
        workspace_registry,
        "get_all",
    ):
        return (
            workspace_registry.get_all()
            or []
        )

    if hasattr(
        workspace_registry,
        "workspaces",
    ):
        workspaces = workspace_registry.workspaces

        if isinstance(workspaces, dict):
            return list(
                workspaces.values()
            )

        return workspaces or []

    return []


def _safe_get(
    item,
    key,
    default=None,
):
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


def _safe_list(value):
    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


def _safe_text(
    value,
    fallback="",
):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()

    if not text:
        return escape(str(fallback))

    return escape(text)


__all__ = [
    "render_platform",
]
