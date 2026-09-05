"""
Automated tests for the recommendation engine.
Run with: python3 tests/test_recommendations.py
(No external test framework required, to keep V1 dependencies minimal.)
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.recommendation_engine import generate_recommendations, evaluate_scheme

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_data():
    schemes_df = pd.read_csv(os.path.join(DATA_DIR, "schemes.csv"))
    for col in ["is_umbrella_entry", "requires_category", "recommendable", "priority_enabled"]:
        schemes_df[col] = schemes_df[col].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
    rules_df = pd.read_csv(os.path.join(DATA_DIR, "scheme_rules.csv"))
    rules_df["mandatory"] = rules_df["mandatory"].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
    rules_df["weight"] = pd.to_numeric(rules_df["weight"], errors="coerce").fillna(0).astype(int)
    return schemes_df, rules_df


def base_household(**overrides):
    h = {
        "income_range": "Low", "family_size": 1, "land_owned": "No", "agricultural_pump": "No",
        "electricity": "Yes", "household_has_lpg": "Yes", "ration_card": "Yes", "bank_account": "Yes",
        "health_insurance": "No", "house_type": "Pucca", "house_status": "Owned",
        "household_has_toilet": "Yes", "water_access": "Yes", "rooftop_solar": "No",
        "woman_headed": "No", "household_state": "Tamil Nadu",
    }
    h.update(overrides)
    return h


def base_member(**overrides):
    m = {
        "relation": "Head of Household", "age": 35, "gender": "Male", "marital_status": "Married",
        "occupation": "Daily wage worker", "student": "No", "disability": "No", "chronic_illness": "No",
        "pregnant_or_lactating": "No", "widow": "No", "shg_member": "No",
    }
    m.update(overrides)
    return m


def run(name, fn):
    try:
        fn()
        print(f"PASS - {name}")
        return True
    except AssertionError as e:
        print(f"FAIL - {name}: {e}")
        return False


def test_farmer_matches_pm_kisan():
    schemes_df, rules_df = load_data()
    household = base_household(land_owned="Yes")
    members = [base_member(occupation="Farmer")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    ids = [r["scheme_id"] for r in ranked]
    assert "C001" in ids, "PM-KISAN should appear for a landholding farmer"


def test_non_farmer_does_not_get_pm_kisan_as_high():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(occupation="Homemaker")]
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    ids_ranked = [r["scheme_id"] for r in ranked]
    ids_not_matched = [r["scheme_id"] for r in not_matched]
    assert "C001" not in ids_ranked, "Non-farmer should not see PM-KISAN in ranked results"
    assert "C001" in ids_not_matched, "PM-KISAN should be in the not-matched list for a non-farmer"


def test_student_gets_relevant_scholarship():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [
        base_member(occupation="Homemaker"),
        base_member(relation="Daughter", age=17, gender="Female", occupation="Student",
                    student="Yes"),
    ]
    members[1]["education_level"] = "Entering higher education"
    members[1]["school_type"] = "Government"
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    match = [r for r in ranked if r["scheme_id"] == "TN002"]
    assert match, "Pudhumai Penn Thittam should match a girl entering higher education from govt school"
    assert match[0]["relevant_member_label"] == "Daughter", "Should attribute to the daughter, not the household"


def test_elderly_person_matches_ignoaps():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(age=70)]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    ids = [r["scheme_id"] for r in ranked]
    assert "C032" in ids, "Elderly household member should match IGNOAPS"


def test_pregnant_woman_matches_pmmvy():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(gender="Female", pregnant_or_lactating="Yes")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    ids = [r["scheme_id"] for r in ranked]
    assert "C022" in ids, "Pregnant/lactating member should match PMMVY"


def test_disability_gates_igndps():
    schemes_df, rules_df = load_data()
    household = base_household()
    members_yes = [base_member(disability="Yes")]
    members_no = [base_member(disability="No")]
    ranked_yes, _ = generate_recommendations(schemes_df, rules_df, household, members_yes)
    ranked_no, not_matched_no = generate_recommendations(schemes_df, rules_df, household, members_no)
    assert "C034" in [r["scheme_id"] for r in ranked_yes]
    assert "C034" not in [r["scheme_id"] for r in ranked_no]
    assert "C034" in [r["scheme_id"] for r in not_matched_no]


def test_artisan_matches_vishwakarma():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(occupation="Artisan")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C039" in [r["scheme_id"] for r in ranked]


def test_street_vendor_matches_svanidhi():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(occupation="Street vendor")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C038" in [r["scheme_id"] for r in ranked]


def test_small_business_owner_matches_mudra():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(occupation="Small business owner")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C041" in [r["scheme_id"] for r in ranked]


def test_household_with_children_matches_poshan():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [
        base_member(),
        base_member(relation="Son", age=10, occupation="Student", student="Yes", school_type="Government"),
    ]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C075" in [r["scheme_id"] for r in ranked]


def test_household_without_children_does_not_get_poshan():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member()]
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C075" not in [r["scheme_id"] for r in ranked]


def test_farmer_with_pump_matches_kusum():
    schemes_df, rules_df = load_data()
    household = base_household(agricultural_pump="Yes", pump_type="Diesel")
    members = [base_member(occupation="Farmer")]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    kusum = [r for r in ranked if r["scheme_id"] == "C074"]
    assert kusum and kusum[0]["priority"] == "HIGH", "Farmer with a pump should get PM-KUSUM as HIGH priority"


def test_no_electricity_excludes_surya_ghar():
    schemes_df, rules_df = load_data()
    household = base_household(electricity="No")
    members = [base_member()]
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C073" not in [r["scheme_id"] for r in ranked]
    assert "C073" in [r["scheme_id"] for r in not_matched]


def test_no_bank_account_matches_pmjdy():
    schemes_df, rules_df = load_data()
    household = base_household(bank_account="No")
    members = [base_member()]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C042" in [r["scheme_id"] for r in ranked]


def test_mixed_family_gets_multiple_categories():
    schemes_df, rules_df = load_data()
    household = base_household(land_owned="Yes")
    members = [
        base_member(occupation="Farmer", age=48),
        base_member(relation="Daughter", age=19, gender="Female", occupation="Student",
                    student="Yes", education_level="Entering higher education", school_type="Government"),
        base_member(relation="Grandmother", age=71, gender="Female", widow="Yes"),
    ]
    ranked, _ = generate_recommendations(schemes_df, rules_df, household, members)
    ids = [r["scheme_id"] for r in ranked]
    assert "C001" in ids  # farmer -> PM-KISAN
    assert "TN002" in ids  # daughter -> Pudhumai Penn
    assert "C032" in ids  # grandmother -> IGNOAPS


def test_community_schemes_never_appear_in_personal_results():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member()]
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    all_ids = [r["scheme_id"] for r in ranked] + [r["scheme_id"] for r in not_matched]
    community_ids = set(schemes_df[schemes_df["scheme_type"] == "COMMUNITY"]["scheme_id"])
    assert not (set(all_ids) & community_ids), "Community-level schemes must never appear in personal results"


def test_category_specific_schemes_excluded_from_default_flow():
    schemes_df, rules_df = load_data()
    household = base_household()
    members = [base_member(occupation="Farmer")]
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    all_ids = [r["scheme_id"] for r in ranked] + [r["scheme_id"] for r in not_matched]
    category_specific_ids = set(schemes_df[schemes_df["requires_category"] == True]["scheme_id"])
    assert not (set(all_ids) & category_specific_ids), "Category-specific schemes must be excluded from the default flow"


def test_mandatory_condition_overrides_score():
    """A scheme with a failed mandatory condition must never appear as HIGH/MEDIUM/LOW,
    no matter how many supporting conditions would otherwise match."""
    schemes_df, rules_df = load_data()
    household = base_household(land_owned="Yes", bank_account="Yes", ration_card="Yes")
    members = [base_member(occupation="Homemaker")]  # not a farmer -> mandatory gate fails
    ranked, not_matched = generate_recommendations(schemes_df, rules_df, household, members)
    assert "C001" not in [r["scheme_id"] for r in ranked]
    matched_not = [r for r in not_matched if r["scheme_id"] == "C001"]
    assert matched_not and matched_not[0]["status"] == "NOT_CURRENTLY_MATCHED"


if __name__ == "__main__":
    tests = [
        test_farmer_matches_pm_kisan,
        test_non_farmer_does_not_get_pm_kisan_as_high,
        test_student_gets_relevant_scholarship,
        test_elderly_person_matches_ignoaps,
        test_pregnant_woman_matches_pmmvy,
        test_disability_gates_igndps,
        test_artisan_matches_vishwakarma,
        test_street_vendor_matches_svanidhi,
        test_small_business_owner_matches_mudra,
        test_household_with_children_matches_poshan,
        test_household_without_children_does_not_get_poshan,
        test_farmer_with_pump_matches_kusum,
        test_no_electricity_excludes_surya_ghar,
        test_no_bank_account_matches_pmjdy,
        test_mixed_family_gets_multiple_categories,
        test_community_schemes_never_appear_in_personal_results,
        test_category_specific_schemes_excluded_from_default_flow,
        test_mandatory_condition_overrides_score,
    ]
    results = [run(t.__name__, t) for t in tests]
    print(f"\n{sum(results)}/{len(results)} tests passed")
    if not all(results):
        sys.exit(1)
