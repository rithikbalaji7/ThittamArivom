from typing import Dict


sessions: Dict[str, dict] = {}


def get_session(phone: str):
    if phone not in sessions:
        sessions[phone] = {
            "language": None,
            "step": "start",
            "data": {}
        }

    return sessions[phone]


def reset_session(phone: str):
    sessions[phone] = {
        "language": None,
        "step": "start",
        "data": {}
    }


def process_message(phone: str, message: str):

    message = message.strip()

    session = get_session(phone)

    # -------------------------
    # START
    # -------------------------

    if session["step"] == "start":

        if message.upper() in ["START", "HI", "HELLO"]:

            session["step"] = "language"

            return (
                "THITTAMARIVOM\n\n"
                "Choose language:\n"
                "1 - English\n"
                "2 - தமிழ்"
            )

        return "Reply START to begin ThittamArivom."

    # -------------------------
    # LANGUAGE
    # -------------------------

    if session["step"] == "language":

        if message == "1":

            session["language"] = "en"
            session["step"] = "age"

            return "Enter your age:"

        elif message == "2":

            session["language"] = "ta"
            session["step"] = "age"

            return "உங்கள் வயதை உள்ளிடவும்:"

        return "Reply 1 for English or 2 for Tamil."

    # -------------------------
    # AGE
    # -------------------------

    if session["step"] == "age":

        try:
            age = int(message)

            if age < 1 or age > 120:
                raise ValueError

        except ValueError:

            if session["language"] == "ta":
                return "சரியான வயதை உள்ளிடவும்."

            return "Please enter a valid age."

        session["data"]["age"] = age
        session["step"] = "occupation"

        if session["language"] == "ta":
            return (
                "உங்கள் தொழிலை தேர்வு செய்யவும்:\n"
                "1 - விவசாயி\n"
                "2 - கூலி தொழிலாளர்\n"
                "3 - சுய தொழில்\n"
                "4 - மற்றவை"
            )

        return (
            "Select your occupation:\n"
            "1 - Farmer\n"
            "2 - Labourer\n"
            "3 - Self-employed\n"
            "4 - Other"
        )

    # -------------------------
    # OCCUPATION
    # -------------------------

    if session["step"] == "occupation":

        occupations = {
            "1": "farmer",
            "2": "labourer",
            "3": "self_employed",
            "4": "other"
        }

        if message not in occupations:

            if session["language"] == "ta":
                return "1, 2, 3 அல்லது 4 என்பதை தேர்வு செய்யவும்."

            return "Please reply with 1, 2, 3 or 4."

        session["data"]["occupation"] = occupations[message]

        session["step"] = "income"

        if session["language"] == "ta":
            return "உங்கள் குடும்பத்தின் ஆண்டு வருமானத்தை உள்ளிடவும்:"

        return "Enter your annual household income in ₹:"

    # -------------------------
    # INCOME
    # -------------------------

    if session["step"] == "income":

        try:
            income = float(message.replace(",", ""))

            if income < 0:
                raise ValueError

        except ValueError:

            if session["language"] == "ta":
                return "சரியான வருமானத்தை உள்ளிடவும்."

            return "Please enter a valid income."

        session["data"]["income"] = income

        session["step"] = "members"

        if session["language"] == "ta":
            return "உங்கள் குடும்பத்தில் எத்தனை பேர் உள்ளனர்?"

        return "How many people are in your household?"

    # -------------------------
    # HOUSEHOLD MEMBERS
    # -------------------------

    if session["step"] == "members":

        try:
            members = int(message)

            if members < 1 or members > 50:
                raise ValueError

        except ValueError:

            if session["language"] == "ta":
                return "சரியான குடும்ப உறுப்பினர் எண்ணிக்கையை உள்ளிடவும்."

            return "Please enter a valid household member count."

        session["data"]["members"] = members

        session["step"] = "result"

        return generate_result(session)

    # -------------------------
    # RESULT
    # -------------------------

    if session["step"] == "result":

        if message.upper() == "START":
            reset_session(phone)
            return process_message(phone, "START")

        return (
            "Reply START to check schemes again."
        )


def generate_result(session):

    data = session["data"]

    age = data["age"]
    occupation = data["occupation"]
    income = data["income"]

    schemes = []

    # Example rules.
    # We will replace these with your actual
    # ThittamArivom recommendation engine.

    if occupation == "farmer":
        schemes.append("PM-KISAN")

    if income <= 300000:
        schemes.append("PMAY-G")

    schemes.append("PMJDY")

    schemes = list(dict.fromkeys(schemes))

    if session["language"] == "ta":

        result = "உங்களுக்கு பொருந்தக்கூடிய திட்டங்கள்:\n\n"

        for i, scheme in enumerate(schemes, 1):
            result += f"{i}. {scheme}\n"

        result += "\nமேலும் தகவலுக்கு திட்டத்தின் எண்ணை SMS செய்யவும்."

        return result

    result = "You may be eligible for:\n\n"

    for i, scheme in enumerate(schemes, 1):
        result += f"{i}. {scheme}\n"

    result += "\nReply with the scheme number for more information."

    return result