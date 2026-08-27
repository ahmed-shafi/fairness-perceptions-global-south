# -*- coding: utf-8 -*-
"""
Analysis of ride-share-survey.xlsx: a supplementary, ride-sharing-only
follow-up survey fielded as a second, separate Google Form after survey.csv's
collection window closed.

PROVENANCE AND HOW THIS DIFFERS FROM THE MAIN SURVEY (read before using these
numbers):
  - Distinct instrument: identical wording to the ride-sharing scenario in the
    main survey for 12 of 14 items; 2 items (rs_lowincome_fairness,
    rs_discount_fairer) add concrete clarifying examples not present in the
    original wording. No beauty-filter or LLM items were asked -- this
    instrument covers ride-sharing only.
  - Distinct consent/data-collection model: this form collected name
    (required), email (optional, 14/47 provided), and signature (optional,
    39/47 provided) -- unlike the main survey, which explicitly collected no
    identifying information. Per project decision, these 3 columns are
    dropped immediately on load (see PII_COLS in followup_codebook.py) and
    never appear in any analysis output, figure, or notebook cell.
  - Cannot be verified as independent of the main N=199 sample: since the main
    survey collected no identifying information, there is no way to check
    whether any of these 47 respondents also completed the original survey.
    For this reason these 47 responses are analyzed as a separate,
    supplementary sample -- never silently pooled into the primary N=199 for
    headline statistics -- with a labeled pooled-sensitivity check reported
    separately where that view is informative.
  - Demographically distinct: 100% male (vs. 65.8% in the main sample), skews
    markedly older (63.8% aged 27+), and 92% rural/small-town (vs. 64.3%
    major-city in the main sample). This sample sits close to the demographic
    complement of the main study's own stated sampling-skew limitation.
  - No socioeconomic-background item was asked in this instrument.

Given all of the above, this script treats ride-share-survey.xlsx as an
independent replication check on the main study's ride-sharing findings in a
demographically distinct population, not as an extension of N. Every number
below carries its own N and is reported as such in the paper.

Run: python run_followup_analysis.py
Outputs: followup_results.json + figure_followup_emergency_casual.pdf/.png in ../images/
"""
import json
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from followup_codebook import COLS, PII_COLS
from run_analysis import (
    paired_comparison, short_cat, min_detectable_effect,
)
from codebook import COLS as MAIN_COLS

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(HERE, "..", "ride-share-survey.xlsx")
CSV_PATH = os.path.join(HERE, "..", "survey.csv")
IMAGES_DIR = os.path.join(HERE, "..", "images")
RESULTS_PATH = os.path.join(HERE, "followup_results.json")

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
})

results = {}


def save_fig(name, fig=None):
    fig = fig or plt.gcf()
    png_path = os.path.join(IMAGES_DIR, f"{name}.png")
    pdf_path = os.path.join(IMAGES_DIR, f"{name}.pdf")
    fig.savefig(png_path, facecolor="white")
    fig.savefig(pdf_path, facecolor="white")
    plt.close(fig)
    print(f"  saved {name}.png + {name}.pdf")


def load_deidentified():
    """Load ride-share-survey.xlsx and immediately drop the 3 PII columns
    (name, email, signature) by position, before any other processing."""
    df = pd.read_excel(XLSX_PATH, sheet_name="Form Responses 1")
    pii_col_names = [df.columns[i] for i in PII_COLS]
    df = df.drop(columns=pii_col_names)
    return df, list(df.columns)


def col(df, cols_list, key):
    """COLS values are positions in the *original* (pre-PII-drop) column
    order; translate to the post-drop dataframe's actual columns."""
    orig_pos = COLS[key]
    shift = sum(1 for p in PII_COLS if p < orig_pos)
    return df[cols_list[orig_pos - shift]]


def main_col(df, key):
    return df[df.columns[MAIN_COLS[key]]]


def yn_bn(series):
    """Map this instrument's 'Yes / হ্যাঁ' / 'No / না' style labels -> 1/0/nan."""
    s = series.astype(str)
    return pd.Series(np.where(s.str.startswith("Yes"), 1,
                      np.where(s.str.startswith("No"), 0, np.nan)),
                      index=series.index)


def compare_yn(df, cols_list, df_main, followup_key, main_key):
    f = yn_bn(col(df, cols_list, followup_key))
    m = yn_bn(main_col(df_main, main_key))
    ct = pd.DataFrame({
        "group": ["followup"] * int(f.notna().sum()) + ["main"] * int(m.notna().sum()),
        "v": pd.concat([f.dropna(), m.dropna()]).values,
    })
    chi2, p, dof, exp = stats.chi2_contingency(pd.crosstab(ct["group"], ct["v"]))
    return {
        "followup_n": int(f.notna().sum()), "followup_pct_yes": round(float(f.mean()) * 100, 1),
        "main_n": int(m.notna().sum()), "main_pct_yes": round(float(m.mean()) * 100, 1),
        "chi2": round(float(chi2), 3), "p": float(p),
        "min_expected_count": round(float(exp.min()), 2),
    }


def main():
    df, cols_list = load_deidentified()
    n_raw = len(df)

    results["meta"] = {
        "source_file": "ride-share-survey.xlsx",
        "n": n_raw,
        "timestamp_min": str(col(df, cols_list, "timestamp").min()),
        "timestamp_max": str(col(df, cols_list, "timestamp").max()),
        "pii_columns_dropped": ["full name", "email", "signature"],
        "note": "Supplementary ride-sharing-only follow-up sample; analyzed "
                "separately from the main N=199 sample throughout (see module "
                "docstring for why). No beauty-filter or LLM items in this "
                "instrument.",
    }

    # ---------------- Demographics ----------------
    demo = {}
    age = short_cat(col(df, cols_list, "age").dropna())
    demo["age"] = age.value_counts().to_dict()
    demo["age_pct"] = (age.value_counts(normalize=True) * 100).round(1).to_dict()

    gender = short_cat(col(df, cols_list, "gender").dropna())
    demo["gender"] = gender.value_counts().to_dict()

    residence = short_cat(col(df, cols_list, "residence").dropna())
    demo["residence"] = residence.value_counts().to_dict()
    demo["residence_pct"] = (residence.value_counts(normalize=True) * 100).round(1).to_dict()

    awareness = yn_bn(col(df, cols_list, "algo_awareness"))
    demo["algo_awareness_pct_yes"] = round(float(awareness.mean()) * 100, 1)
    results["demographics"] = demo

    # ---------------- Awareness / attitude items, vs. main sample ----------------
    df_main_raw = pd.read_csv(CSV_PATH)
    df_main = df_main_raw[main_col(df_main_raw, "consent").astype(str).str.startswith("Yes")].copy()

    results["awareness_and_attitude_vs_main_sample"] = {
        "aware_diff_pricing": compare_yn(df, cols_list, df_main, "rs_aware_diff_price", "rs_aware_diff_price"),
        "should_explain_fare": compare_yn(df, cols_list, df_main, "rs_should_explain_fare", "rs_should_explain_fare"),
        "transparency_fairer": compare_yn(df, cols_list, df_main, "rs_transparency_fairer", "rs_transparency_fairer"),
    }

    # fair-overall uses Fair/Unfair labels, not Yes/No -- handled separately
    fair_f = col(df, cols_list, "rs_fair_overall").astype(str).str.startswith("Fair")
    fair_f_n = int(col(df, cols_list, "rs_fair_overall").notna().sum())
    fair_m = main_col(df_main, "rs_fair_overall").astype(str).str.startswith("Fair")
    fair_m_n = int(main_col(df_main, "rs_fair_overall").notna().sum())
    ct_fair = pd.DataFrame({
        "group": ["followup"] * fair_f_n + ["main"] * fair_m_n,
        "v": pd.concat([fair_f, fair_m]).astype(int).values,
    })
    chi2f, pf, _, expf = stats.chi2_contingency(pd.crosstab(ct_fair["group"], ct_fair["v"]))
    results["fair_overall_vs_main_sample"] = {
        "followup_n": fair_f_n, "followup_pct_fair": round(float(fair_f.mean()) * 100, 1),
        "main_n": fair_m_n, "main_pct_fair": round(float(fair_m.mean()) * 100, 1),
        "chi2": round(float(chi2f), 3), "p": float(pf),
        "min_expected_count": round(float(expf.min()), 2),
    }

    # ---------------- Emergency vs Casual: the flagship replication test ----------------
    emer = pd.to_numeric(col(df, cols_list, "rs_emergency_fairness"), errors="coerce")
    cas = pd.to_numeric(col(df, cols_list, "rs_casual_fairness"), errors="coerce")
    both = pd.DataFrame({"emer": emer, "cas": cas, "residence": residence}).dropna(subset=["emer", "cas"])

    rs = paired_comparison(both["emer"], both["cas"], "ride_share_followup")
    rs["emergency_mean"] = round(float(both["emer"].mean()), 3)
    rs["emergency_sd"] = round(float(both["emer"].std()), 3)
    rs["casual_mean"] = round(float(both["cas"].mean()), 3)
    rs["casual_sd"] = round(float(both["cas"].std()), 3)
    rs["p_value"] = rs["wilcoxon_p"] if not rs["normality_ok"] else rs["paired_t_p"]
    rs["mde_d_at_this_n"] = min_detectable_effect(rs["n"], paired=True)

    by_residence = {}
    for g, sub in both.dropna(subset=["residence"]).groupby("residence"):
        by_residence[g] = {
            "n": int(len(sub)),
            "emergency_mean": round(float(sub["emer"].mean()), 3),
            "casual_mean": round(float(sub["cas"].mean()), 3),
        }
    rs["by_residence"] = by_residence
    results["ride_share_emergency_vs_casual_followup"] = rs

    # ---------------- Main-sample numbers, side by side, for the paper ----------------
    emer_main = pd.to_numeric(main_col(df_main, "rs_emergency_fairness"), errors="coerce")
    cas_main = pd.to_numeric(main_col(df_main, "rs_casual_fairness"), errors="coerce")
    both_main = pd.DataFrame({"emer": emer_main, "cas": cas_main}).dropna()
    rs_main = paired_comparison(both_main["emer"], both_main["cas"], "ride_share_main")
    results["ride_share_emergency_vs_casual_main_sample_for_reference"] = {
        "n": rs_main["n"],
        "emergency_mean": round(float(both_main["emer"].mean()), 3),
        "casual_mean": round(float(both_main["cas"].mean()), 3),
        "wilcoxon_p": rs_main["wilcoxon_p"],
        "cohens_d": rs_main["cohens_d"],
    }

    # ---------------- Pooled sensitivity check (explicitly secondary) ----------------
    pooled_emer = pd.concat([both["emer"], both_main["emer"]], ignore_index=True)
    pooled_cas = pd.concat([both["cas"], both_main["cas"]], ignore_index=True)
    pooled = paired_comparison(pooled_emer, pooled_cas, "ride_share_pooled_sensitivity")
    pooled["note"] = ("SENSITIVITY CHECK ONLY, not a primary statistic: pools the "
                       "main N=199 sample with the 47-respondent follow-up sample "
                       "despite their different instruments, consent models, and "
                       "unverifiable independence. Reported only to show the "
                       "direction/magnitude does not flip when naively pooled; the "
                       "paper's primary figures are the two samples reported "
                       "separately above.")
    results["ride_share_pooled_sensitivity_check"] = pooled

    # ---------------- Figure: main vs. follow-up side by side ----------------
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    x = np.arange(2)
    w = 0.35
    main_vals = [results["ride_share_emergency_vs_casual_main_sample_for_reference"]["emergency_mean"],
                 results["ride_share_emergency_vs_casual_main_sample_for_reference"]["casual_mean"]]
    followup_vals = [rs["emergency_mean"], rs["casual_mean"]]
    ax.bar(x - w / 2, main_vals, width=w, label=f"Main sample (N={rs_main['n']})", color="#4393c3", alpha=0.85)
    ax.bar(x + w / 2, followup_vals, width=w, label=f"Follow-up sample (N={rs['n']})", color="#d6604d", alpha=0.85)
    for xi, v in zip(x - w / 2, main_vals):
        ax.text(xi, v + 0.08, f"{v:.2f}", ha="center", fontweight="bold", fontsize=9)
    for xi, v in zip(x + w / 2, followup_vals):
        ax.text(xi, v + 0.08, f"{v:.2f}", ha="center", fontweight="bold", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(["Emergency", "Casual"])
    ax.set_ylabel("Perceived Fairness (1=Very Unfair, 5=Very Fair)")
    ax.set_title("Emergency vs. Casual Pricing Fairness:\nMain Sample vs. Rural/Older Follow-Up Sample")
    ax.set_ylim(0, 4)
    ax.legend(loc="upper center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.1))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("figure_followup_emergency_casual")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nWrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
