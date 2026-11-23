# Chemistry Olympiad — curriculum framework (draft 1)

Generated from `drills/frameworks/chemistry-olympiad.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**14 learning objectives** in 4 units (14 core): 14 drilled, 0 partly, 0 with no drills. Core: 14 / 14 drilled.

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
