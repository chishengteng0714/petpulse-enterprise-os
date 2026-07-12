import streamlit as st

from modules.evidence_center.canvas.presenters import RelationshipPresenter


def render(runtime):
    render_relationship_map(runtime)


def render_relationship_map(runtime):
    """
    關聯地圖

    GM-08 Enterprise Design System v2：
    - 移除 HTML Relationship Card
    - 移除 unsafe_allow_html=True
    - 使用 100% Streamlit Native Components
    - 保持 Runtime Behavior 不變
    """

    view_model = RelationshipPresenter(runtime).present()

    st.markdown("### 關聯地圖")
    st.caption("查看目前選取內容與其他證據、議題或行動之間的關聯。")

    _render_summary(view_model)
    _render_relationships(view_model)


def _render_summary(view_model):
    total = view_model.get("total", 0)
    message = view_model.get(
        "message",
        "目前尚未偵測到與選取內容直接相關的情報關聯。",
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric("關聯數", total)

    with col2:
        st.info(message)


def _render_relationships(view_model):
    relationships = view_model.get("relationships", [])

    if not relationships:
        st.caption("請先選取一個內容，系統會顯示相關證據與脈絡。")
        return

    for item in relationships:
        _render_relationship_card(item)


def _render_relationship_card(item):
    title = item.get("title", "相關項目")
    relation_type = item.get("type", "相關")
    label = item.get("label", "相關")
    strength = item.get("strength", "中")
    source = item.get("source", "未知來源")
    target = item.get("target", "未知目標")

    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.caption(label)

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"類型：{relation_type}")
            st.write(f"強度：{strength}")

        with col2:
            st.write(f"來源：{source}")
            st.write(f"目標：{target}")