# Analytical Chemistry — curriculum framework (draft 1)

Generated from `drills/frameworks/analytical-chemistry.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**42 learning objectives** in 6 units (18 core): 42 drilled, 0 partly, 0 with no drills. Core: 18 / 18 drilled.

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
| 6 · Instrumental methods and quality | extension | — | 24 | 24 | 0 | 0 |

## Unit 1 · Titrimetry

Big ideas: MOLES, EQ

### 1.1 Titration types



- ● **AN-1.1.A** (acs-accm-analytical:V.A.1, acs-accm-analytical:V.D.1, acs-accm-analytical:VIII.D.2, acs-accm-analytical:IX.C.1, fe-chemical:5.C) Compute a result from a back titration.
  - EK: Reagent added − reagent left = reagent used.
  - Needs: CH-4.6.A, CH-8.5.C
  - P1 · drills: an-back-titration, an-back-titration-volume
- ● **AN-1.1.B** (acs-accm-analytical:V.D.1) Compute a result from a permanganate titration.
  - EK: Ratio from electrons: MnO₄⁻ 5, Fe²⁺ 1, C₂O₄²⁻ 2.
  - Needs: IN-4.1.A, AN-1.1.A
  - P1 · drills: an-permanganate, an-dichromate-for-permanganate
- ● **AN-1.1.C** (acs-accm-analytical:V.D.1) Compute water hardness from an EDTA titration.
  - EK: EDTA binds metal ions 1:1; report as mg CaCO₃ per L.
  - Needs: AN-1.1.B
  - P1 · drills: an-edta-hardness, an-edta-volume
- ● **AN-1.1.D** (acs-accm-analytical:V.D.1) Compute chloride from a Mohr titration.
  - EK: Ag⁺ + Cl⁻ 1:1; chromate end point at neutral pH.
  - Needs: AN-1.1.C
  - P1 · drills: an-argentometry-why, an-mohr
- ● **AN-1.1.E** Compute protein from a Kjeldahl determination.
  - EK: mol N = acid added − acid left; × factor (6.25).
  - Needs: AN-1.1.A, AN-1.1.D
  - P1 · drills: an-kjeldahl, an-kjeldahl-ammonia

### 1.2 Titration curves



- ● **AN-1.2.A** (acs-accm-analytical:VIII.G.1) Find the pH at any point of a weak-acid–strong-base titration.
  - EK: Start, buffer, equivalence (hydrolysis), excess base.
  - Needs: AN-1.1.E
  - P1 · drills: an-quarter-equivalence, an-titration-ph
- ● **AN-1.2.B** (acs-accm-analytical:V.C.1, acs-accm-analytical:V.F.2, acs-accm-analytical:VIII.A.1) Choose an indicator whose range brackets the equivalence pH.
  - EK: Weak acid + strong base: phenolphthalein.
  - Needs: AN-1.2.A
  - P2 · drills: an-indicator, an-indicator-titration

## Unit 2 · Gravimetric analysis

Big ideas: MOLES

### 2.1 Gravimetric factors



- ● **AN-2.1.A** (acs-accm-analytical:I.E.1, acs-accm-analytical:IX.D.1, fe-chemical:5.C) Compute a mass percent from the weight of a precipitate.
  - EK: Gravimetric factor from molar masses and element counts.
  - Needs: CH-4.5.E
  - P1 · drills: an-gravimetric, an-gravimetric-expected

## Unit 3 · Solubility equilibria in analysis

Big ideas: EQ

### 3.1 Solubility



- ● **AN-3.1.A** (acs-accm-analytical:VIII.C.2, acs-accm-analytical:VIII.E.2) Compute a solubility with a common ion present.
  - EK: s(s + c) = K_sp.
  - Needs: CH-7.12.A
  - P1 · drills: an-common-ion, an-common-ion-factor
- ● **AN-3.1.B** (acs-accm-inorganic:VIII.C.1, acs-accm-analytical:V.A.2, acs-accm-analytical:VIII.C.2) Compute a solubility raised by complex formation.
  - EK: K = K_sp·β₂ for AgX + 2NH₃.
  - Needs: AN-3.1.A
  - P1 · drills: an-complex-dissolve, an-complex-solubility

## Unit 4 · Separations

Big ideas: EQ

### 4.1 Extraction and chromatography



- ● **AN-4.1.A** (acs-accm-analytical:VIII.G.2, acs-accm-analytical:IX.H.2) Compute the fraction left after repeated extractions.
  - EK: q = [V_aq/(V_aq + D V_org)]ⁿ.
  - Needs: CH-3.9.A
  - P1 · drills: an-extraction, an-extractions-needed
- ● **AN-4.1.B** (acs-accm-analytical:IV.C.1, acs-accm-analytical:VIII.G.3, acs-accm-analytical:X.D.2) Compute plate number, retention factor or resolution from a chromatogram.
  - EK: N = 16(t_R/W)², k = (t_R − t_M)/t_M, R_s = 2Δt_R/(W₁+W₂).
  - Needs: AN-4.1.A
  - P1 · drills: an-chromatography, an-resolution-length

## Unit 5 · Measurement, calibration and data

Big ideas: ERROR

### 5.1 Spectrophotometry and calibration



- ● **AN-5.1.A** (acs-accm-analytical:I.D.3) Resolve a two-component mixture by absorbance at two wavelengths.
  - EK: Absorbances add; solve two equations.
  - Needs: CH-0.2.E
  - P1 · drills: an-two-component, an-beer-reverse
- ● **AN-5.1.B** (acs-accm-analytical:IX.A.3, acs-accm-analytical:X.D.1) Find a concentration by standard addition.
  - EK: c = A_x c_s V_s / [V_x (A_sp − A_x)].
  - Needs: AN-5.1.A
  - P1 · drills: an-standard-addition, an-spike-signal
- ● **AN-5.1.C** (acs-accm-general:IX.G.4, acs-accm-analytical:IX.F.3, acs-accm-analytical:X.D.1) Read an unknown off a least-squares calibration line.
  - EK: Slope and intercept from the sums.
  - Needs: AN-5.1.B
  - P1 · drills: an-detection-limit, an-calibration

### 5.2 Data and method choice



- ● **AN-5.2.C** (acs-accm-inorganic:IX.C.2, acs-accm-inorganic:IX.E.2, acs-accm-analytical:VI.A.1, acs-accm-analytical:VI.B.1, acs-accm-analytical:IX.D.5, acs-accm-analytical:IX.H.4, acs-accm-analytical:X.A.1, acs-accm-analytical:X.B.1) Choose an analytical technique for a stated question.
  - EK: Trace metals ICP-MS, volatiles GC, non-volatiles HPLC, water Karl Fischer.
  - Needs: AN-5.1.C
  - P2 · drills: an-instrument, an-technique-measures
- ● **AN-5.2.A** (acs-accm-analytical:IX.F.2, acs-accm-analytical:IX.F.5) Apply Dixon's Q-test to a suspect replicate.
  - EK: Q = gap/range vs Q_crit.
  - Needs: AN-5.2.C
  - P3 · drills: an-q-test, an-q-value
- ● **AN-5.2.B** (acs-accm-inorganic:IX.F.1, acs-accm-analytical:IX.F.2, acs-accm-analytical:IX.F.4) Propagate random uncertainty through a sum or a product.
  - EK: Absolute in quadrature for sums, relative for products.
  - Needs: AN-5.2.A
  - P1 · drills: an-uncertainty, an-uncertainty-product

## Unit 6 · Instrumental methods and quality (extension)

Big ideas: EQ, ERROR

### 6.1 Spectroscopy



- ● **AN-6.1.A** (acs-accm-analytical:I.D.2, acs-accm-analytical:I.D.5, acs-accm-analytical:II.E.1, acs-accm-analytical:VII.A.1, fe-chemical:5.C) Trace the paths an excited molecule takes back to the ground state and tell fluorescence from phosphorescence.
  - EK: Internal conversion and vibrational relaxation are radiationless; fluorescence keeps spin (ns), phosphorescence follows intersystem crossing (ms–s); emission is red-shifted.
  - Needs: AN-1.2.B, AN-5.2.B
  - P1 · drills: an-jablonski, an-fluor-linear
- ● **AN-6.1.B** (acs-accm-analytical:I.D.2, acs-accm-analytical:I.D.3) Convert between transmittance and absorbance and find the concentration where Beer's law holds.
  - EK: A = −log T; 10% T is A = 1; A = εbc is linear for dilute solutions (about A < 1).
  - Needs: AN-6.1.A
  - P1 · drills: an-t-to-a, an-max-conc
- ● **AN-6.1.C** (acs-accm-analytical:I.B.2, acs-accm-analytical:III.D.1) Decide IR and Raman activity from symmetry and count EPR hyperfine lines.
  - EK: IR needs a dipole change, Raman a polarizability change; for a centrosymmetric molecule no mode is both. n equivalent nuclei of spin I split an EPR line into 2nI + 1.
  - Needs: AN-6.1.B
  - P1 · drills: an-epr-lines, an-ir-raman
- ● **AN-6.1.D** (acs-accm-analytical:I.A.2, acs-accm-analytical:I.C.1, acs-accm-analytical:I.D.4, acs-accm-analytical:III.G.1, acs-accm-analytical:IX.D.2, acs-accm-analytical:IX.H.3) Choose the spectrometer components, wavelength and corrections, and anticipate interferences.
  - EK: Measure at λmax; continuum versus line sources; dispersive versus multichannel detection; background subtraction; chemically similar elements interfere; XRF lines scale with Z².
  - Needs: AN-6.1.C
  - P1 · drills: an-spec-choice, an-moseley-ratio

### 6.2 Mass spectrometry and atomic methods



- ● **AN-6.2.A** (acs-accm-analytical:V.B.3, acs-accm-analytical:IX.D.4) Estimate carbon count from the M+1 peak and compute the resolution a mass spectrometer needs.
  - EK: Each carbon adds about 1.1% to M+1; R = m/Δm separates two ions of nearly equal mass.
  - Needs: AN-6.1.D
  - P1 · drills: an-mplus1, an-ms-resolution
- ● **AN-6.2.B** (acs-accm-analytical:II.D.1, acs-accm-analytical:VI.B.1) Choose an atomization or ionization source: flame, furnace, ICP; EI versus ESI and MALDI.
  - EK: Hard ionization (EI) fragments, soft (ESI, MALDI) keeps the molecular ion; ICP's hot plasma atomizes and ionizes for ICP-MS.
  - Needs: AN-6.2.A
  - P1 · drills: an-ion-source, an-esi-mass
- ● **AN-6.2.C** (acs-accm-analytical:I.A.1) Compute an analyte amount by isotope dilution.
  - EK: Spike with an enriched isotope; the measured isotope ratio of the blend gives the original amount without full recovery.
  - Needs: AN-6.2.B
  - P1 · drills: an-isotope-dilution, an-id-mixed

### 6.3 Separations and derivatization



- ● **AN-6.3.A** (acs-accm-analytical:IV.C.1, acs-accm-analytical:IV.C.2) Predict elution order and the effect of solvent strength in normal- and reverse-phase chromatography.
  - EK: Reverse phase (C18, polar mobile phase): polar compounds elute first; more organic solvent speeds elution. Normal phase reverses both.
  - Needs: AN-6.2.C
  - P1 · drills: an-rp-order, an-retention-time
- ● **AN-6.3.B** (acs-accm-analytical:I.G.2) Compute electrophoretic mobility and migration time in capillary electrophoresis.
  - EK: v = (μ_ep + μ_eo)E with E = V/L; cations migrate first with electroosmotic flow toward the cathode.
  - Needs: AN-6.3.A
  - P1 · drills: an-ce-time, an-ce-order
- ● **AN-6.3.C** (acs-accm-analytical:III.F.1, acs-accm-analytical:V.B.2, acs-accm-analytical:V.F.3, acs-accm-analytical:IX.C.1) Choose a derivatization to make an analyte volatile, stable or detectable.
  - EK: Silylation or esterification for GC; chromophore or fluorophore tags for UV and fluorescence; tagging before or after separation.
  - Needs: AN-6.3.B
  - P1 · drills: an-derivatize, an-tag-gain

### 6.4 Thermal and electroanalytical methods



- ● **AN-6.4.A** (acs-accm-analytical:III.H.3, acs-accm-analytical:VI.D.1) Interpret thermogravimetric mass losses and DSC peaks.
  - EK: TGA steps follow loss of water, CO, CO₂ by stoichiometry; DSC peak area gives enthalpy; endotherms for melting, exotherms for crystallization.
  - Needs: AN-6.3.C
  - P1 · drills: an-tga-step, an-dsc-enthalpy
- ● **AN-6.4.B** (acs-accm-analytical:V.B.4, acs-accm-analytical:IX.D.3, acs-accm-analytical:VII.E.1) Choose among potentiometry, voltammetry, amperometry and coulometry, and read a voltammogram.
  - EK: Potentiometry draws no current; voltammetry scans potential and reads current peaks; coulometry counts total charge; enzyme electrodes add selectivity.
  - Needs: AN-6.4.A
  - P1 · drills: an-electro-choice, an-coulometry

### 6.5 Equilibrium in depth



- ● **AN-6.5.A** (acs-accm-analytical:VIII.D.1) Compute the fraction of each form of a diprotic acid at a given pH.
  - EK: α₀ = [H⁺]²/D, α₁ = K₁[H⁺]/D, α₂ = K₁K₂/D with D = [H⁺]² + K₁[H⁺] + K₁K₂.
  - Needs: AN-6.4.B
  - P1 · drills: an-alpha-diprotic, an-alpha-max
- ● **AN-6.5.B** (acs-accm-analytical:VIII.D.2, acs-accm-analytical:VIII.D.6) Compute a conditional formation constant for EDTA at a given pH.
  - EK: K_f′ = α_Y⁴⁻ K_f; titrations need K_f′ large enough (about 10⁸) for a sharp end point.
  - Needs: AN-6.5.A
  - P1 · drills: an-conditional-kf, an-kf-fraction
- ● **AN-6.5.C** (acs-accm-analytical:II.A.1, acs-accm-analytical:VIII.D.3) Correct a solubility for ionic strength with activity coefficients.
  - EK: K_sp = γ₊[M⁺]γ₋[X⁻]: added inert salt lowers γ and raises solubility.
  - Needs: AN-6.5.B
  - P1 · drills: an-activity-solubility, an-ionic-gamma
- ● **AN-6.5.D** (acs-accm-analytical:V.A.2, acs-accm-analytical:VIII.C.1, acs-accm-analytical:VIII.F.5) Use charge and mass balances together when an approximation fails.
  - EK: For very dilute strong acid, [H⁺] = C + [OH⁻] = C + K_w/[H⁺]: 10⁻⁸ M HCl has pH just below 7, not 8.
  - Needs: AN-6.5.C
  - P1 · drills: an-dilute-acid, an-weak-exact

### 6.6 Quality and statistics



- ● **AN-6.6.A** (acs-accm-analytical:IX.A.1, acs-accm-analytical:X.D.1) Compute detection and quantitation limits and sensitivity from blanks and a calibration slope.
  - EK: LOD ≈ 3s_blank/m, LOQ ≈ 10s_blank/m; sensitivity is the calibration slope.
  - Needs: AN-6.5.D
  - P1 · drills: an-lod, an-loq-ratio
- ● **AN-6.6.B** (acs-accm-analytical:IX.A.3) Quantify with an internal standard using a response factor.
  - EK: F = (A_x/[X])/(A_s/[S]) from a standard mixture; then [X] = (A_x/A_s)[S]/F.
  - Needs: AN-6.6.A
  - P1 · drills: an-internal-std, an-cal-choice
- ● **AN-6.6.C** (acs-accm-analytical:IX.C.2) Compute spike recovery and judge whether a method is quantitative.
  - EK: Recovery = (spiked result − unspiked result)/amount added × 100%.
  - Needs: AN-6.6.B
  - P1 · drills: an-recovery, an-limiting-analyte
- ● **AN-6.6.D** (acs-accm-analytical:IX.E.3) Estimate how many samples a heterogeneous lot needs, and pick a sampling plan.
  - EK: n = (t s_s / e)² for sampling standard deviation s_s and allowed error e; random, stratified, systematic and composite sampling.
  - Needs: AN-6.6.C
  - P1 · drills: an-n-samples, an-sampling-plan
- ● **AN-6.6.E** (acs-accm-analytical:IX.F.5, acs-accm-analytical:X.C.1) Compare two means with a t-test.
  - EK: t = |x̄₁ − x̄₂|/(s_pooled √(1/n₁ + 1/n₂)); compare with t from the table.
  - Needs: AN-6.6.D
  - P1 · drills: an-t-two-means, an-t-decide
- ● **AN-6.6.F** (acs-accm-analytical:IX.F.1) Standardize a titrant against a primary standard and explain traceability.
  - EK: KHP (204.22 g/mol) standardizes NaOH 1:1; primary standards are pure, stable, non-hygroscopic and of known formula.
  - Needs: AN-6.6.E
  - P1 · drills: an-khp, an-primary-std
- ● **AN-6.6.G** (acs-accm-analytical:IX.A.2, acs-accm-analytical:IX.E.2, acs-accm-analytical:IX.F.4) Identify random and systematic errors, sample degradation and QC checks.
  - EK: Systematic errors bias results (fix by calibration and blanks); random errors scatter them; control charts track drift; store samples to stop change.
  - Needs: AN-6.6.F
  - P1 · drills: an-error-kind, an-glass-tolerance
- ● **AN-6.6.H** (acs-accm-analytical:X.D.3) Locate an end point from a first-derivative plot.
  - EK: The end point is where ΔpH/ΔV peaks, at the midpoint of the steepest interval.
  - Needs: AN-6.6.G
  - P1 · drills: an-derivative-endpoint, an-log-linear
