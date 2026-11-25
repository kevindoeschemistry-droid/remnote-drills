# Analytical Chemistry — curriculum framework (draft 1)

Generated from `drills/frameworks/analytical-chemistry.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**18 learning objectives** in 5 units (18 core): 18 drilled, 0 partly, 0 with no drills. Core: 18 / 18 drilled.

## Big ideas

- **MOLES · Every analysis is a mole chain.** Volume × concentration or mass ÷ molar mass, through a ratio, to the analyte. Titration, gravimetry and calibration differ only in the first link.
- **EQ · Equilibrium sets the limits.** Common ions, complexing agents and pH decide how much stays dissolved, how sharp an end point is and what precipitates first.
- **ERROR · A number is not a result without its uncertainty.** Replicates, calibration and propagation say how far to trust it; matrix effects say whether to trust it at all.

## Practices

- **P1 · Compute.** Carry the stoichiometric or equilibrium calculation to a number with the right units.
- **P2 · Choose.** Pick the indicator, technique or test that fits.
- **P3 · Judge.** Decide whether data support a result.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Titrimetry | core | — | 7 | 7 | 0 | 0 |
| 2 · Gravimetric analysis | core | — | 1 | 1 | 0 | 0 |
| 3 · Solubility equilibria in analysis | core | — | 2 | 2 | 0 | 0 |
| 4 · Separations | core | — | 2 | 2 | 0 | 0 |
| 5 · Measurement, calibration and data | core | — | 6 | 6 | 0 | 0 |

## Unit 1 · Titrimetry

Big ideas: MOLES, EQ

### 1.1 Titration types



- ● **AN-1.1.A** Compute a result from a back titration.
  - EK: Reagent added − reagent left = reagent used.
  - P1 · drills: an-back-titration, an-back-titration-volume
- ● **AN-1.1.B** Compute a result from a permanganate titration.
  - EK: Ratio from electrons: MnO₄⁻ 5, Fe²⁺ 1, C₂O₄²⁻ 2.
  - Needs: IN-4.1.A
  - P1 · drills: an-permanganate, an-dichromate-for-permanganate
- ● **AN-1.1.C** Compute water hardness from an EDTA titration.
  - EK: EDTA binds metal ions 1:1; report as mg CaCO₃ per L.
  - P1 · drills: an-edta-hardness, an-edta-volume
- ● **AN-1.1.D** Compute chloride from a Mohr titration.
  - EK: Ag⁺ + Cl⁻ 1:1; chromate end point at neutral pH.
  - P1 · drills: an-mohr, an-argentometry-why
- ● **AN-1.1.E** Compute protein from a Kjeldahl determination.
  - EK: mol N = acid added − acid left; × factor (6.25).
  - Needs: AN-1.1.A
  - P1 · drills: an-kjeldahl, an-kjeldahl-ammonia

### 1.2 Titration curves



- ● **AN-1.2.A** Find the pH at any point of a weak-acid–strong-base titration.
  - EK: Start, buffer, equivalence (hydrolysis), excess base.
  - P1 · drills: an-titration-ph, an-quarter-equivalence
- ● **AN-1.2.B** Choose an indicator whose range brackets the equivalence pH.
  - EK: Weak acid + strong base: phenolphthalein.
  - Needs: AN-1.2.A
  - P2 · drills: an-indicator, an-indicator-titration

## Unit 2 · Gravimetric analysis

Big ideas: MOLES

### 2.1 Gravimetric factors



- ● **AN-2.1.A** Compute a mass percent from the weight of a precipitate.
  - EK: Gravimetric factor from molar masses and element counts.
  - P1 · drills: an-gravimetric, an-gravimetric-expected

## Unit 3 · Solubility equilibria in analysis

Big ideas: EQ

### 3.1 Solubility



- ● **AN-3.1.A** Compute a solubility with a common ion present.
  - EK: s(s + c) = K_sp.
  - P1 · drills: an-common-ion, an-common-ion-factor
- ● **AN-3.1.B** (acs-accm-inorganic:VIII.C.1) Compute a solubility raised by complex formation.
  - EK: K = K_sp·β₂ for AgX + 2NH₃.
  - Needs: AN-3.1.A
  - P1 · drills: an-complex-solubility, an-complex-dissolve

## Unit 4 · Separations

Big ideas: EQ

### 4.1 Extraction and chromatography



- ● **AN-4.1.A** Compute the fraction left after repeated extractions.
  - EK: q = [V_aq/(V_aq + D V_org)]ⁿ.
  - P1 · drills: an-extraction, an-extractions-needed
- ● **AN-4.1.B** Compute plate number, retention factor or resolution from a chromatogram.
  - EK: N = 16(t_R/W)², k = (t_R − t_M)/t_M, R_s = 2Δt_R/(W₁+W₂).
  - P1 · drills: an-chromatography, an-resolution-length

## Unit 5 · Measurement, calibration and data

Big ideas: ERROR

### 5.1 Spectrophotometry and calibration



- ● **AN-5.1.A** Resolve a two-component mixture by absorbance at two wavelengths.
  - EK: Absorbances add; solve two equations.
  - P1 · drills: an-two-component, an-beer-reverse
- ● **AN-5.1.B** Find a concentration by standard addition.
  - EK: c = A_x c_s V_s / [V_x (A_sp − A_x)].
  - P1 · drills: an-standard-addition, an-spike-signal
- ● **AN-5.1.C** (acs-accm-general:IX.G.4) Read an unknown off a least-squares calibration line.
  - EK: Slope and intercept from the sums.
  - P1 · drills: an-calibration, an-detection-limit

### 5.2 Data and method choice



- ● **AN-5.2.A** Apply Dixon's Q-test to a suspect replicate.
  - EK: Q = gap/range vs Q_crit.
  - P3 · drills: an-q-test, an-q-value
- ● **AN-5.2.B** (acs-accm-inorganic:IX.F.1) Propagate random uncertainty through a sum or a product.
  - EK: Absolute in quadrature for sums, relative for products.
  - P1 · drills: an-uncertainty, an-uncertainty-product
- ● **AN-5.2.C** (acs-accm-inorganic:IX.C.2, acs-accm-inorganic:IX.E.2) Choose an analytical technique for a stated question.
  - EK: Trace metals ICP-MS, volatiles GC, non-volatiles HPLC, water Karl Fischer.
  - P2 · drills: an-instrument, an-technique-measures
