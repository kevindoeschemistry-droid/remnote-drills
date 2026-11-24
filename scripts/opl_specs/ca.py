import sympy as sp
from opl_dsl import Q, L, U

FW, FILE, IDEA = "CA", "opl-ca", "CHA"

_x = sp.Symbol("x")
TRIG = []
for m, n in [(3, 2), (2, 3), (3, 0), (5, 2), (2, 2), (4, 0), (1, 4), (3, 3)]:
    v = sp.integrate(sp.sin(_x)**m * sp.cos(_x)**n, (_x, 0, sp.pi / 2))
    TRIG.append({"m": m, "n": n, "val": float(v)})

UNITS = [
U(16, "applied-fields", "Calculus in business, the sciences and probability", [
    ("Derivatives in context", [
        L("A", "Find a marginal cost or revenue as a derivative.", "Marginal cost C′(q) approximates the cost of one more unit.", ["CA3.3"], [
            Q("ca-marginal-cost", "calc.rates", "A cost function is $C(q) = {{F}} + {{b}}q + {{c}}q^2$ dollars. What is the marginal cost at $q = {{q0}}$, in dollars per unit?",
              given={"F": {"pick": [500, 1000, 2000]}, "b": {"int": [5, 30]}, "c": {"pick": [0.01, 0.02, 0.05, 0.1]}, "q0": {"pick": [50, 100, 200]}},
              value="b + 2*c*q0", tex="C'(q)", verify="diff(F + b*x + nsimplify(c)*x**2, x).subs(x, q0)",
              explain="Marginal cost is $C'(q) = {{b}} + 2({{c}})q$. The fixed cost ${{F}}$ does not affect it")]),
        L("B", "Maximise profit from revenue and cost functions.", "Profit is maximal where marginal revenue equals marginal cost.", ["CA3.11"], [
            Q("ca-max-profit", "calc.extrema", "Items sell for ${{p}}$ dollars each, and making $q$ of them costs $C(q) = {{F}} + {{c}}q + {{d}}q^2$ dollars. How many items maximise profit?",
              given={"p": {"pick": [40, 60, 80, 100]}, "F": {"pick": [200, 500]}, "c": {"pick": [10, 20]}, "d": {"pick": [0.05, 0.1, 0.2]}},
              value="(p - c)/(2*d)", tex="q^*", verify="solve(diff(p*x - (F + c*x + nsimplify(d)*x**2), x), x)[0]",
              explain="$P(q) = {{p}}q - C(q)$. Setting $P'(q) = 0$ gives ${{p}} = {{c}} + 2({{d}})q$: marginal revenue equals marginal cost. $P'' < 0$, so it is a maximum")]),
        L("C", "Optimise a model from the natural sciences.", "Set the derivative to zero and check that the critical point is a maximum.", ["CA3.13"], [
            Q("ca-peak-concentration", "calc.extrema", "After a dose, a drug's blood concentration is $C(t) = {{A}}\\,t\\,e^{-{{k}}t}$ (t in hours). When is the concentration highest, in hours?",
              given={"A": {"pick": [5, 10, 20]}, "k": {"pick": [0.1, 0.2, 0.25, 0.5]}}, value="1/k", tex="t^*",
              verify="solve(diff(A*x*exp(-nsimplify(k)*x), x), x)[0]",
              explain="$C'(t) = Ae^{-kt}(1 - kt) = 0$ at $t = 1/k$. The same shape (rise, then exponential decay) describes many absorption–elimination models")]),
        L("D", "Compute a price elasticity of demand.", "E = −(dq/dp)(p/q); |E| > 1 is elastic.", ["CA3.18"], [
            Q("ca-elasticity", "calc.derivative-rules", "Demand is $q = {{a}} - {{b}}p$. What is the price elasticity of demand $E = -\\dfrac{p}{q}\\dfrac{dq}{dp}$ at $p = {{p0}}$?",
              given={"a": {"pick": [100, 200, 500]}, "b": {"pick": [2, 4, 5]}, "p0": {"pick": [5, 10, 15, 20]}}, require=["a - b*p0 > 0"],
              value="b*p0/(a - b*p0)", tex="E", verify="(-x/(a - b*x)*diff(a - b*x, x)).subs(x, p0)",
              explain="$E = \\dfrac{bp}{a - bp}$. Where $E > 1$ demand is elastic and raising the price lowers revenue; where $E < 1$ it raises revenue")]),
    ]),
    ("Integrals in context", [
        L("A", "Find a consumer surplus.", "CS = ∫₀^q₀ (demand price − market price) dq.", ["CA6.15"], [
            Q("ca-consumer-surplus", "calc.integration-apps", "Demand is $p = {{a}} - {{b}}q$ and the market price is ${{p0}}$. What is the consumer surplus?",
              given={"a": {"pick": [50, 80, 100]}, "b": {"pick": [0.5, 1, 2]}, "p0": {"pick": [20, 30, 40]}},
              value="(a - p0)^2/(2*b)", tex="CS", verify="integrate(a - nsimplify(b)*x - p0, (x, 0, (a - p0)/nsimplify(b)))",
              explain="Buyers who would have paid more than ${{p0}}$ save the difference. Integrate from 0 to the quantity sold, $q_0 = (a - p_0)/b$: a triangle")]),
        L("B", "Find cardiac output from a dye-dilution curve.", "F = amount injected / ∫ c dt.", ["CA6.16"], [
            Q("ca-cardiac-output", "calc.integration-apps", "{{A}} mg of dye is injected and its concentration leaving the heart is $c(t) = {{k}}\\,t({{T}} - t)$ mg/L for $0 \\le t \\le {{T}}$ s. What is the cardiac output, in L/s?",
              given={"A": {"pick": [5, 8, 10]}, "k": {"pick": [0.01, 0.02, 0.05]}, "T": {"pick": [10, 12, 15]}},
              value="A/(k*T^3/6)", tex="F", verify="A/integrate(nsimplify(k)*x*(T - x), (x, 0, T))",
              explain="All the dye passes through: $A = F\\int_0^T c\\,dt$. The integral of the parabola is $kT^3/6$")]),
        L("C", "Use a probability density function.", "A density integrates to 1; probabilities are areas under it.", ["CA6.17"], [
            Q("ca-pdf-constant", "calc.integration-apps", "$f(x) = k\\,x^{ {{n}} }$ on $[0, {{L}}]$ (and 0 elsewhere) is a probability density. What is $k$?",
              given={"n": {"int": [1, 3]}, "L": {"pick": [1, 2, 3, 4]}}, value="(n + 1)/L^(n + 1)", tex="k",
              verify="solve(Eq(integrate(Symbol('k')*x**n, (x, 0, L)), 1), Symbol('k'))[0]",
              explain="Total probability is 1: $k\\dfrac{L^{n+1}}{n + 1} = 1$. Then $P(a < X < b) = \\int_a^b f$")]),
    ]),
]),
U(17, "more-integration", "More integration techniques and applications", [
    ("Techniques", [
        L("A", "Integrate a product of powers of sine and cosine.", "With an odd power, save one factor and convert the rest; with even powers, use half-angle identities.", ["CA5.5"], [
            Q("ca-trig-integral", "calc.antiderivatives", "Evaluate $\\displaystyle\\int_0^{\\pi/2} \\sin^{ {{m}} }x\\,\\cos^{ {{n}} }x\\,dx$.", cases=TRIG,
              value="val", tex="I", tol=0.0001, verify="integrate(sin(x)**m*cos(x)**n, (x, 0, pi/2))",
              explain="Odd power of sine: keep one $\\sin x$ for $du$ with $u = \\cos x$ and write the rest with $\\sin^2 = 1 - \\cos^2$ (and the same with sine and cosine swapped). Both even: $\\sin^2 x = \\tfrac12(1 - \\cos 2x)$")]),
        L("B", "Evaluate an integral by trigonometric substitution.", "√(a² − x²): x = a sin θ; √(a² + x²): x = a tan θ; √(x² − a²): x = a sec θ.", ["CA5.8"], [
            Q("ca-trig-substitution", "calc.antiderivatives", "Evaluate $\\displaystyle\\int_0^{ {{a}} } \\frac{x^2}{\\sqrt{ {{a^2}} - x^2}}\\,dx$.",
              given={"a": {"int": [1, 6]}}, value="pi*a^2/4", tex="I", verify="integrate(x**2/sqrt(a**2 - x**2), (x, 0, a))",
              explain="$x = {{a}}\\sin\\theta$ turns $\\sqrt{a^2 - x^2}$ into $a\\cos\\theta$ and $dx$ into $a\\cos\\theta\\,d\\theta$; the integral becomes $a^2\\int_0^{\\pi/2}\\sin^2\\theta\\,d\\theta = \\pi a^2/4$")]),
        L("C", "Use an integral from a table.", "Match the integrand to the table form, identify the constants, then substitute.", ["CA5.9"], [
            Q("ca-integral-table", "calc.antiderivatives", "A table gives $\\displaystyle\\int \\frac{dx}{x(a + bx)} = \\frac1a\\ln\\left|\\frac{x}{a + bx}\\right| + C$. Evaluate $\\displaystyle\\int_1^2 \\frac{dx}{x({{a}} + {{b}}x)}$.",
              given={"a": {"int": [1, 5]}, "b": {"int": [1, 4]}}, value="(log(2/(a + 2*b)) - log(1/(a + b)))/a", tex="I",
              verify="integrate(1/(x*(a + b*x)), (x, 1, 2))",
              explain="Here $a = {{a}}$, $b = {{b}}$: $\\frac{1}{ {{a}} }\\left[\\ln\\frac{2}{ {{a + 2*b}} } - \\ln\\frac{1}{ {{a + b}} }\\right]$. Partial fractions gives the same thing")]),
        L("D", "Use and check a computer algebra system's antiderivative.", "Differentiate the CAS answer to check it, then apply the fundamental theorem.", ["CA5.10"], [
            Q("ca-cas-antiderivative", "calc.antiderivatives", "A computer algebra system returns $\\displaystyle\\int x e^{ {{a}}x}\\,dx = e^{ {{a}}x}\\left(\\frac{x}{ {{a}} } - \\frac{1}{ {{a^2}} }\\right) + C$. Use it to evaluate $\\displaystyle\\int_0^1 x e^{ {{a}}x}\\,dx$.",
              given={"a": {"pick": [-2, -1, 1, 2, 3]}}, value="exp(a)*(1/a - 1/a^2) + 1/a^2", tex="I", verify="integrate(x*exp(a*x), (x, 0, 1))",
              explain="Evaluate at 1 and subtract the value at 0, which is $-1/a^2$. Differentiating the CAS answer gives back $xe^{ax}$, which is the check worth doing before trusting it")]),
    ]),
    ("Volumes, surfaces and forces", [
        L("A", "Find a volume by cylindrical shells.", "V = ∫ 2π (radius)(height) dx.", ["CA6.6"], [
            Q("ca-shells", "calc.integration-apps", "The region under $y = {{k}}x - x^2$ (above the $x$-axis) is spun about the $y$-axis. Find the volume.",
              given={"k": {"int": [1, 5]}}, value="pi*k^4/6", tex="V", verify="integrate(2*pi*x*(k*x - x**2), (x, 0, k))",
              explain="Shells of radius $x$ and height ${{k}}x - x^2$: $V = \\int_0^{ {{k}} } 2\\pi x({{k}}x - x^2)\\,dx$. Washers would need $x$ as a function of $y$, which here means two branches")]),
        L("B", "Find the same volume by two methods.", "Discs or washers in one variable and shells in the other must agree.", ["CA6.7"], [
            Q("ca-two-methods", "calc.integration-apps", "The region between $y = x^2$, the $x$-axis and $x = {{a}}$ is spun about the $y$-axis. Find the volume.",
              given={"a": {"int": [1, 4]}}, value="pi*a^4/2", tex="V", verify="integrate(pi*(a**2 - x), (x, 0, a**2))",
              explain="Shells: $\\int_0^a 2\\pi x\\cdot x^2\\,dx$. Washers in $y$: outer radius $a$, inner $\\sqrt y$: $\\int_0^{a^2} \\pi(a^2 - y)\\,dy$. Both give $\\pi a^4/2$")]),
        L("C", "Find the area of a surface of revolution.", "S = ∫ 2π y √(1 + y′²) dx.", ["CA6.9"], [
            Q("ca-surface-revolution", "calc.integration-apps", "The line $y = {{m}}x$, $0 \\le x \\le {{L}}$, is spun about the $x$-axis to make a cone. What is the cone's lateral surface area?",
              cases=[{"m": 0.75, "s": 1.25}, {"m": 1.333333333333333, "s": 1.666666666666667}, {"m": 2.4, "s": 2.6}],
              given={"L": {"int": [1, 5]}}, value="pi*m*L^2*sqrt(1 + m^2)", tex="S", tol=0.001,
              verify="integrate(2*pi*nsimplify(m)*x*sqrt(1 + nsimplify(m)**2), (x, 0, L))",
              explain="$S = \\int_0^L 2\\pi(mx)\\sqrt{1 + m^2}\\,dx = \\pi mL^2\\sqrt{1 + m^2}$: the familiar $\\pi r\\ell$ with $r = mL$ and slant $\\ell = L\\sqrt{1 + m^2}$")]),
        L("D", "Find the hydrostatic force on a submerged plate by integration.", "F = ∫ ρ g (depth) (width at that depth) d(depth).", ["CA6.12"], [
            Q("ca-hydrostatic-triangle", "calc.integration-apps", "A triangular plate with its {{b}} m base at the water surface and its apex {{h}} m below hangs vertically in water ($\\rho g = 9810$ N/m³). What is the force on one side, in kN?",
              given={"b": {"pick": [1, 2, 3, 4]}, "h": {"pick": [1, 2, 3]}}, value="9810*b*h^2/6/1000", tex="F",
              verify="integrate(9810*x*b*(1 - x/h), (x, 0, h))/1000",
              explain="At depth $y$ the width is ${{b}}(1 - y/{{h}})$; $F = \\int_0^h \\rho g\\,y\\,b(1 - y/h)\\,dy = \\rho g b h^2/6$. Pressure, not area alone, decides the force: the wide part is shallow")]),
    ]),
]),
U(18, "sequences-curves", "Sequences, series strategy, parametric and polar curves", [
    ("Sequences and series", [
        L("A", "Find the limit of a sequence.", "Divide by the highest power of n.", ["CA7.1"], [
            Q("ca-sequence-limit", "calc.series", "Find $\\displaystyle\\lim_{n\\to\\infty} \\frac{ {{p}}n^2 + {{q}} }{ {{r}}n^2 + {{s}}n}$.",
              given={"p": {"int": [1, 9]}, "q": {"int": [-5, 5]}, "r": {"int": [1, 9]}, "s": {"int": [1, 6]}}, value="p/r", tex="L",
              verify="limit((p*x**2 + q)/(r*x**2 + s*x), x, oo)",
              explain="Divide top and bottom by $n^2$: everything else goes to 0. A sequence converges when its terms settle; a series converges when its partial sums do")]),
        L("B", "Apply the root test.", "L = lim |aₙ|^(1/n); converges if L < 1, diverges if L > 1.", ["CA7.10"], [
            Q("ca-root-test", "calc.series", "For $\\displaystyle\\sum_{n=1}^\\infty \\left(\\frac{ {{a}}n}{ {{b}}n + 1}\\right)^n$, find the root-test limit $\\lim |a_n|^{1/n}$.",
              given={"a": {"int": [1, 7]}, "b": {"int": [1, 7]}}, value="a/b", tex="L", verify="limit(a*x/(b*x + 1), x, oo)",
              explain="The $n$th root strips the outer power: $\\frac{ {{a}}n}{ {{b}}n + 1} \\to {{a}}/{{b}}$. Below 1 converges, above 1 diverges; equal to 1 says nothing")]),
        L("C", "Choose a convergence test for a series.", "Look at the form: geometric, p-series, factorials (ratio), nth powers (root), alternating, or a comparison.", ["CA7.13"], [
            Q("ca-series-strategy", "calc.series", "Which test settles $\\displaystyle\\sum {{s}}$ most directly?", pace="recall",
              cases=[{"s": "\\frac{n!}{5^n}", "ans": 0}, {"s": "\\left(\\frac{2n}{3n + 1}\\right)^n", "ans": 1}, {"s": "\\frac{(-1)^n}{\\sqrt n}", "ans": 2},
                     {"s": "\\frac{1}{n^2 + 7}", "ans": 3}, {"s": "\\frac{n}{n + 1}", "ans": 4}, {"s": "\\frac{3^n}{n!}", "ans": 0},
                     {"s": "\\frac{(-1)^n n}{n^2 + 1}", "ans": 2}, {"s": "\\frac{1}{2^n + n}", "ans": 3}],
              choice=["Ratio test", "Root test", "Alternating series test", "Comparison test", "nth-term (divergence) test"], correct="ans", verify="authored",
              explain="Factorials → ratio. A whole expression to the nth power → root. Alternating signs with terms shrinking to 0 → alternating series test. Looks like a p-series or geometric series → compare. Terms that do not go to 0 → divergence")]),
    ]),
    ("Parametric and polar curves", [
        L("A", "Eliminate the parameter.", "Solve one equation for t and substitute into the other.", ["CA8.2"], [
            Q("ca-eliminate-parameter", "calc.parametric-polar", "A curve is $x = t + {{h}}$, $y = {{b}}t^2 + {{c}}$. Eliminate $t$ and find $y$ when $x = {{x1}}$.",
              given={"h": {"int": [-3, 3]}, "b": {"int": [1, 4]}, "c": {"int": [-5, 5]}, "x1": {"int": [-3, 4]}}, require=["b*(x1 - h)^2 + c != 0"],
              value="b*(x1 - h)^2 + c", tex="y", verify="(b*Symbol('t')**2 + c).subs(Symbol('t'), solve(Eq(Symbol('t') + h, x1), Symbol('t'))[0])",
              explain="$t = x - {{h}}$, so $y = {{b}}(x - {{h}})^2 + {{c}}$: a parabola. Eliminating the parameter loses the direction and speed of travel")]),
        L("B", "Find the area under a parametric curve.", "A = ∫ y dx = ∫ y(t) x′(t) dt.", ["CA8.6"], [
            Q("ca-parametric-area", "calc.parametric-polar", "Find the area under $x = t^2$, $y = t^3$ for $0 \\le t \\le {{T}}$ (between the curve and the $x$-axis).",
              given={"T": {"pick": [1, 2, 3]}}, value="2*T^5/5", tex="A", verify="integrate(x**Rational(3, 2), (x, 0, T**2))",
              explain="$\\int y\\,dx = \\int_0^T t^3\\cdot 2t\\,dt = \\tfrac25T^5$. Eliminating $t$ gives $y = x^{3/2}$, which integrates to the same")]),
        L("C", "Find a volume of revolution for a parametric curve.", "V = ∫ π y² dx with dx = x′(t) dt.", ["CA8.7"], [
            Q("ca-parametric-volume", "calc.parametric-polar", "The upper half of $x = {{r}}\\cos t$, $y = {{r}}\\sin t$ ($0 \\le t \\le \\pi$) is spun about the $x$-axis. Find the volume.",
              given={"r": {"int": [1, 5]}}, value="4*pi*r^3/3", tex="V", verify="integrate(pi*(r**2 - x**2), (x, -r, r))",
              explain="$V = \\int \\pi y^2\\,dx = \\int_\\pi^0 \\pi r^2\\sin^2 t\\,(-r\\sin t)\\,dt = \\tfrac43\\pi r^3$, the sphere")]),
        L("D", "Find a surface area of revolution for a parametric curve.", "S = ∫ 2π y √(x′² + y′²) dt.", ["CA8.8"], [
            Q("ca-parametric-surface", "calc.parametric-polar", "The upper half of $x = {{r}}\\cos t$, $y = {{r}}\\sin t$ is spun about the $x$-axis. Find the surface area.",
              given={"r": {"int": [1, 5]}}, value="4*pi*r^2", tex="S", verify="integrate(2*pi*r*sin(Symbol('t'))*r, (Symbol('t'), 0, pi))",
              explain="$\\sqrt{x'^2 + y'^2} = r$, so $S = \\int_0^\\pi 2\\pi r\\sin t\\cdot r\\,dt = 4\\pi r^2$")]),
        L("E", "Find the arc length of a polar curve.", "L = ∫ √(r² + (dr/dθ)²) dθ.", ["CA9.7"], [
            Q("ca-polar-arc-length", "calc.parametric-polar", "Find the length of the cardioid $r = {{a}}(1 + \\cos\\theta)$.",
              given={"a": {"int": [1, 6]}}, value="8*a", tex="L", verify="2*integrate(2*a*cos(x/2), (x, 0, pi))",
              explain="$r^2 + r'^2 = 2a^2(1 + \\cos\\theta) = 4a^2\\cos^2(\\theta/2)$, so $L = \\int_0^{2\\pi} 2a|\\cos(\\theta/2)|\\,d\\theta = 8a$. Watch the absolute value past $\\theta = \\pi$")]),
        L("F", "Find the limit of a vector function.", "Take the limit of each component.", ["MV2.2"], [
            Q("ca-vector-limit", "calc.vectors-3d", "Find the second component of $\\displaystyle\\lim_{t\\to0}\\left\\langle \\frac{\\sin {{a}}t}{t},\\; \\frac{e^{ {{b}}t} - 1}{t},\\; \\cos t\\right\\rangle$.",
              given={"a": {"int": [1, 5]}, "b": {"pick": [-3, -2, 2, 3, 4]}}, value="b", tex="L_2", verify="limit((exp(b*x) - 1)/x, x, 0)",
              explain="Componentwise: the first is ${{a}}$, the second is the derivative of $e^{bt}$ at 0, which is ${{b}}$, the third is 1")]),
    ]),
]),
]
