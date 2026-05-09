# HOURLY GENERATION HANDOFF — VC2 Question Files

**Purpose:** This file is the single source of truth for an hourly cron / scheduled session that continues VC2 question-file generation without drift. It is read at the **start of every run** and the routine's own instructions are refreshed from it.

**Working directory (absolute, do not change):**
`/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum`

---

## 0. Hard rules (NEVER violate)

1. **Sequential only.** NEVER run question-generation agents in parallel. Rate limits destroy files. One builder at a time, one validate at a time.
2. **One file per cycle.** Build → bulk-extend → validate → mark → rebuild index → delete builder. Do not move on until the current file shows `Passed: 1/1`.
3. **First Nations central lens, strength-based, present-tense.** Aboriginal and Torres Strait Islander Peoples have living cultures, knowledge systems, and Country today. Never frame as past-tense / lost / pre-history.
4. **Engage Traditional Owners in scenarios; follow protocols on Country; do not include sacred / restricted detail.** Use accurate Country / Nation names where named.
5. **Never edit `_meta.code`, never edit skeleton variant numbers**, never reorder slots.
6. **Do NOT commit, do NOT push, do NOT touch git** unless the user explicitly asks. The cron only writes JSON and updates the manifest/index.

---

## 1. Where to resume

The next file to build is the lowest-numbered `pending` entry in the level manifest, in this priority order:

1. `questions/_tracker/level-08-manifest.json` — Y8 (in progress: History HH then Civics HC)
2. `questions/_tracker/level-10-manifest.json` — Y10 humanities pending
3. `questions/_tracker/level-06-manifest.json` — Y6 humanities pending

Find it with:

```bash
python3 - <<'PY'
import json
for lvl in ('08','10','06'):
    d = json.load(open(f'questions/_tracker/level-{lvl}-manifest.json'))
    def walk(n, path=''):
        if isinstance(n, dict):
            for k,v in n.items():
                if isinstance(v,dict) and v.get('status')=='pending' and k.startswith('VC2'):
                    print(lvl, k); return True
                if walk(v, path+'/'+k): return True
        elif isinstance(n, list):
            for x in n:
                if walk(x, path): return True
        return False
    if walk(d): break
PY
```

Stop conditions: if every manifest is fully validated, exit cleanly with `ALL DONE` and skip the rest of the routine.

---

## 2. The build-validate-mark cycle (run exactly this, in order)

For one file `VC2{AREA}{LEVEL}{CODE}` (e.g. `VC2HH8K05`):

### 2.1 Read the skeleton's `keyKnowledge`

```bash
python3 -c "import json,sys; d=json.load(open('questions/level-{LL}/{Area}/{CODE}.skeleton.json')); print(d['_meta']['keyKnowledge'])"
```

This drives the topical content.

### 2.2 Write the builder

Path: `questions/_tracker/build_{CODE}.py`

The builder must:

- Define module-level lists `TF_L2` (12 items), `TF_L3` (8), `TF_L4` (2), `MC_L2` (12), `MC_L3` (12), `MC_L4` (12), `MC_L5` (14), `CLOZE_L2` (2), `CLOZE_L3` (6), `CLOZE_L4` (12), `CLOZE_L5` (12). Total 104.
- TF tuple shape: `(question, "True"|"False", correctExplanation, otherSideExplanation)`.
- MC tuple shape: `(question, correct, correctExplanation, [(distractor_answer, explanation, "inferred"), ...])`. Y8 has **3** distractors; Y6/Y10 follow their level's option count (check an existing validated file for the same level).
- Cloze tuple shape: `(sentence_with_{{blank:N}}_markers, [(correct, [d1, d2]), ...])`. Max **4** blanks per sentence — extras are dropped silently by `fill_cloze`.
- Use `fill_tf` / `fill_mc` / `fill_cloze` helpers (template below) and slice the skeleton: `skel['toLevel2'][:12]` for TF, `[12:24]` for MC, `[24:26]` for Cloze, etc. (toLevel5 is `[:14]` MC + `[14:26]` Cloze, no TF.)
- After dumping JSON, run an in-script **bulk-extension pass** on distractors (see §3).
- Print `TF L2 F: x/12`, `TF L3 F: x/8`, `TF L4 F: x/2` before writing — gives the routine an early signal of TF balance.

**Required TF balance:** L2 ≥ 7/12 FALSE, L3 ≥ 5/8 FALSE, L4 ≥ 1/2 FALSE. If counts are short after the first build, flip TRUE statements to the **"no link" misconception form** (see §4).

### 2.3 Run the builder

```bash
python3 questions/_tracker/build_{CODE}.py
```

### 2.4 Validate

```bash
python3 questions/_validation/validate.py "questions/level-{LL}/{Area}/{CODE}.json"
```

Look for `Passed: 1/1`. If not, follow §4 fixes; rerun the builder; revalidate. **Do not edit the JSON by hand** — always change the builder so re-runs are reproducible.

### 2.5 Mark validated + rebuild index + delete builder

```bash
python3 - <<PY
import json
p='questions/_tracker/level-{LL}-manifest.json'
d=json.load(open(p))
def mark(n):
    if isinstance(n,dict):
        for k,v in n.items():
            if k=='{CODE}' and isinstance(v,dict): v['status']='validated'
            else: mark(v)
    elif isinstance(n,list):
        [mark(x) for x in n]
mark(d); json.dump(d,open(p,'w'),indent=2)
PY
python3 build-index.py
rm questions/_tracker/build_{CODE}.py
```

The index count should increase by exactly 1.

---

## 3. Bulk-extension recipe (REQUIRED — fixes char-parity errors)

Distractors are written short with the canonical tail `today at every stage at all today`. After the JSON is dumped, the builder's `main()` runs a two-pass extension:

```python
def ext(s):
    if 'today at every stage' in s and 'in any country at any stage' not in s and len(s) < 100:
        s = s.replace('today at every stage','in any country at any stage today at every stage')
    if 'today at every stage' in s and 'across many regions' not in s and len(s) < 125:
        s = s.replace('today at every stage','across many regions today at every stage')
    if 'today at every stage' in s and 'over many years' not in s and len(s) < 145:
        s = s.replace('today at every stage','over many years today at every stage')
    if 'today at every stage' in s and 'across many societies' not in s and len(s) < 175:
        s = s.replace('today at every stage','across many societies today at every stage')
    return s
```

Walk the JSON's flat item lists (`toLevel2`..`toLevel5`); for each item apply `ext` to every `distractors[].answer` and every `blanks[].distractors[].answer`. Re-write the file.

This typically takes a fresh build from ~78% MC_CHAR_LENGTH_BIAS errors to 0 in one pass.

---

## 4. Fix recipes for common validator failures

| Error | Fix |
|---|---|
| `TF_BALANCE` (FALSE < 55%) | Flip a TRUE statement to the no-link misconception form: `"X has no link to any Y in any country at any stage today at every stage at all today."` with `"False"` correct and a one-sentence rebuttal explanation. |
| `MC_OPTION_PARITY` (>20% over mean words) — option 1 is correct and too long | Shorten the correct answer (drop one filler clause), or apply more bulk extension to distractors. |
| `MC_OPTION_CHAR_PARITY` (>30% over mean chars) | Same as above — usually solved by the §3 second-pass extension. |
| `MC_CHAR_LENGTH_BIAS` (correct >8c over longest distractor AND ≥30% over avg) | Run the §3 two-pass extension. If still failing on a single item, shorten the correct option. |
| `MC_SYSTEMATIC_LENGTH_BIAS` (correct longest in >30% items) | §3 fixes this collaterally; if still failing, several correct options need trimming. |
| `MC_CONTRACTION` | Replace any contraction in the **stem** with the expanded form. |
| `TF_WORD_COUNT` (>28 words at Y8) | Trim the TF stem. |
| `CLOZE_BLANK_COUNT` (>4 blanks) | Limit `fill_cloze` to the first 4 blanks (already in the template). |
| `MC_OPTION_PARITY` on overlong "no link" distractor | Trim `today at every stage at all today` → `today at all` (saves ~4 words). |
| `MC_OPTION_WORDS` (correct >30 words) | Add a `trim_words(s, mx=30)` step to the builder that drops trailing filler clauses (`' across many years and many regions on the land together'`, `' on the land'`, `' over many years'`, `' together'`) until ≤ 30 words. Apply to every `it['correct']` after bulk-extension. |
| `MC_OPTION_WORDS` (distractor >30 words after 4-pass extension) | Add a `trim_dist(s, mx=30)` step that swaps the longest extension chunk (`' across many societies today...'`) for a shorter one until ≤ 30 words. Apply to every distractor `answer` after the bulk-extension passes. |

---

## 5. Builder template (copy this skeleton, then fill content)

```python
#!/usr/bin/env python3
"""Build {CODE} — {one-line topic}."""
import json, datetime
from pathlib import Path

ROOT = Path("/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum")
SK = ROOT / "questions/level-{LL}/{Area}/{CODE}.skeleton.json"
OUT = ROOT / "questions/level-{LL}/{Area}/{CODE}.json"

TF_L2 = [ ... 12 tuples ... ]
TF_L3 = [ ...  8 tuples ... ]
TF_L4 = [ ...  2 tuples ... ]
MC_L2 = [ ... 12 tuples ... ]
MC_L3 = [ ... 12 tuples ... ]
MC_L4 = [ ... 12 tuples ... ]
MC_L5 = [ ... 14 tuples ... ]
CLOZE_L2 = [ ...  2 tuples ... ]
CLOZE_L3 = [ ...  6 tuples ... ]
CLOZE_L4 = [ ... 12 tuples ... ]
CLOZE_L5 = [ ... 12 tuples ... ]

def fill_tf(items, slots):
    for it, slot in zip(items, slots):
        q,c,ce,de = it
        slot.update(question=q, correct=c, correctExplanation=ce)
        other = "False" if c=="True" else "True"
        slot['distractors'] = [{"answer": other, "explanation": de}]

def fill_mc(items, slots):
    for it, slot in zip(items, slots):
        q,c,ce,dlist = it
        slot.update(question=q, correct=c, correctExplanation=ce)
        slot['distractors'] = [{"answer":a,"explanation":e,"misconceptionSource":m} for (a,e,m) in dlist]

def fill_cloze(items, slots):
    for it, slot in zip(items, slots):
        sent, blanks = it
        slot['sentence'] = sent
        slot['blanks'] = []
        for i,(corr,dlist) in enumerate(blanks[:4], 1):
            slot['blanks'].append({
                "id": str(i), "correct": corr,
                "correctExplanation": "This option fits the sentence and matches the topic idea being tested.",
                "distractors": [{"answer":d,"explanation":f"{d.capitalize()} is unrelated to {corr}.","misconceptionSource":"inferred"} for d in dlist]
            })
        slot['scoring'] = "partial"

def main():
    skel = json.load(open(SK))
    skel['_meta']['generatedAt'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("TF L2 F:", sum(1 for x in TF_L2 if x[1]=="False"), "/12")
    print("TF L3 F:", sum(1 for x in TF_L3 if x[1]=="False"), "/8")
    print("TF L4 F:", sum(1 for x in TF_L4 if x[1]=="False"), "/2")
    fill_tf(TF_L2, skel['toLevel2'][:12]);  fill_mc(MC_L2, skel['toLevel2'][12:24]); fill_cloze(CLOZE_L2, skel['toLevel2'][24:26])
    fill_tf(TF_L3, skel['toLevel3'][:8]);   fill_mc(MC_L3, skel['toLevel3'][8:20]);  fill_cloze(CLOZE_L3, skel['toLevel3'][20:26])
    fill_tf(TF_L4, skel['toLevel4'][:2]);   fill_mc(MC_L4, skel['toLevel4'][2:14]);  fill_cloze(CLOZE_L4, skel['toLevel4'][14:26])
    fill_mc(MC_L5, skel['toLevel5'][:14]);  fill_cloze(CLOZE_L5, skel['toLevel5'][14:26])
    json.dump(skel, open(OUT,'w'), indent=2)

    # bulk-extend short distractors (two passes)
    d = json.load(open(OUT))
    def ext(s):
        if 'today at every stage' in s and 'in any country at any stage' not in s and len(s)<100:
            s = s.replace('today at every stage','in any country at any stage today at every stage')
        if 'today at every stage' in s and 'across many regions' not in s and len(s)<125:
            s = s.replace('today at every stage','across many regions today at every stage')
        if 'today at every stage' in s and 'over many years' not in s and len(s)<145:
            s = s.replace('today at every stage','over many years today at every stage')
        return s
    def walk(items):
        for it in items:
            for dd in it.get('distractors', []) or []:
                if isinstance(dd, dict) and 'answer' in dd:
                    dd['answer'] = ext(dd['answer'])
            for b in it.get('blanks', []) or []:
                for dd in b.get('distractors', []):
                    if isinstance(dd, dict) and 'answer' in dd:
                        dd['answer'] = ext(dd['answer'])
    for k in ('toLevel2','toLevel3','toLevel4','toLevel5'):
        walk(d.get(k, []))
    json.dump(d, open(OUT,'w'), indent=2)
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
```

---

## 6. Drift-prevention: refresh instructions every cycle

At the **start of every run**, the routine MUST:

1. Re-read this file (`questions/_tracker/HOURLY-HANDOFF.md`) end-to-end before producing any tool calls.
2. Re-read `questions/_tracker/SEQUENTIAL-GENERATION.md` and `questions/_tracker/HUMANITIES-HANDOFF.md` if they exist — they may contain newer constraints.
3. Re-read the **most recently validated JSON** for the target level/area (highest-numbered validated file in the same Area folder) to lock in shape, length, distractor tone, and ATSI framing voice. Drift creeps in when the model invents new patterns instead of mirroring proven ones.
4. Sample-check `_meta.specVersions` on the skeleton matches the validated file's `_meta.specVersions`. If they differ, STOP and surface the mismatch.
5. Confirm the level's MC option count by looking at any validated MC item: Y6 = 3 options (correct + 2), Y8 = 4 (correct + 3), Y10 = 5 (correct + 4). Wrong option count = silent failure.
6. Print a one-line acknowledgement of these confirmations before running the builder so the log is auditable.

If at any point the routine cannot satisfy steps 1–5, it must abort the cycle and write a one-line note to `questions/_tracker/HOURLY-LOG.md` rather than push through with a guess.

---

## 7. Per-run log

Append one line per cycle to `questions/_tracker/HOURLY-LOG.md`:

```
{ISO timestamp}  {CODE}  {result}  {index_count}  {notes}
```

`result` is one of `validated`, `failed:<reason>`, `skipped:<reason>`, `all-done`. The log is the only persistent record between runs and is the first thing a human checks if a cycle silently breaks.

---

## 8. Time / token budget

- One full file ≈ 25–35k output tokens for the builder + ~5k for fixes. Fits one Claude conversation comfortably.
- If the routine has time left after one validated file, **stop anyway** — finishing one clean file per hour beats half-finishing two. The next cron tick will pick the next pending file.
- Hard cap: never spend more than 30 minutes on a single file. If two fix iterations have not produced `Passed: 1/1`, write `failed:<lastError>` to the log and exit so a human can review.

---

## 9. What "done" looks like for one cycle

- `questions/level-{LL}/{Area}/{CODE}.json` exists and validates.
- `questions/_tracker/level-{LL}-manifest.json` shows `{CODE}` as `validated`.
- `files-index.json` count incremented by exactly 1.
- `questions/_tracker/build_{CODE}.py` is **deleted**.
- One new line in `HOURLY-LOG.md`.

If any of those five is missing, the cycle is incomplete — do not advance to the next file.

---

## 10. Escalate to human (do not auto-fix)

- Manifest entries with no skeleton present.
- Skeleton with a different `_meta.specVersions` than already-validated peers.
- Any content involving sacred / restricted material, or a Country / Nation name the routine is not confident is correct.
- Validator emits an error code not listed in §4.

In all four cases: write the situation to `HOURLY-LOG.md` with prefix `ESCALATE:` and exit cleanly.
