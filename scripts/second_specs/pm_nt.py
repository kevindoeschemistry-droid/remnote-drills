"""Number Theory (NT, Nov 2026): divisibility, congruences, residues, and Diophantine and prime questions. Structure
in UNITS (written by scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IA Numbers and Sets and Part II Number Theory schedules (read through an extraction of the
2026-27 Schedules booklet). The card answers by the theorem; tests/verify/pmcalc.py recounts by brute force."""
from math import gcd
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "nt-number-theory", "number-theory", "P1"
FW = dict(id="number-theory", title="Number Theory", code="NT", domain="nt", requires=["discrete-mathematics"], level=3,
          primary="cambridge-ii-number-theory", also=["cambridge-ia-numbers-sets"],
          note="Anchored on the Cambridge Numbers and Sets and Number Theory schedules (read through an extraction). The Jacobi symbol, binary quadratic forms and factorisation methods (T4, T5, T9) are not drilled in draft 1.",
          header=["Elementary number theory up to quadratic reciprocity, continued fractions and primality testing.",
                  "Mental Math already drills divisibility tricks and Computer Science drills RSA as a protocol; this framework",
                  "is the theory both rest on. Proofs are drilled as the computations they license."])
SKILLS = [("divisibility", "Euclid's algorithm, Bezout's identity and unique factorisation", "Divisibility", []),
          ("congruences", "Modular inverses, Fermat-Euler, the Chinese remainder theorem and RSA", "Congruences", ["nt.divisibility"]),
          ("residues", "Orders, primitive roots, quadratic residues and reciprocity", "Residues", ["nt.congruences"]),
          ("diophantine", "Continued fractions, Pell's equation, sums of squares and primality", "Diophantine questions and primes", ["nt.residues"])]
IDEAS = [("MOD", "Work in the right modulus", "Most questions about integers become finite once reduced modulo the right number; the art is choosing it."),
         ("STRUCT", "The units modulo n form a group", "Fermat, Euler, Wilson and primitive roots are all statements about the group of units, and its order is φ(n).")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
DV, CG, RS, DP = "nt.divisibility", "nt.congruences", "nt.residues", "nt.diophantine"
T = lambda *s: [f"cambridge-ii-number-theory:{x}" for x in s]
NS = lambda *s: [f"cambridge-ia-numbers-sets:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def steps(a, b):
    k = 0
    while b: a, b, k = b, a % b, k + 1
    return k


def phi(n):
    r, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0: m //= p
            r -= r // p
        p += 1
    return r - r // m if m > 1 else r


def order(a, n):
    k, r = 1, a % n
    while r != 1: r, k = r * a % n, k + 1
    return k


UNITS = {
 1: ("divisibility", "Divisibility and factorisation", T("T1") + NS("N4"), ["MOD"], {
   1: ("Euclid and unique factorisation", [
     ("A", T("T1") + NS("N4"), "Run Euclid's algorithm and say how long it takes.",
      "gcd(a, b) = gcd(b, a mod b); the last non-zero remainder is the gcd. Consecutive Fibonacci numbers are the slowest inputs.", "P1", [
       N("nt-gcd", DV, "Find the highest common factor of {{ka}} and {{kb}}.", "gcd(ka, kb)", "ka*kb/lcm(ka, kb)",
         "Divide and keep the remainder: gcd(a, b) = gcd(b, a mod b), until the remainder is zero", tex="\\gcd",
         given={"ka": {"pick": [252, 462, 1071, 2310]}, "kb": {"pick": [198, 105, 147, 390]}}),
       N("nt-euclid-steps", DV, "How many division steps does Euclid's algorithm take on ({{ka}}, {{kb}}), counting the final one that leaves remainder 0?", "kans", "pm_gcd_steps(ka, kb)",
         "Write out a = qb + r until r = 0 and count the lines. Consecutive Fibonacci numbers such as (34, 21) take the most steps for their size", tex="steps",
         cases=[{"ka": a, "kb": b, "kans": steps(a, b)} for a, b in [(34, 21), (100, 7), (91, 35), (55, 34), (120, 36), (89, 55)]])]),
     ("B", T("T1") + NS("N4"), "Solve a linear congruence or a linear Diophantine equation with Bezout's identity.",
      "ax + by = c has integer solutions exactly when gcd(a, b) divides c; running Euclid backwards finds one, and the rest differ by multiples of (b/g, −a/g).", "P1", [
       N("nt-linear-congruence", DV, "Find the least non-negative x with {{ka}}x ≡ {{kg}} (mod {{kb}}), where {{kg}} = gcd({{ka}}, {{kb}}).", "kans", "pm_bezout_x(ka, kb)",
         "Run Euclid's algorithm on (a, b) and back-substitute to write the gcd as ax + by; reduce x modulo b", tex="x",
         cases=[{"ka": a, "kb": b, "kg": gcd(a, b), "kans": next(x for x in range(b) if (a * x - gcd(a, b)) % b == 0)} for a, b in [(7, 30), (17, 60), (9, 24), (11, 26), (15, 35), (13, 100)]]),
       N("nt-coin-solutions", DV, "In how many ways can {{kc}} be written as {{ka}}x + {{kb}}y with x and y non-negative integers?", "kans", "pm_dioph_count(ka, kb, kc)",
         "Find one solution, then step x by b and y by −a (the two are coprime here) and count the steps that keep both non-negative", tex="ways",
         cases=[{"ka": a, "kb": b, "kc": c, "kans": sum(1 for x in range(c // a + 1) if (c - a * x) % b == 0)} for a, b, c in [(3, 5, 30), (4, 7, 60), (2, 3, 20), (5, 7, 70), (3, 4, 25), (5, 8, 100)]])]),
     ("C", T("T1") + NS("N4"), "Count and sum the divisors of an integer from its prime factorisation.",
      "If n = Π p^a then n has Π (a + 1) divisors and σ(n) = Π (p^(a+1) − 1)/(p − 1); both functions are multiplicative.", "P1", [
       N("nt-divisor-count", DV, "How many positive divisors has 2^{{ka}} · 3^{{kb}} · 5^{{kc}}?", "(ka + 1)*(kb + 1)*(kc + 1)", "pm_ndiv(2**ka*3**kb*5**kc)",
         "A divisor picks an exponent from 0 to a for each prime independently", tex="d(n)",
         given={"ka": {"pick": [1, 2, 3, 4]}, "kb": {"pick": [1, 2, 3]}, "kc": {"pick": [1, 2]}}),
       N("nt-divisor-sum", DV, "Find the sum of all positive divisors of {{kn}}.", "kans", "pm_sigma(kn)",
         "Factorise, then multiply the sums 1 + p + … + p^a over the primes. A number is perfect when this sum is twice the number, as for 6, 28 and 496", tex="\\sigma(n)",
         cases=[{"kn": n, "kans": sum(k for k in range(1, n + 1) if n % k == 0)} for n in (12, 28, 36, 60, 100, 496)])])]),
 }),
 2: ("congruences", "Congruences", T("T1", "T2") + NS("N4"), ["MOD", "STRUCT"], {
   1: ("Arithmetic modulo n", [
     ("A", T("T1") + NS("N4"), "Find a modular inverse and reduce a large power with Fermat's little theorem.",
      "a has an inverse modulo n exactly when gcd(a, n) = 1. For a prime p not dividing a, a^(p−1) ≡ 1 (mod p), so exponents reduce modulo p − 1.", "P1", [
       N("nt-inverse", CG, "Find the inverse of {{ka}} modulo {{kn}}, as a number from 1 to {{kn}} − 1.", "kans", "pm_inv(ka, kn)",
         "Solve ax ≡ 1 by Euclid's algorithm run backwards, or for a small modulus look for a multiple of n that is one less than a multiple of a", tex="a^{-1}",
         cases=[{"ka": a, "kn": n, "kans": pow(a, -1, n)} for a, n in [(3, 7), (5, 11), (7, 26), (9, 20), (11, 13), (17, 100), (4, 15)]]),
       N("nt-fermat-power", CG, "Find the remainder when {{ka}}^{{kk}} is divided by the prime {{kp}}.", "kans", "pm_powmod(ka, kk, kp)",
         "Reduce the exponent modulo p − 1 first, since a^(p−1) ≡ 1; then compute the small power that is left", tex="remainder",
         cases=[{"ka": a, "kk": k, "kp": p, "kans": pow(a, k, p)} for a, k, p in [(2, 100, 7), (3, 100, 11), (5, 62, 13), (2, 75, 11), (7, 50, 13), (3, 200, 17)]])]),
     ("B", T("T1") + NS("N4"), "Compute Euler's function and use Euler's theorem.",
      "φ(n) = n Π (1 − 1/p) over the primes dividing n, and a^φ(n) ≡ 1 (mod n) whenever gcd(a, n) = 1.", "P1", [
       N("nt-euler-phi", CG, "Find φ({{kn}}), the number of integers from 1 to {{kn}} that are coprime to {{kn}}.", "kans", "pm_phi(kn)",
         "Factorise n and multiply n by (1 − 1/p) for each prime p dividing it", tex="\\varphi(n)",
         cases=[{"kn": n, "kans": phi(n)} for n in (12, 30, 36, 45, 100, 101, 210)]),
       N("nt-last-two-digits", CG, "What are the last two digits of {{ka}}^{{kk}}? (Give the number they form.)", "kans", "pm_powmod(ka, kk, 100)",
         "φ(100) = 40, so for a coprime to 100 the exponent reduces modulo 40", tex="digits",
         cases=[{"ka": a, "kk": k, "kans": pow(a, k, 100)} for a, k in [(3, 82), (7, 43), (9, 41), (11, 122), (13, 42), (3, 123)]])]),
     ("C", T("T2") + NS("N4"), "Solve simultaneous congruences and use Wilson's theorem.",
      "If m and n are coprime, x ≡ a (mod m), x ≡ b (mod n) has exactly one solution modulo mn. Wilson: (p − 1)! ≡ −1 (mod p) exactly when p is prime.", "P1", [
       N("nt-crt", CG, "Find the least non-negative x with x ≡ {{ka}} (mod {{km}}) and x ≡ {{kb}} (mod {{kn}}).", "kans", "pm_crt(ka, km, kb, kn)",
         "List the numbers congruent to the first residue and test them against the second, or write x = a + mt and solve for t modulo n", tex="x",
         cases=[{"ka": a, "km": m, "kb": b, "kn": n, "kans": next(x for x in range(m * n) if x % m == a and x % n == b)}
                for a, m, b, n in [(2, 3, 3, 5), (1, 4, 2, 7), (3, 5, 4, 7), (2, 7, 5, 9), (1, 5, 6, 8), (4, 9, 7, 10)]]),
       N("nt-wilson", CG, "Find the remainder when {{kq}}! is divided by the prime {{kp}} (note {{kq}} = {{kp}} − 2).", "1", "factorial(kp - 2) % kp",
         "Wilson gives (p − 1)! ≡ −1; dividing by p − 1 ≡ −1 leaves (p − 2)! ≡ 1", tex="remainder",
         cases=[{"kp": p, "kq": p - 2} for p in (7, 11, 13, 17, 19)])]),
     ("D", NS("N4"), "Find an RSA decryption exponent and encrypt a small message.",
      "With n = pq and φ = (p − 1)(q − 1), the public exponent e and private exponent d satisfy ed ≡ 1 (mod φ); encryption is m^e mod n and decryption c^d mod n.", "P1", [
       N("nt-rsa-private", CG, "RSA with p = {{kp}}, q = {{kq}} and public exponent e = {{ke}}. Find the private exponent d (from 1 to φ − 1).", "kans", "pm_inv(ke, (kp - 1)*(kq - 1))",
         "φ = (p − 1)(q − 1), and d is the inverse of e modulo φ, not modulo n", tex="d",
         cases=[{"kp": p, "kq": qq, "ke": e, "kans": pow(e, -1, (p - 1) * (qq - 1))} for p, qq, e in [(3, 11, 3), (5, 11, 3), (7, 11, 7), (5, 17, 5), (7, 13, 5), (11, 13, 7)]]),
       N("nt-rsa-encrypt", CG, "RSA with modulus n = {{kn}} and public exponent e = {{ke}}. Encrypt the message m = {{km}}.", "kans", "pm_powmod(km, ke, kn)",
         "The ciphertext is m^e reduced modulo n; square and multiply, reducing as you go", tex="c",
         cases=[{"kn": n, "ke": e, "km": m, "kans": pow(m, e, n)} for n, e, m in [(33, 3, 4), (55, 3, 7), (77, 7, 2), (33, 7, 5), (91, 5, 3), (55, 7, 2)]])])]),
 }),
 3: ("residues", "Primitive roots and quadratic residues", T("T2", "T3"), ["STRUCT"], {
   1: ("The structure of the units", [
     ("A", T("T2"), "Find the order of an element modulo a prime and count primitive roots.",
      "The order of a modulo p divides p − 1. A primitive root has order p − 1; every prime has φ(p − 1) of them.", "P1", [
       N("nt-order-mod-p", RS, "What is the order of {{ka}} modulo {{kp}}?", "kans", "pm_order(ka, kp)",
         "Only divisors of p − 1 can occur, so test those in increasing order", tex="order",
         cases=[{"ka": a, "kp": p, "kans": order(a, p)} for a, p in [(2, 7), (3, 7), (2, 11), (3, 11), (5, 13), (2, 17), (4, 13)]]),
       N("nt-primitive-root-count", RS, "How many primitive roots are there modulo {{kp}}?", "kans", "pm_primroots(kp)",
         "The units modulo p form a cyclic group of order p − 1, which has φ(p − 1) generators", tex="roots",
         cases=[{"kp": p, "kans": phi(p - 1)} for p in (7, 11, 13, 17, 19, 31)])]),
     ("B", T("T3"), "Evaluate a Legendre symbol with Euler's criterion and the reciprocity laws.",
      "(a/p) ≡ a^((p−1)/2) (mod p). (−1/p) = 1 exactly when p ≡ 1 (mod 4); (2/p) = 1 exactly when p ≡ ±1 (mod 8); for odd primes (p/q)(q/p) = −1 only when both are 3 mod 4.", "P1", [
       N("nt-legendre", RS, "Evaluate the Legendre symbol ({{ka}}/{{kp}}): answer 1 if {{ka}} is a square modulo {{kp}}, and −1 if not.", "kans", "pm_legendre(ka, kp)",
         "Use Euler's criterion a^((p−1)/2), or flip with quadratic reciprocity and reduce until the symbol is one you know", tex="(a/p)",
         cases=[{"ka": a, "kp": p, "kans": 1 if any(k * k % p == a % p for k in range(1, p)) else -1} for a, p in [(2, 7), (3, 7), (5, 11), (2, 11), (3, 13), (7, 19), (10, 13), (6, 17)]]),
       F("nt-reciprocity-facts", RS, [
           ("−1 is a square modulo an odd prime p exactly when:", "p ≡ 1 (mod 4)", "p ≡ 3 (mod 4)", "p ≡ 1 (mod 3)", "p is any odd prime"),
           ("2 is a square modulo an odd prime p exactly when:", "p ≡ ±1 (mod 8)", "p ≡ ±3 (mod 8)", "p ≡ 1 (mod 4)", "p ≡ 3 (mod 4)"),
           ("For distinct odd primes p and q, (p/q) and (q/p) differ exactly when:", "Both p and q are 3 mod 4", "Either is 3 mod 4", "Both are 1 mod 4", "p + q is a multiple of 4"),
           ("How many of the residues 1, …, p − 1 are squares modulo an odd prime p?", "(p − 1)/2", "p − 1", "(p + 1)/2", "φ(p − 1)"),
           ("Euler's criterion says (a/p) is congruent modulo p to:", "a^((p−1)/2)", "a^(p−1)", "a^((p+1)/2)", "a²")],
         "Squaring is two-to-one on the non-zero residues, so exactly half are squares; reciprocity relates the two symbols with a sign that depends only on p and q modulo 4")])]),
 }),
 4: ("diophantine", "Diophantine equations and primes", T("T6", "T7", "T8"), ["MOD"], {
   1: ("Continued fractions, squares and primality", [
     ("A", T("T7"), "Expand a rational as a continued fraction and solve a Pell equation.",
      "The continued fraction of p/q is Euclid's algorithm written down. The convergents of √d give the solutions of x² − dy² = 1, and every solution is a power of the smallest.", "P1", [
       N("nt-continued-fraction", DP, "{{kp}}/{{kq}} = [a₀; a₁, a₂, …]. Find a_{{kk}}.", "kans", "pm_cf_term(kp, kq, kk)",
         "Take the integer part, invert the fractional part and repeat: the partial quotients are the quotients in Euclid's algorithm", tex="a_k",
         cases=[{"kp": 43, "kq": 19, "kk": 2, "kans": 1}, {"kp": 43, "kq": 19, "kk": 1, "kans": 3}, {"kp": 67, "kq": 29, "kk": 2, "kans": 4},
                {"kp": 355, "kq": 113, "kk": 1, "kans": 7}, {"kp": 355, "kq": 113, "kk": 2, "kans": 16}, {"kp": 99, "kq": 70, "kk": 3, "kans": 2}]),
       N("nt-pell", DP, "Find the smallest x > 1 for which x² − {{kd}}y² = 1 has a solution in positive integers.", "kans", "pm_pell_x(kd)",
         "Try y = 1, 2, 3, … until dy² + 1 is a square, or read the solution off the convergents of √d", tex="x",
         cases=[{"kd": 2, "kans": 3}, {"kd": 3, "kans": 2}, {"kd": 5, "kans": 9}, {"kd": 6, "kans": 5}, {"kd": 7, "kans": 8}, {"kd": 8, "kans": 3}, {"kd": 10, "kans": 19}])]),
     ("B", T("T3") + ["cambridge-ib-grm:RI"], "Decide whether an integer is a sum of two squares.",
      "An odd prime is a sum of two squares exactly when it is 1 mod 4. In general n is one exactly when every prime that is 3 mod 4 divides n to an even power.", "P2", [
       Q("nt-sum-two-squares", DP, "Is {{kn}} a sum of two integer squares?", pace="recall", cases=[
           {"kn": 13, "kc": 0}, {"kn": 21, "kc": 1}, {"kn": 29, "kc": 0}, {"kn": 45, "kc": 0}, {"kn": 30, "kc": 1},
           {"kn": 49, "kc": 0}, {"kn": 65, "kc": 0}, {"kn": 77, "kc": 1}, {"kn": 90, "kc": 0}, {"kn": 99, "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Factorise and look only at the primes that are 3 mod 4 (3, 7, 11, 19, …): each must appear to an even power. 45 = 3² · 5 = 36 + 9 works; 21 = 3 · 7 does not"),
       F("nt-two-squares-facts", DP, [
           ("An odd prime p is a sum of two squares exactly when:", "p ≡ 1 (mod 4)", "p ≡ 3 (mod 4)", "p ≡ 1 (mod 3)", "p ≡ ±1 (mod 8)"),
           ("No integer that is 3 mod 4 is a sum of two squares because squares modulo 4 are only:", "0 and 1", "0 and 2", "1 and 3", "0, 1 and 2"),
           ("In the Gaussian integers, the prime 5 factorises as:", "(2 + i)(2 − i)", "It stays prime", "(1 + i)²", "(5 + i)(5 − i)"),
           ("In the Gaussian integers, the prime 7:", "Stays prime", "Factorises as (2 + i)(2 − i)", "Is a unit", "Is a square")],
         "A prime splits in the Gaussian integers exactly when it is a sum of two squares, which is how the theorem is proved")]),
     ("C", T("T6", "T8"), "Estimate how many primes lie below a bound and apply the Fermat primality test.",
      "π(x) is about x/ln x. If a^(n−1) is not 1 modulo n then n is composite; composites that pass for base a are pseudoprimes, and Carmichael numbers such as 561 pass for every coprime base.", "P1", [
       Q("nt-prime-count-estimate", DP, "Use the prime number theorem to estimate how many primes are below 10^{{kk}}.", value="10^kk/(kk*log(10))", tex="\\pi(x)", tol=0.02,
         verify="10**kk/log(10**kk)", explain="π(x) ≈ x/ln x, and ln 10^k = k ln 10 ≈ 2.303k. The estimate runs about 10% low at these sizes: there are 78,498 primes below a million",
         given={"kk": {"pick": [4, 6, 9]}}),
       N("nt-fermat-test", DP, "Compute 2^{{km}} modulo {{kn}} (note {{km}} = {{kn}} − 1). A result other than 1 proves {{kn}} is composite.", "kans", "pm_powmod(2, kn - 1, kn)",
         "Square repeatedly and reduce. A prime would give 1 by Fermat's little theorem; the test never needs a factor to convict a composite", tex="remainder",
         cases=[{"kn": n, "km": n - 1, "kans": pow(2, n - 1, n)} for n in (9, 15, 21, 25, 33, 35)])])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
