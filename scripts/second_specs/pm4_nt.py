"""Number Theory, the intermediate steps (Nov 2026): 12 objectives between the ones draft 1 jumped across —
remainders and factorisations before Euclid and Bezout, congruence arithmetic before inverses and Fermat, squares
modulo p before the Legendre symbol, the sieve before the prime number theorem. NEEDS rewires the framework so the
path meets the small steps first. Basis unchanged: the Cambridge Numbers and Sets and Number Theory schedules."""
from math import comb, gcd
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "nt-steps", "number-theory", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
DV, CG, RS, DP = "nt.divisibility", "nt.congruences", "nt.residues", "nt.diophantine"
T = lambda *s: [f"cambridge-ii-number-theory:{x}" for x in s]
NS = lambda *s: [f"cambridge-ia-numbers-sets:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def primes(lo, hi):
    return sum(1 for m in range(max(2, lo), hi + 1) if all(m % d for d in range(2, int(m ** 0.5) + 1)))


def legendre(n, p):
    e, q = 0, p
    while q <= n: e += n // q; q *= p
    return e


TOPICS = {"1.2": "Remainders and factorisations", "2.2": "Congruence arithmetic", "3.2": "Squares modulo a prime", "4.2": "Primes up close"}
OBJS = [
 ("NT-1.2.A", T("T1") + NS("N4"), "Apply the division algorithm, including to negative numbers.", "For any integer a and positive n there is exactly one pair q, r with a = qn + r and 0 ≤ r < n. The remainder is never negative: −7 = (−2)·5 + 3."),
 ("NT-1.2.B", T("T1") + NS("N4"), "Find how often a prime divides a factorial.", "The exponent of p in n! is ⌊n/p⌋ + ⌊n/p²⌋ + ⌊n/p³⌋ + … (Legendre). The number of trailing zeros of n! is the exponent of 5."),
 ("NT-1.2.C", T("T1") + NS("N4"), "Read the gcd and lcm off prime factorisations.", "Take the smaller exponent of each prime for the gcd and the larger for the lcm, so gcd(a, b) · lcm(a, b) = ab."),
 ("NT-2.2.A", T("T1") + NS("N4"), "Add, multiply and take powers of residues.", "Congruence respects addition and multiplication, so any integer may be replaced by its remainder at any stage. Powers of a residue repeat in a cycle."),
 ("NT-2.2.B", T("T1") + NS("N4"), "Explain and use the digit tests for 9 and 11.", "Since 10 ≡ 1 (mod 9), a number is congruent to its digit sum modulo 9; since 10 ≡ −1 (mod 11), it is congruent to its alternating digit sum modulo 11."),
 ("NT-2.2.C", T("T1") + NS("N4"), "Solve a linear congruence and count its solutions.", "ax ≡ b (mod n) has a solution exactly when d = gcd(a, n) divides b, and then it has exactly d solutions modulo n."),
 ("NT-2.2.D", T("T1") + NS("N4"), "Reduce an exponent with Euler's theorem and invert with Fermat's.", "If gcd(a, n) = 1 then exponents may be reduced modulo φ(n). Modulo a prime p, the inverse of a is a^(p−2)."),
 ("NT-3.2.A", T("T3"), "List the squares modulo a prime and count the solutions of x² ≡ a.", "Modulo an odd prime p the non-zero squares are the (p − 1)/2 values of 1², 2², …, ((p − 1)/2)². x² ≡ a has two solutions if a is a non-zero square, one if a ≡ 0, none otherwise."),
 ("NT-3.2.B", T("T3"), "Apply Euler's criterion by direct computation.", "a^((p−1)/2) is congruent to 1 if a is a non-zero square modulo p and to −1 (that is, p − 1) if it is not."),
 ("NT-4.2.A", T("T6"), "Count primes in a range with the sieve of Eratosthenes.", "To find the primes up to N, cross out multiples of each prime up to √N; what survives is prime. A number below N with no prime factor up to √N is prime."),
 ("NT-4.2.B", T("T1", "T8"), "Connect Mersenne primes to even perfect numbers.", "If 2ᵖ − 1 is prime then 2ᵖ⁻¹(2ᵖ − 1) is perfect, and every even perfect number has this form (Euclid, Euler). 2ᵖ − 1 can only be prime when p is prime, but need not be: 2¹¹ − 1 = 23 · 89."),
 ("NT-4.2.C", T("T7"), "Generate Pythagorean triples.", "For m > n > 0, (m² − n², 2mn, m² + n²) is a Pythagorean triple; it is primitive exactly when m and n are coprime and of opposite parity, and every primitive triple arises this way."),
]
ADD = [
 ("NT-1.2.A", N("nt-remainder-negative", DV, "Find the remainder r (with 0 ≤ r < {{kn}}) when −{{ka}} is divided by {{kn}}.", "mod(-ka, kn)", "-ka - kn*floor(Rational(-ka, kn))",
    "Go down to the multiple of n just below −a and measure up from there: the remainder is never negative", tex="r",
    cases=[{"ka": 7, "kn": 5}, {"ka": 17, "kn": 6}, {"ka": 23, "kn": 7}, {"ka": 100, "kn": 9}, {"ka": 1, "kn": 12}, {"ka": 38, "kn": 11}])),
 ("NT-1.2.A", N("nt-quotient-remainder", DV, "{{ka}} = q · {{kn}} + r with 0 ≤ r < {{kn}}. Find q + r.", "floor(ka/kn) + mod(ka, kn)", "floor(Rational(ka, kn)) + ka - kn*floor(Rational(ka, kn))",
    "Divide, keep the whole part as q and what is left over as r", tex="q+r",
    given={"ka": {"pick": [100, 257, 365, 1000]}, "kn": {"pick": [7, 12, 13, 24]}})),
 ("NT-1.2.B", N("nt-prime-in-factorial", DV, "What is the highest power of {{kp}} that divides {{kn}}!? Give the exponent.", "kans", "pm_vp_factorial(kn, kp)",
    "Count the multiples of p up to n, then the multiples of p² again, then p³, and add", tex="exponent",
    cases=[{"kn": n, "kp": p, "kans": legendre(n, p)} for n, p in [(10, 2), (20, 3), (25, 5), (30, 2), (50, 7), (100, 3)]])),
 ("NT-1.2.B", N("nt-trailing-zeros", DV, "How many zeros does {{kn}}! end in?", "kans", "pm_vp_factorial(kn, 5)",
    "Each trailing zero needs a factor 2 and a factor 5, and fives are the scarce ones: count ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …", tex="zeros",
    cases=[{"kn": n, "kans": legendre(n, 5)} for n in (10, 25, 50, 100, 125, 30)])),
 ("NT-1.2.C", N("nt-lcm-from-factors", DV, "Find the lowest common multiple of 2^{{a1}} · 3^{{b1}} and 2^{{a2}} · 3^{{b2}} · 5.", "2^max(a1, a2)*3^max(b1, b2)*5", "lcm(2**a1*3**b1, 2**a2*3**b2*5)",
    "Take the larger exponent of each prime that appears in either number", tex="\\mathrm{lcm}",
    cases=[{"a1": 3, "b1": 1, "a2": 1, "b2": 2}, {"a1": 2, "b1": 2, "a2": 3, "b2": 1}, {"a1": 1, "b1": 3, "a2": 2, "b2": 1}, {"a1": 4, "b1": 1, "a2": 2, "b2": 2}])),
 ("NT-1.2.C", N("nt-gcd-lcm-product", DV, "Two positive integers have gcd {{kg}} and lcm {{kl}}, and one of them is {{ka}}. Find the other.", "kg*kl/ka", "solve(Eq(ka*Symbol('m'), kg*kl), Symbol('m'))[0]",
    "gcd × lcm equals the product of the two numbers", tex="b",
    cases=[{"kg": 6, "kl": 72, "ka": 18}, {"kg": 4, "kl": 120, "ka": 24}, {"kg": 5, "kl": 150, "ka": 25}, {"kg": 3, "kl": 180, "ka": 36}, {"kg": 7, "kl": 84, "ka": 21}])),
 ("NT-2.2.A", N("nt-residue-expression", CG, "Find the remainder when {{ka}} · {{kb}} + {{kc}} is divided by {{kn}}.", "mod(ka*kb + kc, kn)", "pm_powmod(ka*kb + kc, 1, kn)",
    "Reduce each number modulo n first, then multiply and add the small residues", tex="remainder",
    cases=[{"ka": 123, "kb": 457, "kc": 89, "kn": 10}, {"ka": 38, "kb": 44, "kc": 17, "kn": 7}, {"ka": 101, "kb": 99, "kc": 50, "kn": 9}, {"ka": 65, "kb": 27, "kc": 14, "kn": 13}, {"ka": 250, "kb": 31, "kc": 6, "kn": 11}])),
 ("NT-2.2.A", N("nt-last-digit-power", CG, "What is the last digit of {{ka}}^{{kk}}?", "kans", "pm_powmod(ka, kk, 10)",
    "Last digits of powers repeat with period at most 4, so reduce the exponent modulo the period", tex="digit",
    cases=[{"ka": a, "kk": k, "kans": pow(a, k, 10)} for a, k in [(7, 100), (3, 2025), (2, 50), (8, 31), (13, 77), (9, 123)]])),
 ("NT-2.2.B", N("nt-mod-nine", CG, "Find the remainder when {{kn}} is divided by 9.", "kans", "pm_digit_mod(kn, 9)",
    "Add the digits (and again if needed): a number and its digit sum leave the same remainder modulo 9", tex="remainder",
    cases=[{"kn": n, "kans": n % 9} for n in (58231, 712345, 99998, 4040404, 1234567, 86420)])),
 ("NT-2.2.B", N("nt-mod-eleven", CG, "Find the remainder (between 0 and 10) when {{kn}} is divided by 11.", "kans", "pm_digit_mod(kn, 11)",
    "Take the alternating sum of the digits starting from the units digit with a plus sign, then reduce modulo 11", tex="remainder",
    cases=[{"kn": n, "kans": n % 11} for n in (5831, 71234, 90817, 123456, 2468, 918273)])),
 ("NT-2.2.C", N("nt-congruence-count", CG, "How many solutions modulo {{kn}} has {{ka}}x ≡ {{kb}} (mod {{kn}})?", "kans", "pm_cong_solutions(ka, kb, kn)",
    "Let d = gcd(a, n). If d does not divide b there are none; if it does there are exactly d", tex="solutions",
    cases=[{"ka": a, "kb": b, "kn": n, "kans": gcd(a, n) if b % gcd(a, n) == 0 else 0} for a, b, n in [(6, 9, 15), (4, 6, 10), (3, 5, 7), (8, 12, 20), (6, 4, 9), (10, 15, 25), (9, 6, 12)]])),
 ("NT-2.2.C", N("nt-congruence-solve", CG, "Find the least non-negative solution of {{ka}}x ≡ {{kb}} (mod {{kn}}).", "kans", "pm_cong_least(ka, kb, kn)",
    "Multiply both sides by the inverse of a modulo n, which exists because a and n are coprime", tex="x",
    cases=[{"ka": a, "kb": b, "kn": n, "kans": b * pow(a, -1, n) % n} for a, b, n in [(3, 5, 7), (5, 2, 11), (7, 3, 10), (4, 9, 13), (9, 7, 20), (11, 4, 15)]])),
 ("NT-2.2.D", N("nt-euler-reduce", CG, "φ({{kn}}) = {{kf}}. Use Euler's theorem to find {{ka}}^{{kk}} modulo {{kn}}.", "kans", "pm_powmod(ka, kk, kn)",
    "Reduce the exponent modulo φ(n), then compute the small power that remains", tex="remainder",
    cases=[{"kn": n, "kf": f, "ka": a, "kk": k, "kans": pow(a, k, n)} for n, f, a, k in [(10, 4, 3, 42), (15, 8, 2, 83), (9, 6, 2, 100), (20, 8, 3, 66), (14, 6, 5, 61), (21, 12, 2, 50)]])),
 ("NT-2.2.D", N("nt-fermat-inverse", CG, "Modulo the prime {{kp}}, the inverse of {{ka}} is {{ka}}^{{kq}}. Compute it.", "kans", "pm_inv(ka, kp)",
    "a^(p−1) ≡ 1, so a · a^(p−2) ≡ 1: the power a^(p−2) is the inverse", tex="a^{-1}",
    cases=[{"kp": p, "ka": a, "kq": p - 2, "kans": pow(a, p - 2, p)} for p, a in [(7, 3), (11, 2), (13, 5), (7, 5), (11, 7), (17, 3)]])),
 ("NT-3.2.A", N("nt-square-solutions", RS, "How many solutions modulo {{kp}} has x² ≡ {{ka}} (mod {{kp}})?", "kans", "pm_poly_roots_mod(cf, kp)",
    "Square 1, 2, …, (p − 1)/2 to list the non-zero squares. A value on the list is hit twice, by x and by −x", tex="solutions",
    cases=[{"kp": p, "ka": a, "cf": f"{-a},0,1", "kans": sum(1 for x in range(p) if (x * x - a) % p == 0)} for p, a in [(7, 2), (7, 3), (11, 5), (11, 7), (13, 10), (13, 5), (17, 13)]])),
 ("NT-3.2.A", N("nt-count-squares", RS, "How many of the numbers 1, 2, …, {{kq}} are squares modulo the prime {{kp}}?", "(kp - 1)/2", "pm_distinct_values(py, kq)",
    "The map x ↦ x² is two-to-one on the non-zero residues, since x and −x have the same square, so exactly half are squares", tex="squares",
    cases=[{"kp": p, "kq": p - 1, "py": f"n**2 % {p}"} for p in (7, 11, 13, 17, 19, 23)])),
 ("NT-3.2.B", N("nt-euler-criterion", RS, "Compute {{ka}}^{{ke}} modulo {{kp}} (note {{ke}} = ({{kp}} − 1)/2). The answer is 1 or {{km}}.", "kans", "pm_powmod(ka, ke, kp)",
    "Euler's criterion: the result is 1 when a is a square modulo p and p − 1 (that is, −1) when it is not", tex="value",
    cases=[{"ka": a, "kp": p, "ke": (p - 1) // 2, "km": p - 1, "kans": pow(a, (p - 1) // 2, p)} for a, p in [(2, 7), (3, 7), (5, 11), (2, 11), (3, 13), (2, 13), (6, 17)]])),
 ("NT-3.2.B", F("nt-criterion-facts", RS, [
    ("Modulo 13, 5⁶ ≡ −1. Therefore 5 is:", "Not a square modulo 13", "A square modulo 13", "A primitive root for certain", "Congruent to 1"),
    ("If a and b are both non-squares modulo an odd prime p, then ab is:", "A square", "A non-square", "Zero", "Impossible to classify"),
    ("Modulo an odd prime p, (−1)^((p−1)/2) = 1 exactly when:", "p ≡ 1 (mod 4)", "p ≡ 3 (mod 4)", "p ≡ 1 (mod 3)", "p > 5"),
    ("A primitive root modulo an odd prime is always:", "A non-square", "A square", "Equal to 2", "Congruent to −1")],
    "The squares form a subgroup of index 2 in the units, so the Legendre symbol multiplies: non-square times non-square is a square")),
 ("NT-4.2.A", N("nt-count-primes", DP, "How many primes are there from {{ka}} to {{kb}} inclusive?", "kans", "pm_prime_count(ka, kb)",
    "Cross out multiples of 2, 3, 5 and 7 (enough for anything below 121) and count what is left", tex="primes",
    cases=[{"ka": a, "kb": b, "kans": primes(a, b)} for a, b in [(1, 30), (1, 50), (50, 100), (1, 100), (30, 60), (90, 120)]])),
 ("NT-4.2.A", N("nt-trial-division-bound", DP, "To show {{kn}} is prime by trial division, what is the largest prime you need to try?", "kans", "pm_trial_bound(kn)",
    "A composite number has a prime factor no larger than its square root, so stop at the largest prime below √n", tex="p",
    cases=[{"kn": 97, "kans": 7}, {"kn": 127, "kans": 11}, {"kn": 199, "kans": 13}, {"kn": 307, "kans": 17}, {"kn": 401, "kans": 19}, {"kn": 541, "kans": 23}])),
 ("NT-4.2.B", N("nt-perfect-from-mersenne", DP, "2^{{kp}} − 1 = {{km}} is prime. Find the even perfect number it gives.", "2^(kp - 1)*(2^kp - 1)", "pm_sigma(2**(kp - 1)*(2**kp - 1))/2",
    "Euclid: if 2ᵖ − 1 is prime, 2ᵖ⁻¹(2ᵖ − 1) equals the sum of its proper divisors", tex="n",
    cases=[{"kp": 2, "km": 3}, {"kp": 3, "km": 7}, {"kp": 5, "km": 31}, {"kp": 7, "km": 127}])),
 ("NT-4.2.B", F("nt-mersenne-facts", DP, [
    ("2¹¹ − 1 = 2047 = 23 · 89. This shows that:", "p prime does not make 2ᵖ − 1 prime", "2ᵖ − 1 is never prime", "11 is not prime", "Every Mersenne number is composite"),
    ("If n is composite, 2ⁿ − 1 is:", "Composite", "Prime", "Perfect", "A power of 2"),
    ("Every even perfect number has the form:", "2ᵖ⁻¹(2ᵖ − 1) with 2ᵖ − 1 prime", "2ᵖ − 1", "p(p + 1)/2 for a prime p", "2ᵖ + 1"),
    ("Whether an odd perfect number exists is:", "Unknown", "Proved impossible", "Known: 945 is one", "Equivalent to the Riemann hypothesis")],
    "If n = ab then 2ᵃ − 1 divides 2ⁿ − 1, so only prime exponents can give Mersenne primes, and not all of them do")),
 ("NT-4.2.C", N("nt-triple-hypotenuse", DP, "Find the hypotenuse of the Pythagorean triple generated by m = {{km}}, n = {{kn}}.", "km^2 + kn^2", "sqrt((km**2 - kn**2)**2 + (2*km*kn)**2)",
    "The triple is (m² − n², 2mn, m² + n²); the identity (m² − n²)² + (2mn)² = (m² + n²)² is why it works", tex="c",
    cases=[{"km": 2, "kn": 1}, {"km": 3, "kn": 2}, {"km": 4, "kn": 1}, {"km": 4, "kn": 3}, {"km": 5, "kn": 2}, {"km": 6, "kn": 1}])),
 ("NT-4.2.C", Q("nt-triple-primitive", DP, "Is the Pythagorean triple generated by m = {{km}}, n = {{kn}} primitive (no common factor)?", pace="recall",
    cases=[{"km": m, "kn": n, "kc": 0 if gcd(m, n) == 1 and (m - n) % 2 == 1 else 1} for m, n in [(2, 1), (3, 1), (3, 2), (4, 2), (5, 2), (5, 3), (6, 1), (6, 3)]],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Primitive exactly when m and n are coprime and one is even, one odd. If both are odd, all three numbers are even")),
]
NEEDS = {
 "NT-1.2.A": ["DM-1.2.A"], "NT-1.2.C": ["NT-1.2.A"], "NT-1.1.A": ["NT-1.2.C"], "NT-1.2.B": ["NT-1.2.A"], "NT-1.1.C": ["NT-1.2.C", "NT-1.2.B"],
 "NT-2.2.A": ["NT-1.2.A"], "NT-2.2.B": ["NT-2.2.A"], "NT-2.2.C": ["NT-2.2.A", "NT-1.1.B"], "NT-2.1.A": ["NT-2.2.C"], "NT-2.2.D": ["NT-2.1.A", "NT-2.1.B"], "NT-2.1.D": ["NT-2.2.D"],
 "NT-3.2.A": ["NT-2.2.A"], "NT-3.2.B": ["NT-3.2.A", "NT-2.1.A"], "NT-3.1.B": ["NT-3.2.B"],
 "NT-4.2.A": ["NT-1.2.A"], "NT-4.1.C": ["NT-4.2.A"], "NT-4.2.B": ["NT-1.1.C", "NT-4.2.A"], "NT-4.2.C": ["NT-1.2.C"], "NT-4.1.B": ["NT-4.2.C"],
}
