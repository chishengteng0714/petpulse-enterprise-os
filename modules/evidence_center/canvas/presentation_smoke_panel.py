import streamlit as st

from modules.evidence_center.canvas.presenters import CanvasPresentationSmokeTest


def render_presentation_smoke_panel(runtime):
    """
    Canvas Presentation Smoke Test Panel

    檢查所有 Presenter 是否能穩定產出 View Model。
    """

    st.markdown("### Presentation Runtime Smoke Test")
    st.caption("檢查 Canvas Presenters 是否能正常讀取 Intelligence Context。")

    if not runtime:
        st.error("Canvas Runtime 尚未初始化。")
        return

    result = CanvasPresentationSmokeTest(runtime).run()

    if result.get("passed"):
        st.success("All Canvas Presenters Passed.")
    else:
        st.error("Some Canvas Presenters Failed.")

    results = result.get("results", {})

    for name, item in results.items():
        with st.expander(f"{name}｜{item.get('presenter')}"):
            st.write(f"Passed：{item.get('passed')}")
            st.write(f"Keys：{item.get('keys', [])}")

            if item.get("error"):
                st.error(item.get("error"))