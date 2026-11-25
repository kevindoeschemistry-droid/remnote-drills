# Polymers and Materials — curriculum framework (draft 1)

Generated from `drills/frameworks/materials.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**17 learning objectives** in 3 units (6 core): 17 drilled, 0 partly, 0 with no drills. Core: 6 / 6 drilled.

## Big ideas

- **CHAINS · Polymers are distributions, not molecules.** A sample holds many chain lengths; averages and dispersity, not one molar mass, describe it.
- **PROPS · Structure sets properties.** Cross-links, band gaps and bond stiffness decide whether a material flows, conducts or stretches.

## Practices

- **P1 · Compute.** Carry the calculation to a number with units.
- **P2 · Classify.** Place a material in its family from its chemistry.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Polymers | core | — | 4 | 4 | 0 | 0 |
| 2 · Properties of solids | core | — | 2 | 2 | 0 | 0 |
| 3 · Colloids and DLVO theory | extension | — | 11 | 11 | 0 | 0 |

## Unit 1 · Polymers

Big ideas: CHAINS

### 1.1 Molar mass and growth



- ● **MT-1.1.A** Compute M_n, M_w and dispersity from a chain distribution.
  - EK: M_n = ΣnM/Σn; M_w = ΣnM²/ΣnM.
  - P1 · drills: mt-molar-mass-averages, mt-blend-mn
- ● **MT-1.1.B** Compute the degree of polymerisation of a step-growth polymer.
  - EK: X_n = (1 + r)/(1 + r − 2rp).
  - Needs: MT-1.1.A
  - P1 · drills: mt-carothers, mt-carothers-reverse
- ● **MT-1.1.C** Classify a polymer as chain-growth or step-growth.
  - EK: Vinyl polymers chain; polyesters, polyamides step.
  - P2 · drills: mt-growth-type, mt-growth-evidence
- ● **MT-1.1.D** Classify a polymer as thermoplastic or thermoset.
  - EK: Cross-linked networks do not melt.
  - P2 · drills: mt-thermoset, mt-thermoset-evidence

## Unit 2 · Properties of solids

Big ideas: PROPS

### 2.1 Mechanical and electronic



- ● **MT-2.1.A** Compute Young's modulus from a tensile test.
  - EK: E = (F/A)/(ΔL/L₀).
  - P1 · drills: mt-youngs-modulus, mt-elongation
- ● **MT-2.1.B** Relate a semiconductor's band gap to the wavelength it absorbs or emits.
  - EK: λ = hc/E_g.
  - P1 · drills: mt-band-gap, mt-gap-from-emission

## Unit 3 · Colloids and DLVO theory (extension)

Big ideas: PROPS

### 3.1 The electrical double layer



- ● **MT-3.1.A** Compute the Debye length from the ionic strength, and say how salt and valence change it.
  - EK: κ⁻¹ = √(εkT/2N_Ae²I); 0.304/√I nm for 1:1 salt at 25 °C.
  - P1 · drills: col-debye-length, col-debye-scaling, col-debye-valence
- ● **MT-3.1.B** Relate surface charge to surface potential with the Grahame equation.
  - EK: σ = √(8εkTn∞) sinh(eψ₀/2kT); σ ≈ εκψ₀ at low potential.
  - Needs: MT-3.1.A
  - P1 · drills: col-grahame, col-grahame-scale
- ● **MT-3.1.C** Find a zeta potential from electrophoretic mobility and judge stability from it.
  - EK: Smoluchowski μ = εζ/η (κa ≫ 1); Hückel μ = 2εζ/3η (κa ≪ 1); |ζ| > 30 mV usually stable.
  - Needs: MT-3.1.A
  - P1 · P2 · drills: col-zeta-from-mobility, col-huckel-or-smoluchowski, col-zeta-stability

### 3.2 Van der Waals forces between bodies



- ● **MT-3.2.A** Compute the van der Waals energy of spheres and plates from the Hamaker constant, and state its distance law.
  - EK: Spheres −AR/12D; sphere–wall −AR/6D; plates −A/12πD² per area (Derjaguin).
  - P1 · drills: col-vdw-spheres, col-vdw-distance-law
- ● **MT-3.2.B** Estimate a Hamaker constant across a medium with the combining rule.
  - EK: A₁₃₁ ≈ (√A₁₁ − √A₃₃)².
  - Needs: MT-3.2.A
  - P1 · drills: col-hamaker-combining, col-hamaker-same

### 3.3 DLVO theory



- ● **MT-3.3.A** Compute the double-layer repulsion between spheres in the weak-overlap, low-potential limit.
  - EK: W = 2πεRψ₀²e^(−κD) for equal spheres.
  - Needs: MT-3.1.A
  - P1 · drills: col-edl-repulsion, col-edl-decay
- ● **MT-3.3.B** Add attraction and repulsion into the DLVO curve, find the barrier, and read its minima.
  - EK: Primary minimum, barrier, secondary minimum; barriers above ~15–20 kT give stability.
  - Needs: MT-3.3.A, MT-3.2.A
  - P1 · P2 · drills: col-dlvo-total, col-dlvo-barrier, col-secondary-minimum
- ● **MT-3.3.C** Predict how salt, valence, surface potential and Hamaker constant change stability, including the Schulze–Hardy rule.
  - EK: CCC where W = 0 and dW/dD = 0; c_ccc ∝ z⁻⁶ at high potential.
  - Needs: MT-3.3.B
  - P2 · drills: col-salt-effect, col-schulze-hardy, col-ccc-condition

### 3.4 Kinetics of aggregation and forces beyond DLVO



- ● **MT-3.4.A** Compute a Brownian diffusion coefficient with Stokes–Einstein.
  - EK: D = kT/6πηa.
  - P1 · drills: col-stokes-einstein, col-diffusion-time
- ● **MT-3.4.B** Compute the half-life of rapid (barrierless) coagulation.
  - EK: k_f = 4kT/3η; t½ = 3η/4kTN₀.
  - Needs: MT-3.4.A
  - P1 · drills: col-fast-coagulation, col-coag-scale
- ● **MT-3.4.C** Recognise steric, depletion, bridging and hydration forces that DLVO leaves out.
  - EK: Polymers and solvent structure add terms DLVO lacks.
  - Needs: MT-3.3.B
  - P2 · drills: col-beyond-dlvo, col-nondlvo-scenario
