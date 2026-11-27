# Physical Chemistry — curriculum framework (draft 1)

Generated from `drills/frameworks/physical-chemistry.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**158 learning objectives** in 22 units (158 core): 156 drilled, 2 partly, 0 with no drills. Core: 156 / 158 drilled.

## Big ideas

- **ENERGY · Energy is conserved and state functions don't care about the path.** Heat and work depend on how a change is carried out; U and H depend only on where it starts and ends. That is what lets one measured path stand in for another.
- **SPONT · Entropy decides direction, Gibbs energy keeps the books.** A process goes when the entropy of the universe rises. At constant T and P that is the same as ΔG < 0, and every equilibrium (phase, solution, reaction, cell) is the point where G stops falling.
- **QUANT · Confinement quantises energy.** A particle held in a region can only have certain energies. The box, the oscillator, the rotor and the hydrogen atom are the same idea with different potentials, and the wavefunction holds everything that can be known.
- **SPEC · Spectra are energy-level spacings made visible.** Each kind of spectroscopy reads one kind of spacing (rotational, vibrational, electronic, nuclear spin), and selection rules and symmetry say which transitions appear.
- **STAT · Bulk properties are Boltzmann-weighted averages over quantum states.** The partition function counts the states that are thermally reachable. Every thermodynamic quantity is a derivative of its logarithm.
- **RATE · Rates come from molecular motion and barriers.** How fast molecules move, how often they collide and how high the barrier is set transport coefficients and rate constants; mechanisms are built from elementary steps.

## Practices

- **P1 · Define the system and the process.** Say what is held constant (T, P, V, composition), what crosses the boundary, and which state the system starts and ends in.
- **P2 · Choose the model.** Ideal or real gas, ideal or real solution, box, oscillator or rotor, steady state or pre-equilibrium, and say when the choice stops being good.
- **P3 · Compute with units.** SI throughout, kelvin always, J against kJ, per molecule against per mole, wavelength against wavenumber against frequency.
- **P4 · Manipulate the mathematics.** Take the derivative, do the integral, apply the operator, sum the series.
- **P5 · Check and interpret.** Sign, size, limiting cases, and what the number says about the molecules.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Gases, work, heat and the first law | core | — | 8 | 8 | 0 | 0 |
| 2 · Thermochemistry | core | — | 3 | 3 | 0 | 0 |
| 3 · Entropy and the second and third laws | core | — | 5 | 5 | 0 | 0 |
| 4 · Gibbs energy and chemical equilibrium | core | — | 5 | 5 | 0 | 0 |
| 5 · Real gases | core | — | 4 | 4 | 0 | 0 |
| 6 · Phase equilibria of pure substances | core | — | 7 | 7 | 0 | 0 |
| 7 · Ideal and real solutions | core | — | 7 | 7 | 0 | 0 |
| 8 · Electrolyte solutions | core | — | 4 | 4 | 0 | 0 |
| 9 · Electrochemical cells | core | — | 4 | 4 | 0 | 0 |
| 10 · From classical to quantum mechanics | core | — | 5 | 5 | 0 | 0 |
| 11 · The Schrödinger equation and the postulates | core | — | 8 | 8 | 0 | 0 |
| 12 · Model systems: box, oscillator and rotor | core | — | 12 | 12 | 0 | 0 |
| 13 · Vibrational and rotational spectroscopy | core | — | 6 | 6 | 0 | 0 |
| 14 · The hydrogen atom and many-electron atoms | core | — | 10 | 9 | 1 | 0 |
| 15 · Chemical bonding and computational chemistry | core | — | 12 | 11 | 1 | 0 |
| 16 · Electronic spectroscopy | core | — | 5 | 5 | 0 | 0 |
| 17 · Molecular symmetry | core | — | 6 | 6 | 0 | 0 |
| 18 · Nuclear magnetic resonance | core | — | 5 | 5 | 0 | 0 |
| 19 · Probability and the Boltzmann distribution | core | — | 6 | 6 | 0 | 0 |
| 20 · Partition functions and statistical thermodynamics | core | — | 11 | 11 | 0 | 0 |
| 21 · Kinetic theory of gases and transport | core | — | 9 | 9 | 0 | 0 |
| 22 · Chemical kinetics | core | — | 16 | 16 | 0 | 0 |

## Unit 1 · Gases, work, heat and the first law

Big ideas: ENERGY

### 1.1 The ideal gas as a reference state

Book: engel-reid-3e §1.4

- ● **PC-1.1.A** (webwork-opl:TH2.12, webwork-opl:TH12.2, acs-accm-pchem:IV.A.4, acs-accm-pchem:VI.G.4, acs-accm-pchem:X.A.3, acs-accm-pchem:X.D.5) Calculate the pressure, volume, amount or temperature of an ideal gas from the other three.
  - EK: PV = nRT with T in kelvin; R = 8.314 J/mol·K = 0.08314 L·bar/mol·K.
  - Needs: CH-3.4.D, CH-6.10.B, PH-9.4.D, CA-12.2.B
  - P3 · drills: pc-gas-density, pc-ideal-gas

### 1.2 Work and heat along a path

Book: engel-reid-3e §2.8, §2.8, §2.5, §3.4, §2.11

- ● **PC-1.2.A** (webwork-opl:TH1.11, webwork-opl:TH1.12, acs-accm-pchem:VI.G.6, acs-accm-pchem:VI.G.3) Calculate the work of an expansion or compression against a constant external pressure.
  - EK: w = −P_ext ΔV; work done on the system is positive, so expansion gives w < 0.
  - Needs: PC-1.1.A
  - P3 · drills: pc-volume-from-work, pc-work-irrev
- ● **PC-1.2.B** (webwork-opl:TH1.12, acs-accm-pchem:VI.G.3, acs-accm-pchem:VI.G.6, acs-accm-pchem:VI.G.2) Calculate the work and heat of a reversible isothermal expansion of an ideal gas.
  - EK: w = −nRT ln(V₂/V₁); ΔU = 0 for an ideal gas at constant T, so q = −w.
  - Needs: PC-1.2.A
  - P3 · drills: th-fl-isothermal, sc-isothermal-work-ratio
- ● **PC-1.2.C** (webwork-opl:TH1.9, webwork-opl:TH2.10, acs-accm-pchem:VI.G.7, acs-accm-pchem:VI.G.2) Calculate the heat and internal-energy change for heating at constant volume.
  - EK: q_V = ΔU = nC_V ΔT; no P–V work is done.
  - Needs: PC-1.2.B
  - P3 · drills: td-isochoric-pressure, th-fl-isochoric
- ● **PC-1.2.D** (webwork-opl:TH1.10, webwork-opl:TH2.11, webwork-opl:TH2.14, acs-accm-pchem:VI.G.8) Calculate the heat and enthalpy change for heating at constant pressure.
  - EK: q_P = ΔH = nC_P ΔT; C_P − C_V = R for an ideal gas.
  - Needs: PC-1.2.C
  - P3 · drills: td-isobaric-dh, th-fl-isobaric
- ● **PC-1.2.E** (webwork-opl:TH7.16, acs-accm-pchem:VI.G.3, acs-accm-pchem:VI.G.5) Calculate the final temperature and the work of a reversible adiabatic expansion.
  - EK: T₁V₁^(γ−1) = T₂V₂^(γ−1) with γ = C_P/C_V; q = 0, so w = ΔU = nC_V ΔT.
  - Needs: PC-1.2.D
  - P3 · drills: td-adiabatic-work, th-fl-adiabatic

### 1.3 Enthalpy and internal energy

Book: engel-reid-3e §2.9

- ● **PC-1.3.B** (acs-accm-pchem:VI.A.1, acs-accm-pchem:VI.A.2, acs-accm-pchem:VI.A.3, acs-accm-pchem:VI.B.2, acs-accm-pchem:VI.G.10) Keep first-law books: choose the system, sign q and w, and find ΔU.
  - EK: ΔU = q + w with q > 0 into the system and w > 0 done on it; open, closed and isolated systems differ in what crosses; thermodynamics is silent on rates.
  - Needs: PC-1.2.E
  - P1 · drills: pc-system-types, pc-du-signs
- ● **PC-1.3.A** (webwork-opl:TH1.10, acs-accm-pchem:VI.G.8, acs-accm-pchem:VI.G.7) Convert between ΔH and ΔU for a process that changes the moles of gas.
  - EK: ΔH = ΔU + Δn_gas RT; condensed phases contribute almost nothing to Δ(PV).
  - Needs: PC-1.3.B
  - P3 · drills: pc-du-from-dh, pc-dh-du

## Unit 2 · Thermochemistry

Big ideas: ENERGY

### 2.1 Reaction enthalpies

Book: engel-reid-3e §4.2, §4.3, §4.4

- ● **PC-2.1.A** (webwork-opl:TH13.5, acs-accm-pchem:VI.A.4, acs-accm-pchem:VI.G.7, acs-accm-pchem:VI.G.8) Convert a constant-volume (bomb calorimeter) reaction energy into a reaction enthalpy.
  - EK: A bomb measures q_V = ΔU; ΔH = ΔU + Δn_gas RT, with Δn counted from the balanced equation.
  - Needs: PC-1.3.A, CH-6.9.A
  - P3 · drills: pc-bomb-calorimeter, ~pc-dh-du
- ● **PC-2.1.B** (webwork-opl:TH13.3, webwork-opl:TH13.4, acs-accm-pchem:VI.G.9, acs-accm-pchem:VI.D.1, acs-accm-pchem:IV.E.4) Calculate a standard reaction enthalpy from standard enthalpies of formation.
  - EK: ΔH°_rxn = Σ ν ΔH°_f(products) − Σ ν ΔH°_f(reactants); elements in their standard states are zero.
  - Needs: PC-2.1.A
  - P3 · drills: pc-hess-combine, pc-hess
- ● **PC-2.1.C** (acs-accm-pchem:VI.G.5, acs-accm-pchem:VI.G.9) Correct a reaction enthalpy to a different temperature with Kirchhoff's law.
  - EK: ΔH(T₂) = ΔH(T₁) + ΔC_P (T₂ − T₁) when ΔC_P is constant over the range.
  - Needs: PC-2.1.B
  - P3 · drills: pc-dcp-from-two, pc-kirchhoff

## Unit 3 · Entropy and the second and third laws

Big ideas: SPONT

### 3.1 Heat engines

Book: engel-reid-3e §5.2

- ● **PC-3.1.A** (webwork-opl:TH6.6, acs-accm-pchem:VI.F.1, acs-accm-pchem:VI.F.2, acs-accm-pchem:VI.H.4) Calculate the efficiency of a Carnot engine and the work it delivers from a given heat input.
  - EK: η = 1 − T_C/T_H = w/q_H, temperatures in kelvin; no engine between the same reservoirs does better.
  - Needs: PC-1.3.A, CH-9.2.A
  - P3 · drills: pc-carnot-rejected, pc-carnot

### 3.2 Entropy changes

Book: engel-reid-3e §5.4, §5.4, §5.4, §5.10

- ● **PC-3.2.A** (webwork-opl:TH7.10, acs-accm-pchem:VI.H.2, acs-accm-pchem:VI.H.3) Calculate the entropy change of an ideal gas that expands isothermally.
  - EK: ΔS = nR ln(V₂/V₁) = nR ln(P₁/P₂); a state function, so the path need not be reversible.
  - Needs: PC-3.1.A
  - P3 · drills: pc-volume-from-ds, pc-ds-expansion
- ● **PC-3.2.B** (webwork-opl:TH7.10, acs-accm-pchem:VI.H.2) Calculate the entropy change for heating at constant pressure.
  - EK: ΔS = nC_P ln(T₂/T₁) for constant C_P; kelvin inside the logarithm.
  - Needs: PC-3.2.A
  - P3 · drills: pc-temperature-from-ds, pc-ds-heating
- ● **PC-3.2.C** (webwork-opl:TH7.8, acs-accm-pchem:VI.H.2, acs-accm-pchem:IV.D.1) Calculate the entropy change of a phase transition at its transition temperature.
  - EK: ΔS_tr = ΔH_tr/T_tr; Trouton's rule puts ΔS_vap near 85–88 J/mol·K for many liquids.
  - Needs: PC-3.2.B
  - P3 · drills: pc-trouton-boiling, pc-ds-phase
- ● **PC-3.2.D** (webwork-opl:TH13.12, acs-accm-pchem:VI.H.7, acs-accm-pchem:III.H.3, acs-accm-general:VI.H.3) Calculate a standard reaction entropy from absolute molar entropies.
  - EK: ΔS°_rxn = Σ ν S°(products) − Σ ν S°(reactants); the third law fixes S° on an absolute scale.
  - Needs: PC-3.2.C
  - P2 · P5 · drills: pc-reaction-entropy-t, pc-reaction-entropy

## Unit 4 · Gibbs energy and chemical equilibrium

Big ideas: SPONT

### 4.1 Gibbs energy

Book: engel-reid-3e §6.1, §6.3

- ● **PC-4.1.A** (webwork-opl:TH13.15, acs-accm-pchem:VI.H.6, acs-accm-pchem:VI.H.1) Calculate ΔG from ΔH and ΔS and decide whether a process is spontaneous at a given temperature.
  - EK: ΔG = ΔH − TΔS; spontaneous at constant T and P when ΔG < 0; the sign flips at T = ΔH/ΔS.
  - Needs: PC-2.1.C, PC-3.2.D, CH-9.5.C, CH-7.3.B
  - P3 · drills: pc-crossover-t, pc-dg
- ● **PC-4.1.B** (acs-accm-pchem:VI.H.6, acs-accm-pchem:VI.G.5) Calculate the change in Gibbs energy of an ideal gas with pressure.
  - EK: G(P) = G° + nRT ln(P/P°), so ΔG = nRT ln(P₂/P₁) at constant T.
  - Needs: PC-4.1.A
  - P3 · drills: pc-pressure-for-dg, pc-g-pressure

### 4.2 The equilibrium constant

Book: engel-reid-3e §6.7, §6.10

- ● **PC-4.2.C** (acs-accm-pchem:V.A.1, acs-accm-pchem:V.A.2, acs-accm-pchem:VIII.A.1, acs-accm-pchem:VIII.B.2, acs-accm-pchem:VIII.G.1) Use the extent of reaction and convert between chemical and biochemical standard states.
  - EK: nᵢ = nᵢ⁰ + νᵢξ; ΔG°′ (pH 7) = ΔG° + ν(H⁺)·RT ln 10⁻⁷ for a reaction producing ν protons.
  - Needs: PC-4.1.B
  - P1 · drills: pc-extent, pc-biochem-standard
- ● **PC-4.2.A** (webwork-opl:TH13.2, acs-accm-pchem:VIII.F.2, acs-accm-pchem:VIII.D.1, acs-accm-pchem:VIII.D.2, acs-accm-pchem:VIII.C.1) Calculate an equilibrium constant from a standard reaction Gibbs energy, and the reverse.
  - EK: ΔG° = −RT ln K; a negative ΔG° gives K > 1.
  - Needs: PC-4.2.C
  - P3 · drills: td-k-temperature-free, th-ce-k
- ● **PC-4.2.B** (acs-accm-pchem:VIII.E.2, acs-accm-pchem:VIII.E.1) Calculate how an equilibrium constant shifts with temperature using the van't Hoff equation.
  - EK: ln(K₂/K₁) = −(ΔH°/R)(1/T₂ − 1/T₁); K rises with T for an endothermic reaction.
  - Needs: PC-4.2.A
  - P3 · drills: th-ce-vant-hoff, sc-equilibrium-constant-temperature

## Unit 5 · Real gases

Big ideas: ENERGY

### 5.1 Departures from ideality

Book: engel-reid-3e §7.3, §7.2, §7.4, §7.5

- ● **PC-5.1.A** (webwork-opl:TH2.15, acs-accm-pchem:IV.A.5, acs-accm-pchem:IV.A.2) Calculate the compression factor of a gas and say whether attraction or repulsion dominates.
  - EK: Z = PV_m/RT; Z < 1 means attractions dominate, Z > 1 repulsions.
  - Needs: PC-1.3.A, CH-3.6.A
  - P3 · drills: pc-volume-from-z, pc-compression-z
- ● **PC-5.1.B** (webwork-opl:TH15.5, acs-accm-pchem:IV.A.5, acs-accm-pchem:IV.A.2) Calculate the pressure of a gas from the van der Waals equation.
  - EK: P = RT/(V_m − b) − a/V_m²; b is excluded volume, a measures attraction.
  - Needs: PC-5.1.A
  - P3 · drills: pc-boyle-vdw, pc-vdw
- ● **PC-5.1.C** (webwork-opl:TH15.6, acs-accm-pchem:IV.A.5, acs-accm-pchem:IV.D.7) Calculate reduced variables and use corresponding states to compare gases.
  - EK: T_r = T/T_c, P_r = P/P_c; gases at the same reduced state have about the same Z.
  - Needs: PC-5.1.B
  - P2 · P5 · drills: pc-vdw-critical-t, pc-reduced-temperature
- ● **PC-5.1.D** (webwork-opl:TH15.10, acs-accm-pchem:VIII.C.3, acs-accm-pchem:IV.D.1) Calculate a fugacity from a fugacity coefficient and relate it to chemical potential.
  - EK: f = φP; μ = μ° + RT ln(f/P°); φ → 1 as P → 0.
  - Needs: PC-5.1.C
  - P2 · P5 · drills: pc-mu-from-phi, pc-fugacity-potential

## Unit 6 · Phase equilibria of pure substances

Big ideas: SPONT

### 6.1 Phase diagrams

Book: engel-reid-3e §8.3, §8.6, §8.8

- ● **PC-6.1.D** (acs-accm-pchem:IV.A.1, acs-accm-pchem:IV.A.2, acs-accm-pchem:IV.A.3, acs-accm-pchem:IV.C.2, acs-accm-pchem:IV.C.3, acs-accm-pchem:IV.C.5) Read a Lennard-Jones potential and scale dispersion energies with distance and polarisability.
  - EK: V = 4ε[(σ/r)¹² − (σ/r)⁶]: zero at σ, minimum −ε at 2^(1/6)σ; London energy ∝ −α₁α₂/r⁶.
  - Needs: PC-4.2.B, CH-6.5.B
  - P1 · drills: pc-lj-minimum, pc-london-scale
- ● **PC-6.1.E** (acs-accm-pchem:IV.C.1, acs-accm-pchem:IV.C.4, acs-accm-pchem:IV.C.6, acs-accm-pchem:IV.C.7, acs-accm-pchem:IV.B.1, acs-accm-pchem:IV.B.2, acs-accm-pchem:IV.B.3, acs-accm-pchem:IV.E.3) Classify the interactions between molecules and inside biomolecules, and how they scale with distance.
  - EK: Ion–ion ∝ 1/r, ion–dipole 1/r², dipole–dipole (fixed) 1/r³, rotating dipoles and dispersion 1/r⁶; the hydrophobic effect drives folding and micelles.
  - Needs: PC-6.1.D
  - P1 · drills: pc-imf-type, pc-dipole-scale
- ● **PC-6.1.F** (acs-accm-pchem:IX.A.1, acs-accm-pchem:III.H.2, acs-accm-pchem:III.H.4, acs-accm-pchem:II.G.1, acs-accm-general:II.G.2, acs-accm-inorganic:II.G.2, acs-accm-inorganic:X.A.2, acs-accm-analytical:III.H.1) Use Bragg's law and cubic lattice spacings, and explain conduction in metals and semiconductors by bands.
  - EK: nλ = 2d sin θ; cubic d_hkl = a/√(h² + k² + l²); a band gap sets whether a solid conducts.
  - Needs: PC-6.1.E
  - P1 · drills: pc-bragg, pc-bands
- ● **PC-6.1.G** (acs-accm-pchem:V.F.2, acs-accm-pchem:IX.C.2, acs-accm-inorganic:III.H.4, acs-accm-inorganic:X.A.1) Estimate the share of atoms at a nanoparticle's surface and explain size-dependent properties.
  - EK: Fraction in an outer shell of thickness t: 1 − (1 − t/R)³; small particles melt lower, and quantum dots absorb at shorter wavelength as they shrink.
  - Needs: PC-6.1.F
  - P1 · drills: pc-surface-fraction, pc-nanoscale
- ● **PC-6.1.A** (webwork-opl:TH2.1, acs-accm-pchem:VIII.F.1, acs-accm-pchem:IV.D.2, acs-accm-pchem:X.D.1) Apply the Gibbs phase rule to count the degrees of freedom of a system.
  - EK: F = C − P + 2; a pure substance at its triple point has F = 0.
  - Needs: PC-6.1.G
  - P3 · drills: pc-max-phases, pc-phase-rule
- ● **PC-6.1.B** (webwork-opl:TH15.3, acs-accm-pchem:IV.D.5, acs-accm-pchem:IV.D.3) Calculate a vapour pressure, a boiling temperature or an enthalpy of vaporisation from the Clausius–Clapeyron equation.
  - EK: ln(P₂/P₁) = −(ΔH_vap/R)(1/T₂ − 1/T₁); assumes an ideal vapour and constant ΔH_vap.
  - Needs: PC-6.1.A
  - P3 · drills: th-pe-cc-pressure, th-pe-cc-enthalpy, th-pe-cc-temperature, sc-vapour-pressure-ten-degrees
- ● **PC-6.1.C** (acs-accm-pchem:IV.D.4) Calculate the pressure difference across a curved liquid surface.
  - EK: ΔP = 2γ/r for a droplet or a bubble in a liquid; smaller radius, larger excess pressure.
  - Needs: PC-6.1.B
  - P3 · drills: pc-bubble-pressure, pc-laplace-pressure

## Unit 7 · Ideal and real solutions

Big ideas: SPONT

### 7.1 Ideal solutions

Book: engel-reid-3e §9.3, §9.4, §9.5

- ● **PC-7.1.A** (acs-accm-pchem:IV.D.6, acs-accm-pchem:VIII.C.2) Calculate partial and total vapour pressures above an ideal solution.
  - EK: p_i = x_i P_i*; the total is the mole-fraction-weighted sum.
  - Needs: PC-4.2.B, PC-6.1.C, CH-3.7.D
  - P3 · drills: td-bubble-from-dew, th-so-raoult
- ● **PC-7.1.B** (acs-accm-pchem:X.D.1) Apply the lever rule to find the amounts of two phases in a two-phase region.
  - EK: n_α(z − z_α) = n_β(z_β − z); the phase nearer the overall composition is the larger one.
  - Needs: PC-7.1.A
  - P2 · P5 · drills: pc-overall-composition, pc-lever-rule
- ● **PC-7.1.C** (webwork-opl:TH15.9, acs-accm-pchem:VIII.F.1, acs-accm-pchem:VIII.C.2) Use the Gibbs–Duhem equation to relate changes in the chemical potentials of two components.
  - EK: x₁ dμ₁ + x₂ dμ₂ = 0 at constant T and P.
  - Needs: PC-7.1.B
  - P3 · drills: pc-gibbs-duhem-dmu, ~th-fe-gibbs-duhem

### 7.2 Colligative properties

Book: engel-reid-3e §9.7, §9.8

- ● **PC-7.2.A** (webwork-opl:TH18.1, acs-accm-pchem:VIII.F.1) Calculate a boiling-point elevation or freezing-point depression from molality.
  - EK: ΔT_b = K_b m and ΔT_f = K_f m; depends on the amount of solute, not what it is.
  - Needs: PC-7.1.C
  - P3 · drills: pc-molar-mass-freezing, pc-colligative
- ● **PC-7.2.B** (webwork-opl:TH18.1, acs-accm-pchem:VIII.F.1) Calculate an osmotic pressure, or a molar mass from a measured osmotic pressure.
  - EK: Π = cRT with c in mol/m³ (or mol/L with R = 0.08314 L·bar/mol·K).
  - Needs: PC-7.2.A
  - P3 · drills: pc-osmotic-column, pc-osmotic

### 7.3 Real solutions

Book: engel-reid-3e §9.11, §9.12

- ● **PC-7.3.A** (acs-accm-pchem:IV.D.8, acs-accm-pchem:VIII.C.3) Calculate an activity and an activity coefficient from a measured partial pressure.
  - EK: a_i = p_i/P_i* = γ_i x_i; γ > 1 is a positive deviation from Raoult's law.
  - Needs: PC-7.2.B
  - P3 · drills: pc-pressure-from-gamma, ~th-so-activity
- ● **PC-7.3.B** (acs-accm-pchem:IV.D.8) Calculate the partial pressure or solubility of a dilute solute with Henry's law.
  - EK: p_A = k_H x_A; Henry for the dilute solute, Raoult for the solvent.
  - Needs: PC-7.3.A
  - P3 · drills: td-henry-pressure, th-so-henry

## Unit 8 · Electrolyte solutions

Big ideas: SPONT

### 8.1 Ions in solution

Book: engel-reid-3e §10.1, §10.3, §10.4, §10.5

- ● **PC-8.1.A** (webwork-opl:TH18.2, acs-accm-pchem:IV.E.2, acs-accm-analytical:I.G.3) Calculate the ionic strength of an electrolyte solution.
  - EK: I = ½ Σ m_i z_i²; a 1:1 salt gives I = m, a 2:1 salt I = 3m.
  - Needs: PC-7.3.B
  - P3 · drills: pc-molarity-from-i, pc-ionic-strength
- ● **PC-8.1.B** (acs-accm-pchem:IV.E.2, acs-accm-pchem:VIII.C.3) Calculate a mean ionic molality and a mean ionic activity.
  - EK: m_± = (m₊^ν₊ m₋^ν₋)^(1/ν); a_± = γ_± m_±/m°.
  - Needs: PC-8.1.A
  - P2 · P5 · drills: pc-nu-pm-factor, pc-mean-ionic-molality
- ● **PC-8.1.C** (webwork-opl:TH18.2, acs-accm-pchem:IV.E.2, acs-accm-pchem:IV.D.8, acs-accm-analytical:I.G.3, acs-accm-analytical:II.A.1, acs-accm-analytical:IV.A.1) Estimate a mean activity coefficient with the Debye–Hückel limiting law.
  - EK: log₁₀ γ_± = −A|z₊z₋|√I with A = 0.509 in water at 298 K; valid only at low I.
  - Needs: PC-8.1.B
  - P3 · drills: pc-i-from-gamma, pc-debye-huckel
- ● **PC-8.1.D** (acs-accm-pchem:VIII.C.3, acs-accm-pchem:IV.E.2) Calculate the solubility of a sparingly soluble salt, with and without activity corrections.
  - EK: K_sp = a₊a₋ = (γ_± m/m°)² for a 1:1 salt; added inert salt lowers γ_± and raises solubility.
  - Needs: PC-8.1.C
  - P2 · P5 · drills: pc-solubility-ab2, pc-solubility-activity

## Unit 9 · Electrochemical cells

Big ideas: SPONT

### 9.1 Cell potentials

Book: engel-reid-3e §11.5, §11.6, §11.4, §11.7

- ● **PC-9.1.A** (acs-accm-pchem:VI.E.2, acs-accm-pchem:IX.D.3) Calculate a standard cell potential from two standard reduction potentials.
  - EK: E°_cell = E°_cathode − E°_anode; potentials are intensive and are never multiplied by stoichiometric coefficients.
  - Needs: PC-4.2.B, PC-8.1.D, CH-9.9.B
  - P3 · drills: pc-unknown-half, pc-cell-potential
- ● **PC-9.1.B** (acs-accm-pchem:VI.E.2, acs-accm-pchem:VI.C.3) Calculate the standard reaction Gibbs energy from a standard cell potential.
  - EK: ΔG° = −nFE°; a positive E° means a spontaneous cell reaction.
  - Needs: PC-9.1.A
  - P3 · drills: pc-e-from-dg, pc-cell-potential
- ● **PC-9.1.C** (webwork-opl:TH18.3, acs-accm-pchem:VI.E.2, acs-accm-pchem:V.F.1) Calculate a cell potential away from standard conditions with the Nernst equation.
  - EK: E = E° − (RT/nF) ln Q; at 298 K, RT/F = 0.02569 V.
  - Needs: PC-9.1.B
  - P3 · drills: pc-nernst-ratio, pc-nernst
- ● **PC-9.1.D** (acs-accm-pchem:VIII.F.2, acs-accm-pchem:VI.E.2) Calculate an equilibrium constant from a standard cell potential.
  - EK: ln K = nFE°/RT; at equilibrium E = 0 and Q = K.
  - Needs: PC-9.1.C
  - P2 · P5 · drills: pc-e-from-k, pc-cell-equilibrium-constant

## Unit 10 · From classical to quantum mechanics

Big ideas: QUANT

### 10.1 Quantisation and wave–particle duality

Book: engel-reid-3e §12.3, §12.4, §12.5, §12.7

- ● **PC-10.1.E** (acs-accm-pchem:I.G.2, acs-accm-pchem:IX.D.4, acs-accm-pchem:VI.I.1, acs-accm-pchem:I.F.1, acs-accm-organic:I.D.2, acs-accm-analytical:I.G.2, acs-accm-analytical:IX.D.4) Compute mass-spectrometry m/z values and nuclear energies from mass changes.
  - EK: [M + zH]ᶻ⁺ appears at (M + z·1.00728)/z; E = Δm·c², about 931.5 MeV per u.
  - Needs: CH-1.5.B, PH-15.5.A, PH-14.8.A
  - P1 · drills: pc-ms-mz, pc-mass-energy
- ● **PC-10.1.A** (acs-accm-pchem:I.D.1, acs-accm-pchem:IX.D.1) Calculate the energy of a photon, or of n quanta, from a frequency or a wavelength.
  - EK: E = hν = hc/λ; h = 6.626 × 10⁻³⁴ J·s.
  - Needs: PC-10.1.E
  - P3 · drills: pc-photon-rate, pc-photon
- ● **PC-10.1.B** (acs-accm-pchem:I.D.1) Calculate the kinetic energy of a photoelectron and the threshold frequency of a metal.
  - EK: KE = hν − Φ; no electrons below ν₀ = Φ/h however intense the light.
  - Needs: PC-10.1.A
  - P3 · drills: pc-threshold-wavelength, pc-photoelectric
- ● **PC-10.1.C** (acs-accm-pchem:I.B.1) Calculate the de Broglie wavelength of a moving particle.
  - EK: λ = h/p = h/mv; only noticeable when λ is comparable to the size of the system.
  - Needs: PC-10.1.B
  - P3 · drills: pc-voltage-for-wavelength, pc-de-broglie
- ● **PC-10.1.D** (acs-accm-pchem:I.D.3, acs-accm-pchem:I.A.1) Calculate hydrogen energy levels and the wavelength of a transition between them.
  - EK: E_n = −13.6 eV/n²; ΔE = 13.6 eV (1/n₁² − 1/n₂²) = hc/λ.
  - Needs: PC-10.1.C
  - P3 · drills: pc-series-limit, pc-bohr

## Unit 11 · The Schrödinger equation and the postulates

Big ideas: QUANT

### 11.1 Operators and eigenfunctions

Book: engel-reid-3e §13.5, §13.6, §13.7

- ● **PC-11.1.A** (acs-accm-pchem:X.A.2) Test whether a function is an eigenfunction of an operator and find the eigenvalue.
  - EK: Âψ = aψ; applying the operator must return the same function times a constant.
  - Needs: PC-10.1.D, CA-7.2.A
  - P2 · P5 · drills: pc-second-derivative-eigen, qm-eigenvalue
- ● **PC-11.1.B** (acs-accm-pchem:I.B.4) Show that two wavefunctions are orthogonal and normalise a wavefunction.
  - EK: ∫ψ_m*ψ_n dτ = δ_mn; eigenfunctions of a Hermitian operator with different eigenvalues are orthogonal.
  - Needs: PC-11.1.A
  - P2 · P5 · drills: qm-orthogonality, qm-normalization-constant
- ● **PC-11.1.C** (acs-accm-pchem:X.A.2) Expand a function in a complete set of eigenfunctions and compute a coefficient.
  - EK: f = Σ c_n ψ_n with c_n = ∫ψ_n* f dτ.
  - Needs: PC-11.1.B
  - P2 · P5 · drills: pc-expansion-probability, qm-expansion-coefficient

### 11.2 Measurement

Book: engel-reid-3e §14.1, §14.4, §14.5

- ● **PC-11.2.A** (acs-accm-pchem:I.B.4, acs-accm-pchem:X.A.1) Calculate the probability of finding a particle in a region from its wavefunction.
  - EK: P = ∫|ψ|² dτ over the region; the total over all space is 1.
  - Needs: PC-11.1.C
  - P2 · P5 · drills: qm-pib-probability, qm-superposition-probability
- ● **PC-11.2.B** (acs-accm-pchem:X.A.1) Calculate the expectation value of an observable.
  - EK: ⟨A⟩ = ∫ψ*Âψ dτ; equals the eigenvalue when ψ is an eigenfunction of Â.
  - Needs: PC-11.2.A
  - P2 · P5 · drills: pc-x2-expectation, qm-expectation-energy
- ● **PC-11.2.C** (acs-accm-pchem:I.D.5) Write the time dependence of a superposition and say when a probability density changes with time.
  - EK: Each term carries e^(−iE_n t/ħ); a single eigenstate is stationary, a superposition beats at (E_m − E_n)/h.
  - Needs: PC-11.2.B
  - P2 · P5 · drills: pc-beat-period, qm-time-dependence

### 11.3 Commutation and uncertainty

Book: engel-reid-3e §17.1, §17.3

- ● **PC-11.3.A** (acs-accm-pchem:X.A.1) Evaluate a commutator and decide whether two observables can be known together.
  - EK: [x̂, p̂_x] = iħ; observables whose operators commute share eigenfunctions.
  - Needs: PC-11.2.C
  - P2 · P5 · drills: qm-commutator, qm-compatible-observables
- ● **PC-11.3.B** (acs-accm-pchem:I.B.1) Estimate the minimum uncertainty in momentum or position from the uncertainty principle.
  - EK: Δx Δp_x ≥ ħ/2.
  - Needs: PC-11.3.A
  - P3 · drills: pc-min-dx, pc-uncertainty

## Unit 12 · Model systems: box, oscillator and rotor

Big ideas: QUANT

### 12.1 The particle in a box

Book: engel-reid-3e §15.2, §15.2, §15.3, §16.3

- ● **PC-12.1.A** (acs-accm-pchem:X.A.4) Calculate particle-in-a-box energy levels and the wavelength of a transition between them.
  - EK: E_n = n²h²/8mL²; spacing grows with n and shrinks as the box or the mass gets larger.
  - Needs: PC-11.3.B, PH-7.4.A, PH-6.3.B
  - P3 · drills: pc-box-from-wavelength, pc-pib-energy
- ● **PC-12.1.B** (acs-accm-pchem:I.B.4, acs-accm-pchem:X.D.4, acs-accm-inorganic:I.B.1, acs-accm-inorganic:X.D.4) Use the particle-in-a-box wavefunction to locate nodes and compute a probability.
  - EK: ψ_n = √(2/L) sin(nπx/L); n − 1 interior nodes.
  - Needs: PC-12.1.A
  - P2 · P5 · drills: qm-pib-node, qm-pib-probability
- ● **PC-12.1.C** (acs-accm-pchem:X.A.4) Calculate energies and degeneracies for a particle in a three-dimensional box.
  - EK: E = (h²/8m)(n_x²/a² + n_y²/b² + n_z²/c²); a cube makes permutations of the quantum numbers degenerate.
  - Needs: PC-12.1.B
  - P2 · P5 · drills: pc-rect-box-energy, qm-3d-box-degeneracy
- ● **PC-12.1.D** (acs-accm-pchem:X.A.4, acs-accm-pchem:III.A.2) Estimate the absorption wavelength of a conjugated molecule with the free-electron model.
  - EK: Fill levels two electrons at a time; ΔE(HOMO→LUMO) = (2n + 1)h²/8m_eL².
  - Needs: PC-12.1.C
  - P3 · drills: pc-chain-from-color, qm-free-electron-absorption

### 12.2 Finite wells and tunnelling

Book: engel-reid-3e §16.1, §16.5, §16.6

- ● **PC-12.2.A** (acs-accm-pchem:X.A.1) Calculate the decay constant of a wavefunction inside a classically forbidden region.
  - EK: ψ ∝ e^(−κx) with κ = √(2m(V₀ − E))/ħ.
  - Needs: PC-12.1.D
  - P2 · P5 · drills: pc-penetration-depth, qm-tunnelling-decay-constant
- ● **PC-12.2.B** (acs-accm-pchem:X.A.1) Estimate the transmission probability through a barrier.
  - EK: T ≈ e^(−2κL); exponentially sensitive to width, mass and barrier height.
  - Needs: PC-12.2.A
  - P2 · P5 · drills: pc-barrier-width, qm-tunnelling-probability
- ● **PC-12.2.C** (acs-accm-pchem:X.A.1) Compare tunnelling probabilities when the mass or the barrier width changes.
  - EK: Electrons tunnel far more readily than protons; an STM current falls about tenfold per ångström.
  - Needs: PC-12.2.B
  - P2 · P5 · drills: pc-tunnel-height, qm-tunnelling-compare

### 12.3 Vibration and rotation

Book: engel-reid-3e §18.3, §18:rotation-2d, §18.5, §18.6, §18:spherical-harmonics

- ● **PC-12.3.A** (acs-accm-pchem:II.C.2, acs-accm-pchem:II.F.2) Calculate the vibrational frequency, level spacing and zero-point energy of a harmonic oscillator.
  - EK: E_v = (v + ½)hν with ν = (1/2π)√(k/μ); zero-point energy ½hν.
  - Needs: PC-12.2.C
  - P3 · drills: pc-zpe-molar, pc-harmonic
- ● **PC-12.3.B** (acs-accm-pchem:X.A.4) Calculate the energy levels of a particle on a ring.
  - EK: E_m = m²ħ²/2I, m = 0, ±1, ±2, …; all levels except m = 0 are doubly degenerate.
  - Needs: PC-12.3.A
  - P2 · P5 · drills: pc-ring-wavelength, qm-ring-transition
- ● **PC-12.3.C** (acs-accm-pchem:III.A.3) Calculate the moment of inertia, rotational levels and level spacings of a diatomic rigid rotor.
  - EK: E_J = J(J + 1)ħ²/2I with I = μr²; each level is (2J + 1)-fold degenerate.
  - Needs: PC-12.3.B
  - P3 · drills: pc-rotational-line, pc-rigid-rotor
- ● **PC-12.3.D** (acs-accm-pchem:I.B.1) Calculate the magnitude and z-component of an angular momentum from its quantum numbers.
  - EK: |L| = √(J(J + 1)) ħ; L_z = m_J ħ.
  - Needs: PC-12.3.C
  - P2 · P5 · drills: pc-angular-momentum-angle, qm-angular-momentum-magnitude
- ● **PC-12.3.E** (acs-accm-pchem:I.B.1) Identify the eigenvalues of L̂² and L̂_z for a spherical harmonic.
  - EK: L̂²Y_l^m = l(l + 1)ħ²Y_l^m; L̂_zY_l^m = mħY_l^m.
  - Needs: PC-12.3.D
  - P2 · P5 · drills: pc-harmonic-count, qm-spherical-harmonic-eigenvalue

## Unit 13 · Vibrational and rotational spectroscopy

Big ideas: SPEC

### 13.1 Reading diatomic spectra

Book: engel-reid-3e §19.3, §19.4, §19.6, §19:einstein

- ● **PC-13.1.E** (acs-accm-pchem:VII.A.4, acs-accm-pchem:I.A.3, acs-accm-organic:I.A.1, acs-accm-inorganic:I.A.2, acs-accm-analytical:I.B.1, acs-accm-analytical:II.F.1) Predict isotope shifts in vibrational frequencies and estimate a kinetic isotope effect.
  - EK: ν ∝ √(k/μ), so C–D vibrates near ν(C–H)/√2; a primary KIE ≈ exp(Δ(ZPE)/k_BT), about 7 at room temperature for C–H/C–D.
  - Needs: PC-12.3.E
  - P1 · drills: pc-isotope-shift, pc-kie
- ● **PC-13.1.F** (acs-accm-pchem:III.F.2, acs-accm-pchem:III.A.1, acs-accm-inorganic:II.D.2) Assign infrared bands to functional groups and compare stretches by force constant.
  - EK: O–H ≈ 3300 cm⁻¹ (broad), C–H ≈ 2900, C≡N ≈ 2250, C=O ≈ 1700, C–O ≈ 1100; at fixed μ, ν ∝ √k.
  - Needs: PC-13.1.E
  - P1 · drills: pc-ir-group, pc-force-constant-ratio
- ● **PC-13.1.A** (acs-accm-pchem:II.F.2, acs-accm-pchem:I.A.3, acs-accm-pchem:III.A.3) Calculate a vibrational wavenumber from a force constant and reduced mass, and the reverse.
  - EK: ν̃ = (1/2πc)√(k/μ); heavier isotopes shift the band to lower wavenumber.
  - Needs: PC-13.1.F
  - P3 · drills: pc-force-constant, ~pc-harmonic
- ● **PC-13.1.B** (acs-accm-pchem:III.D.2, acs-accm-pchem:III.A.2) Apply selection rules to decide whether a vibration or rotation absorbs.
  - EK: Δv = ±1 with a changing dipole; ΔJ = ±1 with a permanent dipole.
  - Needs: PC-13.1.A
  - P2 · P5 · drills: pc-mode-count, qm-selection-rules
- ● **PC-13.1.C** (acs-accm-pchem:III.A.3, acs-accm-pchem:III.C.2) Calculate a bond length from the spacing of lines in a rotational spectrum.
  - EK: Lines at 2B̃(J + 1), spaced 2B̃, with B̃ = h/8π²cI.
  - Needs: PC-13.1.B
  - P3 · drills: pc-rotational-constant, ~pc-rigid-rotor
- ● **PC-13.1.D** (acs-accm-pchem:I.D.5) Relate the Einstein coefficients for absorption, stimulated emission and spontaneous emission.
  - EK: B₁₂ = B₂₁; A₂₁/B₂₁ = 8πhν³/c³, so spontaneous emission dominates at high frequency.
  - Needs: PC-13.1.C
  - P2 · P5 · drills: pc-spontaneous-ratio, qm-einstein-coefficients

## Unit 14 · The hydrogen atom and many-electron atoms

Big ideas: QUANT

### 14.1 The hydrogen atom

Book: engel-reid-3e §20.3, §20.4, §20:radial-prob

- ● **PC-14.1.A** (acs-accm-pchem:I.A.1, acs-accm-pchem:I.G.1) Calculate hydrogen-like energy levels and ionisation energies.
  - EK: E_n = −13.606 eV Z²/n².
  - Needs: PC-12.3.E, CH-1.9.A, CA-13.7.A
  - P3 · drills: pc-hydrogenlike-transition, qm-hydrogenlike-ionization
- ● **PC-14.1.B** (acs-accm-pchem:I.B.1, acs-accm-pchem:I.C.1) List the allowed quantum numbers and count the orbitals in a shell.
  - EK: l = 0 … n − 1, m_l = −l … l; n² orbitals and 2n² electrons per shell.
  - Needs: PC-14.1.A
  - P2 · P5 · drills: pc-radial-nodes, qm-orbitals-in-shell
- ● **PC-14.1.C** (acs-accm-pchem:I.C.2, acs-accm-pchem:X.D.4) Find the most probable radius from a radial distribution function.
  - EK: P(r) = r²|R(r)|²; for 1s the maximum is at a₀.
  - Needs: PC-14.1.B
  - P2 · P5 · drills: pc-mean-radius, qm-most-probable-radius

### 14.2 Many-electron atoms

Book: engel-reid-3e §21.4, §21.6, §21:hf-scf

- ● **PC-14.2.A** (acs-accm-pchem:II.E.2) Use the variational principle to judge and improve a trial wavefunction.
  - EK: ⟨E⟩_trial ≥ E₀ for any trial function; lower is better.
  - Needs: PC-14.1.C
  - P2 · P5 · drills: pc-gaussian-variational, qm-variational-principle
- ● **PC-14.2.B** (acs-accm-pchem:III.G.1, acs-accm-pchem:I.C.1) Estimate an effective nuclear charge with Slater's rules.
  - EK: Z_eff = Z − σ; same-shell electrons shield about 0.35, the shell below 0.85, deeper shells 1.00.
  - Needs: PC-14.2.A
  - P2 · P5 · drills: pc-slater-orbital-energy, qm-slater-zeff
- ● **PC-14.2.C** (acs-accm-pchem:II.E.1, acs-accm-pchem:II.B.2, acs-accm-pchem:I.B.3) Describe how the Hartree–Fock energy is built from one-electron, Coulomb and exchange terms.
  - EK: E_HF = Σ h_i + Σ(2J_ij − K_ij); it is not the sum of orbital energies.
  - Needs: PC-14.2.B
  - P2 · P5 · drills: qm-hf-closed-shell-energy, qm-hf-two-electron-energy

### 14.3 Atomic states and spectra

Book: engel-reid-3e §22.1, §22:config-energy, §22.3

- ● **PC-14.3.D** (acs-accm-pchem:I.D.2, acs-accm-pchem:I.D.4, acs-accm-pchem:III.D.3, acs-accm-pchem:I.G.3) Apply atomic selection rules and parity to decide whether a transition is allowed.
  - EK: One-electron electric-dipole transitions need Δl = ±1 (parity must change), ΔS = 0, ΔJ = 0, ±1 (not 0 → 0).
  - Needs: PC-14.2.C
  - P1 · drills: pc-atomic-selection, pc-allowed-count
- ◐ **PC-14.3.A** (acs-accm-pchem:I.B.2, acs-accm-pchem:I.B.3) Write the term symbols that arise from an electron configuration.
  - EK: ²ˢ⁺¹L_J with J from |L − S| to L + S.
  - Needs: PC-14.3.D
  - P2 · P5 · drills: ~qm-ground-term, ~qm-ground-level-j
- ● **PC-14.3.B** (acs-accm-pchem:I.B.2) Use Hund's rules to pick the ground-state term.
  - EK: Highest S first, then highest L; J = |L − S| for a less-than-half-filled shell, L + S for more.
  - Needs: PC-14.3.A
  - P2 · P5 · drills: qm-ground-term, qm-ground-level-j
- ● **PC-14.3.C** (acs-accm-pchem:I.B.2) Calculate the spin–orbit splitting between levels of a term.
  - EK: ΔE = ½A[J(J + 1) − L(L + 1) − S(S + 1)].
  - Needs: PC-14.3.B
  - P2 · P5 · drills: pc-spin-orbit-constant, qm-lande-interval

## Unit 15 · Chemical bonding and computational chemistry

Big ideas: QUANT

### 15.1 Diatomic molecules

Book: engel-reid-3e §23:h2-plus, §23.3, §23:homonuclear, §23.7

- ● **PC-15.1.E** (acs-accm-pchem:II.A.1, acs-accm-pchem:II.A.3) Build a molecular Hamiltonian's Coulomb terms and state what the Born–Oppenheimer approximation separates.
  - EK: For N nuclei and n electrons: n(n − 1)/2 electron–electron, nN electron–nucleus and N(N − 1)/2 nucleus–nucleus terms; BO fixes the nuclei while solving for electrons.
  - Needs: PC-14.3.C, CH-2.8.A
  - P1 · drills: pc-hamiltonian-terms, pc-born-oppenheimer
- ● **PC-15.1.F** (acs-accm-pchem:III.D.1, acs-accm-pchem:II.F.3) Find the spin multiplicity and term symbol of a diatomic's ground state from its MO filling.
  - EK: 2S + 1 from the unpaired electrons in the highest occupied MOs; Σ/Π from Λ, g/u from inversion, ± from reflection: O₂ is ³Σg⁻, N₂ ¹Σg⁺.
  - Needs: PC-15.1.E
  - P1 · drills: pc-diatomic-multiplicity, pc-term-symbol
- ● **PC-15.1.A** (acs-accm-pchem:II.B.2, acs-accm-pchem:II.E.3) Calculate the bonding and antibonding energies of H₂⁺ from the LCAO integrals.
  - EK: E_± = (H_AA ± H_AB)/(1 ± S_AB).
  - Needs: PC-15.1.F
  - P2 · P5 · drills: pc-lcao-gap, qm-lcao-bonding-energy
- ● **PC-15.1.B** (acs-accm-pchem:II.E.3, acs-accm-pchem:II.B.1) Explain why the antibonding orbital is raised more than the bonding orbital is lowered.
  - EK: ψ_± = (ψ_A ± ψ_B)/√(2(1 ± S)); the overlap S makes the splitting asymmetric.
  - Needs: PC-15.1.A
  - P2 · P5 · drills: pc-antibonding-asymmetry, ~qm-lcao-bonding-energy
- ● **PC-15.1.C** (acs-accm-pchem:II.E.3, acs-accm-pchem:II.F.1) Fill a molecular-orbital diagram for a homonuclear diatomic and predict magnetism.
  - EK: Fill in energy order, two per orbital, Hund's rule in degenerate pairs; unpaired electrons mean paramagnetic.
  - Needs: PC-15.1.B
  - P2 · P5 · drills: pc-unpaired-diatomic, qm-paramagnetism
- ● **PC-15.1.D** (acs-accm-pchem:II.F.1, acs-accm-pchem:II.F.2) Calculate a bond order and use it to rank bond length and strength.
  - EK: Bond order = (n_bonding − n_antibonding)/2; higher order, shorter and stronger bond.
  - Needs: PC-15.1.C
  - P2 · P5 · drills: pc-bond-order-change, qm-bond-order

### 15.2 Polyatomic molecules

Book: engel-reid-3e §24.2, §24.5, §24:huckel

- ● **PC-15.2.A** (acs-accm-pchem:III.B.2) Assign hybridisation and predict geometry from the number of electron domains.
  - EK: sp linear 180°, sp² trigonal 120°, sp³ tetrahedral 109.5°.
  - Needs: PC-15.1.D
  - P2 · P5 · drills: qm-hybridisation
- ◐ **PC-15.2.B** (acs-accm-pchem:III.B.3) Use qualitative MO theory to identify the HOMO and LUMO and predict a geometry.
  - EK: A Walsh diagram tracks orbital energy against angle; the HOMO decides the shape.
  - Needs: PC-15.2.A
  - P2 · P5 · drills: ~qm-walsh-ah2
- ● **PC-15.2.C** (acs-accm-pchem:II.E.1) Calculate Hückel π-orbital energies and the π-electron energy of a conjugated chain.
  - EK: E_k = α + 2β cos(kπ/(N + 1)), k = 1 … N; β is negative.
  - Needs: PC-15.2.B
  - P2 · P5 · drills: pc-polyene-gap, qm-huckel-chain

### 15.3 Computational chemistry

Book: engel-reid-3e §26:hf, §26:pes, §26:post-hf

- ● **PC-15.3.A** (acs-accm-pchem:II.E.1, acs-accm-pchem:II.B.2) Compute a Hartree–Fock energy from given one- and two-electron integrals.
  - EK: E_HF = Σ h_i + ½ Σ(J_ij − K_ij) over spin orbitals.
  - Needs: PC-15.2.C
  - P2 · P5 · drills: qm-hf-two-electron-energy
- ● **PC-15.3.B** (acs-accm-pchem:III.C.3, acs-accm-pchem:III.C.1, acs-accm-pchem:V.B.4, acs-accm-general:III.C, acs-accm-organic:III.C.1, acs-accm-inorganic:III.C.1) Classify stationary points on a potential-energy surface.
  - EK: All first derivatives vanish; a minimum has no negative curvatures, a transition state exactly one.
  - Needs: PC-15.3.A
  - P2 · P5 · drills: pc-hessian-classify, qm-stationary-point
- ● **PC-15.3.C** (acs-accm-pchem:II.A.2, acs-accm-pchem:II.E.1) Calculate a correlation energy and rank methods by the correlation they recover.
  - EK: E_corr = E_exact − E_HF, always negative; HF < MP2 < CCSD(T) toward the exact answer.
  - Needs: PC-15.3.B
  - P2 · P5 · drills: pc-correlation-recovered, ~qm-correlation-energy

## Unit 16 · Electronic spectroscopy

Big ideas: SPEC

### 16.1 Absorption and emission

Book: engel-reid-3e §25.1, §25.5, §25:franck-condon, §25.7

- ● **PC-16.1.E** (acs-accm-pchem:VI.C.2, acs-accm-pchem:VI.C.4, acs-accm-pchem:II.D.1, acs-accm-pchem:II.D.2, acs-accm-inorganic:V.F.10) Compute photon counts and quantum yields, and say how light breaks bonds.
  - EK: Photons = Pt/(hc/λ); Φ = molecules reacted ÷ photons absorbed; Φ > 1 signals a chain; photolysis is usually homolytic.
  - Needs: PC-13.1.D, PC-15.3.C
  - P1 · drills: pc-quantum-yield, pc-photochem
- ● **PC-16.1.A** (acs-accm-pchem:IX.D.1, acs-accm-pchem:III.A.2) Convert between the energy, wavelength and wavenumber of an electronic transition.
  - EK: ΔE = hν = hc/λ = hcν̃.
  - Needs: PC-16.1.E
  - P3 · drills: pc-ev-from-wavenumber, ~pc-photon
- ● **PC-16.1.B** (acs-accm-pchem:IX.D.1, acs-accm-pchem:VII.A.3, acs-accm-analytical:I.D.3, acs-accm-analytical:II.E.1, acs-accm-analytical:V.B.1) Calculate an absorbance, a concentration or a molar absorption coefficient.
  - EK: A = εcl = −log₁₀(I/I₀).
  - Needs: PC-16.1.A
  - P3 · drills: pc-transmittance, pc-beer-lambert
- ● **PC-16.1.C** (acs-accm-pchem:II.C.1, acs-accm-pchem:II.C.3) Use the Franck–Condon principle to predict which vibronic band is strongest.
  - EK: Transitions are vertical; intensity follows the overlap |⟨χ_v′|χ_v⟩|².
  - Needs: PC-16.1.B
  - P2 · P5 · drills: pc-zero-zero-overlap, qm-franck-condon-strongest
- ● **PC-16.1.D** (acs-accm-pchem:IX.D.1) Calculate a Stokes shift and explain why emission is at longer wavelength than absorption.
  - EK: Vibrational relaxation in the excited state comes first, so λ_em > λ_abs.
  - Needs: PC-16.1.C
  - P2 · P5 · drills: pc-stokes-energy, qm-stokes-shift

## Unit 17 · Molecular symmetry

Big ideas: SPEC

### 17.1 Point groups and their uses

Book: engel-reid-3e §27:symmetry, §27:point-groups, §27:character-tables, §27:normal-modes, §27:selection-rules

- ● **PC-17.1.A** (acs-accm-pchem:III.B.1, acs-accm-inorganic:X.D.3) Identify the symmetry elements of a molecule.
  - EK: E, C_n, σ, i, S_n; every molecule has at least E.
  - Needs: PC-15.3.C, CH-2.7.B
  - P2 · P5 · drills: gt-group-order, gt-mirror-planes
- ● **PC-17.1.B** (acs-accm-pchem:III.B.1, acs-accm-general:III.D, acs-accm-inorganic:III.D.1) Assign a molecule to its point group.
  - EK: Work down the flow chart: linear? high symmetry? principal axis? perpendicular C₂? mirror planes?
  - Needs: PC-17.1.A
  - P2 · P5 · drills: gt-point-group-common, gt-point-group-more
- ● **PC-17.1.D** (acs-accm-pchem:III.D.2) Count the normal modes of a molecule and find their symmetries.
  - EK: 3N − 6 for nonlinear, 3N − 5 for linear molecules.
  - Needs: PC-17.1.B
  - P2 · P5 · drills: gt-normal-modes, gt-modes-symmetry
- ● **PC-17.1.E** (acs-accm-pchem:III.D.2, acs-accm-organic:III.D.1, acs-accm-inorganic:II.E.4, acs-accm-inorganic:III.D.3, acs-accm-inorganic:III.D.4) Decide from symmetry whether a mode is IR active, Raman active or both.
  - EK: IR active if it transforms like x, y or z; Raman active like a quadratic; mutually exclusive with an inversion centre.
  - Needs: PC-17.1.D
  - P2 · P5 · drills: gt-ir-raman
- ● **PC-17.1.C** (acs-accm-pchem:III.D.2) Reduce a representation with a character table.
  - EK: n_i = (1/h) Σ χ(R) χ_i(R) over all operations.
  - Needs: PC-17.1.E
  - P2 · P5 · drills: gt-operation-product, gt-reduce-c2v, gt-reduce-c3v
- ● **PC-17.1.F** (acs-accm-pchem:III.E.1, acs-accm-organic:III.E.5, acs-accm-organic:IX.C.2, acs-accm-analytical:III.E.1) Use optical rotation to find specific rotation and enantiomeric excess.
  - EK: [α] = α/(l·c) with l in dm and c in g/mL; ee = [α]_obs/[α]_pure × 100%.
  - Needs: PC-17.1.C
  - P1 · drills: pc-specific-rotation, pc-ee

## Unit 18 · Nuclear magnetic resonance

Big ideas: SPEC

### 18.1 The NMR experiment

Book: engel-reid-3e §28:larmor, §28:chemical-shift, §28:shielding, §28:spin-spin, §28:coupling

- ● **PC-18.1.A** (acs-accm-pchem:I.A.2) Calculate the Larmor frequency of a nucleus in a given field.
  - EK: ν₀ = γB₀/2π; for ¹H, 42.58 MHz per tesla.
  - Needs: PC-14.3.C, PH-12.2.C
  - P3 · drills: pc-field-for-frequency, pc-larmor
- ● **PC-18.1.B** (acs-accm-pchem:I.A.2) Convert between a frequency offset in hertz and a chemical shift in ppm.
  - EK: δ = (ν_sample − ν_ref)/ν_ref × 10⁶; the ppm value does not depend on the field.
  - Needs: PC-18.1.A
  - P3 · drills: pc-hz-other-field, pc-chemical-shift
- ● **PC-18.1.C** (acs-accm-pchem:I.A.2) Relate shielding to chemical shift and predict which nuclei appear downfield.
  - EK: Electron-withdrawing neighbours deshield, giving a larger δ.
  - Needs: PC-18.1.B
  - P2 · P5 · drills: nmr-downfield
- ● **PC-18.1.D** (acs-accm-pchem:I.A.2) Predict the multiplicity of a signal from the n + 1 rule.
  - EK: n equivalent spin-½ neighbours split a signal into n + 1 lines with Pascal's-triangle intensities.
  - Needs: PC-18.1.C
  - P2 · P5 · drills: pc-two-set-splitting, nmr-multiplicity
- ● **PC-18.1.E** (acs-accm-pchem:I.A.2) Estimate a three-bond coupling constant from a dihedral angle.
  - EK: ³J = A − B cos φ + C cos² φ (Karplus); largest near 0° and 180°.
  - Needs: PC-18.1.D
  - P2 · P5 · drills: nmr-karplus

## Unit 19 · Probability and the Boltzmann distribution

Big ideas: STAT

### 19.1 Counting and distributions

Book: engel-reid-3e §29.2, §29:stirling, §29:distributions

- ● **PC-19.1.A** (acs-accm-pchem:X.C.2, acs-accm-pchem:VI.H.2) Count the microstates of a configuration.
  - EK: W = N!/(a₀! a₁! a₂! …).
  - Needs: PC-1.3.A
  - P3 · drills: td-multinomial-probability, sm-anagram
- ● **PC-19.1.B** (acs-accm-pchem:X.B.1) Apply Stirling's approximation to the logarithm of a large factorial.
  - EK: ln N! ≈ N ln N − N.
  - Needs: PC-19.1.A
  - P2 · P5 · drills: pc-stirling-error, sm-stirling
- ● **PC-19.1.C** (acs-accm-pchem:X.C.1) Calculate the mean and variance of a distribution.
  - EK: ⟨x⟩ = ∫x f(x) dx; σ² = ⟨x²⟩ − ⟨x⟩².
  - Needs: PC-19.1.B
  - P3 · drills: pc-discrete-variance, ~sm-fl-exact

### 19.2 The Boltzmann distribution

Book: engel-reid-3e §30:microstates, §30:beta, §30.2

- ● **PC-19.2.A** (acs-accm-pchem:VI.H.2, acs-accm-pchem:X.C.1) Calculate an entropy from a number of microstates.
  - EK: S = k_B ln W.
  - Needs: PC-19.1.C
  - P3 · drills: pc-log-w-from-s, ~sm-two-state
- ● **PC-19.2.B** (acs-accm-pchem:X.C.2, acs-accm-pchem:X.D.3) Calculate the population ratio of two levels at a given temperature.
  - EK: n_i/n_j = (g_i/g_j) e^(−Δε/k_BT); β = 1/k_BT.
  - Needs: PC-19.2.A
  - P3 · drills: td-boltzmann-degenerate, sm-bz-ratio
- ● **PC-19.2.C** (acs-accm-pchem:X.C.2, acs-accm-pchem:X.C.1) Calculate a partition function and the fraction of molecules in each level.
  - EK: q = Σ g_j e^(−ε_j/k_BT); P_i = g_i e^(−ε_i/k_BT)/q.
  - Needs: PC-19.2.B
  - P3 · drills: sm-pf-q, sm-bz-fraction

## Unit 20 · Partition functions and statistical thermodynamics

Big ideas: STAT

### 20.1 Molecular partition functions

Book: engel-reid-3e §31.4, §31.5, §31:rot-poly, §31.7, §31:electronic, §31.8

- ● **PC-20.1.A** (acs-accm-pchem:X.C.1) Calculate a translational partition function.
  - EK: q_trans = V(2πmk_BT/h²)^(3/2) = V/Λ³.
  - Needs: PC-3.2.D, PC-12.3.E, PC-19.2.C, CA-10.2.A
  - P3 · drills: td-qtrans-scaling, sm-ig-qtrans
- ● **PC-20.1.B** (acs-accm-pchem:X.C.1, acs-accm-pchem:III.A.3) Calculate the rotational partition function of a diatomic molecule.
  - EK: q_rot = T/(σθ_rot) when T ≫ θ_rot; σ = 2 for a homonuclear diatomic.
  - Needs: PC-20.1.A
  - P3 · drills: td-symmetry-number, sm-ig-qrot
- ● **PC-20.1.C** (acs-accm-pchem:X.C.1) Calculate the rotational partition function of a polyatomic molecule.
  - EK: Linear: T/(σΘ); nonlinear: (√π/σ)(T³/Θ_AΘ_BΘ_C)^(1/2).
  - Needs: PC-20.1.B
  - P2 · P5 · drills: pc-qrot-poly-scaling, sm-rotational-partition-nonlinear
- ● **PC-20.1.D** (acs-accm-pchem:X.C.1) Calculate a vibrational partition function.
  - EK: q_vib = 1/(1 − e^(−θ_vib/T)) measured from the ground level.
  - Needs: PC-20.1.C
  - P3 · drills: td-vibrational-population, sm-ig-qvib
- ● **PC-20.1.E** (acs-accm-pchem:X.C.2) Calculate an electronic partition function from level degeneracies and energies.
  - EK: q_el = Σ g_i e^(−ε_i/k_BT) ≈ g₀ when the first excited level is far above k_BT.
  - Needs: PC-20.1.D
  - P2 · P5 · drills: pc-no-upper-fraction, sm-electronic-partition
- ● **PC-20.1.F** (acs-accm-pchem:X.C.1, acs-accm-pchem:VI.E.1) Use equipartition to predict a molar heat capacity.
  - EK: ½RT per quadratic degree of freedom per mole; vibrations count only when T ≫ θ_vib.
  - Needs: PC-20.1.E
  - P3 · drills: td-equipartition-cp, sm-cv-equipartition

### 20.2 Thermodynamic functions from the partition function

Book: engel-reid-3e §32:energy, §32.3, §32.4, §32.6, §32:residual-entropy

- ● **PC-20.2.A** (acs-accm-pchem:X.C.1) Calculate an internal energy from a partition function.
  - EK: U = −(∂ ln Q/∂β)_V = k_BT²(∂ ln Q/∂T)_V.
  - Needs: PC-20.1.F
  - P3 · drills: pc-vib-thermal-energy, ~sm-pf-u-two-level
- ● **PC-20.2.B** (acs-accm-pchem:X.C.1) Calculate the vibrational contribution to a heat capacity.
  - EK: C_V,vib/R = u²e^(−u)/(1 − e^(−u))² with u = θ_vib/T.
  - Needs: PC-20.2.A
  - P3 · drills: td-einstein-temperature-from-cv, sm-cv-einstein
- ● **PC-20.2.C** (acs-accm-pchem:X.C.1, acs-accm-pchem:VI.H.2) Calculate an entropy from a partition function.
  - EK: S = k_B ln Q + U/T.
  - Needs: PC-20.2.B
  - P3 · drills: pc-vib-entropy, ~sm-pf-s-two-level
- ● **PC-20.2.D** (acs-accm-pchem:X.C.1, acs-accm-pchem:VI.H.5) Calculate a Helmholtz energy from a partition function.
  - EK: A = −k_BT ln Q.
  - Needs: PC-20.2.C
  - P3 · drills: pc-vib-helmholtz, ~sm-pf-f
- ● **PC-20.2.E** (acs-accm-pchem:VI.H.7, acs-accm-pchem:III.H.3, acs-accm-general:VI.H.3) Calculate the residual entropy of a crystal with orientational disorder.
  - EK: S₀ = R ln W₀ per mole, W₀ being the number of equally likely orientations.
  - Needs: PC-20.2.D
  - P3 · drills: pc-w-from-residual, pc-residual-entropy

## Unit 21 · Kinetic theory of gases and transport

Big ideas: RATE

### 21.1 Molecular speeds and collisions

Book: engel-reid-3e §33:maxwell, §33:speeds, §33:effusion, §33:collisions, §33:mean-free-path

- ● **PC-21.1.A** (acs-accm-pchem:VII.D.2, acs-accm-pchem:X.A.3) Use the Maxwell speed distribution to compare speeds at different temperatures and masses.
  - EK: f(v) = 4π(m/2πk_BT)^(3/2) v² e^(−mv²/2k_BT); broader and faster for high T or low mass.
  - Needs: PC-1.3.A, PC-19.2.C, CH-3.5.B
  - P2 · P5 · drills: pc-rms-ratio, kt-maxwell-compare
- ● **PC-21.1.B** (acs-accm-pchem:VII.D.2) Calculate the most probable, mean and root-mean-square speeds of a gas.
  - EK: v_mp = √(2RT/M), v̄ = √(8RT/πM), v_rms = √(3RT/M), with M in kg/mol.
  - Needs: PC-21.1.A
  - P3 · drills: pc-matching-temperature, pc-speeds
- ● **PC-21.1.C** (acs-accm-pchem:X.A.3) Calculate a ratio of effusion rates, or a molar mass from one.
  - EK: r₁/r₂ = √(M₂/M₁).
  - Needs: PC-21.1.B
  - P3 · drills: pc-effusion-time, pc-effusion
- ● **PC-21.1.D** (acs-accm-pchem:VII.D.3) Calculate the collision frequency of a molecule in a gas.
  - EK: z = √2 σ v̄ (N/V) with σ = πd².
  - Needs: PC-21.1.C
  - P2 · P5 · drills: pc-collision-scaling, kt-collision-frequency
- ● **PC-21.1.E** (acs-accm-pchem:VII.D.3) Calculate the mean free path of a gas molecule.
  - EK: λ = v̄/z = k_BT/(√2 σP).
  - Needs: PC-21.1.D
  - P3 · drills: pc-pressure-for-mfp, pc-mean-free-path

### 21.2 Transport

Book: engel-reid-3e §34:ficks-first, §34:ficks-second, §34:thermal-conduction, §34:viscosity

- ● **PC-21.2.A** (acs-accm-pchem:X.A.3) Calculate a diffusive flux from a concentration gradient.
  - EK: J = −D dC/dx; flux runs down the gradient.
  - Needs: PC-21.1.E
  - P2 · P5 · drills: pc-gradient-for-flux, tr-fick-flux
- ● **PC-21.2.B** (acs-accm-pchem:X.A.3) Estimate how far a species diffuses in a given time.
  - EK: ∂C/∂t = D ∂²C/∂x²; x_rms = √(2Dt) in one dimension.
  - Needs: PC-21.2.A
  - P3 · drills: pc-diffusion-time, pc-diffusion-distance
- ● **PC-21.2.C** (acs-accm-pchem:VI.G.1) Calculate a conductive heat flux from a temperature gradient.
  - EK: J_q = −κ dT/dx.
  - Needs: PC-21.2.B
  - P3 · drills: pc-conductivity-from-flux, ~ht-cond
- ● **PC-21.2.D** (webwork-opl:FM1.3, acs-accm-pchem:IV.D.4) Calculate a shear stress from a viscosity and a velocity gradient.
  - EK: τ = η du/dz; for a gas η = ⅓ρv̄λ, which rises with temperature.
  - Needs: PC-21.2.C
  - P2 · P5 · drills: pc-gradient-from-stress, tr-shear-stress

## Unit 22 · Chemical kinetics

Big ideas: RATE

### 22.1 Rate laws

Book: engel-reid-3e §35:rate-laws, §35:integrated

- ● **PC-22.1.C** (acs-accm-pchem:VII.A.1, acs-accm-pchem:IX.A.2, acs-accm-pchem:IX.E.1, acs-accm-pchem:IX.F.1, acs-accm-pchem:IX.F.2, acs-accm-pchem:IX.F.3, acs-accm-pchem:V.C.2, acs-accm-pchem:VII.C.6, acs-accm-pchem:IX.D.2, acs-accm-pchem:IX.G.1) Choose a kinetic method for the time scale and isolate one reactant to get pseudo-first-order data.
  - EK: With [B]₀ ≫ [A]₀, rate = k′[A] with k′ = k[B]₀; stopped flow reaches milliseconds, relaxation and flash photolysis microseconds, femtosecond lasers bond vibrations.
  - Needs: PC-4.2.B, CH-5.11.A, CA-7.8.A
  - P1 · drills: pc-pseudo-first, pc-kinetic-method
- ● **PC-22.1.A** (acs-accm-pchem:VII.B.1, acs-accm-pchem:VII.B.2, acs-accm-pchem:IX.E.1) Determine reaction orders and a rate constant from initial-rate data.
  - EK: rate = k[A]^m[B]^n; compare runs that change one concentration at a time.
  - Needs: PC-22.1.C
  - P3 · drills: pc-rate-prediction, pc-initial-rates
- ● **PC-22.1.B** (acs-accm-pchem:VII.B.1, acs-accm-pchem:VII.B.3, acs-accm-pchem:VII.A.5) Use an integrated rate law to find a concentration, a time or a half-life.
  - EK: First order: [A] = [A]₀e^(−kt), t½ = ln 2/k. Second order: 1/[A] = 1/[A]₀ + kt.
  - Needs: PC-22.1.A
  - P3 · drills: pc-first-order, pc-second-order

### 22.2 Temperature dependence

Book: engel-reid-3e §35:arrhenius, §35:collision-theory, §35:eyring

- ● **PC-22.2.D** (acs-accm-pchem:VII.E.1, acs-accm-pchem:VII.E.2, acs-accm-pchem:V.F.4, acs-accm-pchem:V.G.1, acs-accm-pchem:VII.F.1, acs-accm-pchem:VI.B.1, acs-accm-pchem:VI.C.1, acs-accm-pchem:V.B.1, acs-accm-pchem:V.B.2, acs-accm-pchem:V.B.3, acs-accm-pchem:V.D.1, acs-accm-pchem:X.D.2, acs-accm-pchem:V.F.3, acs-accm-general:VII.F.1, acs-accm-organic:V.E.2, acs-accm-organic:VII.F.1, acs-accm-inorganic:VII.F.1) Quantify how a catalyst or a higher temperature speeds a reaction, and tell kinetic from thermodynamic control.
  - EK: Lowering Eₐ by ΔEₐ multiplies k by exp(ΔEₐ/RT); a catalyst leaves K and the products unchanged; the fraction of collisions above Eₐ goes as exp(−Eₐ/RT).
  - Needs: PC-22.1.B
  - P1 · drills: pc-catalyst-speedup, pc-control
- ● **PC-22.2.A** (acs-accm-pchem:VII.B.4, acs-accm-pchem:V.C.1) Calculate an activation energy from rate constants at two temperatures, or a rate constant at a new temperature.
  - EK: k = Ae^(−E_a/RT); ln(k₂/k₁) = −(E_a/R)(1/T₂ − 1/T₁).
  - Needs: PC-22.2.D
  - P3 · drills: sm-rate-ea, sm-rate-k2
- ● **PC-22.2.B** (acs-accm-pchem:VII.D.4, acs-accm-pchem:VII.D.1) Estimate a rate constant from collision theory and interpret the steric factor.
  - EK: k = pZ_AB e^(−E_a/RT); p < 1 accounts for orientation.
  - Needs: PC-22.2.A
  - P2 · P5 · drills: pc-energetic-fraction, kn-steric-factor
- ● **PC-22.2.C** (acs-accm-pchem:VII.D.4, acs-accm-pchem:VII.D.1) Calculate a rate constant from an activation Gibbs energy with the Eyring equation.
  - EK: k = (k_BT/h) e^(−ΔG‡/RT); k_BT/h ≈ 6.2 × 10¹² s⁻¹ at 298 K.
  - Needs: PC-22.2.B
  - P3 · drills: td-eyring-half-life, sm-rate-eyring

### 22.3 Multi-step reactions

Book: engel-reid-3e §35:reversible, §35:parallel, §35:sequential, §34:steady-state, §36:preequil, §36:lindemann, §36:michaelis, §36:radical-chain

- ● **PC-22.3.I** (acs-accm-pchem:VIII.G.2, acs-accm-pchem:III.H.1, acs-accm-inorganic:V.D.5, acs-accm-inorganic:VII.E.2) Use the Langmuir isotherm to find surface coverage, or the pressure for a target coverage.
  - EK: θ = KP/(1 + KP); half coverage at P = 1/K; heterogeneous rates follow the coverage of the adsorbed reactant.
  - Needs: PC-22.2.C
  - P1 · drills: pc-langmuir, pc-langmuir-pressure
- ● **PC-22.3.A** (acs-accm-pchem:VIII.B.1, acs-accm-pchem:VII.A.2) Calculate concentrations as a reversible first-order reaction approaches equilibrium.
  - EK: [A](t) = [A]_eq + ([A]₀ − [A]_eq)e^(−(k₁ + k₋₁)t); K = k₁/k₋₁.
  - Needs: PC-22.3.I
  - P2 · P5 · drills: pc-reversible-halfway, kn-reversible-first-order
- ● **PC-22.3.B** (acs-accm-pchem:VII.C.1) Calculate the product ratio and overall decay of parallel first-order reactions.
  - EK: [A] = [A]₀e^(−(k₁ + k₂)t); [B]/[C] = k₁/k₂ at all times.
  - Needs: PC-22.3.A
  - P3 · drills: pc-parallel-time, pc-parallel
- ● **PC-22.3.C** (acs-accm-pchem:VII.C.5) Calculate the concentration and time of the maximum of an intermediate in A → B → C.
  - EK: [B] = k₁[A]₀/(k₂ − k₁) (e^(−k₁t) − e^(−k₂t)); t_max = ln(k₁/k₂)/(k₁ − k₂).
  - Needs: PC-22.3.B
  - P2 · P5 · drills: pc-intermediate-max-time, ~kn-intermediate-maximum
- ● **PC-22.3.D** (acs-accm-pchem:VII.C.3, acs-accm-pchem:VII.C.5, acs-accm-inorganic:VII.C.2) Apply the steady-state approximation to derive a rate law.
  - EK: Set d[I]/dt ≈ 0 for a reactive intermediate and solve for [I].
  - Needs: PC-22.3.C
  - P2 · P5 · drills: pc-steady-state-keff, kn-steady-state-rate
- ● **PC-22.3.E** (acs-accm-pchem:VII.C.3, acs-accm-pchem:VII.C.4) Apply the pre-equilibrium approximation to a mechanism with a fast first step.
  - EK: The fast step stays at equilibrium: [I] = K[A][B], so rate = k₂K[A][B].
  - Needs: PC-22.3.D
  - P2 · P5 · drills: pc-pre-equilibrium-ea, kn-pre-equilibrium
- ● **PC-22.3.F** (acs-accm-pchem:VII.C.2, acs-accm-pchem:VII.C.3) Use the Lindemann mechanism to explain the pressure dependence of a unimolecular rate.
  - EK: rate = k_a k_b[A]²/(k₋ₐ[A] + k_b): first order at high pressure, second order at low.
  - Needs: PC-22.3.E
  - P2 · P5 · drills: pc-lindemann-half, kn-lindemann
- ● **PC-22.3.G** (acs-accm-pchem:VII.E.3, acs-accm-pchem:VII.C.8, acs-accm-analytical:X.A.2) Calculate an enzyme rate from the Michaelis–Menten equation, and V_max and K_M from data.
  - EK: v = V_max[S]/(K_M + [S]); v = V_max/2 when [S] = K_M.
  - Needs: PC-22.3.F
  - P3 · drills: pc-substrate-for-fraction, pc-michaelis
- ● **PC-22.3.H** (acs-accm-pchem:VII.C.3, acs-accm-pchem:VII.C.7) Calculate a steady-state radical concentration and a kinetic chain length.
  - EK: [R·]_ss = √(R_i/k_t); chain length = propagation rate / initiation rate.
  - Needs: PC-22.3.G
  - P2 · P5 · drills: pc-initiation-from-chain, kn-chain-length

## Drills not yet placed on the map

- aq-atomic-mass (pchem.thermochemistry)
- aq-molar-mass (pchem.thermochemistry)
- aq-element-from-mass (pchem.thermochemistry)
- aq-mass-percent (pchem.thermochemistry)
- sc-carnot-efficiency (pchem.entropy)
- aq-factor-of-ten (pchem.gibbs)
- aq-free-energy-to-K (pchem.gibbs)
- aq-dg-for-factor (pchem.gibbs)
- aq-k-to-dg (pchem.gibbs)
- aq-amounts (pchem.real-gases)
- aq-moles-in-flask (pchem.real-gases)
- aq-energy-conversion (quantum.origins)
- aq-photon-energy (quantum.origins)
- aq-ev-to-nm (quantum.origins)
- aq-lengths (quantum.model-systems)
- aq-dna-length (quantum.model-systems)
- aq-wavenumber-wavelength (quantum.spectroscopy)
- sc-rms-speed (kinetics.gas-kinetic)
