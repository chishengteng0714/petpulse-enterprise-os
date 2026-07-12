import streamlit as st

from modules.evidence_center.engine.session import ensure_engine_runtime
from modules.evidence_center.investigation_os.ui.action_panel import (
    render_action_panel,
)
from modules.evidence_center.investigation_os.ui.flow_panel import (
    render_flow_panel,
)
from modules.evidence_center.investigation_os.ui.graph_canvas import (
    render_graph_canvas,
)
from modules.evidence_center.investigation_os.ui.runtime_panel import (
    render_runtime_panel,
)


def _ensure_engine_runtime(evidence_items):
    """
    Migration Sprint A-5

    Investigation OS Workspace 不再建立自己的 Kernel。
    不再建立 Investigation OS Runtime。
    不再透過 EngineKernelAdapter 橋接。

    Single Source of Truth:
    Evidence Center Engine Runtime
    """

    return ensure_engine_runtime(evidence_items)


def render_investigation_os_workspace(evidence_items):
    """
    Investigation OS Workspace

    Migration 後定位：
    - 這裡只是一個 legacy UI shell
    - Runtime 來自 Evidence Center Engine
    - Graph / Action / Flow 全部吃同一個 Engine Runtime
    - 不建立第二套 Runtime
    - 不建立 Investigation OS Kernel
    """

    engine_runtime = _ensure_engine_runtime(evidence_items)

    st.markdown("# Investigation OS v2")
    st.caption(
        "Legacy UI Shell。此頁面已改由 Evidence Center Engine Runtime 驅動，Engine 是唯一資料來源。"
    )

    if engine_runtime is None:
        st.error("找不到 Evidence Center Engine Runtime。")
        return

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Graph Canvas",
            "Action Panel",
            "Flow Panel",
            "Runtime Panel",
        ]
    )

    with tab1:
        render_graph_canvas(
            evidence_items=evidence_items,
            runtime=engine_runtime,
            kernel=None,
        )

    with tab2:
        render_action_panel(
            evidence_items=evidence_items,
            runtime=engine_runtime,
            kernel=None,
        )

    with tab3:
        render_flow_panel(
            evidence_items=evidence_items,
            runtime=engine_runtime,
            kernel=None,
        )

    with tab4:
        render_runtime_panel(
            evidence_items=evidence_items,
            runtime=engine_runtime,
            kernel=None,
        )


def render(evidence_items):
    """
    保留 render() 入口，避免舊頁面 import 爆掉。
    """

    render_investigation_os_workspace(evidence_items)