# Linear Algebra — curriculum framework (draft 2)

Generated from `drills/frameworks/linear-algebra.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**54 learning objectives** in 9 units (54 core): 54 drilled, 0 partly, 0 with no drills. Core: 54 / 54 drilled.

## Big ideas

- **MAIN · A matrix is a linear map.** Every question (solvable or not, invertible or not, which directions are only stretched) is a question about what the map does to space.

## Practices

- **P1 · Compute and interpret.** Carry a calculation to a number or a vector and say what it means for the system or the map.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Linear systems and independence | core | — | 6 | 6 | 0 | 0 |
| 2 · Matrix algebra | core | — | 7 | 7 | 0 | 0 |
| 3 · Determinants | core | — | 4 | 4 | 0 | 0 |
| 4 · Rank and the null space | core | — | 5 | 5 | 0 | 0 |
| 5 · Eigenvalues and eigenvectors | core | — | 5 | 5 | 0 | 0 |
| 6 · Orthogonality and least squares | core | — | 5 | 5 | 0 | 0 |
| 7 · Symmetric matrices and singular values | core | — | 5 | 5 | 0 | 0 |
| 8 · Linear transformations | core | — | 5 | 5 | 0 | 0 |
| 9 · Abstract vector spaces and special matrices | core | — | 12 | 12 | 0 | 0 |

## Unit 1 · Linear systems and independence

Big ideas: MAIN

### 1.1 Row reduction



- ● **LA-1.1.A** (lay-5e:1, webwork-opl:LA1.1, webwork-opl:LA1.2, webwork-opl:LA2.2) Solve a linear system by row reduction.
  - EK: Pivots give the basic variables; a row 0 = c means no solution.
  - P1 · drills: la-system, la-is-solution
- ● **LA-1.1.B** (lay-5e:1, webwork-opl:LA4.4) Decide whether a set of vectors is linearly independent.
  - EK: Independent exactly when the only solution of Ax = 0 is zero.
  - P1 · drills: la-independence, la-independence-parameter
- ● **LA-1.1.C** (cupm-2015-la:1, webwork-opl:LA1.6, webwork-opl:LA2.3) Read the number of solutions off an echelon form.
  - EK: A pivot in every variable column: one; a free variable: infinitely many; a row 0 = c: none.
  - P1 · drills: la-solution-type, la-inconsistent-h
- ● **LA-1.1.D** (cupm-2015-la:1, webwork-opl:LA1.3) Count the free variables of a consistent system.
  - EK: Free variables are the non-pivot columns.
  - P1 · drills: la-free-variables, la-min-free-vars

### 1.2 Vector equations and span



- ● **LA-1.2.A** (cupm-2015-la:1, lay-5e:1, webwork-opl:LA1.5, webwork-opl:LA4.2, webwork-opl:LA4.3) Decide whether a vector is in the span of others.
  - EK: b is in the span exactly when [v1 … vk | b] has no pivot in the last column.
  - P1 · drills: la-span-membership, la-span-h
- ● **LA-1.2.B** (cupm-2015-la:1, lay-5e:1) Describe the solution set of Ax = b as a shifted null space.
  - EK: Every solution is a particular solution plus a solution of Ax = 0.
  - P1 · drills: la-solution-set-shape, la-solution-set-dim

## Unit 2 · Matrix algebra

Big ideas: MAIN

### 2.1 Inverses



- ● **LA-2.1.A** (lay-5e:2, webwork-opl:LA2.6) Find the inverse of a 2 × 2 matrix.
  - EK: Swap the diagonal, negate the off-diagonal, divide by the determinant.
  - P1 · drills: la-inverse, la-inverse-check
- ● **LA-2.1.B** (cupm-2015-la:1, webwork-opl:LA1.4) Solve Ax = b with a known inverse.
  - EK: x = A⁻¹b; row i of A⁻¹ dotted with b gives x_i.
  - P1 · drills: la-solve-with-inverse, la-transpose-inverse
- ● **LA-2.1.C** (cupm-2015-la:1, lay-5e:2, webwork-opl:LA2.6) Use the invertible matrix theorem.
  - EK: For a square matrix, invertible, n pivots, independent columns, det ≠ 0 and 0 not an eigenvalue stand or fall together.
  - P1 · drills: la-invertible-matrix-theorem, la-imt-consequence

### 2.2 Matrix operations



- ● **LA-2.2.A** (cupm-2015-la:1, lay-5e:2, webwork-opl:LA2.1) Compute one entry of a product without computing the rest.
  - EK: (AB)_ij is row i of A dotted with column j of B.
  - P1 · drills: la-product-entry, la-square-entry
- ● **LA-2.2.B** (cupm-2015-la:1, lay-5e:2, webwork-opl:LA2.1, webwork-opl:LA2.5) Track sizes through products and transposes.
  - EK: (AB)ᵀ = BᵀAᵀ; an m × n times an n × p is m × p.
  - P1 · drills: la-product-size, la-multiplication-count

### 2.3 LU factorisation



- ● **LA-2.3.A** (cupm-2015-la:1, lay-5e:2, webwork-opl:LA3.2) Factor a matrix as LU.
  - EK: The multipliers of row reduction go below the diagonal of L; U is the echelon form.
  - P1 · drills: la-lu-pivot, la-det-from-lu
- ● **LA-2.3.B** (cupm-2015-la:1, lay-5e:2, webwork-opl:LA3.2) Solve with LU by forward and back substitution.
  - EK: Ly = b, then Ux = y.
  - P1 · drills: la-lu-forward, la-forward-step

## Unit 3 · Determinants

Big ideas: MAIN

### 3.1 Cofactor expansion



- ● **LA-3.1.A** (lay-5e:3, webwork-opl:LA10.1) Compute a 3 × 3 determinant.
  - EK: Expand along the row or column with the most zeros.
  - P1 · drills: la-det, mm-determinant, la-det-triangular

### 3.2 Properties of determinants



- ● **LA-3.2.A** (cupm-2015-la:2, lay-5e:3, webwork-opl:LA10.2) Use det(AB) = det A det B, det Aᵀ = det A and det(kA) = kⁿ det A.
  - EK: A scalar multiplies every row, so it comes out to the nth power.
  - P1 · drills: la-det-properties, la-det-combo
- ● **LA-3.2.B** (cupm-2015-la:2, lay-5e:3, webwork-opl:LA2.2, webwork-opl:LA10.2) Track the determinant through row operations.
  - EK: Swap: sign flips; scale a row: scales; add a multiple of a row: no change.
  - P1 · drills: la-det-row-ops, la-det-before-ops
- ● **LA-3.2.C** (cupm-2015-la:2, lay-5e:3, webwork-opl:LA10.3) Read |det A| as the factor by which A scales area or volume.
  - EK: Area of the image = |det A| × area.
  - P1 · drills: la-det-area, la-triangle-area-det

## Unit 4 · Rank and the null space

Big ideas: MAIN

### 4.1 Rank



- ● **LA-4.1.A** (lay-5e:4, webwork-opl:LA2.4, webwork-opl:LA4.7) Find the rank of a matrix and use the rank theorem.
  - EK: rank + dim Nul = number of columns.
  - P1 · drills: la-rank-3x3, la-rank-nullity, la-row-space-reverse

### 4.2 Subspaces, bases and dimension



- ● **LA-4.2.A** (cupm-2015-la:3, lay-5e:4, webwork-opl:LA4.5) Decide whether a set is a subspace.
  - EK: Contains 0, closed under addition and scaling.
  - P1 · drills: la-subspace-test, la-subspace-which
- ● **LA-4.2.B** (cupm-2015-la:3, lay-5e:4, webwork-opl:LA4.6) Find the dimension of a span.
  - EK: Dimension = the number of independent vectors = rank.
  - P1 · drills: la-span-dimension, la-span-dim-3

### 4.3 Coordinates and change of basis



- ● **LA-4.3.A** (cupm-2015-la:4, lay-5e:4, webwork-opl:LA4.8) Find the coordinates of a vector in a basis.
  - EK: Solve P_B [x]_B = x.
  - P1 · drills: la-coordinates, la-orthogonal-coordinates
- ● **LA-4.3.B** (cupm-2015-la:4, lay-5e:4, webwork-opl:LA4.8) Convert coordinates back to the standard basis.
  - EK: x = P_B [x]_B, with the basis vectors as columns.
  - P1 · drills: la-change-of-basis, la-coords-to-standard-3

## Unit 5 · Eigenvalues and eigenvectors

Big ideas: MAIN

### 5.1 The eigenvalue problem



- ● **LA-5.1.A** (lay-5e:5, webwork-opl:LA7.1) Find the eigenvalues and eigenvectors of a 2 × 2 matrix.
  - EK: Sum of eigenvalues = trace, product = determinant.
  - P1 · drills: la-eigenvalues, la-eigenvector, mm-eigen-trace-det, la-eigen-triangular
- ● **LA-5.1.B** (lay-5e:5, webwork-opl:LA3.1, webwork-opl:LA7.2) Decide whether a matrix is diagonalisable and use the diagonal form.
  - EK: n independent eigenvectors; powers act on the eigenvalues.
  - P1 · drills: la-diagonalizable-facts, la-trace-of-power, em-diagonalise

### 5.2 Eigenvectors at work



- ● **LA-5.2.A** (cupm-2015-la:5, lay-5e:5, webwork-opl:LA7.5) Compute Aᵏx by expanding x in eigenvectors.
  - EK: Each eigenvector component is multiplied by λᵏ.
  - P1 · drills: la-power-by-eigenvectors, la-det-power
- ● **LA-5.2.B** (cupm-2015-la:5, lay-5e:5, webwork-opl:LA2.9, webwork-opl:PB7.1) Find the steady state of a Markov chain.
  - EK: The eigenvector for λ = 1, scaled to sum to 1.
  - P1 · drills: la-markov-steady-state, la-markov-two-step
- ● **LA-5.2.C** (cupm-2015-la:5, lay-5e:5, webwork-opl:LA7.3) Read a complex eigenvalue as a rotation and a scaling.
  - EK: [[a, −b], [b, a]] rotates by arg λ and scales by |λ| = √(a² + b²).
  - P1 · drills: la-complex-eigen-modulus, la-rotation-angle

## Unit 6 · Orthogonality and least squares

Big ideas: MAIN

### 6.1 Projections



- ● **LA-6.1.A** (lay-5e:6, webwork-opl:LA8.1, webwork-opl:LA8.3, webwork-opl:LA8.4, webwork-opl:LA8.5) Test orthogonality, project one vector on another and take a Gram–Schmidt step.
  - EK: proj = (u·v / v·v) v.
  - P1 · drills: la-orthogonal-check, la-projection-scalar, la-gram-schmidt-step
- ● **LA-6.1.B** (lay-5e:6, webwork-opl:LA8.4, webwork-opl:LA8.7) Set up and solve a least-squares problem.
  - EK: AᵀAx = Aᵀb.
  - P1 · drills: la-least-squares-slope, la-least-squares-facts

### 6.2 Length, complements and QR



- ● **LA-6.2.A** (cupm-2015-la:6, lay-5e:6, webwork-opl:LA4.1, webwork-opl:LA8.4) Find lengths and distances.
  - EK: ‖u − v‖ = √((u − v)·(u − v)).
  - P1 · drills: la-distance, la-cos-angle
- ● **LA-6.2.B** (cupm-2015-la:6, lay-5e:6, webwork-opl:LA8.4) Find vectors in an orthogonal complement.
  - EK: W⊥ is everything orthogonal to a spanning set of W.
  - P1 · drills: la-orthogonal-complement, la-perp-h
- ● **LA-6.2.C** (cupm-2015-la:6, lay-5e:6, webwork-opl:LA3.3) Find an entry of the QR factorisation.
  - EK: r_ii = length after removing earlier directions; r_ij = q_i · a_j.
  - P1 · drills: la-qr-entry, la-qr-r11

## Unit 7 · Symmetric matrices and singular values

Big ideas: MAIN

### 7.1 Singular values



- ● **LA-7.1.A** (lay-5e:7, webwork-opl:LA3.4) Find a singular value of a small matrix.
  - EK: Singular values are the square roots of the eigenvalues of AᵀA.
  - P1 · drills: la-singular-value, la-rank-one-singular-value
- ● **LA-7.1.B** (cupm-2015-la:second, lay-5e:7, webwork-opl:LA7.2) Use orthogonality of a symmetric matrix's eigenvectors.
  - EK: Different eigenvalues, orthogonal eigenvectors.
  - P1 · drills: la-symmetric-eigenvector, la-symmetric-larger-eig

### 7.2 Quadratic forms



- ● **LA-7.2.A** (cupm-2015-la:second, lay-5e:7, webwork-opl:LA7.4) Classify a quadratic form.
  - EK: The signs of the eigenvalues of its symmetric matrix decide.
  - P1 · drills: la-quadratic-form-classify, la-form-min-eig
- ● **LA-7.2.B** (cupm-2015-la:second, lay-5e:7, webwork-opl:LA7.4) Find the extreme values of a quadratic form on the unit sphere.
  - EK: The largest and smallest eigenvalues, at their eigenvectors.
  - P1 · drills: la-quadratic-form-max, la-form-max-radius

### 7.3 The singular value decomposition



- ● **LA-7.3.A** (cupm-2015-la:second, lay-5e:7, webwork-opl:LA3.4) Find the condition number from the singular values.
  - EK: κ = σ_max / σ_min.
  - P1 · drills: la-condition-number, la-cond-diag

## Unit 8 · Linear transformations

Big ideas: MAIN

### 8.1 The matrix of a linear map



- ● **LA-8.1.A** (cupm-2015-la:4, lay-5e:1, webwork-opl:LA9.1, webwork-opl:LA9.2) Build a map from the images of the basis vectors.
  - EK: The columns of the standard matrix are T(e1), …, T(en).
  - P1 · drills: la-map-from-basis-images, la-rotate-point
- ● **LA-8.1.B** (cupm-2015-la:4, lay-5e:2, webwork-opl:LA9.3) Compose linear maps as matrix products.
  - EK: S ∘ T has matrix ST: the first map stands on the right.
  - P1 · drills: la-composition, la-composition-order
- ● **LA-8.1.C** (cupm-2015-la:4, lay-5e:1, webwork-opl:LA9.4) Decide whether a map is one-to-one or onto from its rank.
  - EK: One-to-one: rank = number of columns; onto: rank = number of rows.
  - P1 · drills: la-one-to-one-onto, la-rank-onto

### 8.2 Kernel, range and other bases



- ● **LA-8.2.A** (cupm-2015-la:4, lay-5e:4, webwork-opl:LA6.6, webwork-opl:LA9.5) Find the dimensions of the kernel and range of a map on a function space.
  - EK: Rank–nullity holds for any linear map on a finite-dimensional space.
  - P1 · drills: la-kernel-dimension, la-derivative-range
- ● **LA-8.2.B** (cupm-2015-la:4, lay-5e:4, webwork-opl:LA6.7, webwork-opl:LA9.3) Write the matrix of a map relative to a basis.
  - EK: Columns are the coordinates of T(b1), …, T(bn).
  - P1 · drills: la-matrix-relative-to-basis, la-shift-matrix-entry

## Unit 9 · Abstract vector spaces and special matrices

Big ideas: MAIN

### 9.1 Abstract vector spaces



- ● **LA-9.1.A** (webwork-opl:LA6.1, webwork-opl:LA6.5) Decide whether a set with its operations is a vector space.
  - EK: Check the zero vector, closure under addition and under scaling; the rest of the axioms usually come free.
  - P1 · drills: la-is-vector-space, la-axiom-fails
- ● **LA-9.1.B** (webwork-opl:LA6.2) Write a polynomial as a combination of other polynomials.
  - EK: Match coefficients of each power and solve the linear system.
  - P1 · drills: la-poly-combination, la-poly-combo-2
- ● **LA-9.1.C** (webwork-opl:LA6.3) Decide whether a polynomial lies in the span of others.
  - EK: In the span exactly when the coefficient system is consistent.
  - P1 · drills: la-poly-span, la-poly-span-h
- ● **LA-9.1.D** (webwork-opl:LA6.4) Decide when polynomials are linearly dependent.
  - EK: Dependent exactly when the matrix of their coefficient vectors is singular.
  - P1 · drills: la-poly-dependence, la-poly-dependent-k
- ● **LA-9.1.E** (webwork-opl:LA6.8) Find the dimension of a standard space of matrices or polynomials.
  - EK: Count the free entries: symmetric n(n+1)/2, skew n(n−1)/2, trace zero n² − 1, P_n has n + 1.
  - P1 · drills: la-space-dimension, la-special-dim
- ● **LA-9.1.F** (webwork-opl:LA8.2) Compute an inner product of functions.
  - EK: ⟨f, g⟩ = ∫ f g dx is an inner product on continuous functions.
  - P1 · drills: la-function-inner-product, la-orthogonal-shift

### 9.2 Special matrices and applications



- ● **LA-9.2.A** (webwork-opl:LA1.7) Balance a chemical equation from the null space of its composition matrix.
  - EK: Each element gives one equation; the coefficients span the null space.
  - P1 · drills: la-balance-combustion, la-oxygen-coefficient
- ● **LA-9.2.B** (webwork-opl:LA2.7) Invert an elementary matrix.
  - EK: The inverse undoes the row operation: add −k instead of k, divide instead of multiply, swap back.
  - P1 · drills: la-elementary-inverse, la-elementary-power
- ● **LA-9.2.C** (webwork-opl:LA2.8) Compute with complex matrix entries.
  - EK: Arithmetic is ordinary arithmetic with i² = −1; conjugates pair up into real numbers.
  - P1 · drills: la-complex-det, la-complex-det-modulus
- ● **LA-9.2.D** (webwork-opl:LA3.5) Compute a power of a Jordan block.
  - EK: [[λ, 1], [0, λ]]ᵏ = [[λᵏ, kλᵏ⁻¹], [0, λᵏ]].
  - P1 · drills: la-jordan-power, la-jordan-exp
- ● **LA-9.2.E** (webwork-opl:LA8.6) Use the properties of an orthogonal matrix.
  - EK: Qᵀ Q = I, so Q⁻¹ = Qᵀ and lengths and angles are preserved.
  - P1 · drills: la-orthogonal-inverse, la-orthogonal-norm
- ● **LA-9.2.F** (webwork-opl:LA9.6) Invert a linear transformation.
  - EK: T is invertible exactly when its matrix is; T⁻¹ has the inverse matrix.
  - P1 · drills: la-map-inverse, la-poly-map-inverse

## Drills not yet placed on the map

- hs2-inverse-2x2 (la.inverse)
