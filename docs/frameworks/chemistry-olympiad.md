# Chemistry Olympiad — curriculum framework (draft 1)

Generated from `drills/frameworks/chemistry-olympiad.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**73 learning objectives** in 15 units (73 core): 73 drilled, 0 partly, 0 with no drills. Core: 73 / 73 drilled.

## Big ideas

- **EXACT · Solve the balance, not the shortcut.** Charge and mass balances solved exactly show when the approximations hold and fix them when they fail.
- **CYCLE · Energies add around cycles.** Hess's law, Born–Haber cycles and adding ΔG = −nFE° are the same move.
- **COUNT · Count the possibilities.** Isotope peaks and NMR lines are combinatorics of independent choices.

## Practices

- **P1 · Compute.** Carry a multi-step problem to a number.
- **P2 · Count.** Enumerate outcomes systematically.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Equilibria in depth | core | — | 5 | 5 | 0 | 0 |
| 2 · Electrochemistry and thermochemistry in depth | core | — | 4 | 4 | 0 | 0 |
| 3 · Kinetics in depth | core | — | 2 | 2 | 0 | 0 |
| 4 · Solutions and spectra in depth | core | — | 3 | 3 | 0 | 0 |
| 5 · USNCO band 1: stoichiometry and solutions | core | — | 5 | 5 | 0 | 0 |
| 6 · USNCO band 2: descriptive chemistry and the laboratory | core | — | 6 | 6 | 0 | 0 |
| 7 · USNCO band 3: states of matter | core | — | 5 | 5 | 0 | 0 |
| 8 · USNCO band 4: thermodynamics | core | — | 5 | 5 | 0 | 0 |
| 9 · USNCO band 5: kinetics | core | — | 5 | 5 | 0 | 0 |
| 10 · USNCO band 6: equilibrium | core | — | 5 | 5 | 0 | 0 |
| 11 · USNCO band 7: oxidation–reduction and electrochemistry | core | — | 5 | 5 | 0 | 0 |
| 12 · USNCO band 8: atomic structure and periodicity | core | — | 6 | 6 | 0 | 0 |
| 13 · USNCO band 9: bonding and molecular structure | core | — | 5 | 5 | 0 | 0 |
| 14 · USNCO band 10: organic chemistry, biochemistry and spectroscopy | core | — | 6 | 6 | 0 | 0 |
| 15 · USNCO Part II: multi-step problems | core | — | 6 | 6 | 0 | 0 |

## Unit 1 · Equilibria in depth

Big ideas: EXACT

### 1.1 Acid–base and solubility



- ● **CO-1.1.A** Compute the pH of a polyprotic acid or one of its salts from the full charge balance.
  - EK: Amphiprotic salts sit near ½(pKₐₙ + pKₐₙ₊₁).
  - P1 · drills: co-polyprotic-ph
- ● **CO-1.1.B** Compute a buffer's pH after strong acid is added.
  - EK: Convert base to acid mole for mole, then the equilibrium.
  - P1 · drills: co-buffer-acid
- ● **CO-1.1.C** Compute the solubility of a salt of a weak acid at fixed pH.
  - EK: s = [K_sp(1 + [H⁺]/Kₐ)²/4]^⅓ for CaF₂.
  - Needs: CO-1.1.A
  - P1 · drills: co-solubility-ph

### 1.2 Gas equilibria



- ● **CO-1.2.A** Convert K_c to K_p.
  - EK: K_p = K_c(RT)^Δn.
  - P1 · drills: co-kp-kc
- ● **CO-1.2.B** Compute the degree of dissociation at a given total pressure.
  - EK: α = √(K_p/(4P + K_p)) for N₂O₄.
  - Needs: CO-1.2.A
  - P1 · drills: co-dissociation

## Unit 2 · Electrochemistry and thermochemistry in depth

Big ideas: CYCLE

### 2.1 Electrochemistry



- ● **CO-2.1.A** Compute E° of an insoluble-salt electrode from K_sp.
  - EK: E° = E°(Mⁿ⁺/M) + (RT/nF) ln K_sp.
  - P1 · drills: co-e-from-ksp
- ● **CO-2.1.B** Compute the mass deposited or the time needed in electrolysis.
  - EK: n = It/(zF).
  - P1 · drills: co-electrolysis

### 2.2 Thermochemistry



- ● **CO-2.2.A** Close a Born–Haber cycle for the lattice enthalpy.
  - EK: ΔH_f = sublimation + IE + atomisation + EA + lattice.
  - P1 · drills: co-born-haber
- ● **CO-2.2.B** Estimate a reaction enthalpy from bond enthalpies.
  - EK: Σ broken − Σ formed.
  - P1 · drills: co-bond-enthalpy

## Unit 3 · Kinetics in depth

Big ideas: EXACT

### 3.1 Integrated laws and decay chains



- ● **CO-3.1.A** Compute the time to reach a concentration for zero-, first- or second-order kinetics.
  - EK: Integrated rate laws.
  - P1 · drills: co-integrated-rate
- ● **CO-3.1.B** Compute the daughter population in a two-step decay chain.
  - EK: Bateman equation.
  - Needs: CO-3.1.A
  - P1 · drills: co-decay-chain

## Unit 4 · Solutions and spectra in depth

Big ideas: COUNT

### 4.1 Colligative and spectroscopic counting



- ● **CO-4.1.A** Find the degree of dissociation from a freezing-point depression.
  - EK: i = 1 + α(ν − 1).
  - P1 · drills: co-vant-hoff
- ● **CO-4.1.B** Predict relative isotope-peak intensities for Cl and Br compounds.
  - EK: Binomial in the isotope fractions.
  - P2 · drills: co-isotope-pattern
- ● **CO-4.1.C** Count the lines of a first-order NMR multiplet.
  - EK: (n + 1)(m + 1), collapsing when J are equal.
  - P2 · drills: co-nmr-multiplicity

## Unit 5 · USNCO band 1: stoichiometry and solutions

Big ideas: EXACT

### 5.1 Stoichiometry and solutions



- ● **CO-5.1.A** (usnco:1) Find a C:H ratio from combustion analysis.
  - EK: All C ends in CO₂ and all H in H₂O; compare moles.
  - P1 · drills: co-combustion-ratio
- ● **CO-5.1.B** (usnco:1) Find the water of crystallisation of a hydrate.
  - EK: n = (mass of water / 18.015) / (mass of anhydrous salt / M).
  - P1 · drills: co-hydrate-n
- ● **CO-5.1.C** (usnco:1) Prepare a solution of given molality.
  - EK: Molality is moles of solute per kilogram of solvent.
  - P1 · drills: co-molality-mass
- ● **CO-5.1.D** (usnco:1) Find a product yield from a limiting reagent.
  - EK: Convert both reactants to moles of product; the smaller wins.
  - P1 · drills: co-limiting-yield
- ● **CO-5.1.E** (usnco:1) Work a back titration.
  - EK: Excess reagent is titrated; what reacted is total minus excess.
  - P1 · drills: co-back-titration

## Unit 6 · USNCO band 2: descriptive chemistry and the laboratory

Big ideas: EXACT

### 6.1 Descriptive and laboratory chemistry



- ● **CO-6.1.A** (usnco:2) Know flame-test colours.
  - EK: Li crimson, Na yellow, K lilac, Ca orange-red, Sr red, Ba pale green, Cu blue-green.
  - P1 · drills: co-flame-test
- ● **CO-6.1.B** (usnco:2) Choose a reagent that tells two salts apart.
  - EK: Pick a reagent that gives a precipitate, gas or colour with one and not the other.
  - P1 · drills: co-distinguish-salts
- ● **CO-6.1.C** (usnco:2) Recall the colours of common precipitates and ions.
  - EK: AgCl white, AgBr cream, AgI yellow, PbI₂ bright yellow, Cu(OH)₂ blue, Fe(OH)₃ rust-brown, Fe(OH)₂ green, CuS and PbS black.
  - P1 · drills: co-precipitate-colour
- ● **CO-6.1.D** (usnco:2) Choose a colorimeter wavelength.
  - EK: Measure at the colour the solution absorbs: the complement of the colour you see.
  - P1 · drills: co-colorimeter-led
- ● **CO-6.1.E** (usnco:2) Predict the direction of a laboratory error.
  - EK: Follow the error through the calculation: which measured quantity is too big or too small?
  - P1 · drills: co-lab-error
- ● **CO-6.1.F** (usnco:2) Correct a gas collected over water.
  - EK: p_gas = P_total − p_water; then n = pV/RT.
  - P1 · drills: co-gas-over-water

## Unit 7 · USNCO band 3: states of matter

Big ideas: EXACT

### 7.1 Gases, liquids and solids



- ● **CO-7.1.A** (usnco:3) Find a density from a cubic unit cell.
  - EK: ρ = Z M / (N_A a³); Z = 1, 2, 4 for sc, bcc, fcc.
  - P1 · drills: co-unit-cell-density
- ● **CO-7.1.B** (usnco:3) Give coordination numbers in common ionic structures.
  - EK: Rock salt 6:6; CsCl 8:8; zinc blende 4:4; fluorite Ca 8, F 4; rutile Ti 6, O 3.
  - P1 · drills: co-coordination-structure
- ● **CO-7.1.C** (usnco:3) Find how much liquid remains when some evaporates into a closed flask.
  - EK: Vapour moles = P_vap V/RT; if less than the total, the rest stays liquid.
  - P1 · drills: co-liquid-remaining
- ● **CO-7.1.D** (usnco:3) Use Graham's law.
  - EK: Effusion rate ∝ 1/√M.
  - P1 · drills: co-graham
- ● **CO-7.1.E** (usnco:3) Rank substances by boiling or melting point.
  - EK: Ionic and network solids first; then hydrogen bonding; then dispersion, which grows with size and surface area.
  - P1 · drills: co-boiling-rank

## Unit 8 · USNCO band 4: thermodynamics

Big ideas: EXACT

### 8.1 Thermodynamics



- ● **CO-8.1.A** (usnco:4) Find K from ΔH° and ΔS° at a temperature.
  - EK: ΔG° = ΔH° − TΔS°; K = e^{−ΔG°/RT}.
  - P1 · drills: co-k-from-dh-ds
- ● **CO-8.1.B** (usnco:4) Find the temperature at which a reaction becomes spontaneous.
  - EK: T = ΔH°/ΔS° when both have the same sign.
  - P1 · drills: co-crossover-temperature
- ● **CO-8.1.C** (usnco:4) Find an enthalpy of solution from calorimetry.
  - EK: q = m c ΔT absorbed by the solution; ΔH_soln = −q/n.
  - P1 · drills: co-enthalpy-solution
- ● **CO-8.1.D** (usnco:4) Predict the sign of ΔS.
  - EK: More moles of gas, dissolving a solid, melting and mixing raise entropy; forming fewer, more ordered particles lowers it.
  - P1 · drills: co-entropy-sign
- ● **CO-8.1.E** (usnco:4) Close a Hess's-law cycle.
  - EK: Reverse and scale the given reactions until they add to the target; do the same to their ΔH.
  - P1 · drills: co-hess-cycle

## Unit 9 · USNCO band 5: kinetics

Big ideas: EXACT

### 9.1 Kinetics



- ● **CO-9.1.A** (usnco:5) Find a reaction order from initial-rate data.
  - EK: Order = log(rate ratio)/log(concentration ratio).
  - P1 · drills: co-order-from-rates
- ● **CO-9.1.B** (usnco:5) Find the rate law from a mechanism with a fast pre-equilibrium.
  - EK: Rate = k₂K₁[...]: substitute the intermediate from the equilibrium.
  - P1 · drills: co-preequilibrium-order
- ● **CO-9.1.C** (usnco:5) Find product fractions for parallel first-order reactions.
  - EK: Fraction of B = k_B/(k_B + k_C); with Arrhenius, the higher-Eₐ path grows with T.
  - P1 · drills: co-parallel-arrhenius
- ● **CO-9.1.D** (usnco:5) Use a kinetic isotope effect.
  - EK: C–D bonds have lower zero-point energy than C–H, so breaking them in the rate-determining step is slower (k_H/k_D ≈ 2–7).
  - P1 · drills: co-isotope-effect
- ● **CO-9.1.E** (usnco:5) Find the activity of a daughter after a decay chain reaches secular equilibrium.
  - EK: When the parent lives much longer, daughter activity equals parent activity.
  - P1 · drills: co-secular-equilibrium

## Unit 10 · USNCO band 6: equilibrium

Big ideas: EXACT

### 10.1 Equilibrium



- ● **CO-10.1.A** (usnco:6) Combine equilibrium constants.
  - EK: Reverse: 1/K; multiply by n: Kⁿ; add reactions: multiply K's.
  - P1 · drills: co-combine-k
- ● **CO-10.1.B** (usnco:6) Find pKa from a percent ionisation.
  - EK: Ka = c α²/(1 − α).
  - P1 · drills: co-pka-from-ionisation
- ● **CO-10.1.C** (usnco:6) Find a solubility enhanced by complex formation.
  - EK: AgCl + 2NH₃ ⇌ Ag(NH₃)₂⁺ + Cl⁻ with K = K_sp K_f; s ≈ √K [NH₃].
  - P1 · drills: co-complex-solubility
- ● **CO-10.1.D** (usnco:6) Write and use K for a heterogeneous equilibrium.
  - EK: Pure solids and liquids are left out of K.
  - P1 · drills: co-heterogeneous-kp
- ● **CO-10.1.E** (usnco:6) Find the pH at points of a diprotic titration.
  - EK: First half-equivalence: pH = pKa₁; first equivalence: (pKa₁ + pKa₂)/2; second half-equivalence: pKa₂.
  - P1 · drills: co-diprotic-points

## Unit 11 · USNCO band 7: oxidation–reduction and electrochemistry

Big ideas: EXACT

### 11.1 Redox and electrochemistry



- ● **CO-11.1.A** (usnco:7) Find an average oxidation state.
  - EK: Charge balance with the usual values for the other atoms.
  - P1 · drills: co-average-ox-state
- ● **CO-11.1.B** (usnco:7) Combine half-reaction potentials.
  - EK: Potentials do not add; ΔG = −nFE does: E₃ = (n₁E₁ + n₂E₂)/(n₁ + n₂).
  - P1 · drills: co-combine-potentials
- ● **CO-11.1.C** (usnco:7) Use the Nernst equation.
  - EK: E = E° − (RT/nF) ln Q.
  - P1 · drills: co-nernst
- ● **CO-11.1.D** (usnco:7) Find K from a standard cell potential.
  - EK: ln K = nFE°/RT.
  - P1 · drills: co-k-from-e
- ● **CO-11.1.E** (usnco:7) Count electrons in a redox half-reaction.
  - EK: Change in oxidation state × atoms changed.
  - P1 · drills: co-half-electrons

## Unit 12 · USNCO band 8: atomic structure and periodicity

Big ideas: EXACT

### 12.1 Atomic structure



- ● **CO-12.1.A** (usnco:8) Identify a group from successive ionisation energies.
  - EK: The big jump comes after the last valence electron.
  - P1 · drills: co-ionisation-jump
- ● **CO-12.1.B** (usnco:8) Count electrons with given quantum numbers.
  - EK: Each orbital holds 2; there are 2l + 1 orbitals per subshell and n² per shell.
  - P1 · drills: co-quantum-count
- ● **CO-12.1.C** (usnco:8) Explain anomalies in periodic trends.
  - EK: Half-filled and filled subshells resist adding or removing electrons.
  - P1 · drills: co-trend-anomaly
- ● **CO-12.1.D** (usnco:8) Find the wavelength of a hydrogen transition.
  - EK: 1/λ = R_H(1/n₁² − 1/n₂²), R_H = 1.097×10⁷ m⁻¹.
  - P1 · drills: co-hydrogen-line
- ● **CO-12.1.E** (usnco:8) Count unpaired electrons in a transition-metal ion.
  - EK: Remove s electrons first, then put the d electrons into five orbitals by Hund's rule (free ion).
  - P1 · drills: co-unpaired-ion
- ● **CO-12.1.F** (usnco:8) Predict a radioactive decay mode.
  - EK: Neutron-rich nuclides β⁻ decay; proton-rich ones β⁺ or capture electrons; very heavy ones α decay.
  - P1 · drills: co-decay-mode

## Unit 13 · USNCO band 9: bonding and molecular structure

Big ideas: EXACT

### 13.1 Bonding and structure



- ● **CO-13.1.A** (usnco:9) Predict a VSEPR shape including lone pairs.
  - EK: Count electron domains, then name the shape from the atoms only.
  - P1 · drills: co-vsepr-shape
- ● **CO-13.1.B** (usnco:9) Count the stereoisomers of an octahedral complex.
  - EK: Enumerate arrangements up to rotation; mirror images count separately.
  - P1 · drills: co-octahedral-isomers
- ● **CO-13.1.C** (usnco:9) Find a bond order from a molecular-orbital diagram.
  - EK: Bond order = (bonding − antibonding)/2.
  - P1 · drills: co-mo-bond-order
- ● **CO-13.1.D** (usnco:9) Choose the most stable resonance arrangement or isomer by formal charge.
  - EK: Prefer formal charges near zero, with negative charge on the more electronegative atom.
  - P1 · drills: co-formal-charge
- ● **CO-13.1.E** (usnco:9) Find a fractional bond order from resonance.
  - EK: Spread the π bonds over the equivalent positions: bond order = total bonds / positions.
  - P1 · drills: co-resonance-bond-order

## Unit 14 · USNCO band 10: organic chemistry, biochemistry and spectroscopy

Big ideas: EXACT

### 14.1 Organic and biochemistry



- ● **CO-14.1.A** (usnco:10) Count structural isomers.
  - EK: Enumerate chains, then branches; include rings when the formula allows.
  - P1 · drills: co-isomer-count
- ● **CO-14.1.B** (usnco:10) Find the degree of unsaturation.
  - EK: DoU = (2C + 2 + N − H − X)/2: rings plus π bonds.
  - P1 · drills: co-unsaturation
- ● **CO-14.1.C** (usnco:10) Assign an infrared band.
  - EK: O–H broad 3200–3550; C=O sharp near 1700; C≡N near 2250; C–H just below 3000 (sp³) or above (sp²).
  - P1 · drills: co-ir-band
- ● **CO-14.1.D** (usnco:10) Count ¹H NMR environments.
  - EK: Equivalent hydrogens (by symmetry) give one signal.
  - P1 · drills: co-nmr-environments
- ● **CO-14.1.E** (usnco:10) Identify the monomer of a polymer.
  - EK: Addition polymers repeat the alkene's carbons; condensation polymers lose a small molecule at each link.
  - P1 · drills: co-monomer
- ● **CO-14.1.F** (usnco:10) Find an amino acid's isoelectric point.
  - EK: pI is the average of the two pKa values on either side of the neutral form.
  - P1 · drills: co-isoelectric

## Unit 15 · USNCO Part II: multi-step problems

Big ideas: EXACT

### 15.1 Linked problems



- ● **CO-15.1.A** (usnco:P2, usnco:6) Find a molar solubility with a common ion, then compare it with pure water.
  - EK: Ksp = s(s + c) ≈ s c when c ≫ s.
  - P1 · drills: co-p2-common-ion
- ● **CO-15.1.B** (usnco:P2, usnco:7) Get ΔS° of a cell reaction from the temperature dependence of E°.
  - EK: ΔS° = nF(dE°/dT); ΔH° = ΔG° + TΔS°.
  - P1 · drills: co-p2-cell-entropy
- ● **CO-15.1.C** (usnco:P2, usnco:4) Find ΔS° from ΔG° and calorimetric ΔH°.
  - EK: ΔG° = −RT ln K; ΔS° = (ΔH° − ΔG°)/T.
  - P1 · drills: co-p2-entropy-from-k
- ● **CO-15.1.D** (usnco:P2, usnco:1) Find a hydrate's water count from an iodometric titration.
  - EK: Cu²⁺ + I⁻ → CuI + ½I₂; I₂ + 2 S₂O₃²⁻: one thiosulfate per Cu.
  - P1 · drills: co-p2-iodometric
- ● **CO-15.1.E** (usnco:P2, usnco:3) Find a density and an oxidation state from a perovskite unit cell.
  - EK: ABO₃: A at the corners (1), B at the centre (1), O at the face centres (3).
  - P1 · drills: co-p2-perovskite
- ● **CO-15.1.F** (usnco:P2, usnco:8) Find a photon energy per mole for bond breaking.
  - EK: E = N_A hc/λ.
  - P1 · drills: co-p2-photon-kj
