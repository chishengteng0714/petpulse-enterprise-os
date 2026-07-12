from pathlib import Path

import streamlit as st

from components.workspace.overview import render_overview_workspace
from utils.data_loader import load_analysis_data, load_history_data


BASE_DIR = Path(__file__).resolve().parents[1]
CSS_PATH = BASE_DIR / "assets" / "enterprise.css"


def configure_workspace_page():
    """
    Workspace Page Configuration

    GM-09 Enterprise UI Polish：
    - 保持 Runtime Behavior 不變
    - 保持 Architecture 不變
    - 維持 wide layout 作為 Enterprise OS 基礎版面
    - 統一產品名稱與瀏覽器頁籤識別
    """

    st.set_page_config(
        page_title="PetPulse Enterprise OS",
        page_icon="🐶",
        layout="wide",
    )


def load_enterprise_styles():
    """
    Enterprise Theme Loader

    全站品牌視覺由 assets/enterprise.css 統一管理。

    注意：
    - 此處僅載入既有 CSS
    - 不新增 Runtime UI 行為
    - 不新增 Theme Engine
    - 不改變 Architecture
    """

    if not CSS_PATH.exists():
        st.warning("找不到企業視覺樣式檔，請確認 assets/enterprise.css 是否存在。")
        return

    with open(CSS_PATH, "r", encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def render_workspace_application():
    """
    PetPulse Enterprise OS Application Entry

    GM-09 Enterprise UI Polish：
    - 不新增功能
    - 不改資料流
    - 不改 Workspace Architecture
    - 僅維持全站設定、樣式載入與首頁渲染順序
    """

    configure_workspace_page()
    load_enterprise_styles()

    data = load_analysis_data()
    history = load_history_data()

    render_overview_workspace(data, history)