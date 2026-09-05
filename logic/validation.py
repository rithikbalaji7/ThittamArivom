"""
Condition-evaluation helpers used by the recommendation engine.
Kept separate so the engine's control flow stays readable.
"""
import re


def parse_age_range(value: str):
    """
    Parses condition_value strings used for age_band rules in scheme_rules.csv:
      "18-40" -> (18, 40)
      "50+"   -> (50, None)
    Returns (low, high) where high=None means "and above".
    """
    value = value.strip()
    if value.endswith("+"):
        return int(value[:-1]), None
    m = re.match(r"^(\d+)\s*-\s*(\d+)$", value)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None


def age_matches(age, condition_value: str) -> bool:
    if age is None:
        return False
    low, high = parse_age_range(condition_value)
    if low is None:
        return False
    if high is None:
        return age >= low
    return low <= age <= high


def values_equal(actual, expected) -> bool:
    if actual is None:
        return False
    return str(actual).strip().lower() == str(expected).strip().lower()


def value_in_list(actual, condition_value: str) -> bool:
    if actual is None:
        return False
    options = [v.strip().lower() for v in condition_value.split(",")]
    return str(actual).strip().lower() in options


def truthy(value) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ["yes", "true", "1"]


def evaluate_operator(operator: str, actual, condition_value: str) -> bool:
    if operator == "=":
        return values_equal(actual, condition_value)
    if operator == "!=":
        return not values_equal(actual, condition_value)
    if operator == "in":
        return value_in_list(actual, condition_value)
    return False
