import streamlit as st

from database.db_access import load_schemes, load_scheme_rules, load_translations
from ui.styles import inject_base_styles
from ui.components import language_switcher
from ui.styles import rerun
from pages.home import render_home
from pages.questionnaire import render_questionnaire
from pages.results import render_results
from pages.scheme_details import render_scheme_details
from pages.community import render_community
from pages.directory import render_directory
from pages.demo import render_demo

st.set_page_config(
    page_title="Thittam Arivom | திட்டம் அறிவோம்",
    page_icon="\U0001F3E1",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_base_styles()

if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "language" not in st.session_state:
    st.session_state["language"] = "en"

schemes_df = load_schemes()
rules_df = load_scheme_rules()
translations = load_translations()

language_switcher(translations)

page = st.session_state["page"]

if page == "home":
    render_home(translations)
elif page == "questionnaire":
    render_questionnaire(translations)
elif page == "results":
    render_results(translations, schemes_df, rules_df)
elif page == "scheme_details":
    render_scheme_details(translations, schemes_df)
elif page == "community":
    render_community(translations, schemes_df)
elif page == "directory":
    render_directory(translations, schemes_df)
elif page == "demo":
    render_demo(translations)
else:
    st.session_state["page"] = "home"
    rerun()
