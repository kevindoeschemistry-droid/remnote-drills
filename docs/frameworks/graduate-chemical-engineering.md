# Graduate Chemical Engineering Core — curriculum framework (draft 1)

Generated from `drills/frameworks/graduate-chemical-engineering.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**38 learning objectives** in 6 units (38 core): 38 drilled, 0 partly, 0 with no drills. Core: 38 / 38 drilled.

## Big ideas

- **SOLVE · Solve the governing equation, then read off the quantity.** A velocity, temperature or concentration field comes from a balance with its boundary conditions; forces, fluxes and rates are integrals or gradients of that field.
- **STABLE · Steady is not the same as stable.** A reactor, a mixture or a control loop can sit at a solution of its equations and still run away from it; a slope or a curvature decides.

## Practices

- **P1 · Compute.** Carry the model to a number with units.
- **P2 · Judge.** Decide stability, regime or direction from a derivative or a dimensionless group.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Momentum transport (CBE 220B) | core | — | 9 | 9 | 0 | 0 |
| 2 · Heat and mass transport (CBE 220A) | core | — | 6 | 6 | 0 | 0 |
| 3 · Advanced thermodynamics (CBE 240) | core | — | 7 | 7 | 0 | 0 |
| 4 · Reaction engineering (CBE 210) | core | — | 6 | 6 | 0 | 0 |
| 5 · Process dynamics and control (CBE 200) | core | — | 7 | 7 | 0 | 0 |
| 6 · Separations past the McCabe–Thiele diagram | core | — | 3 | 3 | 0 | 0 |

## Unit 1 · Momentum transport (CBE 220B)

Big ideas: SOLVE

### 1.1 Viscous, creeping and inviscid flow



- ● **GC-1.1.A** (uci-cbe-core:220B) Find the flow rate in an annulus from the Navier–Stokes equation in cylindrical coordinates.
  - EK: Solve (1/r)(r v′)′ = −(ΔP/L)/μ with no slip on both walls.
  - P1 · drills: gc-annulus-flow
- ● **GC-1.1.B** (uci-cbe-core:220B) Find the torque in circular Couette flow.
  - EK: v_θ = Ar + B/r; the torque on the inner cylinder is 4πμΩκ²R²/(1 − κ²) per unit length.
  - P1 · drills: gc-couette-torque
- ● **GC-1.1.C** (uci-cbe-core:220B) Find the force in a squeeze film from lubrication theory.
  - EK: Thin gap: p(r) = 3μV(R² − r²)/h³; F = 3πμVR⁴/(2h³).
  - P1 · drills: gc-squeeze-film
- ● **GC-1.1.D** (uci-cbe-core:220B) Find the friction drag of a laminar boundary layer.
  - EK: Blasius: local τ_w = 0.332ρU²/√Re_x; average C_f = 1.328/√Re_L.
  - P1 · drills: gc-blasius-drag
- ● **GC-1.1.E** (uci-cbe-core:220B) Find the pressure on a cylinder in potential flow.
  - EK: Surface speed 2U sin θ, so C_p = 1 − 4 sin²θ.
  - P1 · drills: gc-cylinder-cp
- ● **GC-1.1.F** (uci-cbe-core:220B) Find the flow rate of a power-law fluid in a tube.
  - EK: Q = πR³ n/(3n + 1) (ΔP R/(2mL))^{1/n}.
  - P1 · drills: gc-power-law-tube
- ● **GC-1.1.G** (uci-cbe-core:220B) Find the start-up time of viscous flow.
  - EK: The slowest mode of Couette start-up decays as exp(−π²νt/h²).
  - P1 · drills: gc-startup-time
- ● **GC-1.1.H** (uci-cbe-core:220B) Use the turbulent log law.
  - EK: u⁺ = (1/0.41) ln y⁺ + 5.0, with u* = √(τ_w/ρ) and y⁺ = y u*/ν.
  - P1 · drills: gc-log-law
- ● **GC-1.1.I** (uci-cbe-core:220B) Compare the fall of a drop with that of a rigid sphere.
  - EK: Hadamard–Rybczynski: drag 2πμaU(2 + 3λ)/(1 + λ), λ = μ_drop/μ.
  - P1 · drills: gc-drop-drag

## Unit 2 · Heat and mass transport (CBE 220A)

Big ideas: SOLVE

### 2.1 Scaling, unsteady and convective transport



- ● **GC-2.1.A** (uci-cbe-core:220A) Find the Taylor dispersion coefficient.
  - EK: K = D + U²a²/(48D) for laminar flow in a tube of radius a.
  - P1 · drills: gc-taylor-dispersion
- ● **GC-2.1.B** (uci-cbe-core:220A) Find the temperature rise from viscous heating.
  - EK: Couette flow with both walls at T₀: ΔT_max = μV²/(8k).
  - P1 · drills: gc-brinkman
- ● **GC-2.1.C** (uci-cbe-core:220A) Find a freezing time from the quasi-steady Stefan problem.
  - EK: ρL dδ/dt = kΔT/δ, so δ = √(2kΔT t/(ρL)).
  - P1 · drills: gc-stefan-freeze
- ● **GC-2.1.D** (uci-cbe-core:220A) Find the diffusion coefficient of a salt (ambipolar diffusion).
  - EK: Zero current couples the ions: D = 2D₊D₋/(D₊ + D₋) for a 1:1 salt.
  - P1 · drills: gc-ambipolar
- ● **GC-2.1.E** (uci-cbe-core:220A) Find a flux with a surface reaction that changes the moles.
  - EK: For A → 2B at a catalytic surface, N_B = −2N_A, so N_A = (cD/δ) ln(1 + y_A0).
  - P1 · drills: gc-film-reaction-flux
- ● **GC-2.1.F** (uci-cbe-core:220A) Find an average mass-transfer coefficient on a flat plate.
  - EK: Local Sh_x = 0.332 Re_x^{1/2} Sc^{1/3}; the plate average is twice the local value at the end.
  - P1 · drills: gc-plate-mass

## Unit 3 · Advanced thermodynamics (CBE 240)

Big ideas: SOLVE

### 3.1 Equations of state, mixtures and equilibria



- ● **GC-3.1.A** (uci-cbe-core:240) Find a van der Waals critical temperature from its constants.
  - EK: dP/dV = d²P/dV² = 0 gives T_c = 8a/(27Rb).
  - P1 · drills: gc-vdw-critical
- ● **GC-3.1.B** (uci-cbe-core:240) Find a compressibility factor from the Peng–Robinson equation.
  - EK: Solve the cubic in Z; take the largest root for vapour, the smallest for liquid.
  - P1 · drills: gc-peng-robinson-z
- ● **GC-3.1.C** (uci-cbe-core:240) Decide whether a mixture splits into two liquids.
  - EK: One-constant Margules: ∂²(Δg_mix/RT)/∂x₁² = 1/x₁ + 1/x₂ − 2A; negative means unstable.
  - P1 · drills: gc-margules-stability
- ● **GC-3.1.D** (uci-cbe-core:240) Find a residual enthalpy from the virial equation.
  - EK: H^R = P(B − T dB/dT) at low pressure.
  - P1 · drills: gc-virial-residual-h
- ● **GC-3.1.E** (uci-cbe-core:240) Solve simultaneous chemical equilibria.
  - EK: Each independent reaction has its own K; solve them together with the mole balance.
  - P1 · drills: gc-series-equilibria
- ● **GC-3.1.F** (uci-cbe-core:240) Integrate the van 't Hoff equation with a heat-capacity change.
  - EK: d ln K/dT = ΔH(T)/RT², ΔH(T) = ΔH₀ + ΔCp(T − T₀).
  - P1 · drills: gc-vant-hoff-cp
- ● **GC-3.1.G** (uci-cbe-core:240) Locate an azeotrope.
  - EK: At an azeotrope x = y, so γ₁P₁^sat = γ₂P₂^sat.
  - P1 · drills: gc-azeotrope

## Unit 4 · Reaction engineering (CBE 210)

Big ideas: SOLVE

### 4.1 Stability, catalysis, optimisation and dispersed phases



- ● **GC-4.1.A** (uci-cbe-core:210) Judge the stability of a CSTR steady state by the slope condition.
  - EK: Stable when the heat-removal line is steeper than the heat-generation curve: dR/dT > dG/dT.
  - P1 · drills: gc-cstr-slope
- ● **GC-4.1.B** (uci-cbe-core:210) Find the optimum temperature for a reversible exothermic reaction.
  - EK: Maximise r = k₁(1 − X) − k₂X at fixed X: T_opt = (E₂ − E₁)/(R ln[A₂E₂X/(A₁E₁(1 − X))]).
  - P1 · drills: gc-optimum-temperature
- ● **GC-4.1.C** (uci-cbe-core:210) Combine internal and external resistances into an overall effectiveness.
  - EK: Ω = η/(1 + ηφ²/(3Bi)), η = 3(φ coth φ − 1)/φ² for a first-order sphere.
  - P1 · drills: gc-overall-effectiveness
- ● **GC-4.1.D** (uci-cbe-core:210) Find an enhancement factor for gas absorption with reaction.
  - EK: Film theory, pseudo-first order: E = Ha/tanh Ha, Ha = √(kD)/k_L.
  - P1 · drills: gc-hatta-enhancement
- ● **GC-4.1.E** (uci-cbe-core:210) Find the overall rate in a slurry reactor from resistances in series.
  - EK: C_gas/r = 1/(k_b a_b) + 1/(k_c a_p) + 1/(η k a_p)-type terms add.
  - P1 · drills: gc-slurry-resistances
- ● **GC-4.1.F** (uci-cbe-core:210) Find a conversion with a decaying catalyst.
  - EK: First-order decay a = e^{−k_d t}: ln[1/(1 − X)] = (k/k_d)(1 − e^{−k_d t}).
  - P1 · drills: gc-deactivation

## Unit 5 · Process dynamics and control (CBE 200)

Big ideas: SOLVE

### 5.1 Responses, stability and tuning



- ● **GC-5.1.A** (uci-cbe-core:200) Find a time from a first-order step response.
  - EK: y = KM(1 − e^{−t/τ}); 63.2% at τ, 95% at 3τ, 99% at 4.6τ.
  - P1 · drills: gc-first-order-time
- ● **GC-5.1.B** (uci-cbe-core:200) Find the overshoot of an underdamped second-order process.
  - EK: OS = exp(−πζ/√(1 − ζ²)), independent of τ.
  - P1 · drills: gc-overshoot
- ● **GC-5.1.C** (uci-cbe-core:200) Find the offset under proportional control.
  - EK: Final value theorem: setpoint offset = 1/(1 + K K_c) for a first-order process.
  - P1 · drills: gc-p-offset
- ● **GC-5.1.D** (uci-cbe-core:200) Find the ultimate gain of a third-order process.
  - EK: Substitute s = iω in 1 + K_cG = 0: the imaginary part fixes ω_u, the real part K_c,u.
  - P1 · drills: gc-ultimate-gain
- ● **GC-5.1.E** (uci-cbe-core:200) Find the ultimate period, then a Ziegler–Nichols setting.
  - EK: ω_u = √(a₁/a₃); P_u = 2π/ω_u; ZN PI: K_c = 0.45K_cu, τ_I = P_u/1.2.
  - P1 · drills: gc-ultimate-period
- ● **GC-5.1.F** (uci-cbe-core:200) Find an amplitude ratio from the frequency response.
  - EK: First order: AR = K/√(1 + ω²τ²), phase −atan(ωτ).
  - P1 · drills: gc-amplitude-ratio
- ● **GC-5.1.G** (uci-cbe-core:200) Find the crossover frequency of a first-order-plus-dead-time process.
  - EK: Phase −atan(ωτ) − ωθ = −π; no closed form.
  - P1 · drills: gc-fopdt-crossover

## Unit 6 · Separations past the McCabe–Thiele diagram

Big ideas: SOLVE

### 6.1 Batch distillation and absorption



- ● **GC-6.1.A** (pe-chemical:6.B) Find what remains in a Rayleigh batch distillation.
  - EK: ln(W₀/W) = ∫ dx/(y − x) from x to x₀; with constant α it has a closed form.
  - P1 · drills: gc-rayleigh
- ● **GC-6.1.B** (pe-chemical:6.B) Find the minimum absorbent rate.
  - EK: (L/G)_min = (y_in − y_out)/(x*_out − x_in), x*_out = y_in/m for a dilute linear system.
  - P1 · drills: gc-min-absorbent
- ● **GC-6.1.C** (pe-chemical:6.B) Find where the feed line meets the rectifying line.
  - EK: q-line y = qx/(q − 1) − z/(q − 1); rectifying line y = Rx/(R + 1) + x_D/(R + 1).
  - P1 · drills: gc-q-line-intersection
