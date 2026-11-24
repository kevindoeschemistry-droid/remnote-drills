from opl_dsl import Q, L, U

FW, FILE, IDEA = "EM", "opl-em", "MODEL"

PYTH = [{"a": 3, "b": 4, "r": 5}, {"a": 5, "b": 12, "r": 13}, {"a": 8, "b": 6, "r": 10}, {"a": -3, "b": 4, "r": 5}, {"a": 7, "b": 24, "r": 25}]

UNITS = [
U(13, "ode-more", "More on ODEs: circuits, bifurcations, operators, existence", [
    ("Applications and theory", [
        L("A", "Solve an RC circuit.", "R q′ + q/C = E: the charge rises with time constant RC and the current decays.", ["DE2.9"], [
            Q("em-rc-current", "ode1.modeling", "An RC circuit ($R = {{R}}\\,\\Omega$, $C = {{C}}$ F) is switched onto a ${{E}}$ V battery with the capacitor uncharged. What is the current, in A, at $t = {{t}}$ s?",
              given={"R": {"pick": [10, 50, 100]}, "C": {"pick": [0.01, 0.02, 0.05]}, "E": {"pick": [6, 9, 12]}, "t": {"pick": [0.5, 1, 2]}},
              value="E/R*exp(-t/(R*C))", tex="i(t)", tol=0.001,
              verify="diff(nsimplify(C)*E*(1 - exp(-x/(R*nsimplify(C)))), x).subs(x, nsimplify(t))",
              explain="$q(t) = CE(1 - e^{-t/RC})$, and $i = dq/dt = \\dfrac ER e^{-t/RC}$. The time constant here is $RC = {{R*C}}$ s; after five of them the capacitor is essentially full")]),
        L("B", "Locate a saddle-node bifurcation.", "Equilibria appear or vanish where f(y) = 0 and f′(y) = 0 together.", ["DE2.14"], [
            Q("em-bifurcation", "ode1.modeling", "For $y' = y^2 - {{2*a}}y + r$, at what value of $r$ do the two equilibria merge and disappear?",
              given={"a": {"pick": [-3, -2, -1, 1, 2, 3, 4]}}, value="a^2", tex="r_c",
              verify="solve(Eq((2*a)**2 - 4*x, 0), x)[0]",
              explain="Equilibria solve $y^2 - 2ay + r = 0$: two when $r < a^2$, one (half-stable) at $r = a^2$, none beyond. At a saddle-node bifurcation the phase line changes its count of equilibria")]),
        L("C", "Apply a differential operator.", "L[e^{kx}] = p(k)e^{kx} for L = p(D) with constant coefficients.", ["DE3.12"], [
            Q("em-operator-exponential", "ode2.higher-order", "Let $L = D^2 + ({{a}})D + ({{b}})$ with $D = d/dx$. Then $L[e^{ {{k}}x}] = c\\,e^{ {{k}}x}$. Find $c$.",
              given={"a": {"int": [-4, 4]}, "b": {"int": [-6, 6]}, "k": {"int": [-3, 3]}}, require=["k^2 + a*k + b != 0", "k != 0"],
              value="k^2 + a*k + b", tex="c", verify="simplify((diff(exp(k*x), x, 2) + a*diff(exp(k*x), x) + b*exp(k*x))/exp(k*x))",
              explain="Each $D$ brings down a factor ${{k}}$: $L[e^{kx}] = (k^2 + ak + b)e^{kx}$, the characteristic polynomial. That is why $e^{rx}$ solves $L[y] = 0$ exactly at its roots")]),
        L("D", "Find the interval on which a linear IVP is guaranteed a unique solution.", "The largest open interval around x₀ on which all coefficients are continuous.", ["DE3.13"], [
            Q("em-existence-interval", "ode2.wronskian", "$y'' + \\dfrac{1}{x - {{a}}}y' + \\dfrac{1}{x + {{c}}}y = 0$ with $y({{x0}}) = 1$, $y'({{x0}}) = 0$. How long is the largest interval on which a unique solution is guaranteed?",
              given={"a": {"int": [2, 8]}, "c": {"int": [1, 6]}, "x0": {"int": [-0, 1]}}, value="a + c", tex="\\ell",
              verify="a - (-c)",
              explain="The coefficients break down at $x = {{a}}$ and $x = {{-c}}$; the initial point ${{x0}}$ lies between them, so the guarantee holds on $({{-c}}, {{a}})$. The solution may well extend further; the theorem just does not promise it")]),
        L("E", "Verify that a vector function solves a linear system.", "x = e^{λt}v solves x′ = Ax exactly when Av = λv.", ["DE5.2"], [
            Q("em-system-verify", "odesys.eigenvalue", "For which $\\lambda$ does $\\mathbf x = e^{\\lambda t}\\begin{pmatrix} 1 \\\\ {{s}} \\end{pmatrix}$ solve $\\mathbf x' = \\begin{pmatrix} {{p}} & 1 \\\\ {{s^2}} & {{p}} \\end{pmatrix}\\mathbf x$?",
              given={"p": {"int": [-3, 3]}, "s": {"pick": [-2, -1, 1, 2, 3]}}, require=["p + s != 0"], value="p + s", tex="\\lambda",
              verify="(Matrix([[p, 1], [s**2, p]])*Matrix([1, s]))[0]",
              explain="Substitute: $\\lambda e^{\\lambda t}v = Ae^{\\lambda t}v$, so $Av = \\lambda v$. The first row gives $\\lambda = {{p}} + {{s}}$; check the second row agrees")]),
    ]),
]),
U(14, "complex", "Complex analysis", [
    ("Complex equations, regions and functions", [
        L("A", "Solve a linear equation in z.", "Divide by multiplying top and bottom by the conjugate.", ["CX2.1"], [
            Q("em-complex-linear", "cplx.functions", "Solve $({{a}} + {{b}}i)z = {{c}} + ({{d}})i$. What is $\\operatorname{Re} z$?",
              given={"a": {"int": [1, 4]}, "b": {"int": [-3, 3]}, "c": {"int": [-6, 6]}, "d": {"int": [-6, 6]}}, require=["a*c + b*d != 0"],
              value="(a*c + b*d)/(a^2 + b^2)", tex="\\operatorname{Re}z", verify="re(solve(Eq((a + b*I)*Symbol('z'), c + d*I), Symbol('z'))[0])",
              explain="$z = \\dfrac{c + di}{a + bi}\\cdot\\dfrac{a - bi}{a - bi} = \\dfrac{(ac + bd) + (ad - bc)i}{a^2 + b^2}$")]),
        L("B", "Solve a nonlinear equation in z.", "Write the right side in polar form; z² = w has two roots ±√w.", ["CX2.3"], [
            Q("em-complex-sqrt", "cplx.functions", "Solve $z^2 = {{a^2 - b^2}} + {{2*a*b}}i$. What is the real part of the root with positive real part?",
              given={"a": {"int": [1, 5]}, "b": {"int": [-4, 4]}}, require=["b != 0"], value="a", tex="\\operatorname{Re}z",
              verify="re(sqrt(a**2 - b**2 + 2*a*b*I))",
              explain="Try $z = p + qi$: $p^2 - q^2 = {{a^2 - b^2}}$ and $2pq = {{2*a*b}}$, giving $p = {{a}}$, $q = {{b}}$. The other root is its negative")]),
        L("C", "Decide whether a point lies in a region of the plane.", "|z − z₀| < r is the open disc of radius r about z₀.", ["CX3.1"], [
            Q("em-complex-region", "cplx.functions", "Is $z = {{p}} + ({{q}})i$ in the region $|z - ({{a}} + {{b}}i)| < {{r}}$?", pace="recall",
              given={"p": {"int": [-4, 4]}, "q": {"int": [-4, 4]}, "a": {"int": [-2, 2]}, "b": {"int": [-2, 2]}, "r": {"pick": [2, 3, 4]}},
              require=["(p - a)^2 + (q - b)^2 != r^2"], choice=["Yes", "No"], correct="(p - a)^2 + (q - b)^2 < r^2 ? 0 : 1",
              verify="0 if Abs((p + q*I) - (a + b*I)) < r else 1",
              explain="The distance from ${{a}} + {{b}}i$ is $\\sqrt{({{p - a}})^2 + ({{q - b}})^2}$; compare it with ${{r}}$. An open, connected region is called a domain")]),
        L("D", "Find the image of a point under a complex map.", "w = z² squares the modulus and doubles the argument.", ["CX4.1"], [
            Q("em-complex-map", "cplx.functions", "Under $w = z^2$, what is $\\operatorname{Re} w$ for $z = {{p}} + ({{q}})i$?",
              given={"p": {"int": [-4, 5]}, "q": {"int": [-4, 4]}}, require=["p^2 - q^2 != 0"], value="p^2 - q^2", tex="u",
              verify="re(expand((p + q*I)**2))",
              explain="$z^2 = (x^2 - y^2) + 2xyi$: so $u = x^2 - y^2$ and $v = 2xy$. Lines $x = c$ map to parabolas; angles at points with $z \\neq 0$ are preserved")]),
        L("E", "Evaluate a limit of a complex function.", "A complex limit must agree from every direction; algebra works as for real limits.", ["CX4.2"], [
            Q("em-complex-limit", "cplx.functions", "Find $\\operatorname{Re}\\displaystyle\\lim_{z\\to z_0} \\frac{z^2 - z_0^2}{z - z_0}$ for $z_0 = {{p}} + ({{q}})i$.",
              given={"p": {"int": [-4, 5]}, "q": {"int": [-4, 4]}}, require=["p != 0"], value="2*p", tex="\\operatorname{Re}L",
              verify="re(limit((Symbol('z')**2 - (p + q*I)**2)/(Symbol('z') - (p + q*I)), Symbol('z'), p + q*I))",
              explain="Factor: $\\frac{(z - z_0)(z + z_0)}{z - z_0} \\to 2z_0$, which is the derivative of $z^2$ at $z_0$")]),
    ]),
    ("Analytic functions", [
        L("A", "Use the Cauchy–Riemann equations.", "f = u + iv is analytic where uₓ = v_y and u_y = −vₓ.", ["CX5.1"], [
            Q("em-cauchy-riemann", "cplx.analytic", "$u = x^2 - y^2 + {{a}}x$ and $v = 2xy + by$. For which $b$ is $f = u + iv$ analytic?",
              given={"a": {"pick": [-4, -3, -2, 2, 3, 5]}}, value="a", tex="b",
              verify="solve(Eq(diff(x**2 - Symbol('y')**2 + a*x, x), diff(2*x*Symbol('y') + Symbol('B')*Symbol('y'), Symbol('y'))), Symbol('B'))[0]",
              explain="$u_x = 2x + {{a}}$ must equal $v_y = 2x + b$; the second equation $u_y = -2y = -v_x$ already holds. Then $f = z^2 + {{a}}z$")]),
        L("B", "Test whether a function is harmonic.", "u is harmonic when u_xx + u_yy = 0; real parts of analytic functions are.", ["CX5.2"], [
            Q("em-harmonic", "cplx.analytic", "For which $b$ is $u = {{a}}x^3 + b\\,xy^2$ harmonic?",
              given={"a": {"pick": [-3, -2, -1, 1, 2, 4]}}, value="-3*a", tex="b",
              verify="solve(Eq(diff(a*x**3 + Symbol('B')*x*Symbol('y')**2, x, 2) + diff(a*x**3 + Symbol('B')*x*Symbol('y')**2, Symbol('y'), 2), 0), Symbol('B'))[0]",
              explain="$u_{xx} + u_{yy} = 6ax + 2bx = 0$ needs $b = -3a$: then $u = a\\operatorname{Re}(z^3)$")]),
        L("C", "Recognise entire functions.", "Entire = analytic at every point of the plane.", ["CX5.3"], [
            Q("em-entire", "cplx.analytic", "Is ${{f}}$ entire?", pace="recall",
              cases=[{"f": "e^{z}", "ans": 0}, {"f": "\\sin z", "ans": 0}, {"f": "z^3 - 2z", "ans": 0}, {"f": "\\cosh z", "ans": 0},
                     {"f": "\\bar z", "ans": 1}, {"f": "1/z", "ans": 1}, {"f": "|z|^2", "ans": 1}, {"f": "e^{1/z}", "ans": 1}, {"f": "\\tan z", "ans": 1}],
              choice=["Yes", "No"], correct="ans", verify="authored",
              explain="Polynomials, exponentials, sine, cosine and their sums and products are entire. The conjugate and $|z|^2$ fail Cauchy–Riemann; $1/z$, $e^{1/z}$ and $\\tan z$ blow up at points")]),
        L("D", "Find a harmonic conjugate.", "Integrate v_y = uₓ in y, then fix the function of x with vₓ = −u_y.", ["CX5.4"], [
            Q("em-harmonic-conjugate", "cplx.analytic", "$u = x^2 - y^2 + {{c}}x$. Find its harmonic conjugate $v$ (with $v(0, 0) = 0$) at $(x, y) = ({{x0}}, {{y0}})$.",
              given={"c": {"int": [-4, 4]}, "x0": {"int": [-3, 3]}, "y0": {"int": [-3, 3]}}, require=["2*x0*y0 + c*y0 != 0"],
              value="2*x0*y0 + c*y0", tex="v",
              verify="integrate(diff(x**2 - Symbol('y')**2 + c*x, x), (Symbol('y'), 0, y0)).subs(x, x0)",
              explain="$v_y = u_x = 2x + {{c}}$ gives $v = 2xy + {{c}}y + g(x)$; $v_x = 2y = -u_y$ forces $g$ constant. In flow problems $u$ and $v$ are the potential and stream function")]),
    ]),
    ("Integration and series", [
        L("A", "Use Cauchy's integral formula.", "∮ f(z)/(z − z₀) dz = 2πi f(z₀) for z₀ inside the contour and f analytic.", ["CX7.1"], [
            Q("em-cauchy-formula", "cplx.series", "For the circle $|z| = {{R}}$ traversed once counterclockwise, $\\displaystyle\\oint \\frac{e^{ {{a}}z}}{z - {{p}}}\\,dz = 2\\pi i\\cdot c$. Find $c$.",
              given={"R": {"pick": [2, 3, 5]}, "a": {"pick": [-2, -1, 1, 2]}, "p": {"pick": [-1, 0.5, 1]}}, value="exp(a*p)", tex="c", tol=0.0001,
              verify="limit((x - nsimplify(p))*exp(a*x)/(x - nsimplify(p)), x, nsimplify(p))",
              explain="The pole at ${{p}}$ lies inside $|z| = {{R}}$, so the integral is $2\\pi i\\,e^{ {{a}}\\cdot{{p}} }$. A pole outside the contour would give 0 (Cauchy's theorem)")]),
        L("B", "Decide whether a complex sequence converges.", "zⁿ → 0 when |z| < 1 and diverges when |z| > 1.", ["CX8.1"], [
            Q("em-complex-sequence", "cplx.series", "Does $z_n = \\left(\\dfrac{ {{a}} + {{b}}i}{ {{c}} }\\right)^n$ converge?", pace="recall",
              cases=PYTH, given={"c": {"pick": [4, 6, 12, 26]}}, require=["r != c"], choice=["Yes, to 0", "No"], correct="r < c ? 0 : 1",
              verify="0 if Abs((a + b*I)/c) < 1 else 1",
              explain="$|z_n| = (|{{a}} + {{b}}i|/{{c}})^n = ({{r}}/{{c}})^n$. The argument just rotates; the modulus decides")]),
        L("C", "Find a Taylor coefficient of an analytic function.", "e^{az} = Σ aᵏ zᵏ / k!; 1/(1 − az) = Σ aᵏ zᵏ for |az| < 1.", ["CX8.2"], [
            Q("em-complex-taylor", "cplx.series", "Find the coefficient of $z^{ {{k}} }$ in the Maclaurin series of $e^{ {{a}}z}$.",
              given={"a": {"pick": [-2, -1, 2, 3]}, "k": {"int": [2, 5]}}, value="a^k/factorial(k)", tex="c_k",
              verify="series(exp(a*x), x, 0, k + 1).removeO().coeff(x, k)",
              explain="$e^w = \\sum w^k/k!$ with $w = {{a}}z$. Complex Taylor series converge in the largest disc that avoids every singularity")]),
        L("D", "Find a Laurent coefficient (a residue).", "The coefficient of 1/(z − z₀) is the residue.", ["CX8.3", "CX8.5"], [
            Q("em-laurent-residue", "cplx.series", "Find the coefficient of $1/z$ in the Laurent series of $\\dfrac{e^{ {{a}}z}}{z^{ {{n}} }}$ about 0.",
              given={"a": {"pick": [-2, -1, 1, 2, 3]}, "n": {"int": [1, 5]}}, value="a^(n - 1)/factorial(n - 1)", tex="b_1",
              verify="series(exp(a*x), x, 0, n + 1).removeO().coeff(x, n - 1)",
              explain="Divide the series of $e^{az}$ by $z^n$: the $z^{n-1}$ term becomes $1/z$. That coefficient is the residue, and $\\oint f\\,dz = 2\\pi i$ times it")]),
        L("E", "Find the order of a zero.", "The order is the power of the first nonzero term of the Taylor series.", ["CX8.4"], [
            Q("em-zero-order", "cplx.series", "What is the order of the zero of $f(z) = z^{ {{m}} }\\,({{g}})$ at $z = 0$?",
              given={"m": {"int": [0, 3]}},
              cases=[{"g": "\\sin z", "gp": "sin(Symbol('t'))", "o": 1}, {"g": "1 - \\cos z", "gp": "1 - cos(Symbol('t'))", "o": 2}, {"g": "e^z - 1 - z", "gp": "exp(Symbol('t')) - 1 - Symbol('t')", "o": 2},
                     {"g": "\\sin z - z", "gp": "sin(Symbol('t')) - Symbol('t')", "o": 3}, {"g": "\\tan z", "gp": "tan(Symbol('t'))", "o": 1}],
              value="m + o", tex="m", final=True,
              verify="series(Symbol('t')**m*calc(gp), Symbol('t'), 0, 12).removeO().as_ordered_terms()[-1].as_coeff_exponent(Symbol('t'))[1]",
              explain="Multiply orders: $z^{ {{m}} }$ has order ${{m}}$ and the factor's series starts at $z^{ {{o}} }$. At a zero of order $m$, $1/f$ has a pole of order $m$")]),
    ]),
]),
]
