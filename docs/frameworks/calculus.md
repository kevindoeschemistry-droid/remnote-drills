# Calculus — curriculum framework (draft 1)

Generated from `drills/frameworks/calculus.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**203 learning objectives** in 18 units (130 core): 203 drilled, 0 partly, 0 with no drills. Core: 130 / 130 drilled.

## Big ideas

- **CHA · Change.** Calculus is about how quantities change — rates at an instant and accumulation over an interval — and derivatives and integrals are the two linked ways of measuring it.
- **LIM · Limits.** A limit makes sense of the infinite — infinitely close, infinitely small, infinitely many terms. Derivatives, definite integrals, continuity and series are all defined by limits.
- **FUN · Analysis of functions.** Derivatives and integrals reveal how a function behaves — where it rises, peaks and bends, what it accumulates — and the theorems of calculus (IVT, MVT, EVT, FTC) license conclusions about it.

## Practices

- **P1 · Implementing mathematical processes.** Identify what is asked and what is given, pick the rule or procedure the form of the problem calls for, carry it out (with or without technology), and say how an approximation relates to the true value.
- **P2 · Connecting representations.** Read information from graphs, tables, formulas and words; re-express it in another representation; and relate a function's features to those of its derivative or accumulation function.
- **P3 · Justification.** Name the definition, theorem or test that applies, check its hypotheses, apply it, and give reasons for the conclusion — including what the answer means in context and whether it is reasonable.
- **P4 · Communication and notation.** Use precise language, correct notation, units of measure, sensible graphs, and the stated rounding (three decimal places on AP).

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Limits and continuity | core | — | 18 | 18 | 0 | 0 |
| 2 · Differentiation: definition and fundamental properties | core | — | 13 | 13 | 0 | 0 |
| 3 · Differentiation: composite, implicit and inverse functions | core | — | 7 | 7 | 0 | 0 |
| 4 · Contextual applications of differentiation | core | — | 9 | 9 | 0 | 0 |
| 5 · Analytical applications of differentiation | core | — | 13 | 13 | 0 | 0 |
| 6 · Integration and accumulation of change | core | — | 17 | 17 | 0 | 0 |
| 7 · Differential equations | core | — | 9 | 9 | 0 | 0 |
| 8 · Applications of integration | core | — | 14 | 14 | 0 | 0 |
| 9 · Parametric equations, polar coordinates and vector-valued functions (BC only) | bc | — | 10 | 10 | 0 | 0 |
| 10 · Infinite sequences and series (BC only) | bc | — | 20 | 20 | 0 | 0 |
| 11 · Vectors and the geometry of space | extension | — | 8 | 8 | 0 | 0 |
| 12 · Partial derivatives | extension | — | 12 | 12 | 0 | 0 |
| 13 · Multiple integrals | extension | — | 9 | 9 | 0 | 0 |
| 14 · Vector calculus | extension | — | 14 | 14 | 0 | 0 |
| 15 · Hyperbolic functions | core | — | 6 | 6 | 0 | 0 |
| 16 · Calculus in business, the sciences and probability | core | — | 7 | 7 | 0 | 0 |
| 17 · More integration techniques and applications | core | — | 8 | 8 | 0 | 0 |
| 18 · Sequences, series strategy, parametric and polar curves | core | — | 9 | 9 | 0 | 0 |

## Unit 1 · Limits and continuity

Big ideas: CHA, LIM, FUN

### 1.1 Can change occur at an instant?



- ● **CA-1.1.A** (CHA-1.A, webwork-opl:CA1.1) Explain why an instantaneous rate of change has to be defined as a limit of average rates over shrinking intervals.
  - EK: Average rate = Δy/Δx over an interval; at a single instant Δx = 0, so the rate is what Δy/Δx approaches as Δx → 0.
  - P2 · drills: ca-shrinking-average-rate, ca-secant-to-tangent

### 1.2 Limits and limit notation



- ● **CA-1.2.A** (LIM-1.A, webwork-opl:CA1.20) Read and write limit statements in symbols and words, including one-sided limits.
  - EK: lim_(x→c) f(x) = L means f(x) can be made as close to L as wanted by taking x close enough to c (x ≠ c); f(c) itself is irrelevant.
  - P4 · drills: ca-limit-statement, ~ca-limit-graph
- ● **CA-1.2.B** (LIM-1.B, webwork-opl:CA1.9) Decide whether a limit exists by comparing the two one-sided limits.
  - EK: lim_(x→c) f(x) exists ⇔ both one-sided limits exist and are equal; unbounded or oscillating behaviour means no limit.
  - Needs: CA-1.2.A
  - P3 · drills: ca-lim-onesided, ca2-onesided-exists

### 1.3 Estimating limits from graphs



- ● **CA-1.3.A** (LIM-1.C, webwork-opl:CA1.2) Estimate one-sided and two-sided limits from a graph, including at holes and jumps.
  - EK: Follow the curve toward x = c from each side; an open circle or a filled dot elsewhere does not change the limit.
  - Needs: CA-1.2.B
  - P2 · drills: ca-limit-graph, ca-limit-from-formula

### 1.4 Estimating limits from tables



- ● **CA-1.4.A** (LIM-1.C, webwork-opl:CA1.15) Estimate a limit from a table of values that approach c from both sides, and say when the table is not enough.
  - EK: Look for a common trend from left and right; a table can mislead if the sampled x-values miss oscillation.
  - Needs: CA-1.2.B
  - P2 · P1 · drills: ca-limit-table, ca-limit-table-reverse

### 1.5 Limit laws



- ● **CA-1.5.A** (LIM-1.D, webwork-opl:CA1.3) Find limits of sums, products, quotients and compositions from the limits of their parts, and by direct substitution at points of an elementary function's domain.
  - EK: lim(f ± g), lim(fg), lim(f/g) (denominator limit ≠ 0) are the sums, products, quotients of the limits; elementary functions are continuous on their domains, so substitution works there.
  - P1 · drills: ca-lim-substitute, ca-lim-quotient

### 1.6 Algebraic manipulation of limits



- ● **CA-1.6.A** (LIM-1.E, webwork-opl:CA1.4, webwork-opl:CA1.5) Evaluate a 0/0 limit by factoring and cancelling, or by multiplying by a conjugate to clear a radical.
  - EK: f and the simplified form agree for x ≠ c, so their limits at c are the same; (√a − √b)(√a + √b) = a − b.
  - Needs: CA-1.5.A
  - P1 · drills: ca-lim-factor, ca-lim-conjugate
- ● **CA-1.6.B** (LIM-1.E, webwork-opl:CA1.7) Evaluate trig limits by rewriting them in terms of sin x / x → 1 and (1 − cos x)/x → 0.
  - EK: lim_(x→0) sin(kx)/(kx) = 1; multiply and divide by k to set it up.
  - Needs: CA-1.5.A
  - P1 · drills: ca-lim-trig, ca2-trig-limit

### 1.7 Selecting procedures for limits



- ● **CA-1.7.A** (LIM-1.D, LIM-1.E, webwork-opl:CA1.6) Choose a limit procedure from the form the expression takes at c: substitute, factor, rationalize, use a trig identity, or recognise a nonzero/0 infinite limit.
  - EK: Substitute first: a number means done; 0/0 means manipulate; nonzero/0 means an infinite limit or none.
  - Needs: CA-1.6.A, CA-1.6.B
  - P1 · drills: ca-limit-procedure, ~ca-lim-factor

### 1.8 The squeeze theorem



- ● **CA-1.8.A** (LIM-1.E, webwork-opl:CA1.8) Find a limit with the squeeze theorem after bounding the function between two functions with a common limit.
  - EK: g ≤ f ≤ h near c and lim g = lim h = L ⇒ lim f = L; −1 ≤ sin(anything) ≤ 1 is the usual bound.
  - Needs: CA-1.5.A
  - P3 · drills: ca-lim-squeeze, ca-squeeze-bounds

### 1.9 Connecting representations of limits



- ● **CA-1.9.A** (LIM-1.C, LIM-1.D, webwork-opl:CA1.19) Find the same limit from a graph, a table and a formula, and resolve disagreements between them.
  - EK: Graphs and tables estimate; algebra decides. All three should agree once the scale and sample are right.
  - Needs: CA-1.3.A, CA-1.4.A, CA-1.7.A
  - P2 · drills: ca-limit-three-ways, ~ca-limit-table, ~ca-limit-graph

### 1.10 Types of discontinuities



- ● **CA-1.10.A** (LIM-2.A, webwork-opl:CA1.11) Classify a discontinuity as removable, jump or infinite from a graph or formula.
  - EK: Removable: limit exists but ≠ f(c) or f(c) undefined; jump: one-sided limits differ; infinite: a one-sided limit is ±∞.
  - Needs: CA-1.2.B
  - P2 · drills: ca-discontinuity-graph, ca-discontinuity-formula

### 1.11 Continuity at a point



- ● **CA-1.11.A** (LIM-2.A, webwork-opl:CA1.10) Prove or disprove continuity at a point by checking the three conditions.
  - EK: f continuous at c ⇔ f(c) is defined, lim_(x→c) f(x) exists, and they are equal.
  - Needs: CA-1.10.A
  - P3 · drills: ca-continuity-conditions, ~ca-continuity-k

### 1.12 Continuity over an interval



- ● **CA-1.12.A** (LIM-2.B, webwork-opl:CA1.10) State the intervals on which a function (including a piecewise one) is continuous.
  - EK: Polynomials, rational, power, exponential, log and trig functions are continuous on their domains; check a piecewise function at its break points.
  - Needs: CA-1.11.A
  - P3 · drills: ca-make-continuous, ca-piecewise-continuous-check

### 1.13 Removing discontinuities



- ● **CA-1.13.A** (LIM-2.C, webwork-opl:CA1.11) Remove a discontinuity: redefine f at a removable point, or solve for constants that make a piecewise function continuous at its break.
  - EK: Set f(c) = lim_(x→c) f(x); for a piecewise function, match the left and right limits at the break and f(c).
  - Needs: CA-1.11.A, CA-1.6.A
  - P1 · drills: ca-continuity-k, ca-removable-value

### 1.14 Infinite limits and vertical asymptotes



- ● **CA-1.14.A** (LIM-2.D, webwork-opl:CA1.13, webwork-opl:CA1.18) Find vertical asymptotes and the sign of the infinite one-sided limits at each.
  - EK: Nonzero/0 at x = c ⇒ x = c is a vertical asymptote; the sign of numerator and denominator on each side gives +∞ or −∞.
  - Needs: CA-1.10.A
  - P1 · P2 · drills: ca-vert-asymptote, ca2-asymptote-count

### 1.15 Limits at infinity and horizontal asymptotes



- ● **CA-1.15.A** (LIM-2.D, webwork-opl:CA1.14, webwork-opl:CA1.18) Find limits at ±∞ and horizontal asymptotes of rational and radical expressions, and of expressions mixing exponentials, powers and logs.
  - EK: Divide by the highest power in the denominator: deg num < deg den → 0, equal → ratio of leading coefficients, greater → unbounded; √(x²) = |x|; as x → ∞, ln x ≪ x^p ≪ e^x.
  - P1 · P2 · drills: ca-lim-infinity, ca-lim-infinity-radical

### 1.16 The Intermediate Value Theorem



- ● **CA-1.16.A** (FUN-1.A, webwork-opl:CA1.12) Use the IVT to justify that a function takes a given value (or has a root) on an interval, after confirming continuity.
  - EK: f continuous on [a, b] and N between f(a) and f(b) ⇒ f(c) = N for some c in (a, b).
  - Needs: CA-1.12.A
  - P3 · drills: ca-ivt, ca-ivt-applies

## Unit 2 · Differentiation: definition and fundamental properties

Big ideas: CHA, LIM, FUN

### 2.1 Average and instantaneous rates of change



- ● **CA-2.1.A** (CHA-2.A) Calculate an average rate of change as the slope of a secant line.
  - EK: (f(b) − f(a))/(b − a), in units of output per unit input.
  - P1 · drills: ca-avg-rate, ca-avg-rate-table
- ● **CA-2.1.B** (CHA-2.B, webwork-opl:CA1.16) Express an instantaneous rate of change as the limit of a difference quotient.
  - EK: lim_(h→0) (f(a + h) − f(a))/h — the secant slope as the interval shrinks to a point.
  - Needs: CA-2.1.A, CA-1.1.A
  - P2 · drills: ca-difference-quotient-limit, ~ca-def-derivative

### 2.2 The derivative and its notation



- ● **CA-2.2.A** (CHA-2.B, webwork-opl:CA2.1) Compute a derivative from the limit definition (h-form or x → a form), and recognise a given difference-quotient limit as a derivative.
  - EK: f′(x) = lim_(h→0)(f(x+h) − f(x))/h; f′(a) = lim_(x→a)(f(x) − f(a))/(x − a); lim_(h→0)(sin(π/3 + h) − sin(π/3))/h is just cos(π/3).
  - Needs: CA-2.1.B, CA-1.6.A
  - P1 · P2 · drills: ca-def-derivative, ca-recognize-limit-derivative
- ● **CA-2.2.B** (CHA-2.C, webwork-opl:CA1.17) Write the equation of the tangent line at a point, using f′, dy/dx or d/dx notation correctly.
  - EK: y − f(a) = f′(a)(x − a).
  - Needs: CA-2.2.A
  - P4 · drills: ca-tangent-line, ca2-tangent-slope-where

### 2.3 Estimating derivatives at a point



- ● **CA-2.3.A** (CHA-2.D, webwork-opl:CA2.2) Estimate a derivative at a point from a table or graph with a difference quotient.
  - EK: Use the closest bracketing data: (f(b) − f(a))/(b − a) estimates f′ between a and b; a symmetric quotient is usually best.
  - Needs: CA-2.1.A
  - P1 · P2 · drills: ca-estimate-derivative, ca-tangent-line-value

### 2.4 Differentiability and continuity



- ● **CA-2.4.A** (FUN-2.A, webwork-opl:CA2.2) Identify where a function fails to be differentiable (discontinuity, corner, cusp, vertical tangent), including at the break of a piecewise function.
  - EK: Differentiable ⇒ continuous, not conversely; a piecewise function is differentiable at its break only if it is continuous there and the one-sided derivatives match.
  - Needs: CA-2.2.A, CA-1.13.A
  - P3 · drills: ca-differentiability, ca-corner-cusp-pick

### 2.5 The power rule



- ● **CA-2.5.A** (FUN-3.A, webwork-opl:CA2.3) Differentiate x^n for any real n, rewriting roots and reciprocals as powers first.
  - EK: d/dx x^n = n x^(n−1); √x = x^(1/2), 1/x³ = x^(−3).
  - Needs: CA-2.2.A
  - P1 · drills: ca-power-rule, ca-power-reciprocal, ca-power-root, hy-derivative-which, hy-derivative-value

### 2.6 Constant, sum, difference and constant-multiple rules



- ● **CA-2.6.A** (FUN-3.A, webwork-opl:CA2.3) Differentiate polynomials and sums of power terms term by term.
  - EK: Derivative is linear: (af + bg)′ = af′ + bg′; constants differentiate to 0.
  - Needs: CA-2.5.A
  - P1 · drills: ca-poly-derivative, ca2-higher-derivative

### 2.7 Derivatives of sin x, cos x, e^x and ln x



- ● **CA-2.7.A** (FUN-3.A, webwork-opl:CA2.8, webwork-opl:CA2.9, webwork-opl:CA2.10) Differentiate sin x, cos x, e^x and ln x and combinations of them with the sum and constant-multiple rules.
  - EK: (sin x)′ = cos x, (cos x)′ = −sin x, (e^x)′ = e^x, (ln x)′ = 1/x.
  - Needs: CA-2.6.A
  - P1 · drills: ca-elementary-derivative, ca-derivative-at-point
- ● **CA-2.7.B** (LIM-3.A) Derive the derivative of sin x or e^x from the limit definition.
  - EK: sin(x+h) = sin x cos h + cos x sin h, then use sin h/h → 1 and (cos h − 1)/h → 0.
  - Needs: CA-2.2.A, CA-1.6.B
  - P3 · drills: ca-derive-sin-exp, ca-sin-limit-value

### 2.8 The product rule



- ● **CA-2.8.A** (FUN-3.B, webwork-opl:CA2.4, webwork-opl:CA2.5) Differentiate a product, from a formula or from given values of f, g, f′, g′.
  - EK: (fg)′ = f′g + fg′.
  - Needs: CA-2.7.A
  - P1 · drills: ca-product-rule, ca-product-exp, ca-product-values

### 2.9 The quotient rule



- ● **CA-2.9.A** (FUN-3.B, webwork-opl:CA2.6, webwork-opl:CA2.7) Differentiate a quotient, from a formula or from given values.
  - EK: (f/g)′ = (f′g − fg′)/g².
  - Needs: CA-2.8.A
  - P1 · drills: ca-quotient-rule, ca-quotient-values

### 2.10 Derivatives of tan, cot, sec and csc



- ● **CA-2.10.A** (FUN-3.B, webwork-opl:CA2.7, webwork-opl:CA2.8) Derive and use the derivatives of tan x, cot x, sec x and csc x.
  - EK: Write each as a quotient of sin and cos: (tan x)′ = sec²x, (sec x)′ = sec x tan x, (cot x)′ = −csc²x, (csc x)′ = −csc x cot x.
  - Needs: CA-2.9.A
  - P1 · drills: ca-trig-derivative, ca-trig-derivative-value

## Unit 3 · Differentiation: composite, implicit and inverse functions

Big ideas: FUN

### 3.1 The chain rule



- ● **CA-3.1.A** (FUN-3.C, webwork-opl:CA2.15, webwork-opl:CA2.16) Differentiate a composite function with the chain rule — nested compositions, b^x and log_b x, and from tables or graphs of f, g and their derivatives.
  - EK: (f(g(x)))′ = f′(g(x)) g′(x); (b^x)′ = b^x ln b, (log_b x)′ = 1/(x ln b); from a table read g(a) first, then f′ at that value.
  - Needs: CA-2.10.A
  - P1 · P2 · drills: ca-chain-power, ca-chain-trig, ca-chain-exp, ca-chain-ln, ca-chain-values, ca-exp-base

### 3.2 Implicit differentiation



- ● **CA-3.2.A** (FUN-3.D, webwork-opl:CA2.22) Find dy/dx for an implicitly defined relation and the slope or tangent line at a point on it.
  - EK: Every y-term gets a factor dy/dx by the chain rule; collect the dy/dx terms and solve; substitute both x and y of the point.
  - Needs: CA-3.1.A, CA-2.2.B
  - P1 · drills: ca-implicit-slope, ~mv-implicit

### 3.3 Derivatives of inverse functions



- ● **CA-3.3.A** (FUN-3.E, webwork-opl:CA2.11) Find the derivative of an inverse function at a point from f, a table or a graph.
  - EK: If f(a) = b then (f⁻¹)′(b) = 1/f′(a) — reciprocal slope at the reflected point.
  - Needs: CA-3.1.A
  - P1 · P2 · drills: ca-inverse-derivative, ca-inverse-derivative-table

### 3.4 Derivatives of inverse trig functions



- ● **CA-3.4.A** (FUN-3.E, webwork-opl:CA2.12) Differentiate arcsin, arccos and arctan (and compositions with them).
  - EK: (arcsin x)′ = 1/√(1 − x²), (arccos x)′ = −1/√(1 − x²), (arctan x)′ = 1/(1 + x²).
  - Needs: CA-3.3.A
  - P1 · drills: ca-arctan-derivative, ca-arcsin-derivative

### 3.5 Selecting procedures for derivatives



- ● **CA-3.5.A** (FUN-3.A, FUN-3.B, FUN-3.C, FUN-3.D, FUN-3.E, webwork-opl:CA2.18, webwork-opl:CA2.19, webwork-opl:CA2.20) Choose and combine the differentiation rules a given expression needs, simplifying first when it helps.
  - EK: Read the outermost operation: sum → term by term, product → product rule, quotient → quotient rule (or rewrite), composition → chain rule.
  - Needs: CA-3.1.A, CA-3.2.A, CA-3.4.A
  - P1 · drills: ca-rules-combined, ca-chain-at-point
- ● **CA-3.5.B** (FUN-3.C, webwork-opl:CA2.21) Differentiate a variable power such as x^x or a messy product by logarithmic differentiation.
  - EK: Take ln of both sides, differentiate implicitly: y′ = y·(ln y)′. Beyond the CED, but used everywhere downstream.
  - Needs: CA-3.2.A
  - P1 · drills: ca-log-diff, ca-exp-base-derivative

### 3.6 Higher-order derivatives



- ● **CA-3.6.A** (FUN-3.F, webwork-opl:CA2.17) Compute second and higher derivatives, including d²y/dx² of an implicit relation.
  - EK: f″ = (f′)′, d²y/dx²; implicitly, differentiate dy/dx again and replace each dy/dx with its expression.
  - Needs: CA-3.5.A
  - P1 · P4 · drills: ca-second-derivative, ca-second-derivative-trig

## Unit 4 · Contextual applications of differentiation

Big ideas: CHA, LIM

### 4.1 The derivative in context



- ● **CA-4.1.A** (CHA-3.A, webwork-opl:CA3.2) Interpret f′(a) in context, with units, as the rate of change of the quantity at that input.
  - EK: Units of f′ = output units per input unit; sign says increasing or decreasing at that instant.
  - Needs: CA-2.2.A
  - P3 · P4 · drills: ca-rate-units, ca-rate-interpret

### 4.2 Straight-line motion



- ● **CA-4.2.A** (CHA-3.B, webwork-opl:CA3.4) Find velocity, acceleration and speed from position, and decide when the particle moves left/right or speeds up/slows down.
  - EK: v = x′, a = v′ = x″; speed = |v|; speeding up ⇔ v and a have the same sign.
  - Needs: CA-3.6.A
  - P1 · P3 · drills: ca-motion, ca2-speeding-up

### 4.3 Rates of change in other contexts



- ● **CA-4.3.A** (CHA-3.C, webwork-opl:CA3.5) Interpret first and second derivatives of applied quantities (cost, population, temperature, volume) in context.
  - EK: f′ is the rate; f″ says whether that rate is itself rising or falling.
  - Needs: CA-4.1.A
  - P3 · P4 · drills: ca-rate-of-rate, ~ca-rate-units

### 4.4 Introduction to related rates



- ● **CA-4.4.A** (CHA-3.D, webwork-opl:CA3.15) Differentiate an equation linking several quantities with respect to time to relate their rates.
  - EK: Implicit differentiation in t: every changing quantity gets its own d/dt.
  - Needs: CA-3.2.A
  - P1 · drills: ca-related-sphere, ca2-related-circle-radius

### 4.5 Solving related rates problems



- ● **CA-4.5.A** (CHA-3.E, webwork-opl:CA3.15) Solve a related-rates problem: draw, relate the quantities with geometry, differentiate, then substitute the instant's values.
  - EK: Substitute values only after differentiating; similar triangles or Pythagoras usually give the relation.
  - Needs: CA-4.4.A
  - P1 · P4 · drills: ca-related-circle, ca-related-ladder, ca2-related-rate-scaling

### 4.6 Local linearity and linearization



- ● **CA-4.6.A** (CHA-3.F, webwork-opl:CA3.14) Approximate a function value with the tangent-line approximation.
  - EK: f(x) ≈ f(a) + f′(a)(x − a) for x near a.
  - Needs: CA-2.2.B
  - P1 · drills: ca-linearization, ca2-linear-approx-root
- ● **CA-4.6.B** (CHA-3.F, webwork-opl:CA3.14) Decide whether a tangent-line approximation over- or under-estimates, from concavity.
  - EK: Concave up ⇒ tangent lies below ⇒ underestimate; concave down ⇒ overestimate.
  - Needs: CA-4.6.A, CA-3.6.A
  - P3 · drills: ca-linearization-error, ca-linearization-value

### 4.7 L'Hospital's rule



- ● **CA-4.7.A** (LIM-4.A, webwork-opl:CA3.16) Evaluate a 0/0 or ∞/∞ limit with L'Hospital's rule after confirming the form.
  - EK: Indeterminate f/g ⇒ lim f/g = lim f′/g′ if the latter exists; check the form again before reapplying.
  - Needs: CA-3.5.A, CA-1.7.A
  - P3 · drills: ca-lhospital-exp, ca-lhospital-twice
- ● **CA-4.7.B** (LIM-4.A, webwork-opl:CA3.16) Rewrite 0·∞, ∞ − ∞, 1^∞, 0⁰ and ∞⁰ forms as a quotient (or take a log) and apply L'Hospital's rule.
  - EK: 0·∞: f/(1/g); powers: L = e^(lim g ln f). Beyond the CED, standard in college calculus.
  - Needs: CA-4.7.A
  - P1 · drills: ca-lhospital-power, ca2-one-to-infinity

## Unit 5 · Analytical applications of differentiation

Big ideas: FUN

### 5.1 The Mean Value Theorem



- ● **CA-5.1.A** (FUN-1.B, webwork-opl:CA3.1) Verify the MVT hypotheses and find or justify a point where the instantaneous rate equals the average rate.
  - EK: f continuous on [a, b], differentiable on (a, b) ⇒ f′(c) = (f(b) − f(a))/(b − a) for some c in (a, b).
  - Needs: CA-2.4.A, CA-2.1.A
  - P3 · drills: ca-mvt, ca2-mvt-c

### 5.2 Extreme Value Theorem and critical points



- ● **CA-5.2.A** (FUN-1.C, webwork-opl:CA3.8) Decide whether the EVT guarantees absolute extrema on an interval, and find the critical points of a function.
  - EK: Continuous on a closed, bounded interval ⇒ absolute max and min exist; critical point: c in the domain with f′(c) = 0 or undefined — local extrema occur only there.
  - Needs: CA-1.12.A, CA-3.5.A
  - P1 · P3 · drills: ca-critical-points, ca-evt-guarantee

### 5.3 Increasing and decreasing intervals



- ● **CA-5.3.A** (FUN-4.A, webwork-opl:CA3.6) Find the intervals where a function increases or decreases with a sign chart of f′.
  - EK: f′ > 0 on an interval ⇒ f increasing there; f′ < 0 ⇒ decreasing.
  - Needs: CA-5.2.A
  - P1 · P3 · drills: ca-decreasing-interval, ~ca-critical-points

### 5.4 The first derivative test



- ● **CA-5.4.A** (FUN-4.A, webwork-opl:CA3.6) Classify each critical point as a relative max, min or neither by the sign change of f′.
  - EK: f′ changes + to − ⇒ relative max; − to + ⇒ relative min; no change ⇒ neither.
  - Needs: CA-5.3.A
  - P3 · drills: ca-critical-points, ca-second-deriv-at-critical

### 5.5 The candidates test



- ● **CA-5.5.A** (FUN-4.A, webwork-opl:CA3.8) Find absolute extrema on a closed interval by comparing f at critical points and endpoints.
  - EK: Largest value among the candidates is the absolute max, smallest the absolute min.
  - Needs: CA-5.2.A
  - P1 · P3 · drills: ca-abs-extrema, ca-abs-max-value

### 5.6 Concavity and points of inflection



- ● **CA-5.6.A** (FUN-4.A, webwork-opl:CA3.7) Find intervals of concavity and points of inflection from the sign of f″.
  - EK: f″ > 0 ⇒ concave up (f′ increasing); inflection where f″ changes sign, not merely where f″ = 0.
  - Needs: CA-3.6.A, CA-5.3.A
  - P1 · P3 · drills: ca-inflection, ca2-concavity-meaning

### 5.7 The second derivative test



- ● **CA-5.7.A** (FUN-4.A, webwork-opl:CA3.7) Classify a critical point with f′(c) = 0 using the sign of f″(c), and say when the test fails.
  - EK: f″(c) > 0 ⇒ min, < 0 ⇒ max, = 0 ⇒ inconclusive (go back to the first derivative test).
  - Needs: CA-5.6.A, CA-5.4.A
  - P3 · drills: ca-second-derivative-test, ca2-second-test

### 5.8 Sketching graphs of functions and their derivatives



- ● **CA-5.8.A** (FUN-4.A, webwork-opl:CA3.9) Sketch the graph of f′ from the graph of f, and a possible f from the graph of f′.
  - EK: Zeros of f′ at horizontal tangents of f; f′ positive where f rises; extrema of f′ at inflection points of f.
  - Needs: CA-5.6.A
  - P2 · P4 · drills: ca-sketch-derivative, ca-read-derivative-graph, dr-derivative-sketch

### 5.9 Connecting f, f′ and f″



- ● **CA-5.9.A** (FUN-4.A, webwork-opl:CA3.9) Read the extrema, monotonicity, concavity and inflection points of f from a graph or table of f′ (or f″), and justify each claim.
  - EK: Justify from the derivative given, not from the shape of its graph: 'f′ changes from + to − at x = 2'.
  - Needs: CA-5.8.A, CA-5.7.A
  - P2 · P3 · drills: ca-read-derivative-graph, ca-concavity-from-fpp

### 5.10 Setting up optimization problems



- ● **CA-5.10.A** (FUN-4.B, webwork-opl:CA3.10) Translate an optimization situation into a function of one variable with its feasible domain.
  - EK: Write the quantity to optimize, use the constraint to eliminate a variable, state the domain from physical limits.
  - Needs: CA-5.5.A
  - P1 · P2 · drills: ca-optimization-setup, ~ca-optimization-fence

### 5.11 Solving optimization problems



- ● **CA-5.11.A** (FUN-4.C, webwork-opl:CA3.10, webwork-opl:CA3.12) Solve an optimization problem and justify that the answer is the absolute extremum.
  - EK: Candidates test on a closed domain; on an open domain, a single critical point that is a relative extremum is absolute.
  - Needs: CA-5.10.A
  - P3 · P4 · drills: ca-optimization-fence, ca-optimization-box

### 5.12 Behaviour of implicit relations



- ● **CA-5.12.A** (FUN-4.D) Find the points where an implicit curve has a horizontal or vertical tangent.
  - EK: dy/dx = N/D: horizontal where N = 0 (D ≠ 0), vertical where D = 0 (N ≠ 0); the point must lie on the curve.
  - Needs: CA-3.2.A
  - P1 · drills: ca-implicit-horizontal, ca-implicit-slope-point
- ● **CA-5.12.B** (FUN-4.E) Use implicit dy/dx and d²y/dx² to classify extrema and concavity of an implicit curve at a point.
  - EK: At a point with dy/dx = 0, the sign of d²y/dx² gives max/min, as in the second derivative test.
  - Needs: CA-5.12.A, CA-3.6.A, CA-5.7.A
  - P3 · drills: ca-implicit-second-derivative, ca-implicit-concavity

## Unit 6 · Integration and accumulation of change

Big ideas: CHA, LIM, FUN

### 6.1 Accumulations of change



- ● **CA-6.1.A** (CHA-4.A, webwork-opl:CA4.1) Interpret the area between a rate graph and the axis as accumulated change, with units and sign.
  - EK: rate × time = amount; area below the axis counts as negative change.
  - Needs: CA-4.1.A
  - P2 · P4 · drills: ca-accumulation-graph, ca-net-change-rate

### 6.2 Riemann sums



- ● **CA-6.2.A** (LIM-5.A, webwork-opl:CA4.6, webwork-opl:CA5.13) Approximate a definite integral with left, right, midpoint or trapezoidal sums from a formula or a table with unequal subintervals.
  - EK: Sum of (height × width); trapezoid = average of left and right heights × width.
  - Needs: CA-6.1.A
  - P1 · drills: ca-riemann-sums, ca-trapezoid-table, ca2-integral-by-area, ca2-symmetry-integral
- ● **CA-6.2.B** (LIM-5.A, webwork-opl:CA4.6) Decide whether a Riemann or trapezoidal sum over- or under-estimates from monotonicity or concavity.
  - EK: Increasing f: left sum under, right sum over. Concave up: trapezoid over, midpoint under.
  - Needs: CA-6.2.A, CA-5.6.A
  - P3 · drills: ca-riemann-over-under, ca2-riemann-direction, ~ca-riemann-sums

### 6.3 Riemann sums, summation notation and the definite integral



- ● **CA-6.3.A** (LIM-5.B, LIM-5.C, webwork-opl:CA4.6) Write a Riemann sum in sigma notation and convert between a limit of Riemann sums and a definite integral.
  - EK: Δx = (b − a)/n, x_k = a + kΔx; ∫_a^b f(x)dx = lim_(n→∞) Σ f(x_k)Δx — read b − a from Δx and a from x_k.
  - Needs: CA-6.2.A
  - P2 · P4 · drills: ca-riemann-limit, ca-riemann-left-right

### 6.4 The Fundamental Theorem and accumulation functions



- ● **CA-6.4.A** (FUN-5.A, webwork-opl:CA4.9) Differentiate an accumulation function, including variable upper and lower limits.
  - EK: d/dx ∫_a^x f(t)dt = f(x); with limit g(x): f(g(x))g′(x); a variable lower limit flips the sign.
  - Needs: CA-6.3.A, CA-3.1.A
  - P1 · drills: ca-ftc-derivative, ca2-ftc-derivative

### 6.5 Behaviour of accumulation functions



- ● **CA-6.5.A** (FUN-5.A, webwork-opl:CA4.9) Find where g(x) = ∫_a^x f(t)dt increases, has extrema and changes concavity, from the graph of f.
  - EK: g′ = f and g″ = f′: g rises where f > 0, peaks where f changes + to −, inflects at extrema of f.
  - Needs: CA-6.4.A, CA-5.9.A
  - P2 · P3 · drills: ca-read-derivative-graph, ca-ftc-g-prime

### 6.6 Properties of definite integrals



- ● **CA-6.6.A** (FUN-6.A, webwork-opl:CA4.7) Evaluate definite integrals from geometry (areas of triangles, rectangles, circles) and the properties of integrals.
  - EK: ∫_a^b = ∫_a^c + ∫_c^b; ∫_b^a = −∫_a^b; ∫(kf + g) = k∫f + ∫g; ∫_a^a = 0.
  - Needs: CA-6.1.A
  - P1 · P2 · drills: ca-integral-properties, ca2-integral-properties

### 6.7 The Fundamental Theorem and definite integrals



- ● **CA-6.7.A** (FUN-6.B, webwork-opl:CA4.7, webwork-opl:CA4.8) Evaluate a definite integral with an antiderivative, or find a function value from f(a) plus an integral of f′.
  - EK: ∫_a^b f(x)dx = F(b) − F(a); f(b) = f(a) + ∫_a^b f′(x)dx.
  - Needs: CA-6.4.A, CA-6.6.A
  - P1 · drills: ca-definite-poly, ca-net-change-ftc

### 6.8 Basic antiderivatives



- ● **CA-6.8.A** (FUN-6.C, webwork-opl:CA4.2, webwork-opl:CA4.3, webwork-opl:CA4.4, webwork-opl:CA4.5) Find indefinite integrals of power, exponential, trig, 1/x and inverse-trig-form integrands, rewriting the integrand first when needed.
  - EK: ∫x^n dx = x^(n+1)/(n+1) + C (n ≠ −1); ∫dx/x = ln|x| + C; ∫dx/(1 + x²) = arctan x + C; always + C.
  - Needs: CA-3.4.A, CA-6.7.A
  - P1 · drills: ca-antiderivative-poly, ca-antiderivative-elementary, ca-antiderivative-root

### 6.9 Integration by substitution



- ● **CA-6.9.A** (FUN-6.D, webwork-opl:CA5.1, webwork-opl:CA5.2) Evaluate indefinite and definite integrals by u-substitution, changing the limits to u-values for a definite integral.
  - EK: ∫f(g(x))g′(x)dx = ∫f(u)du; a missing constant factor is fine, a missing x is not; ∫_a^b → ∫_(g(a))^(g(b)).
  - Needs: CA-6.8.A, CA-3.1.A
  - P1 · drills: usub-poly, usub-exp, usub-trig, usub-log, usub-ratio, usub-linear, ca-usub-definite, ca2-u-sub-choice

### 6.10 Long division and completing the square



- ● **CA-6.10.A** (FUN-6.D) Integrate a rational function after long division (improper fraction) or completing the square (to an arctan form).
  - EK: deg num ≥ deg den ⇒ divide first; x² + bx + c = (x + b/2)² + k², ∫du/(u² + k²) = (1/k) arctan(u/k) + C.
  - Needs: CA-6.9.A
  - P1 · drills: ca-arctan-integral, ca-long-division-integral

### 6.11 Integration by parts (BC only)



- ● **CA-6.11.A** (FUN-6.E, webwork-opl:CA5.3) Evaluate an integral by parts, choosing u by LIATE, including log and inverse-trig integrands.
  - EK: ∫u dv = uv − ∫v du; pick u to simplify when differentiated (ln x, arctan x, polynomials).
  - Needs: CA-6.9.A
  - P1 · drills: parts-x-exp, parts-x-trig, parts-x-log, parts-inverse
- ● **CA-6.11.B** (FUN-6.E, webwork-opl:CA5.4) Evaluate integrals that need repeated parts (tabular) or that cycle back to themselves (e^ax·trig).
  - EK: Tabular: differentiate u to 0, integrate dv, alternate signs. Cyclic: the original integral reappears — solve algebraically.
  - Needs: CA-6.11.A
  - P1 · drills: parts-tabular, parts-exp-trig

### 6.12 Linear partial fractions (BC only)



- ● **CA-6.12.A** (FUN-6.F, webwork-opl:CA5.7) Decompose a rational function with distinct linear factors into partial fractions and integrate it.
  - EK: A/(x − a) + B/(x − b) + …; cover-up: A = (rest of the fraction) evaluated at x = a; ∫A/(x − a) = A ln|x − a|.
  - Needs: CA-6.9.A
  - P1 · drills: pf-distinct, pf-three, pf-coeffs
- ● **CA-6.12.B** (FUN-6.F, webwork-opl:CA5.7) Decompose and integrate with repeated linear factors, irreducible quadratic factors or an improper fraction (beyond the CED).
  - EK: (x − a)^k needs k terms; an irreducible quadratic gets (Ax + B); divide first if improper.
  - Needs: CA-6.12.A, CA-6.10.A
  - P1 · drills: pf-repeated, pf-irreducible, pf-improper

### 6.13 Improper integrals (BC only)



- ● **CA-6.13.A** (LIM-6.A, webwork-opl:CA4.10) Evaluate an improper integral — infinite interval or unbounded integrand — as a limit, or show it diverges.
  - EK: ∫_a^∞ f dx = lim_(b→∞) ∫_a^b f dx; split at an infinite discontinuity and take one-sided limits; ∫_1^∞ dx/x^p converges ⇔ p > 1, ∫_0^1 dx/x^p ⇔ p < 1.
  - Needs: CA-6.7.A, CA-1.15.A, CA-1.14.A
  - P1 · P3 · drills: ca-improper-power, ca-improper-exp, ca-improper-ptest

### 6.14 Selecting techniques of antidifferentiation



- ● **CA-6.14.A** (FUN-6.C, FUN-6.D, FUN-6.E, FUN-6.F, webwork-opl:CA5.11, webwork-opl:CA5.12) Choose the antidifferentiation technique an integrand calls for: basic rule, substitution, division, completing the square, parts or partial fractions.
  - EK: Look for an inner function and its derivative first; then products of unlike types (parts); then rational functions (division, then partial fractions).
  - Needs: CA-6.10.A, CA-6.11.A, CA-6.12.A
  - P1 · drills: ca-choose-technique, ca-u-sub-value

## Unit 7 · Differential equations

Big ideas: CHA, FUN

### 7.1 Modeling with differential equations



- ● **CA-7.1.A** (FUN-7.A, webwork-opl:DE2.11) Write a differential equation from a verbal description of a rate (proportional to, inversely proportional to, …).
  - EK: 'Rate of change of y is proportional to y' ⇒ dy/dt = ky; identify the dependent and independent variables first.
  - Needs: CA-4.3.A
  - P2 · drills: ca-write-de, ca-de-verify-solution

### 7.2 Verifying solutions



- ● **CA-7.2.A** (FUN-7.B, webwork-opl:DE1.1) Verify that a function solves a differential equation by substituting it and its derivatives.
  - EK: A solution makes the equation an identity for all t in an interval, not just at one point.
  - Needs: CA-3.6.A, CA-7.1.A
  - P3 · drills: ca-verify-solution, ca2-exponential-solution-k

### 7.3 Sketching slope fields



- ● **CA-7.3.A** (FUN-7.C, webwork-opl:DE2.12) Sketch a slope field for dy/dx = f(x, y) at given points.
  - EK: At each grid point draw a short segment with slope f(x, y); slopes depend on x only, y only, or both.
  - Needs: CA-7.2.A
  - P2 · P4 · drills: ca-slope-field-points, ca-slope-field-equilibrium

### 7.4 Reasoning with slope fields



- ● **CA-7.4.A** (FUN-7.C, webwork-opl:DE2.12) Match a slope field to its differential equation and sketch the solution through a given point.
  - EK: Check where slopes are 0, where they are constant along vertical or horizontal lines, and their sign in each quadrant; solution curves follow the segments.
  - Needs: CA-7.3.A
  - P2 · drills: ca-slope-field-match, ca-slope-field-feature

### 7.5 Euler's method (BC only)



- ● **CA-7.5.A** (FUN-7.C, webwork-opl:DE6.1) Approximate a solution value with a few steps of Euler's method, and say whether it over- or under-estimates.
  - EK: y_(n+1) = y_n + h·f(x_n, y_n); concave-up solutions are underestimated (tangent-line steps lie below).
  - Needs: CA-7.4.A, CA-4.6.B
  - P1 · P3 · drills: ca-euler-method, ca-euler-vs-exact

### 7.6 Separation of variables — general solutions



- ● **CA-7.6.A** (FUN-7.D, webwork-opl:DE2.3) Find the general solution of a separable differential equation.
  - EK: dy/dx = g(x)h(y) ⇒ ∫dy/h(y) = ∫g(x)dx + C; one constant is enough.
  - Needs: CA-6.9.A, CA-7.2.A
  - P1 · drills: ca-separable-general, ca-separable-constant

### 7.7 Separation of variables — particular solutions



- ● **CA-7.7.A** (FUN-7.E, webwork-opl:DE2.3) Find the particular solution of a separable IVP, solve for y, and state its domain.
  - EK: Use the initial condition to find C before solving for y; the domain is the interval containing x₀ where the solution is defined.
  - Needs: CA-7.6.A
  - P1 · P3 · drills: ca-separable-ivp, ca-ivp-domain

### 7.8 Exponential models



- ● **CA-7.8.A** (FUN-7.F, FUN-7.G, webwork-opl:DE2.6) Solve dy/dt = ky, apply it to growth, decay and Newton cooling, and find a doubling time, half-life or time to reach a value.
  - EK: y = y₀e^(kt); dT/dt = −k(T − T_a) ⇒ T = T_a + (T₀ − T_a)e^(−kt); t_double = ln 2/k, t_half = ln 2/|k|.
  - Needs: CA-7.7.A
  - P1 · P3 · drills: ca-exponential-growth, ca-half-life, ca-newton-cooling

### 7.9 Logistic models (BC only)



- ● **CA-7.9.A** (FUN-7.H, webwork-opl:DE2.7) Find the carrying capacity, the long-run limit and the population at which growth is fastest from a logistic differential equation.
  - EK: dy/dt = ky(1 − y/L): y → L for y₀ > 0; growth is fastest at y = L/2, where the solution inflects.
  - Needs: CA-7.8.A, CA-5.6.A
  - P2 · P3 · drills: ca-logistic, ca2-logistic-k

## Unit 8 · Applications of integration

Big ideas: CHA, LIM

### 8.1 Average value of a function



- ● **CA-8.1.A** (CHA-4.B, webwork-opl:CA6.1) Find the average value of a function on an interval.
  - EK: f_avg = (1/(b − a))∫_a^b f(x)dx — the height of the rectangle with the same area.
  - Needs: CA-6.7.A
  - P1 · drills: ca-average-value, ca2-average-value

### 8.2 Position, velocity and acceleration with integrals



- ● **CA-8.2.A** (CHA-4.C, webwork-opl:CA6.10) Find displacement, total distance and position at a time from a velocity function.
  - EK: Displacement = ∫v dt; distance = ∫|v| dt (split at sign changes); x(t) = x(0) + ∫_0^t v.
  - Needs: CA-6.7.A, CA-4.2.A
  - P1 · P3 · drills: ca-distance, ca2-turn-time

### 8.3 Accumulation in applied contexts



- ● **CA-8.3.A** (CHA-4.D, CHA-4.E, webwork-opl:CA6.14) Find an amount at a time from an initial amount plus the integral of a net rate (in − out), and interpret the integral in context with units.
  - EK: A(t) = A(0) + ∫_0^t (in − out) dt; ∫_a^b r(t)dt is net change, in rate units × time units.
  - Needs: CA-6.7.A
  - P1 · P4 · drills: ca-net-change-tank, ca-net-vs-total

### 8.4 Area between curves (functions of x)



- ● **CA-8.4.A** (CHA-5.A, webwork-opl:CA6.2) Find the area between two curves y = f(x), y = g(x), finding the limits from their intersections.
  - EK: A = ∫(top − bottom)dx.
  - Needs: CA-6.7.A
  - P1 · drills: ca-area-between, ca2-area-reverse

### 8.5 Area between curves (functions of y)



- ● **CA-8.5.A** (CHA-5.A, webwork-opl:CA6.2) Find the area between curves x = f(y), x = g(y) by integrating in y.
  - EK: A = ∫(right − left)dy; choose y when slicing in x would need two integrals.
  - Needs: CA-8.4.A
  - P1 · P2 · drills: ca-area-between-y, ca-area-x-vs-y

### 8.6 Curves that intersect more than twice



- ● **CA-8.6.A** (CHA-5.A, webwork-opl:CA6.2) Find the area enclosed by curves that cross several times by splitting the interval at each intersection.
  - EK: A = ∫|f − g|dx: the top curve changes at each crossing.
  - Needs: CA-8.4.A
  - P1 · drills: ca-area-crossings, ca-area-two-curves

### 8.7 Cross sections — squares and rectangles



- ● **CA-8.7.A** (CHA-5.B, webwork-opl:CA6.3) Find the volume of a solid with square or rectangular cross sections perpendicular to an axis.
  - EK: V = ∫A(x)dx; side s = top − bottom ⇒ A = s² (or s·(given height)).
  - Needs: CA-8.4.A
  - P1 · P2 · drills: ca-volume-squares, ca-cross-section-squares-y

### 8.8 Cross sections — triangles and semicircles



- ● **CA-8.8.A** (CHA-5.B, webwork-opl:CA6.3) Find the volume of a solid with triangular or semicircular cross sections.
  - EK: Equilateral: (√3/4)s²; isosceles right on a leg: s²/2; semicircle on diameter s: (π/8)s².
  - Needs: CA-8.7.A
  - P1 · drills: ca-volume-semicircles, ca-cross-section-triangles

### 8.9 Disc method about the x- or y-axis



- ● **CA-8.9.A** (CHA-5.C, webwork-opl:CA6.4) Find the volume of a solid of revolution about a coordinate axis by discs.
  - EK: V = π∫R(x)²dx, R = distance from axis to curve.
  - Needs: CA-8.7.A
  - P1 · drills: ca-volume-disc, ca2-shell-volume

### 8.10 Disc method about other axes



- ● **CA-8.10.A** (CHA-5.C, webwork-opl:CA6.4) Find a disc-method volume about a horizontal or vertical line other than an axis.
  - EK: Revolving about y = k: R = |f(x) − k|.
  - Needs: CA-8.9.A
  - P1 · drills: ca-volume-disc-line, ca-disc-about-axis

### 8.11 Washer method about the x- or y-axis



- ● **CA-8.11.A** (CHA-5.C, webwork-opl:CA6.5) Find the volume of a solid of revolution with a hole by washers about a coordinate axis.
  - EK: V = π∫(R² − r²)dx: outer radius squared minus inner radius squared, not (R − r)².
  - Needs: CA-8.9.A
  - P1 · drills: ca-volume-washer, ca-washer-setup

### 8.12 Washer method about other axes



- ● **CA-8.12.A** (CHA-5.C, webwork-opl:CA6.5) Find a washer-method volume about a line other than an axis.
  - EK: Both radii are distances from the axis of revolution: R = |far curve − k|, r = |near curve − k|.
  - Needs: CA-8.10.A, CA-8.11.A
  - P1 · drills: ca-volume-washer-line, ca-washer-about-line-above

### 8.13 Arc length and distance travelled (BC only)



- ● **CA-8.13.A** (CHA-6.A, webwork-opl:CA6.8) Set up and evaluate the arc length of a smooth curve y = f(x).
  - EK: L = ∫_a^b √(1 + f′(x)²)dx.
  - Needs: CA-6.7.A
  - P1 · drills: ca-arc-length, ca-arc-length-line

### 8.14 Physical applications (beyond the CED)



- ● **CA-8.14.A** (CHA-4.E, webwork-opl:CA6.11) Compute work done by a variable force or in pumping a fluid by slicing and integrating.
  - EK: W = ∫F(x)dx; pumping: W = ∫ρg·A(y)·(lift distance)dy.
  - Needs: CA-8.3.A
  - P1 · P4 · drills: ca-work-spring, ca-pumping-work

## Unit 9 · Parametric equations, polar coordinates and vector-valued functions (BC only)

Big ideas: CHA, FUN

### 9.1 Derivatives of parametric equations



- ● **CA-9.1.A** (CHA-3.G, webwork-opl:CA8.1, webwork-opl:CA8.3) Find dy/dx and tangent lines for a parametric curve, including horizontal and vertical tangents.
  - EK: dy/dx = (dy/dt)/(dx/dt); horizontal where dy/dt = 0, vertical where dx/dt = 0.
  - Needs: CA-3.5.A, CA-2.2.B
  - P1 · drills: ca-parametric-slope, ca-parametric-horizontal

### 9.2 Second derivatives of parametric equations



- ● **CA-9.2.A** (CHA-3.G, webwork-opl:CA8.4) Find d²y/dx² for a parametric curve and use it for concavity.
  - EK: d²y/dx² = (d/dt(dy/dx))/(dx/dt) — divide by dx/dt again, not by d²x/dt².
  - Needs: CA-9.1.A
  - P1 · drills: ca-parametric-slope, ca-parametric-concavity

### 9.3 Arc length of parametric curves



- ● **CA-9.3.A** (CHA-6.B, webwork-opl:CA8.5) Find the arc length of a parametric curve.
  - EK: L = ∫√((dx/dt)² + (dy/dt)²)dt.
  - Needs: CA-9.1.A, CA-8.13.A
  - P1 · drills: ca-parametric-arc, ca-speed-parametric

### 9.4 Derivatives of vector-valued functions



- ● **CA-9.4.A** (CHA-3.H) Differentiate a vector-valued function to get velocity and acceleration vectors.
  - EK: r(t) = ⟨x(t), y(t)⟩ ⇒ v = ⟨x′, y′⟩, a = ⟨x″, y″⟩, componentwise.
  - Needs: CA-9.1.A
  - P1 · P4 · drills: ca-vector-velocity, ca-vector-acceleration

### 9.5 Integrating vector-valued functions



- ● **CA-9.5.A** (FUN-8.A) Integrate a velocity or acceleration vector with an initial condition to recover position.
  - EK: Integrate each component; one constant vector fixed by r(t₀).
  - Needs: CA-9.4.A, CA-6.7.A
  - P1 · drills: ca-vector-position, ca-displacement-vector

### 9.6 Motion with parametric and vector functions



- ● **CA-9.6.A** (FUN-8.B, webwork-opl:CA8.3) Find speed, displacement and total distance for planar motion given by vectors.
  - EK: Speed = |v| = √(x′² + y′²); distance = ∫|v|dt; displacement = ∫v dt (a vector).
  - Needs: CA-9.5.A, CA-9.3.A
  - P1 · P3 · drills: ca-planar-distance, ~ca-vector-velocity

### 9.7 Polar coordinates and their derivatives



- ● **CA-9.7.A** (FUN-3.G, webwork-opl:CA9.8) Convert points and curves between polar and rectangular form.
  - EK: x = r cos θ, y = r sin θ, r² = x² + y², tan θ = y/x (watch the quadrant).
  - P2 · drills: ca-polar-convert, ca-rect-to-polar
- ● **CA-9.7.B** (FUN-3.G, webwork-opl:CA9.5) Find dy/dx for a polar curve and interpret dr/dθ.
  - EK: Treat θ as the parameter: x = r(θ)cos θ, y = r(θ)sin θ; dr/dθ > 0 ⇒ moving away from the pole.
  - Needs: CA-9.7.A, CA-9.1.A
  - P1 · P2 · drills: ca-polar-slope, ca-polar-slope-reason

### 9.8 Area of a polar region



- ● **CA-9.8.A** (CHA-5.D, webwork-opl:CA9.6) Find the area enclosed by a single polar curve, finding the θ-limits from where r = 0 or the curve closes.
  - EK: A = ½∫_α^β r(θ)²dθ.
  - Needs: CA-9.7.A, CA-6.7.A
  - P1 · drills: ca-polar-area, ca-polar-rose

### 9.9 Area between two polar curves



- ● **CA-9.9.A** (CHA-5.D, webwork-opl:CA9.6) Find the area inside one polar curve and outside another.
  - EK: A = ½∫(r_outer² − r_inner²)dθ between intersection angles.
  - Needs: CA-9.8.A
  - P1 · drills: ca-polar-between, ca-polar-area-petal

## Unit 10 · Infinite sequences and series (BC only)

Big ideas: LIM, FUN

### 10.1 Convergent and divergent series



- ● **CA-10.1.A** (LIM-7.A, webwork-opl:CA7.2, webwork-opl:CA7.3) Define a series' sum as the limit of its partial sums and decide convergence from a partial-sum formula.
  - EK: S_n = a₁ + … + a_n; Σa_n converges to S ⇔ S_n → S. Telescoping series collapse S_n.
  - Needs: CA-1.15.A
  - P3 · P4 · drills: ca-partial-sums, ca-telescoping-sum

### 10.2 Geometric series



- ● **CA-10.2.A** (LIM-7.A, webwork-opl:CA7.5) Decide whether a geometric series converges and find its sum.
  - EK: Σ_(n=0)^∞ ar^n = a/(1 − r) if |r| < 1; diverges if |r| ≥ 1.
  - Needs: CA-10.1.A
  - P1 · drills: ca-geometric-series, ca2-geometric-series-sum

### 10.3 The nth-term test



- ● **CA-10.3.A** (LIM-7.A, webwork-opl:CA7.6) Show a series diverges with the nth-term test, and explain why the test can't prove convergence.
  - EK: a_n ↛ 0 ⇒ diverges; a_n → 0 says nothing (harmonic series).
  - Needs: CA-10.1.A, CA-4.7.A
  - P3 · drills: ca-nth-term-test, ca-geometric-sum

### 10.4 The integral test



- ● **CA-10.4.A** (LIM-7.A, webwork-opl:CA7.8) Apply the integral test after checking positivity, continuity and decrease.
  - EK: f positive, continuous, decreasing, a_n = f(n) ⇒ Σa_n and ∫_1^∞ f dx converge or diverge together.
  - Needs: CA-10.3.A, CA-6.13.A
  - P3 · drills: ca-integral-test, ca-p-series-pick

### 10.5 Harmonic series and p-series



- ● **CA-10.5.A** (LIM-7.A, webwork-opl:CA7.8) Decide convergence of a p-series and recognise the harmonic series.
  - EK: Σ1/n^p converges ⇔ p > 1; Σ1/n diverges.
  - Needs: CA-10.4.A
  - P3 · drills: ca-p-series, ca2-p-series-pick

### 10.6 Comparison tests



- ● **CA-10.6.A** (LIM-7.A, webwork-opl:CA7.7) Decide convergence with the direct or limit comparison test against a geometric or p-series.
  - EK: 0 ≤ a_n ≤ b_n: Σb_n conv ⇒ Σa_n conv; lim a_n/b_n = c, 0 < c < ∞ ⇒ same behaviour.
  - Needs: CA-10.5.A, CA-10.2.A
  - P3 · drills: ca-comparison-test, ca-limit-comparison-ratio

### 10.7 The alternating series test



- ● **CA-10.7.A** (LIM-7.A, webwork-opl:CA7.11) Show an alternating series converges by checking that |a_n| decreases to 0.
  - EK: Σ(−1)^n b_n with b_n decreasing and b_n → 0 converges.
  - Needs: CA-10.3.A
  - P3 · drills: ca-alternating-series-test, ~ca-absolute-conditional

### 10.8 The ratio test



- ● **CA-10.8.A** (LIM-7.A, webwork-opl:CA7.9) Apply the ratio test, especially to series with factorials or exponentials.
  - EK: L = lim|a_(n+1)/a_n|: L < 1 converges absolutely, L > 1 diverges, L = 1 inconclusive.
  - Needs: CA-10.2.A
  - P1 · P3 · drills: ca-ratio-test, ca2-ratio-limit

### 10.9 Absolute and conditional convergence



- ● **CA-10.9.A** (LIM-7.A, webwork-opl:CA7.12) Classify a series as absolutely convergent, conditionally convergent or divergent.
  - EK: Σ|a_n| converges ⇒ absolute; Σa_n converges but Σ|a_n| doesn't ⇒ conditional (e.g. alternating harmonic).
  - Needs: CA-10.7.A, CA-10.6.A
  - P3 · drills: ca-absolute-conditional, ca-alternating-converge-pick

### 10.10 Alternating series error bound



- ● **CA-10.10.A** (LIM-7.B, webwork-opl:CA7.11) Bound the error of a partial sum of an alternating series.
  - EK: |S − S_n| ≤ b_(n+1), the first omitted term; the sign of the error is that of the first omitted term.
  - Needs: CA-10.7.A
  - P1 · P3 · drills: ca-alternating-error, ca-alternating-terms-needed

### 10.11 Taylor polynomials



- ● **CA-10.11.A** (LIM-8.A, LIM-8.B, webwork-opl:CA7.4) Build the nth-degree Taylor polynomial about x = a and use it to approximate a function value (or read derivatives off its coefficients).
  - EK: P_n(x) = Σ_(k=0)^n f^(k)(a)(x − a)^k/k!; coefficient of (x − a)^k is f^(k)(a)/k!; P₁ is the tangent line.
  - Needs: CA-3.6.A, CA-4.6.A
  - P1 · P2 · drills: ca-taylor-exp, ca-taylor-ln, ca-taylor-coefficients, ca2-taylor-coefficient

### 10.12 The Lagrange error bound



- ● **CA-10.12.A** (LIM-8.C, webwork-opl:CA7.19) Bound the error of a Taylor approximation with the Lagrange error bound.
  - EK: |f(x) − P_n(x)| ≤ max|f^(n+1)|·|x − a|^(n+1)/(n + 1)!, max taken between a and x.
  - Needs: CA-10.11.A
  - P1 · P3 · drills: ca-lagrange-bound, ca-lagrange-degree

### 10.13 Radius and interval of convergence



- ● **CA-10.13.A** (LIM-8.D, webwork-opl:CA7.14) Find the radius and interval of convergence of a power series, testing each endpoint separately.
  - EK: Ratio test gives |x − a| < R; at x = a ± R the series is an ordinary series — use p-series, alternating or comparison tests.
  - Needs: CA-10.8.A, CA-10.9.A
  - P1 · P3 · drills: ca-radius-convergence, ca-radius-ratio

### 10.14 Taylor and Maclaurin series



- ● **CA-10.14.A** (LIM-8.E, webwork-opl:CA7.15, webwork-opl:CA7.16) Write the Taylor or Maclaurin series of a function in sigma notation with its general term.
  - EK: Σ f^(n)(a)(x − a)^n/n!; e^x = Σx^n/n!, sin x = Σ(−1)^n x^(2n+1)/(2n+1)!, cos x = Σ(−1)^n x^(2n)/(2n)!, 1/(1 − x) = Σx^n.
  - Needs: CA-10.11.A, CA-10.13.A
  - P1 · P4 · drills: ca-series-general-term, ca2-maclaurin-coefficient
- ● **CA-10.14.B** (LIM-8.F, webwork-opl:CA7.16) Interpret a Taylor series: use it to evaluate a limit, a derivative value or a sum.
  - EK: Inside its interval of convergence the series equals the function; e.g. Σ1/n! = e.
  - Needs: CA-10.14.A
  - P2 · P3 · drills: ca-series-use, ca-series-coefficient

### 10.15 Representing functions as power series



- ● **CA-10.15.A** (LIM-8.G, webwork-opl:CA7.17, webwork-opl:CA7.18) Build a power series for a new function by substitution, multiplication, or term-by-term differentiation or integration of a known series.
  - EK: 1/(1 + x²) = Σ(−1)^n x^(2n); integrate ⇒ arctan x = Σ(−1)^n x^(2n+1)/(2n+1). Differentiating or integrating keeps the radius.
  - Needs: CA-10.14.A
  - P1 · drills: ca-series-build, ~sigma-derivative
- ● **CA-10.15.B** (LIM-8.G, webwork-opl:CA7.17) Shift a summation index so two power series start at the same index and carry the same power of x, then combine them.
  - EK: Replace n by n ± k and adjust the limits; the sum is unchanged. Needed for power-series solutions of ODEs (beyond the CED).
  - Needs: CA-10.15.A
  - P1 · P4 · drills: sigma-shift-down, sigma-shift-up, sigma-prefactor, sigma-derivative, sigma-combine

### 10.16 Complex exponentials (beyond the CED)



- ● **CA-10.16.A** (LIM-8.F, N-CN.B.4, webwork-opl:CX6.1) Derive Euler's formula from the Maclaurin series of e^x, cos x and sin x, and convert complex numbers between rectangular, polar and exponential form.
  - EK: Put x = iθ in Σx^n/n! and sort real and imaginary terms: e^(iθ) = cos θ + i sin θ; z = re^(iθ), r = |z|, θ = arg z.
  - Needs: CA-10.14.A, CA-9.7.A
  - P2 · P1 · drills: euler-rect, euler-polar, euler-re-im
- ● **CA-10.16.B** (N-CN.B.5, webwork-opl:CX1.9) Compute powers and roots of a complex number with De Moivre's formula.
  - EK: (re^(iθ))^n = r^n e^(inθ); n distinct n-th roots spaced 2π/n apart.
  - Needs: CA-10.16.A
  - P1 · drills: euler-demoivre, ca-complex-modulus-power
- ● **CA-10.16.C** (N-CN.C.7, webwork-opl:CX2.2) Find the complex roots α ± βi of a real quadratic and write e^((α ± iβ)x) as e^(αx)(cos βx ± i sin βx).
  - EK: α = −b/2a, β = √(4ac − b²)/2a; complex roots of real polynomials come in conjugate pairs.
  - Needs: CA-10.16.A
  - P1 · drills: euler-quad-roots, ca-complex-root-real-part

## Unit 11 · Vectors and the geometry of space (extension)

Big ideas: FUN, CHA

### 11.1 Three-dimensional coordinates and vectors

Book: stewart-8e §12.1, §12.2

- ● **CA-11.1.A** (ST-12.1, ST-12.2, webwork-opl:MV3.2) Compute distances and spheres in 3-D, and add, scale and normalise vectors in components.
  - EK: |P₁P₂| = √(Δx² + Δy² + Δz²); (x − h)² + (y − k)² + (z − l)² = r²; |v| = √(v·v), û = v/|v|.
  - P1 · P4 · drills: cm-distance-3d, cm-unit-vector-component

### 11.2 The dot product

Book: stewart-8e §12.3

- ● **CA-11.2.A** (ST-12.3) Use the dot product for angles, orthogonality, projections and the work of a constant force.
  - EK: a·b = |a||b|cos θ, = 0 ⇔ perpendicular; proj_a b = (a·b/|a|²)a; W = F·D.
  - Needs: CA-11.1.A
  - P1 · drills: cm-dot-product, cm-projection-length

### 11.3 The cross product

Book: stewart-8e §12.4

- ● **CA-11.3.A** (ST-12.4) Compute a cross product as a 3×3 determinant and use it for a normal vector, parallelogram area or torque.
  - EK: a × b ⊥ both, |a × b| = |a||b|sin θ = parallelogram area; right-hand rule; b × a = −a × b.
  - Needs: CA-11.2.A
  - P1 · drills: cm-cross-product, cm-triangle-area

### 11.4 Lines and planes

Book: stewart-8e §12.5

- ● **CA-11.4.A** (ST-12.5, webwork-opl:MV2.1) Write vector, parametric and symmetric equations of a line from a point and a direction or two points.
  - EK: r = r₀ + tv.
  - Needs: CA-11.1.A
  - P1 · P4 · drills: cm-line-plane-hit, cm-line-distance-point
- ● **CA-11.4.B** (ST-12.5) Write the equation of a plane from a point and normal, or from three points, and find the distance from a point to a plane.
  - EK: n·(r − r₀) = 0 ⇒ ax + by + cz = d; normal from (P₂ − P₁) × (P₃ − P₁); D = |ax₁ + by₁ + cz₁ − d|/|n|.
  - Needs: CA-11.3.A, CA-11.4.A
  - P1 · drills: cm-plane, cm-plane-distance

### 11.5 Cylinders and quadric surfaces

Book: stewart-8e §12.6

- ● **CA-11.5.A** (ST-12.6, webwork-opl:MV3.3) Identify and sketch a quadric surface from its equation using traces.
  - EK: Set x, y or z constant and read the conic: ellipsoid, paraboloid, hyperboloid of one or two sheets, cone, cylinder.
  - Needs: CA-11.1.A
  - P2 · P4 · drills: ca-quadric, ca-quadric-traces

### 11.6 Vector functions and space curves

Book: stewart-8e §13.1, §13.2, §13.3, §13.4

- ● **CA-11.6.A** (ST-13.2, webwork-opl:MV2.3, webwork-opl:MV2.4) Differentiate and integrate a 3-D vector function and find the unit tangent and tangent line.
  - EK: Componentwise, as in the plane; T = r′/|r′|.
  - Needs: CA-9.5.A, CA-11.4.A
  - P1 · drills: cm-vector-function, cm-curve-speed
- ● **CA-11.6.B** (ST-13.3, ST-13.4, webwork-opl:MV2.5, webwork-opl:MV2.6) Find arc length, curvature, and the tangential and normal components of acceleration of a space curve.
  - EK: L = ∫|r′|dt; κ = |r′ × r″|/|r′|³; a_T = v·a/|v|, a_N = |v × a|/|v|.
  - Needs: CA-11.6.A, CA-11.3.A, CA-9.6.A
  - P1 · P3 · drills: cm-helix, cm-circle-curvature

## Unit 12 · Partial derivatives (extension)

Big ideas: CHA, LIM, FUN

### 12.1 Functions of several variables, limits and continuity

Book: stewart-8e §14.1, §14.2

- ● **CA-12.1.A** (ST-14.1, webwork-opl:MV3.1, webwork-opl:MV3.6) Find the domain of a function of two or three variables and sketch its level curves or describe its level surfaces.
  - EK: Level curve f(x, y) = k; close spacing means steep.
  - Needs: CA-11.5.A
  - P2 · drills: ca-domain-level-curve, ca-level-curve-shape
- ● **CA-12.1.B** (ST-14.2, webwork-opl:MV4.1) Show a two-variable limit does not exist by approaching along two paths that give different values.
  - EK: Limit must be the same along every path to (a, b); try lines y = mx and curves like y = x².
  - Needs: CA-12.1.A, CA-1.2.B
  - P3 · drills: ca-two-path-limit, mvd-two-path

### 12.2 Partial derivatives

Book: stewart-8e §14.3

- ● **CA-12.2.A** (ST-14.3, webwork-opl:MV4.2) Compute first partial derivatives and interpret each as a slope with the other variables held fixed.
  - EK: ∂f/∂x: differentiate in x, treat y as a constant; it is the slope of the trace y = b.
  - Needs: CA-12.1.A, CA-3.5.A
  - P1 · P2 · drills: mv-partial, mvd-partial
- ● **CA-12.2.B** (ST-14.3, webwork-opl:MV4.2) Compute second and mixed partial derivatives and use Clairaut's theorem.
  - EK: f_xy = f_yx when the mixed partials are continuous.
  - Needs: CA-12.2.A
  - P1 · drills: mv-mixed, mvd-mixed

### 12.3 Tangent planes and linear approximation

Book: stewart-8e §14.4

- ● **CA-12.3.A** (ST-14.4, webwork-opl:MV4.4) Write the tangent plane to z = f(x, y), and estimate a change or a propagated error with the total differential.
  - EK: z − z₀ = f_x(a, b)(x − a) + f_y(a, b)(y − b); dz = f_x dx + f_y dy.
  - Needs: CA-12.2.A, CA-4.6.A
  - P1 · P4 · drills: cm-tangent-plane, mvd-linearize

### 12.4 The multivariable chain rule

Book: stewart-8e §14.5

- ● **CA-12.4.A** (ST-14.5, webwork-opl:MV4.3) Apply the chain rule to a function of intermediate variables, drawing the dependency tree.
  - EK: z = f(x, y), x = x(s, t), y = y(s, t) ⇒ ∂z/∂s = f_x x_s + f_y y_s — one term per path in the tree.
  - Needs: CA-12.2.A, CA-3.1.A
  - P1 · drills: cm-chain-rule, mvd-chain-t, mvd-chain-partial
- ● **CA-12.4.B** (ST-14.5, webwork-opl:MV4.3) Find dy/dx or ∂z/∂x for an implicitly defined function with partial derivatives.
  - EK: F(x, y) = 0 ⇒ dy/dx = −F_x/F_y; F(x, y, z) = 0 ⇒ ∂z/∂x = −F_x/F_z.
  - Needs: CA-12.4.A, CA-3.2.A
  - P1 · drills: mv-implicit, mvd-implicit, mvd-implicit-3

### 12.5 Directional derivatives and the gradient

Book: stewart-8e §14.6

- ● **CA-12.5.A** (ST-14.6, webwork-opl:MV4.5) Compute the gradient and the directional derivative in a given direction.
  - EK: ∇f = ⟨f_x, f_y, f_z⟩; D_u f = ∇f·u with u a unit vector.
  - Needs: CA-12.2.A, CA-11.2.A
  - P1 · drills: cm-gradient, mvd-directional, ~mv-partial
- ● **CA-12.5.B** (ST-14.6, webwork-opl:MV4.5) Use the gradient to find the direction and rate of steepest ascent and the tangent plane to a level surface.
  - EK: Max rate |∇f| in direction ∇f; ∇F ⊥ the level surface F = k, so it is the plane's normal.
  - Needs: CA-12.5.A, CA-11.4.B
  - P2 · P3 · drills: cm-gradient, mvd-max-rate, mvd-tangent-plane-implicit, mvd-level-slope, mvd-gradient-facts

### 12.6 Maximum and minimum values

Book: stewart-8e §14.7

- ● **CA-12.6.A** (ST-14.7, webwork-opl:MV4.6, webwork-opl:MV6.2) Find and classify the critical points of f(x, y) with the second derivatives test.
  - EK: ∇f = 0; D = f_xx f_yy − f_xy²: D > 0, f_xx > 0 min; D > 0, f_xx < 0 max; D < 0 saddle; D = 0 inconclusive.
  - Needs: CA-12.2.B, CA-5.7.A
  - P1 · P3 · drills: cm-critical-point, mvd-classify, mvd-critical-count
- ● **CA-12.6.B** (ST-14.7, webwork-opl:MV4.6) Find absolute extrema of f on a closed bounded region by checking interior critical points and the boundary.
  - EK: Parametrise each boundary piece and reduce to one-variable problems; compare all candidates (EVT in 2-D).
  - Needs: CA-12.6.A, CA-5.5.A
  - P1 · P3 · drills: ca-extrema-region, ca-critical-point-classify

### 12.7 Lagrange multipliers

Book: stewart-8e §14.8

- ● **CA-12.7.A** (ST-14.8, webwork-opl:MV4.7) Optimise f subject to a constraint g = k with Lagrange multipliers, and interpret λ.
  - EK: ∇f = λ∇g and g = k; λ = rate of change of the optimum with respect to k.
  - Needs: CA-12.5.B, CA-12.6.B
  - P1 · P3 · drills: cm-lagrange-product, cm-lagrange-circle, mvd-lagrange, mvd-lagrange-two

## Unit 13 · Multiple integrals (extension)

Big ideas: CHA, LIM

### 13.1 Double integrals over rectangles

Book: stewart-8e §15.1, §15.2

- ● **CA-13.1.A** (ST-15.1, ST-15.2, webwork-opl:MV5.1, webwork-opl:MV5.2) Evaluate a double integral over a rectangle as an iterated integral, in either order.
  - EK: Fubini: ∬_R f dA = ∫_a^b∫_c^d f dy dx = ∫_c^d∫_a^b f dx dy for continuous f; a double Riemann-sum limit.
  - Needs: CA-6.7.A, CA-6.3.A
  - P1 · drills: cm-double-rect, cm-double-integral-order

### 13.2 Double integrals over general regions

Book: stewart-8e §15.3

- ● **CA-13.2.A** (ST-15.3, webwork-opl:MV5.3) Set up a double integral over a region bounded by curves as type I or type II, and evaluate it.
  - EK: Type I: x from a to b, y from g₁(x) to g₂(x). Inner limits may depend on the outer variable, never the reverse.
  - Needs: CA-13.1.A, CA-8.4.A
  - P1 · P2 · drills: cm-double-region, mvd-region-setup, mvd-region-value
- ● **CA-13.2.B** (ST-15.3, webwork-opl:MV5.3) Reverse the order of integration by redrawing the region.
  - EK: Sketch the region, then read the new limits from the other direction; used when the inner integral has no elementary antiderivative.
  - Needs: CA-13.2.A, CA-8.5.A
  - P2 · drills: cm-reverse-order, mvd-reverse-setup

### 13.3 Double integrals in polar coordinates

Book: stewart-8e §15.4

- ● **CA-13.3.A** (ST-15.4, webwork-opl:MV5.4) Convert a double integral over a disc, annulus or polar region to polar coordinates and evaluate it.
  - EK: dA = r dr dθ — don't drop the r.
  - Needs: CA-13.2.A, CA-9.8.A
  - P1 · drills: cm-double-polar, cm-gaussian-polar, mvd-polar-setup, mvd-polar-value

### 13.4 Applications of double integrals

Book: stewart-8e §15.5

- ● **CA-13.4.A** (ST-15.5, webwork-opl:CA6.13, webwork-opl:MV5.8) Compute the mass, centre of mass and moments of inertia of a lamina, and the average value of f over a region.
  - EK: m = ∬ρ dA; x̄ = ∬xρ dA/m; I_x = ∬y²ρ dA; f_avg = ∬f dA/area.
  - Needs: CA-13.2.A, CA-8.4.A
  - P1 · P4 · drills: cm-center-of-mass, mvd-center-mass, mvd-average, mvd-inertia

### 13.5 Triple integrals

Book: stewart-8e §15.7

- ● **CA-13.5.A** (ST-15.7, webwork-opl:MV5.5, webwork-opl:MV5.9) Set up and evaluate a triple integral over a solid bounded by surfaces, and use it for volume or mass.
  - EK: Project the solid onto a coordinate plane for the outer two limits; the inner limits are the bottom and top surfaces.
  - Needs: CA-13.2.A, CA-11.5.A
  - P1 · P2 · drills: cm-tetrahedron, mvd-triple-setup, mvd-triple-value, mvd-coordinates, mvd-center-mass-solid, mvd-triple-order

### 13.6 Triple integrals in cylindrical coordinates

Book: stewart-8e §15.8

- ● **CA-13.6.A** (ST-15.8, webwork-opl:MV3.4, webwork-opl:MV5.7) Evaluate a triple integral in cylindrical coordinates for solids with an axis of symmetry.
  - EK: x = r cos θ, y = r sin θ, z = z; dV = r dz dr dθ.
  - Needs: CA-13.5.A, CA-13.3.A
  - P1 · drills: cm-cylindrical, mvd-triple-setup, mvd-triple-value

### 13.7 Triple integrals in spherical coordinates

Book: stewart-8e §15.9

- ● **CA-13.7.A** (ST-15.9, webwork-opl:MV3.4, webwork-opl:MV5.7) Evaluate a triple integral in spherical coordinates for balls, cones and shells.
  - EK: x = ρ sin φ cos θ, y = ρ sin φ sin θ, z = ρ cos φ; dV = ρ² sin φ dρ dφ dθ.
  - Needs: CA-13.6.A
  - P1 · drills: cm-spherical, mvd-triple-setup, mvd-triple-value

### 13.8 Change of variables and the Jacobian

Book: stewart-8e §15.10

- ● **CA-13.8.A** (ST-15.10, webwork-opl:MV5.6) Change variables in a double or triple integral with the Jacobian determinant.
  - EK: dx dy = |∂(x, y)/∂(u, v)| du dv; polar, cylindrical and spherical factors are special cases.
  - Needs: CA-13.7.A, CA-12.2.A
  - P1 · P3 · drills: cm-jacobian, mvd-jacobian, mvd-change-variables

## Unit 14 · Vector calculus (extension)

Big ideas: CHA, FUN

### 14.1 Vector fields

Book: stewart-8e §16.1

- ● **CA-14.1.A** (ST-16.1, webwork-opl:MV6.1) Sketch or read a 2-D vector field and recognise a gradient field.
  - EK: F(x, y) = ⟨P, Q⟩ assigns an arrow to each point; F = ∇f is a gradient (conservative) field with potential f.
  - Needs: CA-12.5.A
  - P2 · drills: ca-vector-field-match, ca-gradient-field-check

### 14.2 Line integrals

Book: stewart-8e §16.2

- ● **CA-14.2.A** (ST-16.2, webwork-opl:MV7.2) Evaluate a scalar line integral ∫_C f ds along a parametrised curve.
  - EK: ds = |r′(t)|dt; independent of orientation.
  - Needs: CA-14.1.A, CA-11.6.B
  - P1 · drills: cm-line-integral-scalar, mvd-scalar-line
- ● **CA-14.2.B** (ST-16.2, webwork-opl:MV7.2, webwork-opl:MV7.4) Evaluate the work or circulation ∫_C F·dr along a curve.
  - EK: ∫F(r(t))·r′(t)dt = ∫P dx + Q dy + R dz; reversing the orientation flips the sign.
  - Needs: CA-14.2.A
  - P1 · drills: cm-work-line, mvd-work, mvd-work-space

### 14.3 The fundamental theorem for line integrals

Book: stewart-8e §16.3

- ● **CA-14.3.A** (ST-16.3, webwork-opl:MV7.3) Test whether a 2-D field P i + Q j (or a differential P dx + Q dy) is conservative.
  - EK: On a simply connected region, conservative ⇔ ∂P/∂y = ∂Q/∂x — the same test as an exact differential.
  - Needs: CA-14.1.A, CA-12.2.B
  - P3 · drills: mv-exact-test, mvd-conservative
- ● **CA-14.3.B** (ST-16.3, webwork-opl:MV7.3, webwork-opl:MV8.1) Find a potential function and evaluate a line integral of a conservative field from endpoint values.
  - EK: f_x = P: integrate in x, differentiate in y, match Q; ∫_C ∇f·dr = f(end) − f(start), path-independent, 0 around a closed loop.
  - Needs: CA-14.3.A, CA-14.2.B
  - P1 · drills: cm-potential, mvd-potential-work

### 14.4 Green's theorem

Book: stewart-8e §16.4

- ● **CA-14.4.A** (ST-16.4, webwork-opl:MV8.2) Convert a line integral around a closed plane curve into a double integral with Green's theorem, or the reverse (including areas).
  - EK: ∮_C P dx + Q dy = ∬_D (Q_x − P_y)dA, C positively oriented (region on the left); area = ½∮x dy − y dx.
  - Needs: CA-14.2.B, CA-13.2.A
  - P1 · P3 · drills: cm-green, mvd-green, mvd-flux-plane, mvd-green-area

### 14.5 Curl and divergence

Book: stewart-8e §16.5

- ● **CA-14.5.A** (ST-16.5, webwork-opl:MV7.1, webwork-opl:MV7.5) Compute the divergence, curl and Laplacian of a vector or scalar field.
  - EK: div F = ∇·F; curl F = ∇ × F; ∇²f = ∇·∇f; curl ∇f = 0 and div curl F = 0.
  - Needs: CA-14.1.A, CA-11.3.A, CA-12.2.B
  - P1 · drills: cm-div-curl, cm-laplacian, mvd-div-curl, mvd-div-curl-facts
- ● **CA-14.5.B** (ST-16.5, webwork-opl:MV7.5) Interpret divergence as net outflow per volume and curl as local rotation, and use curl F = 0 to test a 3-D field for being conservative.
  - EK: div > 0 is a source; curl F = 0 on a simply connected domain ⇒ F = ∇f.
  - Needs: CA-14.5.A, CA-14.3.A
  - P2 · P3 · drills: ca-curl-conservative, mvd-conservative

### 14.6 Parametric surfaces and surface area

Book: stewart-8e §16.6

- ● **CA-14.6.A** (ST-16.6, webwork-opl:MV3.5) Parametrise a surface (graph, cylinder, sphere, cone) and compute its area.
  - EK: r(u, v); dS = |r_u × r_v| du dv; for z = g(x, y), dS = √(1 + g_x² + g_y²)dA.
  - Needs: CA-11.5.A, CA-11.3.A, CA-13.3.A
  - P1 · P2 · drills: cm-surface-area, mvd-surface-integral

### 14.7 Surface integrals and flux

Book: stewart-8e §16.7

- ● **CA-14.7.A** (ST-16.7, webwork-opl:MV7.6) Evaluate a surface integral ∬_S f dS of a scalar function.
  - EK: ∬f(r(u, v))|r_u × r_v| du dv.
  - Needs: CA-14.6.A
  - P1 · drills: cm-surface-integral, mvd-surface-integral
- ● **CA-14.7.B** (ST-16.7, webwork-opl:MV7.7) Compute the flux ∬_S F·n dS of a vector field through an oriented surface.
  - EK: ∬F·(r_u × r_v) du dv, with r_u × r_v pointing the chosen way (outward for closed surfaces).
  - Needs: CA-14.7.A
  - P1 · P4 · drills: cm-flux-disc, mvd-flux, mvd-orientation

### 14.8 Stokes' theorem

Book: stewart-8e §16.8

- ● **CA-14.8.A** (ST-16.8, webwork-opl:MV8.3) Use Stokes' theorem to trade a circulation around a closed curve for the flux of the curl through a surface it bounds, or the reverse.
  - EK: ∮_C F·dr = ∬_S (∇ × F)·n dS; orientation of C and n by the right-hand rule; any surface with the same boundary gives the same answer.
  - Needs: CA-14.7.B, CA-14.5.A, CA-14.4.A
  - P1 · P3 · drills: cm-stokes, mvd-stokes, mvd-which-theorem, mvd-stokes-surface

### 14.9 The divergence theorem

Book: stewart-8e §16.9

- ● **CA-14.9.A** (ST-16.9, webwork-opl:MV8.4) Use the divergence theorem to compute the outward flux through a closed surface as a volume integral, or the reverse.
  - EK: ∯_S F·n dS = ∭_E ∇·F dV, n outward.
  - Needs: CA-14.7.B, CA-14.5.A, CA-13.7.A
  - P1 · P3 · drills: cm-divergence-theorem, mvd-divergence-theorem, mvd-divergence-curved
- ● **CA-14.9.B** (ST-16.9, webwork-opl:FM3.1) Turn an integral balance on an arbitrary control volume into a differential conservation law with the divergence theorem.
  - EK: d/dt∭c dV = −∯N·n dS + ∭R dV for every volume ⇒ ∂c/∂t + ∇·N = R.
  - Needs: CA-14.9.A, CA-14.5.B
  - P2 · P3 · drills: ca-conservation-law, ca-continuity-1d

## Unit 15 · Hyperbolic functions

Big ideas: CHA

### 15.1 Definitions and identities



- ● **CA-15.1.A** (ST-3.11, webwork-opl:CA2.13) Recognise sinh, cosh and tanh from their exponential definitions and evaluate them at ln a.
  - EK: cosh x = ½(eˣ + e⁻ˣ), sinh x = ½(eˣ − e⁻ˣ); eˣ = cosh x + sinh x.
  - P1 · drills: hy-which-definition, hy-value-at-log, hy-tanh-value
- ● **CA-15.1.B** (ST-3.11, webwork-opl:CA2.13) Use cosh² − sinh² = 1 and the double-argument identities, and tell a true hyperbolic identity from a false one.
  - EK: Osborn's rule: flip the sign of any product of two sines.
  - P1 · drills: hy-pythagorean, hy-identity-check, hy-double-argument
- ● **CA-15.1.C** (ST-3.11) Describe the graphs: parity, range and behaviour for small and large x.
  - EK: cosh ≥ 1 and even; sinh odd and unbounded; tanh odd and between −1 and 1.
  - P1 · drills: hy-parity-and-range, hy-cosh-value

### 15.2 Calculus and uses



- ● **CA-15.2.A** (ST-3.11, webwork-opl:CA2.14, webwork-opl:CA5.6) Differentiate and integrate hyperbolic functions.
  - EK: sinh′ = cosh, cosh′ = sinh, tanh′ = sech²; no sign changes.
  - P1 · drills: hy-derivative-which, hy-derivative-value, hy-integral
- ● **CA-15.2.B** (ST-3.11) Write an inverse hyperbolic function as a logarithm.
  - EK: sinh⁻¹ s = ln(s + √(s² + 1)).
  - P1 · drills: hy-inverse-sinh, hy-arcsinh-value
- ● **CA-15.2.C** (ST-3.11) Solve y″ = k²y with cosh and sinh, connect them to the circular functions, and say where each turns up.
  - EK: cos(ix) = cosh x; catenary, fins and slabs use cosh; saturating ratios use tanh.
  - P1 · drills: hy-ode-solution, hy-circular-link, hy-where-used

## Unit 16 · Calculus in business, the sciences and probability

Big ideas: CHA

### 16.1 Derivatives in context



- ● **CA-16.1.A** (webwork-opl:CA3.3) Find a marginal cost or revenue as a derivative.
  - EK: Marginal cost C′(q) approximates the cost of one more unit.
  - P1 · drills: ca-marginal-cost
- ● **CA-16.1.B** (webwork-opl:CA3.11) Maximise profit from revenue and cost functions.
  - EK: Profit is maximal where marginal revenue equals marginal cost.
  - P1 · drills: ca-max-profit
- ● **CA-16.1.C** (webwork-opl:CA3.13) Optimise a model from the natural sciences.
  - EK: Set the derivative to zero and check that the critical point is a maximum.
  - P1 · drills: ca-peak-concentration
- ● **CA-16.1.D** (webwork-opl:CA3.18) Compute a price elasticity of demand.
  - EK: E = −(dq/dp)(p/q); |E| > 1 is elastic.
  - P1 · drills: ca-elasticity

### 16.2 Integrals in context



- ● **CA-16.2.A** (webwork-opl:CA6.15) Find a consumer surplus.
  - EK: CS = ∫₀^q₀ (demand price − market price) dq.
  - P1 · drills: ca-consumer-surplus
- ● **CA-16.2.B** (webwork-opl:CA6.16) Find cardiac output from a dye-dilution curve.
  - EK: F = amount injected / ∫ c dt.
  - P1 · drills: ca-cardiac-output
- ● **CA-16.2.C** (webwork-opl:CA6.17) Use a probability density function.
  - EK: A density integrates to 1; probabilities are areas under it.
  - P1 · drills: ca-pdf-constant

## Unit 17 · More integration techniques and applications

Big ideas: CHA

### 17.1 Techniques



- ● **CA-17.1.A** (webwork-opl:CA5.5) Integrate a product of powers of sine and cosine.
  - EK: With an odd power, save one factor and convert the rest; with even powers, use half-angle identities.
  - P1 · drills: ca-trig-integral
- ● **CA-17.1.B** (webwork-opl:CA5.8) Evaluate an integral by trigonometric substitution.
  - EK: √(a² − x²): x = a sin θ; √(a² + x²): x = a tan θ; √(x² − a²): x = a sec θ.
  - P1 · drills: ca-trig-substitution
- ● **CA-17.1.C** (webwork-opl:CA5.9) Use an integral from a table.
  - EK: Match the integrand to the table form, identify the constants, then substitute.
  - P1 · drills: ca-integral-table
- ● **CA-17.1.D** (webwork-opl:CA5.10) Use and check a computer algebra system's antiderivative.
  - EK: Differentiate the CAS answer to check it, then apply the fundamental theorem.
  - P1 · drills: ca-cas-antiderivative

### 17.2 Volumes, surfaces and forces



- ● **CA-17.2.A** (webwork-opl:CA6.6) Find a volume by cylindrical shells.
  - EK: V = ∫ 2π (radius)(height) dx.
  - P1 · drills: ca-shells
- ● **CA-17.2.B** (webwork-opl:CA6.7) Find the same volume by two methods.
  - EK: Discs or washers in one variable and shells in the other must agree.
  - P1 · drills: ca-two-methods
- ● **CA-17.2.C** (webwork-opl:CA6.9) Find the area of a surface of revolution.
  - EK: S = ∫ 2π y √(1 + y′²) dx.
  - P1 · drills: ca-surface-revolution
- ● **CA-17.2.D** (webwork-opl:CA6.12) Find the hydrostatic force on a submerged plate by integration.
  - EK: F = ∫ ρ g (depth) (width at that depth) d(depth).
  - P1 · drills: ca-hydrostatic-triangle

## Unit 18 · Sequences, series strategy, parametric and polar curves

Big ideas: CHA

### 18.1 Sequences and series



- ● **CA-18.1.A** (webwork-opl:CA7.1) Find the limit of a sequence.
  - EK: Divide by the highest power of n.
  - P1 · drills: ca-sequence-limit
- ● **CA-18.1.B** (webwork-opl:CA7.10) Apply the root test.
  - EK: L = lim |aₙ|^(1/n); converges if L < 1, diverges if L > 1.
  - P1 · drills: ca-root-test
- ● **CA-18.1.C** (webwork-opl:CA7.13) Choose a convergence test for a series.
  - EK: Look at the form: geometric, p-series, factorials (ratio), nth powers (root), alternating, or a comparison.
  - P1 · drills: ca-series-strategy

### 18.2 Parametric and polar curves



- ● **CA-18.2.A** (webwork-opl:CA8.2) Eliminate the parameter.
  - EK: Solve one equation for t and substitute into the other.
  - P1 · drills: ca-eliminate-parameter
- ● **CA-18.2.B** (webwork-opl:CA8.6) Find the area under a parametric curve.
  - EK: A = ∫ y dx = ∫ y(t) x′(t) dt.
  - P1 · drills: ca-parametric-area
- ● **CA-18.2.C** (webwork-opl:CA8.7) Find a volume of revolution for a parametric curve.
  - EK: V = ∫ π y² dx with dx = x′(t) dt.
  - P1 · drills: ca-parametric-volume
- ● **CA-18.2.D** (webwork-opl:CA8.8) Find a surface area of revolution for a parametric curve.
  - EK: S = ∫ 2π y √(x′² + y′²) dt.
  - P1 · drills: ca-parametric-surface
- ● **CA-18.2.E** (webwork-opl:CA9.7) Find the arc length of a polar curve.
  - EK: L = ∫ √(r² + (dr/dθ)²) dθ.
  - P1 · drills: ca-polar-arc-length
- ● **CA-18.2.F** (webwork-opl:MV2.2) Find the limit of a vector function.
  - EK: Take the limit of each component.
  - P1 · drills: ca-vector-limit

## Drills not yet placed on the map

- mm-coverup-two (calc.partial-fractions)
- mm-coverup-three (calc.partial-fractions)
- mm-coverup-repeated (calc.partial-fractions)
- mm-coverup-quadratic (calc.partial-fractions)
- mm-limit-at-infinity (calc.limits)
- mm-asymptote (calc.limits)
- mm-removable-limit (calc.limits)
- mm-horizontal-asymptote (calc.limits)
- mm-derivative-at-a-point (calc.derivative-rules)
- mm-tangent-slope (calc.derivative-rules)
- mm-product-derivative (calc.derivative-rules)
- mm-tangent-intercept (calc.derivative-rules)
- mm-diff-linear-power (calc.chain-rule)
- mm-diff-sin-inner (calc.chain-rule)
- mm-diff-log-inner (calc.chain-rule)
- mm-diff-power-exp (calc.chain-rule)
- mm-inverse-derivative (calc.chain-rule)
- mm-critical-value (calc.extrema)
- mm-quadratic-maximum (calc.extrema)
- mm-inflection (calc.extrema)
- mm-max-product (calc.extrema)
- mm-definite-integral (calc.riemann-ftc)
- mm-average-value (calc.riemann-ftc)
- mm-int-cos-kx (calc.antiderivatives)
- mm-int-sin-kx (calc.antiderivatives)
- mm-int-exp-kx (calc.antiderivatives)
- mm-int-linear-power (calc.antiderivatives)
- mm-int-reciprocal-linear (calc.antiderivatives)
- mm-int-log-form (calc.antiderivatives)
- mm-int-x-exp-square (calc.antiderivatives)
- mm-int-sin-power-cos (calc.antiderivatives)
