import streamlit as st


def render_status_metric(label, status):
    if status == "Healthy":
        st.metric(label, "Healthy")
    elif status == "Warning":
        st.metric(label, "Warning")
    else:
        st.metric(label, "Error")


def render_status_badge(status: str):
    if status == "Healthy":
        st.success("Healthy")
    elif status == "Warning":
        st.warning("Warning")
    else:
        st.error("Error")


def render_contract_badge(status: str):
    if status == "Passed":
        st.success("Passed")
    elif status == "Warning":
        st.warning("Warning")
    else:
        st.error("Failed")


def render_json_card(title, payload):
    with st.container(border=True):
        st.markdown(f"### {title}")

        if payload is None:
            st.info("No data available.")
            return

        st.json(payload)


def render_health_section(title, checks):
    st.markdown(f"## {title}")

    if not checks:
        st.info("No runtime checks available.")
        return

    for check in checks:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {check.name}")
                st.caption(check.message)

            with col2:
                render_status_badge(check.status)

            if check.details:
                with st.expander("Details", expanded=False):
                    st.json(check.details)


def calculate_group_status(checks):
    if not checks:
        return "Warning"

    statuses = [check.status for check in checks]

    if "Error" in statuses:
        return "Error"

    if "Warning" in statuses:
        return "Warning"

    return "Healthy"


def calculate_contract_status(contract_report):
    if contract_report.failed > 0:
        return "Error"

    if contract_report.warning > 0:
        return "Warning"

    return "Healthy"


def format_bool(value):
    return "Yes" if value else "No"