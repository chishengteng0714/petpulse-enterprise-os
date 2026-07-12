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


def _get_flows_from_runtime(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_flows"):
        return _safe_list(runtime.get_flows())

    flow_engine = _safe_get(runtime, "flow_engine")
    flows = _safe_get(flow_engine, "flows", [])

    return _safe_list(flows)


def _flow_id(flow):
    return (
        _safe_get(flow, "flow_id")
        or _safe_get(flow, "id")
        or _safe_get(flow, "key")
        or "unknown_flow"
    )


def _flow_title(flow):
    return (
        _safe_get(flow, "title")
        or _safe_get(flow, "name")
        or _safe_get(flow, "label")
        or _flow_id(flow)
    )


def _flow_description(flow):
    return (
        _safe_get(flow, "description")
        or _safe_get(flow, "summary")
        or _safe_get(flow, "content")
        or "此 Flow 目前尚未提供說明。"
    )


def _flow_type(flow):
    return (
        _safe_get(flow, "flow_type")
        or _safe_get(flow, "type")
        or _safe_get(flow, "category")
        or "Flow"
    )


def _flow_status(flow):
    return (
        _safe_get(flow, "status")
        or _safe_get(flow, "state")
        or "Ready"
    )


def _flow_steps(flow):
    return _safe_list(
        _safe_get(flow, "steps")
        or _safe_get(flow, "nodes")
        or _safe_get(flow, "tasks")
        or []
    )


def _flow_source(flow):
    return (
        _safe_get(flow, "source")
        or _safe_get(flow, "source_id")
        or _safe_get(flow, "evidence_id")
        or "Evidence Engine"
    )


def _step_title(step):
    return (
        _safe_get(step, "title")
        or _safe_get(step, "name")
        or _safe_get(step, "label")
        or _safe_get(step, "id")
        or "Flow Step"
    )


def _step_status(step):
    return (
        _safe_get(step, "status")
        or _safe_get(step, "state")
        or "Pending"
    )


def _render_empty_state():
    st.info(
        "目前 Engine Runtime 尚未產生 Flows。請先確認 Evidence Items 已成功進入 Evidence Center Engine。"
    )


def _render_flow_summary(flows):
    total_count = len(flows)
    ready_count = 0
    running_count = 0
    completed_count = 0

    for flow in flows:
        status = str(_flow_status(flow)).lower()

        if status in ["completed", "complete", "done", "resolved"]:
            completed_count += 1
        elif status in ["running", "active", "in_progress"]:
            running_count += 1
        else:
            ready_count += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Engine Flows", total_count)

    with col2:
        st.metric("Ready", ready_count)

    with col3:
        st.metric("Running", running_count)

    with col4:
        st.metric("Completed", completed_count)


def _render_flow_table(flows):
    st.markdown("### Flow Queue")

    if not flows:
        st.caption("尚無 Flow。")
        return

    rows = []

    for flow in flows:
        rows.append(
            {
                "Flow": _flow_title(flow),
                "Type": _flow_type(flow),
                "Status": _flow_status(flow),
                "Steps": len(_flow_steps(flow)),
                "Source": _flow_source(flow),
            }
        )

    st.dataframe(rows, width="stretch", hide_index=True)


def _render_flow_cards(flows):
    st.markdown("### Flow Detail")

    if not flows:
        st.caption("尚無 Flow Detail。")
        return

    for flow in flows:
        with st.container(border=True):
            st.caption(f"{_flow_type(flow)} · {_flow_status(flow)}")
            st.markdown(f"**{_flow_title(flow)}**")
            st.write(_flow_description(flow))

            col1, col2 = st.columns(2)

            with col1:
                st.caption("Source")
                st.write(_flow_source(flow))

            with col2:
                st.caption("Steps")
                st.write(len(_flow_steps(flow)))

            steps = _flow_steps(flow)

            if steps:
                with st.expander("Flow Steps"):
                    for index, step in enumerate(steps, start=1):
                        st.markdown(
                            f"{index}. **{_step_title(step)}** · {_step_status(step)}"
                        )

            metadata = _safe_get(flow, "metadata", None)

            if metadata:
                with st.expander("Flow Metadata"):
                    st.json(metadata)


def render_flow_panel(evidence_items=None, runtime=None, kernel=None):
    """
    Evidence Center Flow Panel

    A-5.5 Step 5-3:
    - 優先使用 Runtime API
    - runtime.get_flows()
    - 不再猜測 Flow Engine 內部結構作為主要資料來源
    - Investigation OS Kernel 保留參數但不使用
    """

    st.markdown("## Flow Panel")
    st.caption(
        "由 Evidence Center Runtime API 驅動畫面。Flow Panel 只負責呈現，不建立自己的 Flow Queue。"
    )

    engine_runtime = _resolve_engine_runtime(
        evidence_items=evidence_items,
        runtime=runtime,
    )

    if engine_runtime is None:
        st.error("找不到 Evidence Center Engine Runtime。")
        return

    flows = _get_flows_from_runtime(engine_runtime)

    if not flows:
        _render_empty_state()
        return

    _render_flow_summary(flows)

    st.divider()

    _render_flow_table(flows)

    st.divider()

    _render_flow_cards(flows)