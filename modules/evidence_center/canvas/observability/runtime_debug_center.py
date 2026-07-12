import streamlit as st

from modules.evidence_center.canvas.observability.api_panel import (
    render_api_panel,
)
from modules.evidence_center.canvas.observability.context_panel import (
    render_context_panel,
)
from modules.evidence_center.canvas.observability.contract_panel import (
    render_contract_panel,
)
from modules.evidence_center.canvas.observability.overview_panel import (
    render_overview_panel,
)
from modules.evidence_center.canvas.observability.performance_panel import (
    render_performance_panel,
)
from modules.evidence_center.canvas.observability.presenter_panel import (
    render_presenter_panel,
)
from modules.evidence_center.canvas.observability.runtime_panel import (
    render_runtime_panel,
)
from modules.evidence_center.canvas.observability.session_panel import (
    render_session_panel,
)
from modules.evidence_center.canvas.observability.snapshot_panel import (
    render_snapshot_panel,
)
from modules.evidence_center.canvas.observability.timeline_panel import (
    render_timeline_panel,
)


OBSERVABILITY_PANELS = [
    {
        "tab": "Overview",
        "name": "Overview Panel",
        "renderer": render_overview_panel,
        "description": "Canvas Runtime 的總覽觀測。",
    },
    {
        "tab": "Snapshot",
        "name": "Snapshot Panel",
        "renderer": render_snapshot_panel,
        "description": "Enterprise Observability Snapshot 狀態入口。",
    },
    {
        "tab": "Runtime",
        "name": "Runtime Panel",
        "renderer": render_runtime_panel,
        "description": "Runtime 狀態與核心資料觀測。",
    },
    {
        "tab": "Session",
        "name": "Session Panel",
        "renderer": render_session_panel,
        "description": "Streamlit Session 與 Canvas Session 狀態觀測。",
    },
    {
        "tab": "Context",
        "name": "Context Panel",
        "renderer": render_context_panel,
        "description": "Canvas Intelligence Context 狀態觀測。",
    },
    {
        "tab": "Timeline",
        "name": "Timeline Panel",
        "renderer": render_timeline_panel,
        "description": "Timeline Context 與事件序列觀測。",
    },
    {
        "tab": "Presenter",
        "name": "Presenter Panel",
        "renderer": render_presenter_panel,
        "description": "Presentation Presenter Layer 健康狀態觀測。",
    },
    {
        "tab": "API",
        "name": "API Panel",
        "renderer": render_api_panel,
        "description": "Runtime API 可用性觀測。",
    },
    {
        "tab": "Contracts",
        "name": "Contract Panel",
        "renderer": render_contract_panel,
        "description": "Enterprise Runtime Contracts 覆蓋率觀測。",
    },
    {
        "tab": "Performance",
        "name": "Performance Panel",
        "renderer": render_performance_panel,
        "description": "Runtime API 基礎效能觀測。",
    },
]


def render_runtime_debug_center(runtime):
    """
    Runtime Debug Center

    Enterprise Observability Platform 的主要組裝器。

    原則：
    - 不直接承載大量 UI 細節
    - 不直接承載 Runtime 診斷邏輯
    - 每個 Observability Panel 都拆成獨立模組
    - 此檔案只負責組裝與安全渲染
    """

    st.markdown("## Enterprise Observability Center")
    st.caption(
        "Canvas Runtime、Session、Context、Presenter、API、Contract、Performance 與 Snapshot 的集中觀測中心。"
    )

    if runtime is None:
        st.error("Canvas Runtime 尚未初始化。")
        return

    _render_architecture_overview()

    tabs = st.tabs([panel["tab"] for panel in OBSERVABILITY_PANELS])

    for tab, panel in zip(tabs, OBSERVABILITY_PANELS):
        with tab:
            _safe_render_panel(
                panel_name=panel["name"],
                render_function=panel["renderer"],
                runtime=runtime,
                description=panel["description"],
            )


def _render_architecture_overview():
    """
    顯示 Observability 架構總覽。
    """

    with st.expander("Observability Architecture", expanded=False):
        st.markdown(
            """
            ```text
            Canvas Observability

            Runtime Debug Center
                    │
                    ▼
            Observability Panels
                    │
            ┌───────┼────────┬─────────┬──────────┐
            │       │        │         │          │
         Overview Snapshot Runtime   Session   Context
            │       │        │         │          │
            ├───────┴────────┴─────────┴──────────┤
            │                                      │
        Timeline                              Presenter
            │                                      │
          API ───────── Contracts ───────── Performance
            ```
            """
        )

        st.caption(
            "Runtime Debug Center 只負責組裝，所有診斷與顯示邏輯皆由各 Panel 或 Service 負責。"
        )


def _safe_render_panel(panel_name, render_function, runtime, description=""):
    """
    安全渲染 Observability Panel。

    避免單一 Panel 出錯時導致整個 Debug Center 無法使用。
    """

    if description:
        st.caption(description)

    try:
        render_function(runtime)

    except TypeError:
        try:
            render_function()
        except Exception as error:
            _render_panel_error(panel_name, error)

    except Exception as error:
        _render_panel_error(panel_name, error)


def _render_panel_error(panel_name, error):
    st.error(f"{panel_name} failed to render.")
    st.exception(error)