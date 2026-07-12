import streamlit as st


RUNTIME_API_CONTRACTS = [
    {
        "group": "Core Runtime",
        "methods": [
            "get_nodes",
            "get_edges",
            "get_actions",
            "get_flows",
            "get_summary",
        ],
    },
    {
        "group": "Canvas Selection",
        "methods": [
            "get_selected_object",
            "get_selected_node",
            "get_selected_edge",
            "select_object",
            "clear_selection",
        ],
    },
    {
        "group": "Canvas View",
        "methods": [
            "get_view_mode",
            "set_view_mode",
            "get_layout_mode",
            "set_layout_mode",
        ],
    },
    {
        "group": "Canvas Events",
        "methods": [
            "emit_event",
            "get_event_log",
            "clear_event_log",
        ],
    },
    {
        "group": "Canvas Panel State",
        "methods": [
            "get_panel_state",
            "set_panel_state",
        ],
    },
]


def render_api_panel(runtime):
    """
    API Observability Panel

    檢查 Canvas Runtime 對外 API 是否存在、是否 callable，
    並提供基本 API Health Snapshot。
    """

    st.subheader("Runtime API Health")
    st.caption(
        "檢查 Canvas Runtime 是否提供穩定 API，"
        "確保 Presentation Layer、Intelligence Layer 與 Observability Layer 能安全存取。"
    )

    api_results = _inspect_runtime_api(runtime)

    total = len(api_results)
    available = len([item for item in api_results if item["status"] == "Available"])
    missing = len([item for item in api_results if item["status"] == "Missing"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("API Checked", total)

    with col2:
        st.metric("Available", available)

    with col3:
        st.metric("Missing", missing)

    st.divider()

    for contract in RUNTIME_API_CONTRACTS:
        _render_api_group(contract["group"], api_results)

    st.divider()

    _render_api_snapshot(runtime)


def _inspect_runtime_api(runtime):
    results = []

    for contract in RUNTIME_API_CONTRACTS:
        for method_name in contract["methods"]:
            method = getattr(runtime, method_name, None)

            if callable(method):
                status = "Available"
                message = "Callable API method."
            else:
                status = "Missing"
                message = "API method not found or not callable."

            results.append(
                {
                    "group": contract["group"],
                    "method": method_name,
                    "status": status,
                    "message": message,
                }
            )

    return results


def _render_api_group(group_name, api_results):
    group_items = [item for item in api_results if item["group"] == group_name]

    available = len([item for item in group_items if item["status"] == "Available"])
    total = len(group_items)

    with st.container(border=True):
        st.markdown(f"### {group_name}")
        st.caption(f"{available}/{total} API methods available")

        for item in group_items:
            if item["status"] == "Available":
                st.success(f"✅ {item['method']}")
            else:
                st.warning(f"⚠️ {item['method']} - {item['message']}")


def _render_api_snapshot(runtime):
    st.subheader("API Snapshot")
    st.caption("以安全方式讀取目前 Runtime 對外資料。")

    snapshot = {
        "nodes": _safe_len(_safe_call(runtime, "get_nodes", [])),
        "edges": _safe_len(_safe_call(runtime, "get_edges", [])),
        "actions": _safe_len(_safe_call(runtime, "get_actions", [])),
        "flows": _safe_len(_safe_call(runtime, "get_flows", [])),
        "summary_available": _safe_call(runtime, "get_summary") is not None,
        "selected_object_available": _safe_call(runtime, "get_selected_object") is not None,
        "event_log_size": _safe_len(_safe_call(runtime, "get_event_log", [])),
    }

    st.json(snapshot)


def _safe_call(runtime, method_name, default=None):
    if runtime is None:
        return default

    method = getattr(runtime, method_name, None)

    if not callable(method):
        return default

    try:
        return method()
    except Exception:
        return default


def _safe_len(value):
    try:
        return len(value)
    except Exception:
        return 0