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
