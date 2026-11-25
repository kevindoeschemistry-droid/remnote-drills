# Anchor Quantities — curriculum framework (draft 1)

Generated from `drills/frameworks/anchor-quantities.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**14 learning objectives** in 6 units (14 core): 14 drilled, 0 partly, 0 with no drills. Core: 14 / 14 drilled.

## Big ideas

- **FEEL · A number should mean something.** Knowing that a teaspoon is 5 mL, that water is 55 M, or that a tablespoon of water is about a mole turns a computed answer into something you can picture and sanity-check.
- **SCALE · Compare with the natural scale.** An energy is large or small against k_BT, a length against a bond or a protein, a count against Avogadro's number. Carrying the scale lets you estimate an answer before computing it.

## Practices

- **P1 · Recall the anchor.** Give the value, with its unit, to within a few percent, without looking it up.
- **P2 · Use the anchor.** Chain one or two anchors into an estimate good to about ten percent.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Household and bench measures | core | — | 2 | 2 | 0 | 0 |
| 2 · Thermal energy | core | — | 4 | 4 | 0 | 0 |
| 3 · Energy units and light | core | — | 2 | 2 | 0 | 0 |
| 4 · Amounts and concentrations | core | — | 3 | 3 | 0 | 0 |
| 5 · Sizes: bonds to cells | core | — | 1 | 1 | 0 | 0 |
| 6 · Numbers in cells | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Household and bench measures

Big ideas: FEEL

### 1.1 Spoons, cups and ounces



- ● **AQ-1.1.A** Recall the metric size of a teaspoon, tablespoon, cup, fluid ounce and ounce.
  - EK: Teaspoon 5 mL, tablespoon 15 mL, cup 240 mL, fluid ounce 30 mL, ounce 28 g (US labelling values).
  - P1 · drills: aq-household-measure, aq-kitchen-ratio
- ● **AQ-1.1.B** Turn a spoonful of water into grams and moles.
  - EK: Water is 1 g/mL and 18 g/mol, so a tablespoon is a little under a mole.
  - P2 · drills: aq-spoon-of-water, aq-spoons-per-mole

## Unit 2 · Thermal energy

Big ideas: SCALE

### 2.1 RT and kT at room temperature



- ● **AQ-2.1.A** (acs-accm-pchem:X.C.2) Recall RT and k_BT at 25 °C in kJ/mol, kcal/mol, meV, cm⁻¹ and pN·nm.
  - EK: RT ≈ 2.48 kJ/mol ≈ 0.593 kcal/mol; k_BT ≈ 25.7 meV ≈ 207 cm⁻¹ ≈ 4.1 pN·nm.
  - P1 · drills: aq-thermal-energy, aq-rt-at-t
- ● **AQ-2.1.B** (acs-accm-pchem:X.D.3, acs-accm-pchem:X.C.2) Estimate a Boltzmann population ratio for a gap of a few k_BT.
  - EK: N₂/N₁ = e^(−ΔE/k_BT): 0.37, 0.14, 0.05 for 1, 2, 3 k_BT.
  - P2 · drills: aq-boltzmann-ratio, aq-gap-for-ratio

### 2.2 Free energy and equilibrium



- ● **AQ-2.2.A** (acs-accm-pchem:VIII.F.2, acs-accm-pchem:VIII.D.1) Recall the free-energy cost of a factor of ten in an equilibrium constant.
  - EK: RT ln 10 ≈ 5.7 kJ/mol ≈ 1.36 kcal/mol at 25 °C.
  - P1 · drills: aq-factor-of-ten, aq-dg-for-factor
- ● **AQ-2.2.B** (acs-accm-pchem:VIII.F.2, acs-accm-pchem:VIII.D.1) Convert a standard free energy to the order of magnitude of K in one step.
  - EK: log₁₀K = −ΔG°/(5.7 kJ/mol).
  - P2 · drills: aq-free-energy-to-K, aq-k-to-dg

## Unit 3 · Energy units and light

Big ideas: SCALE

### 3.1 Conversions



- ● **AQ-3.1.A** (acs-accm-pchem:I.D.1, acs-accm-general:VI.A.3) Recall the conversions among eV, kJ/mol, kcal/mol, cm⁻¹ and hartree, and hc in eV·nm.
  - EK: 1 eV ≈ 96.5 kJ/mol ≈ 23.06 kcal/mol ≈ 8066 cm⁻¹; 1 E_h ≈ 27.2 eV ≈ 627.5 kcal/mol; hc ≈ 1240 eV·nm.
  - P1 · drills: aq-energy-conversion, aq-ev-to-nm

### 3.2 Photons



- ● **AQ-3.2.A** (acs-accm-pchem:IX.D.1, acs-accm-pchem:I.D.1, acs-accm-analytical:I.D.1, acs-accm-analytical:I.D.4) Estimate a photon's energy from its wavelength, and an infrared wavelength from a wavenumber.
  - EK: E(eV) ≈ 1240/λ(nm); λ(µm) = 10⁴/ν̃(cm⁻¹).
  - P2 · drills: aq-photon-energy, aq-wavenumber-wavelength

## Unit 4 · Amounts and concentrations

Big ideas: FEEL, SCALE

### 4.1 Counts and volumes



- ● **AQ-4.1.A** (acs-accm-pchem:I.E.1, acs-accm-pchem:X.B.1) Recall the molarity of water, the molar volume of a gas, the number density of a 1 M solution, and the Avogadro and Faraday constants.
  - EK: Water 55.5 M; 22.4 L/mol at 0 °C and 24.5 L/mol at 25 °C; 1 M = 0.6 nm⁻³; N_A = 6.022×10²³; F = 96 485 C/mol.
  - P1 · drills: aq-amounts, aq-moles-in-flask

### 4.2 Atomic and molar masses



- ● **AQ-4.2.A** (acs-accm-pchem:I.E.1) Recall the atomic masses of the common elements.
  - EK: H 1, C 12, N 14, O 16, Na 23, P 31, S 32, Cl 35.5, K 39, Ca 40, Fe 56.
  - P1 · drills: aq-atomic-mass, aq-element-from-mass
- ● **AQ-4.2.B** (acs-accm-pchem:I.E.1) Add up the molar mass of a small molecule in the head.
  - EK: Round each atom to the nearest unit (half unit for Cl).
  - P2 · drills: aq-molar-mass, aq-mass-percent

## Unit 5 · Sizes: bonds to cells

Big ideas: SCALE

### 5.1 Lengths



- ● **AQ-5.1.A** (acs-accm-pchem:IV.A.1) Recall the lengths of common bonds and the sizes of water, DNA, a protein, a membrane and a bacterium.
  - EK: Bonds 100–150 pm (C–C 154 pm); water 0.3 nm; DNA 2 nm wide, 0.34 nm per base pair; protein 3–6 nm; membrane 4–10 nm; E. coli 2–4 µm.
  - P1 · drills: aq-lengths, aq-dna-length

## Unit 6 · Numbers in cells

Big ideas: FEEL, SCALE

### 6.1 Rates, energies and counts



- ● **AQ-6.1.A** Recall rule-of-thumb rates, energies and genome sizes for cells.
  - EK: Ribosome 10–20 aa/s; E. coli divides in 20–40 min; ATP hydrolysis 40–60 kJ/mol ≈ 20 k_BT; genomes 4×10⁶ bp (E. coli), 3×10⁹ bp (human); diffusion limit 10⁸–10⁹ M⁻¹s⁻¹.
  - P1 · drills: aq-cell-numbers, aq-ribosome-time
- ● **AQ-6.1.B** Turn a concentration into a number of molecules in a cell.
  - EK: 1 nM in 1 fL (1 µm³) is about 0.6 molecules.
  - P2 · drills: aq-molecules-per-cell, aq-one-molecule-conc
