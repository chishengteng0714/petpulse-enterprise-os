import streamlit as st

from modules.evidence_center.canvas.presenters import DecisionPresenter


def render(runtime):
    render_decision_queue(runtime)


def render_decision_queue(runtime):
    """
    建議決策

    GM-08 Enterprise Design System v2：
    - 移除 HTML Decision Card
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native Components
    - 保持 Runtime Behavior 不變
    """

    view_model = DecisionPresenter(runtime).present()

    st.markdown("### 建議決策")
    st.caption("根據目前選取內容與關聯脈絡，整理可能需要主管確認的決策事項。")

    _render_summary(view_model)
    _render_decision_cards(view_model)


def _render_summary(view_model):
    col1, col2 = st.columns(2)

    with col1:
        st.metric("選取內容", view_model.get("selected_title", "尚未選取"))

    with col2:
        st.metric("關聯數", view_model.get("relationship_total", 0))

    st.info(
        view_model.get(
            "recommended_focus",
            "請先選取一個證據、行動或流程。",
        )
    )


def _render_decision_cards(view_model):
    cards = view_model.get("decision_cards", [])

    if not cards:
        st.caption("目前沒有可顯示的建議決策。")
        return

    for card in cards:
        _render_decision_card(card)


def _render_decision_card(card):
    title = card.get("title", "決策事項")
    status = card.get("status", "待確認")
    description = card.get("description", "")

    with st.container(border=True):
        title_col, status_col = st.columns([3, 1])

        with title_col:
            st.markdown(f"#### {title}")

        with status_col:
            st.caption(status)

        if description:
            st.write(description)