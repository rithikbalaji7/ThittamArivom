import streamlit as st
from ui.styles import t, rerun, display_category
from ui.components import scheme_directory_card


def render_directory(translations, schemes_df):
    st.subheader(
        t(translations, "view_all_schemes", "View All Schemes")
    )

    st.caption(
        t(
            translations,
            "directory_note",
            "This directory lists the scheme records in the project dataset, including entries not used in default recommendations.",
        )
    )

    search_query = st.text_input(
        t(translations, "search_placeholder", "Search for schemes..."),
        key="dir_search_query",
    )

    all_label = "அனைத்தும்" if st.session_state.get("language") == "ta" else "All"
    categories = ["All"] + sorted(
        schemes_df["category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        t(translations, "filter_category", "Filter by category"),
        categories,
        key="dir_category_filter",
        format_func=lambda x: (all_label if x == "All" else display_category(x)) if st.session_state.get("language") == "ta" else x,
    )

    filtered = (
        schemes_df
        if selected_category == "All"
        else schemes_df[schemes_df["category"] == selected_category]
    )

    if search_query.strip():
        q = search_query.strip().lower()
        filtered = filtered[
            filtered["scheme_name"].str.lower().str.contains(q, na=False)
            | filtered["target_group_text"].str.lower().str.contains(q, na=False)
            | filtered["category"].str.lower().str.contains(q, na=False)
        ]

    filtered = filtered.sort_values("scheme_name")

    st.caption(
        f"{len(filtered)} {t(translations, 'scheme_count', 'scheme(s)')}"
    )

    for _, row in filtered.iterrows():
        scheme_directory_card(
            row.to_dict(),
            translations,
            on_details_click=_go_to_details,
            key_prefix="directory",
        )

    if st.button(t(translations, "home_button", "Home")):
        st.session_state["page"] = "home"
        rerun()


def _go_to_details(scheme_id):
    st.session_state["selected_scheme_id"] = scheme_id
    st.session_state["previous_page"] = "directory"
    st.session_state["page"] = "scheme_details"
    rerun()
