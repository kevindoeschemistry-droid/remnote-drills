# Geometry — curriculum framework (draft 1)

Generated from `drills/frameworks/geometry.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**8 learning objectives** in 3 units (8 core): 8 drilled, 0 partly, 0 with no drills. Core: 8 / 8 drilled.

## Big ideas

- **LINE · Straight means shortest.** A geodesic is a locally shortest path. On a sphere it is a great circle; in the half-plane model it is a vertical line or a semicircle meeting the boundary at right angles.
- **CURV · Curvature is the angle surplus per area.** A triangle's angles exceed π on a sphere and fall short in the hyperbolic plane, by exactly the curvature times its area.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Spherical geometry | core | — | 3 | 3 | 0 | 0 |
| 2 · Hyperbolic geometry | core | — | 3 | 3 | 0 | 0 |
| 3 · Curvature | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Spherical geometry

Big ideas: LINE, CURV

### 1.1 Lines and triangles on the sphere



- ● **GE-1.1.A** (cambridge-ib-geometry:SPH) Find great-circle distances and the areas of lunes.
  - EK: Spherical lines are great circles. The distance between two points is R times the angle they subtend at the centre, and a lune between two great circles meeting at angle θ has area 2θR².
  - P1 · drills: ge-great-circle-distance, ge-lune-area
- ● **GE-1.1.B** (cambridge-ib-geometry:SPH) Use the angle excess of a spherical triangle or polygon.
  - EK: A spherical triangle with angles α, β, γ on a sphere of radius R has area (α + β + γ − π)R². An n-gon has area (angle sum − (n − 2)π)R².
  - Needs: GE-1.1.A
  - P1 · drills: ge-spherical-triangle-area, ge-spherical-third-angle
- ● **GE-1.1.C** (cambridge-ib-geometry:SPH) Describe the isometries of the sphere and its finite rotation groups.
  - EK: The isometries of the sphere are the orthogonal maps: rotations about an axis and their compositions with reflections. The finite groups of rotations are cyclic, dihedral, or the rotation groups of the tetrahedron (order 12), cube (24) and icosahedron (60).
  - Needs: GE-1.1.B
  - P2 · drills: ge-sphere-isometries, ge-triangulation-count

## Unit 2 · Hyperbolic geometry

Big ideas: LINE, CURV

### 2.1 The half-plane and disc models



- ● **GE-2.1.A** (cambridge-ib-geometry:RIE, cambridge-ib-geometry:HYP) Measure length in the upper half-plane and identify its geodesics.
  - EK: The half-plane metric is (dx² + dy²)/y². Geodesics are vertical lines and semicircles centred on the real axis; the distance from ai to bi is |ln(b/a)|.
  - Needs: GE-1.1.A
  - P1 · drills: ge-hyperbolic-distance, ge-hyperbolic-geodesics
- ● **GE-2.1.B** (cambridge-ib-geometry:HYP) Use the angle defect of a hyperbolic triangle and compare parallels in the three geometries.
  - EK: A hyperbolic triangle with angles α, β, γ has area π − (α + β + γ), so no triangle has area above π; an ideal triangle has area exactly π. Through a point off a line there are infinitely many lines that never meet it.
  - Needs: GE-2.1.A, GE-1.1.B
  - P1 · drills: ge-hyperbolic-triangle-area, ge-parallels
- ● **GE-2.1.C** (cambridge-ib-geometry:RIE, cambridge-ib-geometry:HYP) Compare circumferences of circles in the three geometries.
  - EK: A circle of geodesic radius r has circumference 2π sin r on the unit sphere, 2πr in the plane and 2π sinh r in the hyperbolic plane: less room than flat on the sphere, more in the hyperbolic plane.
  - Needs: GE-2.1.A
  - P1 · drills: ge-circle-sphere, ge-circle-hyperbolic

## Unit 3 · Curvature

Big ideas: CURV

### 3.1 One number behind three geometries



- ● **GE-3.1.A** (cambridge-ib-geometry:CUR) State the Gaussian curvature of the model spaces and how it scales.
  - EK: A sphere of radius R has curvature 1/R², the plane 0, and the hyperbolic plane −1. Scaling lengths by a factor c divides curvature by c².
  - Needs: GE-2.1.C
  - P1 · drills: ge-sphere-curvature, ge-curvature-sign
- ● **GE-3.1.B** (cambridge-ib-geometry:CUR, cambridge-ib-geometry:SPH, cambridge-ib-geometry:HYP) Use the Gauss-Bonnet relation between curvature, area and angle sum.
  - EK: For a geodesic triangle, α + β + γ − π = ∫ K dA. For a closed surface, ∫ K dA = 2πχ: 4π for any sphere, 0 for a torus, 4π(1 − g) for genus g.
  - Needs: GE-3.1.A, GE-2.1.B
  - P1 · drills: ge-total-curvature, ge-angle-sum-from-curvature
