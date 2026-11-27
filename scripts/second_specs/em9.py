"""Second question types for the 81 Engineering Math objectives that still listed one drill (Nov 2026). Each asks the
same model another way (in reverse, for a parameter, for a different quantity, or as a choice of case) and is
verified along another route: a solve on the governing condition, a determinant, a residue as a limit, an integral.
Units 13-14 sit inside the opl-fill block, so opl_fill.py injects those: run second_types.py, then opl_fill.py."""
from opl_dsl import Q

FILE, FRAMEWORK = "em-second-types", "engineering-math"
M = "Symbol('m')"
SK = {"1.2": "calc.complex-euler", "1.4": "calc.multivariable", "2.1": "calc.diffeq", "2.3": "ode1.exact-if", "2.6": "ode1.modeling", "2.7": "ode1.recognize", "3.1": "ode2.characteristic", "3.2": "ode2.characteristic",
      "3.3": "ode2.euler-cauchy", "3.4.B": "ode2.spring-undamped", "3.4.C": "ode2.spring-damped", "3.6.C": "ode2.spring-forced", "3.6.D": "ode2.spring-damped", "4.1.A": "ode2.wronskian", "4.1.B": "ode2.higher-order",
      "5.1": "odesys.kinetics-series", "5.2": "odesys.eigenvalue", "5.3": "odesys.phase", "5.4": "odesys.phase", "5.5": "odesys.eigenvalue", "6.1.A": "series.points", "6.1.B": "series.radius", "6.3.A": "series.indicial",
      "6.3.B": "series.frobenius-case", "6.3.C": "series.indicial", "6.4": "series.special-functions", "7.4": "laplace.shifting", "7.6": "laplace.convolution", "8.1": "la.row-reduction", "8.2": "la.independence",
      "8.3.A": "la.determinant", "8.3.B": "la.inverse", "8.4.A": "la.eigenvalues", "8.4.B": "la.eigenvectors", "8.5": "la.eigenvalues", "9.1": "bvp.fourier-series", "9.2.A": "bvp.sl-form", "9.2.B": "bvp.sl-classify",
      "9.2.C": "bvp.sl-eigenvalues", "9.2.D": "bvp.sl-eigenfunctions", "9.3.A": "bvp.sl-eigenfunctions", "9.3.B": "series.special-functions", "10.2": "pde.nonhomogeneous", "10.4": "pde.review-4", "10.5": "pde.laplace-transform",
      "10.6": "pde.review-5", "11.1": "bvp.fourier-series", "12.1": "calc.vector-calculus", "13.1.A": "ode1.modeling", "13.1.B": "ode1.modeling", "13.1.C": "ode2.higher-order", "13.1.D": "ode2.wronskian",
      "13.1.E": "odesys.eigenvalue", "14.1": "cplx.functions", "14.2": "cplx.analytic", "14.3": "cplx.series"}
ADD = []


def sk(code):
    return SK.get(code) or SK[code.rsplit(".", 1)[0]]


def N(code, name, prompt, value, verify, explain, tex="answer", **kw):
    ADD.append((f"EM-{code}", Q(name, sk(code), prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)))


def L(code, name, prompt, options, rows, explain):
    ADD.append((f"EM-{code}", Q(name, sk(code), prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)))


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


# ── unit 1 ──
N("1.2.B", "em-demoivre-real-part", "z has modulus {{kr}} and argument {{kd}}°. Find the real part of z^{{kn}}.", "kr^kn*cos(kn*kd*pi/180)", "re((kr*exp(I*kd*pi/180))**kn)",
  "De Moivre: raise the modulus to the power and multiply the argument by it", tex="\\mathrm{Re}", cases=C("kr kd kn", [(2, 20, 3), (3, 30, 2), (2, 15, 4), (2, 60, 2), (1, 10, 6), (2, 45, 3)]))
N("1.2.C", "em-quadratic-from-complex-roots", "A real quadratic x² + bx + c has roots {{ka}} ± {{kb}}i. Find c.", "ka^2 + kb^2", "re((ka + kb*I)*(ka - kb*I))",
  "The product of conjugate roots α ± βi is α² + β², and their sum is 2α = −b", tex="c", final=True, cases=C("ka kb", [(-1, 2), (2, 1), (3, 4), (-2, 3), (1, 1)]))
N("1.4.B", "em-implicit-slope-ellipse", "Find dy/dx at ({{kx}}, {{ky}}) on the curve x² + {{kk}}y² = c through that point.", "-kx/(kk*ky)",
  "(-diff(x**2 + kk*Y**2, x)/diff(x**2 + kk*Y**2, Y)).subs(x, kx).subs(Y, ky)", "dy/dx = −F_x/F_y", tex="y'", cases=C("kk kx ky", [(1, 3, 4), (4, 2, 1), (2, 1, 3), (3, 3, -1), (1, -5, 12)]))
N("1.4.C", "em-exact-missing-coefficient", "For what k is {{ka}}xy dx + (kx² + {{kb}}) dy an exact differential?", "ka/2",
  f"solve(Eq(diff(ka*x*Y, Y), diff({M}*x**2 + kb, x)), {M})[0]", "Exactness needs M_y = N_x: here ax = 2kx", tex="k", given={"ka": {"pick": [4, 6, 10, 3]}, "kb": {"pick": [1, 3]}})
# ── unit 2 ──
N("2.1.C", "em-euler-two-steps", "Apply two Euler steps of size {{kh}} to y′ = {{kk}}y, y(0) = 1. What value do you get for y at t = 2h?", "(1 + kh*kk)^2",
  "(1 + nsimplify(kh)*kk) + nsimplify(kh)*kk*(1 + nsimplify(kh)*kk)", "Each step multiplies by 1 + hk, so n steps give (1 + hk)ⁿ, against the exact e^(nhk)", tex="y_2",
  given={"kh": {"pick": [0.1, 0.5, 0.25]}, "kk": {"pick": [1, 2, -1]}})
N("2.3.B", "em-integrating-factor-power", "For {{ka}}y dx + x dy = 0, (M_y − N_x)/N depends on x alone. Find the integrating factor μ(x), normalised to μ(1) = 1, at x = 2.", "2^(ka - 1)",
  "exp(integrate((diff(ka*Y, Y) - diff(x, x))/x, (x, 1, 2)))", "μ = exp ∫ (M_y − N_x)/N dx = x^(a−1)", tex="\\mu(2)", given={"ka": {"pick": [2, 3, 4]}})
N("2.6.A", "em-mixing-half-time", "A {{kv}} L tank of pure water receives brine at {{kq}} L/min and drains at the same rate, well mixed. After how many minutes is the tank at half the inlet concentration?",
  "kv/kq*log(2)", "kv*integrate(1/(1 - Y), (Y, 0, Rational(1, 2)))/kq", "c/c_in = 1 − e^(−qt/V), so t = (V/q) ln 2: the residence time times ln 2", tex="t",
  given={"kv": {"pick": [100, 200, 500]}, "kq": {"pick": [5, 10, 20]}})
N("2.6.C", "em-logistic-half-capacity-time", "A population follows P′ = {{kr}}P(1 − P/{{kc}}) from P(0) = {{k0}}. When does it reach half the carrying capacity?", "log((kc - k0)/k0)/kr",
  "integrate(1/(nsimplify(kr)*Y*(1 - Y/kc)), (Y, k0, Rational(kc, 2)))", "Separate and integrate from P₀ to K/2; growth is fastest exactly there", tex="t",
  given={"kr": {"pick": [0.5, 0.2, 1]}, "kc": {"pick": [100, 1000]}, "k0": {"pick": [10, 20]}})
L("2.6.D", "em-phase-line-fate", "{{q}} As t → ∞ the solution:", ["Approaches the smaller equilibrium", "Approaches the larger equilibrium", "Decreases without bound", "Increases without bound"], [
  ("y′ = (y − 1)(4 − y), y(0) = 2.", 1), ("y′ = (y − 1)(4 − y), y(0) = 6.", 1), ("y′ = (y − 1)(4 − y), y(0) = 0.", 2), ("y′ = (y − 2)(y − 5), y(0) = 3.", 0),
  ("y′ = (y − 2)(y − 5), y(0) = 6.", 3), ("y′ = (y − 2)(y − 5), y(0) = 1.", 0)],
  "Mark the equilibria on a line and the sign of y′ between them; the solution moves in that direction until it meets an equilibrium or runs off")
L("2.7.A", "em-existence-uniqueness-verdict", "For the initial-value problem {{q}}, the existence and uniqueness theorem gives:",
  ["A unique solution near the initial point", "Existence, but uniqueness is not guaranteed", "No guarantee at all (f is not continuous there)"], [
  ("y′ = y^(1/3), y(0) = 0", 1), ("y′ = y^(1/3), y(0) = 1", 0), ("y′ = x/y, y(1) = 0", 2), ("y′ = x² + y², y(0) = 0", 0), ("y′ = √|y|, y(2) = 0", 1), ("y′ = y/x, y(0) = 1", 2), ("y′ = y/x, y(1) = 0", 0)],
  "Continuity of f gives existence; continuity of ∂f/∂y as well gives uniqueness. y^(1/3) is continuous at 0 but its derivative blows up there")
# ── unit 3 ──
N("3.1.A", "em-superposition-coefficient", "y = c₁e^({{k1}}x) + c₂e^({{k2}}x) satisfies y(0) = {{ka}}, y′(0) = {{kb}}. Find c₁.", "(kb - k2*ka)/(k1 - k2)",
  f"solve([{M} + Y - ka, k1*{M} + k2*Y - kb], [{M}, Y])[{M}]", "Two conditions give two linear equations for the two constants", tex="c_1", cases=C("k1 k2 ka kb", [(1, -1, 2, 4), (2, -3, 1, 7), (3, 1, 2, 4), (-1, -2, 3, -4)]))
N("3.2.B", "em-repeated-root-ivp-value", "y″ + ({{kp}})y′ + {{kq}}y = 0 has the repeated root r = {{ka}}. With y(0) = {{k0}} and y′(0) = {{k1}}, find y(1).", "(k0 + (k1 - ka*k0))*exp(ka)",
  f"(solve([{M} - k0, ka*{M} + Y - k1], [{M}, Y])[{M}] + solve([{M} - k0, ka*{M} + Y - k1], [{M}, Y])[Y])*exp(ka)", "y = (c₁ + c₂x)e^(rx): c₁ = y(0), and y′(0) = rc₁ + c₂", tex="y(1)",
  cases=C("ka kp kq k0 k1", [(1, -2, 1, 1, 3), (2, -4, 4, 1, 0), (-1, 2, 1, 2, 1), (3, -6, 9, 1, 1)]))
N("3.3.A", "em-euler-cauchy-exponent-sum", "x²y″ + {{ka}}xy′ + {{kb}}y = 0 has solutions x^m. What is the sum of the two exponents?", "1 - ka", "-diff(x*(x - 1) + ka*x + kb, x).subs(x, 0)",
  "The auxiliary equation is m(m − 1) + am + b = 0, that is m² + (a − 1)m + b = 0: not m² + am + b", tex="m_1+m_2", final=True, given={"ka": {"pick": [3, 4, -1, 5]}, "kb": {"pick": [1, 2, -3]}})
N("3.4.B", "em-undamped-amplitude", "A {{km}} kg mass on a {{kk}} N/m spring starts at y = {{k0}} m with speed {{kv}} m/s. Find the amplitude of the motion, in m.", "sqrt(k0^2 + kv^2*km/kk)",
  "sqrt(2*(kk*nsimplify(k0)**2/2 + km*nsimplify(kv)**2/2)/kk)", "A² = y₀² + (v₀/ω)² with ω² = k/m; equivalently all the energy is spring energy at the turning point", tex="A",
  cases=C("km kk k0 kv", [(1, 4, 3, 8), (2, 8, 1, 2), (1, 9, 4, 9), (4, 16, 0.5, 1)]))
N("3.4.C", "em-critical-damping-constant", "A {{km}} kg mass hangs on a {{kk}} N/m spring. What damping constant c makes it critically damped?", "2*sqrt(km*kk)", "Max(*solve(Eq(x**2 - 4*km*kk, 0), x))",
  "Critical damping is where the discriminant c² − 4mk vanishes", tex="c", given={"km": {"pick": [1, 2, 4]}, "kk": {"pick": [4, 9, 16]}})
N("3.6.C", "em-resonance-peak-limit", "A {{km}} kg mass on a {{kk}} N/m spring is driven sinusoidally. Above what damping constant c does the amplitude curve lose its resonance peak?", "sqrt(2*km*kk)",
  "Max(*solve(Eq(Rational(kk, km) - x**2/(2*km**2), 0), x))", "Practical resonance sits at ω² = k/m − c²/(2m²), which only exists while that is positive", tex="c",
  given={"km": {"pick": [1, 2]}, "kk": {"pick": [8, 18, 50]}})
N("3.6.D", "em-rlc-critical-resistance", "A series RLC circuit has L = {{kl}} H and C = {{kf}} F. What resistance makes it critically damped, in Ω?", "2*sqrt(kl/kf)",
  "Max(*solve(Eq(x**2 - 4*nsimplify(kl)/nsimplify(kf), 0), x))", "L ↔ m, R ↔ c, 1/C ↔ k, so c² = 4mk becomes R² = 4L/C", tex="R", cases=C("kl kf", [(1, 0.25), (2, 0.02), (0.5, 0.005), (1, 0.01)]))
# ── unit 4 ──
N("4.1.A", "em-wronskian-three-exponentials", "Find the Wronskian of e^({{ka}}x), e^({{kb}}x) and e^({{kg}}x) at x = 0.", "(kb - ka)*(kg - ka)*(kg - kb)",
  "Matrix([[1, 1, 1], [ka, kb, kg], [ka**2, kb**2, kg**2]]).det()", "At x = 0 the Wronskian matrix is a Vandermonde matrix; it is nonzero exactly when the exponents differ", tex="W(0)", final=True,
  cases=C("ka kb kg", [(1, 2, 3), (0, 1, -1), (1, -1, 2), (2, 3, 5), (-2, 0, 1)]))
N("4.1.B", "em-third-root", "y‴ − {{ks}}y″ + {{kt}}y′ − {{ku}}y = 0 has characteristic roots 1 and 2. Find the third root.", "ks - 3", "Max(*solve(x**3 - ks*x**2 + kt*x - ku, x))",
  "The roots sum to the coefficient of y″ with its sign changed; or divide out (r − 1)(r − 2)", tex="r_3", final=True, cases=C("ks kt ku", [(7, 14, 8), (8, 17, 10), (6, 11, 6), (9, 20, 12)]))
# ── unit 5 ──
N("5.1.B", "em-series-kinetics-peak-time", "In A → B → C with rate constants k₁ = {{k1}} and k₂ = {{k2}} per minute, starting from pure A, when is the amount of B largest?", "log(k1/k2)/(k1 - k2)",
  "integrate(1/Y, (Y, k2, k1))/(k1 - k2)", "B peaks when its formation and consumption balance, k₁A = k₂B, which gives t = ln(k₁/k₂)/(k₁ − k₂)", tex="t_{max}", cases=C("k1 k2", [(2, 1), (3, 1), (4, 2), (5, 2), (1, 3)]))
N("5.2.A", "em-system-dominant-rate", "For y′ = Ay with A = [[{{ka}}, {{kb}}], [{{kb}}, {{ka}}]], what growth rate dominates at large t?", "ka + kb", "Max(*Matrix([[ka, kb], [kb, ka]]).eigenvals().keys())",
  "The eigenvalues are a ± b; the solution is eventually ruled by the larger one, along its eigenvector (1, 1)", tex="\\lambda", final=True, cases=C("ka kb", [(1, 2), (3, 1), (-2, 1), (0, 3), (2, 5)]))
N("5.2.D", "em-repeated-eigenvalue", "A = [[{{k1}}, {{k2}}], [{{k3}}, {{k4}}]] has a single repeated eigenvalue. Find it.", "(k1 + k4)/2", "Max(*Matrix([[k1, k2], [k3, k4]]).eigenvals().keys())",
  "A repeated eigenvalue is half the trace. With only one eigenvector, the second solution needs a generalised eigenvector and a factor of t", tex="\\lambda", final=True,
  cases=C("k1 k2 k3 k4", [(3, 1, -1, 1), (1, 1, -1, 3), (5, 4, -1, 1), (0, 1, -4, 4), (2, -1, 1, 4)]))
L("5.3.C", "em-portrait-type", "A linear system has eigenvalues {{q}}. Its phase portrait is a:", ["Saddle", "Node", "Spiral", "Centre"], [
  ("2 and −1", 0), ("−1 and −3", 1), ("−1 ± 2i", 2), ("±3i", 3), ("1 and 4", 1), ("0.5 ± i", 2), ("−2 and 5", 0)],
  "Real with opposite signs: saddle. Real with the same sign: node. Complex: spiral, or a centre when the real part is zero")
L("5.3.B", "em-stability-from-trace-det", "A 2×2 linear system has trace {{q}}. The origin is:", ["Asymptotically stable", "Stable but not asymptotically stable", "Unstable"], [
  ("−3 and determinant 2", 0), ("0 and determinant 4", 1), ("2 and determinant 5", 2), ("−1 and determinant −6", 2), ("−4 and determinant 4", 0), ("3 and determinant −2", 2)],
  "Asymptotic stability needs trace < 0 and determinant > 0. A negative determinant is always a saddle; zero trace with positive determinant is a centre")
N("5.4.A", "em-coexistence-point", "x′ = x({{ka}} − x − y), y′ = y(x − {{kb}}). Find the y-coordinate of the critical point where neither x nor y is zero.", "ka - kb",
  "solve([ka - x - Y, x - kb], [x, Y])[Y]", "Set each bracket to zero: x = b from the second, then y = a − x", tex="y^*", final=True, cases=C("ka kb", [(5, 2), (4, 1), (6, 4), (3, 1)]))
N("5.4.B", "em-jacobian-determinant", "x′ = x({{ka}} − x − y), y′ = y(x − {{kb}}). Find the determinant of the Jacobian at the critical point ({{kb}}, {{kd}}).", "kb*kd",
  "Matrix([[diff(x*(ka - x - Y), x), diff(x*(ka - x - Y), Y)], [diff(Y*(x - kb), x), diff(Y*(x - kb), Y)]]).subs(x, kb).subs(Y, kd).det()",
  "J = [[a − 2x − y, −x], [y, x − b]]; at (b, a − b) it is [[−b, −b], [a − b, 0]]. Positive determinant with negative trace: asymptotically stable", tex="\\det J", final=True,
  cases=C("ka kb kd", [(5, 2, 3), (4, 1, 3), (6, 4, 2), (3, 1, 2)]))
N("5.5.A", "em-system-constant-particular", "y′ = Ay + g with A = [[{{k1}}, {{k2}}], [{{k3}}, {{k4}}]] and constant g = ({{kg}}, {{kh}}). Find the first component of the constant particular solution.",
  "-(k4*kg - k2*kh)/(k1*k4 - k2*k3)", "(-Matrix([[k1, k2], [k3, k4]]).inv()*Matrix([kg, kh]))[0]", "A constant y_p makes y′ = 0, so Ay_p = −g", tex="y_{p1}",
  cases=C("k1 k2 k3 k4 kg kh", [(1, 2, 3, 4, 2, 6), (2, 1, 1, 3, 5, 5), (-1, 2, 0, -3, 4, 6), (2, 0, 1, 1, 4, 3)]))
# ── unit 6 ──
N("6.1.A", "em-singular-point-location", "(x² − {{ks}})y″ + xy′ + y = 0. Where is its positive singular point?", "sqrt(ks)", "Max(*solve(x**2 - ks, x))",
  "Singular points are where the coefficient of y″ vanishes (after any common factor is cancelled)", tex="x", given={"ks": {"pick": [4, 9, 16, 2]}})
N("6.1.B", "em-radius-from-complex-singularity", "(x² + {{ks}})y″ + y = 0 is expanded in a power series about x = {{kx}}. What radius of convergence is guaranteed?", "sqrt(kx^2 + ks)",
  "Abs(kx - sqrt(ks)*I)", "The radius is the distance to the nearest singular point in the complex plane, here ±i√s, even though the equation looks harmless on the real line", tex="R",
  cases=C("ks kx", [(4, 0), (9, 4), (16, 3), (1, 1), (4, 2)]))
N("6.3.A", "em-indicial-p0", "At a regular singular point the indicial equation r(r − 1) + p₀r + q₀ = 0 has roots {{k1}} and {{k2}}. Find p₀.", "1 - (k1 + k2)",
  f"solve([nsimplify(k1)*(nsimplify(k1) - 1) + {M}*nsimplify(k1) + Y, nsimplify(k2)*(nsimplify(k2) - 1) + {M}*nsimplify(k2) + Y], [{M}, Y])[{M}]",
  "Written out, r² + (p₀ − 1)r + q₀ = 0, so the roots sum to 1 − p₀", tex="p_0", cases=C("k1 k2", [(0.5, -1), (1, -1), (2, -2), (0.5, -0.5), (3, 1)]))
L("6.3.B", "em-frobenius-case-from-roots", "The indicial roots are {{q}}. The second solution:", ["Is a second Frobenius series, with no logarithm", "Certainly contains a logarithm", "May contain a logarithm"], [
  ("1/2 and 0", 0), ("0 and 0", 1), ("2 and −1", 2), ("1/3 and −1/3", 0), ("1 and 1", 1), ("3 and 0", 2), ("1/2 and −1/2", 2)],
  "Roots differing by a non-integer: two series. Equal roots: always a log. Differing by a positive integer (1/2 and −1/2 differ by 1): a log may or may not appear")
N("6.3.C", "em-bessel-series-a2", "For Bessel's equation of order {{kn}}, the Frobenius series from the larger root has a₀ = 1. Find a₂.", "-1/(4*(1 + kn))",
  f"solve(Eq({M}*((kn + 2)**2 - kn**2) + 1, 0), {M})[0]", "The recurrence is a_k[(r + k)² − ν²] + a_(k−2) = 0 with r = ν", tex="a_2", given={"kn": {"pick": [1, 2, 3, 4]}})
N("6.4.B", "em-bessel-zero-scale", "J₀ first vanishes at 2.404826. What is the smallest λ > 0 for which y = J₀(λx) is zero at x = {{kl}}?", "2.404826/kl", "jzero(0, 1)/kl",
  "λx must equal a zero of J₀, so λ = j₀₁/L. This is how a boundary condition picks out eigenvalues for a cylinder", tex="\\lambda", given={"kl": {"pick": [2, 4, 5, 10]}})
L("6.4.C", "em-bessel-second-solution", "For Bessel's equation of order ν = {{q}}, a second independent solution is:", ["J₋ν", "Y_ν, because J₋ν is not independent of J_ν"], [
  ("1/2", 0), ("0", 1), ("1", 1), ("1/3", 0), ("2", 1), ("3/2", 0)],
  "For integer ν, J₋ν = (−1)^ν J_ν, so the Bessel function of the second kind is needed. For non-integer ν (including half-integers) J₋ν is independent")
N("6.4.D", "em-legendre-norm", "Evaluate the integral of P_{{kn}}(x)² over −1 ≤ x ≤ 1.", "2/(2*kn + 1)", "integrate(legendre(kn, x)**2, (x, -1, 1))", "The Legendre polynomials are orthogonal with squared norm 2/(2n + 1)", tex="I",
  given={"kn": {"pick": [1, 2, 3, 4]}})
# ── unit 7 ──
N("7.4.B", "em-shifted-inverse-value", "F(s) = e^(−{{ka}}s)/(s + {{kb}}). Find f({{kt}}).", "exp(-kb*(kt - ka))", "limit((Z + kb)*exp(Z*(nsimplify(kt) - ka))/(Z + kb), Z, -kb)",
  "e^(−as) delays by a: f(t) = u(t − a)e^(−b(t − a))", tex="f", cases=C("ka kb kt", [(1, 2, 3), (2, 1, 2.5), (1, 3, 1.5), (3, 1, 5)]))
N("7.6.A", "em-convolution-two-exponentials", "Evaluate the convolution (e^({{ka}}t) * e^({{kb}}t)) at t = {{kt}}.", "(exp(ka*kt) - exp(kb*kt))/(ka - kb)", "integrate(exp(ka*Y)*exp(kb*(kt - Y)), (Y, 0, kt))",
  "∫₀ᵗ e^(aτ)e^(b(t−τ)) dτ; in s-space it is 1/((s − a)(s − b))", tex="f*g", cases=C("ka kb kt", [(1, -1, 1), (2, 1, 1), (-1, -2, 2), (1, 0, 2)]))
N("7.6.C", "em-volterra-exponential", "y(t) = {{ka}} + {{kk}}∫₀ᵗ y(τ) dτ. Find y({{kt}}).", "ka*exp(kk*kt)", "limit((Z - kk)*ka/(Z - kk)*exp(Z*kt), Z, kk)",
  "Transform: Y = a/s + kY/s, so Y = a/(s − k). Or differentiate: y′ = ky with y(0) = a", tex="y", cases=C("ka kk kt", [(2, 1, 1), (1, -2, 1), (3, 2, 1), (5, -1, 2)]))
# ── unit 8 ──
N("8.1.A", "em-system-no-solution-parameter", "{{k1}}x + {{k2}}y = {{kg}} and {{k3}}x + ky = {{kh}}. For what k does the system have no solution?", "k3*k2/k1",
  f"solve(Matrix([[k1, k2], [k3, {M}]]).det(), {M})[0]", "No solution needs parallel lines: a zero determinant, with right-hand sides that are not in the same ratio", tex="k",
  cases=C("k1 k2 k3 kg kh", [(1, 2, 2, 3, 5), (2, 3, 4, 1, 5), (1, -1, 3, 2, 7), (3, 6, 1, 4, 1)]))
N("8.2.A", "em-dependence-parameter", "For what k are ({{a1}}, {{a2}}, {{a3}}), ({{b1}}, {{b2}}, {{b3}}) and ({{g1}}, {{g2}}, k) linearly dependent?", "kans",
  f"solve(Matrix([[a1, a2, a3], [b1, b2, b3], [g1, g2, {M}]]).det(), {M})[0]", "Three vectors in space are dependent exactly when their determinant is zero", tex="k", final=True,
  cases=C("a1 a2 a3 b1 b2 b3 g1 g2 kans", [(1, 2, 3, 0, 1, 2, 1, 3, 5), (1, 0, 2, 0, 1, 1, 2, 1, 5), (2, 1, 0, 1, 1, 1, 3, 2, 1), (1, 1, 1, 1, 2, 4, 1, 3, 7)]))
N("8.3.A", "em-determinant-scaling", "A is 3×3 with det A = {{kd}}. Find det({{kc}}A).", "kc^3*kd", "(kc*Matrix.diag(kd, 1, 1)).det()",
  "Each of the three rows picks up the factor, so det(cA) = c³ det A for a 3×3 matrix", tex="\\det", final=True, given={"kd": {"pick": [2, 5, -3]}, "kc": {"pick": [2, 3, -1]}})
N("8.3.B", "em-inverse-entry", "Find the (1, 2) entry of the inverse of [[{{k1}}, {{k2}}], [{{k3}}, {{k4}}]].", "-k2/(k1*k4 - k2*k3)", "Matrix([[k1, k2], [k3, k4]]).inv()[0, 1]",
  "Swap the diagonal, negate the off-diagonal, divide by the determinant", tex="(A^{-1})_{12}", cases=C("k1 k2 k3 k4", [(2, 1, 5, 3), (4, 3, 2, 2), (1, 2, 3, 4), (3, -1, 2, 1)]))
N("8.4.A", "em-eigenvalue-from-trace-det", "A 2×2 matrix has trace {{kt}} and determinant {{kd}}. Find its larger eigenvalue.", "(kt + sqrt(kt^2 - 4*kd))/2", "Max(*solve(x**2 - kt*x + kd, x))",
  "The characteristic polynomial is λ² − (trace)λ + det", tex="\\lambda", cases=C("kt kd", [(5, 6), (7, 10), (2, -8), (6, 5), (1, -12)]))
N("8.4.B", "em-eigenvector-second-component", "A = [[{{k1}}, {{k2}}], [{{k3}}, {{k4}}]] has eigenvalue {{kl}}. Its eigenvector is (1, v). Find v.", "(kl - k1)/k2",
  f"solve((Matrix([[k1, k2], [k3, k4]])*Matrix([1, {M}]) - kl*Matrix([1, {M}]))[0], {M})[0]", "The first row of (A − λI)v = 0 gives (a − λ) + bv = 0", tex="v",
  cases=C("k1 k2 k3 k4 kl", [(2, 1, 1, 2, 3), (4, 1, 2, 3, 5), (4, 1, 2, 3, 2), (1, 2, 3, 2, 4), (1, 2, 3, 2, -1)]))
N("8.5.A", "em-matrix-power-by-diagonalising", "A = [[{{ka}}, {{kb}}], [{{kb}}, {{ka}}]]. Find the (1, 1) entry of A^{{kn}}.", "((ka + kb)^kn + (ka - kb)^kn)/2", "(Matrix([[ka, kb], [kb, ka]])**kn)[0, 0]",
  "Diagonalise with eigenvectors (1, 1) and (1, −1): Aⁿ = P Dⁿ P⁻¹, and Dⁿ just powers the eigenvalues a ± b", tex="(A^n)_{11}", final=True, cases=C("ka kb kn", [(1, 2, 3), (2, 1, 4), (3, 1, 3), (0, 2, 4), (1, 1, 5)]))
# ── unit 9 ──
N("9.1.B", "em-fourier-abs-a1", "f(x) = |x| on (−{{kl}}, {{kl}}), extended with period {{kp}}. Find the coefficient a₁ of cos(πx/{{kl}}).", "-4*kl/pi^2", "Rational(2, kl)*integrate(x*cos(pi*x/kl), (x, 0, kl))",
  "f is even, so only cosines appear and a_n = (2/L)∫₀ᴸ f cos(nπx/L) dx", tex="a_1", cases=C("kl kp", [(1, 2), (2, 4), (3, 6), (5, 10)]))
N("9.1.C", "em-half-range-sine-coefficient", "Expand f(x) = 1 on (0, {{kl}}) in a half-range sine series. Find b_{{kn}}.", "2*(1 - cos(kn*pi))/(kn*pi)", "Rational(2, kl)*integrate(sin(kn*pi*x/kl), (x, 0, kl))",
  "b_n = (2/L)∫₀ᴸ sin(nπx/L) dx = 2(1 − cos nπ)/(nπ): 4/(nπ) for odd n, and the even ones vanish", tex="b_n", given={"kl": {"pick": [1, 2, 3]}, "kn": {"pick": [1, 3, 5]}})
N("9.1.D", "em-resonant-harmonic", "y″ + {{kw}}y = r(t), where r has period 2π and contains every harmonic sin nt. Which harmonic n drives the oscillator at resonance?", "sqrt(kw)", "Max(*solve(Eq(x**2, kw), x))",
  "Each harmonic is answered separately with amplitude ∝ 1/(ω₀² − n²); the one with n = ω₀ grows without bound", tex="n", final=True, given={"kw": {"pick": [9, 25, 49, 4]}})
N("9.2.A", "em-sl-weight", "To put y″ + {{ka}}y′ + λy = 0 in Sturm–Liouville form you multiply by p(x) = e^({{ka}}x), which also becomes the weight. Find the weight at x = 1.", "exp(ka)",
  "exp(integrate(ka, (x, 0, 1)))", "p = exp ∫ (coefficient of y′) dx; then (py′)′ + λpy = 0, so r(x) = p(x)", tex="r(1)", given={"ka": {"pick": [1, 2, -1, 3]}})
L("9.2.B", "em-sl-kind", "{{q}} This Sturm–Liouville problem is:", ["Regular", "Periodic", "Singular"], [
  ("Legendre's equation on [−1, 1], where p(x) = 1 − x² vanishes at both ends.", 2), ("y″ + λy = 0 with y(0) = y(L) = 0.", 0), ("y″ + λy = 0 with y(−π) = y(π) and y′(−π) = y′(π).", 1),
  ("Bessel's equation on [0, a], where p(x) = x vanishes at 0.", 2), ("y″ + λy = 0 with y′(0) = 0 and y(1) + y′(1) = 0.", 0), ("y″ + λy = 0 on the half-line x ≥ 0.", 2)],
  "Regular: finite interval, p and r positive throughout, separated conditions at both ends. Singular: p vanishes at an end or the interval is infinite")
N("9.2.C", "em-sl-mixed-eigenvalue", "y″ + λy = 0, y(0) = 0, y′({{kl}}) = 0. Find the eigenvalue λ_{{kn}}.", "((2*kn - 1)*pi/(2*kl))^2", "(pi/2 + (kn - 1)*pi)**2/kl**2",
  "y = sin(√λ x) and the far end needs cos(√λ L) = 0, the odd multiples of π/2", tex="\\lambda_n", given={"kl": {"pick": [1, 2, 4]}, "kn": {"pick": [1, 2, 3]}})
N("9.2.D", "em-eigenfunction-first-node", "y_n = sin(nπx/{{kl}}) is the nth eigenfunction for fixed ends on (0, {{kl}}). Where is the first interior zero of y_{{kn}}?", "kl/kn", "Max(*solve(sin(kn*pi*x/kl), x))",
  "The nth eigenfunction has n − 1 interior zeros, evenly spaced L/n apart", tex="x", given={"kl": {"pick": [1, 2, 6]}, "kn": {"pick": [2, 3, 4]}})
N("9.3.A", "em-eigenfunction-norm", "Evaluate the integral of sin²({{kn}}πx/{{kl}}) over 0 ≤ x ≤ {{kl}}.", "kl/2", "integrate(sin(kn*pi*x/kl)**2, (x, 0, kl))",
  "Different eigenfunctions integrate to zero; each one against itself gives L/2, which is the 2/L in the coefficient formula", tex="I", given={"kl": {"pick": [1, 2, 3, 5]}, "kn": {"pick": [1, 2, 3]}})
N("9.3.B", "em-legendre-coefficient", "Expand f(x) = x^{{kp}} in Legendre polynomials on [−1, 1]. Find the coefficient of P_{{kn}}.", "kv/kw", "Rational(2*kn + 1, 2)*integrate(x**kp*legendre(kn, x), (x, -1, 1))",
  "c_n = (2n + 1)/2 × ∫ f P_n dx. For example x² = (1/3)P₀ + (2/3)P₂", tex="c_n", cases=C("kp kn kv kw", [(2, 0, 1, 3), (2, 2, 2, 3), (3, 1, 3, 5), (3, 3, 2, 5), (4, 2, 4, 7)]))
# ── unit 10 ──
N("10.2.F", "em-steady-flux-end", "A rod of conductivity {{kk}} W/m·K and length {{kl}} m is held at {{k0}} °C at x = 0 and loses {{kq}} W/m² at x = L. Find the steady temperature at x = L.", "k0 - kq*kl/kk",
  f"k0 + solve(Eq(-kk*{M}, kq), {M})[0]*kl", "Steady state is a straight line whose slope is fixed by the flux: −ku′ = q", tex="u(L)", given={"kk": {"pick": [10, 50]}, "kl": {"pick": [1, 2]}, "k0": {"pick": [100, 200]}, "kq": {"pick": [500, 1000]}})
N("10.2.G", "em-shift-leaves-source", "u_t = αu_xx on 0 < x < {{kl}} with u(0, t) = 0 and u({{kl}}, t) = {{ka}}t. Subtracting w = x·{{ka}}t/{{kl}} leaves a source −w_t in the equation for v. Find that source at x = {{kx}}.",
  "-ka*kx/kl", "-diff(x*ka*Y/kl, Y).subs(x, kx)", "w satisfies the boundary values but not the PDE: w_xx = 0 and w_t = ax/L, so v_t = αv_xx − ax/L with zero boundary values", tex="s",
  cases=C("kl ka kx", [(2, 4, 1), (1, 3, 0.5), (4, 2, 3), (5, 10, 2)]))
N("10.4.D", "em-sphere-time-constant", "A sphere of radius {{kr}} m and diffusivity {{kal}} m²/s has its surface held at 0. What is the time constant of its slowest mode, in s?", "kr^2/(kal*pi^2)",
  "1/(nsimplify(kal)*Max(*solve(sin(x*nsimplify(kr)), x))**2)", "With v = ru the sphere becomes a rod of length R, so the slowest mode decays as exp(−απ²t/R²)", tex="\\tau",
  cases=C("kr kal", [(0.1, 0.0001), (0.05, 0.00001), (0.2, 0.0001), (0.01, 0.000001)]))
L("10.5.C", "em-pde-method-pick", "{{q}} The first move is:", ["Separation of variables as it stands", "Subtract a steady state first", "A Laplace transform in time or a similarity variable", "Finite differences"], [
  ("A finite rod with both ends held at 0 and a given initial profile.", 0), ("A finite rod with its ends held at two different constant temperatures.", 1), ("A semi-infinite solid whose surface temperature is stepped at t = 0.", 2),
  ("A rod whose conductivity depends on temperature.", 3), ("A finite rod with insulated ends and a given initial profile.", 0), ("An irregular plate with mixed boundary data.", 3)],
  "Separation needs a linear equation and homogeneous boundary conditions on a finite interval. Fix the boundary first if it is not homogeneous; no length scale means similarity or transforms")
N("10.6.C", "em-ghost-node-value", "At the boundary node, the condition −k ∂u/∂x = q is applied with a central difference. With k = {{kk}}, q = {{kq}}, Δx = {{kdx}} and u₁ = {{ku}}, find the ghost value u₋₁.", "ku + 2*kdx*kq/kk",
  f"solve(Eq(-kk*(ku - {M})/(2*nsimplify(kdx)), kq), {M})[0]", "−k(u₁ − u₋₁)/(2Δx) = q. An insulated end (q = 0) simply mirrors: u₋₁ = u₁", tex="u_{-1}",
  cases=C("kk kq kdx ku", [(10, 100, 0.1, 50), (2, 40, 0.05, 20), (50, 500, 0.2, 80), (1, 10, 0.1, 30)]))
N("10.6.D", "em-crank-nicolson-one-node", "A rod with both ends at 0 has one interior node, at {{ku}}. Take one Crank–Nicolson step with r = αΔt/Δx² = {{kr}}. Find the new value.", "ku*(1 - kr)/(1 + kr)",
  f"solve(Eq({M} - ku, nsimplify(kr)/2*((0 - 2*{M} + 0) + (0 - 2*ku + 0))), {M})[0]", "Average the second difference at the old and new time levels. The explicit scheme would give ku(1 − 2r), which blows up for r > 1", tex="u^{new}",
  cases=C("ku kr", [(100, 0.5), (80, 0.25), (60, 2), (50, 4)]))
# ── units 11-12 ──
N("11.1.A", "em-fourier-sine-transform-exponential", "With the convention F_s(w) = √(2/π)∫₀^∞ f(x) sin wx dx, find the sine transform of e^(−{{ka}}x) at w = {{kw}}.", "sqrt(2/pi)*kw/(ka^2 + kw^2)",
  "sqrt(2/pi)*integrate(exp(-ka*x)*sin(kw*x), (x, 0, oo))", "∫₀^∞ e^(−ax) sin wx dx = w/(a² + w²)", tex="F_s", cases=C("ka kw", [(1, 1), (2, 1), (1, 3), (3, 4)]))
N("12.1.B", "em-flux-divergence-source", "In steady state the flux along a duct is J(x) = {{ka}}x². What must the generation rate per unit volume be at x = {{kx}}?", "2*ka*kx",
  "limit((ka*(kx + Y)**2 - ka*kx**2)/Y, Y, 0)", "A balance on a thin slice: what leaves minus what enters equals what is generated, so the source is dJ/dx", tex="s", final=True, given={"ka": {"pick": [2, 3, 5]}, "kx": {"pick": [1, 2, 4]}})
# ── unit 13 ──
N("13.1.A", "em-rc-charge-time", "A capacitor of {{kcp}} µF charges through {{kr}} kΩ from zero. After how many ms has it reached {{kf}} of its final voltage?", "-kr*kcp*log(1 - kf)",
  "kr*kcp*integrate(1/(1 - Y), (Y, 0, nsimplify(kf)))", "v/V = 1 − e^(−t/RC), and kΩ × µF = ms", tex="t", given={"kcp": {"pick": [1, 10, 47]}, "kr": {"pick": [1, 2.2, 10]}, "kf": {"pick": [0.5, 0.9, 0.99]}})
N("13.1.B", "em-saddle-node-stable-branch", "y′ = {{kr}} − y². Find the stable equilibrium.", "sqrt(kr)", "Max(*solve(kr - x**2, x))",
  "The equilibria ±√r appear at r = 0. The upper one is stable because f′(y) = −2y is negative there", tex="y^*", given={"kr": {"pick": [4, 9, 2, 16]}})
N("13.1.C", "em-operator-on-exponential", "Apply (D² + {{ka}}D + {{kb}}) to e^({{kr}}x) and evaluate the result at x = 0.", "kr^2 + ka*kr + kb",
  "(diff(exp(kr*x), x, 2) + ka*diff(exp(kr*x), x) + kb*exp(kr*x)).subs(x, 0)", "P(D)e^(rx) = P(r)e^(rx): an exponential turns a differential operator into its characteristic polynomial", tex="P(r)", final=True,
  cases=C("ka kb kr", [(3, 2, 1), (1, -6, 2), (-4, 4, 3), (2, 5, -1)]))
N("13.1.D", "em-existence-interval-end", "(x − {{ka}})(x − {{kb}})y″ + y′ + y = 0 with y({{k0}}) = 1, y′({{k0}}) = 0. The solution is guaranteed on an interval a < x < b. Find b.", "kb",
  "Max(*solve((x - ka)*(x - kb), x))", "Divide by the leading coefficient; the coefficients are continuous between its zeros, and the interval is the one containing the initial point", tex="b", final=True,
  cases=C("ka kb k0", [(1, 4, 2), (-2, 3, 0), (0, 5, 1), (-3, -1, -2)]))
N("13.1.E", "em-system-solution-exponent", "y = e^(λt)(1, {{kv}}) solves y′ = Ay with A = [[{{k1}}, {{k2}}], [{{k3}}, {{k4}}]]. Find λ.", "k1 + k2*kv",
  f"solve((Matrix([[k1, k2], [k3, k4]])*Matrix([1, kv]))[0] - {M}, {M})[0]", "Substitute: λv = Av, so the first row gives λ = a + bv", tex="\\lambda", final=True,
  cases=C("k1 k2 k3 k4 kv", [(2, 1, 1, 2, 1), (2, 1, 1, 2, -1), (4, 1, 2, 3, 1), (4, 1, 2, 3, -2)]))
# ── unit 14 ──
N("14.1.A", "em-complex-linear-imaginary-part", "Solve ({{ka}} + i)z = {{kb}} + {{kg}}i and give the imaginary part of z.", "(ka*kg - kb)/(ka^2 + 1)", "im((kb + kg*I)/(ka + I))",
  "Divide by multiplying top and bottom by the conjugate a − i", tex="\\mathrm{Im}\\,z", cases=C("ka kb kg", [(1, 3, 1), (2, 1, 3), (3, 4, 2), (1, 1, 3)]))
N("14.1.B", "em-complex-square-root", "z² = {{ka}}i. Find the real part of the root in the first quadrant.", "sqrt(ka/2)", "re(sqrt(ka*I))",
  "ai has modulus a and argument 90°, so its square root has modulus √a and argument 45°", tex="\\mathrm{Re}\\,z", given={"ka": {"pick": [2, 8, 18, 4]}})
L("14.1.C", "em-point-and-circle", "Relative to the circle {{q}} is:", ["Inside", "On the circle", "Outside"], [
  ("|z| = 5, the point 3 + 4i", 1), ("|z − 1| = 2, the point 2 + i", 0), ("|z − i| = 1, the point 2", 2), ("|z − (1 + i)| = 3, the point 1 − 2i", 1), ("|z + 1| = 2, the point 0", 0), ("|z| = 1, the point 1 + i", 2)],
  "|z − c| is the distance from z to c; compare it with the radius")
N("14.1.D", "em-inversion-modulus", "Under w = 1/z, find |w| for z = {{ka}} + {{kb}}i.", "1/sqrt(ka^2 + kb^2)", "Abs(1/(ka + kb*I))", "|1/z| = 1/|z|: inversion sends points outside the unit circle inside, and the reverse", tex="|w|",
  cases=C("ka kb", [(3, 4), (1, 1), (5, 12), (2, 0), (0, 4)]))
N("14.1.E", "em-complex-limit-removable", "Find the imaginary part of the limit of (z² + {{ks}})/(z − {{ka}}i) as z → {{ka}}i.", "2*ka", "im(limit((Z**2 + ks)/(Z - ka*I), Z, ka*I))",
  "Factor: z² + a² = (z − ai)(z + ai), so the limit is 2ai", tex="\\mathrm{Im}", final=True, cases=C("ka ks", [(1, 1), (2, 4), (3, 9), (5, 25)]))
N("14.2.A", "em-cauchy-riemann-coefficient", "u = {{ka}}x² + my² and v = {{kb}}xy. For what m do the Cauchy–Riemann equations hold?", "-kb/2",
  f"solve(Eq(diff(ka*x**2 + {M}*Y**2, Y), -diff(kb*x*Y, x)), {M})[0]", "u_x = v_y already holds (2ax = bx); u_y = −v_x then needs 2my = −by", tex="m", final=True, cases=C("ka kb", [(1, 2), (2, 4), (3, 6), (5, 10)]))
N("14.2.B", "em-harmonic-coefficient", "For what m is u = {{ka}}x³ + mxy² harmonic?", "-3*ka", f"solve(Eq(diff(ka*x**3 + {M}*x*Y**2, x, 2) + diff(ka*x**3 + {M}*x*Y**2, Y, 2), 0), {M})[0]",
  "u_xx + u_yy = 6ax + 2mx must vanish. With a = 1 this is the real part of z³", tex="m", final=True, given={"ka": {"pick": [1, 2, 4, -1]}})
L("14.2.C", "em-analytic-where", "The function {{q}} is:", ["Entire", "Analytic except at isolated points", "Analytic nowhere"], [
  ("e^z", 0), ("1/z", 1), ("the conjugate of z", 2), ("z³ − 2z", 0), ("|z|²", 2), ("tan z", 1), ("sin z", 0), ("1/(z² + 1)", 1)],
  "Polynomials, e^z, sin z and cos z are entire. Quotients fail only where the denominator vanishes. Anything built from the conjugate or |z| fails the Cauchy–Riemann equations (|z|² is differentiable only at 0)")
N("14.2.D", "em-harmonic-conjugate-value", "u = x² − y² + {{ka}}x. Find its harmonic conjugate v, with v(0, 0) = 0, at ({{kx}}, {{ky}}).", "2*kx*ky + ka*ky",
  "integrate(diff(x**2 - Y**2 + ka*x, x), (Y, 0, ky)).subs(x, kx)", "v_y = u_x = 2x + a gives v = 2xy + ay + g(x), and v_x = −u_y = 2y makes g constant. This is z² + az", tex="v", final=True,
  cases=C("ka kx ky", [(1, 2, 3), (3, 1, 1), (2, -1, 4), (4, 2, 1)]))
N("14.3.A", "em-cauchy-formula-derivative", "The integral of e^({{ka}}z)/z² once counterclockwise around |z| = 1 equals bi. Find b.", "2*pi*ka", "im(2*pi*I*diff(exp(ka*Z), Z).subs(Z, 0))",
  "Cauchy's formula for the first derivative: ∮ f(z)/(z − z₀)² dz = 2πi f′(z₀)", tex="b", given={"ka": {"pick": [1, 2, 3, 5]}})
L("14.3.B", "em-complex-sequence-fate", "The sequence z_n = {{q}}:", ["Converges to 0", "Converges to a nonzero limit", "Diverges"], [
  ("(i/2)^n", 0), ("((3 + 4i)/5)^n", 2), ("(1 + i)^n", 2), ("(2n + i)/(n − i)", 1), ("((1 + i)/2)^n", 0), ("i^n/n", 0), ("n/(n + i)", 1), ("i^n", 2)],
  "A power wⁿ goes to 0 when |w| < 1, blows up when |w| > 1, and circles for ever when |w| = 1 (unless w = 1). For a quotient, divide through by n")
N("14.3.C", "em-taylor-coefficient-geometric", "Find the coefficient of z^{{kn}} in the Taylor series of 1/({{ka}} − z) about 0.", "1/ka^(kn + 1)", "diff(1/(ka - Z), Z, kn).subs(Z, 0)/factorial(kn)",
  "1/(a − z) = (1/a)·1/(1 − z/a) = Σ zⁿ/a^(n+1), valid for |z| < a", tex="c_n", given={"ka": {"pick": [2, 3, 5]}, "kn": {"pick": [1, 2, 3]}})
N("14.3.D", "em-residue-double-pole-exp", "Find the residue of e^({{ka}}z)/(z − {{kq}})² at z = {{kq}}.", "ka*exp(ka*kq)", "limit(diff(exp(ka*Z), Z), Z, kq)",
  "At a double pole the residue is the derivative of (z − z₀)²f(z) at z₀", tex="\\mathrm{Res}", cases=C("ka kq", [(1, 1), (2, 1), (3, -1), (1, 2), (2, -1)]))
L("14.3.E", "em-zero-order-pick", "At z = 0 the function {{q}} has a zero of order:", ["1", "2", "3", "4"], [
  ("z² sin z", 2), ("1 − cos z", 1), ("z − sin z", 2), ("e^z − 1 − z", 1), ("sin² z", 1), ("z³(e^z − 1)", 3), ("e^z − 1", 0)],
  "Expand about 0 and read off the first power that survives: sin z = z − z³/6 + …, cos z = 1 − z²/2 + …, e^z = 1 + z + z²/2 + …")
assert len(ADD) == 81, len(ADD)
