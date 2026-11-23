"""PDE checks for pde-final.yaml, by routes other than the cards':

time-varying BC   the source left after the shift, from w_t − k w_xx with sympy
heat source       steady state by solving u'' = −Q/k with dsolve; mode coefficients by integration
cylinder shift    Fourier–Bessel coefficient by numerical quadrature with the weight r
sphere            coefficients of r·u from the sine-series integral
LT inversion      the series solution by separation (coefficient of the shifted problem), not residues
FD                ghost node and implicit steps by sympy linear solves on the full stencil
"""
import mpmath as mp
import sympy as sp

xx, tt = sp.symbols("xx tt", real=True)


def check(p, H):
    """helpers only: data.py calls these through verify expressions"""
    return None


def N(v):
    return sp.nsimplify(v)


def shift_source(g, L, k, x):
    """u(0,t) = 0, u(L,t) = g(t). w = x g/L, v = u − w obeys v_t = k v_xx + F(x,t); F at (x, t = 0)"""
    G = sp.sympify(g, locals={"t": tt})
    w = xx * G / N(L)
    F = -(sp.diff(w, tt) - N(k) * sp.diff(w, xx, 2))
    return sp.N(F.subs({xx: N(x), tt: 0}), 15)


def source_steady(Q, k, L, x, kind=0):
    """k u'' + Q = 0: kind 0 both ends zero, kind 1 u(0) = 0 and u'(L) = 0"""
    f = sp.Function("f")
    sol = sp.dsolve(N(k) * f(xx).diff(xx, 2) + N(Q), f(xx)).rhs
    C1, C2 = sorted(sol.free_symbols - {xx}, key=str)
    bc2 = sp.Eq(sol.subs(xx, N(L)), 0) if kind == 0 else sp.Eq(sol.diff(xx).subs(xx, N(L)), 0)
    cs = sp.solve([sp.Eq(sol.subs(xx, 0), 0), bc2], [C1, C2])
    return sp.N(sol.subs(cs).subs(xx, N(x)), 15)


def sine_coef(fexpr, L, n):
    """b_n of f on (0, L)"""
    f = sp.sympify(fexpr, locals={"x": xx})
    return sp.N(2 / N(L) * sp.integrate(f * sp.sin(n * sp.pi * xx / N(L)), (xx, 0, N(L))), 15)


def bessel_coef(U, a, n=1):
    """A_n in U = Σ A_n J0(α_n r/a) on 0 < r < a, by quadrature with weight r"""
    mp.mp.dps = 25
    al = mp.besseljzero(0, n)
    a, U = mp.mpf(str(a)), mp.mpf(str(U))
    num = mp.quad(lambda r: r * U * mp.besselj(0, al * r / a), [0, a])
    den = mp.quad(lambda r: r * mp.besselj(0, al * r / a) ** 2, [0, a])
    return sp.Float(num / den, 15)


def bessel_rate(k, a, n=1):
    mp.mp.dps = 25
    return sp.Float(mp.mpf(str(k)) * (mp.besseljzero(0, n) / mp.mpf(str(a))) ** 2, 15)


def sphere_coef(U0, a, n):
    """B_n of r·U0 = Σ B_n sin(nπr/a)"""
    r = sp.Symbol("r", positive=True)
    return sp.N(2 / N(a) * sp.integrate(r * N(U0) * sp.sin(n * sp.pi * r / N(a)), (r, 0, N(a))), 15)


def sphere_centre(U0, a, k, t, terms=60):
    """u(0, t) = Σ B_n (nπ/a) e^(−k(nπ/a)² t), the limit of sin(λr)/r at r = 0"""
    s = 0
    for n in range(1, terms + 1):
        lam = n * sp.pi / N(a)
        s += sphere_coef(U0, a, n) * lam * sp.exp(-N(k) * lam**2 * N(t))
    return sp.N(s, 15)


def ramp_series_coef(L, x, n):
    """u(0) = 0, u(L) = 1, u(x, 0) = 0: coefficient of e^{−(nπ/L)² t} at x, by separation of v = u − x/L"""
    b = 2 / N(L) * sp.integrate((0 - xx / N(L)) * sp.sin(n * sp.pi * xx / N(L)), (xx, 0, N(L)))
    return sp.N(b * sp.sin(n * sp.pi * N(x) / N(L)), 15)


def ghost_step(u0, u1, r, h, g):
    """explicit step at x = 0 with u_x(0) = g: central difference with a ghost node, solved by sympy"""
    gh = sp.Symbol("gh")
    ghost = sp.solve(sp.Eq((N(u1) - gh) / (2 * N(h)), N(g)), gh)[0]
    return sp.N(N(u0) + N(r) * (N(u1) - 2 * N(u0) + ghost), 15)


def implicit_mid(a, b, c, r, theta=1):
    """one θ-scheme step (θ = 1 backward Euler, θ = 1/2 Crank–Nicolson) on three interior nodes, ends 0;
    returns the middle node"""
    th = N(theta)
    r = N(r)
    old = [0, N(a), N(b), N(c), 0]
    u = sp.symbols("u1:4")
    full = [0, *u, 0]
    eqs = []
    for i in range(1, 4):
        lap_new = full[i - 1] - 2 * full[i] + full[i + 1]
        lap_old = old[i - 1] - 2 * old[i] + old[i + 1]
        eqs.append(sp.Eq(full[i] - old[i], r * (th * lap_new + (1 - th) * lap_old)))
    sol = sp.solve(eqs, u)
    return sp.N(sol[u[1]], 15)


FUNCS = {f.__name__: f for f in [shift_source, source_steady, sine_coef, bessel_coef, bessel_rate, sphere_coef, sphere_centre,
                                 ramp_series_coef, ghost_step, implicit_mid]}
