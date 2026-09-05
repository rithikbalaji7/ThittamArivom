import sqlite3
import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
DB_PATH = os.path.join(BASE, "database", "thittam_arivom.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE schemes (
    scheme_id           TEXT PRIMARY KEY,
    scheme_name          TEXT NOT NULL,
    tamil_name             TEXT,
    government              TEXT NOT NULL,
    category                 TEXT,
    scheme_type                TEXT NOT NULL,
    target_group_text            TEXT,
    description                    TEXT,
    benefit                          TEXT,
    eligibility_text                   TEXT,
    documents                            TEXT,
    application_route                      TEXT,
    official_source                          TEXT,
    last_verified                              DATE,
    is_umbrella_entry                            BOOLEAN NOT NULL DEFAULT 0,
    requires_category                              BOOLEAN NOT NULL DEFAULT 0,
    recommendable                                    BOOLEAN NOT NULL DEFAULT 1,
    priority_enabled                                   BOOLEAN NOT NULL DEFAULT 1,
    source_flag                                          TEXT
);

CREATE TABLE scheme_rules (
    rule_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_id             TEXT NOT NULL REFERENCES schemes(scheme_id),
    condition_field         TEXT NOT NULL,
    condition_operator        TEXT NOT NULL,
    condition_value              TEXT NOT NULL,
    condition_type                 TEXT NOT NULL CHECK(condition_type IN ('PRIMARY','SUPPORTING')),
    weight                            INTEGER NOT NULL,
    mandatory                           BOOLEAN NOT NULL,
    description                           TEXT
);

CREATE TABLE households (
    household_id      TEXT PRIMARY KEY,
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    language                TEXT,
    occupation                TEXT,
    income_range                 TEXT,
    family_size                    INTEGER,
    land_owned                       BOOLEAN,
    land_size                          TEXT,
    agricultural_pump                    BOOLEAN,
    pump_type                              TEXT,
    farming_activity                         TEXT,
    electricity                                BOOLEAN,
    household_has_lpg                            BOOLEAN,
    ration_card                                    BOOLEAN,
    bank_account                                     BOOLEAN,
    health_insurance                                   BOOLEAN,
    house_type                                           TEXT,
    house_status                                           TEXT,
    household_has_toilet                                     BOOLEAN,
    water_access                                               BOOLEAN,
    rooftop_solar                                                BOOLEAN,
    woman_headed                                                   BOOLEAN,
    household_state                                                  TEXT DEFAULT 'Tamil Nadu'
);

CREATE TABLE family_members (
    member_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id          TEXT NOT NULL REFERENCES households(household_id),
    relation                TEXT,
    age                        INTEGER,
    age_band                     TEXT,
    gender                          TEXT,
    marital_status                    TEXT,
    occupation                          TEXT,
    student                               BOOLEAN,
    education_level                         TEXT,
    school_type                               TEXT,
    disability                                  BOOLEAN,
    chronic_illness                               BOOLEAN,
    pregnant_or_lactating                           BOOLEAN,
    widow                                             BOOLEAN,
    shg_member                                          BOOLEAN,
    age_elderly                                           BOOLEAN
);

CREATE TABLE recommendations (
    recommendation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id             TEXT NOT NULL REFERENCES households(household_id),
    scheme_id                   TEXT NOT NULL REFERENCES schemes(scheme_id),
    relevant_member_id             INTEGER REFERENCES family_members(member_id),
    score                             INTEGER,
    priority                            TEXT,
    status                                 TEXT,
    reasons                                  TEXT,
    missing_information                        TEXT,
    generated_at                                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE translations (
    key       TEXT PRIMARY KEY,
    english     TEXT,
    tamil          TEXT
);
""")

def load_csv(path, table, columns):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        placeholders = ",".join(["?"] * len(columns))
        col_list = ",".join(columns)
        for row in reader:
            values = [row[c] for c in columns]
            cur.execute(f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})", values)

load_csv(os.path.join(DATA, "schemes.csv"), "schemes",
    ["scheme_id","scheme_name","tamil_name","government","category","scheme_type",
     "target_group_text","description","benefit","eligibility_text","documents",
     "application_route","official_source","is_umbrella_entry","requires_category",
     "recommendable","priority_enabled","source_flag"])

load_csv(os.path.join(DATA, "scheme_rules.csv"), "scheme_rules",
    ["scheme_id","condition_field","condition_operator","condition_value",
     "condition_type","weight","mandatory","description"])

load_csv(os.path.join(DATA, "translations.csv"), "translations", ["key","english","tamil"])

conn.commit()

# quick counts for confirmation
for t in ["schemes","scheme_rules","translations"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {n} rows")

conn.close()
print(f"\nDatabase built at {DB_PATH}")
