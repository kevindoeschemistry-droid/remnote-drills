# Fluid Mechanics — curriculum framework (draft 1)

Generated from `drills/frameworks/fluid-mechanics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**64 learning objectives** in 13 units (64 core): 64 drilled, 0 partly, 0 with no drills. Core: 64 / 64 drilled.

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
| 11 · Kinematics, statics extras and differential analysis | core | — | 9 | 9 | 0 | 0 |
| 12 · Boundary layers, potential flow and compressible flow | core | — | 19 | 19 | 0 | 0 |
| 13 · Open-channel flow and turbines | core | — | 6 | 6 | 0 | 0 |

## Unit 1 · Properties and statics

Big ideas: HEAD

### 1.1 Properties



- ● **FM-1.1.A** (fe-chemical:6.A, webwork-opl:TH1.6, webwork-opl:FM1.2, webwork-opl:FM1.3) Relate dynamic and kinematic viscosity, density and specific gravity.
  - EK: ν = μ/ρ. Water is about 1 mm²/s, air about 15.
  - P1 · drills: fm-kinematic-viscosity, fm-dynamic-from-kinematic

### 1.2 Statics



- ● **FM-1.2.A** (fe-chemical:6.A, webwork-opl:FM2.1, webwork-opl:FM2.2) Compute hydrostatic pressure and read a U-tube manometer.
  - EK: P = ρgh; across a manometer only the density difference counts.
  - P1 · P3 · drills: fm-hydrostatic-pressure, fm-manometer
- ● **FM-1.2.B** (webwork-opl:FM2.6) Apply Archimedes' principle to a floating body.
  - EK: Submerged fraction = body density over fluid density.
  - P1 · drills: fm-floating-fraction, fm-push-under-force

## Unit 2 · Dimensionless numbers and flow regime

Big ideas: REGIME

### 2.1 Reynolds number



- ● **FM-2.1.A** (fe-chemical:6.B, webwork-opl:FM6.9) Compute a Reynolds number and a hydraulic diameter, and say what each common dimensionless group compares.
  - EK: Re = ρvD/μ; D_h = 4A/P; Re, Fr, We, Ma, Eu each compare two forces or speeds.
  - P1 · P2 · drills: fm-reynolds-number, fm-hydraulic-diameter, fm-dimensionless-groups, sc-reynolds-diameter, sc-stokes-settling
- ● **FM-2.1.B** (fe-chemical:6.E, webwork-opl:FM6.3) Classify pipe flow as laminar, transitional or turbulent.
  - EK: Laminar below about 2100, turbulent above about 4000.
  - P2 · drills: fm-flow-regime, fm-max-laminar-speed
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



- ● **FM-4.2.A** (fe-chemical:6.C, fe-chemical:6.G, webwork-opl:TH5.6, webwork-opl:FM3.6, webwork-opl:FM6.7, webwork-opl:FM6.8, webwork-opl:FM11.1, aiche-bok:T.FLOW) Find the head a pump must supply and the power it draws.
  - EK: Pump head = lift + losses (+ pressure and velocity changes); shaft power = ρgQH/η.
  - P1 · P3 · drills: fm-pump-head, fm-pump-power, sc-pump-power-flow
- ● **FM-4.2.B** (fe-chemical:6.G, webwork-opl:FM6.8, webwork-opl:FM11.2, aiche-bok:T.FLOW) Explain cavitation and NPSH, and what pumps in series and in parallel do.
  - EK: Available NPSH must exceed required; series adds head, parallel adds flow.
  - P2 · drills: fm-pump-concepts, fm-npsh-available

## Unit 5 · Flow measurement

Big ideas: CONSERVE

### 5.1 Meters



- ● **FM-5.1.A** (fe-chemical:6.F, webwork-opl:FM10.6) Compute a velocity from a pitot reading and a flow from a venturi reading.
  - EK: Pitot: ΔP = ½ρv². Venturi: continuity plus Bernoulli, times a discharge coefficient.
  - P1 · drills: fm-pitot, fm-venturi
- ● **FM-5.1.B** (fe-chemical:6.F) Choose between pitot, orifice, venturi and rotameter.
  - EK: Orifice is cheap with high permanent loss; venturi recovers pressure; rotameter is variable-area.
  - P2 · drills: fm-meter-choice, fm-orifice-flow

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
  - P1 · drills: fm-jet-plate, fm-moving-plate-jet
- ● **FM-7.1.B** (webwork-opl:FM3.3) Find the force on a vane that turns a jet through an angle.
  - EK: F_x = ṁv(1 − cos θ); a 180° turn doubles the flat-plate force.
  - P1 · drills: fm-vane-force, fm-vane-resultant

## Unit 8 · Viscous flow and differential analysis

Big ideas: REGIME

### 8.1 Exact solutions of the Navier–Stokes equations



- ● **FM-8.1.A** (webwork-opl:FM4.3) Find the shear force in Couette flow.
  - EK: Linear profile: τ = μU/h everywhere in the gap.
  - P1 · drills: fm-couette-force, fm-couette-dissipation
- ● **FM-8.1.B** (webwork-opl:FM6.2) Find the flow rate of laminar pipe flow from the pressure drop.
  - EK: Q = πR⁴ΔP/8μL; the profile is a parabola.
  - P1 · drills: fm-poiseuille-flow, fm-poiseuille-max-velocity
- ● **FM-8.1.C** (webwork-opl:FM4.3) Find the mean velocity of a falling film.
  - EK: ū = ρgδ²/3μ; zero shear at the free surface.
  - P1 · drills: fm-falling-film, fm-film-thickness
- ● **FM-8.1.D** (webwork-opl:FM4.2) Use continuity to find a missing velocity component.
  - EK: ∂u/∂x + ∂v/∂y = 0 for incompressible flow.
  - P1 · drills: fm-continuity-2d, fm-incompressible-check
- ● **FM-8.1.E** (webwork-opl:FM6.1) Estimate the laminar entry length.
  - EK: L_e ≈ 0.05 Re D.
  - P1 · drills: fm-entry-length, fm-turbulent-entry

## Unit 9 · Dimensional analysis and drag

Big ideas: REGIME

### 9.1 Dimensional analysis



- ● **FM-9.1.A** (webwork-opl:FM5.1) Count the dimensionless groups with the Buckingham pi theorem.
  - EK: Groups = variables − independent dimensions.
  - P1 · drills: fm-pi-count, fm-group-exponent
- ● **FM-9.1.B** (webwork-opl:FM5.3) Find the model speed that matches the Reynolds number.
  - EK: V_m = V_p (L_p/L_m)(ν_m/ν_p).
  - P1 · drills: fm-model-similarity, fm-froude-model

### 9.2 Drag



- ● **FM-9.2.A** (webwork-opl:FM7.5) Compute a drag force from a drag coefficient.
  - EK: F_D = C_D · ½ρV² · A.
  - P1 · drills: fm-drag-force, fm-cd-from-force
- ● **FM-9.2.B** (webwork-opl:FM7.5) Find a Stokes terminal velocity.
  - EK: v_t = (ρ_p − ρ)gd²/18μ, valid for Re < 1.
  - P1 · drills: fm-stokes-terminal, fm-stokes-max-diameter

## Unit 10 · Piping systems, pumps and submerged surfaces

Big ideas: HEAD

### 10.1 Networks and pumps



- ● **FM-10.1.A** (webwork-opl:FM6.10) Split flow between parallel pipes.
  - EK: Parallel pipes share the head loss; Q ∝ D^(5/2)/√L at equal f.
  - P1 · drills: fm-parallel-pipes, fm-laminar-split
- ● **FM-10.1.B** (webwork-opl:FM11.3, aiche-bok:T.SU) Scale a pump with the affinity laws.
  - EK: Q ∝ N, H ∝ N², P ∝ N³.
  - P1 · drills: fm-pump-affinity, fm-affinity-speed
- ● **FM-10.1.C** (webwork-opl:FM6.8, aiche-bok:T.FLOW) Find the operating point of a pump and a system.
  - EK: Pump head = system head.
  - P1 · drills: fm-operating-point, fm-operating-power

### 10.2 Submerged surfaces



- ● **FM-10.2.A** (webwork-opl:FM2.3) Find the hydrostatic force on a vertical plane gate.
  - EK: F = ρg h_c A, acting below the centroid.
  - P1 · drills: fm-gate-force, fm-center-of-pressure

## Unit 11 · Kinematics, statics extras and differential analysis

Big ideas: HEAD

### 11.1 Statics extras



- ● **FM-11.1.A** (webwork-opl:FM2.4) Find the vertical force on a curved surface.
  - EK: The vertical component equals the weight of fluid above the surface.
  - P1 · drills: fm-curved-surface, fm-curved-horizontal
- ● **FM-11.1.B** (webwork-opl:FM2.5) Find pressure through layered fluids.
  - EK: Add ρgh layer by layer.
  - P1 · drills: fm-layered-pressure, fm-manometer-reading
- ● **FM-11.1.C** (webwork-opl:FM2.7) Find the free surface of a liquid in rigid-body rotation.
  - EK: The surface is a paraboloid; the rim stands ω²R²/2g above the centre.
  - P1 · drills: fm-rotating-tank, fm-rotating-touch-bottom

### 11.2 Kinematics



- ● **FM-11.2.A** (webwork-opl:FM1.4) Find a streamline of a steady flow.
  - EK: Along a streamline dy/dx = v/u; in steady flow streamlines, pathlines and streaklines coincide.
  - P1 · drills: fm-streamline, fm-travel-time
- ● **FM-11.2.B** (webwork-opl:FM4.1) Find the convective acceleration of a steady flow.
  - EK: a = (V·∇)V; steady flow can still accelerate.
  - P1 · drills: fm-convective-acceleration, fm-acceleration-magnitude
- ● **FM-11.2.C** (webwork-opl:FM4.5) Use a stream function.
  - EK: u = ∂ψ/∂y, v = −∂ψ/∂x; ψ is constant along streamlines.
  - P1 · drills: fm-stream-function, fm-flow-between-streamlines
- ● **FM-11.2.D** (webwork-opl:FM4.6) Compute vorticity.
  - EK: ω_z = ∂v/∂x − ∂u/∂y; irrotational flow has ω = 0.
  - P1 · drills: fm-vorticity, fm-circulation-rotation
- ● **FM-11.2.E** (webwork-opl:FM4.7) Get velocities from a velocity potential.
  - EK: V = ∇φ in irrotational flow.
  - P1 · drills: fm-velocity-potential, fm-potential-pressure
- ● **FM-11.2.F** (webwork-opl:FM4.4) Find viscous dissipation.
  - EK: In Couette flow, Φ = μ(du/dy)² per unit volume.
  - P1 · drills: fm-viscous-dissipation, fm-poiseuille-dissipation

## Unit 12 · Boundary layers, potential flow and compressible flow

Big ideas: HEAD

### 12.1 Similarity, angular momentum and diffusers



- ● **FM-12.1.A** (webwork-opl:FM5.2) Compute a Froude number.
  - EK: Fr = V/√(gL): inertia over gravity, the group for free-surface flows.
  - P1 · drills: fm-froude, fm-critical-froude-depth
- ● **FM-12.1.B** (webwork-opl:FM3.5) Find a torque from an angular-momentum balance.
  - EK: T = ṁ r V_t for a jet leaving at radius r.
  - P1 · drills: fm-sprinkler-torque, fm-sprinkler-free-spin
- ● **FM-12.1.C** (webwork-opl:FM6.11) Find the ideal pressure recovery of a diffuser.
  - EK: C_p = 1 − (A₁/A₂)² for frictionless incompressible flow.
  - P1 · drills: fm-diffuser, fm-diffuser-pressure-rise

### 12.2 Boundary layers



- ● **FM-12.2.A** (webwork-opl:FM7.1) Estimate a laminar boundary-layer thickness.
  - EK: δ ≈ 5x/√Re_x (Blasius); the momentum-integral method gives 5.48.
  - P1 · drills: fm-boundary-thickness, fm-turbulent-bl-thickness
- ● **FM-12.2.B** (webwork-opl:FM7.4) Predict the effect of a pressure gradient on a boundary layer.
  - EK: Adverse (rising) pressure slows the near-wall fluid and can separate it.
  - P1 · drills: fm-pressure-gradient, fm-gradient-sign

### 12.3 Potential flow



- ● **FM-12.3.A** (webwork-opl:FM8.1) Find the velocity induced by a source.
  - EK: A 2-D source of strength m gives v_r = m/(2πr).
  - P1 · drills: fm-source-velocity, fm-source-strength
- ● **FM-12.3.B** (webwork-opl:FM8.2) Superpose a uniform stream and a source.
  - EK: The stagnation point sits where the source's outflow cancels the stream: x = −m/(2πU).
  - P1 · drills: fm-rankine-stagnation, fm-half-body-width
- ● **FM-12.3.C** (webwork-opl:FM8.3) Use the potential flow past a cylinder.
  - EK: Surface speed 2U sin θ; C_p = 1 − 4 sin²θ.
  - P1 · drills: fm-cylinder-cp, fm-kutta-lift
- ● **FM-12.3.D** (webwork-opl:FM8.4) Use the Joukowski map.
  - EK: z = ζ + a²/ζ maps the circle |ζ| = a onto a flat plate from −2a to 2a.
  - P1 · drills: fm-joukowski, fm-joukowski-plate
- ● **FM-12.3.E** (webwork-opl:FM8.5) Use thin-airfoil theory.
  - EK: c_l = 2πα (α in radians) for a thin symmetric airfoil.
  - P1 · drills: fm-thin-airfoil, fm-thin-airfoil-alpha
- ● **FM-12.3.F** (webwork-opl:FM8.6) Use the potential flow past a sphere.
  - EK: The surface speed peaks at 1.5U at the equator.
  - P1 · drills: fm-sphere-speed, fm-sphere-cp

### 12.4 Compressible flow



- ● **FM-12.4.A** (webwork-opl:FM9.2) Find a stagnation temperature.
  - EK: T₀ = T(1 + (k − 1)M²/2).
  - P1 · drills: fm-stagnation-temperature, fm-mach-from-stagnation
- ● **FM-12.4.B** (webwork-opl:FM9.3) Use the area–Mach relation.
  - EK: A/A* = (1/M)[(2/(k+1))(1 + (k−1)M²/2)]^((k+1)/(2(k−1))).
  - P1 · drills: fm-area-mach, fm-throat-area
- ● **FM-12.4.C** (webwork-opl:FM9.4) Find the choking pressure ratio of a nozzle.
  - EK: P*/P₀ = (2/(k+1))^(k/(k−1)).
  - P1 · drills: fm-critical-pressure, fm-choked-check
- ● **FM-12.4.D** (webwork-opl:FM9.5) Find the Mach number behind a normal shock.
  - EK: M₂² = (1 + (k−1)M₁²/2)/(kM₁² − (k−1)/2).
  - P1 · drills: fm-normal-shock, fm-shock-pressure-ratio
- ● **FM-12.4.E** (webwork-opl:FM9.6) Find a Mach angle.
  - EK: sin μ = 1/M: the weakest oblique wave.
  - P1 · drills: fm-mach-angle, fm-mach-from-angle
- ● **FM-12.4.F** (webwork-opl:FM9.7) Evaluate the Prandtl–Meyer function.
  - EK: ν(M) = √((k+1)/(k−1)) atan√((k−1)(M²−1)/(k+1)) − atan√(M²−1).
  - P1 · drills: fm-prandtl-meyer, fm-pm-turn
- ● **FM-12.4.G** (webwork-opl:FM9.8) Use Fanno flow (adiabatic duct with friction).
  - EK: 4f̄L*/D = (1 − M²)/(kM²) + ((k+1)/(2k)) ln[(k+1)M²/(2 + (k−1)M²)].
  - P1 · drills: fm-fanno, fm-fanno-temperature
- ● **FM-12.4.H** (webwork-opl:FM9.9) Use Rayleigh flow (frictionless duct with heat transfer).
  - EK: T₀/T₀* = 2(k+1)M²(1 + (k−1)M²/2)/(1 + kM²)².
  - P1 · drills: fm-rayleigh, fm-rayleigh-pressure

## Unit 13 · Open-channel flow and turbines

Big ideas: HEAD

### 13.1 Open channels



- ● **FM-13.1.A** (webwork-opl:FM10.1) Find the critical depth of a rectangular channel.
  - EK: y_c = (q²/g)^(1/3) with q the flow per unit width.
  - P1 · drills: fm-critical-depth, fm-minimum-specific-energy
- ● **FM-13.1.B** (webwork-opl:FM10.2) Find uniform-flow velocity with Manning's equation.
  - EK: V = (1/n) R^(2/3) S^(1/2) (SI); Chézy V = C√(RS).
  - P1 · drills: fm-manning, fm-manning-slope
- ● **FM-13.1.C** (webwork-opl:FM10.3) Find the most efficient rectangular section.
  - EK: For a given area, the best rectangle is twice as wide as deep: R = y/2.
  - P1 · drills: fm-best-section, fm-best-rectangle-radius
- ● **FM-13.1.D** (webwork-opl:FM10.4) Read the slope of a gradually varied flow profile.
  - EK: dy/dx = (S₀ − S_f)/(1 − Fr²).
  - P1 · drills: fm-gradually-varied, fm-profile-class
- ● **FM-13.1.E** (webwork-opl:FM10.5) Find the depth after a hydraulic jump.
  - EK: y₂/y₁ = ½(−1 + √(1 + 8Fr₁²)).
  - P1 · drills: fm-hydraulic-jump, fm-jump-head-loss

### 13.2 Turbines



- ● **FM-13.2.A** (webwork-opl:FM11.4) Find the power of a hydraulic turbine.
  - EK: P = ηρgQH; a Pelton wheel works best with buckets at half the jet speed.
  - P1 · drills: fm-turbine-power, fm-turbine-head

## Drills not yet placed on the map

- gc-annulus-flow (fm.viscous)
- gc-annulus-vs-pipe (fm.viscous)
- gc-couette-torque (fm.viscous)
- gc-couette-shear-rate (fm.viscous)
- gc-squeeze-film (fm.viscous)
- gc-squeeze-time (fm.viscous)
- gc-power-law-tube (fm.viscous)
- gc-apparent-viscosity (fm.viscous)
- gc-startup-time (fm.viscous)
- gc-stokes-first-problem (fm.viscous)
- gc-log-law (fm.similarity)
- gc-wall-region (fm.similarity)
- gc-blasius-drag (fm.external)
- gc-blasius-length-scaling (fm.external)
- gc-cylinder-cp (fm.external)
- gc-cylinder-pressure-drop (fm.external)
- gc-drop-drag (fm.external)
- gc-bubble-terminal (fm.external)
