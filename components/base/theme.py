import streamlit as st


def inject_petpulse_theme():
    """
    PetPulse Enterprise Theme

    GM-10 Enterprise Presentation Rewrite：
    - Presentation Layer Only
    - 不新增 Theme Engine
    - 不修改 Runtime / Registry / State
    - 只注入全域 CSS
    """

    st.markdown(
        """
        <style>
            :root {
                --pp-primary: #1F3C2E;
                --pp-secondary: #6F8F72;
                --pp-accent: #C2A86F;
                --pp-background: #FBF8F1;
                --pp-card: #FFFFFF;
                --pp-text: #1F3C2E;
                --pp-muted: #5F6F63;
                --pp-border: rgba(31, 60, 46, 0.10);
                --pp-shadow: 0 18px 46px rgba(31, 60, 46, 0.07);
                --pp-shadow-soft: 0 14px 34px rgba(31, 60, 46, 0.055);
                --pp-radius-lg: 28px;
                --pp-radius-md: 22px;
                --pp-radius-sm: 16px;
            }

            html,
            body,
            [data-testid="stAppViewContainer"] {
                background: var(--pp-background);
                color: var(--pp-text);
            }

            [data-testid="stAppViewContainer"] > .main {
                background:
                    radial-gradient(circle at top left, rgba(194, 168, 111, 0.12), transparent 32%),
                    linear-gradient(180deg, #FBF8F1 0%, #F8F3E9 100%);
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 4rem;
                max-width: 1240px;
            }

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                color: var(--pp-primary);
                letter-spacing: -0.03em;
            }

            p,
            li,
            span {
                color: inherit;
            }

            div[data-testid="stMarkdownContainer"] p {
                color: var(--pp-muted);
                line-height: 1.75;
            }

            hr {
                border: none;
                border-top: 1px solid var(--pp-border);
                margin: 1.5rem 0;
            }

            button[kind="primary"],
            button[kind="secondary"],
            .stButton > button {
                border-radius: 999px !important;
                border: 1px solid rgba(194, 168, 111, 0.38) !important;
                background: #F4EBD8 !important;
                color: var(--pp-primary) !important;
                font-weight: 900 !important;
                box-shadow: 0 10px 24px rgba(31, 60, 46, 0.06) !important;
                transition:
                    transform 180ms ease,
                    background 180ms ease,
                    border-color 180ms ease,
                    box-shadow 180ms ease !important;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                background: #EFE2C7 !important;
                border-color: rgba(194, 168, 111, 0.68) !important;
                box-shadow: 0 14px 30px rgba(31, 60, 46, 0.10) !important;
            }

            label {
                color: var(--pp-primary) !important;
                font-weight: 850 !important;
            }

            [data-baseweb="select"] > div,
            [data-baseweb="input"] > div,
            textarea {
                border-radius: var(--pp-radius-sm) !important;
                border-color: rgba(31, 60, 46, 0.14) !important;
                background: #FFFEFB !important;
                box-shadow: none !important;
            }

            [data-baseweb="select"] > div:hover,
            [data-baseweb="input"] > div:hover,
            textarea:hover {
                border-color: rgba(111, 143, 114, 0.42) !important;
            }

            input,
            textarea {
                color: var(--pp-primary) !important;
            }

            [data-testid="stDataFrame"],
            [data-testid="stTable"] {
                border-radius: var(--pp-radius-md);
                overflow: hidden;
                border: 1px solid var(--pp-border);
                box-shadow: var(--pp-shadow-soft);
            }

            [data-testid="stMetric"] {
                padding: 18px;
                border-radius: var(--pp-radius-md);
                background: var(--pp-card);
                border: 1px solid var(--pp-border);
                box-shadow: var(--pp-shadow-soft);
            }

            [data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at top left, rgba(194, 168, 111, 0.14), transparent 32%),
                    linear-gradient(180deg, #FBF8F1 0%, #F7F3EA 100%);
                border-right: 1px solid var(--pp-border);
            }

            [data-testid="stSidebar"] * {
                color: var(--pp-primary);
            }

            [data-testid="stSidebar"] [role="radio"] {
                border-radius: 16px;
            }

            [data-testid="stAlert"] {
                border-radius: var(--pp-radius-md);
                border: 1px solid var(--pp-border);
                box-shadow: var(--pp-shadow-soft);
            }

            .pp-enterprise-card {
                background: var(--pp-card);
                border: 1px solid var(--pp-border);
                border-radius: var(--pp-radius-md);
                box-shadow: var(--pp-shadow-soft);
            }

            .pp-enterprise-badge {
                display: inline-flex;
                align-items: center;
                min-height: 28px;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 850;
                background: #F7F4EC;
                color: #4E604F;
                border: 1px solid rgba(31, 60, 46, 0.08);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )