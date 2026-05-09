# Humanities Generation — Session Handoff (Y2–Y10)

Scope: History, Geography, Civics & Citizenship, Economics & Business across years 2, 4, 6, 8, 10.

**Status as of 2026-05-09**: 29 files validated, 323 pending. Y8 Economics now COMPLETE (16/16).

| Subject | Y2 | Y4 | Y6 | Y8 | Y10 | Total | Validated |
|---|---:|---:|---:|---:|---:|---:|---:|
| History | 14 | 19 | 22 | 38 | 51 | 144 | 0 |
| Geography | 12 | 15 | 15 | 29 | 25 | 96 | 0 |
| Civics & Citizenship | — | 12 | 15 | 20 | 19 | 66 | 0 |
| Economics & Business | — | — | 14 | 16 | 16 | 46 | **29** (Y6 K01–K07 + S01–S04; Y8 K01–K10 + S01–S06 — Y8 COMPLETE) |
| **Total** | 26 | 46 | 66 | 103 | 111 | **352** | **29** |

**Next pending code**: First Y8 Geography or Civics file (per recommended sequence: Geography next), OR Y6 Economics S05–S07 if returning to complete Y6 Economics.

**Y8 Economics summary**: All 16 files validated (K01–K10, S01–S06). 104 questions per file × 16 files = 1,664 questions. Index has 111 entries.

**Discipline that worked for the lean Y8 builds**:
- Distractors at 16-22 words from the first draft, never padded with "in any country at any stage of any year today" tails.
- TF balance check before validation: count FALSE during drafting; flip 2-3 in L2 and 1-2 in L3 if natural drafting under-shoots.
- Parity issues: when one distractor exceeds 1.20× mean, trim it down rather than padding others up. Each option ideally within 16-22 words.

User direction: skipping forward through Y8 humanities in batches of 3 before returning to Y6 S05–S07. After Y8 humanities complete, move to Y10 humanities ("9–10" learning area band per user).

**Lessons learned this session**:
- For Y8 (4 MC options, max 30 words/option), keep distractors lean from the first draft. Padding distractors with verbose tail phrases like "in any year of any life today at every stage" produces overflow errors and parity failures that are expensive to repair. Aim for 16–22 words per option.
- The bulk-trim sed approach corrupted parity in K06's first attempt — had to rewrite the whole file. Lean from the start beats trim-after.
- TF balance bug pattern: writing alternating True/False naturally produces 4-5 FALSE in a 12-item L2; need to track and flip 2-3 more to FALSE during drafting to hit the 7/12 minimum.

---

## START HERE — Picking up this work

**You are resuming sequential generation of Humanities question files for the Victorian Curriculum v2 navigator.** Read this section, then jump to the next pending code.

### First message template

Paste this as your first message to confirm setup before generating:

> Resuming Humanities generation per `questions/_tracker/HUMANITIES-HANDOFF.md`. I'll read this handoff, the generation prompt master, and the relevant voice guide for the target age band, then start with the next pending code from the queue. After each file: validate to `Passed: 1/1`, update the level manifest, rebuild the index, delete the builder script, then move to the next file. I will work sequentially, one file at a time — never via sub-agents.

### Step-by-step kickoff

1. **Read the rules** (in this order):
   - This handoff
   - Generation prompt master (`questions/_tracker/generation-prompt-master.md`) — contains the latest `MC_CHAR_LENGTH_BIAS` rule and per-item mechanical length rule
   - Voice guide for the target age band (paths table at bottom)
   - **ATSI integration guide** (`Question Specifications/atsi-integration-guide.md`) — load this for every Humanities file. Many codes reference First Nations content directly.
2. **Pick the next pending code** from the queue tables below, in the suggested order under "Recommended sequence".
3. **Resolve the folder**: code prefix tells you the subject, but the folder layout is misaligned in this project. See "Folder mislabel" warning.
4. **Read the skeleton**: `questions/level-XX/<correct folder>/<CODE>.skeleton.json` — note `_meta.ageBand`, `_meta.keyKnowledge`, and `_source` (`w` / `y` / `eg`).
5. **Author all 104 questions** in a builder script saved at `questions/_tracker/build_<CODE>.py`. Pattern: define TF/MC/Cloze items as Python tuples per Bloom level, assemble into the skeleton structure. Set `_meta.generatedAt` to the current ISO 8601 UTC timestamp. Remove `_source` from output.
6. **Run the builder**: `python3 questions/_tracker/build_<CODE>.py`. It writes the JSON.
7. **Validate**: `python3 questions/_validation/validate.py <output-path>`. Must report `Passed: 1/1` with 0 errors. Iterate on the builder until clean.
8. **Update manifest**: in `questions/_tracker/level-XX-manifest.json`, change the code's `"status": "pending"` to `"status": "validated"`.
9. **Rebuild index**: `python3 build-index.py` from project root.
10. **Delete the builder script**: `rm questions/_tracker/build_<CODE>.py`.
11. **Report briefly to the user**: code, pass/fail, key metrics (char-bias %, longest %), index entry count. Wait for the user's go-ahead before the next file.

### Hard rules — never break

- **Never use sub-agents (Agent tool) for new generation.** They time out mid-file and lose work. Author directly in the main conversation. Sub-agents are acceptable only for bounded mechanical tasks like distractor regeneration on existing files.
- **One file at a time, sequentially.** Wait for `Passed: 1/1` before starting the next.
- **Never overwrite a validated file** without checking — the manifest is the source of truth for what's done.

---

## Folder mislabel — read before opening any file

This project has an inherited folder/area mismatch in `units_of_work.json`. The folder name does not always match the curriculum subject. Trust the code prefix, not the folder name.

| Code prefix | Subject | Folder it actually lives in |
|---|---|---|
| `HH` | History | `History/` ✓ |
| `HG` | Geography | `Geography/` ✓ |
| `HC` | Civics & Citizenship | **`Health - Community Health/`** ⚠️ |
| `HE` | Economics & Business | `Economics and Business/` ✓ |

The `Civics and Citizenship` folder you may see in the tree contains Critical & Creative Thinking content (`CC*` codes), not civics. The `Critical and Creative Thinking` folder contains Ethical Capability content. Do not be guided by folder names alone.

---

## Voice register by year band

| Years | Age band | Voice | MC options | Voice guide path |
|---|---|---|---:|---|
| Y2 | 7–8 | primary-warm | 3 | `Question Specifications/voice-guide-primary.md` |
| Y4 | 9–10 | primary-warm | 3 | same |
| Y6 | 11–12 | secondary-neutral | 3 | `Question Specifications/voice-guide-secondary-7-9.md` |
| Y8 | 13–14 | secondary-neutral | 4 | same |
| Y10 | 15–16 | VCE-formal | 4 | `Question Specifications/Exam Voice specifications/VCAA_VCE_Unified_Exam_Voice.md` |

---

## Hard validator limits (age-banded)

| Parameter | 7–8 | 9–10 | 11–12 | 13–14 | 15–16 |
|---|---:|---:|---:|---:|---:|
| TF max words | 12 | 18 | 22 | 28 | 35 |
| MC stem max words | 15 | 35 | 55 | 80 | 130 |
| MC option max words | 5 | 12 | 20 | 30 | 40 |
| MC options total | 3 | 3 | 3 | 4 | 4 |
| MC distractors | 2 | 2 | 2 | 3 | 3 |
| FK grade max | 3.0 | 5.0 | 7.0 | 9.0 | 11.0 |
| Negation in stems | NO | NO | sparingly | sparingly | permitted |

File-level rules (validator-enforced on every file):
- TF FALSE balance per Bloom level: 55–65% (or ≥1 if only 2 TF items)
- MC option parity: ±20% words AND ±30% chars within each item
- `MC_SYSTEMATIC_LENGTH_BIAS`: correct longest in ≤30% of MC items (4-option) or ≤40% (3-option)
- `MC_CHAR_LENGTH_BIAS`: ≤10% of items where correct chars > max distractor + 8 AND ≥30% above avg
- Variant similarity: <40% content-word overlap between any two variants in same Bloom level
- No contractions in stems — including possessive `'s`

---

## Recommended sequence

Order minimises drift risk by starting with low-stakes content at familiar age bands, then scaling up:

1. **Y6 Economics & Business** (14) — clean canary for Y6 secondary-neutral voice; concrete content (markets, scarcity, choice) with low ATSI surface area
2. **Y6 History** (22), then **Y6 Geography** (15), then **Y6 Civics** (15) — same age band, builds Y6 fluency
3. **Y4 History** (19), **Y4 Geography** (15), **Y4 Civics** (12) — primary-warm voice; some First Contact content in History
4. **Y2 History** (14), **Y2 Geography** (12) — youngest age band; concrete and observable; primary-warm voice
5. **Y8 Economics** (16), then **Y8 Geography** (29), **Y8 History** (38), **Y8 Civics** (20) — secondary-neutral voice with 4 MC options; substantial ATSI integration in History and Civics
6. **Y10 Economics** (16), then **Y10 Geography** (25), **Y10 History** (51), **Y10 Civics** (19) — VCE-formal voice; densest content; most demanding ATSI integration

You can deviate (e.g. user asks for History first) — but pick a Y6 file as your first canary regardless. The voice register is the dominant drift driver, not the subject content.

---

## Pending queue summary

The full per-code list is in the manifests at `questions/_tracker/level-XX-manifest.json`. Pending counts:

### History (144 files)
- Y2: 14 (`VC2HH2K*`, `VC2HH2S*`)
- Y4: 19 (`VC2HH4*`)
- Y6: 22 (`VC2HH6*`)
- Y8: 38 (`VC2HH8*`)
- Y10: 51 (`VC2HH10*`)

### Geography (96 files)
- Y2: 12, Y4: 15, Y6: 15, Y8: 29, Y10: 25

### Civics & Citizenship (66 files) — `HC*` prefix, lives in `Health - Community Health` folder
- Y4: 12, Y6: 15, Y8: 20, Y10: 19

### Economics & Business (46 files)
- Y6: 14, Y8: 16, Y10: 16

---

## ATSI integration — applies often in Humanities

A meaningful share of Humanities codes reference Aboriginal and Torres Strait Islander knowledge, history, governance, or relationships with Country. Open every skeleton's `_source.y` and `_source.eg` to check before drafting. If those fields name First Nations content, the ATSI integration guide applies.

Subjects where ATSI integration is most likely:
- **History Y4–Y10**: First Contact, frontier conflict, dispossession, Mabo and Native Title, Stolen Generations, civil rights movements, contemporary self-determination. Strength-based framing throughout. Distinguish recall (events, dates) from analysis (perspectives, impacts) — keep recall items factually precise, keep analysis items framed around documented historical interpretation.
- **Geography Y6–Y10**: Country and connection to place, traditional ecological knowledge, fire management, seasonal calendars, sustainable land management. Present tense for living cultural practices.
- **Civics Y6–Y10**: First Nations governance traditions, Constitution and recognition, citizenship, native title in legal frameworks.
- **Economics**: less common, but possible — Aboriginal trade networks pre-contact, contemporary First Nations economic development, land rights and economic outcomes.

ATSI rules to apply (from the integration guide):
- Specificity: name the nation or language group when the source allows ("Kulin Nation", "Yolngu peoples"). Avoid pan-Aboriginal generalisation.
- Present tense for continuing cultures and practices.
- Strength-based framing — never deficit framing, even in FALSE TF items.
- Never assess sacred, ceremonial, or restricted knowledge.
- FALSE TF items target documented misconceptions (e.g. "nomadic with no fixed home"), never offensive framings.
- Distractors in MC must be plausible misunderstandings, not dismissive shortcuts.

---

## Drift lessons (apply to every file)

These cost rebuild cycles. Avoid up front:

1. **Possessive `'s` triggers `MC_CONTRACTION`.** Replace `Australia's parliament` → `the Australian parliament` in stems. `student's view` → `view of the student`. Validator does not distinguish possessive from contraction. Note: TF stems and named-character setups outside MC stems do not trigger this; the rule is MC-specific.
2. **Stem family templates trigger variant-similarity.** `Which one of the following is the best example of [X]?` repeated across Bloom levels for the same concept exceeds the 40% content-word overlap threshold. Vary the stem opener: scenario clauses, named characters, different verb phrases.
3. **Repeating named characters across MC L4 and Cloze L4 is the single biggest source of variant-similarity warnings.** If MC L4 v3 uses "Mia at the snack stall," do NOT use "Mia at the snack stall" in Cloze L4. Either use generic actors in Cloze L4 ("a student", "a class", "a council") or rotate through a different name set. Counted as 8+ warnings per file when ignored.
4. **TF balance: count carefully.** Y6 (12/8/2 TF distribution) needs L2: 7 FALSE, L3: 5 FALSE, L4: ≥1 FALSE. Count before writing the builder; flipping after the fact is the most common rework cycle. Easy mistake: drafting all the obvious TRUE statements first, then realising the FALSE quota is short.
5. **Cloze paraphrasing a TF in the same Bloom level triggers variant-similarity.** Test different aspects of the topic across types — if a TF defines `composition`, do not blank `composition` in a cloze at the same level.
6. **MC parity per item**: write the longest distractor first, then the correct answer at or below that character count, then remaining distractors within ±20% words / ±30% chars of mean. Track file-level "correct strictly longest" — keep word-count `longest` ≤ 17/50 for 4-option (Y8/Y10), ≤ 19/50 for 3-option (Y2/Y4/Y6/Y7) to stay under the validator's 30%/40% caps.
7. **The validator's `MC_SYSTEMATIC_LENGTH_BIAS` uses WORD count, but my pre-write helper output uses CHAR count.** Char-based "longest" can be 50%+ while the file passes. Trust the validator's word-count check; the char-bias rule (`MC_CHAR_LENGTH_BIAS`) is a separate ≤10% threshold for the severe full-sentence-vs-short-phrase pattern.
8. **History dates and proper nouns are content words for the variant-similarity check.** Two variants both built around "1788" or "Federation" will easily exceed 40% overlap. Use varied frames: actor (a settler, a colonial governor, a Wurundjeri elder), perspective (economic, political, cultural), scale (local, colony, nation).
9. **Geography place names are content words.** Spread variants across regions; don't anchor every Y4 Geography variant on Melbourne or Australia broadly.
10. **Y6 has TF max 22 words, not 28.** Easy to overshoot if reusing patterns from Y8 work. The age-band table in this handoff is correct — refer to it when sizing TF stems.
11. **Cloze distractors must come from the same semantic category** but the cloze validator does not appear to enforce this strictly. The K01–K04 builders use `uniform`, `fixture`, `scored`, `season` as default distractors when no good in-domain alternative exists. Acceptable for now but a real reviewer would flag this — consider rotating distractors when in-domain options exist (e.g. for Economics, use `donation`, `subsidy`, `wage` rather than `uniform`).
12. **For ATSI integration**, when the source mentions First Nations content: reference the nation by name where the curriculum allows (Kulin, Yolngu, Wurundjeri), use present tense for continuing practices ("First Nations rangers care for Country today"), avoid past-tense phrasing for living cultures ("Aboriginal peoples used to..."), and target documented misconceptions for FALSE TF items ("First Nations economies had no organised work" → FALSE).

---

## Sensitive-content guidance — Humanities-specific

Several Humanities topics need extra care:

- **Frontier history and dispossession (Y4 History onward)**: present events accurately. Aboriginal peoples are agents, not objects. Avoid passive constructions that obscure colonial actors ("Land was taken" → "Colonial governments took land"). FALSE TF items target real misconceptions (e.g. "Australia was unoccupied at colonisation"), not offensive framings.
- **Stolen Generations (Y8/Y10 History)**: assess only at the level the curriculum specifies. Use the established historical record. Distractors target factual misunderstandings, not minimisation of impact.
- **Civil rights and Mabo (Y10 History/Civics)**: present in present tense where the legal/political reality is current. Native Title and the recognition process are continuing.
- **Voice/Treaty discourse (Y10 Civics)**: stick to documented historical and legal facts. Avoid contested contemporary political framing in stems or distractors.
- **Religion and cultural diversity (Y8 Civics K11)**: respectful neutrality. No religion is centred or dismissed via the question framing. Distractors target misconceptions about how diversity functions in a secular democracy, not stereotypes about specific groups.
- **Globalisation and migration (Y8/Y10 Geography, History, Economics)**: avoid framing migrants or any country as monolithic. Use specific examples.

If a file requires content beyond what the skeleton clearly supports, pause and ask the user before proceeding.

---

## Builder pattern that worked for K01–K04

Each successful builder followed this structure:

```python
"""Build VC2HE6KXX.json — Y6 Economics: <topic>. Age 11-12, 3 MC options."""
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum')
SKEL = BASE / 'questions/level-06/Economics and Business/VC2HE6KXX.skeleton.json'
OUT  = BASE / 'questions/level-06/Economics and Business/VC2HE6KXX.json'

# Data: TF as (stmt, T/F, exp_correct, exp_distractor)
# MC as (stem, [opt0, opt1, opt2], correct_idx, exp_correct, [exp_per_option])
# Cloze as (sentence_with_{{blank:N}}, [(blank_id, [opt0,opt1,opt2], correct_idx, [distractor_explanations])])

TF_L2 = [...]  # 12 items, target 7 FALSE
TF_L3 = [...]  # 8 items, target 5 FALSE
TF_L4 = [...]  # 2 items, ≥1 FALSE
MC_L2 = MC_L3 = MC_L4 = [...]  # 12 items each
MC_L5 = [...]  # 14 items
CLOZE_L2 = [...]  # 2 items
CLOZE_L3 = [...]  # 6 items
CLOZE_L4 = CLOZE_L5 = [...]  # 12 items each

# fill_tf, fill_mc, fill_cloze functions (copy from previous builder)
# main() with pre-write checks for TF balance, char-bias, longest counts
```

The pre-write checks block in main() prints `TF FALSE`, `longest_words`, `longest_chars`, and `char-bias` percentages — invaluable for iterating without running the validator each time.

## Optional efficiency improvement (consider before continuing)

Each builder typically takes 1–2 fix cycles. Two upstream changes would cut this:

1. **Shared authoring lint helper** at `questions/_tracker/lint_authoring.py`. Each builder imports it and calls `lint_authoring.check(items)` before writing the JSON. Catches contractions (including possessive `'s`), word-count violations, FALSE balance, and char parity locally — turns rebuild cycles into edit-and-rerun cycles.
2. **Pre-validation in the builder template**. Same checks inline. Less reusable but no shared dependency.

Worth implementing once for Humanities given the volume (352 files). The validator already catches everything; the lint helper just shifts detection earlier.

---

## After every file: report template

```
VC2Hxxxxxx — PASS
- 104 questions (22 TF + 50 MC + 32 Cloze)
- Char-bias: X/50 (Y%)
- Correct-strictly-longest: X/50 (Y%)
- Manifest updated, index rebuilt (N entries), builder removed.
- Next: VC2Hxxxxxx
```

---

## Files / paths quick reference

| Resource | Path |
|---|---|
| Skeletons | `questions/level-XX/<correct folder>/<CODE>.skeleton.json` (see Folder mislabel section) |
| Output | same folder, `.json` |
| Manifest | `questions/_tracker/level-XX-manifest.json` |
| Validator | `questions/_validation/validate.py` |
| Index builder | `build-index.py` (project root) |
| Generation prompt | `questions/_tracker/generation-prompt-master.md` |
| Voice guide (Y2/Y4) | `Question Specifications/voice-guide-primary.md` |
| Voice guide (Y6/Y8) | `Question Specifications/voice-guide-secondary-7-9.md` |
| Voice guide (Y10) | `Question Specifications/Exam Voice specifications/VCAA_VCE_Unified_Exam_Voice.md` |
| ATSI guide | `Question Specifications/atsi-integration-guide.md` |
| Sequential rule | `questions/_tracker/SEQUENTIAL-GENERATION.md` |
| Project-wide handoff | `questions/_tracker/HANDOFF.md` |
| Health handoff (sibling doc) | `questions/_tracker/HEALTH-HANDOFF.md` |
