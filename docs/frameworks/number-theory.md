# Number Theory — curriculum framework (draft 1)

Generated from `drills/frameworks/number-theory.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**26 learning objectives** in 4 units (26 core): 26 drilled, 0 partly, 0 with no drills. Core: 26 / 26 drilled.

## Big ideas

- **MOD · Work in the right modulus.** Most questions about integers become finite once reduced modulo the right number; the art is choosing it.
- **STRUCT · The units modulo n form a group.** Fermat, Euler, Wilson and primitive roots are all statements about the group of units, and its order is φ(n).

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Divisibility and factorisation | core | — | 6 | 6 | 0 | 0 |
| 2 · Congruences | core | — | 8 | 8 | 0 | 0 |
| 3 · Primitive roots and quadratic residues | core | — | 5 | 5 | 0 | 0 |
| 4 · Diophantine equations and primes | core | — | 7 | 7 | 0 | 0 |

## Unit 1 · Divisibility and factorisation

Big ideas: MOD

### 1.1 Euclid and unique factorisation



- ● **NT-1.1.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Run Euclid's algorithm and say how long it takes.
  - EK: gcd(a, b) = gcd(b, a mod b); the last non-zero remainder is the gcd. Consecutive Fibonacci numbers are the slowest inputs.
  - Needs: DM-1.2.A, NT-1.2.C
  - P1 · drills: nt-gcd, nt-euclid-steps
- ● **NT-1.1.B** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Solve a linear congruence or a linear Diophantine equation with Bezout's identity.
  - EK: ax + by = c has integer solutions exactly when gcd(a, b) divides c; running Euclid backwards finds one, and the rest differ by multiples of (b/g, −a/g).
  - Needs: NT-1.1.A
  - P1 · drills: nt-linear-congruence, nt-coin-solutions
- ● **NT-1.1.C** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Count and sum the divisors of an integer from its prime factorisation.
  - EK: If n = Π p^a then n has Π (a + 1) divisors and σ(n) = Π (p^(a+1) − 1)/(p − 1); both functions are multiplicative.
  - Needs: NT-1.1.A, NT-1.2.C, NT-1.2.B
  - P1 · drills: nt-divisor-count, nt-divisor-sum

### 1.2 Remainders and factorisations



- ● **NT-1.2.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Apply the division algorithm, including to negative numbers.
  - EK: For any integer a and positive n there is exactly one pair q, r with a = qn + r and 0 ≤ r < n. The remainder is never negative: −7 = (−2)·5 + 3.
  - Needs: DM-1.2.A
  - P1 · drills: nt-remainder-negative, nt-quotient-remainder
- ● **NT-1.2.B** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Find how often a prime divides a factorial.
  - EK: The exponent of p in n! is ⌊n/p⌋ + ⌊n/p²⌋ + ⌊n/p³⌋ + … (Legendre). The number of trailing zeros of n! is the exponent of 5.
  - Needs: NT-1.2.A
  - P1 · drills: nt-prime-in-factorial, nt-trailing-zeros
- ● **NT-1.2.C** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Read the gcd and lcm off prime factorisations.
  - EK: Take the smaller exponent of each prime for the gcd and the larger for the lcm, so gcd(a, b) · lcm(a, b) = ab.
  - Needs: NT-1.2.A
  - P1 · drills: nt-lcm-from-factors, nt-gcd-lcm-product

## Unit 2 · Congruences

Big ideas: MOD, STRUCT

### 2.1 Arithmetic modulo n



- ● **NT-2.1.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Find a modular inverse and reduce a large power with Fermat's little theorem.
  - EK: a has an inverse modulo n exactly when gcd(a, n) = 1. For a prime p not dividing a, a^(p−1) ≡ 1 (mod p), so exponents reduce modulo p − 1.
  - Needs: NT-1.1.B, NT-2.2.C
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
  - Needs: NT-2.1.B, NT-2.2.D
  - P1 · drills: nt-rsa-private, nt-rsa-encrypt

### 2.2 Congruence arithmetic



- ● **NT-2.2.A** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Add, multiply and take powers of residues.
  - EK: Congruence respects addition and multiplication, so any integer may be replaced by its remainder at any stage. Powers of a residue repeat in a cycle.
  - Needs: NT-1.2.A
  - P1 · drills: nt-residue-expression, nt-last-digit-power
- ● **NT-2.2.B** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Explain and use the digit tests for 9 and 11.
  - EK: Since 10 ≡ 1 (mod 9), a number is congruent to its digit sum modulo 9; since 10 ≡ −1 (mod 11), it is congruent to its alternating digit sum modulo 11.
  - Needs: NT-2.2.A
  - P1 · drills: nt-mod-nine, nt-mod-eleven
- ● **NT-2.2.C** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Solve a linear congruence and count its solutions.
  - EK: ax ≡ b (mod n) has a solution exactly when d = gcd(a, n) divides b, and then it has exactly d solutions modulo n.
  - Needs: NT-2.2.A, NT-1.1.B
  - P1 · drills: nt-congruence-count, nt-congruence-solve
- ● **NT-2.2.D** (cambridge-ii-number-theory:T1, cambridge-ia-numbers-sets:N4) Reduce an exponent with Euler's theorem and invert with Fermat's.
  - EK: If gcd(a, n) = 1 then exponents may be reduced modulo φ(n). Modulo a prime p, the inverse of a is a^(p−2).
  - Needs: NT-2.1.A, NT-2.1.B
  - P1 · drills: nt-euler-reduce, nt-fermat-inverse

## Unit 3 · Primitive roots and quadratic residues

Big ideas: STRUCT

### 3.1 The structure of the units



- ● **NT-3.1.A** (cambridge-ii-number-theory:T2) Find the order of an element modulo a prime and count primitive roots.
  - EK: The order of a modulo p divides p − 1. A primitive root has order p − 1; every prime has φ(p − 1) of them.
  - Needs: NT-2.1.B
  - P1 · drills: nt-order-mod-p, nt-primitive-root-count
- ● **NT-3.1.B** (cambridge-ii-number-theory:T3) Evaluate a Legendre symbol with Euler's criterion and the reciprocity laws.
  - EK: (a/p) ≡ a^((p−1)/2) (mod p). (−1/p) = 1 exactly when p ≡ 1 (mod 4); (2/p) = 1 exactly when p ≡ ±1 (mod 8); for odd primes (p/q)(q/p) = −1 only when both are 3 mod 4.
  - Needs: NT-3.1.A, NT-3.2.B
  - P1 · drills: nt-legendre, nt-reciprocity-facts
- ● **NT-3.1.C** (cambridge-ii-number-theory:T4) Evaluate a Jacobi symbol by reciprocity and say what it does and does not tell you.
  - EK: The Jacobi symbol (a/n) for odd n multiplies the Legendre symbols over the prime factors of n and obeys the same reciprocity rules, so it is computed without factorising. (a/n) = −1 means a is not a square modulo n; (a/n) = 1 does not mean it is.
  - Needs: NT-3.1.B
  - P1 · drills: nt-jacobi, nt-jacobi-facts

### 3.2 Squares modulo a prime



- ● **NT-3.2.A** (cambridge-ii-number-theory:T3) List the squares modulo a prime and count the solutions of x² ≡ a.
  - EK: Modulo an odd prime p the non-zero squares are the (p − 1)/2 values of 1², 2², …, ((p − 1)/2)². x² ≡ a has two solutions if a is a non-zero square, one if a ≡ 0, none otherwise.
  - Needs: NT-2.2.A
  - P1 · drills: nt-square-solutions, nt-count-squares
- ● **NT-3.2.B** (cambridge-ii-number-theory:T3) Apply Euler's criterion by direct computation.
  - EK: a^((p−1)/2) is congruent to 1 if a is a non-zero square modulo p and to −1 (that is, p − 1) if it is not.
  - Needs: NT-3.2.A, NT-2.1.A
  - P1 · drills: nt-euler-criterion, nt-criterion-facts

## Unit 4 · Diophantine equations and primes

Big ideas: MOD

### 4.1 Continued fractions, squares and primality



- ● **NT-4.1.B** (cambridge-ii-number-theory:T3, cambridge-ib-grm:RI) Decide whether an integer is a sum of two squares.
  - EK: An odd prime is a sum of two squares exactly when it is 1 mod 4. In general n is one exactly when every prime that is 3 mod 4 divides n to an even power.
  - Needs: NT-3.1.B, NT-4.2.C
  - P2 · drills: nt-sum-two-squares, nt-two-squares-facts
- ● **NT-4.1.A** (cambridge-ii-number-theory:T7) Expand a rational as a continued fraction and solve a Pell equation.
  - EK: The continued fraction of p/q is Euclid's algorithm written down. The convergents of √d give the solutions of x² − dy² = 1, and every solution is a power of the smallest.
  - Needs: NT-1.1.A
  - P1 · drills: nt-continued-fraction, nt-pell
- ● **NT-4.1.C** (cambridge-ii-number-theory:T6, cambridge-ii-number-theory:T8) Estimate how many primes lie below a bound and apply the Fermat primality test.
  - EK: π(x) is about x/ln x. If a^(n−1) is not 1 modulo n then n is composite; composites that pass for base a are pseudoprimes, and Carmichael numbers such as 561 pass for every coprime base.
  - Needs: NT-2.1.A, NT-4.2.A
  - P1 · drills: nt-prime-count-estimate, nt-fermat-test
- ● **NT-4.1.D** (cambridge-ii-number-theory:T9) Factorise an integer by writing it as a difference of squares.
  - EK: If n = a² − b² then n = (a − b)(a + b). Fermat's method tries a = ⌈√n⌉, ⌈√n⌉ + 1, … until a² − n is a square. More generally x² ≡ y² (mod n) with x ≢ ±y gives the factor gcd(x − y, n).
  - Needs: NT-1.1.C
  - P1 · drills: nt-fermat-factorise, nt-congruent-squares

### 4.2 Primes up close



- ● **NT-4.2.A** (cambridge-ii-number-theory:T6) Count primes in a range with the sieve of Eratosthenes.
  - EK: To find the primes up to N, cross out multiples of each prime up to √N; what survives is prime. A number below N with no prime factor up to √N is prime.
  - Needs: NT-1.2.A
  - P1 · drills: nt-count-primes, nt-trial-division-bound
- ● **NT-4.2.B** (cambridge-ii-number-theory:T1, cambridge-ii-number-theory:T8) Connect Mersenne primes to even perfect numbers.
  - EK: If 2ᵖ − 1 is prime then 2ᵖ⁻¹(2ᵖ − 1) is perfect, and every even perfect number has this form (Euclid, Euler). 2ᵖ − 1 can only be prime when p is prime, but need not be: 2¹¹ − 1 = 23 · 89.
  - Needs: NT-1.1.C, NT-4.2.A
  - P1 · drills: nt-perfect-from-mersenne, nt-mersenne-facts
- ● **NT-4.2.C** (cambridge-ii-number-theory:T7) Generate Pythagorean triples.
  - EK: For m > n > 0, (m² − n², 2mn, m² + n²) is a Pythagorean triple; it is primitive exactly when m and n are coprime and of opposite parity, and every primitive triple arises this way.
  - Needs: NT-1.2.C
  - P1 · drills: nt-triple-hypotenuse, nt-triple-primitive
