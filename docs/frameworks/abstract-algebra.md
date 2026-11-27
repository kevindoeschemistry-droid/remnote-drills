# Abstract Algebra — curriculum framework (draft 1)

Generated from `drills/frameworks/abstract-algebra.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**20 learning objectives** in 6 units (16 core): 20 drilled, 0 partly, 0 with no drills. Core: 16 / 16 drilled.

## Big ideas

- **SYM · A group is the symmetries of something.** Every group acts, and counting orbits and stabilisers is how its structure is read off.
- **DIV · Orders divide.** Lagrange's theorem and its relatives turn structural questions into arithmetic on the order of the group.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Groups and subgroups | core | — | 4 | 4 | 0 | 0 |
| 2 · Permutations | core | — | 3 | 3 | 0 | 0 |
| 3 · Group actions | core | — | 3 | 3 | 0 | 0 |
| 4 · Quotients and structure | core | — | 3 | 3 | 0 | 0 |
| 5 · Rings | core | — | 3 | 3 | 0 | 0 |
| 6 · Fields and Galois theory | extension | — | 4 | 4 | 0 | 0 |

## Unit 1 · Groups and subgroups

Big ideas: SYM, DIV

### 1.1 Axioms, orders and Lagrange



- ● **AA-1.1.A** (cambridge-ia-groups:G1) Decide whether a set with an operation is a group and name the axiom that fails.
  - EK: A group needs closure, associativity, an identity and an inverse for every element. Commutativity is not required.
  - P2 · drills: aa-is-it-a-group, aa-failed-axiom
- ● **AA-1.1.B** (cambridge-ia-groups:G1, cambridge-ia-groups:G2) Find the order of an element of a cyclic group and count elements of a given order.
  - EK: In Z_n the element a has order n/gcd(a, n). A cyclic group of order n has φ(d) elements of order d for each divisor d, and none of any other order.
  - P1 · drills: aa-order-in-zn, aa-count-order-d
- ● **AA-1.1.C** (cambridge-ia-groups:G2) Use Lagrange's theorem to limit subgroup orders and count cosets.
  - EK: The order of a subgroup divides the order of the group, and the index |G|/|H| is the number of cosets. A group of prime order is cyclic.
  - P1 · drills: aa-coset-count, aa-lagrange-facts
- ● **AA-1.1.D** (cambridge-ia-groups:G2) Find the order of the group of units modulo n and decide whether it is cyclic.
  - EK: The units modulo n form a group of order φ(n). It is cyclic exactly for n = 1, 2, 4, p^k and 2p^k with p an odd prime.
  - P1 · drills: aa-unit-group-order, aa-unit-group-cyclic

## Unit 2 · Permutations

Big ideas: SYM

### 2.1 Cycles, sign and conjugacy



- ● **AA-2.1.A** (cambridge-ia-groups:G6) Compose permutations in cycle notation and find the order of a permutation.
  - EK: Disjoint cycles commute and the order of a permutation is the least common multiple of its cycle lengths. Products are applied right to left.
  - P1 · drills: aa-perm-order, aa-perm-compose
- ● **AA-2.1.B** (cambridge-ia-groups:G6) Find the sign of a permutation and work with the alternating group.
  - EK: A cycle of length k is a product of k − 1 transpositions, so it is even when k is odd. The even permutations form A_n, of order n!/2.
  - P1 · drills: aa-perm-sign, aa-alternating-order
- ● **AA-2.1.C** (cambridge-ia-groups:G6, cambridge-ia-groups:G3) Count conjugacy classes in a symmetric group and the size of a class.
  - EK: Two permutations are conjugate in S_n exactly when they have the same cycle type, so the classes are the partitions of n. A class with m_k cycles of length k has n!/Π(k^m_k · m_k!) elements.
  - P1 · drills: aa-sn-class-count, aa-sn-class-size

## Unit 3 · Group actions

Big ideas: SYM, DIV

### 3.1 Orbits, stabilisers and counting



- ● **AA-3.1.A** (cambridge-ia-groups:G3, cambridge-ia-groups:G5) Use the orbit-stabiliser theorem to find the order of a symmetry group.
  - EK: |G| = |orbit| × |stabiliser|. The rotations of a cube move a face to any of 6 faces and 4 rotations fix a face, so there are 24.
  - P1 · drills: aa-orbit-stabiliser, aa-stabiliser-size
- ● **AA-3.1.B** (cambridge-ia-groups:G3) Count orbits with Burnside's lemma.
  - EK: The number of orbits is the average number of fixed points: (1/|G|) Σ |Fix(g)|. A rotation by r places of an n-bead ring fixes k^gcd(n, r) colourings.
  - P1 · drills: aa-necklaces, aa-burnside-average
- ● **AA-3.1.C** (cambridge-ia-groups:G3, cambridge-ib-grm:GR) Use centralisers, the class equation and Cauchy's theorem.
  - EK: The size of a conjugacy class is |G| divided by the size of the centraliser. The class equation forces a non-trivial centre in a p-group, and Cauchy: if a prime p divides |G| there is an element of order p.
  - P1 · drills: aa-centraliser-size, aa-class-equation-facts

## Unit 4 · Quotients and structure

Big ideas: DIV

### 4.1 Homomorphisms, abelian groups and Sylow



- ● **AA-4.1.A** (cambridge-ia-groups:G4, cambridge-ib-grm:GR) Apply the first isomorphism theorem and count homomorphisms between cyclic groups.
  - EK: The image of a homomorphism is isomorphic to G/ker, so |image| = |G|/|kernel|. A homomorphism from Z_m to Z_n is fixed by where 1 goes, and there are gcd(m, n) of them.
  - P1 · drills: aa-image-size, aa-hom-count
- ● **AA-4.1.B** (cambridge-ib-grm:MO) Classify finite abelian groups of a given order and decide when a product is cyclic.
  - EK: Every finite abelian group is a product of cyclic groups of prime-power order. For n = Π p^a the number of abelian groups is Π (number of partitions of a). Z_m × Z_n is cyclic exactly when gcd(m, n) = 1.
  - P1 · drills: aa-abelian-count, aa-product-max-order
- ● **AA-4.1.C** (cambridge-ib-grm:GR) Use the Sylow theorems to limit the number of Sylow subgroups.
  - EK: If |G| = p^a m with p not dividing m, the number of Sylow p-subgroups divides m and is 1 mod p. When that leaves only 1, the subgroup is normal and the group is not simple.
  - P1 · drills: aa-sylow-options, aa-sylow-facts

## Unit 5 · Rings

Big ideas: DIV

### 5.1 Units, ideals and factorisation



- ● **AA-5.1.A** (cambridge-ib-grm:RI) Count units, zero divisors and idempotents in Z_n.
  - EK: In Z_n a non-zero residue is a unit if it is coprime to n and a zero divisor otherwise. Z_n has 2^k idempotents, where k is the number of distinct primes dividing n.
  - P1 · drills: aa-zero-divisors, aa-idempotents
- ● **AA-5.1.B** (cambridge-ib-grm:RI) Decide whether a quotient ring is a field and count roots of a polynomial over Z_p.
  - EK: Z_n is a field exactly when n is prime, and F[x]/(f) is a field exactly when f is irreducible. Over a field a polynomial of degree d has at most d roots; over Z_n with n composite it can have more.
  - P2 · drills: aa-field-or-not, aa-roots-mod-n
- ● **AA-5.1.C** (cambridge-ib-grm:RI) Work with norms in the Gaussian integers and recognise failures of unique factorisation.
  - EK: N(a + bi) = a² + b² is multiplicative, so an element of prime norm is irreducible. Z[i] has unique factorisation; Z[√−5] does not, since 6 = 2 · 3 = (1 + √−5)(1 − √−5).
  - P1 · drills: aa-gaussian-norm, aa-factorisation-facts

## Unit 6 · Fields and Galois theory (extension)

Big ideas: SYM, DIV

### 6.1 Extensions, finite fields and the Galois correspondence



- ● **AA-6.1.D** (cambridge-ii-galois-theory:S) Decide what can be constructed by ruler and compass or solved by radicals.
  - EK: A length is constructible only if its degree over Q is a power of 2, so a regular n-gon is constructible exactly when φ(n) is a power of 2. A polynomial is soluble by radicals exactly when its Galois group is soluble; S₅ is not.
  - P1 · drills: aa-constructible-polygon, aa-impossibility-facts
- ● **AA-6.1.A** (cambridge-ii-galois-theory:E) Find the degree of a field extension and use the tower law.
  - EK: [K(α) : K] is the degree of the minimal polynomial of α over K, and degrees multiply up a tower: [M : K] = [M : L][L : K].
  - P1 · drills: aa-extension-degree, aa-tower-law
- ● **AA-6.1.B** (cambridge-ii-galois-theory:F) Count the elements, subfields and irreducible polynomials of a finite field.
  - EK: There is exactly one field of each prime-power order pⁿ. Its non-zero elements form a cyclic group, its subfields are the fields of order p^d for d dividing n, and xᵖⁿ − x is the product of every monic irreducible over F_p whose degree divides n.
  - P1 · drills: aa-irreducible-count, aa-subfield-count
- ● **AA-6.1.C** (cambridge-ii-galois-theory:G) Find the order of a Galois group and read the Galois correspondence.
  - EK: For a Galois extension the group has order equal to the degree, and subgroups correspond to intermediate fields with inclusions reversed; a subfield is normal over the base exactly when its subgroup is normal. Q(ζ_n) has group the units modulo n, of order φ(n).
  - P1 · drills: aa-cyclotomic-degree, aa-galois-correspondence
