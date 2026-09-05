import streamlit as st
from ui.styles import t, display_value, display_category, rerun
from ui.components import disclaimer_box
from ui.tamil_text import ta_text, SCHEME_NAMES
from data.scheme_details import DETAILS

NA_EN = "Detailed information is not available in the current project dataset."
NA_TA = "இந்தத் திட்டத்திற்கான விரிவான தகவல் தற்போதைய திட்டத் தரவுத்தளத்தில் இன்னும் சேர்க்கப்படவில்லை."


def _text(ta, en):
    return ta if st.session_state.get("language", "en") == "ta" and ta else (ta_text(en) if st.session_state.get("language", "en") == "ta" else en)


def _rule_eligibility(scheme):
    """Create a readable English eligibility summary from the app's own rules."""
    target = str(scheme.get("target_group_text", "")).strip()
    parts = []
    if target and target.lower() != "nan":
        parts.append(f"இந்தத் திட்டம் {ta_text(target)} என்பவர்களுக்காகும்." if st.session_state.get("language", "en") == "ta" else f"This scheme is intended for {target}.")

    try:
        from pathlib import Path
        import csv
        rules_file = Path(__file__).resolve().parents[1] / "data" / "scheme_rules.csv"
        with rules_file.open(encoding="utf-8-sig", newline="") as f:
            rows = [r for r in csv.DictReader(f) if r.get("scheme_id") == str(scheme.get("scheme_id"))]
    except Exception:
        rows = []

    primary = [r for r in rows if str(r.get("condition_type", "")).upper() == "PRIMARY"]
    supporting = [r for r in rows if str(r.get("condition_type", "")).upper() == "SUPPORTING"]

    for r in primary:
        desc = str(r.get("description", "")).strip()
        if desc:
            parts.append(f"முக்கிய தகுதி நிபந்தனை: {ta_text(desc)}." if st.session_state.get("language", "en") == "ta" else f"Main eligibility condition: {desc}.")
    for r in supporting:
        desc = str(r.get("description", "")).strip()
        if desc:
            parts.append(f"கூடுதல் ஆதரவு நிபந்தனை: {ta_text(desc)}." if st.session_state.get("language", "en") == "ta" else f"Additional supporting condition: {desc}.")

    if not parts:
        parts.append("தகுதி என்பது திட்டத்தின் தற்போதைய அரசு வழிகாட்டுதல்கள் மற்றும் விண்ணப்பதாரரின் சூழ்நிலைகளைப் பொறுத்தது." if st.session_state.get("language", "en") == "ta" else "Eligibility depends on the scheme's current government guidelines and the applicant's circumstances.")
    parts.append("இறுதி தகுதி தற்போதைய விதிகளின்படி தொடர்புடைய அரசு துறை அல்லது செயல்படுத்தும் அமைப்பால் தீர்மானிக்கப்படுகிறது." if st.session_state.get("language", "en") == "ta" else "Final eligibility is decided by the concerned government department or implementing agency under the current rules.")
    return " ".join(parts)


def _field(scheme, detail, field, tamil_field, fallback):
    if st.session_state.get("language", "en") == "ta" and detail and detail.get(tamil_field):
        return detail[tamil_field]
    english_field = f"{field}_en"
    if field == "eligibility_text":
        return _rule_eligibility(scheme)
    if detail and detail.get(english_field):
        return detail[english_field] if st.session_state.get("language", "en") != "ta" else ta_text(detail[english_field])
    value = scheme.get(field, "")
    if value is None or not str(value).strip() or str(value).lower() == "not available in source":
        return fallback
    return str(value) if st.session_state.get("language", "en") != "ta" else ta_text(str(value))


def render_scheme_details(translations, schemes_df):
    scheme_id = st.session_state.get("selected_scheme_id")
    if not scheme_id:
        st.info(t(translations, "no_scheme_selected", "No scheme selected."))
        return

    row = schemes_df[schemes_df["scheme_id"] == scheme_id]
    if row.empty:
        st.error(t(translations, "scheme_not_found", "Scheme not found."))
        return

    scheme = row.iloc[0].to_dict()
    detail = DETAILS.get(scheme_id, {})
    tamil = st.session_state.get("language", "en") == "ta"

    name = detail.get("tamil_name") if tamil else None
    name = name or (SCHEME_NAMES.get(str(scheme.get("scheme_name", "")), str(scheme.get("scheme_name", ""))) if tamil else str(scheme.get("scheme_name", "")))
    st.markdown(f"# {name}")

    if not tamil and False:
        st.caption(detail["tamil_name"])

    st.markdown(
        f"<div class='small-muted'>{display_value(scheme.get('government'))} · "
        f"{display_category(scheme.get('category'))}</div>",
        unsafe_allow_html=True,
    )

    # Clear, myScheme-style sections instead of one long label:value list.
    sections = [
        ("overview", "திட்டத்தைப் பற்றி", "About the scheme", "description", "description_ta"),
        ("benefit", "என்ன பயன்?", "What is the benefit?", "benefit", "benefit_ta"),
        ("eligibility", "யார் பெறலாம்?", "Who can get it?", "eligibility_text", "eligibility_ta"),
    ]

    for _, ta_title, en_title, field, tamil_field in sections:
        title = ta_title if tamil else en_title
        value = _field(scheme, detail, field, tamil_field, NA_TA if tamil else NA_EN)
        # Keep every visible detail in the selected language.
        if tamil and value and not (field == "eligibility_text" and isinstance(value, str)):
            value = ta_text(str(value))
        st.markdown(f"### {title}")
        st.markdown(f"<div class='detail-box'>{value}</div>", unsafe_allow_html=True)

    st.markdown(f"### {'தேவையான ஆவணங்கள்' if tamil else 'Documents required'}")
    docs = detail.get("documents_ta") if tamil else detail.get("documents_en")
    if docs:
        for doc in docs:
            st.markdown(f"<div class='doc-item'>📄 {doc}</div>", unsafe_allow_html=True)
    else:
        raw_docs = str(scheme.get("documents", "")).strip()
        if raw_docs and raw_docs.lower() != "not available in source":
            for doc in re_split_docs(raw_docs):
                st.markdown(f"<div class='doc-item'>📄 {doc}</div>", unsafe_allow_html=True)
        else:
            generic_docs = ([
                "தேவையான இடங்களில் ஆதார் அல்லது பிற செல்லுபடியாகும் அடையாளச் சான்று",
                "தேவையான இடங்களில் வங்கி கணக்கு விவரங்கள்",
                "தேவையான இடங்களில் முகவரி / வசிப்பிடச் சான்று",
                "தொடர்புடைய அரசு துறை கேட்கும் திட்டத்திற்கான கூடுதல் ஆவணங்கள்",
            ] if tamil else [
                "Aadhaar or other valid identity proof, where applicable",
                "Bank account details, where applicable",
                "Address/residence proof, where applicable",
                "Scheme-specific supporting documents required by the concerned department",
            ])
            for doc in generic_docs:
                st.markdown(f"<div class='doc-item'>📄 {doc}</div>", unsafe_allow_html=True)

    st.markdown(f"### {'எப்படி விண்ணப்பிப்பது?' if tamil else 'How to apply'}")
    app_text = detail.get("application_ta") if tamil else detail.get("application_en")
    if not app_text:
        app_text = _field(
            scheme,
            detail,
            "application_route",
            "application_ta",
            NA_TA if tamil else (
                "Apply through the official scheme portal or the concerned government "
                "department, bank, local body or implementing agency, as applicable. "
                "Verify the current application procedure before applying."
            ),
        )
    st.markdown(f"<div class='detail-box'>{app_text}</div>", unsafe_allow_html=True)

    official_source = detail.get("official_source") or str(scheme.get("official_source", "")).strip()
    st.markdown(f"### {'அதிகாரப்பூர்வ இணையதளம்' if tamil else 'Official website'}")
    if official_source.startswith(("http://", "https://")):
        label = "அதிகாரப்பூர்வ தளத்தைத் திறக்க" if tamil else "Open official website"
        st.markdown(f"🔗 [{label}]({official_source})")
        if detail:
            st.caption("தகவல் அதிகாரப்பூர்வ அரசு ஆதாரத்தை அடிப்படையாகக் கொண்டது. விண்ணப்பிக்கும் முன் தற்போதைய விதிகளைச் சரிபார்க்கவும்." if tamil else "Information is based on an official government source. Verify the current rules before applying.")
    else:
        st.info(NA_TA if tamil else "No verified official URL is stored for this scheme yet.")

    # Recommendation-specific explanation, if opened from results.
    ranked = st.session_state.get("ranked_results", [])
    matches = [r for r in ranked if r["scheme_id"] == scheme_id]
    if matches:
        st.markdown("---")
        st.markdown(f"### {t(translations, 'why_shown', 'Why this appears')}")
        for rec in matches:
            st.markdown(
                f"**{t(translations, 'relevance_score_label', 'Relevance Score')}: {rec['score']}/100**"
            )
            for reason in rec.get("reasons", []):
                st.markdown(f"- ✓ {ta_text(reason) if tamil else reason}")

    disclaimer_box(translations, "disclaimer_main")
    if st.button(t(translations, "back_button", "Back"), key="details_back"):
        st.session_state["page"] = st.session_state.get("previous_page", "home")
        rerun()


def re_split_docs(raw):
    # Dataset entries may be semicolon/comma separated. Keep this deliberately simple.
    import re
    return [x.strip() for x in re.split(r"[;|\\n]+", raw) if x.strip()]
