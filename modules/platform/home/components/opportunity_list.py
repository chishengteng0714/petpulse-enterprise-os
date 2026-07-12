import streamlit as st


def render_opportunity_list(summary):
    st.markdown("## 值得關注的成長機會")
    st.caption("將市場討論、消費者需求與競品動態轉成可追蹤的成長行動。")

    columns = st.columns(3)

    for index, item in enumerate(summary["opportunities"][:3]):
        with columns[index]:
            _render_opportunity_item(item, index + 1)

    st.divider()


def _render_opportunity_item(item, index):
    with st.container(border=True):
        st.caption(f"Opportunity {index}")
        st.markdown(f"### {item['title']}")
        st.write(item["signal"])

        st.metric("Impact", item["impact"])
        st.caption(f"Window：{item['window']}")

        st.button(
            item["action"],
            key=f"opportunity_{item['id']}",
            use_container_width=True,
        )