# Session Handoff — Question Generation

## What This Project Is

A Victorian Curriculum v2 (VC2) student self-assessment app. We are batch-generating 104 assessment questions per curriculum code (TF / MC / Cloze across Bloom's levels 2-5).

## CRITICAL RULES — READ FIRST

1. **Generate question files ONE AT A TIME, sequentially.** Never run multiple codes in parallel.
2. **Do NOT use sub-agents (the Agent tool) for generation.** Agents run too long, exhaust credits mid-file, and the generated content is lost when they time out. This has happened multiple times.
3. **Generate directly in the main conversation.** Read the skeleton, read the generation prompt, build the JSON yourself, write the file, validate, fix, move on.

Read `questions/_tracker/SEQUENTIAL-GENERATION.md` for background. The short version: one code at a time, no agents, no parallelism.

## Current State (as of 2026-04-11, session 3)

### Valid files (47 total, 4,888 questions)

| Subject | Year | Codes | Count |
|---------|------|-------|-------|
| Science | 2 | S2U01 | 1 |
| Science | 8 | H01-H04, I01-I08, U01-U17 | 29 |
| Mathematics | 8 | N01 | 1 |
| Music | 8 | AMU8E01 | 1 |
| Science | 10 | H01-H04, I01-I08, U01, U08, U09 | 15 |

### Y8 Science — COMPLETE

All 29 Y8 Science codes are now generated and validated.

### Remaining (RESUME HERE)

| Subject | Year | Codes needed | Count |
|---------|------|-------------|-------|
| Science | 10 | U02-U07, U10-U17 | 13 |
| Mathematics | 7 | All 31 codes (A01-A06, M01-M06, N01-N10, P01-P02, SP01-SP04, ST01-ST03) | 31 |
| Mathematics | 8 | All except N01 — 28 codes (A01-A05, M01-M07, N02-N06, P01-P03, SP01-SP04, ST01-ST04) | 28 |
| Mathematics | 9 | All 24 codes (A01-A07, M01-M05, N01, P01-P03, SP01-SP03, ST01-ST05) | 24 |
| Mathematics | 10 | All 56 codes | 56 |

**Total remaining: 152 codes**

## How to Generate One Code

**Do this yourself in the main conversation. Do NOT delegate to agents.**

```
1. Delete any existing invalid .json file for that code
2. Read: questions/level-XX/Subject/CODE.skeleton.json
3. Read: questions/_tracker/generation-prompt-master.md
4. Fill all null fields directly, remove _source block
5. Write to: questions/level-XX/Subject/CODE.json
6. Validate: python3 questions/_validation/validate.py <file>
7. Fix and re-validate until Passed: 1/1
8. Confirm Passed: 1/1
9. Only then start the next code
```

## Age Band Parameters

| Year | Age | Voice | MC options | TF max | MC stem max | MC opt max | MC phrasing |
|------|-----|-------|-----------|--------|-------------|------------|-------------|
| 7 | 11-12 | secondary-neutral | 3 | 22w | 55w | 20w | "Which of the following..." |
| 8-9 | 13-14 | secondary-neutral | 4 | 28w | 80w | 30w | "Which one of the following..." |
| 10 | 15-16 | vce-formal | 4 | 35w | 130w | 40w | "Which one of the following..." |

## Question Distribution (same for all codes)

| Bloom's | TF | MC | Cloze | Total |
|---------|----|----|-------|-------|
| 2 (Remember) | 12 | 12 | 2 | 26 |
| 3 (Understand) | 8 | 12 | 6 | 26 |
| 4 (Apply) | 2 | 12 | 12 | 26 |
| 5 (Analyse) | 0 | 14 | 12 | 26 |

## Key Files

- `questions/_tracker/generation-prompt-master.md` — Full generation rules (read this before generating)
- `questions/_tracker/SEQUENTIAL-GENERATION.md` — Why and how to generate one at a time
- `questions/_tracker/GENERATION-WORKFLOW.md` — Master workflow document
- `questions/_validation/validate.py` — Validation script (use `python3`, not `python`)
- `question-viewer.py` — Local web viewer at http://localhost:8777

## Question Viewer

```bash
python3 question-viewer.py
# Open http://localhost:8777
```

Browse by level/subject, filter by Bloom's level and question type, validate in-browser.

---

## Distractor Quality & Option Length — Revised Procedure (April 2026)

### The problem we discovered

Audit of the first 60 completed question files (3,000 MC questions) revealed a systematic bias: **the correct answer was the longest option in 53% of MC questions** — more than double the 25% chance rate for 4-option MC. A test-wise student could pick the longest option and score above chance without knowing the content.

Root cause: when the LLM writes the correct answer first, it accumulates specificity and detail. When it then writes distractors, they come out shorter, more shortcut-ish, or more obviously wrong. The length gap becomes an exploitable cue.

### Fix: two valid authoring methods — alternate between them

Both methods below produce parity-compliant MC questions. **Alternate between them across a file** (e.g. odd-numbered MC → Method A, even-numbered → Method B) to avoid any single-ordering bias accumulating across the corpus.

Non-negotiables for either method:
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

`generation-prompt-master.md` documents both methods.

### Tightened validator thresholds

- **Correct-longest cap: 30%** for 4-option MC (down from 40%)
- **Correct-longest cap: 40%** for 3-option MC (down from 50%)
- **Per-question parity: ±20% word count AND ±30% character count** (unchanged)
- Validator rejects files exceeding either threshold — nothing commits to the corpus with systematic bias

Location: `questions/_validation/validate.py` → `validate_mc_correct_position_balance`

### Auditing existing files for length bias

```bash
python3 -c "
import json, glob
for fpath in sorted(glob.glob('questions/level-XX/Subject/*.json')):
    if '.skeleton.' in fpath or '.pre-' in fpath: continue
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
| `regen-distractors` | **Preferred for fixing existing files.** Keep stems and correct answers, only replace distractor `answer` text |
| `merge` | Slot new distractors back, auto-validate, commit only if valid |

Location: `questions/_tracker/extract-mc-for-regen.py`

### Distractor regeneration workflow

For each file needing regeneration (audit shows >30% correct-longest):

1. **Extract the brief**
   ```
   python3 questions/_tracker/extract-mc-for-regen.py regen-distractors <path-to-CODE.json>
   ```
   Creates backup + a brief listing each MC question's stem, correct answer, correct word count, target distractor range, and the existing misconception explanation.

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

4. **Clean up** the `.new-distractors.json` and `.distractor-brief.json` files.

### Progress on the audit/fix pass

**Year 10 Science (29 files): COMPLETE**
- Before: 53% avg correct-longest, +3.7w avg diff
- After: 15% avg correct-longest, 0.0w avg diff
- All files pass the 30% threshold

**Year 8 Science (29 files): IN PROGRESS (as of 17 April 2026)**
- 9 files already passed (I04, I06, I07, I08, U07, U11, U13, U14, H04)
- 20 files needed regen — being processed in batches

### Edge cases to accept

Some MC questions have structural constraints where strict parity is unavoidable:

- **Single-word correct answers** (e.g. "Methane", "Europa", "Homeostasis"): character parity can fail when distractors must also be single-word terms of differing natural length. Accept as-is.
- **Distractor answers that must literally name the misconception** referenced in the `explanation` field (e.g. "Confuses solar radiation with..."): changing the answer text would desync the explanation. If parity fails, use a shorter synonym (e.g. "sunlight" instead of "solar radiation") and update the explanation to match.

### When generating new question files from scratch

The same rules apply:
1. Read `generation-prompt-master.md` — MC RULE 4 (two authoring methods)
2. Alternate Method A (distractor-first) and Method B (correct-first with parity lock) across the file's MC questions
3. Make at least one distractor match or slightly exceed the correct answer's length, regardless of method
4. Run validator after each file — it enforces the 30% / 40% caps
5. If validation fails on `MC_SYSTEMATIC_LENGTH_BIAS`, fix the specific questions flagged before moving on

This should prevent the need for future audit/regen passes on newly generated files.
