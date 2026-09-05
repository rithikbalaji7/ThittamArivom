"""
Builds data/scheme_rules.csv.
Only schemes with recommendable=TRUE in schemes.csv get rules (umbrella/generic/
community/category-specific schemes are directory-only and unscored in V1).

Rule design principle (per project owner's Phase 2 priority-hierarchy requirement):
- MANDATORY rules are hard gates. If a mandatory condition is answered FALSE,
  the scheme is excluded from ranked results entirely (status = NOT CURRENTLY MATCHED),
  regardless of how many supporting conditions match.
- SUPPORTING rules only add to the score AFTER all mandatory gates pass.
- Weights follow the Phase 1 default template (Primary target +30, secondary +20,
  age +15, household condition +15, income +10, additional +10) but are adjusted
  per scheme based on what the source actually specifies. Where the source gives
  only a target-group phrase and nothing else, that becomes the single mandatory
  PRIMARY condition and no supporting rules are invented.
"""
import csv

rules = []  # scheme_id, condition_field, condition_operator, condition_value, condition_type, weight, mandatory, description

def r(sid, field, op, val, ctype, weight, mandatory, desc):
    rules.append([sid, field, op, val, ctype, weight, mandatory, desc])

# ---- Agriculture ----
r("C001","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C001","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land")
r("C001","bank_account","=","Yes","SUPPORTING",20,False,"Household has a bank account (needed for direct transfer)")
r("C001","ration_card","=","Yes","SUPPORTING",20,False,"Household has a ration card on record")

r("C002","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C002","land_owned","=","Yes","SUPPORTING",40,False,"Household owns/cultivates agricultural land")
r("C002","agricultural_pump","=","Yes","SUPPORTING",10,False,"Household has active irrigation/farming inputs")

r("C003","occupation","in","Farmer,Agricultural worker,Livestock owner,Fisherman","PRIMARY",30,True,
  "Household occupation is Farmer, agricultural worker, livestock owner, or fisherman (KCC use-case)")
r("C003","land_owned","=","Yes","SUPPORTING",20,False,"Household owns agricultural land (agriculture use-case)")
r("C003","bank_account","=","Yes","SUPPORTING",20,False,"Household has a bank account")
r("C003","occupation","=","Livestock owner","SUPPORTING",20,False,"Household keeps livestock (allied-activity use-case)")
r("C003","occupation","=","Fisherman","SUPPORTING",20,False,"Household occupation is fisherman (fisheries use-case)")

r("C004","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C004","land_owned","=","Yes","SUPPORTING",20,False,"Household owns land (small/marginal profile indicator)")

r("C005","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C005","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land needing irrigation")

r("C006","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C006","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land")

r("C007","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C007","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land")

r("C008","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C008","farming_activity","=","Horticulture","SUPPORTING",40,False,"Household grows horticultural crops")

r("C009","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C009","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land")

r("C010","occupation","in","Farmer,Small business owner","PRIMARY",30,True,"Household is a farmer, FPO member, or agri-business")
r("C010","land_owned","=","Yes","SUPPORTING",30,False,"Household owns agricultural land/infrastructure")

r("C011","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C011","farming_activity","=","Organic","SUPPORTING",40,False,"Household practises organic farming")

r("C012","occupation","=","Farmer","PRIMARY",30,True,"Household is in the agriculture sector")

# ---- Housing ----
r("C013","house_status","in","Kutcha,No house,Needs housing","PRIMARY",40,True,"Household lacks pucca housing")
r("C013","ration_card","=","Yes","SUPPORTING",20,False,"Household has a ration card on record")

r("C015","household_has_toilet","=","No","PRIMARY",40,True,"Household lacks sanitation facility")
r("C016","water_access","=","No","PRIMARY",40,True,"Household lacks piped drinking water access")
r("C018","occupation","in","Daily wage worker,Agricultural worker,Unorganised worker","PRIMARY",30,True,
  "Household seeks rural wage employment")

# ---- Women & Mothers ----
r("C022","pregnant_or_lactating","=","Yes","PRIMARY",40,True,"A household member is pregnant or lactating")
r("C023","household_has_lpg","=","No","PRIMARY",40,True,"Household does not have an LPG connection")
r("C024","shg_member","=","Yes","PRIMARY",30,True,"A household member is an SHG member")
r("C024","gender","=","Female","SUPPORTING",20,False,"Household member is a woman (SHG/rural-women focus)")

# ---- Health ----
r("C026","health_insurance","=","No","PRIMARY",30,True,"Household lacks existing health insurance/coverage")
r("C026","ration_card","=","Yes","SUPPORTING",20,False,"Household has a ration card on record")
r("C029","chronic_illness","=","Yes","PRIMARY",30,True,"Household self-declared a long-term/chronic health condition")
r("C030","has_children","=","Yes","PRIMARY",30,True,"Household has children")
r("C030","pregnant_or_lactating","=","Yes","SUPPORTING",20,False,"A household member is pregnant or lactating")

# ---- Pension ----
r("C032","age_elderly","=","Yes","PRIMARY",40,True,"A household member is of eligible elderly age")
r("C033","widow","=","Yes","PRIMARY",40,True,"A household member is a widow")
r("C034","disability","=","Yes","PRIMARY",40,True,"A household member has a self-declared disability")
r("C035","bank_account","=","Yes","PRIMARY",30,True,"Household has a bank account (enrolment channel; source gives no age criteria to verify against)")
r("C036","occupation","=","Unorganised worker","PRIMARY",30,True,"Household member is an unorganised worker")

# ---- Workers ----
r("C037","occupation","=","Unorganised worker","PRIMARY",30,True,"Household member is an unorganised worker")
r("C038","occupation","=","Street vendor","PRIMARY",40,True,"Household member is a street vendor")
r("C039","occupation","=","Artisan","PRIMARY",40,True,"Household member is a traditional artisan")
r("C040","occupation","=","Small business owner","PRIMARY",30,True,"Household is starting/running a micro-enterprise")
r("C041","occupation","in","Small business owner,Street vendor,Artisan","PRIMARY",30,True,
  "Household runs or is starting a small/micro business")

# ---- Banking & Insurance ----
r("C042","bank_account","=","No","PRIMARY",40,True,"Household does not have a bank account")
r("C043","bank_account","=","Yes","PRIMARY",30,True,"Household has a bank account (enrolment channel; source gives no age criteria to verify against)")
r("C044","bank_account","=","Yes","PRIMARY",30,True,"Household has a bank account (enrolment channel; source gives no age criteria to verify against)")

# ---- Small Business (Stand-Up India, women path only; SC/ST path is category-specific and excluded) ----
r("C058","occupation","=","Small business owner","PRIMARY",20,True,"Household is starting/running a business")
r("C058","gender","=","Female","PRIMARY",30,True,"Applicant is a woman entrepreneur (source's non-category-specific path)")
r("C059","occupation","=","Small business owner","PRIMARY",30,True,"Household is starting a new venture/startup")

# ---- Livestock ----
r("C060","occupation","=","Livestock owner","PRIMARY",40,True,"Household keeps livestock")
r("C061","occupation","=","Livestock owner","PRIMARY",40,True,"Household keeps cattle/livestock")

# ---- Fisheries ----
r("C068","occupation","=","Fisherman","PRIMARY",40,True,"Household occupation is fisherman")

# ---- Energy & Nutrition ----
r("C073","electricity","=","Yes","PRIMARY",30,True,"Household has a grid-connected electricity connection")
r("C073","house_status","!=","No house","SUPPORTING",10,False,"Household has a residence suitable for rooftop installation")
r("C074","occupation","=","Farmer","PRIMARY",30,True,"Household occupation is Farmer")
r("C074","agricultural_pump","=","Yes","SUPPORTING",40,False,"Household already has/needs an agricultural pump")
r("C075","student","=","Yes","PRIMARY",30,True,"A household member is a school-going child")
r("C075","school_type","=","Government","SUPPORTING",40,False,"Child attends a government/government-aided school")

# ---- Tamil Nadu ----
r("TN001","woman_headed","=","Yes","PRIMARY",40,True,"Household is headed by a woman")
r("TN002","student","=","Yes","PRIMARY",25,True,"A household member is a student")
r("TN002","gender","=","Female","PRIMARY",25,True,"Student is a girl")
r("TN002","school_type","=","Government","SUPPORTING",20,False,"Attends/attended a government school")
r("TN002","education_level","=","Entering higher education","SUPPORTING",20,False,"Entering higher education")
r("TN003","student","=","Yes","PRIMARY",25,True,"A household member is a student")
r("TN003","gender","=","Male","PRIMARY",25,True,"Student is a boy")
r("TN003","school_type","=","Government","SUPPORTING",20,False,"Attends/attended a government school")
r("TN003","education_level","=","Entering higher education","SUPPORTING",20,False,"Entering higher education")
r("TN004","student","=","Yes","PRIMARY",30,True,"A household member is a school-going child")
r("TN004","school_type","=","Government","SUPPORTING",30,False,"Attends a government school")
r("TN005","student","=","Yes","PRIMARY",30,True,"A household member is a school-going child")
r("TN006","pregnant_or_lactating","=","Yes","PRIMARY",40,True,"A household member is pregnant or a new mother")
r("TN007","house_status","in","Kutcha,No house,Needs housing","PRIMARY",40,True,"Household lacks pucca housing (rural)")
r("TN008","occupation","in","Farmer,Agricultural worker","PRIMARY",40,True,"Household occupation is farmer or agricultural labourer")
r("TN010","widow","=","Yes","PRIMARY",30,True,"Household member is a widow")
r("TN010","income_range","=","Low","SUPPORTING",30,False,"Household income is in the lower band (destitution indicator)")
r("TN011","widow","=","Yes","PRIMARY",30,True,"Household member is destitute/deserted (widow/wife status closest available field)")
r("TN012","gender","=","Female","PRIMARY",20,True,"Household member is a woman")
r("TN012","age_band","=","50+","PRIMARY",20,True,"Household member is aged 50 or above")
r("TN012","marital_status","=","Unmarried","PRIMARY",20,True,"Household member is unmarried")
r("TN012","income_range","=","Low","SUPPORTING",30,False,"Household income is in the lower band")
r("TN024","household_state","=","Tamil Nadu","PRIMARY",20,True,"Household is a Tamil Nadu resident family")
r("TN024","health_insurance","=","No","SUPPORTING",40,False,"Household lacks existing health coverage")
r("TN024","ration_card","=","Yes","SUPPORTING",40,False,"Household has a ration card on record")
r("TN025","occupation","=","Small business owner","PRIMARY",30,True,"Household member is a new entrepreneur")
# TN026 (UYEGP - Unemployed Youth Employment Generation Programme): no rule added.
# The source target group is "Unemployed youth," but the questionnaire has no sourced,
# collectible field for "currently unemployed" or a stated youth age band -- using
# occupation or an invented age range as a proxy would mean guessing eligibility
# criteria not in the source. Left recommendable=False in schemes.csv; stays in the
# directory only until a genuine field/criterion is available.
r("TN027","gender","=","Female","PRIMARY",25,True,"Household member is a woman")
r("TN027","occupation","=","Small business owner","PRIMARY",25,True,"Household member runs/is starting a business")
r("TN028","occupation","=","Artisan","PRIMARY",40,True,"Household member is an artisan/craftsperson")
r("TN029","girl_child_count","in","1,2","PRIMARY",40,True,"Household has one or two girl children")


# ---------------------------------------------------------------------------
# Weight recalibration (Phase 3 fix, applied after project owner's priority
# hierarchy clarification): a passed mandatory gate represents "clearly
# matches the main target group" and should carry a MEDIUM baseline (60) on
# its own -- not fall to LOW just because the source gives no further
# eligibility detail to add as supporting weight. Supporting conditions still
# add on top, pushing genuinely well-evidenced matches into HIGH (80-100).
# Only the mandatory weights are rescaled here; supporting weights and every
# condition/description/field stay exactly as authored above.
# ---------------------------------------------------------------------------
from collections import defaultdict

mandatory_by_scheme = defaultdict(list)
for idx, row in enumerate(rules):
    if row[6] is True:
        mandatory_by_scheme[row[0]].append(idx)

TARGET_MANDATORY_SUM = 60
for scheme_id, idxs in mandatory_by_scheme.items():
    current_sum = sum(rules[i][5] for i in idxs)
    if current_sum == 0:
        continue
    remaining = TARGET_MANDATORY_SUM
    for n, i in enumerate(idxs):
        if n == len(idxs) - 1:
            new_weight = remaining  # last one absorbs rounding remainder
        else:
            share = round(rules[i][5] / current_sum * TARGET_MANDATORY_SUM)
            new_weight = share
            remaining -= share
        rules[i][5] = new_weight

fields = ["scheme_id","condition_field","condition_operator","condition_value",
          "condition_type","weight","mandatory","description"]

with open("scheme_rules.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(fields)
    w.writerows(rules)

print(f"Wrote {len(rules)} rule rows to scheme_rules.csv")

# sanity check: every recommendable scheme should have >=1 mandatory rule
import csv as _csv
recommendable = set()
with open("schemes.csv",encoding="utf-8") as f:
    for row in _csv.DictReader(f):
        if row["recommendable"] == "True":
            recommendable.add(row["scheme_id"])

covered = set(r[0] for r in rules if r[6] is True)
missing = recommendable - covered
if missing:
    print("WARNING - recommendable schemes with NO mandatory rule yet:", sorted(missing))
else:
    print("OK - every recommendable scheme has at least one mandatory gate rule.")
