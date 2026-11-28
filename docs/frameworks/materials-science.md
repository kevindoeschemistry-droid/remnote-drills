# Materials Science and Engineering — curriculum framework (draft 1)

Generated from `drills/frameworks/materials-science.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**71 learning objectives** in 7 units (71 core): 71 drilled, 0 partly, 0 with no drills. Core: 71 / 71 drilled.

## Big ideas

- **LATTICE · Structure sets what can move.** Which planes are densest and which directions are shortest decide how a crystal slips, diffracts and packs; everything else is counted from the unit cell.
- **DEFECT · Properties live in the defects.** A perfect crystal would be a thousand times stronger and far less useful: vacancies carry diffusion, dislocations carry plastic flow, and every strengthening method is a way to pin a dislocation.
- **PATH · Processing chooses the microstructure.** The phase diagram says where equilibrium is; cooling rate, cold work and heat treatment decide how far the material gets there, and so which phases and grain sizes it ends with.

## Practices

- **P1 · Compute.** Carry a geometric, rate or mechanical relation to a number with its unit.
- **P2 · Classify.** Name the structure, defect, mechanism or technique a description points to.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Crystal structure | core | — | 10 | 10 | 0 | 0 |
| 2 · Defects and dislocations | core | — | 11 | 11 | 0 | 0 |
| 3 · Deformation and strengthening | core | — | 12 | 12 | 0 | 0 |
| 4 · Diffusion in solids | core | — | 4 | 4 | 0 | 0 |
| 5 · Phase diagrams and transformations | core | — | 11 | 11 | 0 | 0 |
| 6 · Failure | core | — | 6 | 6 | 0 | 0 |
| 7 · Material classes and characterisation | core | — | 17 | 17 | 0 | 0 |

## Unit 1 · Crystal structure

Big ideas: LATTICE

### 1.1 Unit cells



- ● **MSE-1.1.A** (engineers-canada-materials:A3.1) Count the atoms in a cubic unit cell and state its coordination number.
  - EK: A corner atom is shared by 8 cells, a face atom by 2, a body atom by 1. FCC holds 4 atoms with 12 nearest neighbours; BCC holds 2 with 8; simple cubic holds 1 with 6.
  - Needs: CH-3.2.A
  - P1 · drills: mse-cell-facts, mse-cell-count
- ● **MSE-1.1.B** (engineers-canada-materials:A3.1) Relate the cell edge to the atomic radius in FCC and BCC.
  - EK: Atoms touch along the face diagonal in FCC, so a√2 = 4r; along the body diagonal in BCC, so a√3 = 4r.
  - Needs: MSE-1.1.A
  - P1 · drills: mse-edge-from-radius, mse-radius-from-edge
- ● **MSE-1.1.C** (engineers-canada-materials:A3.1) Compute an atomic packing factor.
  - EK: APF is the volume of the atoms in the cell over the cell volume: 0.74 for FCC and HCP, 0.68 for BCC, 0.52 for simple cubic.
  - Needs: MSE-1.1.B
  - P1 · drills: mse-apf, mse-apf-facts
- ● **MSE-1.1.D** (engineers-canada-materials:A3.1, fe-mechanical:9A) Compute a theoretical density from the unit cell.
  - EK: ρ = nA ÷ (V_cell N_A): atoms per cell times molar mass, over cell volume times Avogadro's number. With a in nm, a³ in cm³ is (a × 10⁻⁷)³.
  - Needs: MSE-1.1.C
  - P1 · drills: mse-density, mse-molar-mass-from-cell

### 1.2 Directions, planes and diffraction



- ● **MSE-1.2.A** (engineers-canada-materials:A3.1) Write the Miller indices of a plane from its intercepts and test whether a direction lies in a plane.
  - EK: Take the intercepts in units of the cell edges, invert, and clear fractions; a plane parallel to an axis has index 0 for it. In a cubic crystal [uvw] lies in (hkl) when hu + kv + lw = 0.
  - Needs: MSE-1.1.D
  - P2 · drills: mse-miller-plane, mse-direction-in-plane
- ● **MSE-1.2.B** (engineers-canada-materials:A3.1) Write a direction's indices and find the angle between two directions.
  - EK: A direction is the vector between two lattice points reduced to smallest integers. In a cubic crystal the angle between [u₁v₁w₁] and [u₂v₂w₂] comes from the dot product.
  - Needs: MSE-1.2.A
  - P1 · drills: mse-direction-angle, mse-direction-indices
- ● **MSE-1.2.C** (engineers-canada-materials:A3.1, engineers-canada-materials:A3.2) Compute the spacing of (hkl) planes in a cubic crystal.
  - EK: d = a ÷ √(h² + k² + l²). Low-index planes are the most widely spaced and the most densely packed.
  - Needs: MSE-1.2.B
  - P1 · drills: mse-d-spacing, mse-edge-from-spacing
- ● **MSE-1.2.D** (engineers-canada-materials:A3.2) Use Bragg's law.
  - EK: nλ = 2d sin θ. A diffractometer reports 2θ, the angle between the incident and diffracted beams.
  - Needs: MSE-1.2.C
  - P1 · drills: mse-bragg-angle, mse-bragg-spacing
- ● **MSE-1.2.E** (engineers-canada-materials:A3.2) Decide which reflections a cubic structure allows.
  - EK: BCC reflects only when h + k + l is even; FCC only when h, k and l are all odd or all even; simple cubic reflects for every plane.
  - Needs: MSE-1.2.D
  - P2 · drills: mse-reflection-allowed, mse-first-peaks
- ● **MSE-1.2.F** (engineers-canada-materials:A3.1) Compute a linear and a planar density.
  - EK: Linear density is atom centres per length along a direction; planar density is atoms per area on a plane. Slip prefers the densest directions on the densest planes.
  - Needs: MSE-1.2.E
  - P1 · drills: mse-linear-density, mse-planar-density

## Unit 2 · Defects and dislocations

Big ideas: DEFECT

### 2.1 Point defects and solid solutions



- ● **MSE-2.1.A** (engineers-canada-materials:A4.1, engineers-canada-materials:A5.4) Compute an equilibrium vacancy concentration.
  - EK: N_v ÷ N = exp(−Q_v ÷ kT), with k = 8.617 × 10⁻⁵ eV/K. Near melting about one site in ten thousand is vacant.
  - Needs: MSE-1.2.F
  - P1 · drills: mse-vacancy-fraction, mse-vacancy-energy
- ● **MSE-2.1.B** (engineers-canada-materials:A4.2) Tell substitutional from interstitial solid solutions and apply the size rule.
  - EK: A solute sits on host sites when its radius is within about 15% of the host's and the structures, valences and electronegativities are alike; a much smaller atom (C, N, H) sits between host atoms.
  - Needs: MSE-2.1.A
  - P2 · drills: mse-solution-type, mse-size-mismatch
- ● **MSE-2.1.C** (engineers-canada-materials:A4.2, fe-mechanical:9A) Convert a composition between weight percent and atom percent.
  - EK: Divide each weight percent by its molar mass to get moles, then normalise; multiply atom percents by molar mass and normalise to go back.
  - Needs: MSE-2.1.B
  - P1 · drills: mse-wt-to-at, mse-at-to-wt
- ● **MSE-2.1.D** (engineers-canada-materials:B6.2) Identify Schottky and Frenkel defects and the vacancies a dopant forces in an ionic crystal.
  - EK: A Schottky defect is a cation vacancy with an anion vacancy; a Frenkel defect is a cation moved to an interstitial site. Both keep the crystal neutral, and an impurity of different charge brings compensating vacancies.
  - Needs: MSE-2.1.C
  - P2 · drills: mse-ionic-defects, mse-dopant-vacancy

### 2.2 Dislocations and the Burgers vector



- ● **MSE-2.2.A** (engineers-canada-materials:A4.1) Tell edge, screw and mixed dislocations apart by the Burgers vector and the line.
  - EK: The Burgers vector b is the lattice displacement a dislocation carries. Edge: b perpendicular to the line (an extra half-plane). Screw: b parallel to the line (a spiral ramp). Anything between is mixed.
  - Needs: MSE-2.1.D
  - P2 · drills: mse-dislocation-facts, mse-dislocation-character
- ● **MSE-2.2.B** (engineers-canada-materials:A4.1) Find a Burgers vector from a Burgers circuit.
  - EK: Walk a closed loop of lattice steps around the line, equal steps in opposite directions. In perfect crystal the loop closes; around a dislocation it does not, and the vector needed to close it is b.
  - Needs: MSE-2.2.A
  - P1 · drills: mse-burgers-circuit, mse-burgers-circuit-facts
- ● **MSE-2.2.C** (engineers-canada-materials:A4.1) Compute the magnitude of a Burgers vector from its indices.
  - EK: A perfect dislocation's b joins nearest neighbours: (a/2)⟨110⟩ in FCC, (a/2)⟨111⟩ in BCC. Its length is (a/2)√(h² + k² + l²), which equals two atomic radii.
  - Needs: MSE-2.2.B
  - P1 · drills: mse-burgers-magnitude, mse-burgers-from-radius
- ● **MSE-2.2.D** (engineers-canada-materials:A4.1, engineers-canada-materials:A4.2) Use the b² rule for a dislocation's energy and for dislocation reactions.
  - EK: The elastic energy per length of a dislocation is about ½Gb². A reaction b₁ → b₂ + b₃ is favourable when b₁² > b₂² + b₃² (Frank's rule), which is why dislocations take the shortest lattice vector.
  - Needs: MSE-2.2.C
  - P1 · drills: mse-dislocation-energy, mse-frank-rule
- ● **MSE-2.2.E** (engineers-canada-materials:A4.1) Work with a dislocation density.
  - EK: Density ρ is line length per volume, in m⁻²: about 10¹⁰ in an annealed metal, 10¹⁴ to 10¹⁶ after heavy cold work. The mean spacing between dislocations is about 1 ÷ √ρ.
  - Needs: MSE-2.2.D
  - P1 · drills: mse-dislocation-spacing, mse-dislocation-length

### 2.3 Grain boundaries and planar defects



- ● **MSE-2.3.A** (engineers-canada-materials:A3.3, engineers-canada-materials:A4.2) Convert between ASTM grain size number and grain count.
  - EK: N = 2^(G − 1): N grains per square inch at 100× magnification for ASTM grain size number G. A larger G means finer grains.
  - Needs: MSE-2.2.E
  - P1 · drills: mse-astm-grains, mse-astm-number
- ● **MSE-2.3.B** (engineers-canada-materials:A4.2) Identify low-angle boundaries, twins and stacking faults.
  - EK: A low-angle tilt boundary is a wall of edge dislocations of spacing D with misorientation θ ≈ b ÷ D. A twin boundary is a mirror plane; a stacking fault is a mistake in the ABCABC sequence.
  - Needs: MSE-2.3.A
  - P1 · drills: mse-tilt-angle, mse-planar-defects

## Unit 3 · Deformation and strengthening

Big ideas: DEFECT

### 3.1 Slip



- ● **MSE-3.1.A** (engineers-canada-materials:A4.1) Name the slip systems of FCC, BCC and HCP metals.
  - EK: Slip runs on the most densely packed planes along the closest-packed directions: (111) planes and 110-type directions in FCC (12 systems), 111-type directions in BCC, the basal plane in HCP (3 systems).
  - Needs: MSE-2.3.B, MEC-3.1.H
  - P2 · drills: mse-slip-systems, mse-slip-count
- ● **MSE-3.1.B** (engineers-canada-materials:A4.1) Apply Schmid's law.
  - EK: τ_R = σ cos φ cos λ, with φ between the load axis and the slip-plane normal and λ between the load axis and the slip direction. Slip starts when τ_R reaches the critical resolved shear stress; the factor cannot exceed 0.5.
  - Needs: MSE-3.1.A
  - P1 · drills: mse-schmid-stress, mse-schmid-yield
- ● **MSE-3.1.C** (engineers-canada-materials:A4.1) Compare theoretical and observed shear strength.
  - EK: Shearing a whole plane at once would take about G ÷ 2π. Real crystals yield at a thousandth of that because a dislocation moves the slip one row at a time.
  - Needs: MSE-3.1.B
  - P1 · drills: mse-theoretical-strength, mse-why-weak

### 3.2 Strengthening mechanisms



- ● **MSE-3.2.A** (engineers-canada-materials:A4.2) Use the Hall-Petch relation.
  - EK: σ_y = σ₀ + k_y d^(−1/2): a grain boundary stops a dislocation, so finer grains give higher yield strength.
  - Needs: MSE-3.1.C
  - P1 · drills: mse-hall-petch, mse-hall-petch-constant
- ● **MSE-3.2.B** (engineers-canada-materials:A4.2) Compute percent cold work and the strength from dislocation density.
  - EK: %CW = (A₀ − A_d) ÷ A₀ × 100. Work hardening follows τ = αGb√ρ with α about 0.5: flow stress rises as the square root of dislocation density.
  - Needs: MSE-3.2.A
  - P1 · drills: mse-cold-work, mse-taylor-hardening
- ● **MSE-3.2.C** (engineers-canada-materials:A4.2) Explain solid-solution and precipitation strengthening and use the Orowan stress.
  - EK: Solute atoms strain the lattice and drag on dislocations. Fine coherent precipitates are cut; larger ones are bypassed by bowing between them at τ = Gb ÷ L, so strength peaks at an intermediate ageing time and falls on overageing.
  - Needs: MSE-3.2.B
  - P1 · drills: mse-orowan, mse-precipitation-facts
- ● **MSE-3.2.D** (engineers-canada-materials:A5.2, fe-mechanical:9G) Order recovery, recrystallization and grain growth.
  - EK: On annealing a cold-worked metal: recovery rearranges dislocations and relieves stress with little change in strength; recrystallization replaces the worked grains with new strain-free ones and restores ductility; grain growth then coarsens them.
  - Needs: MSE-3.2.C
  - P2 · drills: mse-anneal-stage, mse-recrystallization-facts

### 3.3 The tensile test



- ● **MSE-3.3.A** (engineers-canada-materials:A4.1, fe-mechanical:9B) Read ductility and plastic strain from a tensile test.
  - EK: Percent elongation is (l_f − l₀) ÷ l₀ × 100. On unloading, the elastic strain σ ÷ E is recovered along a line parallel to the elastic slope, leaving the plastic strain.
  - Needs: MSE-3.2.D
  - P1 · drills: mse-elongation, mse-plastic-strain
- ● **MSE-3.3.B** (engineers-canada-materials:A4.1, fe-mechanical:9B) Convert engineering stress and strain to true stress and strain.
  - EK: σ_T = σ(1 + ε) and ε_T = ln(1 + ε) = ln(l ÷ l₀), valid up to necking. True strain adds up the increments dl ÷ l.
  - Needs: MSE-3.3.A
  - P1 · drills: mse-true-stress, mse-true-strain
- ● **MSE-3.3.C** (engineers-canada-materials:A4.1, fe-mechanical:9B) Use the strain-hardening law.
  - EK: In the plastic range σ_T = K ε_T^n. The exponent n runs from about 0.1 to 0.5, and necking begins when the true strain equals n.
  - Needs: MSE-3.3.B
  - P1 · drills: mse-hardening-stress, mse-hardening-exponent
- ● **MSE-3.3.D** (engineers-canada-materials:A4.1, fe-mechanical:9A, fe-mechanical:9B) Compute the modulus of resilience and tell it from toughness.
  - EK: Resilience is the elastic energy per volume up to yield, U_r = σ_y² ÷ 2E; toughness is the whole area under the stress-strain curve to fracture.
  - Needs: MSE-3.3.C
  - P1 · drills: mse-resilience, mse-toughness-facts
- ● **MSE-3.3.E** (fe-mechanical:9A, engineers-canada-materials:A4.1) Relate hardness to strength and name the hardness tests.
  - EK: Hardness is resistance to local plastic indentation. For steels, tensile strength in MPa is about 3.45 times the Brinell number.
  - Needs: MSE-3.3.D
  - P1 · drills: mse-hardness-strength, mse-hardness-tests

## Unit 4 · Diffusion in solids

Big ideas: DEFECT

### 4.1 Rates of diffusion



- ● **MSE-4.1.A** (engineers-canada-materials:A5.4) Apply Fick's first law to steady diffusion through a plate.
  - EK: J = −D dC/dx: flux runs down the concentration gradient. For a linear profile J = D ΔC ÷ Δx.
  - Needs: MSE-2.3.B, CH-5.5.A
  - P1 · drills: mse-fick-flux, mse-fick-thickness
- ● **MSE-4.1.B** (engineers-canada-materials:A5.4) Use the Arrhenius law for a diffusion coefficient.
  - EK: D = D₀ exp(−Q_d ÷ RT). A plot of ln D against 1 ÷ T is a line of slope −Q_d ÷ R.
  - Needs: MSE-4.1.A
  - P1 · drills: mse-diffusivity, mse-diffusion-activation
- ● **MSE-4.1.C** (engineers-canada-materials:A5.4) Scale a diffusion depth with time and temperature.
  - EK: For a fixed surface concentration, a given composition is reached at a depth proportional to √(Dt). The same profile results whenever the product Dt is the same.
  - Needs: MSE-4.1.B
  - P1 · drills: mse-diffusion-time, mse-equal-dt
- ● **MSE-4.1.D** (engineers-canada-materials:A5.4) Compare diffusion mechanisms and paths.
  - EK: Interstitial atoms diffuse faster than substitutional ones, which must wait for a vacancy. Grain boundaries and surfaces are faster paths than the lattice; open structures and low melting points give faster diffusion.
  - Needs: MSE-4.1.C
  - P2 · drills: mse-diffusion-faster, mse-diffusion-mechanism

## Unit 5 · Phase diagrams and transformations

Big ideas: PATH

### 5.1 Binary phase diagrams



- ● **MSE-5.1.A** (engineers-canada-materials:A5.1, fe-mechanical:9G) Apply the Gibbs phase rule at constant pressure.
  - EK: F = C − P + 1 when pressure is fixed. In a binary system a two-phase field has one degree of freedom and a three-phase reaction (eutectic, eutectoid, peritectic) has none: it happens at one temperature.
  - Needs: MSE-4.1.D
  - P1 · drills: mse-phase-rule, mse-phase-rule-meaning
- ● **MSE-5.1.B** (engineers-canada-materials:A5.1, fe-mechanical:9G) Use the lever rule.
  - EK: In a two-phase field the phase compositions are the ends of the tie line, and the fraction of one phase is the opposite lever arm over the whole tie line.
  - Needs: MSE-5.1.A
  - P1 · drills: mse-lever-rule, mse-lever-composition
- ● **MSE-5.1.C** (engineers-canada-materials:A5.1) Split a hypoeutectic alloy into primary phase and eutectic.
  - EK: Just above the eutectic temperature the liquid has the eutectic composition; all of it becomes eutectic microconstituent. The primary phase fraction is a lever between the solubility limit and the eutectic point.
  - Needs: MSE-5.1.B
  - P1 · drills: mse-primary-alpha, mse-eutectic-alpha
- ● **MSE-5.1.D** (engineers-canada-materials:A5.1, fe-mechanical:9G) Name the invariant reactions.
  - EK: On cooling: eutectic, liquid → two solids; eutectoid, one solid → two solids; peritectic, liquid + solid → a different solid.
  - Needs: MSE-5.1.C
  - P2 · drills: mse-invariant-name, mse-diagram-facts

### 5.2 Steel and heat treatment



- ● **MSE-5.2.A** (engineers-canada-materials:A5.1, fe-mechanical:9C) Identify the phases and landmarks of the iron-carbon diagram.
  - EK: Ferrite (α) is BCC and holds at most 0.022 wt% C; austenite (γ) is FCC and holds up to 2.14; cementite Fe₃C is 6.70 wt% C. The eutectoid is 0.76 wt% C at 727 °C; steels lie below 2.14 wt% C, cast irons above.
  - Needs: MSE-5.1.D
  - P2 · drills: mse-fe-c-facts, mse-steel-class
- ● **MSE-5.2.B** (engineers-canada-materials:A5.1, fe-mechanical:9C, fe-mechanical:9G) Compute the microconstituents of a slowly cooled steel.
  - EK: In a hypoeutectoid steel the austenite left at 727 °C has 0.76 wt% C and becomes pearlite, so pearlite is a lever between 0.022 and 0.76. Total cementite is a lever between 0.022 and 6.70.
  - Needs: MSE-5.2.A
  - P1 · drills: mse-pearlite-fraction, mse-cementite-fraction
- ● **MSE-5.2.C** (engineers-canada-materials:A5.7, fe-mechanical:9G) Predict the product of an isothermal or quench treatment from a TTT diagram.
  - EK: Austenite held just below 727 °C gives coarse pearlite, lower gives fine pearlite, below the nose (about 550 to 250 °C) bainite; quenched fast enough to miss the nose it shears to martensite, which is hard, brittle and not on the equilibrium diagram.
  - Needs: MSE-5.2.B
  - P2 · drills: mse-ttt-product, mse-martensite-facts
- ● **MSE-5.2.D** (engineers-canada-materials:A5.2, fe-mechanical:9G) Choose a heat treatment for steel and explain hardenability.
  - EK: Full annealing (furnace cool) gives the softest structure; normalizing (air cool) a finer, stronger one; quench and temper gives the best strength with toughness. Hardenability is the depth to which a steel forms martensite, measured by the Jominy end-quench test and raised by alloying.
  - Needs: MSE-5.2.C
  - P2 · drills: mse-heat-treatment, mse-hardenability-facts
- ● **MSE-5.2.E** (engineers-canada-materials:A5.3, engineers-canada-materials:A5.5) Use the Avrami equation for the fraction transformed.
  - EK: y = 1 − exp(−k tⁿ): the S-shaped curve of nucleation and growth. The rate is often quoted as 1 ÷ t at half transformation.
  - Needs: MSE-5.2.D
  - P1 · drills: mse-avrami-fraction, mse-avrami-half-time

### 5.3 Nucleation and glass



- ● **MSE-5.3.A** (engineers-canada-materials:A5.5) Compute a critical nucleus radius and scale the nucleation barrier.
  - EK: A solid nucleus gains volume free energy and pays surface energy: r* = 2γT_m ÷ (ΔH_f ΔT) and ΔG* varies as 1 ÷ ΔT². Larger undercooling means smaller nuclei and a lower barrier.
  - Needs: MSE-5.2.E
  - P1 · drills: mse-critical-radius, mse-nucleation-barrier
- ● **MSE-5.3.B** (engineers-canada-materials:A5.6) Tell a glass transition from melting.
  - EK: A crystal melts sharply at T_m. An amorphous solid has no T_m: it softens over the glass transition T_g, where the slope of volume against temperature changes. A semicrystalline polymer shows both.
  - Needs: MSE-5.3.A
  - P2 · drills: mse-tg-or-tm, mse-glass-facts

## Unit 6 · Failure

Big ideas: DEFECT

### 6.1 Fracture, fatigue and creep



- ● **MSE-6.1.A** (engineers-canada-materials:A4.4, fe-mechanical:9J) Use fracture toughness to find a critical stress or flaw size.
  - EK: K = Yσ√(πa); fracture when K reaches K_IC. For a surface crack a is the depth, for an internal crack half the length.
  - Needs: MSE-3.3.E
  - P1 · drills: mse-critical-stress, mse-critical-flaw
- ● **MSE-6.1.B** (engineers-canada-materials:A4.3, engineers-canada-materials:A4.4) Apply the Griffith criterion and tell ductile from brittle fracture.
  - EK: A brittle crack grows when the elastic energy released pays for the new surface: σ_c = √(2Eγ_s ÷ πa). Ductile fracture absorbs far more energy through plastic flow (cup and cone); BCC metals turn brittle below a transition temperature.
  - Needs: MSE-6.1.A
  - P1 · drills: mse-griffith, mse-fracture-mode
- ● **MSE-6.1.C** (engineers-canada-materials:A4.4, fe-mechanical:9J) Compute the stress at the tip of a flaw.
  - EK: σ_m = 2σ₀√(a ÷ ρ_t): the maximum stress at a crack of length a and tip radius ρ_t. Sharp cracks concentrate stress; drilling a hole at the tip blunts it.
  - Needs: MSE-6.1.B
  - P1 · drills: mse-tip-stress, mse-tip-radius
- ● **MSE-6.1.D** (engineers-canada-materials:A4.6, fe-mechanical:9J) Describe a fatigue cycle and read an S-N curve.
  - EK: σ_m = (σ_max + σ_min) ÷ 2, σ_a = (σ_max − σ_min) ÷ 2, R = σ_min ÷ σ_max. Steels and titanium alloys have a fatigue limit below which life is unlimited; aluminium, copper and magnesium do not.
  - Needs: MSE-6.1.C
  - P1 · drills: mse-fatigue-amplitude, mse-fatigue-limit
- ● **MSE-6.1.E** (engineers-canada-materials:A4.6) Use the Paris law for fatigue crack growth.
  - EK: da/dN = A(ΔK)^m with ΔK = YΔσ√(πa) and m about 2 to 4 for metals. Life is the integral of dN from the initial to the critical crack length.
  - Needs: MSE-6.1.D
  - P1 · drills: mse-paris-ratio, mse-paris-life
- ● **MSE-6.1.F** (engineers-canada-materials:A4.5, fe-mechanical:9J) Work with steady-state creep and the Larson-Miller parameter.
  - EK: Steady creep rate goes as σⁿ exp(−Q_c ÷ RT); creep matters above about 0.4 of the absolute melting temperature. The Larson-Miller parameter T(C + log t_r), with C about 20 and t_r in hours, trades temperature against rupture life.
  - Needs: MSE-6.1.E
  - P1 · drills: mse-larson-miller, mse-creep-exponent

## Unit 7 · Material classes and characterisation

Big ideas: LATTICE, PATH

### 7.1 Ceramics



- ● **MSE-7.1.A** (engineers-canada-materials:B6.1) Predict a ceramic's coordination from the radius ratio and name the common structures.
  - EK: The cation takes as many anion neighbours as can touch it: r_C ÷ r_A of 0.225 to 0.414 gives tetrahedral (4), 0.414 to 0.732 octahedral (6), 0.732 to 1.0 cubic (8).
  - Needs: MSE-1.2.F, MSE-3.3.E
  - P2 · drills: mse-radius-ratio, mse-ceramic-structures
- ● **MSE-7.1.B** (engineers-canada-materials:B6.1) Compute a ceramic's density and cell edge from its ions.
  - EK: ρ = n′(ΣA_C + ΣA_A) ÷ (V_cell N_A), with n′ formula units per cell. In rock salt the ions touch along the cell edge, so a = 2(r_C + r_A).
  - Needs: MSE-7.1.A
  - P1 · drills: mse-ceramic-density, mse-rock-salt-edge
- ● **MSE-7.1.C** (engineers-canada-materials:B6.3, fe-mechanical:9A) Compute a flexural strength from a three-point bend test.
  - EK: Ceramics are tested in bending because they are hard to grip in tension. For a rectangular bar σ_fs = 3FL ÷ 2bd², with L the support span.
  - Needs: MSE-7.1.B
  - P1 · drills: mse-flexural-strength, mse-flexural-load
- ● **MSE-7.1.D** (engineers-canada-materials:B6.4, engineers-canada-materials:A4.7) Compute a thermal stress and a thermal shock limit.
  - EK: A constrained body heated or cooled by ΔT carries σ = EαΔT. A brittle solid survives a sudden temperature change of about σ_f ÷ Eα, so low expansion and high conductivity resist thermal shock.
  - Needs: MSE-7.1.C
  - P1 · drills: mse-thermal-stress, mse-thermal-shock

### 7.2 Composites



- ● **MSE-7.2.A** (engineers-canada-materials:B11.1, fe-mechanical:9E) Compute a continuous-fibre composite's modulus along the fibres.
  - EK: Loaded along the fibres, fibre and matrix strain equally (isostrain): E_c = E_m V_m + E_f V_f, the upper bound.
  - Needs: MSE-7.1.D
  - P1 · drills: mse-isostrain-modulus, mse-fibre-fraction
- ● **MSE-7.2.B** (engineers-canada-materials:B11.1, fe-mechanical:9E) Compute the transverse modulus and say which loading gives which bound.
  - EK: Loaded across the fibres, fibre and matrix carry equal stress (isostress): 1 ÷ E_c = V_m ÷ E_m + V_f ÷ E_f, the lower bound, dominated by the soft matrix.
  - Needs: MSE-7.2.A
  - P1 · drills: mse-isostress-modulus, mse-composite-bound
- ● **MSE-7.2.C** (engineers-canada-materials:B11.1, engineers-canada-materials:B11.2, fe-mechanical:9E) Compute the load carried by the fibres and the critical fibre length.
  - EK: Under isostrain F_f ÷ F_m = E_f V_f ÷ E_m V_m. A fibre reaches its full strength only if it is longer than l_c = σ_f d ÷ 2τ_c, with τ_c the fibre-matrix bond strength.
  - Needs: MSE-7.2.B
  - P1 · drills: mse-fibre-load-share, mse-critical-length

### 7.3 Electronic and magnetic behaviour



- ● **MSE-7.3.A** (engineers-canada-materials:A4.8, engineers-canada-materials:B8.1) Compute a conductivity from carrier density and mobility.
  - EK: σ = n|e|μ, with e = 1.602 × 10⁻¹⁹ C. Metals have about one free electron per atom or more; their mobility, not their carrier count, falls on heating or alloying.
  - Needs: MSE-7.2.C
  - P1 · drills: mse-conductivity, mse-mobility
- ● **MSE-7.3.B** (engineers-canada-materials:B8.1, engineers-canada-materials:B8.2) Classify a solid by its band gap and compute an intrinsic conductivity.
  - EK: Metals have a partly filled band or overlapping bands; semiconductors a gap under about 2 eV; insulators a wider one. An intrinsic semiconductor has equal electrons and holes: σ = n_i|e|(μ_e + μ_h).
  - Needs: MSE-7.3.A
  - P1 · drills: mse-intrinsic-conductivity, mse-band-class
- ● **MSE-7.3.C** (engineers-canada-materials:B8.2) Predict the carrier type a dopant gives.
  - EK: In silicon or germanium a group 15 atom (P, As, Sb) donates an electron: n-type. A group 13 atom (B, Al, Ga, In) accepts one and leaves a hole: p-type.
  - Needs: MSE-7.3.B
  - P2 · drills: mse-dopant-type, mse-extrinsic-facts
- ● **MSE-7.3.D** (engineers-canada-materials:B8.3) Classify magnetic behaviour and state what a superconductor does.
  - EK: Diamagnets weakly oppose a field; paramagnets weakly align with it; ferromagnets (Fe, Co, Ni) align strongly and stay magnetised below the Curie temperature. Below T_c a superconductor has zero resistance and expels magnetic flux.
  - Needs: MSE-7.3.C
  - P2 · drills: mse-magnetic-class, mse-magnet-facts

### 7.4 Alloys and processing



- ● **MSE-7.4.A** (fe-mechanical:9C) Read a steel designation and tell the classes of ferrous alloy apart.
  - EK: In AISI/SAE four-digit steels the last two digits are carbon in hundredths of a weight percent: 1040 is plain carbon with 0.40% C. Stainless steels need at least about 11% Cr. Gray iron has graphite flakes, ductile iron spheroids.
  - Needs: MSE-7.3.D
  - P2 · drills: mse-steel-designation, mse-carbon-class
- ● **MSE-7.4.B** (fe-mechanical:9D) Identify the common nonferrous alloys and how they are strengthened.
  - EK: Brass is Cu-Zn, bronze Cu-Sn. Aluminium tempers: T means solution treated and aged, H strain hardened, O annealed. Titanium alloys give the best strength to weight; nickel superalloys keep strength hot.
  - Needs: MSE-7.4.A
  - P2 · drills: mse-nonferrous-facts, mse-temper
- ● **MSE-7.4.C** (fe-mechanical:9F) Match a manufacturing process to what it does to the metal.
  - EK: Casting fills a mould with liquid; forging, rolling, extrusion and drawing shape the solid, hot (above recrystallization, no hardening) or cold (strain hardened, better finish); powder metallurgy presses and sinters powder; welding leaves a heat-affected zone.
  - Needs: MSE-7.4.B
  - P2 · drills: mse-hot-or-cold, mse-process-facts

### 7.5 Characterisation



- ● **MSE-7.5.A** (engineers-canada-materials:A3.2) Choose between XRD, EDS and XPS.
  - EK: X-ray diffraction gives crystal structure, phases and lattice parameters. EDS in an electron microscope gives elemental composition from characteristic X-rays. XPS gives the composition and chemical state of the top few nanometres.
  - Needs: MSE-7.4.C
  - P2 · drills: mse-analysis-choice, mse-analysis-facts
- ● **MSE-7.5.B** (engineers-canada-materials:A3.3) Choose between optical, scanning and transmission electron microscopy.
  - EK: Optical microscopes resolve about 0.2 µm and show grains on a polished, etched surface. SEM resolves nanometres with great depth of field on bulk samples. TEM passes electrons through a thin foil and images dislocations and lattice planes.
  - Needs: MSE-7.5.A
  - P2 · drills: mse-microscope-choice, mse-microscopy-facts
- ● **MSE-7.5.C** (engineers-canada-materials:A3.4) Choose between DSC and TGA and read what each shows.
  - EK: DSC (and DTA) record heat flow against temperature: glass transitions, melting, crystallisation, heats of reaction. TGA records mass against temperature: drying, decomposition, oxidation, filler content.
  - Needs: MSE-7.5.B
  - P2 · drills: mse-thermal-choice, mse-thermal-facts
