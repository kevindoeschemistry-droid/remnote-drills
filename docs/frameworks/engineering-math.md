# Applied Engineering Mathematics — curriculum framework (draft 1)

Generated from `drills/frameworks/engineering-math.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**118 learning objectives** in 12 units (114 core): 93 drilled, 4 partly, 21 with no drills. Core: 93 / 114 drilled.

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
| 2 · First-order ODEs | core | 15–20% | 17 | 12 | 0 | 5 |
| 3 · Second-order linear ODEs | core | 20–25% | 18 | 16 | 0 | 2 |
| 4 · Higher-order linear ODEs | core | 5% | 4 | 3 | 1 | 0 |
| 5 · Systems of ODEs, phase plane and stability | core | 15–20% | 13 | 8 | 1 | 4 |
| 6 · Series solutions and special functions | core | 15% | 11 | 9 | 0 | 2 |
| 7 · Laplace transforms | core | 15% | 14 | 14 | 0 | 0 |
| 8 · Linear algebra for ODEs | core | as needed | 7 | 6 | 0 | 1 |
| 9 · Fourier series and Sturm–Liouville boundary-value problems | core | 10–15% | 11 | 8 | 0 | 3 |
| 10 · Partial differential equations | core | — | 9 | 7 | 1 | 1 |
| 11 · Fourier integrals and transforms | extension | — | 2 | 0 | 0 | 2 |
| 12 · Vector calculus for transport | extension | — | 2 | 0 | 1 | 1 |

## Unit 1 · The calculus and complex-number toolkit

Big ideas: FORM, TRANS

### 1.1 Integration techniques

Book: kreyszig-10e §1.3, §1.5, §6.4

- ● **EM-1.1.A** Evaluate an integral by u-substitution, choosing u so its derivative appears in the integrand.
  - EK: ∫f(g(x))g′(x)dx = ∫f(u)du; a missing constant factor is fine, a missing x is not.
  - P3 · drills: usub-poly, usub-exp, usub-trig, usub-log, usub-ratio, usub-linear
- ● **EM-1.1.B** Evaluate an integral by parts, including tabular and cyclic (e^ax·trig) cases.
  - EK: ∫u dv = uv − ∫v du; LIATE picks u; cyclic integrals return to themselves and are solved algebraically.
  - P3 · drills: parts-x-exp, parts-x-trig, parts-x-log, parts-tabular, parts-exp-trig, parts-inverse
- ● **EM-1.1.C** Decompose a rational function into partial fractions (distinct, repeated, irreducible quadratic, improper) and integrate it.
  - EK: Divide first if improper; repeated factor (x−a)^k needs k terms; irreducible quadratic gets (Ax+B).
  - P3 · drills: pf-distinct, pf-repeated, pf-three, pf-irreducible, pf-improper, pf-coeffs

### 1.2 Complex numbers and Euler's formula

Book: kreyszig-10e §2.2, §13.1, §13.2, §13.5

- ● **EM-1.2.A** Convert complex numbers between rectangular, polar and exponential form.
  - EK: e^(iθ) = cos θ + i sin θ; z = re^(iθ), r = |z|, θ = arg z.
  - P3 · drills: euler-rect, euler-polar, euler-re-im
- ● **EM-1.2.B** Compute powers and roots of a complex number with De Moivre's formula.
  - EK: (re^(iθ))^n = r^n e^(inθ); n distinct n-th roots spaced 2π/n apart.
  - P3 · drills: euler-demoivre
- ● **EM-1.2.C** Find the complex roots α ± βi of a real quadratic.
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
- ● **EM-1.4.C** Test whether M dx + N dy is an exact differential.
  - EK: Exact on a simply connected domain ⇔ ∂M/∂y = ∂N/∂x.
  - P2 · drills: mv-exact-test

## Unit 2 · First-order ODEs

Big ideas: MODEL, FORM, TRANS

### 2.1 Basic concepts, direction fields and Euler's method

Book: kreyszig-10e §1.1, §1.2

- ○ **EM-2.1.A** Classify an ODE by order and linearity, and verify that a given function solves it.
  - EK: Order = highest derivative; linear ⇔ y and its derivatives appear to first power with coefficients in x only.
  - P2 · P5
- ○ **EM-2.1.B** Sketch a direction field and solution curves from isoclines of y′ = f(x, y).
  - EK: Isocline f(x, y) = k has slope k everywhere; solution curves are tangent to the field.
  - P6
- ○ **EM-2.1.C** Approximate an IVP solution with a few steps of Euler's method and estimate the error trend.
  - EK: y_(n+1) = y_n + h f(x_n, y_n); global error is O(h).
  - P3 · P5

### 2.2 Separable equations and reducing substitutions

Book: kreyszig-10e §1.3

- ● **EM-2.2.A** Solve a separable ODE explicitly where possible, including the IVP constant.
  - EK: g(y)dy = f(x)dx, integrate both sides; check for lost equilibrium solutions when dividing by g.
  - Needs: EM-1.1.A, EM-1.1.C
  - P3 · P4 · drills: sep-exp-growth, sep-over-y, sep-y-squared, sep-exp-split, sep-over-y2
- ● **EM-2.2.B** Reduce an ODE to separable form with u = y/x or u = ax + by + c, and solve it.
  - EK: y′ = f(y/x): y = ux ⇒ u + xu′ = f(u); y′ = f(ax + by + c): u′ = a + bf(u).
  - Needs: EM-2.2.A
  - P2 · P3 · drills: sub-ratio, sub-square, sub-exp, sub-linear-square, sub-arctan

### 2.3 Exact equations and integrating factors

Book: kreyszig-10e §1.4

- ● **EM-2.3.A** Solve an exact ODE by finding the potential u(x, y) = c, and fit an IVP.
  - EK: u_x = M, u_y = N; integrate one, differentiate, match the other.
  - Needs: EM-1.4.C
  - P3 · P4 · drills: exact-poly, exact-trans, exact-exy, exact-ivp
- ● **EM-2.3.B** Decide whether an integrating factor depending only on x or only on y exists.
  - EK: R = (M_y − N_x)/N a function of x alone ⇒ F(x) = exp∫R dx; R* = (N_x − M_y)/M of y alone ⇒ F(y).
  - P2 · drills: if-test
- ● **EM-2.3.C** Find the integrating factor and solve the resulting exact equation.
  - EK: Multiply by F, re-check exactness, then solve as exact.
  - Needs: EM-2.3.A, EM-2.3.B
  - P3 · drills: if-factor-x, if-factor-y, if-solve

### 2.4 Linear and Bernoulli equations

Book: kreyszig-10e §1.5

- ● **EM-2.4.A** Solve a linear first-order ODE with an integrating factor, including IVPs and forcing that matches e^(−∫p).
  - EK: y′ + py = r ⇒ y = e^(−h)[∫e^h r dx + c], h = ∫p dx.
  - Needs: EM-1.1.A
  - P3 · P4 · drills: lin-exp, lin-const, lin-power, lin-gauss, lin-trig, lin-resonant
- ● **EM-2.4.B** Solve a linear ODE whose integrating-factor integral needs integration by parts.
  - EK: ∫e^h r dx often pairs a polynomial or trig with an exponential.
  - Needs: EM-2.4.A, EM-1.1.B
  - P3 · drills: ibp-poly, ibp-over-x-trig, ibp-over-x-exp, ibp-x-exp, ibp-trig-exp, ibp-power-exp
- ● **EM-2.4.C** Reduce a Bernoulli equation to a linear one with u = y^(1−a) and solve it.
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

- ● **EM-2.6.A** Set up and solve a mixing-tank balance for concentration or mass of solute.
  - EK: dm/dt = (rate in) − (rate out), rate out = (m/V)·Q_out.
  - P1 · P3 · drills: model-mixing
- ● **EM-2.6.B** Model Newton's cooling and first-order decay, and extract a time constant, half-life or time to reach a value.
  - EK: dT/dt = −k(T − T_a); y = y_0 e^(−kt), t_1/2 = ln 2/k.
  - P1 · P6 · drills: model-cooling, model-decay
- ● **EM-2.6.C** Solve the logistic equation and find its equilibria and carrying capacity.
  - EK: y′ = ky(1 − y/K) is separable and Bernoulli; y → K for y_0 > 0.
  - P1 · P6 · drills: model-logistic
- ○ **EM-2.6.D** Find and classify the equilibria of an autonomous ODE y′ = f(y) from a phase line.
  - EK: f(y*) = 0; stable if f′(y*) < 0.
  - P6

### 2.7 Existence and uniqueness

Book: kreyszig-10e §1.7

- ○ **EM-2.7.A** Decide whether an IVP has a unique solution near the initial point from the continuity of f and ∂f/∂y.
  - EK: f and f_y continuous on a rectangle around (x_0, y_0) ⇒ unique solution on some |x − x_0| < α.
  - P2

## Unit 3 · Second-order linear ODEs

Big ideas: LIN, EIG, FORM, MODEL

### 3.1 Homogeneous theory, reduction of order and the Wronskian

Book: kreyszig-10e §2.1, §2.6

- ○ **EM-3.1.A** Use superposition to build a general solution from a basis and fit it to an IVP.
  - EK: For a linear homogeneous ODE, any combination c_1y_1 + c_2y_2 of solutions is a solution; two independent ones form a basis.
  - P4
- ● **EM-3.1.B** Find a second solution from a known one by reduction of order.
  - EK: y_2 = u y_1, u′ = U = e^(−∫p dx)/y_1² (standard form y″ + py′ + qy = 0).
  - P3 · drills: red-euler, red-trig, red-exp, red-gauss, red-const
- ● **EM-3.1.C** Compute the Wronskian of two or three functions and use it to decide linear independence.
  - EK: W = det of the functions and their derivatives; W ≠ 0 somewhere ⇒ independent; for ODE solutions W ≡ 0 or never 0 (Abel).
  - P3 · P5 · drills: wr-exps, wr-repeated, wr-trig, wr-damped, wr-powers, wr-log, wr-dependent

### 3.2 Constant coefficients

Book: kreyszig-10e §2.2, §2.3

- ● **EM-3.2.A** Write the general solution of ay″ + by′ + cy = 0 for each of the three root cases of the characteristic equation.
  - EK: Distinct real: e^(λ₁x), e^(λ₂x); double: e^(λx), xe^(λx); complex α ± iβ: e^(αx)cos βx, e^(αx)sin βx.
  - Needs: EM-1.2.C
  - P2 · P3 · drills: char-distinct, char-repeated, char-complex
- ● **EM-3.2.B** Solve a constant-coefficient IVP.
  - EK: Two conditions y(x_0), y′(x_0) fix c_1, c_2.
  - Needs: EM-3.2.A
  - P4 · drills: char-ivp

### 3.3 Euler–Cauchy equations

Book: kreyszig-10e §2.5

- ● **EM-3.3.A** Find the roots of the auxiliary equation of an Euler–Cauchy ODE.
  - EK: x²y″ + axy′ + by = 0 with y = x^m ⇒ m² + (a − 1)m + b = 0.
  - P2 · drills: ec-roots
- ● **EM-3.3.B** Write the general solution of an Euler–Cauchy ODE for each root case and fit an IVP.
  - EK: Distinct: x^(m₁), x^(m₂); double: x^m, x^m ln x; complex: x^μ cos(ν ln x), x^μ sin(ν ln x).
  - Needs: EM-3.3.A
  - P3 · P4 · drills: ec-distinct, ec-double, ec-complex, ec-ivp

### 3.4 Free oscillations

Book: kreyszig-10e §2.4

- ● **EM-3.4.A** Find the natural frequency, period, amplitude and phase of an undamped mass–spring system.
  - EK: my″ + ky = 0 ⇒ ω₀ = √(k/m); A cos ω₀t + B sin ω₀t = C cos(ω₀t − δ), C = √(A² + B²).
  - P1 · P6 · drills: spring-frequency, spring-amplitude-phase
- ● **EM-3.4.B** Solve an undamped oscillator IVP.
  - EK: y(0) and y′(0) give A and B/ω₀.
  - P4 · drills: spring-undamped-ivp
- ● **EM-3.4.C** Classify a damped oscillator as over-, critically or underdamped from c² − 4mk.
  - EK: c² > 4mk overdamped, = critical, < under; underdamped frequency ω* = √(4mk − c²)/2m.
  - P2 · P6 · drills: spring-classify
- ● **EM-3.4.D** Solve a damped oscillator IVP in each damping regime.
  - EK: Same three root cases as 3.2.A, with α = −c/2m < 0 so every solution decays.
  - Needs: EM-3.2.B
  - P3 · P4 · drills: spring-over-ivp, spring-critical-ivp, spring-under-ivp

### 3.5 Nonhomogeneous equations

Book: kreyszig-10e §2.7, §2.10

- ● **EM-3.5.A** Find a particular solution by undetermined coefficients, including the modification rule.
  - EK: Guess the form of r(x) (poly, e^(γx), cos/sin); multiply by x (or x²) when the guess solves the homogeneous ODE.
  - Needs: EM-3.2.A
  - P2 · P3 · drills: uc-poly, uc-exp, uc-trig, uc-resonance
- ● **EM-3.5.B** Assemble y = y_h + y_p and fit an IVP for a nonhomogeneous ODE.
  - EK: Apply initial conditions to the full solution, never to y_h alone.
  - P4 · drills: uc-general, vop-general
- ● **EM-3.5.C** Find a particular solution by variation of parameters when r(x) is not of undetermined-coefficient form or coefficients vary.
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
- ○ **EM-3.6.D** Model an RLC circuit as a second-order ODE and map it onto the mass–spring analogy.
  - EK: LI″ + RI′ + I/C = E′(t): L ↔ m, R ↔ c, 1/C ↔ k.
  - P1

## Unit 4 · Higher-order linear ODEs

Big ideas: LIN, EIG

### 4.1 Homogeneous theory and constant coefficients

Book: kreyszig-10e §3.1, §3.2

- ● **EM-4.1.A** Test n functions for linear independence with the n×n Wronskian.
  - EK: Rows are f, f′, …, f^(n−1); expand by cofactors.
  - Needs: EM-3.1.C, EM-8.3.A
  - P3 · drills: wr-three
- ● **EM-4.1.B** Find the roots of an n-th order characteristic polynomial.
  - EK: Rational root test, then synthetic division to a quadratic.
  - P3 · drills: hi-roots
- ● **EM-4.1.C** Write the general solution of an n-th order constant-coefficient ODE with distinct, repeated and complex roots, and fit an IVP.
  - EK: A root of multiplicity k gives e^(λx), xe^(λx), …, x^(k−1)e^(λx).
  - Needs: EM-4.1.B
  - P3 · P4 · drills: hi-distinct, hi-repeated, hi-complex, hi-ivp

### 4.2 Nonhomogeneous higher-order equations

Book: kreyszig-10e §3.3

- ◐ **EM-4.2.A** Find a particular solution of an n-th order ODE by undetermined coefficients or variation of parameters.
  - EK: Same modification rule; variation of parameters uses Cramer's rule with W_k/W.
  - Needs: EM-3.5.A, EM-4.1.C
  - P3 · drills: ~uc-general

## Unit 5 · Systems of ODEs, phase plane and stability

Big ideas: EIG, LIN, MODEL

### 5.1 Systems as models

Book: kreyszig-10e §4.1, §4.2

- ◐ **EM-5.1.A** Convert an n-th order ODE into a first-order system.
  - EK: y₁ = y, y₂ = y′, …; the companion matrix's eigenvalues are the characteristic roots.
  - P1 · drills: ~phase-ode2
- ● **EM-5.1.B** Write the rate matrix for series first-order kinetics A → B → C.
  - EK: d[A]/dt = −k₁[A], d[B]/dt = k₁[A] − k₂[B]; C follows from mass conservation.
  - P1 · drills: kin-matrix

### 5.2 Constant-coefficient systems by eigenvalues

Book: kreyszig-10e §4.3

- ● **EM-5.2.A** Find the eigenvalues and eigenvectors that give the basis solutions of y′ = Ay.
  - EK: y = x e^(λt) with (A − λI)x = 0.
  - Needs: EM-8.4.A, EM-8.4.B
  - P3 · drills: sys-eigen
- ● **EM-5.2.B** Write the general solution of a 2×2 system with real distinct eigenvalues and fit an IVP.
  - EK: y = c₁x⁽¹⁾e^(λ₁t) + c₂x⁽²⁾e^(λ₂t).
  - Needs: EM-5.2.A
  - P3 · P4 · drills: sys-general, sys-ivp
- ● **EM-5.2.C** Write real solutions of a 2×2 system with complex eigenvalues and fit an IVP.
  - EK: Take real and imaginary parts of x e^((α+iβ)t).
  - Needs: EM-5.2.A, EM-1.2.A
  - P3 · P4 · drills: sys-complex, sys-complex-ivp
- ● **EM-5.2.D** Solve a 2×2 system with a repeated eigenvalue using a generalised eigenvector.
  - EK: Second solution x t e^(λt) + u e^(λt), (A − λI)u = x.
  - P3 · drills: sys-repeated
- ● **EM-5.2.E** Solve series kinetics A → B → C and find the time of maximum intermediate.
  - EK: Eigenvalues −k₁, −k₂; [B] = k₁A₀(e^(−k₁t) − e^(−k₂t))/(k₂ − k₁); t_max = ln(k₁/k₂)/(k₁ − k₂), = 1/k when k₁ = k₂.
  - Needs: EM-5.1.B
  - P3 · P6 · drills: kin-eigen, kin-B, kin-C, kin-tmax

### 5.3 Critical points and stability

Book: kreyszig-10e §4.3, §4.4

- ● **EM-5.3.A** Classify the critical point of a linear 2×2 system (node, saddle, centre, spiral) from its eigenvalues or from trace and determinant.
  - EK: p = tr A, q = det A, Δ = p² − 4q: q < 0 saddle; q > 0, Δ ≥ 0 node; Δ < 0 spiral (p ≠ 0) or centre (p = 0).
  - P2 · P6 · drills: phase-matrix, phase-equations, phase-ode2
- ● **EM-5.3.B** Decide whether a critical point is stable, asymptotically stable or unstable.
  - EK: Asymptotically stable ⇔ p < 0, q > 0; centre is stable, not asymptotically.
  - P6 · drills: phase-stability
- ○ **EM-5.3.C** Sketch a phase portrait with eigenvector directions and trajectory orientation.
  - EK: Trajectories leave along the fast-growing eigenvector and approach along the slow-decaying one.
  - P6

### 5.4 Nonlinear systems

Book: kreyszig-10e §4.5

- ○ **EM-5.4.A** Find the critical points of a nonlinear autonomous system and linearise at each with the Jacobian.
  - EK: Set f = g = 0; J = [[f_x, f_y], [g_x, g_y]] at the point.
  - P3
- ○ **EM-5.4.B** Classify each critical point of a nonlinear system from its linearisation, noting when linearisation is inconclusive.
  - EK: Hyperbolic points keep their type; a linear centre may be a spiral in the nonlinear system.
  - Needs: EM-5.3.A, EM-5.4.A
  - P6

### 5.5 Nonhomogeneous linear systems

Book: kreyszig-10e §4.6

- ○ **EM-5.5.A** Find a particular solution of y′ = Ay + g by undetermined coefficients, diagonalisation or variation of parameters.
  - EK: Fundamental matrix Y: y_p = Y∫Y⁻¹g dt.
  - P3

## Unit 6 · Series solutions and special functions

Big ideas: TRANS, FORM

### 6.1 Ordinary and singular points

Book: kreyszig-10e §5.1, §5.3

- ● **EM-6.1.A** Classify a point as ordinary, regular singular or irregular singular.
  - EK: Standard form y″ + py′ + qy = 0: ordinary if p, q analytic; regular singular if (x − x₀)p and (x − x₀)²q are analytic.
  - P2 · drills: series-classify-point
- ● **EM-6.1.B** Give the guaranteed radius of convergence of a power-series solution about an ordinary point.
  - EK: At least the distance to the nearest singular point in the complex plane.
  - Needs: EM-6.1.A
  - P2 · drills: series-radius

### 6.2 Power series method

Book: kreyszig-10e §5.1

- ● **EM-6.2.A** Derive the recurrence relation for the coefficients of a power-series solution.
  - EK: Substitute Σa_m x^m, shift indices to a common power, set each coefficient to zero.
  - Needs: EM-1.3.A
  - P3 · drills: series-recurrence, series-recurrence-airy
- ● **EM-6.2.B** Generate the first terms of the series solution from the recurrence and initial values.
  - EK: a₀ = y(0), a₁ = y′(0); even and odd coefficients often split into two basis series.
  - Needs: EM-6.2.A
  - P3 · P4 · drills: series-terms, series-terms-airy

### 6.3 Frobenius method

Book: kreyszig-10e §5.3

- ● **EM-6.3.A** Find the indicial equation and its roots at a regular singular point.
  - EK: r(r − 1) + b₀r + c₀ = 0, b₀ = lim xp, c₀ = lim x²q.
  - Needs: EM-6.1.A
  - P3 · drills: frobenius-indicial
- ● **EM-6.3.B** Decide which Frobenius case applies and what form the second solution takes.
  - EK: Roots not differing by an integer: two x^r series; double root: second has ln x; differ by an integer: second may have ln x.
  - Needs: EM-6.3.A
  - P2 · drills: frobenius-case
- ○ **EM-6.3.C** Construct the first Frobenius series solution from the larger indicial root.
  - EK: y = x^r Σa_m x^m; same index-shifting as the power series method.
  - Needs: EM-6.3.A, EM-6.2.A
  - P3

### 6.4 Legendre and Bessel functions

Book: kreyszig-10e §5.2, §5.4, §5.5

- ● **EM-6.4.A** Recognise Legendre's, Bessel's and Euler–Cauchy equations in a given ODE and read off the order or degree.
  - EK: (1 − x²)y″ − 2xy′ + n(n+1)y = 0; x²y″ + xy′ + (x² − ν²)y = 0.
  - P2 · drills: spec-identify, spec-legendre-n, spec-bessel-order
- ● **EM-6.4.B** Solve a scaled Bessel equation x²y″ + xy′ + (λ²x² − ν²)y = 0 with J_ν(λx), Y_ν(λx).
  - EK: Substitute z = λx.
  - P2 · P3 · drills: spec-bessel-scaled
- ● **EM-6.4.C** Write the general solution of Bessel's equation, choosing J₋ν or Y_ν as the second solution.
  - EK: J_ν, J₋ν independent unless ν is an integer, where J₋ₙ = (−1)ⁿJₙ; then use Y_ν.
  - P2 · P5 · drills: spec-bessel-independent
- ○ **EM-6.4.D** Use Legendre polynomials' explicit form, Rodrigues' formula or orthogonality to evaluate P_n or an integral.
  - EK: P_n(x) = (1/2ⁿn!) dⁿ/dxⁿ (x² − 1)ⁿ; ∫P_mP_n = 0 on [−1, 1] for m ≠ n.
  - P3

## Unit 7 · Laplace transforms

Big ideas: TRANS, LIN, MODEL

### 7.1 The transform, linearity and s-shifting

Book: kreyszig-10e §6.1

- ● **EM-7.1.A** Find the Laplace transform of a combination of elementary functions from the table, using identities where needed.
  - EK: L{tⁿ} = n!/s^(n+1); L{e^(at)} = 1/(s − a); L{cos ωt} = s/(s² + ω²); sin² = (1 − cos 2t)/2.
  - P3 · drills: lt-linear, lt-trig, lt-power, lt-hyperbolic, lt-identity
- ● **EM-7.1.B** Apply the first shifting theorem forwards and in reverse.
  - EK: L{e^(at)f(t)} = F(s − a); complete the square to expose s − a.
  - P3 · drills: shift-s-forward, shift-s-inverse

### 7.2 Inverse transforms by partial fractions

Book: kreyszig-10e §6.1, §6.4

- ● **EM-7.2.A** Invert a rational F(s) by partial fractions with distinct, repeated or complex poles.
  - EK: Repeated pole ⇒ tⁿe^(at)/n!; complex pole pair ⇒ e^(at)(cos, sin).
  - Needs: EM-1.1.C
  - P3 · drills: ilt-distinct, ilt-repeated, ilt-complex, ilt-three, ilt-quadratic

### 7.3 Solving IVPs by Laplace transform

Book: kreyszig-10e §6.2

- ● **EM-7.3.A** Solve a constant-coefficient IVP by transforming, solving the subsidiary equation and inverting.
  - EK: L{y′} = sY − y(0); L{y″} = s²Y − sy(0) − y′(0); initial conditions enter automatically.
  - Needs: EM-7.2.A
  - P3 · P4 · drills: livp-real, livp-complex, livp-double, livp-exp, livp-const
- ● **EM-7.3.B** Identify the transfer function of a linear system and relate its poles to stability and damping.
  - EK: Q(s) = Y/R with zero ICs = 1/(as² + bs + c); poles in the left half-plane ⇔ decay.
  - P6 · drills: transfer-g, transfer-poles, transfer-stable

### 7.4 Unit step and t-shifting

Book: kreyszig-10e §6.3

- ● **EM-7.4.A** Write a piecewise function with unit step functions and transform it.
  - EK: f = f₁ + (f₂ − f₁)u(t − a) + …; L{f(t − a)u(t − a)} = e^(−as)F(s).
  - P1 · P3 · drills: shift-t-forward, shift-piecewise
- ● **EM-7.4.B** Invert a transform containing e^(−as).
  - EK: e^(−as)F(s) ↦ f(t − a)u(t − a).
  - P3 · drills: shift-t-inverse
- ● **EM-7.4.C** Solve an IVP with switched or piecewise forcing.
  - EK: Transform the step-written forcing; the solution is piecewise with continuous y and y′.
  - Needs: EM-7.3.A, EM-7.4.A
  - P1 · P3 · drills: step-ivp-on, step-ivp-pulse

### 7.5 Impulses and the Dirac delta

Book: kreyszig-10e §6.4

- ● **EM-7.5.A** Model a sudden impulse with δ(t − a) and solve the resulting IVP, including the impulse response.
  - EK: L{δ(t − a)} = e^(−as); impulse response = L⁻¹{transfer function}.
  - P1 · P3 · drills: delta-ivp, delta-response

### 7.6 Convolution and integral equations

Book: kreyszig-10e §6.5

- ● **EM-7.6.A** Compute a convolution integral directly.
  - EK: (f * g)(t) = ∫₀ᵗ f(τ)g(t − τ)dτ.
  - P3 · drills: conv-compute
- ● **EM-7.6.B** Invert a product of transforms or transform an integral using the convolution theorem.
  - EK: L{f * g} = FG; L{∫₀ᵗ f dτ} = F/s.
  - P3 · drills: conv-inverse, conv-transform
- ● **EM-7.6.C** Solve a Volterra integral equation of convolution type.
  - EK: Transform, solve for Y algebraically, invert.
  - Needs: EM-7.6.B
  - P3 · drills: conv-volterra

### 7.7 Transform derivatives and systems

Book: kreyszig-10e §6.6, §6.7

- ● **EM-7.7.A** Use L{tf(t)} = −F′(s) to transform or invert functions and solve ODEs with linear coefficients.
  - EK: Differentiation in s ↔ multiplication by −t; integration in s ↔ division by t.
  - P3 · drills: tmul-forward, tmul-inverse
- ● **EM-7.7.B** Solve a linear system of ODEs by Laplace transform.
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

- ○ **EM-8.5.A** Diagonalise a matrix with a full set of eigenvectors and use it to decouple a linear system.
  - EK: D = X⁻¹AX; symmetric A has real eigenvalues and orthogonal eigenvectors.
  - Needs: EM-8.4.B, EM-8.3.B
  - P3

## Unit 9 · Fourier series and Sturm–Liouville boundary-value problems

Big ideas: EIG, TRANS, LIN

### 9.1 Fourier series

Book: kreyszig-10e §11.1, §11.2

- ● **EM-9.1.A** Compute the Fourier coefficients of a 2π-periodic function given on one period.
  - EK: a₀ = (1/2π)∫f, a_n = (1/π)∫f cos nx, b_n = (1/π)∫f sin nx over (−π, π).
  - Needs: EM-1.1.B
  - P3 · drills: fs-step, fs-sawtooth, fs-parabola, fs-abs
- ● **EM-9.1.B** Compute the Fourier series of a function of period 2L, using even/odd symmetry to skip coefficients.
  - EK: Replace nx by nπx/L and 1/π by 1/L; even ⇒ cosine series, odd ⇒ sine series.
  - P2 · P3 · drills: fs-period-2l
- ● **EM-9.1.C** Write the half-range sine or cosine expansion of a function on (0, L).
  - EK: Odd extension ⇒ sine series; even extension ⇒ cosine series; b_n = (2/L)∫₀ᴸ f sin(nπx/L).
  - P3 · drills: fs-half-range
- ○ **EM-9.1.D** Find the periodic steady-state response of an oscillator to a periodic non-sinusoidal force by Fourier series.
  - EK: Solve term by term; the term with nω nearest ω₀ dominates.
  - Needs: EM-9.1.A, EM-3.6.A
  - P3 · P6

### 9.2 Sturm–Liouville problems

Book: kreyszig-10e §11.5

- ● **EM-9.2.A** Rewrite a second-order eigenvalue ODE in Sturm–Liouville form and identify p, q and r.
  - EK: (py′)′ + (q + λr)y = 0; multiply by the integrating factor e^(∫a₁/a₂)/a₂ when needed.
  - P2 · drills: sl-form
- ● **EM-9.2.B** Classify a Sturm–Liouville problem as regular, periodic or singular.
  - EK: Regular: p > 0, r > 0 on [a, b] with separated BCs; periodic: y(a) = y(b), y′(a) = y′(b); singular: p vanishes at an end.
  - Needs: EM-9.2.A
  - P2 · drills: sl-classify
- ● **EM-9.2.C** Find the eigenvalues of y″ + λy = 0 under Dirichlet, Neumann or mixed boundary conditions.
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

- ○ **EM-9.3.A** Verify orthogonality of eigenfunctions with respect to the weight r(x).
  - EK: ∫ₐᵇ r y_m y_n dx = 0 for m ≠ n in a regular or periodic S–L problem.
  - P5
- ○ **EM-9.3.B** Expand a function in a generalised Fourier series of S–L eigenfunctions (e.g. Legendre or Fourier–Bessel).
  - EK: a_n = ∫ r f y_n dx / ∫ r y_n² dx.
  - Needs: EM-9.3.A
  - P3

## Unit 10 · Partial differential equations

Big ideas: EIG, TRANS, MODEL

### 10.1 Basic concepts and classification

Book: kreyszig-10e §12.1

- ● **EM-10.1.A** Classify a second-order linear PDE as elliptic, parabolic or hyperbolic and verify a solution.
  - EK: Au_xx + 2Bu_xy + Cu_yy: AC − B² > 0 elliptic, = 0 parabolic, < 0 hyperbolic.
  - P2 · drills: pde-classify, pde-verify

### 10.2 Heat equation by separation of variables

Book: kreyszig-10e §12.5, §12.6

- ● **EM-10.2.A** Separate u = F(x)G(t) in the heat equation and find each mode's decay rate.
  - EK: F″ + kF = 0 (an S–L problem), G′ + c²kG = 0 ⇒ G = e^(−c²λ_n t).
  - Needs: EM-9.2.C
  - P2 · P3 · drills: pde-rates
- ● **EM-10.2.B** Solve the heat equation on a finite rod with Dirichlet or insulated ends by Fourier series.
  - EK: Dirichlet ⇒ sine series; insulated ⇒ cosine series with a constant term (the mean).
  - Needs: EM-10.2.A, EM-9.1.C
  - P3 · P4 · drills: pde-heat, pde-neumann
- ● **EM-10.2.C** Solve the heat equation with non-homogeneous Dirichlet ends by subtracting the steady state.
  - EK: u = u_s(x) + v; u_s linear; v satisfies zero BCs with v(x, 0) = f − u_s.
  - Needs: EM-10.2.B
  - P2 · P3 · drills: pde-steady

### 10.3 Wave equation

Book: kreyszig-10e §12.2, §12.3, §12.4

- ● **EM-10.3.A** Solve the vibrating string by separation of variables and Fourier series.
  - EK: u = Σ(B_n cos λ_n t + B_n* sin λ_n t) sin(nπx/L), λ_n = cnπ/L.
  - Needs: EM-9.1.C
  - P3 · P4 · drills: pde-wave
- ● **EM-10.3.B** Write d'Alembert's solution for an infinite string from initial displacement and velocity.
  - EK: u = ½[f(x + ct) + f(x − ct)] + (1/2c)∫ g.
  - P3 · drills: dalembert-displacement, dalembert-velocity

### 10.4 Laplace's equation and other geometries

Book: kreyszig-10e §12.6, §12.10, §12.11

- ● **EM-10.4.A** Solve the steady 2-D Dirichlet problem on a rectangle by separation.
  - EK: One direction gives sines, the other sinh; one non-zero side at a time, then superpose.
  - P3 · drills: laplace-rect-modes, laplace-rect-coef
- ◐ **EM-10.4.B** Separate a PDE in polar, cylindrical or spherical coordinates and identify the Bessel or Legendre equation that appears.
  - EK: Radial part in cylinders ⇒ Bessel; polar angle in spheres ⇒ Legendre in cos θ.
  - Needs: EM-6.4.A
  - P2 · drills: ~spec-identify

### 10.5 Transform methods for PDEs

Book: kreyszig-10e §12.7, §12.12

- ○ **EM-10.5.A** Solve a PDE on a semi-infinite or infinite domain by Laplace or Fourier transform.
  - EK: Transform out t (Laplace) or x (Fourier) to get an ODE in the other variable.
  - P3

## Unit 11 · Fourier integrals and transforms (extension)

Big ideas: TRANS

### 11.1 Fourier integral and transforms

Book: kreyszig-10e §11.7, §11.8, §11.9

- ○ **EM-11.1.A** Represent a non-periodic function by its Fourier integral, or its cosine or sine transform.
  - EK: Limit L → ∞ of the Fourier series; even ⇒ cosine transform, odd ⇒ sine.
  - P3
- ○ **EM-11.1.B** Compute a Fourier transform and use its derivative property to turn an ODE into algebra.
  - EK: F{f′} = iwF{f}; F{e^(−ax²)} is Gaussian.
  - P3

## Unit 12 · Vector calculus for transport (extension)

Big ideas: MODEL

### 12.1 Grad, div, curl and the integral theorems

Book: kreyszig-10e §9.7, §9.8, §9.9, §10.7, §10.9

- ◐ **EM-12.1.A** Compute the gradient, divergence, curl and Laplacian of a field in Cartesian coordinates.
  - EK: ∇f, ∇·v, ∇×v, ∇²f = ∇·∇f.
  - P3 · drills: ~mv-partial
- ○ **EM-12.1.B** Derive a differential conservation equation from an integral balance with the divergence theorem.
  - EK: ∭∇·F dV = ∯F·n dA ⇒ ∂c/∂t + ∇·N = R.
  - P1
