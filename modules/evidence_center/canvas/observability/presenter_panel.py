import inspect

import streamlit as st


PRESENTER_MODULES = [
    {
        "name": "CopilotPresenter",
        "module": "modules.evidence_center.canvas.presentation.copilot_presenter",
        "class_name": "CopilotPresenter",
        "responsibility": "建立 Copilot 所需的 Canvas Intelligence Context。",
    },
    {
        "name": "DecisionPresenter",
        "module": "modules.evidence_center.canvas.presentation.decision_presenter",
        "class_name": "DecisionPresenter",
        "responsibility": "整理決策視角、建議行動與判斷依據。",
    },
    {
        "name": "RelationshipPresenter",
        "module": "modules.evidence_center.canvas.presentation.relationship_presenter",
        "class_name": "RelationshipPresenter",
        "responsibility": "整理節點、邊與證據之間的關係脈絡。",
    },
    {
        "name": "TimelinePresenter",
        "module": "modules.evidence_center.canvas.presentation.timeline_presenter",
        "class_name": "TimelinePresenter",
        "responsibility": "整理時間序列、事件脈絡與 Timeline Context。",
    },
    {
        "name": "InspectorPresenter",
        "module": "modules.evidence_center.canvas.presentation.inspector_presenter",
        "class_name": "InspectorPresenter",
        "responsibility": "整理目前選取物件的 Inspector 顯示資料。",
    },
]


def render_presenter_panel(runtime):
    """
    Presenter Observability Panel

    用來檢查 Canvas Presentation Layer 的 Presenter 狀態。
    這個 Panel 不負責商業邏輯，只負責 Observability。
    """

    st.subheader("Presenter Health")
    st.caption(
        "檢查 Canvas Presentation Layer 是否已完成 Presenter 化，"
        "並確認各 Presenter 可被正常載入。"
    )

    presenter_statuses = [_inspect_presenter(item) for item in PRESENTER_MODULES]

    total = len(presenter_statuses)
    healthy = len([item for item in presenter_statuses if item["status"] == "Healthy"])
    degraded = len([item for item in presenter_statuses if item["status"] == "Degraded"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Presenters", total)

    with col2:
        st.metric("Healthy", healthy)

    with col3:
        st.metric("Degraded", degraded)

    st.divider()

    for item in presenter_statuses:
        _render_presenter_card(item)

    st.divider()

    _render_selected_object_preview(runtime)


def _inspect_presenter(config):
    try:
        module = __import__(config["module"], fromlist=[config["class_name"]])
        presenter_class = getattr(module, config["class_name"], None)

        if presenter_class is None:
            return {
                **config,
                "status": "Degraded",
                "message": "Presenter class not found.",
                "methods": [],
            }

        methods = _get_public_methods(presenter_class)

        return {
            **config,
            "status": "Healthy",
            "message": "Presenter loaded successfully.",
            "methods": methods,
        }

    except Exception as error:
        return {
            **config,
            "status": "Degraded",
            "message": str(error),
            "methods": [],
        }


def _get_public_methods(presenter_class):
    methods = []

    for name, value in inspect.getmembers(presenter_class, predicate=inspect.isfunction):
        if not name.startswith("_"):
            methods.append(name)

    return methods


def _render_presenter_card(item):
    status_icon = "✅" if item["status"] == "Healthy" else "⚠️"

    with st.container(border=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {status_icon} {item['name']}")
            st.caption(item["responsibility"])
            st.code(item["module"], language="text")

        with col2:
            st.metric("Status", item["status"])

        if item["methods"]:
            st.markdown("**Public Methods**")
            st.write(", ".join(item["methods"]))
        else:
            st.caption("No public methods detected.")

        if item["message"]:
            st.caption(item["message"])


def _render_selected_object_preview(runtime):
    st.subheader("Presenter Runtime Context")
    st.caption("顯示 Presenter 目前可取得的選取物件狀態。")

    selected_object = _safe_call(runtime, "get_selected_object")

    if not selected_object:
        st.info("目前沒有選取任何 Canvas Object。")
        return

    st.json(selected_object)


def _safe_call(runtime, method_name, default=None):
    if runtime is None:
        return default

    method = getattr(runtime, method_name, None)

    if not callable(method):
        return default

    try:
        return method()
    except Exception:
        return default