# Chemical Reaction Engineering — curriculum framework (draft 1)

Generated from `drills/frameworks/reaction-engineering.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**52 learning objectives** in 9 units (46 core): 52 drilled, 0 partly, 0 with no drills. Core: 46 / 46 drilled.

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
| 9 · Bioprocessing | extension | — | 6 | 6 | 0 | 0 |

## Unit 1 · Rates

Big ideas: CONCENTRATION

### 1.1 Rate laws and order



- ● **RE-1.1.A** (fe-chemical:12.A) Evaluate a power-law rate, find the order from how the rate responds to concentration, and read the order from the units of k.
  - EK: Doubling C multiplies an nth-order rate by 2ⁿ; k carries (mol/L)^(1−n) per time.
  - P1 · drills: cre-rate-from-law, cre-order-from-doubling, cre-rate-constant-units
- ● **RE-1.1.B** (fe-chemical:12.A) Compute a first-order half-life.
  - EK: t½ = ln 2 / k, independent of the starting concentration.
  - P1 · drills: cre-half-life, re-k-from-fraction
- ● **RE-1.1.C** Find the equilibrium conversion of a reversible reaction from K_C.
  - EK: A ⇌ B: X_e = K/(1 + K). A + B ⇌ C, equimolar: K C_A0 (1 − X)² = X.
  - Needs: RE-1.1.A
  - P1 · drills: re-equil-conversion, re-kc-from-conversion

### 1.2 Temperature dependence



- ● **RE-1.2.A** (fe-chemical:12.B) Use the Arrhenius equation to find how k changes with temperature, and the activation energy from two rate constants.
  - EK: ln(k₂/k₁) = (Eₐ/R)(1/T₁ − 1/T₂), kelvin and joules.
  - P1 · drills: cre-arrhenius-ratio, cre-activation-energy, sc-arrhenius-ten-degrees

### 1.3 Stoichiometry



- ● **RE-1.3.A** Convert a rate for one species into the rate for another.
  - EK: −r_A/a = −r_B/b = r_C/c.
  - P1 · drills: re-relative-rates, re-net-rate
- ● **RE-1.3.B** Compute ε for a gas-phase feed, with inerts.
  - EK: ε = y_A0 δ, δ = change in gas moles per mole of A.
  - Needs: RE-1.3.A
  - P1 · drills: re-epsilon, re-inert-from-epsilon
- ● **RE-1.3.C** Write C_A in a gas-phase flow reactor with a change in moles, temperature and pressure.
  - EK: C_A = C_A0 (1 − X)/(1 + εX) · (P/P₀)(T₀/T).
  - Needs: RE-1.3.B
  - P1 · drills: re-gas-conc, re-exit-flow

### 1.4 Rate data



- ● **RE-1.4.A** Pick the order whose integrated rate law linearises a batch data set.
  - EK: Zero: C vs t; first: ln C vs t; second: 1/C vs t.
  - Needs: RE-2.1.A
  - P2 · drills: re-integral-plot, re-k-two-points
- ● **RE-1.4.B** Find the order from how the half-life depends on C_A0.
  - EK: t½ ∝ C_A0^(1 − n).
  - Needs: RE-1.1.B
  - P1 · drills: re-half-life-order, re-half-life-predict
- ● **RE-1.4.C** Find an order from initial rates when two concentrations change at once.
  - EK: Divide the rate laws; remove the known factor first.
  - Needs: RE-1.1.A
  - P1 · drills: re-initial-rates, re-rate-predict

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
  - P1 · drills: re-cstr-second-order, re-cstr2-volume
- ● **RE-2.2.C** Find how long a CSTR takes to approach steady state after start-up.
  - EK: t = τ ln[1/(1 − f)]/(1 + τk); 99% ≈ 4.6τ/(1 + τk).
  - Needs: RE-2.2.A
  - P1 · drills: re-cstr-startup, re-cstr-approach

### 2.3 PFR



- ● **RE-2.3.A** (fe-chemical:12.E) Size a plug-flow reactor and compare it with a CSTR.
  - EK: V = (v₀/k) ln[1/(1 − X)]; for positive order a PFR is always smaller.
  - P1 · P2 · drills: cre-pfr-volume, cre-reactor-comparison
- ● **RE-2.3.C** Size reactors in series (CSTR then PFR) from the Levenspiel plot.
  - EK: Rectangle for the CSTR, area under F_A0/(−r_A) for the PFR.
  - Needs: RE-2.3.A
  - P1 · P2 · drills: re-cstr-then-pfr, re-pfr-then-cstr
- ● **RE-2.3.B** Size a PFR for a gas-phase reaction with a change in moles, first or second order.
  - EK: C_A = C_A0(1 − X)/(1 + εX) inside the design integral.
  - Needs: RE-2.3.A, RE-1.3.C
  - P1 · drills: re-pfr-gas-eps, re-epsilon-volume-ratio

### 2.4 Packed beds



- ● **RE-2.4.A** Find the pressure ratio and conversion in an isothermal packed bed with pressure drop (ε = 0).
  - EK: y = (1 − αW)^½; ln[1/(1 − X)] = (k′/v₀)(2/3α)[1 − (1 − αW)^(3/2)].
  - Needs: RE-2.3.A
  - P1 · drills: re-pbr-pressure-drop, re-pbr-pressure

## Unit 3 · Multiple reactions

Big ideas: CONCENTRATION

### 3.1 Series and parallel



- ● **RE-3.1.A** (fe-chemical:12.D) Find when the intermediate of a series reaction peaks.
  - EK: t_max = ln(k₁/k₂)/(k₁ − k₂).
  - P1 · drills: cre-series-optimum-time, re-series-cc
- ● **RE-3.1.B** (fe-chemical:12.C, fe-chemical:12.D) Compute the instantaneous selectivity of parallel reactions and choose the reactor that favours the desired one.
  - EK: S goes as C_A^(a_D − a_U): high concentration if the desired path has the higher order, low if the lower.
  - P1 · P2 · drills: cre-parallel-selectivity, cre-selectivity-strategy
- ● **RE-3.1.C** Find the highest intermediate concentration in a batch series reaction.
  - EK: C_B,max/C_A0 = (k₁/k₂)^(k₂/(k₂ − k₁)).
  - Needs: RE-3.1.A
  - P1 · drills: re-series-bmax, re-series-equal-k
- ● **RE-3.1.D** Find the space time that maximises the intermediate in a CSTR, and that maximum.
  - EK: τ_opt = 1/√(k₁k₂).
  - Needs: RE-3.1.C, RE-2.2.A
  - P1 · P2 · drills: re-cstr-series-opt, re-cstr-series-yield
- ● **RE-3.1.E** Compute the product made by parallel reactions in a CSTR or a PFR to a given conversion.
  - EK: CSTR: C_D = (C_A0 − C_A)φ(C_A). PFR: C_D = ∫φ dC_A.
  - Needs: RE-3.1.B
  - P1 · P2 · drills: re-parallel-overall, re-instant-selectivity

## Unit 4 · Catalysis

Big ideas: CONCENTRATION

### 4.1 Surfaces



- ● **RE-4.1.A** (fe-chemical:12.F) Compute Langmuir coverage and state what a catalyst does and does not change.
  - EK: θ = KP/(1 + KP); a catalyst lowers the activation energy and leaves equilibrium alone.
  - P1 · P2 · drills: cre-langmuir-coverage, cre-catalysis-facts
- ● **RE-4.1.B** Evaluate a Langmuir–Hinshelwood rate law, single or dual site.
  - EK: θ_v = 1/(1 + K_AP_A + K_BP_B); dual site squares it.
  - Needs: RE-4.1.A
  - P1 · drills: re-lh-rate, re-lh-max
- ● **RE-4.1.C** Identify the rate-limiting step from the form of a catalytic rate law.
  - EK: The denominator lists the species whose adsorption is in equilibrium.
  - Needs: RE-4.1.B
  - P2 · drills: re-rls-pick, re-langmuir-coverage

## Unit 5 · Mechanisms and bioreactions

Big ideas: CONCENTRATION

### 5.1 Pseudo-steady state



- ● **RE-5.1.A** Derive a rate law from a mechanism with the PSSH and evaluate it.
  - EK: Set the net rate of each active intermediate to zero; Lindemann: r = k₁k₃C²/(k₂C + k₃).
  - Needs: RE-1.1.A
  - P1 · drills: re-lindemann, re-lindemann-falloff
- ● **RE-5.1.B** Read the apparent order of a PSSH rate law in its high and low limits.
  - EK: High C: first order; low C: second order.
  - Needs: RE-5.1.A
  - P2 · drills: re-lindemann-order, re-apparent-order

### 5.2 Enzymes and cells



- ● **RE-5.2.A** Compute an enzyme rate from elementary steps (Michaelis–Menten).
  - EK: V_max = k₂E_t; K_m = (k₋₁ + k₂)/k₁.
  - Needs: RE-5.1.A
  - P1 · drills: re-mm-steps, re-enzyme-bound-fraction
- ● **RE-5.2.B** Find V_max and K_m from rate data.
  - EK: 1/r = (K_m/V_max)(1/S) + 1/V_max.
  - Needs: RE-5.2.A
  - P1 · drills: re-mm-fit, re-substrate-for-rate
- ● **RE-5.2.C** Classify an inhibitor from how it changes K_m and V_max.
  - EK: Competitive: K_m up. Uncompetitive: both down. Noncompetitive: V_max down.
  - Needs: RE-5.2.B
  - P2 · drills: re-inhibition-type, re-competitive-rate
- ● **RE-5.2.D** Find the steady state and washout of a chemostat with Monod growth.
  - EK: μ = D ⇒ S = K_sD/(μ_max − D); D_max = μ_max S₀/(K_s + S₀).
  - Needs: RE-5.2.A, RE-2.2.A
  - P1 · drills: re-chemostat, re-chemostat-productivity

## Unit 6 · Nonisothermal reactors

Big ideas: BALANCE

### 6.1 Adiabatic operation



- ● **RE-6.1.A** (webwork-opl:TH13.9) Relate temperature and conversion in an adiabatic reactor.
  - EK: T = T₀ + (−ΔH)X/ΣΘC_p.
  - Needs: RE-2.3.A
  - P1 · drills: re-adiabatic-T, re-adiabatic-X
- ● **RE-6.1.B** Find the adiabatic equilibrium conversion of a reversible exothermic reaction.
  - EK: Intersect X_EB(T) with X_e(T) = K/(1 + K), K from van 't Hoff.
  - Needs: RE-6.1.A, RE-1.1.C
  - P1 · drills: re-adiabatic-xe, re-equilibrium-X-T

### 6.2 CSTR steady states



- ● **RE-6.2.A** Count the steady states of an adiabatic CSTR from G(T) and R(T).
  - EK: Sigmoid generation meets a straight removal line once or three times; the middle state is unstable.
  - Needs: RE-6.1.A, RE-1.2.A
  - P2 · drills: re-mss-count, re-removal-line, gc-cstr-slope
- ● **RE-6.2.B** Find the temperature of an adiabatic CSTR with a single steady state.
  - EK: Solve X_MB(T) = X_EB(T).
  - Needs: RE-6.2.A
  - P1 · drills: re-cstr-adiabatic-T, re-cstr-X-at-T

## Unit 7 · Diffusion and reaction

Big ideas: CONCENTRATION

### 7.1 External mass transfer



- ● **RE-7.1.A** Combine film mass transfer and a first-order surface rate in series.
  - EK: −r″ = C_b/(1/k_c + 1/k_r).
  - Needs: RE-4.1.A
  - P1 · drills: re-ext-mt, re-which-limits
- ● **RE-7.1.B** Find the conversion of a mass-transfer-limited packed bed.
  - EK: X = 1 − exp(−k_c a_c L/U).
  - Needs: RE-7.1.A
  - P1 · drills: re-mt-bed, re-mt-bed-length

### 7.2 Internal diffusion



- ● **RE-7.2.A** Compute the Thiele modulus and internal effectiveness factor of a slab or sphere.
  - EK: Slab η = tanh φ/φ; sphere η = (3/φ²)(φ coth φ − 1).
  - Needs: RE-7.1.A
  - P1 · drills: re-effectiveness, re-deff-from-rate
- ● **RE-7.2.B** Judge internal diffusion limitation with the Weisz–Prater parameter.
  - EK: C_WP = ηφ² for first order; ≫ 1 means limited.
  - Needs: RE-7.2.A
  - P1 · P2 · drills: re-weisz-prater, re-wp-max-radius
- ● **RE-7.2.C** Combine external and internal resistances into an overall rate.
  - EK: Rate = C_b/[1/(k_ca_c) + 1/(ηk)].
  - Needs: RE-7.2.A, RE-7.1.A
  - P1 · drills: re-overall-eff, gc-overall-effectiveness

## Unit 8 · Residence times and nonideal reactors

Big ideas: TIME

### 8.1 Residence-time distributions



- ● **RE-8.1.A** Compute the mean residence time and variance from pulse-tracer data.
  - EK: t_m = ∫tE dt, σ² = ∫(t − t_m)²E dt.
  - Needs: RE-2.2.A
  - P1 · drills: re-rtd-moments, re-tanks-from-variance
- ● **RE-8.1.B** Find the fraction of fluid leaving before or after a time for one or more ideal tanks.
  - EK: F = 1 − e^(−nθ) Σ (nθ)^i/i!.
  - Needs: RE-8.1.A
  - P1 · drills: re-tanks-F, re-tanks-E

### 8.2 Conversion from the RTD



- ● **RE-8.2.A** Predict conversion with the segregation model.
  - EK: X̄ = ∫X_batch(t)E(t) dt; linear kinetics ignore mixing.
  - Needs: RE-8.1.B, RE-2.1.A
  - P1 · drills: re-segregation, re-segregation-zero-order
- ● **RE-8.2.B** Fit a tanks-in-series model to an RTD and predict a first-order conversion.
  - EK: n = t_m²/σ²; X = 1 − (1 + kt_m/n)^(−n).
  - Needs: RE-8.1.A, RE-2.2.A
  - P1 · drills: re-tis-model, re-tis-design
- ● **RE-8.2.C** Predict a first-order conversion with the dispersion model.
  - EK: Danckwerts closed–closed: q = √(1 + 4Da/Pe).
  - Needs: RE-8.2.B
  - P1 · drills: re-dispersion, re-dispersion-variance

## Unit 9 · Bioprocessing (extension)

Big ideas: TIME

### 9.1 Growth and product formation



- ● **RE-9.1.A** (fe-chemical:5.E) Compute a specific growth rate from the Monod equation and the doubling time it gives
  - EK: Monod kinetics is Michaelis-Menten applied to a whole organism: growth saturates at a maximum specific rate, and the doubling time is the natural logarithm of two over that rate.
  - P1 · drills: fe-monod-rate, fe-doubling-time
- ● **RE-9.1.B** (fe-chemical:5.E) Compute a yield coefficient and the substrate a stated batch needs
  - EK: A yield coefficient is cells or product per unit substrate consumed, so the substrate charge follows from the target titre; what the coefficient leaves out is maintenance, which is why a slow fermentation uses more substrate per gram of product than a fast one.
  - P1 · drills: fe-yield-substrate, fe-yield-from-batch
- ● **RE-9.1.C** (fe-chemical:5.E) Compute the dilution rate at which a chemostat washes out and the productivity near it
  - EK: At steady state in a chemostat the specific growth rate equals the dilution rate, so raising the feed rate raises productivity until the dilution rate reaches the maximum growth rate, at which point the culture washes out.
  - P1 · drills: fe-washout, fe-chemostat-feed

### 9.2 Bioreactor operation



- ● **RE-9.2.A** (fe-chemical:5.E) Compute the oxygen transfer a stated aerobic fermentation needs and compare it with the supply
  - EK: An aerobic culture's oxygen demand is its oxygen uptake rate, and the supply is the transfer coefficient times the driving force to the dissolved concentration; because oxygen is barely soluble, the driving force is small and transfer is usually what limits scale-up rather than kinetics.
  - P1 · drills: fe-oxygen-demand, fe-kla-needed
- ● **RE-9.2.B** (fe-chemical:5.E) State which mode of bioreactor operation a stated objective calls for
  - EK: Batch is simplest and gives a defined lot, fed-batch avoids substrate inhibition and catabolite repression and is what most industrial fermentations use, continuous gives the highest productivity but risks contamination and strain drift over long runs, and perfusion keeps cells while removing product.
  - P2 · drills: fe-reactor-mode, fe-fedbatch-feed
- ● **RE-9.2.C** (fe-chemical:5.E) Compute the sterilisation hold a stated thermal death requirement needs
  - EK: Thermal death is first order in viable count, so the hold time is the number of log reductions times the decimal reduction time at that temperature; the design basis is the probability of one survivor in the whole batch, not an average.
  - P1 · drills: fe-sterilisation-hold, fe-sterilisation-logs

## Drills not yet placed on the map

- gc-deactivation (cre.catalysis)
- gc-deactivation-limit (cre.catalysis)
- gc-generation-slope (cre.nonisothermal)
- gc-optimum-temperature (cre.nonisothermal)
- gc-equilibrium-temperature (cre.nonisothermal)
- gc-surface-concentration (cre.diffusion)
- gc-hatta-enhancement (cre.diffusion)
- gc-hatta-regime (cre.diffusion)
- gc-slurry-resistances (cre.diffusion)
- gc-slurry-controlling (cre.diffusion)
