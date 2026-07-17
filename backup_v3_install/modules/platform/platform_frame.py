from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from typing import Any

import streamlit as st

from modules.platform.home.enterprise_home import render_enterprise_home
from modules.platform.runtime import create_platform_runtime
from modules.platform.workspace_registry import create_workspace_registry

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"
CSS_FILE = ASSETS_DIR / "enterprise.css"


def render_platform() -> None:
    _load_enterprise_design_system()
    runtime = create_platform_runtime()
    workspace_registry = create_workspace_registry()
    render_shared_sidebar_brand_and_navigation("home", runtime, workspace_registry)
    render_enterprise_home(runtime)


def render_shared_sidebar_brand_and_navigation(
    active_page: str | None = None,
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
) -> None:
    _load_enterprise_design_system()
    with st.sidebar:
        st.markdown(_brand_html(), unsafe_allow_html=True)
        st.markdown('<div class="pp-shell-nav-label">企業情報工作區</div>', unsafe_allow_html=True)
        st.page_link("app.py", label="企業首頁", icon=":material/home:")
        st.page_link("pages/2_證據中心.py", label="證據中心", icon=":material/fact_check:")
        st.markdown(_status_html(runtime, workspace_registry), unsafe_allow_html=True)
        st.markdown('''<div class="pp-shell-spacer"></div><div class="pp-shell-footer"><strong>PetPulse Enterprise OS</strong>Enterprise Intelligence Platform · v3</div>''', unsafe_allow_html=True)


def _brand_html() -> str:
    logo = _logo_html()
    return f'''<section class="pp-shell-brand"><div class="pp-shell-logo">{logo}</div><div class="pp-shell-name">PetPulse Enterprise OS</div><div class="pp-shell-edition">寵物公園企業情報決策系統</div></section>'''


def _logo_html() -> str:
    candidates = [ASSETS_DIR / name for name in ("petpark_logo.png","petpark-logo.png","logo.png","logo.jpg","logo.jpeg","logo.webp")]
    candidates += [p for p in ASSETS_DIR.glob("*") if p.suffix.lower() in {".png",".jpg",".jpeg",".webp"} and "logo" in p.stem.lower()]
    path = next((p for p in candidates if p.exists()), None)
    if not path:
        return '<div class="pp-shell-logo-fallback">寵物公園<br>Pet\'s Park</div>'
    try:
        data = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return '<div class="pp-shell-logo-fallback">寵物公園</div>'
    mime = {".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp"}.get(path.suffix.lower(),"application/octet-stream")
    return f'<img src="data:{mime};base64,{data}" alt="寵物公園 Logo">'


def _status_html(runtime: Any | None, registry: Any | None) -> str:
    status = "系統上線"
    if runtime is not None:
        for key in ("operating_status","status","runtime_status","health"):
            value = getattr(runtime, key, None)
            if value not in (None, ""):
                status = str(value); break
    count = 2
    if registry is not None:
        for key in ("routes","workspaces","items"):
            value = getattr(registry, key, None)
            try:
                if value is not None: count = len(value); break
            except TypeError: pass
    return f'''<section class="pp-shell-status"><div><span>系統狀態</span><strong>{escape(status)}</strong></div><div><span>工作入口</span><strong>{count} 個</strong></div></section>'''


def _load_enterprise_design_system() -> None:
    css = _read_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _read_css() -> str:
    try: return CSS_FILE.read_text(encoding="utf-8")
    except (OSError, UnicodeError): return ""


__all__ = ["render_platform", "render_shared_sidebar_brand_and_navigation"]
