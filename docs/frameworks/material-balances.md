# Material and Energy Balances — curriculum framework (draft 1)

Generated from `drills/frameworks/material-balances.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**18 learning objectives** in 6 units (18 core): 18 drilled, 0 partly, 0 with no drills. Core: 18 / 18 drilled.

## Big ideas

- **CONSERVE · In minus out plus generation equals accumulation.** Every problem is this one sentence applied to a chosen boundary and a chosen quantity. Mass and energy are conserved; moles of a species are not when it reacts.
- **BOUNDARY · The boundary is a choice.** A box around the whole process hides the recycle; a box around the mixing point exposes it. Picking the boundary that cuts the fewest unknowns is most of the work.
- **BASIS · Pick a basis and count unknowns before solving.** Flows scale freely until one is fixed. Degrees of freedom say whether the problem can be solved before any algebra is done.

## Practices

- **P1 · Set up.** Draw the boundary, choose a basis, name the unknowns and count the independent equations.
- **P2 · Solve.** Write the balances and solve for the unknown, carrying units.
- **P3 · Judge.** Say which balance or boundary to use and whether an answer is physically sensible.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Process variables | core | — | 2 | 2 | 0 | 0 |
| 2 · Steady-state balances without reaction | core | — | 3 | 3 | 0 | 0 |
| 3 · Balances with reaction | core | — | 5 | 5 | 0 | 0 |
| 4 · Energy balances | core | — | 3 | 3 | 0 | 0 |
| 5 · Unsteady balances | core | — | 3 | 3 | 0 | 0 |
| 6 · Multiunit balances and degrees of freedom | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Process variables

Big ideas: BASIS

### 1.1 Composition and flow



- ● **MB-1.1.A** (webwork-opl:TH1.5, webwork-opl:TH12.1) Convert between mass fractions and mole fractions, and find the average molar mass of a mixture.
  - EK: Take 100 g or 1 mol as a basis; the average molar mass is the mole-fraction-weighted mean.
  - P2 · drills: mb-mass-to-mole-fraction, mb-average-molar-mass
- ● **MB-1.1.B** (webwork-opl:TH4.1) Convert a volumetric flow of a liquid or an ideal gas to a molar flow.
  - EK: Liquid: density then molar mass. Gas: n = PV/RT, with T in kelvin.
  - P2 · drills: mb-liquid-molar-flow, mb-ideal-gas-molar-flow

## Unit 2 · Steady-state balances without reaction

Big ideas: CONSERVE, BOUNDARY, BASIS

### 2.1 Single units



- ● **MB-2.1.A** (fe-chemical:8.A, webwork-opl:TH4.2, webwork-opl:MB2.2) Solve a mixer, a separator and an evaporator with a total balance and one component balance.
  - EK: Two independent balances for two components; a component that passes through unchanged is a tie.
  - P1 · P2 · drills: mb-mixer, mb-distillation-split, mb-evaporator, mb-dilution
- ● **MB-2.1.B** (fe-chemical:8.A, webwork-opl:MB2.1, webwork-opl:MB3.2) Count degrees of freedom and say whether a balance problem is specified.
  - EK: Unknowns minus independent equations: zero is solvable, positive is underspecified, negative overspecified.
  - P1 · P3 · drills: mb-degrees-of-freedom, mb-dof-mixer

### 2.2 Recycle, bypass and purge



- ● **MB-2.2.A** (fe-chemical:8.E, webwork-opl:MB2.4) Balance a mixing point to find a recycle flow, and explain what recycle, bypass and purge are for.
  - EK: The overall balance never contains the recycle stream; a purge stops an inert accumulating.
  - P1 · P2 · P3 · drills: mb-recycle-mixing-point, mb-recycle-concepts

## Unit 3 · Balances with reaction

Big ideas: CONSERVE

### 3.1 Stoichiometry in a flowing system



- ● **MB-3.1.A** (fe-chemical:8.F, webwork-opl:TH13.1, webwork-opl:MB3.1) Identify the limiting reactant and compute percent excess.
  - EK: Divide each feed by its coefficient; excess is measured against the stoichiometric requirement.
  - P2 · drills: mb-limiting-reactant, mb-percent-excess
- ● **MB-3.1.B** (fe-chemical:8.F, webwork-opl:TH13.1, webwork-opl:MB3.1, webwork-opl:MB3.3) Use conversion or the extent of reaction to find every outlet flow.
  - EK: n_i = n_i0 + ν_i ξ; one measured species fixes ξ.
  - P2 · drills: mb-conversion-outlet, mb-extent-of-reaction
- ● **MB-3.1.C** (fe-chemical:8.F, webwork-opl:MB3.3) Apply selectivity and yield to parallel reactions.
  - EK: Conversion says how much reacted; selectivity says where it went.
  - P2 · drills: mb-yield-with-side-reaction, mb-selectivity-from-yield
- ● **MB-3.1.D** (fe-chemical:8.E, fe-chemical:8.F, webwork-opl:MB3.4) Relate single-pass conversion, overall conversion and recycle flow for a reactor with recycle.
  - EK: With complete recycle of unreacted feed the reactor feed is the fresh feed divided by the single-pass conversion.
  - P1 · P2 · drills: mb-recycle-reactor, mb-recycle-flow

### 3.2 Combustion



- ● **MB-3.2.A** (fe-chemical:8.F, webwork-opl:TH13.6, webwork-opl:MB3.3) Find the theoretical air for a fuel and the dry flue-gas composition at a given excess air.
  - EK: O2 needed per mole CxHyOz: x + y/4 − z/2. Dry basis leaves the water out; excess O2 and all the N2 pass through.
  - P2 · drills: mb-theoretical-air, mb-flue-gas-oxygen

## Unit 4 · Energy balances

Big ideas: CONSERVE

### 4.1 Without reaction



- ● **MB-4.1.A** (fe-chemical:8.C, webwork-opl:TH2.9, webwork-opl:MB4.5) Compute a heat duty from sensible and latent heat, and the steam needed to supply it.
  - EK: Q = m cp ΔT for a temperature change, m ΔHvap for a phase change; add the steps along the path.
  - P2 · drills: mb-sensible-heat, mb-heat-and-vaporize, mb-steam-requirement
- ● **MB-4.1.B** (fe-chemical:8.C, webwork-opl:TH5.9, webwork-opl:MB4.5) Find the outlet temperature of an adiabatic mixer.
  - EK: Enthalpy in equals enthalpy out; with one cp the outlet is the mass-weighted mean temperature.
  - P2 · drills: mb-adiabatic-mixing, mb-mixer-flow-needed

### 4.2 With reaction



- ● **MB-4.2.A** (fe-chemical:8.C, fe-chemical:7.H, webwork-opl:TH13.3, webwork-opl:TH13.4) Compute a standard heat of reaction from heats of formation.
  - EK: Σ ν ΔHf, products positive and reactants negative; elements are zero; the phase of water matters.
  - P2 · drills: mb-heat-of-reaction, mb-heat-of-reaction-T

## Unit 5 · Unsteady balances

Big ideas: CONSERVE

### 5.1 Mass



- ● **MB-5.1.A** (fe-chemical:8.B, webwork-opl:TH4.3, webwork-opl:MB5.1) Find the time to fill or drain a tank at constant flows.
  - EK: dV/dt = in − out; with constant flows the level changes linearly.
  - P2 · drills: mb-tank-fill-time, mb-drain-time
- ● **MB-5.1.B** (fe-chemical:8.B, webwork-opl:MB5.1) Model the washout of a stirred tank and use its time constant.
  - EK: V dC/dt = −qC gives C = C0 e^(−t/τ), τ = V/q: 37% after one τ, 5% after three.
  - P2 · P3 · drills: mb-washout-time, mb-residence-time-decay

### 5.2 Energy



- ● **MB-5.2.A** (fe-chemical:8.D, webwork-opl:TH5.3, webwork-opl:MB5.5) Find the time to heat a batch at a constant heating rate.
  - EK: m cp dT/dt = Q; with no losses the temperature rises linearly.
  - P2 · drills: mb-tank-heating-time, mb-heating-coil-time

## Unit 6 · Multiunit balances and degrees of freedom

Big ideas: CONSERVE

### 6.1 Flowsheets



- ● **MB-6.1.A** (webwork-opl:MB2.3) Solve a two-unit separation train.
  - EK: Balance each unit in turn; a component's recovery multiplies through units in series.
  - P1 · drills: mb-two-column, mb-single-column-split
- ● **MB-6.1.B** (webwork-opl:MB4.1) Count degrees of freedom for an energy balance.
  - EK: DOF = unknowns − independent equations; the energy balance adds one equation and usually one unknown (Q or a temperature).
  - P1 · drills: mb-energy-dof, mb-energy-dof-heater

## Drills not yet placed on the map

- sc-dilution (meb.nonreactive)
