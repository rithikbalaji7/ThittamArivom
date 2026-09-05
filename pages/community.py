import streamlit as st
from ui.styles import t, rerun
from ui.components import scheme_directory_card


def render_community(translations, schemes_df):
    st.subheader(
        t(translations, "community_schemes", "Village / Community Schemes")
    )
    st.caption(
        t(
            translations,
            "community_note",
            "Community-level schemes are shown separately and are not part of personal household recommendations.",
        )
    )

    community = schemes_df[
        schemes_df["scheme_type"] == "COMMUNITY"
    ].sort_values("scheme_name")

    if community.empty:
        st.info(t(translations, "no_community", "No community schemes found."))
    else:
        for _, row in community.iterrows():
            scheme_directory_card(
                row.to_dict(),
                translations,
                on_details_click=_go_to_details,
                key_prefix="community",
            )

    if st.button(t(translations, "home_button", "Home")):
        st.session_state["page"] = "home"
        rerun()


def _go_to_details(scheme_id):
    st.session_state["selected_scheme_id"] = scheme_id
    st.session_state["previous_page"] = "community"
    st.session_state["page"] = "scheme_details"
    rerun()
