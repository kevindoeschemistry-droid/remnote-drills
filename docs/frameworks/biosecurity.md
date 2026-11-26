# Biosecurity — curriculum framework (draft 1)

Generated from `drills/frameworks/biosecurity.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**64 learning objectives** in 8 units (42 core): 64 drilled, 0 partly, 0 with no drills. Core: 42 / 42 drilled.

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
| 8 · Health-system capacities and treaty machinery | extension | — | 22 | 22 | 0 | 0 |

## Unit 1 · Building a pandemic-proof world

Big ideas: GROWTH, LAYERS

### 1.1 Epidemic arithmetic



- ● **BS-1.1.A** Relate the reproduction number, growth rate, generation interval and doubling time.
  - EK: T_d = ln 2 / r; with a fixed generation interval T_g, R = e^{rT_g}.
  - P1 · drills: bs-doubling-time, bs-r-from-doubling
- ● **BS-1.1.B** Compute the herd-immunity threshold from R₀, and R₀ from it.
  - EK: Threshold = 1 − 1/R₀.
  - P1 · drills: bs-r0-from-threshold, bs-herd-threshold
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
  - P1 · drills: bs-secondary-attack, bs-attack-rate
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



- ● **BS-5.1.C** Describe rapid countermeasure programmes: platforms, the 100 Days Mission, financing and trials.
  - EK: CEPI's goal: vaccines within 100 days of a threat; platform technologies; advance commitments.
  - P2 · drills: bs-mcm-facts, bs-mcm-scenario
- ● **BS-5.1.A** Compute the vaccination coverage needed for herd protection given vaccine efficacy.
  - EK: V_c = (1 − 1/R₀)/E; above 100% means vaccination alone cannot stop spread.
  - P1 · drills: bs-vaccine-coverage, bs-efficacy-needed
- ● **BS-5.1.B** Compute vaccine efficacy from trial attack rates.
  - EK: VE = 1 − AR_vaccinated / AR_unvaccinated.
  - P1 · drills: bs-ve-trial, bs-ve-expected-cases
- ● **BS-5.1.D** Compute the number needed to vaccinate and the expected cases averted.
  - EK: NNV = 1/(AR_unvaccinated × VE).
  - P1 · drills: bs-nnv, bs-cases-averted

### 5.2 Scale-up and governance



- ● **BS-5.2.B** Name the global health governance instruments and who decides what.
  - EK: IHR (2005) and its 2024 amendments; the WHO Pandemic Agreement (2025); the Director-General declares a PHEIC on Emergency Committee advice.
  - P2 · drills: bs-governance-facts, bs-who-decides
- ● **BS-5.2.A** Compute manufacturing and delivery rates needed to cover a population in time.
  - EK: Doses per day = population × doses per person ÷ days.
  - P1 · drills: bs-doses-per-day, bs-campaign-days

## Unit 6 · Contributing to biosecurity

Big ideas: LAYERS, NORMS

### 6.1 Working responsibly and choosing a focus



- ● **BS-6.1.A** Apply information-hazard norms in discussion and writing.
  - EK: Don't brainstorm new ways to cause harm; discuss defences, not attack details; ask before sharing.
  - P3 · drills: bs-infohazard, bs-infohazard-scenario
- ● **BS-6.1.B** Map an intervention to its layer and compute the combined protection of independent layers.
  - EK: P(all layers fail) = product of each layer's failure probability.
  - P1 · P3 · drills: bs-defence-layers, bs-layer-match

## Unit 8 · Health-system capacities and treaty machinery (extension)

Big ideas: NORMS

### 8.1 Prevent capacities



- ● **BS-8.1.A** (who-jee3:P1, who-jee3:P2) State what the legal-instruments and financing capacities require of a country
  - EK: A country needs the laws and regulations that let it act in an emergency, assessed before the emergency rather than drafted during it, and a financing route that releases money fast enough to matter; both are capacities that look like paperwork and fail only when they are needed.
  - P2 · drills: bs-legal-financing, bs-fund-delay
- ● **BS-8.1.B** (who-jee3:P3) State what the National IHR Focal Point is for and what it must be able to do
  - EK: Every State Party names a focal point reachable at all times that notifies the WHO of events and relays information inside the country, so the capacity being assessed is a channel and the authority to use it, not an office.
  - P2 · drills: bs-nfp, bs-notification-window
- ● **BS-8.1.C** (who-jee3:P4) Compute antimicrobial consumption in defined daily doses per 1000 inhabitants per day
  - EK: Consumption is reported in defined daily doses per thousand inhabitants per day so that countries and years can be compared, and it is the denominator against which a resistance trend is read: rising resistance with flat consumption points somewhere other than prescribing.
  - P1 · drills: bs-ddd, bs-consumption-change
- ● **BS-8.1.D** (who-jee3:P4) Compute a resistance proportion and what a stated change means for empirical therapy
  - EK: A resistance proportion is isolates resistant over isolates tested, and once it passes the threshold a guideline sets, the empirical first choice has to change: the number is surveillance, the threshold is policy.
  - P1 · drills: bs-resistance-proportion, bs-empirical-failure
- ● **BS-8.1.E** (who-jee3:P5, who-jee3:P6) State what zoonotic-disease and food-safety capacities each require and where they meet
  - EK: Zoonotic capacity is joint human, animal and environmental surveillance with a route for one sector to act on another's signal; food safety is the ability to trace a contaminated product and recall it. Both are One Health capacities, and most emerging human pathogens arrive through them.
  - P2 · drills: bs-one-health, bs-spillover-sampling
- ● **BS-8.1.F** (who-jee3:P6) Compute an attack rate and the food-specific risk ratio in a stated outbreak investigation
  - EK: A food-specific attack rate among those who ate an item, against those who did not, gives the risk ratio that identifies the vehicle; the investigation is a case-control or cohort calculation done against the clock.
  - P1 · drills: bs-food-risk-ratio, bs-event-attack-rate
- ● **BS-8.1.G** (who-jee3:P8) Compute the immunization coverage a stated reproduction number needs, and the effective coverage a vaccine's efficacy gives
  - EK: The herd-immunity threshold is one minus the reciprocal of the reproduction number, and because no vaccine is perfectly effective the coverage needed is that threshold divided by the efficacy, which is why a highly transmissible pathogen can need coverage above what any real programme reaches.
  - P1 · drills: bs-coverage-gap, bs-herd-coverage-vaccine

### 8.2 Detect and respond capacities



- ● **BS-8.2.A** (who-jee3:D1) State what a national laboratory system must provide and what tiering it
  - EK: The capacity is reliable testing for the priority diseases, a specimen referral and transport system that reaches it, and a quality system that makes the results trustworthy; tiering puts screening near the patient and confirmation in reference laboratories.
  - P2 · drills: bs-lab-system, bs-lab-capacity
- ● **BS-8.2.B** (who-jee3:D1) Compute specimen turnaround time and what a stated referral delay costs an outbreak response
  - EK: Turnaround is collection to result, and every day of it is a day of transmission the response cannot act on: a test that is accurate but slow has the epidemiological value of a test that is not done.
  - P1 · drills: bs-turnaround, bs-referral-saving
- ● **BS-8.2.C** (who-jee3:D3) Compute a public-health workforce density and the field-epidemiology output a stated target needs
  - EK: Workforce capacity is measured as staff per unit population, and a trained field epidemiologist is the scarcest part: a programme graduating a fixed cohort a year takes a predictable number of years to reach a density target.
  - P1 · drills: bs-workforce-density, bs-fetp-years
- ● **BS-8.2.D** (who-jee3:R1) State what health emergency management requires beyond a written plan
  - EK: The capacity is an emergency operations centre that can be activated within hours with named people, a plan that has been exercised, and the legal authority to direct resources; a plan that has never been exercised is evidence of intent rather than of capacity.
  - P2 · drills: bs-emergency-management, bs-eoc-activation
- ● **BS-8.2.E** (who-jee3:R3) Compute the surge demand a stated caseload puts on beds and oxygen
  - EK: Surge demand is incident cases times the fraction needing that level of care times the length of stay, which converts an epidemic curve into beds and oxygen: the peak, not the total, is what decides whether the system holds.
  - P1 · drills: bs-surge-beds, bs-oxygen-demand
- ● **BS-8.2.F** (who-jee3:R4) Compute a healthcare-associated infection rate and the effect of a stated compliance change
  - EK: Infection rates are reported per thousand patient-days or per device-day so that a busier ward is comparable with a quieter one, and the interventions that move them are hand hygiene, device care and isolation rather than new agents.
  - P1 · drills: bs-hai-rate, bs-ipc-effect
- ● **BS-8.2.G** (who-jee3:R5) State what risk communication and community engagement must achieve and how it fails
  - EK: The capacity is a channel to the public that is in place before the emergency and trusted when it arrives, with messages that say what is known, what is not, and what to do; it fails by silence, by over-reassurance later contradicted, and by addressing a population that does not use that channel.
  - P2 · drills: bs-risk-comms, bs-comms-reach

### 8.3 Hazard-specific and border capacities



- ● **BS-8.3.A** (who-jee3:PoE) Compute the detections a stated border screening programme can expect, and its positive predictive value
  - EK: Entry screening detects the fraction of infected travellers who are symptomatic at that moment, so for a pathogen with a long incubation it finds very few; the arithmetic is why border measures delay rather than prevent introduction.
  - P1 · drills: bs-border-screening, bs-screening-ppv
- ● **BS-8.3.B** (who-jee3:CE) Compute the dilution or distance a stated chemical release requires to reach an exposure guideline
  - EK: Chemical-event capacity is an inventory of what is held where, guideline exposure levels for each, and the ability to model a release well enough to decide who shelters and who evacuates.
  - P1 · drills: bs-chemical-dilution, bs-shelter-decision
- ● **BS-8.3.C** (who-jee3:RE) Compute dose rate against distance, time and shielding for a stated radiation source
  - EK: Dose rate falls with the square of distance, rises with time and falls by half for each half-value layer of shielding, which is the whole of protective practice: distance first because it is free, then time, then shielding.
  - P1 · drills: bs-dose-distance, bs-shielding-layers
- ● **BS-8.3.D** (who-jee3:RE) Compute the activity left after a stated decay time and when a source reaches a release level
  - EK: Activity falls by half each half-life, so a short-lived isotope is managed by waiting and a long-lived one by containment; which it is decides whether an incident is an evacuation or a cordon.
  - P1 · drills: bs-activity-decay, bs-decay-time

### 8.4 Treaty machinery



- ● **BS-8.4.A** (bwc:II, bwc:III) State what Articles II and III of the Convention require and of whom
  - EK: Article II requires existing stocks to be destroyed or diverted to peaceful purposes, and Article III forbids transferring the agents or assisting anyone to acquire them, which is what makes export controls and screening a treaty obligation rather than a courtesy.
  - P2 · drills: bs-bwc-ii-iii, bs-bwc-parties
- ● **BS-8.4.B** (bwc:V, bwc:VI) State the routes the Convention gives for dealing with a suspected breach
  - EK: Article V provides for consultation and cooperation among the Parties, and Article VI allows a complaint to the Security Council, which may investigate; the Convention has no verification organisation of its own, which is the structural weakness every review conference returns to.
  - P2 · drills: bs-bwc-breach, bs-review-conference
- ● **BS-8.4.C** (bwc:VII) State what Article VII provides and what triggers it
  - EK: A Party exposed to danger as a result of a violation may request assistance, and the other Parties undertake to provide it if the Security Council decides the Party has been exposed; the obligation is to help a victim, not to deter an attacker.
  - P2 · drills: bs-bwc-vii, bs-assistance-shortfall
- ● **BS-8.4.D** (bwc:X) State what Article X protects and the tension it creates with Article III
  - EK: Article X protects the right to exchange equipment, materials and information for peaceful purposes and to participate in that exchange, so every control measure under Article III has to be justified against it: the Convention's bargain is non-proliferation without blocking public-health and industrial biology.
  - P2 · drills: bs-bwc-x, bs-screening-coverage
