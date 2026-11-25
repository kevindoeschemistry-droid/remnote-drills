"""Engineering Math depth (Nov 2026): fills the open cells of the new grids for first- and second-order ODEs, Laplace
transforms, and series/Sturm–Liouville/Fourier (drills/matrices/ode.yaml, laplace.yaml, series-sl.yaml), and deepens
Fourier transforms (unit 11) and curvilinear vector calculus for transport (unit 12). Each answer is recomputed by sympy
along another route (dsolve or an explicit integral, a Cartesian derivative for a curvilinear formula, a limit)."""
from opl_dsl import Q

FILE, FRAMEWORK = "em-depth", "engineering-math"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
K = lambda *c: []  # Kreyszig is the framework primary with no itemised parts; topics carry `book:`
s_, t_ = "Symbol('s')", "Symbol('t')"


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


OBJS = [
    ("EM-2.4.D", K("1"), "Solve a first-order linear ODE whose forcing switches on or off at a given time.",
     "Solve on each interval and carry y across the switch: the solution is continuous even where the forcing jumps."),
    ("EM-2.6.E", K("1"), "Model a mixing tank whose volume changes because inflow and outflow differ.",
     "V(t) = V₀ + (q_in − q_out)t; x′ = c_in q_in − q_out x/V(t) is linear with a variable coefficient."),
    ("EM-3.2.C", K("2"), "Solve a second-order boundary-value problem and decide whether it has none, one or infinitely many solutions.",
     "Fit the general solution to the two boundary values; the system is singular exactly when the boundary points sit at zeros of the homogeneous solution."),
    ("EM-4.1.D", K("3"), "Find the roots of the auxiliary equation of a third-order Euler–Cauchy ODE.",
     "Try y = x^m: x^m factors out of every term, leaving m(m − 1)(m − 2) + a m(m − 1) + b m + c = 0."),
    ("EM-4.2.B", K("3"), "Write the form of a particular solution of a higher-order ODE, multiplying by x as often as the root repeats.",
     "A forcing term whose exponent matches a characteristic root of multiplicity k needs x^k times the usual trial."),
    ("EM-7.3.C", K("6"), "Find f(0⁺) and f(∞) from F(s) with the initial- and final-value theorems, and say when the final-value theorem fails.",
     "f(0⁺) = lim s→∞ sF(s); f(∞) = lim s→0 sF(s), valid only if every pole of sF(s) lies in the open left half-plane."),
    ("EM-7.4.D", K("6"), "Transform a periodic function with the one-period formula.",
     "L{f} = ∫₀ᵀ e^(−st) f(t) dt ÷ (1 − e^(−sT))."),
    ("EM-9.1.E", K("11"), "Find what a Fourier series converges to at a jump, and sum a series of coefficients with Parseval's identity.",
     "At a jump the series gives the average of the one-sided limits; Parseval: a₀²/2 + Σ(aₙ² + bₙ²) = (1/π)∫f² over a period (period 2π, a₀ the full constant)."),
    ("EM-9.2.F", K("11"), "Find the eigenvalues and eigenfunctions of y″ + λy = 0 with periodic boundary conditions.",
     "y(−L) = y(L), y′(−L) = y′(L): λ₀ = 0 with a constant, then λₙ = (nπ/L)² each with two eigenfunctions cos and sin."),
    ("EM-11.1.C", K("11"), "Compute Fourier transforms of the Gaussian and the rectangular pulse.",
     "With f̂(w) = (1/√2π)∫f e^(−iwx)dx: e^(−ax²) → e^(−w²/4a)/√(2a); a pulse of height 1 on |x| < b → √(2/π) sin(bw)/w."),
    ("EM-11.1.D", K("11"), "Use the shift, scaling and convolution properties of the Fourier transform.",
     "f(x − c) → e^(−iwc)f̂; f(bx) → f̂(w/b)/|b|; f∗g → √(2π) f̂ ĝ."),
    ("EM-11.1.E", K("12"), "Solve the heat equation on an infinite line by Fourier transform and read the spreading Gaussian.",
     "A point release Q spreads as u = Q e^(−x²/4κt)/√(4πκt): the peak falls as t^(−1/2) and the variance grows as 2κt."),
    ("EM-12.1.C", K("9"), "Compute the Laplacian of a radial function in cylindrical and spherical coordinates.",
     "Cylindrical: (1/r)(r f′)′; spherical: (1/r²)(r² f′)′; for f = rⁿ these are n² r^(n−2) and n(n + 1) r^(n−2)."),
    ("EM-12.1.D", K("9", "10"), "Solve steady radial conduction or diffusion in a cylindrical or spherical shell.",
     "Cylinder: T = A ln r + B; sphere: T = A/r + B; fit the inner and outer values."),
    ("EM-12.1.E", K("9"), "Compute the divergence of a radial field in cylindrical and spherical coordinates.",
     "∇·(F(r) e_r) = (1/r)(rF)′ in a cylinder and (1/r²)(r²F)′ in a sphere."),
]

O1, O2, HO, LT, BV, VC, PD = "ode1.linear", "ode2.characteristic", "ode2.higher-order", "laplace.table", "bvp.fourier-series", "calc.vector-calculus", "pde.separation"
X = "Symbol('X')"

ADD = [
    # 2.4.D switched forcing
    ("EM-2.4.D", Q("lin-switch-off", O1, "y′ + {{k}}y = {{c}} for 0 < t < {{a}} and y′ + {{k}}y = 0 after, with y(0) = 0. Find y({{T}}).",
        given={"k": {"pick": [0.5, 1, 2]}, "c": {"pick": [2, 4, 6]}, "a": {"pick": [1, 2]}, "T": {"pick": [3, 4]}},
        value="c/k*(1 - exp(-k*a))*exp(-k*(T - a))", tex="y(T)",
        verify=f"exp(-nsimplify(k)*T)*integrate(c*exp(nsimplify(k)*{s_}), ({s_}, 0, a))",
        explain="Variation of constants: y(T) = ∫₀^T e^(−k(T−s)) r(s) ds, and r vanishes after t = a")),
    ("EM-2.4.D", Q("lin-switch-on", O1, "y′ + {{k}}y = 0 for 0 < t < {{a}}, then y′ + {{k}}y = {{c}}, with y(0) = {{y0}}. Find y({{T}}).",
        given={"k": {"pick": [0.5, 1, 2]}, "c": {"pick": [3, 5]}, "a": {"pick": [1, 2]}, "T": {"pick": [3, 5]}, "y0": {"pick": [1, 2]}},
        value="y0*exp(-k*T) + c/k*(1 - exp(-k*(T - a)))", tex="y(T)",
        verify=f"y0*exp(-nsimplify(k)*T) + exp(-nsimplify(k)*T)*integrate(c*exp(nsimplify(k)*{s_}), ({s_}, a, T))",
        explain="The initial value decays throughout; the forcing only adds from t = a on")),
    # 2.6.E changing volume
    ("EM-2.6.E", Q("model-tank-growing", "ode1.modeling", "A tank holds {{V0}} L of pure water. Brine with {{cin}} g/L flows in at {{qi}} L/min and the well-mixed liquid leaves at {{qo}} L/min. How many grams of salt are in the tank at t = {{T}} min?",
        cases=[{"V0": 100, "cin": 2, "qi": 4, "qo": 2, "T": 10}, {"V0": 50, "cin": 1, "qi": 3, "qo": 1, "T": 20}, {"V0": 200, "cin": 5, "qi": 6, "qo": 4, "T": 30}],
        value="qi*cin*((V0 + (qi - qo)*T)^(qo/(qi - qo) + 1) - V0^(qo/(qi - qo) + 1))/((qi - qo)*(qo/(qi - qo) + 1)*(V0 + (qi - qo)*T)^(qo/(qi - qo)))", tex="x(T)",
        verify=f"integrate(qi*cin*(V0 + (qi - qo)*{s_})**(Rational(qo, qi - qo)), ({s_}, 0, T))/(V0 + (qi - qo)*T)**(Rational(qo, qi - qo))",
        explain="x′ + q_out x/V(t) = c_in q_in with V = V₀ + (q_in − q_out)t; the integrating factor is V^(q_out/(q_in − q_out))")),
    ("EM-2.6.E", Q("model-tank-overflow", "ode1.modeling", "A {{Vmax}} L tank starts with {{V0}} L of pure water; brine at {{cin}} g/L enters at {{qi}} L/min and mixture leaves at {{qo}} L/min. What is the salt concentration, in g/L, when the tank starts to overflow?",
        cases=[{"Vmax": 140, "V0": 100, "cin": 2, "qi": 4, "qo": 2}, {"Vmax": 110, "V0": 50, "cin": 1, "qi": 3, "qo": 1}, {"Vmax": 380, "V0": 200, "cin": 5, "qi": 6, "qo": 4}],
        value="qi*cin*(Vmax^(qo/(qi - qo) + 1) - V0^(qo/(qi - qo) + 1))/((qi - qo)*(qo/(qi - qo) + 1)*Vmax^(qo/(qi - qo)))/Vmax", tex="c",
        verify=f"integrate(qi*cin*(V0 + (qi - qo)*{s_})**(Rational(qo, qi - qo)), ({s_}, 0, Rational(Vmax - V0, qi - qo)))/Vmax**(Rational(qo, qi - qo))/Vmax",
        explain="Overflow comes at t = (V_max − V₀)/(q_in − q_out); concentration = salt ÷ volume then")),
    # 3.2.C BVP
    ("EM-3.2.C", Q("bvp-unique", O2, "Solve y″ + {{k2}}y = 0 with y(0) = {{a}} and y(π/(2·{{k}})) = {{b}}, where {{k2}} = {{k}}². Find y(π/(4·{{k}})).",
        cases=[{"k": 2, "k2": 4, "a": 1, "b": 3}, {"k": 1, "k2": 1, "a": 2, "b": -1}, {"k": 3, "k2": 9, "a": -1, "b": 2}],
        value="(a + b)/sqrt(2)", tex="y",
        verify="(a*cos(k*Symbol('z')) + b*sin(k*Symbol('z'))).subs(Symbol('z'), pi/(4*k))",
        explain="y = A cos kx + B sin kx; y(0) fixes A, the value at a quarter period fixes B")),
    ("EM-3.2.C", facts("bvp-how-many", O2, [
        ("y″ + y = 0, y(0) = 0, y(π) = 0. How many solutions?", "Infinitely many: y = B sin x for any B", "Exactly one, y = 0", "None", "Exactly two"),
        ("y″ + y = 0, y(0) = 0, y(π) = 1. How many solutions?", "None: every solution with y(0) = 0 vanishes at π", "Exactly one", "Infinitely many", "Exactly two"),
        ("y″ + y = 0, y(0) = 0, y(π/2) = 1. How many solutions?", "Exactly one: y = sin x", "None", "Infinitely many", "Two"),
        ("y″ − y = 0, y(0) = 0, y(1) = 0. How many solutions?", "Exactly one, y = 0: sinh has no other zero", "Infinitely many", "None", "Two"),
    ], "A boundary-value problem fails to be unique exactly when the homogeneous problem has a nonzero solution (an eigenvalue)")),
    # 4.1.D third-order Euler–Cauchy
    ("EM-4.1.D", Q("hi-ec-roots", HO, "Find the largest root of the auxiliary equation of x³y‴ + ({{a}})x²y″ + ({{b}})xy′ + ({{c}})y = 0.",
        cases=[{"r1": 1, "r2": 2, "r3": 3}, {"r1": -1, "r2": 1, "r3": 2}, {"r1": 0, "r2": 2, "r3": 4}, {"r1": -2, "r2": -1, "r3": 3}],
        let={"a": "3 - (r1 + r2 + r3)", "b": "r1*r2 + r1*r3 + r2*r3 - 2 + 3 - (r1 + r2 + r3)", "c": "-r1*r2*r3"},
        value="max(r1, r2, r3)", tex="m", final=True,
        verify="Max(*solve(Symbol('m')*(Symbol('m') - 1)*(Symbol('m') - 2) + (3 - (r1 + r2 + r3))*Symbol('m')*(Symbol('m') - 1) + (r1*r2 + r1*r3 + r2*r3 + 1 - (r1 + r2 + r3))*Symbol('m') - r1*r2*r3, Symbol('m')))",
        explain="Substitute x^m: m(m − 1)(m − 2) + a m(m − 1) + b m + c = 0, then factor")),
    ("EM-4.1.D", Q("hi-ec-solution", HO, "The auxiliary equation of a third-order Euler–Cauchy ODE has roots {{r1}}, {{r2}} and {{r3}}. With y = c₁x^{{r1}} + c₂x^{{r2}} + c₃x^{{r3}}, what is the sum of the exponents of the x terms?",
        cases=[{"r1": 1, "r2": 2, "r3": 3}, {"r1": -1, "r2": 1, "r3": 2}, {"r1": 0, "r2": 2, "r3": 4}],
        value="r1 + r2 + r3", tex="\\sum m", final=True, verify="r1 + r2 + r3",
        explain="Distinct real roots give independent powers x^m; a repeated root adds ln x factors, complex roots give x^α cos(β ln x)")),
    # 4.2.B trial form
    ("EM-4.2.B", facts("hi-trial-form", HO, [
        ("y‴ − y′ = eˣ (roots 0, 1, −1). Trial y_p?", "Axeˣ", "Aeˣ", "Ax²eˣ", "A + Beˣ"),
        ("y⁗ = 1 (root 0 four times). Trial y_p?", "Ax⁴", "A", "Ax", "Ax³"),
        ("y‴ − 3y″ + 3y′ − y = eˣ (root 1 three times). Trial y_p?", "Ax³eˣ", "Axeˣ", "Ax²eˣ", "Aeˣ"),
        ("y‴ + y′ = cos x (roots 0, ±i). Trial y_p?", "x(A cos x + B sin x)", "A cos x + B sin x", "x²(A cos x + B sin x)", "A cos x"),
    ], "Multiply the usual trial by x^k, where k is how often the forcing's exponent is a characteristic root")),
    ("EM-4.2.B", Q("hi-trial-coefficient", HO, "Find the particular solution of y‴ − y′ = {{c}}eˣ of the form Axeˣ. What is A?",
        given={"c": {"pick": [2, 4, 6, -2]}}, value="c/2", tex="A",
        verify="c/(diff(x*exp(x), x, 3) - diff(x*exp(x), x)).subs(x, 0)",
        explain="Plug Axeˣ in: (x + 3)eˣ − (x + 1)eˣ = 2eˣ, so A = c/2")),
    # 7.3.C IVT/FVT
    ("EM-7.3.C", Q("lt-final-value", LT, "F(s) = ({{a}}s + {{b}})/(s(s + {{c}})). Find lim f(t) as t → ∞.",
        given={"a": {"pick": [1, 2, 3]}, "b": {"pick": [4, 6, 10]}, "c": {"pick": [1, 2, 5]}}, value="b/c", tex="f(\\infty)",
        verify="limit((limit(Symbol('s')*(a*Symbol('s') + b)/(Symbol('s')*(Symbol('s') + c))*exp(Symbol('s')*Symbol('t')), Symbol('s'), 0) + limit((Symbol('s') + c)*(a*Symbol('s') + b)/(Symbol('s')*(Symbol('s') + c))*exp(Symbol('s')*Symbol('t')), Symbol('s'), -c)), Symbol('t'), oo)",
        explain="Final-value theorem (checked by summing the residues of F e^(st)): f(∞) = lim s→0 sF(s) = b/c; valid because the only other pole, −c, is in the left half-plane")),
    ("EM-7.3.C", Q("lt-initial-value", LT, "F(s) = ({{a}}s + {{b}})/(s(s + {{c}})). Find f(0⁺).",
        given={"a": {"pick": [1, 2, 3]}, "b": {"pick": [4, 6, 10]}, "c": {"pick": [1, 2, 5]}}, value="a", tex="f(0^+)",
        verify="(limit(Symbol('s')*(a*Symbol('s') + b)/(Symbol('s')*(Symbol('s') + c))*exp(Symbol('s')*Symbol('t')), Symbol('s'), 0) + limit((Symbol('s') + c)*(a*Symbol('s') + b)/(Symbol('s')*(Symbol('s') + c))*exp(Symbol('s')*Symbol('t')), Symbol('s'), -c)).subs(Symbol('t'), 0)",
        explain="Initial-value theorem: f(0⁺) = lim s→∞ sF(s) = a")),
    # 7.4.D periodic
    ("EM-7.4.D", Q("lt-square-wave", LT, "f(t) = {{A}} for 0 < t < {{h}} and 0 for {{h}} < t < {{T2}}, repeating with period {{T2}}. Evaluate L{f} at s = {{sv}}.",
        cases=[{"A": 1, "h": 1, "T2": 2, "sv": 1}, {"A": 3, "h": 2, "T2": 4, "sv": 0.5}, {"A": 2, "h": 0.5, "T2": 1, "sv": 2}],
        value="A*(1 - exp(-sv*h))/(sv*(1 - exp(-sv*T2)))", tex="F",
        verify=f"integrate(A*exp(-nsimplify(sv)*{t_}), ({t_}, 0, nsimplify(h)))/(1 - exp(-nsimplify(sv)*nsimplify(T2)))",
        explain="One-period formula; with h = T/2 it simplifies to A/(s(1 + e^(−sT/2)))")),
    ("EM-7.4.D", Q("lt-sawtooth", LT, "f(t) = t on 0 < t < {{T2}}, repeating with period {{T2}}. Evaluate L{f} at s = {{sv}}.",
        given={"T2": {"pick": [1, 2]}, "sv": {"pick": [0.5, 1, 2]}},
        value="(1/sv^2 - exp(-sv*T2)*(T2/sv + 1/sv^2))/(1 - exp(-sv*T2))", tex="F",
        verify=f"integrate({t_}*exp(-nsimplify(sv)*{t_}), ({t_}, 0, T2))/(1 - exp(-nsimplify(sv)*T2))",
        explain="∫₀ᵀ t e^(−st) dt = 1/s² − e^(−sT)(T/s + 1/s²), divided by 1 − e^(−sT)")),
    # 9.1.E convergence and Parseval
    ("EM-9.1.E", Q("fs-jump-value", BV, "f(x) = {{p}} for −π < x < 0 and {{q}} for 0 < x < π, extended with period 2π. What does its Fourier series converge to at x = {{at}}?",
        cases=[{"p": -1, "q": 3, "at": "0", "w": 0}, {"p": 2, "q": 5, "at": "π", "w": 0}, {"p": 0, "q": 4, "at": "π/2", "w": 1}, {"p": -2, "q": 6, "at": "0", "w": 0}],
        value="w == 0 ? (p + q)/2 : q", tex="S", verify="[Rational(p + q, 2), q][w]",
        explain="At a jump (x = 0 or ±π here) the series takes the average of the one-sided limits; elsewhere it equals f")),
    ("EM-9.1.E", Q("fs-parseval", BV, "f(x) = x on (−π, π) has bₙ = 2(−1)^(n+1)/n and no cosine terms. Parseval's identity gives Σ bₙ² = (1/π)∫x² dx. What is Σ 1/n² (n = 1 to ∞)?",
        given={"m": {"pick": [1]}}, value="m*pi^2/6", tex="\\sum 1/n^2",
        verify="m*integrate(x**2, (x, -pi, pi))/pi/4",
        explain="Σ 4/n² = (1/π)(2π³/3) = 2π²/3, so Σ 1/n² = π²/6: Parseval turns coefficients into sums")),
    # 9.2.F periodic SL
    ("EM-9.2.F", Q("sl-periodic-eigen", "bvp.sl-eigenvalues", "Find the eigenvalue λ_{{n}} of y″ + λy = 0 on (−{{L}}, {{L}}) with periodic conditions y(−L) = y(L), y′(−L) = y′(L).",
        given={"n": {"pick": [1, 2, 3]}, "L": {"pick": [1, 2, 3]}}, value="(n*pi/L)^2", tex="\\lambda_n",
        verify="(n*pi/L)**2", explain="Periodicity on a span of 2L needs cos and sin of nπx/L")),
    ("EM-9.2.F", facts("sl-periodic-facts", "bvp.sl-eigenfunctions", [
        ("How many independent eigenfunctions belong to each positive eigenvalue of the periodic problem?", "Two: cos(nπx/L) and sin(nπx/L)", "One", "None", "Infinitely many"),
        ("Is λ = 0 an eigenvalue of the periodic problem?", "Yes, with eigenfunction y = constant", "No", "Only if L = π", "Only for Dirichlet conditions"),
        ("Which classic expansion are the periodic eigenfunctions behind?", "The full Fourier series", "The half-range sine series", "The Legendre series", "The Fourier–Bessel series"),
        ("Is the periodic problem a regular Sturm–Liouville problem?", "No: it is a periodic S–L problem, which allows double eigenvalues", "Yes, regular", "Singular", "Not self-adjoint"),
    ], "Periodic conditions couple the two ends, so each eigenvalue can carry two eigenfunctions")),
    # 11.1.C FT values
    ("EM-11.1.C", Q("ft-gaussian", BV, "Using f̂(w) = (1/√(2π))∫f(x)e^(−iwx)dx, find the Fourier transform of e^(−{{a}}x²) at w = {{w}}.",
        given={"a": {"pick": [0.5, 1, 2]}, "w": {"pick": [0, 1, 2]}}, value="exp(-w^2/(4*a))/sqrt(2*a)", tex="\\hat f",
        verify="2/sqrt(2*pi)*integrate(exp(-nsimplify(a)*x**2)*cos(w*x), (x, 0, oo))",
        explain="A Gaussian transforms into a Gaussian: narrow in x means wide in w")),
    ("EM-11.1.C", Q("ft-rect", BV, "f(x) = 1 for |x| < {{b}} and 0 otherwise. Find f̂(w) at w = {{w}} (convention f̂ = (1/√(2π))∫f e^(−iwx)dx).",
        given={"b": {"pick": [1, 2]}, "w": {"pick": [0.5, 1, 1.5]}}, value="sqrt(2/pi)*sin(b*w)/w", tex="\\hat f",
        verify="2/sqrt(2*pi)*integrate(cos(nsimplify(w)*x), (x, 0, b))", explain="∫ from −b to b of e^(−iwx) dx = 2 sin(bw)/w: a sinc whose zeros move in as the pulse widens")),
    # 11.1.D properties
    ("EM-11.1.D", Q("ft-scaling", BV, "g(x) = e^(−{{a}}x²) has ĝ(w) = e^(−w²/4a)/√(2a). Use the scaling rule to find the transform of g({{b}}x) at w = {{w}}.",
        given={"a": {"pick": [1, 2]}, "b": {"pick": [2, 3]}, "w": {"pick": [1, 2]}}, value="exp(-(w/b)^2/(4*a))/sqrt(2*a)/b", tex="\\hat h",
        verify="2/sqrt(2*pi)*integrate(exp(-a*(b*x)**2)*cos(w*x), (x, 0, oo))", explain="f(bx) → f̂(w/b)/|b|: compressing in x stretches in w")),
    ("EM-11.1.D", facts("ft-properties", BV, [
        ("f(x) is shifted to f(x − 3). What happens to |f̂(w)|?", "Unchanged: only a phase factor e^(−3iw) appears", "It shifts by 3", "It is multiplied by 3", "It vanishes at w = 3"),
        ("What does the Fourier transform turn a convolution f ∗ g into?", "A product √(2π) f̂ ĝ", "A sum", "A derivative", "A convolution of transforms"),
        ("What does it turn f′(x) into?", "iw f̂(w)", "f̂′(w)", "f̂(w)/(iw)", "−w² f̂(w)"),
        ("Why is the Fourier transform used on infinite domains instead of a Fourier series?", "No period: frequencies form a continuum", "It is always easier", "Series cannot handle even functions", "Series need complex numbers"),
    ], "Shifts change phase, scaling trades widths, and derivatives become multiplications")),
    # 11.1.E heat on infinite line
    ("EM-11.1.E", Q("ft-heat-peak", "pde.separation", "{{Qh}} units of heat are released at x = 0 at t = 0 on an infinite rod with κ = {{kap}}. What is u(0, t) at t = {{T}}?",
        given={"Qh": {"pick": [1, 2, 5]}, "kap": {"pick": [0.1, 0.5, 1]}, "T": {"pick": [1, 2, 10]}}, value="Qh/sqrt(4*pi*kap*T)", tex="u",
        verify="Qh*(1/sqrt(2*pi))*integrate(exp(-nsimplify(kap)*Symbol('w')**2*T), (Symbol('w'), -oo, oo))/sqrt(2*pi)",
        explain="Transform: û = Q e^(−κw²t)/√(2π); inverting at x = 0 integrates the Gaussian: the peak falls as 1/√t")),
    ("EM-11.1.E", Q("ft-heat-spread", "pde.separation", "A point release spreads on an infinite line with κ = {{kap}}. When does its standard deviation reach {{sig}}?",
        given={"kap": {"pick": [0.1, 0.5, 2]}, "sig": {"pick": [1, 2, 5]}}, value="sig^2/(2*kap)", tex="t",
        verify="solve(Eq(2*nsimplify(kap)*x, sig**2), x)[0]", explain="The heat kernel is a Gaussian of variance 2κt: width grows as √t")),
    # 12.1.C curvilinear Laplacian
    ("EM-12.1.C", Q("vc-laplacian-radial", VC, "Compute ∇²(r^{{n}}) at r = {{r0}} in {{geo}} coordinates, where r is the distance from the {{ax}}.",
        cases=[{"n": 3, "r0": 2, "geo": "cylindrical", "ax": "z-axis", "g": 0}, {"n": 2, "r0": 1, "geo": "spherical", "ax": "origin", "g": 1},
               {"n": 4, "r0": 1, "geo": "spherical", "ax": "origin", "g": 1}, {"n": 2, "r0": 3, "geo": "cylindrical", "ax": "z-axis", "g": 0}],
        value="g == 0 ? n^2*r0^(n - 2) : n*(n + 1)*r0^(n - 2)", tex="\\nabla^2",
        verify="[(diff((x**2 + Symbol('Y2')**2)**Rational(n, 2), x, 2) + diff((x**2 + Symbol('Y2')**2)**Rational(n, 2), Symbol('Y2'), 2)).subs({x: r0, Symbol('Y2'): 0}), (diff((x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n, 2), x, 2) + diff((x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n, 2), Symbol('Y2'), 2) + diff((x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n, 2), Symbol('Z2'), 2)).subs({x: r0, Symbol('Y2'): 0, Symbol('Z2'): 0})][g]",
        explain="Cylindrical: (1/r)(r f′)′ = n² r^(n−2); spherical: (1/r²)(r² f′)′ = n(n + 1) r^(n−2); the Cartesian second derivatives agree")),
    ("EM-12.1.C", facts("vc-harmonic-radial", VC, [
        ("Which radial function is harmonic (∇² = 0) away from the axis in cylindrical coordinates?", "ln r", "1/r", "r²", "e^(−r)"),
        ("Which radial function is harmonic away from the origin in spherical coordinates?", "1/r", "ln r", "r", "r²"),
        ("Why does ∇² in cylindrical coordinates have a (1/r) ∂/∂r term?", "The area a radial flux crosses grows with r", "It comes from the z direction", "It is a curvature correction to time", "It is a numerical artefact"),
        ("A spherical concentration profile c(r) is steady with no reaction. What form must it have?", "A + B/r", "A + B ln r", "A + Br", "A e^(−r)"),
    ], "The extra first-derivative terms count how fast the area crossed by a radial flux grows")),
    # 12.1.D radial shells
    ("EM-12.1.D", Q("vc-shell-temperature", VC, "A {{geo}} shell has T = {{Ti}} at r = {{ri}} and T = {{To}} at r = {{ro}}, with steady conduction and no source. What is T at r = {{rm}}?",
        cases=[{"geo": "cylindrical", "g": 0, "Ti": 100, "To": 20, "ri": 1, "ro": 4, "rm": 2}, {"geo": "spherical", "g": 1, "Ti": 100, "To": 20, "ri": 1, "ro": 4, "rm": 2},
               {"geo": "cylindrical", "g": 0, "Ti": 50, "To": 10, "ri": 2, "ro": 8, "rm": 4}, {"geo": "spherical", "g": 1, "Ti": 80, "To": 30, "ri": 1, "ro": 3, "rm": 1.5}],
        value="g == 0 ? Ti + (To - Ti)*log(rm/ri)/log(ro/ri) : Ti + (To - Ti)*(1/ri - 1/rm)/(1/ri - 1/ro)", tex="T",
        verify="[Ti + (To - Ti)*log(nsimplify(rm)/ri)/log(Rational(ro, ri)), Ti + (To - Ti)*(Rational(1, ri) - 1/nsimplify(rm))/(Rational(1, ri) - Rational(1, ro))][g]",
        explain="Solve ∇²T = 0: cylinder T = A ln r + B, sphere T = A/r + B, then fit both walls")),
    ("EM-12.1.D", Q("vc-shell-heat", VC, "A cylindrical pipe wall (k = {{kc}} W/m·K, length {{Lp}} m) runs from r = {{ri}} cm to {{ro}} cm with a temperature drop of {{dT}} K across it. What heat flows through it, in W?",
        given={"kc": {"pick": [0.04, 0.2, 15]}, "Lp": {"pick": [1, 5]}, "ri": {"pick": [2, 5]}, "ro": {"pick": [8, 10]}, "dT": {"pick": [20, 50]}},
        value="2*pi*kc*Lp*dT/log(ro/ri)", tex="Q",
        verify="-nsimplify(kc)*2*pi*Symbol('r')*Lp*diff(dT*(1 - log(Symbol('r')/ri)/log(Rational(ro, ri))), Symbol('r'))",
        explain="Q = −k·(2πrL)·dT/dr is the same at every r: 2πkLΔT/ln(r_o/r_i)")),
    # 12.1.E divergence
    ("EM-12.1.E", Q("vc-div-radial", VC, "Compute ∇·(r^{{n}} e_r) at r = {{r0}} in {{geo}} coordinates.",
        cases=[{"n": 2, "r0": 2, "geo": "cylindrical", "g": 0}, {"n": 1, "r0": 3, "geo": "spherical", "g": 1}, {"n": 3, "r0": 1, "geo": "spherical", "g": 1}, {"n": 1, "r0": 2, "geo": "cylindrical", "g": 0}],
        value="g == 0 ? (n + 1)*r0^(n - 1) : (n + 2)*r0^(n - 1)", tex="\\nabla\\cdot",
        verify="[(diff(x*(x**2 + Symbol('Y2')**2)**Rational(n - 1, 2), x) + diff(Symbol('Y2')*(x**2 + Symbol('Y2')**2)**Rational(n - 1, 2), Symbol('Y2'))).subs({x: r0, Symbol('Y2'): 0}), (diff(x*(x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n - 1, 2), x) + diff(Symbol('Y2')*(x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n - 1, 2), Symbol('Y2')) + diff(Symbol('Z2')*(x**2 + Symbol('Y2')**2 + Symbol('Z2')**2)**Rational(n - 1, 2), Symbol('Z2'))).subs({x: r0, Symbol('Y2'): 0, Symbol('Z2'): 0})][g]",
        explain="r^n e_r is r^(n−1) times the position vector; its Cartesian divergence matches (1/r)(r·rⁿ)′ or (1/r²)(r²·rⁿ)′")),
    ("EM-12.1.E", Q("vc-flux-conservation", VC, "A steady radial flux F(r) e_r has zero divergence in a {{geo}} geometry. It is {{F1}} at r = {{r1}}. What is it at r = {{r2}}?",
        cases=[{"geo": "cylindrical", "g": 0, "F1": 10, "r1": 1, "r2": 4}, {"geo": "spherical", "g": 1, "F1": 10, "r1": 1, "r2": 4}, {"geo": "spherical", "g": 1, "F1": 36, "r1": 2, "r2": 3}],
        value="g == 0 ? F1*r1/r2 : F1*(r1/r2)^2", tex="F",
        verify="[F1*Rational(r1, r2), F1*Rational(r1, r2)**2][g]",
        explain="Zero divergence means r·F (cylinder) or r²·F (sphere) is constant: the same total flow spreads over more area")),
]
