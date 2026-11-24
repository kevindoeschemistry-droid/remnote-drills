# Chemical Reaction Engineering — curriculum framework (draft 1)

Generated from `drills/frameworks/reaction-engineering.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**46 learning objectives** in 8 units (46 core): 46 drilled, 0 partly, 0 with no drills. Core: 46 / 46 drilled.

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
| 1 · Rates | core | — | 10 | 10 | 0 | 0 |
| 2 · Ideal reactors | core | — | 8 | 8 | 0 | 0 |
| 3 · Multiple reactions | core | — | 5 | 5 | 0 | 0 |
| 4 · Catalysis | core | — | 3 | 3 | 0 | 0 |
| 5 · Mechanisms and bioreactions | core | — | 6 | 6 | 0 | 0 |
| 6 · Nonisothermal reactors | core | — | 4 | 4 | 0 | 0 |
| 7 · Diffusion and reaction | core | — | 5 | 5 | 0 | 0 |
| 8 · Residence times and nonideal reactors | core | — | 5 | 5 | 0 | 0 |

## Unit 1 · Rates

Big ideas: CONCENTRATION

### 1.1 Rate laws and order



- ● **RE-1.1.A** (fe-chemical:12.A) Evaluate a power-law rate, find the order from how the rate responds to concentration, and read the order from the units of k.
  - EK: Doubling C multiplies an nth-order rate by 2ⁿ; k carries (mol/L)^(1−n) per time.
  - P1 · drills: cre-rate-from-law, cre-order-from-doubling, cre-rate-constant-units
- ● **RE-1.1.B** (fe-chemical:12.A) Compute a first-order half-life.
  - EK: t½ = ln 2 / k, independent of the starting concentration.
  - P1 · drills: cre-half-life
- ● **RE-1.1.C** Find the equilibrium conversion of a reversible reaction from K_C.
  - EK: A ⇌ B: X_e = K/(1 + K). A + B ⇌ C, equimolar: K C_A0 (1 − X)² = X.
  - Needs: RE-1.1.A
  - P1 · drills: re-equil-conversion

### 1.2 Temperature dependence



- ● **RE-1.2.A** (fe-chemical:12.B) Use the Arrhenius equation to find how k changes with temperature, and the activation energy from two rate constants.
  - EK: ln(k₂/k₁) = (Eₐ/R)(1/T₁ − 1/T₂), kelvin and joules.
  - P1 · drills: cre-arrhenius-ratio, cre-activation-energy, sc-arrhenius-ten-degrees

### 1.3 Stoichiometry



- ● **RE-1.3.A** Convert a rate for one species into the rate for another.
  - EK: −r_A/a = −r_B/b = r_C/c.
  - P1 · drills: re-relative-rates
- ● **RE-1.3.B** Compute ε for a gas-phase feed, with inerts.
  - EK: ε = y_A0 δ, δ = change in gas moles per mole of A.
  - Needs: RE-1.3.A
  - P1 · drills: re-epsilon
- ● **RE-1.3.C** Write C_A in a gas-phase flow reactor with a change in moles, temperature and pressure.
  - EK: C_A = C_A0 (1 − X)/(1 + εX) · (P/P₀)(T₀/T).
  - Needs: RE-1.3.B
  - P1 · drills: re-gas-conc

### 1.4 Rate data



- ● **RE-1.4.A** Pick the order whose integrated rate law linearises a batch data set.
  - EK: Zero: C vs t; first: ln C vs t; second: 1/C vs t.
  - Needs: RE-2.1.A
  - P2 · drills: re-integral-plot
- ● **RE-1.4.B** Find the order from how the half-life depends on C_A0.
  - EK: t½ ∝ C_A0^(1 − n).
  - Needs: RE-1.1.B
  - P1 · drills: re-half-life-order
- ● **RE-1.4.C** Find an order from initial rates when two concentrations change at once.
  - EK: Divide the rate laws; remove the known factor first.
  - Needs: RE-1.1.A
  - P1 · drills: re-initial-rates

## Unit 2 · Ideal reactors

Big ideas: BALANCE, CONCENTRATION, TIME

### 2.1 Batch



- ● **RE-2.1.A** (fe-chemical:12.C, fe-chemical:12.E) Find the batch time for a given conversion, first and second order.
  - EK: First order: t = (1/k) ln[1/(1 − X)]. Second order: t = X / [k C_A0 (1 − X)].
  - P1 · drills: cre-batch-first-order-time, cre-batch-second-order-time, sc-batch-time-rate-constant, sc-second-order-half-life

### 2.2 CSTR



- ● **RE-2.2.A** (fe-chemical:12.E) Size a CSTR for a conversion, find the conversion from the space time, and treat tanks in series.
  - EK: V = v₀X / [k(1 − X)]; X = kτ/(1 + kτ); n equal tanks give C/C₀ = 1/(1 + kτ)ⁿ.
  - P1 · drills: cre-cstr-volume, cre-cstr-conversion, cre-cstrs-in-series, sc-cstr-volume-conversion
- ● **RE-2.2.B** Find the conversion of a second-order reaction in a CSTR.
  - EK: τkC_A0 = X/(1 − X)²; take the root below 1.
  - Needs: RE-2.2.A
  - P1 · drills: re-cstr-second-order
- ● **RE-2.2.C** Find how long a CSTR takes to approach steady state after start-up.
  - EK: t = τ ln[1/(1 − f)]/(1 + τk); 99% ≈ 4.6τ/(1 + τk).
  - Needs: RE-2.2.A
  - P1 · drills: re-cstr-startup

### 2.3 PFR



- ● **RE-2.3.A** (fe-chemical:12.E) Size a plug-flow reactor and compare it with a CSTR.
  - EK: V = (v₀/k) ln[1/(1 − X)]; for positive order a PFR is always smaller.
  - P1 · P2 · drills: cre-pfr-volume, cre-reactor-comparison
- ● **RE-2.3.B** Size a PFR for a gas-phase reaction with a change in moles, first or second order.
  - EK: C_A = C_A0(1 − X)/(1 + εX) inside the design integral.
  - Needs: RE-2.3.A, RE-1.3.C
  - P1 · drills: re-pfr-gas-eps
- ● **RE-2.3.C** Size reactors in series (CSTR then PFR) from the Levenspiel plot.
  - EK: Rectangle for the CSTR, area under F_A0/(−r_A) for the PFR.
  - Needs: RE-2.3.A
  - P1 · P2 · drills: re-cstr-then-pfr

### 2.4 Packed beds



- ● **RE-2.4.A** Find the pressure ratio and conversion in an isothermal packed bed with pressure drop (ε = 0).
  - EK: y = (1 − αW)^½; ln[1/(1 − X)] = (k′/v₀)(2/3α)[1 − (1 − αW)^(3/2)].
  - Needs: RE-2.3.A
  - P1 · drills: re-pbr-pressure-drop

## Unit 3 · Multiple reactions

Big ideas: CONCENTRATION

### 3.1 Series and parallel



- ● **RE-3.1.A** (fe-chemical:12.D) Find when the intermediate of a series reaction peaks.
  - EK: t_max = ln(k₁/k₂)/(k₁ − k₂).
  - P1 · drills: cre-series-optimum-time
- ● **RE-3.1.B** (fe-chemical:12.C, fe-chemical:12.D) Compute the instantaneous selectivity of parallel reactions and choose the reactor that favours the desired one.
  - EK: S goes as C_A^(a_D − a_U): high concentration if the desired path has the higher order, low if the lower.
  - P1 · P2 · drills: cre-parallel-selectivity, cre-selectivity-strategy
- ● **RE-3.1.C** Find the highest intermediate concentration in a batch series reaction.
  - EK: C_B,max/C_A0 = (k₁/k₂)^(k₂/(k₂ − k₁)).
  - Needs: RE-3.1.A
  - P1 · drills: re-series-bmax
- ● **RE-3.1.D** Find the space time that maximises the intermediate in a CSTR, and that maximum.
  - EK: τ_opt = 1/√(k₁k₂).
  - Needs: RE-3.1.C, RE-2.2.A
  - P1 · P2 · drills: re-cstr-series-opt
- ● **RE-3.1.E** Compute the product made by parallel reactions in a CSTR or a PFR to a given conversion.
  - EK: CSTR: C_D = (C_A0 − C_A)φ(C_A). PFR: C_D = ∫φ dC_A.
  - Needs: RE-3.1.B
  - P1 · P2 · drills: re-parallel-overall

## Unit 4 · Catalysis

Big ideas: CONCENTRATION

### 4.1 Surfaces



- ● **RE-4.1.A** (fe-chemical:12.F) Compute Langmuir coverage and state what a catalyst does and does not change.
  - EK: θ = KP/(1 + KP); a catalyst lowers the activation energy and leaves equilibrium alone.
  - P1 · P2 · drills: cre-langmuir-coverage, cre-catalysis-facts
- ● **RE-4.1.B** Evaluate a Langmuir–Hinshelwood rate law, single or dual site.
  - EK: θ_v = 1/(1 + K_AP_A + K_BP_B); dual site squares it.
  - Needs: RE-4.1.A
  - P1 · drills: re-lh-rate
- ● **RE-4.1.C** Identify the rate-limiting step from the form of a catalytic rate law.
  - EK: The denominator lists the species whose adsorption is in equilibrium.
  - Needs: RE-4.1.B
  - P2 · drills: re-rls-pick

## Unit 5 · Mechanisms and bioreactions

Big ideas: CONCENTRATION

### 5.1 Pseudo-steady state



- ● **RE-5.1.A** Derive a rate law from a mechanism with the PSSH and evaluate it.
  - EK: Set the net rate of each active intermediate to zero; Lindemann: r = k₁k₃C²/(k₂C + k₃).
  - Needs: RE-1.1.A
  - P1 · drills: re-lindemann
- ● **RE-5.1.B** Read the apparent order of a PSSH rate law in its high and low limits.
  - EK: High C: first order; low C: second order.
  - Needs: RE-5.1.A
  - P2 · drills: re-lindemann-order

### 5.2 Enzymes and cells



- ● **RE-5.2.A** Compute an enzyme rate from elementary steps (Michaelis–Menten).
  - EK: V_max = k₂E_t; K_m = (k₋₁ + k₂)/k₁.
  - Needs: RE-5.1.A
  - P1 · drills: re-mm-steps
- ● **RE-5.2.B** Find V_max and K_m from rate data.
  - EK: 1/r = (K_m/V_max)(1/S) + 1/V_max.
  - Needs: RE-5.2.A
  - P1 · drills: re-mm-fit
- ● **RE-5.2.C** Classify an inhibitor from how it changes K_m and V_max.
  - EK: Competitive: K_m up. Uncompetitive: both down. Noncompetitive: V_max down.
  - Needs: RE-5.2.B
  - P2 · drills: re-inhibition-type
- ● **RE-5.2.D** Find the steady state and washout of a chemostat with Monod growth.
  - EK: μ = D ⇒ S = K_sD/(μ_max − D); D_max = μ_max S₀/(K_s + S₀).
  - Needs: RE-5.2.A, RE-2.2.A
  - P1 · drills: re-chemostat

## Unit 6 · Nonisothermal reactors

Big ideas: BALANCE

### 6.1 Adiabatic operation



- ● **RE-6.1.A** (webwork-opl:TH13.9) Relate temperature and conversion in an adiabatic reactor.
  - EK: T = T₀ + (−ΔH)X/ΣΘC_p.
  - Needs: RE-2.3.A
  - P1 · drills: re-adiabatic-T
- ● **RE-6.1.B** Find the adiabatic equilibrium conversion of a reversible exothermic reaction.
  - EK: Intersect X_EB(T) with X_e(T) = K/(1 + K), K from van 't Hoff.
  - Needs: RE-6.1.A, RE-1.1.C
  - P1 · drills: re-adiabatic-xe

### 6.2 CSTR steady states



- ● **RE-6.2.A** Count the steady states of an adiabatic CSTR from G(T) and R(T).
  - EK: Sigmoid generation meets a straight removal line once or three times; the middle state is unstable.
  - Needs: RE-6.1.A, RE-1.2.A
  - P2 · drills: re-mss-count
- ● **RE-6.2.B** Find the temperature of an adiabatic CSTR with a single steady state.
  - EK: Solve X_MB(T) = X_EB(T).
  - Needs: RE-6.2.A
  - P1 · drills: re-cstr-adiabatic-T

## Unit 7 · Diffusion and reaction

Big ideas: CONCENTRATION

### 7.1 External mass transfer



- ● **RE-7.1.A** Combine film mass transfer and a first-order surface rate in series.
  - EK: −r″ = C_b/(1/k_c + 1/k_r).
  - Needs: RE-4.1.A
  - P1 · drills: re-ext-mt
- ● **RE-7.1.B** Find the conversion of a mass-transfer-limited packed bed.
  - EK: X = 1 − exp(−k_c a_c L/U).
  - Needs: RE-7.1.A
  - P1 · drills: re-mt-bed

### 7.2 Internal diffusion



- ● **RE-7.2.A** Compute the Thiele modulus and internal effectiveness factor of a slab or sphere.
  - EK: Slab η = tanh φ/φ; sphere η = (3/φ²)(φ coth φ − 1).
  - Needs: RE-7.1.A
  - P1 · drills: re-effectiveness
- ● **RE-7.2.B** Judge internal diffusion limitation with the Weisz–Prater parameter.
  - EK: C_WP = ηφ² for first order; ≫ 1 means limited.
  - Needs: RE-7.2.A
  - P1 · P2 · drills: re-weisz-prater
- ● **RE-7.2.C** Combine external and internal resistances into an overall rate.
  - EK: Rate = C_b/[1/(k_ca_c) + 1/(ηk)].
  - Needs: RE-7.2.A, RE-7.1.A
  - P1 · drills: re-overall-eff

## Unit 8 · Residence times and nonideal reactors

Big ideas: TIME

### 8.1 Residence-time distributions



- ● **RE-8.1.A** Compute the mean residence time and variance from pulse-tracer data.
  - EK: t_m = ∫tE dt, σ² = ∫(t − t_m)²E dt.
  - Needs: RE-2.2.A
  - P1 · drills: re-rtd-moments
- ● **RE-8.1.B** Find the fraction of fluid leaving before or after a time for one or more ideal tanks.
  - EK: F = 1 − e^(−nθ) Σ (nθ)^i/i!.
  - Needs: RE-8.1.A
  - P1 · drills: re-tanks-F

### 8.2 Conversion from the RTD



- ● **RE-8.2.A** Predict conversion with the segregation model.
  - EK: X̄ = ∫X_batch(t)E(t) dt; linear kinetics ignore mixing.
  - Needs: RE-8.1.B, RE-2.1.A
  - P1 · drills: re-segregation
- ● **RE-8.2.B** Fit a tanks-in-series model to an RTD and predict a first-order conversion.
  - EK: n = t_m²/σ²; X = 1 − (1 + kt_m/n)^(−n).
  - Needs: RE-8.1.A, RE-2.2.A
  - P1 · drills: re-tis-model
- ● **RE-8.2.C** Predict a first-order conversion with the dispersion model.
  - EK: Danckwerts closed–closed: q = √(1 + 4Da/Pe).
  - Needs: RE-8.2.B
  - P1 · drills: re-dispersion

## Drills not yet placed on the map

- gc-deactivation (cre.catalysis)
- gc-cstr-slope (cre.nonisothermal)
- gc-optimum-temperature (cre.nonisothermal)
- gc-overall-effectiveness (cre.diffusion)
- gc-hatta-enhancement (cre.diffusion)
- gc-slurry-resistances (cre.diffusion)
