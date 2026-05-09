# Session Handoff — Question Generation

## What This Project Is

A Victorian Curriculum v2 (VC2) student self-assessment app. We are batch-generating 104 assessment questions per curriculum code (TF / MC / Cloze across Bloom's levels 2–5) and serving them to a static HTML front end (`knowledge-check.html`) deployed on GitHub Pages.

## CRITICAL RULES — READ FIRST

1. **Generate question files ONE AT A TIME, sequentially.** Never run multiple codes in parallel.
2. **Do NOT use sub-agents (the Agent tool) for question generation.** Agents run too long, exhaust credits mid-file, and the generated content is lost when they time out. This has happened multiple times. (Agents are acceptable for bounded mechanical tasks like distractor regeneration — see §Regeneration below — but never for fresh generation.)
3. **Generate directly in the main conversation.** Read the skeleton, read the generation prompt, build the JSON yourself, write the file, validate, fix, move on.
4. **After every new file, rebuild the index:** `python3 build-index.py`. The HTML viewer reads `files-index.json` to know what is available.

Read `questions/_tracker/SEQUENTIAL-GENERATION.md` for background on rule 1/2.

---

## Current State (21 April 2026)

### Valid files: 82 total · 8,528 questions

| Year | Subject | Count | Notes |
|------|---------|-------|-------|
| 2    | Science | 1 | VC2S2U01 |
| 8    | Science | 29 | **COMPLETE** (all 29 codes; distractor-regen audit pass complete) |
| 8    | Mathematics | 1 | VC2M8N01 |
| 8    | Music | 1 | VC2AMU8E01 |
| 8    | Health & PE | 2 | VC2HP8M01, M02 |
| 10   | Science | 29 | **COMPLETE** (all 29 codes; distractor-regen audit pass complete) |
| 10   | Y10 sample set | 19 | One CD per subject — see §Y10 sample set below |

### Y10 sample set (19 files — one CD per subject)

Generated this session as a "flavour" preview before committing to the full 740-file Y10 run. Each passes the validator clean.

| Subject | Code | Folder path |
|---------|------|-------------|
| English | VC2E10LY05 | `English/` |
| Mathematics | VC2M10A13 | `Mathematics/` |
| History | VC2HH10K21 | `History/` |
| Geography | VC2HG10K12 | `Geography/` (includes ATSI content — Kulin Nation, Gunditjmara/Budj Bim) |
| Civics & Citizenship | VC2HC10K10 | `Health - Community Health/` ⚠️ (see folder/area note below) |
| Economics & Business | VC2HE10K08 | `Economics and Business/` |
| Health & PE | VC2HP10P04 | `Health and Physical Education/` |
| Personal & Social Capability | VC2CP10S04 | `Personal and Social Capability/` |
| Critical & Creative Thinking | VC2CC10Q02 | `Civics and Citizenship/` ⚠️ (see note) |
| Ethical Capability | VC2CE10U02 | `Critical and Creative Thinking/` ⚠️ (see note) |
| Intercultural Capability | VC2CI10C02 | `Intercultural Capability/` |
| Dance | VC2ADA10P01 | `Dance/` |
| Drama | VC2ADR10C02 | `Drama/` |
| Media Arts | VC2AMA10D01 | `Media Arts/` |
| Music | VC2AMU10E02 | `Music/` (includes ATSI musicians) |
| Visual Arts | VC2AVA10E01 | `Visual Arts/` (includes ATSI artists — Emily Kame Kngwarreye, Albert Namatjira, Richard Bell) |
| Visual Communication Design | VC2AVC10P01 | `Visual Communication Design/` |
| Design & Technologies | VC2TDE10D05 | `Design and Technologies/` |
| Digital Technologies | VC2TDI10S02 | `Digital Technologies/` |

### ⚠️ Folder / area label mismatches (inherited from `units_of_work.json`)

`units_of_work.json` maps area code `CC` → "Civics and Citizenship" and `CE` → "Critical and Creative Thinking" — the opposite of typical VCAA naming. As a result:
- `VC2CC10Q02` (Critical-thinking content) lives in folder `Civics and Citizenship/` because that matches `area.label` for `CC`.
- `VC2CE10U02` (Ethical content) lives in folder `Critical and Creative Thinking/` because that matches `area.label` for `CE`.

The HTML viewer works correctly because it follows the same `units_of_work.json` mapping. But if you rename folders later, update `units_of_work.json → areas[CC/CE].label` at the same time, and re-run `build-index.py`.

---

## Remaining (RESUME HERE)

The 19 Y10 samples are the preview. Once the curriculum team signs off on the "flavour", the remaining target is the full 740-CD corpus:

| Subject | Year | Codes remaining | Approx count |
|---------|------|-----------------|--------------|
| Mathematics | 7 | All 31 codes (A01-A06, M01-M06, N01-N10, P01-P02, SP01-SP04, ST01-ST03) | 31 |
| Mathematics | 8 | All except N01 — 28 codes | 28 |
| Mathematics | 9 | All 24 codes | 24 |
| Mathematics | 10 | All 56 codes (55 remaining once sample is discounted) | 55 |
| All Y7, Y9 subjects | 7, 9 | Not started | ~200 |
| Y10 non-Science non-sample | 10 | Everything except the 19 samples + 29 Science | ~350 |
| Primary levels 3-7 | 3-7 | Not started | ~various |

Exact remaining counts depend on how the team sequences the full run. The 19-file flavour preview was the gate — once approved, scale up subject by subject following the procedure below.

---

## How to Generate One Code

**Do this yourself in the main conversation. Do NOT delegate to agents.**

```
1. Delete any existing invalid .json file for that code
2. Read: questions/level-XX/Subject/CODE.skeleton.json
3. Read: questions/_tracker/generation-prompt-master.md  (MC RULE 4 — two authoring methods)
4. Fill all null fields directly, remove _source block
5. Write to: questions/level-XX/Subject/CODE.json
6. Validate: python3 questions/_validation/validate.py <file>
7. Fix and re-validate until Passed: 1/1
8. After clean pass, rebuild the index: python3 build-index.py
9. Only then start the next code
```

### Common validator errors and fixes

| Error | Fix |
|-------|-----|
| `TF_BALANCE` — FALSE under 55% at a Bloom's level | Flip True items to False by inverting the claim; update explanations accordingly |
| `MC_OPTION_PARITY` — option >20% longer than mean | Trim the longest option (usually the overlong one is the correct answer or a distractor you wrote after the others) |
| `MC_OPTION_CHAR_PARITY` — option >30% longer than mean by chars | Same fix; use a synonym that is shorter/longer as needed |
| `MC_SYSTEMATIC_LENGTH_BIAS` — correct-longest >30% | Lengthen at least one distractor per flagged question, or trim the correct answer |
| `MC_CONTRACTION` — contraction in stem | Replace "don't"/"I don't know" etc. with "does not"/"do not know"; remember quoted contractions in stems still fail |
| `VARIANT_SIMILARITY` (warning) | Reword a variant with more distinctive content words — fine to leave as warning if minor |

---

## Age Band Parameters

| Year | Age | Voice | MC options | TF max | MC stem max | MC opt max | MC phrasing |
|------|-----|-------|-----------|--------|-------------|------------|-------------|
| 7    | 11-12 | secondary-neutral | 3 | 22w | 55w | 20w | "Which of the following..." |
| 8-9  | 13-14 | secondary-neutral | 4 | 28w | 80w | 30w | "Which one of the following..." |
| 10   | 15-16 | vce-formal | 4 | 35w | 130w | 40w | "Which one of the following..." |

## Question Distribution (same for all codes)

| Bloom's | TF | MC | Cloze | Total |
|---------|----|----|-------|-------|
| 2 (Remember)   | 12 | 12 | 2  | 26 |
| 3 (Understand) | 8  | 12 | 6  | 26 |
| 4 (Apply)      | 2  | 12 | 12 | 26 |
| 5 (Analyse)    | 0  | 14 | 12 | 26 |

---

## MC Parity & Distractor Quality

### The problem we discovered (March–April 2026)

Audit of the first 60 completed question files (3,000 MC questions) revealed a systematic bias: **the correct answer was the longest option in 53% of MC questions** — more than double the 25% chance rate for 4-option MC. A test-wise student could pick the longest option and score above chance without knowing the content.

Root cause: when the LLM writes the correct answer first, it accumulates specificity and detail. Distractors written afterwards come out shorter or more obviously wrong. The length gap becomes an exploitable cue.

### Fix: two valid authoring methods — alternate between them

Both methods below produce parity-compliant MC questions. **Alternate between them across a file** (e.g. odd-numbered MC → Method A, even-numbered → Method B) to avoid any single-ordering bias accumulating across the corpus.

**Non-negotiables for either method:**

- **Interchangeable form.** Every option — correct and incorrect — reads as a confident, specific, substantive claim. A test-wise student scanning for the "most detailed" option must find no signal.
- **Wrong for ONE reason.** Each distractor is wrong for a single, identifiable reason that maps to a real student misconception. Not vague, not a shortcut, not obviously incomplete.
- **Length parity.** ±20% word count and ±30% char count vs the correct answer. At least one distractor per question matches or slightly exceeds the correct answer's length.
- **Corpus target.** ≤30% correct-longest for 4-option MC (≤40% for 3-option). Validator enforces this.

#### Method A — Distractor-first

1. Write the stem.
2. Write the three distractors FIRST, each a confident substantive claim targeting one misconception.
3. Then write the correct answer at comparable length and specificity.

Strength: avoids the "correct answer accumulates detail" bias that caused the original 53% problem.

#### Method B — Correct-first with parity discipline

1. Write the stem.
2. Write the correct answer.
3. **Lock a length target** from the correct answer's word count (±20%).
4. Write each distractor to that target, each wrong for one identifiable misconception.

Strength: anchors the scientific truth first; reliable when the parity target is set explicitly before drafting distractors. Fails when the parity step is skipped — do not use Method B without step 3.

`generation-prompt-master.md` documents both methods (MC RULE 4).

### Validator thresholds (current)

| Check | Threshold | Location in `validate.py` |
|-------|-----------|----------------------------|
| Correct-longest (4-option MC) | ≤ 30% across the file's 50 MC questions | `validate_mc_correct_position_balance` |
| Correct-longest (3-option MC) | ≤ 40% | same |
| Per-question word parity | ±20% vs mean | `validate_mc_option_parity` |
| Per-question character parity | ±30% vs mean | `validate_mc_option_char_parity` |
| TF FALSE balance per Bloom's level | 55–65% (≥1 FALSE if ≤3 TF at a level) | `validate_tf_false_balance` |
| Contractions in stems | Forbidden (including inside quoted phrases) | `validate_mc_contractions` |
| Flesch-Kincaid | ≤ 11.0 (age 15-16) | `validate_readability` |

Validator rejects files exceeding any of these thresholds — nothing commits to the corpus with systematic bias.

### Edge cases to accept

- **Single-word correct answers** (e.g. "Methane", "Europa", "Homeostasis"): character parity can fail when distractors must also be single-word terms of differing natural length. Accept as-is.
- **Distractor answers that must literally name the misconception** referenced in the `explanation` field (e.g. "Confuses solar radiation with..."): changing the answer text would desync the explanation. If parity fails, use a shorter synonym (e.g. "sunlight" instead of "solar radiation") and update the explanation to match.

### Auditing existing files for length bias

```bash
python3 -c "
import json, glob
for fpath in sorted(glob.glob('questions/level-XX/Subject/*.json')):
    if '.' in fpath.rsplit('/',1)[-1].split('.',1)[0]: continue  # skip .pre-regen, .new-distractors etc.
    if '.skeleton.' in fpath: continue
    with open(fpath) as f: data = json.load(f)
    total=0; cl=0
    for lk in ['toLevel2','toLevel3','toLevel4','toLevel5']:
        for q in data[lk]:
            if q['type'] != 'mc': continue
            total += 1
            if len(q['correct'].split()) > max(len(d['answer'].split()) for d in q['distractors']): cl += 1
    pct = cl/total*100
    print(f'{data[\"_meta\"][\"code\"]}: {pct:.0f}%')
"
```

Files with >30% correct-longest (4-option) or >40% (3-option) need distractor regeneration.

### Regeneration tool: `extract-mc-for-regen.py`

Three modes:

| Mode | Purpose |
|------|---------|
| `strip` | Null out all MC content, regenerate from scratch (legacy; rarely used now) |
| `regen-distractors` | **Preferred.** Keep stems and correct answers, only replace distractor `answer` text |
| `merge` | Slot new distractors back, auto-validate, commit only if valid |

Location: `questions/_tracker/extract-mc-for-regen.py`

### Distractor regeneration workflow

For each file needing regeneration (audit shows >30% correct-longest):

1. **Extract the brief**
   ```
   python3 questions/_tracker/extract-mc-for-regen.py regen-distractors <path-to-CODE.json>
   ```
   Creates backup (`CODE.pre-distractor-regen.json`) + a brief (`CODE.distractor-brief.json`) listing each MC question's stem, correct answer, word count, target distractor range, and existing misconception explanation.

2. **Generate new distractors** (sequential agents work here; parallel agents fail rate limits)
   - Each agent reads the brief + generation-prompt-master + original file
   - Agent writes new `answer` strings matching the correct answer's length and specificity
   - Agent verifies correct-longest ≤30% across the 50 MC questions
   - Agent writes output to `<CODE>.new-distractors.json`

3. **Merge**
   ```
   python3 questions/_tracker/extract-mc-for-regen.py merge <original> <new-mc>
   ```
   Slots new distractors in, re-validates, commits only if validation passes. If validation fails, temp file is kept for inspection and the original is unchanged.

4. **Clean up** the `.new-distractors.json`, `.distractor-brief.json`, and `.pre-distractor-regen.json` artefacts.

⚠️ The regen artefacts (`.distractor-brief.json`, `.new-distractors.json`, `.pre-distractor-regen.json`) must NOT appear in `files-index.json`. `build-index.py` skips any file whose stem contains a dot — do not commit artefacts with clean-looking names.

### Regen audit history

| Corpus | Before | After | Status |
|--------|--------|-------|--------|
| Y10 Science (29 files) | 53% avg correct-longest, +3.7w avg diff | 15% avg correct-longest, 0.0w avg diff | COMPLETE |
| Y8 Science (29 files)  | (similar pre-audit profile) | all passing 30% threshold | COMPLETE (April 2026) |

All generation since the audit uses the two-methods procedure up front; the regen workflow is there for future audit passes if needed.

---

## HTML viewer & GitHub Pages deployment

### Key files

- `knowledge-check.html` — single-file SPA, student self-assessment flow
- `files-index.json` — list of available CD files (rebuild after every new file)
- `units_of_work.json` — area / unit / CD structure (source of truth for which CDs exist per subject)
- `cd_explanations.json` — per-CD "this is worth knowing because…" blurbs
- `serve.py` — local dev server on port 8765, subclasses `SimpleHTTPRequestHandler` to send `Cache-Control: no-store` so browsers always see the latest data

### No-cache fetch

`knowledge-check.html` calls `fetch(url, { cache: 'no-store' })` for all JSON data loads. Both the client option and the server header are needed because either alone can be overridden by browser policy.

### Deployment

Served via GitHub Pages from the `cognito` repo (separate from this working directory). After any change:

1. Rebuild index: `python3 build-index.py`
2. Copy changed files to the clone
3. Commit + push
4. GitHub Pages rebuilds in ~1 minute; CDN cache clears within ~10

### Known integration notes

- GitHub Pages is case-sensitive (Linux filesystem); your Mac is not. If fetches 404 on Pages but not locally, check folder case matches `area.label` in `units_of_work.json` exactly.
- Folder names with spaces (e.g. `Health - Community Health`, `Visual Communication Design`) are fine — browsers URL-encode the space automatically in `fetch()`.

---

## Key Files (reference)

- `questions/_tracker/generation-prompt-master.md` — Full generation rules (read this before generating)
- `questions/_tracker/SEQUENTIAL-GENERATION.md` — Why and how to generate one at a time
- `questions/_tracker/GENERATION-WORKFLOW.md` — Master workflow document
- `questions/_validation/validate.py` — Validation script (use `python3`, not `python`)
- `questions/_tracker/extract-mc-for-regen.py` — Regen tool (modes: strip / regen-distractors / merge)
- `build-index.py` — Rebuilds `files-index.json`. Run after every new file. Skips `.skeleton.json` and any file with a dot in its stem (i.e. regen artefacts).
- `serve.py` — Local dev server with no-cache headers (port 8765)
- `question-viewer.py` — Alternative local web viewer at http://localhost:8777 (older tool, still available)

## Question Viewer (local)

```bash
python3 serve.py                            # current HTML front end, port 8765
# then open http://localhost:8765/knowledge-check.html
# or
python3 question-viewer.py                  # legacy viewer, port 8777
```

Browse by level/subject, filter by Bloom's level and question type.
