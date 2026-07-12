import streamlit as st

from modules.evidence_center.canvas.observability.service import (
    create_observability_service,
)


def render_overview_panel(runtime):
    """
    Observability Overview Panel

    Enterprise Observability Center 的總覽面板。
    """

    st.subheader("Enterprise Health Overview")
    st.caption(
        "集中檢查 Canvas Runtime、API、Contracts、Performance 與 Technical Debt 的整體健康狀態。"
    )

    snapshot = _get_safe_snapshot(runtime)

    health_summary = snapshot.get("health_summary", {})
    technical_debt = snapshot.get("technical_debt", {})

    _render_service_status(snapshot)
    st.divider()

    _render_attention_banner(snapshot)
    st.divider()

    _render_overall_status(health_summary)
    st.divider()

    _render_core_metrics(health_summary)
    st.divider()

    _render_health_cards(health_summary)
    st.divider()

    _render_technical_debt_summary(technical_debt)
    st.divider()

    _render_snapshot_json(snapshot)


def _get_safe_snapshot(runtime):
    service = create_observability_service(runtime)
    return service.get_enterprise_snapshot()


def _render_service_status(snapshot):
    service_status = snapshot.get("service_status", "Unknown")

    if service_status == "Healthy":
        st.success("✅ Observability Service：Healthy")
    elif service_status == "Error":
        st.error("❌ Observability Service：Error")
    else:
        st.info(f"ℹ️ Observability Service：{service_status}")


def _render_attention_banner(snapshot):
    requires_attention = snapshot.get("requires_attention", False)

    if requires_attention:
        st.warning(
            "Observability requires attention. "
            "請優先檢查 Critical / High 技術債或 Runtime Contract 缺口。"
        )
    else:
        st.success("Observability is operating within expected range.")


def _render_overall_status(health_summary):
    status = health_summary.get("overall_status", "Unknown")
    summary = health_summary.get("summary", "")

    if status == "Healthy":
        st.success(f"✅ Overall Status：{status}")
    elif status == "Degraded":
        st.warning(f"⚠️ Overall Status：{status}")
    elif status == "Critical":
        st.error(f"❌ Overall Status：{status}")
    else:
        st.info(f"ℹ️ Overall Status：{status}")

    st.caption(summary)

    service_error = health_summary.get("service_error")
    if service_error:
        st.error(service_error)


def _render_core_metrics(health_summary):
    metrics = health_summary.get("metrics", {})

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Nodes", metrics.get("nodes", 0))

    with col2:
        st.metric("Edges", metrics.get("edges", 0))

    with col3:
        st.metric("Actions", metrics.get("actions", 0))

    with col4:
        st.metric("Flows", metrics.get("flows", 0))

    with col5:
        st.metric("Events", metrics.get("events", 0))


def _render_health_cards(health_summary):
    details = health_summary.get("details", {})

    col1, col2 = st.columns(2)

    with col1:
        _render_status_card(
            title="Runtime Health",
            status=health_summary.get("runtime_status", "Unknown"),
            detail=details.get("runtime", {}),
        )

        _render_status_card(
            title="Contract Health",
            status=health_summary.get("contract_status", "Unknown"),
            detail=details.get("contract", {}),
        )

    with col2:
        _render_status_card(
            title="API Health",
            status=health_summary.get("api_status", "Unknown"),
            detail=details.get("api", {}),
        )

        _render_status_card(
            title="Performance Health",
            status=health_summary.get("performance_status", "Unknown"),
            detail=details.get("performance", {}),
        )


def _render_status_card(title, status, detail):
    icon = _get_status_icon(status)

    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.metric("Status", status)

        message = detail.get("message")
        if message:
            st.caption(message)

        if "coverage" in detail:
            st.metric("Coverage", f"{detail.get('coverage', 0)}%")

        if "average_latency_ms" in detail:
            st.metric("Avg Latency", f"{detail.get('average_latency_ms', 0)} ms")

        missing = detail.get("missing", [])
        if missing:
            st.warning("Missing： " + ", ".join(missing))


def _render_technical_debt_summary(technical_debt):
    st.subheader("Technical Debt Registry")
    st.caption("由 Observability Service 自動整理出的技術債清單。")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total", technical_debt.get("total", 0))

    with col2:
        st.metric("Critical", technical_debt.get("critical", 0))

    with col3:
        st.metric("High", technical_debt.get("high", 0))

    with col4:
        st.metric("Medium", technical_debt.get("medium", 0))

    with col5:
        st.metric("Low", technical_debt.get("low", 0))

    service_error = technical_debt.get("service_error")
    if service_error:
        st.error(service_error)

    items = technical_debt.get("items", [])

    if not items:
        st.success("目前沒有偵測到 Observability Technical Debt。")
        return

    for item in items:
        _render_debt_item(item)


def _render_debt_item(item):
    severity = item.get("severity", "Low")
    icon = {
        "Critical": "🚨",
        "High": "❌",
        "Medium": "⚠️",
        "Low": "🟡",
    }.get(severity, "ℹ️")

    with st.container(border=True):
        st.markdown(f"### {icon} {item.get('title', 'Untitled Debt')}")
        st.caption(f"{item.get('category', 'Unknown')} · {severity}")

        st.write(item.get("description", ""))

        recommendation = item.get("recommendation")
        if recommendation:
            st.info(recommendation)

        error = item.get("error")
        if error:
            st.error(error)


def _render_snapshot_json(snapshot):
    with st.expander("Enterprise Observability Snapshot JSON", expanded=False):
        st.json(snapshot)


def _get_status_icon(status):
    return {
        "Healthy": "✅",
        "Degraded": "⚠️",
        "Partial": "🟡",
        "Failed": "❌",
        "Error": "❌",
        "Critical": "🚨",
        "Unavailable": "⚪",
    }.get(status, "ℹ️")