# Thermodynamics and Statistical Mechanics — curriculum framework (draft 1)

Generated from `drills/frameworks/thermodynamics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**124 learning objectives** in 17 units (108 core): 81 drilled, 5 partly, 38 with no drills. Core: 70 / 108 drilled.

## Big ideas

- **EQ · Equilibrium is an extremum under constraints.** An isolated system maximises its entropy; a system coupled to a bath minimises the matching free energy. Every equilibrium condition — equal T, P, μ; K; coexistence — is that extremum written out.
- **FUND · One fundamental equation holds everything.** S(U,V,N) or U(S,V,N) contains all equilibrium information; F, H, G and Ω are the same information re-expressed in the variables a lab controls, by Legendre transform.
- **MEAS · Calculus turns the unmeasurable into the measurable.** Maxwell relations and derivative identities rewrite entropy and chemical-potential changes in terms of P–V–T data, heat capacities, α and κ_T.
- **STAB · Stability is curvature.** Concave entropy (convex energy) means positive heat capacities and compressibilities; where curvature fails, a single phase splits and phase transitions, spinodals and critical points appear.
- **MU · Chemical potential moves matter.** Matter flows from high to low μ between phases, across membranes, into solution and through reactions; nonideality enters only through fugacity and activity.
- **MICRO · Macroscopic properties are Boltzmann-weighted averages.** Count microstates, weight them by e^(−βE), sum into a partition function; its logarithm is a free energy, its derivatives are U, S, P, μ, and its second derivatives are fluctuations.

## Practices

- **P1 · Define the system and constraints.** Say what is isolated, what exchanges energy, volume or particles with a bath, and which variables are held fixed.
- **P2 · Pick the potential or ensemble.** Match the controlled variables to the potential that is extremised (S, F, G, Ω) and to the ensemble (microcanonical, canonical, grand, isobaric).
- **P3 · Manipulate derivatives.** Use exact differentials, Legendre transforms, Maxwell relations, the triple-product and chain rules to reach a derivative you can evaluate.
- **P4 · Build a molecular model.** Count states, choose a lattice, two-level, oscillator, rotor or ideal-gas model, and assemble the partition function from independent pieces.
- **P5 · Compute with units.** R vs k_B, per mole vs per molecule, kelvin, wavenumbers to energy, standard states for K, fugacity and activity.
- **P6 · Check and reason.** Signs, limiting cases (T → 0, T → ∞, ideal limit, large N), stability, and which way a change pushes equilibrium.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Probability and counting states | core | 3–5% | 7 | 5 | 1 | 1 |
| 2 · Entropy, equilibrium and the fundamental equation | core | 8–10% | 12 | 9 | 0 | 3 |
| 3 · The first law and reversibility | core | 5–7% | 7 | 4 | 0 | 3 |
| 4 · Legendre transforms and thermodynamic potentials | core | 8–10% | 7 | 4 | 2 | 1 |
| 5 · Maxwell relations and measurable properties | core | 7–9% | 6 | 4 | 0 | 2 |
| 6 · Stability and metastability | core | 6–8% | 7 | 5 | 1 | 1 |
| 7 · Gases and equations of state | core | 7–9% | 5 | 0 | 1 | 4 |
| 8 · Phase equilibrium of pure substances | core | 6–8% | 6 | 4 | 0 | 2 |
| 9 · Solutions and mixtures | core | 12–14% | 12 | 5 | 0 | 7 |
| 10 · Chemical reaction equilibria | core | 8–10% | 7 | 5 | 0 | 2 |
| 11 · The Boltzmann distribution and the canonical ensemble | core | 8–10% | 8 | 7 | 0 | 1 |
| 12 · Molecular models of gases and solids | core | 10–12% | 15 | 10 | 0 | 5 |
| 13 · Fluctuations | core | 4–6% | 4 | 4 | 0 | 0 |
| 14 · Other ensembles | core | 5–7% | 5 | 4 | 0 | 1 |
| 15 · Binding, adsorption and cooperativity | extension | — | 7 | 6 | 0 | 1 |
| 16 · Reaction rates and transition states | extension | — | 6 | 5 | 0 | 1 |
| 17 · Electrolytes, polymers and simulation | extension | — | 3 | 0 | 0 | 3 |

## Unit 1 · Probability and counting states

Big ideas: MICRO

### 1.1 Counting arrangements

Book: dill-bromberg-2e §1; shell-2015 §2.5

- ● **TD-1.1.A** Count ordered selections of distinguishable objects (permutations).
  - EK: N!/(N − k)! ordered ways to fill k slots from N.
  - P4 · drills: sm-perm
- ● **TD-1.1.B** Count arrangements of indistinguishable particles on distinguishable sites.
  - EK: C(M, N) = M!/(N!(M − N)!) — the lattice-gas multiplicity.
  - P4 · drills: sm-comb
- ● **TD-1.1.C** Count distinct sequences of a multiset (multinomial coefficient).
  - EK: N!/(n_A! n_B! …); identical units are not reordered.
  - P4 · drills: sm-anagram
- ○ **TD-1.1.D** Apply Stirling's approximation to ln W for large N.
  - EK: ln N! ≈ N ln N − N; turns ln C(M, N) into −M Σ x ln x.
  - P4 · P6

### 1.2 Probability distributions

Book: dill-bromberg-2e §1; shell-2015 §2.5, §4.1

- ● **TD-1.2.A** Calculate the probability of exactly k outcomes in N independent two-outcome trials.
  - EK: P(k) = C(N, k) p^k (1 − p)^(N − k).
  - P4 · drills: sm-binom
- ● **TD-1.2.B** Calculate an 'at least one' probability through the complement.
  - EK: P(≥ 1) = 1 − (1 − p)^N for independent events.
  - P4 · P6 · drills: sm-atleast
- ◐ **TD-1.2.C** Calculate the mean and variance of a discrete distribution.
  - EK: ⟨x⟩ = Σ p_i x_i; σ² = ⟨x²⟩ − ⟨x⟩².
  - P5 · drills: ~sm-fl-exact

## Unit 2 · Entropy, equilibrium and the fundamental equation

Big ideas: EQ, MICRO, FUND

### 2.1 Multiplicity and S = k ln W

Book: dill-bromberg-2e §2, §5; shell-2015 §2.3, §3.6, §3.7, §4.2

- ● **TD-2.1.A** Calculate the multiplicity of a system of independent two-state units with a given number excited.
  - EK: W = N!/(n!(N − n)!); S = k_B ln W.
  - Needs: TD-1.1.B
  - P4 · drills: sm-two-state
- ● **TD-2.1.B** Calculate the multiplicity of an Einstein solid with N oscillators and q quanta.
  - EK: W = (q + N − 1)!/(q!(N − 1)!).
  - P4 · drills: sm-einstein-w
- ● **TD-2.1.C** Calculate ΔS from the change in multiplicity of a lattice or spin system.
  - EK: ΔS = k_B ln(W₂/W₁).
  - P4 · P5 · drills: sm-ds-two-state
- ● **TD-2.1.D** Derive the entropy of isothermal ideal-gas expansion by lattice counting.
  - EK: W ∝ M^N, M ∝ V ⇒ ΔS = nR ln(V₂/V₁).
  - P4 · P5 · drills: sm-ds-volume

### 2.2 Equilibrium as maximum entropy

Book: dill-bromberg-2e §2, §6; shell-2015 §4.4, §4.5, §4.6, §4.7

- ● **TD-2.2.A** Calculate the probability of each energy split between two solids in thermal contact and identify the most probable one.
  - EK: P(q_A) ∝ W_A(q_A) W_B(q − q_A); the peak sharpens as N grows.
  - P1 · P4 · drills: sm-einstein-share
- ○ **TD-2.2.B** Derive equality of T, P and μ by maximising total entropy over exchange of U, V and N.
  - EK: ∂S/∂U = 1/T, ∂S/∂V = P/T, ∂S/∂N = −μ/T must match across the wall.
  - P1 · P3
- ○ **TD-2.2.C** Show that maximum entropy at fixed U is equivalent to minimum energy at fixed S.
  - EK: Internal constraints released ⇒ S rises (second law); the energy-minimum principle is its inverse.
  - P3

### 2.3 The fundamental equation and its integrated forms

Book: dill-bromberg-2e §6, §7; shell-2015 §5.1, §5.2, §5.3

- ● **TD-2.3.A** Find T, P or μ as derivatives of a given S(U, V, N).
  - EK: dS = (1/T)dU + (P/T)dV − (μ/T)dN.
  - P3 · drills: th-fe-entropy-rep, th-fe-ideal
- ● **TD-2.3.B** Find T, P or μ as derivatives of a given U(S, V, N).
  - EK: dU = T dS − P dV + μ dN.
  - P3 · drills: th-fe-energy-rep
- ○ **TD-2.3.C** Check that a proposed fundamental equation is extensive (first-order homogeneous).
  - EK: S(λU, λV, λN) = λS(U, V, N); exponents of extensive variables sum to 1.
  - P6
- ● **TD-2.3.D** Calculate U, or any one term, from the Euler relation.
  - EK: U = TS − PV + μN; equivalently G = μN for one component.
  - P5 · drills: th-fe-euler
- ● **TD-2.3.E** Apply the Gibbs–Duhem equation to relate changes in the intensive variables.
  - EK: S dT − V dP + N dμ = 0; at fixed T, dμ = v dP.
  - P3 · P5 · drills: th-fe-gibbs-duhem

## Unit 3 · The first law and reversibility

Big ideas: EQ, FUND

### 3.1 Work and heat on reversible paths

Book: dill-bromberg-2e §3; shell-2015 §6.1, §6.2, §6.3, §6.4

- ● **TD-3.1.A** Calculate q, w and ΔU for a reversible isothermal ideal-gas process.
  - EK: ΔU = 0; w = −nRT ln(V₂/V₁) = −q.
  - P5 · drills: th-fl-isothermal
- ● **TD-3.1.B** Calculate q, w and ΔU for a reversible isobaric ideal-gas process.
  - EK: w = −PΔV = −nRΔT; q = nC_pΔT.
  - P5 · drills: th-fl-isobaric
- ● **TD-3.1.C** Calculate q, w and ΔU for a constant-volume ideal-gas process.
  - EK: w = 0; q = ΔU = nC_vΔT.
  - P5 · drills: th-fl-isochoric
- ● **TD-3.1.D** Find the final state of a reversible adiabatic ideal-gas process.
  - EK: TV^(γ−1) constant; C_v = 3R/2 monatomic, 5R/2 diatomic (no vibration).
  - P5 · drills: th-fl-adiabatic

### 3.2 Baths, irreversibility and heat engines

Book: shell-2015 §6.5, §6.6, §6.7

- ○ **TD-3.2.A** Calculate the total entropy change of system plus bath for an irreversible process and decide whether it can occur.
  - EK: ΔS_bath = −q/T_bath; ΔS_tot ≥ 0, equal only when reversible.
  - P1 · P6
- ○ **TD-3.2.B** Calculate the maximum efficiency or coefficient of performance of a cycle between two reservoirs.
  - EK: η_max = 1 − T_C/T_H from ΔS_tot = 0.
  - P5

### 3.3 Open steady-flow systems

Book: shell-2015 §6.8

- ○ **TD-3.3.A** Apply steady-flow energy and entropy balances to a turbine, compressor, nozzle or throttle.
  - EK: Δh = q + w_s per unit mass; throttling is isenthalpic; Δs ≥ q/T.
  - P1 · P5

## Unit 4 · Legendre transforms and thermodynamic potentials

Big ideas: FUND, EQ

### 4.1 Multivariable calculus tools

Book: dill-bromberg-2e §4; shell-2015 §8.3

- ○ **TD-4.1.A** Test whether a differential is exact (a state function) by equality of cross-derivatives.
  - EK: M dx + N dy exact ⇔ ∂M/∂y = ∂N/∂x; δq and δw are not exact.
  - P3
- ◐ **TD-4.1.B** Apply the triple-product and chain rules to rewrite a partial derivative.
  - EK: (∂x/∂y)_z (∂y/∂z)_x (∂z/∂x)_y = −1.
  - P3 · drills: ~th-mx-triple

### 4.2 Potentials and natural variables

Book: dill-bromberg-2e §8; shell-2015 §7.1, §7.2, §7.3, §7.4, §7.5, §7.6, §7.9

- ● **TD-4.2.A** Construct F, H or G from a given U(S, V, N) by Legendre transform.
  - EK: F = U − TS; eliminate S using T = ∂U/∂S. H = U + PV; G = U − TS + PV.
  - Needs: TD-2.3.B
  - P3 · drills: th-lg-helmholtz, th-lg-enthalpy
- ● **TD-4.2.B** State the natural variables and differential of any potential, including the grand potential.
  - EK: dF = −S dT − P dV + μ dN; dG = −S dT + V dP + μ dN; dΩ = −S dT − P dV − N dμ.
  - P2 · drills: th-lg-natural
- ◐ **TD-4.2.C** Choose the potential minimised at equilibrium for given bath conditions.
  - EK: T, V, N → F; T, P, N → G; T, V, μ → Ω; S, P, N → H.
  - P1 · P2 · drills: ~th-lg-natural

### 4.3 Derivative and integrated relations

Book: dill-bromberg-2e §8; shell-2015 §7.10, §7.11

- ● **TD-4.3.A** Derive P, S, μ or U from a given F(T, V, N) or G(T, P, N).
  - EK: P = −(∂F/∂V)_T, S = −(∂F/∂T)_V, μ = (∂F/∂N)_{T,V}.
  - P3 · drills: th-lg-derive
- ● **TD-4.3.B** Use the Gibbs–Helmholtz relation to get S or H from G(T).
  - EK: S = −(∂G/∂T)_P; H = −T²[∂(G/T)/∂T]_P.
  - P3 · P5 · drills: th-lg-gibbs-helmholtz

## Unit 5 · Maxwell relations and measurable properties

Big ideas: MEAS, FUND

### 5.1 Maxwell relations

Book: dill-bromberg-2e §9; shell-2015 §8.1

- ● **TD-5.1.A** Identify the Maxwell relation that equals a given partial derivative.
  - EK: Cross-derivatives of the potential whose natural variables are the two held fixed: (∂S/∂V)_T = (∂P/∂T)_V from F.
  - Needs: TD-4.2.B
  - P3 · drills: th-mx-pick
- ● **TD-5.1.B** Evaluate an entropy derivative from an equation of state through a Maxwell relation.
  - EK: (∂S/∂V)_T = (∂P/∂T)_V; (∂S/∂P)_T = −(∂V/∂T)_P.
  - P3 · drills: th-mx-eos

### 5.2 Measurable properties

Book: dill-bromberg-2e §9; shell-2015 §8.2, §8.3

- ● **TD-5.2.A** Express a thermodynamic derivative in terms of α, κ_T and c_p and evaluate it.
  - EK: α = (1/V)(∂V/∂T)_P, κ_T = −(1/V)(∂V/∂P)_T; (∂P/∂T)_V = α/κ_T.
  - P3 · P5 · drills: th-mx-measurable
- ● **TD-5.2.B** Estimate the pressure rise when a liquid is heated at constant volume.
  - EK: ΔP ≈ (α/κ_T) ΔT — large for liquids (tens of bar per K).
  - P5 · P6 · drills: th-mx-triple
- ○ **TD-5.2.C** Derive and evaluate c_p − c_v from α and κ_T.
  - EK: c_p − c_v = Tvα²/κ_T; = R for an ideal gas.
  - P3 · P5
- ○ **TD-5.2.D** Derive (∂U/∂V)_T or the Joule–Thomson coefficient for a real gas from its equation of state.
  - EK: (∂U/∂V)_T = T(∂P/∂T)_V − P; μ_JT = (v/c_p)(Tα − 1).
  - P3

## Unit 6 · Stability and metastability

Big ideas: STAB, EQ

### 6.1 Stability criteria

Book: dill-bromberg-2e §25; shell-2015 §11.4

- ● **TD-6.1.A** Decide whether a fundamental equation is stable from the concavity of S(U, V).
  - EK: ∂²S/∂U² ≤ 0, ∂²S/∂V² ≤ 0, and the Hessian determinant ≥ 0.
  - P3 · P6 · drills: th-st-concavity
- ● **TD-6.1.B** Derive C_V from a fundamental equation and check that it is positive.
  - EK: C_V = (∂U/∂T)_V = −(∂S/∂U)²/(∂²S/∂U²) > 0 for stability.
  - P3 · drills: th-st-cv
- ● **TD-6.1.C** Test whether a homogeneous van der Waals state is mechanically stable.
  - EK: Stable ⇔ (∂P/∂V)_T < 0 ⇔ κ_T > 0.
  - P5 · P6 · drills: th-st-vdw-stable
- ● **TD-6.1.D** Calculate κ_T of a fluid from its equation of state.
  - EK: κ_T = −1/[V(∂P/∂V)_T]; for vdW (∂P/∂V)_T = −RT/(V − b)² + 2a/V³.
  - P3 · P5 · drills: th-st-vdw-kappa

### 6.2 Spinodals and the critical point

Book: dill-bromberg-2e §25; shell-2015 §11.1, §11.3

- ● **TD-6.2.A** Find the critical constants of a cubic equation of state.
  - EK: (∂P/∂V)_T = (∂²P/∂V²)_T = 0; vdW: T_c = 8a/27Rb, V_c = 3b, P_c = a/27b².
  - P3 · P5 · drills: th-st-vdw-tc
- ◐ **TD-6.2.B** Locate the spinodal and classify a state as stable, metastable or unstable.
  - EK: Spinodal: (∂P/∂V)_T = 0; between binodal and spinodal the state is metastable.
  - P6 · drills: ~th-st-vdw-stable

### 6.3 Common-tangent and equal-area constructions

Book: shell-2015 §11.2, §10.5

- ○ **TD-6.3.A** Find coexisting states by a common tangent on G or F, or Maxwell's equal-area rule on a vdW isotherm.
  - EK: Equal μ and P in both phases ⇔ common tangent ⇔ ∫P dV over the loop = P_sat ΔV.
  - P2 · P3

## Unit 7 · Gases and equations of state

Big ideas: FUND, MU, MEAS

### 7.1 Ideal gases and ideal-gas mixtures

Book: dill-bromberg-2e §11; shell-2015 §9.2, §9.3

- ◐ **TD-7.1.A** Write μ(T, P) for a pure ideal gas and for a component of an ideal-gas mixture and calculate Δμ.
  - EK: μ = μ°(T) + RT ln(P/P°); in a mixture replace P by p_i = y_iP.
  - P5 · drills: ~th-fe-gibbs-duhem

### 7.2 Nonideal gases

Book: dill-bromberg-2e §24; shell-2015 §9.4, §9.5

- ○ **TD-7.2.A** Calculate Z and residual (departure) properties from a virial or cubic equation of state.
  - EK: Z = PV/RT = 1 + B/V + …; h − h^ig = ∫[T(∂P/∂T)_V − P]dV + RT(Z − 1).
  - P3 · P5
- ○ **TD-7.2.B** Calculate a fugacity coefficient from a virial or cubic equation of state.
  - EK: ln φ = ∫₀^P (Z − 1) dP/P; truncated virial: ln φ = BP/RT.
  - P3 · P5
- ○ **TD-7.2.C** Relate the second virial coefficient to the intermolecular pair potential.
  - EK: B(T) = −2πN_A ∫(e^(−βu(r)) − 1) r² dr; B < 0 when attraction dominates.
  - P4
- ○ **TD-7.2.D** Estimate properties of a gas or gas mixture by corresponding states and mixing rules.
  - EK: Z = f(T_r, P_r, ω); a_mix = ΣΣ y_iy_j √(a_ia_j)(1 − k_ij), b_mix = Σ y_ib_i.
  - P3 · P5

## Unit 8 · Phase equilibrium of pure substances

Big ideas: MU, STAB, EQ

### 8.1 Conditions for phase equilibrium and the phase rule

Book: dill-bromberg-2e §14; shell-2015 §10.1, §10.2, §10.4

- ○ **TD-8.1.A** State the conditions for phase coexistence and apply the Gibbs phase rule to a phase diagram.
  - EK: T, P, μ_i equal in every phase; F = C − π + 2.
  - P1 · P2

### 8.2 The Clapeyron and Clausius–Clapeyron equations

Book: dill-bromberg-2e §14; shell-2015 §10.3

- ● **TD-8.2.A** Calculate the slope of a coexistence curve from the Clapeyron equation.
  - EK: dP/dT = Δh/(TΔv).
  - P5 · drills: th-pe-clapeyron
- ● **TD-8.2.B** Estimate a vapor pressure at a new temperature with the integrated Clausius–Clapeyron equation.
  - EK: ln(P₂/P₁) = −(Δh_vap/R)(1/T₂ − 1/T₁); ideal vapor, v_liq ≪ v_vap, constant Δh.
  - P5 · drills: th-pe-cc-pressure
- ● **TD-8.2.C** Find Δh_vap from vapor pressures at two temperatures.
  - EK: Slope of ln P vs 1/T is −Δh_vap/R.
  - P5 · drills: th-pe-cc-enthalpy
- ● **TD-8.2.D** Find the boiling temperature at a new pressure.
  - EK: 1/T₂ = 1/T₁ − (R/Δh_vap) ln(P₂/P₁).
  - P5 · drills: th-pe-cc-temperature

### 8.3 Order parameters and types of transition

Book: dill-bromberg-2e §25; shell-2015 §10.6

- ○ **TD-8.3.A** Classify a transition as first- or second-order from which derivatives of G are discontinuous.
  - EK: First order: jumps in S, V (latent heat); continuous: jumps or divergences in C_p, κ_T; the order parameter vanishes at T_c.
  - P6

## Unit 9 · Solutions and mixtures

Big ideas: MU, EQ, STAB

### 9.1 Ideal solutions

Book: dill-bromberg-2e §15; shell-2015 §12.1

- ● **TD-9.1.A** Calculate the entropy of ideal mixing.
  - EK: ΔS_mix = −nR Σ x_i ln x_i (from lattice counting).
  - Needs: TD-1.1.D
  - P5 · drills: th-so-mix-entropy
- ● **TD-9.1.B** Calculate the Gibbs energy of ideal mixing.
  - EK: ΔG_mix = nRT Σ x_i ln x_i; ΔH_mix = ΔV_mix = 0.
  - P5 · drills: th-so-mix-gibbs

### 9.2 Partial molar quantities and Gibbs–Duhem in mixtures

Book: dill-bromberg-2e §9; shell-2015 §12.8, §12.9

- ○ **TD-9.2.A** Calculate partial molar properties from a total property, e.g. by the tangent-intercept method.
  - EK: v̄_i = (∂V/∂n_i)_{T,P,n_j}; V = Σ n_i v̄_i.
  - P3
- ○ **TD-9.2.B** Use Gibbs–Duhem to get one activity coefficient from the other or to test data for consistency.
  - EK: Σ x_i d ln γ_i = 0 at fixed T, P.
  - Needs: TD-2.3.E
  - P3 · P6

### 9.3 Vapor–liquid equilibrium

Book: dill-bromberg-2e §15, §16; shell-2015 §12.2, §13.1, §13.2, §13.3, §13.4, §13.5

- ● **TD-9.3.A** Calculate total pressure and vapor composition of an ideal solution with Raoult's law.
  - EK: p_i = x_iP_i*; P = Σ x_iP_i*; y_i = p_i/P.
  - P5 · drills: th-so-raoult
- ● **TD-9.3.B** Calculate the solubility of a dilute solute from Henry's law.
  - EK: p_i = x_iK_H,i for x_i → 0; K_H grows with T for most gases in water.
  - P5 · drills: th-so-henry
- ○ **TD-9.3.C** Perform bubble-point, dew-point and isothermal flash calculations for a multicomponent mixture.
  - EK: K_i = y_i/x_i; flash: Σ z_i(K_i − 1)/[1 + β(K_i − 1)] = 0 (Rachford–Rice).
  - P2 · P5

### 9.4 Nonideal solutions and activity

Book: dill-bromberg-2e §15; shell-2015 §12.6, §12.7, §13.6, §13.7

- ● **TD-9.4.A** Calculate activity coefficients from an excess-Gibbs-energy model (regular solution, Margules).
  - EK: G^ex/n = W x_Ax_B ⇒ RT ln γ_A = W x_B².
  - P3 · P5 · drills: th-so-activity
- ○ **TD-9.4.B** Derive the regular-solution model from a lattice with nearest-neighbour interactions and predict when the mixture phase-separates.
  - EK: ΔG_mix/nRT = Σ x ln x + χ x_Ax_B; unstable for χ > 2 (upper critical point at χ = 2, x = ½).
  - Needs: TD-6.1.A
  - P4 · P6
- ○ **TD-9.4.C** Calculate VLE with modified Raoult's law and identify an azeotrope.
  - EK: y_iP = x_iγ_iP_i*; at an azeotrope x_i = y_i and γ_A P_A* = γ_B P_B*.
  - P5 · P6

### 9.5 Colligative properties

Book: dill-bromberg-2e §16; shell-2015 §12.3, §12.4, §12.5

- ○ **TD-9.5.A** Calculate boiling-point elevation, freezing-point depression or osmotic pressure of a dilute solution.
  - EK: ΔT_b = RT_b²x_B/Δh_vap; ΔT_f = RT_f²x_B/Δh_fus; Π = c_BRT (van 't Hoff).
  - P5

### 9.6 Solvation and transfer between phases

Book: dill-bromberg-2e §16

- ○ **TD-9.6.A** Relate a partition coefficient to the free energy of transferring a solute between phases.
  - EK: ΔG°_transfer = −RT ln K_partition; set by μ° differences in the two solvents.
  - P2 · P5

## Unit 10 · Chemical reaction equilibria

Big ideas: MU, EQ, MICRO

### 10.1 The equilibrium constant

Book: dill-bromberg-2e §13; shell-2015 §20.1, §20.2, §20.3, §20.4

- ● **TD-10.1.A** Calculate K from ΔG°.
  - EK: K = exp(−ΔG°/RT); standard state fixes the units of each activity.
  - P5 · drills: th-ce-k
- ● **TD-10.1.B** Calculate ΔG° from K.
  - EK: ΔG° = −RT ln K.
  - P5 · drills: th-ce-dg
- ● **TD-10.1.C** Predict the direction of reaction from Q versus K.
  - EK: ΔG = ΔG° + RT ln Q = RT ln(Q/K); Q < K ⇒ forward.
  - P6 · drills: th-ce-direction

### 10.2 Equilibrium composition

Book: dill-bromberg-2e §13; shell-2015 §20.3, §20.4

- ● **TD-10.2.A** Solve for the equilibrium extent of reaction and composition from K and the feed.
  - EK: n_i = n_i0 + ν_iξ; K = Π(y_iP/P°)^ν_i for ideal gases.
  - P2 · P5 · drills: th-ce-extent
- ○ **TD-10.2.B** Predict how pressure, inerts or a nonideal phase shift an equilibrium.
  - EK: K_y = K(P/P°)^(−Δν); raising P favours fewer gas moles; fugacity or activity replaces y_iP in real phases.
  - P6

### 10.3 Temperature dependence of K

Book: dill-bromberg-2e §13; shell-2015 §20.5

- ● **TD-10.3.A** Find ΔH° from K at two temperatures, or K at a new temperature, with the van 't Hoff equation.
  - EK: d ln K/d(1/T) = −ΔH°/R.
  - P5 · drills: th-ce-vant-hoff

### 10.4 Reaction equilibrium from molecular partition functions

Book: dill-bromberg-2e §13; shell-2015 §20.6, §20.7

- ○ **TD-10.4.A** Calculate K for a gas-phase reaction from molecular partition functions.
  - EK: K = Π(q_i/V)^ν_i e^(−ΔE₀/k_BT) (per standard volume); dissociation energies set ΔE₀.
  - Needs: TD-12.2.C
  - P4 · P5

## Unit 11 · The Boltzmann distribution and the canonical ensemble

Big ideas: MICRO, EQ

### 11.1 The Boltzmann distribution

Book: dill-bromberg-2e §10; shell-2015 §16.2, §16.3

- ● **TD-11.1.A** Calculate the population ratio of two levels at a given temperature.
  - EK: N₂/N₁ = (g₂/g₁) e^(−ΔE/k_BT); 1 cm⁻¹ ↔ 1.439 K.
  - P5 · drills: sm-bz-ratio
- ● **TD-11.1.B** Calculate the fraction of molecules in a given level of a multi-level system.
  - EK: p_j = g_j e^(−βE_j)/q.
  - P4 · P5 · drills: sm-bz-fraction, sm-bz-exact
- ● **TD-11.1.C** Find the temperature at which a level reaches a given population ratio.
  - EK: T = ΔE/[k_B ln(g₂N₁/g₁N₂)].
  - P5 · drills: sm-bz-temperature

### 11.2 The partition function and thermodynamic properties

Book: dill-bromberg-2e §10; shell-2015 §16.1, §16.4, §16.5

- ● **TD-11.2.A** Calculate a molecular partition function from a list of levels and degeneracies.
  - EK: q = Σ g_j e^(−βE_j); q counts thermally accessible states.
  - P4 · P5 · drills: sm-pf-q
- ● **TD-11.2.B** Derive the average energy U from ln q for a two-level system or harmonic oscillator.
  - EK: U = −N ∂ln q/∂β; oscillator U/Nε = 1/(e^x − 1).
  - P3 · P4 · drills: sm-pf-u-two-level, sm-pf-u-oscillator
- ● **TD-11.2.C** Derive the entropy from the partition function.
  - EK: S = U/T + Nk_B ln q (localized); S/Nk_B = ln q + βU/N.
  - P3 · P4 · drills: sm-pf-s-two-level
- ● **TD-11.2.D** Calculate the Helmholtz free energy from the partition function.
  - EK: F = −k_BT ln Q; localized independent molecules: Q = q^N.
  - P2 · P5 · drills: sm-pf-f
- ○ **TD-11.2.E** Assemble the system partition function from molecular ones for distinguishable or indistinguishable particles.
  - EK: Q = q^N (localized) or q^N/N! (gas); independent modes multiply: q = q_t q_r q_v q_e.
  - P4

## Unit 12 · Molecular models of gases and solids

Big ideas: MICRO, FUND

### 12.1 Translation and the classical ideal gas

Book: dill-bromberg-2e §11; shell-2015 §9.1, §18.1, §18.4

- ● **TD-12.1.A** Calculate the thermal de Broglie wavelength of a molecule.
  - EK: Λ = h/√(2πmk_BT); classical when Λ³ ≪ V/N.
  - P5 · drills: sm-ig-lambda
- ● **TD-12.1.B** Calculate the translational partition function of a molecule in a box.
  - EK: q_trans = V/Λ³.
  - P5 · drills: sm-ig-qtrans
- ○ **TD-12.1.C** Derive the ideal-gas law and the Sackur–Tetrode entropy from Q = q^N/N!.
  - EK: P = k_BT ∂ln Q/∂V = Nk_BT/V; S/Nk_B = ln(V/NΛ³) + 5/2.
  - Needs: TD-11.2.E
  - P3 · P4

### 12.2 Rotation and vibration

Book: dill-bromberg-2e §11

- ● **TD-12.2.A** Calculate the rotational temperature of a diatomic from masses and bond length.
  - EK: I = μr²; θ_rot = ħ²/(2Ik_B).
  - P5 · drills: sm-ig-theta-rot
- ● **TD-12.2.B** Calculate the high-temperature rotational partition function, including the symmetry number.
  - EK: q_rot = T/(σθ_rot); σ = 2 homonuclear, 1 heteronuclear.
  - P5 · drills: sm-ig-qrot
- ● **TD-12.2.C** Calculate the vibrational temperature and vibrational partition function.
  - EK: θ_vib = hcν̃/k_B; q_vib = 1/(1 − e^(−θ_vib/T)) from the ground state.
  - P5 · drills: sm-ig-qvib

### 12.3 Heat capacity

Book: dill-bromberg-2e §12; shell-2015 §14.4, §14.5, §14.6

- ● **TD-12.3.A** Calculate the classical heat capacity of a gas by equipartition.
  - EK: ½k_B per quadratic term: 3 translational, 2 or 3 rotational, 2 per vibration (3N − 5 or 3N − 6 modes).
  - P4 · P6 · drills: sm-cv-equipartition
- ● **TD-12.3.B** Calculate C_V of a diatomic gas with classical translation and rotation and quantum vibration.
  - EK: C_V,m = 5R/2 + R x²eˣ/(eˣ − 1)², x = θ_vib/T.
  - P4 · P5 · drills: sm-cv-diatomic
- ● **TD-12.3.C** Derive the heat capacity of a two-level (Schottky) system.
  - EK: C_V = (∂U/∂T)_V; peaks near k_BT ~ ε and vanishes at both limits.
  - P3 · P6 · drills: sm-cv-two-level
- ● **TD-12.3.D** Derive the heat capacity of a quantum harmonic oscillator.
  - EK: C_V/Nk_B = x²eˣ/(eˣ − 1)² → 1 classically.
  - P3 · drills: sm-cv-oscillator
- ● **TD-12.3.E** Calculate the molar heat capacity of a crystal from the Einstein model.
  - EK: C_V,m = 3R x²eˣ/(eˣ − 1)², x = θ_E/T; Dulong–Petit 3R at high T.
  - P5 · drills: sm-cv-einstein
- ○ **TD-12.3.F** Apply the Debye T³ law at low temperature and explain why Einstein fails there.
  - EK: C_V ∝ (T/θ_D)³ at T ≪ θ_D: low-frequency acoustic modes stay active.
  - P6

### 12.4 Classical continuous degrees of freedom

Book: shell-2015 §18.1, §18.2, §18.3, §18.5

- ○ **TD-12.4.A** Compute averages from the Maxwell–Boltzmann speed distribution.
  - EK: f(v) ∝ v² e^(−mv²/2k_BT); v_mp = √(2k_BT/m), ⟨v⟩ = √(8k_BT/πm), v_rms = √(3k_BT/m).
  - P4 · P5
- ○ **TD-12.4.B** Write the classical canonical partition function as a phase-space integral and reduce it to a configurational integral.
  - EK: Q = (1/N!h^(3N)) ∫e^(−βH) dp dr = Z/(N!Λ^(3N)).
  - P4

### 12.5 The third law

Book: shell-2015 §15.1, §15.2, §15.3, §15.4

- ○ **TD-12.5.A** Calculate an absolute entropy from heat-capacity data, including residual entropy of a disordered crystal.
  - EK: S(T) = ∫₀^T C_p/T dT + Σ Δh_trans/T_trans; residual S = R ln W per mole (CO: R ln 2).
  - P5 · P6

## Unit 13 · Fluctuations

Big ideas: MICRO, STAB

### 13.1 Energy fluctuations in the canonical ensemble

Book: dill-bromberg-2e §12; shell-2015 §17.1, §17.2, §17.3

- ● **TD-13.1.A** Calculate the energy variance of a molecule with a few discrete levels.
  - EK: σ_E² = ⟨E²⟩ − ⟨E⟩² = ∂²ln q/∂β².
  - Needs: TD-1.2.C
  - P4 · P5 · drills: sm-fl-two-level, sm-fl-exact
- ● **TD-13.1.B** Derive the energy variance of a quantum harmonic oscillator.
  - EK: σ_E²/ε² = eˣ/(eˣ − 1)².
  - P3 · drills: sm-fl-oscillator
- ● **TD-13.1.C** Calculate the rms energy fluctuation from the heat capacity.
  - EK: σ_E² = k_BT²C_V — positive C_V is the stability condition again.
  - P5 · drills: sm-fl-cv
- ● **TD-13.1.D** Calculate the relative energy fluctuation of a macroscopic system and explain why ensembles agree.
  - EK: σ_E/⟨E⟩ ∝ N^(−1/2); monatomic ideal gas: √(2/3N).
  - P5 · P6 · drills: sm-fl-relative

## Unit 14 · Other ensembles

Big ideas: MICRO, MU

### 14.1 The grand canonical ensemble

Book: dill-bromberg-2e §27; shell-2015 §19.2

- ● **TD-14.1.A** Calculate the occupancy probabilities of a site exchanging molecules with a reservoir at fixed μ.
  - EK: Ξ_site = 1 + e^(β(μ + ε)); p_empty = 1/Ξ.
  - P2 · P5 · drills: sm-ens-site
- ● **TD-14.1.B** Calculate the average number of bound molecules on independent sites from the grand partition function.
  - EK: Ξ = (1 + λe^(βε))^M; ⟨N⟩ = λ ∂ln Ξ/∂λ.
  - P3 · P4 · drills: sm-ens-lattice
- ● **TD-14.1.C** Calculate the particle-number variance in the grand canonical ensemble.
  - EK: σ_N² = λ ∂⟨N⟩/∂λ = k_BT (∂⟨N⟩/∂μ).
  - P3 · drills: sm-ens-n-fluct

### 14.2 The isothermal–isobaric ensemble

Book: shell-2015 §19.1

- ● **TD-14.2.A** Calculate the population ratio of two states that differ in energy and volume at fixed T and P.
  - EK: P_B/P_A = e^(−β(ΔE + PΔV)); G = −k_BT ln Δ.
  - P2 · P5 · drills: sm-ens-isobaric

### 14.3 The Gibbs entropy and choosing an ensemble

Book: shell-2015 §19.3

- ○ **TD-14.3.A** Calculate entropy from microstate probabilities with the Gibbs formula and match each ensemble to its potential.
  - EK: S = −k_B Σ p_i ln p_i; NVE ↔ S, NVT ↔ F, NPT ↔ G, μVT ↔ Ω = −PV.
  - P2

## Unit 15 · Binding, adsorption and cooperativity (extension)

Big ideas: MICRO, MU

### 15.1 Single-site binding and Langmuir adsorption

Book: dill-bromberg-2e §27

- ● **TD-15.1.A** Calculate fractional occupancy of a single-site receptor from K_d.
  - EK: θ = c/(K_d + c).
  - Needs: TD-14.1.A
  - P5 · drills: sm-bind-langmuir
- ● **TD-15.1.B** Find the gas pressure that gives a target Langmuir coverage.
  - EK: θ = KP/(1 + KP) ⇒ P = θ/[K(1 − θ)].
  - P5 · drills: sm-bind-pressure
- ● **TD-15.1.C** Calculate the standard binding free energy from K_d.
  - EK: ΔG°_bind = RT ln(K_d/c°), c° = 1 M.
  - P5 · drills: sm-bind-dg

### 15.2 Multi-site and cooperative binding

Book: dill-bromberg-2e §26, §28

- ● **TD-15.2.A** Calculate the average number bound to a two-site molecule with a pair interaction from its binding polynomial.
  - EK: Ξ = 1 + 2y + wy²; ⟨N⟩ = (2y + 2wy²)/Ξ; w > 1 cooperative.
  - P4 · drills: sm-ens-pair
- ● **TD-15.2.B** Calculate fractional saturation from the Hill equation.
  - EK: θ = cⁿ/(K_{1/2}ⁿ + cⁿ).
  - P5 · drills: sm-bind-hill
- ● **TD-15.2.C** Find the Hill coefficient from saturation at two concentrations.
  - EK: n_H = Δ ln[θ/(1 − θ)] / Δ ln c.
  - P5 · P6 · drills: sm-bind-hill-n
- ○ **TD-15.2.D** Solve the Zimm–Bragg helix–coil or 1-D Ising model with a transfer matrix, or a mean-field Ising model for T_c.
  - EK: Q = λ₁^N for large N; mean field: k_BT_c = zJ.
  - P4

## Unit 16 · Reaction rates and transition states (extension)

Big ideas: MICRO, EQ

### 16.1 Arrhenius temperature dependence

Book: dill-bromberg-2e §19; shell-2015 §21.2

- ● **TD-16.1.A** Find the activation energy from rate constants at two temperatures.
  - EK: ln(k₂/k₁) = −(E_a/R)(1/T₂ − 1/T₁).
  - P5 · drills: sm-rate-ea
- ● **TD-16.1.B** Find a rate constant at a new temperature from E_a.
  - EK: k₂ = k₁ exp[−(E_a/R)(1/T₂ − 1/T₁)].
  - P5 · drills: sm-rate-k2
- ● **TD-16.1.C** Calculate the factor by which a rate rises over a temperature interval.
  - EK: k₂/k₁ = exp[(E_a/R)(1/T₁ − 1/T₂)]; the 'doubles per 10 K' rule ↔ E_a ≈ 50 kJ/mol near 300 K.
  - P5 · P6 · drills: sm-rate-factor

### 16.2 Transition-state theory

Book: dill-bromberg-2e §19; shell-2015 §21.1, §21.3, §21.4

- ● **TD-16.2.A** Calculate a rate constant from ΔH‡ and ΔS‡ with the Eyring equation.
  - EK: k = (k_BT/h) e^(ΔS‡/R) e^(−ΔH‡/RT).
  - P5 · drills: sm-rate-eyring
- ● **TD-16.2.B** Find the activation free energy from a measured rate constant.
  - EK: ΔG‡ = −RT ln(kh/k_BT).
  - P5 · drills: sm-rate-dg
- ○ **TD-16.2.C** Relate forward and reverse rate constants to K by detailed balance and read rates off a free-energy profile along a reaction coordinate.
  - EK: k_f/k_r = K; barrier height on F(ξ) sets k; catalysts lower ΔG‡, not ΔG°.
  - Needs: TD-10.1.A
  - P6

## Unit 17 · Electrolytes, polymers and simulation (extension)

Big ideas: MU, MICRO

### 17.1 Electrochemical equilibria and electrolytes

Book: dill-bromberg-2e §22, §23; shell-2015 §13.9

- ○ **TD-17.1.A** Calculate an equilibrium potential with the Nernst equation and a mean ionic activity coefficient with Debye–Hückel.
  - EK: E = E° − (RT/zF) ln Q; ln γ± = −A|z₊z₋|√I (dilute limit).
  - P5

### 17.2 Polymer solutions

Book: dill-bromberg-2e §32; shell-2015 §13.8

- ○ **TD-17.2.A** Calculate the Flory–Huggins free energy of mixing and the critical χ for a polymer solution.
  - EK: ΔG_mix/k_BT = (φ/N) ln φ + (1 − φ) ln(1 − φ) + χφ(1 − φ); χ_c = ½(1 + 1/√N)².
  - Needs: TD-9.4.B
  - P4 · P6

### 17.3 Molecular simulation

Book: shell-2015 §22.1, §22.2, §22.3, §22.4, §22.5

- ○ **TD-17.3.A** Apply the Metropolis acceptance rule and compute an ensemble average from a sampled trajectory.
  - EK: acc = min(1, e^(−βΔE)); ⟨A⟩ = time average over equilibrated, decorrelated samples.
  - P2 · P4
