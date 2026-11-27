# Electric Double Layers — curriculum framework (draft 1)

Generated from `drills/frameworks/electric-double-layers.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**56 learning objectives** in 6 units (56 core): 56 drilled, 0 partly, 0 with no drills. Core: 56 / 56 drilled.

## Big ideas

- **PB · Continuum theory is the baseline the molecular theory corrects.** Poisson–Boltzmann gives the screening length, Grahame's charge–potential law, double-layer forces and electrokinetics; it fails where ion size, solvent structure and specific interactions matter.
- **STRUCT · The solvent and surface chemistry set the double layer.** The surface charge is regulated by a reaction whose reactants' local densities depend on every species near the wall, so structure and charge must be solved together.

## Practices

- **P1 · Compute.** Carry a screening length, charge, pressure, free energy or rate to a number.
- **P2 · Interpret.** Say which model, closure, limit or mechanism applies and what changes when a parameter does.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Foundations: fields, the double layer and the origin of surface charge (ch. 1–2) | core | — | 7 | 7 | 0 | 0 |
| 2 · Continuum theory: Poisson–Boltzmann, interactions and electrokinetics (ch. 3) | core | — | 13 | 13 | 0 | 0 |
| 3 · Liquid-state theory: correlation functions, closures and perturbation theory (ch. 4–5) | core | — | 10 | 10 | 0 | 0 |
| 4 · Density functional theory for electrolytes (ch. 6–7) | core | — | 11 | 11 | 0 | 0 |
| 5 · Molecular structure of the double layer (ch. 8–13) | core | — | 6 | 6 | 0 | 0 |
| 6 · Simulation and numerical methods (ch. 14–16, appendix A) | core | — | 9 | 9 | 0 | 0 |

## Unit 1 · Foundations: fields, the double layer and the origin of surface charge (ch. 1–2)

Big ideas: PB

### 1.1 Charges, fields and the double-layer concept



- ● **EL-1.1.A** (petsev-edl:1) Compute the Coulomb force between ions in a dielectric.
  - EK: F = z₁z₂e²/(4πεε₀r²); water's ε ≈ 78 cuts it about 80-fold.
  - Needs: MT-3.4.C
  - P1 · drills: el-coulomb-force, el-coulomb-kt-distance
- ● **EL-1.1.B** (petsev-edl:1) Relate surface charge to the field at the surface and treat the Helmholtz layer as a capacitor.
  - EK: Gauss: E = σ/(εε₀) at a charged wall; Helmholtz: C = εε₀/d.
  - Needs: EL-1.1.A
  - P1 · drills: el-helmholtz-capacitance, el-surface-field
- ● **EL-1.1.C** (petsev-edl:1) Use the Schulze–Hardy rule.
  - EK: Critical coagulation concentration ∝ z⁻⁶ for highly charged particles, ∝ z⁻² at low potential.
  - Needs: EL-1.1.B
  - P1 · drills: el-schulze-hardy, el-ccc-predict
- ● **EL-1.1.D** (petsev-edl:1) Place electrolyte models in the book's hierarchy.
  - EK: Primitive: ions in a dielectric continuum. Semi-primitive: explicit neutral solvent spheres. Civilized: explicit dipolar solvent.
  - Needs: EL-1.1.C
  - P2 · drills: el-model-hierarchy, el-model-capabilities

### 1.2 Charge regulation and adsorption



- ● **EL-1.2.A** (petsev-edl:2) Compute the Nernst potential of a charge-regulating surface.
  - EK: ψ_N = (ln 10 kT/e)(pI − pH_b): about 59.2 mV per pH unit at 25 °C.
  - Needs: EL-1.1.D
  - P1 · drills: el-nernst-potential, el-nernst-ph
- ● **EL-1.2.B** (petsev-edl:2) Use the low-potential charge-regulation law.
  - EK: For δ ≪ 1: σ = e²Γδ(ψ_N − ψ_s)/kT.
  - Needs: EL-1.2.A
  - P1 · drills: el-regulation-linear, el-regulation-reverse
- ● **EL-1.2.C** (petsev-edl:2) Compute Stern-layer occupancy from a modified Langmuir isotherm.
  - EK: θ = K/(1 + K), K = v₀ρ exp[(−φ − zeψ_St)/kT].
  - Needs: EL-1.2.B
  - P1 · drills: el-stern-langmuir, el-stern-potential

## Unit 2 · Continuum theory: Poisson–Boltzmann, interactions and electrokinetics (ch. 3)

Big ideas: PB

### 2.1 The single flat double layer



- ● **EL-2.1.A** (petsev-edl:3) Compute the Debye screening length.
  - EK: κ² = 2ρ₀q²/(εε₀kT); κ⁻¹ ≈ 0.304/√c nm for 1:1 salt in water at 25 °C.
  - Needs: EL-1.2.C, TD-11.2.E
  - P1 · drills: el-debye-length, el-debye-scaling
- ● **EL-2.1.B** (petsev-edl:3) Relate surface charge to surface potential with the Grahame equation.
  - EK: σ̃ = 2 sinh(ψ̃_s/2), i.e. σ = √(8εε₀ρ₀kT) sinh(eψ_s/2kT) for 1:1.
  - Needs: EL-2.1.A
  - P1 · drills: el-grahame, el-grahame-reverse
- ● **EL-2.1.C** (petsev-edl:3) Evaluate the Gouy–Chapman potential profile.
  - EK: ψ̃(z) = 4 artanh[γ e^{−κz}], γ = tanh(ψ̃_s/4).
  - Needs: EL-2.1.B
  - P1 · drills: el-gouy-chapman-profile, el-gc-half-distance
- ● **EL-2.1.D** (petsev-edl:3) Judge the error of the linearised (Debye–Hückel) profile.
  - EK: Linear: ψ̃ = ψ̃_s e^{−κz}; error = (exact − linear)/exact.
  - Needs: EL-2.1.C
  - P1 · drills: el-linear-error, el-far-field-potential

### 2.2 Interacting and curved double layers



- ● **EL-2.2.A** (petsev-edl:3) Find the double-layer pressure from the midplane potential.
  - EK: Π = 2ρ₀kT[cosh ψ̃_m − 1] for a symmetric 1:1 gap.
  - Needs: EL-2.1.D
  - P1 · drills: el-midplane-pressure, el-midplane-from-pressure
- ● **EL-2.2.B** (petsev-edl:3) Use the weak-overlap approximation.
  - EK: Π ≈ 64ρ₀kT γ² e^{−κh}: superpose the two isolated profiles at the midplane.
  - Needs: EL-2.2.A
  - P1 · drills: el-weak-overlap, el-weak-overlap-ratio
- ● **EL-2.2.C** (petsev-edl:3) Track the charge of plates held at constant potential as they approach.
  - EK: Linear PB: σ̃ = ψ̃_s tanh(κh/2) per plate.
  - Needs: EL-2.2.B
  - P1 · drills: el-constant-potential-charge, el-constant-charge-potential
- ● **EL-2.2.D** (petsev-edl:3) Compute the charge on a weakly charged sphere.
  - EK: Debye–Hückel sphere: σ = εε₀ψ_s(1 + κR)/R.
  - Needs: EL-2.2.C
  - P1 · drills: el-sphere-charge, el-sphere-flat-ratio
- ● **EL-2.2.E** (petsev-edl:3) Convert plate interactions to sphere interactions with the Derjaguin approximation.
  - EK: F(h) = 2π[R₁R₂/(R₁ + R₂)] f(h): πR f for equal spheres.
  - Needs: EL-2.2.D
  - P1 · drills: el-derjaguin-force, el-derjaguin-reverse
- ● **EL-2.2.F** (petsev-edl:3) Combine van der Waals and double-layer terms in DLVO.
  - EK: Sphere–sphere van der Waals at short range: Φ = −A R₁R₂/[6h(R₁ + R₂)].
  - Needs: EL-2.2.E
  - P1 · drills: el-vdw-spheres, el-vdw-kt-separation

### 2.3 Beyond Boltzmann and electrokinetics



- ● **EL-2.3.A** (petsev-edl:3) Compute electroosmotic and electrophoretic speeds.
  - EK: Smoluchowski: v = εε₀ζE/η (κR ≫ 1). Hückel: v = 2εε₀ζE/(3η) (κR ≪ 1).
  - Needs: EL-2.2.F
  - P1 · drills: el-electrophoresis, el-zeta-from-mobility
- ● **EL-2.3.B** (petsev-edl:3) Choose the right electrokinetic limit.
  - EK: κR ≫ 1: Smoluchowski. κR ≪ 1: Hückel. In between: Henry; with strong polarisation (large ζ, thin layers): the full electrokinetic equations.
  - Needs: EL-2.3.A
  - P2 · drills: el-ek-limit, el-ka-limit
- ● **EL-2.3.C** (petsev-edl:3) Know when Boltzmann statistics fail for charge carriers.
  - EK: Degenerate carriers follow Fermi–Dirac; the crossover is the Fermi temperature T_F = ħ²(3π²N)^{2/3}/(2m*k_B).
  - Needs: EL-2.3.B
  - P1 · drills: el-fermi-temperature, el-degenerate-density

## Unit 3 · Liquid-state theory: correlation functions, closures and perturbation theory (ch. 4–5)

Big ideas: PB

### 3.1 Integral equations



- ● **EL-3.1.A** (petsev-edl:4) Use the Ornstein–Zernike equation in Fourier space.
  - EK: ĥ = ĉ/(1 − ρĉ); S(0) = 1/(1 − ρĉ(0)) is the reduced compressibility.
  - Needs: EL-1.2.C, TD-12.5.A
  - P1 · drills: el-oz-structure-factor, el-direct-correlation-from-s
- ● **EL-3.1.B** (petsev-edl:4) Compare the hard-sphere equations of state.
  - EK: PY virial (1 + 2η + 3η²)/(1 − η)²; PY compressibility (1 + η + η²)/(1 − η)³; Carnahan–Starling (1 + η + η² − η³)/(1 − η)³.
  - Needs: EL-3.1.A
  - P1 · drills: el-hs-pressure, el-cs-vs-py-virial
- ● **EL-3.1.C** (petsev-edl:4) Recognise the common closures.
  - EK: PY: c = g(1 − e^{βφ}). HNC: c = h − ln y (i.e. g − 1 − ln y). MSA: g = 0 inside the core, c = −βφ outside.
  - Needs: EL-3.1.B
  - P2 · drills: el-closures, el-closure-forms
- ● **EL-3.1.D** (petsev-edl:4) Compute packing fraction from number density and diameter.
  - EK: η = πρd³/6; ξ₃ for mixtures.
  - Needs: EL-3.1.C
  - P1 · drills: el-packing-fraction, el-diameter-from-packing

### 3.2 Virial, perturbation and mean-field theory



- ● **EL-3.2.A** (petsev-edl:5) Compute second virial coefficients.
  - EK: B₂ = −2π∫(e^{−βφ} − 1)r²dr: 2πd³/3 for hard spheres; square well B₂ = B₂^hs[1 − (λ³ − 1)(e^{βε} − 1)].
  - Needs: EL-3.1.D
  - P1 · drills: el-b2-square-well, el-boyle-square-well
- ● **EL-3.2.B** (petsev-edl:5) Use the van der Waals equation in reduced form.
  - EK: p̃ = 8ρ̃T̃/(3 − ρ̃) − 3ρ̃².
  - Needs: EL-3.2.A
  - P1 · drills: el-vdw-reduced, el-vdw-z-reduced
- ● **EL-3.2.C** (petsev-edl:5) Solve the mean-field (Weiss) equation of the Ising model.
  - EK: m = tanh(βJqm): a nonzero root exists below kT_c = Jq.
  - Needs: EL-3.2.B
  - P1 · drills: el-mean-field-m, el-mf-susceptibility
- ● **EL-3.2.D** (petsev-edl:5) Use scaled-particle results for hard spheres.
  - EK: Probability of an empty cavity of radius σ/2: p₀ = 1 − η, so βW = −ln(1 − η); G(σ/2) = 1/(1 − η).
  - Needs: EL-3.2.C
  - P1 · drills: el-spt-cavity, el-spt-pressure
- ● **EL-3.2.E** (petsev-edl:5) Use the exact one-dimensional hard-rod fluid.
  - EK: Tonks: βp/ρ = 1/(1 − ρσ).
  - Needs: EL-3.2.D
  - P1 · drills: el-tonks, el-tonks-free-energy
- ● **EL-3.2.F** (petsev-edl:5) Split a pair potential for perturbation theory.
  - EK: WCA: split at the LJ minimum r_min = 2^{1/6}σ; Barker–Henderson: split at σ and use d = ∫₀^σ(1 − e^{−βφ})dr.
  - Needs: EL-3.2.E
  - P1 · drills: el-wca-split, el-wca-repulsive

## Unit 4 · Density functional theory for electrolytes (ch. 6–7)

Big ideas: PB

### 4.1 DFT fundamentals



- ● **EL-4.1.A** (petsev-edl:6) Minimise the ideal-gas functional in an external field.
  - EK: δΩ/δρ = 0 with F_id = kT∫ρ[ln(Λ³ρ) − 1] gives ρ(r) = ρ_b e^{−βV_ext(r)}.
  - Needs: EL-3.2.F, TD-4.3.B
  - P1 · drills: el-ideal-functional, el-ideal-well-excess
- ● **EL-4.1.B** (petsev-edl:6) Compute a surface excess adsorption.
  - EK: Γ^ex = ∫[ρ(r) − ρ_b]dr; for ρ = ρ_b(1 + A e^{−z/λ}), Γ^ex = ρ_bAλ.
  - Needs: EL-4.1.A
  - P1 · drills: el-surface-excess, el-excess-gaussian
- ● **EL-4.1.C** (petsev-edl:6) Convert a pair correlation to a potential of mean force.
  - EK: W(r) = −kT ln g(r).
  - Needs: EL-4.1.B
  - P1 · drills: el-pmf, el-g-from-pmf
- ● **EL-4.1.D** (petsev-edl:6) Relate wetting to interfacial free energies.
  - EK: Young: cos θ = (Ω^ex_WV − Ω^ex_WL)/γ_LV.
  - Needs: EL-4.1.C
  - P1 · drills: el-contact-angle, el-work-of-adhesion
- ● **EL-4.1.E** (petsev-edl:6) Scale the Thomas–Fermi kinetic energy.
  - EK: T_TF ∝ ∫ρ^{5/3}dr.
  - Needs: EL-4.1.D
  - P1 · drills: el-thomas-fermi-scaling, el-tf-compression

### 4.2 Classical DFT for electrolytes



- ● **EL-4.2.A** (petsev-edl:7) Compute the Bjerrum length and Debye length from it.
  - EK: λ_B = e²/(4πεε₀kT) ≈ 0.71 nm in water; κ² = 4πλ_BΣz_i²ρ_i.
  - Needs: EL-4.1.E
  - P1 · drills: el-bjerrum, el-debye-from-bjerrum
- ● **EL-4.2.B** (petsev-edl:7) Apply the contact theorem at a charged wall.
  - EK: kTΣρ_i(0) = p_b + σ²/(2εε₀); for an ideal 1:1 bulk p_b = 2ρ₀kT.
  - Needs: EL-4.2.A
  - P1 · drills: el-contact-theorem, el-contact-theorem-sigma
- ● **EL-4.2.C** (petsev-edl:7) Evaluate the Carnahan–Starling hard-sphere free energy.
  - EK: βf_ex = η(4 − 3η)/(1 − η)² per particle.
  - Needs: EL-4.2.B
  - P1 · drills: el-cs-free-energy, el-cs-chemical-potential
- ● **EL-4.2.D** (petsev-edl:7) Know what fundamental-measure theory weights.
  - EK: n₃ is the local packing fraction (volume weight θ(R − |r|)), n₂ the surface weight δ(R − |r|), n₁ and n₀ scaled versions, plus vector weights.
  - Needs: EL-4.2.C
  - P2 · drills: el-fmt-weights, el-fmt-measures
- ● **EL-4.2.E** (petsev-edl:7) Compute the MSA screening parameter.
  - EK: Restricted primitive model: 2Γd = √(1 + 2κd) − 1; Γ → κ/2 at low density.
  - Needs: EL-4.2.D
  - P1 · drills: el-msa-gamma, el-msa-ratio
- ● **EL-4.2.F** (petsev-edl:7) Model a charge-regulating surface with Langmuir site equilibria.
  - EK: Fraction of sites bound: θ = ρ_F(r_s)/(ρ_F(r_s) + K).
  - Needs: EL-4.2.E
  - P1 · drills: el-site-binding, el-site-binding-k

## Unit 5 · Molecular structure of the double layer (ch. 8–13)

Big ideas: PB

### 5.1 Solvent, solvation and surface interactions



- ● **EL-5.1.A** (petsev-edl:8) Explain the solvent's role in a single double layer.
  - EK: The solvent is far denser than the ions, so it sets the structure; the surface reaction involves only the PDIs, but their local density depends on every species.
  - Needs: EL-2.3.C, EL-4.2.F
  - P2 · drills: el-solvent-structure, el-solvent-per-ion
- ● **EL-5.1.B** (petsev-edl:9) Predict how solvation of each ion changes the surface charge.
  - EK: Poorly solvated PDIs crowd the wall and neutralise it; strongly solvated PDIs stay away and the negative charge grows.
  - Needs: EL-5.1.A
  - P2 · drills: el-solvation-effects, el-contact-enhanced-binding
- ● **EL-5.1.C** (petsev-edl:10) Predict effects of non-Coulombic surface interactions.
  - EK: Solvophilic walls attract solvent strongly; PDIs compete with other species for the finite space at the wall; ion–surface attraction feeds the Stern layer.
  - Needs: EL-5.1.B
  - P2 · drills: el-surface-interactions, el-spreading-coefficient

### 5.2 Potential, valency and ion size



- ● **EL-5.2.A** (petsev-edl:11) Interpret the classical double-layer planes molecularly.
  - EK: With c-DFT charge profiles in Poisson's equation, the Helmholtz planes, Stern and Grahame layers and the shear plane get molecular meanings.
  - Needs: EL-5.1.C
  - P2 · drills: el-planes, el-series-capacitance
- ● **EL-5.2.B** (petsev-edl:12) Predict the effect of multivalent ions.
  - EK: Valency changes Coulomb strength and its balance with non-Coulombic forces; multivalent counterions screen far more strongly, as in the Schulze–Hardy rule.
  - Needs: EL-5.2.A
  - P2 · drills: el-multivalent, el-valence-contact-ratio
- ● **EL-5.2.C** (petsev-edl:13) Predict the effect of ion size.
  - EK: The main effects are excluded volume and packing at the charged wall, which change the local PDI density and so the surface reaction.
  - Needs: EL-5.2.B
  - P2 · drills: el-ion-size, el-pb-overpacking

## Unit 6 · Simulation and numerical methods (ch. 14–16, appendix A)

Big ideas: PB

### 6.1 Molecular simulation



- ● **EL-6.1.A** (petsev-edl:14) Apply the Metropolis acceptance rule.
  - EK: Accept a move with probability min(1, e^{−βΔU}).
  - Needs: EL-3.2.F
  - P1 · drills: el-metropolis, el-metropolis-mean-acceptance
- ● **EL-6.1.B** (petsev-edl:14) Compute an excess chemical potential by Widom insertion.
  - EK: βμ_ex = −ln⟨e^{−βΔU}⟩ over random test insertions.
  - Needs: EL-6.1.A
  - P1 · drills: el-widom, el-widom-point
- ● **EL-6.1.C** (petsev-edl:14) Find the collision time of two hard spheres.
  - EK: Solve |r_ij + v_ij t| = σ_ij for the smallest positive t.
  - Needs: EL-6.1.B
  - P1 · drills: el-collision-time, el-collision-offset
- ● **EL-6.1.D** (petsev-edl:15) Compute the coupling parameter of a one-component plasma.
  - EK: Γ = (Ze)²/(4πε₀akT), a the Wigner–Seitz radius.
  - Needs: EL-6.1.C
  - P1 · drills: el-ocp-gamma, el-ocp-gamma-density
- ● **EL-6.1.E** (petsev-edl:15) Use the Debye–Hückel limiting law.
  - EK: log₁₀γ± = −0.509|z₊z₋|√I in water at 25 °C.
  - Needs: EL-6.1.D
  - P1 · drills: el-dh-limiting, el-ionic-strength

### 6.2 Numerical methods for c-DFT and transport



- ● **EL-6.2.A** (petsev-edl:16) Take a damped Picard step.
  - EK: x^{k+1} = (1 − α)x^k + αg(x^k).
  - Needs: EL-6.1.E
  - P1 · drills: el-picard, el-picard-alpha
- ● **EL-6.2.B** (petsev-edl:16) Take a Newton step on a nonlinear residual.
  - EK: J Δx = −R.
  - Needs: EL-6.2.A
  - P1 · drills: el-newton-pb, el-grahame-exact-root
- ● **EL-6.2.C** (petsev-edl:16) Reduce a block system with the Schur complement.
  - EK: S = A₂₂ − A₂₁A₁₁⁻¹A₁₂, then Sx₂ = b₂ − A₂₁A₁₁⁻¹b₁.
  - Needs: EL-6.2.B
  - P1 · drills: el-schur, el-schur-x1
- ● **EL-6.2.D** (petsev-edl:16, petsev-edl:A) Compute a Nernst–Planck flux.
  - EK: J = −D(dc/dx + zc dψ̃/dx): diffusion plus migration.
  - Needs: EL-6.2.C
  - P1 · drills: el-nernst-planck, el-zero-flux-gradient
