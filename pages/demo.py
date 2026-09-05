import streamlit as st
from data.demo_households import DEMO_HOUSEHOLDS
from ui.styles import t, rerun


def render_demo(translations):
    st.subheader(t(translations, "demo_title", "Demo Mode"))
    st.caption(
        t(
            translations,
            "demo_note",
            "Load a sample household to test the recommendation engine.",
        )
    )

    choice = st.selectbox(
        t(translations, "demo_choice", "Choose a demo household"),
        list(DEMO_HOUSEHOLDS.keys()),
        key="demo_choice",
    )

    if st.button(
        t(translations, "load_demo", "Load this household"),
    ):
        demo = DEMO_HOUSEHOLDS[choice]
        st.session_state["household"] = dict(demo["household"])

        # The live questionnaire no longer has a family-member page.
        # For demo compatibility, retain the first/head member only.
        members = demo.get("members", [])
        st.session_state["members"] = [dict(members[0])] if members else []

        if st.session_state["members"]:
            head = st.session_state["members"][0]
            st.session_state["household"]["occupation"] = head.get("occupation", "Other")
            st.session_state["household"]["head_age"] = head.get("age", 40)
            st.session_state["household"]["head_gender"] = head.get("gender", "Male")
            st.session_state["household"]["head_marital_status"] = head.get("marital_status", "Married")

        st.session_state["run_recommendation"] = True
        st.session_state["page"] = "results"
        rerun()

    if st.button(t(translations, "home_button", "Home")):
        st.session_state["page"] = "home"
        rerun()
