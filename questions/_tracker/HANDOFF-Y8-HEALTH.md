# HANDOFF — Y8 Health (HC) Civics Files

## Goal
Finish all 20 Y8 Health (HC) files. The "Health - Community Health" folder actually contains **Y8 Civics & Citizenship** content (democracy, Constitution, legal system, identity).

## Status
**Validated (5/20):** VC2HC8K01, K02, K03, K04, K05
**Remaining (15):** K06, K07, K08, K09, K10, K11, K12, S01, S02, S03, S04, S05, S06, S07, S08

Index: 193 entries. Each new file = +1.

## Topics for remaining files
- **K06** — how citizens influence law-making (contacting reps, etc.)
- **K07** — characteristics of laws: statutory (Parliament) vs common law (courts)
- **K08** — types of law: criminal, civil, and First Nations customary law
- **K09** — Australia's secular democracy and multi-faith society; diverse cultural origins inc. First Nations
- **K10** — values: freedom, respect, fairness, equality of opportunity → cohesive diverse society
- **K11** — how groups express religious and cultural identity (strengthens / can divide)
- **K12** — different perspectives on national identity and citizenship; First Nations connections
- **S01** — develop sharp questions to investigate civic issues
- **S02** — analyse contemporary issues from multiple sources
- **S03** — explain how cultural/religious/social influences shaped Australian democracy
- **S04** — analyse how democratic values & legal principles flow through institutions
- **S05** — explain how political actors (PM, ministers, opposition) exercise power
- **S06** — participate in democratic decision-making (consensus, voting)
- **S07** — methods of civic participation at local/state/national level
- **S08** — well-supported analysis using knowledge, evidence, multiple methods

Run this to confirm topic from skeleton metadata:
```bash
cd "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"
python3 -c "import json; print(json.loads(open('questions/level-08/Health - Community Health/VC2HC8K06.skeleton.json').read())['_meta']['keyKnowledge'])"
```

## Skeleton schema (CRITICAL — get this right or builder fails)
Each skeleton has `toLevel2`/`toLevel3`/`toLevel4`/`toLevel5` as **lists** (not dicts). Each list contains 26 variants of mixed types. Counts per level:

| Level | TF | MC | Cloze | Total |
|---|---|---|---|---|
| toLevel2 | 12 | 12 | 2 | 26 |
| toLevel3 | 8 | 12 | 6 | 26 |
| toLevel4 | 2 | 12 | 12 | 26 |
| toLevel5 | 0 | 14 | 12 | 26 |

Total per file: 22 TF + 50 MC + 32 Cloze = 104 items.

### Variant shapes (fill these fields in-place on each slot):

**TF:** `{type, variant, bloomsLevel, question, correct: "True"|"False", correctExplanation, distractors:[{answer: opposite, explanation}]}` — 1 distractor.

**MC:** `{type, variant, bloomsLevel, question, correct, correctExplanation, distractors:[{answer, explanation, misconceptionSource:"inferred"}, x3]}` — 3 distractors (Y8 = 4-option).

**Cloze:** `{type, variant, bloomsLevel, sentence (with `{{blank:1}}` and `{{blank:2}}`), blanks:[{id:"1"|"2", correct, correctExplanation, distractors:[{answer, explanation, misconceptionSource:"inferred"}, x2]}, x2], scoring:"partial"}` — exactly 2 blanks per cloze, 2 distractors per blank (single-word fillers like "void", "blank", "random", "secret").

## Validator rules to satisfy
- **TF_BALANCE:** L2 ≥7/12 FALSE, L3 ≥5/8 FALSE, L4 ≥1/2 FALSE (max 65% FALSE)
- **TF_WORD_COUNT:** ≤28 words per TF statement
- **MC_OPTION_WORDS:** ≤30 words per option
- **MC_OPTION_PARITY / CHAR_PARITY / CHAR_LENGTH_BIAS / SYSTEMATIC_LENGTH_BIAS:** distractors must be near-equal length to the correct answer

## The proven recipe (works every time)
Use the working K05 builder as a copy-paste template. Each builder has:

1. **Constants:**
   ```python
   NL = "has no link to any law in any region at any stage today at every stage at all today"  # adjust topic
   NLD = "has no link to any law today at every stage at all today"
   NLD2 = "always avoids every elected role today at every stage at all today"
   NLD3 = "always relies on random outcomes today at every stage at all today"
   NLD4 = "always avoids every shared rule today at every stage at all today"
   ```

2. **Data tables** (`TF_L2`, `TF_L3`, `TF_L4`, `MC_L2`, `MC_L3`, `MC_L4`, `MC_L5`, `CL_L2`, `CL_L3`, `CL_L4`, `CL_L5`) — see counts above.

3. **TF balance pre-targets:**
   - TF_L2: aim 7 FALSE / 5 TRUE. Use the "Topic + NL" pattern for FALSE statements.
   - TF_L3: aim 5 FALSE / 3 TRUE.
   - TF_L4: aim 1 FALSE / 1 TRUE.

4. **fill_tf / fill_mc / fill_cloze** functions (identical across builders — copy from K05).

5. **Bulk extension passes** (4-pass) for MC distractor char-length parity:
   ```python
   def ext_pass(thr, suffix):
       for L in ("toLevel2","toLevel3","toLevel4","toLevel5"):
           for v in sk[L]:
               if v["type"] != "mc": continue
               for d in v["distractors"]:
                   if len(d["answer"]) < thr:
                       d["answer"] = d["answer"].rstrip(".") + " " + suffix
   ext_pass(100, "in any country at any stage")
   ext_pass(125, "across many regions")
   ext_pass(145, "over many years")
   ext_pass(175, "across many societies")
   ```

6. **Trim** correct + distractors to ≤30 words:
   ```python
   def trim(s, mx=30):
       ws = s.split()
       if len(ws) <= mx: return s
       return " ".join(ws[:mx]).rstrip(",.;:")
   ```

7. **Print pre-write counts** so you can see TF balance before validating.

## Per-file workflow (run sequentially — NEVER in parallel)
```bash
cd "/Users/jirrahmacarthur/Claude Cowork access/Kulin Nation Curriculum"

# 1. Run builder
python3 questions/_tracker/build_VC2HC8XXX.py

# 2. Validate
python3 questions/_validation/validate.py "questions/level-08/Health - Community Health/VC2HC8XXX.json" 2>&1 | grep -E "ERROR|Errors|Passed"

# 3. If TF_BALANCE errors: flip a TRUE → "Topic " + NL + "." FALSE form. Re-run + validate.
# 4. If TF_WORD_COUNT errors: shorten the TF question (or flip to NL form which is shorter).

# 5. Mark validated in manifest
python3 -c "
import json
from pathlib import Path
m = Path('questions/_tracker/level-08-manifest.json')
d = json.loads(m.read_text())
hc = d['subjects']['HC']
hc['codes']['VC2HC8XXX']['status']='validated'
hc['validated']=sum(1 for c in hc['codes'].values() if c['status']=='validated')
hc['completed']=sum(1 for c in hc['codes'].values() if c['status'] in ('validated','completed'))
d['validatedCodes']=sum(s.get('validated',0) for s in d['subjects'].values())
d['completedCodes']=sum(s.get('completed',0) for s in d['subjects'].values())
m.write_text(json.dumps(d,indent=2))
print('HC validated:', hc['validated'],'/',hc['totalCodes'],' total:',d['validatedCodes'])
"

# 6. Rebuild index
python3 build-index.py 2>&1 | tail -1

# 7. Delete builder
rm questions/_tracker/build_VC2HC8XXX.py
```

## Common fixes
- **TF_BALANCE 50% FALSE on L2/L3:** flip one TRUE → "Topic + NL + ." FALSE form
- **TF_WORD_COUNT >28:** the NL form ("Topic " + NL + ".") is usually short enough; trim "Topic" to a noun phrase. E.g. "High Court invalidating a law that does not fit the Constitution" (too long with NL appended) → "High Court invalidating a law" + NL.
- **TF_L3 6/8 FALSE (overshoot to 75%):** revert one back to TRUE.

## Content guidance — First Nations central lens
- Strength-based, present-tense framing
- Aboriginal and Torres Strait Islander Peoples engage with institutions, share voice, lead, advocate
- Country and Lore acknowledged
- Avoid deficit framing
- Each level should include at least one TF and one MC item that centres First Nations perspective

## Reference template
The most recent working builder was for K05 (legal system). Its structure is the proven template. To rebuild from scratch, copy the structure of any K05-equivalent and swap:
- Topic-specific TF/MC/Cloze content
- The `NL` topic noun ("any law" → "any government" → "any community" etc.)

## Resume command
"Continue Y8 Health from K06" — read this file, build K06, validate, mark, rebuild index, delete builder, then proceed K07 onward.

## User preferences
- Sequential generation only (parallel destroys files via rate limits)
- "209 no problem" — user OK with full Y8 scope
- Push through 3–4 files per turn, then re-prompt to keep cache warm
