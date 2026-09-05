import streamlit as st
from ui.styles import t, rerun
from ui.components import recommendation_card, disclaimer_box
from ui.tamil_text import ta_scheme_name, ta_text
from logic.recommendation_engine import generate_recommendations


def render_results(translations, schemes_df, rules_df):
    st.subheader(
        t(
            translations,
            "results_title",
            "Government Schemes That May Be Relevant to Your Family",
        )
    )

    household = st.session_state.get("household", {})
    members = st.session_state.get("members", [])

    if not household or not members:
        st.info(
            t(
                translations,
                "need_more_info",
                "Please complete the household questionnaire first.",
            )
        )
        if st.button(t(translations, "complete_profile", "Complete Profile")):
            st.session_state["page"] = "questionnaire"
            st.session_state["quest_step"] = 1
            rerun()
        return

    if (
        st.session_state.get("run_recommendation")
        or "ranked_results" not in st.session_state
    ):
        ranked, not_matched = generate_recommendations(
            schemes_df,
            rules_df,
            household,
            members,
        )
        st.session_state["ranked_results"] = ranked
        st.session_state["not_matched_results"] = not_matched
        st.session_state["run_recommendation"] = False

    ranked = st.session_state.get("ranked_results", [])
    not_matched = st.session_state.get("not_matched_results", [])

    st.info(
        t(
            translations,
            "head_only_results_note",
            "Recommendations are based on the household and household-head information collected. "
            "Schemes that require detailed information about other individual family members may need "
            "additional verification.",
        )
    )

    if not ranked:
        st.warning(
            t(
                translations,
                "no_confident_match",
                "No strong match was found from the available information.",
            )
        )
    else:
        for priority in ["HIGH", "MEDIUM", "LOW"]:
            group = [r for r in ranked if r["priority"] == priority]
            if not group:
                continue

            label_key = {
                "HIGH": "priority_high",
                "MEDIUM": "priority_medium",
                "LOW": "priority_low",
            }[priority]

            st.markdown(
                f"### {t(translations, label_key, priority)} ({len(group)})"
            )

            for rec in group:
                recommendation_card(
                    rec,
                    translations,
                    on_details_click=_go_to_details,
                    key_prefix="res",
                )

    if not_matched:
        with st.expander(
            f"{t(translations, 'status_not_matched', 'Not Currently Matched')} "
            f"({len(not_matched)})"
        ):
            st.caption(
                t(
                    translations,
                    "not_matched_note",
                    "These schemes have a mandatory rule that did not match the information provided.",
                )
            )

            for rec in not_matched:
                scheme_name = ta_scheme_name(rec["scheme_name"]) if st.session_state.get("language") == "ta" else rec["scheme_name"]
                st.markdown(f"- **{scheme_name}**")
                for missing in rec["missing_information"]:
                    text = ta_text(missing) if st.session_state.get("language") == "ta" else missing
                    st.markdown(f"  - {text}")

    st.write("")
    disclaimer_box(translations, "score_disclaimer")
    disclaimer_box(translations, "disclaimer_main")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(t(translations, "edit_profile", "Edit Profile")):
            st.session_state["page"] = "questionnaire"
            st.session_state["quest_step"] = 1
            rerun()

    with col2:
        if st.button(t(translations, "community_schemes", "Village / Community Schemes")):
            st.session_state["page"] = "community"
            rerun()

    with col3:
        if st.button(t(translations, "home_button", "Home")):
            st.session_state["page"] = "home"
            rerun()


def _go_to_details(scheme_id):
    st.session_state["selected_scheme_id"] = scheme_id
    st.session_state["previous_page"] = "results"
    st.session_state["page"] = "scheme_details"
    rerun()
