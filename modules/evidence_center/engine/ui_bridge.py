import streamlit as st

from modules.evidence_center.engine.models import EngineEvidence, EngineRuntime


class EngineUIBridge:
    """
    Engine UI Bridge

    負責把 Engine Runtime 的狀態同步給既有 Workspace UI。

    目的：
    - 保留舊的 selected_evidence / selected_evidence_2
    - 讓 Evidence Explorer / Compare Mode 可以逐步吃 Engine Runtime
    - 避免一次重構整個 UI
    """

    def sync_runtime_to_workspace_state(self, runtime: EngineRuntime):
        st.session_state["selected_evidence"] = runtime.selected_evidence_id
        st.session_state["selected_evidence_2"] = runtime.selected_evidence_id_2

    def sync_workspace_state_to_runtime(self, runtime: EngineRuntime) -> EngineRuntime:
        runtime.selected_evidence_id = st.session_state.get("selected_evidence")
        runtime.selected_evidence_id_2 = st.session_state.get("selected_evidence_2")

        return runtime

    def get_selected_evidence(
        self,
        runtime: EngineRuntime,
        slot: str = "A",
    ) -> EngineEvidence | None:
        evidence_id = (
            runtime.selected_evidence_id_2
            if slot == "B"
            else runtime.selected_evidence_id
        )

        if not evidence_id:
            return None

        for evidence in runtime.evidence:
            if evidence.evidence_id == evidence_id:
                return evidence

        return None

    def to_legacy_evidence_items(
        self,
        runtime: EngineRuntime,
    ) -> list[dict]:
        """
        將 EngineEvidence 暫時轉回舊 UI 可吃的 dict。
        """

        return [
            {
                "evidence_id": item.evidence_id,
                "title": item.title,
                "content": item.content,
                "platform": item.platform,
                "topic": item.topic,
                "sentiment": item.sentiment,
                "engagement": item.engagement,
                "source_url": item.source_url,
                "created_time": item.created_time,
                "metadata": item.metadata,
            }
            for item in runtime.evidence
        ]

    def select_evidence(
        self,
        runtime: EngineRuntime,
        evidence_id: str | None,
        slot: str = "A",
    ) -> EngineRuntime:
        if slot == "B":
            runtime.selected_evidence_id_2 = evidence_id
            st.session_state["selected_evidence_2"] = evidence_id
        else:
            runtime.selected_evidence_id = evidence_id
            st.session_state["selected_evidence"] = evidence_id

        return runtime


def create_engine_ui_bridge() -> EngineUIBridge:
    return EngineUIBridge()