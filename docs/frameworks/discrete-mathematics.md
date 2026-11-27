# Discrete Mathematics — curriculum framework (draft 1)

Generated from `drills/frameworks/discrete-mathematics.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**28 learning objectives** in 6 units (28 core): 28 drilled, 0 partly, 0 with no drills. Core: 28 / 28 drilled.

## Big ideas

- **PROOF · A statement is exactly as strong as its quantifiers.** Negating, reversing or weakening a statement changes what has to be shown. Most wrong proofs prove a different statement.
- **COUNT · Count by structure, not by listing.** Every count is a product, a sum, a quotient by symmetry or a complement. The work is choosing which.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Logic and proof | core | — | 9 | 9 | 0 | 0 |
| 2 · Induction and recursion | core | — | 2 | 2 | 0 | 0 |
| 3 · Sets, functions and relations | core | — | 4 | 4 | 0 | 0 |
| 4 · Counting | core | — | 5 | 5 | 0 | 0 |
| 5 · Generating functions | core | — | 2 | 2 | 0 | 0 |
| 6 · Graphs and trees | core | — | 6 | 6 | 0 | 0 |

## Unit 1 · Logic and proof

Big ideas: PROOF

### 1.1 Statements



- ● **DM-1.1.C** (cupm-2015-discrete:D1) Choose a method of proof and state what it assumes and what it must reach.
  - EK: Direct: assume p, reach q. Contrapositive: assume not q, reach not p. Contradiction: assume p and not q, reach an impossibility. Induction: base case plus the step from k to k + 1.
  - Needs: DM-1.2.C
  - P2 · drills: dm-proof-first-line, dm-proof-flaw
- ● **DM-1.1.A** (cupm-2015-discrete:D1) Evaluate a compound proposition and count the cases in which it is true.
  - EK: A proposition in n variables has 2^n rows. p → q is false only when p is true and q is false; it is equivalent to (not p) or q.
  - P1 · drills: dm-truth-rows, dm-equivalent-forms
- ● **DM-1.1.B** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) Negate a quantified statement and say what a counterexample must be.
  - EK: Negation swaps 'for all' and 'there exists' and negates the inside. A universal claim falls to one counterexample; an existential claim needs one witness.
  - Needs: DM-1.1.A
  - P2 · drills: dm-negate-quantifiers, dm-counterexample

### 1.2 From computing to proving



- ● **DM-1.2.A** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) Apply a definition exactly as written to decide whether an object qualifies.
  - EK: A definition is a test. n is even if n = 2k for some integer k; a divides b if b = ak for some integer k; a number is rational if it is a quotient of integers with non-zero denominator. Edge cases (0, 1, negatives) are settled by the wording, not by intuition.
  - Needs: DM-1.1.A
  - P2 · drills: dm-definition-applies, dm-definition-wording
- ● **DM-1.2.B** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) Carry out the algebra a direct proof turns on.
  - EK: A direct proof unpacks the hypothesis with the definition, computes, and repacks the result in the form the conclusion's definition demands: to show a product is odd, exhibit it as 2(something) + 1.
  - Needs: DM-1.2.A
  - P2 · drills: dm-odd-product-witness, dm-direct-proof-steps
- ● **DM-1.2.C** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) State the contrapositive of a claim and recognise the contradiction a proof reaches.
  - EK: The contrapositive of 'if P then Q' is 'if not Q then not P' and is equivalent to it. A proof by contradiction assumes P and not Q together and derives something impossible.
  - Needs: DM-1.2.B, DM-1.1.B
  - P2 · drills: dm-contrapositive-of, dm-contradiction-reached
- ● **DM-1.2.D** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) Split a claim into cases and check them all.
  - EK: A proof by cases must cover every possibility. Working modulo m reduces a claim about all integers to m cases: squares are 0 or 1 modulo 4, and 0, 1 or 4 modulo 8.
  - Needs: DM-1.2.B
  - P2 · drills: dm-square-residues, dm-cases-facts
- ● **DM-1.2.E** (cupm-2015-discrete:D1, cambridge-ia-numbers-sets:N1) Prove existence with a witness and say what uniqueness requires.
  - EK: An existence claim needs one example. Uniqueness needs an argument that any two objects with the property are equal. 'There is exactly one' needs both.
  - Needs: DM-1.2.B, DM-1.1.B
  - P2 · drills: dm-witness, dm-uniqueness-facts
- ● **DM-1.2.F** (cupm-2015-discrete:D2, cambridge-ia-numbers-sets:N3) Lay out an induction: base cases, hypothesis and step, including strong induction.
  - EK: Ordinary induction proves P(1) and that P(k) implies P(k + 1). Strong induction may use every earlier case, and needs as many base cases as the step reaches back.
  - Needs: DM-1.1.C
  - P2 · drills: dm-stamps-threshold, dm-induction-anatomy

## Unit 2 · Induction and recursion

Big ideas: PROOF, COUNT

### 2.1 Induction and recurrences



- ● **DM-2.1.A** (cupm-2015-discrete:D2, cambridge-ia-numbers-sets:N3) Use a closed form established by induction and identify the inductive step.
  - EK: 1 + 2 + … + n = n(n + 1)/2; the first n odd numbers sum to n²; 1² + … + n² = n(n + 1)(2n + 1)/6. The step adds the (k + 1)th term to the assumed formula for k.
  - Needs: DM-1.2.F
  - P1 · drills: dm-sum-squares, dm-induction-step-term
- ● **DM-2.1.B** (cupm-2015-discrete:D2, cupm-2015-discrete:C5) Iterate a linear recurrence and solve it from its characteristic roots.
  - EK: f(n) = a f(n−1) + b f(n−2) has solutions rⁿ for the roots of r² = ar + b; distinct roots give f(n) = A r₁ⁿ + B r₂ⁿ with A and B fixed by the first two values.
  - Needs: DM-2.1.A
  - P1 · drills: dm-recurrence-iterate, dm-recurrence-closed

## Unit 3 · Sets, functions and relations

Big ideas: COUNT

### 3.1 Sets and functions



- ● **DM-3.1.A** (cupm-2015-discrete:D3, cambridge-ia-numbers-sets:N2) Count unions, power sets and Cartesian products of finite sets.
  - EK: |A ∪ B| = |A| + |B| − |A ∩ B|; a set with n elements has 2^n subsets; |A × B| = |A||B|.
  - Needs: DM-1.2.A
  - P1 · drills: dm-union-size, dm-subsets-with-element
- ● **DM-3.1.B** (cupm-2015-discrete:D3, cambridge-ia-numbers-sets:N2) Count functions, injections and surjections between finite sets.
  - EK: From an n-set to a k-set there are k^n functions, k(k−1)…(k−n+1) injections, and the surjections are counted by inclusion-exclusion: Σ (−1)^j C(k, j)(k − j)^n.
  - Needs: DM-3.1.A
  - P1 · drills: dm-injections, dm-surjections
- ● **DM-3.1.D** (cupm-2015-discrete:D3, cambridge-ia-numbers-sets:N6) Decide whether a set is countable and say what Cantor's diagonal argument shows.
  - EK: A set is countable if it can be listed. The integers, the rationals and any countable union of countable sets are countable; the reals and the power set of the naturals are not, and no set maps onto its own power set.
  - Needs: DM-3.1.B, DM-1.2.C
  - P2 · drills: dm-countable-or-not, dm-cantor-facts
- ● **DM-3.1.C** (cupm-2015-discrete:D3, cambridge-ia-numbers-sets:N2) Test a relation for reflexivity, symmetry and transitivity, and count equivalence relations.
  - EK: An equivalence relation is reflexive, symmetric and transitive and is the same thing as a partition into classes; a 3-set has 5 and a 4-set has 15.
  - Needs: DM-3.1.A, DM-1.2.A
  - P2 · drills: dm-relation-properties, dm-count-equivalence

## Unit 4 · Counting

Big ideas: COUNT

### 4.1 Arrangements and selections



- ● **DM-4.1.A** (cupm-2015-discrete:C1, cupm-2015-discrete:C2) Count arrangements with repeated letters and selections under a constraint.
  - EK: n objects with repeats of sizes a, b, … have n!/(a! b! …) arrangements. 'At least one' is counted through the complement.
  - Needs: DM-3.1.A
  - P1 · drills: dm-word-arrangements, dm-committee-at-least
- ● **DM-4.1.B** (cupm-2015-discrete:C2) Count distributions of identical objects by stars and bars.
  - EK: x₁ + … + x_k = n has C(n + k − 1, k − 1) solutions in non-negative integers and C(n − 1, k − 1) in positive integers.
  - Needs: DM-4.1.A
  - P1 · drills: dm-stars-bars, dm-stars-bars-positive
- ● **DM-4.1.C** (cupm-2015-discrete:D4, cupm-2015-discrete:C2, cambridge-ia-numbers-sets:N3) Use the binomial theorem to read off a coefficient or a sum.
  - EK: (a + b)^n = Σ C(n, k) a^k b^(n−k). Setting a = b = 1 gives Σ C(n, k) = 2^n; a = −1 gives the alternating sum 0.
  - Needs: DM-4.1.A, DM-2.1.A
  - P1 · drills: dm-binomial-coefficient, dm-even-subsets
- ● **DM-4.1.D** (cupm-2015-discrete:C4, cambridge-ia-numbers-sets:N2) Count with inclusion-exclusion, including derangements.
  - EK: |A ∪ B ∪ C| = Σ|A| − Σ|A ∩ B| + |A ∩ B ∩ C|. Derangements: n! Σ (−1)^k / k!, close to n!/e.
  - Needs: DM-4.1.A, DM-3.1.A
  - P1 · drills: dm-divisible-by-any, dm-derangements
- ● **DM-4.1.E** (cupm-2015-discrete:D4) Apply the pigeonhole principle to find a guaranteed minimum.
  - EK: If more than kn objects go into n boxes, some box holds more than k. To force k + 1 in one box you need kn + 1 objects.
  - Needs: DM-4.1.A, DM-1.2.D
  - P1 · drills: dm-pigeonhole-force, dm-pigeonhole-facts

## Unit 5 · Generating functions

Big ideas: COUNT

### 5.1 Coefficients that count



- ● **DM-5.1.A** (cupm-2015-discrete:C3) Extract a coefficient from a product of geometric series.
  - EK: 1/(1 − x)^k = Σ C(n + k − 1, k − 1) x^n: the coefficient of x^n counts selections of n objects from k types with repetition.
  - Needs: DM-4.1.B, DM-4.1.C
  - P1 · drills: dm-gf-coefficient, dm-gf-bounded
- ● **DM-5.1.B** (cupm-2015-discrete:C3, cupm-2015-discrete:C5) Model a selection problem with a generating function and read off the count.
  - EK: A coin of value c contributes the factor 1/(1 − x^c); the number of ways to make n is the coefficient of x^n in the product.
  - Needs: DM-5.1.A, DM-2.1.B
  - P1 · drills: dm-gf-change, dm-gf-model

## Unit 6 · Graphs and trees

Big ideas: COUNT, PROOF

### 6.1 Degrees, trees and circuits



- ● **DM-6.1.A** (cupm-2015-discrete:D5, cupm-2015-discrete:GT1, cambridge-ii-graph-theory:H1) Use the handshake lemma on a degree sequence.
  - EK: The degrees sum to twice the number of edges, so the number of odd-degree vertices is even.
  - Needs: DM-4.1.A
  - P1 · drills: dm-handshake-edges, dm-degree-sequence-possible
- ● **DM-6.1.B** (cupm-2015-discrete:GT2, cambridge-ii-graph-theory:H1) Count the edges of a tree or forest and the spanning trees of a small graph.
  - EK: A tree on n vertices has n − 1 edges; a forest with c components has n − c. A cycle C_n has n spanning trees and the complete graph K_n has n^(n−2).
  - Needs: DM-6.1.A, DM-2.1.A
  - P1 · drills: dm-forest-edges, dm-spanning-trees
- ● **DM-6.1.C** (cupm-2015-discrete:GT4, cambridge-ii-graph-theory:H1) Decide whether a graph has an Euler circuit or trail from its degrees.
  - EK: A connected graph has an Euler circuit exactly when every degree is even, and an Euler trail exactly when two vertices have odd degree.
  - Needs: DM-6.1.A
  - P2 · drills: dm-odd-vertices, dm-euler-classify
- ● **DM-6.1.F** (cupm-2015-discrete:GT4, cambridge-ii-graph-theory:H2, cambridge-ii-graph-theory:H3, cambridge-ii-graph-theory:H6) Recognise Hamilton cycles, matchings and the first Ramsey number.
  - EK: A Hamilton cycle visits every vertex once; Dirac: minimum degree at least n/2 guarantees one. Hall: a bipartite graph has a matching covering X exactly when every set S in X has at least |S| neighbours. R(3, 3) = 6.
  - Needs: DM-6.1.C, DM-4.1.E
  - P2 · drills: dm-hamilton-or-not, dm-hall-ramsey-facts
- ● **DM-6.1.D** (cupm-2015-discrete:GT3, cambridge-ii-graph-theory:H5) Find a chromatic number and count proper colourings.
  - EK: χ(G) is the fewest colours with adjacent vertices different. A tree on n vertices has k(k − 1)^(n−1) colourings; the cycle C_n has (k − 1)^n + (−1)^n (k − 1); an odd cycle needs 3 colours.
  - Needs: DM-6.1.B
  - P1 · drills: dm-chromatic-number, dm-count-colourings
- ● **DM-6.1.E** (cupm-2015-discrete:GT1, cambridge-ii-graph-theory:H1) Apply Euler's formula and the edge bound for planar graphs.
  - EK: A connected plane graph has V − E + F = 2. A simple planar graph with V ≥ 3 has E ≤ 3V − 6, and E ≤ 2V − 4 if it has no triangles; so K₅ and K₃,₃ are not planar.
  - Needs: DM-6.1.B
  - P1 · drills: dm-euler-faces, dm-planarity-facts
