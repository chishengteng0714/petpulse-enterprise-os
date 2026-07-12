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


def _get_actions_from_runtime(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_actions"):
        return _safe_list(runtime.get_actions())

    action_engine = _safe_get(runtime, "action_engine")
    actions = _safe_get(action_engine, "actions", [])

    return _safe_list(actions)


def _action_id(action):
    return (
        _safe_get(action, "action_id")
        or _safe_get(action, "id")
        or _safe_get(action, "key")
        or "unknown_action"
    )


def _action_title(action):
    return (
        _safe_get(action, "title")
        or _safe_get(action, "name")
        or _safe_get(action, "label")
        or _action_id(action)
    )


def _action_description(action):
    return (
        _safe_get(action, "description")
        or _safe_get(action, "summary")
        or _safe_get(action, "content")
        or "此 Action 目前尚未提供說明。"
    )


def _action_type(action):
    return (
        _safe_get(action, "action_type")
        or _safe_get(action, "type")
        or _safe_get(action, "category")
        or "Action"
    )


def _action_status(action):
    return (
        _safe_get(action, "status")
        or _safe_get(action, "state")
        or "Pending"
    )


def _action_priority(action):
    return (
        _safe_get(action, "priority")
        or _safe_get(action, "severity")
        or "Normal"
    )


def _action_source(action):
    return (
        _safe_get(action, "source")
        or _safe_get(action, "source_id")
        or _safe_get(action, "evidence_id")
        or "Evidence Engine"
    )


def _render_empty_state():
    st.info(
        "目前 Engine Runtime 尚未產生 Actions。請先確認 Evidence Items 已成功進入 Evidence Center Engine。"
    )


def _render_action_summary(actions):
    total_count = len(actions)
    pending_count = 0
    running_count = 0
    completed_count = 0

    for action in actions:
        status = str(_action_status(action)).lower()

        if status in ["completed", "complete", "done", "resolved"]:
            completed_count += 1
        elif status in ["running", "active", "in_progress"]:
            running_count += 1
        else:
            pending_count += 1

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Engine Actions", total_count)

    with col2:
        st.metric("Pending", pending_count)

    with col3:
        st.metric("Running", running_count)

    with col4:
        st.metric("Completed", completed_count)


def _render_action_table(actions):
    st.markdown("### Action Queue")

    if not actions:
        st.caption("尚無 Action。")
        return

    rows = []

    for action in actions:
        rows.append(
            {
                "Action": _action_title(action),
                "Type": _action_type(action),
                "Priority": _action_priority(action),
                "Status": _action_status(action),
                "Source": _action_source(action),
            }
        )

    st.dataframe(rows, width="stretch", hide_index=True)


def _render_action_cards(actions):
    st.markdown("### Action Detail")

    if not actions:
        st.caption("尚無 Action Detail。")
        return

    for action in actions:
        with st.container(border=True):
            st.caption(f"{_action_type(action)} · {_action_priority(action)}")
            st.markdown(f"**{_action_title(action)}**")
            st.write(_action_description(action))

            col1, col2 = st.columns(2)

            with col1:
                st.caption("Status")
                st.write(_action_status(action))

            with col2:
                st.caption("Source")
                st.write(_action_source(action))

            metadata = _safe_get(action, "metadata", None)

            if metadata:
                with st.expander("Action Metadata"):
                    st.json(metadata)


def render_action_panel(evidence_items=None, runtime=None, kernel=None):
    """
    Evidence Center Action Panel

    A-5.5 Step 5-2:
    - 優先使用 Runtime API
    - runtime.get_actions()
    - 不再猜測 Action Engine 內部結構作為主要資料來源
    - Investigation OS Kernel 保留參數但不使用
    """

    st.markdown("## Action Panel")
    st.caption(
        "由 Evidence Center Runtime API 驅動畫面。Action Panel 只負責呈現，不建立自己的 Action Queue。"
    )

    engine_runtime = _resolve_engine_runtime(
        evidence_items=evidence_items,
        runtime=runtime,
    )

    if engine_runtime is None:
        st.error("找不到 Evidence Center Engine Runtime。")
        return

    actions = _get_actions_from_runtime(engine_runtime)

    if not actions:
        _render_empty_state()
        return

    _render_action_summary(actions)

    st.divider()

    _render_action_table(actions)

    st.divider()

    _render_action_cards(actions)