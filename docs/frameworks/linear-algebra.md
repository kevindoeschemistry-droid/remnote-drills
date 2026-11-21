# Linear Algebra — curriculum framework (draft 1)

Generated from `drills/frameworks/linear-algebra.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**10 learning objectives** in 7 units (10 core): 10 drilled, 0 partly, 0 with no drills. Core: 10 / 10 drilled.

## Big ideas

- **MAIN · A matrix is a linear map.** Every question (solvable or not, invertible or not, which directions are only stretched) is a question about what the map does to space.

## Practices

- **P1 · Compute and interpret.** Carry a calculation to a number or a vector and say what it means for the system or the map.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Linear systems and independence | core | — | 2 | 2 | 0 | 0 |
| 2 · Matrix algebra | core | — | 1 | 1 | 0 | 0 |
| 3 · Determinants | core | — | 1 | 1 | 0 | 0 |
| 4 · Rank and the null space | core | — | 1 | 1 | 0 | 0 |
| 5 · Eigenvalues and eigenvectors | core | — | 2 | 2 | 0 | 0 |
| 6 · Orthogonality and least squares | core | — | 2 | 2 | 0 | 0 |
| 7 · Symmetric matrices and singular values | core | — | 1 | 1 | 0 | 0 |

## Unit 1 · Linear systems and independence

Big ideas: MAIN

### 1.1 Row reduction



- ● **LA-1.1.A** (lay-5e:1) Solve a linear system by row reduction.
  - EK: Pivots give the basic variables; a row 0 = c means no solution.
  - P1 · drills: la-system
- ● **LA-1.1.B** (lay-5e:1) Decide whether a set of vectors is linearly independent.
  - EK: Independent exactly when the only solution of Ax = 0 is zero.
  - P1 · drills: la-independence

## Unit 2 · Matrix algebra

Big ideas: MAIN

### 2.1 Inverses



- ● **LA-2.1.A** (lay-5e:2) Find the inverse of a 2 × 2 matrix.
  - EK: Swap the diagonal, negate the off-diagonal, divide by the determinant.
  - P1 · drills: la-inverse

## Unit 3 · Determinants

Big ideas: MAIN

### 3.1 Cofactor expansion



- ● **LA-3.1.A** (lay-5e:3) Compute a 3 × 3 determinant.
  - EK: Expand along the row or column with the most zeros.
  - P1 · drills: la-det, mm-determinant

## Unit 4 · Rank and the null space

Big ideas: MAIN

### 4.1 Rank



- ● **LA-4.1.A** (lay-5e:4) Find the rank of a matrix and use the rank theorem.
  - EK: rank + dim Nul = number of columns.
  - P1 · drills: la-rank-3x3, la-rank-nullity

## Unit 5 · Eigenvalues and eigenvectors

Big ideas: MAIN

### 5.1 The eigenvalue problem



- ● **LA-5.1.A** (lay-5e:5) Find the eigenvalues and eigenvectors of a 2 × 2 matrix.
  - EK: Sum of eigenvalues = trace, product = determinant.
  - P1 · drills: la-eigenvalues, la-eigenvector, mm-eigen-trace-det
- ● **LA-5.1.B** (lay-5e:5) Decide whether a matrix is diagonalisable and use the diagonal form.
  - EK: n independent eigenvectors; powers act on the eigenvalues.
  - P1 · drills: la-diagonalizable-facts, la-trace-of-power, em-diagonalise

## Unit 6 · Orthogonality and least squares

Big ideas: MAIN

### 6.1 Projections



- ● **LA-6.1.A** (lay-5e:6) Test orthogonality, project one vector on another and take a Gram–Schmidt step.
  - EK: proj = (u·v / v·v) v.
  - P1 · drills: la-orthogonal-check, la-projection-scalar, la-gram-schmidt-step
- ● **LA-6.1.B** (lay-5e:6) Set up and solve a least-squares problem.
  - EK: AᵀAx = Aᵀb.
  - P1 · drills: la-least-squares-slope, la-least-squares-facts

## Unit 7 · Symmetric matrices and singular values

Big ideas: MAIN

### 7.1 Singular values



- ● **LA-7.1.A** (lay-5e:7) Find a singular value of a small matrix.
  - EK: Singular values are the square roots of the eigenvalues of AᵀA.
  - P1 · drills: la-singular-value

## Drills not yet placed on the map

- hs2-inverse-2x2 (la.inverse)
