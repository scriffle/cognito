# VC2M10ASP06 — Mathematics

## Snapshot
- **Descriptor:** VC2M10ASP06. Design, test and refine algorithms for spatial problems.
- **Year level / Learning area:** Years 9–10 Advanced, Mathematics (Space).
- **Big ideas:**
  - An algorithm is a step-by-step procedure guaranteed to solve a class of problems.
  - Spatial algorithms include point-in-polygon tests, shortest path calculations and geometric constructions.
  - Designing algorithms develops computational thinking — decomposing spatial problems into repeatable, testable steps.
- **Curriculum hooks:** Numeracy; Critical and Creative Thinking; Digital Literacy.

## What you are learning
- You are learning to **design, test and refine algorithms** that solve spatial and geometric problems.
- You are learning to express geometric reasoning as step-by-step procedures, test them against known cases, and improve them when they fail.

By the end of this you should be able to:
- Design an algorithm for a spatial task (e.g. point-in-polygon, shortest path, area calculation).
- Express the algorithm in clear, ordered steps (pseudocode or flowchart).
- Test the algorithm against specific cases, including edge cases.
- Identify when an algorithm fails and refine it.
- Evaluate the efficiency of alternative algorithms for the same task.

## Core content

**1. What is a spatial algorithm?** An algorithm is a finite sequence of well-defined steps that solves a problem. A spatial algorithm operates on geometric objects — points, lines, polygons, circles. Examples: determining whether a point lies inside a polygon, finding the shortest path between two points, computing the convex hull of a set of points. *Quick check:* Give an example of a spatial problem that could be solved by an algorithm.

**2. Point-in-polygon test.** One common algorithm: cast a ray from the test point in any direction and count intersections with the polygon boundary. Odd count → inside; even count → outside. Steps: (1) Choose a direction for the ray. (2) For each edge of the polygon, determine whether the ray intersects it. (3) Count total intersections. (4) If odd, the point is inside. *Quick check:* A ray from a test point crosses a polygon boundary 3 times. Is the point inside or outside?

**3. Shortest path algorithms.** On a network (graph), shortest path algorithms find the minimum-distance route. Dijkstra's algorithm: (1) Set distance to start = 0, all others = ∞. (2) Visit the unvisited node with smallest distance. (3) Update distances to its neighbours. (4) Mark as visited. (5) Repeat until destination reached. This guarantees the shortest path in a weighted graph with non-negative weights. *Quick check:* In Dijkstra's algorithm, what is the initial distance assigned to the start node?

**4. Area of an irregular polygon.** The Shoelace formula computes area from coordinates: Area = ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)|. Algorithm: (1) List vertices in order. (2) Multiply each x by the next y. (3) Multiply each y by the next x. (4) Subtract the sums. (5) Take half the absolute value. For triangle (0,0), (4,0), (0,3): Area = ½|0·0 − 4·0 + 4·3 − 0·0 + 0·0 − 0·3| = ½|12| = 6. *Quick check:* Use the Shoelace formula to find the area of the quadrilateral with vertices (0,0), (5,0), (5,4), (0,4).

**5. Testing and edge cases.** A well-designed algorithm must be tested against: (a) typical cases, (b) boundary cases (point on the edge), (c) degenerate cases (collinear points, zero-area polygons). If the point-in-polygon ray passes through a vertex, the count may be incorrect — the algorithm needs a rule for handling this edge case. *Quick check:* Name an edge case that might cause the point-in-polygon algorithm to give an incorrect result.

**6. Worked example — designing a triangle classifier.**
Design an algorithm that classifies a triangle given three side lengths.

*Algorithm:*
1. Input three sides a, b, c.
2. Check triangle inequality: a + b > c, a + c > b, b + c > a. If any fails → "Not a valid triangle." Stop.
3. Sort sides so a ≤ b ≤ c.
4. If a² + b² = c² → "Right-angled."
5. If a² + b² > c² → "Acute."
6. If a² + b² < c² → "Obtuse."
7. If a = b = c → also "Equilateral." If exactly two sides equal → also "Isosceles."

*Testing:* (3, 4, 5) → right-angled. (5, 5, 5) → acute, equilateral. (3, 4, 8) → not valid. (2, 2, 3) → obtuse, isosceles.

**7. Refining algorithms.** After testing reveals failures or inefficiencies, refine the algorithm. Refinements include: handling edge cases, reducing the number of steps, improving accuracy (e.g. using tolerance for floating-point comparisons: |a² + b² − c²| < ε instead of strict equality). Document what was changed and why. *Quick check:* Why might testing a² + b² = c² with decimal side lengths give incorrect results?

## Victorian and cultural context

- **Victorian anchor.** Spatial algorithms underpin geographic information systems (GIS), urban planning, autonomous vehicle navigation and computer-aided design — all significant Victorian industries and research areas.
- **Aboriginal and Torres Strait Islander perspective.** First Nations peoples developed sophisticated algorithmic approaches to spatial problems — route planning across vast landscapes using songlines, systematic fish-trap construction, and seasonal movement patterns optimised over millennia.
- **Multicultural Australian perspective.** Al-Khwarizmi (9th century Persian mathematician) gave the word "algorithm" its name. Euclid's geometric constructions (3rd century BCE) are among the earliest documented spatial algorithms.

## Try these scenarios

1. **Everyday.** Design an algorithm that determines whether a rectangular table (l × w) will fit through a doorway of width d when tilted. Describe the steps and test with l = 2 m, w = 0.8 m, d = 0.9 m.
2. **Civic.** A council needs to determine which properties fall within a flood zone (defined as a polygon on a map). Describe how the point-in-polygon algorithm could be applied.
3. **Vocational.** A delivery driver needs to visit 5 locations and return to the depot. Design an algorithm (greedy nearest-neighbour) to find a short route. What is the limitation of this approach?
4. **Ethical.** A GPS navigation algorithm always finds the shortest distance. Discuss why this may not always be the best route (traffic, road conditions, emissions).
5. **Cross-cultural.** Research al-Khwarizmi's contributions. Then design an algorithm to find the circumcentre of a triangle given three vertex coordinates.

## Memorable takeaways
- An algorithm is a finite, step-by-step procedure that solves a class of problems.
- Point-in-polygon: cast a ray, count crossings — odd = inside.
- Always test algorithms against typical cases, boundary cases and degenerate cases.
- Refine when edge cases cause failure — document what changed.
- The Shoelace formula gives polygon area from coordinates.

## If you need more support
- **Sentence stems to start your writing.** "Step 1: Input ___. Step 2: Calculate ___. Step 3: If ___, then ___. Step 4: Output ___."
- **Words to keep close.** algorithm, pseudocode, flowchart, edge case, boundary case, spatial, polygon, shortest path, efficiency, refinement.
- **Try this picture.** Draw a flowchart for the triangle classifier algorithm, with decision diamonds for each test.
- **A different way to show what you know.** Write pseudocode for an algorithm, then trace through it with a specific example, recording the value of each variable at each step.

## Stretch yourself
(a) Design an algorithm that determines whether two circles intersect, are tangent, or do not intersect, given their centres and radii. (b) Implement the Shoelace formula as pseudocode for a polygon with n vertices. (c) Compare the nearest-neighbour algorithm with a brute-force approach for the delivery driver problem — which is better and why? (d) Discuss how floating-point precision affects spatial algorithms. 250–300 words.

## Watch out for these traps
- **Not handling edge cases.** A point exactly on the boundary, collinear points, or zero-length sides can break algorithms.
- **Assuming the first solution is optimal.** Greedy algorithms (like nearest-neighbour) find a solution quickly but not necessarily the best one.
- **Floating-point equality.** Never test exact equality for calculated values — use a tolerance (|a − b| < ε).
- **Incomplete testing.** Testing only typical cases misses boundary and degenerate failures.

## Try drawing this
Draw a polygon with 6 sides. Mark a point inside and a point outside. For each point, draw a horizontal ray and count the edge crossings to verify the point-in-polygon algorithm.

## Where to read more
- AMSI teacher resources: Algorithms and computational thinking.
- Khan Academy: Algorithms.
- CS Unplugged: Spatial algorithms without a computer.
- GeoGebra: interactive polygon and algorithm tools.
- MacTutor History of Mathematics: Al-Khwarizmi.

A note on certainty. Algorithm design involves both mathematical proof (correctness) and empirical testing (robustness). A correct algorithm is guaranteed to produce the right answer for all valid inputs, but edge cases must be identified and handled through systematic testing.

## Model responses

Use these to check your own thinking after you have had a go.

**Quick checks (Core content)**
1. *Spatial problem example.* Finding the shortest path between two locations on a map; determining whether a point is inside a park boundary.
2. *Ray crosses 3 times.* Inside (odd count).
3. *Dijkstra's start distance.* 0.
4. *Shoelace for rectangle.* Vertices (0,0), (5,0), (5,4), (0,4). Area = ½|0·0 − 5·0 + 5·4 − 5·0 + 5·4 − 0·4 + 0·0 − 0·0| = ½|0 + 20 + 0 + 0 − 0 − 0 − 0 + 0|. Using the formula systematically: ½|(0×0 − 5×0) + (5×4 − 5×0) + (5×4 − 0×4) + (0×0 − 0×0)| — more carefully: Σ(xᵢyᵢ₊₁) = 0 + 20 + 0 + 0 = 20. Σ(xᵢ₊₁yᵢ) = 0 + 0 + 0 + 0 = 0. Area = ½|20| = 10. Hmm — let's recalculate. (0·0) + (5·4) + (5·4) + (0·0) = 40. (0·5) + (0·5) + (4·0) + (4·0) = 0. Area = ½|40 − 0| = 20. This confirms the rectangle has area 5 × 4 = 20. ✓
5. *Edge case.* A ray passing through a vertex of the polygon — the intersection count may be ambiguous.
6. *Triangle classifier.* Tested in core content.
7. *Decimal equality.* Floating-point arithmetic introduces rounding errors. Testing strict equality (a² + b² == c²) may fail even for a genuine right triangle. A tolerance test (|a² + b² − c²| < ε) is needed.

**Try these scenarios**
1. *Table through door.* The diagonal of the table cross-section = √(l² + w²). If w < d, it fits straight; otherwise tilt and check diagonal clearance. √(4 + 0.64) = √4.64 ≈ 2.15 m (too big for tilt), but w = 0.8 < 0.9 = d, so it fits through straight.
2. *Flood zone.* For each property, take a representative point (e.g. centroid). Apply point-in-polygon with the flood zone boundary. Properties with odd crossing counts are in the zone.
3. *Nearest-neighbour.* Start at depot. Visit closest unvisited location. Repeat until all visited. Return to depot. Limitation: does not guarantee the shortest total route — it is a greedy heuristic.
4. *GPS limitation.* Shortest distance may involve narrow roads, school zones, or high-traffic areas. Optimal routing should consider time, safety, fuel consumption and road conditions.
5. *Circumcentre.* Find perpendicular bisectors of two sides. Solve their equations simultaneously. The intersection is the circumcentre.
