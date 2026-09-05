import streamlit as st
from ui.styles import t, display_value, rerun
from ui.components import progress_indicator, disclaimer_box

OCCUPATIONS = [
    "Farmer", "Agricultural worker", "Daily wage worker", "Student", "Artisan",
    "Small business owner", "Street vendor", "Homemaker", "Fisherman",
    "Livestock owner", "Unorganised worker", "Other"
]
FARM_LINKED_OCCUPATIONS = {"Farmer", "Agricultural worker", "Livestock owner", "Fisherman"}

INCOME_OPTIONS = {
    "Below ₹1 lakh": "Low",
    "₹1 lakh – ₹2.5 lakh": "Medium",
    "₹2.5 lakh – ₹5 lakh": "Medium",
    "₹5 lakh – ₹10 lakh": "High",
    "Above ₹10 lakh": "High",
}
INCOME_LABELS = list(INCOME_OPTIONS.keys())

YES_NO = ["No", "Yes"]


def _init_state():
    if "household" not in st.session_state:
        st.session_state["household"] = {}
    if "members" not in st.session_state:
        st.session_state["members"] = []
    if "quest_step" not in st.session_state:
        st.session_state["quest_step"] = 1


def _yn(label, key, default="Yes"):
    return st.radio(
        label, YES_NO, index=YES_NO.index(default), key=key,
        horizontal=True, format_func=lambda x: display_value(x)
    )


def _income_label(internal_value):
    for label, value in INCOME_OPTIONS.items():
        if value == internal_value:
            return label
    return INCOME_LABELS[0]


def _step_label(translations, key, fallback):
    return t(translations, key, fallback)


def render_questionnaire(translations):
    _init_state()

    step = st.session_state["quest_step"]
    total_steps = 3

    lang = st.session_state.get("language", "en")
    title = "உங்களுக்குப் பொருந்தும் திட்டங்களைக் கண்டறியுங்கள்" if lang == "ta" else "Find the schemes that are right for you"
    subtitle = "சில எளிய தகவல்களை அளித்து தொடருங்கள்" if lang == "ta" else "Tell us a little about yourself to get started"
    st.markdown(f"<div class='ta-hero-title'>{title}</div><div class='ta-hero-sub'>{subtitle}</div>", unsafe_allow_html=True)

    if lang == "ta":
        step_labels = ["உங்கள் விவரம்", "குடும்பம் & விவசாயம்", "மதிப்பாய்வு"]
    else:
        step_labels = ["Your details", "Household & farm", "Review"]
    progress_indicator(step, total_steps, translations, step_labels=step_labels)
    st.write("")
    st.markdown("<div class='ta-card'>", unsafe_allow_html=True)

    if step == 1:
        _step1_basic_info(translations)
    elif step == 2:
        _step2_household(translations)
    elif step == 3:
        _step3_review(translations)

    st.markdown("</div>", unsafe_allow_html=True)


def _nav_buttons(back_enabled=True, next_label=None, translations=None, on_next=None):
    col1, col2 = st.columns(2)

    with col1:
        if back_enabled and st.button(
            _step_label(translations, "back_button", "Back"),
            key=f"back_{st.session_state['quest_step']}",
        ):
            if st.session_state["quest_step"] == 1:
                st.session_state["page"] = "home"
            else:
                st.session_state["quest_step"] -= 1
            rerun()

    with col2:
        label = next_label or _step_label(translations, "next_button", "Next")
        st.markdown("<div class='ta-primary'>", unsafe_allow_html=True)
        next_clicked = st.button(label, key=f"next_{st.session_state['quest_step']}")
        st.markdown("</div>", unsafe_allow_html=True)
        if next_clicked:
            if on_next:
                ok = on_next()
                if ok is False:
                    return
            st.session_state["quest_step"] += 1
            rerun()


def _step1_basic_info(translations):
    section_title = _step_label(translations, "basic_info_title", "Basic Information")
    st.markdown(f"<div class='ta-section-title'>{section_title}</div><div class='ta-underline'></div>", unsafe_allow_html=True)

    h = st.session_state["household"]

    age_input = st.text_input(
        _step_label(translations, "head_age", "Age of household head"),
        value=str(h.get("head_age", "")) if h.get("head_age") is not None else "",
        placeholder="வயதை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter age",
        key="q1_age",
    )
    age = None
    if age_input.strip():
        try:
            age = int(age_input.strip())
        except ValueError:
            age = None

    gender_options = ["Male", "Female", "Other"]
    gender_icons = {"Male": "♂", "Female": "♀", "Other": "⚧"}
    saved_gender = h.get("head_gender")
    gender_index = gender_options.index(saved_gender) if saved_gender in gender_options else None
    st.markdown(f"<div class='ta-icon-cards'>", unsafe_allow_html=True)
    gender = st.radio(
        _step_label(translations, "gender", "Gender"),
        gender_options,
        index=gender_index,
        key="q1_gender",
        horizontal=True,
        format_func=lambda x: f"{gender_icons.get(x, '')}  {display_value(x)}",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    marital_options = ["Married", "Unmarried", "Widowed", "Separated"]
    saved_marital = h.get("head_marital_status")
    marital_index = marital_options.index(saved_marital) if saved_marital in marital_options else None
    marital_status = st.selectbox(
        _step_label(translations, "marital_status", "Marital status"),
        marital_options,
        index=marital_index,
        placeholder="திருமண நிலையை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter marital status",
        key="q1_marital",
        format_func=lambda x: display_value(x),
    )

    occupation_options = OCCUPATIONS
    saved_occupation = h.get("occupation")
    occupation_index = occupation_options.index(saved_occupation) if saved_occupation in occupation_options else None
    occupation = st.selectbox(
        _step_label(translations, "occupation", "Occupation"),
        occupation_options,
        index=occupation_index,
        placeholder="தொழிலை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter occupation",
        key="q1_occupation",
        format_func=lambda x: display_value(x),
    )

    income_options = INCOME_LABELS
    saved_income = _income_label(h.get("income_range")) if h.get("income_range") else None
    income_index = income_options.index(saved_income) if saved_income in income_options else None
    income_display = st.selectbox(
        _step_label(translations, "annual_income", "Annual household income"),
        income_options,
        index=income_index,
        placeholder="ஆண்டு வருமானத்தை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter annual income",
        key="q1_income",
        format_func=lambda x: display_value(x),
    )

    family_input = st.text_input(
        _step_label(translations, "family_size", "Number of people in the household"),
        value=str(h.get("family_size", "")) if h.get("family_size") is not None else "",
        placeholder=("குடும்ப உறுப்பினர்களின் எண்ணிக்கையை உள்ளிடவும்"
                     if st.session_state.get("language") == "ta"
                     else "Enter number of household members"),
        key="q1_family_size",
    )
    family_size = None
    if family_input.strip():
        try:
            family_size = int(family_input.strip())
        except ValueError:
            family_size = None

    st.caption(
        _step_label(
            translations,
            "income_note",
            "Income bands are input ranges; they are not official scheme eligibility limits.",
        )
    )

    def save_and_continue():
        if age is None or not (1 <= age <= 110):
            st.error("1 முதல் 110 வரை சரியான வயதை உள்ளிடவும்." if st.session_state.get("language") == "ta" else "Please enter a valid age between 1 and 110.")
            return False
        if gender is None:
            st.error("பாலினத்தைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select a gender.")
            return False
        if marital_status is None:
            st.error("திருமண நிலையைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select marital status.")
            return False
        if occupation is None:
            st.error("தொழிலைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select occupation.")
            return False
        if income_display is None:
            st.error("ஆண்டு குடும்ப வருமானத்தைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select annual household income.")
            return False
        if family_size is None or not (1 <= family_size <= 30):
            st.error("1 முதல் 30 வரை சரியான குடும்ப உறுப்பினர் எண்ணிக்கையை உள்ளிடவும்." if st.session_state.get("language") == "ta" else "Please enter a valid number of household members between 1 and 30.")
            return False

        # The recommendation engine still receives one member: the household head.
        # No separate family-member page is required.
        head_record = {
            "member_id": "head",
            "relation": "Head of Household",
            "age": int(age),
            "gender": gender,
            "marital_status": marital_status,
            "occupation": occupation,
            "student": "No",
            "education_level": None,
            "school_type": None,
            "disability": "No",
            "chronic_illness": "No",
            "pregnant_or_lactating": "No",
            "widow": "Yes" if marital_status == "Widowed" else "No",
            "shg_member": "No",
        }

        st.session_state["members"] = [head_record]

        h.update({
            "head_age": int(age),
            "head_gender": gender,
            "head_marital_status": marital_status,
            "occupation": occupation,
            "income_range": INCOME_OPTIONS[income_display],
            "income_display": income_display,
            "family_size": int(family_size),
        })

        return True

    _nav_buttons(
        back_enabled=True,
        translations=translations,
        on_next=save_and_continue,
    )


def _step2_household(translations):
    section_title = _step_label(translations, "household_info_title", "Household Information")
    st.markdown(f"<div class='ta-section-title'>{section_title}</div><div class='ta-underline'></div>", unsafe_allow_html=True)

    h = st.session_state["household"]
    head_occupation = h.get("occupation")

    st.caption(
        _step_label(
            translations,
            "yes_default_note",
            "Yes is selected by default. Change an answer when it does not apply.",
        )
    )

    house_status_options = ["Owned", "Rented", "No house", "Needs housing"]
    saved_house_status = h.get("house_status")
    house_status_index = house_status_options.index(saved_house_status) if saved_house_status in house_status_options else None
    house_status = st.selectbox(
        _step_label(translations, "house_status", "House status"),
        house_status_options,
        index=house_status_index,
        placeholder="வீட்டின் நிலையை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter house status",
        key="q2_house_status",
        format_func=lambda x: display_value(x),
    )

    # Use simple, user-friendly wording in the form while keeping the
    # internal values expected by the recommendation rules.
    house_type_labels = {
        "Pucca": ("நிரந்தர / கான்கிரீட் வீடு" if st.session_state.get("language") == "ta" else "Permanent / concrete house"),
        "Semi-pucca": ("பகுதி நிரந்தர வீடு" if st.session_state.get("language") == "ta" else "Partly permanent house"),
        "Kutcha": ("தற்காலிக / அடிப்படை வீடு" if st.session_state.get("language") == "ta" else "Temporary / basic house"),
    }
    house_type_options = list(house_type_labels.keys())
    saved_house_type = h.get("house_type")
    house_type_index = house_type_options.index(saved_house_type) if saved_house_type in house_type_options else None
    house_type = st.selectbox(
        _step_label(translations, "house_type", "House type"),
        house_type_options,
        index=house_type_index,
        placeholder="வீட்டு வகையை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter house type",
        key="q2_house_type",
        format_func=lambda x: house_type_labels.get(x, x),
    )

    electricity = _yn(
        _step_label(translations, "electricity", "Electricity connection?"),
        "q2_electricity",
        h.get("electricity", "Yes"),
    )

    lpg = _yn(
        _step_label(translations, "lpg", "LPG connection?"),
        "q2_lpg",
        h.get("household_has_lpg", "Yes"),
    )

    toilet = _yn(
        _step_label(translations, "toilet", "Toilet at home?"),
        "q2_toilet",
        h.get("household_has_toilet", "Yes"),
    )

    water = _yn(
        _step_label(translations, "water", "Piped drinking water access?"),
        "q2_water",
        h.get("water_access", "Yes"),
    )

    ration_card = _yn(
        _step_label(translations, "ration_card", "Ration card?"),
        "q2_ration",
        h.get("ration_card", "Yes"),
    )

    bank_account = _yn(
        _step_label(translations, "bank_account", "Bank account?"),
        "q2_bank",
        h.get("bank_account", "Yes"),
    )

    health_insurance = _yn(
        _step_label(translations, "health_insurance", "Existing health insurance?"),
        "q2_health_ins",
        h.get("health_insurance", "Yes"),
    )

    rooftop_solar = _yn(
        _step_label(translations, "rooftop_solar", "Rooftop solar already installed?"),
        "q2_solar",
        h.get("rooftop_solar", "Yes"),
    )

    woman_headed = _yn(
        _step_label(
            translations,
            "woman_headed",
            "Is this household headed by a woman?",
        ),
        "q2_woman_headed",
        h.get("woman_headed", "No"),
    )

    agri_section_title = _step_label(translations, "agriculture_title", "Agriculture Information")
    st.markdown(f"<div class='ta-section-title'>{agri_section_title}</div><div class='ta-underline'></div>", unsafe_allow_html=True)

    land_owned = _yn(
        _step_label(
            translations,
            "land_owned",
            "Do you own agricultural land?",
        ),
        "q2_land_owned",
        h.get("land_owned", "Yes"),
    )

    land_size = ""
    agri_pump = "No"
    pump_type = ""
    farming_activity = ""

    # Pumpset and farming questions are shown ONLY when land ownership is Yes.
    if land_owned == "Yes":
        land_size = st.text_input(
            _step_label(
                translations,
                "land_size",
                "Approximate agricultural landholding",
            ),
            value=h.get("land_size", ""),
            placeholder=("உதாரணம்: 2 ஏக்கர்"
                         if st.session_state.get("language") == "ta"
                         else "Example: 2 acres"),
            key="q2_land_size",
        )

        agri_pump = _yn(
            _step_label(
                translations,
                "agricultural_pump",
                "Do you have an agricultural pumpset?",
            ),
            "q2_agri_pump",
            h.get("agricultural_pump", "Yes"),
        )

        if agri_pump == "Yes":
            pump_options = ["Electric", "Diesel", "Solar", "Other"]
            saved_pump_type = h.get("pump_type")
            pump_index = pump_options.index(saved_pump_type) if saved_pump_type in pump_options else None
            pump_type = st.selectbox(
                _step_label(translations, "pump_type", "Pumpset type"),
                pump_options,
                index=pump_index,
                placeholder="பம்ப்செட் வகையை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter pumpset type",
                key="q2_pump_type",
                format_func=lambda x: display_value(x),
            )

        farming_options = ["General", "Horticulture", "Organic"]
        saved_farming_activity = h.get("farming_activity")
        farming_index = farming_options.index(saved_farming_activity) if saved_farming_activity in farming_options else None
        farming_activity = st.selectbox(
            _step_label(translations, "farming_activity", "Farming activity"),
            farming_options,
            index=farming_index,
            placeholder="விவசாய செயல்பாட்டை உள்ளிடவும்" if st.session_state.get("language") == "ta" else "Enter farming activity",
            key="q2_farm_activity",
            format_func=lambda x: display_value(x),
        )

    def save_and_continue():
        if house_status is None:
            st.error("வீட்டின் நிலையைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select house status.")
            return False
        if house_type is None:
            st.error("வீட்டு வகையைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select house type.")
            return False
        if land_owned == "Yes" and agri_pump == "Yes" and pump_type is None:
            st.error("பம்ப்செட் வகையைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select pumpset type.")
            return False
        if land_owned == "Yes" and farming_activity is None:
            st.error("விவசாய செயல்பாட்டைத் தேர்ந்தெடுக்கவும்." if st.session_state.get("language") == "ta" else "Please select farming activity.")
            return False

        h.update({
            "house_status": house_status,
            "house_type": house_type,
            "electricity": electricity,
            "household_has_lpg": lpg,
            "household_has_toilet": toilet,
            "water_access": water,
            "ration_card": ration_card,
            "bank_account": bank_account,
            "health_insurance": health_insurance,
            "rooftop_solar": rooftop_solar,
            "woman_headed": woman_headed,
            "land_owned": land_owned,
            "land_size": land_size if land_owned == "Yes" else "",
            "agricultural_pump": agri_pump if land_owned == "Yes" else "No",
            "pump_type": pump_type if land_owned == "Yes" and agri_pump == "Yes" else "",
            "farming_activity": farming_activity if land_owned == "Yes" else "",
            "household_state": "Tamil Nadu",
        })
        return True

    _nav_buttons(
        back_enabled=True,
        translations=translations,
        on_next=save_and_continue,
    )


def _step3_review(translations):
    review_title = _step_label(translations, "review_title", "Review & Get Recommendations")
    st.markdown(f"<div class='ta-section-title'>{review_title}</div><div class='ta-underline'></div>", unsafe_allow_html=True)

    h = st.session_state["household"]

    st.markdown(
        f"**{_step_label(translations, 'occupation', 'Occupation')}:** "
        f"{display_value(h.get('occupation', ''))}"
    )
    st.markdown(
        f"**{_step_label(translations, 'annual_income', 'Annual household income')}:** "
        f"{h.get('income_display', _income_label(h.get('income_range', 'Low')))}"
    )
    st.markdown(
        f"**{_step_label(translations, 'family_size', 'Household size')}:** "
        f"{h.get('family_size', '')}"
    )
    st.markdown(
        f"**{_step_label(translations, 'house_status', 'House status')}:** "
        f"{display_value(h.get('house_status', ''))}"
    )
    st.markdown(
        f"**{_step_label(translations, 'house_type', 'House type')}:** "
        f"{display_value(h.get('house_type', ''))}"
    )

    if h.get("land_owned") == "Yes":
        st.markdown(
            f"**{_step_label(translations, 'land_size', 'Landholding')}:** "
            f"{h.get('land_size') or 'Not entered'}"
        )
        st.markdown(
            f"**{_step_label(translations, 'agricultural_pump', 'Agricultural pumpset')}:** "
            f"{display_value(h.get('agricultural_pump'))}"
        )
        if h.get("agricultural_pump") == "Yes":
            st.markdown(
                f"**{_step_label(translations, 'pump_type', 'Pumpset type')}:** "
                f"{display_value(h.get('pump_type'))}"
            )

    st.info(
        _step_label(
            translations,
            "head_only_note",
            "This version collects household information and household-head information. "
            "It does not collect a separate family-member profile.",
        )
    )

    disclaimer_box(translations, "privacy_notice")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            _step_label(translations, "back_button", "Back"),
            key="review_back",
        ):
            st.session_state["quest_step"] = 2
            rerun()

    with col2:
        if st.button(
            _step_label(
                translations,
                "get_recommendations",
                "Get My Recommendations",
            ),
            key="submit_questionnaire",
        ):
            st.session_state["page"] = "results"
            st.session_state["run_recommendation"] = True
            rerun()
