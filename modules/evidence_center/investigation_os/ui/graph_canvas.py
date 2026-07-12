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


def _node_id(node):
    return (
        _safe_get(node, "node_id")
        or _safe_get(node, "id")
        or _safe_get(node, "evidence_id")
        or "unknown_node"
    )


def _node_title(node):
    return (
        _safe_get(node, "title")
        or _safe_get(node, "label")
        or _safe_get(node, "name")
        or _node_id(node)
    )


def _node_type(node):
    return (
        _safe_get(node, "node_type")
        or _safe_get(node, "type")
        or _safe_get(node, "category")
        or "Evidence"
    )


def _node_summary(node):
    return (
        _safe_get(node, "summary")
        or _safe_get(node, "description")
        or _safe_get(node, "content")
        or "此節點目前尚未提供摘要。"
    )


def _edge_source(edge):
    return _safe_get(edge, "source") or _safe_get(edge, "source_id") or ""


def _edge_target(edge):
    return _safe_get(edge, "target") or _safe_get(edge, "target_id") or ""


def _edge_label(edge):
    return (
        _safe_get(edge, "label")
        or _safe_get(edge, "relation")
        or _safe_get(edge, "edge_type")
        or _safe_get(edge, "type")
        or "relates_to"
    )


def _safe_mermaid_id(value):
    text = str(value)

    safe = ""

    for char in text:
        if char.isalnum():
            safe += char
        else:
            safe += "_"

    if not safe:
        safe = "node"

    if safe[0].isdigit():
        safe = f"node_{safe}"

    return safe


def _build_node_lookup(nodes):
    return {_node_id(node): node for node in nodes}


def _get_nodes_from_runtime(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_nodes"):
        return _safe_list(runtime.get_nodes())

    graph = _safe_get(runtime, "graph")

    if graph is None:
        graph_engine = _safe_get(runtime, "graph_engine")
        graph = _safe_get(graph_engine, "graph")

    nodes = _safe_get(graph, "nodes", [])

    return _safe_list(nodes)


def _get_edges_from_runtime(runtime):
    if runtime is None:
        return []

    if hasattr(runtime, "get_edges"):
        return _safe_list(runtime.get_edges())

    graph = _safe_get(runtime, "graph")

    if graph is None:
        graph_engine = _safe_get(runtime, "graph_engine")
        graph = _safe_get(graph_engine, "graph")

    edges = _safe_get(graph, "edges", [])

    return _safe_list(edges)


def _render_empty_state():
    st.info(
        "目前 Engine Runtime 尚未產生 Graph。請先確認 Evidence Workspace 已成功載入 Evidence Items。"
    )


def _render_graph_summary(nodes, edges):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Engine Nodes", len(nodes))

    with col2:
        st.metric("Engine Edges", len(edges))

    with col3:
        st.metric("Runtime API", "Active")


def _render_mermaid_graph(nodes, edges):
    if not nodes:
        return

    node_lookup = _build_node_lookup(nodes)

    lines = ["graph LR"]

    for node in nodes:
        node_id = _node_id(node)
        title = _node_title(node).replace('"', "'")
        safe_node_id = _safe_mermaid_id(node_id)

        lines.append(f'    {safe_node_id}["{title}"]')

    for edge in edges:
        source = _edge_source(edge)
        target = _edge_target(edge)

        if source not in node_lookup or target not in node_lookup:
            continue

        safe_source = _safe_mermaid_id(source)
        safe_target = _safe_mermaid_id(target)
        label = _edge_label(edge).replace('"', "'")

        lines.append(f"    {safe_source} -->|{label}| {safe_target}")

    mermaid_code = "\n".join(lines)

    st.markdown("### Engine Graph Preview")
    st.code(mermaid_code, language="mermaid")


def _render_node_cards(nodes):
    st.markdown("### Engine Nodes")

    if not nodes:
        st.caption("尚無節點。")
        return

    for node in nodes:
        with st.container(border=True):
            st.caption(_node_type(node))
            st.markdown(f"**{_node_title(node)}**")
            st.write(_node_summary(node))

            evidence_ids = _safe_get(node, "evidence_ids", None)
            metadata = _safe_get(node, "metadata", None)

            if evidence_ids:
                st.caption(f"Evidence IDs：{', '.join(map(str, _safe_list(evidence_ids)))}")

            if metadata:
                with st.expander("Node Metadata"):
                    st.json(metadata)


def _render_edge_table(edges, nodes):
    st.markdown("### Engine Edges")

    if not edges:
        st.caption("尚無關聯邊。")
        return

    node_lookup = _build_node_lookup(nodes)

    rows = []

    for edge in edges:
        source = _edge_source(edge)
        target = _edge_target(edge)

        source_node = node_lookup.get(source)
        target_node = node_lookup.get(target)

        rows.append(
            {
                "Source": _node_title(source_node) if source_node else source,
                "Relation": _edge_label(edge),
                "Target": _node_title(target_node) if target_node else target,
            }
        )

    st.dataframe(rows, width="stretch", hide_index=True)


def render_graph_canvas(evidence_items=None, runtime=None, kernel=None):
    """
    Evidence Center Graph Canvas

    A-5.5 Step 5-1:
    - 優先使用 Runtime API
    - runtime.get_nodes()
    - runtime.get_edges()
    - 不再猜測 Graph 內部結構作為主要資料來源
    - Investigation OS Kernel 保留參數但不使用
    """

    st.markdown("## Graph Canvas")
    st.caption(
        "由 Evidence Center Runtime API 驅動畫面。Graph Canvas 只負責呈現，不建立自己的 Graph。"
    )

    engine_runtime = _resolve_engine_runtime(
        evidence_items=evidence_items,
        runtime=runtime,
    )

    if engine_runtime is None:
        st.error("找不到 Evidence Center Engine Runtime。")
        return

    nodes = _get_nodes_from_runtime(engine_runtime)
    edges = _get_edges_from_runtime(engine_runtime)

    if not nodes:
        _render_empty_state()
        return

    _render_graph_summary(nodes, edges)

    st.divider()

    _render_mermaid_graph(nodes, edges)

    st.divider()

    col1, col2 = st.columns([1.2, 1])

    with col1:
        _render_node_cards(nodes)

    with col2:
        _render_edge_table(edges, nodes)