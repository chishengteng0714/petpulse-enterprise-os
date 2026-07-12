import streamlit as st


def apply_enterprise_theme():
    """
    PetPulse Enterprise Design System v2

    GM-08 Enterprise Design System：
    - 保留 Theme Layer / CSS Improvement
    - 移除 pp-card / pp-badge / pp-grid 舊 Design System
    - 移除所有 HTML Helper 產生的 UI
    - 不修改 Runtime
    - 不修改 Architecture
    - 不新增功能
    """

    st.markdown(
        """
        <style>
        :root {
            --pp-primary-green: #2F8F5B;
            --pp-dark-green: #123D2A;
            --pp-soft-green: #E7F4EC;
            --pp-light-beige: #FAF6EF;
            --pp-warm-beige: #F3E8D7;
            --pp-yellow: #F6C94C;
            --pp-orange: #F28C38;
            --pp-pink: #E96F9F;
            --pp-purple: #7D6AF2;

            --pp-text-main: #17231D;
            --pp-text-muted: #66746C;
            --pp-text-soft: #8A978F;

            --pp-border: #DDE7DF;
            --pp-border-strong: #C7D8CC;
            --pp-surface: #FFFFFF;
            --pp-surface-soft: #FBF8F2;

            --pp-radius-sm: 10px;
            --pp-radius-md: 16px;
            --pp-radius-lg: 24px;

            --pp-shadow-sm: 0 4px 14px rgba(18, 61, 42, 0.06);
            --pp-shadow-md: 0 12px 32px rgba(18, 61, 42, 0.10);
            --pp-shadow-hover: 0 16px 40px rgba(18, 61, 42, 0.14);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(47, 143, 91, 0.08), transparent 34%),
                linear-gradient(180deg, var(--pp-light-beige) 0%, #FFFFFF 44%, #FFFFFF 100%);
            color: var(--pp-text-main);
        }

        h1, h2, h3, h4 {
            color: var(--pp-dark-green);
            letter-spacing: -0.02em;
        }

        p, li, span {
            color: var(--pp-text-main);
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, var(--pp-dark-green) 0%, #1B5138 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #F7FFF9 !important;
        }

        [data-testid="stSidebar"] .stButton button {
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: var(--pp-radius-md);
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background: rgba(255, 255, 255, 0.18);
            border-color: rgba(255, 255, 255, 0.28);
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 4rem;
            max-width: 1280px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--pp-border);
            border-radius: var(--pp-radius-md);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: var(--pp-shadow-sm);
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease,
                background 180ms ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            border-color: var(--pp-border-strong);
            box-shadow: var(--pp-shadow-hover);
            background: #FFFFFF;
        }

        div[data-testid="stMetric"] {
            padding: 20px 22px;
            border-radius: var(--pp-radius-md);
            border: 1px solid var(--pp-border);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: var(--pp-shadow-sm);
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: var(--pp-border-strong);
            box-shadow: var(--pp-shadow-hover);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--pp-text-muted);
            font-weight: 700;
        }

        div[data-testid="stMetricValue"] {
            color: var(--pp-dark-green);
            letter-spacing: -0.04em;
        }

        div[data-testid="stMetricDelta"] {
            color: var(--pp-primary-green);
            font-weight: 700;
        }

        button[kind="primary"],
        .stButton button {
            border-radius: 999px;
            border: 1px solid rgba(47, 143, 91, 0.24);
            background: var(--pp-primary-green);
            color: #FFFFFF;
            font-weight: 800;
            box-shadow: 0 6px 18px rgba(47, 143, 91, 0.18);
            transition:
                transform 160ms ease,
                box-shadow 160ms ease,
                background 160ms ease;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            background: #267A4D;
            border-color: #267A4D;
            box-shadow: 0 10px 24px rgba(47, 143, 91, 0.24);
            color: #FFFFFF;
        }

        div[data-baseweb="select"] > div,
        input,
        textarea {
            border-radius: var(--pp-radius-sm) !important;
            border-color: var(--pp-border) !important;
            background-color: #FFFFFF !important;
        }

        div[data-baseweb="select"] > div:focus-within,
        input:focus,
        textarea:focus {
            border-color: var(--pp-primary-green) !important;
            box-shadow: 0 0 0 3px rgba(47, 143, 91, 0.12) !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: var(--pp-radius-md);
            overflow: hidden;
            border: 1px solid var(--pp-border);
            box-shadow: var(--pp-shadow-sm);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 8px 14px;
            background: rgba(47, 143, 91, 0.08);
            color: var(--pp-dark-green);
            font-weight: 800;
        }

        .stTabs [aria-selected="true"] {
            background: var(--pp-primary-green);
            color: #FFFFFF;
        }

        hr {
            border: none;
            height: 1px;
            background: var(--pp-border);
            margin: 24px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_enterprise_hero(
    eyebrow: str,
    title: str,
    summary: str,
):
    """
    共用 Hero 區塊。

    GM-08：
    - 改為 Streamlit Native
    - 不再產生 HTML
    """

    with st.container(border=True):
        st.caption(eyebrow)
        st.markdown(f"# {title}")
        st.write(summary)


def render_section_header(
    icon: str,
    title: str,
    description: str = "",
):
    """
    共用 Section Header。

    GM-08：
    - 改為 Streamlit Native
    - 不再產生 HTML
    """

    st.markdown(f"## {icon} {title}")

    if description:
        st.caption(description)


def render_enterprise_card(
    icon: str,
    title: str,
    body: str,
    caption: str = "",
    badge: str = "",
    badge_style: str = "green",
    meta: str = "",
):
    """
    共用 Enterprise Card。

    GM-08：
    - 改為 Streamlit Native
    - 保留原有參數相容性
    - badge_style 保留但不改變 Runtime
    """

    with st.container(border=True):
        if caption or badge:
            header_parts = []

            if caption:
                header_parts.append(caption)

            if badge:
                header_parts.append(badge)

            st.caption("｜".join(header_parts))

        st.markdown(f"### {icon} {title}")
        st.write(body)

        if meta:
            st.caption(meta)


def render_status_badge(
    label: str,
    style: str = "green",
):
    """
    共用 Status Badge。

    GM-08：
    - 改為 Streamlit Native
    - 保留 style 參數相容性
    """

    st.caption(label)