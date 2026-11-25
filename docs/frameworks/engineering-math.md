# Applied Engineering Mathematics — curriculum framework (draft 1)

Generated from `drills/frameworks/engineering-math.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**155 learning objectives** in 14 units (151 core): 155 drilled, 0 partly, 0 with no drills. Core: 151 / 151 drilled.

## Big ideas

- **MODEL · Equations come from balances.** A rate of change equals inflow minus outflow plus generation; the ODE or PDE, its initial and boundary conditions, and its parameters all come from the physical system, and its answer must make physical sense.
- **FORM · The form of the equation picks the method.** Order, linearity, coefficients (constant, Euler–Cauchy, analytic, singular) and forcing decide which technique works. Classify before you compute.
- **LIN · Linear problems superpose.** Solutions of a linear homogeneous equation form a vector space; general solution = homogeneous basis + one particular solution, and independence (Wronskian, determinant) says when a basis is complete.
- **EIG · Eigenvalues decouple linear problems.** Characteristic roots, matrix eigenvalues and Sturm–Liouville eigenvalues are one idea — find the modes, and each evolves on its own; their signs and imaginary parts set growth, decay, oscillation and stability.
- **TRANS · Change the representation to simplify.** Substitutions, power series, Laplace transforms and eigenfunction (Fourier) expansions turn a hard problem into algebra or a recurrence, solved there and transformed back.

## Practices

- **P1 · Model the system.** Translate a physical description into a differential equation with initial or boundary conditions; name the variables, parameters and units.
- **P2 · Classify the equation.** State order, linearity, homogeneity, coefficient type, singular points or boundary type, and choose the method that fits.
- **P3 · Execute the method.** Carry out the integration, algebra, recurrence, transform or eigen-decomposition without dropping terms or constants.
- **P4 · Impose conditions.** Apply initial or boundary conditions to fix constants, eigenvalues or coefficients; keep the general solution until the end.
- **P5 · Check the answer.** Substitute back, test limiting cases and t → ∞ behaviour, confirm independence and that the solution satisfies every condition.
- **P6 · Interpret qualitatively.** Read stability, time constants, resonance and long-time behaviour off the roots or eigenvalues; sketch solutions and phase portraits; predict how a parameter change moves them.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · The calculus and complex-number toolkit | core | review | 10 | 10 | 0 | 0 |
| 2 · First-order ODEs | core | 15–20% | 17 | 17 | 0 | 0 |
| 3 · Second-order linear ODEs | core | 20–25% | 18 | 18 | 0 | 0 |
| 4 · Higher-order linear ODEs | core | 5% | 4 | 4 | 0 | 0 |
| 5 · Systems of ODEs, phase plane and stability | core | 15–20% | 13 | 13 | 0 | 0 |
| 6 · Series solutions and special functions | core | 15% | 11 | 11 | 0 | 0 |
| 7 · Laplace transforms | core | 15% | 14 | 14 | 0 | 0 |
| 8 · Linear algebra for ODEs | core | as needed | 11 | 11 | 0 | 0 |
| 9 · Fourier series and Sturm–Liouville boundary-value problems | core | 10–15% | 11 | 11 | 0 | 0 |
| 10 · Partial differential equations | core | — | 23 | 23 | 0 | 0 |
| 11 · Fourier integrals and transforms | extension | — | 2 | 2 | 0 | 0 |
| 12 · Vector calculus for transport | extension | — | 2 | 2 | 0 | 0 |
| 13 · More on ODEs: circuits, bifurcations, operators, existence | core | — | 5 | 5 | 0 | 0 |
| 14 · Complex analysis | core | — | 14 | 14 | 0 | 0 |

## Unit 1 · The calculus and complex-number toolkit

Big ideas: FORM, TRANS

### 1.1 Integration techniques

Book: kreyszig-10e §1.3, §1.5, §6.4

- ● **EM-1.1.A** (webwork-opl:CA5.1) Evaluate an integral by u-substitution, choosing u so its derivative appears in the integrand.
  - EK: ∫f(g(x))g′(x)dx = ∫f(u)du; a missing constant factor is fine, a missing x is not.
  - P3 · drills: usub-poly, usub-exp, usub-trig, usub-log, usub-ratio, usub-linear
- ● **EM-1.1.B** (webwork-opl:CA5.3) Evaluate an integral by parts, including tabular and cyclic (e^ax·trig) cases.
  - EK: ∫u dv = uv − ∫v du; LIATE picks u; cyclic integrals return to themselves and are solved algebraically.
  - P3 · drills: parts-x-exp, parts-x-trig, parts-x-log, parts-tabular, parts-exp-trig, parts-inverse
- ● **EM-1.1.C** (webwork-opl:CA5.7) Decompose a rational function into partial fractions (distinct, repeated, irreducible quadratic, improper) and integrate it.
  - EK: Divide first if improper; repeated factor (x−a)^k needs k terms; irreducible quadratic gets (Ax+B).
  - P3 · drills: pf-distinct, pf-repeated, pf-three, pf-irreducible, pf-improper, pf-coeffs

### 1.2 Complex numbers and Euler's formula

Book: kreyszig-10e §2.2, §13.1, §13.2, §13.5

- ● **EM-1.2.A** (webwork-opl:CX1.1, webwork-opl:CX1.2, webwork-opl:CX1.3, webwork-opl:CX1.4, webwork-opl:CX1.5, webwork-opl:CX1.6, webwork-opl:CX1.7, webwork-opl:CX1.8) Convert complex numbers between rectangular, polar and exponential form.
  - EK: e^(iθ) = cos θ + i sin θ; z = re^(iθ), r = |z|, θ = arg z.
  - P3 · drills: euler-rect, euler-polar, euler-re-im
- ● **EM-1.2.B** (webwork-opl:CX1.9) Compute powers and roots of a complex number with De Moivre's formula.
  - EK: (re^(iθ))^n = r^n e^(inθ); n distinct n-th roots spaced 2π/n apart.
  - P3 · drills: euler-demoivre
- ● **EM-1.2.C** (webwork-opl:CX2.2) Find the complex roots α ± βi of a real quadratic.
  - EK: Complex roots of real polynomials come in conjugate pairs; α = −b/2a, β = √(4ac − b²)/2a.
  - P3 · drills: euler-quad-roots

### 1.3 Summation notation

Book: kreyszig-10e §5.1

- ● **EM-1.3.A** Shift a summation index so two power series start at the same index and carry the same power of x.
  - EK: Replace m by m ± k and adjust the limits; the sum is unchanged.
  - P3 · drills: sigma-shift-down, sigma-shift-up, sigma-prefactor, sigma-derivative, sigma-combine

### 1.4 Partial derivatives and exact differentials

Book: kreyszig-10e §1.4, §9.6

- ● **EM-1.4.A** Compute first and mixed partial derivatives of a function of two variables.
  - EK: Hold the other variable constant; for smooth functions u_xy = u_yx.
  - P3 · drills: mv-partial, mv-mixed
- ● **EM-1.4.B** Find dy/dx for a curve defined implicitly by F(x, y) = c.
  - EK: dy/dx = −F_x / F_y.
  - P3 · drills: mv-implicit
- ● **EM-1.4.C** (webwork-opl:DE2.2) Test whether M dx + N dy is an exact differential.
  - EK: Exact on a simply connected domain ⇔ ∂M/∂y = ∂N/∂x.
  - P2 · drills: mv-exact-test

## Unit 2 · First-order ODEs

Big ideas: MODEL, FORM, TRANS

### 2.1 Basic concepts, direction fields and Euler's method

Book: kreyszig-10e §1.1, §1.2

- ● **EM-2.1.A** (webwork-opl:DE1.1, webwork-opl:DE1.2) Classify an ODE by order and linearity, and verify that a given function solves it.
  - EK: Order = highest derivative; linear ⇔ y and its derivatives appear to first power with coefficients in x only.
  - P2 · P5 · drills: em-verify-solution, ~em-classify-ode
- ● **EM-2.1.B** (webwork-opl:DE2.12) Sketch a direction field and solution curves from isoclines of y′ = f(x, y).
  - EK: Isocline f(x, y) = k has slope k everywhere; solution curves are tangent to the field.
  - P6 · drills: em-isoclines, ca-slope-field-match
- ● **EM-2.1.C** (webwork-opl:DE6.1) Approximate an IVP solution with a few steps of Euler's method and estimate the error trend.
  - EK: y_(n+1) = y_n + h f(x_n, y_n); global error is O(h).
  - P3 · P5 · drills: ca-euler-method

### 2.2 Separable equations and reducing substitutions

Book: kreyszig-10e §1.3

- ● **EM-2.2.A** (webwork-opl:DE2.3) Solve a separable ODE explicitly where possible, including the IVP constant.
  - EK: g(y)dy = f(x)dx, integrate both sides; check for lost equilibrium solutions when dividing by g.
  - Needs: EM-1.1.A, EM-1.1.C
  - P3 · P4 · drills: sep-exp-growth, sep-over-y, sep-y-squared, sep-exp-split, sep-over-y2
- ● **EM-2.2.B** (webwork-opl:DE2.4) Reduce an ODE to separable form with u = y/x or u = ax + by + c, and solve it.
  - EK: y′ = f(y/x): y = ux ⇒ u + xu′ = f(u); y′ = f(ax + by + c): u′ = a + bf(u).
  - Needs: EM-2.2.A
  - P2 · P3 · drills: sub-ratio, sub-square, sub-exp, sub-linear-square, sub-arctan

### 2.3 Exact equations and integrating factors

Book: kreyszig-10e §1.4

- ● **EM-2.3.A** (webwork-opl:DE2.2) Solve an exact ODE by finding the potential u(x, y) = c, and fit an IVP.
  - EK: u_x = M, u_y = N; integrate one, differentiate, match the other.
  - Needs: EM-1.4.C
  - P3 · P4 · drills: exact-poly, exact-trans, exact-exy, exact-ivp
- ● **EM-2.3.B** (webwork-opl:DE2.13) Decide whether an integrating factor depending only on x or only on y exists.
  - EK: R = (M_y − N_x)/N a function of x alone ⇒ F(x) = exp∫R dx; R* = (N_x − M_y)/M of y alone ⇒ F(y).
  - P2 · drills: if-test
- ● **EM-2.3.C** (webwork-opl:DE2.13) Find the integrating factor and solve the resulting exact equation.
  - EK: Multiply by F, re-check exactness, then solve as exact.
  - Needs: EM-2.3.A, EM-2.3.B
  - P3 · drills: if-factor-x, if-factor-y, if-solve

### 2.4 Linear and Bernoulli equations

Book: kreyszig-10e §1.5

- ● **EM-2.4.A** (webwork-opl:DE2.1) Solve a linear first-order ODE with an integrating factor, including IVPs and forcing that matches e^(−∫p).
  - EK: y′ + py = r ⇒ y = e^(−h)[∫e^h r dx + c], h = ∫p dx.
  - Needs: EM-1.1.A
  - P3 · P4 · drills: lin-exp, lin-const, lin-power, lin-gauss, lin-trig, lin-resonant
- ● **EM-2.4.B** (webwork-opl:DE2.1) Solve a linear ODE whose integrating-factor integral needs integration by parts.
  - EK: ∫e^h r dx often pairs a polynomial or trig with an exponential.
  - Needs: EM-2.4.A, EM-1.1.B
  - P3 · drills: ibp-poly, ibp-over-x-trig, ibp-over-x-exp, ibp-x-exp, ibp-trig-exp, ibp-power-exp
- ● **EM-2.4.C** (webwork-opl:DE2.4) Reduce a Bernoulli equation to a linear one with u = y^(1−a) and solve it.
  - EK: y′ + py = g y^a ⇒ u′ + (1−a)p u = (1−a)g.
  - Needs: EM-2.4.A
  - P2 · P3 · drills: bern-const, bern-power, bern-exp

### 2.5 Choosing a first-order method

Book: kreyszig-10e §1.3, §1.4, §1.5

- ● **EM-2.5.A** Identify which first-order method (separable, substitution, linear, Bernoulli, exact) solves a given ODE.
  - EK: Check in order: separable? linear in y? y^a term? exact? homogeneous in y/x?
  - P2 · drills: recog-separable, recog-substitution, recog-linear, recog-bernoulli, recog-exact

### 2.6 Modeling with first-order ODEs

Book: kreyszig-10e §1.3, §1.5

- ● **EM-2.6.A** (webwork-opl:DE2.8, webwork-opl:MB5.2) Set up and solve a mixing-tank balance for concentration or mass of solute.
  - EK: dm/dt = (rate in) − (rate out), rate out = (m/V)·Q_out.
  - P1 · P3 · drills: model-mixing
- ● **EM-2.6.B** (webwork-opl:DE2.6, webwork-opl:DE2.10) Model Newton's cooling and first-order decay, and extract a time constant, half-life or time to reach a value.
  - EK: dT/dt = −k(T − T_a); y = y_0 e^(−kt), t_1/2 = ln 2/k.
  - P1 · P6 · drills: model-cooling, model-decay
- ● **EM-2.6.C** (webwork-opl:DE2.7) Solve the logistic equation and find its equilibria and carrying capacity.
  - EK: y′ = ky(1 − y/K) is separable and Bernoulli; y → K for y_0 > 0.
  - P1 · P6 · drills: model-logistic
- ● **EM-2.6.D** (webwork-opl:DE2.5) Find and classify the equilibria of an autonomous ODE y′ = f(y) from a phase line.
  - EK: f(y*) = 0; stable if f′(y*) < 0.
  - P6 · drills: em-phase-line

### 2.7 Existence and uniqueness

Book: kreyszig-10e §1.7

- ● **EM-2.7.A** (webwork-opl:DE2.15) Decide whether an IVP has a unique solution near the initial point from the continuity of f and ∂f/∂y.
  - EK: f and f_y continuous on a rectangle around (x_0, y_0) ⇒ unique solution on some |x − x_0| < α.
  - P2 · drills: em-existence

## Unit 3 · Second-order linear ODEs

Big ideas: LIN, EIG, FORM, MODEL

### 3.1 Homogeneous theory, reduction of order and the Wronskian

Book: kreyszig-10e §2.1, §2.6

- ● **EM-3.1.A** Use superposition to build a general solution from a basis and fit it to an IVP.
  - EK: For a linear homogeneous ODE, any combination c_1y_1 + c_2y_2 of solutions is a solution; two independent ones form a basis.
  - P4 · drills: em-superposition-ivp
- ● **EM-3.1.B** (webwork-opl:DE3.1) Find a second solution from a known one by reduction of order.
  - EK: y_2 = u y_1, u′ = U = e^(−∫p dx)/y_1² (standard form y″ + py′ + qy = 0).
  - P3 · drills: red-euler, red-trig, red-exp, red-gauss, red-const
- ● **EM-3.1.C** (webwork-opl:DE3.11) Compute the Wronskian of two or three functions and use it to decide linear independence.
  - EK: W = det of the functions and their derivatives; W ≠ 0 somewhere ⇒ independent; for ODE solutions W ≡ 0 or never 0 (Abel).
  - P3 · P5 · drills: wr-exps, wr-repeated, wr-trig, wr-damped, wr-powers, wr-log, wr-dependent

### 3.2 Constant coefficients

Book: kreyszig-10e §2.2, §2.3

- ● **EM-3.2.A** (webwork-opl:DE3.3, webwork-opl:DE3.4, webwork-opl:DE3.5, webwork-opl:DE3.6) Write the general solution of ay″ + by′ + cy = 0 for each of the three root cases of the characteristic equation.
  - EK: Distinct real: e^(λ₁x), e^(λ₂x); double: e^(λx), xe^(λx); complex α ± iβ: e^(αx)cos βx, e^(αx)sin βx.
  - Needs: EM-1.2.C
  - P2 · P3 · drills: char-distinct, char-repeated, char-complex
- ● **EM-3.2.B** (webwork-opl:DE3.6) Solve a constant-coefficient IVP.
  - EK: Two conditions y(x_0), y′(x_0) fix c_1, c_2.
  - Needs: EM-3.2.A
  - P4 · drills: char-ivp

### 3.3 Euler–Cauchy equations

Book: kreyszig-10e §2.5

- ● **EM-3.3.A** (webwork-opl:DE3.7) Find the roots of the auxiliary equation of an Euler–Cauchy ODE.
  - EK: x²y″ + axy′ + by = 0 with y = x^m ⇒ m² + (a − 1)m + b = 0.
  - P2 · drills: ec-roots
- ● **EM-3.3.B** (webwork-opl:DE3.7) Write the general solution of an Euler–Cauchy ODE for each root case and fit an IVP.
  - EK: Distinct: x^(m₁), x^(m₂); double: x^m, x^m ln x; complex: x^μ cos(ν ln x), x^μ sin(ν ln x).
  - Needs: EM-3.3.A
  - P3 · P4 · drills: ec-distinct, ec-double, ec-complex, ec-ivp

### 3.4 Free oscillations

Book: kreyszig-10e §2.4

- ● **EM-3.4.A** (webwork-opl:DE3.2) Find the natural frequency, period, amplitude and phase of an undamped mass–spring system.
  - EK: my″ + ky = 0 ⇒ ω₀ = √(k/m); A cos ω₀t + B sin ω₀t = C cos(ω₀t − δ), C = √(A² + B²).
  - P1 · P6 · drills: spring-frequency, spring-amplitude-phase
- ● **EM-3.4.B** Solve an undamped oscillator IVP.
  - EK: y(0) and y′(0) give A and B/ω₀.
  - P4 · drills: spring-undamped-ivp
- ● **EM-3.4.C** Classify a damped oscillator as over-, critically or underdamped from c² − 4mk.
  - EK: c² > 4mk overdamped, = critical, < under; underdamped frequency ω* = √(4mk − c²)/2m.
  - P2 · P6 · drills: spring-classify
- ● **EM-3.4.D** (webwork-opl:DE3.2) Solve a damped oscillator IVP in each damping regime.
  - EK: Same three root cases as 3.2.A, with α = −c/2m < 0 so every solution decays.
  - Needs: EM-3.2.B
  - P3 · P4 · drills: spring-over-ivp, spring-critical-ivp, spring-under-ivp

### 3.5 Nonhomogeneous equations

Book: kreyszig-10e §2.7, §2.10

- ● **EM-3.5.A** (webwork-opl:DE3.8) Find a particular solution by undetermined coefficients, including the modification rule.
  - EK: Guess the form of r(x) (poly, e^(γx), cos/sin); multiply by x (or x²) when the guess solves the homogeneous ODE.
  - Needs: EM-3.2.A
  - P2 · P3 · drills: uc-poly, uc-exp, uc-trig, uc-resonance
- ● **EM-3.5.B** Assemble y = y_h + y_p and fit an IVP for a nonhomogeneous ODE.
  - EK: Apply initial conditions to the full solution, never to y_h alone.
  - P4 · drills: uc-general, vop-general
- ● **EM-3.5.C** (webwork-opl:DE3.9) Find a particular solution by variation of parameters when r(x) is not of undetermined-coefficient form or coefficients vary.
  - EK: y_p = −y₁∫y₂r/W dx + y₂∫y₁r/W dx, ODE in standard form.
  - Needs: EM-3.1.C
  - P3 · drills: vop-double, vop-trig, vop-euler

### 3.6 Forced oscillations, resonance and circuits

Book: kreyszig-10e §2.8, §2.9

- ● **EM-3.6.A** Find the steady-state response of a damped oscillator to sinusoidal forcing and its amplitude.
  - EK: y_p = a cos ωt + b sin ωt; amplitude C*(ω) = F₀/√((k − mω²)² + c²ω²); the transient dies out.
  - P3 · P6 · drills: forced-steady, forced-amplitude
- ● **EM-3.6.B** Recognise undamped resonance and beats and write the resulting solution.
  - EK: ω = ω₀, c = 0 ⇒ t sin ω₀t growth; ω near ω₀ ⇒ beats with envelope frequency |ω − ω₀|/2.
  - P6 · drills: forced-resonance, forced-beats
- ● **EM-3.6.C** Find the practical-resonance frequency of a damped forced oscillator.
  - EK: ω_max² = k/m − c²/2m², exists only if c² < 2mk.
  - P6 · drills: forced-practical
- ● **EM-3.6.D** (webwork-opl:DE3.2) Model an RLC circuit as a second-order ODE and map it onto the mass–spring analogy.
  - EK: LI″ + RI′ + I/C = E′(t): L ↔ m, R ↔ c, 1/C ↔ k.
  - P1 · drills: em-rlc

## Unit 4 · Higher-order linear ODEs

Big ideas: LIN, EIG

### 4.1 Homogeneous theory and constant coefficients

Book: kreyszig-10e §3.1, §3.2

- ● **EM-4.1.A** (webwork-opl:DE3.11) Test n functions for linear independence with the n×n Wronskian.
  - EK: Rows are f, f′, …, f^(n−1); expand by cofactors.
  - Needs: EM-3.1.C, EM-8.3.A
  - P3 · drills: wr-three
- ● **EM-4.1.B** Find the roots of an n-th order characteristic polynomial.
  - EK: Rational root test, then synthetic division to a quadratic.
  - P3 · drills: hi-roots
- ● **EM-4.1.C** (webwork-opl:DE3.3) Write the general solution of an n-th order constant-coefficient ODE with distinct, repeated and complex roots, and fit an IVP.
  - EK: A root of multiplicity k gives e^(λx), xe^(λx), …, x^(k−1)e^(λx).
  - Needs: EM-4.1.B
  - P3 · P4 · drills: hi-distinct, hi-repeated, hi-complex, hi-ivp

### 4.2 Nonhomogeneous higher-order equations

Book: kreyszig-10e §3.3

- ● **EM-4.2.A** (webwork-opl:DE3.8) Find a particular solution of an n-th order ODE by undetermined coefficients or variation of parameters.
  - EK: Same modification rule; variation of parameters uses Cramer's rule with W_k/W.
  - Needs: EM-3.5.A, EM-4.1.C
  - P3 · drills: em-undetermined-third, ~uc-general

## Unit 5 · Systems of ODEs, phase plane and stability

Big ideas: EIG, LIN, MODEL

### 5.1 Systems as models

Book: kreyszig-10e §4.1, §4.2

- ● **EM-5.1.A** (webwork-opl:DE5.1, webwork-opl:DE5.7) Convert an n-th order ODE into a first-order system.
  - EK: y₁ = y, y₂ = y′, …; the companion matrix's eigenvalues are the characteristic roots.
  - P1 · drills: em-first-order-system, ~phase-ode2
- ● **EM-5.1.B** (webwork-opl:DE5.1) Write the rate matrix for series first-order kinetics A → B → C.
  - EK: d[A]/dt = −k₁[A], d[B]/dt = k₁[A] − k₂[B]; C follows from mass conservation.
  - P1 · drills: kin-matrix

### 5.2 Constant-coefficient systems by eigenvalues

Book: kreyszig-10e §4.3

- ● **EM-5.2.A** (webwork-opl:DE5.4) Find the eigenvalues and eigenvectors that give the basis solutions of y′ = Ay.
  - EK: y = x e^(λt) with (A − λI)x = 0.
  - Needs: EM-8.4.A, EM-8.4.B
  - P3 · drills: sys-eigen
- ● **EM-5.2.B** (webwork-opl:DE5.4) Write the general solution of a 2×2 system with real distinct eigenvalues and fit an IVP.
  - EK: y = c₁x⁽¹⁾e^(λ₁t) + c₂x⁽²⁾e^(λ₂t).
  - Needs: EM-5.2.A
  - P3 · P4 · drills: sys-general, sys-ivp
- ● **EM-5.2.C** (webwork-opl:DE5.5) Write real solutions of a 2×2 system with complex eigenvalues and fit an IVP.
  - EK: Take real and imaginary parts of x e^((α+iβ)t).
  - Needs: EM-5.2.A, EM-1.2.A
  - P3 · P4 · drills: sys-complex, sys-complex-ivp
- ● **EM-5.2.D** (webwork-opl:DE5.6) Solve a 2×2 system with a repeated eigenvalue using a generalised eigenvector.
  - EK: Second solution x t e^(λt) + u e^(λt), (A − λI)u = x.
  - P3 · drills: sys-repeated
- ● **EM-5.2.E** (webwork-opl:DE5.3) Solve series kinetics A → B → C and find the time of maximum intermediate.
  - EK: Eigenvalues −k₁, −k₂; [B] = k₁A₀(e^(−k₁t) − e^(−k₂t))/(k₂ − k₁); t_max = ln(k₁/k₂)/(k₁ − k₂), = 1/k when k₁ = k₂.
  - Needs: EM-5.1.B
  - P3 · P6 · drills: kin-eigen, kin-B, kin-C, kin-tmax

### 5.3 Critical points and stability

Book: kreyszig-10e §4.3, §4.4

- ● **EM-5.3.A** (webwork-opl:DE5.9) Classify the critical point of a linear 2×2 system (node, saddle, centre, spiral) from its eigenvalues or from trace and determinant.
  - EK: p = tr A, q = det A, Δ = p² − 4q: q < 0 saddle; q > 0, Δ ≥ 0 node; Δ < 0 spiral (p ≠ 0) or centre (p = 0).
  - P2 · P6 · drills: phase-matrix, phase-equations, phase-ode2
- ● **EM-5.3.B** (webwork-opl:DE5.9) Decide whether a critical point is stable, asymptotically stable or unstable.
  - EK: Asymptotically stable ⇔ p < 0, q > 0; centre is stable, not asymptotically.
  - P6 · drills: phase-stability
- ● **EM-5.3.C** (webwork-opl:DE5.9) Sketch a phase portrait with eigenvector directions and trajectory orientation.
  - EK: Trajectories leave along the fast-growing eigenvector and approach along the slow-decaying one.
  - P6 · drills: em-phase-portrait

### 5.4 Nonlinear systems

Book: kreyszig-10e §4.5

- ● **EM-5.4.A** (webwork-opl:DE5.10) Find the critical points of a nonlinear autonomous system and linearise at each with the Jacobian.
  - EK: Set f = g = 0; J = [[f_x, f_y], [g_x, g_y]] at the point.
  - P3 · drills: em-nonlinear-critical
- ● **EM-5.4.B** (webwork-opl:DE5.10) Classify each critical point of a nonlinear system from its linearisation, noting when linearisation is inconclusive.
  - EK: Hyperbolic points keep their type; a linear centre may be a spiral in the nonlinear system.
  - Needs: EM-5.3.A, EM-5.4.A
  - P6 · drills: em-nonlinear-critical

### 5.5 Nonhomogeneous linear systems

Book: kreyszig-10e §4.6

- ● **EM-5.5.A** (webwork-opl:DE5.8) Find a particular solution of y′ = Ay + g by undetermined coefficients, diagonalisation or variation of parameters.
  - EK: Fundamental matrix Y: y_p = Y∫Y⁻¹g dt.
  - P3 · drills: em-nonhomog-system

## Unit 6 · Series solutions and special functions

Big ideas: TRANS, FORM

### 6.1 Ordinary and singular points

Book: kreyszig-10e §5.1, §5.3

- ● **EM-6.1.A** (webwork-opl:DE7.2) Classify a point as ordinary, regular singular or irregular singular.
  - EK: Standard form y″ + py′ + qy = 0: ordinary if p, q analytic; regular singular if (x − x₀)p and (x − x₀)²q are analytic.
  - P2 · drills: series-classify-point
- ● **EM-6.1.B** (webwork-opl:DE7.1) Give the guaranteed radius of convergence of a power-series solution about an ordinary point.
  - EK: At least the distance to the nearest singular point in the complex plane.
  - Needs: EM-6.1.A
  - P2 · drills: series-radius

### 6.2 Power series method

Book: kreyszig-10e §5.1

- ● **EM-6.2.A** (webwork-opl:DE7.1) Derive the recurrence relation for the coefficients of a power-series solution.
  - EK: Substitute Σa_m x^m, shift indices to a common power, set each coefficient to zero.
  - Needs: EM-1.3.A
  - P3 · drills: series-recurrence, series-recurrence-airy
- ● **EM-6.2.B** (webwork-opl:DE7.1) Generate the first terms of the series solution from the recurrence and initial values.
  - EK: a₀ = y(0), a₁ = y′(0); even and odd coefficients often split into two basis series.
  - Needs: EM-6.2.A
  - P3 · P4 · drills: series-terms, series-terms-airy

### 6.3 Frobenius method

Book: kreyszig-10e §5.3

- ● **EM-6.3.A** (webwork-opl:DE7.2) Find the indicial equation and its roots at a regular singular point.
  - EK: r(r − 1) + b₀r + c₀ = 0, b₀ = lim xp, c₀ = lim x²q.
  - Needs: EM-6.1.A
  - P3 · drills: frobenius-indicial
- ● **EM-6.3.B** (webwork-opl:DE7.2) Decide which Frobenius case applies and what form the second solution takes.
  - EK: Roots not differing by an integer: two x^r series; double root: second has ln x; differ by an integer: second may have ln x.
  - Needs: EM-6.3.A
  - P2 · drills: frobenius-case
- ● **EM-6.3.C** (webwork-opl:DE7.2) Construct the first Frobenius series solution from the larger indicial root.
  - EK: y = x^r Σa_m x^m; same index-shifting as the power series method.
  - Needs: EM-6.3.A, EM-6.2.A
  - P3 · drills: em-frobenius-first-solution

### 6.4 Legendre and Bessel functions

Book: kreyszig-10e §5.2, §5.4, §5.5

- ● **EM-6.4.A** Recognise Legendre's, Bessel's and Euler–Cauchy equations in a given ODE and read off the order or degree.
  - EK: (1 − x²)y″ − 2xy′ + n(n+1)y = 0; x²y″ + xy′ + (x² − ν²)y = 0.
  - P2 · drills: spec-identify, spec-legendre-n, spec-bessel-order
- ● **EM-6.4.B** (webwork-opl:DE7.3) Solve a scaled Bessel equation x²y″ + xy′ + (λ²x² − ν²)y = 0 with J_ν(λx), Y_ν(λx).
  - EK: Substitute z = λx.
  - P2 · P3 · drills: spec-bessel-scaled
- ● **EM-6.4.C** (webwork-opl:DE7.3) Write the general solution of Bessel's equation, choosing J₋ν or Y_ν as the second solution.
  - EK: J_ν, J₋ν independent unless ν is an integer, where J₋ₙ = (−1)ⁿJₙ; then use Y_ν.
  - P2 · P5 · drills: spec-bessel-independent
- ● **EM-6.4.D** Use Legendre polynomials' explicit form, Rodrigues' formula or orthogonality to evaluate P_n or an integral.
  - EK: P_n(x) = (1/2ⁿn!) dⁿ/dxⁿ (x² − 1)ⁿ; ∫P_mP_n = 0 on [−1, 1] for m ≠ n.
  - P3 · drills: em-legendre-eval

## Unit 7 · Laplace transforms

Big ideas: TRANS, LIN, MODEL

### 7.1 The transform, linearity and s-shifting

Book: kreyszig-10e §6.1

- ● **EM-7.1.A** (webwork-opl:DE4.2) Find the Laplace transform of a combination of elementary functions from the table, using identities where needed.
  - EK: L{tⁿ} = n!/s^(n+1); L{e^(at)} = 1/(s − a); L{cos ωt} = s/(s² + ω²); sin² = (1 − cos 2t)/2.
  - P3 · drills: lt-linear, lt-trig, lt-power, lt-hyperbolic, lt-identity
- ● **EM-7.1.B** (webwork-opl:DE4.7) Apply the first shifting theorem forwards and in reverse.
  - EK: L{e^(at)f(t)} = F(s − a); complete the square to expose s − a.
  - P3 · drills: shift-s-forward, shift-s-inverse

### 7.2 Inverse transforms by partial fractions

Book: kreyszig-10e §6.1, §6.4

- ● **EM-7.2.A** (webwork-opl:DE4.3) Invert a rational F(s) by partial fractions with distinct, repeated or complex poles.
  - EK: Repeated pole ⇒ tⁿe^(at)/n!; complex pole pair ⇒ e^(at)(cos, sin).
  - Needs: EM-1.1.C
  - P3 · drills: ilt-distinct, ilt-repeated, ilt-complex, ilt-three, ilt-quadratic

### 7.3 Solving IVPs by Laplace transform

Book: kreyszig-10e §6.2

- ● **EM-7.3.A** (webwork-opl:DE4.1) Solve a constant-coefficient IVP by transforming, solving the subsidiary equation and inverting.
  - EK: L{y′} = sY − y(0); L{y″} = s²Y − sy(0) − y′(0); initial conditions enter automatically.
  - Needs: EM-7.2.A
  - P3 · P4 · drills: livp-real, livp-complex, livp-double, livp-exp, livp-const
- ● **EM-7.3.B** Identify the transfer function of a linear system and relate its poles to stability and damping.
  - EK: Q(s) = Y/R with zero ICs = 1/(as² + bs + c); poles in the left half-plane ⇔ decay.
  - P6 · drills: transfer-g, transfer-poles, transfer-stable

### 7.4 Unit step and t-shifting

Book: kreyszig-10e §6.3

- ● **EM-7.4.A** (webwork-opl:DE4.6) Write a piecewise function with unit step functions and transform it.
  - EK: f = f₁ + (f₂ − f₁)u(t − a) + …; L{f(t − a)u(t − a)} = e^(−as)F(s).
  - P1 · P3 · drills: shift-t-forward, shift-piecewise
- ● **EM-7.4.B** (webwork-opl:DE4.7) Invert a transform containing e^(−as).
  - EK: e^(−as)F(s) ↦ f(t − a)u(t − a).
  - P3 · drills: shift-t-inverse
- ● **EM-7.4.C** (webwork-opl:DE4.6) Solve an IVP with switched or piecewise forcing.
  - EK: Transform the step-written forcing; the solution is piecewise with continuous y and y′.
  - Needs: EM-7.3.A, EM-7.4.A
  - P1 · P3 · drills: step-ivp-on, step-ivp-pulse

### 7.5 Impulses and the Dirac delta

Book: kreyszig-10e §6.4

- ● **EM-7.5.A** (webwork-opl:DE4.5) Model a sudden impulse with δ(t − a) and solve the resulting IVP, including the impulse response.
  - EK: L{δ(t − a)} = e^(−as); impulse response = L⁻¹{transfer function}.
  - P1 · P3 · drills: delta-ivp, delta-response

### 7.6 Convolution and integral equations

Book: kreyszig-10e §6.5

- ● **EM-7.6.A** (webwork-opl:DE4.4) Compute a convolution integral directly.
  - EK: (f * g)(t) = ∫₀ᵗ f(τ)g(t − τ)dτ.
  - P3 · drills: conv-compute
- ● **EM-7.6.B** (webwork-opl:DE4.4) Invert a product of transforms or transform an integral using the convolution theorem.
  - EK: L{f * g} = FG; L{∫₀ᵗ f dτ} = F/s.
  - P3 · drills: conv-inverse, conv-transform
- ● **EM-7.6.C** (webwork-opl:DE4.4) Solve a Volterra integral equation of convolution type.
  - EK: Transform, solve for Y algebraically, invert.
  - Needs: EM-7.6.B
  - P3 · drills: conv-volterra

### 7.7 Transform derivatives and systems

Book: kreyszig-10e §6.6, §6.7

- ● **EM-7.7.A** Use L{tf(t)} = −F′(s) to transform or invert functions and solve ODEs with linear coefficients.
  - EK: Differentiation in s ↔ multiplication by −t; integration in s ↔ division by t.
  - P3 · drills: tmul-forward, tmul-inverse
- ● **EM-7.7.B** (webwork-opl:DE4.1) Solve a linear system of ODEs by Laplace transform.
  - EK: Transform each equation, solve the algebraic system (Cramer), invert each component.
  - Needs: EM-7.3.A
  - P3 · drills: lsys-ivp, lsys-forced

## Unit 8 · Linear algebra for ODEs

Big ideas: LIN, EIG

### 8.1 Linear systems and Gauss elimination

Book: kreyszig-10e §7.3, §7.5

- ● **EM-8.1.A** Solve a linear system by row reduction and state whether it has none, one or infinitely many solutions.
  - EK: Echelon form; rank A vs rank [A|b] decides existence; free variables give a family.
  - P3 · drills: la-system

### 8.2 Linear independence and rank

Book: kreyszig-10e §7.4

- ● **EM-8.2.A** Decide whether a set of vectors is linearly independent.
  - EK: Independent ⇔ only the trivial combination is zero ⇔ rank = number of vectors; for n vectors in ℝⁿ, det ≠ 0.
  - P2 · drills: la-independence

### 8.3 Determinants and inverses

Book: kreyszig-10e §7.6, §7.7, §7.8

- ● **EM-8.3.A** Evaluate a 3×3 determinant by cofactor expansion.
  - EK: Expand along the row or column with most zeros; sign pattern (−1)^(i+j).
  - P3 · drills: la-det
- ● **EM-8.3.B** Find the inverse of a 2×2 matrix, or show it does not exist.
  - EK: A⁻¹ = (1/det A)[[d, −b], [−c, a]]; singular ⇔ det A = 0.
  - P3 · drills: la-inverse

### 8.4 The matrix eigenvalue problem

Book: kreyszig-10e §8.1, §8.2

- ● **EM-8.4.A** Find the eigenvalues of a 2×2 matrix from its characteristic polynomial.
  - EK: λ² − (tr A)λ + det A = 0.
  - P3 · drills: la-eigenvalues
- ● **EM-8.4.B** Find an eigenvector for each eigenvalue of a 2×2 matrix.
  - EK: Solve (A − λI)x = 0; one row suffices in 2×2.
  - Needs: EM-8.4.A
  - P3 · drills: la-eigenvector

### 8.5 Symmetric matrices and diagonalisation

Book: kreyszig-10e §8.3, §8.4

- ● **EM-8.5.A** Diagonalise a matrix with a full set of eigenvectors and use it to decouple a linear system.
  - EK: D = X⁻¹AX; symmetric A has real eigenvalues and orthogonal eigenvectors.
  - Needs: EM-8.4.B, EM-8.3.B
  - P3 · drills: em-diagonalise

### 8.6 Rank, orthogonality and least squares



- ● **EM-8.6.A** Find the rank of a matrix and the dimension of its null space.
  - EK: Rank + nullity = number of columns.
  - P3 · drills: la-rank-nullity, la-rank-3x3
- ● **EM-8.6.B** Project one vector onto another, test orthogonality, and take one Gram–Schmidt step.
  - EK: proj_u y = (y·u / u·u) u; subtracting it leaves the part orthogonal to u.
  - P3 · drills: la-projection-scalar, la-gram-schmidt-step, la-orthogonal-check
- ● **EM-8.6.C** Set up and solve a least-squares problem with the normal equations, and say what the solution means geometrically.
  - EK: AᵀA x̂ = Aᵀb; Ax̂ is the projection of b onto Col A.
  - P3 · P6 · drills: la-least-squares-slope, la-least-squares-facts
- ● **EM-8.6.D** Use eigenvalues to find powers and traces, know when a matrix is diagonalisable, and read a singular value.
  - EK: A^k has eigenvalues λ^k; symmetric matrices are always diagonalisable; σ = √(eigenvalue of AᵀA).
  - P3 · P6 · drills: la-trace-of-power, la-diagonalizable-facts, la-singular-value

## Unit 9 · Fourier series and Sturm–Liouville boundary-value problems

Big ideas: EIG, TRANS, LIN

### 9.1 Fourier series

Book: kreyszig-10e §11.1, §11.2

- ● **EM-9.1.A** (webwork-opl:CA7.20, webwork-opl:DE8.7) Compute the Fourier coefficients of a 2π-periodic function given on one period.
  - EK: a₀ = (1/2π)∫f, a_n = (1/π)∫f cos nx, b_n = (1/π)∫f sin nx over (−π, π).
  - Needs: EM-1.1.B
  - P3 · drills: fs-step, fs-sawtooth, fs-parabola, fs-abs
- ● **EM-9.1.B** (webwork-opl:CA7.20, webwork-opl:DE8.7) Compute the Fourier series of a function of period 2L, using even/odd symmetry to skip coefficients.
  - EK: Replace nx by nπx/L and 1/π by 1/L; even ⇒ cosine series, odd ⇒ sine series.
  - P2 · P3 · drills: fs-period-2l
- ● **EM-9.1.C** (webwork-opl:CA7.20) Write the half-range sine or cosine expansion of a function on (0, L).
  - EK: Odd extension ⇒ sine series; even extension ⇒ cosine series; b_n = (2/L)∫₀ᴸ f sin(nπx/L).
  - P3 · drills: fs-half-range
- ● **EM-9.1.D** Find the periodic steady-state response of an oscillator to a periodic non-sinusoidal force by Fourier series.
  - EK: Solve term by term; the term with nω nearest ω₀ dominates.
  - Needs: EM-9.1.A, EM-3.6.A
  - P3 · P6 · drills: em-fourier-forced-response

### 9.2 Sturm–Liouville problems

Book: kreyszig-10e §11.5

- ● **EM-9.2.A** Rewrite a second-order eigenvalue ODE in Sturm–Liouville form and identify p, q and r.
  - EK: (py′)′ + (q + λr)y = 0; multiply by the integrating factor e^(∫a₁/a₂)/a₂ when needed.
  - P2 · drills: sl-form
- ● **EM-9.2.B** Classify a Sturm–Liouville problem as regular, periodic or singular.
  - EK: Regular: p > 0, r > 0 on [a, b] with separated BCs; periodic: y(a) = y(b), y′(a) = y′(b); singular: p vanishes at an end.
  - Needs: EM-9.2.A
  - P2 · drills: sl-classify
- ● **EM-9.2.C** (webwork-opl:DE3.10) Find the eigenvalues of y″ + λy = 0 under Dirichlet, Neumann or mixed boundary conditions.
  - EK: Check λ < 0, = 0, > 0 separately; Dirichlet on [0, L]: λ = (nπ/L)², n ≥ 1.
  - P3 · P4 · drills: sl-eigenvalues
- ● **EM-9.2.D** Find the eigenfunction belonging to each eigenvalue.
  - EK: Determined up to a constant multiple; sin(nπx/L), cos(nπx/L) or sin((2n−1)πx/2L).
  - Needs: EM-9.2.C
  - P4 · drills: sl-eigenfunctions
- ● **EM-9.2.E** Find the eigenvalues and eigenfunctions of a shifted problem y″ + (λ + c)y = 0 and count its negative eigenvalues.
  - EK: Set μ = λ + c, solve as 9.2.C, then λ = μ − c.
  - Needs: EM-9.2.C
  - P3 · P4 · drills: sl-shift-eigenvalues, sl-shift-eigenfunctions, sl-shift-negative

### 9.3 Orthogonality and eigenfunction expansions

Book: kreyszig-10e §11.5, §11.6

- ● **EM-9.3.A** Verify orthogonality of eigenfunctions with respect to the weight r(x).
  - EK: ∫ₐᵇ r y_m y_n dx = 0 for m ≠ n in a regular or periodic S–L problem.
  - P5 · drills: em-orthogonality
- ● **EM-9.3.B** Expand a function in a generalised Fourier series of S–L eigenfunctions (e.g. Legendre or Fourier–Bessel).
  - EK: a_n = ∫ r f y_n dx / ∫ r y_n² dx.
  - Needs: EM-9.3.A
  - P3 · drills: em-legendre-expansion

## Unit 10 · Partial differential equations

Big ideas: EIG, TRANS, MODEL

### 10.1 Basic concepts, classification and separation

Book: kreyszig-10e §12.1, §12.3

- ● **EM-10.1.A** (webwork-opl:DE1.2, webwork-opl:DE8.1, webwork-opl:DE8.2) Classify a second-order linear PDE as elliptic, parabolic or hyperbolic and verify a solution.
  - EK: Au_xx + 2Bu_xy + Cu_yy: AC − B² > 0 elliptic, = 0 parabolic, < 0 hyperbolic.
  - P2 · drills: pde-classify, pde-verify
- ● **EM-10.1.B** Substitute u = X(x)T(t) (or X(x)Y(y)), split into two ODEs with a separation constant, and decide the constant's sign from the boundary conditions.
  - EK: Only the sign that gives sines and cosines can meet two zero boundary conditions nontrivially.
  - Needs: EM-3.1.A
  - P2 · drills: mt-separate, mt-sign-of-constant, mt-ode-solution

### 10.2 Heat equation by separation of variables

Book: kreyszig-10e §12.5, §12.6

- ● **EM-10.2.A** Separate u = F(x)G(t) in the heat equation and find each mode's decay rate.
  - EK: F″ + kF = 0 (an S–L problem), G′ + c²kG = 0 ⇒ G = e^(−c²λ_n t).
  - Needs: EM-9.2.C, EM-10.1.B
  - P2 · P3 · drills: pde-rates, mt-heat-time-constant
- ● **EM-10.2.D** Find the eigenvalues and eigenfunctions for Dirichlet, Neumann, mixed and convective (Robin) ends.
  - EK: Dirichlet sin(nπx/L); Neumann cos(nπx/L) with n = 0; mixed sin((2n−1)πx/2L); Robin: a transcendental condition such as λ tan λL = h.
  - Needs: EM-10.1.B
  - P2 · P3 · drills: mt-bc-eigenfunctions, mt-bc-kills, mt-eigenvalue, pde-eigen-condition
- ● **EM-10.2.E** Compute the Fourier sine or cosine coefficients of the initial condition.
  - EK: b_n = (2/L)∫ f sin(nπx/L) dx; a constant start has odd modes only, 4U/nπ.
  - Needs: EM-9.1.C, EM-10.2.D
  - P3 · drills: mt-coefficient-formula, mt-sine-coefficient-constant, mt-sine-coefficient-linear
- ● **EM-10.2.B** (webwork-opl:DE8.3) Solve the heat equation on a finite rod with Dirichlet or insulated ends by Fourier series.
  - EK: Dirichlet ⇒ sine series; insulated ⇒ cosine series with a constant term (the mean).
  - Needs: EM-10.2.A, EM-10.2.E
  - P3 · P4 · drills: pde-heat, pde-neumann, mt-solution-form, mt-read-coefficients, mt-insulated-steady-state
- ● **EM-10.2.C** (webwork-opl:DE8.3) Solve the heat equation with nonzero fixed ends by subtracting the steady state.
  - EK: u = u_s(x) + v; u_s linear; v satisfies zero BCs with v(x, 0) = f − u_s.
  - Needs: EM-10.2.B
  - P2 · P3 · drills: pde-steady, pde-shift-concepts, pde-steady-state-value, pde-shifted-initial-condition, pde-shifted-sine-coefficient
- ● **EM-10.2.F** Find the steady state with a flux or insulated end, and handle a flux boundary in the transient problem.
  - EK: −k u'(L) = q″ fixes the slope; with insulated ends the steady state is the initial mean.
  - Needs: EM-10.2.C
  - P2 · P3 · drills: pde-flux-end-steady-state
- ● **EM-10.2.G** Shift a boundary value that changes in time (w = x g(t)/L) and identify the source term it leaves in the equation.
  - EK: v = u − w has zero ends and v_t = k v_xx − w_t + k w_xx.
  - Needs: EM-10.2.C
  - P2 · drills: pde-time-bc-shift
- ● **EM-10.2.H** (webwork-opl:DE8.8) Solve the heat equation with a source: steady state from k u_s″ = −Q, transient by expanding the source in the eigenfunctions.
  - EK: Both ends zero: u_s = Qx(L − x)/2k; each mode obeys T_n′ + λ_n T_n = q_n.
  - Needs: EM-10.2.C, EM-10.2.E
  - P3 · drills: pde-source-steady, pde-source-mode

### 10.3 Wave equation

Book: kreyszig-10e §12.2, §12.3, §12.4

- ● **EM-10.3.A** (webwork-opl:DE8.4) Solve the vibrating string by separation of variables and Fourier series.
  - EK: u = Σ(B_n cos λ_n t + B_n* sin λ_n t) sin(nπx/L), λ_n = cnπ/L.
  - Needs: EM-9.1.C, EM-10.2.D
  - P3 · P4 · drills: pde-wave, mt-string-frequency, mt-string-time-factor
- ● **EM-10.3.B** (webwork-opl:DE8.4) Write d'Alembert's solution for an infinite string from initial displacement and velocity.
  - EK: u = ½[f(x + ct) + f(x − ct)] + (1/2c)∫ g.
  - P3 · drills: dalembert-displacement, dalembert-velocity

### 10.4 Laplace's equation and other geometries

Book: kreyszig-10e §12.6, §12.10, §12.11

- ● **EM-10.4.A** (webwork-opl:DE8.5) Solve the steady 2-D Dirichlet problem on a rectangle by separation, one nonzero side at a time.
  - EK: The direction with two zero sides oscillates (sines); the other carries sinh or cosh; superpose one problem per nonzero side.
  - Needs: EM-10.2.D
  - P3 · drills: laplace-rect-modes, laplace-rect-coef, mt-which-variable-oscillates, mt-other-direction, pde-laplace-nonzero-sides
- ● **EM-10.4.B** (webwork-opl:DE8.6) Separate a PDE in polar, cylindrical or spherical coordinates and identify the Bessel or Legendre equation that appears.
  - EK: Radial part in cylinders ⇒ Bessel; polar angle in spheres ⇒ Legendre in cos θ.
  - Needs: EM-6.4.A
  - P2 · drills: em-separation-coordinates, ~spec-identify
- ● **EM-10.4.C** Solve transient conduction in a cylinder with Fourier–Bessel series, including a nonzero wall temperature by shifting.
  - EK: u = ΣA_nJ₀(α_nr/a)e^(−k(α_n/a)²t); weight r; uniform start A_n = 2U/(α_nJ₁(α_n)).
  - Needs: EM-10.4.B, EM-9.3.B
  - P3 · drills: mt-bessel-condition, mt-bessel-weight, mt-bessel-decay-length, pde-cylinder-wall
- ● **EM-10.4.D** Solve transient conduction in a sphere with v = r·u, which turns it into a rod.
  - EK: v_t = kv_rr, v(0) = v(a) = 0; u = Σ B_n sin(nπr/a)e^(−k(nπ/a)²t)/r.
  - Needs: EM-10.4.B, EM-10.2.B
  - P3 · drills: pde-sphere

### 10.5 Transform methods for PDEs

Book: kreyszig-10e §12.7, §12.12

- ● **EM-10.5.A** Solve a PDE on a semi-infinite or infinite domain by Laplace or Fourier transform.
  - EK: Transform out t (Laplace) or x (Fourier) to get an ODE in the other variable; bounded at infinity keeps e^(−√s x).
  - Needs: EM-7.1.A
  - P3 · drills: em-semi-infinite-heat, pde-lt-steps, pde-lt-decay-rate, pde-lt-erfc-value
- ● **EM-10.5.B** (webwork-opl:CX8.5) Solve a finite rod by Laplace transform and invert by residues: the poles are the eigenvalues.
  - EK: Residue at s = 0 is the steady state; s_n = −(nπ/L)² rebuild the Fourier series.
  - Needs: EM-10.5.A, EM-10.2.B
  - P3 · P4 · drills: pde-lt-finite-rod-amplitude, pde-lt-pole-is-eigenvalue, pde-lt-residues
- ● **EM-10.5.C** Choose the method for a PDE problem: separation, shift, transform or numerics.
  - EK: Finite domain with homogeneous BCs: separate. Nonzero BCs: shift first. Semi-infinite: transform. Messy geometry or data: finite differences.
  - Needs: EM-10.5.B, EM-10.2.C
  - P2 · drills: pde-method-choice

### 10.6 Finite differences for PDEs

Book: kreyszig-10e §21.4, §21.6

- ● **EM-10.6.A** Write central-difference approximations and state their truncation order.
  - EK: u_xx ≈ (u_{i+1} − 2u_i + u_{i−1})/h², O(h²); forward difference is O(h).
  - P2 · drills: mt-central-second-difference, mt-truncation-order
- ● **EM-10.6.B** Take an explicit time step and check stability.
  - EK: u_i^{n+1} = u_i + r(u_{i+1} − 2u_i + u_{i−1}), stable for r = kΔt/h² ≤ ½.
  - Needs: EM-10.6.A
  - P3 · P5 · drills: mt-explicit-step, mt-explicit-stability, mt-amplification
- ● **EM-10.6.C** Handle a flux or insulated boundary with a ghost node.
  - EK: u_{−1} = u_1 − 2h g from the central difference of u_x(0) = g.
  - Needs: EM-10.6.B
  - P3 · drills: pde-fd-ghost
- ● **EM-10.6.D** Take an implicit or Crank–Nicolson step by solving the tridiagonal system.
  - EK: θ = 1 backward Euler, θ = ½ Crank–Nicolson; unconditionally stable; Thomas algorithm.
  - Needs: EM-10.6.B, EM-8.1.A
  - P3 · P4 · drills: pde-fd-implicit

## Unit 11 · Fourier integrals and transforms (extension)

Big ideas: TRANS

### 11.1 Fourier integral and transforms

Book: kreyszig-10e §11.7, §11.8, §11.9

- ● **EM-11.1.A** Represent a non-periodic function by its Fourier integral, or its cosine or sine transform.
  - EK: Limit L → ∞ of the Fourier series; even ⇒ cosine transform, odd ⇒ sine.
  - P3 · drills: em-fourier-cosine-sine
- ● **EM-11.1.B** Compute a Fourier transform and use its derivative property to turn an ODE into algebra.
  - EK: F{f′} = iwF{f}; F{e^(−ax²)} is Gaussian.
  - P3 · drills: em-fourier-transform-value, em-fourier-derivative-rule

## Unit 12 · Vector calculus for transport (extension)

Big ideas: MODEL

### 12.1 Grad, div, curl and the integral theorems

Book: kreyszig-10e §9.7, §9.8, §9.9, §10.7, §10.9

- ● **EM-12.1.A** Compute the gradient, divergence, curl and Laplacian of a field in Cartesian coordinates.
  - EK: ∇f, ∇·v, ∇×v, ∇²f = ∇·∇f.
  - P3 · drills: cm-gradient, cm-div-curl, cm-laplacian, ~mv-partial
- ● **EM-12.1.B** (webwork-opl:FM4.2) Derive a differential conservation equation from an integral balance with the divergence theorem.
  - EK: ∭∇·F dV = ∯F·n dA ⇒ ∂c/∂t + ∇·N = R.
  - P1 · drills: ca-conservation-law

## Unit 13 · More on ODEs: circuits, bifurcations, operators, existence

Big ideas: MODEL

### 13.1 Applications and theory



- ● **EM-13.1.A** (webwork-opl:DE2.9) Solve an RC circuit.
  - EK: R q′ + q/C = E: the charge rises with time constant RC and the current decays.
  - P1 · drills: em-rc-current
- ● **EM-13.1.B** (webwork-opl:DE2.14) Locate a saddle-node bifurcation.
  - EK: Equilibria appear or vanish where f(y) = 0 and f′(y) = 0 together.
  - P1 · drills: em-bifurcation
- ● **EM-13.1.C** (webwork-opl:DE3.12) Apply a differential operator.
  - EK: L[e^{kx}] = p(k)e^{kx} for L = p(D) with constant coefficients.
  - P1 · drills: em-operator-exponential
- ● **EM-13.1.D** (webwork-opl:DE3.13) Find the interval on which a linear IVP is guaranteed a unique solution.
  - EK: The largest open interval around x₀ on which all coefficients are continuous.
  - P1 · drills: em-existence-interval
- ● **EM-13.1.E** (webwork-opl:DE5.2) Verify that a vector function solves a linear system.
  - EK: x = e^{λt}v solves x′ = Ax exactly when Av = λv.
  - P1 · drills: em-system-verify

## Unit 14 · Complex analysis

Big ideas: MODEL

### 14.1 Complex equations, regions and functions



- ● **EM-14.1.A** (webwork-opl:CX2.1) Solve a linear equation in z.
  - EK: Divide by multiplying top and bottom by the conjugate.
  - P1 · drills: em-complex-linear
- ● **EM-14.1.B** (webwork-opl:CX2.3) Solve a nonlinear equation in z.
  - EK: Write the right side in polar form; z² = w has two roots ±√w.
  - P1 · drills: em-complex-sqrt
- ● **EM-14.1.C** (webwork-opl:CX3.1) Decide whether a point lies in a region of the plane.
  - EK: |z − z₀| < r is the open disc of radius r about z₀.
  - P1 · drills: em-complex-region
- ● **EM-14.1.D** (webwork-opl:CX4.1) Find the image of a point under a complex map.
  - EK: w = z² squares the modulus and doubles the argument.
  - P1 · drills: em-complex-map
- ● **EM-14.1.E** (webwork-opl:CX4.2) Evaluate a limit of a complex function.
  - EK: A complex limit must agree from every direction; algebra works as for real limits.
  - P1 · drills: em-complex-limit

### 14.2 Analytic functions



- ● **EM-14.2.A** (webwork-opl:CX5.1) Use the Cauchy–Riemann equations.
  - EK: f = u + iv is analytic where uₓ = v_y and u_y = −vₓ.
  - P1 · drills: em-cauchy-riemann
- ● **EM-14.2.B** (webwork-opl:CX5.2) Test whether a function is harmonic.
  - EK: u is harmonic when u_xx + u_yy = 0; real parts of analytic functions are.
  - P1 · drills: em-harmonic
- ● **EM-14.2.C** (webwork-opl:CX5.3) Recognise entire functions.
  - EK: Entire = analytic at every point of the plane.
  - P1 · drills: em-entire
- ● **EM-14.2.D** (webwork-opl:CX5.4) Find a harmonic conjugate.
  - EK: Integrate v_y = uₓ in y, then fix the function of x with vₓ = −u_y.
  - P1 · drills: em-harmonic-conjugate

### 14.3 Integration and series



- ● **EM-14.3.A** (webwork-opl:CX7.1) Use Cauchy's integral formula.
  - EK: ∮ f(z)/(z − z₀) dz = 2πi f(z₀) for z₀ inside the contour and f analytic.
  - P1 · drills: em-cauchy-formula
- ● **EM-14.3.B** (webwork-opl:CX8.1) Decide whether a complex sequence converges.
  - EK: zⁿ → 0 when |z| < 1 and diverges when |z| > 1.
  - P1 · drills: em-complex-sequence
- ● **EM-14.3.C** (webwork-opl:CX8.2) Find a Taylor coefficient of an analytic function.
  - EK: e^{az} = Σ aᵏ zᵏ / k!; 1/(1 − az) = Σ aᵏ zᵏ for |az| < 1.
  - P1 · drills: em-complex-taylor
- ● **EM-14.3.D** (webwork-opl:CX8.3, webwork-opl:CX8.5) Find a Laurent coefficient (a residue).
  - EK: The coefficient of 1/(z − z₀) is the residue.
  - P1 · drills: em-laurent-residue
- ● **EM-14.3.E** (webwork-opl:CX8.4) Find the order of a zero.
  - EK: The order is the power of the first nonzero term of the Taylor series.
  - P1 · drills: em-zero-order

## Drills not yet placed on the map

- ca2-u-sub-choice (calc.u-sub)
- mm-coverup-two (calc.partial-fractions)
- mm-coverup-three (calc.partial-fractions)
- mm-coverup-repeated (calc.partial-fractions)
- mm-coverup-quadratic (calc.partial-fractions)
- ca-complex-modulus-power (calc.complex-euler)
- ca-complex-root-real-part (calc.complex-euler)
- mvd-partial (calc.multivariable)
- mvd-mixed (calc.multivariable)
- mvd-chain-t (calc.multivariable)
- mvd-chain-partial (calc.multivariable)
- mvd-implicit (calc.multivariable)
- mvd-two-path (calc.multivariable)
- mvd-implicit-3 (calc.multivariable)
- la-solution-type (la.row-reduction)
- la-free-variables (la.row-reduction)
- la-is-solution (la.row-reduction)
- la-inconsistent-h (la.row-reduction)
- la-min-free-vars (la.row-reduction)
- la-solution-set-dim (la.row-reduction)
- la-independence-parameter (la.independence)
- la-indep-det (la.independence)
- la-indep-count (la.independence)
- la-poly-dependence (la.independence)
- la-poly-dependent-k (la.independence)
- la-solve-with-inverse (la.inverse)
- la-inverse-check (la.inverse)
- la-invertible-matrix-theorem (la.inverse)
- la-transpose-inverse (la.inverse)
- la-imt-consequence (la.inverse)
- hs2-inverse-2x2 (la.inverse)
- la-elementary-inverse (la.inverse)
- la-elementary-power (la.inverse)
- la-det-triangular (la.determinant)
- la-complex-det (la.determinant)
- la-complex-det-modulus (la.determinant)
- la-eigen-triangular (la.eigenvalues)
- la-complex-eigen-modulus (la.eigenvalues)
- mm-eigen-trace-det (la.eigenvalues)
- mm-trace-of-square (la.eigenvalues)
- la-row-space-reverse (la.rank)
- la-distance (la.orthogonality)
- la-orthogonal-complement (la.orthogonality)
- la-qr-entry (la.orthogonality)
- la-cos-angle (la.orthogonality)
- la-perp-h (la.orthogonality)
- la-qr-r11 (la.orthogonality)
- la-function-inner-product (la.orthogonality)
- la-orthogonal-shift (la.orthogonality)
- la-orthogonal-inverse (la.orthogonality)
- la-orthogonal-norm (la.orthogonality)
- la-lsq-slope (la.least-squares)
- la-lsq-residual-sum (la.least-squares)
- la-pinv-entry (la.least-squares)
- la-pinv-diag (la.least-squares)
- la-symmetric-eigenvector (la.diagonalization)
- la-symmetric-larger-eig (la.diagonalization)
- la-jordan-power (la.diagonalization)
- la-jordan-exp (la.diagonalization)
- la-span-membership (la.span)
- la-solution-set-shape (la.span)
- la-span-dim (la.span)
- la-span-shape (la.span)
- la-span-h (la.span)
- la-poly-combination (la.span)
- la-poly-combo-2 (la.span)
- la-poly-span (la.span)
- la-poly-span-h (la.span)
- la-balance-combustion (la.span)
- la-oxygen-coefficient (la.span)
- la-product-entry (la.matrix-ops)
- la-product-size (la.matrix-ops)
- la-square-entry (la.matrix-ops)
- la-multiplication-count (la.matrix-ops)
- la-lu-pivot (la.lu)
- la-lu-forward (la.lu)
- la-det-from-lu (la.lu)
- la-forward-step (la.lu)
- la-det-properties (la.det-properties)
- la-det-row-ops (la.det-properties)
- la-det-area (la.det-properties)
- la-det-combo (la.det-properties)
- la-det-before-ops (la.det-properties)
- la-triangle-area-det (la.det-properties)
- la-subspace-test (la.subspaces)
- la-span-dimension (la.subspaces)
- la-subspace-which (la.subspaces)
- la-span-dim-3 (la.subspaces)
- la-is-vector-space (la.subspaces)
- la-axiom-fails (la.subspaces)
- la-space-dimension (la.subspaces)
- la-special-dim (la.subspaces)
- la-coordinates (la.coordinates)
- la-change-of-basis (la.coordinates)
- la-orthogonal-coordinates (la.coordinates)
- la-coords-to-standard-3 (la.coordinates)
- la-map-from-basis-images (la.transformations)
- la-composition (la.transformations)
- la-one-to-one-onto (la.transformations)
- la-kernel-dimension (la.transformations)
- la-matrix-relative-to-basis (la.transformations)
- la-operator-eigen (la.transformations)
- la-derivative-nilpotent (la.transformations)
- la-rotate-point (la.transformations)
- la-composition-order (la.transformations)
- la-rank-onto (la.transformations)
- la-derivative-range (la.transformations)
- la-shift-matrix-entry (la.transformations)
- la-map-inverse (la.transformations)
- la-poly-map-inverse (la.transformations)
- la-markov-steady-state (la.eigen-applications)
- la-power-by-eigenvectors (la.eigen-applications)
- la-det-power (la.eigen-applications)
- la-markov-two-step (la.eigen-applications)
- la-rotation-angle (la.eigen-applications)
- la-quadratic-form-classify (la.quadratic-forms)
- la-quadratic-form-max (la.quadratic-forms)
- la-form-min-eig (la.quadratic-forms)
- la-form-max-radius (la.quadratic-forms)
- la-condition-number (la.svd)
- la-rank-one-singular-value (la.svd)
- la-rank1-error (la.svd)
- la-frob-error (la.svd)
- la-cond-diag (la.svd)
- mm-damping-class (ode2.characteristic)
- mm-particular-form (ode2.undetermined)
- ca-lim-substitute (calc.limits)
- ca-lim-quotient (calc.limits)
- ca-lim-factor (calc.limits)
- ca-lim-conjugate (calc.limits)
- ca-lim-trig (calc.limits)
- ca-lim-squeeze (calc.limits)
- ca-lim-infinity (calc.limits)
- ca-lim-infinity-radical (calc.limits)
- ca-secant-to-tangent (calc.limits)
- ca-limit-from-formula (calc.limits)
- ca-limit-table-reverse (calc.limits)
- ca-squeeze-bounds (calc.limits)
- ca2-onesided-exists (calc.limits)
- ca2-trig-limit (calc.limits)
- ca2-asymptote-count (calc.limits)
- ca2-one-to-infinity (calc.limits)
- mm-limit-at-infinity (calc.limits)
- mm-asymptote (calc.limits)
- mm-removable-limit (calc.limits)
- mm-horizontal-asymptote (calc.limits)
- ca-limit-graph (calc.limits)
- ca-limit-table (calc.limits)
- ca-shrinking-average-rate (calc.limits)
- ca-limit-statement (calc.limits)
- ca-limit-three-ways (calc.limits)
- ca-limit-procedure (calc.limits)
- ca-lim-onesided (calc.continuity)
- ca-continuity-k (calc.continuity)
- ca-vert-asymptote (calc.continuity)
- ca-ivt (calc.continuity)
- ca-discontinuity-formula (calc.continuity)
- ca-piecewise-continuous-check (calc.continuity)
- ca-removable-value (calc.continuity)
- ca-ivt-applies (calc.continuity)
- ca-discontinuity-graph (calc.continuity)
- ca-make-continuous (calc.continuity)
- ca-continuity-conditions (calc.continuity)
- ca-avg-rate (calc.derivative-basics)
- ca-def-derivative (calc.derivative-basics)
- ca-tangent-line (calc.derivative-basics)
- ca-estimate-derivative (calc.derivative-basics)
- ca-avg-rate-table (calc.derivative-basics)
- ca-recognize-limit-derivative (calc.derivative-basics)
- ca-tangent-line-value (calc.derivative-basics)
- ca-corner-cusp-pick (calc.derivative-basics)
- dr-derivative-sketch (calc.derivative-basics)
- ca-difference-quotient-limit (calc.derivative-basics)
- ca-differentiability (calc.derivative-basics)
- ca2-linear-approx-root (calc.derivative-basics)
- ca-power-rule (calc.derivative-rules)
- ca-power-reciprocal (calc.derivative-rules)
- ca-power-root (calc.derivative-rules)
- ca-poly-derivative (calc.derivative-rules)
- ca-elementary-derivative (calc.derivative-rules)
- ca-product-rule (calc.derivative-rules)
- ca-product-exp (calc.derivative-rules)
- ca-product-values (calc.derivative-rules)
- ca-quotient-rule (calc.derivative-rules)
- ca-quotient-values (calc.derivative-rules)
- ca-trig-derivative (calc.derivative-rules)
- ca-derivative-at-point (calc.derivative-rules)
- ca-sin-limit-value (calc.derivative-rules)
- ca-trig-derivative-value (calc.derivative-rules)
- ca2-tangent-slope-where (calc.derivative-rules)
- ca2-higher-derivative (calc.derivative-rules)
- mm-derivative-at-a-point (calc.derivative-rules)
- mm-tangent-slope (calc.derivative-rules)
- mm-product-derivative (calc.derivative-rules)
- mm-tangent-intercept (calc.derivative-rules)
- ca-derive-sin-exp (calc.derivative-rules)
- ca-elasticity (calc.derivative-rules)
- ca-chain-power (calc.chain-rule)
- ca-chain-trig (calc.chain-rule)
- ca-chain-exp (calc.chain-rule)
- ca-chain-ln (calc.chain-rule)
- ca-chain-values (calc.chain-rule)
- ca-exp-base (calc.chain-rule)
- ca-rules-combined (calc.chain-rule)
- ca-log-diff (calc.chain-rule)
- ca-chain-at-point (calc.chain-rule)
- ca-exp-base-derivative (calc.chain-rule)
- mm-diff-linear-power (calc.chain-rule)
- mm-diff-sin-inner (calc.chain-rule)
- mm-diff-log-inner (calc.chain-rule)
- mm-diff-power-exp (calc.chain-rule)
- mm-inverse-derivative (calc.chain-rule)
- ca-implicit-slope (calc.implicit-inverse)
- ca-inverse-derivative (calc.implicit-inverse)
- ca-arctan-derivative (calc.implicit-inverse)
- ca-arcsin-derivative (calc.implicit-inverse)
- ca-second-derivative (calc.implicit-inverse)
- ca-second-derivative-trig (calc.implicit-inverse)
- ca-inverse-derivative-table (calc.implicit-inverse)
- ca-implicit-slope-point (calc.implicit-inverse)
- ca-implicit-concavity (calc.implicit-inverse)
- ca-implicit-second-derivative (calc.implicit-inverse)
- ca-implicit-horizontal (calc.implicit-inverse)
- ca-motion (calc.rates)
- ca-related-circle (calc.rates)
- ca-related-sphere (calc.rates)
- ca-related-ladder (calc.rates)
- ca-linearization (calc.rates)
- ca-linearization-error (calc.rates)
- ca-lhospital-exp (calc.rates)
- ca-lhospital-twice (calc.rates)
- ca-lhospital-power (calc.rates)
- ca-rate-interpret (calc.rates)
- ca-linearization-value (calc.rates)
- ca2-speeding-up (calc.rates)
- ca2-related-circle-radius (calc.rates)
- ca-rate-of-rate (calc.rates)
- ca-rate-units (calc.rates)
- ca2-related-rate-scaling (calc.rates)
- ca-marginal-cost (calc.rates)
- ca-mvt (calc.extrema)
- ca-critical-points (calc.extrema)
- ca-abs-extrema (calc.extrema)
- ca-inflection (calc.extrema)
- ca-second-derivative-test (calc.extrema)
- ca-optimization-fence (calc.extrema)
- ca-optimization-box (calc.extrema)
- ca-evt-guarantee (calc.extrema)
- ca-second-deriv-at-critical (calc.extrema)
- ca-abs-max-value (calc.extrema)
- ca-concavity-from-fpp (calc.extrema)
- ca-ftc-g-prime (calc.extrema)
- ca2-mvt-c (calc.extrema)
- ca2-second-test (calc.extrema)
- mm-critical-value (calc.extrema)
- mm-quadratic-maximum (calc.extrema)
- mm-inflection (calc.extrema)
- mm-max-product (calc.extrema)
- ca-read-derivative-graph (calc.extrema)
- ca-sketch-derivative (calc.extrema)
- ca-decreasing-interval (calc.extrema)
- ca-optimization-setup (calc.extrema)
- ca2-concavity-meaning (calc.extrema)
- ca-max-profit (calc.extrema)
- ca-peak-concentration (calc.extrema)
- ca-riemann-sums (calc.riemann-ftc)
- ca-trapezoid-table (calc.riemann-ftc)
- ca-ftc-derivative (calc.riemann-ftc)
- ca-integral-properties (calc.riemann-ftc)
- ca-definite-poly (calc.riemann-ftc)
- ca-net-change-ftc (calc.riemann-ftc)
- ca-net-change-rate (calc.riemann-ftc)
- ca-riemann-left-right (calc.riemann-ftc)
- ca2-riemann-direction (calc.riemann-ftc)
- ca2-integral-properties (calc.riemann-ftc)
- mm-definite-integral (calc.riemann-ftc)
- mm-average-value (calc.riemann-ftc)
- ca-accumulation-graph (calc.riemann-ftc)
- ca-riemann-limit (calc.riemann-ftc)
- ca-riemann-over-under (calc.riemann-ftc)
- ca2-integral-by-area (calc.riemann-ftc)
- ca2-symmetry-integral (calc.riemann-ftc)
- ca2-ftc-derivative (calc.riemann-ftc)
- ca-antiderivative-poly (calc.antiderivatives)
- ca-antiderivative-elementary (calc.antiderivatives)
- ca-antiderivative-root (calc.antiderivatives)
- ca-usub-definite (calc.antiderivatives)
- ca-arctan-integral (calc.antiderivatives)
- ca-long-division-integral (calc.antiderivatives)
- ca-improper-power (calc.antiderivatives)
- ca-improper-exp (calc.antiderivatives)
- ca-improper-ptest (calc.antiderivatives)
- ca-u-sub-value (calc.antiderivatives)
- mm-int-cos-kx (calc.antiderivatives)
- mm-int-sin-kx (calc.antiderivatives)
- mm-int-exp-kx (calc.antiderivatives)
- mm-int-linear-power (calc.antiderivatives)
- mm-int-reciprocal-linear (calc.antiderivatives)
- mm-int-log-form (calc.antiderivatives)
- mm-int-x-exp-square (calc.antiderivatives)
- mm-int-sin-power-cos (calc.antiderivatives)
- ca-choose-technique (calc.antiderivatives)
- ca-trig-integral (calc.antiderivatives)
- ca-trig-substitution (calc.antiderivatives)
- ca-integral-table (calc.antiderivatives)
- ca-cas-antiderivative (calc.antiderivatives)
- ca-verify-solution (calc.diffeq)
- ca-separable-general (calc.diffeq)
- ca-separable-ivp (calc.diffeq)
- ca-exponential-growth (calc.diffeq)
- ca-half-life (calc.diffeq)
- ca-newton-cooling (calc.diffeq)
- ca-logistic (calc.diffeq)
- ca-de-verify-solution (calc.diffeq)
- ca-slope-field-equilibrium (calc.diffeq)
- ca-slope-field-feature (calc.diffeq)
- ca-euler-vs-exact (calc.diffeq)
- ca-separable-constant (calc.diffeq)
- ca-ivp-domain (calc.diffeq)
- ca2-exponential-solution-k (calc.diffeq)
- ca2-logistic-k (calc.diffeq)
- ca-slope-field-points (calc.diffeq)
- ca-write-de (calc.diffeq)
- ca-average-value (calc.integration-apps)
- ca-distance (calc.integration-apps)
- ca-net-change-tank (calc.integration-apps)
- ca-area-between (calc.integration-apps)
- ca-area-between-y (calc.integration-apps)
- ca-volume-squares (calc.integration-apps)
- ca-volume-semicircles (calc.integration-apps)
- ca-volume-disc (calc.integration-apps)
- ca-volume-washer (calc.integration-apps)
- ca-arc-length (calc.integration-apps)
- ca-work-spring (calc.integration-apps)
- ca-net-vs-total (calc.integration-apps)
- ca-area-x-vs-y (calc.integration-apps)
- ca-area-two-curves (calc.integration-apps)
- ca-cross-section-triangles (calc.integration-apps)
- ca-cross-section-squares-y (calc.integration-apps)
- ca-disc-about-axis (calc.integration-apps)
- ca-washer-setup (calc.integration-apps)
- ca-washer-about-line-above (calc.integration-apps)
- ca-arc-length-line (calc.integration-apps)
- ca-pumping-work (calc.integration-apps)
- ca2-turn-time (calc.integration-apps)
- ca2-area-reverse (calc.integration-apps)
- ca2-shell-volume (calc.integration-apps)
- ca-area-crossings (calc.integration-apps)
- ca-volume-disc-line (calc.integration-apps)
- ca-volume-washer-line (calc.integration-apps)
- ca2-average-value (calc.integration-apps)
- ca-consumer-surplus (calc.integration-apps)
- ca-cardiac-output (calc.integration-apps)
- ca-pdf-constant (calc.integration-apps)
- ca-shells (calc.integration-apps)
- ca-two-methods (calc.integration-apps)
- ca-surface-revolution (calc.integration-apps)
- ca-hydrostatic-triangle (calc.integration-apps)
- ca-parametric-slope (calc.parametric-polar)
- ca-parametric-arc (calc.parametric-polar)
- ca-vector-velocity (calc.parametric-polar)
- ca-vector-position (calc.parametric-polar)
- ca-polar-convert (calc.parametric-polar)
- ca-polar-slope (calc.parametric-polar)
- ca-polar-area (calc.parametric-polar)
- ca-polar-rose (calc.parametric-polar)
- ca-parametric-horizontal (calc.parametric-polar)
- ca-parametric-concavity (calc.parametric-polar)
- ca-speed-parametric (calc.parametric-polar)
- ca-vector-acceleration (calc.parametric-polar)
- ca-displacement-vector (calc.parametric-polar)
- ca-rect-to-polar (calc.parametric-polar)
- ca-polar-area-petal (calc.parametric-polar)
- ca-polar-slope-reason (calc.parametric-polar)
- ca-planar-distance (calc.parametric-polar)
- ca-polar-between (calc.parametric-polar)
- ca-eliminate-parameter (calc.parametric-polar)
- ca-parametric-area (calc.parametric-polar)
- ca-parametric-volume (calc.parametric-polar)
- ca-parametric-surface (calc.parametric-polar)
- ca-polar-arc-length (calc.parametric-polar)
- ca-partial-sums (calc.series)
- ca-geometric-series (calc.series)
- ca-nth-term-test (calc.series)
- ca-p-series (calc.series)
- ca-ratio-test (calc.series)
- ca-absolute-conditional (calc.series)
- ca-alternating-error (calc.series)
- ca-telescoping-sum (calc.series)
- ca-geometric-sum (calc.series)
- ca-p-series-pick (calc.series)
- ca-limit-comparison-ratio (calc.series)
- ca-alternating-converge-pick (calc.series)
- ca-alternating-terms-needed (calc.series)
- ca2-p-series-pick (calc.series)
- ca2-ratio-limit (calc.series)
- ca-alternating-series-test (calc.series)
- ca-integral-test (calc.series)
- ca-comparison-test (calc.series)
- ca2-geometric-series-sum (calc.series)
- ca-sequence-limit (calc.series)
- ca-root-test (calc.series)
- ca-series-strategy (calc.series)
- ca-taylor-exp (calc.taylor)
- ca-taylor-ln (calc.taylor)
- ca-taylor-coefficients (calc.taylor)
- ca-lagrange-bound (calc.taylor)
- ca-radius-convergence (calc.taylor)
- ca-lagrange-degree (calc.taylor)
- ca-radius-ratio (calc.taylor)
- ca-series-coefficient (calc.taylor)
- ca2-maclaurin-coefficient (calc.taylor)
- ca-series-use (calc.taylor)
- ca-series-build (calc.taylor)
- ca-series-general-term (calc.taylor)
- ca2-taylor-coefficient (calc.taylor)
- cm-unit-vector-component (calc.vectors-3d)
- cm-projection-length (calc.vectors-3d)
- cm-triangle-area (calc.vectors-3d)
- cm-line-distance-point (calc.vectors-3d)
- cm-plane-distance (calc.vectors-3d)
- ca-quadric-traces (calc.vectors-3d)
- cm-curve-speed (calc.vectors-3d)
- cm-circle-curvature (calc.vectors-3d)
- cm-distance-3d (calc.vectors-3d)
- cm-dot-product (calc.vectors-3d)
- cm-cross-product (calc.vectors-3d)
- cm-line-plane-hit (calc.vectors-3d)
- cm-plane (calc.vectors-3d)
- cm-vector-function (calc.vectors-3d)
- cm-helix (calc.vectors-3d)
- ca-quadric (calc.vectors-3d)
- ca-vector-limit (calc.vectors-3d)
- ca-critical-point-classify (calc.partials-apps)
- cm-tangent-plane (calc.partials-apps)
- cm-chain-rule (calc.partials-apps)
- cm-critical-point (calc.partials-apps)
- cm-lagrange-product (calc.partials-apps)
- cm-lagrange-circle (calc.partials-apps)
- mvd-directional (calc.partials-apps)
- mvd-max-rate (calc.partials-apps)
- mvd-level-slope (calc.partials-apps)
- mvd-linearize (calc.partials-apps)
- mvd-tangent-plane-implicit (calc.partials-apps)
- mvd-classify (calc.partials-apps)
- mvd-critical-count (calc.partials-apps)
- mvd-lagrange (calc.partials-apps)
- mvd-gradient-facts (calc.partials-apps)
- mvd-lagrange-two (calc.partials-apps)
- ca-domain-level-curve (calc.partials-apps)
- ca-level-curve-shape (calc.partials-apps)
- ca-two-path-limit (calc.partials-apps)
- ca-extrema-region (calc.partials-apps)
- cm-double-integral-order (calc.multiple-integrals)
- cm-double-rect (calc.multiple-integrals)
- cm-double-region (calc.multiple-integrals)
- cm-reverse-order (calc.multiple-integrals)
- cm-double-polar (calc.multiple-integrals)
- cm-gaussian-polar (calc.multiple-integrals)
- cm-center-of-mass (calc.multiple-integrals)
- cm-tetrahedron (calc.multiple-integrals)
- cm-cylindrical (calc.multiple-integrals)
- cm-spherical (calc.multiple-integrals)
- cm-jacobian (calc.multiple-integrals)
- mvd-region-setup (calc.multiple-integrals)
- mvd-reverse-setup (calc.multiple-integrals)
- mvd-region-value (calc.multiple-integrals)
- mvd-polar-setup (calc.multiple-integrals)
- mvd-polar-value (calc.multiple-integrals)
- mvd-coordinates (calc.multiple-integrals)
- mvd-jacobian (calc.multiple-integrals)
- mvd-triple-setup (calc.multiple-integrals)
- mvd-triple-value (calc.multiple-integrals)
- mvd-center-mass (calc.multiple-integrals)
- mvd-change-variables (calc.multiple-integrals)
- mvd-triple-order (calc.multiple-integrals)
- mvd-average (calc.multiple-integrals)
- mvd-center-mass-solid (calc.multiple-integrals)
- mvd-inertia (calc.multiple-integrals)
- ca-gradient-field-check (calc.vector-calculus)
- ca-continuity-1d (calc.vector-calculus)
- cm-line-integral-scalar (calc.vector-calculus)
- cm-work-line (calc.vector-calculus)
- cm-potential (calc.vector-calculus)
- cm-green (calc.vector-calculus)
- cm-surface-area (calc.vector-calculus)
- cm-surface-integral (calc.vector-calculus)
- cm-flux-disc (calc.vector-calculus)
- cm-stokes (calc.vector-calculus)
- cm-divergence-theorem (calc.vector-calculus)
- mvd-conservative (calc.vector-calculus)
- mvd-potential-work (calc.vector-calculus)
- mvd-work (calc.vector-calculus)
- mvd-scalar-line (calc.vector-calculus)
- mvd-green (calc.vector-calculus)
- mvd-flux-plane (calc.vector-calculus)
- mvd-div-curl (calc.vector-calculus)
- mvd-div-curl-facts (calc.vector-calculus)
- mvd-surface-integral (calc.vector-calculus)
- mvd-flux (calc.vector-calculus)
- mvd-divergence-theorem (calc.vector-calculus)
- mvd-stokes (calc.vector-calculus)
- mvd-orientation (calc.vector-calculus)
- mvd-which-theorem (calc.vector-calculus)
- mvd-work-space (calc.vector-calculus)
- mvd-green-area (calc.vector-calculus)
- mvd-divergence-curved (calc.vector-calculus)
- mvd-stokes-surface (calc.vector-calculus)
- ca-vector-field-match (calc.vector-calculus)
- ca-curl-conservative (calc.vector-calculus)
