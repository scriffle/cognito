# HANDOFF — Universal Question Generation

## What this is

A parallel work queue for building VC2 question files for **Years 7–10 (Levels 07–10)**. Multiple Claude Code sessions work simultaneously. Each session claims codes from the queue, builds complete JSON from skeletons, validates, and checks in.

**Levels 1–6 are out of scope.** Do not attempt any code below Level 07. The Victorian Curriculum only mandates Years 7–8 and 9–10 content at this stage.

**No Python builder scripts.** Every file is hand-authored JSON. Every item is bespoke.

**Scope:** 758 codes across L07–L10. ~124 done. ~634 pending.

---

## Session workflow

### 1. Check out codes

```bash
cd "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"
python3 << 'PYEOF'
import json, os
q = json.load(open('questions/_tracker/generation-queue.json'))
codes = q['codes']
# Check filesystem for what's actually built
for code, info in codes.items():
    lv = str(info['level']).zfill(2)
    folder = info['folder']
    fpath = f"questions/level-{lv}/{folder}/{code}.json"
    if os.path.exists(fpath):
        info['status'] = 'done'

pending = [(c, i) for c, i in codes.items() if i['status'] == 'pending']
claimed = [(c, i) for c, i in codes.items() if i['status'] == 'claimed']
done = [(c, i) for c, i in codes.items() if i['status'] == 'done']
print(f"Done: {len(done)} | Claimed: {len(claimed)} | Pending: {len(pending)}")
print(f"\nNext 4 available:")
for c, i in pending[:4]:
    print(f"  {c} — L{str(i['level']).zfill(2)} {i['area']} ({i['ageBand']}) — {i['keyKnowledge'][:80]}")
PYEOF
```

Claim codes by editing `questions/_tracker/generation-queue.json`:
```json
"VC2XXXXX": { "status": "claimed", "claimedBy": "session-XXX", "claimedAt": "2026-05-16T...", ... }
```

**Claim 4 codes at a time.** Prefer codes from the same level and subject for consistency.

### 2. Build each file

For each claimed code:

1. **Read the skeleton** to get `_meta` (code, level, ageBand, keyKnowledge) and `_source` (w, y, eg):
   ```bash
   python3 -c "import json; s=json.load(open('questions/level-XX/SubjectFolder/VC2XXXXX.skeleton.json')); print(json.dumps({k:s[k] for k in ['_meta','_source']}, indent=2))"
   ```

2. **Check the age band** in the parameter table below and apply the correct rules.

3. **Author the complete JSON** — write directly to `questions/level-XX/SubjectFolder/VC2XXXXX.json`. Drop `_source` from output. Set `_meta.generatedAt` to current timestamp.

4. **Validate:**
   ```bash
   python3 questions/_validation/validate.py "questions/level-XX/SubjectFolder/VC2XXXXX.json"
   ```
   Must show `Passed: 1/1` with 0 errors.

5. **Fix any errors** and re-validate.

### 3. Check in

```bash
python3 questions/_tracker/update_manifests.py
```

Update `generation-queue.json` — set each completed code to `"status": "done"`.

---

## File structure — 104 items per file (ALL levels)

Every file has identical structure regardless of level or subject:

| Level | Bloom's | TF | MC | Cloze | Total |
|-------|---------|----|----|-------|-------|
| toLevel2 | 2 (Remember) | 12 (v1-12) | 12 (v13-24) | 2 (v25-26) | 26 |
| toLevel3 | 3 (Understand) | 8 (v1-8) | 12 (v9-20) | 6 (v21-26) | 26 |
| toLevel4 | 4 (Apply) | 2 (v1-2) | 12 (v3-14) | 12 (v15-26) | 26 |
| toLevel5 | 5 (Analyse) | 0 | 14 (v1-14) | 12 (v15-26) | 26 |

---

## Parameter table — HARD LIMITS by age band

Only Levels 07–10 are in scope. **Do not build anything below Level 07.**

| Parameter | 11-12 (L07) | 13-14 (L08-09) | 15-16 (L10) |
|-----------|-------------|-----------------|-------------|
| **Voice register** | secondary-neutral | secondary-neutral | vce-formal |
| **TF max words** | 22 | 28 | 35 |
| **MC stem max words** | 55 | 80 | 130 |
| **MC option max words** | 20 | 30 | 40 |
| **MC total options** | 3 | 4 | 4 |
| **MC distractors** | 2 | 3 | 3 |
| **Cloze distractors/blank** | 2 | 2 | 2 |
| **Negation in stems** | Sparingly | Sparingly | Permitted |
| **FK grade max** | 7.0 | 9.0 | 11.0 |

**MC parity rules (all levels):**
- All options within ±20% word count of mean
- No option >30% longer/shorter by character count
- Correct answer is longest in ≤30% of MC items per file
- ≤10% of MC items where correct exceeds longest distractor by >8 chars AND ≥30% above avg distractor
- **Write distractors FIRST, then correct.** This prevents length bias.
- At least 1 distractor per item must have char count ≥ correct answer

**TF balance (all levels):** 55–65% FALSE per Bloom's level (for L4 with only 2 TF: ≥1 FALSE)

---

## Voice registers

### Secondary Neutral (Ages 11-14, L07-L09)
- Neutral, precise, respectful. Treats students as developing independent thinkers.
- L07 (ages 11-12): "Which of the following..." accepted. **3 options.** Tier 2 academic vocabulary OK (analyse, identify, compare). ≤20 words per MC option.
- L08-L09 (ages 13-14): "Which one of the following..." (VCAA convention). **4 options.** ≤30 words per MC option. All 3 distractors must be genuinely functional.
- No contractions, no colloquial language ("heaps of", "got", "stuff"), no hedging.
- No "you"/"your". No anthropomorphic language. Active voice default.

### VCE Formal (Ages 15-16, L10)
- Calm, precise authority. Impersonal, objective, economical.
- "Which one of the following..." **4 options.** ≤40 words per MC option.
- Full disciplinary register. Third person throughout. Never "you".
- At least 1 distractor must be a sophisticated misconception requiring deep knowledge.
- IUPAC nomenclature for science. Correct notation throughout.

---

## Item format examples

### True/False (all levels)
```json
{
  "type": "tf",
  "variant": 1,
  "bloomsLevel": 2,
  "question": "Statement here — single proposition only.",
  "correct": "True",
  "correctExplanation": "Why this is true. 1-2 sentences.",
  "distractors": [
    {
      "answer": "False",
      "explanation": "Names the misconception a student choosing False likely holds."
    }
  ]
}
```

### Multiple Choice — 3 options (L07, ages 11-12)
```json
{
  "type": "mc",
  "variant": 13,
  "bloomsLevel": 2,
  "question": "Which of the following best describes a ratio?",
  "correct": "A comparison of two quantities using division to show their relative size",
  "correctExplanation": "A ratio compares two quantities by division, expressing how many times one contains the other.",
  "distractors": [
    {
      "answer": "A comparison of two quantities using subtraction to show the difference between them",
      "explanation": "Confuses ratio (multiplicative comparison) with difference (additive comparison)."
    },
    {
      "answer": "A single quantity expressed as a fraction of one hundred to show its percentage value",
      "explanation": "Describes a percentage, not a ratio; a ratio compares two quantities, not one quantity to 100."
    }
  ]
}
```

### Multiple Choice — 4 options (L08-L10, ages 13-16)
```json
{
  "type": "mc",
  "variant": 13,
  "bloomsLevel": 2,
  "question": "Which of the following correctly states the product rule for exponents with the same base?",
  "correct": "When multiplying such powers, add the exponents to produce the new exponent of the shared base",
  "correctExplanation": "The product rule states a^m × a^n = a^(m+n).",
  "distractors": [
    {
      "answer": "When multiplying such powers, multiply the exponents to produce the new exponent of the shared base",
      "explanation": "Confuses the product rule (add) with the power rule (multiply)."
    },
    {
      "answer": "When multiplying such powers, subtract the exponents to produce the new exponent of the shared base",
      "explanation": "Confuses the product rule (add) with the quotient rule (subtract)."
    },
    {
      "answer": "When multiplying such powers, divide the exponents to produce the new exponent of the shared base",
      "explanation": "Division is not a standard exponent law operation for same-base multiplication."
    }
  ]
}
```

### Cloze (all levels)
```json
{
  "type": "cloze",
  "variant": 25,
  "bloomsLevel": 2,
  "sentence": "When multiplying powers with the same base, {{blank:1}} the exponents; when dividing powers with the same base, {{blank:2}} the exponents.",
  "blanks": [
    {
      "id": "1",
      "correct": "add",
      "correctExplanation": "The product rule states a^m × a^n = a^(m+n).",
      "distractors": [
        {
          "answer": "multiply",
          "explanation": "Confuses the product rule (add) with the power rule (multiply).",
          "misconceptionSource": "inferred"
        },
        {
          "answer": "subtract",
          "explanation": "Confuses the product rule (add) with the quotient rule (subtract).",
          "misconceptionSource": "inferred"
        }
      ]
    },
    {
      "id": "2",
      "correct": "subtract",
      "correctExplanation": "The quotient rule states a^m ÷ a^n = a^(m−n).",
      "distractors": [
        {
          "answer": "divide",
          "explanation": "Confuses the operation on exponents (subtract) with the expression operation (divide).",
          "misconceptionSource": "inferred"
        },
        {
          "answer": "add",
          "explanation": "Confuses the quotient rule (subtract) with the product rule (add).",
          "misconceptionSource": "inferred"
        }
      ]
    }
  ],
  "scoring": "partial"
}
```

**Cloze rules:**
- 2–4 blanks. Format: `{{blank:N}}` exactly.
- Blank content words only — never articles, prepositions, conjunctions.
- 2 distractors per blank with `explanation` + `misconceptionSource` (`"inferred"` is fine).
- All options same part of speech, same semantic category, similar length.
- `scoring`: `"partial"` (default) or `"all"`.

---

## Bloom's level guidance

**Level 2 (Remember):** Definitions, labels, terms, basic facts. Pure recall. No scenarios.

**Level 3 (Understand):** Classification, explanation, examples, paraphrasing. Brief context OK.

**Level 4 (Apply):** Using knowledge in novel concrete scenarios. Named characters (Mia, Jarrah, Anika, Sam, Lila, Kofi, Yen, Rosa, Amir, Jade, Linh, Marcus, Priya, Will). Not repeating taught examples.

**Level 5 (Analyse/Evaluate):** Comparing, evaluating claims, reasoning from evidence. "A student claims..." "Which approach is most efficient?" Ages 7-10: keep concrete. Ages 13+: may include data.

---

## Subject-specific rules

### Mathematics
- Present tense for definitions, properties, rules.
- Write mathematical expressions in readable text: "x squared", "x cubed", "x to the fourth", "the binomial (2x plus 3y)".
- No time-based framing ("today we use..."). Maths is timeless.

### Science
- Present tense for laws, processes, ongoing phenomena ("Water boils at 100°C at sea level").
- IUPAC nomenclature at L10. State symbols where appropriate.

### History / Geography (historical) / Civics (constitutional history) / Economics (economic history)
- **Past tense** for period events, actions, decisions, policies.
- **Past tense** for views and practices of historical peoples in their period.
- **Present tense** ONLY for: living cultural practices, historian's work, genuinely enduring institutions.
- **BANNED:** "X today..." where X is a finished historical subject.

### Health & Physical Education
- Present tense for body systems, skills, current public-health knowledge.
- Strength-based framing.

### ATSI content
- If `_source` references Aboriginal or Torres Strait Islander knowledge:
  - Include in 2-3 variants spread across Bloom's levels.
  - Use specific nation names ("Kulin Nation", "Yolngu people") — never "Aboriginal people believe..."
  - **Present tense** for living cultural practices.
  - Strength-based framing.
  - Safe to assess: ecological knowledge, seasons, fire management, trade, astronomical navigation, governance, language diversity.
  - **Never assess:** sacred/ceremonial knowledge, Dreaming narratives (unless curriculum explicitly references), initiation practices.
- If `_source` does NOT reference ATSI content, do not force inclusion.

---

## Anti-filler rules — CRITICAL

These phrases **killed the previous generation pass** and destroyed thousands of items:

**BANNED:**
- "in maths and everyday calculations"
- "across many problem types"
- "on the page in any case at all"
- "in any country at any stage"
- "across many regions/societies/years"
- "in maths and in maths" (yes, this happened)
- Any generic padding that adds words without adding subject content

Every word in every option must serve the subject matter. If a distractor is too short, make it substantively longer by adding **domain-specific detail** — not by appending filler.

---

## Variant diversity

All 26 variants at a Bloom's level test the **same learning point** but differ in:
- **Frame:** Different real-world contexts
- **Vocabulary:** Different surface words
- **Scenario:** Different characters (L4-L5)
- **Angle:** Different aspects of the concept

Use the skeleton's `_source.eg` (6 examples) and `_source.y` (3 reasons) as diversity seeds.

No two variants may share >40% content words (excluding function words).

---

## Validation

```bash
cd "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"
python3 questions/_validation/validate.py "questions/level-XX/SubjectFolder/VC2XXXXX.json"
```

**Must show `Passed: 1/1` with 0 errors.** Common errors and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `MC_OPTION_PARITY` | An option is >20% longer/shorter than mean | Adjust word count |
| `MC_SYSTEMATIC_LENGTH_BIAS` | Correct is longest in >30% of MC items | Shorten correct answers or lengthen distractors |
| `MC_CHAR_LENGTH_BIAS` | Correct exceeds longest distractor by >8 chars in >10% | Lengthen a distractor |
| `TF_BALANCE` | FALSE% outside 55-65% | Flip one TF item |

---

## Full master prompt

For extended rules, edge cases, and the anti-drift checklist, read:
```
questions/_tracker/generation-prompt-master.md
```
That document is the ultimate authority. This handoff summarises it for speed.

---

## Files of interest

| File | Purpose |
|------|---------|
| `questions/_tracker/HANDOFF-GENERATION.md` | This file — session instructions |
| `questions/_tracker/generation-queue.json` | Universal queue — claim and complete here |
| `questions/_tracker/generation-prompt-master.md` | Full master prompt (extended rules) |
| `questions/_tracker/update_manifests.py` | Run after completing files |
| `questions/_validation/validate.py` | Validator — must pass before checkin |
| `questions/level-XX/SubjectFolder/*.skeleton.json` | Skeleton files (input) |

---

## Scope restriction

**Only Levels 07–10 are in scope.** The queue contains only L07–L10 codes. If a session encounters any code below Level 07, skip it — those levels are not part of the current VC mandate.

| Level | Ages | Voice | MC Options |
|-------|------|-------|-----------|
| L07 | 11-12 | secondary-neutral | 3 (2 distractors) |
| L08 | 13-14 | secondary-neutral | 4 (3 distractors) |
| L09 | 13-14 | secondary-neutral | 4 (3 distractors) |
| L10 | 15-16 | vce-formal | 4 (3 distractors) |

---

## Resume command

Open a new Claude Code session and say:

> Read `questions/_tracker/HANDOFF-GENERATION.md` and `questions/_tracker/generation-prompt-master.md`. Claim the next 4 available codes from `questions/_tracker/generation-queue.json` and build them. Only Levels 07–10 are in scope. No Python scripts — write each JSON file directly. Validate each one before checking in.

To target a specific level or subject:

> Read `questions/_tracker/HANDOFF-GENERATION.md` and `questions/_tracker/generation-prompt-master.md`. Claim 4 codes from Level 10 Mathematics in `questions/_tracker/generation-queue.json` and build them. No Python scripts — write each JSON file directly. Validate each one before checking in.
