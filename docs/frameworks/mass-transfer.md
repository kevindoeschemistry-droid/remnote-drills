# Mass Transfer — curriculum framework (draft 1)

Generated from `drills/frameworks/mass-transfer.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**21 learning objectives** in 5 units (21 core): 21 drilled, 0 partly, 0 with no drills. Core: 21 / 21 drilled.

## Big ideas

- **FLUX · Fluxes need a reference frame.** A diffusive flux is measured relative to a mean velocity; the total flux adds the bulk flow. Which one a problem fixes (stagnant B, equimolar counterdiffusion) decides the answer.
- **SCALE · Time and length scales decide the regime.** L²/D, the Thiele modulus and the Biot and Sherwood numbers say which resistance controls before any equation is solved.

## Practices

- **P1 · Compute.** Carry a flux, coefficient or time to a number with units.
- **P2 · Scale.** Predict how a result changes when D, L, T or a flow changes, from the governing equation.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Diffusivities and fluxes | core | — | 6 | 6 | 0 | 0 |
| 2 · Steady diffusion with reaction and geometry | core | — | 5 | 5 | 0 | 0 |
| 3 · Unsteady diffusion | core | — | 3 | 3 | 0 | 0 |
| 4 · Interphase mass transfer | core | — | 5 | 5 | 0 | 0 |
| 5 · Multicomponent diffusion and membranes | core | — | 2 | 2 | 0 | 0 |

## Unit 1 · Diffusivities and fluxes

Big ideas: FLUX

### 1.1 Estimating diffusivities



- ● **MS-1.1.A** (pe-chemical:6.A) Scale a gas diffusivity with temperature and pressure.
  - EK: Chapman–Enskog: D_AB ∝ T^{3/2}/(P σ² Ω_D); ignoring the collision integral, D ∝ T^{3/2}/P.
  - P1 · drills: ms-gas-diffusivity-scaling
- ● **MS-1.1.B** (pe-chemical:6.A) Scale a liquid diffusivity with temperature and viscosity.
  - EK: Stokes–Einstein: D = kT/(6πμa), so D μ/T is constant.
  - P1 · drills: ms-liquid-diffusivity-scaling
- ● **MS-1.1.C** (pe-chemical:6.A) Estimate a Knudsen diffusivity and decide the regime.
  - EK: D_K = (d/3)√(8RT/πM); Knudsen diffusion takes over when the pore is smaller than the mean free path.
  - P1 · drills: ms-knudsen
- ● **MS-1.1.D** (pe-chemical:6.A) Find an effective diffusivity in a porous solid.
  - EK: D_eff = D ε/τ.
  - P1 · drills: ms-effective-diffusivity

### 1.2 Fluxes and reference frames



- ● **MS-1.2.A** (pe-chemical:6.A) Find the flux for diffusion through a stagnant gas.
  - EK: N_A = (cD/L) ln[(1 − x_A2)/(1 − x_A1)] (Stefan tube).
  - P1 · drills: ms-stagnant-film
- ● **MS-1.2.B** (pe-chemical:6.A) Compare stagnant-film and equimolar fluxes.
  - EK: N_stagnant/N_equimolar = 1/x_B,lm.
  - P1 · drills: ms-bulk-flow-factor

## Unit 2 · Steady diffusion with reaction and geometry

Big ideas: FLUX

### 2.1 Shell balances



- ● **MS-2.1.A** (pe-chemical:6.A) Find the effectiveness factor of a catalyst slab.
  - EK: η = tanh φ / φ with φ = L√(k/D_eff).
  - P1 · drills: ms-effectiveness-slab
- ● **MS-2.1.B** (pe-chemical:6.A) Find the effectiveness factor of a spherical pellet.
  - EK: η = (3/φ²)(φ coth φ − 1) with φ = R√(k/D_eff).
  - P1 · drills: ms-effectiveness-sphere
- ● **MS-2.1.C** (pe-chemical:6.A) Find steady diffusion through a spherical shell.
  - EK: Ẇ = 4πD(c₁ − c₂)/(1/r₁ − 1/r₂).
  - P1 · drills: ms-spherical-shell
- ● **MS-2.1.D** (pe-chemical:6.A) Find the lifetime of an evaporating droplet.
  - EK: Quasi-steady, Sh = 2: d(d²)/dt is constant (the d² law).
  - P1 · drills: ms-droplet-lifetime
- ● **MS-2.1.E** (pe-chemical:6.B) Find the absorption coefficient into a falling film.
  - EK: Penetration theory: k̄ = 2√(D/πt) with contact time t = L/v_max.
  - P1 · drills: ms-film-absorption

## Unit 3 · Unsteady diffusion

Big ideas: FLUX

### 3.1 Time scales and transients



- ● **MS-3.1.A** (pe-chemical:6.A) Estimate a diffusion time from L²/D.
  - EK: t ~ L²/D; penetration depth ~ √(4Dt).
  - P1 · drills: ms-diffusion-time
- ● **MS-3.1.B** (pe-chemical:6.A) Find the amount absorbed by a semi-infinite medium.
  - EK: M/A = 2c₀√(Dt/π).
  - P1 · drills: ms-semi-infinite-uptake
- ● **MS-3.1.C** (pe-chemical:6.A) Find the slowest decay time of a slab.
  - EK: Long-time behaviour: c ∝ exp(−π²Dt/(4L²)) for half-thickness L with fixed surfaces.
  - P1 · drills: ms-slab-time-constant

## Unit 4 · Interphase mass transfer

Big ideas: FLUX

### 4.1 Coefficients and resistances



- ● **MS-4.1.A** (pe-chemical:6.B) Combine film coefficients into an overall coefficient.
  - EK: 1/K_y = 1/k_y + m/k_x.
  - P1 · drills: ms-overall-coefficient
- ● **MS-4.1.B** (pe-chemical:6.B) Find the fraction of the resistance in the gas film.
  - EK: Gas share = (1/k_y)/(1/k_y + m/k_x).
  - P1 · drills: ms-resistance-fraction
- ● **MS-4.1.C** (pe-chemical:6.B) Use a sphere mass-transfer correlation.
  - EK: Ranz–Marshall: Sh = 2 + 0.6 Re^{1/2} Sc^{1/3}.
  - P1 · drills: ms-ranz-marshall
- ● **MS-4.1.D** (pe-chemical:6.B) Predict how k depends on D under each model.
  - EK: Film theory: k ∝ D; penetration and surface renewal: k ∝ D^{1/2}; boundary layers: k ∝ D^{2/3}.
  - P1 · drills: ms-model-scaling
- ● **MS-4.1.E** (pe-chemical:6.B) Find a packed-height from HTU and NTU.
  - EK: Z = H_OG N_OG; for dilute systems with straight lines, N_OG = (y₁ − y₂)/Δy_lm.
  - P1 · drills: ms-htu-ntu

## Unit 5 · Multicomponent diffusion and membranes

Big ideas: FLUX

### 5.1 Mixtures and membranes



- ● **MS-5.1.A** (pe-chemical:6.A) Find an effective diffusivity of A in a stagnant mixture.
  - EK: D_Am = (1 − x_A)/Σ_{j≠A}(x_j/D_Aj) (Wilke).
  - P1 · drills: ms-wilke-mixture
- ● **MS-5.1.B** (pe-chemical:6.B) Find a membrane flux and selectivity.
  - EK: N = P Δp / ℓ; ideal selectivity = P_A/P_B.
  - P1 · drills: ms-membrane-flux
