"""Engineering Math exam-length problems (Nov 2026): several chained parts on one setup, the way a CBE 200 midterm
asks them. A house set (Kevin's CBE 200 exams were not available): each part feeds the next, and each key is checked
along another route (convolution integrals for cascades and switched inputs, the complex impedance for a forced
oscillator, the matrix exponential for a system, the Taylor series of the closed form for a power series)."""
from opl_dsl import QP

FILE, FRAMEWORK = "em-chains", "engineering-math"
U = "Symbol('u')"


def P(label, ask, value, verify, explain="", tex=None, **kw):
    return dict(label=label, ask=ask, value=value, verify=verify, explain=explain, tex=tex or label, **kw)


SYS = [  # A = P diag(l1, l2) P^-1 with eigenvectors (1, v1), (1, v2), l1 > l2
    {"a11": -2, "a12": 1, "a21": 1, "a22": -2, "l1": -1, "l2": -3, "v1": 1, "v2": -1},
    {"a11": 1, "a12": 1, "a21": 2, "a22": 0, "l1": 2, "l2": -1, "v1": 1, "v2": -2},
    {"a11": -3, "a12": 1, "a21": 2, "a22": -2, "l1": -1, "l2": -4, "v1": 2, "v2": -1},
]
SYS = [dict(c, p=p, q=q, T=T) for c in SYS for p, q, T in [(1, 0, 0.5), (2, 1, 1), (1, 3, 0.5)]]
OSC = [{"m": 1, "c": 1, "k": 4, "F0": 2, "om": 1.5}, {"m": 2, "c": 1, "k": 8, "F0": 4, "om": 2},
       {"m": 1, "c": 2, "k": 10, "F0": 5, "om": 3}, {"m": 0.5, "c": 0.4, "k": 2, "F0": 1, "om": 1.8}]
M = "Matrix([[a11, a12], [a21, a22]])"

ADD = [
    ("EM-7.7.B", QP("em-chain-tank-cascade", "laplace.systems",
        "Two well-mixed tanks of {{V}} L each are in series with flow {{qf}} L/min. Both start with clean water; at t = 0 the feed to tank 1 switches to {{c0}} g/L.",
        given={"V": {"pick": [50, 100, 200]}, "qf": {"pick": [10, 20]}, "c0": {"pick": [1, 2, 5]}, "T": {"pick": [2, 5, 10]}},
        parts=[
            P("tau", "Time constant of each tank (min)", "V/qf", "V/qf", "τ = V/q: each tank is a first-order lag", tex="\\tau"),
            P("ca", "Concentration in tank 1 at t = {{T}} min (g/L)", "c0*(1 - exp(-T*qf/V))",
              f"integrate(qf/V*exp(-(T - {U})*qf/V)*c0, ({U}, 0, T))", "c₁ = c₀(1 − e^(−t/τ))", tex="c_1"),
            P("cb", "Concentration in tank 2 at t = {{T}} min (g/L)", "c0*(1 - exp(-T*qf/V)*(1 + T*qf/V))",
              f"integrate(qf/V*exp(-(T - {U})*qf/V)*c0*(1 - exp(-{U}*qf/V)), ({U}, 0, T))",
              "C₂ = C_in/(τs + 1)²: a double pole, so c₂ = c₀(1 − e^(−t/τ)(1 + t/τ)); checked as the convolution of tank 1's output with tank 2's impulse response", tex="c_2"),
            P("pole", "The (double) pole of C₂(s)/C_in(s)", "-qf/V", f"solve(V/qf*Symbol('s') + 1, Symbol('s'))[0]",
              "Each tank contributes 1/(τs + 1), a pole at −1/τ", tex="s"),
        ])),
    ("EM-3.6.A", QP("em-chain-forced-oscillator", "ode2.spring-forced",
        "A mass m = {{m}} kg on a spring k = {{k}} N/m with damping c = {{c}} kg/s is driven by F = {{F0}} cos({{om}} t) N.",
        cases=OSC,
        parts=[
            P("w0", "Undamped natural frequency (rad/s)", "sqrt(k/m)", "sqrt(nsimplify(k)/nsimplify(m))", "ω₀ = √(k/m)", tex="\\omega_0"),
            P("amp", "Steady-state amplitude (m)", "F0/sqrt((k - m*om^2)^2 + (c*om)^2)",
              "Abs(F0/(nsimplify(k) - nsimplify(m)*nsimplify(om)**2 + I*nsimplify(c)*nsimplify(om)))",
              "Try y = Re(Y e^(iωt)): Y = F₀/(k − mω² + icω); the amplitude is |Y|", tex="A"),
            P("ph", "Phase lag δ of the response behind the force (rad, 0 to π)", "atan2(c*om, k - m*om^2)",
              "arg(nsimplify(k) - nsimplify(m)*nsimplify(om)**2 + I*nsimplify(c)*nsimplify(om))",
              "tan δ = cω/(k − mω²); past ω₀ the lag passes π/2", tex="\\delta"),
            P("wr", "Driving frequency that gives the largest amplitude (rad/s)", "sqrt(k/m - c^2/(2*m^2))",
              "Max(*solve(diff((nsimplify(k) - nsimplify(m)*Symbol('w')**2)**2 + (nsimplify(c)*Symbol('w'))**2, Symbol('w')), Symbol('w')))",
              "Minimise (k − mω²)² + (cω)²: ω² = k/m − c²/(2m²), below ω₀", tex="\\omega_r"),
        ])),
    ("EM-10.2.C", QP("em-chain-heat-nonzero", "pde.nonhomogeneous",
        "A rod 0 < x < {{L}} with κ = {{kap}} has its ends held at u(0, t) = {{A}} and u({{L}}, t) = {{B}}; initially u = {{U0}} throughout.",
        given={"L": {"pick": [1, 2]}, "kap": {"pick": [0.1, 0.5]}, "A": {"pick": [0, 20, 50]}, "B": {"pick": [80, 100]},
               "U0": {"pick": [10, 30]}, "T": {"pick": [1, 2]}},
        parts=[
            P("us", "Steady-state temperature at x = L/2", "(A + B)/2", "A + (B - A)*Rational(1, 2)", "u_s = A + (B − A)x/L", tex="u_s"),
            P("b1", "First sine coefficient b₁ of v = u − u_s at t = 0", "2/pi*(2*U0 - A - B)",
              "2/L*integrate((U0 - A - (B - A)*x/L)*sin(pi*x/L), (x, 0, L))",
              "b₁ = (2/L)∫(U₀ − u_s) sin(πx/L) dx", tex="b_1"),
            P("lam", "Decay rate of that mode (1/time)", "kap*pi^2/L^2", "nsimplify(kap)*pi**2/L**2",
              "Mode n decays as e^(−κ(nπ/L)²t)", tex="\\kappa\\lambda_1"),
            P("uT", "u(L/2, {{T}}) keeping only the first term", "(A + B)/2 + 2/pi*(2*U0 - A - B)*exp(-kap*pi^2*T/L^2)",
              "(A + B)/2 + 2/L*integrate((U0 - A - (B - A)*x/L)*sin(pi*x/L), (x, 0, L))*exp(-nsimplify(kap)*pi**2*T/L**2)",
              "u = u_s + b₁ e^(−κπ²t/L²) sin(πx/L) + …; sin(π/2) = 1", tex="u"),
        ])),
    ("EM-7.4.C", QP("em-chain-laplace-pulse", "laplace.step-ivp",
        "y″ + 3y′ + 2y = h(t) with y(0) = y′(0) = 0, where h = {{H}} for 0 < t < {{a}} and h = 0 after.",
        given={"H": {"pick": [1, 2, 4]}, "a": {"pick": [1, 2]}, "T": {"pick": [3, 4]}, "s0": {"pick": [1, 2]}},
        parts=[
            P("Ys", "Y(s) at s = {{s0}}", "H*(1 - exp(-a*s0))/(s0*(s0 + 1)*(s0 + 2))",
              f"integrate(H*(exp(-{U}) - exp(-2*{U}))*integrate(exp(-s0*Symbol('t')), (Symbol('t'), {U}, {U} + a)), ({U}, 0, oo))",
              "L{h} = H(1 − e^(−as))/s, divided by s² + 3s + 2", tex="Y"),
            P("ya", "y at the end of the pulse, t = {{a}}", "H*(1/2 - exp(-a) + exp(-2*a)/2)",
              f"integrate(H*(exp(-(a - {U})) - exp(-2*(a - {U}))), ({U}, 0, a))",
              "Step response H(½ − e^(−t) + ½e^(−2t)); checked as the convolution of h with g = e^(−t) − e^(−2t)", tex="y(a)"),
            P("yT", "y at t = {{T}}", "H*(1/2 - exp(-T) + exp(-2*T)/2) - H*(1/2 - exp(-(T - a)) + exp(-2*(T - a))/2)",
              f"integrate(H*(exp(-(T - {U})) - exp(-2*(T - {U}))), ({U}, 0, a))",
              "After the pulse, y = y_step(t) − y_step(t − a): the switch-off is a second, negative step", tex="y(T)"),
        ])),
    ("EM-5.2.B", QP("em-chain-system", "odesys.eigenvalue",
        "x′ = Ax with A = [[{{a11}}, {{a12}}], [{{a21}}, {{a22}}]] and x(0) = ({{p}}, {{q}}).",
        cases=SYS,
        parts=[
            P("e1", "Larger eigenvalue", "l1", f"Max(*{M}.eigenvals().keys())", "λ² − (tr A)λ + det A = 0", tex="\\lambda_1"),
            P("e2", "Smaller eigenvalue", "l2", f"Min(*{M}.eigenvals().keys())", "The other root", tex="\\lambda_2"),
            P("x1", "x₁(t) at t = {{T}}", "(q - p*v2)/(v1 - v2)*exp(l1*T) + (p - (q - p*v2)/(v1 - v2))*exp(l2*T)",
              f"({M}*nsimplify(T)).exp().multiply(Matrix([p, q]))[0]",
              "x = c₁e^(λ₁t)v₁ + c₂e^(λ₂t)v₂ with c fitted to x(0); checked with the matrix exponential", tex="x_1"),
        ])),
    ("EM-6.2.B", QP("em-chain-power-series", "series.terms",
        "Solve y″ − xy′ − y = 0 by a power series y = Σ aₙxⁿ about x = 0 with y(0) = {{a0}}, y′(0) = 0.",
        given={"a0": {"pick": [1, 2, 3, 6]}, "x0": {"pick": [0.5, 1]}},
        parts=[
            P("c2", "a₂", "a0/2", "a0*series(exp(x**2/2), x, 0, 8).removeO().coeff(x, 2)",
              "(n + 2)(n + 1)a_(n+2) − (n + 1)aₙ = 0, so a_(n+2) = aₙ/(n + 2)", tex="a_2"),
            P("c4", "a₄", "a0/8", "a0*series(exp(x**2/2), x, 0, 8).removeO().coeff(x, 4)", "a₄ = a₂/4", tex="a_4"),
            P("c6", "a₆", "a0/48", "a0*series(exp(x**2/2), x, 0, 8).removeO().coeff(x, 6)", "a₆ = a₄/6", tex="a_6"),
            P("yx", "The series sums to a closed form. What is y({{x0}})?", "a0*exp(x0^2/2)",
              "a0*exp(nsimplify(x0)**2/2)", "a_(2k) = a₀/(2^k k!), the series of a₀e^(x²/2)", tex="y"),
        ])),
]
