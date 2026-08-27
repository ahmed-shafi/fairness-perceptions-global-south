# Survey Instrument (English) — Primary Sample

This is the canonical English presentation of the survey instrument used to collect the primary sample (N=201, 199 consented; `survey.csv`), reproduced from the manuscript's appendix. The survey itself was administered bilingually, side by side in Bangla and English; see `bangla_survey_instrument.pdf` in this folder for the Bangla item wording, consent text, and scenario vignettes, transcribed directly from the live Google Form.

## Informed Consent

You are invited to take part in a research survey about how people perceive fairness in digital decision-making systems. Your participation is completely voluntary, and you may skip any question or withdraw at any time. We will not collect any personally identifying information, and all your responses will remain confidential. The results will only be used for academic research and analysis.

1. **Do you agree to participate in this research survey about fairness in digital decision-making systems?** Yes / No

## Demographic Questions

1. **Age:** Under 18 / 18–20 / 21–23 / 24–26 / 27–30 / Above 30
2. **Gender:** Male / Female
3. **Education Level:** SSC or below / HSC / Bachelor's / Master's
4. **Occupation:** Student / Job Holder / Self-employed / Business / Unemployed
5. **Medium of Study:** What was the primary medium of instruction in your education? Bangla Medium / English Medium / English Version / Madrasa Education
6. **Field of Study or Work:** Computer Science / Engineering; Business / Economics; Social Sciences / Humanities; Natural Sciences; Health / Medical; English
7. **Hometown Background:** Major City / Town or Small City / Rural Area / Village
8. **Socioeconomic Background:** Lower-income / Middle-income / Upper-income
9. **Technology Familiarity:** Very Low / Low / Moderate / High / Very High
10. **Algorithmic Awareness:** Have you heard of "algorithmic bias" or "AI fairness" before? Yes / No
11. **What does "Algorithm Fairness" mean to you?** Equal treatment for everyone; avoiding bias against any group; transparency and explainability of algorithms; regular testing and updating to ensure fairness; prioritizing accuracy over fairness
12. **Language Proficiency:** Bangla / English

## Scenario 1: Ride-Sharing Fare Bias

Suppose you and a friend both open a ride-sharing app at the same time to book a ride from the same pickup point to the same destination. Surprisingly, you see a fare of 320 BDT while your friend sees 250 BDT. Both of you have almost identical ride histories. Later, you find out that the app uses personal data — such as your phone model, location history, and previous spending behavior — to personalize prices.

1. Were you aware ride-sharing apps might show different prices to different users? (Yes/No)
2. Do you think this pricing is fair overall? (Fair/Unfair)
3. Why do you think this is unfair? (select all that apply: discriminates against low-income areas; exploits urgency or emergencies; increases inequality; reduces trust; I think this is fair)
4. How much do you feel harmed personally by this price difference? (1–5)
5. If this is common, how would it affect your trust in the platform? (1–5)
6. How do you feel when fare increases during rain or stormy weather? (1–5)
7. During holidays like Eid when demand is high, do you think the price hike is acceptable? (Yes/No)
8. If someone from a low-income area pays less than someone from a high-income area for the same ride, how fair do you find this? (1–5)
9. Imagine you urgently need a ride to the hospital during a medical emergency and see the price has increased by 20%. How fair do you find this? (1–5)
10. Imagine you are booking a ride for a casual visit and see the price has increased by 20%. How fair do you find this? (1–5)
11. Is personalized pricing more acceptable in e-commerce than in ride-sharing? (Yes/No)
12. Would offering discounts to people with low incomes or in critical situations make this feel fairer? (Yes/No)
13. Do you think ride-sharing apps should explain how your fare is calculated? (Yes/No)
14. If apps are transparent about how pricing works, would that make this option feel fairer? (Yes/No)

## Scenario 2: Beauty Filter Bias

Suppose you're experimenting with several beauty filters on Instagram or Snapchat for fun. You notice that most filters automatically lighten your skin tone, smooth your face, and change your features to match a particular beauty ideal. Later, a friend from a different ethnic background tries the same filters, and the results look dramatically different on them.

1. Were you aware that beauty filters often lighten skin, smooth features, and promote specific beauty standards? (Yes/No)
2. Do you know what the current beauty standards promoted on social media are? (Yes/No)
3. Do you think these filters are fair across different skin tones and facial features? (Yes/No)
4. If unfair, why? (select all that apply: promotes unrealistic beauty ideals; discriminates against darker skin tones; causes social pressure; creates economic pressure to buy beauty products; no, I think it's fair)
5. How personally affected would you feel by such filters? (1–5, unlabeled endpoints)
6. How do such filters affect confidence or self-image? (1–5, unlabeled endpoints)
7. Are some groups more negatively affected? (Yes/No; if yes, open-ended follow-up)
8. People often react more positively to filtered photos. Do you feel social pressure to use beauty filters to fit in? (1–5, unlabeled endpoints)
9. If someone is using filters professionally (e.g., for job applications, modeling), do you think fairness standards should be stricter? (Yes/No)
10. Is this more problematic in beauty filters or fun filters? (Beauty filters / Fun filters / Both equally)
11. Would transparency labels make filters feel fairer? (Yes/No)
12. Should filters work equally well across all ethnicities? (Yes/No)

*A note on the three 1–5 items above:* unlike the ride-sharing fairness items in Scenario 1 (interpreted directionally in the paper's codebook as 1=least fair to 5=most fair), the three beauty-filter impact items above carry no labeled endpoints in the live instrument. The paper interprets a higher score as greater self-reported impact/harm, consistent with this scenario's framing and the direction of the correlation between the personal-affect and self-image items — but that interpretation is inferred from context rather than guaranteed by the scale itself, and is flagged as an instrument limitation in the paper rather than presented as unambiguous.

## Scenario 3: Language Model Cultural Bias

Imagine you ask a language model a question about family values. The answer you receive focuses mainly on individualism, personal freedom, and independence. However, it doesn't mention core cultural values like respect for elders or religious traditions, which are important in your community. Later, you find that your friend received a very different response that aligns more closely with their cultural background.

1. Did you know that large language models (LLMs) can reflect cultural or ideological biases? (Yes/No)
2. How fair do you think it is if the values of one culture dominate the responses of a language model? (1–5)
3. What aspects of the LLM's response made it feel biased or unbiased to you? (select all that apply: agreed too quickly without justification; avoided challenging an incorrect belief; favored a particular culture, group, or opinion; treated all sides fairly and equally) — documented as fixed-choice only, but 5 of 192 respondents in the live data answered in free text instead
4. Have you ever felt misunderstood because the LLM failed to grasp your cultural background or context? (Yes/No)
5. Would repeated bias in LLM responses reduce your trust in the technology? (1–5)
6. To what extent do you believe biased answers from LLMs impact cultural identity? (1–5)
7. Do you think certain cultures or languages are excluded more often in LLM responses? If yes, why? (open-ended)
8. Have you ever felt that a response from an LLM overlooked or disregarded important cultural values? (Yes, I have experienced this / No, I have not experienced this)
9. In your view, should cultural fairness hold greater importance in value-based answers compared to factual ones? (Yes/No)
10. Do you think allowing users to select their cultural context would improve fairness in LLM responses? (1–5, Strongly agree–Strongly disagree)
11. If an AI assistant changes its answer to align with your personal opinion, do you think that reflects cultural bias? (Yes/No)
12. Should AI always agree with the user's cultural viewpoint? (Yes, to show respect / No, it should remain neutral / Depends on the context)

## RQ4: User Expectations (All Scenarios)

1. What things should the system show or let you do so you think is fair? (select all that apply: show how prices/results are decided; let me change or customize settings; allow me to report unfair behavior or results; provide clear rules or policies; show data or history related to me)
2. Would you like to customize how the system works for you? (Yes/No)
3. Should platforms explain how their system works? (Yes/No)
4. Should the system ask for your preferences before making decisions that affect you? (Yes/No)
5. Should AI platforms clearly indicate when an answer may be biased or incomplete for your culture? (Yes/No)

---

# Supplementary Follow-Up Survey (Ride-Sharing Only)

This instrument was fielded separately (24 Aug – 10 Dec 2025, a window entirely inside the primary survey's own collection period rather than after it closed), recruited primarily from ride-sharing drivers and covering ride-sharing only. **Unlike the primary instrument above, this form also requested a full name, an email address, and a signature.** Those fields are not reproduced here, and are also redacted (not merely removed as columns) in `ride-share-survey.xlsx` in this repository — they fell outside the substantive scenario and were dropped from all analysis before it began. Two items add concrete examples not present in the original wording, marked as such below; the rest are identical to Scenario 1 above.

## Demographic Questions

1. **Age:** 21–23 / 24–26 / 27–30 / Above 30
2. **Gender:** Male / Female
3. **Hometown Background:** Major City / Town or Small City / Rural Area / Village
4. **Algorithmic Awareness:** Have you heard of "algorithmic bias" or "AI fairness" before? Yes / No

## Scenario: Ride-Sharing Fare Bias

Same framing scenario as Scenario 1 above.

1. Were you aware ride-sharing apps might show different prices to different users? (Yes/No)
2. Do you think this pricing is fair overall? (Fair/Unfair)
3. Why do you think this is unfair? (select all that apply: discriminates against low-income areas; exploits urgency or emergencies; increases inequality; reduces trust; I think this is fair)
4. How much do you feel harmed personally by this price difference? (1–5)
5. If this is common, how would it affect your trust in the platform? (1–5)
6. How do you feel when fare increases during rain or stormy weather? (1–5)
7. During holidays like Eid when demand is high, do you think the price hike is acceptable? (Yes/No)
8. *[Wording adds concrete examples.]* If someone from a low-income area (e.g., Kerani Ganj) pays less than someone from a high-income area (e.g., Gulshan) for the same ride, how fair do you find this? (1–5)
9. Imagine you urgently need a ride to the hospital during a medical emergency and see the price has increased by 20%. How fair do you find this? (1–5)
10. Imagine you are booking a ride for a casual visit and see the price has increased by 20%. How fair do you find this? (1–5)
11. Is personalized pricing more acceptable in e-commerce than in ride-sharing? (Yes/No)
12. *[Wording adds concrete examples.]* Would offering discounts to people with low incomes or in critical situations (such as emergencies or financial hardship) make this feel fairer? (Yes/No)
13. Do you think ride-sharing apps should explain how your fare is calculated? (Yes/No)
14. If apps are transparent about how pricing works, would that make this option feel fairer? (Yes/No)
