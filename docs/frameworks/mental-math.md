# Mental Math — curriculum framework (draft 1)

Generated from `drills/frameworks/mental-math.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**84 learning objectives** in 6 units (84 core): 84 drilled, 0 partly, 0 with no drills. Core: 84 / 84 drilled.

## Big ideas

- **SEE · See the structure before you compute.** Most mental calculation is noticing that the numbers in front of you are a special case of an identity (a difference of squares, a common factor, a number near a round one) and letting the identity do the work.
- **KNOW · A small set of facts, recalled at once.** Squares, cubes, powers of two, fraction-percent pairs and unit factors are worth knowing cold, because every short-cut bottoms out in one of them and a fact that takes five seconds to rebuild breaks the chain.
- **EST · An estimate is an answer.** A number good to a few percent, with the right order of magnitude, is often all a decision needs, and it is the check that catches a slipped decimal in an exact calculation.

## Practices

- **P1 · Compute in the head.** Hold intermediate results in working memory and say the answer most significant digit first.
- **P2 · Choose the short-cut.** Recognise which identity or known fact fits the numbers before starting.
- **P3 · Estimate and check.** Round deliberately, track the direction of the error, and test an exact answer against its size.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Arithmetic at speed (problems 1–20) | core | — | 24 | 24 | 0 | 0 |
| 2 · Algebra and number (problems 21–40) | core | — | 16 | 16 | 0 | 0 |
| 3 · Advanced algebra and geometry (problems 41–60) | core | — | 17 | 17 | 0 | 0 |
| 4 · Precalculus (problems 61–70) | core | — | 10 | 10 | 0 | 0 |
| 5 · Calculus (problems 71–80) | core | — | 10 | 10 | 0 | 0 |
| 6 · By inspection (beyond the chart) | core | — | 7 | 7 | 0 | 0 |

## Unit 1 · Arithmetic at speed (problems 1–20)

Big ideas: SEE, KNOW, EST

### 1.1 Operations on integers, fractions and decimals



- ● **MM-1.1.B** (H1.1) Take a fraction of a whole number by dividing first.
  - EK: p/q of n: divide by q, then multiply by p.
  - P1 · P2 · drills: mm-fraction-of, mm-whole-from-fraction
- ● **MM-1.1.A** (H1.1) Add and subtract multi-digit numbers left to right, and subtract from a power of ten by complements.
  - EK: Say the large part of the answer first; 1000 − n is nines-and-a-ten on the digits.
  - EK: Slide both numbers so the one taken away is round (541 − 229 = 542 − 230); count up when the two are close.
  - P1 · P2 · drills: mm-add-left-to-right, mm-subtract-from-1000, mm-sub-same-change, mm-sub-round-repay, mm-sub-count-up, mm-add-compensate, mm-money-subtract

### 1.2 Order of operations



- ● **MM-1.2.A** (H1.2) Evaluate a short expression with mixed operations in the right order.
  - EK: Products and quotients before sums and differences, then left to right.
  - P1 · P2 · drills: mm-order-of-operations, mm-order-power

### 1.3 Distributive property



- ● **MM-1.3.A** (H1.3) Spot a common factor and add before multiplying.
  - EK: ab + ac = a(b + c); look for sums that make 10, 50 or 100.
  - P1 · P2 · drills: mm-distributive, mm-distributive-subtract

### 1.4 Comparing fractions and decimals



- ● **MM-1.4.A** (H1.4) Compare two fractions by cross-multiplying.
  - EK: a/b > c/d exactly when ad > bc (positive denominators).
  - P1 · P2 · drills: mm-compare-fractions, mm-fraction-midpoint

### 1.5 Multiplication and division short-cuts



- ● **MM-1.5.A** (H1.5) Multiply by 11, 25, 5, 99 and 101 by rewriting the multiplier.
  - EK: 11 = 10 + 1; 25 = 100/4; 5 = 10/2; 99 = 100 − 1; 101 = 100 + 1.
  - P1 · P2 · drills: mm-times-11, mm-times-25, mm-times-5, mm-times-99-101
- ● **MM-1.5.B** (H1.5) Multiply two numbers just under 100 from their shortfalls.
  - EK: (100 − a)(100 − b) = 100(100 − a − b) + ab.
  - P1 · P2 · drills: mm-near-100, mm-above-100
- ● **MM-1.5.C** (H1.5) Multiply two-digit numbers that share a tens digit and whose ones digits sum to 10, or that sit evenly around a round number.
  - EK: (10t + u)(10t + 10 − u) = 100t(t + 1) + u(10 − u); (m − d)(m + d) = m² − d².
  - P1 · P2 · drills: mm-same-tens, mm-difference-of-squares
- ● **MM-1.5.D** (H1.5) Double one factor and halve the other to make a round number.
  - EK: ab = (a/2)(2b); a factor ending in 5 doubles to a multiple of 10.
  - P1 · P2 · drills: mm-double-and-halve, mm-times-25
- ● **MM-1.5.E** Divide by 5 and 25 by rewriting the divisor, and by a two-digit number in stages.
  - EK: ÷5 = ×2 ÷10; ÷25 = ×4 ÷100; ÷35 = ÷5 then ÷7. Multiply back to check.
  - P1 · P2 · drills: mm-div-5, mm-div-25, mm-div-stages
- ● **MM-1.5.F** Divide by a decimal by moving both decimal points until the divisor is whole.
  - EK: 12.6 ÷ 0.35 = 1260 ÷ 35: dollars ÷ dollars per minute becomes cents ÷ cents per minute.
  - Needs: MM-1.5.E
  - P1 · P2 · drills: mm-div-shift, mm-decimal-product

### 1.6 Squaring numbers



- ● **MM-1.6.A** (H1.6) Square a number ending in 5, or near 50 or 100, from its pattern.
  - EK: (10t + 5)² = 100t(t + 1) + 25; (50 ± d)² = 100(25 ± d) + d²; (100 ± d)² = 100(100 ± 2d) + d².
  - P1 · P2 · drills: mm-square-ending-5, mm-square-near-50, mm-square-near-100
- ● **MM-1.6.B** (H1.6) Square any two-digit number by sliding to a multiple of ten.
  - EK: n² = (n − d)(n + d) + d².
  - P1 · P2 · drills: mm-square-two-digit, mm-difference-of-squares

### 1.7 Conversions



- ● **MM-1.7.A** (H1.7) Recall the percent form of the common fractions, and use it to take a percent of a number.
  - EK: Eighths step by 12.5%; 1/6 = 16⅔%; 1/7 ≈ 14.3%; 1/9 ≈ 11.1%; 1/11 ≈ 9.09%; 1/12 = 8⅓%; 1/16 = 6.25%.
  - P1 · P2 · drills: mm-fraction-to-percent, mm-percent-as-fraction
- ● **MM-1.7.B** (H1.7) Convert between common units of length, capacity, weight and time, including square and cubic units.
  - EK: 12 in/ft, 3 ft/yd, 5280 ft/mi, 4 qt/gal, 2 pt/qt, 16 oz/lb; area factors are squared, volume factors cubed.
  - P1 · P2 · drills: mm-unit-conversion, mm-area-volume-units
- ● **MM-1.7.C** (H1.7) Read a Roman numeral.
  - EK: I V X L C D M = 1 5 10 50 100 500 1000; a smaller symbol before a larger one is subtracted.
  - P1 · P2 · drills: mm-roman-numerals, mm-roman-sum

### 1.8 GCD and LCM



- ● **MM-1.8.A** (H1.8) Find the GCD and LCM of two numbers under 100.
  - EK: The GCD divides the difference; LCM = product ÷ GCD.
  - P1 · P2 · drills: mm-gcd, mm-lcm

### 1.9 Percent problems



- ● **MM-1.9.A** (H1.9) Take a percent of a number by swapping or building from 10%, and apply a percent increase or decrease.
  - EK: a% of b = b% of a; a change of p% multiplies by 1 ± p/100.
  - P1 · P2 · drills: mm-percent-swap, mm-percent-change

### 1.10 Mean, median and mode



- ● **MM-1.10.A** (H1.10) Find a mean with a focus number and the median of a short unsorted list.
  - EK: Mean = guess + (sum of deviations)/n; the median survives striking extremes in pairs.
  - P1 · P2 · drills: mm-mean-focus, mm-median

### 1.11 Sums of integers



- ● **MM-1.11.A** (H1.11) Sum the first n integers, the first n odd numbers, or a short arithmetic series.
  - EK: 1 + … + n = n(n + 1)/2; 1 + 3 + … + (2n − 1) = n²; a series sums to (number of terms)(average of first and last).
  - P1 · P2 · drills: mm-sum-to-n, mm-sum-of-odds, mm-sum-arithmetic

### 1.12 Remainder problems



- ● **MM-1.12.A** (H1.12) Find a remainder on division by 3, 4, 9 or 11 from the digits.
  - EK: Mod 3 and 9: digit sum. Mod 4: last two digits. Mod 11: alternating digit sum from the right.
  - P1 · P2 · drills: mm-remainder-digits, mm-remainder-11

### 1.13 Consumer problems



- ● **MM-1.13.A** (H1.13) Find a sale price or similar everyday percent amount.
  - EK: Pay (100 − p)% of the price; build from 10%.
  - P1 · P2 · drills: mm-sale-price, mm-original-price

### 1.14 Number theory: primes and divisors



- ● **MM-1.14.A** (H1.14) Count the divisors of a number, and sum them, from its prime factorisation.
  - EK: d(n) = ∏(eᵢ + 1); σ is multiplicative, with σ(pᵏ) = 1 + p + … + pᵏ.
  - P1 · P2 · drills: mm-count-divisors, mm-sum-divisors

### 1.15 Starred problems: estimates



- ● **MM-1.15.A** (H1) Estimate a product, a quotient or a square root to within 5 percent.
  - EK: Round in opposite directions for a product and in the same direction for a quotient; √(a² + h) ≈ a + h/(2a).
  - P3 · drills: mm-estimate-product, mm-estimate-quotient, mm-estimate-root

## Unit 2 · Algebra and number (problems 21–40)

Big ideas: SEE, KNOW

### 2.1 Powers of numbers



- ● **MM-2.1.A** (H2.1) Recall the powers of 2 to 2¹² and the cubes to 12³.
  - EK: 2¹⁰ = 1024; 12³ = 1728.
  - P1 · P2 · drills: mm-powers-of-2, mm-cubes

### 2.2 Substitution



- ● **MM-2.2.A** (H2.2) Evaluate an expression at given values without writing it out.
  - EK: Substitute, then use the order of operations.
  - P1 · P2 · drills: mm-substitution, mm-two-variable-sub

### 2.3 Word problems



- ● **MM-2.3.A** (H2.3) Solve a one-step word problem (ages, rates, coins) mentally.
  - EK: Name the unknown and undo one operation.
  - P1 · P2 · drills: mm-sum-and-difference, mm-coin-count

### 2.4 Inverses



- ● **MM-2.4.A** (H2.4) Give the additive or multiplicative inverse of an integer, fraction or mixed number.
  - EK: Additive inverses sum to 0; multiplicative inverses multiply to 1.
  - P1 · P2 · drills: mm-reciprocal-mixed, mm-decimal-reciprocal

### 2.5 Absolute value



- ● **MM-2.5.A** (H2.5) Evaluate an expression with absolute values.
  - EK: |x| is the distance from 0.
  - P1 · P2 · drills: mm-absolute-value, mm-abs-combo

### 2.6 Ratio and proportion



- ● **MM-2.6.A** (H2.6) Solve a proportion by scaling or cross-multiplying.
  - EK: a/b = c/d means ad = bc.
  - P1 · P2 · drills: mm-proportion, mm-unit-rate

### 2.7 Square roots and cube roots



- ● **MM-2.7.A** (H2.7) Find the root of a perfect square or cube from its size and last digit.
  - EK: Bracket between squares of tens; the last digit narrows the ones digit.
  - P1 · P2 · drills: mm-perfect-square-root, mm-cube-root

### 2.8 Sets



- ● **MM-2.8.A** (H2.8) Count subsets, and elements of unions and intersections.
  - EK: A set of n elements has 2ⁿ subsets; |A ∪ B| = |A| + |B| − |A ∩ B|.
  - P1 · P2 · drills: mm-subsets, mm-proper-subsets

### 2.9 Base conversions



- ● **MM-2.9.A** (H2.9) Convert a short numeral from another base to base 10.
  - EK: Multiply by the base and add the next digit, left to right.
  - P1 · P2 · drills: mm-base-to-ten, mm-ten-to-base5

### 2.10 Simple equations



- ● **MM-2.10.A** (H2.10) Solve a one- or two-step linear equation mentally.
  - EK: Undo operations in reverse order.
  - P1 · P2 · drills: mm-linear-equation, mm-both-sides

### 2.11 Systems of equations



- ● **MM-2.11.A** (H2.11) Find x + y or x − y from a 2 × 2 system by adding or subtracting the equations.
  - EK: Often the combination asked for falls out without solving for each variable.
  - P1 · P2 · drills: mm-system-sum, mm-system-x

### 2.12 Repeating decimals to fractions



- ● **MM-2.12.A** (H2.12) Write a repeating decimal as a fraction.
  - EK: A repeating block of k digits sits over k nines.
  - P1 · P2 · drills: mm-repeating-decimal, mm-mixed-repeating

### 2.13 More remainder problems



- ● **MM-2.13.A** (H2.13) Find the remainder of a sum or product from the remainders of its parts.
  - EK: Remainders add and multiply (mod m).
  - P1 · P2 · drills: mm-remainder-product, mm-remainder-sum

### 2.14 Perimeter and area of polygons and circles



- ● **MM-2.14.A** (H2.14) Find the perimeter or area of a rectangle, triangle, trapezoid or circle from its dimensions.
  - EK: A = bh, ½bh, ½(b₁ + b₂)h, πr².
  - P1 · P2 · drills: mm-area, mm-area-trapezoid

### 2.15 Sequences



- ● **MM-2.15.A** (H2.15) Find the next or the n-th term of an arithmetic or geometric sequence.
  - EK: aₙ = a₁ + (n − 1)d; aₙ = a₁rⁿ⁻¹.
  - P1 · P2 · drills: mm-nth-term, mm-arithmetic-sum

### 2.16 Quadratic and cubic equations



- ● **MM-2.16.A** (H2.16) Give the sum or product of the roots of a quadratic or cubic from its coefficients.
  - EK: For ax² + bx + c: sum −b/a, product c/a.
  - P1 · P2 · drills: mm-vieta, mm-other-root

## Unit 3 · Advanced algebra and geometry (problems 41–60)

Big ideas: SEE, KNOW

### 3.1 Laws of exponents



- ● **MM-3.1.A** (H3.1) Simplify a product or quotient of powers by moving to a common base.
  - EK: aᵐaⁿ = aᵐ⁺ⁿ; (aᵐ)ⁿ = aᵐⁿ; 4 = 2², 8 = 2³.
  - P1 · P2 · drills: mm-exponent-laws, mm-exponent-solve

### 3.2 Right triangles



- ● **MM-3.2.A** (H3.2) Complete a Pythagorean triple or a 30-60-90 or 45-45-90 triangle.
  - EK: 3-4-5, 5-12-13, 8-15-17, 7-24-25 and their multiples.
  - P1 · P2 · drills: mm-pythagorean-triple, mm-right-triangle-area

### 3.3 Coordinate geometry



- ● **MM-3.3.A** (H3.3) Find a slope, midpoint, distance or intercept from two points or an equation.
  - EK: m = Δy/Δx; midpoint averages the coordinates.
  - P1 · P2 · drills: mm-slope, mm-intercept-two-points

### 3.4 Regular polygons



- ● **MM-3.4.A** (H3.4) Find an interior or exterior angle, or the number of diagonals, of a regular polygon.
  - EK: Exterior angle 360°/n; diagonals n(n − 3)/2.
  - P1 · P2 · drills: mm-regular-polygon, mm-sides-from-angle

### 3.5 Inequalities



- ● **MM-3.5.A** (H3.5) Solve a linear inequality or count its integer solutions.
  - EK: Multiplying by a negative reverses the inequality.
  - P1 · P2 · drills: mm-inequality-count, mm-abs-inequality-count

### 3.6 Applications of geometry theorems



- ● **MM-3.6.A** (H3.6) Use an angle, chord, tangent or similarity fact to find a length or angle.
  - EK: Inscribed angle = half the arc; similar figures scale areas by k².
  - P1 · P2 · drills: mm-circle-angles, mm-chord-segments

### 3.7 Direct and inverse variation



- ● **MM-3.7.A** (H3.7) Find a value from a direct or inverse variation.
  - EK: y = kx or y = k/x; find k first, or scale.
  - P1 · P2 · drills: mm-variation, mm-inverse-square

### 3.8 Sequences and series, finite and infinite



- ● **MM-3.8.A** (H3.8) Sum an infinite geometric series.
  - EK: S = a/(1 − r) for |r| < 1.
  - P1 · P2 · drills: mm-geometric-sum, mm-ratio-from-sum

### 3.9 Complex numbers



- ● **MM-3.9.A** (H3.9) Multiply two complex numbers or find a modulus or a power of i.
  - EK: i² = −1; |a + bi|² = a² + b².
  - P1 · P2 · drills: mm-complex-product, mm-product-modulus

### 3.10 Logarithms and logarithmic equations



- ● **MM-3.10.A** (H3.10) Evaluate a logarithm of an exact power.
  - EK: log_b(bᵏ) = k.
  - P1 · P2 · drills: mm-log-exact, mm-log-fraction

### 3.11 Factorials, permutations and combinations



- ● **MM-3.11.A** (H3.11) Evaluate a small combination, permutation or factorial ratio.
  - EK: C(n, r) = n(n − 1)…(n − r + 1)/r!.
  - P1 · P2 · drills: mm-combinations, mm-permutations

### 3.12 Probability and odds



- ● **MM-3.12.A** (H3.12) Give the probability or odds of a simple event with dice, coins or cards.
  - EK: Odds in favour = successes : failures.
  - P1 · P2 · drills: mm-two-dice, mm-dice-sum-prob

### 3.13 Conics



- ● **MM-3.13.A** (H3.13) Read a centre, vertex, focus or axis length from a conic in standard form.
  - EK: Circle (x − h)² + (y − k)² = r²; ellipse axes 2a and 2b.
  - P1 · P2 · drills: mm-circle-radius, mm-radius-general-form

### 3.14 Binomial theorem



- ● **MM-3.14.A** (H3.14) Give a coefficient or the sum of coefficients of a binomial expansion.
  - EK: Coefficients are C(n, k); their sum is the expansion at x = y = 1.
  - P1 · P2 · drills: mm-binomial-coefficient, mm-coefficient-2x

### 3.15 Operations in other bases



- ● **MM-3.15.A** (H3.15) Add, subtract or multiply two short numerals in another base.
  - EK: Carry at the base instead of at ten.
  - P1 · P2 · drills: mm-base-addition, mm-largest-base-numeral

### 3.16 Roots of equations



- ● **MM-3.16.A** (H3.16) Use Vieta's relations to find symmetric expressions in the roots.
  - EK: r₁² + r₂² = (r₁ + r₂)² − 2r₁r₂.
  - P1 · P2 · drills: mm-sum-of-squares-of-roots, mm-reciprocal-roots

### 3.17 Polygonal numbers



- ● **MM-3.17.A** (H3.17) Find the n-th triangular, pentagonal or hexagonal number.
  - EK: Triangular n(n + 1)/2; pentagonal n(3n − 1)/2; hexagonal n(2n − 1).
  - P1 · P2 · drills: mm-polygonal-number, mm-triangular-index

## Unit 4 · Precalculus (problems 61–70)

Big ideas: SEE, KNOW

### 4.1 Volume and surface area



- ● **MM-4.1.A** (H4.1) Find the volume or surface area of a prism, cylinder, cone or sphere, in terms of π where needed.
  - EK: V = πr²h, ⅓πr²h, ⁴⁄₃πr³; sphere area 4πr².
  - P1 · P2 · drills: mm-volume-in-pi, mm-sphere-in-pi

### 4.2 Greatest integer



- ● **MM-4.2.A** (H4.2) Evaluate a floor expression, including of negative numbers.
  - EK: ⌊x⌋ is the greatest integer not above x; ⌊−2.3⌋ = −3.
  - P1 · P2 · drills: mm-floor, mm-ceiling-negative

### 4.3 Remainder theorem



- ● **MM-4.3.A** (H4.3) Find the remainder of a polynomial on division by x − a.
  - EK: The remainder is p(a).
  - P1 · P2 · drills: mm-remainder-theorem, mm-factor-k

### 4.4 Trigonometry



- ● **MM-4.4.A** (H4.4) Recall exact trig values at the special angles and use basic identities.
  - EK: sin and cos of 0°, 30°, 45°, 60°, 90° and their reflections; sin² + cos² = 1.
  - P1 · P2 · drills: mm-trig-exact, mm-cos-from-sin

### 4.5 Determinants



- ● **MM-4.5.A** (H4.5) Evaluate a 2 × 2 or simple 3 × 3 determinant.
  - EK: ad − bc.
  - P1 · P2 · drills: mm-determinant, mm-det-zero-x

### 4.6 Matrices



- ● **MM-4.6.A** (H4.6) Find an entry of a matrix sum, product or inverse.
  - EK: Row times column.
  - P1 · P2 · drills: mm-matrix-entry, mm-inverse-entry

### 4.7 Vectors



- ● **MM-4.7.A** (H4.7) Find a dot product or a magnitude.
  - EK: u·v = u₁v₁ + u₂v₂.
  - P1 · P2 · drills: mm-dot-product, mm-3d-magnitude

### 4.8 Composite functions



- ● **MM-4.8.A** (H4.8) Evaluate f(g(a)) for simple f and g.
  - EK: Work from the inside out.
  - P1 · P2 · drills: mm-composite, mm-composite-reverse

### 4.9 Bases with decimals or fractions



- ● **MM-4.9.A** (H4.9) Convert a fraction to or from a numeral with digits after the point in another base.
  - EK: Places after the point are negative powers of the base.
  - P1 · P2 · drills: mm-base-fraction, mm-base-point-value

### 4.10 Polar and rectangular coordinates



- ● **MM-4.10.A** (H4.10) Convert a point between polar and rectangular form at a special angle.
  - EK: x = r cos θ, y = r sin θ.
  - P1 · P2 · drills: mm-polar-to-rectangular, mm-rect-to-r

## Unit 5 · Calculus (problems 71–80)

Big ideas: SEE

### 5.1 Function domains and ranges



- ● **MM-5.1.A** (H5.1) State the excluded value or the range of a simple rational, radical or quadratic function.
  - EK: Denominator ≠ 0; radicand ≥ 0; a quadratic's range starts or ends at its vertex.
  - P1 · P2 · drills: mm-domain-excluded, mm-range-minimum

### 5.2 Modular arithmetic



- ● **MM-5.2.A** (H5.2) Evaluate a sum, product or power modulo m.
  - EK: Reduce before multiplying; powers cycle.
  - P1 · P2 · drills: mm-modular-power, mm-last-digit-power

### 5.3 Limits



- ● **MM-5.3.A** (H5.3) Evaluate a limit of a rational function at a point or at infinity by inspection.
  - EK: At infinity compare leading terms; at a 0/0 point cancel the common factor.
  - P1 · P2 · drills: mm-limit-at-infinity, mm-removable-limit

### 5.4 Derivatives



- ● **MM-5.4.A** (H5.4) Evaluate the derivative of a polynomial or basic function at a point.
  - EK: Power rule term by term.
  - P1 · P2 · drills: mm-derivative-at-a-point, mm-product-derivative

### 5.5 Slopes of tangent lines



- ● **MM-5.5.A** (H5.5) Give the slope of the tangent to a curve at a point.
  - EK: It is f′ at that x.
  - P1 · P2 · drills: mm-tangent-slope, mm-tangent-intercept

### 5.6 Horizontal and vertical asymptotes



- ● **MM-5.6.A** (H5.6) Read the asymptotes of a rational function from its formula.
  - EK: Vertical where the reduced denominator is 0; horizontal from the leading terms.
  - P1 · P2 · drills: mm-asymptote, mm-horizontal-asymptote

### 5.7 Critical values



- ● **MM-5.7.A** (H5.7) Find where a polynomial's derivative is zero.
  - EK: Set f′ = 0 and factor.
  - P1 · P2 · drills: mm-critical-value, mm-inflection

### 5.8 Maximum and minimum problems



- ● **MM-5.8.A** (H5.8) Find the maximum or minimum value of a quadratic or a simple cubic on an interval.
  - EK: A quadratic's extreme is at x = −b/(2a).
  - P1 · P2 · drills: mm-quadratic-maximum, mm-max-product

### 5.9 Definite integration



- ● **MM-5.9.A** (H5.9) Evaluate a definite integral of a polynomial with easy limits.
  - EK: Antidifferentiate term by term; use symmetry for odd and even integrands.
  - P1 · P2 · drills: mm-definite-integral, mm-average-value

### 5.10 Inverse functions



- ● **MM-5.10.A** (H5.10) Evaluate f⁻¹(a) for a linear or simple rational f without finding the inverse formula.
  - EK: Solve f(x) = a.
  - P1 · P2 · drills: mm-inverse-function-value, mm-inverse-derivative

## Unit 6 · By inspection (beyond the chart)

Big ideas: SEE

### 6.1 Heaviside cover-up



- ● **MM-6.1.A** (mit-18-03-coverup:distinct) Read off one coefficient of a partial-fraction decomposition with distinct linear factors by covering up.
  - EK: Cover the factor, substitute its root into what is left.
  - P1 · P2 · drills: mm-coverup-two, mm-coverup-three
- ● **MM-6.1.B** (mit-18-03-coverup:repeated, mit-18-03-coverup:quadratic) Use cover-up where it still works: the top power of a repeated factor, and a linear factor beside an irreducible quadratic.
  - EK: Cover-up gives the highest-power coefficient only; the rest need one more step.
  - P1 · P2 · drills: mm-coverup-repeated, mm-coverup-quadratic

### 6.2 Integrals by inspection



- ● **MM-6.2.A** (mit-integration-bee:pace) Integrate a basic function of a linear inside (cos kx, sin kx, e^kx, (kx + b)^n, 1/(kx + b)) by guessing the shape and fixing the constant.
  - EK: Differentiate the guess in your head; divide by whatever constant it throws out.
  - P1 · P2 · drills: mm-int-cos-kx, mm-int-sin-kx, mm-int-exp-kx, mm-int-linear-power, mm-int-reciprocal-linear
- ● **MM-6.2.B** (mit-integration-bee:pace) Spot an integrand of the form f(g(x))·g′(x) up to a constant and write its antiderivative.
  - EK: f′/f integrates to ln f; u^n du to u^(n+1)/(n+1); x·e^(kx²) to an exponential.
  - P1 · P2 · drills: mm-int-log-form, mm-int-x-exp-square, mm-int-sin-power-cos

### 6.3 Derivatives in one line



- ● **MM-6.3.A** Write the derivative of a one-layer composite or a power-times-exponential product without intermediate steps.
  - EK: Outside derivative with the inside untouched, times the inside derivative.
  - P1 · P2 · drills: mm-diff-linear-power, mm-diff-sin-inner, mm-diff-log-inner, mm-diff-power-exp

### 6.4 Matrices and ODEs on sight



- ● **MM-6.4.A** Find the eigenvalues of a 2 × 2 matrix from its trace and determinant.
  - EK: Sum = trace, product = determinant.
  - P1 · P2 · drills: mm-eigen-trace-det, mm-trace-of-square
- ● **MM-6.4.B** Classify y″ + by′ + cy = 0 by comparing b² with 4c, and choose the trial form for an exponential forcing term.
  - EK: b² > 4c overdamped, = critical, < underdamped; multiply the trial by x once per time the exponent is a characteristic root.
  - P1 · P2 · drills: mm-damping-class, mm-particular-form
