# Engineering Mechanics — curriculum framework (draft 1)

Generated from `drills/frameworks/engineering-mechanics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**20 learning objectives** in 3 units (20 core): 20 drilled, 0 partly, 0 with no drills. Core: 20 / 20 drilled.

## Big ideas

- **FBD · Isolate the body, then balance it.** Every statics and dynamics problem starts by cutting one body free and writing the forces and moments on it: zero for equilibrium, mass times acceleration otherwise.
- **STRESS · Stress is load over the geometry that carries it.** Axial stress divides by area, bending by the section modulus, torsion by the polar moment: the material sees the same load very differently depending on shape.

## Practices

- **P1 · Compute.** Carry an equilibrium, energy or stress relation to a number with its unit.
- **P2 · Classify.** Name the case, the support condition or the rule that applies.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Statics | core | — | 6 | 6 | 0 | 0 |
| 2 · Dynamics and vibrations | core | — | 6 | 6 | 0 | 0 |
| 3 · Mechanics of materials | core | — | 8 | 8 | 0 | 0 |

## Unit 1 · Statics

Big ideas: FBD

### 1.1 Bodies at rest



- ● **MEC-1.1.A** (fe-mechanical:6A) Find the resultant of two forces and the moment of a force.
  - EK: Two forces at angle θ have a resultant of magnitude √(A² + B² + 2AB cos θ). The moment of a force about a point is the force times its perpendicular distance: M = F d sin θ.
  - Needs: PH-5.6.B, CA-6.4.A
  - P1 · drills: mec-resultant, mec-moment
- ● **MEC-1.1.B** (fe-mechanical:6B) Solve a concurrent force system in equilibrium.
  - EK: For a particle in equilibrium the forces sum to zero in each direction. A weight hung from two identical cables at angle θ above the horizontal gives 2T sin θ = W.
  - Needs: MEC-1.1.A
  - P1 · drills: mec-cable-tension, mec-third-force
- ● **MEC-1.1.C** (fe-mechanical:6C) Find support reactions on a beam.
  - EK: Sum moments about one support to get the other reaction, then sum vertical forces. A uniform load acts at the middle of its length.
  - Needs: MEC-1.1.B
  - P1 · drills: mec-beam-reaction, mec-beam-reaction-udl
- ● **MEC-1.1.D** (fe-mechanical:6D) Find member forces in a simple truss and state the truss assumptions.
  - EK: Truss members are two-force members joined by pins and loaded only at joints, so each carries pure tension or compression. At a joint the forces balance: in a symmetric triangular truss with a load P at the apex, each inclined member carries P ÷ (2 sin θ) in compression.
  - Needs: MEC-1.1.C
  - P1 · drills: mec-truss-member, mec-truss-rules
- ● **MEC-1.1.E** (fe-mechanical:6E) Locate a centroid and compute an area moment of inertia.
  - EK: The centroid of a composite area is the area-weighted average of its parts' centroids. A rectangle has I = b h³ ÷ 12 about its own centroidal axis; the parallel-axis theorem moves it: I = I_c + A d².
  - Needs: MEC-1.1.D
  - P1 · drills: mec-centroid-composite, mec-parallel-axis
- ● **MEC-1.1.F** (fe-mechanical:6F) Apply the laws of static friction.
  - EK: Static friction takes whatever value equilibrium needs up to μs N. A block on an incline is on the point of sliding when tan θ = μs.
  - Needs: MEC-1.1.E
  - P1 · drills: mec-angle-of-repose, mec-push-to-slide

## Unit 2 · Dynamics and vibrations

Big ideas: FBD

### 2.1 Bodies in motion



- ● **MEC-2.1.A** (fe-mechanical:7A) Find velocity by integrating acceleration and the normal acceleration on a curve.
  - EK: Velocity is the integral of acceleration over time. On a curved path the acceleration has a tangential part dv/dt and a normal part v² ÷ ρ directed toward the centre of curvature.
  - Needs: MEC-1.1.F, PH-6.6.B, PH-7.4.A
  - P1 · drills: mec-velocity-from-accel, mec-normal-acceleration
- ● **MEC-2.1.B** (fe-mechanical:7B, fe-mechanical:7C) Apply Newton's second law with kinetic friction.
  - EK: On an incline at angle θ a sliding block accelerates at g (sin θ − μk cos θ) down the slope. On level ground a pushed block accelerates at (F − μk m g) ÷ m.
  - Needs: MEC-2.1.A
  - P1 · drills: mec-incline-acceleration, mec-pushed-block
- ● **MEC-2.1.C** (fe-mechanical:7D, fe-mechanical:7E) Use work-energy and impulse-momentum for a particle.
  - EK: The work done by all forces equals the change in kinetic energy. The impulse (force × time) equals the change in momentum.
  - Needs: MEC-2.1.B
  - P1 · drills: mec-speed-with-friction, mec-impulse
- ● **MEC-2.1.D** (fe-mechanical:7F) Relate angular and linear motion and use rolling without slipping.
  - EK: A point at radius r on a body turning at ω moves at v = ω r. A wheel rolling without slipping has v = ω r at its centre; the contact point is momentarily at rest and the top moves at 2v.
  - Needs: MEC-2.1.C
  - P1 · drills: mec-rim-speed, mec-rolling-top
- ● **MEC-2.1.E** (fe-mechanical:7H, fe-mechanical:7I) Apply Newton's second law to rotation and to rolling bodies.
  - EK: Torque = I α. A solid disc has I = ½ m r², a hoop m r², a solid sphere ⅖ m r². A body with I = k m r² rolling without slipping down an incline accelerates at g sin θ ÷ (1 + k).
  - Needs: MEC-2.1.D
  - P1 · drills: mec-angular-acceleration, mec-rolling-incline
- ● **MEC-2.1.F** (fe-mechanical:7K) Find the natural frequency and damping ratio of a spring-mass system.
  - EK: Undamped natural frequency ωn = √(k ÷ m), so f = ωn ÷ 2π. Damping ratio ζ = c ÷ (2 √(k m)): below 1 the system oscillates, at 1 it is critically damped. A forcing frequency near the natural frequency gives resonance.
  - Needs: MEC-2.1.E
  - P1 · drills: mec-natural-frequency, mec-damping-ratio

## Unit 3 · Mechanics of materials

Big ideas: STRESS

### 3.1 Stress and deformation



- ● **MEC-3.1.A** (fe-mechanical:8C) Compute axial stress and elongation.
  - EK: Normal stress σ = P ÷ A. Within the elastic range the elongation is δ = P L ÷ (A E).
  - Needs: MEC-1.1.F
  - P1 · drills: mec-axial-stress, mec-elongation
- ● **MEC-3.1.B** (fe-mechanical:8G, fe-mechanical:8K) Compute thermal expansion and the stress in a constrained bar.
  - EK: A free bar changes length by δ = α ΔT L. If both ends are fixed the bar cannot expand, and the stress is σ = E α ΔT (compressive on heating), whatever its length or area.
  - Needs: MEC-3.1.A
  - P1 · drills: mec-thermal-expansion, mec-thermal-stress
- ● **MEC-3.1.C** (fe-mechanical:8E) Compute torsional shear stress and angle of twist in a solid shaft.
  - EK: Maximum shear stress τ = T c ÷ J with J = π d⁴ ÷ 32 for a solid circular shaft, so τ = 16 T ÷ (π d³). Angle of twist φ = T L ÷ (G J).
  - Needs: MEC-3.1.B
  - P1 · drills: mec-torsion-stress, mec-angle-of-twist
- ● **MEC-3.1.D** (fe-mechanical:8A) Find the maximum shear and bending moment in standard beams.
  - EK: Simply supported beam with a central point load P: maximum shear P ÷ 2, maximum moment P L ÷ 4. With a uniform load w: maximum shear w L ÷ 2, maximum moment w L² ÷ 8. A cantilever with an end load P: maximum moment P L at the wall.
  - Needs: MEC-3.1.C
  - P1 · drills: mec-max-moment-udl, mec-max-moment-point
- ● **MEC-3.1.E** (fe-mechanical:8D, fe-mechanical:8I) Compute bending stress and a standard beam deflection.
  - EK: Bending stress σ = M c ÷ I; for a rectangle b × h this is 6M ÷ (b h²). A simply supported beam with a central load deflects P L³ ÷ (48 E I) at midspan.
  - Needs: MEC-3.1.D
  - P1 · drills: mec-bending-stress, mec-midspan-deflection
- ● **MEC-3.1.F** (fe-mechanical:8B) Find principal stresses and the maximum in-plane shear stress.
  - EK: For plane stress the centre of Mohr's circle is (σx + σy) ÷ 2 and its radius is √(((σx − σy) ÷ 2)² + τxy²). The principal stresses are centre ± radius and the maximum in-plane shear stress is the radius.
  - Needs: MEC-3.1.E
  - P1 · drills: mec-principal-stress, mec-max-shear
- ● **MEC-3.1.G** (fe-mechanical:8H) Compute pressure-vessel stresses and combine axial and bending stress.
  - EK: A thin-walled cylinder under pressure p has hoop stress p r ÷ t and longitudinal stress p r ÷ (2t). Axial load and bending on the same section superpose: σ = P ÷ A ± M c ÷ I.
  - Needs: MEC-3.1.F
  - P1 · drills: mec-hoop-stress, mec-combined-stress
- ● **MEC-3.1.H** (fe-mechanical:8J) Compute an Euler buckling load and choose the effective length factor.
  - EK: Critical load P = π² E I ÷ (K L)². K is 1 for pinned-pinned ends, 0.5 for fixed-fixed, about 0.7 for fixed-pinned and 2 for fixed-free. Buckling depends on stiffness and slenderness, not on strength.
  - Needs: MEC-3.1.G
  - P1 · drills: mec-euler-buckling, mec-effective-length
