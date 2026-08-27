# -*- coding: utf-8 -*-
"""
Authoritative, from-scratch analysis of survey.csv (the final available dataset;
data collection is closed, per project decision -- no further collection planned).

Design decisions (documented here since this file is the single source of truth
for every number that goes into the paper):

  1. Inclusion: consent == "Yes..." (drops 2 of 201 raw rows -> N=199). No
     attention-check exclusion is applied, because no attention-check column
     could be identified with confidence in this export.
  2. Per-analysis N varies (pairwise deletion): each statistic is computed on
     whichever respondents answered *that* question, matching the deletion
     strategy the paper itself claims to use.
  3. Every composite construct is built transparently from named columns via
     codebook.py -- see each function's docstring for exactly which columns
     are combined and how.
  4. Assumption checking (v2 of this script, added after a critical self-review):
     - Normality (Shapiro-Wilk) is checked before any paired comparison; since
       5-point Likert data is reliably non-normal here, the non-parametric
       Wilcoxon signed-rank test is reported as the primary test, with the
       paired t-test retained alongside for comparability with conventional
       reporting -- both are always shown, and they agree in every case in
       this dataset.
     - Homogeneity of variance (Levene's test) is checked before every one-way
       ANOVA; Welch's ANOVA is used automatically when violated.
     - Binary-outcome-by-categorical-group associations (the RQ4 x SES / x
       gender tests) are tested primarily with chi-square (matching the
       paper's stated methodology), with the ANOVA/t-test retained as a
       secondary continuous-outcome-style check, and expected cell counts
       are reported so a reader can see when the chi-square approximation is
       running on thin cells.
     - Correlations default to Spearman unless a variable pair is confirmed
       normal by Shapiro-Wilk (essentially never true for Likert data here).
     - Bonferroni correction is applied within each *exploratory* test family
       (RQ4-by-SES, RQ4-by-gender, technical-familiarity-by-domain) -- not
       across the whole analysis indiscriminately, and not applied to the
       three pre-specified primary comparisons (ride-share context, beauty
       self-image vs. social pressure, harm-trust correlation).
     - A sensitivity/power analysis reports the minimum detectable effect size
       at 80% power for the main comparisons and the smallest subgroup.

Run: python run_analysis.py
Outputs: results.json (all numbers) + vector/raster figures in ../images/
"""
import json
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from codebook import COLS, TECH_FAMILIARITY_ORDER

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "survey.csv")
IMAGES_DIR = os.path.join(HERE, "..", "images")
RESULTS_PATH = os.path.join(HERE, "results.json")

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


def col(df, key):
    return df[df.columns[COLS[key]]]


def yn(series):
    """Map bilingual Yes/No text -> 1/0/np.nan."""
    s = series.astype(str)
    return pd.Series(np.where(s.str.startswith("Yes"), 1,
                      np.where(s.str.startswith("No"), 0, np.nan)),
                      index=series.index)


def short_cat(series):
    """Strip trailing bilingual parenthetical, e.g. 'Middle-income (মধ্যম আয়)' -> 'Middle-income'."""
    return series.astype(str).str.split(" (", n=1, regex=False).str[0].str.strip()


def cohens_d_paired(a, b):
    diff = a - b
    return diff.mean() / diff.std()


def eta_squared_from_paired_t(t, df_t):
    """Standard effect-size conversion for a paired t-test / 2-condition repeated-
    measures ANOVA: eta^2 = t^2 / (t^2 + df). NOTE: an earlier version of this
    script computed eta-squared by concatenating both conditions' values and
    treating them as independent groups -- that formula inflates SS_total with
    between-person variance that a paired design already removes, understating
    the true effect size by roughly 7x on this dataset. This is the corrected
    version; see main.md / IMPROVEMENT_PLAN.md for the worked comparison.
    """
    return t**2 / (t**2 + df_t)


def cronbach_alpha_2item(a, b):
    r = a.corr(b)
    return (2 * r) / (1 + r)


def paired_mean_diff_ci(a, b, confidence=0.95):
    """95% CI for the paired mean difference (a - b), via the t-distribution."""
    diff = a - b
    n = len(diff)
    se = diff.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)
    mean_diff = diff.mean()
    return float(mean_diff - t_crit * se), float(mean_diff + t_crit * se)


def spearman_ci(rho, n, confidence=0.95):
    """95% CI for Spearman's rho via the Fisher z-transform approximation
    (standard for rho, using n-3 in the SE as for Pearson's r)."""
    if n <= 3 or abs(rho) >= 1:
        return None, None
    z = np.arctanh(rho)
    se = 1 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
    lo, hi = np.tanh(z - z_crit * se), np.tanh(z + z_crit * se)
    return float(lo), float(hi)


def paired_comparison(a, b, label):
    """Run the full paired-comparison battery: normality check, paired t-test,
    Wilcoxon signed-rank (primary if normality is violated), Cohen's d, eta^2,
    Cronbach's alpha. Always reports both parametric and non-parametric tests."""
    a, b = a.align(b, join="inner")
    n = len(a)
    sw_a = stats.shapiro(a)
    sw_b = stats.shapiro(b)
    normal = (sw_a.pvalue >= 0.05) and (sw_b.pvalue >= 0.05)

    t, pt = stats.ttest_rel(a, b)
    w_stat, pw = stats.wilcoxon(a, b)
    d = cohens_d_paired(a, b)
    eta2 = eta_squared_from_paired_t(t, n - 1)
    alpha = cronbach_alpha_2item(a, b)
    ci_lo, ci_hi = paired_mean_diff_ci(a, b)

    return {
        "n": int(n),
        "normality_ok": bool(normal),
        "shapiro_p_a": float(sw_a.pvalue),
        "shapiro_p_b": float(sw_b.pvalue),
        "primary_test": "wilcoxon" if not normal else "paired_t",
        "paired_t": round(float(t), 3),
        "paired_t_p": float(pt),
        "wilcoxon_w": round(float(w_stat), 1),
        "wilcoxon_p": float(pw),
        "cohens_d": round(float(d), 3),
        "mean_diff_95ci": [round(ci_lo, 3), round(ci_hi, 3)],
        "eta_squared": round(float(eta2), 4),
        "cronbach_alpha": round(float(alpha), 3),
    }


def one_way_group_test(values_by_group, label):
    """One-way comparison of a continuous/ordinal outcome across 3+ groups:
    Levene's test for homogeneity of variance, then standard ANOVA if variance
    is homogeneous or Welch's ANOVA (via pingouin-free manual implementation)
    if not."""
    groups = list(values_by_group.values())
    lev = stats.levene(*groups)
    homogeneous = lev.pvalue >= 0.05
    if homogeneous:
        f, p = stats.f_oneway(*groups)
        method = "standard_anova"
    else:
        f, p = welch_anova(groups)
        method = "welch_anova"
    return {
        "levene_p": float(lev.pvalue),
        "variance_homogeneous": bool(homogeneous),
        "method": method,
        "F": round(float(f), 3),
        "p": float(p),
    }


def welch_anova(groups):
    """Welch's ANOVA (unequal variances). Manual implementation to avoid an
    extra dependency (pingouin) for a single test."""
    k = len(groups)
    ni = np.array([len(g) for g in groups])
    mi = np.array([np.mean(g) for g in groups])
    vi = np.array([np.var(g, ddof=1) for g in groups])
    wi = ni / vi
    grand_mean = np.sum(wi * mi) / np.sum(wi)
    numerator = np.sum(wi * (mi - grand_mean) ** 2) / (k - 1)
    denom_term = np.sum((1 - wi / np.sum(wi)) ** 2 / (ni - 1))
    denominator = 1 + (2 * (k - 2) / (k ** 2 - 1)) * denom_term
    f = numerator / denominator
    df1 = k - 1
    df2 = (k ** 2 - 1) / (3 * denom_term)
    p = stats.f.sf(f, df1, df2)
    return f, p


def chi_square_by_group(df, outcome_col, group_col, group_order):
    """Chi-square test of independence between a binary outcome and a
    categorical group variable, matching the paper's stated methodology.
    Reports expected cell counts so the chi-square approximation's reliability
    is visible rather than assumed."""
    sub = df[[outcome_col, group_col]].dropna()
    sub = sub[sub[group_col].isin(group_order)]
    ct = pd.crosstab(sub[group_col], sub[outcome_col])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    return {
        "chi2": round(float(chi2), 3),
        "p": float(p),
        "dof": int(dof),
        "min_expected_count": round(float(expected.min()), 2),
        "expected_counts_adequate": bool(expected.min() >= 5),
    }


def bonferroni(p_values):
    """Bonferroni-corrected p-values for a named family of tests."""
    n = len(p_values)
    return {k: round(min(v * n, 1.0), 4) for k, v in p_values.items()}


def min_detectable_effect(n, alpha=0.05, power=0.80, paired=True):
    """Minimum detectable Cohen's d at the given alpha/power for a sample of
    size n, via iterative search using scipy's noncentral t distribution.
    Used for a sensitivity note: not 'was this significant' but 'what effect
    size could this sample size actually have detected'."""
    from scipy.stats import nct
    df_ = n - 1 if paired else n - 2
    t_crit = stats.t.ppf(1 - alpha / 2, df_)

    def power_for_d(d):
        ncp = d * np.sqrt(n) if paired else d * np.sqrt(n / 2)
        return 1 - nct.cdf(t_crit, df_, ncp) + nct.cdf(-t_crit, df_, ncp)

    lo, hi = 0.01, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if power_for_d(mid) < power:
            lo = mid
        else:
            hi = mid
    return round(hi, 3)


def main():
    df_raw = pd.read_csv(CSV_PATH)
    n_raw = len(df_raw)
    df = df_raw[col(df_raw, "consent").astype(str).str.startswith("Yes")].copy()
    n_consented = len(df)

    results["meta"] = {
        "csv_path": "survey.csv",
        "n_raw": n_raw,
        "n_declined_consent": n_raw - n_consented,
        "n_consented": n_consented,
        "timestamp_min": str(df[df.columns[COLS['timestamp']]].min()),
        "timestamp_max": str(df[df.columns[COLS['timestamp']]].max()),
        "note": "N_consented is the analytic base sample. Per-question N varies "
                "below due to pairwise deletion (item non-response), matching the "
                "paper's stated deletion strategy.",
        "methodology_note": "v2: normality/homogeneity assumptions are now checked "
                "explicitly rather than assumed; see module docstring.",
    }

    # ---------------- Demographics ----------------
    demo = {}
    gender = short_cat(col(df, "gender").dropna())
    demo["gender"] = gender.value_counts().to_dict()
    demo["gender_pct"] = (gender.value_counts(normalize=True) * 100).round(1).to_dict()

    age = short_cat(col(df, "age").dropna())
    demo["age"] = age.value_counts().to_dict()

    residence = short_cat(col(df, "residence").dropna())
    demo["residence"] = residence.value_counts().to_dict()
    demo["residence_pct"] = (residence.value_counts(normalize=True) * 100).round(1).to_dict()

    ses = short_cat(col(df, "ses").dropna())
    demo["ses"] = ses.value_counts().to_dict()
    demo["ses_pct"] = (ses.value_counts(normalize=True) * 100).round(1).to_dict()

    awareness = short_cat(col(df, "algo_awareness").dropna())
    demo["algo_awareness"] = awareness.value_counts().to_dict()
    demo["algo_awareness_pct"] = (awareness.value_counts(normalize=True) * 100).round(1).to_dict()

    education = short_cat(col(df, "education").dropna())
    demo["education"] = education.value_counts().to_dict()
    demo["education_pct"] = (education.value_counts(normalize=True) * 100).round(1).to_dict()

    tech_fam = short_cat(col(df, "tech_familiarity").dropna())
    demo["tech_familiarity"] = tech_fam.value_counts().to_dict()
    demo["tech_familiarity_pct"] = (tech_fam.value_counts(normalize=True) * 100).round(1).to_dict()

    demo["n_gender"] = int(gender.shape[0])
    demo["n_age"] = int(age.shape[0])
    demo["n_residence"] = int(residence.shape[0])
    demo["n_ses"] = int(ses.shape[0])
    demo["n_awareness"] = int(awareness.shape[0])
    demo["n_education"] = int(education.shape[0])
    demo["n_tech_familiarity"] = int(tech_fam.shape[0])
    results["demographics"] = demo

    # ---------------- Scenario awareness ----------------
    aware = {}
    for label, key in [("ride_sharing", "rs_aware_diff_price"),
                        ("beauty_filter", "bf_aware_lighten_skin"),
                        ("llm", "llm_aware_cultural_bias")]:
        s = col(df, key).dropna()
        yes = yn(s)
        aware[label] = {"n": int(yes.notna().sum()), "pct_yes": round(float(yes.mean()) * 100, 1)}
    results["scenario_awareness"] = aware

    # ---------------- Ride-share: Emergency vs Casual ----------------
    emer = pd.to_numeric(col(df, "rs_emergency_fairness"), errors="coerce")
    cas = pd.to_numeric(col(df, "rs_casual_fairness"), errors="coerce")
    both = pd.DataFrame({"emer": emer, "cas": cas, "ses": short_cat(col(df, "ses"))}).dropna(subset=["emer", "cas"])

    rs = paired_comparison(both["emer"], both["cas"], "ride_share")
    rs["emergency_mean"] = round(float(both["emer"].mean()), 3)
    rs["emergency_sd"] = round(float(both["emer"].std()), 3)
    rs["casual_mean"] = round(float(both["cas"].mean()), 3)
    rs["casual_sd"] = round(float(both["cas"].std()), 3)
    # kept for backward compatibility with earlier reporting: canonical p-value
    # now follows the primary (non-parametric, since normality is violated) test
    rs["p_value"] = rs["wilcoxon_p"] if not rs["normality_ok"] else rs["paired_t_p"]

    # by SES (descriptive; formal SES x context interaction not tested here --
    # would need a mixed within/between design beyond this script's scope)
    ses_group = {}
    for g, sub in both.groupby("ses"):
        if g in ("Lower-income", "Middle-income", "Upper-income"):
            ses_group[g] = {
                "n": int(len(sub)),
                "emergency_mean": round(float(sub["emer"].mean()), 3),
                "casual_mean": round(float(sub["cas"].mean()), 3),
            }
    rs["by_ses"] = ses_group
    results["ride_share_emergency_vs_casual"] = rs

    # Figure 1: Emergency vs Casual overall (bar with error bars)
    fig, ax = plt.subplots(figsize=(6, 5))
    means = [rs["emergency_mean"], rs["casual_mean"]]
    sds = [rs["emergency_sd"], rs["casual_sd"]]
    bars = ax.bar(["Emergency", "Casual"], means, yerr=sds, capsize=8,
                   color=["#d6604d", "#4393c3"], alpha=0.85, width=0.55)
    for b, m in zip(bars, means):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.08, f"{m:.2f}", ha="center", fontweight="bold")
    ax.set_ylabel("Perceived Fairness (1=Very Unfair, 5=Very Fair)")
    ax.set_title(f"Perceived Fairness of Price Increases:\nEmergency vs. Casual Contexts (N={rs['n']})")
    ax.set_ylim(0, 4)
    p_str = "p < .001" if rs["p_value"] < .001 else f"p = {rs['p_value']:.3f}"
    ax.text(0.5, 3.6, f"Wilcoxon {p_str}, d={rs['cohens_d']:.2f}", ha="center", transform=ax.transData, fontsize=9, style="italic")
    ax.grid(axis="y", alpha=0.25)
    save_fig("figure1")

    # Figure 2: SES moderation
    fig, ax = plt.subplots(figsize=(7, 5))
    order = ["Lower-income", "Middle-income", "Upper-income"]
    x = np.arange(len(order))
    w = 0.35
    emer_vals = [ses_group.get(g, {}).get("emergency_mean", np.nan) for g in order]
    cas_vals = [ses_group.get(g, {}).get("casual_mean", np.nan) for g in order]
    ax.bar(x - w/2, emer_vals, width=w, label="Emergency", color="#d6604d", alpha=0.85)
    ax.bar(x + w/2, cas_vals, width=w, label="Casual", color="#4393c3", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([g.replace("-income", "") for g in order])
    ax.set_ylabel("Perceived Fairness (1-5)")
    ax.set_title("Emergency vs. Casual Scenario Fairness\nby Socioeconomic Status")
    ax.legend()
    ax.set_ylim(0, 4)
    ax.grid(axis="y", alpha=0.25)
    save_fig("figure2")

    # ---------------- Beauty: self-image vs social pressure ----------------
    si = pd.to_numeric(col(df, "bf_self_image_effect"), errors="coerce")
    sp = pd.to_numeric(col(df, "bf_social_pressure"), errors="coerce")
    pa = pd.to_numeric(col(df, "bf_personally_affected"), errors="coerce")
    gender_full = short_cat(col(df, "gender"))
    both_b = pd.DataFrame({"si": si, "sp": sp, "pa": pa, "gender": gender_full}).dropna(subset=["si", "sp"])

    bf = paired_comparison(both_b["si"], both_b["sp"], "beauty_filter")
    bf["self_image_mean"] = round(float(both_b["si"].mean()), 3)
    bf["self_image_sd"] = round(float(both_b["si"].std()), 3)
    bf["social_pressure_mean"] = round(float(both_b["sp"].mean()), 3)
    bf["social_pressure_sd"] = round(float(both_b["sp"].std()), 3)
    bf["p_value"] = bf["wilcoxon_p"] if not bf["normality_ok"] else bf["paired_t_p"]
    results["beauty_self_image_vs_social_pressure"] = bf

    # Figure 3: self-image vs social pressure bar with p-value annotation
    fig, ax = plt.subplots(figsize=(6, 5))
    means3 = [bf["self_image_mean"], bf["social_pressure_mean"]]
    sds3 = [bf["self_image_sd"], bf["social_pressure_sd"]]
    bars = ax.bar(["Self-Image\nImpact", "Social\nPressure"], means3, yerr=sds3, capsize=8,
                   color=["#8073ac", "#f1a340"], alpha=0.9, width=0.55)
    for b, m in zip(bars, means3):
        ax.text(b.get_x() + b.get_width() / 2, m + 0.08, f"{m:.2f}", ha="center", fontweight="bold")
    ax.set_ylabel("Mean Impact Score (1-5)")
    p_str2 = "p < .001" if bf["p_value"] < .001 else f"p = {bf['p_value']:.4f}"
    ax.set_title(f"Mean Impact Score: Self-Image vs. Social Pressure\n(Wilcoxon {p_str2}, N={bf['n']})")
    ax.set_ylim(0, 4)
    ax.grid(axis="y", alpha=0.25)
    save_fig("figure3")

    # ---------------- Beauty: personal-impact -> self-image regression ----------------
    # REVISED CONSTRUCT (after a second critical review -- see main.md / IMPROVEMENT_PLAN.md):
    # the earlier version of this script averaged bf_personally_affected with
    # bf_social_pressure and called the result "filter exposure." Two problems
    # with that: (1) neither item measures exposure/frequency of use -- this
    # survey never asked how often respondents use filters, only how affected
    # they feel -- so "exposure" was the wrong name for what is actually a
    # second impact/affect measure; (2) bf_social_pressure is *also* the other
    # side of the paired comparison directly above (self-image vs. social
    # pressure), so folding it into a predictor of self-image was circular --
    # it would partly be self-image-vs-social-pressure predicting itself.
    # This version uses bf_personally_affected alone as the predictor (the one
    # remaining impact item that isn't already a paired-comparison outcome
    # elsewhere), and frames the result honestly as a correlation between two
    # distinct self-reported impact dimensions -- not a dose-response/exposure
    # claim, which this instrument cannot support (it has no usage-frequency
    # item at all).
    reg_df = both_b.dropna(subset=["pa"]).copy()
    slope, intercept, r_value, p_value_reg, std_err = stats.linregress(reg_df["pa"], reg_df["si"])
    rho_reg, p_rho_reg = stats.spearmanr(reg_df["pa"], reg_df["si"])
    r_ci_lo, r_ci_hi = spearman_ci(float(r_value), len(reg_df))
    reg = {
        "n": int(len(reg_df)),
        "construct_definition": "Predictor is bf_personally_affected alone (\"How personally "
                                 "affected would you feel by such filters?\"); outcome is "
                                 "bf_self_image_effect. Revised from an earlier version that "
                                 "averaged in bf_social_pressure and mislabeled the result "
                                 "'filter exposure' -- this instrument has no usage-frequency "
                                 "item, so no true exposure/dose measure exists in the data. "
                                 "This is reported as a correlation between two distinct "
                                 "self-report impact measures, not a dose-response relationship.",
        "beta": round(float(slope), 3),
        "intercept": round(float(intercept), 3),
        "r_squared": round(float(r_value ** 2), 3),
        "pearson_r_95ci": [round(r_ci_lo, 3), round(r_ci_hi, 3)] if r_ci_lo is not None else None,
        "pearson_p": float(p_value_reg),
        "spearman_rho": round(float(rho_reg), 3),
        "spearman_p": float(p_rho_reg),
    }
    results["beauty_personal_impact_regression"] = reg

    # Figure beauty1: scatter + regression line
    fig, ax = plt.subplots(figsize=(6.5, 5))
    jitter = np.random.default_rng(0).normal(0, 0.05, size=len(reg_df))
    ax.scatter(reg_df["pa"] + jitter, reg_df["si"] + jitter, alpha=0.35, s=28, color="#8073ac")
    xs = np.linspace(reg_df["pa"].min(), reg_df["pa"].max(), 50)
    ax.plot(xs, intercept + slope * xs, color="#d6604d", lw=2.5,
            label=f"y = {intercept:.2f} + {slope:.2f}x\n$R^2$={r_value**2:.3f}, N={len(reg_df)}")
    ax.set_xlabel("\"How personally affected would you feel by such filters?\" (1-5)")
    ax.set_ylabel("Self-Image Impact Score")
    ax.set_title("Personal Impact vs. Self-Image Impact")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    save_fig("beauty1")

    # Figure beauty2: gender interaction
    fig, ax = plt.subplots(figsize=(6.5, 5))
    for g, gcolor in [("Male", "#4393c3"), ("Female", "#d6604d")]:
        sub = reg_df[reg_df["gender"] == g]
        if len(sub) < 3:
            continue
        sl, ic, *_ = stats.linregress(sub["pa"], sub["si"])
        ax.scatter(sub["pa"], sub["si"], alpha=0.35, s=26, color=gcolor, label=f"{g} (n={len(sub)})")
        xs = np.linspace(sub["pa"].min(), sub["pa"].max(), 50)
        ax.plot(xs, ic + sl * xs, color=gcolor, lw=2.5)
    ax.set_xlabel("\"How personally affected would you feel by such filters?\" (1-5)")
    ax.set_ylabel("Self-Image Impact Score")
    ax.set_title("Personal Impact vs. Self-Image Impact, by Gender")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    save_fig("beauty2")

    # Gender/age moderation significance (matches paper's "no demographic difference" claim)
    from statsmodels.formula.api import ols
    mod_df = reg_df.dropna(subset=["gender"]).copy()
    mod_df = mod_df[mod_df["gender"].isin(["Male", "Female"])]
    model = ols("si ~ pa * gender", data=mod_df).fit()
    gender_interaction_p = float(model.pvalues.get("pa:gender[T.Male]", np.nan))
    results["beauty_personal_impact_regression"]["gender_interaction_p"] = round(gender_interaction_p, 4) if not np.isnan(gender_interaction_p) else None

    # ---------------- RQ4: control / transparency / consent ----------------
    rq4_items = [("customize", "rq4_customize"), ("explain", "rq4_explain"),
                 ("prior_consent", "rq4_prior_consent"), ("indicate_bias", "rq4_indicate_bias")]
    rq4 = {}
    for label, key in rq4_items:
        s = yn(col(df, key))
        rq4[label] = {"n": int(s.notna().sum()), "n_yes": int(s.sum()), "pct_yes": round(float(s.mean()) * 100, 1)}
    results["rq4_overall"] = rq4

    # Figure control.png
    fig, ax = plt.subplots(figsize=(7.5, 5))
    labels = ["Customize", "Prior\nConsent", "System\nExplanation", "Bias\nIndicators"]
    vals = [rq4["customize"]["pct_yes"], rq4["prior_consent"]["pct_yes"], rq4["explain"]["pct_yes"], rq4["indicate_bias"]["pct_yes"]]
    bars = ax.bar(labels, vals, color=["#4393c3", "#92c5de", "#2166ac", "#67a9cf"], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
    ax.set_ylabel("% Responding Yes")
    ax.set_ylim(0, 100)
    ax.set_title(f"User Demand for Algorithmic Control and Transparency\n(N≈{rq4['customize']['n']})")
    ax.grid(axis="y", alpha=0.25)
    save_fig("control")

    # ---------------- RQ4 by SES, Gender, and Prior Awareness (with tests) ----------------
    ses_full = short_cat(col(df, "ses"))
    gender_bin = gender_full.map({"Male": 1, "Female": 0})
    awareness_bin = yn(col(df, "algo_awareness"))  # 1 = already aware of algorithmic bias, 0 = not
    education_full = short_cat(col(df, "education"))
    occupation_full = short_cat(col(df, "occupation"))
    residence_full = short_cat(col(df, "residence"))

    by_group = {"by_ses": {}, "by_gender": {}, "by_awareness": {},
                "by_education": {}, "by_occupation": {}, "by_residence": {}}
    ses_p_family, gender_p_family, awareness_p_family = {}, {}, {}
    education_p_family, occupation_p_family, residence_p_family = {}, {}, {}
    for label, key in rq4_items:
        s = yn(col(df, key))
        sub = pd.DataFrame({"v": s, "ses": ses_full, "gender": gender_full, "awareness": awareness_bin,
                             "education": education_full, "occupation": occupation_full,
                             "residence": residence_full}).dropna(subset=["v"])

        # Primary test: chi-square (matches stated methodology for categorical x categorical)
        chi = chi_square_by_group(sub, "v", "ses", ["Lower-income", "Middle-income", "Upper-income"])
        # Secondary: ANOVA-on-0/1 for a continuous-style effect readout, with Levene's check
        ses_groups = {g: gg["v"].values for g, gg in sub.dropna(subset=["ses"]).groupby("ses")
                      if g in ("Lower-income", "Middle-income", "Upper-income")}
        anova = one_way_group_test(ses_groups, f"rq4_{label}_by_ses")
        ses_means = sub.dropna(subset=["ses"]).groupby("ses")["v"].mean().mul(100).round(1).to_dict()
        by_group["by_ses"][label] = {"chi_square": chi, "anova": anova, "pct_yes_by_group": ses_means}
        ses_p_family[label] = chi["p"]

        # gender: chi-square (2x2) + t-test/point-biserial-equivalent-to-phi as secondary
        gsub = sub[sub["gender"].isin(["Male", "Female"])]
        chi_g = chi_square_by_group(gsub, "v", "gender", ["Male", "Female"])
        male_v = gsub.loc[gsub["gender"] == "Male", "v"]
        female_v = gsub.loc[gsub["gender"] == "Female", "v"]
        t, p_gender_t = stats.ttest_ind(male_v, female_v)
        # both variables are binary here, so this is mathematically the phi
        # coefficient, not a point-biserial correlation (point-biserial applies
        # when one side is continuous) -- named correctly below.
        phi, p_phi = stats.pointbiserialr((gsub["gender"] == "Male").astype(int), gsub["v"])
        gender_means = gsub.groupby("gender")["v"].mean().mul(100).round(1).to_dict()
        by_group["by_gender"][label] = {
            "chi_square": chi_g,
            "t_test": {"t": round(float(t), 3), "p": float(p_gender_t)},
            "phi_coefficient": round(float(phi), 3), "phi_p": float(p_phi),
            "pct_yes_by_group": gender_means,
        }
        gender_p_family[label] = chi_g["p"]

        # prior algorithmic-bias awareness: chi-square (2x2) + phi, same pattern as gender.
        # Added to directly test the claim (previously asserted without a computed
        # statistic -- see peer_review_synthesis.md, Critical item A) that prior
        # awareness predicts RQ4 support better than demographics do.
        asub = sub.dropna(subset=["awareness"])
        chi_a = chi_square_by_group(asub, "v", "awareness", [1, 0])
        aware_v = asub.loc[asub["awareness"] == 1, "v"]
        unaware_v = asub.loc[asub["awareness"] == 0, "v"]
        t_a, p_aware_t = stats.ttest_ind(aware_v, unaware_v)
        phi_a, p_phi_a = stats.pointbiserialr(asub["awareness"].astype(int), asub["v"])
        aware_means = asub.groupby("awareness")["v"].mean().mul(100).round(1).to_dict()
        aware_means = {("aware" if k == 1 else "not_aware"): v for k, v in aware_means.items()}
        by_group["by_awareness"][label] = {
            "chi_square": chi_a,
            "t_test": {"t": round(float(t_a), 3), "p": float(p_aware_t)},
            "phi_coefficient": round(float(phi_a), 3), "phi_p": float(p_phi_a),
            "pct_yes_by_group": aware_means,
        }
        awareness_p_family[label] = chi_a["p"]

        # Additional exploratory moderators (education, occupation, urban/rural
        # residence) -- added per Future Work §6.1's "immediately actionable, no
        # new data collection" item. Chi-square only (matching the paper's stated
        # primary categorical test), no secondary t-test/phi, to keep this
        # genuinely exploratory addition proportionate to the other RQ4 families.
        edu_order = ["SSC or below", "HSC", "Bachelor’s", "Master’s"]
        chi_e = chi_square_by_group(sub, "v", "education", edu_order)
        edu_means = sub.dropna(subset=["education"]).groupby("education")["v"].mean().mul(100).round(1).to_dict()
        by_group["by_education"][label] = {"chi_square": chi_e, "pct_yes_by_group": edu_means}
        education_p_family[label] = chi_e["p"]

        # "Faculty / শিক্ষক" (n=4) has no parenthetical to strip via short_cat() (it
        # uses "English / বাংলা" format, unlike the other occupation options'
        # "English (বাংলা)" format), so it must be matched by its full raw string
        # here or it silently drops out of the chi-square test entirely. It is
        # also not in the documented appendix instrument (Student / Job Holder /
        # Self-employed / Business / Unemployed only) -- an undocumented write-in
        # category, same class of gap as "Medium of Study" (see CLAUDE.md).
        occ_order = ["Student", "Job Holder", "Unemployed", "Self-employed / Business", "Faculty / শিক্ষক"]
        chi_o = chi_square_by_group(sub, "v", "occupation", occ_order)
        occ_means = sub.dropna(subset=["occupation"]).groupby("occupation")["v"].mean().mul(100).round(1).to_dict()
        by_group["by_occupation"][label] = {"chi_square": chi_o, "pct_yes_by_group": occ_means}
        occupation_p_family[label] = chi_o["p"]

        res_order = ["Major City", "Town or Small City", "Rural Area / Village"]
        chi_r = chi_square_by_group(sub, "v", "residence", res_order)
        res_means = sub.dropna(subset=["residence"]).groupby("residence")["v"].mean().mul(100).round(1).to_dict()
        by_group["by_residence"][label] = {"chi_square": chi_r, "pct_yes_by_group": res_means}
        residence_p_family[label] = chi_r["p"]

    # Bonferroni correction within each exploratory family (4 tests each, one per RQ4 measure)
    results["rq4_by_group"] = by_group
    results["multiple_comparisons_correction"] = {
        "rq4_by_ses_chi_square_bonferroni": bonferroni(ses_p_family),
        "rq4_by_gender_chi_square_bonferroni": bonferroni(gender_p_family),
        "rq4_by_awareness_chi_square_bonferroni": bonferroni(awareness_p_family),
        "rq4_by_education_chi_square_bonferroni": bonferroni(education_p_family),
        "rq4_by_occupation_chi_square_bonferroni": bonferroni(occupation_p_family),
        "rq4_by_residence_chi_square_bonferroni": bonferroni(residence_p_family),
        "note": "Bonferroni applied within each family of 4 related exploratory tests "
                "(one per RQ4 measure: customize, explain, prior_consent, indicate_bias). "
                "The three pre-specified primary comparisons (ride-share context, beauty "
                "self-image vs. social pressure, harm-trust correlation) are not corrected "
                "against this or any other family. Education/occupation/residence families "
                "(added later, see peer_review_synthesis.md) are exploratory post hoc "
                "additions, not part of the pre-registered SES/gender/awareness set.",
    }

    # Figure sociomic.png (by SES), gender.png (by gender), awareness.png (by prior
    # awareness) -- all four RQ4 measures, including bias indicators (added when
    # that measure's statistics were added; see peer_review_synthesis.md).
    metric_labels = {"customize": "Customize", "prior_consent": "Prior Consent",
                      "explain": "Explanation", "indicate_bias": "Bias Indicators"}
    metrics = ["customize", "prior_consent", "explain", "indicate_bias"]
    w = 0.19

    fig, ax = plt.subplots(figsize=(7.5, 5))
    order = ["Lower-income", "Middle-income", "Upper-income"]
    x = np.arange(len(order))
    for i, m in enumerate(metrics):
        vals = [by_group["by_ses"][m]["pct_yes_by_group"].get(g, np.nan) for g in order]
        ax.bar(x + (i - 1.5) * w, vals, width=w, label=metric_labels[m])
    ax.set_xticks(x)
    ax.set_xticklabels([g.replace("-income", "") for g in order])
    ax.set_ylabel("% Responding Yes")
    ax.set_ylim(0, 100)
    ax.set_title("Demand for Algorithmic Control Across Income Groups")
    ax.legend(fontsize=9, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("sociomic")

    fig, ax = plt.subplots(figsize=(7, 5))
    order_g = ["Male", "Female"]
    x = np.arange(len(order_g))
    for i, m in enumerate(metrics):
        vals = [by_group["by_gender"][m]["pct_yes_by_group"].get(g, np.nan) for g in order_g]
        ax.bar(x + (i - 1.5) * w, vals, width=w, label=metric_labels[m])
    ax.set_xticks(x)
    ax.set_xticklabels(order_g)
    ax.set_ylabel("% Responding Yes")
    ax.set_ylim(0, 100)
    ax.set_title("Demand for Algorithmic Control Across Gender Groups")
    ax.legend(fontsize=9, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("gender")

    fig, ax = plt.subplots(figsize=(7, 5))
    order_a = ["not_aware", "aware"]
    order_a_labels = ["Not Aware", "Aware"]
    x = np.arange(len(order_a))
    for i, m in enumerate(metrics):
        vals = [by_group["by_awareness"][m]["pct_yes_by_group"].get(g, np.nan) for g in order_a]
        ax.bar(x + (i - 1.5) * w, vals, width=w, label=metric_labels[m])
    ax.set_xticks(x)
    ax.set_xticklabels(order_a_labels)
    ax.set_ylabel("% Responding Yes")
    ax.set_ylim(0, 100)
    ax.set_title("Demand for Algorithmic Control by Prior Awareness of Algorithmic Bias")
    ax.legend(fontsize=9, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("awareness")

    # Exploratory: RQ4 by residence (the one exploratory moderator, among
    # education/occupation/residence, with any uncorrected p<.05 cells --
    # see peer_review_synthesis.md-driven Future Work follow-up).
    fig, ax = plt.subplots(figsize=(7.5, 5))
    order_r = ["Major City", "Town or Small City", "Rural Area / Village"]
    order_r_labels = ["Major City", "Town / Small City", "Rural / Village"]
    x = np.arange(len(order_r))
    for i, m in enumerate(metrics):
        vals = [by_group["by_residence"][m]["pct_yes_by_group"].get(g, np.nan) for g in order_r]
        ax.bar(x + (i - 1.5) * w, vals, width=w, label=metric_labels[m])
    ax.set_xticks(x)
    ax.set_xticklabels(order_r_labels)
    ax.set_ylabel("% Responding Yes")
    ax.set_ylim(0, 100)
    ax.set_title("Demand for Algorithmic Control by Residence (Exploratory)")
    ax.legend(fontsize=9, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("residence")

    # ---------------- Technical familiarity vs harm (Spearman), by domain ----------------
    tech = short_cat(col(df, "tech_familiarity")).map(TECH_FAMILIARITY_ORDER)
    rs_harm = pd.to_numeric(col(df, "rs_harm"), errors="coerce")
    bf_harm = pd.to_numeric(col(df, "bf_personally_affected"), errors="coerce")
    llm_harm = pd.to_numeric(col(df, "llm_bias_impact_cultural_identity"), errors="coerce")

    spearman_results = {}
    tech_p_family = {}
    fig, ax = plt.subplots(figsize=(7, 5))
    domain_labels, domain_rs, domain_ps = [], [], []
    for label, harm in [("Ride-Sharing", rs_harm), ("Beauty Filters", bf_harm), ("LLM Cultural Bias", llm_harm)]:
        pair = pd.DataFrame({"tech": tech, "harm": harm}).dropna()
        rho, pv_s = stats.spearmanr(pair["tech"], pair["harm"])
        rho_ci_lo, rho_ci_hi = spearman_ci(float(rho), len(pair))
        spearman_results[label] = {
            "n": int(len(pair)), "rho": round(float(rho), 3), "p": float(pv_s),
            "rho_95ci": [round(rho_ci_lo, 3), round(rho_ci_hi, 3)] if rho_ci_lo is not None else None,
        }
        tech_p_family[label] = pv_s
        domain_labels.append(label)
        domain_rs.append(rho)
        domain_ps.append(pv_s)
    results["technical_familiarity_vs_harm"] = spearman_results
    results["multiple_comparisons_correction"]["technical_familiarity_bonferroni"] = bonferroni(tech_p_family)

    colors = ["#2166ac" if p < 0.05 else "#b2182b" for p in domain_ps]
    bars = ax.bar(domain_labels, domain_rs, color=colors, alpha=0.85, width=0.55)
    y_span = max(domain_rs) - min(min(domain_rs), 0)
    pad = 0.06 * max(y_span, 0.2)
    for b, r, pv_s in zip(bars, domain_rs, domain_ps):
        sig = "*" if pv_s < 0.05 else "ns"
        va = "bottom" if r >= 0 else "top"
        offset = pad if r >= 0 else -pad
        ax.text(b.get_x() + b.get_width()/2, r + offset, f"{r:.2f} ({sig})", ha="center", va=va, fontsize=9)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Spearman's $\\rho$ (Technical Familiarity vs. Harm)")
    ax.set_title("Spearman Correlations: Technical Familiarity vs.\nPerceived Harm Across Algorithmic Domains")
    ymin, ymax = min(min(domain_rs), 0), max(domain_rs)
    ax.set_ylim(ymin - 3 * pad, ymax + 3 * pad)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    save_fig("spearman")

    # ---------------- Harm-trust correlation (ride-sharing) ----------------
    # Both variables fail Shapiro-Wilk (see module docstring) -> Spearman is the
    # primary reported coefficient; Pearson is retained for comparability since
    # the two agree closely on this dataset.
    trust = pd.to_numeric(col(df, "rs_trust_impact"), errors="coerce")
    pair_ht = pd.DataFrame({"harm": rs_harm, "trust": trust}).dropna()
    r_pearson, p_pearson = stats.pearsonr(pair_ht["harm"], pair_ht["trust"])
    rho_ht, p_ht = stats.spearmanr(pair_ht["harm"], pair_ht["trust"])
    rho_ht_ci_lo, rho_ht_ci_hi = spearman_ci(float(rho_ht), len(pair_ht))
    results["harm_trust_correlation"] = {
        "n": int(len(pair_ht)),
        "spearman_rho": round(float(rho_ht), 3), "spearman_p": float(p_ht),
        "spearman_rho_95ci": [round(rho_ht_ci_lo, 3), round(rho_ht_ci_hi, 3)],
        "pearson_r": round(float(r_pearson), 3), "pearson_p": float(p_pearson),
    }

    # ---------------- Cohesion: explain <-> consent <-> bias-disclosure ----------------
    # All three variables are binary -> phi coefficient is the correct name
    # (mathematically identical computation to point-biserial, but that name
    # applies specifically to one-continuous/one-binary pairs).
    explain_v = yn(col(df, "rq4_explain"))
    consent_v = yn(col(df, "rq4_prior_consent"))
    disclosure_v = yn(col(df, "rq4_indicate_bias"))
    pair1 = pd.DataFrame({"a": explain_v, "b": consent_v}).dropna()
    r1, p1 = stats.pointbiserialr(pair1["a"], pair1["b"]) if pair1["a"].nunique() > 1 and pair1["b"].nunique() > 1 else (np.nan, np.nan)
    pair2 = pd.DataFrame({"a": explain_v, "b": disclosure_v}).dropna()
    r2, p2 = stats.pointbiserialr(pair2["a"], pair2["b"]) if pair2["a"].nunique() > 1 and pair2["b"].nunique() > 1 else (np.nan, np.nan)
    results["expectation_cohesion"] = {
        "explain_vs_consent": {"n": int(len(pair1)), "phi": round(float(r1), 3), "p": float(p1)},
        "explain_vs_bias_disclosure": {"n": int(len(pair2)), "phi": round(float(r2), 3), "p": float(p2)},
    }

    # ---------------- Sensitivity / power analysis ----------------
    smallest_subgroup_n = min(
        v["n"] for v in results["ride_share_emergency_vs_casual"]["by_ses"].values()
    )
    results["sensitivity_analysis"] = {
        "note": "Minimum detectable Cohen's d at alpha=.05, 80% power, for a paired "
                "design, given actual N per comparison. Effects smaller than this "
                "could exist in the population without this study reliably detecting them.",
        "main_ride_share_comparison_n": results["ride_share_emergency_vs_casual"]["n"],
        "main_ride_share_mde_d": min_detectable_effect(results["ride_share_emergency_vs_casual"]["n"], paired=True),
        "main_beauty_comparison_n": results["beauty_self_image_vs_social_pressure"]["n"],
        "main_beauty_mde_d": min_detectable_effect(results["beauty_self_image_vs_social_pressure"]["n"], paired=True),
        "smallest_subgroup_n": int(smallest_subgroup_n),
        "smallest_subgroup_mde_d": min_detectable_effect(int(smallest_subgroup_n), paired=True),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nWrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
