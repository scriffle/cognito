# VC2 Question Generation — Master Prompt

**Load this prompt at the start of every generation session. Do not paraphrase or summarise — follow it exactly.**

---

## YOUR TASK

You are filling in a pre-built skeleton JSON file. The skeleton has all structural fields in place (`type`, `variant`, `bloomsLevel`, distractor array sizes). Every field set to `null` needs content. Do not change any structural field. Do not add or remove array items.

**Input:** A `.skeleton.json` file for one curriculum code, plus this prompt.
**Output:** A completed `.json` file with all `null` fields replaced with content.

---

## SESSION CONTEXT

```
YEAR LEVEL:     {{LEVEL}}
AGE BAND:       {{AGE_BAND}}
VOICE REGISTER: {{VOICE}} (primary-warm | secondary-neutral | vce-formal)
CODE:           {{CODE}}
AREA:           {{AREA}}
KEY KNOWLEDGE:  {{KEY_KNOWLEDGE}}
```

The skeleton's `_source` block contains `w` (learning point), `y` (3 reasons why), and `eg` (6 examples). Use these for variant diversity.

---

## PARAMETER TABLE

Every number below is a HARD LIMIT. Exceeding any limit is a validation failure.

| Parameter | 7-8 | 9-10 | 11-12 | 13-14 | 15-16 |
|-----------|-----|------|-------|-------|-------|
| **TF max words** | 12 | 18 | 22 | 28 | 35 |
| **MC stem max words** | 15 | 35 | 55 | 80 | 130 |
| **MC option max words** | 5 | 12 | 20 | 30 | 40 |
| **MC total options** | 3 | 3 | 3 | 4 | 4 |
| **MC distractors** | 2 | 2 | 2 | 3 | 3 |
| **Cloze options/blank** | 3 | 3 | 3 | 3 | 3 |
| **Cloze distractors/blank** | 2 | 2 | 2 | 2 | 2 |
| **Max unfamiliar words** | 1 | 1-2 | 2-3 | 2-4 | 3-5 |
| **FK grade max** | 3.0 | 5.0 | 7.0 | 9.0 | 11.0 |
| **Negation in stems** | NO | NO | Sparingly | Sparingly | Permitted |
| **Scenario max sentences** | 1 context | 2 | 3 | 3+data | Unlimited |
| **Dependent clauses** | NO | 1 (≤8w) | Yes | Yes | Yes |

---

## QUESTION DISTRIBUTION (same for every code)

| Bloom's | TF | MC | Cloze | Total |
|---------|----|----|-------|-------|
| 2 (Remember) | 12 | 12 | 2 | 26 |
| 3 (Understand) | 8 | 12 | 6 | 26 |
| 4 (Apply) | 2 | 12 | 12 | 26 |
| 5 (Analyse) | 0 | 14 | 12 | 26 |

---

## TRUE/FALSE RULES

1. **Single proposition.** One idea only. No "and", "but", "or", "because", "therefore", "however" joining two evaluable claims. The word "and" is permitted only when it is part of the content (e.g., "plants and animals") — not when it joins two separate claims.
2. **Declarative form.** Complete sentence. Not a question. Not a fragment.
3. **FALSE items must target real misconceptions.** Not silly claims. Not simple negation of a true statement. Each FALSE item represents something a student might genuinely believe.
4. **No double negation.** Never "X is not unable to..."
5. **TF FALSE balance:** 55-65% FALSE per Bloom's level (for sets of ≥4 TF items). For Level 4 (only 2 TF items): at least 1 must be FALSE.
6. **Correct field:** Exactly `"True"` or `"False"` (capitalised).
7. **Distractor:** Exactly 1 distractor object. Its `answer` is the opposite of `correct`. Its `explanation` names the misconception being targeted.
8. **No absolute language cues.** Do not use "always", "never", "all", "none", "every", "only" as cues. If used, they must appear in both TRUE and FALSE items.

**Age-specific:**
- Ages 7-10: Negation PROHIBITED. Rephrase to test the positive.
- Ages 11-12: Negation permitted with bold/caps emphasis, max 1 per item.
- Ages 13+: Negation permitted, max 1 per item.
- Ages 13+: State domain of applicability for STEM principles.

---

## MULTIPLE CHOICE RULES

1. **Cover-the-options test.** A knowledgeable student must be able to answer the stem without seeing the options. If not, rewrite as a direct question.
2. **Active voice** in stems (passive only when agent genuinely unknown).
3. **One correct answer.** Exactly one option is defensibly correct.
4. **Write distractors first. Always.**
   a. For EVERY MC question, regardless of Bloom's level, write the distractors BEFORE writing the correct answer. This is mandatory, not a suggestion. Writing the correct answer first causes systematic length bias — analysis of 3,000 existing questions showed the correct answer was longest 53% of the time (target: 25%).
   b. **Distractors are authentically complex incorrect statements.** Each distractor must:
      - Directly address the question being asked (not dodge it or answer a different question)
      - Contain the same level of specific detail, qualification, and domain terminology as the correct answer
      - Sound like a knowledgeable student's genuine reasoning that happens to contain a specific error
      - Be wrong for ONE identifiable reason, not because it is vague, oversimplified, or obviously incomplete
   c. **All options must be interchangeable in form.** A test-wise student scanning for the "most detailed" or "most complete-sounding" option must find no signal. Every option — correct and incorrect — should read as a confident, specific, substantive claim about the topic.
   d. **Distractor length must match or exceed the correct answer.** The simplest way to prevent length cues is to ensure distractors are never shorter than the correct answer. If the correct answer is 18 words, every distractor should be 16-22 words — not 10-12.
   e. All options within a question must be within ±20% word count AND ±30% character count of each other.
   f. Across the 50 MC questions in this file, the correct answer should be the longest option in no more than 25% of questions (+5% tolerance = 30% hard cap). The VALIDATOR WILL REJECT files exceeding 30%.
   g. THE VALIDATOR WILL REJECT the file if (a) any single question violates the parity rule, or (b) the correct answer is the longest in more than 30% of MC questions.
5. **No "All of the above" or "None of the above."**
6. **No K-type items** ("A and C", "Both B and D").
7. **No keyword cues.** Do not repeat a keyword from the stem only in the correct answer.
8. **Every distractor targets a named misconception.** The `explanation` field must name what a student choosing this option likely misunderstands.
9. **Options in logical order:** alphabetical, numerical (smallest→largest), temporal, or by complexity.
10. **No contractions in stems.** "does not" not "doesn't".

**Age-specific:**
- Ages 7-8: Direct questions only. Simple sentences. 3 options. ≤5 words per option.
- Ages 9-10: Direct questions preferred. 3 options. ≤12 words per option. No negation.
- Ages 11-12: "Which of the following..." accepted. 3 options. ≤20 words per option.
- Ages 13-14: "Which one of the following..." (VCAA convention). **4 options.** ≤30 words per option. All 3 distractors must be genuinely functional.
- Ages 15-16: "Which one of the following..." **4 options.** ≤40 words per option. At least 1 distractor must be a sophisticated misconception requiring deep knowledge to reject.

---

## CLOZE RULES

1. **2-4 blanks per item.** Minimum 2. Maximum 4. (1-blank items must be MC instead.)
2. **Blank key content words only.** NEVER blank articles (a, an, the), prepositions (in, on, at), conjunctions (and, but, or), pronouns, or high-frequency verbs (is, are, has).
3. **3 options per blank:** 1 correct + 2 distractors. This applies at ALL age bands.
4. **Grammatical parallelism:** All options for a blank must be the same part of speech, same tense, same singular/plural form, same grammatical structure, and similar length.
5. **Same semantic category:** All options for a blank must come from the same domain (all animals, all processes, all materials, etc.).
6. **Sentence reads naturally.** As if from a well-written class text or textbook. Not stilted, not overly formal for the age band.
7. **Placeholders:** Use EXACTLY `{{blank:1}}`, `{{blank:2}}`, etc. Do NOT use `___1___`, `[blank1]`, `{1}`, or any other format. The double-curly-brace format is mandatory: `{{blank:id}}`. IDs must match the `id` field in the blanks array.
8. **Scoring:** Set to `"partial"` (each blank scored independently) unless all blanks test parts of a single integrated concept, in which case use `"all"`.
9. **Every distractor** must have `explanation` (naming the misconception) AND `misconceptionSource` (one of: `"documented"`, `"teacher-reported"`, `"inferred"`).

---

## BLOOM'S LEVEL GUIDANCE

### Level 2 — Remember
Test factual recall: definitions, labels, terms, basic facts directly taught.
- TF: Straightforward factual propositions.
- MC: "What is...?" "Which one is...?" "What does... mean?"
- Cloze: Fill in key vocabulary terms.
- **No scenarios.** No application. Pure recall.

### Level 3 — Understand
Test comprehension: classifying, explaining, giving examples, paraphrasing.
- TF: Statements requiring classification or conceptual understanding.
- MC: "Which of these is an example of...?" "What does this mean?"
- Cloze: Sentences requiring understanding of relationships between concepts.
- Brief context is OK but the task is recognition/classification, not application.

### Level 4 — Apply
Test application: using knowledge in a new, concrete scenario.
- TF: Statements about what would happen in a described situation.
- MC: Scenario (max 2 sentences at primary, 3 at secondary) followed by a question.
- Cloze: Scenario-based sentences where students apply knowledge to complete.
- **Named characters** may be used. Culturally diverse: Mia, Jarrah, Anika, Sam, Lila, Kofi, Yen, Rosa, Amir, Jade, Linh, Marcus, Priya, Will.
- The scenario must be novel — not a direct repeat of taught examples.

### Level 5 — Analyse/Evaluate
Test analysis: comparing, explaining why, evaluating claims, reasoning from evidence.
- MC: "A student claims that..." "Based on the data..." "Which explanation best accounts for..."
- Cloze: Analytical sentences requiring students to select the correct reasoning.
- Scenarios with observations, simple data, or competing claims.
- At ages 7-10, keep analysis concrete and observable. No abstract reasoning.
- At ages 13+, scenarios may include experimental data, graphs, or quantitative information.

---

## VOICE REGISTER

### Primary Warm (Ages 7-10)
- Warm, clear, encouraging. Never patronising.
- Think: skilled primary teacher during a science investigation.
- Simple, concrete language. Familiar contexts: kitchen, garden, classroom, playground, family, Country.
- One idea per sentence. Active voice. Present tense for facts. Past tense for events.
- No contractions, no hedging, no exclamation marks, no rhetorical questions.
- No abstract nominalisations ("the classification of" → "how we sort").

### Secondary Neutral (Ages 11-14)
- Neutral, precise, respectful. Treats students as developing independent thinkers.
- Think: knowledgeable subject teacher explaining a task.
- Tier 2 academic vocabulary expected without explanation (analyse, identify, compare, evaluate).
- Active voice default. Passive permitted where appropriate.
- No contractions, no colloquial language ("heaps of", "got", "stuff"), no hedging.
- No anthropomorphic language ("cells want", "enzymes try").
- No second person ("you", "your").
- No exclamation marks, no topic labels within questions.

### VCE Formal (Ages 15-16)
- Calm, precise authority. Impersonal, objective, economical.
- Think: VCAA examiner. Every word serves the discipline.
- Third person throughout. Never "you".
- Full disciplinary register. IUPAC nomenclature. State symbols. Correct notation.
- "Which one of the following..." in MC stems.
- No contractions. No hedging. No colloquial language.
- No anthropomorphic language. No ambiguous pronoun references.
- Specific modifiers: "volume" (liquids), "concentration" (dissolved), "mass" (solids) — never "amount".

---

## ATSI INTEGRATION

If the `_source.y` or `_source.eg` fields reference Aboriginal or Torres Strait Islander knowledge:

1. Include ATSI content in **2-3 variants** spread across Bloom's levels.
2. **Specificity:** Use the nation name if provided ("Kulin Nation", "Yolngu people"). Never "Aboriginal people believe..." (pan-Aboriginal generalisation).
3. **Present tense** for living cultural practices. These are continuing cultures.
4. **Strength-based framing.** "Aboriginal peoples managed fire to maintain ecosystems" — not "Before Europeans helped..."
5. **Substantive, not decorative.** The ATSI content must be what the question tests, not background decoration.
6. **Safe to assess:** Ecological knowledge, seasons, fire management, trade, astronomical navigation, governance, language diversity.
7. **Never assess:** Sacred/ceremonial knowledge, Dreaming narratives (unless curriculum explicitly references publicly available aspects), initiation practices.

If the `_source` fields do NOT reference ATSI content, do not force inclusion.

---

## VARIANT DIVERSITY

All 26 variants at a given Bloom's level must assess the **same learning point** but differ in:

- **Frame:** Different real-world contexts
- **Vocabulary:** Different surface words for the same concept
- **Scenario:** Different characters and situations (Level 4-5)
- **Angle:** Different aspects of the same concept

**No two variants may share >40% of their content words** (excluding function words like a, the, is, are, of, in, to, and, but, or).

Use the 6 examples from `_source.eg` and the 3 reasons from `_source.y` as starting points for diversity. You will need to generate additional frames beyond these.

---

## EXPLANATION QUALITY

Every `correctExplanation` and distractor `explanation` must:

1. **Name the specific concept or misconception.** Not "This is incorrect" — say what is misunderstood and why.
2. **Be useful as learning feedback.** A student reading this should learn something.
3. **Match the voice register** for the age band.
4. **Be 1-2 sentences maximum.**

---

## OUTPUT FORMAT

Fill in ALL `null` fields in the skeleton. The structural fields (`type`, `variant`, `bloomsLevel`, array sizes) are already correct — do not change them.

For cloze items: the skeleton provides a 2-blank scaffold. You may modify the blanks array to have 2, 3, or 4 blanks as needed, but always maintain the same distractor structure per blank (2 distractors, each with `answer`, `explanation`, `misconceptionSource`).

Set `_meta.generatedAt` to the current ISO 8601 timestamp.

Remove the `_source` block from the final output — it was for your reference only.

---

## ANTI-DRIFT CHECKLIST

Before completing EACH question, verify:

- [ ] Word count within limit for this age band and question type
- [ ] No prohibited language patterns for this age band
- [ ] Correct number of options/distractors for this age band
- [ ] For EACH MC question: count words AND characters in correct answer and every distractor. No option may be >20% longer/shorter than the mean word count, or >30% longer/shorter than the mean character count.
- [ ] Across all MC questions in this file: track how often the correct answer is the longest. Target: roughly 1/n. Maximum: 50% (3-option) or 40% (4-option). If trending higher, deliberately make the next correct answers shorter or pad the distractors.
- [ ] Every distractor explanation names a specific misconception
- [ ] TF is a single proposition (no compound claims)
- [ ] Cloze blanks test content words only
- [ ] Voice matches the register for this age band
- [ ] This variant is sufficiently different from previous variants

Before completing EACH Bloom's level, verify:

- [ ] TF FALSE balance is 55-65% (or ≥1 FALSE if ≤3 TF items)
- [ ] Bloom's level is genuinely harder than the previous level
- [ ] Variant diversity — no two variants share >40% content words
- [ ] Type counts match the distribution table exactly

---

## WHAT NOT TO DO

These are the most common generation errors. Actively avoid them:

1. **Distractors must match the correct answer in complexity and length.** This is the #1 test-wiseness exploit — analysis of 3,000 existing questions showed the correct answer was longest 53% of the time. The fix: read the correct answer, note its word count, level of detail, and use of domain terminology, then write each distractor to match that complexity with an authentically incorrect but plausible claim. Each distractor should sound like a student who studied hard but misunderstood one specific thing.
2. **Do not write TF statements with compound propositions.** "X and Y" where X is true but Y is false is ambiguous.
3. **Do not blank function words in cloze.** "The {{blank:1}} grows" where the answer is "plant" is fine. "{{blank:1}} plant grows" where the answer is "The" is not.
4. **Do not use past tense for facts/principles.** "Water froze at 0°C" implies it no longer does.
5. **Do not write FALSE TF items that are obviously absurd.** "The sun is purple" tests nothing. "Plants get food from the soil" tests a real misconception.
6. **Do not repeat the same frame across variants.** If variant 1 uses a garden context, variant 2 should not.
7. **Do not use contractions in stems.** Ever. At any age band.
8. **Do not exceed the word limit.** Count words. If in doubt, shorten.
9. **Do not use "you" or "your" in stems** (except ages 5-6 which we are not generating).
10. **Do not write Level 2 (Remember) questions that require reasoning.** If a student needs to think beyond recall, it belongs at Level 3+.
