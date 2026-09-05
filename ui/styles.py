import streamlit as st
from ui.tamil_text import ta_text


def t(translations: dict, key: str, fallback: str = None) -> str:
    lang = st.session_state.get("language", "en")
    entry = translations.get(key)
    if entry:
        value = entry.get(lang) or entry.get("en")
        if value:
            return value
    return fallback if fallback is not None else key


VALUE_EN = {
    "Pucca": "Permanent / concrete house",
    "Semi-pucca": "Partly permanent house",
    "Kutcha": "Temporary / basic house",
}

VALUE_TAMIL = {
    "Yes": "ஆம்", "No": "இல்லை", "Male": "ஆண்", "Female": "பெண்", "Other": "மற்றவை",
    "Married": "திருமணமானவர்", "Unmarried": "திருமணமாகாதவர்", "Widowed": "விதவை / கணவரை இழந்தவர்", "Separated": "பிரிந்தவர்",
    "Farmer": "விவசாயி", "Agricultural worker": "விவசாயத் தொழிலாளர்", "Daily wage worker": "தினக்கூலி தொழிலாளர்",
    "Student": "மாணவர்", "Artisan": "கைவினைஞர்", "Small business owner": "சிறு தொழில் நடத்துபவர்",
    "Street vendor": "தெருவோர வியாபாரி", "Homemaker": "இல்லத்தரசி", "Fisherman": "மீனவர்",
    "Livestock owner": "கால்நடை வளர்ப்பவர்", "Unorganised worker": "அமைப்புசாரா தொழிலாளர்", "Owned": "சொந்த வீடு",
    "Rented": "வாடகை வீடு", "No house": "வீடு இல்லை", "Needs housing": "வீடு தேவை",
    "Pucca": "நிரந்தர / கான்கிரீட் வீடு", "Semi-pucca": "பகுதி நிரந்தர வீடு", "Kutcha": "தற்காலிக / அடிப்படை வீடு",
    "Electric": "மின்சாரம்", "Diesel": "டீசல்", "Solar": "சூரிய ஆற்றல்", "General": "பொதுவான விவசாயம்",
    "Horticulture": "தோட்டக்கலை", "Organic": "இயற்கை விவசாயம்", "Low": "குறைந்த வருமானம்", "Medium": "நடுத்தர வருமானம்", "High": "அதிக வருமானம்",
    "Below ₹1 lakh": "₹1 லட்சத்திற்குக் குறைவு", "₹1 lakh – ₹2.5 lakh": "₹1 லட்சம் – ₹2.5 லட்சம்",
    "₹2.5 lakh – ₹5 lakh": "₹2.5 லட்சம் – ₹5 லட்சம்", "₹5 lakh – ₹10 lakh": "₹5 லட்சம் – ₹10 லட்சம்",
    "Above ₹10 lakh": "₹10 லட்சத்திற்கும் மேல்", "Tamil Nadu": "தமிழ்நாடு", "Government": "அரசு",
}

CATEGORY_TAMIL = {
    "Agriculture": "விவசாயம்", "Housing": "வீடு", "Tribal Welfare": "பழங்குடியினர் நலன்", "Sanitation": "சுகாதாரம் / கழிப்பறை",
    "Water": "குடிநீர்", "Community Development": "கிராம வளர்ச்சி", "Labour": "தொழிலாளர் நலன்", "Women": "பெண்கள் நலன்",
    "Health": "சுகாதாரம்", "Pension": "ஓய்வூதியம்", "Business": "தொழில் / வணிகம்", "Banking": "வங்கி சேவைகள்",
    "Insurance": "காப்பீடு", "Education": "கல்வி", "Disability Welfare": "மாற்றுத்திறனாளிகள் நலன்", "Livestock": "கால்நடை",
    "Fisheries": "மீன்வளம்", "Energy": "ஆற்றல்", "Food/Nutrition": "உணவு / ஊட்டச்சத்து", "Agriculture/Pension": "விவசாயம் / ஓய்வூதியம்",
}


def display_value(value, translations=None):
    if value is None:
        return ""
    text = str(value)
    if st.session_state.get("language", "en") == "ta":
        return VALUE_TAMIL.get(text, CATEGORY_TAMIL.get(text, ta_text(text)))
    return VALUE_EN.get(text, text)


def display_category(value):
    if st.session_state.get("language", "en") == "ta":
        return CATEGORY_TAMIL.get(str(value), ta_text(value))
    return str(value)


PRIORITY_COLORS = {"HIGH": "#C0392B", "MEDIUM": "#D68910", "LOW": "#B7950B"}
PRIORITY_ICONS = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}


def priority_badge(priority: str, score: int, translations: dict) -> str:
    label_key = {"HIGH": "priority_high", "MEDIUM": "priority_medium", "LOW": "priority_low"}[priority]
    label = t(translations, label_key, priority)
    icon = PRIORITY_ICONS[priority]
    color = PRIORITY_COLORS[priority]
    return f"<span class='priority-badge' style='--badge-color:{color}'>{icon} {label} <span>·</span> {score}/100</span>"


def rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def inject_base_styles():
    st.markdown(
        """
        <style>
        :root { --green:#0b8f4d; --green-dark:#08753f; --ink:#14243d; --muted:#68758a; --line:#e3e9e5; --soft:#f4faf6; }
        #MainMenu { visibility:hidden; }
        footer { visibility:hidden; }
        header[data-testid="stHeader"] { background:transparent; }
        [data-testid="stToolbar"] { visibility:hidden; height:0; }
        [data-testid="stDecoration"] { display:none; }
        [data-testid="stStatusWidget"] { visibility:hidden; }
        [data-testid="stSidebar"] { display:none; }
        [data-testid="stSidebarCollapsedControl"] { display:none; }
        [data-testid="stAppViewContainer"] { background: #fbfefd; }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { max-width: 1180px; padding: 1.2rem 2rem 3rem; }

        /* Header */
        .ta-header { display:flex; align-items:center; gap:28px; background:#fff; border:1px solid #edf1ee; border-radius:22px;
                     padding:14px 20px; box-shadow:0 5px 24px rgba(20,55,38,.06); margin-bottom:32px; }
        .ta-brand { min-width:250px; }
        .ta-brand-name { font-size:1.75rem; font-weight:800; color:var(--ink); letter-spacing:-.8px; line-height:1; }
        .ta-brand-name span { color:var(--green); }
        .ta-brand-tag { color:#6e7886; font-size:.76rem; margin-top:7px; }
        .ta-leaf { color:var(--green); }
        .ta-header-right { display:flex; align-items:center; gap:12px; }
        .ta-theme { width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center;
                    border:1px solid #dfe6e2; color:var(--ink); background:#fff; font-size:1.1rem; }

        /* Decorative background */
        .ta-page-bg { position:fixed; left:-130px; top:150px; width:360px; height:360px; border-radius:50%; background:#e8f7ee; opacity:.72; z-index:-1; }
        .ta-page-bg2 { position:fixed; right:-180px; bottom:-180px; width:520px; height:360px; border-radius:50% 50% 0 0; background:#e7f7ed; opacity:.8; z-index:-1; }
        .ta-dots { position:fixed; right:38px; top:300px; width:150px; height:120px; opacity:.35; z-index:-1;
                   background-image:radial-gradient(#8fc7a6 1.5px, transparent 1.5px); background-size:18px 18px; }

        .ta-hero-title { text-align:center; color:var(--ink); font-size:2.1rem; font-weight:800; margin:8px 0 8px; letter-spacing:-.7px; }
        .ta-hero-sub { text-align:center; color:var(--muted); margin-bottom:26px; }
        .ta-card { background:rgba(255,255,255,.97); border:1px solid #edf1ee; border-radius:26px; padding:34px 42px; box-shadow:0 14px 42px rgba(27,65,44,.09); }
        .ta-section-title { color:var(--ink); font-size:1.45rem; font-weight:800; margin-bottom:5px; }
        .ta-underline { width:68px; height:3px; background:var(--green); border-radius:3px; margin:8px 0 24px; }
        .ta-step-count { border-left:4px solid var(--green); padding-left:13px; color:var(--ink); font-weight:700; margin:16px 0; }

        /* Numbered stepper */
        .ta-stepper { display:flex; align-items:flex-start; justify-content:center; margin:22px 0 30px; }
        .ta-step { position:relative; display:flex; flex-direction:column; align-items:center; flex:1; max-width:170px; }
        .ta-step-line { position:absolute; top:17px; left:-50%; width:100%; height:2px; background:#dfe6e2; z-index:0; }
        .ta-step:first-child .ta-step-line { display:none; }
        .ta-step.done .ta-step-line, .ta-step.active .ta-step-line { background:var(--green); }
        .ta-step-circle { position:relative; z-index:1; width:34px; height:34px; border-radius:50%; display:flex; align-items:center;
                           justify-content:center; font-weight:800; font-size:.92rem; border:2px solid #dfe6e2; background:#fff; color:#8994a3; }
        .ta-step.done .ta-step-circle, .ta-step.active .ta-step-circle { background:var(--green); border-color:var(--green); color:#fff; }
        .ta-step-label { margin-top:9px; font-size:.78rem; font-weight:600; color:var(--muted); text-align:center; line-height:1.25; }
        .ta-step.active .ta-step-label { color:var(--ink); text-decoration:underline; text-decoration-color:var(--green); text-underline-offset:5px; }

        /* Icon-card style radio options (e.g. gender) */
        .ta-icon-cards .stRadio > div { flex-direction:row; gap:14px; }
        .ta-icon-cards .stRadio [role="radiogroup"] { flex-direction:row; gap:14px; }
        .ta-icon-cards .stRadio [role="radiogroup"] > label { flex:1; flex-direction:column; align-items:center; justify-content:center;
                           gap:6px; padding:20px 12px; border-radius:16px; text-align:center; font-weight:700; }
        .ta-icon-cards .stRadio [role="radiogroup"] > label:has(input:checked) { border-color:var(--green); background:#eaf8ef; color:var(--green-dark); }

        /* Streamlit controls */
        /* Force readable dark text everywhere, regardless of visitor's device dark-mode setting. */
        label, .stMarkdown p, .stMarkdown, .stMarkdown li,
        [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label,
        [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
        h1, h2, h3, h4, h5, h6,
        .stRadio label, .stCheckbox label, .stSelectbox label, .stTextInput label,
        .stNumberInput label, .stDateInput label, .stTextArea label,
        [data-testid="stCaptionContainer"] { color:var(--ink) !important; }
        .stTextInput input { border-radius:12px !important; border:1px solid #d9e1dc !important; min-height:46px !important; }
        .stSelectbox > div > div { border-radius:12px !important; border-color:#d9e1dc !important; min-height:46px; }
        .stRadio > div { gap:10px; }
        .stRadio [role="radiogroup"] > label { border:1px solid #dfe6e2; border-radius:14px; padding:14px 18px; background:#fff; }
        .stButton > button { border-radius:12px; min-height:46px; font-weight:700; border:1px solid #d6dfda; background:#fff; color:var(--ink); transition:.15s ease; }
        .stButton > button:hover { border-color:var(--green); color:var(--green-dark); transform:translateY(-1px); }
        .stButton > button[kind="primary"] { background:var(--green); color:#fff; border-color:var(--green); min-height:66px; font-size:1.4rem; }
        .stButton > button[kind="primary"]:hover { background:var(--green-dark); border-color:var(--green-dark); color:#fff; }
        .stProgress > div > div > div { background:var(--green); }
        .stProgress > div > div { background:#e8efeb; border-radius:99px; }
        .stCaption { color:#7a8797; }

        .scheme-card { border:1px solid #e4ebe7; border-radius:18px; padding:20px; margin-bottom:15px; background:#fff; box-shadow:0 5px 18px rgba(30,60,43,.04); }
        .scheme-card h4 { margin:0 0 8px 0; color:var(--ink); }
        .small-muted { color:#6B7787; font-size:.88rem; }
        .detail-box { border:1px solid #e5ece8; border-radius:14px; padding:17px; margin:10px 0; background:#fbfdfc; }
        .detail-title { font-size:1.05rem; font-weight:700; margin-bottom:6px; color:var(--ink); }
        .doc-item { padding:7px 0; border-bottom:1px solid #EEEEEE; }
        .disclaimer-box { background:#fff9ec; border:1px solid #f0dca9; border-radius:12px; padding:12px 14px; font-size:.85rem; color:#6b520e; margin:8px 0; }
        .priority-badge { display:inline-flex; gap:7px; align-items:center; background:#fdf2ee; color:var(--badge-color); padding:6px 11px; border-radius:999px; font-weight:700; font-size:.82rem; }

        @media (max-width: 800px) {
          .block-container { padding:1rem 1rem 2rem; }
          .ta-header { flex-wrap:wrap; gap:14px; }
          .ta-brand { min-width:0; flex:1; }
          .ta-card { padding:24px 18px; }
          .ta-hero-title { font-size:1.65rem; }
        }
        </style>
        <div class='ta-page-bg'></div><div class='ta-page-bg2'></div><div class='ta-dots'></div>
        """,
        unsafe_allow_html=True,
    )
