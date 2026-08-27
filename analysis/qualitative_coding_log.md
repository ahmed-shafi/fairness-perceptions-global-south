# Qualitative Coding Log — First Pass, Second-Coder Reviewed and Corrected

**Status: Incorporated into `paper/main.tex` (§Qualitative Themes) as an AI-assisted first pass, subsequently reviewed and corrected by a second, independent human coder (one of the study's authors).** The paper (Methods, Results) now describes this as a two-coder process rather than a single-coder read; it does not report a formal inter-rater agreement coefficient for the correction pass, so treat that specific number as absent rather than implied. This status line previously described the analysis as single-coder and not yet independently reviewed — see `paper/peer_review_synthesis.md` for that earlier review — and has been updated to match the second-coder correction that has since happened. The item this file's limits section flagged as the highest-priority remaining analysis task (independent second-coder verification) is the one that was just completed.

---

## What this is, and its limits

This is a first-pass inductive thematic coding of every genuinely open-ended response in `survey.csv`, following the Braun & Clarke (2006) approach `paper/main.tex` commits to. **Read the limits before reading the findings:**

1. **AI-assisted first pass, second-coder reviewed and corrected, no formal inter-rater agreement statistic.** The coding below was originally a single (AI) pass; a second, independent human coder (one of the study's authors) has since reviewed and corrected it directly. That resolves the original single-coder concern, but no inter-rater agreement coefficient was computed for the correction, so this still falls short of a fully formalized double-coding protocol.
2. **Bangla responses were translated by Claude, not a certified translator.** Translations are given inline; if anything looks off, the original Bangla is preserved alongside it.
3. **This does not match the original manuscript's qualitative claims, and that mismatch itself is worth the authors' attention** — see "Discrepancy with the original manuscript" below.

---

## Scope: which columns actually contain open-ended text

I did not assume the appendix's documented item types were still accurate — `survey.csv` was scanned column-by-column for text length and uniqueness to find every column that behaves like free text rather than a fixed-option (Likert/Yes-No/multi-select) item. Three genuinely open-ended items belong to this study's instrument:

| Item | Question | N (of 199 consented) |
|---|---|---|
| **A** | LLM scenario: *"Do you think certain cultures or languages are excluded more often in LLM responses? If yes, why?"* (`codebook.py`: `llm_cultures_excluded_more`) | 66 |
| **B** | LLM scenario: *"What aspects of the LLM's response made it feel biased or unbiased to you?"* — this question's format is inconsistent across respondents (see note below); only the free-text subset is in scope here | 5 (of 192 total answers to this column; the other 187 used fixed checkbox options) |
| **C** | Beauty-filter scenario, conditional follow-up to *"Are some groups more negatively affected?"* — *"If yes, why?"* (an unlabeled column in the export, `survey.csv` column 59) | 4 |

**Total substantive open-text pool: 75 responses.**

Two things worth flagging about scope:

- **Item B's live behavior doesn't match its documentation.** `paper/main.tex` (§Scenario 3, item 3) — copied faithfully from the original manuscript's own appendix, this isn't a rewrite artifact — documents this item as multi-select only, 4 fixed options, no free-text option. But in the live data, 5 of 192 respondents answered with genuine free text instead of the fixed options ("Cultural domination i guess.", "training based on only particular data or scenario."), and the raw CSV column header has "please explain" appended in Bangla that appears nowhere in either version of the documented instrument. This is a new, previously-unflagged discrepancy between the documented survey and the live form's actual behavior — same family as the "Medium of Study" gap found in `paper/main.md` Round 3, but this time a *format* mismatch on an existing question rather than a wholly undocumented one.
- **The ride-sharing scenario has no open-ended item at all**, in either `survey.csv` or the documented appendix (§Scenario 1, item 3 is explicitly multi-select-only in both the original and rewritten appendix) — and neither does the beauty-filter scenario except the narrow conditional item C. This cross-check against the appendix actually *strengthens* the "Discrepancy with the original manuscript" finding below: since the documented instrument never had an open-ended ride-share item either, "the form was changed mid-collection" is no longer a plausible explanation for that discrepancy — leaving the pilot-study or illustrative-example explanations more likely. See below.

I also found and *excluded* two "Unnamed" columns (57–79 in the raw export) that looked open-ended but turned out to belong to a completely different, unrelated survey about educational-content recommendation ("misrepresents my learning needs," "promotes content not aligned with my goals") — not part of this study's ride-sharing/beauty-filter/LLM instrument. These appear to be a leftover bonus module from a different project sharing the same Google Form infrastructure, and are not analyzed here.

---

## Coded data

### Item A — LLM cultural/language exclusion, "if yes, why?" (n=66)

**Response-quality note, reported honestly rather than smoothed over:** 34 of 66 responses (52%) were bare "No"/"না"/"no comment"/"." with no elaboration, and a further ~10 were bare "Yes" with no reasoning given. This item had a low substantive-response rate even among people who chose to answer it at all — worth reporting as a finding in itself (see Theme 7 below), not just discarded.

One response (`A32`) opened with the literal text **"ChatGPT said:"** followed by an answer — this respondent appears to have copy-pasted an LLM's own output as their survey answer to a question about LLM bias. Flagged, not coded as an authentic personal opinion, and excluded from theme counts below.

Substantive responses, coded:

| # | Response (translated where needed) | Codes |
|---|---|---|
| A01 | "excluded more often due to limited training data, global power dynamics, and Western-centric content dominance" | `Training-Data-Imbalance`, `Western-Centric-Dominance`, `Structural-Power-Dynamics` |
| A02 | "World's politics" | `Political-Influence` |
| A03 | "European and American are focusing over homosexuality all over the internet. this thing don't go with our culture." | `Perceived-Moral-Imposition`, `Cultural-Value-Mismatch` |
| A04 | "Western" | `Western-Centric-Dominance` |
| A07 | (Bangla) "because the training data has less representation of that language/culture, so the model learns less about it" | `Training-Data-Imbalance` |
| A15 | "due to western culture Muslim culture gets less importance" | `Western-Centric-Dominance`, `Religious-Cultural-Marginalization` |
| A19 | "Western Culture it follows" | `Western-Centric-Dominance` |
| A20 | "it follows America or Europe standards" | `Western-Centric-Dominance` |
| A22 | "the less popular culture is often avoided or less prioritized" | `Popularity-Based-Marginalization` |
| A24 | "Bengali or indigenous [languages]... underrepresented... biased training data favoring dominant languages, limited digital content for smaller languages" | `Training-Data-Imbalance`, `Own-Language-Named`, `Digital-Content-Scarcity` |
| A32 | (copy-pasted ChatGPT output, same content as A07) | *excluded from counts — flagged as non-authentic response* |
| A40 | "to increase powerful nation's power" | `Geopolitical-Power-Motive` |
| A44 | "they are not trained [on it]" | `Training-Data-Imbalance` |
| A46 | "probably yet in improving phrase" | `Developmental-Immaturity` |
| A47 | "western values" | `Western-Centric-Dominance` |
| A53 | (long response) "if prompted correctly at the beginning, these will even give responses being non biased... So the answer is NO." | `Bias-Is-Prompt-Dependent`, `Skeptical-of-Inherent-Bias` |
| A55 | "data imbalance, cultural bias, representation graph" | `Training-Data-Imbalance` |
| A57 | "the whole system was developed by west and so they support western culture more" | `Western-Centric-Dominance`, `Developer-Origin-Attribution` |
| A58 | "I believe it is to avoid controversy. Some topics are restricted directly by the developers." | `Deliberate-Content-Moderation`, `Developer-Origin-Attribution` |

### Item B — what made an LLM response feel biased (free-text subset, n=5)

| # | Response | Codes |
|---|---|---|
| B01 | "presents only one perspective, uses emotionally charged language, or favors a particular group or idea without balance" | `One-Sided-Framing`, `Emotionally-Charged-Language`, `Perceived-Favoritism` |
| B02 | "Cultural domination i guess." | `Western-Centric-Dominance` |
| B04 | "training based on only particular data or scenario." | `Training-Data-Imbalance` |

(B03 "Dnt know" and B05 "test" excluded as non-substantive.)

### Item C — beauty filters, groups more negatively affected, why (n=4)

| # | Response | Codes |
|---|---|---|
| C01 | "They struggle to accept their natural face" | `Internalized-Self-Rejection`, `Body-Image-Harm` |
| C02 | "They show themself one in social media but in real life they are different... not that perfect as like filtered picture. This is kind of inauthentic." | `Authenticity-Gap`, `Curated-Self-Presentation` |
| C03 | "filters usually make a fake appearance of a person's outlook" | `Authenticity-Gap` |
| C04 | "Black people faces problem" | `Racial-Skin-Tone-Bias` |

---

## Candidate themes

**Theme 1 — Structural/Training-Data Roots of Exclusion** (`Training-Data-Imbalance`, `Digital-Content-Scarcity`, `Popularity-Based-Marginalization`; 8 of 18 coded Item A/B responses)
The single most common substantive explanation. Respondents who engage with *why* LLMs exclude certain cultures overwhelmingly reach for a technically literate explanation: imbalanced training data. This is consistent with the paper's own literature review (§2.1, §2.2) and suggests the subset of respondents who do elaborate have a reasonably sophisticated model of how LLMs work, not just a vague sense of unfairness.

**Theme 2 — Western-Centric Dominance as the Perceived Default** (`Western-Centric-Dominance`, `Religious-Cultural-Marginalization`, `Perceived-Moral-Imposition`, `Cultural-Value-Mismatch`; 8 of 18)
Distinct from Theme 1: not just "underrepresented" but an active perception that Western — specifically American/European — norms are treated as the default the model reflects, occasionally with explicit friction around religious or moral values (A03's framing around LGBTQ+ content, A15 naming Muslim culture specifically). This is the theme most specific to this study's Bangladeshi, Muslim-majority context, and reads as a more concrete, situated version of the "political/cultural bias" concern the paper's literature review (§2.1, citing `rozado2023`) discusses more abstractly.

**Theme 3 — Intentionality Attribution: Incidental vs. Deliberate** (`Geopolitical-Power-Motive`, `Developer-Origin-Attribution`, `Deliberate-Content-Moderation`; 3 of 18)
A smaller but conceptually important split: most respondents in Theme 1 treat bias as an unintentional byproduct of data imbalance, but a few (A40, A57, A58) frame it as a deliberate or structurally-motivated choice — "to increase powerful nation's power," attributing it to who built the system, or to intentional content moderation. This distinction has real policy implications: "fix the data" and "fix the incentives" are different interventions, and the paper's current Discussion (§5.6) doesn't currently distinguish between these two respondent framings.

**Theme 4 — Skepticism / Counter-Narrative** (`Bias-Is-Prompt-Dependent`, `Skeptical-of-Inherent-Bias`; 1 of 18, but worth reporting)
One respondent (A53) explicitly argues bias is solvable through prompting rather than inherent to the model. A single response isn't a theme in the statistical sense, but good qualitative practice reports genuine dissent rather than only the majority view, and this response is substantive and well-articulated enough to be worth a sentence in any full write-up.

**Theme 5 — Markers of Perceived Bias in Response Style** (`One-Sided-Framing`, `Emotionally-Charged-Language`, `Perceived-Favoritism`; from Item B)
A distinct angle from Themes 1–4: this is about the *form* of a response that reads as biased (one-sidedness, emotional tone) rather than its cultural content. Only 1 clear example (B01) in the current data, but it's a well-formed one and points at a dimension (stylistic markers of bias) the paper's current Results section doesn't discuss.

**Theme 6 — Authenticity Erosion and Racialized Harm in Beauty Filters** (`Internalized-Self-Rejection`, `Body-Image-Harm`, `Authenticity-Gap`, `Curated-Self-Presentation`, `Racial-Skin-Tone-Bias`; all 4 of Item C)
Directly corroborates the paper's own quantitative headline finding (self-image harm > social pressure, `paper/main.tex` §4.2.2): these four respondents describe the harm in terms of authenticity and self-acceptance rather than social comparison, and one (C04) explicitly names race ("Black people") as the locus of harm — consistent with the `riccio2023` technical-audit finding on skin-tone bias in AR filters that this revision added to the literature review (§2.6).

**Theme 7 — Low Elaboration Rate Itself as a Finding** (52% bare "No"/non-answer on Item A)
Worth stating plainly rather than only reporting on the engaged minority: over half of respondents who reached this open-ended item did not elaborate, even though the closed-form items in the same scenario show high awareness (63.5% aware of LLM cultural bias; `paper/main.tex` §4.2.3). This gap — willing to click "yes, aware" but not to explain why — is itself a small piece of evidence for the paper's own "governance gap" framing (§4.2.3: high concern, low articulated solutions), and could be worth a sentence in the Discussion if this analysis is formally incorporated later.

---

## Discrepancy with the original manuscript — flagged for the authors

The original manuscript's Methodology section illustrates its coding procedure with this example quote, attributed to the ride-sharing scenario:

> *"Increasing price during an emergency is like taking advantage of someone's misery."* — coded `[Exploitation-of-Vulnerability]`, `[Moral-Condemnation]`, `[Contextual-Unfairness]`

**I could not find any open-ended text column for the ride-sharing scenario anywhere in `survey.csv`, and confirmed the documented instrument (`paper/main.tex`, §Scenario 1) never had one either** — item 3, "Why do you think this is unfair?", is explicitly multi-select-only in both the original manuscript's appendix and this revision's (unchanged) copy of it. That rules out my earlier weakest explanation. Two remain, in decreasing order of my own confidence:

1. That quote came from the pilot study (`report.tex` mentions a 12-participant pilot) rather than the main survey export, and pilot data — collected under a possibly-different, since-revised instrument — was never merged into `survey.csv`.
2. The quote is illustrative/hypothetical rather than an actual verbatim response — worth the authors directly confirming it isn't, since I have no way to verify it from the data available to me.

(Ruled out: "the item was later changed from open-ended to fixed-choice mid-collection" — the documented instrument shows this item was designed as multi-select from the start, unlike Item B above, which genuinely does show that pattern.)

I'm flagging this neutrally rather than concluding anything: I don't have the information to tell these two apart, and only the authors can check their own records. But it means the original manuscript's one concrete qualitative example currently cannot be verified against `survey.csv` or the documented instrument, which is worth knowing before it's used again in any future version of the paper.

---

## If this gets formally incorporated later

Suggested next steps for the actual research team, not done here because they require judgment calls beyond a first coding pass:
1. A second, independent coder should code the same 75 responses and inter-rater agreement should be computed/reported (standard practice this first pass can't substitute for).
2. Resolve the ride-sharing quote discrepancy above before reusing that example.
3. Decide whether Item B's 5 free-text responses (out of 192 total answers to that column) are enough to report on at all, or whether they're better folded into a note about the form's format change mid-collection.
4. If incorporated into the paper, this belongs as a subsection of `paper/main.tex` (quantitative results) and/or woven into `paper/main.tex` (particularly Theme 2's Bangladesh/Muslim-majority specificity, and Theme 3's incidental-vs-deliberate distinction, which the current Discussion doesn't yet address) — not as a wholesale replacement of the existing quantitative results.
