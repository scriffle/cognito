# Question Generation Workflow

**Priority scope: Years 7–10 → 758 codes × 104 questions = 78,832 questions**
Full scope: 1,814 codes × 104 questions = 188,656 questions

---

## Overview

Each generation session follows a fixed cycle: **Load → Generate → Validate → Fix → Mark Complete**. The master prompt and skeleton system eliminate structural decisions. The workflow below ensures nothing is missed or duplicated across sessions.

**Strategy:** Generate Years 7–10 first. These cover the secondary school range, use two voice registers (secondary-neutral and vce-formal), and include the full breadth of subjects. Years 1–6 follow once the secondary pipeline is proven.

---

## Year Level Order

### Priority: Years 7–10

| Phase | Year levels | Age band | Voice | Codes | Est. sessions |
|-------|-------------|----------|-------|-------|---------------|
| A | 8 + 9 | 13-14 | secondary-neutral | 358 | ~72 |
| B | 10 | 15-16 | vce-formal | 338 | ~68 |
| C | 6 + 7 | 11-12 | secondary-neutral | 62 | ~13 |

**Start with Phase A** (Years 8+9 have the largest combined code count at 358, both use secondary-neutral voice, and Year 8 covers all 20 subjects — ideal for proving the pipeline).
**Phase B** (Year 10, vce-formal voice — second register, builds on Phase A experience).
**Phase C** (Years 6+7 share 11-12 age band with secondary-neutral voice. Year 7 has only 62 codes — English + Maths. Year 6 deferred but included here as they share voice/age band).

### Deferred: Years 1–6

| Phase | Year levels | Age band | Voice | Codes | Est. sessions |
|-------|-------------|----------|-------|-------|---------------|
| D | 2 + 3 | 7-8 | primary-warm | 325 | ~65 |
| E | 4 + 5 | 9-10 | primary-warm | 332 | ~67 |
| F | 6 | 11-12 | secondary-neutral | 249 | ~50 |
| G | 1 | 5-6 | oral/pictorial | 150 | ~30 |

Phases D–G begin after Years 7–10 are complete and reviewed. Year 6 is split: its 62 English+Maths codes can optionally be pulled into Phase C; the remaining ~249 codes wait for Phase F.

### Subject Order Within Each Phase

1. **Science** — strongest misconception literature, cleanest validation
2. **Mathematics** — unambiguous answers, clear Bloom's progression
3. **History** — large code count, First Nations central lens
4. **Geography**
5. **Civics & Citizenship**
6. **Health & PE**
7. **Economics & Business** (where applicable)
8. **Technologies** (Design, Digital)
9. **The Arts** (Dance, Drama, Media Arts, Music, Visual Arts, Vis Comm)
10. **Capabilities** (Critical & Creative, Intercultural, Personal & Social)
11. **English** (largest code count, language-sensitive — benefits from all prior practice)

---

## Session Protocol

### Before Each Session

1. **Check position.** Read the current level manifest to find the next pending codes:
   ```
   questions/_tracker/level-XX-manifest.json
   ```

2. **Load the master prompt:**
   ```
   questions/_tracker/generation-prompt-master.md
   ```

3. **Fill in the session context block** at the top of the master prompt:
   ```
   YEAR LEVEL:     [from manifest]
   AGE BAND:       [from manifest]
   VOICE REGISTER: [primary-warm | secondary-neutral | vce-formal]
   CODE:           [current code]
   AREA:           [from skeleton _meta]
   KEY KNOWLEDGE:  [from skeleton _source.w]
   ```

4. **Select 5 codes** from the next pending subject. Read their skeleton files.

### During Each Session

For each code in the batch:

1. **Read the skeleton:**
   ```
   questions/level-XX/Subject/CODE.skeleton.json
   ```
   This contains all structural fields + the `_source` block with `w`, `y`, `eg`.

2. **Generate.** Fill in all `null` fields following the master prompt rules. Output the completed JSON.

3. **Write** the completed file:
   ```
   questions/level-XX/Subject/CODE.json
   ```

4. **Validate immediately:**
   ```
   python questions/_validation/validate.py questions/level-XX/Subject/CODE.json
   ```

5. **Fix any errors.** Common fixes:
   - Cloze placeholders: must be `{{blank:X}}` not `___X___`
   - MC option count: must match age band (3 or 4)
   - TF word count: count again, shorten if over
   - TF balance: swap a TRUE for FALSE if needed
   - Option parity: shorten the longest option

6. **Re-validate** until PASS (0 errors). Warnings are acceptable.

### After Each Session

1. **Update the manifest.** For each completed code, change status from `"pending"` to `"completed"`:
   ```json
   "VC2S2U01": { "status": "completed", "generatedAt": "2026-04-06T..." }
   ```

2. **Record the handoff** for the next session:
   ```
   HANDOFF:
   - Phase: A (Years 8-9)
   - Current subject: Science
   - Last completed: VC2S8U05
   - Next codes: VC2S8U06, VC2S8U07, VC2S8U08, VC2S8U09, VC2S8U10
   - Codes done this subject: 5/20
   - Codes done this level: 5/306
   ```

---

## Batch Size

**5 codes per session** is the target. This balances:
- Context pressure (104 questions × 5 = 520 questions per session)
- Quality maintenance (fatigue/drift beyond 5 is measurable)
- Session duration (~1 hour per session at current generation speed)

Adjust down to 3-4 for complex subjects (English, History with heavy ATSI content).
Adjust up to 6-8 for simpler subjects (Capabilities, basic Science).

---

## Validation Pipeline

### Stage 1: Structural (automated, per code, immediate)

Run `validate.py` after every code. Must pass with 0 errors before marking complete.

```bash
python questions/_validation/validate.py questions/level-XX/Subject/CODE.json
```

Checks: JSON structure, type counts, word limits, TF balance, option parity, cloze blanks, variant numbers, Bloom's levels.

### Stage 2: Cross-code consistency (automated, per subject batch)

After completing all codes in a subject, run batch validation:

```bash
python questions/_validation/validate.py --batch questions/level-XX/Subject/
```

Then spot-check:
- Pairwise similarity across codes (are different codes producing different questions?)
- Misconception coverage (are the same 3 misconceptions used everywhere?)
- Reading level consistency

### Stage 3: Manual sampling (per year level)

After completing an entire year level, manually review 5 random codes (one per major subject area):

- Factual accuracy
- Voice and tone consistency
- Bloom's progression (does it actually get harder?)
- Distractor quality (are misconceptions real?)
- ATSI integration quality (where applicable)
- "Would I put this in front of a student?" test

---

## Anti-Drift Measures

### Layer 1: Master prompt (frozen per phase)
The master prompt does not change within a phase. If a problem is found, note it for the next phase — do not update mid-phase.

### Layer 2: Skeleton structure
Structural errors are impossible. Type counts, variant numbers, distractor array sizes are all pre-set.

### Layer 3: Immediate validation
Every code is validated before being marked complete. No code proceeds without PASS.

### Layer 4: Cross-session comparison
Every 20 codes, compare 2 random recent codes against the first code completed at this level. Check:
- Word count distribution (are stems getting longer over time?)
- Voice register (is it drifting more formal or informal?)
- Distractor explanation quality (are they getting shorter/vaguer?)

### Layer 5: Reference anchoring
The first code completed per subject per year level is the **reference**. If quality drifts, re-read the reference before continuing.

---

## Error Recovery

| Scenario | Action |
|----------|--------|
| Validation fails (structural) | Fix and re-validate. Do not mark complete until PASS. |
| Validation fails (cannot fix) | Delete the `.json` file and regenerate from skeleton. |
| Session ends mid-code | Delete partial `.json`. Skeleton is untouched. Regenerate next session. |
| Wrong voice register used | Regenerate affected codes. Check 2 codes either side for drift. |
| Spec change needed | **Do not change mid-phase.** Document the change. Apply it at the start of the next phase. Re-validate all codes from the current phase after the change. |
| Duplicate content across codes | Keep the first. Regenerate the second with explicit instruction to avoid the duplicated frame. |

---

## Progress Tracking

### Quick status check

```bash
# How many codes are done?
grep -r '"completed"' questions/_tracker/level-*-manifest.json | wc -l

# How many skeletons still need generation?
find questions -name "*.skeleton.json" | wc -l
# minus
find questions -name "*.json" ! -name "*.skeleton.json" ! -path "*/_tracker/*" ! -path "*/_validation/*" | wc -l
```

### Manifest status values

```
pending          → skeleton exists, not yet generated
completed        → generated and passed validation
validated        → passed Stage 2 cross-code check
failed_validation → failed, needs regeneration
```

---

## Estimated Timeline

At current generation speed (~12 minutes per code with validation), with skeleton pre-fill saving ~40% on output tokens (~7 min effective per code):

### Priority Phases (Years 7–10)

| Phase | Codes | Hours (raw) | Hours (w/ skeleton) | At 4hrs/day |
|-------|-------|-------------|---------------------|-------------|
| A (Yr 8+9) | 358 | ~72 | ~42 | ~11 days |
| B (Yr 10) | 338 | ~68 | ~39 | ~10 days |
| C (Yr 7) | 62 | ~12 | ~7 | ~2 days |
| **Priority total** | **758** | **~152** | **~88** | **~23 days** |

### Deferred Phases (Years 1–6)

| Phase | Codes | Hours (raw) | Hours (w/ skeleton) | At 4hrs/day |
|-------|-------|-------------|---------------------|-------------|
| D (Yr 2+3) | 325 | ~65 | ~38 | ~10 days |
| E (Yr 4+5) | 332 | ~66 | ~39 | ~10 days |
| F (Yr 6) | 249 | ~50 | ~29 | ~8 days |
| G (Yr 1) | 150 | ~30 | ~18 | ~5 days |
| **Deferred total** | **1,056** | **~211** | **~124** | **~33 days** |

| **Full total** | **1,814** | **~363** | **~212** | **~56 days** |

---

## Files Reference

| File | Purpose |
|------|---------|
| `questions/_tracker/generation-prompt-master.md` | Master prompt — loaded every session |
| `questions/_tracker/generate-skeletons.py` | Generates skeleton files from cd_explanations.json |
| `questions/_tracker/manifest.json` | Master progress tracker |
| `questions/_tracker/level-XX-manifest.json` | Per-level progress tracker |
| `questions/_tracker/area-code-mapping.json` | Area code → subject mapping |
| `questions/_validation/validate.py` | Structural validation script |
| `Question Specifications/question-schema.json` | JSON Schema for output files |
| `Question Specifications/voice-guide-primary.md` | Voice spec ages 7-10 |
| `Question Specifications/voice-guide-secondary-7-9.md` | Voice spec ages 11-14 |
| `Question Specifications/VCAA_VCE_Unified_Exam_Voice.md` | Voice spec ages 15-16 |
| `Question Specifications/atsi-integration-guide.md` | ATSI integration rules |
| `Question Specifications/rubrics/emab-descriptors.md` | EMAB rating system |
| `cd_explanations.json` | Source: learning points, reasons, examples |
