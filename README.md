# திட்டம் அறிவோம் · Thittam Arivom (Version 1)

**"தேட வேண்டாம், தெரிந்து கொள்ளுங்கள்!" — "Don't search, know!"**

A mobile-friendly Streamlit app that helps rural households discover government
schemes that may be relevant to them, based on a short household questionnaire.
Built for student volunteers to use during in-person household visits.

**This is an informational tool, not an official government application.** It never
claims a household "is eligible" for anything — only that a scheme is "Potentially
Relevant" based on the information entered, with a transparent relevance score and
an explicit request to verify with the relevant government department.

---

## 1. What it does

1. Collects basic household and family-member information (occupation, income,
   land, house, utilities, education, disability/maternity — all self-declared,
   never a diagnosis).
2. Matches that information against a rule-based scheme database extracted from
   the source PDF (`Kannal_State_And_Central_Shemes.pdf`).
3. Scores each scheme 0–100 and assigns HIGH / MEDIUM / LOW priority.
4. Explains, for every recommendation, exactly which answers caused it to appear.
5. Shows scheme details, a separate community/village-schemes section, and a full
   scheme directory (including category-specific and multi-benefit entries that
   aren't part of the default results).

## 2. Folder structure

```
ThittamArivom/
├── app.py                     Entry point (session-state based routing)
├── requirements.txt
├── README.md
│
├── data/
│   ├── schemes.csv             102 schemes, extracted from the source PDF
│   ├── scheme_rules.csv          Mandatory/supporting rules per scheme
│   ├── translations.csv            English/Tamil UI strings
│   ├── demo_households.py            7 demo households for testing
│   ├── build_schemes.py                Regenerates schemes.csv from source (rarely re-run)
│   └── build_rules.py                    Regenerates scheme_rules.csv (rarely re-run)
│
├── database/
│   ├── thittam_arivom.db      SQLite database (built from the 3 CSVs above)
│   ├── build_database.py        Rebuilds the .db from the CSVs
│   └── db_access.py               Read-only data access + household/recommendation writes
│
├── logic/
│   ├── recommendation_engine.py   Mandatory gates, scoring, priority bands
│   └── validation.py                Condition-evaluation helpers (age ranges, operators)
│
├── ui/
│   ├── components.py            Scheme cards, directory cards, progress bar
│   └── styles.py                   Bilingual label lookup, priority badges, CSS
│
├── pages/
│   ├── home.py, questionnaire.py, results.py, scheme_details.py,
│   └── community.py, directory.py, demo.py
│
└── tests/
    └── test_recommendations.py   18 automated tests (mandatory gates, scoring, exclusions)
```

## 3. How to run it locally

```bash
cd ThittamArivom
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).
On your phone (same Wi-Fi network), use the "Network URL" Streamlit also prints.

To run the automated tests:

```bash
python3 tests/test_recommendations.py
```

## 4. How the recommendation engine works

For every **recommendable** scheme (i.e. not an umbrella entry, not
category-specific, not community-level — those are handled separately):

1. **Mandatory conditions are hard gates.** If a mandatory condition is
   answered and it fails, the scheme is excluded from the ranked results
   entirely — no amount of supporting-condition matching can promote it.
2. If all mandatory conditions pass, the **relevance score** is the sum of the
   weights of every matched rule (mandatory + supporting), capped at 100.
   A passed mandatory gate contributes a baseline of 60 points on its own
   (reflecting "clearly matches the target group, needs verification");
   supporting evidence pushes well-matched schemes into HIGH (80–100).
3. **PERSONAL** schemes (e.g. Pudhumai Penn Thittam) are evaluated per family
   member — the result names the specific person it applies to.
   **HOUSEHOLD** / **BOTH** schemes are evaluated at household level: a
   member-level condition (e.g. "pregnant or lactating") is satisfied if
   *any* family member matches it, and that member is named in the reason.
4. Every recommendation carries its list of matched reasons (in plain
   language) and any unmatched supporting conditions, shown as "needs
   verification."

## 5. Priority bands

| Score | Priority | Meaning |
|---|---|---|
| 80–100 | **HIGH** | Clearly matches the main target group; the scheme addresses a need identified in the questionnaire |
| 60–79 | **MEDIUM** | Appears relevant, but eligibility needs further verification |
| 40–59 | **LOW** | Some relevance, but the connection is weak or information is limited |
| <40 | Hidden by default | Shown only in the "not currently matched" / directory views |

This is a **relevance score**, not an eligibility percentage — the app never
states a household "is eligible."

## 6. Known V1 limitations (carried over honestly from the source data)

- The source PDF gives almost no income thresholds, land-size cutoffs, or age
  bands for most schemes — only target-group text. Scoring is real but coarse
  until more granular criteria are supplied per scheme.
- No benefit amount is available in the source for most schemes (the Girl
  Child Protection Scheme is the one exception, with ₹50,000/₹25,000 stated).
- No official URLs, documents, or application steps are available in the
  source for any scheme — these fields read "Not available in source" and
  should be filled in as they're verified.
- Some schemes needed an *invented* age band to score meaningfully (e.g.
  PM-SYM, Atal Pension Yojana). Per your instruction not to invent
  eligibility conditions, these age bands were **removed** in this version —
  those schemes score on their sourced mandatory condition only, so they may
  appear more broadly than an official age-restricted scheme actually would.
  This is called out in each such scheme's rule description.
- UYEGP ("Unemployed Youth Employment Generation Programme") is excluded from
  scoring entirely in V1: the source names "unemployed youth" as the target,
  but the questionnaire has no sourced field for employment status, and using
  occupation or an invented age range as a proxy would mean guessing. It
  remains in the scheme directory, flagged "More information required."
- ~9 umbrella entries (e.g. "TN Differently Abled Welfare Schemes") bundle
  multiple named benefits with no individual eligibility detail — kept in the
  directory only, never scored, per the Phase 2 decision.
- Tamil translations exist only for the core navigation/results strings in
  `translations.csv` and for scheme names the source itself gave in Tamil.
  Scheme descriptions/benefits are shown in English until Tamil text is
  supplied — no translation is invented.

## 7. How to update scheme data

Everything lives in `data/schemes.csv`, `data/scheme_rules.csv`, and
`data/translations.csv`. Edit those directly, or edit `build_schemes.py` /
`build_rules.py` and re-run them, then rebuild the database:

```bash
cd database
python3 build_database.py
```

No Python code elsewhere needs to change to update scheme text, weights, or
translations.

## 8. Privacy

The app does not collect Aadhaar numbers, bank account numbers, OTPs,
passwords, or exact GPS location. It asks yes/no questions ("Do you have a
bank account?") rather than the sensitive data itself. Health-related
questions are self-declared checkboxes only ("Does anyone have a long-term
health condition?") — no diagnosis or medical detail is collected or stored.
Household data is stored locally in the SQLite database with a generated
household ID, not a name.

## 9. Disclaimer

Thittam Arivom is an informational tool developed for community awareness.
It is not an official government application. Final eligibility and benefit
approval are determined by the relevant government authority.


## 6. Final questionnaire changes

The current implementation uses a three-step household flow:

1. Basic information for the household head and household size.
2. Household information and agriculture information.
3. Review and recommendations.

There is no separate family-members page in the live questionnaire.

### Input behavior

- The interface starts in English.
- A global **English / தமிழ்** language switch is available on every page.
- Annual household income is collected as visible rupee ranges.
- The income ranges are input bands, not claimed official eligibility thresholds.
- Household yes/no fields default to **Yes**, but the user can change them.
- Agricultural land is asked before agricultural pump questions.
- Land size, pumpset, pump type, and farming activity are shown only when agricultural land is `Yes`.
- When agricultural land is `No`, agriculture-dependent fields are cleared so stale values cannot affect recommendations.

### Recommendation integrity

The recommendation engine remains rule-driven from `scheme_rules.csv`. Mandatory rules remain hard gates and supporting rules contribute weighted relevance points. The application does not convert the score into an official eligibility percentage.

The results also show conservative data-quality information:
- **Recommendation status:** whether the record is suitable for the rule-based recommendation flow.
- **Verification status:** whether an actual official URL is present in the project data.

If an official URL is not present in the dataset, the app explicitly tells the user to verify the current scheme details with the relevant government department. It does not invent official sources.

Because the live questionnaire no longer collects detailed information about every family member, recommendations requiring detailed individual-member information should be treated as requiring additional verification.
