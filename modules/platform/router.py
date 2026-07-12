import streamlit as st

from modules.platform.runtime import PlatformRuntime
from modules.platform.workspace_registry import WorkspaceRegistry


class PlatformRouter:
    """
    Resolve and render the active platform workspace.

    The router reads the active workspace from PlatformRuntime,
    validates it through WorkspaceRegistry, and renders the matched workspace.
    """

    def __init__(
        self,
        runtime: PlatformRuntime,
        registry: WorkspaceRegistry,
    ):
        self.runtime = runtime
        self.registry = registry

    def get_active_workspace(self):
        active_key = self.runtime.get_active_workspace_key()

        if not self.registry.exists(active_key):
            enabled_workspaces = self.registry.list_enabled()
            fallback_key = (
                enabled_workspaces[0].key
                if enabled_workspaces
                else "enterprise_home"
            )
            self.runtime.set_active_workspace_key(fallback_key)
            active_key = fallback_key

        return self.registry.get(active_key)

    def render_active_workspace(self):
        workspace = self.get_active_workspace()

        if workspace is None:
            st.error("找不到目前啟用的工作區。")
            return

        if workspace.renderer is None:
            self._render_product_placeholder(workspace)
            return

        workspace.renderer()

    def _render_product_placeholder(self, workspace):
        st.markdown(f"# {workspace.icon} {workspace.label}")
        st.caption(workspace.description)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("工作區狀態", "已註冊")

        with col2:
            st.metric("頁面渲染", "待連接")

        with col3:
            st.metric("工作區群組", workspace.group)

        st.info(
            "此工作區已完成 Platform Layer 註冊。"
            "正式頁面將依照產品路線逐步接上。"
        )

        st.markdown("## 工作區目的")
        st.write(workspace.description)

        st.markdown("## 下一個里程碑")
        st.write("透過 Workspace Registry 連接正式工作區頁面。")

        with st.expander("開發資訊", expanded=False):
            st.json(
                {
                    "key": workspace.key,
                    "label": workspace.label,
                    "description": workspace.description,
                    "group": workspace.group,
                    "enabled": workspace.enabled,
                    "has_renderer": workspace.renderer is not None,
                }
            )