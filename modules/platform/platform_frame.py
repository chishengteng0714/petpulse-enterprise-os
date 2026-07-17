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
ENTERPRISE_CSS_FILE = ASSETS_DIR / "enterprise.css"

_LOGO_CANDIDATES = (
    ASSETS_DIR / "petpark_logo.png",
    ASSETS_DIR / "petpark-logo.png",
    ASSETS_DIR / "petspark_logo.png",
    ASSETS_DIR / "pets-park-logo.png",
    ASSETS_DIR / "logo.png",
    ASSETS_DIR / "logo.jpg",
    ASSETS_DIR / "logo.jpeg",
    ASSETS_DIR / "logo.webp",
)


def render_platform() -> None:
    _load_enterprise_design_system()

    runtime = create_platform_runtime()
    workspace_registry = create_workspace_registry()

    render_shared_sidebar(
        active_page="home",
        runtime=runtime,
        workspace_registry=workspace_registry,
        experience=None,
    )

    render_enterprise_home(runtime)


def render_shared_sidebar(
    active_page: str | None = None,
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
    experience: Any | None = None,
) -> None:
    """
    首頁與證據中心唯一共用 Sidebar Component。

    Presentation Layer Only：
    - 保留 Runtime / Registry / Experience
    - 保留原生 st.page_link 切頁
    - Sidebar 固定拆成四個區塊
    - 不修改任何商業邏輯或資料結構
    """

    _load_enterprise_design_system()
    normalized_active = _normalize_active_page(active_page)

    with st.sidebar:
        st.markdown(
            f'<span data-pp-active-page="{escape(normalized_active)}" '
            'style="display:none"></span>',
            unsafe_allow_html=True,
        )

        with st.container(key="pp-sidebar-brand-section"):
            st.markdown(_render_brand_block(), unsafe_allow_html=True)

        with st.container(key="pp-sidebar-workspace-section"):
            st.markdown(
                '<div class="pp-sidebar-section-label">工作區</div>',
                unsafe_allow_html=True,
            )
            _render_navigation(normalized_active)

        with st.container(key="pp-sidebar-status-section"):
            st.markdown(
                _render_system_status(
                    runtime=runtime,
                    workspace_registry=workspace_registry,
                    experience=experience,
                ),
                unsafe_allow_html=True,
            )

        with st.container(key="pp-sidebar-assistant-section"):
            st.markdown(
                _render_sidebar_assistant(),
                unsafe_allow_html=True,
            )


def _render_navigation(active_page: str) -> None:
    """首頁與證據中心共用的原生 Streamlit Navigation。"""

    with st.container(key="pp-sidebar-nav"):
        with st.container(key="pp-nav-home"):
            st.page_link(
                "app.py",
                label="企業首頁",
                icon=":material/home:",
                use_container_width=True,
            )

        with st.container(key="pp-nav-evidence"):
            st.page_link(
                "pages/2_證據中心.py",
                label="證據中心",
                icon=":material/fact_check:",
                use_container_width=True,
            )

def _render_brand_block() -> str:
    return (
        '<section class="pp4-sidebar-brand" aria-label="PetPulse 品牌識別">'
        '<div class="pp4-sidebar-logo">'
        f"{_build_logo_html()}"
        "</div>"
        '<div class="pp4-sidebar-product">'
        "<strong>PetPulse Enterprise OS</strong>"
        "<span>企業情報決策系統</span>"
        "</div>"
        '<div class="pp4-sidebar-brand-divider" aria-hidden="true"></div>'
        "</section>"
    )


def _render_system_status(
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
    experience: Any | None = None,
) -> str:
    del workspace_registry

    operating_status = _safe_text(
        _safe_get(experience, "operating_status", None),
        _runtime_status(runtime),
    )
    confidence_level = _safe_text(
        _safe_get(experience, "confidence_level", None),
        "高",
    )

    return (
        '<section class="pp-sidebar-status-card" aria-label="System Status">'
        '<div class="pp-sidebar-status-head">'
        '<div class="pp-sidebar-status-title">'
        '<i></i><span>系統正常</span>'
        '</div>'
        f'<strong>{escape(operating_status)}</strong>'
        '</div>'
        '<div class="pp-sidebar-status-grid">'
        '<span>資料可信度</span>'
        f'<strong>{escape(confidence_level)}</strong>'
        '<span>營運狀態</span>'
        f'<strong>{escape(operating_status)}</strong>'
        '</div>'
        '</section>'
    )


def _render_sidebar_assistant() -> str:
    return (
        '<section class="pp-sidebar-assistant-card" aria-label="AI Assistant">'
        '<span class="pp-sidebar-assistant-icon pp4-icon">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3a7 7 0 0 0-4 12.7V19a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-3.3A7 7 0 0 0 12 3z"/>'
        '</svg>'
        '</span>'
        '<div class="pp-sidebar-assistant-copy">'
        '<strong>AI Assistant</strong>'
        '<small>今日情報摘要已完成</small>'
        '</div>'
        '<i class="pp-sidebar-assistant-dot"></i>'
        '</section>'
    )


def _render_sidebar_version() -> str:
    return (
        '<footer class="pp4-sidebar-version">'
        "<strong>PetPulse Enterprise OS</strong>"
        "<span>Sidebar Section Final · v4.0</span>"
        "</footer>"
    )


def _load_enterprise_design_system() -> None:
    if not ENTERPRISE_CSS_FILE.exists():
        return

    try:
        css = ENTERPRISE_CSS_FILE.read_text(encoding="utf-8")
    except OSError:
        return

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _normalize_active_page(active_page: str | None) -> str:
    normalized = (active_page or "").strip().lower()
    return normalized if normalized in {"home", "evidence"} else "home"


def _build_logo_html() -> str:
    logo_path = _find_logo_file()

    if logo_path is None:
        return (
            '<div class="pp4-sidebar-logo-fallback">'
            "寵物公園<br><span>Pet's Park</span>"
            "</div>"
        )

    try:
        encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except OSError:
        return '<div class="pp4-sidebar-logo-fallback">寵物公園</div>'

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(logo_path.suffix.lower(), "application/octet-stream")

    return (
        f'<img src="data:{mime_type};base64,{encoded}" '
        'alt="寵物公園 Pet’s Park Logo">'
    )


def _find_logo_file() -> Path | None:
    for candidate in _LOGO_CANDIDATES:
        if candidate.exists() and candidate.is_file():
            return candidate

    if not ASSETS_DIR.exists():
        return None

    matches: list[Path] = []

    for path in ASSETS_DIR.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue

        normalized = path.stem.lower().replace("-", "").replace("_", "")
        if any(keyword in normalized for keyword in ("logo", "petpark", "petspark")):
            matches.append(path)

    if not matches:
        return None

    return sorted(matches, key=lambda item: len(item.name))[0]


def _runtime_status(runtime: Any | None) -> str:
    if runtime is None:
        return "穩定"

    for attribute in ("operating_status", "status", "runtime_status", "health"):
        value = getattr(runtime, attribute, None)
        if value not in (None, ""):
            return str(value)

    return "穩定"


def _safe_get(item: Any, key: str, default: Any = None) -> Any:
    if item is None:
        return default
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _safe_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return str(fallback)
    text = str(value).strip()
    return text or str(fallback)


# 向下相容：舊頁面名稱直接指向同一個 Sidebar renderer，沒有第二套 DOM。
render_shared_sidebar_brand_and_navigation = render_shared_sidebar


__all__ = [
    "render_platform",
    "render_shared_sidebar",
    "render_shared_sidebar_brand_and_navigation",
]
