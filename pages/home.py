import streamlit as st
from ui.styles import t, rerun
from ui.components import disclaimer_box


def render_home(translations):
    lang = st.session_state.get("language", "en")
    title = "உங்களுக்குப் பொருந்தும் அரசுத் திட்டங்களைக் கண்டறியுங்கள்" if lang == "ta" else "Find the schemes that are right for you"
    sub = "சில எளிய விவரங்களை அளித்து, உங்களுக்குப் பொருத்தமான திட்டங்களை அறியுங்கள்" if lang == "ta" else "Answer a few simple questions and discover schemes that may fit your family."
    st.markdown(f"<div class='ta-hero-title'>{title}</div><div class='ta-hero-sub'>{sub}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='ta-section-title' style='text-align:center'>{'திட்டங்களைத் தேடத் தொடங்குங்கள்' if lang == 'ta' else 'Start finding your schemes'}</div><div class='ta-underline' style='margin-left:auto;margin-right:auto'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button(t(translations, "start_button", "Know Your Schemes"), key="start_journey", use_container_width=True, type="primary"):
            st.session_state["page"] = "questionnaire"; st.session_state["quest_step"] = 1; rerun()

    disclaimer_box(translations)
    st.markdown(f"<p class='small-muted' style='text-align:center'>{t(translations, 'privacy_notice')}</p>", unsafe_allow_html=True)
