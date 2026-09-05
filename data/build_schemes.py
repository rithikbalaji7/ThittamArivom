"""
Builds data/schemes.csv from the Phase-1 source inventory.
Every field traces to the PDF extraction. Missing info is marked explicitly.
Decisions applied (per project owner, Phase 2 kickoff):
 1. Umbrella entries kept, directory-only, not scored.
 2. KCC (C003) merged with C067 (allied/livestock) and C069 (fisheries) into one
    scheme with three use-cases, instead of 3 duplicate rows.
 3. Health-condition fields will be self-declared checkboxes (handled in questionnaire,
    not here).
 4. Generic category labels (no named scheme) kept, non-recommendable, "More information
    required".
 5. No invented Tamil translations; tamil_name left blank unless the PDF gave a Tamil-
    origin title itself (e.g. Thittam-named TN schemes keep their given name as-is).
"""
import csv

NA = "Not available in source"

# Each row: scheme_id, scheme_name, tamil_name, government, category, scheme_type,
# target_group_text, description, benefit, eligibility_text, documents, application_route,
# official_source, is_umbrella_entry, requires_category, recommendable, priority_enabled,
# source_flag
rows = []

def add(sid, name, tamil, gov, cat, stype, target, desc, benefit, elig=NA, docs=NA,
        app_route=NA, source=NA, umbrella=False, req_cat=False, rec=True,
        pri=True, flag=""):
    rows.append([sid, name, tamil, gov, cat, stype, target, desc, benefit, elig, docs,
                 app_route, source, umbrella, req_cat, rec, pri, flag])

# ---------------- A1. Farmers & Agriculture ----------------
add("C001","PM-KISAN","","Central","Agriculture","HOUSEHOLD","Eligible landholding farmers",
    "Direct income support scheme for landholding farmer families.","Income support (amount not stated in source)")
add("C002","Pradhan Mantri Fasal Bima Yojana (PMFBY)","","Central","Agriculture","HOUSEHOLD","Farmers",
    "Crop insurance scheme for farmers.","Crop insurance cover")
add("C003","Kisan Credit Card (KCC)","","Central","Agriculture","HOUSEHOLD","Farmers / allied agricultural activity workers / fishermen",
    "Agricultural credit card. Source material covers three use-cases under one scheme: general agriculture, allied agricultural activities (incl. livestock), and fisheries.",
    "Agricultural credit",flag="Merged with source rows 'KCC for allied agricultural activities' and 'KCC for fisheries' into one scheme with 3 use-cases, per Phase 2 decision #2.")
add("C004","PM-Kisan Maandhan Yojana","","Central","Agriculture","HOUSEHOLD","Eligible small/marginal farmers",
    "Pension scheme for small/marginal farmers.","Pension")
add("C005","Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)","","Central","Agriculture","HOUSEHOLD","Farmers",
    "Irrigation/water management scheme.","Irrigation/water management support")
add("C006","Soil Health Card","","Central","Agriculture","HOUSEHOLD","Farmers",
    "Soil testing and advisory scheme.","Soil testing/advice")
add("C007","Sub-Mission on Agricultural Mechanization","","Central","Agriculture","HOUSEHOLD","Farmers",
    "Support for farm machinery.","Farm machinery assistance")
add("C008","National Horticulture Mission","","Central","Agriculture","HOUSEHOLD","Horticulture farmers",
    "Assistance for horticulture activities.","Assistance for horticulture")
add("C009","National Food Security Mission","","Central","Agriculture","HOUSEHOLD","Farmers",
    "Crop productivity support scheme.","Crop productivity support")
add("C010","Agriculture Infrastructure Fund","","Central","Agriculture","BOTH","Farmers/FPOs/agri businesses",
    "Infrastructure financing for agriculture.","Infrastructure financing")
add("C011","Paramparagat Krishi Vikas Yojana","","Central","Agriculture","HOUSEHOLD","Organic farmers",
    "Support for organic farming.","Organic farming support")
add("C012","Rashtriya Krishi Vikas Yojana","","Central","Agriculture","BOTH","Agriculture sector",
    "Agriculture sector development scheme.","Agriculture development")

# ---------------- A2. Housing & Village Infrastructure ----------------
add("C013","Pradhan Mantri Awas Yojana – Gramin (PMAY-G)","","Central","Housing","HOUSEHOLD",
    "Rural households needing eligible housing assistance","Rural housing assistance scheme.",NA)
add("C014","PM-JANMAN","","Central","Tribal Welfare","CATEGORY_SPECIFIC","Eligible Particularly Vulnerable Tribal Groups (PVTG)",
    "Scheme for Particularly Vulnerable Tribal Groups.",NA,req_cat=True,rec=False,
    flag="Category-specific (PVTG/tribal); excluded from default caste-neutral recommendations per Phase 1 decision.")
add("C015","Swachh Bharat Mission – Gramin","","Central","Sanitation","BOTH","Rural households/sanitation",
    "Rural sanitation scheme.",NA)
add("C016","Jal Jeevan Mission","","Central","Water","BOTH","Rural households",
    "Rural drinking water infrastructure scheme.",NA)
add("C017","Pradhan Mantri Gram Sadak Yojana (PMGSY)","","Central","Community Development","COMMUNITY","Rural connectivity",
    "Rural road connectivity scheme.",NA,rec=False,flag="Community-level; routed to Village/Community section, not personal results.")
add("C018","MGNREGS","","Central","Labour","BOTH","Rural households seeking wage employment",
    "Rural wage employment guarantee scheme.",NA)
add("C019","Rashtriya Gram Swaraj Abhiyan (RGSA)","","Central","Community Development","COMMUNITY","Panchayati Raj capacity/institutions",
    "Panchayati Raj capacity-building scheme.",NA,rec=False,flag="Community-level.")
add("C020","Sansad Adarsh Gram Yojana","","Central","Community Development","COMMUNITY","Village development",
    "Village development scheme.",NA,rec=False,flag="Community-level.")
add("C021","MPLADS","","Central","Community Development","COMMUNITY","Community infrastructure through MPs",
    "Community infrastructure funded through MPs.",NA,rec=False,flag="Community-level.")

# ---------------- A3. Women & Mothers ----------------
add("C022","Pradhan Mantri Matru Vandana Yojana (PMMVY)","","Central","Women","HOUSEHOLD","Eligible pregnant/lactating women",
    "Maternity benefit scheme.",NA,
    flag="Also listed under Health section in source; single scheme, deduplicated.")
add("C023","Pradhan Mantri Ujjwala Yojana (PMUY)","","Central","Women","HOUSEHOLD","Eligible women/households for LPG",
    "LPG connection scheme for eligible women/households.",NA)
add("C024","DAY-NRLM","","Central","Women","BOTH","Rural women/SHGs",
    "Rural livelihoods mission for women/SHGs.",NA,
    flag="Also listed under Workers and Small Business sections; single scheme, deduplicated.")
add("C025","Women SHG livelihood programmes","","Central","Women","HOUSEHOLD","Rural women",
    "Generic label in source; no specific scheme name given.",NA,rec=False,
    flag="Generic category label, not a named scheme — 'More information required'.")

# ---------------- A4. Health ----------------
add("C026","Ayushman Bharat – PM-JAY","","Central","Health","HOUSEHOLD","Eligible families",
    "Health insurance scheme for eligible families.",NA)
add("C027","Ayushman Bharat Health & Wellness Centres / Ayushman Arogya Mandirs","","Central","Health","COMMUNITY",
    "General public","Primary healthcare infrastructure.",NA,rec=False,flag="Community-level facility, not household-scored.")
add("C028","National Health Mission","","Central","Health","COMMUNITY","Public health",
    "Public health mission.",NA,rec=False,flag="Community/public-health level.")
add("C029","National TB Elimination Programme","","Central","Health","PERSONAL","TB patients",
    "TB treatment/elimination programme.",NA,
    flag="Health-condition gated; questionnaire uses self-declared 'chronic/long-term health condition' checkbox only, no diagnosis collected.")
add("C030","Universal Immunisation Programme","","Central","Health","HOUSEHOLD","Children/pregnant women",
    "Immunisation programme.",NA)
add("C031","National programmes for NCDs","","Central","Health","PERSONAL","Eligible patients",
    "Non-communicable disease programmes.",NA,rec=False,
    flag="Health-condition gated; kept in directory only in V1 per data-minimization decision, not scored by default.")

# ---------------- A5. Pension & Social Security ----------------
add("C032","Indira Gandhi National Old Age Pension Scheme (IGNOAPS)","","Central","Pension","HOUSEHOLD","Eligible elderly",
    "Old-age pension scheme.",NA,flag="Also listed within 'Tamil Nadu Social Security Pensions' as a state-administered benefit; single scheme, deduplicated.")
add("C033","Indira Gandhi National Widow Pension Scheme (IGNWPS)","","Central","Pension","HOUSEHOLD","Eligible widows",
    "Widow pension scheme.",NA,flag="Also listed within TN Social Security Pensions; deduplicated.")
add("C034","Indira Gandhi National Disability Pension Scheme (IGNDPS)","","Central","Pension","HOUSEHOLD","Eligible persons with disabilities",
    "Disability pension scheme.",NA,req_cat=False,
    flag="Also listed within TN Social Security Pensions; deduplicated. Gated on self-declared disability checkbox.")
add("C035","Atal Pension Yojana (APY)","","Central","Pension","PERSONAL","Eligible subscribers",
    "Voluntary pension subscription scheme.",NA)
add("C036","PM-SYM","","Central","Pension","PERSONAL","Eligible unorganised workers",
    "Pension scheme for unorganised workers.",NA)

# ---------------- A6. Workers ----------------
add("C037","e-Shram","","Central","Labour","PERSONAL","Unorganised workers",
    "National database/registration for unorganised workers.",NA)
add("C038","PM SVANidhi","","Central","Labour","PERSONAL","Street vendors",
    "Micro-credit scheme for street vendors.",NA)
add("C039","PM Vishwakarma","","Central","Labour","PERSONAL","Traditional artisans",
    "Support scheme for traditional artisans/craftspeople.",NA,
    flag="Source lists trades (carpenter, blacksmith, goldsmith, potter, mason, cobbler, barber, washerman, tailor, others) as occupation sub-categories, not separate schemes.")
add("C040","PMEGP","","Central","Business","PERSONAL","New micro-enterprises",
    "Employment generation programme for new micro-enterprises.",NA)
add("C041","MUDRA","","Central","Business","HOUSEHOLD","Small businesses/micro enterprises",
    "Business loan scheme for small/micro enterprises.",NA,
    flag="Also listed under Banking and Small Business sections; single scheme, deduplicated.")

# ---------------- A7. Banking & Insurance ----------------
add("C042","PM Jan Dhan Yojana (PMJDY)","","Central","Banking","PERSONAL","Bank account/financial inclusion",
    "Basic bank account/financial inclusion scheme.",NA)
add("C043","PM Jeevan Jyoti Bima Yojana (PMJJBY)","","Central","Insurance","PERSONAL","Life insurance",
    "Life insurance scheme.",NA)
add("C044","PM Suraksha Bima Yojana (PMSBY)","","Central","Insurance","PERSONAL","Accident insurance",
    "Accident insurance scheme.",NA)

# ---------------- A8. Education & Scholarships ----------------
add("C045","National Scholarship Portal schemes","","Central","Education","PERSONAL","Students (general)",
    "Umbrella term in source for scholarships listed on the National Scholarship Portal.",NA,rec=False,
    flag="Generic umbrella label, no individual scheme detail given — 'More information required'.")
add("C046","PM YASASVI","","Central","Education","PERSONAL","Students (context: NSP scholarships)",
    "Scholarship scheme.",NA,rec=False,
    flag="Source gives name only, no target/eligibility detail — kept directory-only pending more source data.")
add("C047","Central Sector Scholarship Scheme","","Central","Education","PERSONAL","Students",
    "Scholarship scheme.",NA,rec=False,flag="Source gives name only — directory-only pending more detail.")
add("C048","Pre-Matric Scholarship (eligible groups)","","Central","Education","PERSONAL","Students (eligible groups, unspecified)",
    "Pre-matric scholarship for groups defined by the scheme (not specified in source).",NA,rec=False,
    flag="'Eligible groups' undefined in source — directory-only pending clarification.")
add("C049","Post-Matric Scholarship (eligible groups)","","Central","Education","PERSONAL","Students (eligible groups, unspecified)",
    "Post-matric scholarship for groups defined by the scheme (not specified in source).",NA,rec=False,
    flag="'Eligible groups' undefined in source — directory-only pending clarification.")
add("C050","Scholarships for students with disabilities","","Central","Education","CATEGORY_SPECIFIC","Students with disabilities",
    "Scholarship scheme for students with disabilities.",NA,req_cat=True,rec=False,
    flag="Category-specific (disability) — excluded from default recommendations.")
add("C051","Minority scholarships","","Central","Education","CATEGORY_SPECIFIC","Minority community students",
    "Scholarship scheme for minority community students.",NA,req_cat=True,rec=False,
    flag="Category-specific (religious minority) — excluded from default recommendations.")
add("C052","SC/ST scholarships","","Central","Education","CATEGORY_SPECIFIC","SC/ST students",
    "Scholarship scheme for SC/ST students.",NA,req_cat=True,rec=False,
    flag="Category-specific (SC/ST) — excluded from default recommendations.")

# ---------------- A9. Differently Abled Persons (umbrella) ----------------
add("C053","Assistance through the National Trust","","Central","Disability Welfare","CATEGORY_SPECIFIC",
    "Persons with specified disabilities","Part of the source's 'Differently Abled Persons' umbrella listing.",NA,
    req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific (disability).")
add("C054","Disability skill development programmes","","Central","Disability Welfare","CATEGORY_SPECIFIC",
    "Persons with disabilities","Part of the source's 'Differently Abled Persons' umbrella listing.",NA,
    req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific.")
add("C055","Rehabilitation assistance","","Central","Disability Welfare","CATEGORY_SPECIFIC",
    "Persons with disabilities","Part of the source's 'Differently Abled Persons' umbrella listing.",NA,
    req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific.")
add("C056","Accessible infrastructure programmes","","Central","Disability Welfare","COMMUNITY",
    "Persons with disabilities/public","Part of the source's 'Differently Abled Persons' umbrella listing.",NA,
    rec=False,umbrella=True,flag="Umbrella/directory-only; community-level.")
add("C057","Disability-related social security programmes","","Central","Disability Welfare","CATEGORY_SPECIFIC",
    "Persons with disabilities","Part of the source's 'Differently Abled Persons' umbrella listing.",NA,
    req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific.")

# ---------------- A10. Small Business / Self-Employment ----------------
add("C058","Stand-Up India","","Central","Business","CATEGORY_SPECIFIC","Eligible SC/ST & women entrepreneurs",
    "Loan scheme for SC/ST and women entrepreneurs.",NA,req_cat=True,rec=True,
    flag="Dual-path source target: SC/ST path is category-specific (excluded from default caste-neutral results); women-entrepreneur path is scored normally via gender+occupation rule.")
add("C059","Startup India","","Central","Business","HOUSEHOLD","Startups",
    "Support scheme for startups.",NA)

# ---------------- A11. Livestock & Dairy ----------------
add("C060","National Livestock Mission","","Central","Livestock","HOUSEHOLD","Livestock owners",
    "Livestock development scheme.",NA)
add("C061","Rashtriya Gokul Mission","","Central","Livestock","HOUSEHOLD","Cattle/livestock owners",
    "Cattle development scheme.",NA)
add("C062","Livestock development programmes (generic)","","Central","Livestock","HOUSEHOLD","Livestock owners",
    "Generic category label in source; no specific scheme named.",NA,rec=False,
    flag="Generic label — 'More information required'.")
add("C063","Dairy development programmes (generic)","","Central","Livestock","HOUSEHOLD","Dairy farmers",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")
add("C064","Poultry development programmes (generic)","","Central","Livestock","HOUSEHOLD","Poultry farmers",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")
add("C065","Sheep/goat development programmes (generic)","","Central","Livestock","HOUSEHOLD","Sheep/goat farmers",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")
add("C066","Fodder development programmes (generic)","","Central","Livestock","HOUSEHOLD","Livestock owners",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")

# ---------------- A12. Fisheries ----------------
add("C068","Pradhan Mantri Matsya Sampada Yojana (PMMSY)","","Central","Fisheries","HOUSEHOLD","Fishermen/fishing households",
    "Fisheries sector development scheme.",NA)
add("C070","Fisheries infrastructure assistance (generic)","","Central","Fisheries","BOTH","Fishing households/community",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")
add("C071","Fishermen welfare programmes (generic)","","Central","Fisheries","HOUSEHOLD","Fishermen",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")
add("C072","Livelihood and equipment assistance (generic)","","Central","Fisheries","HOUSEHOLD","Fishermen/fishing households",
    "Generic category label in source; no specific scheme named.",NA,rec=False,flag="Generic label — 'More information required'.")

# ---------------- A13. Energy & Nutrition ----------------
add("C073","PM Surya Ghar: Muft Bijli Yojana","","Central","Energy","HOUSEHOLD","Residential households with eligible grid-connected electricity",
    "Rooftop solar scheme.","Central financial assistance for installing rooftop solar systems, helping households reduce electricity expenses.")
add("C074","PM-KUSUM","","Central","Energy","HOUSEHOLD","Farmers and eligible agricultural entities",
    "Solar agricultural pump scheme.","Financial support for solar agricultural pumps, solarisation of existing agricultural pumps, and certain solar power plants, helping reduce agricultural energy costs.")
add("C075","PM POSHAN","","Central","Food/Nutrition","BOTH","Children in eligible Government and Government-aided schools",
    "School nutrition scheme.","Provision of hot cooked meals to improve children's nutrition, school attendance and retention.")

# ---------------- B1. Tamil Nadu State Schemes ----------------
add("TN001","Kalaignar Magalir Urimai Thittam","Kalaignar Magalir Urimai Thittam","Tamil Nadu","Women","HOUSEHOLD",
    "Eligible women heads of households","Financial assistance scheme for women heads of households.","Monthly financial assistance (amount not stated in source)")
add("TN002","Pudhumai Penn Thittam","Pudhumai Penn Thittam","Tamil Nadu","Education","PERSONAL",
    "Eligible girls from government schools entering higher education","Scholarship-type scheme for girl students entering higher education.",NA)
add("TN003","Tamil Pudhalvan Thittam","Tamil Pudhalvan Thittam","Tamil Nadu","Education","PERSONAL",
    "Eligible boys from government schools entering higher education","Scholarship-type scheme for boy students entering higher education.",NA)
add("TN004","Chief Minister's Breakfast Scheme","","Tamil Nadu","Food/Nutrition","BOTH",
    "Government-school children in eligible classes/schools","School breakfast scheme.",NA)
add("TN005","Puratchi Thalaivar MGR Nutritious Meal Programme","","Tamil Nadu","Food/Nutrition","BOTH",
    "School children","School nutrition programme.",NA)
add("TN006","Dr. Muthulakshmi Reddy Maternity Benefit Scheme","","Tamil Nadu","Women","PERSONAL",
    "Eligible pregnant women/mothers","Maternity benefit scheme.",NA)
add("TN007","Kalaignarin Kanavu Illam","Kalaignarin Kanavu Illam","Tamil Nadu","Housing","HOUSEHOLD",
    "Eligible rural households","Rural housing scheme.",NA,
    flag="Also listed again under 'Other current TN Rural Development schemes' in source; single scheme, deduplicated.")
add("TN008","Chief Minister's Uzhavar Padhukappu Thittam (CMUPT)","","Tamil Nadu","Agriculture/Pension","HOUSEHOLD",
    "Farmers and agricultural labourers","Social-security scheme for farmers and agricultural labourers.",
    "Social-security benefits, including an old-age pension component per TN Revenue Administration Department listing.",
    flag="Source suggests this may itself be a bundle of benefits including an old-age pension component; flagged for verification, not split without confirmation.")
add("TN009","Differently Abled Pension Scheme (TN)","","Tamil Nadu","Pension","CATEGORY_SPECIFIC",
    "Eligible persons with disabilities","State disability pension.",NA,req_cat=True,rec=False,
    flag="Category-specific (disability) — excluded from default recommendations.")
add("TN010","Destitute Widow Pension (TN)","","Tamil Nadu","Pension","HOUSEHOLD","Eligible destitute widows",
    "State pension for destitute widows.",NA)
add("TN011","Destitute/Deserted Wives Pension (TN)","","Tamil Nadu","Pension","HOUSEHOLD","Eligible destitute/deserted wives",
    "State pension for destitute/deserted wives.",NA)
add("TN012","Poor Unmarried Women 50+ Pension (TN)","","Tamil Nadu","Pension","PERSONAL","Eligible poor unmarried women aged 50+",
    "State pension for poor unmarried women aged 50 and above.",NA)
add("TN013","TN BC/MBC/DNC/Minority Education Schemes","","Tamil Nadu","Education","CATEGORY_SPECIFIC",
    "BC/MBC/DNC/Minority students",
    "Umbrella of pre-matric scholarships, post-matric scholarships, free education schemes, hostel facilities, educational assistance, and special scholarships.",
    NA,req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific.")
add("TN014","TN Differently Abled Welfare Schemes","","Tamil Nadu","Disability Welfare","CATEGORY_SPECIFIC",
    "Persons with disabilities",
    "Umbrella of unemployment allowance, maintenance allowance, personal assistance allowance, marriage assistance, transport concessions, welfare-board assistance, accident relief, spectacle assistance, educational assistance, maternity assistance, and CMCHIS-related benefits.",
    NA,req_cat=True,rec=False,umbrella=True,flag="Umbrella/directory-only; category-specific.")
add("TN015","TN Unorganised Workers Welfare Boards","","Tamil Nadu","Labour","HOUSEHOLD",
    "Unorganised/construction/migrant workers",
    "Umbrella of construction-worker registration, inter-state migrant construction-worker registration, pension, housing, auto-rickshaw subsidy, e-scooter subsidy, educational assistance, and other welfare-board claims.",
    NA,rec=False,umbrella=True,flag="Umbrella/directory-only — 'More information required' for individual benefit amounts.")
add("TN016","Anaithu Grama Anna Marumalarchi Thittam-II (AGAMT-II)","Anaithu Grama Anna Marumalarchi Thittam-II","Tamil Nadu","Community Development","COMMUNITY",
    "Village infrastructure/development","Village infrastructure/development scheme.",NA,rec=False,flag="Community-level.")
add("TN017","MLACDS","","Tamil Nadu","Community Development","COMMUNITY","Local development works",
    "Local development works scheme.",NA,rec=False,flag="Community-level.")
add("TN018","Rural house repairs (TN)","","Tamil Nadu","Housing","HOUSEHOLD","Rural households",
    "Generic category label in source; no specific scheme name given.",NA,rec=False,flag="Generic label — 'More information required'.")
add("TN019","Mudalvarin Grama Salaigal Membattu Thittam","Mudalvarin Grama Salaigal Membattu Thittam","Tamil Nadu","Community Development","COMMUNITY",
    "Rural roads","Rural roads scheme.",NA,rec=False,flag="Community-level.")
add("TN020","Namakku Naame Thittam","Namakku Naame Thittam","Tamil Nadu","Community Development","COMMUNITY",
    "Community infrastructure","Community infrastructure scheme.",NA,rec=False,flag="Community-level.")
add("TN021","Child Friendly School Infrastructure Development Scheme","","Tamil Nadu","Education","COMMUNITY",
    "School facilities","School infrastructure scheme.",NA,rec=False,flag="Community-level.")
add("TN022","School Infrastructure Development Scheme","","Tamil Nadu","Education","COMMUNITY","School infrastructure",
    "School infrastructure scheme.",NA,rec=False,flag="Community-level.")
add("TN023","Samathuvapuram","Samathuvapuram","Tamil Nadu","Community Development","COMMUNITY",
    "Community housing/social development","Community housing/social development scheme.",NA,rec=False,flag="Community-level.")
add("TN024","CMCHIS","","Tamil Nadu","Health","HOUSEHOLD","Eligible Tamil Nadu families",
    "Chief Minister's Comprehensive Health Insurance Scheme.","Cashless health insurance for covered treatments.")
add("TN025","NEEDS","","Tamil Nadu","Business","PERSONAL","New entrepreneurs",
    "New Entrepreneur-cum-Enterprise Development Scheme.",NA,
    flag="Per source, currently operating with FY2025-26 applications/sanctions shown on official MSME portal.")
add("TN026","UYEGP","","Tamil Nadu","Business","PERSONAL","Unemployed youth",
    "Unemployed Youth Employment Generation Programme.",NA,rec=False,
    flag="Per source, currently active with FY2025-26 applications/subsidy disbursements recorded. Not scored in V1: no sourced, collectible field distinguishes 'unemployed youth' from other occupations without guessing an age band or employment-status criterion not stated in the source.")
add("TN027","TWEES","","Tamil Nadu","Business","PERSONAL","Women entrepreneurs",
    "Tamil Nadu Women Entrepreneurs Empowerment Scheme.",NA,flag="Per source, currently active.")
add("TN028","Kalaignar Kaivinai Thittam","Kalaignar Kaivinai Thittam","Tamil Nadu","Labour","PERSONAL",
    "Artisans/craftspeople","Support scheme for artisans/craftspeople.",NA)
add("TN029","Chief Minister's Girl Child Protection Scheme (TN)","","Tamil Nadu","Women","HOUSEHOLD",
    "Eligible families with one or two girl children","Financial deposit scheme for families with one or two girl children.",
    "₹50,000 for one eligible girl child, or ₹25,000 each for two eligible girl children, subject to scheme conditions, payable on completion of 18 years.")

fields = ["scheme_id","scheme_name","tamil_name","government","category","scheme_type",
          "target_group_text","description","benefit","eligibility_text","documents",
          "application_route","official_source","is_umbrella_entry","requires_category",
          "recommendable","priority_enabled","source_flag"]

with open("schemes.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(fields)
    w.writerows(rows)

print(f"Wrote {len(rows)} scheme rows to schemes.csv")
