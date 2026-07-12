import streamlit as st

from modules.evidence_center.engine.session import ensure_engine_runtime


def _safe_get(obj, key, default=None):
    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def _safe_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, dict):
        return list(value.values())

    return []


def _resolve_engine_runtime(evidence_items=None, runtime=None):
    if runtime is not None:
        return runtime

    try:
        if evidence_items is not None:
            return ensure_engine_runtime(evidence_items)

        return ensure_engine_runtime()

    except TypeError:
        return ensure_engine_runtime()


def _get_runtime_summary(runtime):
    if runtime is None:
        return {}

    if hasattr(runtime, "get_summary"):
        summary = runtime.get_summary()
        if isinstance(summary, dict):
            return summary

    return {
        "runtime": _safe_get(runtime, "name", "Evidence Center Runtime"),
        "version": _safe_get(runtime, "version", "Engine Runtime"),
        "status": _safe_get(runtime, "status", "Active"),
        "evidence_count": len(_get_evidence_items(runtime)),
        "node_count": len(_get_nodes(runtime)),
        "edge_count": len(_get_edges(runtime)),
        "action_count": len(_get_actions(runtime)),
        "flow_count": len(_get_flows(runtime)),
    }


def _get_evidence_items(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_evidence_items"):
        return _safe_list(runtime.get_evidence_items())

    return _safe_list(_safe_get(runtime, "evidence_items", []))


def _get_nodes(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_nodes"):
        return _safe_list(runtime.get_nodes())

    graph = _safe_get(runtime, "graph")
    graph_engine = _safe_get(runtime, "graph_engine")

    if graph is None:
        graph = _safe_get(graph_engine, "graph")

    return _safe_list(_safe_get(graph, "nodes", []))


def _get_edges(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_edges"):
        return _safe_list(runtime.get_edges())

    graph = _safe_get(runtime, "graph")
    graph_engine = _safe_get(runtime, "graph_engine")

    if graph is None:
        graph = _safe_get(graph_engine, "graph")

    return _safe_list(_safe_get(graph, "edges", []))


def _get_actions(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_actions"):
        return _safe_list(runtime.get_actions())

    action_engine = _safe_get(runtime, "action_engine")
    return _safe_list(_safe_get(action_engine, "actions", []))


def _get_flows(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_flows"):
        return _safe_list(runtime.get_flows())

    flow_engine = _safe_get(runtime, "flow_engine")
    return _safe_list(_safe_get(flow_engine, "flows", []))


def _runtime_name(runtime):
    return (
        _safe_get(runtime, "name")
        or _safe_get(runtime, "runtime_name")
        or "Evidence Center Runtime"
    )


def _runtime_version(runtime):
    return (
        _safe_get(runtime, "version")
        or _safe_get(runtime, "runtime_version")
        or "Engine Runtime"
    )


def _runtime_status(runtime):
    return (
        _safe_get(runtime, "status")
        or _safe_get(runtime, "state")
        or "Active"
    )


def _runtime_metadata(runtime):
    return (
        _safe_get(runtime, "metadata")
        or _safe_get(runtime, "context")
        or {}
    )


def _render_runtime_summary(runtime):
    summary = _get_runtime_summary(runtime)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Evidence", summary.get("evidence_count", 0))

    with col2:
        st.metric("Nodes", summary.get("node_count", 0))

    with col3:
        st.metric("Edges", summary.get("edge_count", 0))

    with col4:
        st.metric("Actions", summary.get("action_count", 0))

    with col5:
        st.metric("Flows", summary.get("flow_count", 0))


def _render_runtime_identity(runtime):
    st.markdown("### Runtime Identity")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("Runtime")
            st.write(_runtime_name(runtime))

        with col2:
            st.caption("Version")
            st.write(_runtime_version(runtime))

        with col3:
            st.caption("Status")
            st.write(_runtime_status(runtime))


def _render_engine_components(runtime):
    st.markdown("### Engine Components")

    rows = [
        {
            "Component": "Graph API",
            "Status": "Active" if hasattr(runtime, "get_nodes") else "Fallback",
            "Source": "runtime.get_nodes() / runtime.get_edges()",
        },
        {
            "Component": "Action API",
            "Status": "Active" if hasattr(runtime, "get_actions") else "Fallback",
            "Source": "runtime.get_actions()",
        },
        {
            "Component": "Flow API",
            "Status": "Active" if hasattr(runtime, "get_flows") else "Fallback",
            "Source": "runtime.get_flows()",
        },
        {
            "Component": "Summary API",
            "Status": "Active" if hasattr(runtime, "get_summary") else "Fallback",
            "Source": "runtime.get_summary()",
        },
    ]

    st.dataframe(rows, width="stretch", hide_index=True)


def _render_runtime_metadata(runtime):
    metadata = _runtime_metadata(runtime)

    st.markdown("### Runtime Metadata")

    if metadata:
        st.json(metadata)
    else:
        st.caption("目前 Runtime 尚未提供 metadata。")


def _render_runtime_summary_json(runtime):
    st.markdown("### Runtime Summary")

    summary = _get_runtime_summary(runtime)

    if summary:
        st.json(summary)
    else:
        st.caption("目前 Runtime 尚未提供 summary。")


def _render_session_state_debug(current_runtime):
    st.markdown("### Session Runtime Keys")

    runtime_keys = []

    for key in st.session_state.keys():
        if "runtime" in key.lower() or "engine" in key.lower():
            runtime_keys.append(key)

    if not runtime_keys:
        st.caption("Session State 中尚未找到 runtime / engine 相關 key。")
        return

    rows = []

    for key in runtime_keys:
        value = st.session_state.get(key)

        rows.append(
            {
                "Session Key": key,
                "Type": type(value).__name__,
                "Is Current Runtime": value is current_runtime,
            }
        )

    st.dataframe(rows, width="stretch", hide_index=True)


def render_runtime_panel(evidence_items=None, runtime=None, kernel=None):
    """
    Evidence Center Runtime Panel

    A-5.5 Step 5-4:
    - 優先使用 Runtime API
    - runtime.get_summary()
    - runtime.get_nodes()
    - runtime.get_edges()
    - runtime.get_actions()
    - runtime.get_flows()
    - Investigation OS Kernel 保留參數但不使用
    """

    st.markdown("## Runtime Panel")
    st.caption(
        "由 Evidence Center Runtime API 驅動畫面。Runtime Panel 只呈現目前 Engine 狀態。"
    )

    engine_runtime = _resolve_engine_runtime(
        evidence_items=evidence_items,
        runtime=runtime,
    )

    if engine_runtime is None:
        st.error("找不到 Evidence Center Engine Runtime。")
        return

    _render_runtime_summary(engine_runtime)

    st.divider()

    _render_runtime_identity(engine_runtime)

    st.divider()

    _render_engine_components(engine_runtime)

    st.divider()

    _render_runtime_summary_json(engine_runtime)

    st.divider()

    _render_runtime_metadata(engine_runtime)

    st.divider()

    with st.expander("Debug Session State"):
        _render_session_state_debug(engine_runtime)