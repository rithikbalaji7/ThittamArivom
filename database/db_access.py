"""
Read-only access to the existing thittam_arivom.db (built in Phase 2).
This module never writes to schemes / scheme_rules / translations.
It DOES write new rows to households / family_members / recommendations
when a volunteer submits a questionnaire (that data is new, per household,
not scheme data).
"""
import os
import sqlite3
import pandas as pd
import streamlit as st

CACHE = getattr(st, "cache_data", None) or st.cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "thittam_arivom.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@CACHE
def load_schemes() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM schemes", conn)
    conn.close()
    # normalize boolean-ish text columns coming from CSV import ('True'/'False'/'')
    for col in ["is_umbrella_entry", "requires_category", "recommendable", "priority_enabled"]:
        df[col] = df[col].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
    return df


@CACHE
def load_scheme_rules() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM scheme_rules", conn)
    conn.close()
    df["mandatory"] = df["mandatory"].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce").fillna(0).astype(int)
    return df


@CACHE
def load_translations() -> dict:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM translations", conn)
    conn.close()
    return {row["key"]: {"en": row["english"], "ta": row["tamil"]} for _, row in df.iterrows()}


def save_household_record(household_id: str, household: dict, members: list):
    """Persist a submitted household + family members into the DB (new data, not scheme data)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM family_members WHERE household_id=?", (household_id,))
    cur.execute("DELETE FROM households WHERE household_id=?", (household_id,))

    h_cols = ["household_id", "language", "income_range", "family_size", "land_owned",
              "land_size", "agricultural_pump", "pump_type", "farming_activity", "electricity",
              "household_has_lpg", "ration_card", "bank_account", "health_insurance",
              "house_type", "house_status", "household_has_toilet", "water_access",
              "rooftop_solar", "woman_headed", "household_state"]
    values = [household_id] + [household.get(c) for c in h_cols[1:]]
    placeholders = ",".join(["?"] * len(h_cols))
    cur.execute(f"INSERT INTO households ({','.join(h_cols)}) VALUES ({placeholders})", values)

    m_cols = ["household_id", "relation", "age", "gender", "marital_status", "occupation",
              "student", "education_level", "school_type", "disability", "chronic_illness",
              "pregnant_or_lactating", "widow", "shg_member"]
    for m in members:
        values = [household_id] + [m.get(c) for c in m_cols[1:]]
        placeholders = ",".join(["?"] * len(m_cols))
        cur.execute(f"INSERT INTO family_members ({','.join(m_cols)}) VALUES ({placeholders})", values)

    conn.commit()
    conn.close()


def save_recommendations(household_id: str, recs: list):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM recommendations WHERE household_id=?", (household_id,))
    for r in recs:
        cur.execute(
            """INSERT INTO recommendations
               (household_id, scheme_id, relevant_member_id, score, priority, status, reasons, missing_information)
               VALUES (?,?,?,?,?,?,?,?)""",
            (household_id, r["scheme_id"], r.get("relevant_member_id"), r["score"],
             r["priority"], r["status"], "; ".join(r["reasons"]), "; ".join(r["missing_information"]))
        )
    conn.commit()
    conn.close()
