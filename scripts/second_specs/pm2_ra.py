"""Real Analysis unit 6 (Nov 2026): uniform convergence, metric spaces, completeness and the contraction mapping
theorem, on the Cambridge Part IB Analysis II schedule (read through an extraction of the 2026-27 Schedules)."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ra-analysis-2", "real-analysis", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
MT = "ra.metric"
B = ["cambridge-ib-analysis-ii:U", "cambridge-ib-analysis-ii:M", "cambridge-ib-analysis-ii:D", "cambridge-ib-analysis-ii:C"]
U, M, D, C = ([x] for x in B)


def F(name, rows, explain):
    return Q(name, MT, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, MT, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


UNITS = {"6": ("metric", "Uniform convergence and metric spaces", ["EPS", "HYP"], B)}
TOPICS = {"6.1": "Uniform convergence", "6.2": "Metric spaces, completeness and contractions"}
OBJS = [
 ("RA-6.1.A", U, "Measure how far a sequence of functions is from its limit in the uniform norm and decide whether convergence is uniform.",
  "f_n → f uniformly when sup |f_n − f| → 0. Pointwise convergence lets the worst point move with n; uniform convergence does not. A uniform limit of continuous functions is continuous."),
 ("RA-6.1.B", U, "Apply the Weierstrass M-test and say what uniform convergence lets you exchange.",
  "If |f_n(x)| ≤ M_n for all x and Σ M_n converges, then Σ f_n converges uniformly. Uniform convergence allows a limit to pass through an integral, and through a derivative when the derivatives converge uniformly."),
 ("RA-6.2.A", M, "Compute distances in the standard norms on Rⁿ and compare the norms.",
  "‖x‖₁ = Σ|x_i|, ‖x‖₂ = √Σx_i², ‖x‖∞ = max|x_i|, with ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁ ≤ n‖x‖∞. All norms on a finite-dimensional space are Lipschitz equivalent, so they give the same open sets."),
 ("RA-6.2.B", C, "Decide whether a metric space is complete and say what completeness buys.",
  "A space is complete when every Cauchy sequence converges in it. Rⁿ and C[a, b] with the uniform norm are complete; the rationals and an open interval are not. A closed subset of a complete space is complete."),
 ("RA-6.2.C", C, "Apply the contraction mapping theorem: find the contraction constant and bound the error of the iteration.",
  "If d(f(x), f(y)) ≤ k d(x, y) with k < 1 on a complete space, f has exactly one fixed point, and the iterates satisfy d(x_n, x*) ≤ kⁿ d(x₁, x₀)/(1 − k). Picard's theorem for ODEs is this theorem in C[a, b]."),
 ("RA-6.2.D", D, "Classify a critical point of a function of two variables from its Hessian.",
  "At a critical point, a positive-definite Hessian is a local minimum, negative-definite a local maximum, indefinite a saddle; a zero determinant leaves the test undecided. Mixed partials agree when they are continuous."),
]
ADD = [
 ("RA-6.1.A", N("ra-sup-norm", "Find sup |f_n(x) − f(x)| on {{dm}} for f_n(x) = {{sh}} and its pointwise limit f, at n = {{kn}}.", "kans", "calc(vy)",
    "Find where |f_n − f| is largest: at an endpoint, or where its derivative vanishes. Convergence is uniform exactly when this supremum tends to 0", tex="\\sup|f_n-f|",
    cases=[{"dm": "[0, 1/2]", "sh": "xⁿ", "kn": 3, "kans": 0.125, "vy": "Rational(1, 2)**3"},
           {"dm": "[0, 1]", "sh": "x/(1 + nx²)", "kn": 4, "kans": 0.25, "vy": "(Y/(1 + 4*Y**2)).subs(Y, Max(*solve(diff(Y/(1 + 4*Y**2), Y), Y)))"},
           {"dm": "[0, 1]", "sh": "x/n", "kn": 5, "kans": 0.2, "vy": "Rational(1, 5)"},
           {"dm": "[0, 1]", "sh": "xⁿ(1 − x)", "kn": 2, "kans": 0.14814815, "vy": "(Y**2*(1 - Y)).subs(Y, Max(*solve(diff(Y**2*(1 - Y), Y), Y)))"},
           {"dm": "[0, ∞)", "sh": "x e^(−nx)", "kn": 2, "kans": 0.18393972, "vy": "(Y*exp(-2*Y)).subs(Y, solve(diff(Y*exp(-2*Y), Y), Y)[0])"}])),
 ("RA-6.1.A", Q("ra-uniform-or-pointwise", MT, "On {{dm}}, the sequence f_n(x) = {{sh}} converges:", pace="recall", cases=[
    {"dm": "[0, 1]", "sh": "xⁿ", "kc": 1}, {"dm": "[0, 1/2]", "sh": "xⁿ", "kc": 0}, {"dm": "the real line", "sh": "x/n", "kc": 1}, {"dm": "[0, 1]", "sh": "x/n", "kc": 0},
    {"dm": "the real line", "sh": "sin(nx)/n", "kc": 0}, {"dm": "[0, 1]", "sh": "nx/(1 + n²x²)", "kc": 1}, {"dm": "[0, 1]", "sh": "x/(1 + nx²)", "kc": 0}],
    choice=["Uniformly", "Pointwise but not uniformly"], correct="kc", verify="authored",
    explain="xⁿ on [0, 1] has a discontinuous limit, so the convergence cannot be uniform. nx/(1 + n²x²) takes the value 1/2 at x = 1/n for every n, so its supremum never shrinks")),
 ("RA-6.1.B", N("ra-m-test-bound", "The M-test bounds Σ cos(nx)/n^{{kp}} (n from 1 to ∞) by Σ 1/n^{{kp}}. Evaluate that bounding sum.", "kans", "summation(1/nn**kp, (nn, 1, oo))",
    "|cos(nx)/n^p| ≤ 1/n^p for every x, and Σ 1/n^p converges for p > 1, so the series converges uniformly on the whole real line and its sum is continuous", tex="\\sum M_n",
    cases=[{"kp": 2, "kans": 1.64493407}, {"kp": 4, "kans": 1.08232323}, {"kp": 6, "kans": 1.01734306}])),
 ("RA-6.1.B", F("ra-exchange-facts", [
    ("f_n is n on (0, 1/n) and 0 elsewhere on [0, 1]. Then f_n → 0 pointwise, but ∫ f_n = 1 for every n. This is possible because the convergence is not:", "Uniform", "Pointwise", "Monotone", "Bounded below"),
    ("A uniform limit of continuous functions is always:", "Continuous", "Differentiable", "Constant", "Monotone"),
    ("f_n(x) = sin(nx)/√n converges uniformly to 0, yet f_n′ does not converge. So uniform convergence of f_n does not control:", "The derivatives", "The integrals", "Continuity of the limit", "Boundedness"),
    ("A power series converges uniformly on:", "Every closed disc strictly inside its disc of convergence", "Its whole open disc of convergence, always", "The boundary circle", "No set containing its centre"),
    ("If f_n → f uniformly on [a, b] and each f_n is Riemann integrable, then the integral of f_n tends to:", "The integral of f", "0", "sup f", "It need not converge")],
    "Uniform convergence passes limits through integrals for free and through continuity for free; for derivatives you need the derivatives themselves to converge uniformly")),
 ("RA-6.2.A", N("ra-norm-distance", "In R³, find the distance between ({{a1}}, {{a2}}, {{a3}}) and the origin in the {{nm}} norm.", "kans", "calc(vy)",
    "ℓ¹ adds the absolute values, ℓ² is the Euclidean length, ℓ∞ takes the largest absolute value", tex="\\|x\\|",
    cases=[{"a1": 3, "a2": -4, "a3": 12, "nm": "ℓ²", "kans": 13, "vy": "sqrt(3**2 + 4**2 + 12**2)"}, {"a1": 3, "a2": -4, "a3": 12, "nm": "ℓ¹", "kans": 19, "vy": "Abs(3) + Abs(-4) + Abs(12)"},
           {"a1": 3, "a2": -4, "a3": 12, "nm": "ℓ∞", "kans": 12, "vy": "Max(Abs(3), Abs(-4), Abs(12))"}, {"a1": 2, "a2": -6, "a3": 9, "nm": "ℓ²", "kans": 11, "vy": "sqrt(2**2 + 6**2 + 9**2)"},
           {"a1": 2, "a2": -6, "a3": 9, "nm": "ℓ¹", "kans": 17, "vy": "Abs(2) + Abs(-6) + Abs(9)"}, {"a1": 1, "a2": -2, "a3": 2, "nm": "ℓ²", "kans": 3, "vy": "sqrt(1 + 4 + 4)"}])),
 ("RA-6.2.A", N("ra-norm-ratio", "What is the largest possible value of ‖x‖₁/‖x‖₂ for a non-zero vector x in R^{{kn}}?", "sqrt(kn)", "Matrix.ones(kn, 1).norm(1)/Matrix.ones(kn, 1).norm(2)",
    "By Cauchy-Schwarz ‖x‖₁ ≤ √n ‖x‖₂, with equality when every coordinate has the same size. Constants like this are what Lipschitz equivalence of norms means", tex="ratio",
    given={"kn": {"pick": [2, 3, 4, 9]}})),
 ("RA-6.2.B", Q("ra-complete-or-not", MT, "Is this metric space complete: {{sp}}?", pace="recall", cases=[
    {"sp": "the rationals with the usual distance", "kc": 1}, {"sp": "the closed interval [0, 1]", "kc": 0}, {"sp": "the open interval (0, 1)", "kc": 1}, {"sp": "Rⁿ with the Euclidean distance", "kc": 0},
    {"sp": "C[0, 1] with the uniform norm", "kc": 0}, {"sp": "C[0, 1] with the norm ∫|f|", "kc": 1}, {"sp": "the integers with the usual distance", "kc": 0}, {"sp": "the polynomials on [0, 1] with the uniform norm", "kc": 1}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Find a Cauchy sequence whose limit has left the space: rationals approaching √2, 1/n in (0, 1), Taylor polynomials approaching eˣ, continuous ramps approaching a step in the integral norm. In the integers a Cauchy sequence is eventually constant")),
 ("RA-6.2.B", F("ra-completeness-uses", [
    ("A closed subset of a complete metric space is:", "Complete", "Compact", "Open", "Bounded"),
    ("Completeness is not a topological property: (0, 1) and the real line are homeomorphic, but only one is complete. The complete one is:", "The real line", "(0, 1)", "Both", "Neither"),
    ("A uniformly Cauchy sequence of continuous functions on [a, b] converges uniformly to a continuous function. This says C[a, b] is:", "Complete in the uniform norm", "Compact", "Finite-dimensional", "Separable only"),
    ("Which theorem needs completeness as a hypothesis?", "The contraction mapping theorem", "The intermediate value theorem", "The triangle inequality", "The mean value theorem")],
    "Completeness is what lets you prove something exists by building a Cauchy sequence that approximates it")),
 ("RA-6.2.C", N("ra-contraction-steps", "A contraction with constant k = {{kk}} is iterated from x₀, and d(x₁, x₀) = {{kd}}. What is the least n for which the bound kⁿ d(x₁, x₀)/(1 − k) is below {{kt}}?", "kans", "pm_first_n(py, 0, kt)",
    "Solve kⁿ < tolerance × (1 − k)/d by taking logarithms, or tabulate the powers of k. The bound needs only the first step, not the fixed point", tex="n", final=True,
    cases=[{"kk": 0.5, "kd": 1, "kt": 0.01, "py": "Rational(1, 2)**n*1/(1 - Rational(1, 2))", "kans": 8}, {"kk": 0.5, "kd": 2, "kt": 0.001, "py": "Rational(1, 2)**n*2/(1 - Rational(1, 2))", "kans": 12},
           {"kk": 0.1, "kd": 1, "kt": 0.0001, "py": "Rational(1, 10)**n*1/(1 - Rational(1, 10))", "kans": 5}, {"kk": 0.25, "kd": 3, "kt": 0.01, "py": "Rational(1, 4)**n*3/(1 - Rational(1, 4))", "kans": 5},
           {"kk": 0.8, "kd": 1, "kt": 0.1, "py": "Rational(4, 5)**n*1/(1 - Rational(4, 5))", "kans": 18}])),
 ("RA-6.2.C", N("ra-contraction-constant", "f(x) = {{sh}} maps [{{ka}}, {{kb}}] into itself. Find its contraction constant, the largest value of |f′| on the interval.", "kans", "calc(vy)",
    "By the mean value theorem |f(x) − f(y)| ≤ sup|f′| · |x − y|, so f is a contraction when that supremum is below 1", tex="k",
    cases=[{"sh": "cos x", "ka": 0, "kb": 1, "kans": 0.84147098, "vy": "Abs(diff(cos(Y), Y).subs(Y, 1))"},
           {"sh": "(x + 2/x)/2", "ka": 1, "kb": 2, "kans": 0.5, "vy": "Max(Abs(diff((Y + 2/Y)/2, Y).subs(Y, 1)), Abs(diff((Y + 2/Y)/2, Y).subs(Y, 2)))"},
           {"sh": "1 + x/3", "ka": 0, "kb": 3, "kans": 0.33333333, "vy": "Abs(diff(1 + Y/3, Y))"},
           {"sh": "e^(−x)", "ka": 0.3, "kb": 0.8, "kans": 0.74081822, "vy": "Abs(diff(exp(-Y), Y).subs(Y, Rational(3, 10)))"},
           {"sh": "√(x + 2)", "ka": 1, "kb": 3, "kans": 0.28867513, "vy": "Abs(diff(sqrt(Y + 2), Y).subs(Y, 1))"}])),
 ("RA-6.2.D", N("ra-hessian-det", "f(x, y) = {{sh}} has a critical point at the origin. Find the determinant of its Hessian there.", "kans", "calc(vy)",
    "The Hessian is the matrix of second partials; its determinant is f_xx f_yy − f_xy². Positive with f_xx > 0 is a minimum, positive with f_xx < 0 a maximum, negative a saddle", tex="\\det H", final=True,
    cases=[{"sh": "x² + xy + y²", "kans": 3, "vy": "Matrix([[2, 1], [1, 2]]).det()"}, {"sh": "x² − 3xy + y²", "kans": -5, "vy": "Matrix([[2, -3], [-3, 2]]).det()"},
           {"sh": "2x² + 4xy + 3y²", "kans": 8, "vy": "Matrix([[4, 4], [4, 6]]).det()"}, {"sh": "−x² + xy − 2y²", "kans": 7, "vy": "Matrix([[-2, 1], [1, -4]]).det()"},
           {"sh": "x² − y²", "kans": -4, "vy": "Matrix([[2, 0], [0, -2]]).det()"}, {"sh": "3x² + 2xy − y²", "kans": -16, "vy": "Matrix([[6, 2], [2, -2]]).det()"}])),
 ("RA-6.2.D", Q("ra-critical-classify", MT, "f(x, y) = {{sh}} has a critical point at the origin. It is:", pace="recall", cases=[
    {"sh": "x² + xy + y²", "kc": 0}, {"sh": "x² − 3xy + y²", "kc": 2}, {"sh": "−x² + xy − 2y²", "kc": 1}, {"sh": "x² − y²", "kc": 2},
    {"sh": "2x² + 4xy + 3y²", "kc": 0}, {"sh": "x⁴ + y⁴", "kc": 3}, {"sh": "−2x² − y²", "kc": 1}, {"sh": "x² + y³", "kc": 3}],
    choice=["A local minimum", "A local maximum", "A saddle point", "Not decided by the Hessian test"], correct="kc", verify="authored",
    explain="Compute f_xx f_yy − f_xy². Negative is a saddle; positive takes the sign of f_xx; zero (as for x⁴ + y⁴, whose Hessian vanishes) leaves the second-order test silent, whatever the point really is")),
]
