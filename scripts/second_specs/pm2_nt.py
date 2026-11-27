"""Number Theory additions (Nov 2026): the Jacobi symbol (NT-3.1.C) and factorisation by difference of squares
(NT-4.1.D), closing items T4 and T9 of the Cambridge Part II Number Theory schedule."""
from math import gcd, isqrt
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "nt-jacobi-factor", "number-theory", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
T4, T9 = ["cambridge-ii-number-theory:T4"], ["cambridge-ii-number-theory:T9"]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def jacobi(a, n):  # the reciprocity algorithm, no factorising
    a %= n; out = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5): out = -out
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3: out = -out
        a %= n
    return out if n == 1 else 0


def fermat(n):
    a = isqrt(n) + (isqrt(n) ** 2 < n)
    while isqrt(a * a - n) ** 2 != a * a - n: a += 1
    return a


OBJS = [
 ("NT-3.1.C", T4, "Evaluate a Jacobi symbol by reciprocity and say what it does and does not tell you.",
  "The Jacobi symbol (a/n) for odd n multiplies the Legendre symbols over the prime factors of n and obeys the same reciprocity rules, so it is computed without factorising. (a/n) = −1 means a is not a square modulo n; (a/n) = 1 does not mean it is."),
 ("NT-4.1.D", T9, "Factorise an integer by writing it as a difference of squares.",
  "If n = a² − b² then n = (a − b)(a + b). Fermat's method tries a = ⌈√n⌉, ⌈√n⌉ + 1, … until a² − n is a square. More generally x² ≡ y² (mod n) with x ≢ ±y gives the factor gcd(x − y, n)."),
]
ADD = [
 ("NT-3.1.C", N("nt-jacobi", "nt.residues", "Evaluate the Jacobi symbol ({{ka}}/{{kn}}).", "kans", "pm_jacobi(ka, kn)",
    "Pull out factors of 2 with the rule for (2/n), flip with reciprocity (a sign change only when both are 3 mod 4), reduce, and repeat", tex="(a/n)",
    cases=[{"ka": a, "kn": n, "kans": jacobi(a, n)} for a, n in [(2, 15), (7, 15), (5, 21), (2, 21), (11, 35), (8, 21), (13, 33), (7, 45)]])),
 ("NT-3.1.C", F("nt-jacobi-facts", "nt.residues", [
    ("The Jacobi symbol (2/15) equals 1. Is 2 a square modulo 15?", "No: it is a non-square modulo both 3 and 5", "Yes", "Only modulo 3", "It cannot be determined"),
    ("If the Jacobi symbol (a/n) equals −1, then a is:", "Not a square modulo n", "A square modulo n", "A unit of order 2", "Divisible by a prime factor of n"),
    ("The main practical advantage of the Jacobi symbol is that it can be computed:", "Without factorising n", "Without any division", "Only for prime n", "In constant time"),
    ("A composite n that satisfies a^((n−1)/2) ≡ (a/n) (mod n) for a base a is called:", "An Euler pseudoprime to base a", "A Carmichael number", "A Fermat prime", "A primitive root")],
    "(2/15) = (2/3)(2/5) = (−1)(−1) = 1: two wrongs make the symbol right, but 2 is still not a square modulo 15")),
 ("NT-4.1.D", N("nt-fermat-factorise", "nt.diophantine", "Fermat's method on n = {{kn}}: what is the first a ≥ √n for which a² − n is a perfect square?", "kans", "pm_fermat_a(kn)",
    "Start at the first integer above √n and step up, testing a² − n each time; then n = (a − b)(a + b). The method is fast exactly when n has two factors close together", tex="a",
    cases=[{"kn": n, "kans": fermat(n)} for n in (5959, 8051, 3127, 2491, 6557, 9991)])),
 ("NT-4.1.D", N("nt-congruent-squares", "nt.diophantine", "{{kx}}² ≡ {{ky}}² (mod {{kn}}). Use this to find a non-trivial factor of {{kn}}: compute gcd({{kx}} − {{ky}}, {{kn}}).", "gcd(kx - ky, kn)", "kn*(kx - ky)/lcm(kn, kx - ky)",
    "n divides (x − y)(x + y) without dividing either factor, so each shares a proper factor with n", tex="factor",
    cases=[{"kx": x, "ky": y, "kn": n} for x, y, n in [(10, 3, 91), (12, 5, 119), (17, 4, 91), (23, 10, 143), (16, 5, 77), (27, 8, 133)] if (x * x - y * y) % n == 0 and 1 < gcd(x - y, n) < n])),
]
