# Fluid Mechanics — curriculum framework (draft 1)

Generated from `drills/frameworks/fluid-mechanics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**15 learning objectives** in 6 units (15 core): 15 drilled, 0 partly, 0 with no drills. Core: 15 / 15 drilled.

## Big ideas

- **HEAD · Everything is a head.** Pressure, velocity, elevation, friction and pump work can all be written as metres of fluid. The mechanical energy balance is bookkeeping in that one currency.
- **REGIME · Find the regime first.** A Reynolds number, or a Mach number, decides which equations apply. Compute it before anything else.
- **CONSERVE · Mass in equals mass out.** Continuity fixes how velocity changes with area; Bernoulli then fixes how pressure changes with velocity.

## Practices

- **P1 · Compute.** Carry a calculation through in SI units to a number with the right order of magnitude.
- **P2 · Classify.** Decide the regime, the kind of fluid or the right instrument from what is given.
- **P3 · Set up.** Choose the two points and the terms that survive in an energy balance.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Properties and statics | core | — | 3 | 3 | 0 | 0 |
| 2 · Dimensionless numbers and flow regime | core | — | 3 | 3 | 0 | 0 |
| 3 · Continuity and Bernoulli | core | — | 2 | 2 | 0 | 0 |
| 4 · The mechanical energy balance | core | — | 3 | 3 | 0 | 0 |
| 5 · Flow measurement | core | — | 2 | 2 | 0 | 0 |
| 6 · Compressible flow and non-Newtonian fluids | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Properties and statics

Big ideas: HEAD

### 1.1 Properties



- ● **FM-1.1.A** (fe-chemical:6.A) Relate dynamic and kinematic viscosity, density and specific gravity.
  - EK: ν = μ/ρ. Water is about 1 mm²/s, air about 15.
  - P1 · drills: fm-kinematic-viscosity

### 1.2 Statics



- ● **FM-1.2.A** (fe-chemical:6.A) Compute hydrostatic pressure and read a U-tube manometer.
  - EK: P = ρgh; across a manometer only the density difference counts.
  - P1 · P3 · drills: fm-hydrostatic-pressure, fm-manometer
- ● **FM-1.2.B** Apply Archimedes' principle to a floating body.
  - EK: Submerged fraction = body density over fluid density.
  - P1 · drills: fm-floating-fraction

## Unit 2 · Dimensionless numbers and flow regime

Big ideas: REGIME

### 2.1 Reynolds number



- ● **FM-2.1.A** (fe-chemical:6.B) Compute a Reynolds number and a hydraulic diameter, and say what each common dimensionless group compares.
  - EK: Re = ρvD/μ; D_h = 4A/P; Re, Fr, We, Ma, Eu each compare two forces or speeds.
  - P1 · P2 · drills: fm-reynolds-number, fm-hydraulic-diameter, fm-dimensionless-groups
- ● **FM-2.1.B** (fe-chemical:6.E) Classify pipe flow as laminar, transitional or turbulent.
  - EK: Laminar below about 2100, turbulent above about 4000.
  - P2 · drills: fm-flow-regime
- ● **FM-2.1.C** (fe-chemical:6.E) Find the pressure drop of laminar pipe flow.
  - EK: Hagen–Poiseuille: ΔP = 32μLv/D², the same as f = 64/Re.
  - P1 · drills: fm-laminar-pressure-drop

## Unit 3 · Continuity and Bernoulli

Big ideas: CONSERVE, HEAD

### 3.1 Frictionless flow



- ● **FM-3.1.A** (fe-chemical:6.D) Use continuity to find a velocity change and Bernoulli to find the pressure change that goes with it.
  - EK: A1v1 = A2v2; P + ½ρv² + ρgz is constant along a streamline without friction.
  - P1 · P3 · drills: fm-continuity, fm-bernoulli-pressure
- ● **FM-3.1.B** (fe-chemical:6.D) Find the efflux velocity from a tank.
  - EK: Torricelli: v = √(2gh).
  - P1 · P3 · drills: fm-torricelli

## Unit 4 · The mechanical energy balance

Big ideas: HEAD

### 4.1 Friction



- ● **FM-4.1.A** (fe-chemical:6.C) Compute friction head loss in a pipe and in a fitting.
  - EK: h_f = f(L/D)v²/2g; h_L = K v²/2g.
  - P1 · drills: fm-friction-head-loss, fm-minor-loss

### 4.2 Pumps



- ● **FM-4.2.A** (fe-chemical:6.C, fe-chemical:6.G) Find the head a pump must supply and the power it draws.
  - EK: Pump head = lift + losses (+ pressure and velocity changes); shaft power = ρgQH/η.
  - P1 · P3 · drills: fm-pump-head, fm-pump-power
- ● **FM-4.2.B** (fe-chemical:6.G) Explain cavitation and NPSH, and what pumps in series and in parallel do.
  - EK: Available NPSH must exceed required; series adds head, parallel adds flow.
  - P2 · drills: fm-pump-concepts

## Unit 5 · Flow measurement

Big ideas: CONSERVE

### 5.1 Meters



- ● **FM-5.1.A** (fe-chemical:6.F) Compute a velocity from a pitot reading and a flow from a venturi reading.
  - EK: Pitot: ΔP = ½ρv². Venturi: continuity plus Bernoulli, times a discharge coefficient.
  - P1 · drills: fm-pitot, fm-venturi
- ● **FM-5.1.B** (fe-chemical:6.F) Choose between pitot, orifice, venturi and rotameter.
  - EK: Orifice is cheap with high permanent loss; venturi recovers pressure; rotameter is variable-area.
  - P2 · drills: fm-meter-choice

## Unit 6 · Compressible flow and non-Newtonian fluids

Big ideas: REGIME

### 6.1 Compressible flow



- ● **FM-6.1.A** (fe-chemical:6.H) Compute the speed of sound in an ideal gas and use the Mach number to decide how to treat a flow.
  - EK: a = √(γRT/M); below Ma ≈ 0.3 a gas flow can be treated as incompressible.
  - P1 · P2 · drills: fm-speed-of-sound, fm-mach-regime

### 6.2 Non-Newtonian fluids



- ● **FM-6.2.A** (fe-chemical:6.H) Classify a fluid as Newtonian, shear-thinning, shear-thickening or Bingham, and compute a power-law apparent viscosity.
  - EK: τ = Kγ̇ⁿ; apparent viscosity Kγ̇ⁿ⁻¹; a Bingham plastic has a yield stress.
  - P1 · P2 · drills: fm-non-newtonian-type, fm-apparent-viscosity
