from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys

import streamlit as st

from modules.platform import render_platform


PROJECT_ROOT = Path(__file__).resolve().parent
UPDATE_SCRIPT = PROJECT_ROOT / "update_evidence.py"
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence.json"


def _inject_app_presentation_style():
    """
    GM27 Sidebar Final Polish

    僅處理 Presentation：
    - 隱藏 Streamlit 原生 app / pages 導覽
    - 建立中文導覽
    - 縮小 Logo 區並上移
    - 更新按鈕改為品牌綠
    """

    st.markdown(
        """
        <style>
        /* 隱藏 Streamlit 自動產生的 app / 證據中心導覽 */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Sidebar 基礎寬度與間距 */
        [data-testid="stSidebar"] {
            width: 312px !important;
            min-width: 312px !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 14px !important;
        }

        /* 既有 Logo 區縮小、上移，避免巨大白框 */
        [data-testid="stSidebar"] .pp-sidebar-brand,
        [data-testid="stSidebar"] .pp-sidebar-brand-premium,
        [data-testid="stSidebar"] .pp-sidebar-logo-card,
        [data-testid="stSidebar"] .pp-brand-card {
            min-height: 112px !important;
            max-height: 138px !important;
            margin-top: 0 !important;
            margin-bottom: 16px !important;
            padding: 14px 18px !important;
            border-radius: 24px !important;
            overflow: hidden !important;
        }

        [data-testid="stSidebar"] .pp-sidebar-logo,
        [data-testid="stSidebar"] .pp-sidebar-logo img,
        [data-testid="stSidebar"] img[alt*="寵物公園"],
        [data-testid="stSidebar"] img[alt*="Pet"] {
            max-width: 218px !important;
            max-height: 76px !important;
            width: auto !important;
            height: auto !important;
            object-fit: contain !important;
            margin: 0 auto !important;
        }

        /* 自訂中文導覽 */
        .pp-app-nav-label {
            margin: 2px 8px 8px;
            color: rgba(255,255,255,.78) !important;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: .14em;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] {
            margin-bottom: 7px;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a {
            min-height: 52px;
            padding: 0 15px !important;
            border: 1px solid transparent !important;
            border-radius: 15px !important;
            color: #173f35 !important;
            background: transparent !important;
            font-size: 15px !important;
            font-weight: 850 !important;
            transition:
                transform 160ms ease,
                background 160ms ease,
                border-color 160ms ease,
                box-shadow 160ms ease !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
            transform: translateX(2px);
            background: rgba(255,255,255,.34) !important;
            border-color: rgba(255,255,255,.34) !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
            background: rgba(255,255,255,.94) !important;
            border-color: rgba(255,255,255,.70) !important;
            box-shadow: 0 12px 26px rgba(0,62,51,.12) !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] p,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span {
            color: #173f35 !important;
            font-size: 15px !important;
            font-weight: 850 !important;
        }

        /* 資料更新區 */
        .pp-update-title {
            margin: 0 0 14px;
            color: #003e33 !important;
            font-size: 19px;
            font-weight: 900;
            letter-spacing: -.02em;
        }

        .pp-update-meta {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 14px;
        }

        .pp-update-meta-card {
            padding: 11px 12px;
            border-radius: 14px;
            background: rgba(255,255,255,.09);
            border: 1px solid rgba(255,255,255,.16);
        }

        .pp-update-meta-card span {
            display: block;
            color: rgba(255,255,255,.68) !important;
            font-size: 10px;
            font-weight: 750;
        }

        .pp-update-meta-card strong {
            display: block;
            margin-top: 5px;
            color: #ffffff !important;
            font-size: 13px;
            font-weight: 900;
            line-height: 1.45;
        }

        /* 立即更新按鈕：覆蓋 enterprise.css 的咖啡色 */
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stSidebar"] button[kind="secondary"] {
            min-height: 49px !important;
            border: 1px solid rgba(255,255,255,.22) !important;
            border-radius: 999px !important;
            color: #ffffff !important;
            background:
                linear-gradient(
                    135deg,
                    #003e33 0%,
                    #2f7147 52%,
                    #7baa3c 100%
                ) !important;
            box-shadow:
                0 13px 28px rgba(0,62,51,.22),
                inset 0 1px 0 rgba(255,255,255,.18) !important;
            font-size: 14px !important;
            font-weight: 850 !important;
            transition:
                transform 160ms ease,
                filter 160ms ease,
                box-shadow 160ms ease !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] button[kind="secondary"]:hover {
            transform: translateY(-1px) !important;
            filter: brightness(1.06) !important;
            box-shadow:
                0 17px 34px rgba(0,62,51,.27),
                inset 0 1px 0 rgba(255,255,255,.20) !important;
        }

        [data-testid="stSidebar"] .stButton > button p,
        [data-testid="stSidebar"] .stButton > button span {
            color: #ffffff !important;
            font-weight: 850 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _load_evidence_status() -> tuple[int, str]:
    """
    讀取 Evidence Center 資料狀態。

    回傳：
    - 資料筆數
    - 最後更新時間
    """

    if not EVIDENCE_FILE.exists():
        return 0, "尚未建立資料"

    try:
        with EVIDENCE_FILE.open("r", encoding="utf-8") as file:
            evidence_data = json.load(file)

        if isinstance(evidence_data, list):
            evidence_count = len(evidence_data)

        elif isinstance(evidence_data, dict):
            possible_items = (
                evidence_data.get("evidence_items")
                or evidence_data.get("evidence")
                or evidence_data.get("items")
                or evidence_data.get("articles")
                or evidence_data.get("data")
                or []
            )

            evidence_count = (
                len(possible_items)
                if isinstance(possible_items, list)
                else 0
            )

        else:
            evidence_count = 0

        modified_timestamp = EVIDENCE_FILE.stat().st_mtime
        modified_datetime = datetime.fromtimestamp(modified_timestamp)

        last_updated = modified_datetime.strftime("%Y/%m/%d %H:%M:%S")

        return evidence_count, last_updated

    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 0, "資料讀取異常"


def _run_evidence_update() -> tuple[bool, str]:
    """
    執行 update_evidence.py。

    回傳：
    - 是否成功
    - 執行訊息
    """

    if not UPDATE_SCRIPT.exists():
        return False, "找不到 update_evidence.py，請確認檔案位於專案根目錄。"

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(UPDATE_SCRIPT),
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            check=False,
        )

    except subprocess.TimeoutExpired:
        return False, "資料更新逾時，請稍後再試。"

    except Exception as exc:
        return False, f"資料更新發生例外：{exc}"

    if result.returncode != 0:
        error_message = (
            result.stderr.strip()
            or result.stdout.strip()
            or "update_evidence.py 執行失敗，但未回傳錯誤內容。"
        )

        return False, error_message

    success_message = (
        result.stdout.strip()
        or "Google News 資料已成功更新。"
    )

    return True, success_message


def _render_primary_navigation():
    """
    以中文 page_link 取代 Streamlit 原生 app 名稱。
    """

    with st.sidebar:
        st.markdown(
            '<div class="pp-app-nav-label">PETPULSE ENTERPRISE OS</div>',
            unsafe_allow_html=True,
        )

        st.page_link(
            "app.py",
            label="企業首頁",
            icon="🏠",
            use_container_width=True,
        )

        evidence_page = PROJECT_ROOT / "pages" / "2_證據中心.py"

        if evidence_page.exists():
            st.page_link(
                "pages/2_證據中心.py",
                label="證據中心",
                icon="🛡️",
                use_container_width=True,
            )


def _render_quick_update_control():
    """
    側邊欄資料更新中心。
    """

    evidence_count, last_updated = _load_evidence_status()

    with st.sidebar:
        st.divider()

        st.markdown(
            '<div class="pp-update-title">📡 資料更新</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="pp-update-meta">
                <div class="pp-update-meta-card">
                    <span>最後更新</span>
                    <strong>{last_updated}</strong>
                </div>
                <div class="pp-update-meta-card">
                    <span>新聞資料</span>
                    <strong>{evidence_count} 筆</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.pop("evidence_update_success", False):
            st.success("資料更新完成，最新新聞已載入。")

        if st.button(
            "🔄 立即更新資料",
            use_container_width=True,
            type="secondary",
            key="update_evidence_button",
        ):
            with st.spinner("正在擷取 Google News 最新資料..."):
                update_success, update_message = _run_evidence_update()

            if not update_success:
                st.error("資料更新失敗")
                st.code(update_message, language="text")
                return

            new_evidence_count, _ = _load_evidence_status()

            st.session_state["evidence_update_success"] = True
            st.session_state["evidence_update_count"] = new_evidence_count

            st.rerun()


def main():
    """
    PetPulse Enterprise OS

    平台啟動入口：
    - 保留既有 Golden Master Architecture
    - 僅加入 Demo 所需的資料更新控制與 Sidebar Presentation
    """

    _inject_app_presentation_style()
    _render_primary_navigation()
    _render_quick_update_control()
    render_platform()


if __name__ == "__main__":
    main()
