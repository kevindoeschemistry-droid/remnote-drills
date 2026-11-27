"""Abstract Algebra, the intermediate steps (Nov 2026): 20 objectives that sit between the ones draft 1 jumped across.
Draft 1 went from "is this a group" to the Sylow theorems in 16 objectives. These are the small steps: one group at
a time (units modulo n, dihedral groups), permutations by hand, orbits by counting, quotients of Z_n, ideals of Z.
NEEDS wires every Abstract Algebra objective, old and new, so the path puts the small steps first.
Basis unchanged: the Cambridge Groups and Groups, Rings and Modules schedules."""
from math import gcd
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "aa-steps", "abstract-algebra", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
GP, PM, AC, QT, RG = "aa.groups", "aa.perms", "aa.actions", "aa.quotients", "aa.rings"
G = lambda *s: [f"cambridge-ia-groups:{x}" for x in s]
R = lambda *s: [f"cambridge-ib-grm:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def cyc(s):
    return "".join("(" + " ".join(c) + ")" for c in s.split("|"))


def order(a, n):
    k, r = 1, a % n
    while r != 1: r, k = r * a % n, k + 1
    return k


def lcm(a, b):
    return a * b // gcd(a, b)


def perm(c, n):
    f = {k: k for k in range(1, n + 1)}
    for part in c.split("|"):
        xs = [int(ch) for ch in part]
        for a, b in zip(xs, xs[1:] + xs[:1]): f[a] = b
    return f


def ncyc(f):
    seen, k = set(), 0
    for a in f:
        if a not in seen:
            k += 1
            while a not in seen: seen.add(a); a = f[a]
    return k


ONE = ["3 1 2 5 4", "2 3 4 1 5", "2 1 4 3 6 5", "4 3 2 1", "2 3 1 5 6 4", "5 4 3 2 1", "2 4 1 3"]
ONEF = [dict(enumerate([int(x) for x in s.split()], 1)) for s in ONE]


def olcm(f):
    seen, out = set(), 1
    for a in f:
        ln = 0
        while a not in seen: seen.add(a); a = f[a]; ln += 1
        if ln: out = lcm(out, ln)
    return out


TOPICS = {"1.2": "One group at a time", "2.2": "Permutations by hand", "3.2": "Orbits by counting", "4.2": "Quotients and products of small groups", "5.2": "Ideals and polynomial arithmetic"}
OBJS = [
 ("AA-1.2.A", G("G1"), "Compute in the group of units modulo n: products and inverses.", "The units modulo n are the residues coprime to n, multiplied modulo n. The identity is 1 and each unit has exactly one inverse, which is again a unit."),
 ("AA-1.2.B", G("G1", "G2"), "Find the order of an element of a multiplicative group by taking powers.", "The order of a is the least k ≥ 1 with a^k equal to the identity. The powers of a cycle with that period, so a^m is the identity exactly when the order divides m."),
 ("AA-1.2.C", G("G1"), "Find the subgroup an element generates and list the subgroups of a cyclic group.", "In Z_n the element a generates the multiples of gcd(a, n), a subgroup of order n/gcd(a, n). Z_n has exactly one subgroup for each divisor of n."),
 ("AA-1.2.D", G("G2"), "Split a cyclic group into the cosets of a subgroup.", "The cosets of ⟨d⟩ in Z_n (d dividing n) are the residue classes modulo d: there are d of them, each of size n/d, and they partition the group."),
 ("AA-1.2.E", G("G1"), "Compute in a dihedral group with the relation between rotations and reflections.", "The symmetry group of a regular n-gon has n rotations and n reflections. With r a rotation by one step and s a reflection, s r s = r⁻¹, so s rᵏ s = r⁻ᵏ and every reflection has order 2."),
 ("AA-1.2.F", G("G1", "G2"), "Decide whether two small groups are isomorphic by comparing invariants.", "Isomorphic groups have the same order, the same number of elements of each order, and are both abelian or both not. One mismatch is enough to tell two groups apart."),
 ("AA-2.2.A", G("G6"), "Turn a permutation written as a list of images into cycles.", "Start at 1, follow where each point is sent until you return, and repeat from the smallest point not yet reached. Fixed points are cycles of length 1."),
 ("AA-2.2.B", G("G6"), "Find powers and the inverse of a permutation.", "σᵏ moves each point k steps along its cycle, and σ⁻¹ runs each cycle backwards. A cycle of length m satisfies σᵐ = identity."),
 ("AA-2.2.C", G("G6"), "Write a permutation as a product of transpositions and count how many are needed.", "A cycle of length m is a product of m − 1 transpositions, so a permutation of n points with c cycles (fixed points included) needs n − c, and no fewer."),
 ("AA-2.2.D", G("G6"), "Conjugate a permutation by relabelling its cycles.", "τστ⁻¹ has the same cycle shape as σ, with every entry a replaced by τ(a). This is why conjugacy classes in S_n are cycle types."),
 ("AA-3.2.A", G("G3"), "Find the orbits of a small group acting on a set.", "The orbit of a point is everything the group can move it to; orbits partition the set. For the group generated by one permutation the orbits are its cycles."),
 ("AA-3.2.B", G("G3"), "Count the colourings a symmetry fixes and apply Burnside to a polygon.", "A symmetry fixes a colouring exactly when each cycle of the symmetry is one colour, so it fixes k^(number of cycles) colourings. Averaging over rotations and reflections counts patterns up to turning over."),
 ("AA-3.2.C", G("G3"), "Find the centre and the conjugacy classes of a dihedral group.", "In the symmetry group of a regular n-gon the centre is trivial for odd n and contains the half-turn for even n. There are (n + 3)/2 conjugacy classes for odd n and (n + 6)/2 for even n."),
 ("AA-4.2.A", G("G4"), "Decide whether a subgroup is normal.", "N is normal when gNg⁻¹ = N for every g, equivalently when left and right cosets agree. Every subgroup of an abelian group is normal, and so is every subgroup of index 2."),
 ("AA-4.2.B", G("G4"), "Compute in a quotient of a cyclic group.", "Z_n/⟨d⟩ is cyclic of order d. The coset of a has order d/gcd(a, d): the least k for which ka lands back in the subgroup."),
 ("AA-4.2.C", G("G4"), "Find the kernel and image of a concrete homomorphism.", "For x ↦ kx on Z_n the kernel has gcd(k, n) elements and the image n/gcd(k, n). The sign map on S_n has kernel A_n; the determinant on invertible matrices has kernel the matrices of determinant 1."),
 ("AA-4.2.D", R("MO"), "Find orders of elements in a direct product.", "The order of (a, b) is the least common multiple of the orders of a and b. Counting elements of each order is the quickest way to tell products such as Z₂ × Z₄ and Z₈ apart."),
 ("AA-5.2.A", R("RI"), "Do arithmetic with polynomials whose coefficients are taken modulo a prime.", "Coefficients add and multiply modulo p. Because p divides the middle binomial coefficients, (x + 1)ᵖ = xᵖ + 1 in Z_p[x]: the 'freshman's dream' is true in characteristic p."),
 ("AA-5.2.B", R("RI"), "Combine ideals of the integers and count the ideals of Z_n.", "Every ideal of Z is (m) for some m. (a) + (b) = (gcd), (a) ∩ (b) = (lcm), and (a) contains (b) exactly when a divides b. The ideals of Z_n correspond to the divisors of n."),
 ("AA-5.2.C", R("RI"), "Use the remainder and factor theorems over Z_p.", "Dividing f(x) by x − a leaves the remainder f(a); so a is a root exactly when x − a is a factor. A quadratic or cubic over a field is irreducible exactly when it has no root."),
]
ADD = [
 ("AA-1.2.A", N("aa-unit-product", GP, "In the group of units modulo {{kn}}, compute {{ka}} · {{kb}}.", "mod(ka*kb, kn)", "pm_powmod(ka*kb, 1, kn)",
    "Multiply as integers and reduce modulo n. The product of two units is always a unit, which is closure", tex="product",
    cases=[{"kn": 9, "ka": 4, "kb": 7}, {"kn": 10, "ka": 3, "kb": 7}, {"kn": 15, "ka": 7, "kb": 8}, {"kn": 14, "ka": 5, "kb": 11}, {"kn": 16, "ka": 5, "kb": 7}, {"kn": 20, "ka": 9, "kb": 13}])),
 ("AA-1.2.A", N("aa-unit-inverse", GP, "In the group of units modulo {{kn}}, find the inverse of {{ka}}.", "kans", "pm_inv(ka, kn)",
    "Look for the unit b with ab ≡ 1. In a small group, trying the units in turn is quickest", tex="a^{-1}",
    cases=[{"kn": n, "ka": a, "kans": pow(a, -1, n)} for n, a in [(9, 2), (10, 3), (14, 3), (15, 2), (16, 3), (20, 7), (9, 5)]])),
 ("AA-1.2.B", N("aa-unit-order", GP, "What is the order of {{ka}} in the group of units modulo {{kn}}?", "kans", "pm_order(ka, kn)",
    "Take powers of a modulo n until you reach 1. The answer must divide the number of units", tex="order",
    cases=[{"kn": n, "ka": a, "kans": order(a, n)} for n, a in [(9, 2), (9, 4), (10, 3), (15, 2), (15, 4), (16, 3), (20, 3), (14, 3)]])),
 ("AA-1.2.B", N("aa-power-reduce", GP, "An element g of a group has order {{ko}}. g^{{kk}} equals g^m for which m between 0 and {{ko}} − 1?", "mod(kk, ko)", "kk - ko*floor(kk/ko)",
    "Powers of g repeat with period equal to its order, so only the exponent modulo the order matters", tex="m",
    cases=[{"ko": 6, "kk": 100}, {"ko": 7, "kk": 50}, {"ko": 12, "kk": 77}, {"ko": 5, "kk": 2024}, {"ko": 8, "kk": 99}])),
 ("AA-1.2.C", N("aa-generated-subgroup", GP, "How many elements has the subgroup of Z_{{kn}} generated by {{ka}}?", "kn/gcd(ka, kn)", "pm_zn_count_order(kn, kn/gcd(ka, kn))/pm_phi(kn/gcd(ka, kn))*kn/gcd(ka, kn)",
    "The multiples of a are the multiples of gcd(a, n), and there are n/gcd(a, n) of them", tex="|\\langle a\\rangle|",
    cases=[{"kn": 12, "ka": 8}, {"kn": 18, "ka": 12}, {"kn": 20, "ka": 6}, {"kn": 30, "ka": 25}, {"kn": 24, "ka": 9}, {"kn": 15, "ka": 10}])),
 ("AA-1.2.C", N("aa-cyclic-subgroup-count", GP, "How many subgroups has the cyclic group Z_{{kn}}?", "kans", "pm_ndiv(kn)",
    "Exactly one subgroup for each divisor of n, so count the divisors", tex="subgroups",
    cases=[{"kn": 12, "kans": 6}, {"kn": 16, "kans": 5}, {"kn": 30, "kans": 8}, {"kn": 36, "kans": 9}, {"kn": 17, "kans": 2}, {"kn": 24, "kans": 8}])),
 ("AA-1.2.D", N("aa-zn-coset-count", GP, "How many cosets has the subgroup generated by {{kd}} in Z_{{kn}}?", "kd", "kn/pm_zn_count_order(kn, 1)/(kn/gcd(kd, kn))",
    "The subgroup ⟨d⟩ has n/d elements when d divides n, so it has n ÷ (n/d) = d cosets: the residue classes modulo d", tex="cosets",
    cases=[{"kn": 12, "kd": 4}, {"kn": 18, "kd": 6}, {"kn": 20, "kd": 5}, {"kn": 24, "kd": 8}, {"kn": 30, "kd": 3}])),
 ("AA-1.2.D", N("aa-coset-representative", GP, "In Z_{{kn}}, which is the smallest non-negative element of the coset {{kx}} + ⟨{{kd}}⟩?", "mod(kx, kd)", "pm_bisect_cover(kn, kd, kx)",
    "The coset is everything congruent to x modulo d, so its least member is x reduced modulo d", tex="element",
    cases=[{"kn": 12, "kd": 4, "kx": 7}, {"kn": 18, "kd": 6, "kx": 17}, {"kn": 20, "kd": 5, "kx": 13}, {"kn": 24, "kd": 8, "kx": 21}, {"kn": 30, "kd": 3, "kx": 26}])),
 ("AA-1.2.E", N("aa-dihedral-relation", GP, "In the symmetry group of a regular {{kn}}-gon, r is a rotation by one step and s a reflection. s r^{{kk}} s = r^j for which j between 0 and {{km}}?", "kn - kk", "pm_dihedral_srs(kn, kk)",
    "Conjugating a rotation by a reflection reverses it: s rᵏ s = r⁻ᵏ = r^(n−k)", tex="j",
    cases=[{"kn": 5, "kk": 2, "km": 4}, {"kn": 6, "kk": 1, "km": 5}, {"kn": 8, "kk": 3, "km": 7}, {"kn": 7, "kk": 4, "km": 6}, {"kn": 10, "kk": 3, "km": 9}])),
 ("AA-1.2.E", N("aa-dihedral-involutions", GP, "How many elements of order 2 are there in the symmetry group of a regular {{kn}}-gon?", "kans", "pm_dihedral_order2(kn)",
    "All n reflections have order 2, and when n is even the half-turn does too", tex="elements",
    cases=[{"kn": 3, "kans": 3}, {"kn": 4, "kans": 5}, {"kn": 5, "kans": 5}, {"kn": 6, "kans": 7}, {"kn": 7, "kans": 7}, {"kn": 8, "kans": 9}])),
 ("AA-1.2.F", Q("aa-isomorphic-or-not", GP, "Are {{ga}} and {{gb}} isomorphic?", pace="recall", cases=[
    {"ga": "Z₄", "gb": "Z₂ × Z₂", "kc": 1}, {"ga": "Z₆", "gb": "Z₂ × Z₃", "kc": 0}, {"ga": "S₃", "gb": "Z₆", "kc": 1}, {"ga": "S₃", "gb": "the symmetry group of a triangle", "kc": 0},
    {"ga": "Z₈", "gb": "Z₂ × Z₄", "kc": 1}, {"ga": "the units modulo 8", "gb": "Z₂ × Z₂", "kc": 0}, {"ga": "the units modulo 5", "gb": "Z₄", "kc": 0},
    {"ga": "the symmetry group of a square", "gb": "the quaternion group", "kc": 1}, {"ga": "Z₁₂", "gb": "Z₃ × Z₄", "kc": 0}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Compare orders of elements. Z₄ has an element of order 4 and Z₂ × Z₂ does not; the square's group has five elements of order 2 and the quaternion group only one; a product Z_m × Z_n is cyclic exactly when m and n are coprime")),
 ("AA-1.2.F", F("aa-isomorphism-invariants", GP, [
    ("Which of these is NOT preserved by every isomorphism?", "The names of the elements", "The order of the group", "Whether the group is abelian", "The number of elements of order 2"),
    ("Up to isomorphism, how many groups of order 4 are there?", "2", "1", "3", "4"),
    ("Up to isomorphism, how many groups of order 6 are there?", "2", "1", "3", "6"),
    ("The smallest non-abelian group has order:", "6", "4", "8", "5"),
    ("Two cyclic groups are isomorphic exactly when they have the same:", "Order", "Generator", "Number of subgroups only", "Identity")],
    "To prove two groups isomorphic you must give the map; to prove them different one invariant suffices")),
 ("AA-2.2.A", N("aa-oneline-cycles", PM, "The permutation σ sends 1, 2, 3, … in turn to {{sh}}. How many cycles does it have, counting fixed points?", "kans", "pm_oneline_cycles(ol)",
    "Trace 1 until it returns, then start again from the smallest unused point", tex="cycles",
    cases=[{"ol": s, "sh": s.replace(" ", ", "), "kans": ncyc(f)} for s, f in zip(ONE, ONEF)])),
 ("AA-2.2.A", N("aa-oneline-order", PM, "The permutation σ sends 1, 2, 3, … in turn to {{sh}}. What is its order?", "kans", "pm_oneline_order(ol)",
    "Write it in cycles first; the order is the least common multiple of the cycle lengths", tex="order",
    cases=[{"ol": s, "sh": s.replace(" ", ", "), "kans": olcm(f)} for s, f in zip(ONE, ONEF)])),
 ("AA-2.2.B", N("aa-perm-power", PM, "For σ = {{sh}}, where does σ^{{kk}} send {{kx}}?", "kans", "pm_perm_power_image(cy, kk, kx)",
    "Move k steps round the cycle containing the point, reducing k modulo that cycle's length first", tex="image",
    cases=[{"cy": c, "sh": cyc(c), "kk": k, "kx": x, "kans": y} for c, k, x, y in [("12345", 2, 1, 3), ("12345", 7, 4, 1), ("123|45", 3, 4, 5), ("1234", 3, 2, 1), ("123|4567", 5, 5, 6), ("123456", 4, 5, 3)]])),
 ("AA-2.2.B", N("aa-perm-inverse", PM, "For σ = {{sh}}, where does σ⁻¹ send {{kx}}?", "kans", "pm_perm_inverse_image(cy, kx)",
    "Read the cycle backwards: σ⁻¹ sends each point to the one written before it", tex="image",
    cases=[{"cy": c, "sh": cyc(c), "kx": x, "kans": y} for c, x, y in [("12345", 1, 5), ("123|45", 2, 1), ("1342", 4, 3), ("15|234", 3, 2), ("123456", 4, 3), ("1432", 1, 2)]])),
 ("AA-2.2.C", N("aa-transposition-count", PM, "What is the smallest number of transpositions whose product is {{sh}} in S_{{kn}}?", "kans", "pm_perm_transpositions(cy, kn)",
    "Each cycle of length m costs m − 1 transpositions, so the total is n minus the number of cycles (fixed points count as cycles)", tex="transpositions",
    cases=[{"cy": c, "sh": cyc(c), "kn": n, "kans": n - ncyc(perm(c, n))} for c, n in [("123|45", 5), ("1234", 4), ("12|34", 4), ("12345", 6), ("123|456", 6), ("12|34|56", 7)]])),
 ("AA-2.2.C", F("aa-transposition-facts", PM, [
    ("The 3-cycle (1 2 3) equals which product of transpositions (applied right to left)?", "(1 3)(1 2)", "(1 2)(1 2)", "(1 2)(3 1)(2 3)(1 2)", "(2 3)"),
    ("A permutation can be written with 4 transpositions. It can also be written with:", "6, but never 5", "5", "3", "Any number at least 4"),
    ("A cycle of even length is:", "An odd permutation", "An even permutation", "The identity", "Not a product of transpositions"),
    ("The transpositions (1 2), (2 3), …, (n − 1 n) of neighbours generate:", "All of S_n", "Only A_n", "A cyclic group", "Only the even permutations")],
    "The number of transpositions is not unique but its parity is, which is what makes the sign well defined")),
 ("AA-2.2.D", N("aa-conjugate-image", PM, "Let σ = {{s1}} and τ = {{s2}}. Where does τστ⁻¹ send {{kx}}?", "kans", "pm_conj_image(c1, c2, kx)",
    "Relabel σ's cycle through τ: (a b c) becomes (τ(a) τ(b) τ(c)); then read off the image", tex="image",
    cases=[{"c1": a, "c2": b, "s1": cyc(a), "s2": cyc(b), "kx": x, "kans": y} for a, b, x, y in [
        ("123", "14", 4, 2), ("123", "14", 2, 3), ("12", "123", 2, 3), ("1234", "13", 3, 2), ("123", "24|35", 4, 5), ("12|34", "23", 1, 3)]])),
 ("AA-2.2.D", F("aa-conjugation-facts", PM, [
    ("Conjugating (1 2 3) by τ = (1 4) gives:", "(4 2 3)", "(1 2 3)", "(1 4)(2 3)", "(1 2 4)"),
    ("Two permutations in S_n are conjugate exactly when they have the same:", "Cycle type", "Order", "Sign", "Number of fixed points"),
    ("In S₄, (1 2)(3 4) and (1 2 3 4) both have even order but are not conjugate because:", "Their cycle types differ", "Their signs agree", "One is in A₄", "Their orders differ by a factor of 2 only"),
    ("An element is conjugate only to itself exactly when it:", "Commutes with everything", "Is the identity", "Has order 2", "Is a transposition")],
    "Conjugation is a change of labels, so it cannot change the shape of the cycles")),
 ("AA-3.2.A", N("aa-orbit-count", AC, "The group generated by σ = {{sh}} acts on the points 1, …, {{kn}}. How many orbits are there?", "kans", "pm_perm_orbits(cy, kn)",
    "The orbits of ⟨σ⟩ are the cycles of σ, and each point σ leaves alone is an orbit by itself", tex="orbits",
    cases=[{"cy": c, "sh": cyc(c), "kn": n, "kans": ncyc(perm(c, n))} for c, n in [("123|45", 7), ("1234", 6), ("12|34", 4), ("12345", 5), ("123|456", 8), ("12", 5)]])),
 ("AA-3.2.A", N("aa-orbit-size-divides", AC, "A group of order {{kg}} acts on a set of {{ks}} points with exactly two orbits, one of size {{ka}}. What is the size of the stabiliser of a point in the other orbit?", "kg/(ks - ka)", "solve(Eq(Symbol('m')*(ks - ka), kg), Symbol('m'))[0]",
    "Orbits partition the set, so the other orbit has the remaining points; then stabiliser = group order ÷ orbit size", tex="|\\mathrm{Stab}|",
    cases=[{"kg": 12, "ks": 7, "ka": 3}, {"kg": 24, "ks": 14, "ka": 6}, {"kg": 20, "ks": 9, "ka": 4}, {"kg": 30, "ks": 16, "ka": 6}, {"kg": 8, "ks": 6, "ka": 2}])),
 ("AA-3.2.B", N("aa-fixed-colourings", AC, "A symmetry permutes the {{kn}} corners of a polygon in {{kc}} cycles. How many colourings of the corners with {{kk}} colours does it leave unchanged?", "kk^kc", "Integer(kk)**kc",
    "Each cycle must be a single colour and the cycles are independent, so there are k^(number of cycles) fixed colourings", tex="colourings",
    cases=[{"kn": 4, "kc": 1, "kk": 3}, {"kn": 4, "kc": 2, "kk": 3}, {"kn": 6, "kc": 3, "kk": 2}, {"kn": 4, "kc": 3, "kk": 2}, {"kn": 6, "kc": 2, "kk": 3}, {"kn": 5, "kc": 3, "kk": 2}])),
 ("AA-3.2.B", N("aa-bracelets", AC, "How many different bracelets of {{kn}} beads can be made with {{kk}} colours, if turning the bracelet round or over gives the same bracelet?", "kans", "pm_bracelets(kn, kk)",
    "Average the fixed colourings over all 2n symmetries of the n-gon: the n rotations, then the n reflections", tex="bracelets",
    cases=[{"kn": 3, "kk": 2, "kans": 4}, {"kn": 4, "kk": 2, "kans": 6}, {"kn": 5, "kk": 2, "kans": 8}, {"kn": 6, "kk": 2, "kans": 13}, {"kn": 4, "kk": 3, "kans": 21}, {"kn": 3, "kk": 3, "kans": 10}])),
 ("AA-3.2.C", N("aa-dihedral-centre", AC, "How many elements are in the centre of the symmetry group of a regular {{kn}}-gon?", "kans", "pm_dihedral_center(kn)",
    "A rotation commutes with every reflection only if it equals its own inverse: the identity, and the half-turn when n is even", tex="|Z(G)|",
    cases=[{"kn": 3, "kans": 1}, {"kn": 4, "kans": 2}, {"kn": 5, "kans": 1}, {"kn": 6, "kans": 2}, {"kn": 7, "kans": 1}, {"kn": 8, "kans": 2}])),
 ("AA-3.2.C", N("aa-dihedral-classes", AC, "How many conjugacy classes has the symmetry group of a regular {{kn}}-gon?", "kans", "pm_dihedral_classes(kn)",
    "Rotations pair up with their inverses; the reflections form one class when n is odd and two when n is even", tex="classes",
    cases=[{"kn": 3, "kans": 3}, {"kn": 4, "kans": 5}, {"kn": 5, "kans": 4}, {"kn": 6, "kans": 6}, {"kn": 8, "kans": 7}])),
 ("AA-4.2.A", Q("aa-normal-or-not", QT, "Is {{sg}} a normal subgroup of {{gp}}?", pace="recall", cases=[
    {"sg": "A₃", "gp": "S₃", "kc": 0}, {"sg": "{e, (1 2)}", "gp": "S₃", "kc": 1}, {"sg": "the rotations", "gp": "the symmetry group of a square", "kc": 0},
    {"sg": "{e, one reflection}", "gp": "the symmetry group of a square", "kc": 1}, {"sg": "the even integers", "gp": "the integers under addition", "kc": 0},
    {"sg": "matrices of determinant 1", "gp": "all invertible 2×2 real matrices", "kc": 0}, {"sg": "the centre", "gp": "any group", "kc": 0}, {"sg": "{e, (1 2)(3 4)}", "gp": "S₄", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Index 2, kernels and centres are always normal. A subgroup generated by one reflection or one transposition is moved by conjugation to another of the same kind")),
 ("AA-4.2.A", F("aa-normal-facts", QT, [
    ("A subgroup of index 2 is always:", "Normal", "Cyclic", "Abelian", "The centre"),
    ("The kernel of a group homomorphism is always:", "A normal subgroup", "Trivial", "Cyclic", "The whole group"),
    ("In an abelian group, which subgroups are normal?", "All of them", "Only the trivial ones", "Only those of prime order", "None"),
    ("Cosets of a subgroup N can be multiplied as (aN)(bN) = abN consistently exactly when N is:", "Normal", "Finite", "Cyclic", "Abelian")],
    "Normality is exactly what makes the set of cosets into a group")),
 ("AA-4.2.B", N("aa-quotient-element-order", QT, "In the quotient group Z_{{kn}}/⟨{{kd}}⟩, what is the order of the coset of {{ka}}?", "kd/gcd(ka, kd)", "pm_quotient_order(ka, kd, kn)",
    "The quotient is Z_d in disguise, so the coset of a has the order of a in Z_d", tex="order",
    cases=[{"kn": 12, "kd": 4, "ka": 2}, {"kn": 12, "kd": 6, "ka": 4}, {"kn": 24, "kd": 8, "ka": 6}, {"kn": 30, "kd": 10, "ka": 4}, {"kn": 18, "kd": 9, "ka": 6}, {"kn": 20, "kd": 5, "ka": 3}])),
 ("AA-4.2.B", N("aa-quotient-order", QT, "G has order {{kg}} and its centre has order {{kz}}. What is the order of G/Z(G)?", "kg/kz", "solve(Eq(Symbol('m')*kz, kg), Symbol('m'))[0]",
    "The quotient has one element per coset. If G/Z(G) were cyclic the group would be abelian, so this order is never a prime", tex="|G/Z|",
    cases=[{"kg": 8, "kz": 2}, {"kg": 12, "kz": 2}, {"kg": 27, "kz": 3}, {"kg": 16, "kz": 4}, {"kg": 24, "kz": 4}])),
 ("AA-4.2.C", N("aa-kernel-size", QT, "The map x ↦ {{kk}}x is a homomorphism from Z_{{kn}} to itself. How many elements has its kernel?", "gcd(kk, kn)", "pm_kernel_size(kk, kn)",
    "kx ≡ 0 (mod n) has gcd(k, n) solutions; the image then has n/gcd(k, n) elements", tex="|\\ker|",
    cases=[{"kn": 12, "kk": 4}, {"kn": 12, "kk": 5}, {"kn": 18, "kk": 6}, {"kn": 20, "kk": 8}, {"kn": 30, "kk": 12}, {"kn": 15, "kk": 10}])),
 ("AA-4.2.C", F("aa-kernel-facts", QT, [
    ("The sign map from S_n to {1, −1} has kernel:", "A_n", "The transpositions", "S_(n−1)", "The identity only"),
    ("The determinant map from invertible n×n real matrices to the non-zero reals has kernel:", "Matrices of determinant 1", "Diagonal matrices", "Orthogonal matrices", "The identity only"),
    ("A homomorphism is injective exactly when its kernel is:", "Trivial", "Normal", "The whole group", "Cyclic"),
    ("The map from the integers to Z_n sending x to x mod n has kernel:", "The multiples of n", "The units modulo n", "{0}", "The integers coprime to n"),
    ("The map x ↦ e^(ix) from the real numbers under addition to the unit circle has kernel:", "The integer multiples of 2π", "{0}", "The integers", "The rationals")],
    "Every quotient you meet in practice is the image of a homomorphism, and the kernel says what was collapsed")),
 ("AA-4.2.D", N("aa-product-element-order", QT, "What is the order of ({{ka}}, {{kb}}) in Z_{{km}} × Z_{{kn}}?", "lcm(km/gcd(ka, km), kn/gcd(kb, kn))", "lcm(lcm(ka, km)/ka, lcm(kb, kn)/kb)",
    "Find the order of each coordinate in its own group and take the least common multiple", tex="order",
    cases=[{"km": 4, "kn": 6, "ka": 2, "kb": 3}, {"km": 6, "kn": 10, "ka": 2, "kb": 5}, {"km": 12, "kn": 8, "ka": 3, "kb": 2}, {"km": 9, "kn": 6, "ka": 3, "kb": 4}, {"km": 10, "kn": 15, "ka": 4, "kb": 6}])),
 ("AA-4.2.D", N("aa-product-count-order", QT, "How many elements of order {{kd}} are there in Z_{{km}} × Z_{{kn}}?", "kans", "pm_prod_count_order(km, kn, kd)",
    "List the possible pairs of coordinate orders whose least common multiple is d and count the elements for each", tex="elements",
    cases=[{"km": 2, "kn": 4, "kd": 2, "kans": 3}, {"km": 2, "kn": 4, "kd": 4, "kans": 4}, {"km": 2, "kn": 2, "kd": 2, "kans": 3}, {"km": 3, "kn": 3, "kd": 3, "kans": 8}, {"km": 2, "kn": 6, "kd": 2, "kans": 3}, {"km": 4, "kn": 4, "kd": 4, "kans": 12}])),
 ("AA-5.2.A", N("aa-binomial-mod-p", RG, "What is the coefficient of x^{{kk}} in (x + 1)^{{kn}} when coefficients are reduced modulo {{kp}}?", "mod(combinations(kn, kk), kp)", "pm_binom_coeff(1, 1, kn, kk) % kp",
    "Take the ordinary binomial coefficient and reduce it. When n = p every middle coefficient is divisible by p, so (x + 1)ᵖ = xᵖ + 1", tex="coefficient",
    cases=[{"kn": 4, "kk": 2, "kp": 5}, {"kn": 6, "kk": 3, "kp": 7}, {"kn": 5, "kk": 2, "kp": 3}, {"kn": 6, "kk": 2, "kp": 2}, {"kn": 4, "kk": 1, "kp": 3}, {"kn": 8, "kk": 4, "kp": 3}])),
 ("AA-5.2.A", F("aa-char-p-facts", RG, [
    ("In Z₅[x], (x + 1)⁵ equals:", "x⁵ + 1", "x⁵ + 5x + 1", "x⁵", "(x + 1)"),
    ("In Z₂[x], x² + 1 factors as:", "(x + 1)²", "It is irreducible", "(x + 1)(x − 1) with distinct factors", "x(x + 1)"),
    ("A field in which 1 + 1 + … + 1 (p times) = 0 is said to have:", "Characteristic p", "Order p", "Degree p", "p elements exactly"),
    ("In Z₃[x], the polynomial x² + 1 has how many roots?", "None", "One", "Two", "Three")],
    "Reducing coefficients modulo p changes which polynomials factor: x² + 1 is irreducible over Z₃ but a perfect square over Z₂")),
 ("AA-5.2.B", N("aa-ideal-sum", RG, "In the integers, the ideal ({{ka}}) + ({{kb}}) equals (m) for which positive m?", "gcd(ka, kb)", "ka*kb/lcm(ka, kb)",
    "The sum of two ideals is everything of the form ax + by, which by Bezout is exactly the multiples of the gcd", tex="m",
    cases=[{"ka": 12, "kb": 18}, {"ka": 20, "kb": 30}, {"ka": 14, "kb": 35}, {"ka": 9, "kb": 16}, {"ka": 24, "kb": 36}])),
 ("AA-5.2.B", N("aa-ideal-intersection", RG, "In the integers, the ideal ({{ka}}) ∩ ({{kb}}) equals (m) for which positive m?", "lcm(ka, kb)", "ka*kb/gcd(ka, kb)",
    "A number is in both ideals when it is a multiple of both generators, that is a multiple of their least common multiple", tex="m",
    cases=[{"ka": 4, "kb": 6}, {"ka": 10, "kb": 15}, {"ka": 8, "kb": 12}, {"ka": 9, "kb": 6}, {"ka": 14, "kb": 21}])),
 ("AA-5.2.C", N("aa-remainder-mod-p", RG, "Find the remainder when x³ + {{ka}}x + {{kb}} is divided by x − {{kr}} in Z_{{kp}}[x].", "mod(kr^3 + ka*kr + kb, kp)", "pm_powmod(kr**3 + ka*kr + kb, 1, kp)",
    "By the remainder theorem the remainder is the value of the polynomial at x = r, reduced modulo p", tex="remainder",
    cases=[{"ka": 2, "kb": 1, "kr": 2, "kp": 5}, {"ka": 1, "kb": 3, "kr": 3, "kp": 7}, {"ka": 4, "kb": 2, "kr": 1, "kp": 5}, {"ka": 3, "kb": 5, "kr": 2, "kp": 11}, {"ka": 2, "kb": 2, "kr": 4, "kp": 7}])),
 ("AA-5.2.C", N("aa-cubic-roots-mod-p", RG, "How many roots has x³ + {{ka}}x + {{kb}} in Z_{{kp}}?", "kans", "pm_poly_roots_mod(cf, kp)",
    "Substitute every residue. A cubic with no root over a field has no linear factor, so it is irreducible", tex="roots",
    cases=[{"ka": a, "kb": b, "kp": p, "cf": f"{b},{a},0,1", "kans": sum(1 for x in range(p) if (x**3 + a*x + b) % p == 0)} for a, b, p in [(1, 1, 3), (2, 2, 5), (1, 2, 5), (3, 1, 7), (1, 2, 3), (4, 1, 5), (2, 3, 7), (1, 3, 5), (6, 6, 7), (2, 1, 3)] if any((x**3 + a*x + b) % p == 0 for x in range(p))])),
]
NEEDS = {
 "AA-1.1.A": [], "AA-1.2.A": ["AA-1.1.A", "NT-2.1.A"], "AA-1.2.B": ["AA-1.2.A"], "AA-1.1.B": ["AA-1.2.B"], "AA-1.2.C": ["AA-1.1.B"],
 "AA-1.2.D": ["AA-1.2.C"], "AA-1.1.C": ["AA-1.2.D"], "AA-1.1.D": ["AA-1.2.B", "NT-2.1.B"], "AA-1.2.E": ["AA-1.2.B"], "AA-1.2.F": ["AA-1.1.D", "AA-1.2.E"],
 "AA-2.2.A": ["AA-1.1.A"], "AA-2.2.B": ["AA-2.2.A"], "AA-2.1.A": ["AA-2.2.B"], "AA-2.2.C": ["AA-2.1.A"], "AA-2.1.B": ["AA-2.2.C"],
 "AA-2.2.D": ["AA-2.1.A"], "AA-2.1.C": ["AA-2.2.D", "AA-1.1.C"],
 "AA-3.2.A": ["AA-2.2.A"], "AA-3.1.A": ["AA-3.2.A", "AA-1.1.C"], "AA-3.2.B": ["AA-3.2.A"], "AA-3.1.B": ["AA-3.2.B", "AA-3.1.A"],
 "AA-3.2.C": ["AA-1.2.E", "AA-2.2.D"], "AA-3.1.C": ["AA-3.2.C", "AA-2.1.C"],
 "AA-4.2.A": ["AA-1.2.D", "AA-2.2.D"], "AA-4.2.B": ["AA-4.2.A"], "AA-4.2.C": ["AA-4.2.B"], "AA-4.1.A": ["AA-4.2.C"], "AA-4.2.D": ["AA-1.1.B"],
 "AA-4.1.B": ["AA-4.2.D"], "AA-4.1.C": ["AA-3.1.C", "AA-4.2.A", "AA-4.1.B"],
 "AA-5.1.A": ["AA-1.2.A"], "AA-5.2.B": ["AA-5.1.A", "NT-1.1.B"], "AA-5.2.A": ["AA-5.1.A"], "AA-5.2.C": ["AA-5.2.A"], "AA-5.1.B": ["AA-5.2.C", "AA-5.2.B"], "AA-5.1.C": ["AA-5.1.B"],
 "AA-6.1.A": ["AA-5.1.B"], "AA-6.1.B": ["AA-6.1.A", "AA-5.2.C"], "AA-6.1.C": ["AA-6.1.B", "AA-4.1.A"], "AA-6.1.D": ["AA-6.1.C", "AA-4.1.C"],
}
NEEDS = {k: v for k, v in NEEDS.items() if v}
