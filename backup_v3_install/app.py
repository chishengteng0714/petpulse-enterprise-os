from datetime import datetime
from html import escape
import json
from pathlib import Path
import subprocess
import sys

import streamlit as st

from modules.platform import render_platform

st.set_page_config(page_title="PetPulse Enterprise OS", page_icon="🐾", layout="wide", initial_sidebar_state="expanded")

PROJECT_ROOT = Path(__file__).resolve().parent
UPDATE_SCRIPT = PROJECT_ROOT / "update_evidence.py"
EVIDENCE_FILE = PROJECT_ROOT / "data" / "evidence.json"


def _load_evidence_status() -> tuple[int, str]:
    if not EVIDENCE_FILE.exists(): return 0, "尚未建立資料"
    try:
        data = json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list): count = len(data)
        elif isinstance(data, dict):
            items = data.get("evidence_items") or data.get("evidence") or data.get("items") or data.get("articles") or data.get("data") or []
            count = len(items) if isinstance(items, list) else 0
        else: count = 0
        updated = datetime.fromtimestamp(EVIDENCE_FILE.stat().st_mtime).strftime("%Y/%m/%d %H:%M")
        return count, updated
    except (OSError, json.JSONDecodeError, TypeError, ValueError): return 0, "資料讀取異常"


def _run_evidence_update() -> tuple[bool, str]:
    if not UPDATE_SCRIPT.exists(): return False, "找不到 update_evidence.py。"
    try:
        result = subprocess.run([sys.executable, str(UPDATE_SCRIPT)], cwd=str(PROJECT_ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, check=False)
    except subprocess.TimeoutExpired: return False, "資料更新逾時，請稍後再試。"
    except Exception as exc: return False, f"資料更新發生例外：{exc}"
    if result.returncode != 0: return False, result.stderr.strip() or result.stdout.strip() or "更新失敗。"
    return True, result.stdout.strip() or "品牌情報資料已更新。"


def _render_quick_update_control() -> None:
    count, updated = _load_evidence_status()
    if st.session_state.pop("evidence_update_success", False):
        st.success(f"資料更新完成，目前已載入 {st.session_state.pop('evidence_update_count', count)} 筆品牌情報。")
    left, right = st.columns([5.2, 1.35], gap="small", vertical_alignment="center")
    with left:
        title = "品牌情報資料已同步" if count else "尚未載入品牌情報"
        meta = f"最後更新 {updated} · 系統目前可供決策查閱" if count else f"最後狀態：{updated}"
        st.markdown(f'''<section class="pp-utility"><div class="pp-utility-copy"><span class="pp-dot"></span><div><div class="pp-utility-title">{escape(title)}</div><div class="pp-utility-meta">{escape(meta)}</div></div></div><div class="pp-pill">{count} 筆情報</div></section>''', unsafe_allow_html=True)
    with right:
        requested = st.button("立即更新資料", type="primary", use_container_width=True, key="petpulse_global_update")
    if requested:
        with st.spinner("正在同步最新品牌情報…"):
            ok, message = _run_evidence_update()
        if not ok:
            st.error("資料更新失敗"); st.code(message, language="text"); return
        new_count, _ = _load_evidence_status()
        st.session_state["evidence_update_success"] = True
        st.session_state["evidence_update_count"] = new_count
        st.rerun()


def main() -> None:
    _render_quick_update_control()
    render_platform()


if __name__ == "__main__": main()
