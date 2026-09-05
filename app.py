import os
import streamlit as st

from database.db_access import load_schemes, load_scheme_rules, load_translations
from ui.styles import inject_base_styles
from ui.components import language_switcher
from ui.styles import rerun
from screens.home import render_home
from screens.questionnaire import render_questionnaire
from screens.results import render_results
from screens.scheme_details import render_scheme_details
from screens.community import render_community
from screens.directory import render_directory
from screens.demo import render_demo

_LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo_icon.png")

st.set_page_config(
    page_title="Thittam Arivom | திட்டம் அறிவோம்",
    page_icon=_LOGO_PATH,
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
