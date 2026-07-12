import streamlit as st


def apply_enterprise_theme():
    """
    PetPulse Enterprise Theme Layer

    GM-08 Enterprise Design System v2

    原則：
    - 不新增 Runtime
    - 不新增 Engine
    - 不新增 Layer / Domain / Registry / API
    - 不改變 Runtime Behavior
    - 不建立 HTML Card Helper
    - 只透過 Streamlit Native Components + 全域 CSS 改善產品視覺
    """

    st.markdown(
        """
        <style>
        :root {
            --pp-bg: #f7f4ef;
            --pp-surface: #ffffff;
            --pp-surface-soft: #fbfaf7;
            --pp-text: #1f2933;
            --pp-muted: #6b7280;
            --pp-border: #e7dfd4;
            --pp-border-strong: #d6c8b9;
            --pp-primary: #8b5e3c;
            --pp-primary-dark: #5f3d28;
            --pp-accent: #d99a5b;
            --pp-success: #3f7d58;
            --pp-warning: #b7791f;
            --pp-danger: #b94a48;
            --pp-radius: 18px;
            --pp-shadow: 0 10px 30px rgba(95, 61, 40, 0.08);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: var(--pp-bg);
            color: var(--pp-text);
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                "Noto Sans TC",
                "Microsoft JhengHei",
                sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(247, 244, 239, 0.86);
            backdrop-filter: blur(16px);
        }

        [data-testid="stSidebar"] {
            background: #efe7dc;
            border-right: 1px solid var(--pp-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--pp-text);
        }

        .block-container {
            padding-top: 2.4rem;
            padding-bottom: 4rem;
            max-width: 1280px;
        }

        h1, h2, h3 {
            color: var(--pp-text);
            letter-spacing: -0.03em;
        }

        h1 {
            font-size: 2.35rem;
            font-weight: 760;
            margin-bottom: 0.35rem;
        }

        h2 {
            font-size: 1.55rem;
            font-weight: 720;
            margin-top: 2.2rem;
            margin-bottom: 0.25rem;
        }

        h3 {
            font-size: 1.15rem;
            font-weight: 680;
        }

        p, li, div, span {
            line-height: 1.72;
        }

        [data-testid="stCaptionContainer"] {
            color: var(--pp-muted);
            font-size: 0.92rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--pp-surface);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius);
            box-shadow: var(--pp-shadow);
            transition:
                border-color 160ms ease,
                box-shadow 160ms ease,
                transform 160ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: var(--pp-border-strong);
            box-shadow: 0 14px 36px rgba(95, 61, 40, 0.12);
            transform: translateY(-1px);
        }

        [data-testid="stMetric"] {
            background: var(--pp-surface);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius);
            padding: 1rem 1.05rem;
            box-shadow: var(--pp-shadow);
        }

        [data-testid="stMetricLabel"] {
            color: var(--pp-muted);
            font-size: 0.86rem;
            font-weight: 560;
        }

        [data-testid="stMetricValue"] {
            color: var(--pp-primary-dark);
            font-size: 1.7rem;
            font-weight: 760;
            letter-spacing: -0.04em;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.86rem;
            font-weight: 620;
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid var(--pp-border-strong);
            background: var(--pp-primary);
            color: #ffffff;
            font-weight: 680;
            padding: 0.52rem 1.05rem;
            transition:
                background 160ms ease,
                border-color 160ms ease,
                transform 160ms ease,
                box-shadow 160ms ease;
        }

        .stButton > button:hover {
            background: var(--pp-primary-dark);
            border-color: var(--pp-primary-dark);
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(95, 61, 40, 0.18);
        }

        .stButton > button:focus {
            box-shadow: 0 0 0 3px rgba(217, 154, 91, 0.28);
        }

        [data-baseweb="select"] > div,
        [data-testid="stTextInput"] input {
            border-radius: 14px;
            border-color: var(--pp-border);
            background: var(--pp-surface);
        }

        [data-baseweb="select"] > div:focus-within,
        [data-testid="stTextInput"] input:focus {
            border-color: var(--pp-accent);
            box-shadow: 0 0 0 3px rgba(217, 154, 91, 0.22);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius);
            overflow: hidden;
            box-shadow: var(--pp-shadow);
            background: var(--pp-surface);
        }

        [data-testid="stTabs"] button {
            color: var(--pp-muted);
            font-weight: 620;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--pp-primary-dark);
        }

        hr {
            border-color: var(--pp-border);
            margin: 2rem 0;
        }

        div[data-testid="stAlert"] {
            border-radius: var(--pp-radius);
            border: 1px solid var(--pp-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_petpulse_enterprise_theme():
    """
    Backward compatible theme entry.

    保留既有 import 名稱：
    from modules.platform.theme import apply_petpulse_enterprise_theme

    Runtime Behavior 不變。
    """

    apply_enterprise_theme()