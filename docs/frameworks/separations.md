# Separations — curriculum framework (draft 1)

Generated from `drills/frameworks/separations.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**6 learning objectives** in 2 units (6 core): 6 drilled, 0 partly, 0 with no drills. Core: 6 / 6 drilled.

## Big ideas

- **STAGE · A stage is an equilibrium plus a balance.** Every separation is equilibrium relations (α, m, solubility) chained by mass balances; the number of stages measures how hard the split is.
- **DRIVE · Separation needs a driving difference.** Volatility, solubility or vapour pressure must differ, and the closer to 1 the ratio, the more stages or reflux it costs.

## Practices

- **P1 · Compute.** Carry the stage or balance calculation to a number.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Equilibrium-stage separations | core | — | 4 | 4 | 0 | 0 |
| 2 · Humidification and evaporation | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Equilibrium-stage separations

Big ideas: STAGE, DRIVE

### 1.1 Distillation



- ● **SP-1.1.A** (webwork-opl:TH16.4) Compute a vapour composition from relative volatility.
  - EK: y = αx/(1 + (α − 1)x).
  - P1 · drills: sp-vle-alpha
- ● **SP-1.1.B** Compute the minimum number of stages with Fenske.
  - EK: N_min = ln[(x_D/(1−x_D))((1−x_B)/x_B)]/ln α.
  - Needs: SP-1.1.A
  - P1 · drills: sp-fenske
- ● **SP-1.1.C** Compute the minimum reflux ratio for a saturated-liquid feed.
  - EK: Pinch on the q-line; Underwood for a binary.
  - Needs: SP-1.1.A
  - P1 · drills: sp-rmin

### 1.2 Absorption



- ● **SP-1.2.A** Compute the stages for an absorber with the Kremser equation.
  - EK: N = ln[(A − f)/(1 − f)]/ln A − 1.
  - P1 · drills: sp-kremser

## Unit 2 · Humidification and evaporation

Big ideas: STAGE

### 2.1 Humid air and evaporators



- ● **SP-2.1.A** (webwork-opl:TH12.5) Compute absolute humidity from relative humidity.
  - EK: H = 0.622 p_w/(P − p_w).
  - P1 · drills: sp-humidity
- ● **SP-2.1.B** Compute the water removed by an evaporator.
  - EK: Solids balance first.
  - P1 · drills: sp-evaporator
