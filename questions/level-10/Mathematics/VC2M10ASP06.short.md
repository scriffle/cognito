# VC2M10ASP06 — Mathematics (Short)

## Snapshot
- **Descriptor:** Design, test and refine algorithms for spatial problems.
- **Year / Area:** Years 9–10 Advanced, Mathematics.
- **Big ideas:** Algorithms are step-by-step procedures for solving spatial problems. Examples include point-in-polygon, shortest path and area from coordinates. Testing must cover edge cases.

## What you are learning
- You are learning to **design, test and refine algorithms** for spatial and geometric problems.
- You should be able to express geometric reasoning as repeatable, testable procedures.

## Core content

**Spatial algorithm:** A finite sequence of steps solving a geometric problem (e.g. point-in-polygon, shortest path, area calculation).

**Point-in-polygon:** Cast a ray from the point, count boundary crossings. Odd = inside, even = outside.

**Shortest path (Dijkstra):** Start = 0, others = ∞. Visit nearest unvisited node, update neighbour distances, repeat.

**Shoelace formula:** Area = ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)| for polygon vertices in order.

**Testing:** Check typical cases, boundary cases (point on edge) and degenerate cases (collinear points). Refine when edge cases cause failure.

**Victorian context.** Spatial algorithms underpin GIS, urban planning and autonomous navigation. Al-Khwarizmi (9th century) gave the word "algorithm" its name.

## Memorable takeaways
- Algorithm: finite, step-by-step procedure solving a class of problems.
- Point-in-polygon: ray crossing count — odd = inside.
- Always test against edge cases and refine when failures occur.
- Shoelace formula gives polygon area from coordinates.

## Watch out for these traps
- Not handling edge cases (points on boundary, collinear vertices).
- Assuming greedy algorithms give optimal solutions.
- Testing floating-point equality without tolerance.

## Model responses

- *Ray crosses boundary 3 times.* Inside (odd).
- *Dijkstra start distance.* 0.
- *Shoelace for (0,0),(5,0),(5,4),(0,4).* Area = 20. ✓
- *Edge case for point-in-polygon.* Ray passing through a vertex.
- *Decimal equality problem.* Floating-point rounding — use tolerance |a − b| < ε.
- *Nearest-neighbour limitation.* Greedy heuristic, not guaranteed shortest total route.
