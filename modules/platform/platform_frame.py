import streamlit as st
from html import escape

from modules.platform.home.enterprise_home import render_enterprise_home
from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_platform_frame():
    """
    PetPulse Enterprise OS v1.0 Golden Master

    GM-13 Phase 2 Premium Sidebar：
    - Presentation Layer Only
    - 保留既有工作區選擇與顯示流程
    - 不修改 Runtime / Router / Registry / Schema
    - 不新增工作區或功能
    - 側欄只讀取既有 EnterpriseHomeExperience
    """

    _inject_platform_frame_style()

    experience = build_enterprise_home_experience()

    _render_platform_sidebar(experience)

    selected_workspace = _render_workspace_selector()

    if selected_workspace == "enterprise_home":
        render_enterprise_home()
    else:
        _render_workspace_placeholder(selected_workspace)


def _safe(value, fallback=""):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()

    if not text:
        return escape(str(fallback))

    return escape(text)


def _items(experience, name):
    return getattr(experience, name, []) or []


def _render_platform_sidebar(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    workspaces = _items(experience, "workspaces")
    health_signals = _items(experience, "health_signals")

    operating_status = _safe(
        getattr(experience, "operating_status", None),
        "營運穩定",
    )

    confidence_level = _safe(
        getattr(experience, "confidence_level", None),
        "高信心",
    )

    health_value = "觀察中"

    if health_signals:
        health_value = _safe(
            getattr(health_signals[0], "value", None),
            "觀察中",
        )

    risk_label = "穩定" if not risks else f"{len(risks)} 項"
    decision_label = "清空" if not decisions else f"{len(decisions)} 項"
    workspace_label = f"{len(workspaces)} 個" if workspaces else "待命"

    with st.sidebar:
        st.markdown(
            f"""
            <section class="pp-sidebar-brand pp-sidebar-brand-premium">
                <div class="pp-sidebar-logo">
                    <span>脈</span>
                </div>

                <div class="pp-sidebar-brand-copy">
                    <div class="pp-sidebar-title">PetPulse</div>
                    <div class="pp-sidebar-subtitle">企業決策作業系統</div>
                </div>

                <div class="pp-sidebar-live-dot" title="系統運作中"></div>
            </section>

            <section class="pp-sidebar-command">
                <div class="pp-sidebar-command-head">
                    <div>
                        <div class="pp-sidebar-command-eyebrow">今日企業狀態</div>
                        <div class="pp-sidebar-command-title">{operating_status}</div>
                    </div>

                    <div class="pp-sidebar-command-badge">即時</div>
                </div>

                <div class="pp-sidebar-health-row">
                    <div>
                        <span>企業健康</span>
                        <strong>{health_value}</strong>
                    </div>

                    <div class="pp-sidebar-health-orbit">
                        <span></span>
                    </div>
                </div>

                <div class="pp-sidebar-status-grid">
                    <div class="pp-sidebar-status">
                        <span>待決策</span>
                        <strong>{decision_label}</strong>
                    </div>

                    <div class="pp-sidebar-status">
                        <span>風險訊號</span>
                        <strong>{risk_label}</strong>
                    </div>

                    <div class="pp-sidebar-status">
                        <span>判斷信心</span>
                        <strong>{confidence_level}</strong>
                    </div>

                    <div class="pp-sidebar-status">
                        <span>工作入口</span>
                        <strong>{workspace_label}</strong>
                    </div>
                </div>
            </section>

            <section class="pp-sidebar-intelligence">
                <div class="pp-sidebar-intelligence-icon">智</div>

                <div>
                    <div class="pp-sidebar-intelligence-title">智慧判讀正常</div>
                    <div class="pp-sidebar-intelligence-desc">
                        今日狀態、決策與風險摘要已完成整理。
                    </div>
                </div>
            </section>

            <section class="pp-sidebar-group pp-sidebar-group-premium">
                <div class="pp-sidebar-group-label">主要工作區</div>

                <div class="pp-sidebar-preview-card pp-sidebar-preview-card-primary">
                    <div class="pp-sidebar-icon-box">
                        <span>首</span>
                    </div>

                    <div>
                        <div class="pp-sidebar-card-title">今日企業首頁</div>
                        <div class="pp-sidebar-card-subtitle">
                            掌握今日狀態、決策與下一步行動
                        </div>
                    </div>
                </div>

                <div class="pp-sidebar-preview-card">
                    <div class="pp-sidebar-icon-box pp-sidebar-icon-gold">
                        <span>證</span>
                    </div>

                    <div>
                        <div class="pp-sidebar-card-title">證據中心</div>
                        <div class="pp-sidebar-card-subtitle">
                            追溯公開來源與原始討論脈絡
                        </div>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )


def _render_workspace_selector():
    with st.sidebar:
        st.markdown(
            """
            <div class="pp-sidebar-switch-label">
                切換工作區
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_workspace = st.radio(
            "切換工作區",
            options=[
                "enterprise_home",
                "evidence_center",
            ],
            format_func=_format_workspace_label,
            index=0,
            key="platform_sidebar_workspace",
            label_visibility="collapsed",
        )

        st.markdown(
            """
            <section class="pp-sidebar-footer">
                <div class="pp-sidebar-footer-mark">P</div>

                <div>
                    <div class="pp-sidebar-footer-title">Golden Master</div>
                    <div class="pp-sidebar-footer-desc">
                        企業展示版本・系統運作正常
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    return selected_workspace


def _format_workspace_label(workspace_key):
    label_map = {
        "enterprise_home": "今日企業首頁",
        "evidence_center": "證據中心",
    }

    return label_map.get(workspace_key, "未知工作區")


def _render_workspace_placeholder(selected_workspace):
    workspace_label = _format_workspace_label(selected_workspace)

    st.markdown(
        f"""
        <section class="pp-workspace-placeholder">
            <div class="pp-placeholder-icon">
                <span>建</span>
            </div>

            <div class="pp-placeholder-eyebrow">工作區入口</div>

            <h1>{_safe(workspace_label)}</h1>

            <p>
                此工作區入口已保留，目前維持既有架構與頁面責任。
                GM-13 僅進行呈現層與視覺設計升級，不新增 Router、
                Runtime、Registry 或任何新功能。
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _inject_platform_frame_style():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background:
                    radial-gradient(
                        circle at 12% 0%,
                        rgba(216, 183, 106, 0.22),
                        transparent 22%
                    ),
                    radial-gradient(
                        circle at 100% 100%,
                        rgba(123, 170, 60, 0.17),
                        transparent 34%
                    ),
                    linear-gradient(
                        180deg,
                        #001f1a 0%,
                        #003e33 56%,
                        #002f27 100%
                    ) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.07);
                box-shadow: 24px 0 70px rgba(0, 31, 26, 0.14);
            }

            [data-testid="stSidebar"] > div:first-child {
                padding-top: 22px;
            }

            [data-testid="stSidebar"] * {
                color: rgba(255, 255, 255, 0.94) !important;
            }

            .pp-sidebar-brand-premium {
                display: grid;
                grid-template-columns: auto minmax(0, 1fr) auto;
                align-items: center;
                gap: 12px;
                margin: 0 0 14px 0;
                padding: 14px;
                border-radius: 20px;
                background:
                    linear-gradient(
                        145deg,
                        rgba(255, 255, 255, 0.11),
                        rgba(255, 255, 255, 0.045)
                    );
                border: 1px solid rgba(255, 255, 255, 0.11);
                box-shadow:
                    inset 0 1px 0 rgba(255, 255, 255, 0.09),
                    0 18px 38px rgba(0, 0, 0, 0.11);
            }

            .pp-sidebar-logo {
                width: 44px;
                height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex: 0 0 auto;
                border-radius: 15px;
                background:
                    radial-gradient(
                        circle at 78% 18%,
                        rgba(216, 183, 106, 0.28),
                        transparent 34%
                    ),
                    linear-gradient(135deg, #0a5247 0%, #7baa3c 150%);
                border: 1px solid rgba(255, 255, 255, 0.13);
                box-shadow:
                    inset 0 1px 0 rgba(255, 255, 255, 0.15),
                    0 14px 30px rgba(0, 0, 0, 0.16);
            }

            .pp-sidebar-logo span {
                color: #ffffff !important;
                font-size: 15px;
                font-weight: 930;
                letter-spacing: 0.08em;
            }

            .pp-sidebar-brand-copy {
                min-width: 0;
            }

            .pp-sidebar-title {
                color: #ffffff !important;
                font-size: 17px;
                line-height: 1.1;
                font-weight: 920;
                letter-spacing: -0.03em;
            }

            .pp-sidebar-subtitle {
                margin-top: 4px;
                color: rgba(255, 255, 255, 0.58) !important;
                font-size: 11.5px;
                line-height: 1.35;
                font-weight: 700;
            }

            .pp-sidebar-live-dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: #91bc55;
                box-shadow:
                    0 0 0 5px rgba(145, 188, 85, 0.11),
                    0 0 18px rgba(145, 188, 85, 0.38);
            }

            .pp-sidebar-command {
                position: relative;
                overflow: hidden;
                margin-bottom: 12px;
                padding: 15px;
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

            .pp-sidebar-command::after {
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

            .pp-sidebar-command-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 10px;
            }

            .pp-sidebar-command-eyebrow {
                color: rgba(255, 255, 255, 0.50) !important;
                font-size: 10px;
                font-weight: 820;
                letter-spacing: 0.13em;
            }

            .pp-sidebar-command-title {
                margin-top: 4px;
                color: #ffffff !important;
                font-size: 16px;
                font-weight: 900;
                letter-spacing: -0.025em;
            }

            .pp-sidebar-command-badge {
                padding: 5px 8px;
                border-radius: 999px;
                background: rgba(123, 170, 60, 0.16);
                border: 1px solid rgba(145, 188, 85, 0.24);
                color: #d8ebbd !important;
                font-size: 9px;
                line-height: 1;
                font-weight: 820;
                letter-spacing: 0.08em;
            }

            .pp-sidebar-health-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-top: 14px;
                padding: 12px;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.055);
                border: 1px solid rgba(255, 255, 255, 0.07);
            }

            .pp-sidebar-health-row span {
                display: block;
                color: rgba(255, 255, 255, 0.52) !important;
                font-size: 10px;
                font-weight: 750;
                letter-spacing: 0.08em;
            }

            .pp-sidebar-health-row strong {
                display: block;
                margin-top: 3px;
                color: #ffffff !important;
                font-size: 18px;
                font-weight: 930;
                letter-spacing: -0.04em;
            }

            .pp-sidebar-health-orbit {
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

            .pp-sidebar-health-orbit span {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #91bc55;
                box-shadow: 0 0 16px rgba(145, 188, 85, 0.48);
            }

            .pp-sidebar-status-grid {
                position: relative;
                z-index: 1;
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 7px;
                margin-top: 8px;
            }

            .pp-sidebar-status {
                padding: 10px;
                border-radius: 14px;
                background: rgba(255, 255, 255, 0.052);
                border: 1px solid rgba(255, 255, 255, 0.065);
            }

            .pp-sidebar-status span {
                display: block;
                color: rgba(255, 255, 255, 0.47) !important;
                font-size: 9.5px;
                font-weight: 750;
                letter-spacing: 0.07em;
            }

            .pp-sidebar-status strong {
                display: block;
                margin-top: 4px;
                color: #ffffff !important;
                font-size: 13px;
                font-weight: 880;
            }

            .pp-sidebar-intelligence {
                display: grid;
                grid-template-columns: auto minmax(0, 1fr);
                gap: 10px;
                align-items: center;
                margin-bottom: 12px;
                padding: 11px 12px;
                border-radius: 16px;
                background:
                    linear-gradient(
                        90deg,
                        rgba(123, 170, 60, 0.12),
                        rgba(216, 183, 106, 0.07)
                    );
                border: 1px solid rgba(123, 170, 60, 0.19);
            }

            .pp-sidebar-intelligence-icon {
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 11px;
                background: rgba(145, 188, 85, 0.14);
                border: 1px solid rgba(145, 188, 85, 0.22);
                color: #d8ebbd !important;
                font-size: 11px;
                font-weight: 900;
            }

            .pp-sidebar-intelligence-title {
                color: #ffffff !important;
                font-size: 11.5px;
                font-weight: 850;
            }

            .pp-sidebar-intelligence-desc {
                margin-top: 2px;
                color: rgba(255, 255, 255, 0.48) !important;
                font-size: 9.5px;
                line-height: 1.45;
            }

            .pp-sidebar-group-premium {
                margin-bottom: 12px;
                padding: 13px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.075);
            }

            .pp-sidebar-group-label {
                margin: 0 0 10px 2px;
                color: rgba(216, 183, 106, 0.88) !important;
                font-size: 10px;
                font-weight: 860;
                letter-spacing: 0.14em;
            }

            .pp-sidebar-preview-card {
                display: grid;
                grid-template-columns: auto minmax(0, 1fr);
                align-items: start;
                gap: 10px;
                padding: 11px;
                margin-bottom: 8px;
                border-radius: 15px;
                background: rgba(255, 255, 255, 0.052);
                border: 1px solid rgba(255, 255, 255, 0.065);
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            }

            .pp-sidebar-preview-card:last-child {
                margin-bottom: 0;
            }

            .pp-sidebar-preview-card-primary {
                background:
                    linear-gradient(
                        90deg,
                        rgba(123, 170, 60, 0.14),
                        rgba(255, 255, 255, 0.045)
                    );
                border-color: rgba(123, 170, 60, 0.18);
            }

            .pp-sidebar-icon-box {
                width: 34px;
                height: 34px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 11px;
                background: rgba(123, 170, 60, 0.13);
                border: 1px solid rgba(145, 188, 85, 0.19);
            }

            .pp-sidebar-icon-gold {
                background: rgba(216, 183, 106, 0.12);
                border-color: rgba(216, 183, 106, 0.20);
            }

            .pp-sidebar-icon-box span {
                color: #ffffff !important;
                font-size: 11px;
                font-weight: 900;
            }

            .pp-sidebar-card-title {
                color: #ffffff !important;
                font-size: 11.5px;
                font-weight: 860;
                line-height: 1.35;
            }

            .pp-sidebar-card-subtitle {
                margin-top: 3px;
                color: rgba(255, 255, 255, 0.47) !important;
                font-size: 9.5px;
                line-height: 1.45;
                font-weight: 620;
            }

            .pp-sidebar-switch-label {
                margin: 2px 2px 7px 2px;
                color: rgba(255, 255, 255, 0.52) !important;
                font-size: 10px;
                font-weight: 820;
                letter-spacing: 0.12em;
            }

            [data-testid="stSidebar"] [role="radiogroup"] {
                display: grid;
                gap: 6px;
                margin-top: 0;
                padding: 8px;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.075);
            }

            [data-testid="stSidebar"] [role="radio"] {
                min-height: 43px;
                padding: 9px 10px;
                border-radius: 13px;
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.065);
                transition:
                    transform 170ms ease,
                    background 170ms ease,
                    border-color 170ms ease;
            }

            [data-testid="stSidebar"] [role="radio"]:hover {
                transform: translateX(3px);
                background: rgba(255, 255, 255, 0.085);
                border-color: rgba(123, 170, 60, 0.24);
            }

            [data-testid="stSidebar"] [role="radio"] p {
                color: rgba(255, 255, 255, 0.88) !important;
                font-size: 12px !important;
                font-weight: 800 !important;
            }

            .pp-sidebar-footer {
                display: grid;
                grid-template-columns: auto minmax(0, 1fr);
                align-items: center;
                gap: 9px;
                margin-top: 12px;
                padding: 10px;
                border-top: 1px solid rgba(255, 255, 255, 0.07);
            }

            .pp-sidebar-footer-mark {
                width: 29px;
                height: 29px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.075);
                color: rgba(255, 255, 255, 0.72) !important;
                font-size: 10px;
                font-weight: 900;
            }

            .pp-sidebar-footer-title {
                color: rgba(255, 255, 255, 0.72) !important;
                font-size: 10px;
                font-weight: 820;
            }

            .pp-sidebar-footer-desc {
                margin-top: 2px;
                color: rgba(255, 255, 255, 0.35) !important;
                font-size: 8.8px;
                line-height: 1.4;
            }

            .pp-workspace-placeholder {
                padding: 48px 36px;
                margin: 18px 0 24px 0;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(216, 183, 106, 0.15),
                        transparent 31%
                    ),
                    linear-gradient(135deg, #ffffff 0%, #fbf8f1 100%);
                border: 1px solid rgba(0, 62, 51, 0.10);
                border-radius: 32px;
                box-shadow: 0 22px 56px rgba(0, 62, 51, 0.08);
            }

            .pp-placeholder-icon {
                width: 58px;
                height: 58px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 18px;
                border-radius: 19px;
                background:
                    radial-gradient(
                        circle at 78% 18%,
                        rgba(216, 183, 106, 0.25),
                        transparent 34%
                    ),
                    linear-gradient(135deg, #001f1a 0%, #0a5247 100%);
                color: #ffffff;
                box-shadow: 0 16px 34px rgba(0, 62, 51, 0.19);
            }

            .pp-placeholder-icon span {
                color: #ffffff !important;
                font-size: 17px;
                font-weight: 900;
            }

            .pp-placeholder-eyebrow {
                color: #8e6d27;
                font-size: 11px;
                font-weight: 900;
                letter-spacing: 0.15em;
                margin-bottom: 8px;
            }

            .pp-workspace-placeholder h1 {
                margin: 0;
                color: #003e33;
                font-size: 36px;
                font-weight: 920;
                letter-spacing: -0.045em;
            }

            .pp-workspace-placeholder p {
                max-width: 730px;
                margin: 12px 0 0 0;
                color: #5f6f63;
                font-size: 15px;
                line-height: 1.82;
            }

            @media (max-width: 760px) {
                .pp-sidebar-status-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


__all__ = ["render_platform_frame"]
