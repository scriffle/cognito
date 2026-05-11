# HANDOFF — Distractor Quality Rewrite

## Status as of handoff

The "today" time-confusion error has been eliminated from all MC content across the project. The remaining issue is **distractor filler**: many distractors got padded to length parity with meaningless content like "in maths and everyday calculations across many problem types" rather than naturally-similar-length substantive maths/curriculum content.

This document is the source of truth for what's done and what's outstanding.

---

## ✅ Done

### Mission-critical "today" fix (complete)
- **2,190 question files swept** by `questions/_tracker/strip_today.py`
- **14,047 problematic "today" instances eliminated** from MC correct + distractors + explanations
- **15 legitimate uses preserved** (e.g. "today's policies", "today-only offer", "inform today's land management")
- No more time-confusion in any MC content
- Audit log: `questions/_tracker/today_audit.json` (snapshot of pre-fix state)

### Infrastructure
- `questions/_tracker/_build_lib.py` — Y8+ builder lib (4-option MC, 30-word options) — unchanged padder
- `questions/_tracker/_build_lib_y7.py` — Y7 builder lib (3-option MC, 20-word options) — padder updated to "in maths and everyday calculations across many problem types" (no "today")
- `questions/_validation/validate.py` — patched to accept levels 7 and 9
- `questions/_tracker/strip_today.py` — one-time sweep (already applied)

### Validator levels supported
- Levels 2, 4, 6, 7, 8, 9, 10 — all enum-accepted

---

## ❌ Outstanding (the real work)

### 1. Padded-distractor rewrite — primary outstanding work
**Scope: 374 files, 14,906 MC items**

Each item has 1-3 distractors padded with filler. Need substantive rewrite of each padded distractor so it reads as natural, pedagogically meaningful content of similar length to the correct answer.

**Master log:** `questions/_tracker/quality_pass_log.json`
- Structure: each file entry has `path`, `n_items_needing_rewrite`, and per-item details (level, slot index, variant, question, correct, distractors)
- Sorted by item count (worst-affected files first)

**Subject breakdown** (top contributors):

| Subject | Files | Items |
|---|---|---|
| L08 Critical & Creative Thinking | ~10 | ~500 |
| L08 Economics & Business | ~6 | ~300 |
| L08 History | 38 | ~1900 |
| L08 Civics & Citizenship | ~20 | ~1000 |
| L08 Geography | 29 | ~1450 |
| L08 HP | 16 | ~800 |
| L10 Civics & Citizenship | 18 | ~900 |
| L10 Economics & Business | 16 | ~800 |
| L10 Geography | 25 | ~1200 |
| L10 HP | 19 | ~950 |
| L10 History | 51 | ~2550 |
| L07 Mathematics | 25 | ~1250 |
| L08 Mathematics | 1 | 50 |
| Misc arts/other | ~12 | ~250 |

### 2. Validation fails — short focused work
**Scope: 22 files** with parity errors revealed by losing the today padder.

**Master log:** `questions/_tracker/post_strip_fails.json`

Breakdown:
- 7 × L07 Mathematics
- 8 × L10 History
- 3 × L08 Economics & Business
- 1 × L08 HP, L10 Civics, L10 Econ, L10 Science

Errors typically `MC_CHAR_LENGTH_BIAS` or `MC_SYSTEMATIC_LENGTH_BIAS` — correct answer is now too long relative to padded distractors after the strip.

### 3. New skeleton content not yet built (separate work, paused)
- Y7 Maths SP02-SP04, ST01-ST03 (6 files)
- Y9 Maths and Y9 English — skeletons present but untouched
- Y7 English — skeletons present but untouched
- Various subjects across years per `level-*-manifest.json` files

---

## Work plan — manual distractor rewrite

### Approach
For each MC item flagged in `quality_pass_log.json`:
1. Read the correct answer
2. Write 2 (Y7, 3-option) or 3 (Y8+, 4-option) substantive distractors of similar length
3. Each distractor must be:
   - Naturally similar length to correct (within 1-2 words)
   - Pedagogically meaningful (a plausible misconception or wrong-but-related claim)
   - Free of filler phrases like "in maths and everyday calculations", "across many problem types", "in any country at any stage"
4. Apply via per-file rewrite scripts in `questions/_tracker/rewrite_<CODE>.py`
5. Validate, mark in manifest, delete the rewrite script

### Priority order
1. ~~**L07 Mathematics** (25 files, ~1250 items)~~ — **COMPLETE** ✅ All 25 files distractor rewritten and validating clean
2. ~~**L08 Mathematics** (2 files, 61 items)~~ — **COMPLETE** ✅ A01 needed full correct+distractor rewrite (botched generation)
3. **L08 History** (38 files, ~1900 items) — large body of historical content
4. **L10 History** (51 files, ~2550 items) — largest single subject affected
5. **L08/L10 Civics & Citizenship** combined (~38 files, ~1900 items)
6. **L08/L10 Geography** (54 files, ~2650 items)
7. **L08/L10 HP** (35 files, ~1750 items)
8. **L08/L10 Economics & Business** (~22 files, ~1100 items)
9. **L08 Critical & Creative Thinking** (~10 files, ~500 items)
10. **Misc arts and other subjects** (~12 files, ~250 items)

### Pace estimate
- Realistic per-file workload: 30-60 min of focused turn time for ~50 MC items
- 374 files × ~45 min average = ~280 hours total
- Across many sessions, batching 2-4 files per turn

### Resume command
"Continue distractor rewrite from `<subject>` `<code>`" — read this file, find the next file in `quality_pass_log.json`, write a `rewrite_<CODE>.py` script, apply, validate, mark, repeat.

---

## Files of interest

| File | Purpose |
|---|---|
| `questions/_tracker/HANDOFF-DISTRACTOR-QUALITY.md` | This file — source of truth |
| `questions/_tracker/quality_pass_log.json` | All 14,906 items needing distractor rewrite |
| `questions/_tracker/post_strip_fails.json` | 22 files failing validation |
| `questions/_tracker/today_audit.json` | Pre-fix state of today instances |
| `questions/_tracker/strip_today.py` | One-time sweep (already applied) |
| `questions/_tracker/_build_lib.py` | Y8+ builder library |
| `questions/_tracker/_build_lib_y7.py` | Y7 builder library |

---

## User preferences captured during the today fix discussion

- **Mission critical: no time-based confusion in maths or historical content.** "Today" framing is unsafe.
- **Distractors must be substantive, not filler.** Naturally similar length to correct, plausible misconceptions.
- **Manual deliberate review** preferred over scripted rewrites. Tokens not a constraint; turns are.
- **Sequential generation only** for new content (rate limits destroy files).
- **First Nations central lens** for all curriculum content; strength-based present-tense framing where appropriate.
