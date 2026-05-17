# VC2M9SP03 — Mathematics

## Snapshot
- **Descriptor:** VC2M9SP03. Design, test and refine algorithms involving a sequence of steps and decisions based on geometric constructions and theorems; discuss and evaluate refinements.
- **Year level / Learning area:** Years 9–10, Mathematics (Space).
- **Big ideas:**
  - An **algorithm** is a step-by-step procedure that, when followed precisely, produces a reliable result.
  - Geometric constructions (compass and straightedge) can be expressed as algorithms — sequences of steps with decision points.
  - Algorithms can be tested, refined and evaluated for efficiency and accuracy.
- **Curriculum hooks:** Numeracy; Critical and Creative Thinking; Digital Technologies.

## What you are learning
- You are learning to **design, test and refine algorithms** for geometric constructions and theorem-based procedures.
- You are learning to evaluate algorithms for correctness, clarity and efficiency.

By the end of this you should be able to:
- Write a clear sequence of steps for a geometric construction.
- Include decision points (if/then) where needed.
- Test your algorithm by having someone else follow it.
- Refine based on feedback — improve clarity, reduce steps, fix errors.
- Discuss why the algorithm works by linking steps to geometric theorems.

## Core content

**1. What is a geometric algorithm?** A geometric algorithm is a precise set of instructions that produces a geometric construction or solves a spatial problem. Like a recipe — each step must be clear, unambiguous, and in the correct order. Example: "To bisect a line segment: (1) Set compass width greater than half the segment. (2) Place compass at one end, draw arcs above and below. (3) Without changing width, repeat from other end. (4) Draw a line through the two intersection points." *Quick check:* Why must the compass width be "greater than half the segment" in step 1?

**2. Decision points in algorithms.** Some algorithms require decisions: "If the angle is obtuse, then..." or "Repeat until the desired accuracy is reached." These conditional steps make algorithms flexible. Example in bisection: "If arcs don't intersect, THEN increase compass width and repeat." *Quick check:* Write a decision point for an algorithm that constructs a perpendicular from a point to a line — what could go wrong that needs a conditional step?

**3. Linking steps to theorems.** Each step in a geometric algorithm works because of an underlying theorem. The perpendicular bisector construction works because "the locus of points equidistant from two endpoints lies on the perpendicular bisector" (theorem). Understanding WHY each step works transforms rote procedure into mathematical reasoning. *Quick check:* Why does the angle bisector construction produce two equal angles?

**4. Testing algorithms.** Give your algorithm to someone unfamiliar with the construction. Can they follow it exactly and get the correct result? Testing reveals: ambiguous steps, missing decisions, incorrect order, or unnecessary steps. A good algorithm works for ANY valid input, not just one specific case. *Quick check:* An algorithm says "Draw a circle." What information is missing that would cause failure?

**5. Refining algorithms.** After testing, improve: clarify ambiguous language, add missing steps, remove redundancy, optimise (fewer steps = more efficient). Consider: does the algorithm work for edge cases (very small angles, very long lines, degenerate triangles)? *Quick check:* Your algorithm for constructing a 60° angle has 8 steps. A classmate achieves the same result in 5 steps. Which is better? Why might the longer version still be preferable in some contexts?

**6. Worked example — algorithm for constructing a triangle given three sides (SSS).**

*Algorithm:*
1. Given sides a, b, c. Check: does each side satisfy the triangle inequality? (a + b > c, b + c > a, a + c > b). If NO → output "triangle impossible." STOP.
2. Draw a base line of length a (using ruler).
3. Set compass to width b. Place at left endpoint. Draw an arc above the base.
4. Set compass to width c. Place at right endpoint. Draw an arc above the base.
5. If arcs do not intersect → error in measurements or step 1 check failed. STOP.
6. Mark intersection point. Connect to both endpoints.
7. Label the triangle. Verify by measuring all three sides.

*Why it works:* The arcs represent all points at distance b from one end and c from the other. Their intersection satisfies both distance requirements simultaneously.

**7. Evaluating algorithms — criteria.** (1) Correctness: does it always produce the right result? (2) Completeness: does it handle all valid inputs and edge cases? (3) Clarity: can someone unfamiliar follow it? (4) Efficiency: does it use the minimum necessary steps? (5) Justification: is each step linked to a theorem or definition? *Quick check:* Rate the SSS algorithm above on these five criteria. Can you suggest an improvement?

## Victorian and cultural context

- **Victorian anchor.** Computer-aided design (CAD) software used by Melbourne architects and engineers (Aurecon, Arup) runs geometric algorithms — every line, arc and intersection in a blueprint is generated by algorithmic instructions. CNC machines in Victorian manufacturing follow geometric algorithms to cut precise shapes. VCE Algorithmics (HESS) teaches algorithmic thinking for exactly these applications. 3D printing relies on algorithms that construct shapes layer by layer.
- **Aboriginal and Torres Strait Islander perspective.** Traditional construction techniques — weaving baskets, building shelters, creating fish traps — follow algorithmic processes refined over thousands of years. Each step produces a specific geometric outcome (angle, curve, structural strength). These are algorithms transmitted orally and through demonstration, tested by function (does the basket hold water? does the trap catch fish?) and refined across generations. Specific cultural knowledge should only be read through published, community-approved material.
- **Multicultural Australian perspective.** Algorithmic construction appears across cultures: Islamic geometric patterns follow precise algorithms to create tessellations; origami uses step-by-step folding algorithms; Celtic knots follow systematic rules. Students from all backgrounds can connect algorithmic thinking to cultural craft traditions.

## Try these scenarios

1. **Everyday.** Write an algorithm for constructing a regular hexagon using compass and straightedge. Test it by giving it to a classmate. Refine based on their feedback.
2. **Civic.** A council needs to find the centre of a circular park (to place a fountain) when only part of the circle's edge is visible. Design an algorithm using the perpendicular bisector of chords method. Include decision points.
3. **Vocational.** A carpenter needs to bisect any angle (for mitre cuts). Write a clear algorithm for angle bisection that a non-mathematician could follow. Justify each step with the relevant theorem.
4. **Ethical.** Two students write different algorithms for the same construction. One has 4 steps but is ambiguous; the other has 8 steps but is crystal clear. Discuss: is efficiency or clarity more important? Does the audience matter?
5. **Cross-cultural.** Research how Islamic geometric artists constructed their patterns (algorithm of repeated circles and connecting points). Write the algorithm for creating a basic 6-fold pattern. Test and refine it.

## Memorable takeaways
- An algorithm is a precise, step-by-step procedure that always works.
- Geometric algorithms include construction steps AND decision points.
- Every step should be justified by a theorem or definition.
- Test by having someone else follow your instructions exactly.
- Refine for correctness, clarity, completeness, and efficiency.

## If you need more support
- **Sentence stems to start your writing.** "Step 1: ___. Step 2: ___. Decision: If ___, then ___. This step works because ___ (theorem). Testing showed ___. I refined by ___."
- **Words to keep close.** algorithm, construction, decision point, conditional, theorem, bisect, perpendicular, locus, test, refine, efficiency.
- **Try this picture.** Write your algorithm on the left side of a page. On the right, draw each step as you follow it. Annotate with the theorem that justifies each step.
- **A different way to show what you know.** Create a flowchart (with diamonds for decisions, rectangles for steps) for a geometric construction. Include error-handling paths.

## Stretch yourself
Design an algorithm that, given any triangle (by its three vertices), finds the circumcentre (the centre of the circle passing through all three vertices). Your algorithm should: (1) construct the perpendicular bisector of two sides, (2) find their intersection, (3) verify by checking the third perpendicular bisector passes through the same point, (4) draw the circumscribed circle. Include all decision points (what if the triangle is right-angled? obtuse?). Justify every step with the relevant theorem. Test your algorithm on three different triangles (acute, right, obtuse). Discuss how the circumcentre's position changes and why. Present as a flowchart with annotations. 250–300 words.

## Watch out for these traps
- **Assuming the reader knows what you know.** Test with someone who hasn't seen the construction before.
- **Missing decision points.** What if arcs don't intersect? What if the point is on the line? Always handle edge cases.
- **Steps out of order.** An algorithm must be sequential — each step depends on previous steps being complete.
- **No justification.** An algorithm without theorem links is just a procedure — you should know WHY each step works.
- **Confusing "algorithm" with "doing the construction."** The algorithm is the written instructions, not the drawing itself.

## Try drawing this
Create a flowchart for "Construct the perpendicular bisector of segment AB": Start → Set compass > ½AB → Arc from A above and below → Arc from B above and below → Do arcs intersect? (Yes → mark intersections, draw line. No → increase compass, go back.) → End. Use proper flowchart symbols (rounded start/end, rectangles for actions, diamonds for decisions).

## Where to read more
- AMSI teacher resources: Geometric constructions.
- Khan Academy: Compass and straightedge constructions.
- NRICH: Construction challenges.
- GeoGebra: Step-by-step construction tools.
- "Algorithms Unplugged" — geometric algorithms without computers.
- VCE Algorithmics (HESS): Computational thinking.

A note on certainty. A correctly designed geometric algorithm produces exact results — the constructions are based on proven theorems and produce mathematically precise outcomes (unlike measurement, which always involves approximation). The bisector IS exact; the angle IS exactly halved. This is the power of construction over measurement. When algorithms are correctly justified by theorems, they guarantee exact results for all valid inputs.

## Model responses

Use these to check your own thinking after you have had a go.

**Quick checks (Core content)**
1. *Compass width > half segment.* Otherwise the arcs drawn from each end won't reach each other — they won't intersect. The arcs need to overlap to create intersection points.
2. *Decision point for perpendicular.* "If the point lies ON the line, THEN use the angle bisection method at that point instead of the external perpendicular method."
3. *Angle bisector works because...* The intersection point of the arcs is equidistant from both rays of the angle (by the property of equal radii). Any point equidistant from both rays lies on the angle bisector.
4. *"Draw a circle" — missing info.* Centre and radius. Without both, the instruction is ambiguous.
5. *8 steps vs 5 steps.* Fewer steps is more efficient but only better if still clear and correct. For a novice audience, clarity (8 steps) is more important. For experienced users, efficiency (5 steps) is preferred. Context and audience determine the right balance.
6. *SSS algorithm.* Worked through in example. The triangle inequality check (step 1) is essential to handle impossible inputs.
7. *SSS evaluation.* Correct: yes (based on theorem). Complete: handles impossible case. Clear: reasonably (could specify "above" more precisely). Efficient: 7 steps is reasonable. Justified: step 6 links to equidistance theorem. Improvement: specify "arc above (on the same side)" more precisely in steps 3–4.

**Try these scenarios**
1. *Hexagon algorithm.* (1) Draw circle, radius r. (2) Mark any point on circumference. (3) Set compass to r. (4) Step around circle marking intersections (each arc meets circle at next vertex). (5) Connect consecutive points. Works because the central angle is 60° (equilateral triangles from centre).
2. *Park centre.* (1) Identify three points on the visible arc. (2) Connect to make two chords. (3) Construct perpendicular bisector of each chord. (4) Bisectors intersect at centre. Decision: if only two points visible, need more of the edge. Theorem: perpendicular bisector of a chord passes through the centre.
3. *Angle bisection for carpenter.* (1) Place compass point at angle vertex. (2) Draw arc cutting both rays. (3) From each intersection, draw equal arcs inside the angle. (4) Draw line from vertex through intersection of arcs. Theorem: intersection point is equidistant from both rays → lies on bisector.
4. *Efficiency vs clarity.* For a trained carpenter (audience), efficient 4-step version is better — they fill in gaps from experience. For a trainee, the 8-step version prevents errors. Good algorithms adapt to their audience. In assessment, clarity with justification is always preferred.
5. *Islamic pattern.* (1) Draw a circle. (2) Mark 6 equally spaced points using radius method (hexagon). (3) Connect alternate points (makes two overlapping triangles = Star of David). (4) Draw circles centred on each vertex through centre. (5) Connect intersection points to form the pattern. Theorem: 6-fold symmetry from equilateral triangles inscribed in a circle.

**Stretch task — example shape of a strong answer.** Circumcentre algorithm: (1) Given triangle ABC. (2) Find midpoint M₁ of AB (measure and halve). (3) Construct perpendicular bisector of AB through M₁. (4) Find midpoint M₂ of BC. (5) Construct perpendicular bisector of BC through M₂. (6) Mark intersection O of the two bisectors. Decision: if lines appear parallel (shouldn't happen for non-degenerate triangle) → check constructions for error. (7) Verify: construct perpendicular bisector of AC — it should pass through O. If not → refine constructions. (8) Set compass to distance OA. Draw circle. Decision: if triangle is right-angled → circumcentre is at the midpoint of the hypotenuse (special case, still works). If obtuse → circumcentre lies outside the triangle (still valid). Justification: perpendicular bisector of a side = locus of points equidistant from that side's endpoints. Intersection of two such bisectors is equidistant from all three vertices. Testing: acute triangle → O inside. Right → O on hypotenuse midpoint. Obtuse → O outside. All correctly handled by the algorithm.
