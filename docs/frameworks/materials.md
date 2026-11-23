# Polymers and Materials — curriculum framework (draft 1)

Generated from `drills/frameworks/materials.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**6 learning objectives** in 2 units (6 core): 6 drilled, 0 partly, 0 with no drills. Core: 6 / 6 drilled.

## Big ideas

- **CHAINS · Polymers are distributions, not molecules.** A sample holds many chain lengths; averages and dispersity, not one molar mass, describe it.
- **PROPS · Structure sets properties.** Cross-links, band gaps and bond stiffness decide whether a material flows, conducts or stretches.

## Practices

- **P1 · Compute.** Carry the calculation to a number with units.
- **P2 · Classify.** Place a material in its family from its chemistry.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Polymers | core | — | 4 | 4 | 0 | 0 |
| 2 · Properties of solids | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Polymers

Big ideas: CHAINS

### 1.1 Molar mass and growth



- ● **MT-1.1.A** Compute M_n, M_w and dispersity from a chain distribution.
  - EK: M_n = ΣnM/Σn; M_w = ΣnM²/ΣnM.
  - P1 · drills: mt-molar-mass-averages
- ● **MT-1.1.B** Compute the degree of polymerisation of a step-growth polymer.
  - EK: X_n = (1 + r)/(1 + r − 2rp).
  - Needs: MT-1.1.A
  - P1 · drills: mt-carothers
- ● **MT-1.1.C** Classify a polymer as chain-growth or step-growth.
  - EK: Vinyl polymers chain; polyesters, polyamides step.
  - P2 · drills: mt-growth-type
- ● **MT-1.1.D** Classify a polymer as thermoplastic or thermoset.
  - EK: Cross-linked networks do not melt.
  - P2 · drills: mt-thermoset

## Unit 2 · Properties of solids

Big ideas: PROPS

### 2.1 Mechanical and electronic



- ● **MT-2.1.A** Compute Young's modulus from a tensile test.
  - EK: E = (F/A)/(ΔL/L₀).
  - P1 · drills: mt-youngs-modulus
- ● **MT-2.1.B** Relate a semiconductor's band gap to the wavelength it absorbs or emits.
  - EK: λ = hc/E_g.
  - P1 · drills: mt-band-gap
