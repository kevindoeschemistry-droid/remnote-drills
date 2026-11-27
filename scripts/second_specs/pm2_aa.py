"""Abstract Algebra unit 6 (Nov 2026): field extensions, finite fields and Galois theory, on the Cambridge Part II
Galois Theory schedule (read through an extraction of the 2026-27 Schedules)."""
from math import gcd
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "aa-fields", "abstract-algebra", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
FD = "aa.fields"
B = ["cambridge-ii-galois-theory:E", "cambridge-ii-galois-theory:F", "cambridge-ii-galois-theory:G", "cambridge-ii-galois-theory:S"]
E, FF, G, S = ([x] for x in B)


def F(name, rows, explain):
    return Q(name, FD, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, FD, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def irr(p, d):  # necklace formula: (1/d) sum over e | d of mu(d/e) p^e
    mu = lambda m: 0 if any(m % (q * q) == 0 for q in range(2, m + 1)) else (-1) ** sum(1 for q in range(2, m + 1) if m % q == 0 and all(q % r for r in range(2, q)))  # noqa: E731
    return sum(mu(d // e) * p ** e for e in range(1, d + 1) if d % e == 0) // d


UNITS = {"6": ("fields", "Fields and Galois theory", ["SYM", "DIV"], B)}
TOPICS = {"6.1": "Extensions, finite fields and the Galois correspondence"}
OBJS = [
 ("AA-6.1.A", E, "Find the degree of a field extension and use the tower law.",
  "[K(α) : K] is the degree of the minimal polynomial of α over K, and degrees multiply up a tower: [M : K] = [M : L][L : K]."),
 ("AA-6.1.B", FF, "Count the elements, subfields and irreducible polynomials of a finite field.",
  "There is exactly one field of each prime-power order pⁿ. Its non-zero elements form a cyclic group, its subfields are the fields of order p^d for d dividing n, and xᵖⁿ − x is the product of every monic irreducible over F_p whose degree divides n."),
 ("AA-6.1.C", G, "Find the order of a Galois group and read the Galois correspondence.",
  "For a Galois extension the group has order equal to the degree, and subgroups correspond to intermediate fields with inclusions reversed; a subfield is normal over the base exactly when its subgroup is normal. Q(ζ_n) has group the units modulo n, of order φ(n)."),
 ("AA-6.1.D", S, "Decide what can be constructed by ruler and compass or solved by radicals.",
  "A length is constructible only if its degree over Q is a power of 2, so a regular n-gon is constructible exactly when φ(n) is a power of 2. A polynomial is soluble by radicals exactly when its Galois group is soluble; S₅ is not."),
]
ADD = [
 ("AA-6.1.A", N("aa-extension-degree", "Find the degree of the field extension Q({{sh}}) over Q.", "kans", "pm_minpoly_deg(py)",
    "Find the minimal polynomial of a generator, or build the field in steps and multiply the degrees with the tower law", tex="[K:\\mathbb{Q}]",
    cases=[{"sh": "√2 + √3", "py": "sqrt(2)+sqrt(3)", "kans": 4}, {"sh": "∛2", "py": "cbrt(2)", "kans": 3}, {"sh": "⁴√2", "py": "root(2,4)", "kans": 4},
           {"sh": "√2 + i", "py": "sqrt(2)+I", "kans": 4}, {"sh": "√(1 + √2)", "py": "sqrt(1+sqrt(2))", "kans": 4}, {"sh": "cos(2π/7)", "py": "cos(2*pi/7)", "kans": 3},
           {"sh": "√2 + √3 + √5", "py": "sqrt(2)+sqrt(3)+sqrt(5)", "kans": 8}])),
 ("AA-6.1.A", N("aa-tower-law", "Q ⊂ K ⊂ L with [L : Q] = {{kl}} and [K : Q] = {{kk}}. Find [L : K].", "kl/kk", "solve(Eq(Symbol('m')*kk, kl), Symbol('m'))[0]",
    "Degrees multiply up a tower, so the degree of any intermediate field must divide the degree of the whole extension", tex="[L:K]",
    cases=[{"kl": 12, "kk": 4}, {"kl": 8, "kk": 2}, {"kl": 6, "kk": 3}, {"kl": 24, "kk": 6}, {"kl": 20, "kk": 4}])),
 ("AA-6.1.B", N("aa-irreducible-count", "How many monic irreducible polynomials of degree {{kd}} are there over the field with {{kp}} elements?", "kans", "pm_irreducible_count(kp, kd)",
    "Every element of the field of order p^d outside its proper subfields is a root of exactly one of them, and each has d roots. For prime d that gives (p^d − p)/d", tex="polynomials",
    cases=[{"kp": p, "kd": d, "kans": irr(p, d)} for p, d in [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (5, 2)]])),
 ("AA-6.1.B", N("aa-subfield-count", "How many subfields has the field with {{kp}}^{{kn}} elements (counting itself and the prime field)?", "kans", "pm_ndiv(kn)",
    "One subfield of order p^d for each divisor d of n, and no others", tex="subfields",
    cases=[{"kp": 2, "kn": 6, "kans": 4}, {"kp": 3, "kn": 4, "kans": 3}, {"kp": 2, "kn": 12, "kans": 6}, {"kp": 5, "kn": 8, "kans": 4}, {"kp": 2, "kn": 30, "kans": 8}, {"kp": 7, "kn": 9, "kans": 3}])),
 ("AA-6.1.C", N("aa-cyclotomic-degree", "What is the order of the Galois group of Q(ζ) over Q, where ζ is a primitive {{kn}}th root of unity?", "kans", "pm_phi(kn)",
    "The group is the units modulo n: each automorphism sends ζ to ζᵏ with k coprime to n", tex="|G|",
    cases=[{"kn": n, "kans": phi(n)} for n in (5, 7, 8, 9, 12, 15, 16, 20)])),
 ("AA-6.1.C", F("aa-galois-correspondence", [
    ("The splitting field of x³ − 2 over Q has degree 6. Its Galois group is:", "S₃", "The cyclic group of order 6", "The cyclic group of order 3", "The Klein four-group"),
    ("In the Galois correspondence, a larger subgroup corresponds to:", "A smaller intermediate field", "A larger intermediate field", "A field of the same degree", "A non-normal extension"),
    ("An intermediate field is a normal extension of the base exactly when its subgroup is:", "Normal in the Galois group", "Cyclic", "Abelian", "Of prime order"),
    ("The Galois group of Q(√2, √3) over Q is:", "The Klein four-group", "The cyclic group of order 4", "S₃", "Trivial"),
    ("The Galois group of the field with pⁿ elements over the field with p elements is:", "Cyclic of order n, generated by x ↦ xᵖ", "The symmetric group Sₙ", "The units modulo n", "Trivial"),
    ("Q(∛2) over Q is not a Galois extension because it:", "Lacks the complex roots of x³ − 2", "Has degree 3", "Is not algebraic", "Is not separable")],
    "The correspondence turns questions about fields, which are infinite, into questions about a finite group. Q(√2, √3) has three quadratic subfields, matching the three subgroups of order 2")),
 ("AA-6.1.D", Q("aa-constructible-polygon", FD, "Can a regular {{kn}}-gon be constructed with ruler and compass?", pace="recall",
    cases=[{"kn": n, "kc": 0 if (phi(n) & (phi(n) - 1)) == 0 else 1} for n in (5, 7, 9, 12, 15, 17, 18, 20, 13, 24)],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Compute φ(n): it must be a power of 2. That allows n = 2ᵏ times distinct Fermat primes (3, 5, 17, 257, 65537), so 15 and 17 work while 7, 9 and 13 do not")),
 ("AA-6.1.D", F("aa-impossibility-facts", [
    ("Doubling the cube is impossible with ruler and compass because ∛2 has degree over Q equal to:", "3, not a power of 2", "2", "4", "Infinity"),
    ("Trisecting a 60° angle is impossible because cos 20° is a root of an irreducible:", "Cubic", "Quadratic", "Quartic", "Quintic"),
    ("The general quintic is not soluble by radicals because its Galois group S₅:", "Is not a soluble group", "Is too large", "Is not abelian", "Has even order"),
    ("Squaring the circle is impossible because π is:", "Transcendental", "Irrational", "Of degree 3", "Not real"),
    ("Every polynomial of degree at most 4 is soluble by radicals because S₂, S₃ and S₄ are:", "Soluble groups", "Abelian groups", "Simple groups", "Cyclic groups")],
    "Constructible numbers live in towers of quadratic extensions, so their degrees are powers of 2; solubility by radicals is the group-theoretic version of the same idea")),
]
