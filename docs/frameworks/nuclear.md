# Nuclear Science and Reactor Theory — curriculum framework (draft 1)

Generated from `drills/frameworks/nuclear.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**19 learning objectives** in 7 units (19 core): 19 drilled, 0 partly, 0 with no drills. Core: 19 / 19 drilled.

## Big ideas

- **BALANCE · A reactor is a neutron balance.** Each generation, neutrons are produced by fission and lost to absorption and leakage. Critical means the two are equal; everything an operator does shifts one side of that balance.
- **EXPONENTIAL · Decay, attenuation and power all go exponentially.** A constant fractional rate gives a half-life, a half-value layer or a reactor period. One piece of mathematics, three settings.
- **DELAYED · A small delayed fraction makes control possible.** Fewer than one neutron in a hundred is delayed, yet those set the timescale of every normal power change.

## Practices

- **P1 · Compute.** Carry a decay, shielding, criticality or kinetics relation to a number.
- **P2 · Predict the direction.** Say whether a change adds or removes reactivity, dose or heat, and why.
- **P3 · Recall an anchor.** Know the handful of magnitudes the field runs on.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Nuclei and radioactive decay | core | — | 3 | 3 | 0 | 0 |
| 2 · Radiation, dose and shielding | core | — | 3 | 3 | 0 | 0 |
| 3 · Neutrons | core | — | 2 | 2 | 0 | 0 |
| 4 · The neutron life cycle and reactivity | core | — | 3 | 3 | 0 | 0 |
| 5 · Kinetics | core | — | 1 | 1 | 0 | 0 |
| 6 · Reactivity effects, poisons and heat | core | — | 3 | 3 | 0 | 0 |
| 7 · Radioactivity in practice | core | — | 4 | 4 | 0 | 0 |

## Unit 1 · Nuclei and radioactive decay

Big ideas: EXPONENTIAL

### 1.1 Nuclides and decay modes



- ● **NU-1.1.A** (doe-hdbk-1019:1) Read nuclide notation and find the daughter of an alpha, beta-minus or positron decay.
  - EK: N = A − Z; charge and nucleon number are conserved in every decay.
  - P1 · drills: nu-neutron-number, nu-decay-daughter
- ● **NU-1.1.B** (doe-hdbk-1019:1) Turn a mass defect into a binding energy per nucleon.
  - EK: 1 u = 931.5 MeV; the curve peaks near iron at about 8.8 MeV per nucleon.
  - P1 · P3 · drills: nu-binding-energy, nu-defect-from-b

### 1.2 The decay law



- ● **NU-1.2.A** (doe-hdbk-1019:1) Use a half-life to find the fraction remaining, the time to reach a given fraction, and the decay constant.
  - EK: N = N₀(½)^(t/T); λ = ln 2 / T; ten half-lives is a factor of about a thousand.
  - P1 · drills: nu-fraction-remaining, nu-time-to-decay, nu-decay-constant

## Unit 2 · Radiation, dose and shielding

Big ideas: EXPONENTIAL

### 2.1 Distance and shielding



- ● **NU-2.1.A** (doe-hdbk-1019:1) Apply the inverse-square law to a point source.
  - EK: Dose rate × r² is constant.
  - P1 · drills: nu-inverse-square, nu-distance-for-rate
- ● **NU-2.1.B** (doe-hdbk-1019:1) Compute gamma attenuation from a linear attenuation coefficient or a half-value layer, and choose a shield for each kind of radiation.
  - EK: I = I₀e^(−μx); HVL = ln 2 / μ; paper for alpha, plastic for beta, dense for gamma, hydrogen for neutrons.
  - P1 · P2 · drills: nu-shielding-choice, nu-half-value-layers, nu-attenuation-coefficient

### 2.2 Dose



- ● **NU-2.2.A** Convert an absorbed dose to an equivalent dose.
  - EK: H (Sv) = w_R × D (Gy); w_R is 1 for photons and betas, 20 for alphas.
  - P1 · drills: nu-equivalent-dose, nu-effective-dose

## Unit 3 · Neutrons

Big ideas: BALANCE, DELAYED

### 3.1 Cross sections



- ● **NU-3.1.A** (doe-hdbk-1019:2) Compute a macroscopic cross section and a mean free path.
  - EK: Σ = Nσ; mean free path = 1/Σ.
  - P1 · drills: nu-mean-free-path, nu-macroscopic-cross-section

### 3.2 Prompt, delayed and thermal neutrons



- ● **NU-3.2.A** (nrc-gfe:192001) Explain where delayed neutrons come from and why they matter, what a moderator does, and the energy of a thermal neutron.
  - EK: β ≈ 0.0065 for U-235; kT = 0.025 eV at room temperature, 2200 m/s.
  - P1 · P3 · drills: nu-neutron-facts, nu-thermal-neutron-energy

## Unit 4 · The neutron life cycle and reactivity

Big ideas: BALANCE, DELAYED

### 4.1 k-effective



- ● **NU-4.1.A** (nrc-gfe:192002) Compute k-effective from the six factors and classify the state of a core.
  - EK: k_eff = ε L_f p L_t f η; subcritical, critical, delayed supercritical, prompt critical.
  - P1 · P2 · drills: nu-criticality-state, nu-six-factor
- ● **NU-4.1.B** (nrc-gfe:192002) Convert k-effective to reactivity.
  - EK: ρ = (k − 1)/k; 1 pcm = 10⁻⁵; one dollar is ρ = β.
  - P1 · drills: nu-reactivity-pcm, nu-k-from-rho

### 4.2 Subcritical multiplication



- ● **NU-4.2.A** (nrc-gfe:192003) Find the multiplication of a source in a subcritical core.
  - EK: M = 1/(1 − k); 1/M falls to zero at criticality.
  - P1 · drills: nu-subcritical-multiplication, nu-count-ratio

## Unit 5 · Kinetics

Big ideas: EXPONENTIAL, DELAYED

### 5.1 Period



- ● **NU-5.1.A** (nrc-gfe:192003) Estimate the stable period for a small reactivity addition and the power change on a period.
  - EK: τ ≈ (β − ρ)/(λρ); P = P₀e^(t/τ); doubling time 0.693τ.
  - P1 · drills: nu-reactor-period, nu-power-on-a-period

## Unit 6 · Reactivity effects, poisons and heat

Big ideas: BALANCE

### 6.1 What moves reactivity



- ● **NU-6.1.A** (nrc-gfe:192004, nrc-gfe:192005, nrc-gfe:192007) Predict the sign of the reactivity change from temperature, control rods, boron, burnup and burnable poisons.
  - EK: More absorption or less fuel is negative; removing an absorber is positive; fuel and moderator temperature feedback are negative by design.
  - P2 · drills: nu-reactivity-effects, nu-reactivity-2
- ● **NU-6.1.B** (nrc-gfe:192006) Describe how xenon-135 and samarium-149 are produced and removed, and what xenon does after a shutdown.
  - EK: Xenon comes mostly from iodine-135, is removed by burnup and decay, and peaks about ten hours after shutdown.
  - P2 · P3 · drills: nu-xenon-facts, nu-iodine-left

### 6.2 Energy



- ● **NU-6.2.A** Relate thermal power to fuel consumed, and state the size of decay heat after shutdown.
  - EK: About 200 MeV per fission, so about 1 g of U-235 per megawatt-day; decay heat starts at 6–7% of full power.
  - P1 · P3 · drills: nu-decay-heat, nu-fuel-consumption

## Unit 7 · Radioactivity in practice

Big ideas: EXPONENTIAL

### 7.1 Chains, activity and dating



- ● **NU-7.1.A** (doe-hdbk-1019:1) Follow a nuclide through a sequence of alpha and beta decays and count the decays in a series.
  - EK: Alpha: Z − 2, A − 4. Beta-minus: Z + 1. Only alphas change A.
  - P1 · drills: ra-decay-chain, ra-count-alphas
- ● **NU-7.1.B** (doe-hdbk-1019:1, acs-accm-analytical:I.F.1) Calculate an activity from a mass and a half-life, and convert between becquerels and curies.
  - EK: A = λN; 1 Ci = 3.7 × 10¹⁰ Bq.
  - P1 · P3 · drills: ra-becquerel-curie, ra-activity-from-mass
- ● **NU-7.1.C** (doe-hdbk-1019:1) Date a sample from its remaining activity and find an effective half-life in the body.
  - EK: t = T ln(1/f)/ln 2; removal rates add.
  - P1 · drills: ra-carbon-dating, ra-effective-half-life
- ● **NU-7.1.D** (doe-hdbk-1019:1) Calculate a Q-value from a mass difference and describe secular equilibrium.
  - EK: 931.5 MeV per u; at equilibrium parent and daughter activities are equal.
  - P1 · P2 · drills: ra-secular-equilibrium, ra-q-value

## Drills not yet placed on the map

- ac-mass-energy (nuc.decay)
