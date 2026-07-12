import streamlit as st

from modules.platform.specification.service import EnterpriseSpecificationService


def render_specification_debug_panel():
    """
    Render the product specification review page.

    Presentation layer only.
    Provides an executive-readable view of the product specification
    and RC Final demo narrative.
    """

    service = EnterpriseSpecificationService()
    spec = service.get_product_spec()

    st.markdown("# 產品規格")
    st.caption("PetPulse Enterprise OS v1.0｜Golden Master")

    _render_product_positioning(spec)
    _render_demo_story()
    _render_product_overview(spec)
    _render_product_principles(spec)
    _render_navigation(spec)
    _render_workspace_specs(spec)


def _render_product_positioning(spec):
    st.markdown("## 產品定位")

    with st.container(border=True):
        st.markdown(f"### {spec.name}")
        st.write("PetPulse 不是資料儀表板，也不是單純的社群監測工具。")
        st.write(
            "PetPulse 是 Enterprise Decision Operating System，協助主管在 30 秒內理解今日企業狀態、"
            "確認今日要決定的事項，並把後續工作交由各工作區承接。"
        )


def _render_demo_story():
    st.markdown("## Demo 敘事")

    steps = [
        {
            "title": "先看今日狀態",
            "description": "主管進入首頁後，先掌握今日企業健康、風險與機會。",
        },
        {
            "title": "確認今日決策",
            "description": "AI 將重要訊號轉成可討論、可指派、可追蹤的決策事項。",
        },
        {
            "title": "進入工作區執行",
            "description": "需要深入分析、證據查核或任務追蹤時，再進入對應工作區。",
        },
        {
            "title": "回到證據中心",
            "description": "所有判斷都能回到 Evidence Center，保留可追溯依據。",
        },
    ]

    cols = st.columns(len(steps))

    for index, (col, step) in enumerate(zip(cols, steps), start=1):
        with col:
            with st.container(border=True):
                st.caption(f"步驟 {index}")
                st.markdown(f"### {step['title']}")
                st.write(step["description"])


def _render_product_overview(spec):
    st.markdown("## 版本狀態")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("產品名稱", spec.name)

    with col2:
        st.metric("版本", spec.version)

    with col3:
        st.metric("工作區數量", len(spec.workspaces))


def _render_product_principles(spec):
    st.markdown("## 產品原則")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 產品體驗原則")
            _render_list(
                spec.product_principles,
                empty_text="目前尚未定義產品體驗原則。",
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 設計原則")
            _render_list(
                spec.design_principles,
                empty_text="目前尚未定義設計原則。",
            )


def _render_navigation(spec):
    st.markdown("## 導覽規格")
    st.caption("以下為 Golden Master 可進入的主要產品區域。")

    for item in spec.navigation:
        with st.container(border=True):
            title_col, status_col = st.columns([3, 1])

            with title_col:
                st.markdown(f"### {item.icon} {item.label}")
                st.write(item.description)

            with status_col:
                st.caption("狀態")
                st.markdown(f"**{_format_status(item.status)}**")

                st.caption("入口")
                st.markdown(f"**{item.target}**")


def _render_workspace_specs(spec):
    st.markdown("## 工作區規格")
    st.caption("工作區負責承接首頁決策後的執行、追蹤、分析與證據查核。")

    for workspace in spec.workspaces:
        with st.expander(workspace.name, expanded=False):
            st.markdown("### 工作區目的")
            st.write(workspace.purpose)

            st.markdown("### 使用者目標")
            st.write(workspace.user_goal)

            _render_workspace_hero(workspace)
            _render_workspace_sections(workspace)
            _render_workspace_interactions(workspace)
            _render_workspace_ai(workspace)


def _render_workspace_hero(workspace):
    st.markdown("### 首屏體驗")

    with st.container(border=True):
        st.caption("問候語")
        st.write(workspace.hero.greeting)

        st.caption("主標題")
        st.write(workspace.hero.title)

        st.caption("摘要")
        st.write(workspace.hero.summary)

        action_col, secondary_col = st.columns(2)

        with action_col:
            st.caption("主要行動")
            st.markdown(f"**{workspace.hero.primary_action or '未設定'}**")

        with secondary_col:
            st.caption("次要行動")
            st.markdown(f"**{workspace.hero.secondary_action or '未設定'}**")


def _render_workspace_sections(workspace):
    st.markdown("### 內容區塊")

    sections = sorted(workspace.sections, key=lambda item: item.priority)

    if not sections:
        st.caption("此工作區目前尚未定義內容區塊。")
        return

    for section in sections:
        with st.container(border=True):
            st.caption(f"顯示順序 {section.priority}")
            st.markdown(f"**{section.title}**")
            st.write(section.description)


def _render_workspace_interactions(workspace):
    st.markdown("### 使用者互動")

    if not workspace.interactions:
        st.caption("此工作區目前尚未定義互動項目。")
        return

    for interaction in workspace.interactions:
        with st.container(border=True):
            st.caption("使用者動作")
            st.write(interaction.trigger)

            st.caption("系統回應")
            st.write(interaction.behavior)

            st.caption("預期結果")
            st.write(interaction.result)


def _render_workspace_ai(workspace):
    st.markdown("### AI 協助")

    if workspace.ai is None:
        st.info("此工作區目前沒有設定 AI 協助角色。")
        return

    with st.container(border=True):
        st.caption("AI 角色")
        st.markdown(f"**{workspace.ai.role}**")

        st.caption("說明")
        st.write(workspace.ai.description)

        st.caption("能力")
        _render_list(
            workspace.ai.capabilities,
            empty_text="目前尚未設定 AI 能力。",
        )


def _render_list(items, empty_text="目前沒有資料。"):
    if not items:
        st.caption(empty_text)
        return

    for item in items:
        st.markdown(f"- {item}")


def _format_status(status):
    status_text = str(status).strip()

    status_map = {
        "available": "可使用",
        "ready": "可使用",
        "active": "可使用",
        "frozen": "已定版",
        "draft": "草稿",
        "disabled": "未開放",
    }

    return status_map.get(status_text.lower(), status_text)