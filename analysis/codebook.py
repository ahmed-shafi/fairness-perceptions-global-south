# -*- coding: utf-8 -*-
"""
Codebook mapping survey.csv column positions to short semantic names.

This exists so every number in the paper can be traced back to a specific,
named survey question rather than a bare column index. Question numbering
and wording below is copied from Appendix A of report.tex (the Full Survey
Instrument), matched against survey.csv's actual header text.
"""

COLS = {
    "timestamp": 0,
    "consent": 1,
    "age": 2,
    "gender": 3,
    "education": 4,
    "occupation": 5,
    "medium_of_study": 6,
    "field": 7,
    "residence": 8,
    "ses": 9,
    "tech_familiarity": 10,
    "algo_awareness": 11,
    "fairness_meaning": 12,
    "language": 13,
    # Scenario 1: Ride-sharing fare bias
    "rs_aware_diff_price": 14,
    "rs_fair_overall": 15,
    "rs_why_unfair": 16,
    "rs_harm": 17,
    "rs_trust_impact": 18,
    "rs_rain_feeling": 19,
    "rs_eid_acceptable": 20,
    "rs_lowincome_fairness": 21,
    "rs_emergency_fairness": 22,   # Emergency scenario, 20% price increase (1=Very Unfair..5=Very Fair)
    "rs_casual_fairness": 23,      # Casual scenario, 20% price increase (1=Very Unfair..5=Very Fair)
    "rs_ecommerce_more_acceptable": 24,
    "rs_discount_fairer": 25,
    "rs_should_explain_fare": 26,
    "rs_transparency_fairer": 27,
    # Scenario 2: Beauty filter bias
    "bf_aware_lighten_skin": 28,
    "bf_know_beauty_standards": 29,
    "bf_fair_across_skin_tones": 30,
    "bf_why_unfair": 31,
    "bf_personally_affected": 32,   # "How personally affected would you feel" (1-5)
    "bf_self_image_effect": 33,     # "How do such filters affect confidence or self-image" (1-5)
    "bf_groups_more_affected": 34,
    "bf_social_pressure": 35,       # "Do you feel social pressure to use beauty filters" (1-5)
    "bf_stricter_for_professional": 36,
    "bf_beauty_vs_fun_problematic": 37,
    "bf_transparency_labels_fairer": 38,
    "bf_should_work_all_ethnicities": 39,
    # Scenario 3: LLM cultural bias
    "llm_aware_cultural_bias": 40,
    "llm_fair_if_one_culture_dominates": 41,
    "llm_what_made_it_biased": 42,
    "llm_felt_misunderstood": 43,
    "llm_repeated_bias_reduce_trust": 44,
    "llm_bias_impact_cultural_identity": 45,
    "llm_cultures_excluded_more": 46,
    "llm_response_overlooked_values": 47,
    "cultural_fairness_vs_factual": 48,
    "user_selected_context_improve": 49,
    "ai_changes_answer_is_bias": 50,
    "ai_should_agree_cultural_viewpoint": 51,
    # RQ4: User expectations (all scenarios)
    "rq4_what_system_should_show": 52,
    "rq4_customize": 53,            # "Would you like to customize how the system works for you?"
    "rq4_explain": 54,              # "Should platforms explain how their system works?"
    "rq4_prior_consent": 55,        # "Should the system ask for your preferences before making decisions?"
    "rq4_indicate_bias": 56,        # "Should AI platforms clearly say when an answer may be biased..."
}

# Ordinal mapping for Technology Familiarity (used for Spearman correlations)
TECH_FAMILIARITY_ORDER = {
    "Very Low": 1, "Low": 2, "Moderate": 3, "High": 4, "Very High": 5,
}

SES_ORDER = ["Lower-income", "Middle-income", "Upper-income"]
AGE_ORDER = ["Under 18", "18", "21-23", "24-26", "27-30", "Above 30"]  # "18" matches both "18-20"/"18–20" via startswith
