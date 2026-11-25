# Process Design, Economics and Safety — curriculum framework (draft 1)

Generated from `drills/frameworks/process-design.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**9 learning objectives** in 3 units (9 core): 9 drilled, 0 partly, 0 with no drills. Core: 9 / 9 drilled.

## Big ideas

- **MONEY · Money has a time value.** A dollar later is worth less than a dollar now; every economic comparison discounts to one date.
- **LAYERS · Safety is layers.** Keep fuel out of its flammable range, exposures under their limits, and find deviations before they happen.
- **DYN · Processes respond with a lag.** A first-order process reaches 63% of a step change in one time constant; control design starts there.

## Practices

- **P1 · Compute.** Carry the calculation to a number.
- **P2 · Judge.** Decide whether a design or exposure is acceptable.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Engineering economics | core | — | 5 | 5 | 0 | 0 |
| 2 · Process safety | core | — | 3 | 3 | 0 | 0 |
| 3 · Process dynamics | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · Engineering economics

Big ideas: MONEY

### 1.1 Time value of money



- ● **PD-1.1.A** Convert a nominal rate to an effective annual rate.
  - EK: (1 + r/m)^m − 1.
  - P1 · drills: pd-effective-rate, pd-nominal-from-effective
- ● **PD-1.1.B** Compute a project's net present value.
  - EK: NPV = −I + A(P/A,i,n) + S(1+i)⁻ⁿ.
  - Needs: PD-1.1.A
  - P1 · drills: pd-npv, pd-capital-recovery
- ● **PD-1.1.C** Compute a simple payback period.
  - EK: Cumulative cash flow covers the investment.
  - P1 · drills: pd-payback, pd-roi

### 1.2 Costs



- ● **PD-1.2.A** Scale an equipment cost by capacity and cost index.
  - EK: C₂ = C₁(S₂/S₁)^0.6 × I₂/I₁.
  - P1 · drills: pd-cost-scaling, pd-capacity-from-budget
- ● **PD-1.2.B** Compute book value under straight-line or declining-balance depreciation.
  - EK: SL (P − S)/n; DDB 2/n of book value.
  - P1 · drills: pd-depreciation, pd-soyd

## Unit 2 · Process safety

Big ideas: LAYERS

### 2.1 Hazards



- ● **PD-2.1.A** (fe-chemical:16.A) Compute the lower flammable limit of a fuel mixture.
  - EK: Le Chatelier: 1/Σ(yᵢ/LFLᵢ).
  - P1 · drills: pd-lfl-mixture, pd-flammable-check
- ● **PD-2.1.B** (fe-chemical:16.B) Judge a mixed exposure against its limits.
  - EK: Σ Cᵢ/TLVᵢ ≤ 1.
  - P2 · drills: pd-tlv-mixture, pd-tlv-allowance
- ● **PD-2.1.C** (fe-chemical:16.C) State what a HAZOP guide word means.
  - EK: NO, MORE, LESS, REVERSE, AS WELL AS, PART OF, OTHER THAN.
  - P2 · drills: pd-hazop, pd-hazop-word

## Unit 3 · Process dynamics

Big ideas: DYN

### 3.1 First-order systems



- ● **PD-3.1.A** Compute the step response of a first-order process.
  - EK: y = KΔu(1 − e^(−t/τ)).
  - P1 · drills: pd-first-order, pd-time-constant-from-data

## Drills not yet placed on the map

- gc-first-order-time (design.control)
- gc-ramp-lag (design.control)
- gc-overshoot (design.control)
- gc-zeta-from-overshoot (design.control)
- gc-p-offset (design.control)
- gc-kc-for-offset (design.control)
- gc-ultimate-gain (design.control)
- gc-stability-check (design.control)
- gc-ultimate-period (design.control)
- gc-zn-reset (design.control)
- gc-amplitude-ratio (design.control)
- gc-phase-lag (design.control)
- gc-fopdt-crossover (design.control)
- gc-fopdt-ultimate-gain (design.control)
- cpd-dihedrals (design.structure)
- cpd-levinthal (design.structure)
- cpd-rotamer-lib (design.structure)
- cpd-rotamer-energy (design.structure)
- cpd-dihedral-which (design.structure)
- cpd-levinthal-time (design.structure)
- cpd-rotamer-apply (design.structure)
- cpd-rotamer-prob (design.structure)
- cpd-pose (design.representation)
- cpd-pose-index (design.representation)
- cpd-centroid (design.representation)
- cpd-centroid-speedup (design.representation)
- cpd-pose-apply (design.representation)
- cpd-pose-reverse (design.representation)
- cpd-resolution-pick (design.representation)
- cpd-atom-count (design.representation)
- cpd-terms (design.energy)
- cpd-weighted-score (design.energy)
- cpd-ref (design.energy)
- cpd-ref-compare (design.energy)
- cpd-units (design.energy)
- cpd-term-decompose (design.energy)
- cpd-term-diagnose (design.energy)
- cpd-weight-change (design.energy)
- cpd-ref-apply (design.energy)
- cpd-ddg-mutation (design.energy)
- cpd-trust-score (design.energy)
- cpd-per-residue (design.energy)
- cpd-metropolis (design.sampling)
- cpd-accept-ratio (design.sampling)
- cpd-packer (design.sampling)
- cpd-pair-table (design.sampling)
- cpd-mc-apply (design.sampling)
- cpd-metropolis-de (design.sampling)
- cpd-protocol-order (design.sampling)
- cpd-pair-table-growth (design.sampling)
- cpd-resfile (design.sequence)
- cpd-seq-space (design.sequence)
- cpd-scan (design.sequence)
- cpd-scan-jobs (design.sequence)
- cpd-recovery (design.sequence)
- cpd-search-methods (design.sequence)
- cpd-task-scenario (design.sequence)
- cpd-alphabet-cut (design.sequence)
- cpd-scan-read (design.sequence)
- cpd-scan-positions (design.sequence)
- cpd-recovery-compare (design.sequence)
- cpd-method-pick (design.sequence)
- cpd-docking (design.interfaces)
- cpd-interface-energy (design.interfaces)
- cpd-ligand (design.interfaces)
- cpd-interface-design (design.interfaces)
- cpd-docking-read (design.interfaces)
- cpd-interface-reverse (design.interfaces)
- cpd-pocket-scenario (design.interfaces)
- cpd-interface-scenario (design.interfaces)
- cpd-denovo-backbone (design.denovo)
- cpd-coiled-coil (design.denovo)
- cpd-hbnet (design.denovo)
- cpd-gap-population (design.denovo)
- cpd-backbone-pick (design.denovo)
- cpd-coiled-coil-length (design.denovo)
- cpd-hbnet-scenario (design.denovo)
- cpd-gap-needed (design.denovo)
- cpd-predictor-inputs (design.ml)
- cpd-coevolution (design.ml)
- cpd-representations (design.ml)
- cpd-diffusion-pipeline (design.ml)
- cpd-funnel-yield (design.ml)
- cpd-self-consistency (design.ml)
- cpd-confidence-scenario (design.ml)
- cpd-msa-scenario (design.ml)
- cpd-representation-pick (design.ml)
- cpd-pipeline-order (design.ml)
- cpd-funnel-reverse (design.ml)
- cpd-evidence-level (design.ml)
- cpd-experiments (design.validation)
- cpd-designs-needed (design.validation)
- cpd-score-vs-alchemical (design.validation)
- cpd-open-problems (design.validation)
- cpd-experiment-order (design.validation)
- cpd-hit-rate (design.validation)
- cpd-method-choice-scenario (design.validation)
- cpd-failure-diagnose (design.validation)
