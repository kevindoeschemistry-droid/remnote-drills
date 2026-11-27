"""Discrete Mathematics topic 1.2, the bridge into proof (Nov 2026): six objectives between truth tables and
induction. Each asks for the piece of a proof a card can check: whether a definition applies, the algebra a direct
proof turns on, the cases an exhaustive proof needs, a witness, and the anatomy of an induction. NEEDS wires every
Discrete Mathematics objective. Basis unchanged (CUPM discrete report D1, D2; Cambridge Numbers and Sets N1, N3)."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "dm-proof-bridge", "discrete-mathematics", "P2"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
LG, IN = "dm.logic", "dm.induction"
D1 = ["cupm-2015-discrete:D1", "cambridge-ia-numbers-sets:N1"]
D2 = ["cupm-2015-discrete:D2", "cambridge-ia-numbers-sets:N3"]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


TOPICS = {"1.2": "From computing to proving"}
OBJS = [
 ("DM-1.2.A", D1, "Apply a definition exactly as written to decide whether an object qualifies.", "A definition is a test. n is even if n = 2k for some integer k; a divides b if b = ak for some integer k; a number is rational if it is a quotient of integers with non-zero denominator. Edge cases (0, 1, negatives) are settled by the wording, not by intuition."),
 ("DM-1.2.B", D1, "Carry out the algebra a direct proof turns on.", "A direct proof unpacks the hypothesis with the definition, computes, and repacks the result in the form the conclusion's definition demands: to show a product is odd, exhibit it as 2(something) + 1."),
 ("DM-1.2.C", D1, "State the contrapositive of a claim and recognise the contradiction a proof reaches.", "The contrapositive of 'if P then Q' is 'if not Q then not P' and is equivalent to it. A proof by contradiction assumes P and not Q together and derives something impossible."),
 ("DM-1.2.D", D1, "Split a claim into cases and check them all.", "A proof by cases must cover every possibility. Working modulo m reduces a claim about all integers to m cases: squares are 0 or 1 modulo 4, and 0, 1 or 4 modulo 8."),
 ("DM-1.2.E", D1, "Prove existence with a witness and say what uniqueness requires.", "An existence claim needs one example. Uniqueness needs an argument that any two objects with the property are equal. 'There is exactly one' needs both."),
 ("DM-1.2.F", D2, "Lay out an induction: base cases, hypothesis and step, including strong induction.", "Ordinary induction proves P(1) and that P(k) implies P(k + 1). Strong induction may use every earlier case, and needs as many base cases as the step reaches back."),
]
ADD = [
 ("DM-1.2.A", Q("dm-definition-applies", LG, "By the definition, is it true that {{st}}?", pace="recall", cases=[
    {"st": "0 is even", "kc": 0}, {"st": "1 is prime", "kc": 1}, {"st": "3 divides 0", "kc": 0}, {"st": "0 divides 5", "kc": 1}, {"st": "−7 is odd", "kc": 0},
    {"st": "0.75 is rational", "kc": 0}, {"st": "2 is prime", "kc": 0}, {"st": "every integer divides itself", "kc": 0}, {"st": "the empty set is a subset of every set", "kc": 0}, {"st": "1 is composite", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Substitute into the definition: 0 = 2 · 0, so 0 is even; 0 = 3 · 0, so 3 divides 0; but 5 = 0 · k has no solution. A prime has exactly two positive divisors, which rules out 1")),
 ("DM-1.2.A", F("dm-definition-wording", LG, [
    ("'a divides b' means there is an integer k with:", "b = ak", "a = bk", "a/b is an integer", "b < a"),
    ("An integer n is odd when there is an integer k with:", "n = 2k + 1", "n = 2k", "n = k + 1", "n/2 is not defined"),
    ("A real number is irrational when it:", "Cannot be written as a quotient of two integers", "Has a decimal expansion", "Is not an integer", "Is a square root"),
    ("A function f is injective when f(a) = f(b) implies:", "a = b", "a and b differ", "f is onto", "a and b are in the range"),
    ("A set A is a subset of B when:", "Every element of A is an element of B", "Some element of A is in B", "A and B have the same size", "B is a subset of A")],
    "Proofs begin by writing the definition out. Getting its direction wrong (which number is the multiple) derails everything after")),
 ("DM-1.2.B", N("dm-odd-product-witness", LG, "(2·{{ka}} + 1)(2·{{kb}} + 1) = 2k + 1. Find k.", "2*ka*kb + ka + kb", "solve(Eq((2*ka + 1)*(2*kb + 1), 2*Symbol('m') + 1), Symbol('m'))[0]",
    "Expand: 4ab + 2a + 2b + 1 = 2(2ab + a + b) + 1. Exhibiting k is the whole proof that a product of odd numbers is odd", tex="k",
    given={"ka": {"pick": [1, 2, 3, 5]}, "kb": {"pick": [2, 4, 7]}})),
 ("DM-1.2.B", F("dm-direct-proof-steps", LG, [
    ("To prove 'if n is even then n² is even' directly, after writing n = 2k the next line is:", "n² = 4k² = 2(2k²)", "Suppose n² is odd", "n² = 2k", "n is odd"),
    ("To prove 'if a divides b and b divides c then a divides c', write b = ak and c = bm, and conclude:", "c = a(km)", "a = c/km", "c = ab", "a = bm"),
    ("To prove 'the sum of two rationals is rational', write them as a/b and c/d and exhibit the sum as:", "(ad + bc)/(bd)", "(a + c)/(b + d)", "ac/bd", "(a + c)/bd"),
    ("In a direct proof of 'if P then Q', the first line is:", "Assume P", "Assume Q", "Assume not Q", "Assume not P")],
    "Unpack with the definition, compute, repack in the shape the conclusion's definition asks for")),
 ("DM-1.2.C", F("dm-contrapositive-of", LG, [
    ("The contrapositive of 'if n² is odd then n is odd' is:", "If n is even then n² is even", "If n is odd then n² is odd", "If n² is even then n is even", "n² is odd and n is even"),
    ("The contrapositive of 'if xy = 0 then x = 0 or y = 0' is:", "If x and y are both non-zero then xy is non-zero", "If x or y is non-zero then xy is non-zero", "If x = 0 or y = 0 then xy = 0", "If xy is non-zero then x is non-zero"),
    ("The contrapositive of 'if a function is differentiable then it is continuous' is:", "If it is not continuous then it is not differentiable", "If it is continuous then it is differentiable", "If it is not differentiable then it is not continuous", "It is differentiable and not continuous"),
    ("The contrapositive of 'if a + b is odd then a or b is odd' is:", "If a and b are both even then a + b is even", "If a or b is even then a + b is even", "If a + b is even then a and b are even", "If a and b are odd then a + b is odd")],
    "Swap and negate both parts, remembering that the negation of 'or' is 'and'")),
 ("DM-1.2.C", F("dm-contradiction-reached", LG, [
    ("In the proof that √2 is irrational, assuming √2 = a/b in lowest terms leads to the contradiction that:", "a and b are both even", "a is odd", "b is zero", "a = b"),
    ("In Euclid's proof of infinitely many primes, N = p₁p₂…pₙ + 1 gives a contradiction because N:", "Has a prime factor not on the list", "Is prime", "Is even", "Is smaller than pₙ"),
    ("To prove 'there is no largest integer' by contradiction, assume a largest integer M and consider:", "M + 1", "M − 1", "2M − M", "0"),
    ("A proof by contradiction of 'if P then Q' assumes:", "P and not Q", "Not P", "Q", "Not P and not Q")],
    "The contradiction can be with the assumption, with a known fact, or with itself; all that matters is that it cannot be true")),
 ("DM-1.2.D", N("dm-square-residues", LG, "How many different remainders can a perfect square leave on division by {{km}}?", "kans", "pm_distinct_values(py, km)",
    "Square each residue 0, 1, …, m − 1 and reduce: the squares of r and m − r agree, so about half the residues occur", tex="remainders",
    cases=[{"km": m, "py": f"n**2 % {m}", "kans": len({r * r % m for r in range(m)})} for m in (3, 4, 5, 7, 8, 10)])),
 ("DM-1.2.D", F("dm-cases-facts", LG, [
    ("No number of the form 4k + 3 is a sum of two squares because squares modulo 4 are only 0 or 1, so two of them sum to:", "0, 1 or 2", "0 or 1", "1, 2 or 3", "Any residue"),
    ("To prove a claim about all integers n by cases on parity, how many cases are needed?", "2", "1", "4", "Infinitely many"),
    ("n² + n is always even. A proof by cases checks:", "n even and n odd", "n positive and n negative", "n prime and n composite", "n = 0 and n = 1"),
    ("A proof by cases is invalid if the cases:", "Do not cover every possibility", "Overlap", "Number more than two", "Use different arguments")],
    "Cases may overlap but they may not leave a gap. Reducing modulo m is the standard way to get finitely many")),
 ("DM-1.2.E", N("dm-witness", LG, "To prove 'there is a positive integer n with n² − {{ks}}n + {{kp}} = 0', give the smaller such n.", "kr", "Min(*solve(Eq(Symbol('m')**2 - ks*Symbol('m') + kp, 0), Symbol('m')))",
    "An existence claim is proved by one example. Factor the quadratic and name a root", tex="n",
    cases=[{"kr": a, "ks": a + b, "kp": a * b} for a, b in [(2, 5), (3, 4), (1, 6), (4, 7), (2, 9)]])),
 ("DM-1.2.E", F("dm-uniqueness-facts", LG, [
    ("To prove an identity element of a group is unique, suppose e and f are both identities and show:", "e = f", "e and f differ", "e exists", "ef = 0"),
    ("'There exists a unique x with P(x)' requires proving:", "Existence and that any two such x are equal", "Existence only", "That P(x) holds for all x", "That no x satisfies P"),
    ("Giving the example x = 2 proves which statement about x² = 4?", "A solution exists", "The solution is unique", "Every x is a solution", "There are exactly two solutions"),
    ("A non-constructive existence proof shows something exists:", "Without exhibiting it", "By exhibiting it", "By checking every case", "Only for finite sets")],
    "e = ef = f: each equality uses that one of them is an identity. Uniqueness proofs nearly always have this suppose-there-are-two shape")),
 ("DM-1.2.F", N("dm-stamps-threshold", IN, "With {{ka}}-cent and {{kb}}-cent stamps, every amount from N cents upward can be made. What is the least such N?", "(ka - 1)*(kb - 1)", "pm_frobenius_next(ka, kb)",
    "The largest amount that cannot be made is ab − a − b, so everything from (a − 1)(b − 1) on can. The proof is a strong induction with a base cases", tex="N",
    cases=[{"ka": 3, "kb": 5}, {"ka": 4, "kb": 5}, {"ka": 3, "kb": 7}, {"ka": 5, "kb": 7}, {"ka": 4, "kb": 9}])),
 ("DM-1.2.F", F("dm-induction-anatomy", IN, [
    ("In an induction proof, the inductive hypothesis is the assumption that:", "The claim holds for k", "The claim holds for k + 1", "The claim holds for all n", "The base case is false"),
    ("A strong induction whose step uses the cases k − 1 and k − 2 needs how many base cases?", "2", "1", "3", "None"),
    ("Proving 'every amount ≥ 12 can be made from 4- and 5-cent stamps' by a step that subtracts 4 needs the base cases:", "12, 13, 14, 15", "12 only", "12 and 13", "4 and 5"),
    ("The well-ordering principle says every non-empty set of positive integers has:", "A least element", "A greatest element", "A prime element", "Finitely many elements"),
    ("An induction step that fails for k = 1 → 2 but works for all larger k proves the claim for:", "n = 1 only", "All n", "All n ≥ 2", "No n")],
    "The famous 'all horses are the same colour' argument fails exactly at the step from 1 to 2: every later step is fine, and the chain is still broken")),
]
NEEDS = {
 "DM-1.1.B": ["DM-1.1.A"], "DM-1.2.A": ["DM-1.1.A"], "DM-1.2.B": ["DM-1.2.A"], "DM-1.2.C": ["DM-1.2.B", "DM-1.1.B"], "DM-1.1.C": ["DM-1.2.C"],
 "DM-1.2.D": ["DM-1.2.B"], "DM-1.2.E": ["DM-1.2.B", "DM-1.1.B"], "DM-1.2.F": ["DM-1.1.C"],
 "DM-2.1.A": ["DM-1.2.F"], "DM-2.1.B": ["DM-2.1.A"],
 "DM-3.1.A": ["DM-1.2.A"], "DM-3.1.B": ["DM-3.1.A"], "DM-3.1.C": ["DM-3.1.A", "DM-1.2.A"], "DM-3.1.D": ["DM-3.1.B", "DM-1.2.C"],
 "DM-4.1.A": ["DM-3.1.A"], "DM-4.1.B": ["DM-4.1.A"], "DM-4.1.C": ["DM-4.1.A", "DM-2.1.A"], "DM-4.1.D": ["DM-4.1.A", "DM-3.1.A"], "DM-4.1.E": ["DM-4.1.A", "DM-1.2.D"],
 "DM-5.1.A": ["DM-4.1.B", "DM-4.1.C"], "DM-5.1.B": ["DM-5.1.A", "DM-2.1.B"],
 "DM-6.1.A": ["DM-4.1.A"], "DM-6.1.B": ["DM-6.1.A", "DM-2.1.A"], "DM-6.1.C": ["DM-6.1.A"], "DM-6.1.D": ["DM-6.1.B"], "DM-6.1.E": ["DM-6.1.B"], "DM-6.1.F": ["DM-6.1.C", "DM-4.1.E"],
}
