import streamlit as st


def render_investigation_graph_canvas(runtime, kernel):
    """
    Investigation OS v2 - Graph Canvas UI

    目前版本：
    - Node 可 click / focus
    - 可 filter subgraph
    - 可依 node type 篩選
    - 可 highlight relationship
    - 顯示 visible nodes / edges
    """

    graph_state = runtime.graph_state

    st.markdown("## 🧠 Investigation Graph Canvas")
    st.caption(
        "以 node-link 結構呈現證據、議題、平台、情緒與關聯路徑。"
    )

    _render_graph_toolbar(runtime, kernel)
    _render_graph_summary(graph_state)

    left_col, right_col = st.columns([1.25, 1])

    with left_col:
        _render_node_canvas(runtime, kernel)

    with right_col:
        _render_focus_panel(runtime)
        _render_edge_panel(runtime, kernel)


def _render_graph_toolbar(runtime, kernel):
    graph_state = runtime.graph_state

    st.markdown("### Canvas Controls")

    node_types = sorted(
        {
            node.node_type
            for node in graph_state.nodes
            if node.node_type
        }
    )

    relationships = sorted(
        {
            edge.relationship
            for edge in graph_state.edges
            if edge.relationship
        }
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_node_type = st.selectbox(
            "Node Type Filter",
            options=["All"] + node_types,
            index=0,
        )

        if st.button("套用 Node Filter", use_container_width=True):
            node_type = None if selected_node_type == "All" else selected_node_type
            runtime = kernel.filter_by_node_type(runtime, node_type)
            st.session_state["investigation_os_v2_runtime"] = runtime
            st.rerun()

    with col2:
        selected_relationship = st.selectbox(
            "Relationship Highlight",
            options=["None"] + relationships,
            index=0,
        )

        if st.button("高亮 Relationship", use_container_width=True):
            relationship = (
                None
                if selected_relationship == "None"
                else selected_relationship
            )
            runtime = kernel.highlight_relationship(runtime, relationship)
            st.session_state["investigation_os_v2_runtime"] = runtime
            st.rerun()

    with col3:
        if st.button("重置 Canvas", use_container_width=True):
            for node in graph_state.nodes:
                node.is_focus = False
                node.is_selected = False
                node.is_filtered = False

            for edge in graph_state.edges:
                edge.is_highlighted = False

            graph_state.focus_node_id = None
            graph_state.selected_node_id = None
            graph_state.active_relationship = None
            graph_state.active_node_type = None

            runtime = kernel.cycle(runtime)
            st.session_state["investigation_os_v2_runtime"] = runtime
            st.rerun()


def _render_graph_summary(graph_state):
    visible_nodes = graph_state.visible_nodes()
    visible_edges = graph_state.visible_edges()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Nodes", len(graph_state.nodes))
    col2.metric("Visible Nodes", len(visible_nodes))
    col3.metric("Total Edges", len(graph_state.edges))
    col4.metric("Visible Edges", len(visible_edges))


def _render_node_canvas(runtime, kernel):
    graph_state = runtime.graph_state

    st.markdown("### Nodes")

    visible_nodes = graph_state.visible_nodes()

    if not visible_nodes:
        st.info("目前沒有可顯示的 Node。")
        return

    for node in sorted(visible_nodes, key=lambda item: item.score, reverse=True):
        _render_node_card(node, runtime, kernel)


def _render_node_card(node, runtime, kernel):
    focus_badge = "🎯 Focus" if node.is_focus else "Node"
    selected_badge = "Selected" if node.is_selected else node.node_type

    with st.container(border=True):
        top_col, action_col = st.columns([3, 1])

        with top_col:
            st.markdown(f"#### {node.label}")
            st.caption(f"{focus_badge} · {selected_badge}")

            if node.description:
                st.write(node.description)

            meta_col1, meta_col2, meta_col3 = st.columns(3)

            with meta_col1:
                st.caption("Platform")
                st.write(node.metadata.get("platform", "Unknown"))

            with meta_col2:
                st.caption("Topic")
                st.write(node.metadata.get("topic", "Unknown"))

            with meta_col3:
                st.caption("Score")
                st.write(round(node.score, 2))

        with action_col:
            if st.button(
                "Focus",
                key=f"focus_node_{node.node_id}",
                use_container_width=True,
            ):
                runtime = kernel.focus_node(runtime, node.node_id)
                st.session_state["investigation_os_v2_runtime"] = runtime
                st.rerun()

            if st.button(
                "Open",
                key=f"open_node_{node.node_id}",
                use_container_width=True,
            ):
                st.session_state["selected_evidence"] = (
                    node.metadata.get("evidence_id") or node.node_id
                )
                st.success("已送到 Evidence Detail。")


def _render_focus_panel(runtime):
    graph_state = runtime.graph_state

    st.markdown("### Focus Panel")

    if not graph_state.focus_node_id:
        st.info("尚未選擇 Focus Node。")
        return

    focus_node = graph_state.get_node(graph_state.focus_node_id)

    if not focus_node:
        st.warning("找不到目前 Focus Node。")
        return

    with st.container(border=True):
        st.markdown(f"#### 🎯 {focus_node.label}")
        st.caption(f"Node Type：{focus_node.node_type}")

        if focus_node.description:
            st.write(focus_node.description)

        st.markdown("##### Metadata")

        for key, value in focus_node.metadata.items():
            st.write(f"**{key}**：{value}")

        connected_node_ids = graph_state.get_connected_node_ids(focus_node.node_id)

        st.markdown("##### Connected Nodes")
        st.write(f"{len(connected_node_ids)} 個直接關聯節點")


def _render_edge_panel(runtime, kernel):
    graph_state = runtime.graph_state

    st.markdown("### Relationships")

    visible_edges = graph_state.visible_edges()

    if not visible_edges:
        st.info("目前沒有可顯示的 Edge。")
        return

    highlighted_edges = [
        edge
        for edge in visible_edges
        if edge.is_highlighted
    ]

    if highlighted_edges:
        st.success(f"目前高亮 {len(highlighted_edges)} 條關係。")

    for edge in visible_edges[:30]:
        _render_edge_card(edge, graph_state, runtime, kernel)


def _render_edge_card(edge, graph_state, runtime, kernel):
    source_node = graph_state.get_node(edge.source)
    target_node = graph_state.get_node(edge.target)

    source_label = source_node.label if source_node else edge.source
    target_label = target_node.label if target_node else edge.target

    highlight_icon = "✨" if edge.is_highlighted else "🔗"

    with st.container(border=True):
        st.markdown(
            f"**{highlight_icon} {source_label} → {target_label}**"
        )
        st.caption(f"Relationship：{edge.relationship}")

        if edge.description:
            st.write(edge.description)

        col1, col2 = st.columns(2)

        with col1:
            st.caption("Weight")
            st.write(edge.weight)

        with col2:
            if st.button(
                "Focus Source",
                key=f"edge_focus_source_{edge.edge_id}",
                use_container_width=True,
            ):
                runtime = kernel.focus_node(runtime, edge.source)
                st.session_state["investigation_os_v2_runtime"] = runtime
                st.rerun()