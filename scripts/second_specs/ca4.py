"""Second question types for Calculus units 16-18 (Nov 2026), the 24 objectives that still had one drill. Each asks
the model in reverse, for a different quantity, or as a choice of method, and is verified along another route
(the washer integral behind a shell answer, the frustum formula behind a surface integral, a limit, a solve).
These objectives sit inside the opl-fill block, so opl_fill.py injects them: run second_types.py, then opl_fill.py."""
from opl_dsl import Q

FILE, FRAMEWORK = "ca-second-types-3", "calculus"
R, EX, DR, IA, AD, SE, PP, V3 = "calc.rates", "calc.extrema", "calc.derivative-rules", "calc.integration-apps", "calc.antiderivatives", "calc.series", "calc.parametric-polar", "calc.vectors-3d"


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


ADD = [
 ("CA-16.1.A", Q("ca-marginal-revenue-zero", R, "Revenue from selling q units is R(q) = {{ka}}q − {{kb}}q² dollars. At what q is the marginal revenue zero?",
    given={"ka": {"pick": [40, 60, 120]}, "kb": {"pick": [2, 3, 5]}}, value="ka/(2*kb)", tex="q", verify="solve(diff(ka*x - kb*x**2, x), x)[0]",
    explain="Marginal revenue is R′(q) = a − 2bq. Past the point where it reaches zero, selling one more unit lowers total revenue")),
 ("CA-16.1.B", Q("ca-max-profit-value", EX, "Items sell for {{kp}} dollars each, and making q of them costs C(q) = {{kf}} + {{kc}}q + {{kd}}q² dollars. What is the largest possible profit, in dollars?",
    given={"kp": {"pick": [50, 80, 110]}, "kf": {"pick": [100, 200]}, "kc": {"pick": [10, 20]}, "kd": {"pick": [0.5, 1, 2]}}, value="(kp - kc)^2/(4*kd) - kf", tex="P_{max}",
    verify="(kp*x - kf - kc*x - nsimplify(kd)*x**2).subs(x, solve(diff(kp*x - kf - kc*x - nsimplify(kd)*x**2, x), x)[0])",
    explain="Find q where marginal revenue equals marginal cost, q = (p − c)/(2d), then put it back into the profit")),
 ("CA-16.1.C", Q("ca-peak-concentration-value", EX, "After a dose, a drug's blood concentration is C(t) = {{ka}}·t·e^(−{{kk}}t) mg/L (t in hours). What is the highest concentration reached?",
    given={"ka": {"pick": [4, 10, 20]}, "kk": {"pick": [0.5, 0.25, 1]}}, value="ka/(kk*exp(1))", tex="C_{max}",
    verify="(ka*x*exp(-nsimplify(kk)*x)).subs(x, solve(Eq(1 - nsimplify(kk)*x, 0), x)[0])",
    explain="C′ = A e^(−kt)(1 − kt) vanishes at t = 1/k, where C = A/(ke)")),
 ("CA-16.1.D", Q("ca-unit-elastic-price", DR, "Demand is q = {{ka}} − {{kb}}p. At what price is demand unit elastic (E = 1)?",
    given={"ka": {"pick": [100, 240, 600]}, "kb": {"pick": [2, 4, 5]}}, value="ka/(2*kb)", tex="p", verify="solve(Eq(kb*x/(ka - kb*x), 1), x)[0]",
    explain="E = bp/(a − bp) = 1 at p = a/(2b), the midpoint of a linear demand curve, which is also where revenue peaks")),
 ("CA-16.2.A", Q("ca-producer-surplus", IA, "Supply is p = {{kc}} + {{kd}}q and the market price is {{kp}}. What is the producer surplus?",
    given={"kc": {"pick": [5, 10]}, "kd": {"pick": [0.5, 1, 2]}, "kp": {"pick": [20, 30, 50]}}, value="(kp - kc)^2/(2*kd)", tex="PS",
    verify="integrate(kp - (kc + nsimplify(kd)*x), (x, 0, (kp - kc)/nsimplify(kd)))",
    explain="Producer surplus is the area between the market price and the supply curve, out to the quantity supplied: a triangle here")),
 ("CA-16.2.B", Q("ca-dye-amount", IA, "A heart pumps {{kf}} L/s. Dye injected upstream leaves with concentration c(t) = {{kk}}·t({{kt}} − t) mg/L for 0 ≤ t ≤ {{kt}} s. How much dye was injected, in mg?",
    given={"kf": {"pick": [0.08, 0.1, 0.12]}, "kk": {"pick": [0.3, 0.5]}, "kt": {"pick": [10, 12, 20]}}, value="kf*kk*kt^3/6", tex="A",
    verify="nsimplify(kf)*integrate(nsimplify(kk)*x*(kt - x), (x, 0, kt))", explain="All the dye passes the sensor, so the amount is flow × ∫ c dt; the same relation read the other way gives the cardiac output")),
 ("CA-16.2.C", Q("ca-pdf-mean", IA, "f(x) = k·x^{{kn}} on [0, {{kl}}] (and 0 elsewhere) is a probability density. What is its mean?",
    given={"kn": {"pick": [1, 2, 3]}, "kl": {"pick": [1, 2, 4]}}, value="(kn + 1)*kl/(kn + 2)", tex="\\mu",
    verify="integrate(x*x**kn, (x, 0, kl))/integrate(x**kn, (x, 0, kl))", explain="Normalise first (k = (n + 1)/L^(n+1)), then μ = ∫ x f(x) dx. The mean sits past the midpoint because the density rises")),
 ("CA-17.1.A", L("ca-trig-integral-strategy", AD, "To integrate {{q}}, the most direct first move is:", ["Save one sin x and substitute u = cos x", "Save one cos x and substitute u = sin x", "Use the half-angle identities"], [
    ("sin³x cos²x", 0), ("sin²x cos³x", 1), ("sin²x cos²x", 2), ("sin⁵x cos⁴x", 0), ("sin⁴x cos x", 1), ("sin⁴x", 2), ("cos³x", 1)],
    "An odd power lends one factor to du and the rest converts with sin² + cos² = 1. Only when both powers are even do you need the half-angle identities")),
 ("CA-17.1.B", L("ca-trig-sub-choice", AD, "Which substitution removes the root in an integral containing {{q}}?", ["x = a sin θ", "x = a tan θ", "x = a sec θ"], [
    ("√(9 − x²)", 0), ("√(x² + 4)", 1), ("√(x² − 25)", 2), ("(16 + x²)^(3/2)", 1), ("√(1 − x²)", 0), ("√(x² − 1)", 2)],
    "Match the Pythagorean identity: a² − a² sin² = a² cos², a² + a² tan² = a² sec², a² sec² − a² = a² tan²")),
 ("CA-17.1.C", Q("ca-table-arctan", AD, "A table gives ∫ dx/(a² + x²) = (1/a) arctan(x/a) + C. Evaluate ∫ from 0 to {{ka}} of dx/({{ks}} + x²).",
    cases=[{"ka": 2, "ks": 4}, {"ka": 3, "ks": 9}, {"ka": 5, "ks": 25}, {"ka": 4, "ks": 16}], value="pi/(4*ka)", tex="I", verify="integrate(1/(ks + x**2), (x, 0, ka))",
    explain="Read a from the constant (a² = the number, so a is its square root), then arctan(1) − arctan(0) = π/4, divided by a")),
 ("CA-17.1.D", Q("ca-cas-check", AD, "A computer algebra system returns F(x) = e^({{ka}}x)(x/{{ka}} − 1/{{ks}}) for ∫ x e^({{ka}}x) dx. To check it, differentiate: what should F′({{kx}}) equal?",
    cases=[{"ka": 2, "ks": 4, "kx": 1}, {"ka": 3, "ks": 9, "kx": 1}, {"ka": 2, "ks": 4, "kx": 0.5}, {"ka": 1, "ks": 1, "kx": 2}], value="kx*exp(ka*kx)", tex="F'",
    verify="diff(exp(ka*x)*(x/ka - Rational(1, ks)), x).subs(x, nsimplify(kx))", explain="If F is right, F′ is the integrand, x e^(ax). The product rule on F cancels everything else")),
 ("CA-17.2.A", Q("ca-shells-power", IA, "The region under y = x^{{kn}} for 0 ≤ x ≤ 1 is spun about the y-axis. Find the volume by shells.",
    given={"kn": {"pick": [1, 2, 3, 4]}}, value="2*pi/(kn + 2)", tex="V", verify="pi - integrate(pi*Y**Rational(2, kn), (Y, 0, 1))",
    explain="Shells: ∫ 2πx·xⁿ dx = 2π/(n + 2). The check is the cylinder of volume π minus the washers' hole, ∫ π y^(2/n) dy")),
 ("CA-17.2.B", Q("ca-two-methods-x-axis", IA, "The region between y = x², the x-axis and x = {{ka}} is spun about the x-axis. Find the volume.",
    given={"ka": {"pick": [1, 2, 3]}}, value="pi*ka^5/5", tex="V", verify="integrate(2*pi*Y*(ka - sqrt(Y)), (Y, 0, ka**2))",
    explain="Discs in x: ∫ π x⁴ dx. Shells in y give the same number: radius y, height a − √y")),
 ("CA-17.2.C", Q("ca-cone-frustum-area", IA, "The line y = {{km}}x for {{ka}} ≤ x ≤ {{kb}} is spun about the x-axis. Find the area of the surface it sweeps.",
    cases=[{"km": 1, "ka": 1, "kb": 2}, {"km": 2, "ka": 1, "kb": 3}, {"km": 0.75, "ka": 4, "kb": 8}, {"km": 1, "ka": 2, "kb": 5}], value="pi*km*sqrt(1 + km^2)*(kb^2 - ka^2)", tex="S",
    verify="pi*(nsimplify(km)*ka + nsimplify(km)*kb)*sqrt((kb - ka)**2 + (nsimplify(km)*(kb - ka))**2)",
    explain="∫ 2π y √(1 + y′²) dx = 2π m √(1 + m²) ∫ x dx. It agrees with the frustum formula π(r₁ + r₂) × slant length")),
 ("CA-17.2.D", Q("ca-hydrostatic-gate", IA, "A vertical rectangular gate {{kw}} m wide and {{kh}} m tall has its top edge {{kd}} m below the water surface (ρg = 9810 N/m³). Find the force on it, in N.",
    given={"kw": {"pick": [2, 3]}, "kh": {"pick": [1, 2, 4]}, "kd": {"pick": [1, 3, 5]}}, value="9810*kw*((kd + kh)^2 - kd^2)/2", tex="F",
    verify="9810*kw*kh*(kd + Rational(kh, 2))", explain="∫ ρg·depth·width d(depth) from d to d + h. It equals the pressure at the gate's centroid times its area")),
 ("CA-18.1.A", Q("ca-sequence-limit-e", SE, "Find the limit of (1 + {{ka}}/n)^n as n → ∞.", given={"ka": {"pick": [2, 3, 5]}}, value="exp(ka)", tex="L",
    verify="limit((1 + Rational(ka)/nn)**nn, nn, oo)", explain="Take logs: n ln(1 + a/n) → a, so the limit is e^a")),
 ("CA-18.1.B", L("ca-root-test-verdict", SE, "For the series with terms ({{q}})^n, the root test says it:", ["Converges", "Diverges", "Is inconclusive"], [
    ("2n/(3n + 1)", 0), ("5n/(2n + 1)", 1), ("n/(n + 1)", 2), ("n/(4n + 1)", 0), ("3n/(3n + 1)", 2), ("7n/(6n + 1)", 1)],
    "The nth root is an/(bn + 1) → a/b. Below 1 converges, above 1 diverges, exactly 1 tells you nothing (here the terms do not even tend to 0, so the series diverges by the nth-term test)")),
 ("CA-18.1.C", L("ca-series-verdict", SE, "The series with terms {{q}} (n from 2 upward):", ["Converges", "Diverges"], [
    ("1/n^1.5", 0), ("n/(2n + 1)", 1), ("(−1)^n/√n", 0), ("3^n/n!", 0), ("1/(n ln n)", 1), ("(2/3)^n", 0), ("n!/10^n", 1), ("1/√n", 1)],
    "p-series need p > 1; terms that do not tend to 0 diverge at once; factorials beat exponentials; 1/(n ln n) diverges by the integral test")),
 ("CA-18.2.A", Q("ca-eliminate-exponential", PP, "A curve is x = e^t, y = e^(2t) + {{kc}}. Eliminate t and find y when x = {{kx}}.",
    given={"kc": {"pick": [1, 3, 5]}, "kx": {"pick": [2, 3, 4]}}, value="kx^2 + kc", tex="y", verify="(exp(2*x) + kc).subs(x, log(kx))", final=True,
    explain="e^(2t) = (e^t)² = x², so y = x² + c (for x > 0 only, since e^t is positive)")),
 ("CA-18.2.B", Q("ca-ellipse-area-parametric", PP, "Find the area enclosed by x = {{ka}} cos t, y = {{kb}} sin t.",
    given={"ka": {"pick": [2, 3, 5]}, "kb": {"pick": [1, 2, 4]}}, value="pi*ka*kb", tex="A", verify="integrate(kb*sin(x)*ka*sin(x), (x, 0, 2*pi))",
    explain="A = ∮ y dx taken clockwise = ∫ b sin t · a sin t dt over a full turn = πab")),
 ("CA-18.2.C", Q("ca-ellipsoid-volume-parametric", PP, "The upper half of x = {{ka}} cos t, y = {{kb}} sin t (0 ≤ t ≤ π) is spun about the x-axis. Find the volume.",
    given={"ka": {"pick": [2, 3, 5]}, "kb": {"pick": [1, 2, 3]}}, value="4*pi*ka*kb^2/3", tex="V", verify="integrate(pi*(kb*sin(x))**2*ka*sin(x), (x, 0, pi))",
    explain="V = ∫ π y² dx with dx = −a sin t dt, taken so that x runs left to right: an ellipsoid of semi-axes a, b, b")),
 ("CA-18.2.D", Q("ca-parametric-cap-area", PP, "The arc x = {{kr}} cos t, y = {{kr}} sin t for 0 ≤ t ≤ {{kd}}° is spun about the x-axis. Find the area of the cap it sweeps.",
    given={"kr": {"pick": [1, 2, 3]}, "kd": {"pick": [30, 60, 90]}}, value="2*pi*kr^2*(1 - cos(kd*pi/180))", tex="S", verify="integrate(2*pi*kr*sin(x)*kr, (x, 0, kd*pi/180))",
    explain="S = ∫ 2π y √(x′² + y′²) dt, and the speed on a circle is r. The result is 2πr × the cap's height, Archimedes' hat-box theorem")),
 ("CA-18.2.E", Q("ca-polar-spiral-length", PP, "Find the length of the spiral r = e^θ for 0 ≤ θ ≤ {{kt}}.", given={"kt": {"pick": [1, 2, 3]}}, value="sqrt(2)*(exp(kt) - 1)", tex="L",
    verify="integrate(sqrt(exp(x)**2 + diff(exp(x), x)**2), (x, 0, kt))", explain="r and dr/dθ are both e^θ, so the integrand is √2 e^θ")),
 ("CA-18.2.F", Q("ca-vector-limit-magnitude", V3, "Find the length of the limit as t → 0 of ⟨sin({{ka}}t)/t, (1 − cos t)/t, {{kb}}⟩.",
    cases=[{"ka": 3, "kb": 4}, {"ka": 5, "kb": 12}, {"ka": 8, "kb": 6}, {"ka": 1, "kb": 1}], value="sqrt(ka^2 + kb^2)", tex="|L|",
    verify="sqrt(limit(sin(ka*x)/x, x, 0)**2 + limit((1 - cos(x))/x, x, 0)**2 + kb**2)", explain="Component by component: sin(at)/t → a, (1 − cos t)/t → 0, and the constant stays")),
]
