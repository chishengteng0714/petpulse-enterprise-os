import streamlit as st


def render(runtime):
    render_graph_layer(runtime)


def render_graph_layer(runtime):
    """
    證據關係圖
    """

    st.markdown("### 證據關係圖")
    st.caption("查看證據、議題與行動之間的關聯，協助判斷事件脈絡。")

    nodes = _safe_call(runtime, "get_nodes", [])
    edges = _safe_call(runtime, "get_edges", [])

    _render_graph_summary(nodes, edges)
    _render_nodes(runtime, nodes)
    _render_edges(edges)


def _render_graph_summary(nodes, edges):
    col1, col2 = st.columns(2)

    with col1:
        st.metric("關聯項目", len(nodes))

    with col2:
        st.metric("關聯線索", len(edges))


def _render_nodes(runtime, nodes):
    st.markdown("#### 關聯項目")

    if not nodes:
        st.caption("目前沒有可顯示的關聯項目。")
        return

    for node in nodes[:12]:
        node_id = _get_object_id(node)
        title = _get_object_title(node)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{title}**")
            st.caption(f"編號：{node_id}")

        with col2:
            if st.button("選取", key=f"select_node_{node_id}", use_container_width=True):
                if runtime and hasattr(runtime, "select_node"):
                    runtime.select_node(node_id)
                    st.rerun()


def _render_edges(edges):
    st.markdown("#### 關聯線索")

    if not edges:
        st.caption("目前沒有可顯示的關聯線索。")
        return

    for edge in edges[:8]:
        st.caption(
            f"{edge.get('source', '未知來源')} → {edge.get('target', '未知目標')}｜"
            f"{edge.get('label', edge.get('type', '相關'))}"
        )


def _safe_call(runtime, method_name, default=None):
    if not runtime or not hasattr(runtime, method_name):
        return default

    try:
        return getattr(runtime, method_name)()
    except Exception:
        return default


def _get_object_id(item):
    return (
        item.get("id")
        or item.get("evidence_id")
        or item.get("node_id")
        or "unknown"
    )


def _get_object_title(item):
    return (
        item.get("title")
        or item.get("label")
        or item.get("name")
        or item.get("summary")
        or item.get("id")
        or item.get("evidence_id")
        or "未命名項目"
    )