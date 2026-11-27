# Number Theory — curriculum framework (draft 1)

Generated from `drills/frameworks/number-theory.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**14 learning objectives** in 4 units (14 core): 14 drilled, 0 partly, 0 with no drills. Core: 14 / 14 drilled.

## Big ideas

- **MOD · Work in the right modulus.** Most questions about integers become finite once reduced modulo the right number; the art is choosing it.
- **STRUCT · The units modulo n form a group.** Fermat, Euler, Wilson and primitive roots are all statements about the group of units, and its order is φ(n).

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Divisibility and factorisation | core | — | 3 | 3 | 0 | 0 |
| 2 · Congruences | core | — | 4 | 4 | 0 | 0 |
| 3 · Primitive roots and quadratic residues | core | — | 3 | 3 | 0 | 0 |
| 4 · Diophantine equations and primes | core | — | 4 | 4 | 0 | 0 |

## Unit 1 · Divisibility and factorisation

Big ideas: MOD

### 1.1 Euclid and unique factorisation



- ● **NT-1.1.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Run Euclid's algorithm and say how long it takes.
  - EK: gcd(a, b) = gcd(b, a mod b); the last non-zero remainder is the gcd. Consecutive Fibonacci numbers are the slowest inputs.
  - Needs: DM-1.2.A
  - P1 · drills: nt-gcd, nt-euclid-steps
- ● **NT-1.1.B** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Solve a linear congruence or a linear Diophantine equation with Bezout's identity.
  - EK: ax + by = c has integer solutions exactly when gcd(a, b) divides c; running Euclid backwards finds one, and the rest differ by multiples of (b/g, −a/g).
  - Needs: NT-1.1.A
  - P1 · drills: nt-linear-congruence, nt-coin-solutions
- ● **NT-1.1.C** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Count and sum the divisors of an integer from its prime factorisation.
  - EK: If n = Π p^a then n has Π (a + 1) divisors and σ(n) = Π (p^(a+1) − 1)/(p − 1); both functions are multiplicative.
  - Needs: NT-1.1.A
  - P1 · drills: nt-divisor-count, nt-divisor-sum

## Unit 2 · Congruences

Big ideas: MOD, STRUCT

### 2.1 Arithmetic modulo n



- ● **NT-2.1.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Find a modular inverse and reduce a large power with Fermat's little theorem.
  - EK: a has an inverse modulo n exactly when gcd(a, n) = 1. For a prime p not dividing a, a^(p−1) ≡ 1 (mod p), so exponents reduce modulo p − 1.
  - Needs: NT-1.1.B
  - P1 · drills: nt-inverse, nt-fermat-power
- ● **NT-2.1.B** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Compute Euler's function and use Euler's theorem.
  - EK: φ(n) = n Π (1 − 1/p) over the primes dividing n, and a^φ(n) ≡ 1 (mod n) whenever gcd(a, n) = 1.
  - Needs: NT-2.1.A, NT-1.1.C
  - P1 · drills: nt-euler-phi, nt-last-two-digits
- ● **NT-2.1.C** (cambridge-ii-number-theory:T2, cambridge-ia-numbers-sets:N4) Solve simultaneous congruences and use Wilson's theorem.
  - EK: If m and n are coprime, x ≡ a (mod m), x ≡ b (mod n) has exactly one solution modulo mn. Wilson: (p − 1)! ≡ −1 (mod p) exactly when p is prime.
  - Needs: NT-2.1.A
  - P1 · drills: nt-crt, nt-wilson
- ● **NT-2.1.D** (cambridge-ia-numbers-sets:N4) Find an RSA decryption exponent and encrypt a small message.
  - EK: With n = pq and φ = (p − 1)(q − 1), the public exponent e and private exponent d satisfy ed ≡ 1 (mod φ); encryption is m^e mod n and decryption c^d mod n.
  - Needs: NT-2.1.B
  - P1 · drills: nt-rsa-private, nt-rsa-encrypt

## Unit 3 · Primitive roots and quadratic residues

Big ideas: STRUCT

### 3.1 The structure of the units



- ● **NT-3.1.A** (cambridge-ii-number-theory:T2) Find the order of an element modulo a prime and count primitive roots.
  - EK: The order of a modulo p divides p − 1. A primitive root has order p − 1; every prime has φ(p − 1) of them.
  - Needs: NT-2.1.B
  - P1 · drills: nt-order-mod-p, nt-primitive-root-count
- ● **NT-3.1.B** (cambridge-ii-number-theory:T3) Evaluate a Legendre symbol with Euler's criterion and the reciprocity laws.
  - EK: (a/p) ≡ a^((p−1)/2) (mod p). (−1/p) = 1 exactly when p ≡ 1 (mod 4); (2/p) = 1 exactly when p ≡ ±1 (mod 8); for odd primes (p/q)(q/p) = −1 only when both are 3 mod 4.
  - Needs: NT-3.1.A
  - P1 · drills: nt-legendre, nt-reciprocity-facts
- ● **NT-3.1.C** (cambridge-ii-number-theory:T4) Evaluate a Jacobi symbol by reciprocity and say what it does and does not tell you.
  - EK: The Jacobi symbol (a/n) for odd n multiplies the Legendre symbols over the prime factors of n and obeys the same reciprocity rules, so it is computed without factorising. (a/n) = −1 means a is not a square modulo n; (a/n) = 1 does not mean it is.
  - Needs: NT-3.1.B
  - P1 · drills: nt-jacobi, nt-jacobi-facts

## Unit 4 · Diophantine equations and primes

Big ideas: MOD

### 4.1 Continued fractions, squares and primality



- ● **NT-4.1.B** (cambridge-ii-number-theory:T3, cambridge-ib-grm:RI) Decide whether an integer is a sum of two squares.
  - EK: An odd prime is a sum of two squares exactly when it is 1 mod 4. In general n is one exactly when every prime that is 3 mod 4 divides n to an even power.
  - Needs: NT-3.1.B
  - P2 · drills: nt-sum-two-squares, nt-two-squares-facts
- ● **NT-4.1.A** (cambridge-ii-number-theory:T7) Expand a rational as a continued fraction and solve a Pell equation.
  - EK: The continued fraction of p/q is Euclid's algorithm written down. The convergents of √d give the solutions of x² − dy² = 1, and every solution is a power of the smallest.
  - Needs: NT-1.1.A
  - P1 · drills: nt-continued-fraction, nt-pell
- ● **NT-4.1.C** (cambridge-ii-number-theory:T6, cambridge-ii-number-theory:T8) Estimate how many primes lie below a bound and apply the Fermat primality test.
  - EK: π(x) is about x/ln x. If a^(n−1) is not 1 modulo n then n is composite; composites that pass for base a are pseudoprimes, and Carmichael numbers such as 561 pass for every coprime base.
  - Needs: NT-2.1.A
  - P1 · drills: nt-prime-count-estimate, nt-fermat-test
- ● **NT-4.1.D** (cambridge-ii-number-theory:T9) Factorise an integer by writing it as a difference of squares.
  - EK: If n = a² − b² then n = (a − b)(a + b). Fermat's method tries a = ⌈√n⌉, ⌈√n⌉ + 1, … until a² − n is a square. More generally x² ≡ y² (mod n) with x ≢ ±y gives the factor gcd(x − y, n).
  - Needs: NT-1.1.C
  - P1 · drills: nt-fermat-factorise, nt-congruent-squares
