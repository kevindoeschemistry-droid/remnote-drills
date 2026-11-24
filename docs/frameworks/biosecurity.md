# Biosecurity — curriculum framework (draft 1)

Generated from `drills/frameworks/biosecurity.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**42 learning objectives** in 7 units (42 core): 42 drilled, 0 partly, 0 with no drills. Core: 42 / 42 drilled.

## Big ideas

- **LAYERS · Defence in depth.** Prevent, detect, withstand and combat are layers; each fails sometimes, and risk falls by stacking layers whose failures are not correlated.
- **GROWTH · Epidemics are exponential, so time is the currency.** Doubling times turn days of delay into multiples of cases; every layer is judged by how much time it buys.
- **NORMS · Norms, rules and safeguards shape what capability becomes.** Treaties, export controls, screening, oversight and model safeguards narrow who can misuse biology without closing the science.

## Practices

- **P1 · Compute.** Carry an epidemic, testing, ventilation or countermeasure calculation to a number.
- **P2 · Explain.** Name the institution, rule or mechanism behind a measure.
- **P3 · Judge.** Choose the right measure, layer or response for a scenario, and say what it buys.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Building a pandemic-proof world | core | — | 5 | 5 | 0 | 0 |
| 7 · Applied epidemiology foundations | core | — | 10 | 10 | 0 | 0 |
| 2 · Preventing engineered pandemics (Prevent) | core | — | 9 | 9 | 0 | 0 |
| 3 · Detecting early infections (Detect) | core | — | 5 | 5 | 0 | 0 |
| 4 · Blocking transmission (Withstand) | core | — | 5 | 5 | 0 | 0 |
| 5 · Exiting the pandemic (Combat) | core | — | 6 | 6 | 0 | 0 |
| 6 · Contributing to biosecurity | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Building a pandemic-proof world

Big ideas: GROWTH, LAYERS

### 1.1 Epidemic arithmetic



- ● **BS-1.1.A** Relate the reproduction number, growth rate, generation interval and doubling time.
  - EK: T_d = ln 2 / r; with a fixed generation interval T_g, R = e^{rT_g}.
  - P1 · drills: bs-doubling-time, bs-r-from-doubling
- ● **BS-1.1.B** Compute the herd-immunity threshold from R₀, and R₀ from it.
  - EK: Threshold = 1 − 1/R₀.
  - P1 · drills: bs-herd-threshold, bs-r0-from-threshold
- ● **BS-1.1.C** Distinguish case and infection fatality ratios and correct for under-ascertainment.
  - EK: CFR = deaths/confirmed cases; IFR = deaths/infections; infections ≈ cases ÷ ascertainment.
  - P1 · P2 · drills: bs-ifr-from-cfr, bs-fatality-bias

### 1.2 Threat landscape and history



- ● **BS-1.2.A** Place landmark events in the history of pandemics and biological weapons.
  - EK: 1918 influenza; smallpox eradication certified 1980; BWC 1972; Sverdlovsk 1979; the 2001 anthrax letters.
  - P2 · drills: bs-history-facts, bs-history-order
- ● **BS-1.2.B** Distinguish natural, accidental and deliberate biological risks and say what makes a risk catastrophic.
  - EK: Spillover, lab accident, misuse; transmissibility, severity and our ability to respond set the scale.
  - P2 · P3 · drills: bs-risk-source, bs-gcbr-features

## Unit 7 · Applied epidemiology foundations

Big ideas: GROWTH

### 7.1 Disease occurrence



- ● **BS-7.1.A** (cdc-ss1978:L1) Name the links in the chain of infection and the stages of natural history, and say which measure breaks which link.
  - EK: Reservoir, portal of exit, transmission, portal of entry, susceptible host; incubation, latent and infectious periods.
  - P2 · P3 · drills: bs-chain-link, bs-natural-history
- ● **BS-7.1.B** (cdc-ss1978:L1, cdc-ss1978:L4) Read an epidemic curve: point source, continuous or propagated, and the likely exposure time.
  - EK: Point source: one peak about one incubation period wide; exposure ≈ peak − median incubation.
  - P1 · P2 · drills: bs-exposure-from-peak, bs-epicurve-shape

### 7.2 Measures of risk



- ● **BS-7.2.A** (cdc-ss1978:L3) Compute attack rates and secondary attack rates.
  - EK: Attack rate = cases ÷ population at risk; secondary attack rate counts contacts of primary cases only.
  - P1 · drills: bs-attack-rate, bs-secondary-attack
- ● **BS-7.2.B** (cdc-ss1978:L3) Distinguish incidence from prevalence and relate them through duration.
  - EK: Prevalence ≈ incidence rate × mean duration (steady state).
  - P1 · P2 · drills: bs-prevalence-from-incidence, bs-incidence-or-prevalence
- ● **BS-7.2.C** (cdc-ss1978:L3) Compute a risk ratio or an odds ratio from a 2 × 2 table and say which design gives which.
  - EK: Cohort: RR = (a/(a+b))/(c/(c+d)); case-control: OR = ad/bc.
  - P1 · drills: bs-risk-ratio, bs-odds-ratio
- ● **BS-7.2.D** (cdc-ss1978:L3) Compute attributable risk and the population attributable fraction.
  - EK: AR% among exposed = (RR − 1)/RR; PAF = p(RR − 1)/(1 + p(RR − 1)).
  - P1 · drills: bs-attributable-fraction-exposed, bs-paf

### 7.3 Surveillance and outbreak investigation



- ● **BS-7.3.A** (cdc-ss1978:L6) Order the steps of an outbreak investigation and apply case definitions.
  - EK: Prepare, confirm the outbreak, verify the diagnosis, define and find cases, describe by time, place and person, hypothesise, test, control, communicate.
  - P2 · P3 · drills: bs-investigation-steps, bs-case-definition
- ● **BS-7.3.B** (cdc-ss1978:L5) Evaluate a surveillance system by sensitivity, predictive value and timeliness.
  - EK: Sensitivity = cases detected ÷ true cases; PVP = true cases ÷ cases reported.
  - P1 · P2 · drills: bs-surveillance-sensitivity, bs-surveillance-pvp

### 7.4 Transmission dynamics



- ● **BS-7.4.A** Compute the final size of an epidemic and the effective reproduction number as susceptibles fall.
  - EK: Final size z solves z = 1 − e^{−R₀z}; R_eff = R₀ × susceptible fraction.
  - P1 · drills: bs-final-size, bs-reff-susceptibles
- ● **BS-7.4.B** Explain superspreading with the dispersion parameter and compute the chance a case transmits to no one.
  - EK: Negative binomial offspring: P(0) = (1 + R/k)^{−k}; small k means most cases infect no one and a few infect many.
  - P1 · P2 · drills: bs-zero-offspring, bs-superspreading

## Unit 2 · Preventing engineered pandemics (Prevent)

Big ideas: NORMS, LAYERS

### 2.1 Treaties and export controls



- ● **BS-2.1.A** (bwc:I, bwc:IV, bwc:XII) State what the BWC prohibits, how it is implemented and reviewed, and what it lacks.
  - EK: Article I: never develop, produce, stockpile or acquire; no verification regime; confidence-building measures; a small Implementation Support Unit.
  - P2 · drills: bs-bwc-facts, bs-bwc-scenario
- ● **BS-2.1.B** Match export controls and other regimes (Australia Group, UNSCR 1540) to what they do.
  - EK: Australia Group harmonises national export lists; UNSCR 1540 obliges states to keep WMD from non-state actors.
  - P2 · drills: bs-export-controls, bs-regime-match

### 2.2 Safeguarding research and its tools



- ● **BS-2.2.A** Explain DNA synthesis screening: what is screened and why both sequence and customer matter.
  - EK: Screen orders against sequences of concern and verify customers; benchtop synthesisers move the checkpoint.
  - P2 · P3 · drills: bs-synthesis-screening, bs-screening-scenario
- ● **BS-2.2.B** Recognise dual-use research of concern and the oversight and publication choices around it.
  - EK: Research reasonably expected to give knowledge or products that could be misapplied; review before funding and before publishing.
  - P2 · P3 · drills: bs-durc-facts, bs-durc-scenario
- ● **BS-2.2.C** Describe layered AI model safeguards and compute the residual risk through independent layers.
  - EK: Refusal training, input/output classifiers, evaluations, access controls; residual = product of each layer's miss rate.
  - P1 · P2 · drills: bs-layered-miss, bs-ai-safeguards

### 2.3 Laboratory biosafety and biosecurity



- ● **BS-2.3.A** (who-lbm4:2, who-lbm4:3, who-lbm4:4, who-lbm4:5) Use the WHO risk-based approach: inherent versus residual risk, core requirements, heightened control and maximum containment.
  - EK: Risk assessment decides the controls; core requirements apply everywhere.
  - P2 · P3 · drills: bs-lbm4-levels, bs-lbm4-scenario
- ● **BS-2.3.B** (who-lbm4:3, who-lbm4:4) Choose primary containment (biosafety cabinet class) and compute filter penetration.
  - EK: Class I protects worker and environment, II also the sample, III is gas-tight; HEPA ≥ 99.97% at the most penetrating size.
  - P1 · P3 · drills: bs-bsc-class, bs-hepa-series
- ● **BS-2.3.C** (who-lbm4:3) Compute decontamination by log reduction and D-values.
  - EK: N = N₀·10^{−t/D}; a 6-log kill takes six D-values.
  - P1 · drills: bs-autoclave-time, bs-log-reduction

### 2.4 National health security capacities



- ● **BS-2.4.A** (who-jee3:P7, who-jee3:D2, who-jee3:R2) Place a national capacity in its JEE technical area and pillar.
  - EK: Prevent P1–P8, Detect D1–D3, Respond R1–R5, plus points of entry, chemical and radiation events.
  - P2 · drills: bs-jee-area, bs-jee-pillar

## Unit 3 · Detecting early infections (Detect)

Big ideas: GROWTH

### 3.1 Surveillance



- ● **BS-3.1.A** Match surveillance systems to what they see and name the IHR's notification duties.
  - EK: Syndromic, wastewater, metagenomic, clinical; IHR (2005) PHEIC and, since 2025, the pandemic emergency.
  - P2 · drills: bs-surveillance-match, bs-ihr-facts
- ● **BS-3.1.B** Compute how detection delay translates into cases.
  - EK: Cases at time t = initial × 2^{t/T_d}.
  - P1 · drills: bs-detection-delay, bs-days-to-threshold
- ● **BS-3.1.C** Compute the sequencing depth needed to see a target at a given relative abundance.
  - EK: Expected target reads = total reads × relative abundance.
  - P1 · drills: bs-reads-needed, bs-abundance-growth
- ● **BS-3.1.D** Compute the probability that sequencing sees at least one target read.
  - EK: Reads are Poisson: P(≥ 1) = 1 − e^{−λ}; 95% needs λ ≈ 3.
  - P1 · drills: bs-detect-prob, bs-depth-for-confidence

### 3.2 Diagnostics



- ● **BS-3.2.A** Compute predictive values of a test from sensitivity, specificity and prevalence.
  - EK: PPV falls as prevalence falls; a second independent positive raises it.
  - P1 · drills: bs-ppv, bs-ppv-two-tests

## Unit 4 · Blocking transmission (Withstand)

Big ideas: LAYERS, GROWTH

### 4.1 Clean air



- ● **BS-4.1.A** Estimate airborne infection risk with the Wells–Riley model and combine air-cleaning rates.
  - EK: P = 1 − exp(−Iqpt/Q); equivalent air changes add.
  - P1 · drills: bs-wells-riley, bs-each-sum
- ● **BS-4.1.B** Explain far-UVC, filtration and ventilation and compute clearance times.
  - EK: 222 nm barely penetrates the skin's dead layer; 99% removal takes ln 100 / ACH hours.
  - P1 · P2 · drills: bs-clearance-time, bs-far-uvc
- ● **BS-4.1.C** (ashrae-241:5) Check a room against an equivalent clean airflow per person target.
  - EK: Total clean air = outdoor air + filtered recirculation × efficiency + air cleaners; ECA per person = total ÷ occupants.
  - P1 · drills: bs-eca-per-person, bs-occupancy-limit

### 4.2 PPE and social measures



- ● **BS-4.2.A** Compare respirator classes by filtration and assigned protection factor, and compute the effect of masking on R.
  - EK: N95 filters ≥ 95%; APF 10 half-mask, 50 full-face, 25 loose PAPR; R_eff = R(1 − ce).
  - P1 · P2 · drills: bs-respirator-facts, bs-mask-reff
- ● **BS-4.2.B** Compute the effect of testing, isolation and contact tracing on R, and match measures to transmission routes.
  - EK: Removing a fraction f of onward transmission multiplies R by 1 − f.
  - P1 · P3 · drills: bs-isolation-reff, bs-npi-match

## Unit 5 · Exiting the pandemic (Combat)

Big ideas: GROWTH, LAYERS

### 5.1 Countermeasures



- ● **BS-5.1.A** Compute the vaccination coverage needed for herd protection given vaccine efficacy.
  - EK: V_c = (1 − 1/R₀)/E; above 100% means vaccination alone cannot stop spread.
  - P1 · drills: bs-vaccine-coverage, bs-efficacy-needed
- ● **BS-5.1.B** Compute vaccine efficacy from trial attack rates.
  - EK: VE = 1 − AR_vaccinated / AR_unvaccinated.
  - P1 · drills: bs-ve-trial, bs-ve-expected-cases
- ● **BS-5.1.C** Describe rapid countermeasure programmes: platforms, the 100 Days Mission, financing and trials.
  - EK: CEPI's goal: vaccines within 100 days of a threat; platform technologies; advance commitments.
  - P2 · drills: bs-mcm-facts, bs-mcm-scenario
- ● **BS-5.1.D** Compute the number needed to vaccinate and the expected cases averted.
  - EK: NNV = 1/(AR_unvaccinated × VE).
  - P1 · drills: bs-nnv, bs-cases-averted

### 5.2 Scale-up and governance



- ● **BS-5.2.A** Compute manufacturing and delivery rates needed to cover a population in time.
  - EK: Doses per day = population × doses per person ÷ days.
  - P1 · drills: bs-doses-per-day, bs-campaign-days
- ● **BS-5.2.B** Name the global health governance instruments and who decides what.
  - EK: IHR (2005) and its 2024 amendments; the WHO Pandemic Agreement (2025); the Director-General declares a PHEIC on Emergency Committee advice.
  - P2 · drills: bs-governance-facts, bs-who-decides

## Unit 6 · Contributing to biosecurity

Big ideas: LAYERS, NORMS

### 6.1 Working responsibly and choosing a focus



- ● **BS-6.1.A** Apply information-hazard norms in discussion and writing.
  - EK: Don't brainstorm new ways to cause harm; discuss defences, not attack details; ask before sharing.
  - P3 · drills: bs-infohazard, bs-infohazard-scenario
- ● **BS-6.1.B** Map an intervention to its layer and compute the combined protection of independent layers.
  - EK: P(all layers fail) = product of each layer's failure probability.
  - P1 · P3 · drills: bs-defence-layers, bs-layer-match
