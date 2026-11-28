# Materials Science and Engineering — curriculum framework (draft 1)

Generated from `drills/frameworks/materials-science.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**144 learning objectives** in 14 units (144 core): 144 drilled, 0 partly, 0 with no drills. Core: 144 / 144 drilled.

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
| 8 · Thermodynamics and transport in processing | core | — | 9 | 9 | 0 | 0 |
| 9 · Selection and degradation | core | — | 13 | 13 | 0 | 0 |
| 10 · Polymer structure and properties | core | — | 9 | 9 | 0 | 0 |
| 11 · Extraction and refining | core | — | 11 | 11 | 0 | 0 |
| 12 · Fabrication | core | — | 10 | 10 | 0 | 0 |
| 13 · Functional materials and microfabrication | core | — | 14 | 14 | 0 | 0 |
| 14 · Composites and service practice | core | — | 7 | 7 | 0 | 0 |

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

## Unit 8 · Thermodynamics and transport in processing

Big ideas: PATH

### 8.1 Thermochemistry of processes



- ● **MSE-8.1.A** (engineers-canada-materials:A1.2, engineers-canada-materials:A1.6) Run a heat balance for heating and melting a charge.
  - EK: Q = m[c_p(T_m − T₀) + L_f]: sensible heat to the melting point plus latent heat. Furnace energy is this divided by the thermal efficiency.
  - Needs: MSE-5.3.B, CH-6.4.C
  - P1 · drills: mse-melt-heat, mse-melt-energy
- ● **MSE-8.1.B** (engineers-canada-materials:A1.3) Compute a standard free energy of oxidation and where it changes sign.
  - EK: ΔG° = ΔH° − TΔS°. On an Ellingham diagram this is a line of slope −ΔS°; an oxide decomposes on heating above the temperature where its line crosses zero.
  - Needs: MSE-8.1.A
  - P1 · drills: mse-ellingham-dg, mse-ellingham-zero
- ● **MSE-8.1.C** (engineers-canada-materials:A1.3, engineers-canada-materials:A1.6) Decide from free energies of formation whether one metal reduces another's oxide.
  - EK: Compare the oxides per mole of O₂: the element whose oxide has the more negative ΔG° takes the oxygen. Carbon's line to CO slopes downward, so carbon reduces more oxides the hotter it gets.
  - Needs: MSE-8.1.B
  - P1 · drills: mse-reduction-dg, mse-reduction-feasible
- ● **MSE-8.1.D** (engineers-canada-materials:A1.4) Compute the entropy and enthalpy of mixing of a binary solution.
  - EK: Ideal mixing: ΔS = −R(x ln x + (1 − x) ln(1 − x)), largest at x = 0.5. A regular solution adds ΔH = Ωx(1 − x): positive Ω means like atoms prefer each other.
  - Needs: MSE-8.1.C
  - P1 · drills: mse-mixing-entropy, mse-regular-enthalpy
- ● **MSE-8.1.E** (engineers-canada-materials:A1.4, engineers-canada-materials:A1.5) Link a solution model to the shape of the phase diagram.
  - EK: Phases in equilibrium share a common tangent to their free-energy curves. A regular solution with Ω > 2RT has a double-welled curve and separates into two phases; the miscibility gap closes at T_c = Ω ÷ 2R.
  - Needs: MSE-8.1.D
  - P1 · drills: mse-miscibility-tc, mse-miscibility-gap

### 8.2 Heat and flow in processing



- ● **MSE-8.2.A** (engineers-canada-materials:A2.1, pe-metmat:3B) Estimate a casting's solidification time with Chvorinov's rule.
  - EK: t = B(V ÷ A)²: freezing time goes as the square of the volume-to-surface ratio (the casting modulus). A riser must have a larger modulus than the section it feeds.
  - Needs: MSE-8.1.E
  - P1 · drills: mse-chvorinov, mse-chvorinov-ratio
- ● **MSE-8.2.B** (engineers-canada-materials:A2.3) Compute radiant heat loss from a hot surface.
  - EK: q = εσA(T⁴ − T_s⁴), with σ = 5.670 × 10⁻⁸ W/m²·K⁴. Because of the fourth power, radiation dominates the heat loss of hot metal.
  - Needs: MSE-8.2.A
  - P1 · drills: mse-radiation-loss, mse-radiation-ratio
- ● **MSE-8.2.C** (engineers-canada-materials:A2.2, engineers-canada-materials:B9.1) Use residence time for a ladle or tundish.
  - EK: Mean residence time τ = V ÷ Q. In a well-mixed vessel a step change washes out as exp(−t ÷ τ); plug flow would deliver it all at once after τ.
  - Needs: MSE-8.2.B
  - P1 · drills: mse-residence-time, mse-washout
- ● **MSE-8.2.D** (engineers-canada-materials:A2.1, engineers-canada-materials:A2.4, engineers-canada-materials:B9.1) Use the Biot number to choose a quench model.
  - EK: Bi = hL_c ÷ k compares surface convection with conduction inside. Below about 0.1 the part is nearly uniform and a lumped model works; above it, the inside lags and a conduction solution is needed.
  - Needs: MSE-8.2.C
  - P1 · drills: mse-biot, mse-lumped-valid

## Unit 9 · Selection and degradation

Big ideas: PATH

### 9.1 Selecting a material



- ● **MSE-9.1.A** (engineers-canada-materials:A6.1, engineers-canada-materials:A6.3, fe-mechanical:9H, pe-metmat:2I) Choose and compute a material index for a light, stiff or strong part.
  - EK: Translate the design: function, constraint, objective, free variable. A light stiff tie maximises E ÷ ρ, a beam E^½ ÷ ρ, a panel E^⅓ ÷ ρ; a light strong tie σ_y ÷ ρ.
  - Needs: MSE-6.1.F, MSE-7.5.C, CH-9.8.B
  - P1 · drills: mse-beam-index, mse-index-choice
- ● **MSE-9.1.B** (engineers-canada-materials:A6.3, pe-metmat:2I) Compare two materials by index and read a selection chart.
  - EK: For a tie of fixed stiffness the mass goes as ρ ÷ E. On a log-log property chart, materials on a line of slope set by the index perform equally; those above it are better.
  - Needs: MSE-9.1.A
  - P1 · drills: mse-tie-mass-ratio, mse-chart-facts
- ● **MSE-9.1.C** (engineers-canada-materials:A6.2) Compute a shape factor and say what limits it.
  - EK: Shape puts material far from the neutral axis. The elastic bending shape factor φ = 4πI ÷ A² is 1 for a solid round bar; for a tube it is (r_o² + r_i²) ÷ (r_o² − r_i²).
  - Needs: MSE-9.1.B
  - P1 · drills: mse-shape-factor, mse-shape-facts
- ● **MSE-9.1.D** (engineers-canada-materials:A6.4, engineers-canada-materials:A6.5, pe-metmat:2J) Compute an embodied energy and name the stages of a life cycle assessment.
  - EK: Embodied energy is mass times the energy to make a kilogram, less with recycled content. An LCA sets a functional unit, then counts material production, manufacture, use and end of life.
  - Needs: MSE-9.1.C
  - P1 · drills: mse-embodied-energy, mse-lca-facts

### 9.2 Degradation and protection



- ● **MSE-9.2.A** (engineers-canada-materials:A7.2, engineers-canada-materials:A7.3, fe-mechanical:9I, pe-metmat:2A) Find the cell voltage of a galvanic couple and which metal corrodes.
  - EK: The metal with the lower (more negative) potential is the anode and corrodes; the emf is E_cathode − E_anode. A small anode joined to a large cathode corrodes fastest.
  - Needs: MSE-9.1.D
  - P1 · drills: mse-galvanic-emf, mse-galvanic-anode
- ● **MSE-9.2.B** (engineers-canada-materials:A7.3) Apply the Nernst equation to a metal electrode.
  - EK: E = E° + (0.0592 ÷ n) log[Mⁿ⁺] at 25 °C: a metal in a dilute solution of its ions is more active, which is what drives a concentration cell.
  - Needs: MSE-9.2.A
  - P1 · drills: mse-nernst-metal, mse-nernst-concentration
- ● **MSE-9.2.C** (engineers-canada-materials:A7.3, pe-metmat:4D) Compute a corrosion rate from weight loss and from current density.
  - EK: Penetration in mm/yr = 87.6W ÷ (ρAt), with W in mg, ρ in g/cm³, A in cm², t in hours. By Faraday's law a corrosion current density i removes iM ÷ (nFρ) of depth per second.
  - Needs: MSE-9.2.B
  - P1 · drills: mse-corrosion-weight-loss, mse-corrosion-current
- ● **MSE-9.2.D** (engineers-canada-materials:A7.3, engineers-canada-materials:A7.2) Read the active, passive and transpassive regions of a polarization curve.
  - EK: A passive metal (stainless steel, aluminium, titanium) forms a thin oxide film and its corrosion current falls by orders of magnitude as the potential rises; at higher potential still the film breaks down. Chlorides break the film locally and cause pitting.
  - Needs: MSE-9.2.C
  - P2 · drills: mse-passivity-region, mse-passivity-facts
- ● **MSE-9.2.E** (engineers-canada-materials:A7.1, pe-metmat:2A, pe-metmat:4F) Compute a Pilling-Bedworth ratio and judge the oxide scale.
  - EK: P-B ratio = volume of oxide formed ÷ volume of metal consumed = (M_oxide ρ_metal) ÷ (n M_metal ρ_oxide). Under 1 the scale is porous; 1 to 2 protective; well above 2 it cracks and spalls. A protective scale grows parabolically.
  - Needs: MSE-9.2.D
  - P1 · drills: mse-pilling-bedworth, mse-scale-protective
- ● **MSE-9.2.F** (engineers-canada-materials:A7.4, pe-metmat:2A) Tell stress-corrosion cracking, hydrogen embrittlement and corrosion fatigue apart.
  - EK: SCC needs a tensile stress, a susceptible alloy and a specific environment together. Hydrogen embrittlement comes from atomic hydrogen entering high-strength steel. Corrosion fatigue removes the fatigue limit.
  - Needs: MSE-9.2.E
  - P2 · drills: mse-stress-corrosion-type, mse-stress-corrosion-facts
- ● **MSE-9.2.G** (engineers-canada-materials:A7.5, engineers-canada-materials:A7.6, engineers-canada-materials:A7.7, pe-metmat:3C, pe-metmat:4E) Choose a protection method and size a sacrificial anode.
  - EK: Cathodic protection makes the structure the cathode, by a sacrificial anode (Zn, Mg, Al) or an impressed current. Anodic protection holds a passivating alloy in its passive range. Coatings are barriers; inhibitors slow the anodic or cathodic reaction. Anode mass consumed is ItM ÷ nF.
  - Needs: MSE-9.2.F
  - P1 · drills: mse-anode-mass, mse-protection-method
- ● **MSE-9.2.H** (engineers-canada-materials:A7.1, pe-metmat:2B) Describe how polymers and ceramics degrade.
  - EK: Polymers swell or dissolve in chemically similar liquids, and their chains are cut by UV, heat, oxygen and hydrolysis. Ceramics are already oxides and resist corrosion, but dissolve in molten slags and, for silicates, in hydrofluoric acid and strong alkali.
  - Needs: MSE-9.2.G
  - P2 · drills: mse-nonmetal-degradation, mse-nonmetal-degradation-facts
- ● **MSE-9.2.I** (pe-metmat:2E) Compute wear volume with Archard's law and name the wear modes.
  - EK: V = KFs ÷ H: wear volume grows with load and sliding distance and falls with hardness; K is a dimensionless wear coefficient found by test.
  - Needs: MSE-9.2.H
  - P1 · drills: mse-archard, mse-wear-modes

## Unit 10 · Polymer structure and properties

Big ideas: LATTICE, PATH

### 10.1 Chains, transitions and flow



- ● **MSE-10.1.A** (engineers-canada-materials:B7.1) Compute the size of a random-coil chain.
  - EK: A freely jointed chain of n links of length l has root-mean-square end-to-end distance l√n, far shorter than its contour length nl. That gap is why rubber can stretch several hundred percent.
  - Needs: MSE-5.3.B
  - P1 · drills: mse-chain-rms, mse-chain-extension
- ● **MSE-10.1.B** (engineers-canada-materials:B7.2, pe-metmat:4C) Match a molar-mass method to the average it gives and use the Mark-Houwink relation.
  - EK: Colligative methods (osmometry, end-group analysis) count molecules and give M_n; light scattering weights by size and gives M_w; viscometry gives M_v through [η] = K Mᵃ; gel permeation chromatography gives the whole distribution.
  - Needs: MSE-10.1.A
  - P1 · drills: mse-molar-mass-method, mse-mark-houwink
- ● **MSE-10.1.C** (engineers-canada-materials:B7.3) Use the Flory-Huggins parameter to judge solvent quality.
  - EK: χ measures polymer-solvent contact energy. Below 0.5 the solvent is good and coils swell; at 0.5 (the theta condition) they are ideal; above it the polymer separates. For a chain of N segments the critical value is ½(1 + 1 ÷ √N)².
  - Needs: MSE-10.1.B
  - P1 · drills: mse-flory-critical, mse-solvent-quality
- ● **MSE-10.1.D** (engineers-canada-materials:B7.4) Estimate a glass transition temperature and say what moves it.
  - EK: For a miscible blend or random copolymer the Fox equation gives 1 ÷ T_g = w₁ ÷ T_g1 + w₂ ÷ T_g2 (kelvin). T_g rises with chain stiffness, bulky or polar side groups and crosslinking, and falls with plasticizer and free volume.
  - Needs: MSE-10.1.C
  - P1 · drills: mse-fox-tg, mse-tg-facts
- ● **MSE-10.1.E** (engineers-canada-materials:B7.5, pe-metmat:1A) Compute percent crystallinity from density.
  - EK: % crystallinity = ρ_c(ρ_s − ρ_a) ÷ [ρ_s(ρ_c − ρ_a)] × 100, a mass fraction from the specimen, fully crystalline and fully amorphous densities. Regular, linear chains cooled slowly crystallise most.
  - Needs: MSE-10.1.D
  - P1 · drills: mse-crystallinity, mse-crystallinity-facts
- ● **MSE-10.1.F** (engineers-canada-materials:B7.6) Use the Maxwell model and tell creep from stress relaxation.
  - EK: A Maxwell element (spring and dashpot in series) held at fixed strain relaxes as σ = σ₀ exp(−t ÷ τ), with relaxation time τ = η ÷ E. Creep is strain growing under constant stress; stress relaxation is stress falling at constant strain.
  - Needs: MSE-10.1.E
  - P1 · drills: mse-maxwell-relaxation, mse-viscoelastic-test
- ● **MSE-10.1.G** (engineers-canada-materials:B7.6) Compute a rubber's modulus and a time-temperature shift.
  - EK: Rubber elasticity is entropic: G = ρRT ÷ M_c, rising with temperature and crosslink density. The WLF equation log a_T = −17.44(T − T_g) ÷ (51.6 + T − T_g) shifts a relaxation time from T_g to T.
  - Needs: MSE-10.1.F
  - P1 · drills: mse-rubber-modulus, mse-wlf
- ● **MSE-10.1.H** (engineers-canada-materials:B7.7) Use the power law for a polymer melt's viscosity.
  - EK: Polymer melts shear thin: η = K γ̇ⁿ⁻¹ with n below 1, because chains disentangle and align. n = 1 is Newtonian.
  - Needs: MSE-10.1.G
  - P1 · drills: mse-power-law-viscosity, mse-flow-class
- ● **MSE-10.1.I** (engineers-canada-materials:B7.8, pe-metmat:3J) Match a polymer part to its process.
  - EK: Injection moulding makes complex solid parts in a closed mould; extrusion makes continuous sections; blow moulding makes hollow containers from a tube of melt; compression moulding and casting suit thermosets, which cannot be remelted.
  - Needs: MSE-10.1.H
  - P2 · drills: mse-polymer-process, mse-polymer-process-facts

## Unit 11 · Extraction and refining

Big ideas: PATH

### 11.1 From ore to metal



- ● **MSE-11.1.A** (engineers-canada-materials:B2.1) Compute grinding energy with Bond's law and order the mineral-processing steps.
  - EK: W = 10 W_i (1 ÷ √P₈₀ − 1 ÷ √F₈₀) kWh per tonne, with sizes in micrometres. Ore is crushed and ground to free the mineral, classified, concentrated (often by flotation), then dewatered.
  - Needs: MSE-8.2.D
  - P1 · drills: mse-bond-energy, mse-mineral-processing-facts
- ● **MSE-11.1.B** (engineers-canada-materials:B2.1, engineers-canada-materials:B2.4) Compute recovery and concentration ratio from assays.
  - EK: A two-product balance on feed f, concentrate c and tailing t (assays in %): C ÷ F = (f − t) ÷ (c − t), and recovery = c(f − t) ÷ [f(c − t)] × 100.
  - Needs: MSE-11.1.A
  - P1 · drills: mse-flotation-recovery, mse-concentration-ratio
- ● **MSE-11.1.C** (engineers-canada-materials:B2.2, engineers-canada-materials:B4.2) Name the pyrometallurgical steps for a sulphide ore.
  - EK: Roasting burns sulphur to SO₂ and makes oxide. Smelting melts the charge into a sulphide matte under a slag. Converting blows air through matte to oxidise iron and sulphur, leaving blister metal. Refining removes the last impurities, often electrolytically.
  - Needs: MSE-11.1.B
  - P2 · drills: mse-pyro-step, mse-pyro-facts
- ● **MSE-11.1.D** (engineers-canada-materials:B2.4, engineers-canada-materials:A1.6) Do the stoichiometry of a roast.
  - EK: ZnS + 1.5 O₂ → ZnO + SO₂: each mole of sulphide gives one of SO₂, which can become one of H₂SO₄. Use ZnS 97.44, SO₂ 64.06, H₂SO₄ 98.08 g/mol.
  - Needs: MSE-11.1.C
  - P1 · drills: mse-roast-so2, mse-roast-acid
- ● **MSE-11.1.E** (engineers-canada-materials:B1.1, engineers-canada-materials:B1.3, engineers-canada-materials:B1.5) Name the hydrometallurgical operations and where each is used.
  - EK: Leaching dissolves the metal (acid for copper oxide and zinc calcine, alkaline for bauxite, cyanide for gold, pressure acid for laterites). The liquor is purified by solvent extraction, ion exchange or precipitation, and the metal is recovered by cementation or electrowinning.
  - Needs: MSE-11.1.D
  - P2 · drills: mse-hydro-step, mse-hydro-facts
- ● **MSE-11.1.F** (engineers-canada-materials:B1.2) Read the regions and lines of a Pourbaix diagram.
  - EK: A potential-pH diagram maps where the metal (immunity), a dissolved ion (corrosion) or a solid oxide or hydroxide (passivation) is stable. Horizontal lines are electron transfer alone, vertical lines acid-base alone; water is stable between the hydrogen and oxygen lines.
  - Needs: MSE-11.1.E
  - P2 · drills: mse-pourbaix-region, mse-pourbaix-facts
- ● **MSE-11.1.G** (engineers-canada-materials:B1.4) Compute metal deposited and energy used in electrowinning.
  - EK: Faraday: m = ItMη ÷ nF, with η the current efficiency. The energy per kilogram is VnF ÷ (Mη), so high cell voltage and low efficiency both cost power.
  - Needs: MSE-11.1.F
  - P1 · drills: mse-electrowin-mass, mse-electrowin-energy
- ● **MSE-11.1.H** (engineers-canada-materials:B3.1) Describe ironmaking and do its stoichiometry.
  - EK: In a blast furnace, coke burns to CO, which reduces iron oxide as the charge descends; limestone fluxes the gangue into slag; the hot metal holds about 4% carbon. Direct reduction uses reformed natural gas or hydrogen and leaves solid sponge iron.
  - Needs: MSE-11.1.G
  - P1 · drills: mse-iron-from-ore, mse-ironmaking-facts
- ● **MSE-11.1.I** (engineers-canada-materials:B3.2, engineers-canada-materials:B3.3, engineers-canada-materials:B3.4) Place a steelmaking operation and compute a deoxidation addition.
  - EK: The basic oxygen furnace blows oxygen through hot metal to burn out carbon; the electric arc furnace melts scrap. Ladle treatment adjusts composition, deoxidises (2Al + 3O → Al₂O₃), desulphurises and degasses; the continuous caster freezes the steel into slabs or billets.
  - Needs: MSE-11.1.H
  - P1 · drills: mse-steelmaking-step, mse-deoxidation
- ● **MSE-11.1.J** (engineers-canada-materials:B4.3, engineers-canada-materials:B4.4) Describe fused-salt electrolysis and the Kroll process.
  - EK: Aluminium is too reactive for carbon reduction, so alumina dissolved in molten cryolite is electrolysed (Hall-Héroult); the carbon anode burns away: 2Al₂O₃ + 3C → 4Al + 3CO₂. Titanium is made by chlorinating the oxide and reducing TiCl₄ with magnesium (Kroll).
  - Needs: MSE-11.1.I
  - P1 · drills: mse-anode-carbon, mse-fused-salt-facts
- ● **MSE-11.1.K** (engineers-canada-materials:B2.3, engineers-canada-materials:B3.5) Classify refractories and compute a slag basicity.
  - EK: Acid refractories (silica, fireclay) resist acid slags; basic ones (magnesia, dolomite) resist basic slags; chromite, carbon and high alumina are close to neutral. Slag basicity is commonly %CaO ÷ %SiO₂; steelmaking slags run basic to hold phosphorus and sulphur.
  - Needs: MSE-11.1.J
  - P1 · drills: mse-slag-basicity, mse-refractory-class

## Unit 12 · Fabrication

Big ideas: PATH

### 12.1 Heat treating, shaping and joining



- ● **MSE-12.1.A** (engineers-canada-materials:B5.3, pe-metmat:3G) Tell the special heat treatments of steel apart.
  - EK: Austempering holds below the nose until bainite forms, with no temper needed. Martempering holds just above M_s to even out the temperature, then cools to martensite with less distortion. Process annealing softens cold-worked low-carbon steel below 727 °C; spheroidizing gives the softest high-carbon steel.
  - Needs: MSE-5.3.B, MSE-6.1.F
  - P2 · drills: mse-special-heat-treatment, mse-special-treatment-facts
- ● **MSE-12.1.B** (engineers-canada-materials:B5.4, pe-metmat:3E) Choose a surface-hardening method and estimate a case depth.
  - EK: Carburizing diffuses carbon into low-carbon steel, then quenches for a hard case on a tough core. Nitriding forms hard nitrides at about 500 °C with no quench. Induction and flame hardening heat only the surface of a medium-carbon steel. Depth goes as √(Dt).
  - Needs: MSE-12.1.A
  - P1 · drills: mse-surface-hardening, mse-case-depth
- ● **MSE-12.1.C** (engineers-canada-materials:B5.5, pe-metmat:3B) Choose a casting method and size a pattern.
  - EK: Sand casting suits large or one-off parts; die casting forces low-melting alloys into steel dies for high volume; investment (lost-wax) casting gives fine detail in any alloy; continuous casting makes slab and billet. A pattern is made oversize by the solid shrinkage.
  - Needs: MSE-12.1.B
  - P1 · drills: mse-casting-method, mse-pattern-size
- ● **MSE-12.1.D** (engineers-canada-materials:B5.6, pe-metmat:3A) Compute the limits and strain of a rolling pass.
  - EK: The rolls bite only if the draft is under μ²R. The true strain of a pass is ln(h₀ ÷ h_f).
  - Needs: MSE-12.1.C
  - P1 · drills: mse-rolling-draft, mse-rolling-strain
- ● **MSE-12.1.E** (engineers-canada-materials:B5.6, pe-metmat:3A) Estimate an extrusion pressure and name a bulk-forming process.
  - EK: Ideal extrusion pressure is p = Y ln(A₀ ÷ A_f), with Y the mean flow stress; friction and redundant work raise it. Rolling passes stock between rolls, forging squeezes it between dies, extrusion pushes it and drawing pulls it through a die.
  - Needs: MSE-12.1.D
  - P1 · drills: mse-extrusion-pressure, mse-forming-process
- ● **MSE-12.1.F** (engineers-canada-materials:B5.7, pe-metmat:3A) Compute a blanking force and name a sheet-metal operation.
  - EK: The force to shear a blank is the shear strength times the cut area, perimeter × thickness. Deep drawing pulls a blank into a cup; stretch forming thins it over a form; hydroforming shapes it with fluid pressure.
  - Needs: MSE-12.1.E
  - P1 · drills: mse-blanking-force, mse-sheet-operation
- ● **MSE-12.1.G** (engineers-canada-materials:B5.8, pe-metmat:3F) Compute a weld's heat input and choose a joining process.
  - EK: Heat input per length is ηVI ÷ v. High heat input widens the heat-affected zone and coarsens grains. Arc welding melts with an electric arc; laser welding gives a narrow deep weld; friction stir welding joins in the solid state; brazing melts only a filler.
  - Needs: MSE-12.1.F
  - P1 · drills: mse-weld-heat-input, mse-joining-process
- ● **MSE-12.1.H** (engineers-canada-materials:B5.8, pe-metmat:3F) Compute a carbon equivalent and judge weldability.
  - EK: CE = C + Mn÷6 + (Cr + Mo + V)÷5 + (Ni + Cu)÷15, the IIW formula in weight percent. A high CE means a hard, crack-prone heat-affected zone: usual guidance is no preheat under about 0.40, preheat from 0.40 to 0.60, and preheat with low-hydrogen practice and post-heat above.
  - Needs: MSE-12.1.G
  - P1 · drills: mse-carbon-equivalent, mse-weldability
- ● **MSE-12.1.I** (pe-metmat:3H) Compute porosity and sintering shrinkage of a powder compact.
  - EK: Porosity = (1 − ρ ÷ ρ_theoretical) × 100. Mass is conserved on sintering, so linear shrinkage is 1 − (ρ_green ÷ ρ_sintered)^⅓.
  - Needs: MSE-12.1.H
  - P1 · drills: mse-powder-porosity, mse-sinter-shrinkage
- ● **MSE-12.1.J** (pe-metmat:3I) Name the additive-manufacturing routes and compute an energy density.
  - EK: Powder bed fusion melts thin layers of powder with a laser or electron beam; directed energy deposition feeds powder or wire into a melt pool; binder jetting glues powder for later sintering; material extrusion lays down a filament. Volumetric energy density is P ÷ (v h t).
  - Needs: MSE-12.1.I
  - P1 · drills: mse-additive-route, mse-energy-density

## Unit 13 · Functional materials and microfabrication

Big ideas: LATTICE, DEFECT

### 13.1 Ceramics and dielectrics in use



- ● **MSE-13.1.A** (engineers-canada-materials:B6.5, pe-metmat:3H) Compute grain growth and explain sintering.
  - EK: Sintering bonds powder below melting, driven by the fall in surface energy; finer powder sinters faster. Afterward grains coarsen by d² − d₀² = Kt.
  - Needs: MSE-7.5.C, MSE-4.1.D
  - P1 · drills: mse-grain-growth, mse-sintering-facts
- ● **MSE-13.1.B** (engineers-canada-materials:B6.7) Compute an ionic conductivity from a diffusion coefficient.
  - EK: The Nernst-Einstein relation ties the two: σ = n(ze)²D ÷ kT. Ceramics such as stabilised zirconia conduct by oxygen vacancies, and their conductivity rises with temperature.
  - Needs: MSE-13.1.A
  - P1 · drills: mse-nernst-einstein, mse-ionic-conduction-facts
- ● **MSE-13.1.C** (engineers-canada-materials:B6.6, engineers-canada-materials:B8.4) Compute a capacitance and a breakdown voltage.
  - EK: C = ε₀ε_r A ÷ d, with ε₀ = 8.854 × 10⁻¹² F/m. The dielectric fails when the field reaches its dielectric strength, so V_max = strength × thickness.
  - Needs: MSE-13.1.B
  - P1 · drills: mse-capacitance, mse-breakdown-voltage
- ● **MSE-13.1.D** (engineers-canada-materials:B8.4) Tell piezoelectric, pyroelectric and ferroelectric behaviour apart.
  - EK: Piezoelectric crystals polarise under stress (and strain under a field). Pyroelectrics have a spontaneous polarisation that changes with temperature. Ferroelectrics have a spontaneous polarisation that an applied field can reverse; they lose it above the Curie temperature. Every ferroelectric is pyroelectric and piezoelectric.
  - Needs: MSE-13.1.C
  - P2 · drills: mse-polar-class, mse-polar-facts
- ● **MSE-13.1.E** (engineers-canada-materials:B8.4, pe-metmat:4J) Compute a surface reflectivity and a critical angle.
  - EK: At normal incidence from air, R = [(n − 1) ÷ (n + 1)]². Light inside a material of index n is totally reflected beyond the critical angle, sin θ_c = 1 ÷ n, which is how an optical fibre guides light.
  - Needs: MSE-13.1.D
  - P1 · drills: mse-reflectivity, mse-critical-angle

### 13.2 Electrons, junctions and superconductors



- ● **MSE-13.2.A** (engineers-canada-materials:B8.6) Use the Fermi-Dirac distribution.
  - EK: f(E) = 1 ÷ [exp((E − E_F) ÷ kT) + 1]: one half at the Fermi level, falling to zero a few kT above it. Only electrons within a few kT of E_F take part in conduction.
  - Needs: MSE-13.1.E
  - P1 · drills: mse-fermi-dirac, mse-fermi-facts
- ● **MSE-13.2.B** (engineers-canada-materials:B8.5) Compute a junction's built-in potential and say what bias does.
  - EK: V_bi = (kT ÷ q) ln(N_A N_D ÷ n_i²). Forward bias lowers the barrier and current rises exponentially; reverse bias raises it and only a small leakage flows. A solar cell is a junction that separates carriers made by light.
  - Needs: MSE-13.2.A
  - P1 · drills: mse-built-in-potential, mse-junction-bias
- ● **MSE-13.2.C** (engineers-canada-materials:B8.3) Compute a superconductor's critical field and tell type I from type II.
  - EK: H_c(T) = H_c(0)[1 − (T ÷ T_c)²]. Superconductivity needs temperature, field and current density all below their critical values. Type I expels flux completely up to H_c; type II lets flux in as vortices between H_c1 and a much higher H_c2, which is why magnets use it.
  - Needs: MSE-13.2.B
  - P1 · drills: mse-critical-field, mse-superconductor-facts

### 13.3 Microfabrication



- ● **MSE-13.3.A** (engineers-canada-materials:B10.1) Compute lithographic resolution and depth of focus.
  - EK: Rayleigh: the smallest printable feature is k₁λ ÷ NA and the depth of focus k₂λ ÷ NA². A larger numerical aperture sharpens the image but shrinks the focus range.
  - Needs: MSE-13.2.C
  - P1 · drills: mse-litho-resolution, mse-litho-focus
- ● **MSE-13.3.B** (engineers-canada-materials:B10.2) Tell isotropic from anisotropic etching and use selectivity.
  - EK: Wet chemical etches usually attack equally in all directions and undercut the mask; plasma (dry) etches can cut straight down. Selectivity is the etch rate of the film over that of the mask or the layer beneath.
  - Needs: MSE-13.3.A
  - P1 · drills: mse-etch-profile, mse-etch-selectivity
- ● **MSE-13.3.C** (engineers-canada-materials:B10.3) Choose a deposition method and count ALD cycles.
  - EK: Sputtering and evaporation are physical: atoms travel in a line from a source. CVD reacts gases at the surface and coats more evenly. ALD alternates two self-limiting gas pulses and grows a fixed fraction of a monolayer per cycle. Electrodeposition plates metal from solution.
  - Needs: MSE-13.3.B
  - P1 · drills: mse-deposition-method, mse-ald-cycles
- ● **MSE-13.3.D** (engineers-canada-materials:B10.4) Compute an oxide thickness with the Deal-Grove model and the silicon it consumes.
  - EK: x² + Ax = Bt: growth is linear in time while the surface reaction limits it, parabolic once diffusion through the oxide does. The oxide takes silicon from the wafer: Si occupies 12.06 cm³/mol and SiO₂ 27.3, so 44% of the oxide thickness was silicon.
  - Needs: MSE-13.3.C
  - P1 · drills: mse-deal-grove, mse-silicon-consumed
- ● **MSE-13.3.E** (engineers-canada-materials:B10.5) Estimate a dopant's diffusion length and compare diffusion with implantation.
  - EK: A dopant spreads about √(Dt) in a thermal step. Ion implantation fires ions at a set energy and dose: depth is set by energy, the amount by dose, at low temperature, but the crystal damage must then be annealed.
  - Needs: MSE-13.3.D
  - P1 · drills: mse-dopant-length, mse-doping-method
- ● **MSE-13.3.F** (engineers-canada-materials:B10.6) Compute die yield and dies per wafer.
  - EK: The Poisson model gives yield Y = exp(−D₀A) for defect density D₀ and die area A: large dies suffer most. Gross dies per wafer ≈ π(d÷2)² ÷ A − πd ÷ √(2A), the second term allowing for the edge.
  - Needs: MSE-13.3.E
  - P1 · drills: mse-die-yield, mse-dies-per-wafer

## Unit 14 · Composites and service practice

Big ideas: PATH

### 14.1 Composites in practice



- ● **MSE-14.1.A** (engineers-canada-materials:B11.3, engineers-canada-materials:B11.6) Classify a composite by its matrix and say why it is used.
  - EK: Polymer-matrix composites give the best strength and stiffness per weight near room temperature. Metal-matrix composites add stiffness, wear resistance and temperature capability to a metal. Ceramic-matrix composites add toughness to a ceramic, by fibres bridging and pulling out of cracks.
  - Needs: MSE-7.5.C, MSE-6.1.F
  - P2 · drills: mse-composite-class, mse-composite-class-facts
- ● **MSE-14.1.B** (engineers-canada-materials:B11.4, pe-metmat:3J) Choose a composite fabrication route and convert fibre weight fraction to volume fraction.
  - EK: Hand lay-up suits large one-off shapes; filament winding makes tubes and pressure vessels; pultrusion pulls constant sections through a heated die; prepreg cured in an autoclave gives the highest quality. V_f = (w_f ÷ ρ_f) ÷ (w_f ÷ ρ_f + w_m ÷ ρ_m).
  - Needs: MSE-14.1.A
  - P1 · drills: mse-composite-fabrication, mse-fibre-volume-fraction
- ● **MSE-14.1.C** (engineers-canada-materials:B11.5, pe-metmat:4I) Compute a longitudinal strength and name a composite failure mode.
  - EK: When the fibres fail first, σ_c = σ_f V_f + σ′_m(1 − V_f), with σ′_m the matrix stress at the fibre failure strain. Across the fibres or between plies the weak matrix and interface decide: matrix cracking, debonding, delamination.
  - Needs: MSE-14.1.B
  - P1 · drills: mse-composite-strength, mse-composite-failure
- ● **MSE-14.1.D** (engineers-canada-materials:B11.2, pe-metmat:4I) Allow for fibre orientation with an efficiency factor.
  - EK: E_c = K E_f V_f + E_m V_m, with K = 1 for aligned fibres loaded along their length, 3/8 for fibres random in a plane and 1/5 for fibres random in three dimensions.
  - Needs: MSE-14.1.C
  - P1 · drills: mse-orientation-modulus, mse-orientation-facts

### 14.2 Inspection, failure analysis and life



- ● **MSE-14.2.A** (pe-metmat:2F, pe-metmat:4E) Choose a non-destructive test.
  - EK: Dye penetrant shows cracks open to the surface. Magnetic particle shows surface and near-surface flaws in ferromagnetic parts. Eddy current finds surface flaws and measures coating thickness on conductors. Ultrasound finds internal flaws and measures thickness. Radiography images internal voids and inclusions.
  - Needs: MSE-14.1.D
  - P2 · drills: mse-ndt-choice, mse-ndt-facts
- ● **MSE-14.2.B** (pe-metmat:1C, pe-metmat:2G) Read a fracture surface and order a failure analysis.
  - EK: Beach marks and striations mean fatigue; dimples mean ductile overload; flat facets with river patterns mean cleavage; a rock-candy surface means intergranular fracture. Chevron marks point back to the origin. Preserve and document first, test non-destructively, and cut samples last.
  - Needs: MSE-14.2.A
  - P2 · drills: mse-fractography, mse-failure-analysis-facts
- ● **MSE-14.2.C** (pe-metmat:2H) Sum fatigue damage with Miner's rule.
  - EK: Damage from n cycles at a level where life is N is n ÷ N; failure is predicted when the fractions sum to 1.
  - Needs: MSE-14.2.B
  - P1 · drills: mse-miner-damage, mse-miner-remaining
