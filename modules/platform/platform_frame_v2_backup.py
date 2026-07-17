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
    """
    PetPulse Enterprise OS v3 application shell.

    Frozen Architecture compliance:
    - Runtime 建立方式不變。
    - Workspace Registry 建立方式不變。
    - Enterprise Home Experience / Business Logic 不變。
    - 本檔只負責 CSS、Sidebar、Navigation 與頁面 Presentation 組裝。
    """

    _load_enterprise_design_system()

    runtime = create_platform_runtime()
    workspace_registry = create_workspace_registry()

    render_shared_sidebar_brand_and_navigation(
        active_page="home",
        runtime=runtime,
        workspace_registry=workspace_registry,
    )

    render_enterprise_home(runtime)


def render_shared_sidebar_brand_and_navigation(
    active_page: str | None = None,
    runtime: Any | None = None,
    workspace_registry: Any | None = None,
) -> None:
    """
    首頁與證據中心共用的唯一 Sidebar。

    active_page 僅作為舊版 Streamlit 的視覺相容參數。
    支援的值：
    - "home"
    - "evidence"

    新版 Streamlit 會由 st.page_link 自動輸出 aria-current="page"，
    enterprise.css 會直接處理 Active State。
    """

    _load_enterprise_design_system()

    with st.sidebar:
        st.markdown(_render_brand_block(), unsafe_allow_html=True)

        st.markdown(
            '<div class="pp-shell-nav-label">企業情報工作區</div>',
            unsafe_allow_html=True,
        )

        _render_navigation(active_page=active_page)

        st.markdown(
            _render_system_status(
                runtime=runtime,
                workspace_registry=workspace_registry,
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="pp-shell-spacer" aria-hidden="true"></div>
            <footer class="pp-shell-footer">
                <strong>PetPulse Enterprise OS</strong>
                <span>Enterprise Intelligence Platform · v3</span>
            </footer>
            """,
            unsafe_allow_html=True,
        )


def _render_navigation(active_page: str | None = None) -> None:
    """
    使用 Streamlit 原生 page_link 建立可靠路由。

    active_page 保留給較舊 Streamlit 版本的相容標記；
    正式 Active State 優先由 aria-current="page" 判定。
    """

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
    logo_html = _build_logo_html()

    return f"""
    <section class="pp-shell-brand" aria-label="PetPulse 品牌識別">
        <div class="pp-shell-brand-logo">
            {logo_html}
        </div>
        <div class="pp-shell-product">
            <span class="pp-shell-product-name">PetPulse Enterprise OS</span>
            <span class="pp-shell-product-edition">
                寵物公園企業情報決策系統
            </span>
        </div>
    </section>
    """


def _build_logo_html() -> str:
    logo_path = _find_logo_file()

    if logo_path is None:
        return (
            '<div class="pp-shell-brand-fallback">'
            "寵物公園<br>Pet's Park"
            "</div>"
        )

    try:
        encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    except OSError:
        return (
            '<div class="pp-shell-brand-fallback">'
            "寵物公園<br>Pet's Park"
            "</div>"
        )

    mime_type = _image_mime_type(logo_path)
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

    supported_suffixes = {".png", ".jpg", ".jpeg", ".webp"}
    keywords = ("logo", "petpark", "petspark", "pet", "寵物公園")

    for path in sorted(ASSETS_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in supported_suffixes:
            continue

        normalized_name = path.stem.lower().replace("-", "").replace("_", "")
        if any(
            keyword.lower().replace("-", "").replace("_", "") in normalized_name
            for keyword in keywords
        ):
            return path

    return None


def _image_mime_type(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"

    return "application/octet-stream"


def _render_system_status(
    runtime: Any | None,
    workspace_registry: Any | None,
) -> str:
    runtime_status = _resolve_runtime_status(runtime)
    workspace_status = _resolve_workspace_status(workspace_registry)

    return f"""
    <section class="pp-shell-status" aria-label="系統狀態">
        <div class="pp-shell-status-item">
            <span>系統狀態</span>
            <strong>{escape(runtime_status)}</strong>
        </div>
        <div class="pp-shell-status-item">
            <span>工作區</span>
            <strong>{escape(workspace_status)}</strong>
        </div>
    </section>
    """


def _resolve_runtime_status(runtime: Any | None) -> str:
    if runtime is None:
        return "系統上線"

    for attribute in (
        "operating_status",
        "status",
        "runtime_status",
        "health",
    ):
        value = getattr(runtime, attribute, None)
        if value not in (None, ""):
            return str(value)

    return "系統上線"


def _resolve_workspace_status(workspace_registry: Any | None) -> str:
    if workspace_registry is None:
        return "2 個入口"

    for attribute in ("routes", "workspaces", "items"):
        value = getattr(workspace_registry, attribute, None)
        count = _safe_count(value)
        if count is not None:
            return f"{count} 個入口"

    try:
        count = len(workspace_registry)
    except (TypeError, AttributeError):
        count = None

    if count is not None:
        return f"{count} 個入口"

    return "2 個入口"


def _safe_count(value: Any) -> int | None:
    if value is None or isinstance(value, (str, bytes)):
        return None

    try:
        return len(value)
    except (TypeError, AttributeError):
        return None


def _load_enterprise_design_system() -> None:
    """
    載入 v3 唯一 Design System。

    使用 cache_data 避免每次 rerun 重複讀取磁碟，
    但仍讓 Streamlit 在每個頁面輸出必要的 style 標籤。
    """

    css = _read_enterprise_css()

    if not css:
        st.warning(
            "找不到 assets/enterprise.css，PetPulse v3 Design System 尚未載入。"
        )
        return

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _read_enterprise_css() -> str:
    try:
        return ENTERPRISE_CSS_FILE.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


__all__ = [
    "render_platform",
    "render_shared_sidebar_brand_and_navigation",
]
