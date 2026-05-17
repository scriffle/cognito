# VC2M8SP04 — Mathematics (Short)

## Snapshot
- **Descriptor:** Design and test algorithms involving a sequence of steps and decisions that identify congruency or similarity of shapes, and describe how the algorithm works.
- **Year / Area:** Years 7–8, Mathematics.
- **Big ideas:** An algorithm is a step-by-step procedure with decisions. You can systematically classify shapes as congruent, similar or neither. Testing with multiple inputs reveals whether the algorithm is reliable.

## What you are learning
- You are learning to **design and test algorithms** that identify congruency or similarity of shapes through a sequence of steps and decisions.
- You should be able to create, test and describe your algorithm clearly.

## Core content

An **algorithm** is a finite sequence of steps with decisions (yes/no branches) that produces an output from an input. Key features: sequence, decision, defined input/output.

**Triangle congruence algorithm.** Input: measurements of two triangles. Steps: (1) Sort sides shortest to longest. (2) Check SSS (all sides equal?). (3) Check SAS. (4) Check ASA. (5) Check AAS. (6) Check RHS. (7) If no match → not congruent.

**Similarity extension.** After ruling out congruence: (A) Check AAA. (B) Check all side ratios equal (SSS-ratio). (C) Check SAS-ratio. (D) If none → neither.

**Testing.** Try known cases: (3,4,5) & (3,4,5) → SSS ✓. (3,4,5) & (6,8,10) → ratio 2, similar ✓. (3,4,5) & (3,4,6) → neither ✓. Edge cases (equilateral, degenerate, impossible triangles) expose bugs.

**Worked example: quadrilateral similarity.** Step 1: check all four angle pairs equal. Step 2: check all four side ratios equal. Both must hold (unlike triangles, equal angles alone do not guarantee quadrilateral similarity).

**Describing the algorithm.** Explain: what inputs, what each decision checks, why that order, what the output means. Clear enough for someone else to follow without help.

**Victorian and cultural context.** Quality-control in Victorian manufacturing uses algorithmic checking against geometric tolerances. Traditional First Nations manufacturing (shaping boomerangs, grinding axes) involves iterative check-and-adjust — algorithmic thinking in physical materials. Weavers across cultures follow step-by-step decision procedures to produce congruent repeated motifs.

## Memorable takeaways
- Algorithm = steps + decisions → classification.
- Congruence: check SSS, SAS, ASA, AAS, RHS.
- Similarity: check AAA, SSS-ratio, SAS-ratio.
- Always test with known cases and edge cases.

## Watch out for these traps
- "Forgot to sort sides." Comparing mismatched sides gives false results.
- "Stopped after one check." Exhaust all conditions before concluding "neither."
- "Works for my examples = correct." Edge cases expose bugs — always test broadly.

## Model responses

Use these to check your thinking after you have had a go.

- *Three features of an algorithm?* Sequence, decision, defined input/output.
- *Why sort sides first?* To ensure you compare corresponding sides (shortest to shortest, etc.).
- *Can shapes be congruent AND similar?* Yes — congruence is similarity with scale factor 1.
- *(3,4,5) & (6,8,10)?* Not congruent; ratios all 2 → similar (SSS-ratio).
- *(1,2,5) tested by algorithm?* 1+2 = 3 < 5 → triangle inequality fails → "impossible triangle."
