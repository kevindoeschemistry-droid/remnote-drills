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
  - P1 · drills: pd-effective-rate
- ● **PD-1.1.B** Compute a project's net present value.
  - EK: NPV = −I + A(P/A,i,n) + S(1+i)⁻ⁿ.
  - Needs: PD-1.1.A
  - P1 · drills: pd-npv
- ● **PD-1.1.C** Compute a simple payback period.
  - EK: Cumulative cash flow covers the investment.
  - P1 · drills: pd-payback

### 1.2 Costs



- ● **PD-1.2.A** Scale an equipment cost by capacity and cost index.
  - EK: C₂ = C₁(S₂/S₁)^0.6 × I₂/I₁.
  - P1 · drills: pd-cost-scaling
- ● **PD-1.2.B** Compute book value under straight-line or declining-balance depreciation.
  - EK: SL (P − S)/n; DDB 2/n of book value.
  - P1 · drills: pd-depreciation

## Unit 2 · Process safety

Big ideas: LAYERS

### 2.1 Hazards



- ● **PD-2.1.A** (fe-chemical:16.A) Compute the lower flammable limit of a fuel mixture.
  - EK: Le Chatelier: 1/Σ(yᵢ/LFLᵢ).
  - P1 · drills: pd-lfl-mixture
- ● **PD-2.1.B** (fe-chemical:16.B) Judge a mixed exposure against its limits.
  - EK: Σ Cᵢ/TLVᵢ ≤ 1.
  - P2 · drills: pd-tlv-mixture
- ● **PD-2.1.C** (fe-chemical:16.C) State what a HAZOP guide word means.
  - EK: NO, MORE, LESS, REVERSE, AS WELL AS, PART OF, OTHER THAN.
  - P2 · drills: pd-hazop

## Unit 3 · Process dynamics

Big ideas: DYN

### 3.1 First-order systems



- ● **PD-3.1.A** Compute the step response of a first-order process.
  - EK: y = KΔu(1 − e^(−t/τ)).
  - P1 · drills: pd-first-order
