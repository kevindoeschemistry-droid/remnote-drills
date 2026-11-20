# Chemical Reaction Engineering — curriculum framework (draft 1)

Generated from `drills/frameworks/reaction-engineering.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**9 learning objectives** in 4 units (9 core): 9 drilled, 0 partly, 0 with no drills. Core: 9 / 9 drilled.

## Big ideas

- **BALANCE · A reactor is a mole balance with a rate law in it.** In minus out plus generation equals accumulation. Batch, CSTR and PFR differ only in which terms survive and where the rate is evaluated.
- **CONCENTRATION · The rate lives at the local concentration.** A stirred tank reacts at its exit concentration; a tube reacts at every concentration on the way down. That one fact explains reactor size and selectivity.
- **TIME · Compare the reaction time to the residence time.** The Damköhler number, kτ for first order, says how much will react before the fluid leaves.

## Practices

- **P1 · Compute.** Carry a design equation to a number.
- **P2 · Choose.** Pick the reactor or the operating condition from the kinetics.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Rates | core | — | 3 | 3 | 0 | 0 |
| 2 · Ideal reactors | core | — | 3 | 3 | 0 | 0 |
| 3 · Multiple reactions | core | — | 2 | 2 | 0 | 0 |
| 4 · Catalysis | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · Rates

Big ideas: CONCENTRATION

### 1.1 Rate laws and order



- ● **RE-1.1.A** (fe-chemical:12.A) Evaluate a power-law rate, find the order from how the rate responds to concentration, and read the order from the units of k.
  - EK: Doubling C multiplies an nth-order rate by 2ⁿ; k carries (mol/L)^(1−n) per time.
  - P1 · drills: cre-rate-from-law, cre-order-from-doubling, cre-rate-constant-units
- ● **RE-1.1.B** (fe-chemical:12.A) Compute a first-order half-life.
  - EK: t½ = ln 2 / k, independent of the starting concentration.
  - P1 · drills: cre-half-life

### 1.2 Temperature dependence



- ● **RE-1.2.A** (fe-chemical:12.B) Use the Arrhenius equation to find how k changes with temperature, and the activation energy from two rate constants.
  - EK: ln(k₂/k₁) = (Eₐ/R)(1/T₁ − 1/T₂), kelvin and joules.
  - P1 · drills: cre-arrhenius-ratio, cre-activation-energy

## Unit 2 · Ideal reactors

Big ideas: BALANCE, CONCENTRATION, TIME

### 2.1 Batch



- ● **RE-2.1.A** (fe-chemical:12.C, fe-chemical:12.E) Find the batch time for a given conversion, first and second order.
  - EK: First order: t = (1/k) ln[1/(1 − X)]. Second order: t = X / [k C_A0 (1 − X)].
  - P1 · drills: cre-batch-first-order-time, cre-batch-second-order-time

### 2.2 CSTR



- ● **RE-2.2.A** (fe-chemical:12.E) Size a CSTR for a conversion, find the conversion from the space time, and treat tanks in series.
  - EK: V = v₀X / [k(1 − X)]; X = kτ/(1 + kτ); n equal tanks give C/C₀ = 1/(1 + kτ)ⁿ.
  - P1 · drills: cre-cstr-volume, cre-cstr-conversion, cre-cstrs-in-series

### 2.3 PFR



- ● **RE-2.3.A** (fe-chemical:12.E) Size a plug-flow reactor and compare it with a CSTR.
  - EK: V = (v₀/k) ln[1/(1 − X)]; for positive order a PFR is always smaller.
  - P1 · P2 · drills: cre-pfr-volume, cre-reactor-comparison

## Unit 3 · Multiple reactions

Big ideas: CONCENTRATION

### 3.1 Series and parallel



- ● **RE-3.1.A** (fe-chemical:12.D) Find when the intermediate of a series reaction peaks.
  - EK: t_max = ln(k₁/k₂)/(k₁ − k₂).
  - P1 · drills: cre-series-optimum-time
- ● **RE-3.1.B** (fe-chemical:12.C, fe-chemical:12.D) Compute the instantaneous selectivity of parallel reactions and choose the reactor that favours the desired one.
  - EK: S goes as C_A^(a_D − a_U): high concentration if the desired path has the higher order, low if the lower.
  - P1 · P2 · drills: cre-parallel-selectivity, cre-selectivity-strategy

## Unit 4 · Catalysis

Big ideas: CONCENTRATION

### 4.1 Surfaces



- ● **RE-4.1.A** (fe-chemical:12.F) Compute Langmuir coverage and state what a catalyst does and does not change.
  - EK: θ = KP/(1 + KP); a catalyst lowers the activation energy and leaves equilibrium alone.
  - P1 · P2 · drills: cre-langmuir-coverage, cre-catalysis-facts
