# Real Analysis — curriculum framework (draft 1)

Generated from `drills/frameworks/real-analysis.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**21 learning objectives** in 6 units (15 core): 21 drilled, 0 partly, 0 with no drills. Core: 15 / 15 drilled.

## Big ideas

- **EPS · A limit is a promise about every epsilon.** Convergence means a challenge ε can always be met; the proof is the rule that produces N or δ from ε.
- **HYP · Every hypothesis is there for a reason.** Closed, bounded, continuous, monotone: drop one and a standard counterexample appears. Knowing the counterexample is knowing the theorem.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · The real numbers | core | — | 2 | 2 | 0 | 0 |
| 2 · Sequences | core | — | 3 | 3 | 0 | 0 |
| 3 · Series | core | — | 3 | 3 | 0 | 0 |
| 4 · Continuity | core | — | 3 | 3 | 0 | 0 |
| 5 · Differentiation and integration | core | — | 4 | 4 | 0 | 0 |
| 6 · Uniform convergence and metric spaces | extension | — | 6 | 6 | 0 | 0 |

## Unit 1 · The real numbers

Big ideas: HYP

### 1.1 Completeness



- ● **RA-1.1.A** (cambridge-ia-numbers-sets:N5) Find the supremum and infimum of a set and say whether they are attained.
  - EK: The supremum is the least upper bound. Every non-empty set of reals that is bounded above has one, which need not belong to the set; the rationals lack this property.
  - P1 · drills: ra-supremum, ra-sup-attained
- ● **RA-1.1.B** (cambridge-ia-numbers-sets:N5, cambridge-ia-analysis-i:A1) Use the Archimedean property and say where the rationals fail to be complete.
  - EK: For any real ε > 0 there is a natural number n with 1/n < ε. The rationals are dense but not complete: {x : x² < 2} has no rational least upper bound.
  - P1 · drills: ra-archimedean, ra-completeness-facts

## Unit 2 · Sequences

Big ideas: EPS

### 2.1 Convergence



- ● **RA-2.1.A** (cambridge-ia-analysis-i:A1) Produce the N that the definition of a limit asks for.
  - EK: a_n → L means: for every ε > 0 there is an N with |a_n − L| < ε for all n ≥ N. Solving the inequality for n gives N as a function of ε.
  - P1 · drills: ra-epsilon-n, ra-limit-value
- ● **RA-2.1.B** (cambridge-ia-analysis-i:A1) Find the limit of a bounded monotone recursive sequence and know what guarantees it exists.
  - EK: A bounded monotone sequence converges. Once the limit is known to exist, it must satisfy the recurrence as a fixed-point equation. Bolzano-Weierstrass: every bounded sequence has a convergent subsequence.
  - P1 · drills: ra-recursive-limit, ra-sequence-theorems
- ● **RA-2.1.C** (cambridge-ia-analysis-i:A1) Find the limit superior and limit inferior of a bounded sequence.
  - EK: lim sup is the largest limit of any subsequence and lim inf the smallest. The sequence converges exactly when the two agree.
  - P1 · drills: ra-limsup, ra-limsup-facts

## Unit 3 · Series

Big ideas: EPS, HYP

### 3.1 Convergence of series



- ● **RA-3.1.A** (cambridge-ia-analysis-i:A1) Classify a series as absolutely convergent, conditionally convergent or divergent.
  - EK: Absolute convergence implies convergence. The alternating series test gives convergence for decreasing terms tending to 0; Σ 1/n^p converges exactly when p > 1.
  - P2 · drills: ra-series-classify, ra-ratio-test
- ● **RA-3.1.B** (cambridge-ia-analysis-i:A1) Sum a geometric or telescoping series exactly.
  - EK: Σ r^n from n = 0 is 1/(1 − r) for |r| < 1. A telescoping series is summed from its partial sums, which collapse to the first and last terms.
  - P1 · drills: ra-telescoping, ra-geometric-from-k
- ● **RA-3.1.C** (cambridge-ia-analysis-i:A4) Find the radius of convergence of a power series and test its endpoints.
  - EK: Σ a_n x^n converges absolutely for |x| < R and diverges for |x| > R, with 1/R = lim |a_(n+1)/a_n| when that exists. Behaviour at |x| = R must be tested separately.
  - P1 · drills: ra-radius, ra-endpoints

## Unit 4 · Continuity

Big ideas: EPS, HYP

### 4.1 Continuous functions



- ● **RA-4.1.A** (cambridge-ia-analysis-i:A2) Produce the δ that the definition of continuity asks for.
  - EK: f is continuous at a when for every ε > 0 there is a δ > 0 with |f(x) − f(a)| < ε whenever |x − a| < δ. For a linear f, δ = ε/|slope|; for x², restrict to δ ≤ 1 and bound the other factor.
  - P1 · drills: ra-delta-linear, ra-delta-square
- ● **RA-4.1.B** (cambridge-ia-analysis-i:A2) Apply the intermediate and extreme value theorems and say which hypothesis each needs.
  - EK: A continuous function on a closed bounded interval takes every value between its end values, is bounded, and attains its bounds. Each conclusion fails on an open or unbounded interval, or for a discontinuous function.
  - P2 · drills: ra-bisection-steps, ra-ivt-evt-facts
- ● **RA-4.1.C** (cambridge-ia-analysis-i:A2) Decide whether a function is uniformly continuous and find a Lipschitz constant.
  - EK: Uniform continuity means one δ works at every point. A continuous function on a closed bounded interval is uniformly continuous; a bounded derivative gives a Lipschitz constant sup|f′|, hence uniform continuity.
  - P2 · drills: ra-uniformly-continuous, ra-lipschitz

## Unit 5 · Differentiation and integration

Big ideas: HYP, EPS

### 5.1 The theorems behind calculus



- ● **RA-5.1.A** (cambridge-ia-analysis-i:A3) Find the point the mean value theorem promises and say what Rolle's theorem needs.
  - EK: If f is continuous on [a, b] and differentiable inside, some c has f′(c) = (f(b) − f(a))/(b − a). Rolle is the case f(a) = f(b).
  - P1 · drills: ra-mvt-point, ra-mvt-facts
- ● **RA-5.1.B** (cambridge-ia-analysis-i:A3) Bound a Taylor remainder with Lagrange's form.
  - EK: f(x) = Taylor polynomial of degree n + R_n, with R_n = f⁽ⁿ⁺¹⁾(c) x^(n+1)/(n + 1)! for some c between 0 and x. For e^x at x = 1, |R_n| < 3/(n + 1)!.
  - P1 · drills: ra-taylor-degree, ra-taylor-bound
- ● **RA-5.1.C** (cambridge-ia-analysis-i:A5) Compute upper and lower Riemann sums and say which functions are integrable.
  - EK: For an increasing f on n equal pieces, the upper sum uses right endpoints and the lower sum left endpoints, and U − L = (f(b) − f(a))(b − a)/n → 0. Monotone and continuous functions are integrable; the indicator of the rationals is not.
  - P1 · drills: ra-upper-sum, ra-upper-minus-lower
- ● **RA-5.1.D** (cambridge-ia-analysis-i:A5) Decide whether an improper integral converges and evaluate it.
  - EK: ∫₁^∞ x^(−p) dx converges exactly when p > 1, to 1/(p − 1); ∫₀¹ x^(−p) dx converges exactly when p < 1, to 1/(1 − p). Comparison with these settles most cases.
  - P1 · drills: ra-improper-value, ra-improper-converges

## Unit 6 · Uniform convergence and metric spaces (extension)

Big ideas: EPS, HYP

### 6.1 Uniform convergence



- ● **RA-6.1.A** (cambridge-ib-analysis-ii:U) Measure how far a sequence of functions is from its limit in the uniform norm and decide whether convergence is uniform.
  - EK: f_n → f uniformly when sup |f_n − f| → 0. Pointwise convergence lets the worst point move with n; uniform convergence does not. A uniform limit of continuous functions is continuous.
  - P1 · drills: ra-sup-norm, ra-uniform-or-pointwise
- ● **RA-6.1.B** (cambridge-ib-analysis-ii:U) Apply the Weierstrass M-test and say what uniform convergence lets you exchange.
  - EK: If |f_n(x)| ≤ M_n for all x and Σ M_n converges, then Σ f_n converges uniformly. Uniform convergence allows a limit to pass through an integral, and through a derivative when the derivatives converge uniformly.
  - P1 · drills: ra-m-test-bound, ra-exchange-facts

### 6.2 Metric spaces, completeness and contractions



- ● **RA-6.2.B** (cambridge-ib-analysis-ii:C) Decide whether a metric space is complete and say what completeness buys.
  - EK: A space is complete when every Cauchy sequence converges in it. Rⁿ and C[a, b] with the uniform norm are complete; the rationals and an open interval are not. A closed subset of a complete space is complete.
  - P1 · drills: ra-complete-or-not, ra-completeness-uses
- ● **RA-6.2.A** (cambridge-ib-analysis-ii:M) Compute distances in the standard norms on Rⁿ and compare the norms.
  - EK: ‖x‖₁ = Σ|x_i|, ‖x‖₂ = √Σx_i², ‖x‖∞ = max|x_i|, with ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ ≤ n‖x‖∞. All norms on a finite-dimensional space are Lipschitz equivalent, so they give the same open sets.
  - P1 · drills: ra-norm-distance, ra-norm-ratio
- ● **RA-6.2.C** (cambridge-ib-analysis-ii:C) Apply the contraction mapping theorem: find the contraction constant and bound the error of the iteration.
  - EK: If d(f(x), f(y)) ≤ k d(x, y) with k < 1 on a complete space, f has exactly one fixed point, and the iterates satisfy d(x_n, x*) ≤ kⁿ d(x₁, x₀)/(1 − k). Picard's theorem for ODEs is this theorem in C[a, b].
  - P1 · drills: ra-contraction-steps, ra-contraction-constant
- ● **RA-6.2.D** (cambridge-ib-analysis-ii:D) Classify a critical point of a function of two variables from its Hessian.
  - EK: At a critical point, a positive-definite Hessian is a local minimum, negative-definite a local maximum, indefinite a saddle; a zero determinant leaves the test undecided. Mixed partials agree when they are continuous.
  - P1 · drills: ra-hessian-det, ra-critical-classify
