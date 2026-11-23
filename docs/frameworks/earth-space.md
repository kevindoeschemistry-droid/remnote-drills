# Earth and Space Science — curriculum framework (draft 1)

Generated from `drills/frameworks/earth-space.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**18 learning objectives** in 4 units (18 core): 18 drilled, 0 partly, 0 with no drills. Core: 18 / 18 drilled.

## Big ideas

- **GRAV · Gravity shapes the sky.** One law gives orbital periods, escape speeds and the motion of every planet and satellite.
- **LIGHT · Light carries the information.** A star's colour gives its temperature, its brightness and size its power, its spectrum its composition and motion.
- **BALANCE · Energy in equals energy out.** A planet's temperature is set where absorbed sunlight balances emitted infrared; the greenhouse effect and feedbacks move that balance.
- **CLOCKS · Decay is a clock.** Radioactive decay dates rocks and fossils; the choice of isotope sets the range of ages it can measure.

## Practices

- **P1 · Compute.** Carry a physical model to a number with sensible units and magnitude.
- **P2 · Explain.** Name the process, boundary or feedback behind an observation.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Earth's place in the universe | core | — | 8 | 8 | 0 | 0 |
| 2 · Earth's interior and history | core | — | 4 | 4 | 0 | 0 |
| 3 · Earth's systems and climate | core | — | 5 | 5 | 0 | 0 |
| 4 · Earth and human activity | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · Earth's place in the universe

Big ideas: GRAV, LIGHT

### 1.1 Orbits



- ● **ES-1.1.A** (ngss-hs:ESS1-4) Compute an orbital period from the central mass and radius.
  - EK: T = 2π√(a³/GM).
  - P1 · drills: es-kepler
- ● **ES-1.1.B** (ngss-hs:ESS1-4) Compute an escape speed.
  - EK: v = √(2GM/R).
  - Needs: ES-1.1.A
  - P1 · drills: es-escape

### 1.2 Stars



- ● **ES-1.2.A** (ngss-hs:ESS1-1) Find a star's peak wavelength from its temperature.
  - EK: λ_max = b/T.
  - P1 · drills: es-wien
- ● **ES-1.2.B** (ngss-hs:ESS1-1) Compute a star's luminosity from its radius and temperature.
  - EK: L = 4πR²σT⁴.
  - Needs: ES-1.2.A
  - P1 · drills: es-luminosity
- ● **ES-1.2.C** (ngss-hs:ESS1-1) Scale a main-sequence lifetime with mass.
  - EK: t ∝ M/L ∝ M⁻²·⁵.
  - Needs: ES-1.2.B
  - P1 · drills: es-star-life
- ● **ES-1.2.D** (ngss-hs:ESS1-1, ngss-hs:ESS1-3) Compute the energy released by a fusion step.
  - EK: Q = Δm c², 931.5 MeV per u.
  - P1 · drills: es-fusion-energy

### 1.3 Cosmology



- ● **ES-1.3.A** (ngss-hs:ESS1-2) Apply Hubble's law and estimate the Hubble time.
  - EK: v = H₀d; t ≈ 1/H₀.
  - P1 · drills: es-hubble
- ● **ES-1.3.B** (ngss-hs:ESS1-3) Say where an element was made.
  - EK: Big Bang, stellar fusion, neutron capture, spallation.
  - Needs: ES-1.2.D
  - P2 · drills: es-element-origin

## Unit 2 · Earth's interior and history

Big ideas: CLOCKS

### 2.1 Plates and the interior



- ● **ES-2.1.A** (ngss-hs:ESS2-1, ngss-hs:ESS1-5) Classify a plate boundary.
  - EK: Divergent, convergent, transform.
  - P2 · drills: es-plate-boundary
- ● **ES-2.1.B** (ngss-hs:ESS2-3) Say which seismic waves cross a region of the interior.
  - EK: S waves cannot cross liquid: the outer-core shadow.
  - P2 · drills: es-seismic

### 2.2 Dating



- ● **ES-2.2.A** (ngss-hs:ESS1-5, ngss-hs:ESS1-6) Compute an age from a daughter-to-parent ratio.
  - EK: t = (t½/ln 2) ln(1 + D/P).
  - P1 · drills: es-radiometric
- ● **ES-2.2.B** (ngss-hs:ESS1-6) Choose a dating method for a sample.
  - EK: ¹⁴C to 50 ky; K–Ar volcanic; U–Pb oldest.
  - Needs: ES-2.2.A
  - P2 · drills: es-dating-method

## Unit 3 · Earth's systems and climate

Big ideas: BALANCE

### 3.1 Energy balance



- ● **ES-3.1.A** (ngss-hs:ESS2-4, ib-physics-2025:B.2) Compute a planet's radiative-equilibrium temperature.
  - EK: T_e = [S(1 − α)/4σ]^¼.
  - P1 · drills: es-equilibrium-temp
- ● **ES-3.1.B** (ib-physics-2025:B.2) Compute the surface temperature under one absorbing layer.
  - EK: T_s = 2^¼ T_e.
  - Needs: ES-3.1.A
  - P1 · drills: es-one-layer
- ● **ES-3.1.C** (ngss-hs:ESS3-5, ib-biology-2025:D4.3) Estimate equilibrium warming from a CO₂ change.
  - EK: ΔF = 5.35 ln(C/C₀); ΔT = λΔF.
  - Needs: ES-3.1.A
  - P1 · drills: es-co2-forcing
- ● **ES-3.1.D** (ngss-hs:ESS2-2) Say whether a climate feedback amplifies or damps warming.
  - EK: Ice-albedo and water vapour positive; Planck and weathering negative.
  - P2 · drills: es-feedback

### 3.2 Carbon cycle



- ● **ES-3.2.A** (ngss-hs:ESS2-6, ngss-hs:ESS3-6) Convert between ppm CO₂ and gigatonnes of carbon.
  - EK: ≈ 2.13 GtC per ppm.
  - P1 · drills: es-carbon-mass

## Unit 4 · Earth and human activity

Big ideas: BALANCE

### 4.1 Growth



- ● **ES-4.1.A** (ngss-hs:ESS3-3) Compute a doubling time from a growth rate.
  - EK: t = ln 2/ln(1 + r) ≈ 70/%.
  - P1 · drills: es-doubling
