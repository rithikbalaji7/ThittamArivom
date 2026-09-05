"""
Rule-based recommendation engine.

Reads scheme_rules from the existing scheme_rules table/CSV only — no rule is
invented here. For each recommendable scheme:

 1. Mandatory rules are hard gates. If a mandatory condition is answered and
    fails, the scheme is excluded from the ranked/high-priority results
    (status = NOT_CURRENTLY_MATCHED), no matter how many supporting
    conditions happen to match.
 2. If every mandatory rule passes, the relevance score is the sum of the
    weights of every matched rule (mandatory + supporting), capped at 100.
 3. Priority bands (fixed, per spec): 80-100 HIGH, 60-79 MEDIUM, 40-59 LOW,
    <40 hidden by default.
 4. PERSONAL schemes are evaluated per family member (household fields are
    still visible to a member's context). HOUSEHOLD / BOTH schemes are
    evaluated at household level, where member-level fields are satisfied if
    ANY family member matches (and that member is recorded in the reason).
 5. CATEGORY_SPECIFIC and COMMUNITY schemes, and non-recommendable /
    umbrella / generic-label schemes, are never scored here — they are
    handled separately (directory / community views).
"""
from logic.validation import evaluate_operator, age_matches, truthy

MEMBER_LEVEL_FIELDS = {
    "occupation", "gender", "marital_status", "student", "education_level",
    "school_type", "disability", "chronic_illness", "pregnant_or_lactating",
    "widow", "shg_member",
}

HOUSEHOLD_LEVEL_FIELDS = {
    "income_range", "family_size", "land_owned", "land_size", "agricultural_pump",
    "pump_type", "farming_activity", "electricity", "household_has_lpg", "ration_card",
    "bank_account", "health_insurance", "house_type", "house_status",
    "household_has_toilet", "water_access", "rooftop_solar", "woman_headed",
    "household_state",
}

DERIVED_FIELDS = {"age_band", "age_elderly", "has_children", "girl_child_count"}


def _member_field_value(member, field):
    if field == "age_elderly":
        return truthy(member.get("age", 0) is not None and member.get("age", 0) >= 60)
    return member.get(field)


def _household_derived_value(field, household, members):
    if field == "has_children":
        return any((m.get("age") is not None and m.get("age") < 18) for m in members)
    if field == "girl_child_count":
        count = sum(1 for m in members if truthy(m.get("age") is not None and m.get("age") < 18)
                    and str(m.get("gender", "")).strip().lower() == "female")
        return str(count)
    return None


def _evaluate_rule_for_member(rule, household, member):
    """Evaluate one rule against a single merged (household + member) context. Used for PERSONAL schemes."""
    field = rule["condition_field"]
    if field == "age_band":
        matched = age_matches(member.get("age"), rule["condition_value"])
    elif field in DERIVED_FIELDS:
        value = _member_field_value(member, field) if field == "age_elderly" else None
        matched = evaluate_operator(rule["condition_operator"], value, rule["condition_value"])
    elif field in HOUSEHOLD_LEVEL_FIELDS:
        matched = evaluate_operator(rule["condition_operator"], household.get(field), rule["condition_value"])
    else:
        # member-level field (occupation, gender, student, disability, etc.)
        matched = evaluate_operator(rule["condition_operator"], member.get(field), rule["condition_value"])
    return matched


def _evaluate_rule_for_household(rule, household, members):
    """Evaluate one rule at household level: household fields directly, member fields as 'any member matches'."""
    field = rule["condition_field"]

    if field == "age_band":
        for m in members:
            if age_matches(m.get("age"), rule["condition_value"]):
                return True, [m]
        return False, []

    if field in ("age_elderly", "has_children", "girl_child_count"):
        if field == "age_elderly":
            matching = [m for m in members if truthy(m.get("age") is not None and m.get("age") >= 60)]
            return (len(matching) > 0), matching
        value = _household_derived_value(field, household, members)
        matched = evaluate_operator(rule["condition_operator"], value, rule["condition_value"])
        return matched, []

    if field in HOUSEHOLD_LEVEL_FIELDS:
        matched = evaluate_operator(rule["condition_operator"], household.get(field), rule["condition_value"])
        return matched, []

    # member-level field: matches if ANY member satisfies it
    matching_members = []
    for m in members:
        if evaluate_operator(rule["condition_operator"], m.get(field), rule["condition_value"]):
            matching_members.append(m)
    return (len(matching_members) > 0), matching_members


def _priority_for_score(score):
    if score >= 80:
        return "HIGH"
    if score >= 60:
        return "MEDIUM"
    if score >= 40:
        return "LOW"
    return "HIDDEN"


def evaluate_scheme(scheme_row, rules_for_scheme, household, members):
    """
    Returns a list of recommendation dicts (usually one, but PERSONAL schemes
    can produce one per qualifying member).
    """
    mandatory_rules = [r for r in rules_for_scheme if r["mandatory"]]
    supporting_rules = [r for r in rules_for_scheme if not r["mandatory"]]
    scheme_type = scheme_row["scheme_type"]

    results = []

    if scheme_type == "PERSONAL":
        for member in members:
            mandatory_ok = True
            reasons = []
            missing = []
            for r in mandatory_rules:
                if _evaluate_rule_for_member(r, household, member):
                    reasons.append(r["description"])
                else:
                    mandatory_ok = False
            if not mandatory_ok:
                continue  # this member doesn't qualify; skip silently, don't spam "not matched" per member

            score = sum(r["weight"] for r in mandatory_rules)  # matched mandatory contributes to score
            for r in supporting_rules:
                if _evaluate_rule_for_member(r, household, member):
                    score += r["weight"]
                    reasons.append(r["description"])
                else:
                    missing.append(r["description"])
            score = min(100, score)
            results.append({
                "scheme_id": scheme_row["scheme_id"],
                "relevant_member_id": member.get("member_id"),
                "relevant_member_label": member.get("relation", "Family member"),
                "score": score,
                "priority": _priority_for_score(score),
                "status": "Potentially Relevant",
                "reasons": reasons,
                "missing_information": missing,
            })
        return results

    # HOUSEHOLD / BOTH
    mandatory_ok = True
    reasons = []
    missing = []
    matched_members_all = []
    for r in mandatory_rules:
        matched, matched_members = _evaluate_rule_for_household(r, household, members)
        if matched:
            reasons.append(r["description"])
            matched_members_all.extend(matched_members)
        else:
            mandatory_ok = False

    if not mandatory_ok:
        return [{
            "scheme_id": scheme_row["scheme_id"],
            "relevant_member_id": None,
            "relevant_member_label": "Household",
            "score": 0,
            "priority": "HIDDEN",
            "status": "NOT_CURRENTLY_MATCHED",
            "reasons": [],
            "missing_information": ["Mandatory condition not met: " + r["description"] for r in mandatory_rules],
        }]

    score = sum(r["weight"] for r in mandatory_rules)
    for r in supporting_rules:
        matched, matched_members = _evaluate_rule_for_household(r, household, members)
        if matched:
            score += r["weight"]
            reasons.append(r["description"])
            matched_members_all.extend(matched_members)
        else:
            missing.append(r["description"])
    score = min(100, score)

    member_labels = sorted({m.get("relation", "Family member") for m in matched_members_all})
    relevant_label = "Household" if not member_labels else "Household (" + ", ".join(member_labels) + ")"

    results.append({
        "scheme_id": scheme_row["scheme_id"],
        "relevant_member_id": None,
        "relevant_member_label": relevant_label,
        "score": score,
        "priority": _priority_for_score(score),
        "status": "Potentially Relevant",
        "reasons": reasons,
        "missing_information": missing,
    })
    return results


def _data_quality_for_scheme(scheme_row, rules_for_scheme):
    """
    Project-level viability/credibility check.

    This is deliberately conservative:
    - viability means the record is allowed into the recommendation engine
      and has at least one rule;
    - verification status never claims official eligibility unless an actual
      official URL is present in the dataset.
    """
    recommendable = bool(scheme_row.get("recommendable", False))
    scheme_type = str(scheme_row.get("scheme_type", "")).upper()
    umbrella = bool(scheme_row.get("is_umbrella_entry", False))
    category_specific = bool(scheme_row.get("requires_category", False))
    has_rules = len(rules_for_scheme) > 0

    viable = (
        recommendable
        and not umbrella
        and not category_specific
        and scheme_type not in {"COMMUNITY", "CATEGORY_SPECIFIC"}
        and has_rules
    )

    official_source = str(scheme_row.get("official_source", "") or "").strip()
    has_real_url = official_source.startswith(("http://", "https://"))

    verification_status = (
        "Official source recorded in project data; verify current eligibility before applying."
        if has_real_url
        else "Official source URL is not provided in the project source data; verify with the relevant department."
    )

    viability_status = (
        "Recommendation-ready rule set"
        if viable
        else "Directory / manual-verification record"
    )

    return verification_status, viability_status


def generate_recommendations(schemes_df, rules_df, household, members):
    """
    Top-level entry point. Only scores schemes that are recommendable, not
    umbrella entries, and not CATEGORY_SPECIFIC / COMMUNITY (those are
    handled by separate views).
    Returns (ranked_results, not_matched_results) as lists of dicts, each
    enriched with scheme_name / category / government for display.
    """
    scoreable = schemes_df[
        (schemes_df["recommendable"] == True)
        & (schemes_df["is_umbrella_entry"] == False)
        & (~schemes_df["scheme_type"].isin(["COMMUNITY", "CATEGORY_SPECIFIC"]))
    ]

    all_results = []
    for _, scheme_row in scoreable.iterrows():
        rules_for_scheme = rules_df[rules_df["scheme_id"] == scheme_row["scheme_id"]].to_dict("records")
        if not rules_for_scheme:
            continue
        recs = evaluate_scheme(scheme_row, rules_for_scheme, household, members)
        verification_status, viability_status = _data_quality_for_scheme(
            scheme_row, rules_for_scheme
        )
        for rec in recs:
            rec["verification_status"] = verification_status
            rec["viability_status"] = viability_status
            rec["scheme_name"] = scheme_row["scheme_name"]
            rec["category"] = scheme_row["category"]
            rec["government"] = scheme_row["government"]
            rec["benefit"] = scheme_row["benefit"]
            all_results.append(rec)

    ranked = [r for r in all_results if r["priority"] in ("HIGH", "MEDIUM", "LOW")]
    not_matched = [r for r in all_results if r["status"] == "NOT_CURRENTLY_MATCHED"]

    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    ranked.sort(key=lambda r: (priority_order[r["priority"]], -r["score"]))

    return ranked, not_matched
