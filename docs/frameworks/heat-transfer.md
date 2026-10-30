# Heat Transfer — curriculum framework (draft 1)

Generated from `drills/frameworks/heat-transfer.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**98 learning objectives** in 14 units (90 core): 73 drilled, 6 partly, 19 with no drills. Core: 65 / 90 drilled.

## Big ideas

- **ENG · Energy is conserved.** Every problem starts as an energy balance on a control volume or a surface — in, out, generated, stored. The balance, not a memorised formula, is what fixes the answer.
- **RATE · Rates follow driving potential over resistance.** Conduction, convection and radiation each move heat at a rate set by a temperature difference and a resistance; resistances add in series and parallel, and the largest one controls.
- **FIELD · Temperature is a field set by an equation and its boundaries.** The heat equation plus boundary and initial conditions determines T everywhere; geometry and boundaries, not the material alone, shape the profile.
- **SCALE · Dimensionless groups decide the model.** Bi, Fo, Re, Pr, Gr, Ra and Nu say which simplification is valid — lumped or not, laminar or turbulent, free or forced — before any number is computed.
- **SYS · Real systems are networks of modes.** Devices combine conduction, convection and radiation in series and parallel; analysing and designing them means building that network and finding the bottleneck.

## Practices

- **P1 · Define the system.** Draw the control volume or surface, label every energy term (in, out, generation, storage), state steady or transient.
- **P2 · Set up the model.** State the assumptions (1-D, constant k, …) and translate the physical description into the governing equation and boundary/initial conditions.
- **P3 · Choose the right relation.** Pick the correlation, shape factor, chart or solution that fits — check its validity range (Re, Ra, Pr, Bi, geometry) and the temperature properties are evaluated at.
- **P4 · Compute with units.** SI throughout, kelvin for radiation and property tables, per-unit-length vs per-area vs total rates kept straight.
- **P5 · Check the answer.** Signs and directions, limiting cases, orders of magnitude (typical h, k), energy closes.
- **P6 · Reason and design.** Sketch profiles, predict what changes when a parameter changes, compare options, size a design to a constraint.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Modes and energy balances | core | 4–6% | 7 | 4 | 2 | 1 |
| 2 · The heat equation and boundary conditions | core | 6–8% | 8 | 3 | 2 | 3 |
| 3 · Steady 1-D conduction and resistance networks | core | 8–10% | 9 | 7 | 1 | 1 |
| 4 · Conduction with thermal energy generation | core | 8–10% | 8 | 8 | 0 | 0 |
| 5 · Extended surfaces | core | 6–8% | 5 | 3 | 1 | 1 |
| 6 · Two-dimensional steady conduction | core | 6–8% | 5 | 3 | 0 | 2 |
| 7 · Transient conduction | core | 10–12% | 11 | 7 | 0 | 4 |
| 8 · Convection fundamentals and external flow | core | 10–12% | 8 | 8 | 0 | 0 |
| 9 · Internal forced convection | core | 8–10% | 6 | 5 | 0 | 1 |
| 10 · Free convection | core | 6–8% | 5 | 3 | 0 | 2 |
| 11 · Thermal radiation | core | 12–14% | 11 | 10 | 0 | 1 |
| 12 · Heat exchangers and system-level thermal analysis | core | 10–12% | 7 | 4 | 0 | 3 |
| 13 · Boiling and condensation | extension | — | 3 | 3 | 0 | 0 |
| 14 · Mass transfer | extension | — | 5 | 5 | 0 | 0 |

## Unit 1 · Modes and energy balances

Big ideas: ENG, RATE

### 1.1 The three modes and their rate equations

Book: incropera-8e §1.1, §1.2 · FE: me-A, me-B, me-C, che-A, che-B, che-C

- ◐ **HT-1.1.A** Identify which modes act in a described system and write the rate law for each.
  - EK: Conduction needs a medium; convection needs fluid motion; radiation needs neither.
  - P1 · drills: ~mae-concept
- ● **HT-1.1.B** Calculate a conduction flux or rate, or an unknown k, from Fourier's law across a plane layer.
  - EK: q'' = k ΔT / L; heat flows down the temperature gradient.
  - P4 · drills: ht-cond
- ● **HT-1.1.C** Calculate a convection rate from Newton's law of cooling and judge whether h is plausible.
  - EK: q = hA(T_s − T∞); h ~ 2–25 free gas, 25–250 forced gas, 50–20 000 forced liquid, 2 500–100 000 phase change (W/m²·K).
  - P4 · P5 · drills: ht-conv
- ◐ **HT-1.1.D** Calculate net radiation between a small surface and large surroundings, and linearise it to a radiation coefficient h_r.
  - EK: q'' = εσ(T_s⁴ − T_sur⁴) in kelvin; h_r = εσ(T_s + T_sur)(T_s² + T_sur²).
  - P4 · drills: ~ht-rad

### 1.2 Energy balances on control volumes and surfaces

Book: incropera-8e §1.3 · FE: me-A, che-A

- ● **HT-1.2.A** Apply conservation of energy to a control volume: in − out + generated = stored.
  - EK: Generation is volumetric (I²R, reaction); storage is ρcV dT/dt; both vanish from a surface balance.
  - P1 · drills: ht-eb-wire
- ● **HT-1.2.B** Apply a surface energy balance linking conduction, convection and radiation at a boundary.
  - EK: A surface has no volume: what conducts in, convects and radiates out.
  - P1 · drills: ht-eb-surface
- ○ **HT-1.2.C** Find the instantaneous rate of temperature change of a body from an unsteady energy balance.
  - EK: dT/dt = (Σq_in − Σq_out + Ė_g)/(ρcV) at that instant.
  - P1 · P4

## Unit 2 · The heat equation and boundary conditions

Big ideas: FIELD, ENG

### 2.1 Fourier's law and thermal properties

Book: incropera-8e §2.1, §2.2 · FE: me-A, che-A

- ● **HT-2.1.A** Calculate heat flux (magnitude and direction) from a given temperature field.
  - EK: q'' = −k∇T; flux points from hot to cold, normal to isotherms.
  - P4 · drills: ht-he-flux
- ○ **HT-2.1.B** Use k, ρc_p and α = k/ρc_p to compare how materials conduct, store and diffuse heat.
  - EK: High k moves heat; high ρc_p stores it; α sets how fast a disturbance spreads.
  - P6

### 2.2 The heat diffusion equation

Book: incropera-8e §2.3 · FE: me-A

- ○ **HT-2.2.A** Write the heat equation in Cartesian, cylindrical or spherical coordinates and simplify it for a stated case (steady, 1-D, no generation, constant k).
  - EK: (1/r)d/dr(r dT/dr) and (1/r²)d/dr(r² dT/dr) are the radial Laplacians; each assumption strikes a term.
  - P2
- ● **HT-2.2.B** From a given T field, find the generation rate, the surface fluxes or the local rate of change ∂T/∂t.
  - EK: k∇²T + q̇ = ρc ∂T/∂t; read each term off the derivatives of T.
  - P2 · P4 · drills: ht-he-gen, ht-he-dTdt, ht-gen-poly
- ● **HT-2.2.C** Decide whether a temperature field can be a steady, generation-free solution.
  - EK: Steady, no q̇, constant k ⇒ ∇²T = 0 (Laplace).
  - P5 · drills: mae-laplace

### 2.3 Boundary and initial conditions

Book: incropera-8e §2.4 · FE: me-A

- ○ **HT-2.3.A** Translate a physical boundary into its mathematical condition: fixed temperature, fixed flux, insulated or symmetry plane, convection, radiation, perfect-contact interface.
  - EK: −k dT/dx|_s = q''_s; insulated or symmetric ⇒ dT/dx = 0; convection: −k dT/dx|_s = h(T_s − T∞); interface: T and k dT/dx continuous.
  - P2
- ◐ **HT-2.3.B** Write the complete formulation (equation + two BCs, or + IC) of a 1-D problem from a word description.
  - EK: A second-order ODE needs two independent conditions; a transient one also needs T(x, 0).
  - P1 · P2 · drills: ~mae-pot
- ◐ **HT-2.3.C** Sketch T(x) and read boundary conditions and k ratios from slopes.
  - EK: Insulated ⇒ zero slope; in series, slope ∝ 1/k; with generation the profile curves (concave down for q̇ > 0).
  - P6 · drills: ~mae-wall-compare

## Unit 3 · Steady 1-D conduction and resistance networks

Big ideas: RATE, FIELD, SYS

### 3.1 The plane wall and thermal resistance

Book: incropera-8e §3.1 · FE: me-A, che-A, che-D

- ● **HT-3.1.A** Find T(x) and q in a plane wall with fixed-temperature or convective boundaries.
  - EK: No generation ⇒ linear T(x); q is the same at every x.
  - P2 · drills: mae-wall-point
- ● **HT-3.1.B** Build a series–parallel resistance network for a composite wall and compute q, U and every interface temperature.
  - EK: R_cond = L/kA, R_conv = 1/hA; series add, parallel add as conductances; U = 1/(R_tot A).
  - P1 · P4 · drills: ht-wall, mae-series-parallel
- ● **HT-3.1.C** Include thermal contact resistance and judge when it matters.
  - EK: R''_t,c in series at the interface; matters when it rivals L/k of the layers.
  - P3 · P5 · drills: ht-contact
- ● **HT-3.1.D** Reason qualitatively about a network: same q in series, largest ΔT across the largest R, which change helps most.
  - EK: ΔT_i / ΔT_tot = R_i / R_tot.
  - P6 · drills: mae-wall-compare, ~mae-concept

### 3.2 Varying area or conductivity

Book: incropera-8e §3.2 · FE: me-A

- ○ **HT-3.2.A** Find q and T(x) when the cross-section A(x) or k(T) varies, by integrating Fourier's law with q constant.
  - EK: Steady, no q̇ ⇒ q_x constant; q ∫dx/A(x) = −∫k(T)dT.
  - P2

### 3.3 Radial systems and critical insulation

Book: incropera-8e §3.3, §3.4 · FE: me-A, che-A

- ● **HT-3.3.A** Calculate q′ and T(r) for a cylindrical wall or insulated pipe using its resistance.
  - EK: R′ = ln(r₂/r₁)/(2πk); T(r) is logarithmic.
  - P4 · drills: ht-cyl
- ● **HT-3.3.B** Calculate q for a spherical shell using its resistance.
  - EK: R = (1/r₁ − 1/r₂)/(4πk).
  - P4 · drills: ht-sphere
- ● **HT-3.3.C** Find the critical insulation radius and decide whether adding insulation raises or lowers q.
  - EK: r_cr = k/h (cylinder), 2k/h (sphere); below r_cr insulation increases q.
  - P5 · P6 · drills: ht-rcrit
- ◐ **HT-3.3.D** State which quantities stay constant with radius in steady radial conduction.
  - EK: q (or q′) is constant; q″ falls as 1/r (cylinder) or 1/r² (sphere).
  - P5 · drills: ~mae-concept

## Unit 4 · Conduction with thermal energy generation

Big ideas: ENG, FIELD

### 4.1 Plane wall with uniform generation

Book: incropera-8e §3.5.1 · FE: me-A

- ● **HT-4.1.A** Find the surface temperature from an overall energy balance before solving for the profile.
  - EK: Everything generated leaves through the cooled surfaces: q̇V = hA(T_s − T∞).
  - P1 · drills: ht-gen-wall-conv
- ● **HT-4.1.B** Solve for the parabolic T(x) and T_max with symmetric fixed-temperature or convective boundaries.
  - EK: T_max − T_s = q̇L²/2k; the midplane (or insulated face) is adiabatic.
  - P2 · drills: ht-gen-wall-fixed, ht-gen-wall-conv
- ● **HT-4.1.C** With unequal face temperatures, locate the maximum and find the flux through each face.
  - EK: x_max = k(T₂ − T₁)/(2q̇L); more heat leaves through the cooler face.
  - P2 · P5 · drills: ht-gen-wall-asym
- ● **HT-4.1.D** Analyse a generating layer bonded to non-generating layers, chaining flux, interface and maximum temperatures.
  - EK: Flux leaving the generating layer = q̇L_A and passes unchanged through the plain layers.
  - P1 · P2 · drills: ht-gen-composite

### 4.2 Radial systems with generation

Book: incropera-8e §3.5.2 · FE: me-A

- ● **HT-4.2.A** Find surface and centreline temperatures of a solid cylinder or wire with generation, including q̇ from Joule heating.
  - EK: T_s = T∞ + q̇r_o/2h; T₀ − T_s = q̇r_o²/4k; q̇ = I²ρ_e/A².
  - P1 · P4 · drills: ht-gen-rod, ht-gen-wire, ht-eb-wire
- ● **HT-4.2.B** Find surface and centre temperatures of a sphere with generation.
  - EK: T_s = T∞ + q̇r_o/3h; T₀ − T_s = q̇r_o²/6k.
  - P4 · drills: ht-gen-sphere
- ● **HT-4.2.C** Solve a hollow cylinder with generation and one insulated or convective surface.
  - EK: General T = −q̇r²/4k + C₁ ln r + C₂; apply one BC per surface.
  - P2 · drills: ht-gen-tube

### 4.3 Design limits with generation

Book: incropera-8e §3.5 · FE: me-A

- ● **HT-4.3.A** Find the largest allowable q̇, or the h or thickness needed, to keep T_max below a limit.
  - EK: T_max − T∞ = q̇L/h + q̇L²/2k: a film rise plus a conduction rise.
  - P6 · drills: ht-gen-qmax

## Unit 5 · Extended surfaces

Big ideas: FIELD, RATE, SCALE

### 5.1 The fin equation and its solutions

Book: incropera-8e §3.6.1, §3.6.2, §3.6.3 · FE: me-A

- ● **HT-5.1.A** Derive the fin equation from an energy balance on a fin element and compute m for a given geometry.
  - EK: d²θ/dx² − m²θ = 0, m² = hP/kA_c; θ = T − T∞.
  - P1 · P2 · drills: ht-fin-m
- ● **HT-5.1.B** Choose the tip condition (infinite, adiabatic, convective via corrected length) and compute fin heat rate and tip or local temperature.
  - EK: q_f = M tanh mL (adiabatic); M = √(hPkA_c)θ_b; L_c = L + D/4 for a pin.
  - P2 · P3 · drills: ht-fin-infinite, ht-fin-adiabatic, ht-fin-tip
- ◐ **HT-5.1.C** Explain why fin temperature decays exponentially rather than linearly, and how to change the decay.
  - EK: Side convection removes heat along the length; larger m (low k, high h, thin) ⇒ faster decay.
  - P6 · drills: ~mae-concept

### 5.2 Fin performance

Book: incropera-8e §3.6.4 · FE: me-A

- ● **HT-5.2.A** Calculate fin efficiency and effectiveness and decide whether a fin is worthwhile.
  - EK: η_f = q_f/(hA_fθ_b); ε_f = q_f/(hA_c,bθ_b); fins pay off when ε_f ≳ 2, i.e. high k, low h.
  - P3 · P6 · drills: ht-fin-efficiency, ~mae-concept

### 5.3 Fin arrays

Book: incropera-8e §3.6.5 · FE: me-A

- ○ **HT-5.3.A** Calculate overall surface efficiency and heat rate of a fin array and its resistance.
  - EK: η_o = 1 − (NA_f/A_t)(1 − η_f); q_t = η_o h A_t θ_b; R_t,o = 1/(η_o h A_t).
  - P4

## Unit 6 · Two-dimensional steady conduction

Big ideas: FIELD, SYS

### 6.1 Separation of variables

Book: incropera-8e §4.2

- ○ **HT-6.1.A** Set up the separable solution for a rectangle with one non-homogeneous edge and evaluate its leading terms.
  - EK: θ = Σ C_n sin(nπx/L) sinh(nπy/L)/sinh(nπW/L); homogeneous BCs set the eigenfunctions.
  - P2

### 6.2 Conduction shape factors

Book: incropera-8e §4.3 · FE: me-A

- ● **HT-6.2.A** Pick the matching shape-factor case and compute q = Sk ΔT.
  - EK: S has units of length; R = 1/Sk; check the geometric validity condition.
  - P3 · drills: ht-shape, mae-rod-slab
- ● **HT-6.2.B** Combine shape-factor resistances with other resistances in a network.
  - EK: Two buried objects ⇒ two resistances in series across T₁ − T₂.
  - P1 · P3 · drills: mae-two-spheres

### 6.3 Finite-difference equations

Book: incropera-8e §4.4, §4.5

- ● **HT-6.3.A** Write the finite-difference equation of an interior, surface or corner node by an energy balance on its cell, including Δx ≠ Δy, convection and radiation.
  - EK: Each face: conductance × (T_neighbour − T_m); boundary faces get h·ℓ or h_r·ℓ terms; half cells on edges.
  - P1 · P2 · drills: ht-fd, mae-fd
- ○ **HT-6.3.B** Solve a small node system directly or by Gauss–Seidel iteration and check the energy balance.
  - EK: Iterate T_i = (Σa_jT_j + b)/a_i until changes are below tolerance.
  - P4 · P5

## Unit 7 · Transient conduction

Big ideas: SCALE, ENG, FIELD

### 7.1 Lumped capacitance

Book: incropera-8e §5.1, §5.2, §5.3 · FE: me-D

- ● **HT-7.1.A** Compute the Biot number with L_c = V/A_s and decide whether lumped capacitance applies.
  - EK: Bi = hL_c/k < 0.1 ⇒ internal gradients negligible; L_c = r/3 sphere, r/2 cylinder, half-thickness wall.
  - P3 · drills: ht-bi
- ● **HT-7.1.B** Find temperature at a time, or the time to reach a temperature, for a lumped body.
  - EK: θ/θ_i = exp(−t/τ), τ = ρVc/hA_s.
  - P4 · drills: ht-lumped-time, ht-lumped-temp
- ● **HT-7.1.C** Find the energy transferred over an interval.
  - EK: Q = ρVcθ_i[1 − exp(−t/τ)].
  - P4 · drills: ht-lumped-energy
- ○ **HT-7.1.D** Set up and solve a general lumped balance with radiation, surface flux or generation.
  - EK: ρVc dT/dt = q''_sA − hA(T − T∞) − εσA(T⁴ − T_sur⁴) + Ė_g; solve or integrate numerically.
  - P1 · P2

### 7.2 Spatial effects — one-term solutions

Book: incropera-8e §5.4, §5.5, §5.6 · FE: me-D

- ● **HT-7.2.A** Compute Bi and Fo and find the centre temperature of a wall, cylinder or sphere with the one-term approximation.
  - EK: θ₀* = C₁exp(−ζ₁²Fo), valid for Fo > 0.2; ζ₁, C₁ from Bi (wall uses half-thickness).
  - P3 · P4 · drills: ht-ot-wall-center, ht-ot-cyl-center, ht-ot-sphere-center
- ● **HT-7.2.B** Find the temperature at another position, or the time to reach a temperature.
  - EK: θ* = θ₀* cos(ζ₁x*) (wall), θ₀* J₀(ζ₁r*) (cylinder), θ₀* sin(ζ₁r*)/(ζ₁r*) (sphere).
  - P4 · drills: ht-ot-wall-surface, ht-ot-wall-time
- ○ **HT-7.2.C** Find the fraction of the maximum energy transferred, Q/Q₀.
  - EK: Wall: Q/Q₀ = 1 − (sin ζ₁/ζ₁)θ₀*; cylinder and sphere have their own forms.
  - P4

### 7.3 The semi-infinite solid

Book: incropera-8e §5.7 · FE: me-D

- ● **HT-7.3.A** Find temperature at a depth and time, the depth reached, or the time needed, after a sudden surface temperature change.
  - EK: (T − T_s)/(T_i − T_s) = erf(x/2√(αt)); valid while the far side hasn't felt it.
  - P3 · P4 · drills: ht-erf-temp, ht-erf-depth, ht-erf-time
- ● **HT-7.3.B** Find the surface heat flux, and the contact temperature when two semi-infinite solids touch.
  - EK: q''_s = k(T_s − T_i)/√(παt); T_s = (√(kρc)_A T_A + √(kρc)_B T_B)/(√(kρc)_A + √(kρc)_B).
  - P4 · P6 · drills: ht-erf-flux, ht-erf-contact

### 7.4 Multidimensional transient effects

Book: incropera-8e §5.8

- ○ **HT-7.4.A** Build a 2-D or 3-D transient solution as a product of 1-D solutions.
  - EK: Short cylinder = infinite cylinder × plane wall, each in dimensionless θ*.
  - P2 · P3

### 7.5 Finite-difference transient methods

Book: incropera-8e §5.10

- ○ **HT-7.5.A** Write the explicit finite-difference equation for a transient node and check its stability limit.
  - EK: T_m^{p+1} = Fo(T_{m+1}^p + T_{m−1}^p) + (1 − 2Fo)T_m^p; stable if Fo ≤ 1/2 (interior, 1-D).
  - P2 · P5

## Unit 8 · Convection fundamentals and external flow

Big ideas: SCALE, RATE

### 8.1 Boundary layers and dimensionless groups

Book: incropera-8e §6.1, §6.2, §6.3, §6.5, §6.6, §6.7 · FE: me-B, che-B, che-D

- ● **HT-8.1.A** Compute Re, Pr and Nu and identify laminar, transitional or turbulent flow.
  - EK: Re_x = u∞x/ν (transition ≈ 5×10⁵ on a plate); Pr = ν/α; Nu = hL/k_f.
  - P3 · P4 · drills: ht3-bl-groups, ht3-bl-transition
- ● **HT-8.1.B** Relate local and average convection coefficients.
  - EK: h̄ = (1/L)∫h_x dx; laminar h_x ∝ x^(−1/2) ⇒ h̄ = 2h_x(L).
  - P4 · drills: ht3-bl-average
- ● **HT-8.1.C** Estimate velocity and thermal boundary-layer thicknesses and how Pr relates them.
  - EK: δ ≈ 5x/√Re_x; δ/δ_t ≈ Pr^(1/3).
  - P4 · P6 · drills: ht3-bl-thickness
- ● **HT-8.1.D** Use the Reynolds–Colburn analogy to get h from friction (or friction from h).
  - EK: C_f/2 = St Pr^(2/3).
  - P3 · drills: ht3-bl-colburn

### 8.2 The flat plate in parallel flow

Book: incropera-8e §7.1, §7.2, §7.3 · FE: me-B, che-B

- ● **HT-8.2.A** Calculate average h and q for laminar flow over a flat plate, with properties at the film temperature.
  - EK: Nu̅ = 0.664 Re_L^(1/2) Pr^(1/3); T_f = (T_s + T∞)/2.
  - P3 · P4 · drills: ht-plate-lam
- ● **HT-8.2.B** Calculate average h for a mixed laminar–turbulent boundary layer.
  - EK: Nu̅ = (0.037 Re_L^(4/5) − 871) Pr^(1/3) for Re_x,c = 5×10⁵.
  - P3 · P4 · drills: ht-plate-mixed

### 8.3 Cylinders and spheres in cross flow

Book: incropera-8e §7.4, §7.5 · FE: me-B, che-B

- ● **HT-8.3.A** Calculate h and q for a cylinder or sphere in cross flow with the appropriate correlation.
  - EK: Churchill–Bernstein (cylinder, Re Pr > 0.2); Whitaker (sphere, μ ratio).
  - P3 · P4 · drills: ht-cyl-cb, ht-sphere-whitaker

### 8.4 Flow across tube banks

Book: incropera-8e §7.6 · FE: che-E

- ● **HT-8.4.A** Find the maximum velocity, average h and outlet temperature for flow across a tube bank.
  - EK: V_max from the minimum free area (aligned vs staggered); Žukauskas Nu̅ with row correction; log-mean ΔT across the bank.
  - P3 · P4 · drills: ht3-tb-vmax, ht3-tb-zukauskas, ht3-tb-outlet

## Unit 9 · Internal forced convection

Big ideas: SCALE, ENG

### 9.1 Flow conditions and entry lengths

Book: incropera-8e §8.1, §8.2 · FE: me-B, che-B

- ● **HT-9.1.A** Compute Re_D from ṁ and decide whether the flow is laminar and how long the entry regions are.
  - EK: Re_D = 4ṁ/(πDμ); laminar below ≈ 2300; x_fd,h ≈ 0.05 Re_D D; x_fd,t ≈ 0.05 Re_D Pr D.
  - P3 · P4 · drills: ht-int-re

### 9.2 The mean temperature energy balance

Book: incropera-8e §8.3 · FE: me-B, che-B

- ● **HT-9.2.A** Find outlet temperature or required length with uniform wall heat flux.
  - EK: q = ṁc_p(T_m,o − T_m,i) = q''_s πDL; T_m rises linearly.
  - P1 · P4 · drills: ht-tm-flux
- ● **HT-9.2.B** Find outlet temperature or heat rate with uniform wall temperature, using the log-mean temperature difference.
  - EK: ΔT_o/ΔT_i = exp(−PL h̄/ṁc_p); q = h̄A_s ΔT_lm.
  - P1 · P4 · drills: ht-tm-ts

### 9.3 Convection correlations for tubes

Book: incropera-8e §8.4, §8.5 · FE: me-B, che-B, che-D

- ● **HT-9.3.A** Use the fully developed laminar results for constant flux or constant wall temperature.
  - EK: Nu_D = 4.36 (uniform q''_s), 3.66 (uniform T_s).
  - P3 · drills: ht-lam-fd
- ● **HT-9.3.B** Calculate h for turbulent flow with Dittus–Boelter (or Gnielinski), choosing the right exponent and property temperature.
  - EK: Nu_D = 0.023 Re^(4/5) Pr^n, n = 0.4 heating, 0.3 cooling; properties at mean T_m.
  - P3 · P4 · drills: ht-dittus

### 9.4 Noncircular tubes and annuli

Book: incropera-8e §8.6 · FE: che-B

- ○ **HT-9.4.A** Use the hydraulic diameter and annulus results for noncircular passages.
  - EK: D_h = 4A_c/P; laminar Nu depends on shape; annulus uses D_o − D_i.
  - P3

## Unit 10 · Free convection

Big ideas: SCALE

### 10.1 Buoyancy-driven flow and when it matters

Book: incropera-8e §9.1, §9.2, §9.3, §9.4, §9.5 · FE: me-B, che-B

- ● **HT-10.1.A** Compute Gr and Ra and identify laminar or turbulent free convection.
  - EK: Ra_L = gβΔT L³/(να); β = 1/T_f for an ideal gas; transition near Ra ≈ 10⁹ on a vertical plate.
  - P3 · P4 · drills: ht-ra
- ○ **HT-10.1.B** Decide whether free, forced or mixed convection governs.
  - EK: Gr/Re² ≪ 1 forced, ≫ 1 free, ~1 mixed.
  - P3

### 10.2 Correlations for external free convection

Book: incropera-8e §9.6 · FE: me-B, che-B

- ● **HT-10.2.A** Calculate h for a vertical plate with the Churchill–Chu correlation.
  - EK: Nu̅_L = {0.825 + 0.387Ra^(1/6)/[1 + (0.492/Pr)^(9/16)]^(8/27)}².
  - P3 · P4 · drills: ht-chu-vertical
- ● **HT-10.2.B** Calculate h for horizontal plates (hot side up or down) and horizontal cylinders and spheres.
  - EK: L = A_s/P for horizontal plates; separate correlations for upper/lower surfaces.
  - P3 · P4 · drills: ht-free-horiz, ht-free-cyl

### 10.3 Enclosures and mixed convection

Book: incropera-8e §9.8, §9.9

- ○ **HT-10.3.A** Calculate heat transfer across a vertical or horizontal enclosure (e.g. double-pane window).
  - EK: Ra_L across the gap; Nu = 1 means pure conduction below the critical Ra.
  - P3 · P4

## Unit 11 · Thermal radiation

Big ideas: RATE, SYS

### 11.1 Blackbody radiation and surface properties

Book: incropera-8e §12.1, §12.2, §12.3, §12.4, §12.5, §12.6, §12.7, §12.8 · FE: me-C, che-C

- ● **HT-11.1.A** Use Stefan–Boltzmann and Wien's law to relate emissive power, peak wavelength and temperature.
  - EK: E_b = σT⁴; λ_max T = 2898 μm·K.
  - P4 · drills: ht3-wien, ht3-stefan
- ● **HT-11.1.B** Find the fraction of blackbody emission in a wavelength band.
  - EK: F(0→λ) from λT (Table 12.2); band = difference of two fractions.
  - P3 · P4 · drills: ht3-band
- ● **HT-11.1.C** Find total emissivity or absorptivity from spectral data and apply Kirchhoff's law and the gray-surface assumption.
  - EK: α = ∫α_λG_λdλ / G; ε = α only for a gray or diffuse-gray surface at the same T.
  - P3 · drills: ht3-spectral
- ● **HT-11.1.D** Solve a surface energy balance with irradiation, emission and convection for a steady surface temperature.
  - EK: αG = εσT⁴ (+ h(T − T∞)) at steady state.
  - P1 · drills: ht3-rad-balance

### 11.2 View factors

Book: incropera-8e §13.1 · FE: me-C, che-C

- ● **HT-11.2.A** Find view factors with reciprocity, summation and symmetry, including long ducts and cavities.
  - EK: A_iF_ij = A_jF_ji; Σ_j F_ij = 1; flat or convex surfaces have F_ii = 0.
  - P3 · drills: ht-vf-reciprocity, ht-vf-duct, ht-vf-cavity
- ● **HT-11.2.B** Evaluate view factors for standard geometries from formulas or charts.
  - EK: Concentric cylinders/spheres: F₁₂ = 1; coaxial disks, aligned rectangles from Tables 13.1–13.2.
  - P3 · drills: ht-vf-concentric

### 11.3 Radiation exchange between surfaces

Book: incropera-8e §13.2, §13.3 · FE: me-C, che-C

- ● **HT-11.3.A** Calculate net exchange between black surfaces.
  - EK: q_ij = A_iF_ijσ(T_i⁴ − T_j⁴).
  - P4 · drills: ht-black-disks
- ● **HT-11.3.B** Calculate net exchange in a two-surface gray enclosure (parallel plates, concentric cylinders or spheres).
  - EK: q = σ(T₁⁴ − T₂⁴)/[(1−ε₁)/ε₁A₁ + 1/A₁F₁₂ + (1−ε₂)/ε₂A₂].
  - P1 · P4 · drills: ht-two-surface
- ● **HT-11.3.C** Quantify the effect of radiation shields.
  - EK: Each shield adds two surface resistances and one space resistance in series.
  - P6 · drills: ht-shield
- ● **HT-11.3.D** Solve a three-surface enclosure with a reradiating (adiabatic) surface by the radiosity network.
  - EK: Reradiating: J = E_b at that surface, net q = 0.
  - P1 · P4 · drills: ht-reradiating

### 11.4 Multimode heat transfer with radiation

Book: incropera-8e §13.4 · FE: me-C

- ○ **HT-11.4.A** Combine radiation exchange with conduction and convection at a surface or in an enclosure.
  - EK: Radiation and convection from one surface act in parallel; h_r lets radiation join the resistance network.
  - P1 · P3

## Unit 12 · Heat exchangers and system-level thermal analysis

Big ideas: SYS, ENG, RATE

### 12.1 The overall heat transfer coefficient

Book: incropera-8e §11.1, §11.2 · FE: me-E, che-D, che-E

- ○ **HT-12.1.A** Calculate U for a tube wall including both films, fouling and finned surfaces.
  - EK: 1/UA = 1/(η_o hA)_c + R''_f,c/(η_oA)_c + R_w + R''_f,h/(η_oA)_h + 1/(η_o hA)_h.
  - P1 · P4

### 12.2 The log-mean temperature difference method

Book: incropera-8e §11.3 · FE: me-E, che-E

- ● **HT-12.2.A** Size a parallel-flow or counterflow exchanger with q = UA ΔT_lm when all inlet and outlet temperatures are known.
  - EK: ΔT_lm = (ΔT₁ − ΔT₂)/ln(ΔT₁/ΔT₂), end differences defined by flow arrangement; counterflow needs less area.
  - P3 · P4 · drills: ht-lmtd-counter, ht-lmtd-parallel
- ● **HT-12.2.B** Apply the LMTD correction factor for shell-and-tube and cross-flow exchangers.
  - EK: q = UAF ΔT_lm,CF with F from P and R charts.
  - P3 · drills: ht-shell-tube

### 12.3 The effectiveness–NTU method

Book: incropera-8e §11.4, §11.5 · FE: me-E, che-E

- ● **HT-12.3.A** Find effectiveness and heat rate from NTU and C_r.
  - EK: NTU = UA/C_min; C_r = C_min/C_max; ε from the arrangement's relation; q = εC_min(T_h,i − T_c,i).
  - P3 · P4 · drills: ht-ntu-eff
- ● **HT-12.3.B** Predict outlet temperatures of an existing exchanger when they are unknown.
  - EK: ε–NTU avoids iteration when outlets are unknown; then energy balances give each outlet.
  - P3 · P4 · drills: ht-ntu-outlet

### 12.4 System-level thermal networks

Book: incropera-8e §1.3, §3.1, §13.4 · FE: me-A, me-B, me-C

- ○ **HT-12.4.A** Model a device (electronics package, building wall, pipe run) as a network of conduction, convection and radiation resistances and find its operating temperature.
  - EK: One energy balance per node; parallel paths from a surface (convection ∥ radiation); iterate when h_r depends on T.
  - P1 · P2 · P4
- ○ **HT-12.4.B** Identify the controlling resistance and choose the design change that best meets a temperature limit.
  - EK: Reduce the largest R first; compare options by their effect on R_tot.
  - P6

## Unit 13 · Boiling and condensation (extension)

Big ideas: SCALE, RATE

### 13.1 Boiling

Book: incropera-8e §10.1, §10.2, §10.3, §10.4 · FE: che-B, che-D

- ● **HT-13.1.A** Identify the boiling regime from the excess temperature on the boiling curve.
  - EK: Free convection → nucleate → transition → film; CHF at the nucleate peak.
  - P3 · drills: ht3-boil-regime
- ● **HT-13.1.B** Calculate nucleate boiling flux (Rohsenow) and critical heat flux.
  - EK: q''_s ∝ ΔT_e³; q''_max = 0.149 h_fg ρ_v [σg(ρ_l − ρ_v)/ρ_v²]^(1/4).
  - P3 · P4 · drills: ht3-rohsenow, ht3-chf

### 13.2 Film condensation

Book: incropera-8e §10.6, §10.7, §10.8 · FE: che-B, che-D

- ● **HT-13.2.A** Calculate film condensation on a vertical plate or horizontal tube.
  - EK: Nusselt analysis with h′_fg = h_fg(1 + 0.68 Ja); tube constant 0.729.
  - P3 · P4 · drills: ht3-cond-plate, ht3-cond-tube

## Unit 14 · Mass transfer (extension)

Big ideas: RATE, SCALE

### 14.1 Diffusion

Book: incropera-8e §14.1, §14.2, §14.3, §14.4, §14.5, §14.6

- ● **HT-14.1.A** Calculate a diffusive flux in a stationary medium with Fick's law, including membranes and solubility.
  - EK: N_A = −D_AB dC_A/dx; at an interface C = S·p.
  - P4 · drills: ht3-fick, ht3-membrane
- ● **HT-14.1.B** Calculate evaporation through a stagnant gas column (Stefan flow).
  - EK: N_A = (CD_AB/L) ln[(1 − x_A,L)/(1 − x_A,0)].
  - P2 · P4 · drills: ht3-stefan-flow
- ● **HT-14.1.C** Solve diffusion with a homogeneous reaction.
  - EK: D d²C/dx² − k₁C = 0 ⇒ cosh/sinh profile, like a fin.
  - P2 · drills: ht3-reaction

### 14.2 Convective mass transfer and the analogy

Book: incropera-8e §6.7, §7.8

- ● **HT-14.2.A** Use the heat–mass analogy to convert between h and h_m, and Nu and Sh correlations.
  - EK: h/h_m = ρc_p Le^(2/3); Sh = f(Re, Sc) mirrors Nu = f(Re, Pr).
  - P3 · drills: ht3-mc-analogy, ht3-mc-sherwood
- ● **HT-14.2.B** Solve a coupled heat and mass balance at an evaporating surface (wet bulb).
  - EK: h(T∞ − T_s) = h_m h_fg(ρ_A,s − ρ_A,∞).
  - P1 · P4 · drills: ht3-mc-evap
