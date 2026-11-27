"""Real Analysis (RA, Nov 2026): the real numbers, sequences, series, continuity, and the theorems behind calculus.
Structure in UNITS (written by scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IA Analysis I schedule, with the real-number block of Numbers and Sets (both read through
an extraction of the 2026-27 Schedules booklet). Calculus already drills the computations; this framework drills
what makes them legitimate: the epsilon, the hypothesis and the counterexample."""
from math import factorial
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ra-analysis", "real-analysis", "P1"
FW = dict(id="real-analysis", title="Real Analysis", code="RA", domain="ra", requires=["calculus", "discrete-mathematics"], level=4,
          primary="cambridge-ia-analysis-i", also=["cambridge-ia-numbers-sets"],
          note="Anchored on the Cambridge Analysis I schedule (read through an extraction). Uniform convergence, metric spaces and the multivariable theory (Cambridge Analysis II) are not built; Topology takes up compactness and connectedness.",
          header=["The same objects as Calculus, asked the other way round: not 'what is the limit' but 'how far out must n be',",
                  "not 'find the maximum' but 'which hypothesis guarantees one'. A card cannot grade a proof, so each theorem is",
                  "drilled as the N or delta it produces and as the example that breaks it when a hypothesis is dropped."])
SKILLS = [("reals", "Suprema, completeness and the Archimedean property", "The real numbers", []),
          ("sequences", "Epsilon-N limits, monotone and Cauchy sequences, limsup", "Sequences", ["ra.reals"]),
          ("series", "Convergence tests, absolute convergence and radius of convergence", "Series", ["ra.sequences"]),
          ("continuity", "Epsilon-delta continuity, the intermediate and extreme value theorems, uniform continuity", "Continuity", ["ra.sequences"]),
          ("calculus", "The mean value theorem, Taylor's remainder, Riemann sums and improper integrals", "Differentiation and integration", ["ra.continuity"])]
IDEAS = [("EPS", "A limit is a promise about every epsilon", "Convergence means a challenge ε can always be met; the proof is the rule that produces N or δ from ε."),
         ("HYP", "Every hypothesis is there for a reason", "Closed, bounded, continuous, monotone: drop one and a standard counterexample appears. Knowing the counterexample is knowing the theorem.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
RL, SQ, SR, CN, CL = "ra.reals", "ra.sequences", "ra.series", "ra.continuity", "ra.calculus"
A = lambda *s: [f"cambridge-ia-analysis-i:{x}" for x in s]
NS = lambda *s: [f"cambridge-ia-numbers-sets:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=True, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


def taylor_n(tol):  # least n with 3/(n+1)! < tol
    n = 1
    while not 3 / factorial(n + 1) < tol: n += 1
    return n


UNITS = {
 1: ("reals", "The real numbers", NS("N5") + A("A1"), ["HYP"], {
   1: ("Completeness", [
     ("A", NS("N5"), "Find the supremum and infimum of a set and say whether they are attained.",
      "The supremum is the least upper bound. Every non-empty set of reals that is bounded above has one, which need not belong to the set; the rationals lack this property.", "P1", [
       N("ra-supremum", RL, "Find the supremum of the set {{st}}.", "kans", "calc(vy)",
         "Find a value the set approaches or reaches from below and check nothing smaller is still an upper bound", tex="\\sup", final=False,
         cases=[{"st": "{1 − 1/n : n = 1, 2, 3, …}", "kans": 1, "vy": "limit(1 - 1/nn, nn, oo)"},
                {"st": "{(−1)ⁿ/n : n = 1, 2, 3, …}", "kans": 0.5, "vy": "Max(-1, Rational(1, 2), -Rational(1, 3), Rational(1, 4))"},
                {"st": "{x rational : x² < 2}", "kans": 1.41421356, "vy": "sqrt(2)"},
                {"st": "{n/(2n + 1) : n = 1, 2, 3, …}", "kans": 0.5, "vy": "limit(nn/(2*nn + 1), nn, oo)"},
                {"st": "{1/n + 1/m : n, m = 1, 2, 3, …}", "kans": 2, "vy": "Max(2, Rational(3, 2), 1)"},
                {"st": "{3 − 2/n² : n = 1, 2, 3, …}", "kans": 3, "vy": "limit(3 - 2/nn**2, nn, oo)"}]),
       Q("ra-sup-attained", RL, "Does the set {{st}} contain its supremum?", pace="recall", cases=[
           {"st": "{1 − 1/n : n ≥ 1}", "kc": 1}, {"st": "the closed interval [0, 1]", "kc": 0}, {"st": "the open interval (0, 1)", "kc": 1},
           {"st": "{(−1)ⁿ/n : n ≥ 1}", "kc": 0}, {"st": "{x rational : x² < 2}", "kc": 1}, {"st": "{1/n : n ≥ 1}", "kc": 0}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="A supremum that belongs to the set is a maximum. Sets that creep up to a bound without reaching it have a supremum but no maximum")]),
     ("B", NS("N5") + A("A1"), "Use the Archimedean property and say where the rationals fail to be complete.",
      "For any real ε > 0 there is a natural number n with 1/n < ε. The rationals are dense but not complete: {x : x² < 2} has no rational least upper bound.", "P1", [
       N("ra-archimedean", RL, "What is the least positive integer n with 1/n < {{ke}}?", "floor(1/ke) + 1", "pm_first_n('1/n', 0, ke)",
         "1/n < ε exactly when n > 1/ε, so take the first integer strictly beyond 1/ε", tex="n",
         given={"ke": {"pick": [0.3, 0.07, 0.03, 0.013, 0.006]}}),
       F("ra-completeness-facts", RL, [
           ("Which property distinguishes the real numbers from the rational numbers?", "Every non-empty set bounded above has a least upper bound", "Between any two elements lies another", "Addition and multiplication obey the field axioms", "The order is total"),
           ("Between any two distinct real numbers there is:", "Both a rational and an irrational number", "A rational but not always an irrational", "An integer", "Only finitely many rationals"),
           ("The proof that √2 is irrational assumes √2 = a/b in lowest terms and shows:", "Both a and b are even", "a is odd", "b = 1", "a² < 2b²"),
           ("A bounded increasing sequence of real numbers must:", "Converge to its supremum", "Be eventually constant", "Converge to a rational number", "Have a decreasing subsequence")],
         "Density and the field axioms hold in the rationals too; the least upper bound axiom is what fills in the gaps")])]),
 }),
 2: ("sequences", "Sequences", A("A1"), ["EPS"], {
   1: ("Convergence", [
     ("A", A("A1"), "Produce the N that the definition of a limit asks for.",
      "a_n → L means: for every ε > 0 there is an N with |a_n − L| < ε for all n ≥ N. Solving the inequality for n gives N as a function of ε.", "P1", [
       N("ra-epsilon-n", SQ, "a_n = {{sh}} converges to {{kl}}. What is the least N such that |a_n − {{kl}}| < {{ke}} for every n ≥ N?", "kans", "pm_first_n(py, kl, ke)",
         "Write |a_n − L| as a simple expression in n and solve the inequality; the answer is the first integer that satisfies it", tex="N",
         cases=[{"sh": "(n + 1)/n", "py": "(n + 1)/n", "kl": 1, "ke": 0.01, "kans": 101}, {"sh": "(2n + 3)/n", "py": "(2*n + 3)/n", "kl": 2, "ke": 0.1, "kans": 31},
                {"sh": "1/n²", "py": "1/n**2", "kl": 0, "ke": 0.01, "kans": 11}, {"sh": "n/(n + 1)", "py": "n/(n + 1)", "kl": 1, "ke": 0.05, "kans": 20},
                {"sh": "(3n + 1)/(n + 2)", "py": "(3*n + 1)/(n + 2)", "kl": 3, "ke": 0.1, "kans": 49}, {"sh": "1/√n", "py": "1/sqrt(n)", "kl": 0, "ke": 0.1, "kans": 101}]),
       N("ra-limit-value", SQ, "Find the limit of a_n = {{sh}} as n → ∞.", "kans", "calc(vy)",
         "Divide through by the dominant term, or recognise a standard limit such as (1 + a/n)ⁿ → e^a and n^(1/n) → 1", tex="\\lim a_n", final=False,
         cases=[{"sh": "(3n² + n)/(2n² − 5)", "kans": 1.5, "vy": "limit((3*nn**2 + nn)/(2*nn**2 - 5), nn, oo)"},
                {"sh": "√(n² + 4n) − n", "kans": 2, "vy": "limit(sqrt(nn**2 + 4*nn) - nn, nn, oo)"},
                {"sh": "(1 + 2/n)ⁿ", "kans": 7.3890561, "vy": "limit((1 + 2/nn)**nn, nn, oo)"},
                {"sh": "n^(1/n)", "kans": 1, "vy": "limit(nn**(1/nn), nn, oo)"},
                {"sh": "(2ⁿ + 3ⁿ)^(1/n)", "kans": 3, "vy": "limit((2**nn + 3**nn)**(1/nn), nn, oo)"},
                {"sh": "√(n² + n) − n", "kans": 0.5, "vy": "limit(sqrt(nn**2 + nn) - nn, nn, oo)"}])]),
     ("B", A("A1"), "Find the limit of a bounded monotone recursive sequence and know what guarantees it exists.",
      "A bounded monotone sequence converges. Once the limit is known to exist, it must satisfy the recurrence as a fixed-point equation. Bolzano-Weierstrass: every bounded sequence has a convergent subsequence.", "P1", [
       N("ra-recursive-limit", SQ, "x₁ = 1 and x_(n+1) = √({{kk}} + x_n). The sequence is increasing and bounded. Find its limit.", "(1 + sqrt(1 + 4*kk))/2", "Max(*solve(Eq(Symbol('m')**2, kk + Symbol('m')), Symbol('m')))",
         "The limit L satisfies L = √(k + L), so L² − L − k = 0; take the positive root. The step that needs proof is that the limit exists at all", tex="L", final=False,
         given={"kk": {"pick": [2, 6, 12, 20]}}),
       F("ra-sequence-theorems", SQ, [
           ("Bolzano-Weierstrass says every bounded sequence of real numbers has:", "A convergent subsequence", "A limit", "A monotone tail", "A maximum"),
           ("A sequence is Cauchy when:", "Its terms are eventually within ε of each other, for every ε", "Consecutive terms get closer together", "It is bounded", "It is monotone"),
           ("a_n = 1 + 1/2 + … + 1/n has a_(n+1) − a_n → 0. The sequence:", "Diverges: it is not Cauchy", "Converges", "Is bounded", "Is eventually constant"),
           ("In the real numbers, a sequence converges exactly when it is:", "Cauchy", "Bounded", "Monotone", "Positive"),
           ("The sequence (−1)ⁿ is bounded and has:", "Convergent subsequences but no limit", "Limit 0", "No convergent subsequence", "Limit 1")],
         "Consecutive terms closing up is weaker than Cauchy: the harmonic sums gain a full 1/2 between n and 2n however large n is")]),
     ("C", A("A1"), "Find the limit superior and limit inferior of a bounded sequence.",
      "lim sup is the largest limit of any subsequence and lim inf the smallest. The sequence converges exactly when the two agree.", "P1", [
       N("ra-limsup", SQ, "Find the lim sup of a_n = {{sh}}.", "kans", "calc(vy)",
         "Split into subsequences that each converge (even and odd n, or n by residue) and take the largest of their limits", tex="\\limsup", final=False,
         cases=[{"sh": "(−1)ⁿ(1 + 1/n)", "kans": 1, "vy": "limit(1 + 1/(2*nn), nn, oo)"},
                {"sh": "sin(nπ/2) + 1/n", "kans": 1, "vy": "limit(1 + 1/(4*nn + 1), nn, oo)"},
                {"sh": "(−1)ⁿ n/(n + 1) + 2", "kans": 3, "vy": "limit(2*nn/(2*nn + 1) + 2, nn, oo)"},
                {"sh": "cos(nπ) · 3 + 1/n²", "kans": 3, "vy": "limit(3 + 1/(2*nn)**2, nn, oo)"},
                {"sh": "(1 + (−1)ⁿ)/2 · 5", "kans": 5, "vy": "limit(5 + 0*nn, nn, oo)"}]),
       F("ra-limsup-facts", SQ, [
           ("A bounded sequence converges exactly when:", "Its lim sup equals its lim inf", "Its lim sup is finite", "It has a convergent subsequence", "Its lim inf is 0"),
           ("The lim inf of (−1)ⁿ(1 + 1/n) is:", "−1", "1", "0", "−2"),
           ("For any bounded sequence, some subsequence converges to:", "The lim sup", "The supremum", "The average of lim sup and lim inf", "Zero"),
           ("The lim sup of a sequence compared with its supremum is always:", "Less than or equal to it", "Equal to it", "Greater than or equal to it", "Unrelated")],
         "The supremum can be a single early term that never recurs; the lim sup only sees what happens infinitely often")])]),
 }),
 3: ("series", "Series", A("A1", "A4"), ["EPS", "HYP"], {
   1: ("Convergence of series", [
     ("A", A("A1"), "Classify a series as absolutely convergent, conditionally convergent or divergent.",
      "Absolute convergence implies convergence. The alternating series test gives convergence for decreasing terms tending to 0; Σ 1/n^p converges exactly when p > 1.", "P2", [
       Q("ra-series-classify", SR, "The series Σ {{sh}} (n from 1 to ∞) is:", pace="recall", cases=[
           {"sh": "(−1)ⁿ/n", "kc": 1}, {"sh": "(−1)ⁿ/n²", "kc": 0}, {"sh": "1/n", "kc": 2}, {"sh": "(−1)ⁿ/√n", "kc": 1}, {"sh": "n/2ⁿ", "kc": 0},
           {"sh": "(−1)ⁿ n/(n + 1)", "kc": 2}, {"sh": "1/(n² + 1)", "kc": 0}, {"sh": "1/(n ln n), from n = 2", "kc": 2}, {"sh": "sin(n)/n²", "kc": 0}],
         choice=["Absolutely convergent", "Conditionally convergent", "Divergent"], correct="kc", verify="authored",
         explain="First ask whether the terms tend to 0; if not, it diverges. Then test the absolute values with comparison, ratio or integral; if those diverge but the signs alternate with decreasing terms, convergence is conditional"),
       N("ra-ratio-test", SR, "For the series Σ {{sh}}, find the limit of |a_(n+1)/a_n|. (Below 1 the series converges absolutely.)", "kans", "calc(vy)",
         "Write out the ratio and cancel: factorials leave a single factor, powers leave the base, polynomial factors tend to 1", tex="\\lim|a_{n+1}/a_n|", final=False,
         cases=[{"sh": "n²/3ⁿ", "kans": 0.33333333, "vy": "limit(((nn + 1)**2/3**(nn + 1))/(nn**2/3**nn), nn, oo)"},
                {"sh": "2ⁿ/n³", "kans": 2, "vy": "limit((2**(nn + 1)/(nn + 1)**3)/(2**nn/nn**3), nn, oo)"},
                {"sh": "n!/nⁿ", "kans": 0.36787944, "vy": "limit((nn/(nn + 1))**nn, nn, oo)"},
                {"sh": "(n!)²/(2n)!", "kans": 0.25, "vy": "limit((nn + 1)**2/((2*nn + 1)*(2*nn + 2)), nn, oo)"},
                {"sh": "5ⁿ/(n · 4ⁿ)", "kans": 1.25, "vy": "limit((Rational(5, 4)**(nn + 1)/(nn + 1))/(Rational(5, 4)**nn/nn), nn, oo)"}])]),
     ("B", A("A1"), "Sum a geometric or telescoping series exactly.",
      "Σ r^n from n = 0 is 1/(1 − r) for |r| < 1. A telescoping series is summed from its partial sums, which collapse to the first and last terms.", "P1", [
       N("ra-telescoping", SR, "Evaluate Σ 1/(n(n + {{kk}})) for n from 1 to ∞.", "kans", "summation(1/(nn*(nn + kk)), (nn, 1, oo))",
         "Partial fractions give (1/k)(1/n − 1/(n + k)); all but the first k positive terms cancel, leaving (1/k)(1 + 1/2 + … + 1/k)", tex="sum", final=False,
         cases=[{"kk": 1, "kans": 1}, {"kk": 2, "kans": 0.75}, {"kk": 3, "kans": 0.61111111}, {"kk": 4, "kans": 0.52083333}]),
       N("ra-geometric-from-k", SR, "Evaluate Σ ({{kp}}/{{kq}})ⁿ for n from {{ks}} to ∞.", "(kp/kq)^ks/(1 - kp/kq)", "summation(Rational(kp, kq)**nn, (nn, ks, oo))",
         "Factor out the first term r^s and sum the rest as 1/(1 − r)", tex="sum", final=False,
         given={"kp": {"pick": [1, 2]}, "kq": {"pick": [3, 5]}, "ks": {"pick": [1, 2, 3]}})]),
     ("C", A("A4"), "Find the radius of convergence of a power series and test its endpoints.",
      "Σ a_n x^n converges absolutely for |x| < R and diverges for |x| > R, with 1/R = lim |a_(n+1)/a_n| when that exists. Behaviour at |x| = R must be tested separately.", "P1", [
       N("ra-radius", SR, "Find the radius of convergence of Σ {{sh}}.", "kans", "calc(vy)",
         "Apply the ratio test to the coefficients: R is the limit of |a_n/a_(n+1)|", tex="R", final=False,
         cases=[{"sh": "xⁿ/(n · 3ⁿ)", "kans": 3, "vy": "limit((1/(nn*3**nn))/(1/((nn + 1)*3**(nn + 1))), nn, oo)"},
                {"sh": "n² 2ⁿ xⁿ", "kans": 0.5, "vy": "limit((nn**2*2**nn)/((nn + 1)**2*2**(nn + 1)), nn, oo)"},
                {"sh": "(2n)! xⁿ/(n!)²", "kans": 0.25, "vy": "limit((nn + 1)**2/((2*nn + 1)*(2*nn + 2)), nn, oo)"},
                {"sh": "nⁿ xⁿ/n!", "kans": 0.36787944, "vy": "limit((nn/(nn + 1))**nn, nn, oo)"},
                {"sh": "xⁿ/n²", "kans": 1, "vy": "limit((nn + 1)**2/nn**2, nn, oo)"}]),
       Q("ra-endpoints", SR, "Σ {{sh}} has radius of convergence 1. At the endpoints x = 1 and x = −1 it converges at:", pace="recall", cases=[
           {"sh": "xⁿ/n", "kc": 2}, {"sh": "xⁿ/n²", "kc": 0}, {"sh": "xⁿ", "kc": 3}, {"sh": "(−1)ⁿ xⁿ/n", "kc": 1}, {"sh": "n xⁿ", "kc": 3}, {"sh": "xⁿ/√n", "kc": 2}],
         choice=["Both endpoints", "x = 1 only", "x = −1 only", "Neither endpoint"], correct="kc", verify="authored",
         explain="Substitute each endpoint and test the numerical series that results. Σ xⁿ/n is the harmonic series at 1 and the alternating harmonic series at −1")])]),
 }),
 4: ("continuity", "Continuity", A("A2"), ["EPS", "HYP"], {
   1: ("Continuous functions", [
     ("A", A("A2"), "Produce the δ that the definition of continuity asks for.",
      "f is continuous at a when for every ε > 0 there is a δ > 0 with |f(x) − f(a)| < ε whenever |x − a| < δ. For a linear f, δ = ε/|slope|; for x², restrict to δ ≤ 1 and bound the other factor.", "P1", [
       N("ra-delta-linear", CN, "For f(x) = {{ka}}x + {{kb}}, what is the largest δ such that |x − 2| < δ guarantees |f(x) − f(2)| < {{ke}}?", "ke/ka", "solve(Eq(ka*Symbol('m'), ke), Symbol('m'))[0]",
         "|f(x) − f(2)| = a|x − 2|, so the condition is exactly |x − 2| < ε/a", tex="\\delta", final=False,
         given={"ka": {"pick": [2, 4, 5]}, "kb": {"pick": [1, 3]}, "ke": {"pick": [0.1, 0.02, 0.5]}}),
       N("ra-delta-square", CN, "To show x² is continuous at {{ka}}, restrict to |x − {{ka}}| < 1 so that |x + {{ka}}| < {{kb}}. Which δ then works for ε = {{ke}}? Give min(1, ε/{{kb}}).", "min(1, ke/kb)", "Min(1, nsimplify(ke)/(2*ka + 1))",
         "|x² − a²| = |x − a||x + a| < δ(2a + 1) once δ ≤ 1, so δ = min(1, ε/(2a + 1)) is enough", tex="\\delta", final=False,
         cases=[{"ka": a, "kb": 2 * a + 1, "ke": e} for a, e in [(1, 0.3), (2, 0.1), (3, 0.7), (4, 0.09), (2, 10)]])]),
     ("B", A("A2"), "Apply the intermediate and extreme value theorems and say which hypothesis each needs.",
      "A continuous function on a closed bounded interval takes every value between its end values, is bounded, and attains its bounds. Each conclusion fails on an open or unbounded interval, or for a discontinuous function.", "P2", [
       N("ra-bisection-steps", CN, "A continuous f changes sign on an interval of length {{kl}}. How many bisection steps guarantee an interval of length at most {{kt}} containing a root?", "ceil(log2(kl/kt))", "pm_first_n('2**(-n)', 0, nsimplify(kt)/kl + Rational(1, 10**9))",
         "Each step halves the interval and the intermediate value theorem keeps a root inside, so n steps leave length L/2ⁿ", tex="steps",
         cases=[{"kl": 1, "kt": 0.01}, {"kl": 2, "kt": 0.001}, {"kl": 4, "kt": 0.05}, {"kl": 1, "kt": 0.0001}, {"kl": 8, "kt": 0.3}]),
       F("ra-ivt-evt-facts", CN, [
           ("f(x) = 1/x on the open interval (0, 1) is continuous but unbounded. Which hypothesis of the extreme value theorem fails?", "The interval is not closed", "f is not continuous", "The interval is not bounded", "f is not differentiable"),
           ("f(x) = x on the open interval (0, 1) is bounded but has no maximum because:", "Its supremum 1 is not attained", "It is not continuous", "It is not bounded above", "It is decreasing"),
           ("x⁵ + x − 1 has a real root because it is continuous and:", "Negative at 0 and positive at 1", "A polynomial of odd degree only", "Increasing", "Bounded"),
           ("The function that is −1 for x < 0 and 1 for x ≥ 0 never takes the value 0 on [−1, 1]. This is consistent with the intermediate value theorem because:", "The function is not continuous", "The interval is not closed", "0 is not between −1 and 1", "The function is not bounded"),
           ("A continuous function from [0, 1] to [0, 1] must have:", "A fixed point", "A zero", "A maximum at an endpoint", "An inverse")],
         "For the fixed point, apply the intermediate value theorem to f(x) − x, which is ≥ 0 at 0 and ≤ 0 at 1")]),
     ("C", A("A2"), "Decide whether a function is uniformly continuous and find a Lipschitz constant.",
      "Uniform continuity means one δ works at every point. A continuous function on a closed bounded interval is uniformly continuous; a bounded derivative gives a Lipschitz constant sup|f′|, hence uniform continuity.", "P2", [
       Q("ra-uniformly-continuous", CN, "Is f(x) = {{fn}} uniformly continuous on {{dm}}?", pace="recall", cases=[
           {"fn": "x²", "dm": "[0, 1]", "kc": 0}, {"fn": "x²", "dm": "the whole real line", "kc": 1}, {"fn": "1/x", "dm": "(0, 1)", "kc": 1}, {"fn": "1/x", "dm": "[1, ∞)", "kc": 0},
           {"fn": "√x", "dm": "[0, ∞)", "kc": 0}, {"fn": "sin x", "dm": "the whole real line", "kc": 0}, {"fn": "sin(1/x)", "dm": "(0, 1)", "kc": 1}, {"fn": "eˣ", "dm": "the whole real line", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="A bounded derivative is enough (sin x, 1/x on [1, ∞)); so is continuity on a closed bounded interval. Unbounded slope on an unbounded domain (x², eˣ) or wild behaviour at an open end (1/x, sin(1/x) near 0) breaks it. √x is uniformly continuous although its slope is unbounded at 0"),
       N("ra-lipschitz", CN, "Find the smallest Lipschitz constant of f(x) = {{sh}} on [{{ka}}, {{kb}}].", "kans", "calc(vy)",
         "By the mean value theorem the best constant is the largest value of |f′| on the interval", tex="L", final=False,
         cases=[{"sh": "x²", "ka": 0, "kb": 3, "kans": 6, "vy": "Max(Abs(diff(Y**2, Y).subs(Y, 0)), Abs(diff(Y**2, Y).subs(Y, 3)))"},
                {"sh": "x³", "ka": 1, "kb": 2, "kans": 12, "vy": "Max(Abs(diff(Y**3, Y).subs(Y, 1)), Abs(diff(Y**3, Y).subs(Y, 2)))"},
                {"sh": "1/x", "ka": 2, "kb": 5, "kans": 0.25, "vy": "Max(Abs(diff(1/Y, Y).subs(Y, 2)), Abs(diff(1/Y, Y).subs(Y, 5)))"},
                {"sh": "√x", "ka": 4, "kb": 9, "kans": 0.25, "vy": "Max(Abs(diff(sqrt(Y), Y).subs(Y, 4)), Abs(diff(sqrt(Y), Y).subs(Y, 9)))"},
                {"sh": "e^(2x)", "ka": 0, "kb": 1, "kans": 14.7781122, "vy": "Max(Abs(diff(exp(2*Y), Y).subs(Y, 0)), Abs(diff(exp(2*Y), Y).subs(Y, 1)))"}])])]),
 }),
 5: ("calculus", "Differentiation and integration", A("A3", "A5"), ["HYP", "EPS"], {
   1: ("The theorems behind calculus", [
     ("A", A("A3"), "Find the point the mean value theorem promises and say what Rolle's theorem needs.",
      "If f is continuous on [a, b] and differentiable inside, some c has f′(c) = (f(b) − f(a))/(b − a). Rolle is the case f(a) = f(b).", "P1", [
       N("ra-mvt-point", CL, "For f(x) = x³ on [0, {{kb}}], find the c in (0, {{kb}}) with f′(c) equal to the average slope.", "kb/sqrt(3)", "Max(*solve(Eq(diff(Y**3, Y), (kb**3 - 0)/kb), Y))",
         "The average slope is b², so 3c² = b² and c = b/√3", tex="c", final=False,
         given={"kb": {"pick": [1, 2, 3, 6]}}),
       F("ra-mvt-facts", CL, [
           ("f(x) = |x| on [−1, 1] has f(−1) = f(1) but no point with f′(c) = 0. Which hypothesis of Rolle's theorem fails?", "Differentiability inside the interval", "Continuity on the closed interval", "Equal end values", "Boundedness"),
           ("If f′(x) = 0 for every x in an interval, the mean value theorem shows f is:", "Constant", "Linear", "Zero", "Periodic"),
           ("If |f′(x)| ≤ M on an interval, then |f(x) − f(y)| is at most:", "M|x − y|", "M", "M(x − y)²", "|x − y|/M"),
           ("If f′ > 0 on an interval, then f is:", "Strictly increasing", "Convex", "Positive", "Bounded")],
         "Almost every 'derivative tells you about the function' fact is the mean value theorem applied to two points")]),
     ("B", A("A3"), "Bound a Taylor remainder with Lagrange's form.",
      "f(x) = Taylor polynomial of degree n + R_n, with R_n = f⁽ⁿ⁺¹⁾(c) x^(n+1)/(n + 1)! for some c between 0 and x. For e^x at x = 1, |R_n| < 3/(n + 1)!.", "P1", [
       N("ra-taylor-degree", CL, "Using |R_n| < 3/(n + 1)! for e at x = 1, what is the smallest degree n that guarantees an error below {{sh}}?", "kans", "pm_first_n('3/factorial(n + 1)', 0, kt)",
         "Tabulate 3/(n + 1)!: 3/2, 1/2, 1/8, 1/40, 1/240, 1/1680, 1/13440, … and stop at the first value below the tolerance", tex="n",
         cases=[{"sh": s, "kt": t, "kans": taylor_n(t)} for s, t in [("0.01", 0.01), ("0.001", 0.001), ("0.0001", 0.0001), ("0.000001", 0.000001)]]),
       N("ra-taylor-bound", CL, "Bound the error of sin x ≈ x − x³/6 at x = {{kx}} by the next term's Lagrange bound, x⁵/5!.", "kx^5/120", "nsimplify(kx)**5/factorial(5)",
         "Every derivative of sin is at most 1 in size, so the remainder after the x⁴ term (which is zero) is at most x⁵/120", tex="|R|", final=False,
         given={"kx": {"pick": [0.1, 0.5, 1, 2]}})]),
     ("C", A("A5"), "Compute upper and lower Riemann sums and say which functions are integrable.",
      "For an increasing f on n equal pieces, the upper sum uses right endpoints and the lower sum left endpoints, and U − L = (f(b) − f(a))(b − a)/n → 0. Monotone and continuous functions are integrable; the indicator of the rationals is not.", "P1", [
       N("ra-upper-sum", CL, "Find the upper Riemann sum of f(x) = x² on [0, 1] with {{kn}} equal subintervals.", "(kn + 1)*(2*kn + 1)/(6*kn^2)", "pm_upper_sum('t**2', 0, 1, kn)",
         "Right endpoints give (1/n) Σ (k/n)² = (n + 1)(2n + 1)/(6n²), which decreases to 1/3", tex="U", final=False,
         given={"kn": {"pick": [2, 4, 5, 10]}}),
       N("ra-upper-minus-lower", CL, "For f(x) = {{sh}} on [{{ka}}, {{kb}}] with {{kn}} equal subintervals, find the upper sum minus the lower sum.", "kans", "pm_upper_sum(py, ka, kb, kn) - pm_lower_sum(py, ka, kb, kn)",
         "For an increasing function everything cancels except the end values: U − L = (f(b) − f(a))(b − a)/n. This is the proof that monotone functions are integrable", tex="U-L", final=False,
         cases=[{"sh": "x²", "py": "t**2", "ka": 0, "kb": 2, "kn": 4, "kans": 2}, {"sh": "x³", "py": "t**3", "ka": 0, "kb": 1, "kn": 5, "kans": 0.2},
                {"sh": "√x", "py": "sqrt(t)", "ka": 0, "kb": 4, "kn": 8, "kans": 1}, {"sh": "x²", "py": "t**2", "ka": 1, "kb": 3, "kn": 10, "kans": 1.6},
                {"sh": "2x + 1", "py": "2*t + 1", "ka": 0, "kb": 5, "kn": 10, "kans": 5}])]),
     ("D", A("A5"), "Decide whether an improper integral converges and evaluate it.",
      "∫₁^∞ x^(−p) dx converges exactly when p > 1, to 1/(p − 1); ∫₀¹ x^(−p) dx converges exactly when p < 1, to 1/(1 − p). Comparison with these settles most cases.", "P1", [
       N("ra-improper-value", CL, "Evaluate ∫ x^(−{{kp}}) dx from 1 to ∞.", "1/(kp - 1)", "integrate(Y**(-nsimplify(kp)), (Y, 1, oo))",
         "The antiderivative x^(1−p)/(1 − p) tends to 0 at infinity because p > 1, leaving 1/(p − 1)", tex="I", final=False,
         given={"kp": {"pick": [2, 3, 1.5, 5]}}),
       Q("ra-improper-converges", CL, "Does ∫ {{sh}} converge?", pace="recall", cases=[
           {"sh": "1/x dx from 1 to ∞", "kc": 1}, {"sh": "1/x² dx from 1 to ∞", "kc": 0}, {"sh": "1/√x dx from 0 to 1", "kc": 0}, {"sh": "1/x dx from 0 to 1", "kc": 1},
           {"sh": "1/x² dx from 0 to 1", "kc": 1}, {"sh": "e^(−x) dx from 0 to ∞", "kc": 0}, {"sh": "1/√x dx from 1 to ∞", "kc": 1}, {"sh": "1/(x² + 1) dx over the whole real line", "kc": 0},
           {"sh": "sin(x)/x² dx from 1 to ∞", "kc": 0}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="At infinity the power must beat 1/x; at 0 it must lose to 1/x. The borderline 1/x diverges at both ends, logarithmically")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
