from __future__ import annotations

from modules.platform.home.enterprise_home import render_enterprise_home
from modules.platform.home.product_experience import (
    build_enterprise_home_experience,
)
from modules.platform.platform_frame import (
    render_shared_sidebar_brand_and_navigation,
)
from modules.platform.runtime import create_platform_runtime
from modules.platform.theme import apply_petpulse_enterprise_theme
from modules.platform.workspace_registry import create_workspace_registry


def render_platform() -> None:
    """
    PetPulse Enterprise OS Platform Shell.

    Frozen Architecture:
    - Runtime 建立方式不變。
    - Workspace Registry 建立方式不變。
    - Home Experience 建立方式不變。
    - Enterprise Home Renderer 不變。
    - 本檔只負責 Presentation Shell 組裝。
    """

    apply_petpulse_enterprise_theme()

    runtime = create_platform_runtime()
    workspace_registry = create_workspace_registry()
    experience = build_enterprise_home_experience()

    render_shared_sidebar_brand_and_navigation(
        active_page="home",
        runtime=runtime,
        workspace_registry=workspace_registry,
        experience=experience,
    )

    render_enterprise_home(runtime)


__all__ = [
    "render_platform",
]
