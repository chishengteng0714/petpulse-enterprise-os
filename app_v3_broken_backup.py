from __future__ import annotations

from datetime import datetime
from html import escape
import json
from pathlib import Path
import subprocess
import sys

import streamlit as st

from modules.platform import render_platform


st.set_page_config(
    page_title="PetPulse Enterprise OS",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)


PROJECT_ROOT = Path(__file__).resolve().parent
UPDATE_SCRIPT = PROJECT_ROOT / "update_evidence.py"
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence.json"


def _load_evidence_status() -> tuple[int, str]:
    """
    讀取既有 Evidence 資料狀態。

    Frozen Architecture compliance:
    - 不修改資料來源。
    - 不修改資料結構。
    - 不修改 Evidence Service / Repository。
    """

    if not EVIDENCE_FILE.exists():
        return 0, "尚未建立資料"

    try:
        with EVIDENCE_FILE.open("r", encoding="utf-8") as file:
            evidence_data = json.load(file)

        evidence_count = _count_evidence_items(evidence_data)

        modified_datetime = datetime.fromtimestamp(
            EVIDENCE_FILE.stat().st_mtime
        )
        last_updated = modified_datetime.strftime("%Y/%m/%d %H:%M")

        return evidence_count, last_updated

    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 0, "資料讀取異常"


def _count_evidence_items(evidence_data: object) -> int:
    if isinstance(evidence_data, list):
        return len(evidence_data)

    if not isinstance(evidence_data, dict):
        return 0

    possible_items = (
        evidence_data.get("evidence_items")
        or evidence_data.get("evidence")
        or evidence_data.get("items")
        or evidence_data.get("articles")
        or evidence_data.get("data")
        or []
    )

    return len(possible_items) if isinstance(possible_items, list) else 0


def _run_evidence_update() -> tuple[bool, str]:
    """
    執行既有 update_evidence.py。

    更新腳本、工作目錄、Timeout 與回傳判斷均保留既有行為。
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
        or "品牌情報資料已成功更新。"
    )
    return True, success_message


def _render_quick_update_control() -> None:
    """
    首頁與證據中心共用的 Global Utility Bar。

    此函式名稱保留，讓證據中心現有 import 在 v3 改寫前仍可運作。
    """

    evidence_count, last_updated = _load_evidence_status()

    if st.session_state.pop("evidence_update_success", False):
        updated_count = st.session_state.pop(
            "evidence_update_count",
            evidence_count,
        )
        st.success(f"資料更新完成，目前已載入 {updated_count} 筆品牌情報。")

    status_class, status_title, status_meta = _resolve_update_status(
        evidence_count=evidence_count,
        last_updated=last_updated,
    )

    status_column, action_column = st.columns(
        [5.2, 1.35],
        gap="small",
        vertical_alignment="center",
    )

    with status_column:
        st.markdown(
            f"""
            <section class="pp-utility-bar" aria-label="資料同步狀態">
                <div class="pp-utility-copy">
                    <span class="pp-utility-status-dot {status_class}"></span>
                    <div class="pp-utility-text">
                        <div class="pp-utility-title">
                            {escape(status_title)}
                        </div>
                        <div class="pp-utility-meta">
                            {escape(status_meta)}
                        </div>
                    </div>
                </div>
                <div class="pp-badge">
                    {evidence_count} 筆情報
                </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    with action_column:
        update_requested = st.button(
            "立即更新資料",
            type="primary",
            use_container_width=True,
            key="petpulse_global_update_button",
        )

    if not update_requested:
        return

    with st.spinner("正在同步最新品牌情報…"):
        update_success, update_message = _run_evidence_update()

    if not update_success:
        st.error("資料更新失敗")
        st.code(update_message, language="text")
        return

    new_evidence_count, _ = _load_evidence_status()

    st.session_state["evidence_update_success"] = True
    st.session_state["evidence_update_count"] = new_evidence_count
    st.rerun()


def _resolve_update_status(
    evidence_count: int,
    last_updated: str,
) -> tuple[str, str, str]:
    if last_updated == "資料讀取異常":
        return (
            "danger",
            "資料狀態異常",
            "目前無法讀取資料檔案，請重新執行更新。",
        )

    if evidence_count <= 0:
        return (
            "warning",
            "尚未載入品牌情報",
            f"最後狀態：{last_updated}",
        )

    return (
        "",
        "品牌情報資料已同步",
        f"最後更新 {last_updated} · 系統目前可供決策查閱",
    )


def main() -> None:
    """
    PetPulse Enterprise OS v3 entry point.

    執行順序：
    1. 顯示全域資料 Utility Bar。
    2. 啟動既有 Platform Runtime 與 Enterprise Home。
    """

    _render_quick_update_control()
    render_platform()


if __name__ == "__main__":
    main()
