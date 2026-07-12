import streamlit as st


def render_knowledge_graph(evidences: list):
    """
    Simple Knowledge Graph UI (Streamlit Native)

    GM-06 Final Schema Consistency Audit

    - Nodes = Evidence
    - Edges = Same Topic Relationship
    - 使用 Golden Master Evidence Schema
    """

    st.subheader("🧠 Knowledge Graph")

    if not evidences:
        st.info("No data")
        return

    # =========================
    # BUILD NODES
    # =========================

    nodes = []
    edges = []

    for evidence in evidences:
        nodes.append(
            {
                "id": evidence.get("evidence_id") or evidence.get("id"),
                "label": (
                    evidence.get("content")
                    or evidence.get("evidence_id")
                    or evidence.get("id")
                    or "Untitled Evidence"
                ),
                "topic": evidence.get("topic", "unknown"),
            }
        )

    # =========================
    # BUILD EDGES
    # =========================

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[i]["topic"] == nodes[j]["topic"]:
                edges.append(
                    (
                        nodes[i]["id"],
                        nodes[j]["id"],
                    )
                )

    # =========================
    # RENDER
    # =========================

    st.markdown("### Nodes")

    for node in nodes:
        st.markdown(f"- 🟢 {node['label']} (`{node['topic']}`)")

    st.markdown("### Connections")

    if not edges:
        st.info("No strong relationships detected")
        return

    for source_id, target_id in edges:
        st.markdown(f"- {source_id} ↔ {target_id}")