from pathlib import Path
import streamlit as st


def apply_enterprise_theme():
    css_path = Path(__file__).resolve().parents[1] / "assets" / "enterprise.css"

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning("找不到 enterprise.css，請確認 dashboard/assets/enterprise.css 是否存在。")