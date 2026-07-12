import streamlit as st


RUNTIME_CONTRACTS = [
    {
        "name": "Runtime Core Contract",
        "description": "Runtime 必須提供 Evidence Center 核心資料讀取能力。",
        "required_methods": [
            "get_nodes",
            "get_edges",
            "get_actions",
            "get_flows",
            "get_summary",
        ],
    },
    {
        "name": "Canvas Selection Contract",
        "description": "Canvas 必須提供統一選取物件 API，讓所有 Layer 不直接碰資料結構。",
        "required_methods": [
            "get_selected_object",
            "get_selected_node",
            "get_selected_edge",
            "select_object",
            "clear_selection",
        ],
    },
    {
        "name": "Canvas View Contract",
        "description": "Canvas 必須提供 View Mode 與 Layout Mode 控制能力。",
        "required_methods": [
            "get_view_mode",
            "set_view_mode",
            "get_layout_mode",
            "set_layout_mode",
        ],
    },
    {
        "name": "Canvas Event Contract",
        "description": "Canvas 必須提供 Event Bus 與 Event Log 觀測能力。",
        "required_methods": [
            "emit_event",
            "get_event_log",
            "clear_event_log",
        ],
    },
    {
        "name": "Canvas Panel State Contract",
        "description": "Canvas 必須提供 Panel State 讀寫能力，支援可維護的 UI 狀態管理。",
        "required_methods": [
            "get_panel_state",
            "set_panel_state",
        ],
    },
    {
        "name": "Observability Contract",
        "description": "Runtime 應提供 Snapshot 能力，支援 Debug Center 與 Enterprise Observability。",
        "required_methods": [
            "get_runtime_snapshot",
            "get_session_snapshot",
            "get_context_snapshot",
            "get_event_snapshot",
            "get_performance_snapshot",
        ],
    },
]


def render_contract_panel(runtime):
    """
    Runtime Contract Observability Panel

    Contract Panel 負責檢查 Runtime 是否符合企業級平台契約。
    與 API Panel 不同：
    - API Panel 偏向目前有哪些 API 可用
    - Contract Panel 偏向 Runtime 是否符合架構承諾
    """

    st.subheader("Runtime Contracts")
    st.caption(
        "檢查 Canvas Runtime 是否符合 Enterprise Observability Platform 所需的架構契約。"
    )

    contract_results = [_inspect_contract(runtime, contract) for contract in RUNTIME_CONTRACTS]

    total = len(contract_results)
    passed = len([item for item in contract_results if item["status"] == "Passed"])
    degraded = len([item for item in contract_results if item["status"] == "Degraded"])
    failed = len([item for item in contract_results if item["status"] == "Failed"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Contracts", total)

    with col2:
        st.metric("Passed", passed)

    with col3:
        st.metric("Degraded", degraded)

    with col4:
        st.metric("Failed", failed)

    st.divider()

    for result in contract_results:
        _render_contract_card(result)

    st.divider()

    _render_contract_summary(contract_results)


def _inspect_contract(runtime, contract):
    required_methods = contract["required_methods"]
    available_methods = []
    missing_methods = []

    for method_name in required_methods:
        method = getattr(runtime, method_name, None)

        if callable(method):
            available_methods.append(method_name)
        else:
            missing_methods.append(method_name)

    if not missing_methods:
        status = "Passed"
    elif available_methods:
        status = "Degraded"
    else:
        status = "Failed"

    return {
        **contract,
        "status": status,
        "available_methods": available_methods,
        "missing_methods": missing_methods,
        "coverage": _calculate_coverage(available_methods, required_methods),
    }


def _calculate_coverage(available_methods, required_methods):
    if not required_methods:
        return 100

    return round((len(available_methods) / len(required_methods)) * 100)


def _render_contract_card(result):
    status_icon = {
        "Passed": "✅",
        "Degraded": "⚠️",
        "Failed": "❌",
    }.get(result["status"], "ℹ️")

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {status_icon} {result['name']}")
            st.caption(result["description"])

        with col2:
            st.metric("Coverage", f"{result['coverage']}%")
            st.caption(result["status"])

        if result["available_methods"]:
            st.markdown("**Available Methods**")
            st.success(", ".join(result["available_methods"]))

        if result["missing_methods"]:
            st.markdown("**Missing Methods**")
            st.warning(", ".join(result["missing_methods"]))


def _render_contract_summary(contract_results):
    st.subheader("Contract Summary")

    summary = {
        "overall_status": _get_overall_status(contract_results),
        "contracts": [
            {
                "name": item["name"],
                "status": item["status"],
                "coverage": item["coverage"],
                "missing_methods": item["missing_methods"],
            }
            for item in contract_results
        ],
    }

    st.json(summary)


def _get_overall_status(contract_results):
    if any(item["status"] == "Failed" for item in contract_results):
        return "Failed"

    if any(item["status"] == "Degraded" for item in contract_results):
        return "Degraded"

    return "Healthy"