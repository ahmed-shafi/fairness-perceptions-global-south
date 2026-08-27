# -*- coding: utf-8 -*-
"""
Codebook for ride-share-survey.xlsx (a supplementary, ride-sharing-only follow-up
instrument, fielded as a separate Google Form after the main survey; see
run_followup_analysis.py's module docstring for the full provenance and
limitations of this second data source).

Column positions below match the raw "Form Responses 1" sheet exactly.
Columns 1-3 (name, email, signature) are personally identifying and are
excluded from every analysis step -- see PII_COLS below, dropped
immediately on load in run_followup_analysis.py.
"""

COLS = {
    "timestamp": 0,
    # 1: full name, 2: email, 3: signature -- PII, excluded (see PII_COLS)
    "age": 4,
    "gender": 5,
    "residence": 6,
    "algo_awareness": 7,
    "rs_aware_diff_price": 8,
    "rs_fair_overall": 9,
    "rs_why_unfair": 10,
    "rs_harm": 11,
    "rs_trust_impact": 12,
    "rs_rain_feeling": 13,
    "rs_eid_acceptable": 14,
    "rs_lowincome_fairness": 15,     # wording adds concrete local examples (Kerani Ganj / Gulshan); same 1-5 construct as the original survey's rs_lowincome_fairness
    "rs_emergency_fairness": 16,     # identical construct to survey.csv's rs_emergency_fairness (1=Very Unfair..5=Very Fair)
    "rs_casual_fairness": 17,        # identical construct to survey.csv's rs_casual_fairness
    "rs_ecommerce_more_acceptable": 18,
    "rs_discount_fairer": 19,        # wording adds clarifying examples ("such as emergencies or financial hardship")
    "rs_should_explain_fare": 20,
    "rs_transparency_fairer": 21,
}

# Personally identifying columns present in this instrument (absent from the
# main survey.csv by design). Dropped immediately on load; never written to
# any output file, figure, or notebook cell in this project.
PII_COLS = [1, 2, 3]
