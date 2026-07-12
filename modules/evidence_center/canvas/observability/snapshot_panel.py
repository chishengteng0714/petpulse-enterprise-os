import streamlit as st

from modules.evidence_center.canvas.observability.service import (
    create_observability_service,
)


def render_snapshot_panel(runtime):
    """
    Enterprise Observability Snapshot Panel

    顯示由 ObservabilityService 產生的完整平台觀測快照。
    此 Panel 是未來 Executive Briefing、Strategy Center、
    Multi-Agent Runtime 可共用的狀態入口。
    """

    st.subheader("Enterprise Observability Snapshot")
    st.caption(
        "集中顯示 Canvas Runtime 的健康狀態、技術債與是否需要處理的判斷。"
    )

    snapshot = _get_safe_snapshot(runtime)

    _render_service_status(snapshot)
    st.divider()

    _render_snapshot_status(snapshot)
    st.divider()

    _render_snapshot_metrics(snapshot)
    st.divider()

    _render_snapshot_sections(snapshot)
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


def _render_snapshot_status(snapshot):
    overall_status = snapshot.get("overall_status", "Unknown")
    requires_attention = snapshot.get("requires_attention", False)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Overall Status", overall_status)

    with col2:
        st.metric("Technical Debt", snapshot.get("technical_debt_total", 0))

    with col3:
        st.metric(
            "Requires Attention",
            "Yes" if requires_attention else "No",
        )

    if requires_attention:
        st.warning(
            "此 Snapshot 顯示目前 Observability 需要處理。"
            "請優先查看 Technical Debt、Contracts 與 Performance。"
        )
    else:
        st.success("此 Snapshot 顯示目前 Observability 狀態穩定。")


def _render_snapshot_metrics(snapshot):
    health_summary = snapshot.get("health_summary", {})
    metrics = health_summary.get("metrics", {})

    st.markdown("### Runtime Metrics")

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


def _render_snapshot_sections(snapshot):
    health_summary = snapshot.get("health_summary", {})
    technical_debt = snapshot.get("technical_debt", {})

    col1, col2 = st.columns(2)

    with col1:
        _render_health_summary_section(health_summary)

    with col2:
        _render_technical_debt_section(technical_debt)


def _render_health_summary_section(health_summary):
    st.markdown("### Health Summary")

    with st.container(border=True):
        st.metric("Runtime", health_summary.get("runtime_status", "Unknown"))
        st.metric("API", health_summary.get("api_status", "Unknown"))
        st.metric("Contracts", health_summary.get("contract_status", "Unknown"))
        st.metric("Performance", health_summary.get("performance_status", "Unknown"))

        summary = health_summary.get("summary")
        if summary:
            st.caption(summary)

        service_error = health_summary.get("service_error")
        if service_error:
            st.error(service_error)


def _render_technical_debt_section(technical_debt):
    st.markdown("### Technical Debt")

    with st.container(border=True):
        st.metric("Total", technical_debt.get("total", 0))
        st.metric("Critical", technical_debt.get("critical", 0))
        st.metric("High", technical_debt.get("high", 0))
        st.metric("Medium", technical_debt.get("medium", 0))
        st.metric("Low", technical_debt.get("low", 0))

        service_error = technical_debt.get("service_error")
        if service_error:
            st.error(service_error)

        items = technical_debt.get("items", [])

        if not items:
            st.caption("No technical debt detected.")
            return

        st.caption("Top detected debt items:")

        for item in items[:5]:
            st.warning(
                f"{item.get('severity', 'Unknown')} · "
                f"{item.get('category', 'Unknown')} · "
                f"{item.get('title', 'Untitled')}"
            )


def _render_snapshot_json(snapshot):
    with st.expander("Snapshot JSON", expanded=False):
        st.json(snapshot)