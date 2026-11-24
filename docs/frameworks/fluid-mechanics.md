# Fluid Mechanics — curriculum framework (draft 1)

Generated from `drills/frameworks/fluid-mechanics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**30 learning objectives** in 10 units (30 core): 30 drilled, 0 partly, 0 with no drills. Core: 30 / 30 drilled.

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
| 7 · Momentum balances on a control volume | core | — | 2 | 2 | 0 | 0 |
| 8 · Viscous flow and differential analysis | core | — | 5 | 5 | 0 | 0 |
| 9 · Dimensional analysis and drag | core | — | 4 | 4 | 0 | 0 |
| 10 · Piping systems, pumps and submerged surfaces | core | — | 4 | 4 | 0 | 0 |

## Unit 1 · Properties and statics

Big ideas: HEAD

### 1.1 Properties



- ● **FM-1.1.A** (fe-chemical:6.A, webwork-opl:TH1.6, webwork-opl:FM1.2, webwork-opl:FM1.3) Relate dynamic and kinematic viscosity, density and specific gravity.
  - EK: ν = μ/ρ. Water is about 1 mm²/s, air about 15.
  - P1 · drills: fm-kinematic-viscosity

### 1.2 Statics



- ● **FM-1.2.A** (fe-chemical:6.A, webwork-opl:FM2.1, webwork-opl:FM2.2) Compute hydrostatic pressure and read a U-tube manometer.
  - EK: P = ρgh; across a manometer only the density difference counts.
  - P1 · P3 · drills: fm-hydrostatic-pressure, fm-manometer
- ● **FM-1.2.B** (webwork-opl:FM2.6) Apply Archimedes' principle to a floating body.
  - EK: Submerged fraction = body density over fluid density.
  - P1 · drills: fm-floating-fraction

## Unit 2 · Dimensionless numbers and flow regime

Big ideas: REGIME

### 2.1 Reynolds number



- ● **FM-2.1.A** (fe-chemical:6.B, webwork-opl:FM6.9) Compute a Reynolds number and a hydraulic diameter, and say what each common dimensionless group compares.
  - EK: Re = ρvD/μ; D_h = 4A/P; Re, Fr, We, Ma, Eu each compare two forces or speeds.
  - P1 · P2 · drills: fm-reynolds-number, fm-hydraulic-diameter, fm-dimensionless-groups, sc-reynolds-diameter, sc-stokes-settling
- ● **FM-2.1.B** (fe-chemical:6.E, webwork-opl:FM6.3) Classify pipe flow as laminar, transitional or turbulent.
  - EK: Laminar below about 2100, turbulent above about 4000.
  - P2 · drills: fm-flow-regime
- ● **FM-2.1.C** (fe-chemical:6.E, webwork-opl:FM6.2) Find the pressure drop of laminar pipe flow.
  - EK: Hagen–Poiseuille: ΔP = 32μLv/D², the same as f = 64/Re.
  - P1 · drills: fm-laminar-pressure-drop, sc-laminar-pressure-drop-diameter

## Unit 3 · Continuity and Bernoulli

Big ideas: CONSERVE, HEAD

### 3.1 Frictionless flow



- ● **FM-3.1.A** (fe-chemical:6.D, webwork-opl:FM3.2, webwork-opl:FM3.4) Use continuity to find a velocity change and Bernoulli to find the pressure change that goes with it.
  - EK: A1v1 = A2v2; P + ½ρv² + ρgz is constant along a streamline without friction.
  - P1 · P3 · drills: fm-continuity, fm-bernoulli-pressure
- ● **FM-3.1.B** (fe-chemical:6.D, webwork-opl:FM3.4) Find the efflux velocity from a tank.
  - EK: Torricelli: v = √(2gh).
  - P1 · P3 · drills: fm-torricelli, sc-torricelli-head

## Unit 4 · The mechanical energy balance

Big ideas: HEAD

### 4.1 Friction



- ● **FM-4.1.A** (fe-chemical:6.C, webwork-opl:FM6.4, webwork-opl:FM6.5, webwork-opl:FM6.6) Compute friction head loss in a pipe and in a fitting.
  - EK: h_f = f(L/D)v²/2g; h_L = K v²/2g.
  - P1 · drills: fm-friction-head-loss, fm-minor-loss, sc-turbulent-pressure-drop-flow

### 4.2 Pumps



- ● **FM-4.2.A** (fe-chemical:6.C, fe-chemical:6.G, webwork-opl:TH5.6, webwork-opl:FM3.6, webwork-opl:FM6.7, webwork-opl:FM6.8, webwork-opl:FM11.1) Find the head a pump must supply and the power it draws.
  - EK: Pump head = lift + losses (+ pressure and velocity changes); shaft power = ρgQH/η.
  - P1 · P3 · drills: fm-pump-head, fm-pump-power, sc-pump-power-flow
- ● **FM-4.2.B** (fe-chemical:6.G, webwork-opl:FM6.8, webwork-opl:FM11.2) Explain cavitation and NPSH, and what pumps in series and in parallel do.
  - EK: Available NPSH must exceed required; series adds head, parallel adds flow.
  - P2 · drills: fm-pump-concepts

## Unit 5 · Flow measurement

Big ideas: CONSERVE

### 5.1 Meters



- ● **FM-5.1.A** (fe-chemical:6.F, webwork-opl:FM10.6) Compute a velocity from a pitot reading and a flow from a venturi reading.
  - EK: Pitot: ΔP = ½ρv². Venturi: continuity plus Bernoulli, times a discharge coefficient.
  - P1 · drills: fm-pitot, fm-venturi
- ● **FM-5.1.B** (fe-chemical:6.F) Choose between pitot, orifice, venturi and rotameter.
  - EK: Orifice is cheap with high permanent loss; venturi recovers pressure; rotameter is variable-area.
  - P2 · drills: fm-meter-choice

## Unit 6 · Compressible flow and non-Newtonian fluids

Big ideas: REGIME

### 6.1 Compressible flow



- ● **FM-6.1.A** (fe-chemical:6.H, webwork-opl:FM9.1) Compute the speed of sound in an ideal gas and use the Mach number to decide how to treat a flow.
  - EK: a = √(γRT/M); below Ma ≈ 0.3 a gas flow can be treated as incompressible.
  - P1 · P2 · drills: fm-speed-of-sound, fm-mach-regime

### 6.2 Non-Newtonian fluids



- ● **FM-6.2.A** (fe-chemical:6.H, webwork-opl:FM1.3) Classify a fluid as Newtonian, shear-thinning, shear-thickening or Bingham, and compute a power-law apparent viscosity.
  - EK: τ = Kγ̇ⁿ; apparent viscosity Kγ̇ⁿ⁻¹; a Bingham plastic has a yield stress.
  - P1 · P2 · drills: fm-non-newtonian-type, fm-apparent-viscosity

## Unit 7 · Momentum balances on a control volume

Big ideas: CONSERVE

### 7.1 Jets, vanes and bends



- ● **FM-7.1.A** (webwork-opl:FM3.3) Find the force a jet exerts on a flat plate.
  - EK: F = ṁv = ρAv² for a jet stopped in its own direction.
  - P1 · drills: fm-jet-plate
- ● **FM-7.1.B** (webwork-opl:FM3.3) Find the force on a vane that turns a jet through an angle.
  - EK: F_x = ṁv(1 − cos θ); a 180° turn doubles the flat-plate force.
  - P1 · drills: fm-vane-force

## Unit 8 · Viscous flow and differential analysis

Big ideas: REGIME

### 8.1 Exact solutions of the Navier–Stokes equations



- ● **FM-8.1.A** (webwork-opl:FM4.3) Find the shear force in Couette flow.
  - EK: Linear profile: τ = μU/h everywhere in the gap.
  - P1 · drills: fm-couette-force
- ● **FM-8.1.B** (webwork-opl:FM6.2) Find the flow rate of laminar pipe flow from the pressure drop.
  - EK: Q = πR⁴ΔP/8μL; the profile is a parabola.
  - P1 · drills: fm-poiseuille-flow, fm-poiseuille-max-velocity
- ● **FM-8.1.C** (webwork-opl:FM4.3) Find the mean velocity of a falling film.
  - EK: ū = ρgδ²/3μ; zero shear at the free surface.
  - P1 · drills: fm-falling-film
- ● **FM-8.1.D** (webwork-opl:FM4.2) Use continuity to find a missing velocity component.
  - EK: ∂u/∂x + ∂v/∂y = 0 for incompressible flow.
  - P1 · drills: fm-continuity-2d
- ● **FM-8.1.E** (webwork-opl:FM6.1) Estimate the laminar entry length.
  - EK: L_e ≈ 0.05 Re D.
  - P1 · drills: fm-entry-length

## Unit 9 · Dimensional analysis and drag

Big ideas: REGIME

### 9.1 Dimensional analysis



- ● **FM-9.1.A** (webwork-opl:FM5.1) Count the dimensionless groups with the Buckingham pi theorem.
  - EK: Groups = variables − independent dimensions.
  - P1 · drills: fm-pi-count
- ● **FM-9.1.B** (webwork-opl:FM5.3) Find the model speed that matches the Reynolds number.
  - EK: V_m = V_p (L_p/L_m)(ν_m/ν_p).
  - P1 · drills: fm-model-similarity

### 9.2 Drag



- ● **FM-9.2.A** (webwork-opl:FM7.5) Compute a drag force from a drag coefficient.
  - EK: F_D = C_D · ½ρV² · A.
  - P1 · drills: fm-drag-force
- ● **FM-9.2.B** (webwork-opl:FM7.5) Find a Stokes terminal velocity.
  - EK: v_t = (ρ_p − ρ)gd²/18μ, valid for Re < 1.
  - P1 · drills: fm-stokes-terminal

## Unit 10 · Piping systems, pumps and submerged surfaces

Big ideas: HEAD

### 10.1 Networks and pumps



- ● **FM-10.1.A** (webwork-opl:FM6.10) Split flow between parallel pipes.
  - EK: Parallel pipes share the head loss; Q ∝ D^(5/2)/√L at equal f.
  - P1 · drills: fm-parallel-pipes
- ● **FM-10.1.B** (webwork-opl:FM11.3) Scale a pump with the affinity laws.
  - EK: Q ∝ N, H ∝ N², P ∝ N³.
  - P1 · drills: fm-pump-affinity
- ● **FM-10.1.C** (webwork-opl:FM6.8) Find the operating point of a pump and a system.
  - EK: Pump head = system head.
  - P1 · drills: fm-operating-point

### 10.2 Submerged surfaces



- ● **FM-10.2.A** (webwork-opl:FM2.3) Find the hydrostatic force on a vertical plane gate.
  - EK: F = ρg h_c A, acting below the centroid.
  - P1 · drills: fm-gate-force
