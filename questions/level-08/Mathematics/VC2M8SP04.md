# VC2M8SP04 — Mathematics

## Snapshot
- **Descriptor:** VC2M8SP04. Design and test algorithms involving a sequence of steps and decisions that identify congruency or similarity of shapes, and describe how the algorithm works.
- **Year level / Learning area:** Years 7–8, Mathematics (Space).
- **Big ideas:**
  - An algorithm is a step-by-step procedure with clear decisions at each stage.
  - You can design a decision-making algorithm to systematically determine whether two shapes are congruent, similar or neither.
  - Testing an algorithm with different inputs reveals whether it works reliably.
- **Curriculum hooks:** Numeracy; Critical and Creative Thinking; Digital Literacy; Aboriginal and Torres Strait Islander Histories and Cultures.

## What you are learning
- You are learning to **design and test algorithms** that use a sequence of steps and decisions to identify congruency or similarity of shapes.
- You are learning to think procedurally — breaking a complex judgement into smaller, testable decisions.

By the end of this you should be able to:
- Define what an algorithm is and identify its key features (sequence, decision, input, output).
- Design a flowchart-style algorithm that classifies pairs of triangles as congruent, similar or neither.
- Test your algorithm with multiple examples (including edge cases).
- Describe how and why your algorithm works.

## Core content

**1. What is an algorithm?** An **algorithm** is a finite sequence of well-defined steps that produces an output from a given input. It includes **decisions** (yes/no branches) that direct the flow. A recipe, a diagnostic checklist and a computer program are all algorithms. *Quick check:* What are the three key features of an algorithm?

**2. Inputs and outputs for a congruence/similarity algorithm.** Input: measurements of two shapes (side lengths, angles, or both). Output: a classification — "congruent," "similar" or "neither." The algorithm must decide which measurements to compare and in what order. *Quick check:* What measurements would you need as input to classify two triangles?

**3. Designing a triangle congruence algorithm.**

Step 1: Measure all sides and angles of both triangles.
Step 2: Sort each triangle's sides from shortest to longest.
Step 3: Are all three corresponding sides equal? → If yes: **congruent (SSS)**. Stop.
Step 4: Are two sides and the included angle equal? → If yes: **congruent (SAS)**. Stop.
Step 5: Are two angles and the included side equal? → If yes: **congruent (ASA)**. Stop.
Step 6: Are two angles and a non-included side equal? → If yes: **congruent (AAS)**. Stop.
Step 7: Is there a right angle, equal hypotenuse and one equal side? → If yes: **congruent (RHS)**. Stop.
Step 8: If none of the above: not congruent by these tests.

*Quick check:* Why does this algorithm check SSS before SAS?

**4. Extending to similarity.** After ruling out congruence (or as a separate branch), check for similarity:
Step A: Are all three pairs of corresponding angles equal? → If yes: **similar (AAA)**.
Step B: Are all three pairs of sides in the same ratio? → If yes: **similar (SSS-ratio)**.
Step C: Are two pairs of sides in the same ratio with included angle equal? → If yes: **similar (SAS-ratio)**.
Step D: If none: **neither congruent nor similar**.

*Quick check:* Can a pair of shapes be both congruent and similar?

**5. Testing the algorithm.** Test with known examples:
- Triangles (3,4,5) and (3,4,5) → SSS → congruent. ✓
- Triangles (3,4,5) and (6,8,10) → not congruent; ratio 2 for all sides → similar. ✓
- Triangles (3,4,5) and (3,4,6) → no match → neither. ✓
- Two equilateral triangles: sides 5,5,5 and 7,7,7 → not congruent; ratio 7/5 for all → similar. ✓

Testing reveals bugs. *Quick check:* What would happen if your algorithm did not sort sides from shortest to longest first?

**6. Worked example: designing and describing a quadrilateral algorithm.**

Design an algorithm to determine if two quadrilaterals are similar.

*Follow the thinking:*
- Input: four side lengths and four angles for each quadrilateral.
- Step 1: Check all four corresponding angles are equal. If not → neither.
- Step 2: Check all four corresponding side ratios are equal. If not → neither.
- Step 3: If both conditions met → similar.
- Describe: "The algorithm first verifies angle matching, then ratio matching. Both conditions must hold for quadrilateral similarity because, unlike triangles, equal angles alone do not guarantee similarity in quadrilaterals."

**7. Describing how the algorithm works.** A good description explains: what the inputs are, what each decision checks, why the decisions are in that order, and what the output means. It should be clear enough that someone else could follow it without your help. *Quick check:* Why is describing an algorithm important even after it works?

## Victorian and cultural context

- **Victorian anchor.** Engineers Australia uses algorithmic checking procedures for structural design — verifying that components meet geometric specifications is a step-by-step process. Quality-control systems at Australian manufacturing plants (e.g. Toyota Altona, before closure) used decision algorithms to check part dimensions against tolerances (congruence to a template). Victorian school IT curricula connect mathematical algorithms to coding.
- **Aboriginal and Torres Strait Islander perspective.** Traditional manufacturing processes — shaping boomerangs, grinding axes, weaving baskets — involve step-by-step decision-making: check the shape, adjust, check again. This iterative design-and-test process is algorithmic thinking applied to physical materials. Specific cultural knowledge should only be read through published, community-approved material.
- **Multicultural Australian perspective.** Algorithmic thinking underlies pattern recognition in textile design worldwide — weavers across cultures follow step-by-step procedures with decisions (which thread, which colour, which angle) to produce congruent repeated motifs.

## Try these scenarios

1. **Everyday.** You have two triangular pieces of fabric and need to check if they are the same shape and size (congruent) for a sewing project. Design a three-step algorithm using only a ruler and protractor. What do you measure first?
2. **Civic.** A council officer at the City of Casey needs to verify that replacement park signs are similar to the originals (same shape, scaled up by 1.5×). Design an algorithm she can follow with a tape measure.
3. **Vocational.** A CNC (computer numerical control) machinist programs a quality-check algorithm to verify cut metal triangles match a template. Write pseudocode (numbered steps with IF/THEN decisions) for the check.
4. **Ethical.** A facial recognition system uses algorithmic comparison of face proportions (similar triangles between facial landmarks). Discuss the benefits and risks of applying geometric similarity algorithms to human faces.
5. **Cross-cultural.** You are writing instructions for a partner class overseas to classify pairs of triangles you send them. They do not speak your language fluently. Design your algorithm using only flowchart symbols (boxes, diamonds, arrows) and mathematical notation — no English sentences inside the shapes.

## Memorable takeaways
- An algorithm = sequence of steps + decisions → classification.
- For congruence: check SSS, SAS, ASA, AAS, RHS in order.
- For similarity: check AAA, SSS-ratio, SAS-ratio.
- Always test your algorithm with known examples and edge cases.
- Describing how it works is part of the mathematics.

## If you need more support
- **Sentence stems to start your writing.** "My algorithm takes as input ___. Step 1: check if ___. If yes → ___. If no → go to Step 2. The algorithm works because ___."
- **Words to keep close.** Algorithm, sequence, decision, input, output, flowchart, pseudocode, test, edge case, congruent, similar.
- **Try this picture.** Draw a flowchart with diamond-shaped decision boxes and rectangular process boxes, showing the path from "Input: two triangles' measurements" to "Output: congruent / similar / neither."
- **A different way to show what you know.** Code your algorithm in Scratch or Python — input side lengths, output the classification. Test with five pairs of triangles.

## Stretch yourself
Design a complete algorithm (as a flowchart or pseudocode) that takes the three side lengths of two triangles as input and outputs one of: "congruent (SSS)," "similar (SSS-ratio)," or "neither." Your algorithm must: (a) sort both sets of sides from smallest to largest, (b) check for congruence first, (c) check for similarity if not congruent, (d) handle the edge case where one or both triangles are impossible (triangle inequality: any two sides must sum to more than the third). Test your algorithm with these pairs: (3,4,5) and (3,4,5); (3,4,5) and (6,8,10); (3,4,5) and (3,4,7); (1,2,5) and (2,4,10). Describe what each test reveals about your algorithm. 250–300 words.

## Watch out for these traps
- "I checked one condition and stopped." An algorithm should keep checking until it finds a match or exhausts all conditions. Stopping too early gives false negatives.
- "I forgot to sort the sides." Without sorting, you might compare the longest side of one triangle with the shortest side of another and falsely conclude "neither."
- "My algorithm works for my examples so it must be correct." You need edge cases: degenerate triangles, equilateral triangles, right triangles, impossible triangles. Testing only with easy cases misses bugs.
- "Describing the algorithm is optional." The description is how you communicate your reasoning — without it, nobody can verify or improve your algorithm.

## Try drawing this
A complete flowchart starting with "Input: sides of Triangle 1 and Triangle 2" and branching through SSS, SAS, ASA, AAS, RHS decisions, with each diamond labelled with the condition being checked and arrows labelled "Yes" and "No."

## Where to read more
- AMSI: "Algorithmic thinking" and "Congruence" modules.
- Khan Academy: "Intro to algorithms" and "Triangle congruence."
- ABC Education: Digital Technologies and Mathematics resources.
- nrich.maths.org: "Algorithm design" investigations.
- CS Unplugged: Algorithmic thinking activities (free, NZ-based, widely used in Victoria).

A note on certainty. The congruence and similarity conditions are mathematically proven. The algorithmic structures (sequence, decision, loop) are well-established in computer science. Designing a correct algorithm requires careful logic — testing is how you build confidence.

## Model responses

Use these to check your own thinking after you have had a go.

**Quick checks (Core content)**

1. *Three key features of an algorithm.* Sequence (ordered steps), decision (branching), and defined input/output.
2. *Inputs for triangle classification.* Three side lengths and/or three angles for each triangle.
3. *Why check SSS before SAS?* SSS requires only side measurements (simplest check). If it matches, you can stop immediately without measuring angles. Ordering from simplest to most complex is efficient.
4. *Can shapes be both congruent and similar?* Yes — congruent shapes are similar with scale factor 1.
5. *What if sides are not sorted?* You might compare mismatched sides (e.g. longest to shortest), producing incorrect ratios and a false "neither" result.
6. *Why describe the algorithm?* So others can follow, verify, improve and debug it. An undescribed algorithm is a black box.

**Try these scenarios**

1. *Fabric triangles.* Step 1: Measure all three sides of each piece. Step 2: Sort sides shortest to longest. Step 3: Compare corresponding sides — if all three match, congruent; if not, check ratios for similarity.
2. *Council signs.* Step 1: Measure original sign's width and height. Step 2: Multiply by 1.5 to get target dimensions. Step 3: Measure replacement sign. Step 4: If measurements match targets (within tolerance), accept; otherwise reject.
3. *CNC pseudocode.* 1. INPUT measured sides s1, s2, s3. 2. INPUT template sides t1, t2, t3. 3. IF |s1−t1| < 0.1 AND |s2−t2| < 0.1 AND |s3−t3| < 0.1 THEN OUTPUT "PASS." 4. ELSE OUTPUT "FAIL."
4. *Facial recognition.* Benefits: security, finding missing persons. Risks: bias in training data, surveillance overreach, consent issues, false matches disproportionately affecting some groups.
5. *Universal flowchart.* Use: rectangles for "Sort sides," diamonds for "All sides equal? / All ratios equal?", arrows labelled with ✓ and ✗, output boxes labelled "≅", "∼", "≠".

**Stretch task — example shape of a strong answer.** Algorithm: (1) Sort both side sets. (2) Triangle inequality check: if a+b ≤ c for any pair → output "impossible triangle." (3) Compare sorted sides: if all equal → "congruent (SSS)." (4) Else: compute ratios s₁/t₁, s₂/t₂, s₃/t₃. If all ratios equal → "similar (SSS-ratio)." (5) Else → "neither." Tests: (3,4,5)&(3,4,5) → congruent ✓. (3,4,5)&(6,8,10) → ratios all 2 → similar ✓. (3,4,5)&(3,4,7) → not equal, ratios 1,1,1.4 → neither ✓. (1,2,5)&(2,4,10) → 1+2=3<5 → "impossible triangle" ✓. Edge case handled.
