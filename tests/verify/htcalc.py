"""Heat and mass transfer checks for ht-final.yaml, each by a different route from the card:

fins          solve θ'' = m²θ with sympy's dsolve and the tip condition, then q = −kAc θ'(0)
one-term      eigenvalue by bisection on the transcendental equation, the solution from its own
              series terms (J0, J1 from mpmath), not the tabulated C1
semi-infinite constant flux and surface convection by the error-function solutions written out
lumped (rad)  time by integrating dt = −ρVc dT / (εσA(T⁴ − Tsur⁴)) numerically, not the closed form
surface       steady surface temperature from the energy balance with nsolve
FD nodes      energy balance on the node's own control volume (half and quarter cells), solved
mass          erf profile solved for the unknown with nsolve
"""
import mpmath as mp
import sympy as sp

SIGMA = sp.Rational("5.670374419e-8")


def check(p, H):
    """helpers only: data.py calls these through verify expressions"""
    return None


def N(v):
    return sp.nsimplify(v)


def fin_q(kind, h, k, D, L, Tb, Tinf, TL=0, what=0):
    """pin fin, diameter D. kind 0 convective tip, 1 prescribed tip temperature. what 0 heat rate (W),
    1 tip temperature, 2 effectiveness"""
    h, k, D, L, Tb, Tinf, TL = map(N, (h, k, D, L, Tb, Tinf, TL))
    xs = sp.Symbol("xs")
    th = sp.Function("th")
    P, Ac = sp.pi * D, sp.pi * D**2 / 4
    m2 = h * P / (k * Ac)
    sol = sp.dsolve(th(xs).diff(xs, 2) - m2 * th(xs), th(xs)).rhs
    C1, C2 = sorted(sol.free_symbols - {xs}, key=str)
    if kind == 0:
        bcs = [sp.Eq(sol.subs(xs, 0), Tb - Tinf), sp.Eq(-k * sol.diff(xs).subs(xs, L), h * sol.subs(xs, L))]
    else:
        bcs = [sp.Eq(sol.subs(xs, 0), Tb - Tinf), sp.Eq(sol.subs(xs, L), TL - Tinf)]
    cs = sp.solve(bcs, [C1, C2])
    prof = sol.subs(cs)
    q = -k * Ac * prof.diff(xs).subs(xs, 0)
    if what == 0:
        return sp.N(q, 15)
    if what == 1:
        return sp.N(prof.subs(xs, L) + Tinf, 15)
    return sp.N(q / (h * Ac * (Tb - Tinf)), 15)


def _bisect(f, a, b, n=200):
    fa = f(a)
    for _ in range(n):
        c = (a + b) / 2
        fc = f(c)
        if (fa < 0) == (fc < 0):
            a, fa = c, fc
        else:
            b = c
    return (a + b) / 2


def zeta1(geom, Bi):
    """first eigenvalue: geom 0 wall (ζ tan ζ = Bi), 1 cylinder (ζ J1/J0 = Bi), 2 sphere (1 − ζ cot ζ = Bi)"""
    mp.mp.dps = 30
    Bi = mp.mpf(str(Bi))
    if geom == 0:
        return _bisect(lambda z: z * mp.tan(z) - Bi, mp.mpf("1e-12"), mp.pi / 2 - mp.mpf("1e-12"))
    if geom == 1:
        return _bisect(lambda z: z * mp.besselj(1, z) - Bi * mp.besselj(0, z), mp.mpf("1e-12"), mp.mpf("2.4048255576957727"))
    return _bisect(lambda z: 1 - z * mp.cot(z) - Bi, mp.mpf("1e-12"), mp.pi - mp.mpf("1e-12"))


def one_term(geom, Bi, Fo, rstar, what):
    """what 0: θ* at r* (centre when r* = 0), 1: Q/Q0. Coefficient C1 from the orthogonality integral"""
    mp.mp.dps = 30
    z = zeta1(geom, Bi)
    if geom == 0:
        phi = lambda r: mp.cos(z * r)  # noqa: E731
        w = lambda r: 1  # noqa: E731
    elif geom == 1:
        phi = lambda r: mp.besselj(0, z * r)  # noqa: E731
        w = lambda r: r  # noqa: E731
    else:
        phi = lambda r: mp.sinc(z * r) if r != 0 else mp.mpf(1)  # noqa: E731
        w = lambda r: r**2  # noqa: E731
    C1 = mp.quad(lambda r: w(r) * phi(r), [0, 1]) / mp.quad(lambda r: w(r) * phi(r) ** 2, [0, 1])
    th0 = C1 * mp.exp(-z**2 * mp.mpf(str(Fo)))
    if what == 0:
        return sp.Float(th0 * phi(mp.mpf(str(rstar))), 15)
    dim = [1, 2, 3][geom]
    mean = dim * mp.quad(lambda r: w(r) * phi(r), [0, 1])  # volume average of the shape, weight r^(dim-1)
    return sp.Float(1 - th0 * mean, 15)


def semi_flux_T(q0, k, alpha, t, x, Ti):
    q0, k, alpha, t, x, Ti = map(N, (q0, k, alpha, t, x, Ti))
    s = sp.sqrt(alpha * t)
    return sp.N(Ti + 2 * q0 * s / (k * sp.sqrt(sp.pi)) * sp.exp(-x**2 / (4 * alpha * t)) - q0 * x / k * sp.erfc(x / (2 * s)), 15)


def semi_conv_T(h, k, alpha, t, x, Ti, Tinf):
    h, k, alpha, t, x, Ti, Tinf = map(N, (h, k, alpha, t, x, Ti, Tinf))
    s = sp.sqrt(alpha * t)
    eta = x / (2 * s)
    frac = sp.erfc(eta) - sp.exp(h * x / k + h**2 * alpha * t / k**2) * sp.erfc(eta + h * s / k)
    return sp.N(Ti + (Tinf - Ti) * frac, 15)


def lumped_rad_time(rho, c, V_over_A, eps, Ti, T, Tsur):
    """seconds to cool from Ti to T by radiation alone, integrating dT/dt numerically"""
    mp.mp.dps = 25
    rho, c, VA, eps, Ti, T, Tsur = (mp.mpf(str(v)) for v in (rho, c, V_over_A, eps, Ti, T, Tsur))
    sig = mp.mpf("5.670374419e-8")
    return sp.Float(mp.quad(lambda TT: -rho * c * VA / (eps * sig * (TT**4 - Tsur**4)), [Ti, T]), 15)


def surface_T(qin, h, Tinf, eps, Tsur, guess=350):
    """steady T with qin (W/m²) in = h(T − T∞) + εσ(T⁴ − Tsur⁴) out"""
    Tt = sp.Symbol("Tt", positive=True)
    qin, h, Tinf, eps, Tsur = map(N, (qin, h, Tinf, eps, Tsur))
    return sp.nsolve(qin - h * (Tt - Tinf) - eps * SIGMA * (Tt**4 - Tsur**4), Tt, guess, prec=20)


def fd_node(kind, a, b, c, d, Bi, Tinf):
    """steady 2-D node, square grid, Bi = hΔx/k, by its own control-volume balance (per unit depth, k = 1).
    kind 0: plane surface with convection (a = the node inside, b and c along the surface)
    kind 1: external corner with convection (a, b the two neighbours)
    kind 2: internal corner with convection (a, b full-face neighbours; c, d half-face neighbours)
    kind 3: insulated plane surface (a inside, b and c along the surface)"""
    T = sp.Symbol("Tn")
    a, b, c, d, Bi, Tinf = map(N, (a, b, c, d, Bi, Tinf))
    if kind == 0:
        bal = (a - T) + (b - T) / 2 + (c - T) / 2 + Bi * (Tinf - T)
    elif kind == 1:
        bal = (a - T) / 2 + (b - T) / 2 + Bi * (Tinf - T)
    elif kind == 2:
        bal = (a - T) + (b - T) + (c - T) / 2 + (d - T) / 2 + Bi * (Tinf - T)
    else:
        bal = (a - T) + (b - T) / 2 + (c - T) / 2
    return sp.solve(bal, T)[0]


def mass_erf_time(Cs, Ci, C, x, D):
    """time for C(x) to reach C when the surface is held at Cs: (C − Cs)/(Ci − Cs) = erf(x / 2√(Dt))"""
    t = sp.Symbol("tt", positive=True)
    Cs, Ci, C, x, D = map(N, (Cs, Ci, C, x, D))
    guess = (x / 2) ** 2 / D
    return sp.nsolve(sp.erf(x / (2 * sp.sqrt(D * t))) - (C - Cs) / (Ci - Cs), t, guess, prec=20)


def plate_local(kind, u, nu, k, Pr, x, xi, q, Tinf):
    """laminar local flat-plate results (Incropera 7.2.4, 7.2.5), written from the definitions of Re and Nu"""
    u, nu, k, Pr, x, xi, q, Tinf = map(N, (u, nu, k, Pr, x, xi, q, Tinf))
    Rex = u * x / nu
    if kind == 0:
        h = k / x * sp.Rational(332, 1000) * sp.sqrt(Rex) * Pr ** sp.Rational(1, 3) * (1 - (xi / x) ** sp.Rational(3, 4)) ** sp.Rational(-1, 3)
        return sp.N(h, 15)
    h = k / x * sp.Rational(453, 1000) * sp.sqrt(Rex) * Pr ** sp.Rational(1, 3)
    return sp.N(Tinf + q / h, 15)


FUNCS = {f.__name__: f for f in [plate_local, fin_q, zeta1, one_term, semi_flux_T, semi_conv_T, lumped_rad_time, surface_T, fd_node, mass_erf_time]}
