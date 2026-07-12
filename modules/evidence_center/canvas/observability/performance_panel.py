import time

import streamlit as st


PERFORMANCE_CHECKS = [
    {
        "name": "Nodes Load",
        "method": "get_nodes",
        "description": "檢查 Runtime 載入 Nodes 的耗時。",
    },
    {
        "name": "Edges Load",
        "method": "get_edges",
        "description": "檢查 Runtime 載入 Edges 的耗時。",
    },
    {
        "name": "Actions Load",
        "method": "get_actions",
        "description": "檢查 Runtime 載入 Actions 的耗時。",
    },
    {
        "name": "Flows Load",
        "method": "get_flows",
        "description": "檢查 Runtime 載入 Flows 的耗時。",
    },
    {
        "name": "Summary Load",
        "method": "get_summary",
        "description": "檢查 Runtime 載入 Summary 的耗時。",
    },
    {
        "name": "Selected Object Load",
        "method": "get_selected_object",
        "description": "檢查 Runtime 取得 Selected Object 的耗時。",
    },
    {
        "name": "Event Log Load",
        "method": "get_event_log",
        "description": "檢查 Runtime 取得 Event Log 的耗時。",
    },
]


def render_performance_panel(runtime):
    """
    Performance Observability Panel

    檢查 Runtime API 的基本讀取效能。
    此 Panel 不做壓力測試，只提供開發階段的可觀測基準。
    """

    st.subheader("Performance Snapshot")
    st.caption(
        "檢查 Canvas Runtime 主要 API 的讀取耗時，"
        "協助觀察 Runtime、Presentation Layer 與 Debug Center 的基本效能狀態。"
    )

    performance_results = [_measure_api_call(runtime, check) for check in PERFORMANCE_CHECKS]

    total = len(performance_results)
    available = len([item for item in performance_results if item["status"] == "Available"])
    unavailable = len([item for item in performance_results if item["status"] == "Unavailable"])
    slow = len([item for item in performance_results if item["level"] == "Slow"])

    average_ms = _calculate_average_ms(performance_results)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Checks", total)

    with col2:
        st.metric("Available", available)

    with col3:
        st.metric("Unavailable", unavailable)

    with col4:
        st.metric("Avg Latency", f"{average_ms} ms")

    if slow > 0:
        st.warning(f"偵測到 {slow} 個較慢的 Runtime API。")
    else:
        st.success("Runtime API latency looks healthy.")

    st.divider()

    for result in performance_results:
        _render_performance_card(result)

    st.divider()

    _render_performance_snapshot(performance_results)


def _measure_api_call(runtime, check):
    method_name = check["method"]
    method = getattr(runtime, method_name, None)

    if not callable(method):
        return {
            **check,
            "status": "Unavailable",
            "level": "Unavailable",
            "latency_ms": None,
            "result_size": None,
            "message": "API method not found or not callable.",
        }

    started_at = time.perf_counter()

    try:
        result = method()
        ended_at = time.perf_counter()

        latency_ms = round((ended_at - started_at) * 1000, 2)

        return {
            **check,
            "status": "Available",
            "level": _classify_latency(latency_ms),
            "latency_ms": latency_ms,
            "result_size": _safe_len(result),
            "message": "API call completed.",
        }

    except Exception as error:
        ended_at = time.perf_counter()

        latency_ms = round((ended_at - started_at) * 1000, 2)

        return {
            **check,
            "status": "Error",
            "level": "Error",
            "latency_ms": latency_ms,
            "result_size": None,
            "message": str(error),
        }


def _classify_latency(latency_ms):
    if latency_ms < 50:
        return "Fast"

    if latency_ms < 200:
        return "Normal"

    return "Slow"


def _calculate_average_ms(results):
    latencies = [
        item["latency_ms"]
        for item in results
        if isinstance(item.get("latency_ms"), (int, float))
    ]

    if not latencies:
        return 0

    return round(sum(latencies) / len(latencies), 2)


def _render_performance_card(result):
    icon = {
        "Fast": "✅",
        "Normal": "🟡",
        "Slow": "⚠️",
        "Unavailable": "⚪",
        "Error": "❌",
    }.get(result["level"], "ℹ️")

    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"### {icon} {result['name']}")
            st.caption(result["description"])
            st.code(result["method"], language="text")

        with col2:
            st.metric(
                "Latency",
                "-" if result["latency_ms"] is None else f"{result['latency_ms']} ms",
            )

        with col3:
            st.metric(
                "Size",
                "-" if result["result_size"] is None else result["result_size"],
            )

        if result["status"] == "Error":
            st.error(result["message"])
        elif result["status"] == "Unavailable":
            st.warning(result["message"])
        else:
            st.caption(result["message"])


def _render_performance_snapshot(results):
    st.subheader("Performance Result JSON")
    st.caption("提供 Debug 與後續 Technical Debt 追蹤使用。")

    snapshot = {
        "overall_status": _get_overall_status(results),
        "checks": [
            {
                "name": item["name"],
                "method": item["method"],
                "status": item["status"],
                "level": item["level"],
                "latency_ms": item["latency_ms"],
                "result_size": item["result_size"],
            }
            for item in results
        ],
    }

    st.json(snapshot)


def _get_overall_status(results):
    if any(item["status"] == "Error" for item in results):
        return "Error"

    if any(item["level"] == "Slow" for item in results):
        return "Degraded"

    if any(item["status"] == "Unavailable" for item in results):
        return "Partial"

    return "Healthy"


def _safe_len(value):
    try:
        return len(value)
    except Exception:
        return 1 if value is not None else 0