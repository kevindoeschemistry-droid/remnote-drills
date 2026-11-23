"""Independent checks for drills/problems/re-depth.yaml (framework reaction-engineering, RE).

The generator (scripts/re_cases.py) answers with the closed forms the cards teach: Xe = K/(1 + K),
the ε-corrected PFR integral, (1 − αW)^½, (k1/k2)^(k2/(k2 − k1)), Michaelis–Menten, η = (3/φ²)(φ coth φ − 1),
Danckwerts' closed form and so on. Each function here reaches the same number another way: a mole
table instead of ε, ODE integration instead of the integrated rate law, a PSSH solve instead of the
quoted rate law, dsolve on the diffusion–reaction BVP, root counting instead of a plotted crossing.
"""
import math

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
R_ = mp.mpf("8.314462618")


def check(p, H):
    return None


def _m(v):
    return mp.mpf(str(sp.N(v, 30)))


def eq_X(kind, K, CA0=1):
    """equilibrium conversion: 0 A ⇌ B; 1 A + B ⇌ C from an equimolar feed at C_A0"""
    X = sp.Symbol("X")
    K, CA0 = sp.nsimplify(K), sp.nsimplify(CA0)
    eq = [K * (1 - X) - X, K * CA0 * (1 - X) ** 2 - X][int(kind)]
    return [r for r in sp.Poly(eq, X).nroots(n=30) if r.is_real and 0 < r < 1][0]


def gas_CA(CA0, yA0, a, dn, X, Pr, T0, T):
    """C_A from a mole table: per mole of A fed, F_T = 1/y_A0 + (Δn/a) X; C_T0 = C_A0 / y_A0"""
    CA0, yA0, a, dn, X, Pr, T0, T = map(_m, (CA0, yA0, a, dn, X, Pr, T0, T))
    FT0 = 1 / yA0
    FT = FT0 + dn / a * X
    CT = CA0 / yA0 * Pr * T0 / T
    return sp.Float(CT * (1 - X) / FT, 15)


def plot_order(ts, Cs):
    """order 0, 1 or 2 whose linearising transform (C, ln C, 1/C against t) fits best"""
    best, which = None, None
    for n, f in enumerate((lambda c: c, math.log, lambda c: 1 / c)):
        y = [f(float(c)) for c in Cs]
        x = [float(t) for t in ts]
        mx, my = sum(x) / len(x), sum(y) / len(y)
        sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
        sxx = sum((a - mx) ** 2 for a in x)
        syy = sum((b - my) ** 2 for b in y)
        r2 = sxy * sxy / (sxx * syy)
        if best is None or r2 > best:
            best, which = r2, n
    return which


def cstr_X(n, Da):
    """root in (0, 1) of Da = X / (1 − X)^n"""
    X = sp.Symbol("X")
    eq = sp.nsimplify(Da) * (1 - X) ** int(n) - X
    return [r for r in sp.Poly(eq, X).nroots(n=30) if r.is_real and 0 < r < 1][0]


def pfr_V(n, k, v0, CA0, eps, X):
    """V = ∫ F_A0 dX / (k C_A^n) with C_A = C_A0 (1 − X)/(1 + εX), by quadrature"""
    n, k, v0, CA0, eps, X = int(n), _m(k), _m(v0), _m(CA0), _m(eps), _m(X)
    FA0 = v0 * CA0
    return sp.Float(mp.quad(lambda x: FA0 / (k * (CA0 * (1 - x) / (1 + eps * x)) ** n), [0, X]), 15)


def cstr_pfr_V(k, v0, X1, X2):
    """first order, liquid: a CSTR to X1 then a PFR to X2 (algebraic balance plus quadrature)"""
    k, v0, X1, X2 = map(_m, (k, v0, X1, X2))
    x = mp.findroot(lambda V: V * k * (1 - X1) - v0 * X1, 1)
    return sp.Float(x + mp.quad(lambda z: v0 / (k * (1 - z)), [X1, X2]), 15)


def _rk4(f, u0, t1, steps=4000):
    """classical RK4 in floats; h⁴ error is far below the 1e-6 check at 4000 steps"""
    h, t, u = t1 / steps, 0.0, [float(v) for v in u0]
    for _ in range(steps):
        k1 = f(t, u)
        k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(u, k1)])
        k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(u, k2)])
        k4 = f(t + h, [a + h * b for a, b in zip(u, k3)])
        u = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(u, k1, k2, k3, k4)]
        t += h
    return u


def pbr(w, k, v0, alpha, W):
    """isothermal first-order gas PBR, ε = 0: integrate y' = −α/(2y), X' = k(1 − X)y/v0 together (RK4)"""
    k, v0, alpha, W = (float(sp.N(v)) for v in (k, v0, alpha, W))
    u = _rk4(lambda s, u: [-alpha / (2 * u[0]), k * (1 - u[1]) * u[0] / v0], [1.0, 0.0], W)
    return sp.Float(u[int(w)], 15)


def power_exponent(ratio, base):
    """real n with ratio = base^n (nsolve from 1, so a complex branch can never be picked)"""
    n = sp.Symbol("n", real=True)
    return sp.nsolve(sp.nsimplify(base) ** n - sp.nsimplify(ratio), n, 1)


def cstr_startup(tau, k, frac):
    """time for an initially A-free CSTR to reach frac of its steady exit concentration (dsolve)"""
    t = sp.Symbol("t", positive=True)
    C = sp.Function("C")
    tau, k, frac = sp.nsimplify(tau), sp.nsimplify(k), sp.nsimplify(frac)
    sol = sp.dsolve(sp.Eq(C(t).diff(t), (1 - C(t)) / tau - k * C(t)), C(t), ics={C(0): 0}).rhs
    Cs = sp.limit(sol, t, sp.oo)
    return sp.N(sp.solve(sp.Eq(sol, frac * Cs), t)[0], 15)


def series_cb_max(k1, k2):
    """A → B → C in a batch: integrate, then bisect dB/dt = k1 A − k2 B = 0"""
    k1, k2 = _m(k1), _m(k2)
    f = mp.odefun(lambda t, u: [-k1 * u[0], k1 * u[0] - k2 * u[1]], 0, [mp.mpf(1), mp.mpf(0)])
    g = lambda t: (lambda u: k1 * u[0] - k2 * u[1])(f(t))  # noqa: E731
    lo, hi = mp.mpf("1e-9"), mp.mpf(1)
    while g(hi) > 0:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
    return sp.Float(f((lo + hi) / 2)[1], 12)


def cstr_series(w, k1, k2):
    """A → B → C in one CSTR: solve the two balances, then the stationary point in τ"""
    tau, CA, CB = sp.symbols("tau CA CB", positive=True)
    k1, k2 = sp.nsimplify(k1), sp.nsimplify(k2)
    s = sp.solve([1 - CA - tau * k1 * CA, -CB + tau * (k1 * CA - k2 * CB)], [CA, CB], dict=True)[0]
    cb = s[CB]
    t_opt = sp.nsolve(sp.diff(cb, tau), tau, float(sp.N(1 / sp.sqrt(k1 * k2))) * 1.5)
    return sp.N([t_opt, cb.subs(tau, t_opt)][int(w)], 15)


def parallel_overall(kind, k1, a1, k2, a2, CA0, X):
    """moles of D per volume when A → D (k1 C^a1) and A → U (k2 C^a2) reach conversion X.
    0: one CSTR (solve the balances); 1: PFR (integrate in time, stop at the exit C_A)"""
    k1, a1, k2, a2, CA0, X = map(_m, (k1, a1, k2, a2, CA0, X))
    CA = CA0 * (1 - X)
    if int(kind) == 0:
        tau = mp.findroot(lambda t: CA0 - CA - t * (k1 * CA**a1 + k2 * CA**a2), 1)
        return sp.Float(tau * k1 * CA**a1, 15)
    f = mp.odefun(lambda t, u: [-(k1 * u[0] ** a1 + k2 * u[0] ** a2), k1 * u[0] ** a1], 0, [CA0, mp.mpf(0)])
    lo, hi = mp.mpf(0), mp.mpf(1)
    while f(hi)[0] > CA:
        hi *= 2
    for _ in range(70):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid)[0] > CA else (lo, mid)
    return sp.Float(f((lo + hi) / 2)[1], 12)


def lh_rate(kind, k, KA, PA, KB, PB):
    """Langmuir–Hinshelwood: vacant fraction from the site balance; 0 single site k θ_A, 1 dual site k θ_A θ_v"""
    tv = sp.Symbol("tv", positive=True)
    k, KA, PA, KB, PB = map(sp.nsimplify, (k, KA, PA, KB, PB))
    v = sp.solve(tv + KA * PA * tv + KB * PB * tv - 1, tv)[0]
    return sp.N(k * KA * PA * v * (v if int(kind) else 1), 15)


def lind_rate(k1, k2, k3, C):
    """A + A → A* + A (k1), A* + A → 2A (k2), A* → P (k3): PSSH on A*, rate = k3 [A*]"""
    s = sp.Symbol("s", positive=True)
    k1, k2, k3, C = map(sp.nsimplify, (k1, k2, k3, C))
    a = sp.solve(k1 * C**2 - k2 * C * s - k3 * s, s)[0]
    return sp.N(k3 * a, 15)


def lind_order(k1, k2, k3, C):
    """apparent order d ln r / d ln C, rounded to 0, 1 or 2"""
    c = sp.Symbol("c", positive=True)
    r = sp.nsimplify(k1) * sp.nsimplify(k3) * c**2 / (sp.nsimplify(k2) * c + sp.nsimplify(k3))
    n = sp.N((sp.diff(sp.log(r), c) * c).subs(c, sp.nsimplify(C)))
    return int(round(float(n)))


def mm_pssh(k1, km1, k2, Et, S):
    """E + S ⇌ ES → E + P: PSSH on ES with an enzyme balance; rate = k2 [ES]"""
    E, ES = sp.symbols("E ES", positive=True)
    k1, km1, k2, Et, S = map(sp.nsimplify, (k1, km1, k2, Et, S))
    s = sp.solve([k1 * E * S - (km1 + k2) * ES, E + ES - Et], [E, ES], dict=True)[0]
    return sp.N(k2 * s[ES], 15)


def mm_fit(w, S1, v1, S2, v2):
    """V_max (w = 0) or K_m (w = 1) from two (S, v) points, solving the rate law directly"""
    S1, v1, S2, v2 = map(sp.nsimplify, (S1, v1, S2, v2))
    # V_max S − v K_m = v S at both points: a 2 × 2 linear system
    sol = sp.Matrix([[S1, -v1], [S2, -v2]]).LUsolve(sp.Matrix([v1 * S1, v2 * S2]))
    return sp.N(sol[int(w)], 15)


def chemostat(w, mumax, Ks, S0, D, Y):
    """steady chemostat with Monod growth: 0 washout dilution rate, 1 substrate S, 2 cell mass X"""
    S, Dd = sp.symbols("S Dd", positive=True)
    mumax, Ks, S0, D, Y = map(sp.nsimplify, (mumax, Ks, S0, D, Y))
    mu = mumax * S / (Ks + S)
    if int(w) == 0:  # growth just balances washout when the tank holds feed-strength substrate
        return sp.N(sp.solve(sp.Eq(Dd, mu.subs(S, S0)), Dd)[0], 15)
    s = sp.solve(sp.Eq(mu, D), S)[0]
    return sp.N([None, s, Y * (S0 - s)][int(w)], 15)


def adiabatic_T(T0, dH, cp, X):
    """steady-flow energy balance with ΔC_p = 0: Σθ C_p (T − T0) + ΔH X = 0"""
    T = sp.Symbol("T")
    return sp.N(sp.solve(sp.nsimplify(cp) * (T - sp.nsimplify(T0)) + sp.nsimplify(dH) * sp.nsimplify(X), T)[0], 15)


def adiabatic_xe(K1, T1, dH, cp, T0):
    """A ⇌ B adiabatic: substitute the energy balance into X_e = K/(1 + K) and solve for X"""
    K1, T1, dH, cp, T0 = map(_m, (K1, T1, dH, cp, T0))
    K = lambda T: K1 * mp.exp(-dH / R_ * (1 / T - 1 / T1))  # noqa: E731
    g = lambda X: X - K(T0 - dH * X / cp) / (1 + K(T0 - dH * X / cp))  # noqa: E731
    return sp.Float(mp.findroot(g, (mp.mpf("1e-6"), mp.mpf("0.999999")), solver="anderson"), 15)


def _cstr_roots(tau, k1, T1, E, dH, cp, T0):
    tau, k1, T1, E, dH, cp, T0 = map(_m, (tau, k1, T1, E, dH, cp, T0))
    k = lambda T: k1 * mp.exp(-E / R_ * (1 / T - 1 / T1))  # noqa: E731
    g = lambda T: tau * k(T) / (1 + tau * k(T)) - cp * (T - T0) / (-dH)  # noqa: E731
    top = T0 + (-dH) / cp
    roots = []
    for i in range(1, 400):
        try:
            r = mp.findroot(g, T0 + (top - T0) * i / 400)
        except (ValueError, ZeroDivisionError):
            continue
        if T0 <= r <= top + 1 and abs(g(r)) < mp.mpf("1e-15") and all(abs(r - q) > mp.mpf("1e-6") for q in roots):
            roots.append(r)
    return sorted(roots)


def cstr_adiabatic(w, tau, k1, T1, E, dH, cp, T0):
    """first-order adiabatic CSTR: 0 → number of steady states coded 0 (one) / 1 (three); 1 → T of the single state"""
    roots = _cstr_roots(tau, k1, T1, E, dH, cp, T0)
    if int(w) == 0:
        return {1: 0, 3: 1}[len(roots)]
    assert len(roots) == 1
    return sp.Float(roots[0], 15)


def ext_mt(kc, kr, Cb):
    """first-order surface reaction behind a film: k_c (C_b − C_s) = k_r C_s"""
    Cs = sp.Symbol("Cs", positive=True)
    kc, kr, Cb = map(sp.nsimplify, (kc, kr, Cb))
    return sp.N(kr * sp.solve(kc * (Cb - Cs) - kr * Cs, Cs)[0], 15)


def mt_bed(kc, a, L, U):
    """mass-transfer-limited bed: dC/dz = −k_c a C / U, solved by dsolve"""
    z = sp.Symbol("z")
    C = sp.Function("C")
    kc, a, L, U = map(sp.nsimplify, (kc, a, L, U))
    sol = sp.dsolve(sp.Eq(C(z).diff(z), -kc * a * C(z) / U), C(z), ics={C(0): 1}).rhs
    return sp.N(1 - sol.subs(z, L), 15)


def eta(geom, phi):
    """internal effectiveness from the diffusion–reaction BVP (dsolve).
    geom 0: slab, ψ'' = φ²ψ, ψ'(0) = 0, ψ(1) = 1, η = ψ'(1)/φ².
    geom 1: sphere, ψ = u/λ with u'' = φ²u, u(0) = 0, u(1) = 1, η = 3ψ'(1)/φ²."""
    lam = sp.Symbol("lam", positive=True)
    u = sp.Function("u")
    p = sp.nsimplify(phi)
    if int(geom) == 0:
        s = sp.dsolve(u(lam).diff(lam, 2) - p**2 * u(lam), u(lam), ics={u(lam).diff(lam).subs(lam, 0): 0, u(1): 1}).rhs
        return sp.N(sp.diff(s, lam).subs(lam, 1) / p**2, 15)
    s = sp.dsolve(u(lam).diff(lam, 2) - p**2 * u(lam), u(lam), ics={u(0): 0, u(1): 1}).rhs
    psi = s / lam
    return sp.N(3 * sp.diff(psi, lam).subs(lam, 1) / p**2, 15)


def cwp(R, k, De):
    """Weisz–Prater group for a first-order sphere: observed rate η k C_s, so C_WP = η k R²/D_e"""
    R, k, De = map(sp.nsimplify, (R, k, De))
    return sp.N(eta(1, R * sp.sqrt(k / De)) * k * R**2 / De, 15)


def overall_rate(kc, a, et, k, Cb):
    """film in series with an internally limited first-order pellet: k_c a (C_b − C_s) = η k C_s"""
    Cs = sp.Symbol("Cs", positive=True)
    kc, a, et, k, Cb = map(sp.nsimplify, (kc, a, et, k, Cb))
    return sp.N(et * k * sp.solve(kc * a * (Cb - Cs) - et * k * Cs, Cs)[0], 15)


def rtd_moments(w, ts, Cs):
    """t_m (w = 0) or σ² (w = 1) from pulse data by the trapezoid rule"""
    t = [sp.nsimplify(x) for x in ts]
    c = [sp.nsimplify(x) for x in Cs]

    def trap(f):
        return sum((t[i + 1] - t[i]) * (f(i) + f(i + 1)) / 2 for i in range(len(t) - 1))
    area = trap(lambda i: c[i])
    tm = trap(lambda i: t[i] * c[i]) / area
    var = trap(lambda i: (t[i] - tm) ** 2 * c[i]) / area
    return sp.N([tm, var][int(w)], 15)


def tanks_F(n, tau, tt, w):
    """fraction of fluid with residence time below (w = 0) or above (w = 1) tt, n equal tanks, total τ"""
    s = sp.Symbol("s", positive=True)
    n, tau, tt = int(n), sp.nsimplify(tau), sp.nsimplify(tt)
    E = n**n * s ** (n - 1) / (sp.factorial(n - 1) * tau**n) * sp.exp(-n * s / tau)
    Fv = sp.integrate(E, (s, 0, tt))
    return sp.N([Fv, 1 - Fv][int(w)], 15)


def seg_X(kind, Da, n=1):
    """segregation model. kind 0: first order, RTD of n equal tanks (symbolic integral);
    kind 1: second order (Da = k C_A0 τ), CSTR RTD, integrated over u = e^(−t/τ)"""
    if int(kind) == 0:
        s = sp.Symbol("s", positive=True)
        n = int(n)
        Da = sp.nsimplify(Da)
        E = n**n * s ** (n - 1) / sp.factorial(n - 1) * sp.exp(-n * s)  # θ = t/τ
        return sp.N(sp.integrate((1 - sp.exp(-Da * s)) * E, (s, 0, sp.oo)), 15)
    Da = _m(Da)
    return sp.Float(mp.quad(lambda u: (Da * -mp.log(u)) / (1 + Da * -mp.log(u)), [0, 1]), 15)


def tis_X(n, Da):
    """first order through n equal tanks, solved one tank at a time; Da = k τ_total"""
    C = sp.Integer(1)
    for _ in range(int(n)):
        C = C / (1 + sp.nsimplify(Da) / int(n))
    return sp.N(1 - C, 15)


def disp_X(Pe, Da):
    """closed–closed dispersion, first order: ψ''/Pe − ψ' − Da ψ = 0, ψ(0) − ψ'(0)/Pe = 1, ψ'(1) = 0"""
    r = sp.Symbol("r")
    z = sp.Symbol("z")
    A, B = sp.symbols("A B")
    Pe, Da = sp.nsimplify(Pe), sp.nsimplify(Da)
    r1, r2 = sp.solve(r**2 / Pe - r - Da, r)
    psi = A * sp.exp(r1 * z) + B * sp.exp(r2 * z)
    s = sp.solve([psi.subs(z, 0) - sp.diff(psi, z).subs(z, 0) / Pe - 1, sp.diff(psi, z).subs(z, 1)], [A, B], dict=True)[0]
    return sp.N(1 - psi.subs(s).subs(z, 1), 15)


FUNCS = {f.__name__: f for f in [eq_X, gas_CA, plot_order, cstr_X, pfr_V, cstr_pfr_V, pbr, cstr_startup, series_cb_max,
                                 cstr_series, parallel_overall, power_exponent, lh_rate, lind_rate, lind_order, mm_pssh, mm_fit, chemostat,
                                 adiabatic_T, adiabatic_xe, cstr_adiabatic, ext_mt, mt_bed, eta, cwp, overall_rate,
                                 rtd_moments, tanks_F, seg_X, tis_X, disp_X]}
