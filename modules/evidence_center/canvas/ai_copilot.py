# modules/evidence_center/canvas/ai_copilot.py

import streamlit as st

from modules.evidence_center.canvas.presenters import CopilotPresenter


def render(runtime):
    render_ai_copilot(runtime)


def render_ai_copilot(runtime):
    """
    AI 調查助理

    GM-08 Enterprise Design System v2：
    - 移除 HTML Relationship Item
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native Components
    - 保持 Runtime Behavior 不變
    """

    view_model = CopilotPresenter(runtime).present()

    st.markdown("### AI 調查助理")
    st.caption("協助整理選取內容的證據脈絡、關聯、風險與下一步問題。")

    _render_status(view_model)
    _render_focus(view_model)
    _render_evidence(view_model)
    _render_relationships(view_model)
    _render_risk(view_model)
    _render_prompts(view_model)


def _render_status(view_model):
    col1, col2 = st.columns(2)

    with col1:
        st.metric("協助狀態", _format_mode(view_model.get("mode", "idle")))

    with col2:
        st.metric("選取類型", _format_type(view_model.get("selected_type", "None")))


def _render_focus(view_model):
    st.markdown("#### 目前焦點")
    st.info(view_model.get("focus", "尚未選取分析目標。"))


def _render_evidence(view_model):
    evidence = view_model.get("evidence", {})

    st.markdown("#### 證據脈絡")

    if not evidence.get("available"):
        st.caption(evidence.get("message", "尚未取得證據脈絡。"))
        return

    st.write(f"**內容：** {evidence.get('content', '未命名證據')}")
    st.write(f"**資料來源：** {evidence.get('platform', '未知')}")
    st.write(f"**議題：** {evidence.get('topic', '未知')}")
    st.write(f"**情緒傾向：** {evidence.get('sentiment', '未知')}")
    st.write(f"**優先度：** {evidence.get('priority', '未知')}")

    ai_summary = evidence.get("ai_summary")
    if ai_summary:
        st.caption(ai_summary)


def _render_relationships(view_model):
    relationships = view_model.get("relationships", {})

    st.markdown("#### 關聯脈絡")
    st.caption(relationships.get("message", "目前尚未偵測到明確關聯。"))

    items = relationships.get("items", [])

    if not items:
        return

    for item in items[:5]:
        _render_relationship_item(item)


def _render_relationship_item(item):
    content = item.get("content", "相關項目")
    relation_type = item.get("type", "相關")
    strength = item.get("strength", "中")

    with st.container(border=True):
        st.markdown(f"#### {content}")
        st.caption(f"類型：{relation_type}｜強度：{strength}")


def _render_risk(view_model):
    risk = view_model.get("risk", {})

    st.markdown("#### 風險與下一步")
    st.warning(risk.get("risk_note", "目前沒有足夠上下文判斷風險。"))
    st.success(risk.get("next_step", "請先選取一個分析目標。"))


def _render_prompts(view_model):
    st.markdown("#### 建議追問")

    prompts = view_model.get("recommended_prompts", [])

    for prompt in prompts[:5]:
        st.button(prompt, use_container_width=True)

    next_best_question = view_model.get("next_best_question")

    if next_best_question:
        st.markdown("#### 下一個關鍵問題")
        st.info(next_best_question)


def _format_mode(value):
    return {
        "idle": "待命",
        "active": "分析中",
    }.get(str(value), str(value))


def _format_type(value):
    return {
        "None": "未選取",
        "node": "關聯項目",
        "evidence": "證據",
        "action": "行動",
        "flow": "流程",
    }.get(str(value), str(value))