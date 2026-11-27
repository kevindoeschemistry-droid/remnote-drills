# Abstract Algebra — curriculum framework (draft 1)

Generated from `drills/frameworks/abstract-algebra.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**40 learning objectives** in 6 units (36 core): 40 drilled, 0 partly, 0 with no drills. Core: 36 / 36 drilled.

## Big ideas

- **SYM · A group is the symmetries of something.** Every group acts, and counting orbits and stabilisers is how its structure is read off.
- **DIV · Orders divide.** Lagrange's theorem and its relatives turn structural questions into arithmetic on the order of the group.

## Practices

- **P1 · Compute.** Carry the definition or theorem to a number, a count or an example.
- **P2 · Decide.** Say whether a statement holds, which hypothesis fails, or which example breaks it.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Groups and subgroups | core | — | 10 | 10 | 0 | 0 |
| 2 · Permutations | core | — | 7 | 7 | 0 | 0 |
| 3 · Group actions | core | — | 6 | 6 | 0 | 0 |
| 4 · Quotients and structure | core | — | 7 | 7 | 0 | 0 |
| 5 · Rings | core | — | 6 | 6 | 0 | 0 |
| 6 · Fields and Galois theory | extension | — | 4 | 4 | 0 | 0 |

## Unit 1 · Groups and subgroups

Big ideas: SYM, DIV

### 1.1 Axioms, orders and Lagrange



- ● **AA-1.1.A** (cambridge-ia-groups:G1) Decide whether a set with an operation is a group and name the axiom that fails.
  - EK: A group needs closure, associativity, an identity and an inverse for every element. Commutativity is not required.
  - P2 · drills: aa-is-it-a-group, aa-failed-axiom
- ● **AA-1.1.B** (cambridge-ia-groups:G1, cambridge-ia-groups:G2) Find the order of an element of a cyclic group and count elements of a given order.
  - EK: In Z_n the element a has order n/gcd(a, n). A cyclic group of order n has φ(d) elements of order d for each divisor d, and none of any other order.
  - Needs: AA-1.2.B
  - P1 · drills: aa-order-in-zn, aa-count-order-d
- ● **AA-1.1.C** (cambridge-ia-groups:G2) Use Lagrange's theorem to limit subgroup orders and count cosets.
  - EK: The order of a subgroup divides the order of the group, and the index |G|/|H| is the number of cosets. A group of prime order is cyclic.
  - Needs: AA-1.2.D
  - P1 · drills: aa-coset-count, aa-lagrange-facts
- ● **AA-1.1.D** (cambridge-ia-groups:G2) Find the order of the group of units modulo n and decide whether it is cyclic.
  - EK: The units modulo n form a group of order φ(n). It is cyclic exactly for n = 1, 2, 4, p^k and 2p^k with p an odd prime.
  - Needs: AA-1.2.B, NT-2.1.B
  - P1 · drills: aa-unit-group-order, aa-unit-group-cyclic

### 1.2 One group at a time



- ● **AA-1.2.A** (cambridge-ia-groups:G1) Compute in the group of units modulo n: products and inverses.
  - EK: The units modulo n are the residues coprime to n, multiplied modulo n. The identity is 1 and each unit has exactly one inverse, which is again a unit.
  - Needs: AA-1.1.A, NT-2.1.A
  - P1 · drills: aa-unit-product, aa-unit-inverse
- ● **AA-1.2.B** (cambridge-ia-groups:G1, cambridge-ia-groups:G2) Find the order of an element of a multiplicative group by taking powers.
  - EK: The order of a is the least k ≥ 1 with a^k equal to the identity. The powers of a cycle with that period, so a^m is the identity exactly when the order divides m.
  - Needs: AA-1.2.A
  - P1 · drills: aa-unit-order, aa-power-reduce
- ● **AA-1.2.C** (cambridge-ia-groups:G1) Find the subgroup an element generates and list the subgroups of a cyclic group.
  - EK: In Z_n the element a generates the multiples of gcd(a, n), a subgroup of order n/gcd(a, n). Z_n has exactly one subgroup for each divisor of n.
  - Needs: AA-1.1.B
  - P1 · drills: aa-generated-subgroup, aa-cyclic-subgroup-count
- ● **AA-1.2.D** (cambridge-ia-groups:G2) Split a cyclic group into the cosets of a subgroup.
  - EK: The cosets of ⟨d⟩ in Z_n (d dividing n) are the residue classes modulo d: there are d of them, each of size n/d, and they partition the group.
  - Needs: AA-1.2.C
  - P1 · drills: aa-zn-coset-count, aa-coset-representative
- ● **AA-1.2.E** (cambridge-ia-groups:G1) Compute in a dihedral group with the relation between rotations and reflections.
  - EK: The symmetry group of a regular n-gon has n rotations and n reflections. With r a rotation by one step and s a reflection, s r s = r⁻¹, so s rᵏ s = r⁻ᵏ and every reflection has order 2.
  - Needs: AA-1.2.B
  - P1 · drills: aa-dihedral-relation, aa-dihedral-involutions
- ● **AA-1.2.F** (cambridge-ia-groups:G1, cambridge-ia-groups:G2) Decide whether two small groups are isomorphic by comparing invariants.
  - EK: Isomorphic groups have the same order, the same number of elements of each order, and are both abelian or both not. One mismatch is enough to tell two groups apart.
  - Needs: AA-1.1.D, AA-1.2.E
  - P1 · drills: aa-isomorphic-or-not, aa-isomorphism-invariants

## Unit 2 · Permutations

Big ideas: SYM

### 2.1 Cycles, sign and conjugacy



- ● **AA-2.1.A** (cambridge-ia-groups:G6) Compose permutations in cycle notation and find the order of a permutation.
  - EK: Disjoint cycles commute and the order of a permutation is the least common multiple of its cycle lengths. Products are applied right to left.
  - Needs: AA-2.2.B
  - P1 · drills: aa-perm-order, aa-perm-compose
- ● **AA-2.1.B** (cambridge-ia-groups:G6) Find the sign of a permutation and work with the alternating group.
  - EK: A cycle of length k is a product of k − 1 transpositions, so it is even when k is odd. The even permutations form A_n, of order n!/2.
  - Needs: AA-2.2.C
  - P1 · drills: aa-perm-sign, aa-alternating-order
- ● **AA-2.1.C** (cambridge-ia-groups:G6, cambridge-ia-groups:G3) Count conjugacy classes in a symmetric group and the size of a class.
  - EK: Two permutations are conjugate in S_n exactly when they have the same cycle type, so the classes are the partitions of n. A class with m_k cycles of length k has n!/Π(k^m_k · m_k!) elements.
  - Needs: AA-2.2.D, AA-1.1.C
  - P1 · drills: aa-sn-class-count, aa-sn-class-size

### 2.2 Permutations by hand



- ● **AA-2.2.A** (cambridge-ia-groups:G6) Turn a permutation written as a list of images into cycles.
  - EK: Start at 1, follow where each point is sent until you return, and repeat from the smallest point not yet reached. Fixed points are cycles of length 1.
  - Needs: AA-1.1.A
  - P1 · drills: aa-oneline-cycles, aa-oneline-order
- ● **AA-2.2.B** (cambridge-ia-groups:G6) Find powers and the inverse of a permutation.
  - EK: σᵏ moves each point k steps along its cycle, and σ⁻¹ runs each cycle backwards. A cycle of length m satisfies σᵐ = identity.
  - Needs: AA-2.2.A
  - P1 · drills: aa-perm-power, aa-perm-inverse
- ● **AA-2.2.C** (cambridge-ia-groups:G6) Write a permutation as a product of transpositions and count how many are needed.
  - EK: A cycle of length m is a product of m − 1 transpositions, so a permutation of n points with c cycles (fixed points included) needs n − c, and no fewer.
  - Needs: AA-2.1.A
  - P1 · drills: aa-transposition-count, aa-transposition-facts
- ● **AA-2.2.D** (cambridge-ia-groups:G6) Conjugate a permutation by relabelling its cycles.
  - EK: τστ⁻¹ has the same cycle shape as σ, with every entry a replaced by τ(a). This is why conjugacy classes in S_n are cycle types.
  - Needs: AA-2.1.A
  - P1 · drills: aa-conjugate-image, aa-conjugation-facts

## Unit 3 · Group actions

Big ideas: SYM, DIV

### 3.1 Orbits, stabilisers and counting



- ● **AA-3.1.A** (cambridge-ia-groups:G3, cambridge-ia-groups:G5) Use the orbit-stabiliser theorem to find the order of a symmetry group.
  - EK: |G| = |orbit| × |stabiliser|. The rotations of a cube move a face to any of 6 faces and 4 rotations fix a face, so there are 24.
  - Needs: AA-3.2.A, AA-1.1.C
  - P1 · drills: aa-orbit-stabiliser, aa-stabiliser-size
- ● **AA-3.1.B** (cambridge-ia-groups:G3) Count orbits with Burnside's lemma.
  - EK: The number of orbits is the average number of fixed points: (1/|G|) Σ |Fix(g)|. A rotation by r places of an n-bead ring fixes k^gcd(n, r) colourings.
  - Needs: AA-3.2.B, AA-3.1.A
  - P1 · drills: aa-necklaces, aa-burnside-average
- ● **AA-3.1.C** (cambridge-ia-groups:G3, cambridge-ib-grm:GR) Use centralisers, the class equation and Cauchy's theorem.
  - EK: The size of a conjugacy class is |G| divided by the size of the centraliser. The class equation forces a non-trivial centre in a p-group, and Cauchy: if a prime p divides |G| there is an element of order p.
  - Needs: AA-3.2.C, AA-2.1.C
  - P1 · drills: aa-centraliser-size, aa-class-equation-facts

### 3.2 Orbits by counting



- ● **AA-3.2.A** (cambridge-ia-groups:G3) Find the orbits of a small group acting on a set.
  - EK: The orbit of a point is everything the group can move it to; orbits partition the set. For the group generated by one permutation the orbits are its cycles.
  - Needs: AA-2.2.A
  - P1 · drills: aa-orbit-count, aa-orbit-size-divides
- ● **AA-3.2.B** (cambridge-ia-groups:G3) Count the colourings a symmetry fixes and apply Burnside to a polygon.
  - EK: A symmetry fixes a colouring exactly when each cycle of the symmetry is one colour, so it fixes k^(number of cycles) colourings. Averaging over rotations and reflections counts patterns up to turning over.
  - Needs: AA-3.2.A
  - P1 · drills: aa-fixed-colourings, aa-bracelets
- ● **AA-3.2.C** (cambridge-ia-groups:G3) Find the centre and the conjugacy classes of a dihedral group.
  - EK: In the symmetry group of a regular n-gon the centre is trivial for odd n and contains the half-turn for even n. There are (n + 3)/2 conjugacy classes for odd n and (n + 6)/2 for even n.
  - Needs: AA-1.2.E, AA-2.2.D
  - P1 · drills: aa-dihedral-centre, aa-dihedral-classes

## Unit 4 · Quotients and structure

Big ideas: DIV

### 4.1 Homomorphisms, abelian groups and Sylow



- ● **AA-4.1.A** (cambridge-ia-groups:G4, cambridge-ib-grm:GR) Apply the first isomorphism theorem and count homomorphisms between cyclic groups.
  - EK: The image of a homomorphism is isomorphic to G/ker, so |image| = |G|/|kernel|. A homomorphism from Z_m to Z_n is fixed by where 1 goes, and there are gcd(m, n) of them.
  - Needs: AA-4.2.C
  - P1 · drills: aa-image-size, aa-hom-count
- ● **AA-4.1.B** (cambridge-ib-grm:MO) Classify finite abelian groups of a given order and decide when a product is cyclic.
  - EK: Every finite abelian group is a product of cyclic groups of prime-power order. For n = Π p^a the number of abelian groups is Π (number of partitions of a). Z_m × Z_n is cyclic exactly when gcd(m, n) = 1.
  - Needs: AA-4.2.D
  - P1 · drills: aa-abelian-count, aa-product-max-order
- ● **AA-4.1.C** (cambridge-ib-grm:GR) Use the Sylow theorems to limit the number of Sylow subgroups.
  - EK: If |G| = p^a m with p not dividing m, the number of Sylow p-subgroups divides m and is 1 mod p. When that leaves only 1, the subgroup is normal and the group is not simple.
  - Needs: AA-3.1.C, AA-4.2.A, AA-4.1.B
  - P1 · drills: aa-sylow-options, aa-sylow-facts

### 4.2 Quotients and products of small groups



- ● **AA-4.2.A** (cambridge-ia-groups:G4) Decide whether a subgroup is normal.
  - EK: N is normal when gNg⁻¹ = N for every g, equivalently when left and right cosets agree. Every subgroup of an abelian group is normal, and so is every subgroup of index 2.
  - Needs: AA-1.2.D, AA-2.2.D
  - P1 · drills: aa-normal-or-not, aa-normal-facts
- ● **AA-4.2.B** (cambridge-ia-groups:G4) Compute in a quotient of a cyclic group.
  - EK: Z_n/⟨d⟩ is cyclic of order d. The coset of a has order d/gcd(a, d): the least k for which ka lands back in the subgroup.
  - Needs: AA-4.2.A
  - P1 · drills: aa-quotient-element-order, aa-quotient-order
- ● **AA-4.2.C** (cambridge-ia-groups:G4) Find the kernel and image of a concrete homomorphism.
  - EK: For x ↦ kx on Z_n the kernel has gcd(k, n) elements and the image n/gcd(k, n). The sign map on S_n has kernel A_n; the determinant on invertible matrices has kernel the matrices of determinant 1.
  - Needs: AA-4.2.B
  - P1 · drills: aa-kernel-size, aa-kernel-facts
- ● **AA-4.2.D** (cambridge-ib-grm:MO) Find orders of elements in a direct product.
  - EK: The order of (a, b) is the least common multiple of the orders of a and b. Counting elements of each order is the quickest way to tell products such as Z₂ × Z₄ and Z₈ apart.
  - Needs: AA-1.1.B
  - P1 · drills: aa-product-element-order, aa-product-count-order

## Unit 5 · Rings

Big ideas: DIV

### 5.1 Units, ideals and factorisation



- ● **AA-5.1.A** (cambridge-ib-grm:RI) Count units, zero divisors and idempotents in Z_n.
  - EK: In Z_n a non-zero residue is a unit if it is coprime to n and a zero divisor otherwise. Z_n has 2^k idempotents, where k is the number of distinct primes dividing n.
  - Needs: AA-1.2.A
  - P1 · drills: aa-zero-divisors, aa-idempotents
- ● **AA-5.1.B** (cambridge-ib-grm:RI) Decide whether a quotient ring is a field and count roots of a polynomial over Z_p.
  - EK: Z_n is a field exactly when n is prime, and F[x]/(f) is a field exactly when f is irreducible. Over a field a polynomial of degree d has at most d roots; over Z_n with n composite it can have more.
  - Needs: AA-5.2.C, AA-5.2.B
  - P2 · drills: aa-field-or-not, aa-roots-mod-n
- ● **AA-5.1.C** (cambridge-ib-grm:RI) Work with norms in the Gaussian integers and recognise failures of unique factorisation.
  - EK: N(a + bi) = a² + b² is multiplicative, so an element of prime norm is irreducible. Z[i] has unique factorisation; Z[√−5] does not, since 6 = 2 · 3 = (1 + √−5)(1 − √−5).
  - Needs: AA-5.1.B
  - P1 · drills: aa-gaussian-norm, aa-factorisation-facts

### 5.2 Ideals and polynomial arithmetic



- ● **AA-5.2.A** (cambridge-ib-grm:RI) Do arithmetic with polynomials whose coefficients are taken modulo a prime.
  - EK: Coefficients add and multiply modulo p. Because p divides the middle binomial coefficients, (x + 1)ᵖ = xᵖ + 1 in Z_p[x]: the 'freshman's dream' is true in characteristic p.
  - Needs: AA-5.1.A
  - P1 · drills: aa-binomial-mod-p, aa-char-p-facts
- ● **AA-5.2.B** (cambridge-ib-grm:RI) Combine ideals of the integers and count the ideals of Z_n.
  - EK: Every ideal of Z is (m) for some m. (a) + (b) = (gcd), (a) ∩ (b) = (lcm), and (a) contains (b) exactly when a divides b. The ideals of Z_n correspond to the divisors of n.
  - Needs: AA-5.1.A, NT-1.1.B
  - P1 · drills: aa-ideal-sum, aa-ideal-intersection
- ● **AA-5.2.C** (cambridge-ib-grm:RI) Use the remainder and factor theorems over Z_p.
  - EK: Dividing f(x) by x − a leaves the remainder f(a); so a is a root exactly when x − a is a factor. A quadratic or cubic over a field is irreducible exactly when it has no root.
  - Needs: AA-5.2.A
  - P1 · drills: aa-remainder-mod-p, aa-cubic-roots-mod-p

## Unit 6 · Fields and Galois theory (extension)

Big ideas: SYM, DIV

### 6.1 Extensions, finite fields and the Galois correspondence



- ● **AA-6.1.A** (cambridge-ii-galois-theory:E) Find the degree of a field extension and use the tower law.
  - EK: [K(α) : K] is the degree of the minimal polynomial of α over K, and degrees multiply up a tower: [M : K] = [M : L][L : K].
  - Needs: AA-5.1.B
  - P1 · drills: aa-extension-degree, aa-tower-law
- ● **AA-6.1.B** (cambridge-ii-galois-theory:F) Count the elements, subfields and irreducible polynomials of a finite field.
  - EK: There is exactly one field of each prime-power order pⁿ. Its non-zero elements form a cyclic group, its subfields are the fields of order p^d for d dividing n, and xᵖⁿ − x is the product of every monic irreducible over F_p whose degree divides n.
  - Needs: AA-6.1.A, AA-5.2.C
  - P1 · drills: aa-irreducible-count, aa-subfield-count
- ● **AA-6.1.C** (cambridge-ii-galois-theory:G) Find the order of a Galois group and read the Galois correspondence.
  - EK: For a Galois extension the group has order equal to the degree, and subgroups correspond to intermediate fields with inclusions reversed; a subfield is normal over the base exactly when its subgroup is normal. Q(ζ_n) has group the units modulo n, of order φ(n).
  - Needs: AA-6.1.B, AA-4.1.A
  - P1 · drills: aa-cyclotomic-degree, aa-galois-correspondence
- ● **AA-6.1.D** (cambridge-ii-galois-theory:S) Decide what can be constructed by ruler and compass or solved by radicals.
  - EK: A length is constructible only if its degree over Q is a power of 2, so a regular n-gon is constructible exactly when φ(n) is a power of 2. A polynomial is soluble by radicals exactly when its Galois group is soluble; S₅ is not.
  - Needs: AA-6.1.C, AA-4.1.C
  - P1 · drills: aa-constructible-polygon, aa-impossibility-facts
