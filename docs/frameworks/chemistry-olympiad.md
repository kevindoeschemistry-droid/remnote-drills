# Chemistry Olympiad — curriculum framework (draft 1)

Generated from `drills/frameworks/chemistry-olympiad.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**92 learning objectives** in 16 units (73 core): 92 drilled, 0 partly, 0 with no drills. Core: 73 / 73 drilled.

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
| 16 · Camp-level steps | extension | — | 19 | 19 | 0 | 0 |

## Unit 1 · Equilibria in depth

Big ideas: EXACT

### 1.1 Acid–base and solubility



- ● **CO-1.1.B** Compute a buffer's pH after strong acid is added.
  - EK: Convert base to acid mole for mole, then the equilibrium.
  - Needs: CO-10.1.E
  - P1 · drills: co-buffer-acid, co-buffer-capacity-acid
- ● **CO-1.1.A** (acs-accm-analytical:VIII.F.5) Compute the pH of a polyprotic acid or one of its salts from the full charge balance.
  - EK: Amphiprotic salts sit near ½(pKₐₙ + pKₐₙ₊₁).
  - Needs: CO-1.1.B
  - P1 · drills: co-phosphate-fraction, co-polyprotic-ph
- ● **CO-1.1.C** Compute the solubility of a salt of a weak acid at fixed pH.
  - EK: s = [K_sp(1 + [H⁺]/Kₐ)²/4]^⅓ for CaF₂.
  - Needs: CO-1.1.A
  - P1 · drills: co-solubility-ph, co-solubility-ph-factor

### 1.2 Gas equilibria



- ● **CO-1.2.A** Convert K_c to K_p.
  - EK: K_p = K_c(RT)^Δn.
  - Needs: CO-1.1.C
  - P1 · drills: co-kp-kc, co-kc-from-kp
- ● **CO-1.2.B** Compute the degree of dissociation at a given total pressure.
  - EK: α = √(K_p/(4P + K_p)) for N₂O₄.
  - Needs: CO-1.2.A
  - P1 · drills: co-dissociation, co-pressure-for-alpha

## Unit 2 · Electrochemistry and thermochemistry in depth

Big ideas: CYCLE

### 2.1 Electrochemistry



- ● **CO-2.1.A** Compute E° of an insoluble-salt electrode from K_sp.
  - EK: E° = E°(Mⁿ⁺/M) + (RT/nF) ln K_sp.
  - Needs: CO-8.1.E, CO-11.1.E
  - P1 · drills: co-e-from-ksp, co-ksp-from-e
- ● **CO-2.1.B** Compute the mass deposited or the time needed in electrolysis.
  - EK: n = It/(zF).
  - Needs: CO-2.1.A
  - P1 · drills: co-electrolysis, co-current-needed

### 2.2 Thermochemistry



- ● **CO-2.2.A** Close a Born–Haber cycle for the lattice enthalpy.
  - EK: ΔH_f = sublimation + IE + atomisation + EA + lattice.
  - Needs: CO-2.1.B
  - P1 · drills: co-lattice-compare, co-born-haber
- ● **CO-2.2.B** Estimate a reaction enthalpy from bond enthalpies.
  - EK: Σ broken − Σ formed.
  - Needs: CO-2.2.A
  - P1 · drills: co-bond-enthalpy, co-bond-from-dh

## Unit 3 · Kinetics in depth

Big ideas: EXACT

### 3.1 Integrated laws and decay chains



- ● **CO-3.1.A** Compute the time to reach a concentration for zero-, first- or second-order kinetics.
  - EK: Integrated rate laws.
  - Needs: CO-9.1.E
  - P1 · drills: co-integrated-rate, co-half-life-scaling
- ● **CO-3.1.B** Compute the daughter population in a two-step decay chain.
  - EK: Bateman equation.
  - Needs: CO-3.1.A
  - P1 · drills: co-decay-chain, co-daughter-max-time

## Unit 4 · Solutions and spectra in depth

Big ideas: COUNT

### 4.1 Colligative and spectroscopic counting



- ● **CO-4.1.A** Find the degree of dissociation from a freezing-point depression.
  - EK: i = 1 + α(ν − 1).
  - Needs: CO-7.1.E
  - P1 · drills: co-vant-hoff, co-freezing-predict
- ● **CO-4.1.B** Predict relative isotope-peak intensities for Cl and Br compounds.
  - EK: Binomial in the isotope fractions.
  - Needs: CO-4.1.A
  - P2 · drills: co-isotope-pattern, co-m2-ratio
- ● **CO-4.1.C** (acs-accm-analytical:I.A.3) Count the lines of a first-order NMR multiplet.
  - EK: (n + 1)(m + 1), collapsing when J are equal.
  - Needs: CO-4.1.B
  - P2 · drills: co-nmr-multiplicity, co-multiplet-centre

## Unit 5 · USNCO band 1: stoichiometry and solutions

Big ideas: EXACT

### 5.1 Stoichiometry and solutions



- ● **CO-5.1.A** (usnco:1) Find a C:H ratio from combustion analysis.
  - EK: All C ends in CO₂ and all H in H₂O; compare moles.
  - Needs: CH-4.9.D
  - P1 · drills: co-combustion-ratio, co-co2-mass
- ● **CO-5.1.B** (usnco:1) Find the water of crystallisation of a hydrate.
  - EK: n = (mass of water / 18.015) / (mass of anhydrous salt / M).
  - Needs: CO-5.1.A
  - P1 · drills: co-hydrate-n, co-hydrate-percent
- ● **CO-5.1.C** (usnco:1) Prepare a solution of given molality.
  - EK: Molality is moles of solute per kilogram of solvent.
  - Needs: CO-5.1.B
  - P1 · drills: co-molality-mass, co-molality-from-percent
- ● **CO-5.1.D** (usnco:1) Find a product yield from a limiting reagent.
  - EK: Convert both reactants to moles of product; the smaller wins.
  - Needs: CO-5.1.C
  - P1 · drills: co-limiting-yield, co-percent-yield
- ● **CO-5.1.E** (usnco:1) Work a back titration.
  - EK: Excess reagent is titrated; what reacted is total minus excess.
  - Needs: CO-5.1.D
  - P1 · drills: co-back-titration, co-antacid-naoh

## Unit 6 · USNCO band 2: descriptive chemistry and the laboratory

Big ideas: EXACT

### 6.1 Descriptive and laboratory chemistry



- ● **CO-6.1.A** (usnco:2) Know flame-test colours.
  - EK: Li crimson, Na yellow, K lilac, Ca orange-red, Sr red, Ba pale green, Cu blue-green.
  - Needs: IN-4.2.C
  - P1 · drills: co-flame-test, co-flame-confusion
- ● **CO-6.1.B** (usnco:2) Choose a reagent that tells two salts apart.
  - EK: Pick a reagent that gives a precipitate, gas or colour with one and not the other.
  - Needs: CO-6.1.A
  - P1 · drills: co-distinguish-salts, co-tell-apart
- ● **CO-6.1.C** (usnco:2) Recall the colours of common precipitates and ions.
  - EK: AgCl white, AgBr cream, AgI yellow, PbI₂ bright yellow, Cu(OH)₂ blue, Fe(OH)₃ rust-brown, Fe(OH)₂ green, CuS and PbS black.
  - Needs: CO-6.1.B
  - P1 · drills: co-precipitate-colour, co-ppt-identify
- ● **CO-6.1.D** (usnco:2) Choose a colorimeter wavelength.
  - EK: Measure at the colour the solution absorbs: the complement of the colour you see.
  - Needs: CO-6.1.C
  - P1 · drills: co-colorimeter-led, co-colour-complement
- ● **CO-6.1.E** (usnco:2) Predict the direction of a laboratory error.
  - EK: Follow the error through the calculation: which measured quantity is too big or too small?
  - Needs: CO-6.1.D
  - P1 · drills: co-lab-error, co-error-direction
- ● **CO-6.1.F** (usnco:2) Correct a gas collected over water.
  - EK: p_gas = P_total − p_water; then n = pV/RT.
  - Needs: CO-6.1.E
  - P1 · drills: co-gas-over-water, co-wet-gas-volume

## Unit 7 · USNCO band 3: states of matter

Big ideas: EXACT

### 7.1 Gases, liquids and solids



- ● **CO-7.1.A** (usnco:3) Find a density from a cubic unit cell.
  - EK: ρ = Z M / (N_A a³); Z = 1, 2, 4 for sc, bcc, fcc.
  - Needs: CH-3.14.C
  - P1 · drills: co-unit-cell-density, co-molar-mass-from-cell
- ● **CO-7.1.B** (usnco:3) Give coordination numbers in common ionic structures.
  - EK: Rock salt 6:6; CsCl 8:8; zinc blende 4:4; fluorite Ca 8, F 4; rutile Ti 6, O 3.
  - Needs: CO-7.1.A
  - P1 · drills: co-coordination-structure, co-structure-cn
- ● **CO-7.1.C** (usnco:3) Find how much liquid remains when some evaporates into a closed flask.
  - EK: Vapour moles = P_vap V/RT; if less than the total, the rest stays liquid.
  - Needs: CO-7.1.B
  - P1 · drills: co-liquid-remaining, co-vapour-pressure-evap
- ● **CO-7.1.D** (usnco:3) Use Graham's law.
  - EK: Effusion rate ∝ 1/√M.
  - Needs: CO-7.1.C
  - P1 · drills: co-graham, co-graham-mass
- ● **CO-7.1.E** (usnco:3) Rank substances by boiling or melting point.
  - EK: Ionic and network solids first; then hydrogen bonding; then dispersion, which grows with size and surface area.
  - Needs: CO-7.1.D
  - P1 · drills: co-boiling-rank, co-mp-rank

## Unit 8 · USNCO band 4: thermodynamics

Big ideas: EXACT

### 8.1 Thermodynamics



- ● **CO-8.1.A** (usnco:4) Find K from ΔH° and ΔS° at a temperature.
  - EK: ΔG° = ΔH° − TΔS°; K = e^{−ΔG°/RT}.
  - Needs: CH-9.12.A
  - P1 · drills: co-k-from-dh-ds, co-dg-from-k
- ● **CO-8.1.B** (usnco:4) Find the temperature at which a reaction becomes spontaneous.
  - EK: T = ΔH°/ΔS° when both have the same sign.
  - Needs: CO-8.1.A
  - P1 · drills: co-crossover-temperature, co-ds-from-crossover
- ● **CO-8.1.C** (usnco:4) Find an enthalpy of solution from calorimetry.
  - EK: q = m c ΔT absorbed by the solution; ΔH_soln = −q/n.
  - Needs: CO-8.1.B
  - P1 · drills: co-enthalpy-solution, co-temp-change-solution
- ● **CO-8.1.D** (usnco:4) Predict the sign of ΔS.
  - EK: More moles of gas, dissolving a solid, melting and mixing raise entropy; forming fewer, more ordered particles lowers it.
  - Needs: CO-8.1.C
  - P1 · drills: co-entropy-sign, co-ds-sign-2
- ● **CO-8.1.E** (usnco:4) Close a Hess's-law cycle.
  - EK: Reverse and scale the given reactions until they add to the target; do the same to their ΔH.
  - Needs: CO-8.1.D
  - P1 · drills: co-hess-cycle, co-hf-from-hc

## Unit 9 · USNCO band 5: kinetics

Big ideas: EXACT

### 9.1 Kinetics



- ● **CO-9.1.A** (usnco:5) Find a reaction order from initial-rate data.
  - EK: Order = log(rate ratio)/log(concentration ratio).
  - Needs: CH-5.11.A
  - P1 · drills: co-order-from-rates, co-rate-predict
- ● **CO-9.1.B** (usnco:5) Find the rate law from a mechanism with a fast pre-equilibrium.
  - EK: Rate = k₂K₁[...]: substitute the intermediate from the equilibrium.
  - Needs: CO-9.1.A
  - P1 · drills: co-preequilibrium-order, co-mechanism-rate-law
- ● **CO-9.1.C** (usnco:5) Find product fractions for parallel first-order reactions.
  - EK: Fraction of B = k_B/(k_B + k_C); with Arrhenius, the higher-Eₐ path grows with T.
  - Needs: CO-9.1.B
  - P1 · drills: co-parallel-arrhenius, co-equal-rate-temp
- ● **CO-9.1.D** (usnco:5) Use a kinetic isotope effect.
  - EK: C–D bonds have lower zero-point energy than C–H, so breaking them in the rate-determining step is slower (k_H/k_D ≈ 2–7).
  - Needs: CO-9.1.C
  - P1 · drills: co-isotope-effect, co-kie-from-freq
- ● **CO-9.1.E** (usnco:5) Find the activity of a daughter after a decay chain reaches secular equilibrium.
  - EK: When the parent lives much longer, daughter activity equals parent activity.
  - Needs: CO-9.1.D
  - P1 · drills: co-secular-equilibrium, co-daughter-halflife

## Unit 10 · USNCO band 6: equilibrium

Big ideas: EXACT

### 10.1 Equilibrium



- ● **CO-10.1.A** (usnco:6) Combine equilibrium constants.
  - EK: Reverse: 1/K; multiply by n: Kⁿ; add reactions: multiply K's.
  - Needs: CH-8.11.A
  - P1 · drills: co-combine-k, co-k-reverse-scale
- ● **CO-10.1.B** (usnco:6) Find pKa from a percent ionisation.
  - EK: Ka = c α²/(1 − α).
  - Needs: CO-10.1.A
  - P1 · drills: co-pka-from-ionisation, co-ionisation-from-pka
- ● **CO-10.1.C** (usnco:6) Find a solubility enhanced by complex formation.
  - EK: AgCl + 2NH₃ ⇌ Ag(NH₃)₂⁺ + Cl⁻ with K = K_sp K_f; s ≈ √K [NH₃].
  - Needs: CO-10.1.B
  - P1 · drills: co-complex-solubility, co-agcl-in-ammonia
- ● **CO-10.1.D** (usnco:6) Write and use K for a heterogeneous equilibrium.
  - EK: Pure solids and liquids are left out of K.
  - Needs: CO-10.1.C
  - P1 · drills: co-heterogeneous-kp, co-carbonate-decomposed
- ● **CO-10.1.E** (usnco:6) Find the pH at points of a diprotic titration.
  - EK: First half-equivalence: pH = pKa₁; first equivalence: (pKa₁ + pKa₂)/2; second half-equivalence: pKa₂.
  - Needs: CO-10.1.D
  - P1 · drills: co-diprotic-points, co-first-equivalence-ph

## Unit 11 · USNCO band 7: oxidation–reduction and electrochemistry

Big ideas: EXACT

### 11.1 Redox and electrochemistry



- ● **CO-11.1.A** (usnco:7) Find an average oxidation state.
  - EK: Charge balance with the usual values for the other atoms.
  - Needs: CH-9.12.A
  - P1 · drills: co-average-ox-state, co-mixed-valence-fraction
- ● **CO-11.1.B** (usnco:7) Combine half-reaction potentials.
  - EK: Potentials do not add; ΔG = −nFE does: E₃ = (n₁E₁ + n₂E₂)/(n₁ + n₂).
  - Needs: CO-11.1.A
  - P1 · drills: co-combine-potentials, co-disprop-potential
- ● **CO-11.1.C** (usnco:7, acs-accm-analytical:VI.E.1) Use the Nernst equation.
  - EK: E = E° − (RT/nF) ln Q.
  - Needs: CO-11.1.B
  - P1 · drills: co-nernst, co-ratio-from-emf
- ● **CO-11.1.D** (usnco:7, acs-accm-analytical:VIII.F.1, acs-accm-analytical:VIII.G.5) Find K from a standard cell potential.
  - EK: ln K = nFE°/RT.
  - Needs: CO-11.1.C
  - P1 · drills: co-k-from-e, co-e-from-k
- ● **CO-11.1.E** (usnco:7) Count electrons in a redox half-reaction.
  - EK: Change in oxidation state × atoms changed.
  - Needs: CO-11.1.D
  - P1 · drills: co-half-electrons, co-protons-in-half

## Unit 12 · USNCO band 8: atomic structure and periodicity

Big ideas: EXACT

### 12.1 Atomic structure



- ● **CO-12.1.A** (usnco:8) Identify a group from successive ionisation energies.
  - EK: The big jump comes after the last valence electron.
  - Needs: CH-1.10.D
  - P1 · drills: co-ionisation-jump, co-jump-position
- ● **CO-12.1.B** (usnco:8) Count electrons with given quantum numbers.
  - EK: Each orbital holds 2; there are 2l + 1 orbitals per subshell and n² per shell.
  - Needs: CO-12.1.A
  - P1 · drills: co-quantum-count, co-max-electrons
- ● **CO-12.1.C** (usnco:8) Explain anomalies in periodic trends.
  - EK: Half-filled and filled subshells resist adding or removing electrons.
  - Needs: CO-12.1.B
  - P1 · drills: co-trend-anomaly, co-anomaly-explain
- ● **CO-12.1.D** (usnco:8) Find the wavelength of a hydrogen transition.
  - EK: 1/λ = R_H(1/n₁² − 1/n₂²), R_H = 1.097×10⁷ m⁻¹.
  - Needs: CO-12.1.C
  - P1 · drills: co-hydrogen-line, co-series-limit
- ● **CO-12.1.E** (usnco:8) Count unpaired electrons in a transition-metal ion.
  - EK: Remove s electrons first, then put the d electrons into five orbitals by Hund's rule (free ion).
  - Needs: CO-12.1.D
  - P1 · drills: co-unpaired-ion, co-ion-moment
- ● **CO-12.1.F** (usnco:8) Predict a radioactive decay mode.
  - EK: Neutron-rich nuclides β⁻ decay; proton-rich ones β⁺ or capture electrons; very heavy ones α decay.
  - Needs: CO-12.1.E
  - P1 · drills: co-decay-mode, co-daughter-z

## Unit 13 · USNCO band 9: bonding and molecular structure

Big ideas: EXACT

### 13.1 Bonding and structure



- ● **CO-13.1.A** (usnco:9) Predict a VSEPR shape including lone pairs.
  - EK: Count electron domains, then name the shape from the atoms only.
  - Needs: CH-2.8.A
  - P1 · drills: co-vsepr-shape, co-lone-pairs-centre
- ● **CO-13.1.B** (usnco:9) Count the stereoisomers of an octahedral complex.
  - EK: Enumerate arrangements up to rotation; mirror images count separately.
  - Needs: CO-13.1.A
  - P1 · drills: co-octahedral-isomers, co-square-planar-isomers
- ● **CO-13.1.C** (usnco:9) Find a bond order from a molecular-orbital diagram.
  - EK: Bond order = (bonding − antibonding)/2.
  - Needs: CO-13.1.B
  - P1 · drills: co-mo-bond-order, co-mo-unpaired
- ● **CO-13.1.D** (usnco:9) Choose the most stable resonance arrangement or isomer by formal charge.
  - EK: Prefer formal charges near zero, with negative charge on the more electronegative atom.
  - Needs: CO-13.1.C
  - P1 · drills: co-formal-charge, co-formal-charge-atom
- ● **CO-13.1.E** (usnco:9) Find a fractional bond order from resonance.
  - EK: Spread the π bonds over the equivalent positions: bond order = total bonds / positions.
  - Needs: CO-13.1.D
  - P1 · drills: co-resonance-bond-order, co-bond-length-rank

## Unit 14 · USNCO band 10: organic chemistry, biochemistry and spectroscopy

Big ideas: EXACT

### 14.1 Organic and biochemistry



- ● **CO-14.1.A** (usnco:10) Count structural isomers.
  - EK: Enumerate chains, then branches; include rings when the formula allows.
  - P1 · drills: co-isomer-count, co-isomer-count-2
- ● **CO-14.1.B** (usnco:10) Find the degree of unsaturation.
  - EK: DoU = (2C + 2 + N − H − X)/2: rings plus π bonds.
  - Needs: CO-14.1.A
  - P1 · drills: co-unsaturation, co-h-from-dou
- ● **CO-14.1.C** (usnco:10, acs-accm-analytical:I.B.1, acs-accm-analytical:II.F.1, acs-accm-analytical:III.F.1) Assign an infrared band.
  - EK: O–H broad 3200–3550; C=O sharp near 1700; C≡N near 2250; C–H just below 3000 (sp³) or above (sp²).
  - Needs: CO-14.1.B
  - P1 · drills: co-ir-band, co-ir-tell
- ● **CO-14.1.D** (usnco:10, acs-accm-organic:III.D.2, acs-accm-analytical:I.A.3, acs-accm-analytical:III.D.1) Count ¹H NMR environments.
  - EK: Equivalent hydrogens (by symmetry) give one signal.
  - Needs: CO-14.1.C
  - P1 · drills: co-nmr-environments, co-nmr-env-2
- ● **CO-14.1.E** (usnco:10) Identify the monomer of a polymer.
  - EK: Addition polymers repeat the alkene's carbons; condensation polymers lose a small molecule at each link.
  - Needs: CO-14.1.D
  - P1 · drills: co-monomer, co-polymer-from-monomer
- ● **CO-14.1.F** (usnco:10) Find an amino acid's isoelectric point.
  - EK: pI is the average of the two pKa values on either side of the neutral form.
  - Needs: CO-14.1.E
  - P1 · drills: co-isoelectric, co-glycine-charge

## Unit 15 · USNCO Part II: multi-step problems

Big ideas: EXACT

### 15.1 Linked problems



- ● **CO-15.1.A** (usnco:P2, usnco:6) Find a molar solubility with a common ion, then compare it with pure water.
  - EK: Ksp = s(s + c) ≈ s c when c ≫ s.
  - Needs: CO-5.1.E, CO-8.1.E, CO-10.1.E, CO-11.1.E
  - P1 · drills: co-p2-common-ion, co-ksp-from-common-ion
- ● **CO-15.1.B** (usnco:P2, usnco:7) Get ΔS° of a cell reaction from the temperature dependence of E°.
  - EK: ΔS° = nF(dE°/dT); ΔH° = ΔG° + TΔS°.
  - Needs: CO-15.1.A
  - P1 · drills: co-p2-cell-entropy, co-dedt-from-ds
- ● **CO-15.1.C** (usnco:P2, usnco:4) Find ΔS° from ΔG° and calorimetric ΔH°.
  - EK: ΔG° = −RT ln K; ΔS° = (ΔH° − ΔG°)/T.
  - Needs: CO-15.1.B
  - P1 · drills: co-p2-entropy-from-k, co-vant-hoff-k
- ● **CO-15.1.D** (usnco:P2, usnco:1) Find a hydrate's water count from an iodometric titration.
  - EK: Cu²⁺ + I⁻ → CuI + ½I₂; I₂ + 2 S₂O₃²⁻: one thiosulfate per Cu.
  - Needs: CO-15.1.C
  - P1 · drills: co-p2-iodometric, co-iodometric-copper
- ● **CO-15.1.E** (usnco:P2, usnco:3) Find a density and an oxidation state from a perovskite unit cell.
  - EK: ABO₃: A at the corners (1), B at the centre (1), O at the face centres (3).
  - Needs: CO-15.1.D
  - P1 · drills: co-p2-perovskite, co-tolerance-factor
- ● **CO-15.1.F** (usnco:P2, usnco:8) Find a photon energy per mole for bond breaking.
  - EK: E = N_A hc/λ.
  - Needs: CO-15.1.E
  - P1 · drills: co-p2-photon-kj, co-threshold-wavelength

## Unit 16 · Camp-level steps (extension)

Big ideas: EXACT, COUNT

### 16.1 Electrochemical and equilibrium steps



- ● **CO-16.1.A** (usnco:P2, usnco:7) Read the number of electrons transferred from an electrode's slope per decade.
  - EK: At 25 °C a Nernstian electrode moves 59.16/n mV for each tenfold change in concentration, so the slope gives n before any chemistry is assumed.
  - Needs: CO-1.2.B, CO-2.2.B, CO-3.1.B
  - P1 · drills: co-slope-electrons, co-decade-shift
- ● **CO-16.1.B** (usnco:P2, usnco:6) Find an acid's K_a from the shift in an ion-selective electrode's potential with pH.
  - EK: The electrode sees only the free anion; the shift from its strong-base reading gives the free fraction α = 10^(−ΔE/59.16), and K_a = [H⁺]α/(1 − α).
  - Needs: CO-16.1.A
  - P1 · drills: co-ka-from-shift, co-free-fraction
- ● **CO-16.1.C** (usnco:P2, usnco:6) Find the solubility of two sparingly soluble salts of weak acids sharing a cation.
  - EK: The cation balances both anions in all their forms: [M⁺]² = K_spA(1 + [H⁺]/K_A) + K_spB(1 + [H⁺]/K_B).
  - Needs: CO-16.1.B
  - P1 · drills: co-two-salt-solubility, co-two-salt-ratio
- ● **CO-16.1.D** (usnco:P2, usnco:1) Find two anions from the successive end points of one silver titration.
  - EK: Cyanide first takes silver as Ag(CN)₂⁻ (one Ag⁺ per two CN⁻), then precipitates as AgCN, and only then does chloride precipitate, so the volumes between end points count each anion.
  - Needs: CO-16.1.C
  - P1 · drills: co-cyanide-first-endpoint, co-chloride-third-endpoint
- ● **CO-16.1.E** (usnco:P2, usnco:7) Find the cell emf at the equivalence point of a precipitation titration.
  - EK: At the equivalence point of a 1:1 salt [Ag⁺] = √K_sp, and the silver electrode reads E° + 0.05916 log[Ag⁺] against the reference.
  - Needs: CO-16.1.D
  - P1 · drills: co-equivalence-emf, co-silver-from-emf

### 16.2 Solids, rates and stoichiometric steps



- ● **CO-16.2.A** (usnco:P2, usnco:3) Find the vacancy fraction of a nonstoichiometric oxide from the share of cations oxidised.
  - EK: With the anion lattice intact, charge balance fixes the cation count: for Cu₂₋ₓO with a fraction f of copper as Cu²⁺, (2 − x)(1 + f) = 2.
  - Needs: CO-16.1.E
  - P1 · drills: co-vacancy-x, co-vacancy-percent
- ● **CO-16.2.B** (usnco:P2, usnco:4) Find the temperature at which two solid phases exchange stability from formation data.
  - EK: Build ΔH° and ΔS° of the interconversion from the formation values, then T = ΔH°/ΔS°; with three phases, each pair has its own boundary.
  - Needs: CO-16.2.A
  - P1 · drills: co-phase-boundary, co-phase-dg
- ● **CO-16.2.C** (usnco:P2, usnco:5) Find a rate constant from the time a limiting reagent takes to vanish at constant rate.
  - EK: A straight concentration–time line means zero order in the limiting reagent: the rate is its initial concentration over the reaction time, and the other species give the rate law.
  - Needs: CO-16.2.B
  - P1 · drills: co-reaction-time-rate, co-reaction-time-k
- ● **CO-16.2.D** (usnco:P2, usnco:5) Find the overall activation energy of a chain reaction from its composite rate constant.
  - EK: Activation energies combine the way the rate constants do: a product adds them, a quotient subtracts them, and a square root halves them.
  - Needs: CO-16.2.C
  - P1 · drills: co-composite-ea, co-composite-ea-half
- ● **CO-16.2.E** (usnco:P2, usnco:1) Identify the metal of a chloride hydrate from a silver titration.
  - EK: Silver counts chloride; mass per mole of chloride times the chlorides per formula is the formula mass, and what is left after chloride and water is the metal.
  - Needs: CO-16.2.D
  - P1 · drills: co-hydrate-metal, co-mass-per-chloride

### 16.3 Inorganic steps



- ● **CO-16.3.A** (usnco:P2, usnco:9) Count valence electrons of carbonyl and nitrosyl complexes and spot the 17-electron ones.
  - EK: Neutral counting: the metal's group number, two per CO, three per linear NO, minus the charge. Seventeen-electron fragments either dimerise through a metal–metal bond or are easily reduced.
  - Needs: CO-16.2.E
  - P1 · drills: co-carbonyl-count, co-nitrosyl-count
- ● **CO-16.3.B** (usnco:P2, usnco:9) Find the metal–metal bonds a carbonyl cluster needs and say what light does to them.
  - EK: Metal–metal bonds = (18 × metals − total electrons)/2. The M–M σ bond is the weakest in the molecule, and UV light promotes σ → σ*, breaking it into two 17-electron radicals.
  - Needs: CO-16.3.A
  - P1 · drills: co-metal-metal-bonds, co-metal-metal-light
- ● **CO-16.3.C** (usnco:P2, usnco:2) Predict the chemistry of nitrogen fluorides: where they form, what stabilises NF₄⁺ and how it hydrolyses.
  - EK: Fluorination is an oxidation, so NF₃ forms at the anode; NF₄⁺ needs a strong fluoride acceptor to hold the counter-ion, and with water it gives back NF₃ and oxidises water to O₂.
  - Needs: CO-16.3.B
  - P1 · drills: co-nitrogen-fluorides, co-nf4-oxygen
- ● **CO-16.3.D** (usnco:P2, usnco:2) Write the products of reactions that are not simple exchange: disproportionation, hydrolysis and redox in base.
  - EK: Copper(I) disproportionates in non-complexing acid, acyl chlorides hydrolyse to HCl and the acid (oxalyl chloride falls apart to CO and CO₂), and permanganate in strong base stops at green manganate.
  - Needs: CO-16.3.C
  - P1 · drills: co-not-simple-exchange, co-disproportionation-mass

### 16.4 Organic steps



- ● **CO-16.4.B** (usnco:P2, usnco:10) Rank substituents by the CIP rules and assign R or S.
  - EK: Rank by atomic number at the first point of difference, counting multiple bonds as duplicated atoms; with the lowest group pointing away, 1 → 2 → 3 clockwise is R.
  - Needs: CO-16.3.D
  - P1 · drills: co-cip-priority, co-r-or-s
- ● **CO-16.4.C** (usnco:P2, usnco:10) Read a Fischer projection: its geometry, what moves are allowed, and D or L.
  - EK: Horizontal bonds come toward the viewer and vertical bonds go back. A 180° turn in the plane keeps the configuration; swapping two groups inverts it. D means the OH on the highest-numbered stereocentre is on the right.
  - Needs: CO-16.4.B
  - P1 · drills: co-fischer-rules, co-fischer-r-or-s
- ● **CO-16.4.A** (usnco:P2, usnco:10) Work back from ozonolysis fragments to the alkene.
  - EK: Each C=C carbon becomes a carbonyl: with oxidative work-up =CH– gives an acid, =C< a ketone and =CH₂ carbon dioxide. One fragment carrying both carbonyls means the double bond was in a ring.
  - Needs: CO-16.4.C
  - P1 · drills: co-ozonolysis-back, co-ozonolysis-carbons
- ● **CO-16.4.D** (usnco:P2, usnco:10) Predict the product of a Birch reduction and where a substituent ends up.
  - EK: Sodium in liquid ammonia with an alcohol gives the non-conjugated 1,4-diene. An electron-donating group ends on a double-bond carbon, an electron-withdrawing group on an sp³ carbon.
  - Needs: CO-16.4.A
  - P1 · drills: co-birch, co-birch-sodium
- ● **CO-16.4.E** (usnco:P2, usnco:10) Carry phenol to aspirin and say why each step goes where it does.
  - EK: Phenoxide, not phenol, is nucleophilic enough to attack CO₂ (Kolbe–Schmitt), giving the ortho acid on acidification; acetic anhydride then acetylates the phenol oxygen.
  - Needs: CO-16.4.D
  - P1 · drills: co-phenol-to-aspirin, co-aspirin-yield
