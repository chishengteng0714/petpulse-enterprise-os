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

    render_shared_sidebar_brand_and_navigation(
        active_page="home",
        runtime=runtime,
        workspace_registry=workspace_registry,
        experience=None,
    )

    render_enterprise_home(runtime)


def render_shared_sidebar_brand_and_navigation(
    active_page: str | None = None,
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
    experience: Any | None = None,
) -> None:
    """
    首頁與證據中心共用 Sidebar。

    Frozen Architecture：
    - 保留 Runtime / Registry / Experience
    - 保留 st.page_link 原生路由
    - 僅處理 Presentation
    """

    _load_enterprise_design_system()

    with st.sidebar:
        st.markdown(_render_brand_block(), unsafe_allow_html=True)

        st.markdown(
            '<div class="pp32-sidebar-workspace">企業情報工作區</div>',
            unsafe_allow_html=True,
        )

        _render_navigation(active_page=active_page)

        st.markdown('<div class="pp32-sidebar-divider"></div>', unsafe_allow_html=True)

        st.markdown(
            _render_system_status(
                runtime=runtime,
                workspace_registry=workspace_registry,
                experience=experience,
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            _render_sidebar_version(),
            unsafe_allow_html=True,
        )


def _render_navigation(active_page: str | None = None) -> None:
    st.page_link(
        "app.py",
        label="企業首頁",
        icon=":material/home:",
    )

    st.page_link(
        "pages/2_證據中心.py",
        label="證據中心",
        icon=":material/fact_check:",
    )

    normalized_active = (active_page or "").strip().lower()

    if normalized_active in {"home", "evidence"}:
        st.markdown(
            f'<span data-pp-active-page="{escape(normalized_active)}" '
            'style="display:none"></span>',
            unsafe_allow_html=True,
        )


def _render_brand_block() -> str:
    return (
        '<section class="pp32-sidebar-brand" aria-label="PetPulse 品牌識別">'
        '<div class="pp32-sidebar-brand-row">'
        '<div class="pp32-sidebar-logo">'
        f'{_build_logo_html()}'
        '</div>'
        '<div class="pp32-sidebar-product">'
        '<strong>PetPulse Enterprise OS</strong>'
        '<span>寵物公園企業情報決策系統</span>'
        '</div>'
        '</div>'
        '</section>'
    )


def _render_system_status(
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
    experience: Any | None = None,
) -> str:
    operating_status = _safe_text(
        _safe_get(experience, "operating_status", None),
        _runtime_status(runtime),
    )
    confidence_level = _safe_text(
        _safe_get(experience, "confidence_level", None),
        "高",
    )

    return (
        '<section class="pp32-sidebar-status-compact" aria-label="Enterprise Status">'
        '<div class="pp32-status-line">'
        '<i></i>'
        f'<span>系統正常 · {escape(operating_status)}</span>'
        '</div>'
        f'<small>資料可信度 {escape(confidence_level)}</small>'
        '</section>'
        '<section class="pp32-sidebar-ai-compact" aria-label="AI Assistant">'
        '<span class="pp32-sidebar-ai-mark pp32-icon">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3a7 7 0 0 0-4 12.7V19a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-3.3A7 7 0 0 0 12 3z"/>'
        '</svg>'
        '</span>'
        '<div><strong>AI Assistant</strong>'
        '<small>情報摘要已就緒</small></div>'
        '</section>'
    )


def _render_sidebar_version() -> str:
    return (
        '<footer class="pp32-sidebar-version">'
        '<strong>PetPulse Enterprise OS</strong>'
        '<span>GM33 · v3.0</span>'
        '</footer>'
    )


def _load_enterprise_design_system() -> None:
    if not ENTERPRISE_CSS_FILE.exists():
        return

    try:
        css = ENTERPRISE_CSS_FILE.read_text(encoding="utf-8")
    except OSError:
        return

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _build_logo_html() -> str:
    logo_path = _find_logo_file()

    if logo_path is None:
        return (
            '<div class="pp32-sidebar-logo-fallback">'
            "寵物公園<br><span>Pet's Park</span>"
            "</div>"
        )

    try:
        encoded = base64.b64encode(
            logo_path.read_bytes()
        ).decode("ascii")
    except OSError:
        return '<div class="pp32-sidebar-logo-fallback">寵物公園</div>'

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

        if path.suffix.lower() not in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        }:
            continue

        normalized = (
            path.stem.lower()
            .replace("-", "")
            .replace("_", "")
        )

        if any(
            keyword in normalized
            for keyword in ("logo", "petpark", "petspark")
        ):
            matches.append(path)

    if not matches:
        return None

    return sorted(matches, key=lambda item: len(item.name))[0]


def _runtime_status(runtime: Any | None) -> str:
    if runtime is None:
        return "穩定"

    for attribute in (
        "operating_status",
        "status",
        "runtime_status",
        "health",
    ):
        value = getattr(runtime, attribute, None)

        if value not in (None, ""):
            return str(value)

    return "穩定"


def _get_registered_workspaces(
    workspace_registry: Any | None,
) -> list[Any]:
    if workspace_registry is None:
        return []

    if isinstance(workspace_registry, dict):
        return list(workspace_registry.values())

    if isinstance(workspace_registry, (list, tuple)):
        return list(workspace_registry)

    for method_name in ("list_workspaces", "get_all"):
        method = getattr(workspace_registry, method_name, None)

        if callable(method):
            try:
                result = method() or []
            except Exception:
                continue

            return (
                list(result.values())
                if isinstance(result, dict)
                else list(result)
            )

    workspaces = getattr(
        workspace_registry,
        "workspaces",
        None,
    )

    if isinstance(workspaces, dict):
        return list(workspaces.values())

    if isinstance(workspaces, (list, tuple)):
        return list(workspaces)

    routes = getattr(
        workspace_registry,
        "routes",
        None,
    )

    if isinstance(routes, dict):
        return list(routes.values())

    if isinstance(routes, (list, tuple)):
        return list(routes)

    return []


def _safe_get(
    item: Any,
    key: str,
    default: Any = None,
) -> Any:
    if item is None:
        return default

    if isinstance(item, dict):
        return item.get(key, default)

    return getattr(item, key, default)


def _safe_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


def _safe_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return str(fallback)

    text = str(value).strip()
    return text or str(fallback)


__all__ = [
    "render_platform",
    "render_shared_sidebar_brand_and_navigation",
]
