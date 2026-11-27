"""Real Analysis, the intermediate steps (Nov 2026): 17 objectives between the ones draft 1 jumped across —
inequalities before suprema, limit rules before epsilon-N, partial sums before convergence tests, limits of functions
before continuity, the difference quotient before the mean value theorem. NEEDS wires every Real Analysis objective,
old and new, so the path puts the small steps first. Basis unchanged: the Cambridge Analysis I and II schedules."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ra-steps", "real-analysis", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
RL, SQ, SR, CN, CL = "ra.reals", "ra.sequences", "ra.series", "ra.continuity", "ra.calculus"
A = lambda *s: [f"cambridge-ia-analysis-i:{x}" for x in s]
NS = lambda *s: [f"cambridge-ia-numbers-sets:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


TOPICS = {"1.2": "Inequalities and bounds", "2.2": "Limits by the rules", "3.2": "Series from the ground up", "4.2": "Limits of functions", "5.2": "The derivative from its definition"}
OBJS = [
 ("RA-1.2.A", NS("N5"), "Turn an absolute-value inequality into an interval and use the triangle inequality.", "|x − a| < r means a − r < x < a + r. The triangle inequality |x + y| ≤ |x| + |y| and its reverse ||x| − |y|| ≤ |x − y| are the two tools nearly every estimate in analysis uses."),
 ("RA-1.2.B", NS("N5"), "Find upper and lower bounds of a set and say whether it is bounded.", "An upper bound is any number at least as large as every element; the infimum is the greatest lower bound. A set is bounded when it has both kinds."),
 ("RA-1.2.C", NS("N5"), "Use the AM-GM and Bernoulli inequalities to bound an expression.", "For positive numbers the arithmetic mean is at least the geometric mean, with equality only when they are equal; so x + k/x ≥ 2√k. Bernoulli: (1 + x)ⁿ ≥ 1 + nx for x ≥ −1."),
 ("RA-2.2.A", A("A1"), "Find a limit with the algebra of limits and the squeeze rule.", "Limits respect sums, products and quotients (non-zero denominator). If a_n ≤ b_n ≤ c_n and the outer two share a limit, so does b_n: bounded × null is null."),
 ("RA-2.2.B", A("A1"), "Use subsequences to show a sequence diverges and count its subsequential limits.", "Every subsequence of a convergent sequence has the same limit, so two subsequences with different limits prove divergence."),
 ("RA-2.2.C", A("A1"), "Rank the growth of standard sequences.", "For large n: logarithms ≪ powers of n ≪ exponentials cⁿ (c > 1) ≪ n! ≪ nⁿ. The ratio of a slower to a faster one tends to 0."),
 ("RA-2.2.D", A("A1"), "Test a sequence against the Cauchy criterion.", "A sequence is Cauchy when |a_m − a_n| can be made small for all large m and n together, not just neighbours. The harmonic sums fail: s_2n − s_n ≥ 1/2 for every n."),
 ("RA-3.2.A", A("A1"), "Compute partial sums and apply the nth-term test.", "A series converges when its partial sums do. If the terms do not tend to 0 the series diverges; if they do, the test says nothing."),
 ("RA-3.2.B", A("A1"), "Decide convergence by comparison with a p-series.", "For positive terms, a series behaves like Σ 1/nᵖ when its terms are comparable to 1/nᵖ, and that converges exactly when p > 1. For a ratio of polynomials, p is the degree gap."),
 ("RA-3.2.C", A("A1"), "Bound the error of an alternating series and of a p-series tail.", "For an alternating series with terms decreasing to 0, the error after n terms is at most the next term. For Σ 1/kᵖ the tail after n terms is at most ∫ₙ^∞ x⁻ᵖ dx = 1/((p − 1)nᵖ⁻¹)."),
 ("RA-3.2.D", A("A1"), "Say what absolute convergence allows that conditional convergence does not.", "An absolutely convergent series can be rearranged freely with the same sum. A conditionally convergent one can be rearranged to converge to any number, or to diverge (Riemann)."),
 ("RA-4.2.A", A("A2"), "Find one-sided limits and classify a discontinuity.", "A limit exists when both one-sided limits exist and agree. Agree but differ from the value: removable. Exist but differ: jump. One fails to exist as a finite number: essential."),
 ("RA-4.2.B", A("A2"), "Evaluate standard limits of functions and use sequences to show a limit fails.", "sin x / x → 1, (1 − cos x)/x² → 1/2 and (eˣ − 1)/x → 1 as x → 0. f(x) → L exactly when f(x_n) → L for every sequence x_n → a; two sequences with different outcomes show there is no limit."),
 ("RA-4.2.C", A("A2"), "Locate the points where a function is continuous.", "Sums, products, quotients (non-zero denominator) and compositions of continuous functions are continuous. Step functions jump at their break points; a function can even be continuous at exactly one point."),
 ("RA-5.2.A", A("A3"), "Compute a derivative from the difference quotient and decide differentiability at a point.", "f′(a) = lim (f(a + h) − f(a))/h. Differentiable implies continuous but not conversely: |x| has a corner and ∛x a vertical tangent at 0."),
 ("RA-5.2.B", A("A3"), "Evaluate an indeterminate limit by L'Hôpital's rule or a Taylor expansion.", "For 0/0 or ∞/∞ forms, lim f/g = lim f′/g′ when the latter exists. Expanding numerator and denominator to the first non-vanishing order gives the same answer and shows why."),
 ("RA-5.2.C", A("A3"), "Differentiate an inverse function.", "If f is differentiable with f′(a) ≠ 0 and b = f(a), then (f⁻¹)′(b) = 1/f′(a): the graph is reflected in the diagonal, so slopes are reciprocated."),
]
ADD = [
 ("RA-1.2.A", N("ra-abs-interval", RL, "What is the largest x satisfying |{{ka}}x − {{kb}}| ≤ {{kc}}?", "(kb + kc)/ka", "Max(solve(Eq(ka*Y - kb, kc), Y)[0], solve(Eq(ka*Y - kb, -kc), Y)[0])",
    "The inequality says −c ≤ ax − b ≤ c, so x runs from (b − c)/a to (b + c)/a", tex="x",
    given={"ka": {"pick": [2, 3, 4]}, "kb": {"pick": [1, 3, 5]}, "kc": {"pick": [7, 9, 11]}})),
 ("RA-1.2.A", F("ra-triangle-inequality", RL, [
    ("If |x − 2| < 0.1 and |y − 2| < 0.1, the triangle inequality guarantees |x − y| is less than:", "0.2", "0.1", "0.01", "0.4"),
    ("If |x| ≤ 3 and |y| ≤ 5, the largest possible value of |x − y| is:", "8", "2", "15", "5"),
    ("The reverse triangle inequality says ||x| − |y|| is at most:", "|x − y|", "|x| + |y|", "|xy|", "|x| − |y|"),
    ("If |x − 5| < 1, then |x| is less than:", "6", "4", "5", "1")],
    "Insert a middle point: |x − y| ≤ |x − 2| + |2 − y|. Almost every ε-proof is this move")),
 ("RA-1.2.B", N("ra-infimum", RL, "Find the infimum of the set {{st}}.", "kans", "calc(vy)",
    "Look for the smallest value the set reaches or approaches, and check nothing larger is still a lower bound", tex="\\inf",
    cases=[{"st": "{2 + 1/n : n = 1, 2, 3, …}", "kans": 2, "vy": "limit(2 + 1/nn, nn, oo)"}, {"st": "{n + 4/n : n = 1, 2, 3, …}", "kans": 4, "vy": "Min(5, 4, 3 + Rational(4, 3), 5, 5 + Rational(4, 5))"},
           {"st": "{x² − 4x + 7 : x real}", "kans": 3, "vy": "(Y**2 - 4*Y + 7).subs(Y, solve(diff(Y**2 - 4*Y + 7, Y), Y)[0])"}, {"st": "{(n + 1)/n : n = 1, 2, 3, …}", "kans": 1, "vy": "limit((nn + 1)/nn, nn, oo)"},
           {"st": "{3 − 1/n : n = 1, 2, 3, …}", "kans": 2, "vy": "3 - 1"}, {"st": "{eˣ + 1 : x real}", "kans": 1, "vy": "limit(exp(Y) + 1, Y, -oo)"}])),
 ("RA-1.2.B", Q("ra-bounded-how", RL, "The set {{st}} is:", pace="recall", cases=[
    {"st": "{1/n : n ≥ 1}", "kc": 0}, {"st": "the natural numbers", "kc": 1}, {"st": "{x real : x < 5}", "kc": 2}, {"st": "the integers", "kc": 3},
    {"st": "{(−1)ⁿ n : n ≥ 1}", "kc": 3}, {"st": "{sin n : n ≥ 1}", "kc": 0}, {"st": "{n² : n ≥ 1}", "kc": 1}, {"st": "{−eˣ : x real}", "kc": 2}],
    choice=["Bounded", "Bounded below only", "Bounded above only", "Unbounded in both directions"], correct="kc", verify="authored",
    explain="Ask separately whether some number sits above everything and whether some number sits below everything")),
 ("RA-1.2.C", N("ra-am-gm-minimum", RL, "Find the minimum value of x + {{kk}}/x for x > 0.", "2*sqrt(kk)", "(Y + kk/Y).subs(Y, Max(*solve(diff(Y + kk/Y, Y), Y)))",
    "AM-GM on x and k/x: their sum is at least 2√(x · k/x) = 2√k, with equality when x = √k", tex="minimum",
    given={"kk": {"pick": [4, 9, 16, 2, 5]}})),
 ("RA-1.2.C", F("ra-inequality-facts", RL, [
    ("For positive a and b, (a + b)/2 compared with √(ab) is always:", "At least as large", "At most as large", "Equal", "Unrelated"),
    ("Bernoulli's inequality gives (1.01)¹⁰⁰ ≥:", "2", "1.01", "100", "1.1"),
    ("Equality holds in the AM-GM inequality exactly when the numbers are:", "All equal", "All positive", "Integers", "Reciprocals"),
    ("A rectangle of perimeter 20 has area at most:", "25", "20", "100", "50")],
    "With sides x and 10 − x, AM-GM gives x(10 − x) ≤ 5²: the square wins")),
 ("RA-2.2.A", N("ra-squeeze-limit", SQ, "Find the limit of ({{ka}}n + sin n)/({{kb}}n) as n → ∞.", "ka/kb", "limit((ka*nn + 1)/(kb*nn), nn, oo)",
    "sin n is trapped between −1 and 1, so the sequence is squeezed between (an − 1)/(bn) and (an + 1)/(bn), which share the limit a/b", tex="\\lim",
    given={"ka": {"pick": [1, 3, 5]}, "kb": {"pick": [2, 4]}})),
 ("RA-2.2.A", F("ra-limit-algebra-facts", SQ, [
    ("If a_n → 3 and b_n → 0 with b_n ≠ 0, then a_n/b_n:", "Has no finite limit", "Tends to 0", "Tends to 3", "Tends to 1"),
    ("If a_n is bounded and b_n → 0, then a_n b_n:", "Tends to 0", "Is unbounded", "Need not converge", "Tends to the bound of a_n"),
    ("If a_n + b_n converges and a_n converges, then b_n:", "Converges", "May diverge", "Is constant", "Tends to 0"),
    ("If a_n b_n converges and a_n converges, then b_n:", "May diverge, for example when a_n → 0", "Converges", "Is bounded", "Tends to 1"),
    ("cos(n)/n tends to 0 by:", "The squeeze rule", "The ratio test", "Monotone convergence", "It does not converge")],
    "The algebra of limits works forwards; going backwards you can subtract but you cannot divide by something tending to 0")),
 ("RA-2.2.B", N("ra-subsequential-limits", SQ, "How many different limits do the convergent subsequences of a_n = {{sh}} have?", "kans", "pm_distinct_values(py, 48)",
    "The sequence is periodic, so list one period: each value that recurs is the limit of the subsequence that keeps hitting it", tex="limits", final=True,
    cases=[{"sh": "(−1)ⁿ", "py": "(-1)**n", "kans": 2}, {"sh": "sin(nπ/2)", "py": "sin(n*pi/2)", "kans": 3}, {"sh": "cos(nπ/3)", "py": "cos(n*pi/3)", "kans": 4},
           {"sh": "the remainder of n on division by 4", "py": "n % 4", "kans": 4}, {"sh": "sin(nπ/3)", "py": "sin(n*pi/3)", "kans": 3}, {"sh": "cos(nπ/2)", "py": "cos(n*pi/2)", "kans": 3}])),
 ("RA-2.2.B", Q("ra-converge-or-diverge", SQ, "Does a_n = {{sh}} converge?", pace="recall", cases=[
    {"sh": "(−1)ⁿ", "kc": 1}, {"sh": "(−1)ⁿ/n", "kc": 0}, {"sh": "sin(nπ/2)", "kc": 1}, {"sh": "1/n for even n and 1/n² for odd n", "kc": 0},
    {"sh": "n for even n and 1/n for odd n", "kc": 1}, {"sh": "(−1)ⁿ n/(n + 1)", "kc": 1}, {"sh": "1 + (−1)ⁿ/n²", "kc": 0}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Compare the even and odd subsequences: if they have different limits, or one is unbounded, the sequence diverges; if every such piece has the same limit it converges")),
 ("RA-2.2.C", Q("ra-growth-ratio", SQ, "As n → ∞, the ratio {{sh}} tends to:", pace="recall", cases=[
    {"sh": "n¹⁰⁰/2ⁿ", "kc": 0}, {"sh": "2ⁿ/n!", "kc": 0}, {"sh": "n!/nⁿ", "kc": 0}, {"sh": "(ln n)/√n", "kc": 0}, {"sh": "3ⁿ/2ⁿ", "kc": 2},
    {"sh": "(2n² + 1)/(n² + n)", "kc": 1}, {"sh": "n!/100ⁿ", "kc": 2}, {"sh": "√(4n² + n)/n", "kc": 1}, {"sh": "n/(ln n)¹⁰", "kc": 2}],
    choice=["0", "A finite non-zero number", "Infinity"], correct="kc", verify="authored",
    explain="Logarithms lose to powers, powers lose to exponentials, exponentials lose to factorials, and factorials lose to nⁿ, whatever the constants")),
 ("RA-2.2.C", F("ra-growth-order", SQ, [
    ("Which grows fastest as n → ∞?", "n!", "2ⁿ", "n¹⁰", "n ln n"),
    ("Which grows slowest as n → ∞?", "ln n", "√n", "n/ln n", "n^0.1"),
    ("Which grows fastest as n → ∞?", "nⁿ", "n!", "10ⁿ", "n¹⁰⁰⁰"),
    ("n^(1/n) tends to:", "1", "0", "e", "Infinity"),
    ("(1 + 1/n)ⁿ tends to:", "e", "1", "Infinity", "2")],
    "Take logarithms when in doubt: ln(n!) is about n ln n, while ln(cⁿ) is only n ln c")),
 ("RA-2.2.D", N("ra-harmonic-block", SQ, "Let s_n = 1 + 1/2 + … + 1/n. Compute s_{{km}} − s_{{kn}}.", "kans", "summation(1/nn, (nn, kn + 1, km))",
    "The block has n terms each at least 1/(2n), so it is at least 1/2 however far out you go. That is why the harmonic sums are not Cauchy", tex="s_{2n}-s_n",
    cases=[{"kn": 1, "km": 2, "kans": 0.5}, {"kn": 2, "km": 4, "kans": 0.58333333}, {"kn": 3, "km": 6, "kans": 0.61666667}, {"kn": 4, "km": 8, "kans": 0.63452381}])),
 ("RA-2.2.D", F("ra-cauchy-facts", SQ, [
    ("A sequence with |a_(n+1) − a_n| → 0 is:", "Not necessarily Cauchy", "Always Cauchy", "Always convergent", "Always bounded"),
    ("Every Cauchy sequence of real numbers is:", "Convergent", "Monotone", "Eventually constant", "Rational"),
    ("Every convergent sequence is:", "Cauchy", "Monotone", "Positive", "Periodic"),
    ("A Cauchy sequence of rationals can fail to converge in the rationals because the rationals are not:", "Complete", "Dense", "Ordered", "Countable"),
    ("If |a_(n+1) − a_n| ≤ 1/2ⁿ for all n, the sequence is Cauchy because the gaps:", "Have a convergent sum", "Tend to 0", "Are positive", "Alternate in sign")],
    "Small steps are not enough; the steps must be summable. √n has steps tending to 0 and still runs off to infinity")),
 ("RA-3.2.A", N("ra-partial-sum", SR, "Find the partial sum 1/(1·2) + 1/(2·3) + … + 1/({{kn}}·{{km}}).", "kn/(kn + 1)", "summation(1/(nn*(nn + 1)), (nn, 1, kn))",
    "Each term is 1/k − 1/(k + 1), so the sum telescopes to 1 − 1/(n + 1)", tex="S_n",
    cases=[{"kn": n, "km": n + 1} for n in (4, 9, 19, 99)])),
 ("RA-3.2.A", Q("ra-nth-term-test", SR, "For Σ {{sh}}, the nth-term test:", pace="recall", cases=[
    {"sh": "n/(2n + 1)", "kc": 0}, {"sh": "1/n", "kc": 1}, {"sh": "(−1)ⁿ", "kc": 0}, {"sh": "1/n²", "kc": 1}, {"sh": "cos(1/n)", "kc": 0}, {"sh": "1/√n", "kc": 1}, {"sh": "n sin(1/n)", "kc": 0}],
    choice=["Shows the series diverges", "Is inconclusive"], correct="kc", verify="authored",
    explain="Check whether the terms tend to 0. If not, divergence is certain. If they do, the test is silent: 1/n and 1/n² both pass it, and only one of them converges")),
 ("RA-3.2.B", Q("ra-comparison-degree", SR, "Does Σ {{sh}} converge?", pace="recall", cases=[
    {"sh": "n/(n³ + 1)", "kc": 0}, {"sh": "n²/(n³ + 1)", "kc": 1}, {"sh": "(n + 5)/(n² + 3)", "kc": 1}, {"sh": "1/(n√n)", "kc": 0}, {"sh": "√n/(n² + 1)", "kc": 0},
    {"sh": "1/(2n + 7)", "kc": 1}, {"sh": "(n² + 1)/(n⁴ + n)", "kc": 0}, {"sh": "1/√(n² + 1)", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Keep only the leading powers: the terms behave like 1/nᵖ with p the degree gap, and the series converges exactly when p > 1")),
 ("RA-3.2.B", N("ra-p-threshold", SR, "Σ n^{{ka}}/(n^b + 1) converges exactly when b exceeds what number?", "ka + 1", "solve(Eq(Symbol('m') - ka, 1), Symbol('m'))[0]",
    "The terms behave like 1/n^(b − a), and a p-series converges exactly when p > 1, so b must exceed a + 1", tex="b", final=True,
    given={"ka": {"pick": [1, 2, 3, 5]}})),
 ("RA-3.2.C", N("ra-alternating-terms", SR, "For the alternating series Σ (−1)ⁿ⁺¹/n{{pw}}, what is the least number of terms n for which the error bound, the next term, is below {{kt}}?", "kans", "pm_first_n(py, 0, kt)",
    "The error after n terms is at most the (n + 1)th term, so solve 1/(n + 1)ᵖ < tolerance", tex="n", final=True,
    cases=[{"pw": "", "py": "1/(n + 1)", "kt": 0.01, "kans": 100}, {"pw": "", "py": "1/(n + 1)", "kt": 0.001, "kans": 1000}, {"pw": "²", "py": "1/(n + 1)**2", "kt": 0.01, "kans": 10},
           {"pw": "²", "py": "1/(n + 1)**2", "kt": 0.0001, "kans": 100}, {"pw": "³", "py": "1/(n + 1)**3", "kt": 0.001, "kans": 10}])),
 ("RA-3.2.C", N("ra-integral-tail", SR, "Use the integral test to bound the tail Σ 1/k^{{kp}} for k > {{kn}}.", "1/((kp - 1)*kn^(kp - 1))", "integrate(Y**(-kp), (Y, kn, oo))",
    "The tail after n terms lies under the curve x⁻ᵖ from n onwards, whose area is 1/((p − 1)nᵖ⁻¹)", tex="bound",
    given={"kp": {"pick": [2, 3, 4]}, "kn": {"pick": [5, 10, 100]}})),
 ("RA-3.2.D", F("ra-rearrangement-facts", SR, [
    ("Rearranging the terms of an absolutely convergent series:", "Never changes the sum", "Can change the sum", "Makes it diverge", "Makes it conditionally convergent"),
    ("The alternating harmonic series can be rearranged to converge to:", "Any real number", "Only ln 2", "Only 0 or ln 2", "Only numbers below 1"),
    ("A series that converges but not absolutely is called:", "Conditionally convergent", "Divergent", "Uniformly convergent", "Telescoping"),
    ("If Σ |a_n| converges, then Σ a_n:", "Converges", "May diverge", "Converges to 0", "Is alternating")],
    "A conditionally convergent series has positive and negative parts that each diverge, which is what lets a rearrangement steer the sum anywhere")),
 ("RA-3.2.D", Q("ra-absolute-check", SR, "Is Σ {{sh}} absolutely convergent?", pace="recall", cases=[
    {"sh": "(−1)ⁿ/n²", "kc": 0}, {"sh": "(−1)ⁿ/n", "kc": 1}, {"sh": "sin(n)/n³", "kc": 0}, {"sh": "(−1)ⁿ/√n", "kc": 1}, {"sh": "(−1)ⁿ/2ⁿ", "kc": 0}, {"sh": "(−1)ⁿ/ln(n + 1)", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Drop the signs and test what is left. Only if that series converges may the terms be reordered or grouped freely")),
 ("RA-4.2.A", Q("ra-discontinuity-type", CN, "At x = 0, the function {{fn}} has:", pace="recall", cases=[
    {"fn": "sin(x)/x (undefined at 0)", "kc": 0}, {"fn": "x/|x|", "kc": 1}, {"fn": "1/x", "kc": 2}, {"fn": "sin(1/x)", "kc": 2}, {"fn": "(x² + x)/x", "kc": 0},
    {"fn": "the floor of x", "kc": 1}, {"fn": "e^(−1/x²) (undefined at 0)", "kc": 0}, {"fn": "1/x²", "kc": 2}],
    choice=["A removable discontinuity", "A jump discontinuity", "An essential discontinuity (a one-sided limit fails to exist or is infinite)"], correct="kc", verify="authored",
    explain="Compute the two one-sided limits. Equal and finite: removable. Finite but different: jump. Otherwise essential")),
 ("RA-4.2.A", N("ra-removable-value", CN, "What value must f({{ka}}) be given so that f(x) = (x² − {{kq}})/(x − {{ka}}) is continuous at x = {{ka}}?", "2*ka", "limit((Y**2 - ka**2)/(Y - ka), Y, ka)",
    "Cancel the common factor: the function equals x + a away from the point, so the limit is 2a", tex="f(a)", final=True,
    cases=[{"ka": a, "kq": a * a} for a in (2, 3, 5, 7)])),
 ("RA-4.2.B", N("ra-standard-function-limit", CN, "Find the limit of {{sh}} as x → 0.", "kans", "calc(vy)",
    "Use sin x ≈ x, 1 − cos x ≈ x²/2 and eˣ − 1 ≈ x near 0", tex="\\lim",
    cases=[{"sh": "sin(3x)/x", "kans": 3, "vy": "limit(sin(3*Y)/Y, Y, 0)"}, {"sh": "(1 − cos x)/x²", "kans": 0.5, "vy": "limit((1 - cos(Y))/Y**2, Y, 0)"},
           {"sh": "(e^(2x) − 1)/x", "kans": 2, "vy": "limit((exp(2*Y) - 1)/Y, Y, 0)"}, {"sh": "sin(5x)/sin(2x)", "kans": 2.5, "vy": "limit(sin(5*Y)/sin(2*Y), Y, 0)"},
           {"sh": "tan(4x)/x", "kans": 4, "vy": "limit(tan(4*Y)/Y, Y, 0)"}, {"sh": "(1 − cos(2x))/x²", "kans": 2, "vy": "limit((1 - cos(2*Y))/Y**2, Y, 0)"}])),
 ("RA-4.2.B", F("ra-sequential-criterion", CN, [
    ("sin(1/x) has no limit as x → 0 because along x = 1/(nπ) it is 0 and along x = 1/((2n + 1/2)π) it is:", "1", "0", "−1", "Undefined"),
    ("f(x) → L as x → a exactly when f(x_n) → L for:", "Every sequence x_n → a with no term equal to a", "Some sequence x_n → a", "The sequence a + 1/n only", "Every bounded sequence"),
    ("x sin(1/x) → 0 as x → 0 by:", "The squeeze rule, since |x sin(1/x)| ≤ |x|", "L'Hôpital's rule", "The mean value theorem", "It has no limit"),
    ("To prove a limit does NOT exist it is enough to find:", "Two sequences tending to a with different limits of f", "One sequence along which f converges", "A point where f is undefined", "A sequence along which f is bounded")],
    "The sequential criterion turns questions about functions into questions about sequences, where the earlier unit's tools apply")),
 ("RA-4.2.C", N("ra-floor-jumps", CN, "How many points of discontinuity has the floor of {{kk}}x on the open interval (0, 1)?", "kk - 1", "summation(1, (nn, 1, kk - 1))",
    "The floor jumps where kx passes an integer: at x = 1/k, 2/k, …, (k − 1)/k", tex="points", final=True,
    given={"kk": {"pick": [3, 4, 6, 10]}})),
 ("RA-4.2.C", F("ra-where-continuous", CN, [
    ("The function equal to x for rational x and 0 for irrational x is continuous at:", "0 only", "Every rational", "Every irrational", "No point"),
    ("The function equal to 1 for rational x and 0 for irrational x is continuous at:", "No point", "Every rational", "Every irrational", "0 only"),
    ("1/(x² − 1) is continuous everywhere except at:", "x = 1 and x = −1", "x = 0", "x = 1 only", "No point"),
    ("If f and g are continuous at a, which of these may fail to be continuous at a?", "f/g", "f + g", "fg", "|f|"),
    ("A composition g(f(x)) is continuous at a when f is continuous at a and g is continuous at:", "f(a)", "a", "0", "g(a)")],
    "Near 0 both branches of the first function are small, so it is squeezed to its value there; anywhere else rationals and irrationals pull it apart")),
 ("RA-5.2.A", N("ra-difference-quotient", CL, "Evaluate the limit of ((({{ka}} + h)³ − {{kq}})/h) as h → 0.", "3*ka^2", "limit(((ka + Y)**3 - ka**3)/Y, Y, 0)",
    "Expand: (a + h)³ − a³ = 3a²h + 3ah² + h³; divide by h and let h go to 0. It is the derivative of x³ at a", tex="f'(a)", final=True,
    cases=[{"ka": a, "kq": a ** 3} for a in (1, 2, 3, 5)])),
 ("RA-5.2.A", Q("ra-differentiable-at-zero", CL, "Is f(x) = {{fn}} differentiable at x = 0?", pace="recall", cases=[
    {"fn": "|x|", "kc": 1}, {"fn": "x|x|", "kc": 0}, {"fn": "∛x", "kc": 1}, {"fn": "x² sin(1/x), with f(0) = 0", "kc": 0}, {"fn": "x sin(1/x), with f(0) = 0", "kc": 1},
    {"fn": "√|x|", "kc": 1}, {"fn": "|x|³", "kc": 0}, {"fn": "x^(4/3)", "kc": 0}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Form f(h)/h and ask whether it has a limit. For x² sin(1/x) it is h sin(1/h) → 0; for x sin(1/x) it is sin(1/h), which oscillates")),
 ("RA-5.2.B", N("ra-lhopital", CL, "Find the limit of {{sh}} as x → 0.", "kans", "calc(vy)",
    "Differentiate top and bottom until the form is no longer 0/0, or expand both to the first power that survives", tex="\\lim",
    cases=[{"sh": "(eˣ − 1 − x)/x²", "kans": 0.5, "vy": "limit((exp(Y) - 1 - Y)/Y**2, Y, 0)"}, {"sh": "(x − sin x)/x³", "kans": 0.16666667, "vy": "limit((Y - sin(Y))/Y**3, Y, 0)"},
           {"sh": "(tan x − x)/x³", "kans": 0.33333333, "vy": "limit((tan(Y) - Y)/Y**3, Y, 0)"}, {"sh": "ln(1 + 3x)/x", "kans": 3, "vy": "limit(log(1 + 3*Y)/Y, Y, 0)"},
           {"sh": "(cos x − 1)/x²", "kans": -0.5, "vy": "limit((cos(Y) - 1)/Y**2, Y, 0)"}, {"sh": "(eˣ − e^(−x))/sin x", "kans": 2, "vy": "limit((exp(Y) - exp(-Y))/sin(Y), Y, 0)"}])),
 ("RA-5.2.B", F("ra-lhopital-facts", CL, [
    ("L'Hôpital's rule applies to limits of the form:", "0/0 or ∞/∞", "0 · 1", "1/0", "Any quotient"),
    ("lim (x + sin x)/x as x → ∞ is 1, but the ratio of derivatives (1 + cos x)/1 has no limit. This shows the rule:", "Gives no conclusion when the derivative ratio has no limit", "Is false", "Proves the limit does not exist", "Applies only at 0"),
    ("To use L'Hôpital on the form 0 · ∞ you first:", "Rewrite it as a quotient", "Differentiate each factor", "Take a square root", "Apply the product rule"),
    ("lim x ln x as x → 0⁺ is:", "0", "−∞", "1", "−1")],
    "The rule is a one-way implication: if the derivative ratio has a limit, so does the original, and they agree")),
 ("RA-5.2.C", N("ra-inverse-derivative", CL, "f(x) = x³ + x is increasing, and f({{ka}}) = {{kb}}. Find the derivative of the inverse function at {{kb}}.", "1/(3*ka^2 + 1)", "1/diff(Y**3 + Y, Y).subs(Y, ka)",
    "(f⁻¹)′(b) = 1/f′(a), with a the point that f sends to b", tex="(f^{-1})'(b)",
    cases=[{"ka": a, "kb": a ** 3 + a} for a in (1, 2, 3)])),
 ("RA-5.2.C", N("ra-inverse-derivative-exp", CL, "g is the inverse of f(x) = eˣ + {{kk}}x. Find g′(1), noting that f(0) = 1.", "1/(1 + kk)", "1/diff(exp(Y) + kk*Y, Y).subs(Y, 0)",
    "g′(1) = 1/f′(0), and f′(0) = 1 + k. No formula for g is needed", tex="g'(1)",
    given={"kk": {"pick": [1, 2, 3, 4]}})),
]
NEEDS = {
 "RA-1.2.B": ["RA-1.2.A"], "RA-1.2.C": ["RA-1.2.A"], "RA-1.1.A": ["RA-1.2.B"], "RA-1.1.B": ["RA-1.1.A"],
 "RA-2.2.A": ["RA-1.2.A", "CA-1.2.A"], "RA-2.2.C": ["RA-2.2.A"], "RA-2.1.A": ["RA-2.2.A", "RA-1.1.B", "DM-1.1.B"], "RA-2.2.B": ["RA-2.1.A"], "RA-2.1.B": ["RA-2.2.B", "RA-1.1.A"],
 "RA-2.1.C": ["RA-2.2.B"], "RA-2.2.D": ["RA-2.1.B"],
 "RA-3.2.A": ["RA-2.2.A"], "RA-3.2.B": ["RA-3.2.A", "RA-2.2.C"], "RA-3.1.B": ["RA-3.2.A"], "RA-3.1.A": ["RA-3.2.B", "RA-3.2.D"], "RA-3.2.C": ["RA-3.2.B"], "RA-3.2.D": ["RA-3.2.B"],
 "RA-3.1.C": ["RA-3.1.A"],
 "RA-4.2.A": ["RA-2.2.A"], "RA-4.2.B": ["RA-4.2.A", "RA-2.2.B"], "RA-4.2.C": ["RA-4.2.A"], "RA-4.1.A": ["RA-4.2.B", "RA-2.1.A"], "RA-4.1.B": ["RA-4.2.C", "RA-4.1.A"], "RA-4.1.C": ["RA-4.1.B"],
 "RA-5.2.A": ["RA-4.2.B"], "RA-5.1.A": ["RA-5.2.A", "RA-4.1.B"], "RA-5.2.B": ["RA-5.1.A"], "RA-5.2.C": ["RA-5.2.A"], "RA-5.1.B": ["RA-5.2.B", "RA-3.1.C"],
 "RA-5.1.C": ["RA-5.1.A", "RA-2.1.A"], "RA-5.1.D": ["RA-5.1.C", "RA-3.2.C"],
 "RA-6.1.A": ["RA-4.1.C", "RA-1.1.A"], "RA-6.1.B": ["RA-6.1.A", "RA-3.1.A"], "RA-6.2.A": ["RA-1.2.A"], "RA-6.2.B": ["RA-6.2.A", "RA-2.2.D"], "RA-6.2.C": ["RA-6.2.B", "RA-4.1.C"], "RA-6.2.D": ["RA-5.1.B"],
}
