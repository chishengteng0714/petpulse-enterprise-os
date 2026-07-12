import streamlit as st

from .ui_helpers import render_json_card


def render_timeline_panel(report):
    """
    Runtime Timeline
    """

    st.markdown("## Runtime Timeline")
    st.caption(
        "Canvas Runtime Event Stream"
    )

    snapshot = report.event_snapshot

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Events",
            snapshot.get("event_count", 0),
        )

    with col2:
        st.metric(
            "Event Types",
            snapshot.get("unique_event_types", 0),
        )

    with col3:
        st.metric(
            "Latest",
            "Yes" if snapshot.get("latest_event") else "No",
        )

    tab_type, tab_latest, tab_stream = st.tabs(
        [
            "Event Types",
            "Latest",
            "Stream",
        ]
    )

    with tab_type:
        render_json_card(
            "Event Type Distribution",
            snapshot.get("event_types"),
        )

    with tab_latest:
        render_json_card(
            "Latest Event",
            snapshot.get("latest_event"),
        )

    with tab_stream:

        stream = snapshot.get("event_stream", [])

        if not stream:
            st.info("No runtime events.")

        for event in reversed(stream[-30:]):

            with st.container(border=True):

                st.markdown(
                    f"### {event.get('type')}"
                )

                st.caption(
                    f"#{event.get('index')}"
                )

                with st.expander(
                    "Payload",
                    expanded=False,
                ):
                    st.json(event.get("payload"))