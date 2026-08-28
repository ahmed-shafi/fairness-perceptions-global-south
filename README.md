# Algorithmic Fairness Perceptions in the Global South

Data and code for **"Algorithmic Fairness Perceptions in the Global South: Evidence from Bangladesh on Ride-Sharing, Beauty Filters, and Large Language Models"** — an empirical survey study (N=199) examining how people in Bangladesh perceive algorithmic fairness across three everyday domains: ride-sharing pricing, AI beauty filters, and large language models.

**Authors:** Ahmed Abdal Shafi Rasel, Ahmed Mustafa Amlan, Tasmim Shajahan Mim (Department of Computer Science and Engineering, East West University, Dhaka, Bangladesh)

**Status:** Manuscript in preparation for submission to *Human Behavior and Emerging Technologies* (Wiley). This repository accompanies the paper's Data and Code Availability statement; a full citation will be added here once the article is published.

---

## What's in this repository

```
├── survey.csv                       # Primary dataset (N=201, 199 consented)
├── ride-share-survey.xlsx           # Supplementary driver sample (N=47), de-identified
├── analysis/
│   ├── run_analysis.py              # Main analysis pipeline (primary sample)
│   ├── codebook.py                  # Column-name mapping for survey.csv
│   ├── results.json                 # Every statistic reported in the paper
│   ├── FairnessPerception.ipynb     # Executed notebook, primary analysis
│   ├── run_followup_analysis.py     # Analysis pipeline (supplementary driver sample)
│   ├── followup_codebook.py         # Column-name mapping for ride-share-survey.xlsx
│   ├── followup_results.json        # Results from the driver sample
│   └── RideShareFollowUp.ipynb      # Executed notebook, follow-up analysis
├── images/                          # All figures reported in the paper (PNG + vector PDF)
└── survey_instrument/
    ├── english_survey_instrument.md # Full English wording, both instruments
    ├── bangla_survey_instrument.pdf # Bangla wording, consent text, and scenario vignettes
    └── bangla_survey_instrument.tex # LaTeX source for the Bangla PDF
```

## Reproducing the analysis

Requires Python 3 with `pandas`, `scipy`, `statsmodels`, and `matplotlib`.

```bash
cd analysis
python run_analysis.py            # regenerates results.json and every figure in images/
python run_followup_analysis.py   # regenerates followup_results.json
```

Running `run_analysis.py` against `survey.csv` regenerates every quantitative statistic, table, and figure reported in the paper's Results section from scratch.

## Data and privacy

- **`survey.csv`** (primary sample, N=201, 199 consented) collected no personally identifying information at all — no names, phone numbers, email addresses, or IP addresses.
- **`ride-share-survey.xlsx`** (supplementary driver sample, N=47) used a different consent model that *did* collect a full name, email address, and signature. Those three fields have been **redacted in place** (replaced with `[REDACTED]`, not deleted as columns) before release, so the file's column structure — and `followup_codebook.py`'s fixed column-position mapping — still matches the original instrument exactly. The redacted values never appear anywhere in this repository, in any analysis output, or in the paper.
- Both datasets are bilingual (Bangla item headers and response labels alongside English).

See `survey_instrument/` for the full item wording in both languages, including the informed-consent text participants saw before beginning.

## Known data caveats

Documented in full in the paper's Methods and Limitations sections; briefly:
- The analytic sample is N=199 (2 of 201 respondents declined consent).
- The supplementary driver sample (N=47) is a small, non-representative convenience sample (100% male, older, rural-skewed) and is never pooled with the primary sample in any headline result.
- `survey.csv` contains 23 unlabeled columns from shared Google Form infrastructure; most belong to an unrelated survey, but one (column 59) is this study's own beauty-filter follow-up item. See `analysis/codebook.py` and the paper's Methods section for the full column-by-column accounting.

## License

Code and data are released under the [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) license, matching the paper's own open-access license.
