# modules/evidence_center/components/interactive_graph.py

import streamlit as st

from modules.evidence_center.graph_ai_engine import GraphAIEngine
from modules.evidence_center.investigation_agent import InvestigationAgent


engine = GraphAIEngine()
agent = InvestigationAgent()


def render_interactive_graph(evidences, selected=None):

    st.subheader("🧠 Autonomous Investigation Graph")

    if not evidences:
        st.info("No data")
        return

    # =========================
    # AI + AGENT LAYER
    # =========================
    clusters = engine.cluster(evidences)
    anomalies = engine.detect_anomalies(evidences)
    path = engine.suggest_path(evidences)

    ranked = agent.score_evidence(evidences)
    next_e = agent.next_best_evidence(evidences, selected)
    loop_hint = agent.investigation_loop_hint(evidences)

    # =========================
    # PRIORITY VIEW
    # =========================
    st.markdown("### 🎯 Priority Ranking")

    for r in ranked[:5]:
        e = r["evidence"]
        st.markdown(f"- {_get_evidence_content(e)} → score {r['score']:.1f}")

    # =========================
    # NEXT BEST ACTION
    # =========================
    st.markdown("### 🤖 Next Best Evidence")

    if next_e:
        st.success(f"👉 {_get_evidence_content(next_e)}")

    # =========================
    # LOOP HINT
    # =========================
    st.markdown("### 🔁 Investigation Loop")

    st.info(loop_hint)

    # =========================
    # CLUSTERS
    # =========================
    st.markdown("### 🧩 Clusters")

    for k, v in clusters.items():
        st.markdown(f"- **{k}** → {len(v)} nodes")

    # =========================
    # ANOMALIES
    # =========================
    st.markdown("### ⚠️ Anomalies")

    for a in anomalies:
        st.warning(f"{a['id']} → {a['reason']}")

    # =========================
    # NODE VIEW
    # =========================
    st.markdown("### Nodes")

    focused = None

    for e in evidences:

        eid = e.get("evidence_id") or e.get("id")

        col1, col2 = st.columns([4, 1])

        with col1:
            mark = (
                "🟢"
                if selected
                and (
                    selected.get("id") == eid
                    or selected.get("evidence_id") == eid
                )
                else "⚪"
            )
            st.markdown(f"{mark} **{_get_evidence_content(e)}**")

        with col2:
            if st.button("Focus", key=f"a96_{eid}"):
                focused = e

    return focused


def _get_evidence_content(evidence):
    if not evidence:
        return "未命名證據"

    return (
        evidence.get("content")
        or evidence.get("evidence_id")
        or evidence.get("id")
        or "未命名證據"
    )