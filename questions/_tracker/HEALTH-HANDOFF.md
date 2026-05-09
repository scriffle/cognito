# Health & PE Generation — Session Handoff (Y7, Y8, Y10)

Scope: Year 7 HPE (1 file), Year 8 HPE + Community Health (~38 files), Year 10 HPE + Community Health (~37 files). Year 9 has no Health skeletons in the project.

---

## START HERE — Picking up this work

**You are resuming sequential generation of Health & PE question files for the Victorian Curriculum v2 navigator.** Read this section, then jump to the next pending code.

### First message template

Paste this as your first message to confirm setup before generating:

> Resuming Health & PE generation per `questions/_tracker/HEALTH-HANDOFF.md`. I'll read this handoff, the generation prompt master, and the relevant voice guide, then start with the next pending code from the queue. After each file: validate to `Passed: 1/1`, update the level manifest, rebuild the index, delete the builder script, then move to the next file. I will work sequentially, one file at a time — never via sub-agents.

### Step-by-step kickoff

1. **Read the rules** (in this order):
   - This handoff (`questions/_tracker/HEALTH-HANDOFF.md`)
   - Generation prompt master (`questions/_tracker/generation-prompt-master.md`) — has the latest `MC_CHAR_LENGTH_BIAS` rule
   - Voice guide for the target age band (see paths table at bottom)
   - ATSI integration guide (`Question Specifications/atsi-integration-guide.md`)
2. **Pick the next pending code** from the queue tables below. Work top-to-bottom within a year level.
3. **Read the skeleton**: `questions/level-XX/<area folder>/<CODE>.skeleton.json` — note `_meta.ageBand`, `_meta.keyKnowledge`, and `_source` (`w` / `y` / `eg`).
4. **Author all 104 questions** in a builder script saved at `questions/_tracker/build_<CODE>.py`. Pattern: define TF/MC/Cloze items as Python tuples per Bloom level, then assemble into the skeleton structure. Set `_meta.generatedAt` to the current ISO 8601 UTC timestamp. Remove `_source` from output.
5. **Run the builder**: `python3 questions/_tracker/build_<CODE>.py`. It writes the JSON.
6. **Validate**: `python3 questions/_validation/validate.py <output-path>`. Must report `Passed: 1/1` with 0 errors. Iterate on the builder until clean.
7. **Update manifest**: in `questions/_tracker/level-XX-manifest.json`, change the code's `"status": "pending"` to `"status": "validated"`.
8. **Rebuild index**: `python3 build-index.py` from project root.
9. **Delete the builder script**: `rm questions/_tracker/build_<CODE>.py`.
10. **Report briefly to the user**: code, pass/fail, key metrics (char-bias %, longest %), index entry count. Wait for the user's go-ahead before the next file.

### Hard rules — never break

- **Never use sub-agents (Agent tool) for new generation.** They time out mid-file and lose work. Author directly in the main conversation. Sub-agents are acceptable only for bounded mechanical tasks like distractor regeneration on existing files.
- **One file at a time, sequentially.** Wait for `Passed: 1/1` before starting the next.
- **Never overwrite a validated file** without checking — the manifest is the source of truth for what's done.

---

## Status snapshot

**Validated this session:**
- VC2HP8M01, VC2HP8M02 (distractor-regen pass for length-bias remediation)
- VC2HP8M03, VC2HP8M04 (full new generation)
- Manifest updated to reflect all four.

**Workflow hardening this session:**
- Added `MC_CHAR_LENGTH_BIAS` rule to `validate.py`
- Added per-item mechanical length rule (4f) and self-check step (4i) to `generation-prompt-master.md`
- Cleared all stale workflow artifacts from the questions tree (`.pre-distractor-regen.json`, `.distractor-brief.json`, `.new-distractors.json`, `.pre-mc-regen.json`)

---

## Pending queue

### Year 7 HPE (1 file, age band 11–12)

| Code | Path |
|---|---|
| VC2HPFP07 | `questions/level-07/Health and Physical Education/` |

Note: ages 11–12 use **3 MC options** (not 4). TF ≤22 words, MC stem ≤55 words, MC option ≤20 words.

### Year 8 HPE — Movement (M05–M10, 6 files, age 13–14)

| Code | Topic |
|---|---|
| VC2HP8M05 | regular physical activity → health/fitness over time |
| VC2HP8M06 | community / outdoor / aquatic settings → health, safety, social outcomes |
| VC2HP8M07 | designing/justifying a physical activity plan; less sitting |
| VC2HP8M08 | propose/test/evaluate movement strategies in different situations |
| VC2HP8M09 | equipment/rules/scoring modifications → fair play, inclusion |
| VC2HP8M10 | leadership, collaboration, group decision-making |

### Year 8 HPE — Personal & Social (P01–P10, 10 files, age 13–14)

| Code | Topic |
|---|---|
| VC2HP8P01 | values and beliefs → identity development |
| VC2HP8P02 | life changes/transitions → support strategies |
| VC2HP8P03 | roles, decision-making, power dynamics in relationships |
| VC2HP8P04 | respect, empathy, power, coercion in relationships |
| VC2HP8P05 | valuing diversity → community inclusion |
| VC2HP8P06 | emotional responses → emotion management strategies |
| VC2HP8P07 | assertive/respectful communication; consent |
| VC2HP8P08 | protective behaviours → community help-seeking |
| VC2HP8P09 | media and influencers → health attitudes |
| VC2HP8P10 | strategies to improve own/others' health, safety, wellbeing |

### Year 8 Community Health (HC8K01–HC8S08, 20 files, age 13–14)

12 K-codes (`VC2HC8K01` to `VC2HC8K12`) and 8 S-codes (`VC2HC8S01` to `VC2HC8S08`). Read each skeleton's `keyKnowledge` on pickup. Path: `questions/level-08/Health - Community Health/`.

### Year 10 HPE — Movement (M01–M10, 10 files, age 15–16)

Path: `questions/level-10/Health and Physical Education/`. Age 15–16 uses **VCE-formal voice** — see `Question Specifications/Exam Voice specifications/VCAA_VCE_Unified_Exam_Voice.md`. 4 MC options, ≤40 words per option.

### Year 10 HPE — Personal & Social (P01–P10)

10 codes total. **VC2HP10P04 is already validated** from a prior Y10 sample-set run — skip it. Generate P01, P02, P03, P05–P10 (9 files).

### Year 10 Community Health (HC10K01–HC10S08, ~19 files)

Path: `questions/level-10/Health - Community Health/`. **VC2HC10K10 is already validated** from the Y10 sample set — skip it. Generate the remaining ~19.

### Year 9 — none

No Year 9 Health skeletons exist in the project. Skip.

---

## Hard validator limits (age-banded)

| Parameter | 11–12 (Y7) | 13–14 (Y8) | 15–16 (Y10) |
|---|---|---|---|
| TF max words | 22 | 28 | 35 |
| MC stem max words | 55 | 80 | 130 |
| MC option max words | 20 | 30 | 40 |
| MC options total | 3 | 4 | 4 |
| MC distractors | 2 | 3 | 3 |
| FK grade max | 7.0 | 9.0 | 11.0 |

File-level rules (applied by validator on every file):
- TF FALSE balance per Bloom level: 55–65% (or ≥1 if only 2 TF items)
- MC option parity: ±20% words AND ±30% chars within each item
- `MC_SYSTEMATIC_LENGTH_BIAS`: correct longest in ≤30% of MC items (4-option) or ≤40% (3-option)
- `MC_CHAR_LENGTH_BIAS` (added this session): ≤10% of items where correct chars > max distractor + 8 AND ≥30% above avg
- Variant similarity: <40% content-word overlap between any two variants in same Bloom level
- No contractions in stems — including possessive `'s`

---

## Drift lessons from M03/M04 (apply to every file)

These cost rebuild cycles. Avoid up front:

1. **Possessive `'s` triggers `MC_CONTRACTION`.** Replace `unit's concepts` → `concepts in this unit`. Replace `student's view` → `view of the student`. Validator does not distinguish possessive from contraction.
2. **The "Which best example of [X] concept" stem family triggers variant-similarity warnings** when used across multiple Bloom levels for the same concept set. Vary stem opener: scenario clauses, named characters, different verb phrases. Don't repeat the same template.
3. **TF balance: count carefully.** L2 with 12 TF needs 7 FALSE (58%). L3 with 8 TF needs 5 FALSE (62%). L4 with 2 TF needs ≥1 FALSE.
4. **Cloze that paraphrases a TF in the same Bloom level triggers variant-similarity.** A TF defining a term plus a cloze blanking that same term tend to overlap. Test different aspects of the topic across types.
5. **MC parity per item**: write the longest distractor first, then the correct answer at or below that character count, then remaining distractors within ±20% words / ±30% chars of mean. Track file-level "correct strictly longest" — keep ≤15/50.
6. **No ATSI forcing** unless `_source.y` or `_source.eg` references Aboriginal or Torres Strait Islander knowledge. Thoughtful omission > tokenistic inclusion.

---

## Sensitive-content guidance (P-series and Community Health)

P-series files (consent, coercion, emotional regulation, protective behaviours) and many Community Health codes cover topics that need extra care:

- Voice register: secondary-neutral (Y7–8) or VCE-formal (Y10) as age-appropriate. Never second person. No hedging. No colloquialism.
- FALSE TF items must target real, documented student misconceptions — never offensive, trivialising, or harmful framings. Prejudice is not a misconception.
- Distractors should be plausible misunderstandings, not dismissive shortcuts.
- Verify content against the skeleton's `_source` and the curriculum source rather than improvising. The closer to the curriculum text, the safer.
- For consent/relationships content (Y8 P03/P04/P07/P08; Y10 equivalents), prefer scenario-based items where named characters demonstrate the principle, with distractors that name common misconceptions (e.g. "passive non-response equals consent" → FALSE).
- For emotional regulation and mental health content, avoid distractors that promote unhealthy coping strategies, even as wrong answers. Distractors should target *misunderstandings about strategies*, not *the strategies themselves*.

If a file requires content beyond what the skeleton clearly supports, pause and ask the user before proceeding.

---

## Optional efficiency improvement (consider before continuing)

The M03/M04 builders each took 1–2 fix cycles. Two upstream changes would cut this:

1. **Shared authoring lint helper** at `questions/_tracker/lint_authoring.py`. Each builder imports it and calls `lint_authoring.check(items)` before writing the JSON. Catches contractions, word-count violations, FALSE balance, and char parity locally — turns rebuild cycles into edit-and-rerun cycles.
2. **Pre-validation in the builder template**. Same checks inline. Less reusable but no shared dependency.

Either is optional. The validator already catches everything; the lint helper just shifts detection earlier. Skip if you'd rather just generate.

---

## After every file: report template

```
VC2HPxxxxx — PASS
- 104 questions (22 TF + 50 MC + 32 Cloze)
- Char-bias: X/50 (Y%)
- Correct-strictly-longest: X/50 (Y%)
- Manifest updated, index rebuilt (N entries), builder removed.
- Next: VC2HPxxxxx
```

---

## Files / paths quick reference

| Resource | Path |
|---|---|
| Skeletons | `questions/level-XX/<area folder>/<CODE>.skeleton.json` |
| Output | `questions/level-XX/<area folder>/<CODE>.json` |
| Manifest | `questions/_tracker/level-XX-manifest.json` |
| Validator | `questions/_validation/validate.py` |
| Index builder | `build-index.py` (project root) |
| Generation prompt | `questions/_tracker/generation-prompt-master.md` |
| Voice guide (Y7–8) | `Question Specifications/voice-guide-secondary-7-9.md` |
| Voice guide (Y10) | `Question Specifications/Exam Voice specifications/VCAA_VCE_Unified_Exam_Voice.md` |
| ATSI guide | `Question Specifications/atsi-integration-guide.md` |
| Sequential rule | `questions/_tracker/SEQUENTIAL-GENERATION.md` |
| Project-wide handoff | `questions/_tracker/HANDOFF.md` |
