import base64
import mimetypes
from html import escape
from pathlib import Path

import streamlit as st

from modules.platform.home.enterprise_home import render_enterprise_home
from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)


def render_platform_frame():
    """
    PetPulse Enterprise OS v1.3 Executive Copilot
    GM27 Sidebar Final Redesign

    Presentation Layer Only
    不修改 Runtime / Router / Registry / Schema
    不修改 Business Logic / Evidence Schema
    """

    _inject_platform_frame_style()

    experience = build_enterprise_home_experience()
    _render_platform_sidebar(experience)

    render_enterprise_home()


def _safe(value, fallback=""):
    if value is None:
        return escape(str(fallback))

    text = str(value).strip()
    if not text:
        return escape(str(fallback))

    return escape(text)


def _items(experience, name):
    return getattr(experience, name, []) or []


def _find_brand_logo_data_uri():
    """
    在既有 assets 內尋找寵物公園 Logo。
    僅讀取既有 Presentation Asset，不新增資料夾或業務邏輯。
    """

    assets_dir = Path(__file__).resolve().parents[2] / "assets"

    if not assets_dir.exists():
        return ""

    preferred_names = (
        "petpark_logo",
        "petspark_logo",
        "pet_park_logo",
        "petpulse_logo",
        "寵物公園",
        "logo",
    )

    image_files = []
    for suffix in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        image_files.extend(assets_dir.rglob(suffix))

    ranked_files = sorted(
        image_files,
        key=lambda path: (
            min(
                (
                    index
                    for index, keyword in enumerate(preferred_names)
                    if keyword.lower() in path.stem.lower()
                ),
                default=999,
            ),
            len(path.name),
        ),
    )

    if not ranked_files:
        return ""

    logo_path = ranked_files[0]

    try:
        mime_type = mimetypes.guess_type(str(logo_path))[0] or "image/png"
        encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"
    except OSError:
        return ""


def _render_platform_sidebar(experience):
    decisions = _items(experience, "decisions")
    risks = _items(experience, "risks")
    workspaces = _items(experience, "workspaces")
    health_signals = _items(experience, "health_signals")

    operating_status = _safe(
        getattr(experience, "operating_status", None),
        "穩定",
    )
    confidence_level = _safe(
        getattr(experience, "confidence_level", None),
        "高",
    )

    health_value = "觀察中"
    if health_signals:
        health_value = _safe(
            getattr(health_signals[0], "value", None),
            "觀察中",
        )

    risk_label = "0 項" if not risks else f"{len(risks)} 項"
    decision_label = "0 項" if not decisions else f"{len(decisions)} 項"
    workspace_label = f"{len(workspaces)} 個" if workspaces else "待命"

    logo_data_uri = _find_brand_logo_data_uri()

    if logo_data_uri:
        logo_html = (
            f'<img class="pp27-sidebar-logo-image" '
            f'src="{logo_data_uri}" alt="寵物公園">'
        )
    else:
        logo_html = """
        <div class="pp27-sidebar-logo-fallback">
            <div class="pp27-sidebar-logo-mark">P</div>
            <div>
                <div class="pp27-sidebar-logo-title">寵物公園</div>
                <div class="pp27-sidebar-logo-subtitle">
                    PetPulse Enterprise OS
                </div>
            </div>
        </div>
        """

    with st.sidebar:
        st.markdown(
            f"""
            <section class="pp27-sidebar-brand">
                {logo_html}
            </section>

            <div class="pp27-sidebar-product">
                PETPULSE ENTERPRISE OS
            </div>
            """,
            unsafe_allow_html=True,
        )

        _render_sidebar_navigation()

        st.markdown(
            f"""
            <div class="pp27-sidebar-divider"></div>

            <section class="pp27-sidebar-command">
                <div class="pp27-sidebar-command-head">
                    <div>
                        <div class="pp27-sidebar-eyebrow">今日企業狀態</div>
                        <div class="pp27-sidebar-command-title">
                            {operating_status}
                        </div>
                    </div>
                    <div class="pp27-sidebar-live-badge">即時</div>
                </div>

                <div class="pp27-sidebar-health">
                    <div>
                        <span>品牌健康度</span>
                        <strong>{health_value}</strong>
                    </div>
                    <div class="pp27-sidebar-health-dot"></div>
                </div>

                <div class="pp27-sidebar-metric-grid">
                    <div>
                        <span>今日待決策</span>
                        <strong>{decision_label}</strong>
                    </div>
                    <div>
                        <span>風險訊號</span>
                        <strong>{risk_label}</strong>
                    </div>
                    <div>
                        <span>判斷信心</span>
                        <strong>{confidence_level}</strong>
                    </div>
                    <div>
                        <span>工作入口</span>
                        <strong>{workspace_label}</strong>
                    </div>
                </div>
            </section>

            <section class="pp27-sidebar-intelligence">
                <div class="pp27-sidebar-ai-mark">AI</div>
                <div>
                    <div class="pp27-sidebar-ai-title">智慧判讀正常</div>
                    <div class="pp27-sidebar-ai-desc">
                        今日狀態、決策與風險摘要已完成整理。
                    </div>
                </div>
            </section>

            <section class="pp27-sidebar-footer">
                <div class="pp27-sidebar-footer-mark">P</div>
                <div>
                    <div class="pp27-sidebar-footer-title">
                        PetPulse Enterprise OS
                    </div>
                    <div class="pp27-sidebar-footer-desc">
                        Powered by AI Intelligence
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )


def _render_sidebar_navigation():
    """
    使用 Streamlit 原生 page_link 取代自動頁面導覽。
    因此不再顯示英文 app。
    """

    st.page_link(
        "app.py",
        label="企業首頁",
        icon="🏠",
        use_container_width=True,
    )

    evidence_page = Path(__file__).resolve().parents[2] / "pages" / "2_證據中心.py"

    if evidence_page.exists():
        st.page_link(
            "pages/2_證據中心.py",
            label="證據中心",
            icon="🛡️",
            use_container_width=True,
        )


def _inject_platform_frame_style():
    st.markdown(
        """
        <style>
        /* 隱藏 Streamlit 自動產生的 app / pages 導覽 */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            width: 312px !important;
            min-width: 312px !important;
            background:
                radial-gradient(
                    circle at 16% 2%,
                    rgba(255, 255, 255, .10),
                    transparent 26%
                ),
                linear-gradient(
                    180deg,
                    #7baa3c 0%,
                    #82ad48 54%,
                    #7ba743 100%
                ) !important;
            border-right: 1px solid rgba(0, 62, 51, .08);
            box-shadow: 18px 0 52px rgba(0, 62, 51, .10);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 18px 18px 22px !important;
        }

        [data-testid="stSidebar"] * {
            box-sizing: border-box;
        }

        /* 品牌區：縮小、上移、取消過大的空白 */
        .pp27-sidebar-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 116px;
            margin: 0 0 18px;
            padding: 18px 20px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, .62);
            border-radius: 26px;
            background:
                radial-gradient(
                    circle at 88% 8%,
                    rgba(216, 183, 106, .18),
                    transparent 32%
                ),
                rgba(255, 255, 255, .94);
            box-shadow:
                0 18px 40px rgba(0, 62, 51, .16),
                inset 0 1px 0 rgba(255, 255, 255, .92);
        }

        .pp27-sidebar-logo-image {
            display: block;
            width: auto;
            max-width: 218px;
            max-height: 78px;
            object-fit: contain;
        }

        .pp27-sidebar-logo-fallback {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #003e33;
        }

        .pp27-sidebar-logo-mark {
            display: grid;
            place-items: center;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #7baa3c;
            color: #ffffff;
            font-size: 21px;
            font-weight: 900;
        }

        .pp27-sidebar-logo-title {
            color: #18231f;
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -.03em;
        }

        .pp27-sidebar-logo-subtitle {
            margin-top: 3px;
            color: #5c6e65;
            font-size: 11px;
            font-weight: 700;
        }

        .pp27-sidebar-product {
            margin: 0 10px 10px;
            color: rgba(255, 255, 255, .78);
            font-size: 10px;
            font-weight: 900;
            letter-spacing: .14em;
        }

        /* 自訂頁面導覽 */
        [data-testid="stSidebar"] [data-testid="stPageLink"] {
            margin-bottom: 7px;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a {
            min-height: 52px;
            padding: 0 15px !important;
            border: 1px solid transparent;
            border-radius: 15px;
            color: #173f35 !important;
            background: transparent;
            font-size: 15px;
            font-weight: 850;
            transition:
                transform 160ms ease,
                background 160ms ease,
                border-color 160ms ease,
                box-shadow 160ms ease;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
            transform: translateX(2px);
            background: rgba(255, 255, 255, .36);
            border-color: rgba(255, 255, 255, .34);
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
            background: rgba(255, 255, 255, .92);
            border-color: rgba(255, 255, 255, .72);
            box-shadow: 0 12px 26px rgba(0, 62, 51, .11);
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] p,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span {
            color: #173f35 !important;
            font-size: 15px !important;
            font-weight: 850 !important;
        }

        .pp27-sidebar-divider {
            height: 1px;
            margin: 18px 0;
            background: rgba(255, 255, 255, .24);
        }

        /* 更新按鈕：全面取代咖啡色 */
        [data-testid="stSidebar"] .stButton > button {
            min-height: 48px !important;
            border: 1px solid rgba(255, 255, 255, .22) !important;
            border-radius: 999px !important;
            color: #ffffff !important;
            background:
                linear-gradient(
                    135deg,
                    #003e33 0%,
                    #356f43 48%,
                    #7baa3c 100%
                ) !important;
            box-shadow:
                0 12px 28px rgba(0, 62, 51, .21),
                inset 0 1px 0 rgba(255, 255, 255, .16) !important;
            font-size: 14px !important;
            font-weight: 850 !important;
            transition:
                transform 160ms ease,
                box-shadow 160ms ease,
                filter 160ms ease !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            transform: translateY(-1px);
            filter: brightness(1.05);
            box-shadow:
                0 16px 32px rgba(0, 62, 51, .26),
                inset 0 1px 0 rgba(255, 255, 255, .18) !important;
        }

        [data-testid="stSidebar"] .stButton > button:active {
            transform: translateY(0);
        }

        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            color: #ffffff !important;
            font-weight: 850 !important;
        }

        .pp27-sidebar-command {
            margin-top: 18px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, .20);
            border-radius: 21px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, .14),
                    rgba(255, 255, 255, .07)
                );
            box-shadow:
                0 14px 34px rgba(0, 62, 51, .10),
                inset 0 1px 0 rgba(255, 255, 255, .18);
        }

        .pp27-sidebar-command-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 12px;
        }

        .pp27-sidebar-eyebrow {
            color: rgba(255, 255, 255, .69);
            font-size: 10px;
            font-weight: 850;
            letter-spacing: .10em;
        }

        .pp27-sidebar-command-title {
            margin-top: 5px;
            color: #ffffff;
            font-size: 17px;
            font-weight: 900;
        }

        .pp27-sidebar-live-badge {
            padding: 5px 9px;
            border: 1px solid rgba(255, 255, 255, .17);
            border-radius: 999px;
            color: #ffffff;
            background: rgba(255, 255, 255, .12);
            font-size: 9px;
            font-weight: 850;
        }

        .pp27-sidebar-health {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 14px;
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, .16);
            border-radius: 16px;
            background: rgba(255, 255, 255, .08);
        }

        .pp27-sidebar-health span,
        .pp27-sidebar-metric-grid span {
            display: block;
            color: rgba(255, 255, 255, .66);
            font-size: 10px;
            font-weight: 750;
        }

        .pp27-sidebar-health strong {
            display: block;
            margin-top: 4px;
            color: #ffffff;
            font-size: 19px;
            font-weight: 900;
        }

        .pp27-sidebar-health-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #a7cf60;
            box-shadow: 0 0 0 6px rgba(167, 207, 96, .13);
        }

        .pp27-sidebar-metric-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
            margin-top: 8px;
        }

        .pp27-sidebar-metric-grid > div {
            padding: 10px;
            border: 1px solid rgba(255, 255, 255, .14);
            border-radius: 14px;
            background: rgba(255, 255, 255, .065);
        }

        .pp27-sidebar-metric-grid strong {
            display: block;
            margin-top: 5px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 900;
        }

        .pp27-sidebar-intelligence {
            display: grid;
            grid-template-columns: auto minmax(0, 1fr);
            align-items: center;
            gap: 10px;
            margin-top: 12px;
            padding: 11px 12px;
            border: 1px solid rgba(255, 255, 255, .13);
            border-radius: 15px;
            background: rgba(255, 255, 255, .07);
        }

        .pp27-sidebar-ai-mark {
            display: grid;
            place-items: center;
            width: 31px;
            height: 31px;
            border-radius: 10px;
            color: #ffffff;
            background: rgba(255, 255, 255, .13);
            font-size: 10px;
            font-weight: 900;
        }

        .pp27-sidebar-ai-title {
            color: #ffffff;
            font-size: 11px;
            font-weight: 850;
        }

        .pp27-sidebar-ai-desc {
            margin-top: 2px;
            color: rgba(255, 255, 255, .57);
            font-size: 9px;
            line-height: 1.45;
        }

        .pp27-sidebar-footer {
            display: grid;
            grid-template-columns: auto minmax(0, 1fr);
            align-items: center;
            gap: 9px;
            margin-top: 22px;
            padding: 15px 4px 0;
            border-top: 1px solid rgba(255, 255, 255, .20);
        }

        .pp27-sidebar-footer-mark {
            display: grid;
            place-items: center;
            width: 29px;
            height: 29px;
            border: 1px solid rgba(255, 255, 255, .18);
            border-radius: 10px;
            color: #ffffff;
            background: rgba(255, 255, 255, .10);
            font-size: 10px;
            font-weight: 900;
        }

        .pp27-sidebar-footer-title {
            color: #ffffff;
            font-size: 10px;
            font-weight: 850;
        }

        .pp27-sidebar-footer-desc {
            margin-top: 2px;
            color: rgba(255, 255, 255, .55);
            font-size: 8.8px;
        }

        @media (max-width: 760px) {
            [data-testid="stSidebar"] {
                width: 285px !important;
                min-width: 285px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


__all__ = ["render_platform_frame"]
