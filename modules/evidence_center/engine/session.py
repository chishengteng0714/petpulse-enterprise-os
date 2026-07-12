import streamlit as st

from modules.evidence_center.engine.runtime import (
    create_evidence_center_runtime_engine,
)


ENGINE_KEY = "evidence_center_engine"
RUNTIME_KEY = "evidence_center_runtime"


def ensure_engine_runtime(raw_evidence_items):
    """
    確保 Evidence Center Engine / Runtime 已存在。

    所有 Workspace / Studio / UI 都應從這裡取得同一份 Runtime。
    """

    if ENGINE_KEY not in st.session_state:
        st.session_state[ENGINE_KEY] = create_evidence_center_runtime_engine()

    if RUNTIME_KEY not in st.session_state:
        engine = st.session_state[ENGINE_KEY]
        st.session_state[RUNTIME_KEY] = engine.boot(raw_evidence_items)

    return get_engine_runtime()


def get_engine_runtime():
    """
    取得目前 Engine 與 Runtime。
    """

    return (
        st.session_state.get(ENGINE_KEY),
        st.session_state.get(RUNTIME_KEY),
    )


def save_engine_runtime(runtime):
    """
    儲存更新後的 Runtime。
    """

    st.session_state[RUNTIME_KEY] = runtime


def reset_engine_runtime(raw_evidence_items):
    """
    重新啟動 Evidence Center Runtime。
    """

    engine = create_evidence_center_runtime_engine()
    runtime = engine.boot(raw_evidence_items)

    st.session_state[ENGINE_KEY] = engine
    st.session_state[RUNTIME_KEY] = runtime

    return engine, runtime