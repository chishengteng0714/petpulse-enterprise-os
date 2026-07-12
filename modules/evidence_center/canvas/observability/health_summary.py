"""
Observability Health Summary

集中產生 Canvas Runtime 的 Enterprise Health Summary。

此模組只負責資料整理，不負責 Streamlit UI。
"""

import time

from modules.evidence_center.canvas.observability.models import (
    HealthDetail,
    HealthStatus,
    HealthSummary,
    PerformanceCheckResult,
    RuntimeMetrics,
)


RUNTIME_CORE_METHODS = [
    "get_nodes",
    "get_edges",
    "get_actions",
    "get_flows",
    "get_summary",
]

SELECTION_METHODS = [
    "get_selected_object",
    "get_selected_node",
    "get_selected_edge",
    "select_object",
    "clear_selection",
]

VIEW_METHODS = [
    "get_view_mode",
    "set_view_mode",
    "get_layout_mode",
    "set_layout_mode",
]

EVENT_METHODS = [
    "emit_event",
    "get_event_log",
    "clear_event_log",
]

OBSERVABILITY_METHODS = [
    "get_runtime_snapshot",
    "get_session_snapshot",
    "get_context_snapshot",
    "get_event_snapshot",
    "get_performance_snapshot",
]


def build_observability_health_summary(runtime):
    """
    建立 Enterprise Observability Health Summary。
    """

    if runtime is None:
        return HealthSummary(
            overall_status=HealthStatus.UNAVAILABLE.value,
            runtime_status=HealthStatus.UNAVAILABLE.value,
            api_status=HealthStatus.UNAVAILABLE.value,
            contract_status=HealthStatus.UNAVAILABLE.value,
            performance_status=HealthStatus.UNAVAILABLE.value,
            summary="Canvas Runtime 尚未初始化。",
            metrics=RuntimeMetrics().to_dict(),
            details={},
        ).to_dict()

    runtime_health = _build_runtime_health(runtime)
    api_health = _build_api_health(runtime)
    contract_health = _build_contract_health(runtime)
    performance_health = _build_performance_health(runtime)

    overall_status = _resolve_overall_status(
        [
            runtime_health.status,
            api_health.status,
            contract_health.status,
            performance_health.status,
        ]
    )

    return HealthSummary(
        overall_status=overall_status,
        runtime_status=runtime_health.status,
        api_status=api_health.status,
        contract_status=contract_health.status,
        performance_status=performance_health.status,
        summary=_build_summary_text(overall_status),
        metrics=runtime_health.metrics,
        details={
            "runtime": runtime_health.to_dict(),
            "api": api_health.to_dict(),
            "contract": contract_health.to_dict(),
            "performance": performance_health.to_dict(),
        },
    ).to_dict()


def _build_runtime_health(runtime):
    nodes = _safe_call(runtime, "get_nodes", [])
    edges = _safe_call(runtime, "get_edges", [])
    actions = _safe_call(runtime, "get_actions", [])
    flows = _safe_call(runtime, "get_flows", [])
    event_log = _safe_call(runtime, "get_event_log", [])

    metrics = RuntimeMetrics(
        nodes=_safe_len(nodes),
        edges=_safe_len(edges),
        actions=_safe_len(actions),
        flows=_safe_len(flows),
        events=_safe_len(event_log),
    )

    has_core_data = any(
        [
            metrics.nodes > 0,
            metrics.edges > 0,
            metrics.actions > 0,
            metrics.flows > 0,
        ]
    )

    status = (
        HealthStatus.HEALTHY.value
        if has_core_data
        else HealthStatus.DEGRADED.value
    )

    return HealthDetail(
        status=status,
        metrics=metrics.to_dict(),
        message=(
            "Runtime core data is available."
            if has_core_data
            else "Runtime initialized, but core data appears empty."
        ),
    )


def _build_api_health(runtime):
    required_methods = (
        RUNTIME_CORE_METHODS
        + SELECTION_METHODS
        + VIEW_METHODS
        + EVENT_METHODS
    )

    available, missing = _inspect_methods(runtime, required_methods)
    status = _resolve_coverage_status(available, required_methods)

    return HealthDetail(
        status=status,
        available=available,
        missing=missing,
        coverage=_calculate_coverage(available, required_methods),
        message=_build_coverage_message(status),
    )


def _build_contract_health(runtime):
    required_methods = (
        RUNTIME_CORE_METHODS
        + SELECTION_METHODS
        + VIEW_METHODS
        + EVENT_METHODS
        + OBSERVABILITY_METHODS
    )

    available, missing = _inspect_methods(runtime, required_methods)
    status = _resolve_coverage_status(available, required_methods)

    return HealthDetail(
        status=status,
        available=available,
        missing=missing,
        coverage=_calculate_coverage(available, required_methods),
        message=_build_coverage_message(status),
    )


def _build_performance_health(runtime):
    checks = [
        "get_nodes",
        "get_edges",
        "get_actions",
        "get_flows",
        "get_summary",
        "get_selected_object",
        "get_event_log",
    ]

    results = []

    for method_name in checks:
        method = getattr(runtime, method_name, None)

        if not callable(method):
            results.append(
                PerformanceCheckResult(
                    method=method_name,
                    status=HealthStatus.UNAVAILABLE.value,
                    latency_ms=None,
                ).to_dict()
            )
            continue

        started_at = time.perf_counter()

        try:
            method()
            ended_at = time.perf_counter()

            results.append(
                PerformanceCheckResult(
                    method=method_name,
                    status="Available",
                    latency_ms=round((ended_at - started_at) * 1000, 2),
                ).to_dict()
            )

        except Exception:
            ended_at = time.perf_counter()

            results.append(
                PerformanceCheckResult(
                    method=method_name,
                    status=HealthStatus.ERROR.value,
                    latency_ms=round((ended_at - started_at) * 1000, 2),
                ).to_dict()
            )

    if any(item["status"] == HealthStatus.ERROR.value for item in results):
        status = HealthStatus.ERROR.value
    elif any(item["latency_ms"] and item["latency_ms"] >= 200 for item in results):
        status = HealthStatus.DEGRADED.value
    elif any(item["status"] == HealthStatus.UNAVAILABLE.value for item in results):
        status = HealthStatus.PARTIAL.value
    else:
        status = HealthStatus.HEALTHY.value

    return HealthDetail(
        status=status,
        average_latency_ms=_calculate_average_latency(results),
        results=results,
        message=_build_performance_message(status),
    )


def _inspect_methods(runtime, required_methods):
    available = []
    missing = []

    for method_name in required_methods:
        method = getattr(runtime, method_name, None)

        if callable(method):
            available.append(method_name)
        else:
            missing.append(method_name)

    return available, missing


def _resolve_coverage_status(available, required):
    if not required:
        return HealthStatus.HEALTHY.value

    if len(available) == len(required):
        return HealthStatus.HEALTHY.value

    if len(available) > 0:
        return HealthStatus.DEGRADED.value

    return HealthStatus.FAILED.value


def _resolve_overall_status(statuses):
    if any(
        status
        in [
            HealthStatus.FAILED.value,
            HealthStatus.ERROR.value,
            HealthStatus.UNAVAILABLE.value,
        ]
        for status in statuses
    ):
        return HealthStatus.CRITICAL.value

    if any(
        status in [HealthStatus.DEGRADED.value, HealthStatus.PARTIAL.value]
        for status in statuses
    ):
        return HealthStatus.DEGRADED.value

    return HealthStatus.HEALTHY.value


def _calculate_coverage(available, required):
    if not required:
        return 100

    return round((len(available) / len(required)) * 100)


def _calculate_average_latency(results):
    latencies = [
        item["latency_ms"]
        for item in results
        if isinstance(item.get("latency_ms"), (int, float))
    ]

    if not latencies:
        return 0

    return round(sum(latencies) / len(latencies), 2)


def _build_summary_text(status):
    if status == HealthStatus.HEALTHY.value:
        return "Canvas Runtime observability is healthy."

    if status == HealthStatus.DEGRADED.value:
        return "Canvas Runtime observability is partially degraded."

    if status == HealthStatus.CRITICAL.value:
        return "Canvas Runtime observability requires attention."

    return "Canvas Runtime observability status is unknown."


def _build_coverage_message(status):
    if status == HealthStatus.HEALTHY.value:
        return "All required methods are available."

    if status == HealthStatus.DEGRADED.value:
        return "Some required methods are missing."

    return "Required methods are unavailable."


def _build_performance_message(status):
    if status == HealthStatus.HEALTHY.value:
        return "Runtime API latency looks healthy."

    if status == HealthStatus.DEGRADED.value:
        return "Some Runtime API calls are slower than expected."

    if status == HealthStatus.PARTIAL.value:
        return "Some Runtime API methods are unavailable."

    if status == HealthStatus.ERROR.value:
        return "Some Runtime API calls failed."

    return "Performance status is unknown."


def _safe_call(runtime, method_name, default=None):
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
        return 1 if value is not None else 0