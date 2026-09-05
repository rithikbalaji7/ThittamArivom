import streamlit as st
from ui.styles import t, priority_badge, display_value, display_category, rerun
from data.scheme_details import DETAILS
from ui.tamil_text import ta_text, ta_scheme_name


def _set_language(lang):
    st.session_state["language"] = lang


def language_switcher(translations):
    """Modern header. No government logo and no sign-in control."""
    current = st.session_state.get("language", "en")
    st.markdown(
        f"""
        <div class='ta-header'>
          <div class='ta-brand'>
            <div class='ta-brand-name'>Thittam<span>Arivom</span> <span class='ta-leaf'>⌁</span></div>
            <div class='ta-brand-tag'>{t(translations, 'tagline', 'Find the right government schemes for you')}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([6.4, 1, 1])
    with c2:
        if st.button("தமிழ்", key="global_lang_ta", disabled=current == "ta"):
            _set_language("ta")
            rerun()
    with c3:
        if st.button("English", key="global_lang_en", disabled=current == "en"):
            _set_language("en")
            rerun()


def disclaimer_box(translations, key="disclaimer_main"):
    st.markdown(f"<div class='disclaimer-box'>⚠ {t(translations, key)}</div>", unsafe_allow_html=True)


def progress_indicator(step: int, total: int, translations, step_labels=None):
    label = t(translations, "step_label", "Step")
    st.markdown(f"<div class='ta-step-count'>{label} {step} / {total}</div>", unsafe_allow_html=True)

    if not step_labels:
        st.progress(step / total)
        return

    circles = []
    for i, step_text in enumerate(step_labels, start=1):
        state = "active" if i == step else ("done" if i < step else "")
        marker = "✓" if i < step else str(i)
        circles.append(
            f"<div class='ta-step {state}'>"
            f"<div class='ta-step-line'></div>"
            f"<div class='ta-step-circle'>{marker}</div>"
            f"<div class='ta-step-label'>{step_text}</div>"
            f"</div>"
        )
    st.markdown(f"<div class='ta-stepper'>{''.join(circles)}</div>", unsafe_allow_html=True)


def scheme_directory_card(scheme_row: dict, translations: dict, on_details_click=None, key_prefix="dir"):
    with st.container():
        st.markdown("<div class='scheme-card'>", unsafe_allow_html=True)
        name = DETAILS.get(str(scheme_row['scheme_id']), {}).get('tamil_name') if st.session_state.get('language') == 'ta' else None
        name = name or (ta_scheme_name(str(scheme_row['scheme_name'])) if st.session_state.get('language') == 'ta' else str(scheme_row['scheme_name']))
        st.markdown(f"#### {name}")
        tags = []
        if scheme_row["requires_category"]: tags.append(t(translations, "category_specific_label"))
        if scheme_row["is_umbrella_entry"]: tags.append(t(translations, "umbrella_label"))
        if not scheme_row["recommendable"] and not scheme_row["is_umbrella_entry"] and not scheme_row["requires_category"]: tags.append(t(translations, "more_info_required"))
        if tags: st.markdown(" &nbsp; ".join(f"`{tag}`" for tag in tags))
        target = ta_text(scheme_row['target_group_text']) if st.session_state.get('language') == 'ta' else scheme_row['target_group_text']
        st.markdown(f"<span class='small-muted'>{display_value(scheme_row['government'])} · {display_category(scheme_row['category'])} · {target}</span>", unsafe_allow_html=True)
        if on_details_click and st.button(t(translations, "view_details", "View Details"), key=f"{key_prefix}_{scheme_row['scheme_id']}"):
            on_details_click(scheme_row["scheme_id"])
        st.markdown("</div>", unsafe_allow_html=True)


def recommendation_card(rec: dict, translations: dict, on_details_click=None, key_prefix=""):
    with st.container():
        st.markdown("<div class='scheme-card'>", unsafe_allow_html=True)
        name = DETAILS.get(str(rec['scheme_id']), {}).get('tamil_name') if st.session_state.get('language') == 'ta' else None
        name = name or (ta_scheme_name(str(rec['scheme_name'])) if st.session_state.get('language') == 'ta' else str(rec['scheme_name']))
        st.markdown(f"#### {name}")
        if rec["priority"] != "HIDDEN":
            st.markdown(priority_badge(rec["priority"], rec["score"], translations), unsafe_allow_html=True)
        relevant = ta_text(rec['relevant_member_label']) if st.session_state.get('language') == 'ta' else rec['relevant_member_label']
        st.markdown(f"<span class='small-muted'>{display_value(rec['government'])} · {display_category(rec['category'])} · {t(translations, 'why_shown', 'Why this appears')}: {relevant}</span>", unsafe_allow_html=True)
        if rec.get("reasons"):
            st.markdown(f"**{t(translations, 'why_shown', 'Why this appears')}**")
            for reason in rec["reasons"]:
                st.markdown(f"- ✓ {ta_text(reason) if st.session_state.get('language') == 'ta' else reason}")
        if rec.get("missing_information"):
            with st.expander(t(translations, "needs_verification", "Needs verification")):
                for missing in rec["missing_information"]:
                    st.markdown(f"- ⚠ {ta_text(missing) if st.session_state.get('language') == 'ta' else missing}")
        if rec.get("verification_status"):
            st.caption(f"{t(translations, 'verification_status', 'Verification status')}: {ta_text(rec['verification_status']) if st.session_state.get('language') == 'ta' else rec['verification_status']}")
        if rec.get("viability_status"):
            st.caption(f"{t(translations, 'viability_status', 'Recommendation status')}: {ta_text(rec['viability_status']) if st.session_state.get('language') == 'ta' else rec['viability_status']}")
        if on_details_click and st.button(t(translations, "view_details", "View Details"), key=f"{key_prefix}_{rec['scheme_id']}_{rec.get('relevant_member_id')}"):
            on_details_click(rec["scheme_id"])
        st.markdown("</div>", unsafe_allow_html=True)
