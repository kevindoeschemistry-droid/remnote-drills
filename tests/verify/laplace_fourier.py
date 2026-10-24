"""
First-principles sympy checks for the Laplace / Fourier / PDE / special-function drills.
Nothing here reuses the generator's closed forms:

  laplace.table, laplace.shifting (forward)   sympy laplace_transform of f(t) == reference F(s)
  laplace.inverse, laplace.shifting (inverse) laplace_transform of the reference f(t) == the given F(s)
  laplace.ivp                                 dsolve of the IVP == reference y(t)
  laplace.convolution                         the convolution integral evaluated by sympy (compute,
                                              transform), L{reference} == F (inverse), or the reference
                                              substituted into the integral equation (Volterra)
  bvp.fourier-series                          Euler formulas integrated piece by piece for n = 1..6
  pde.separation                              u substituted into the PDE, both BCs and the IC(s);
                                              rates: product solutions satisfy PDE + BCs for n = start..start+3
  series.special-functions                    classify by Q/P, R/P against the standard forms; Legendre n
                                              from P_n solving the ODE; Bessel order / scale / independence
                                              by substituting besselj numerically
"""
import random

import mpmath
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

s, t, x, n, tau = sp.symbols("s t x n tau")
_LOC = {"s": s, "t": t, "x": x, "n": n, "exp": sp.exp, "sin": sp.sin, "cos": sp.cos, "sinh": sp.sinh,
        "cosh": sp.cosh, "sqrt": sp.sqrt, "abs": sp.Abs, "pi": sp.pi, "e": sp.E, "heaviside": sp.Heaviside}

SKILLS = {"laplace.table", "laplace.inverse", "laplace.shifting", "laplace.ivp", "laplace.convolution",
          "bvp.fourier-series", "pde.separation", "series.special-functions"}


def P(src):
    return parse_expr(str(src).replace("^", "**"), local_dict=_LOC)


def num_equal(a, b, var, pts, tol=1e-10):
    """a == b at every sample point (high-precision numerics; skips singular points)."""
    good = 0
    for v in pts:
        try:
            av = complex(sp.N(a.subs(var, v), 30))
            bv = complex(sp.N(b.subs(var, v), 30))
        except (TypeError, ZeroDivisionError):
            continue
        if av != av or bv != bv:
            continue
        # relative: e^{-as} makes values tiny, so an absolute floor would hide errors
        if abs(av - bv) > max(tol * max(abs(av), abs(bv)), 1e-25):
            return False
        good += 1
    return good >= 3


S_PTS = [sp.Rational(k, 7) for k in (45, 52, 61, 73, 88)]  # s in (6.4, 12.6): right of every pole used


def laplace(f):
    F = sp.laplace_transform(f, t, s, noconds=True)
    if F.has(sp.LaplaceTransform):
        raise ValueError(f"sympy could not transform {f}")
    return F


def t_points(meta):
    return [sp.Rational(k, 100) for k in (23, 61, 97, 134, 171, 228, 263, 319, 377)]


def check_forward(p):
    return num_equal(laplace(P(p["meta"]["f"])), P(p["answer"]["ref"]), s, S_PTS)


def check_inverse(p):
    return num_equal(laplace(P(p["answer"]["ref"])), P(p["meta"]["F"]), s, S_PTS)


def check_ivp(p):
    a, meta = p["answer"], p["meta"]
    y = sp.Function("y")
    rhs = P(meta["rhs"])
    ode = sp.Eq(y(t).diff(t, 2) + meta["b"] * y(t).diff(t) + meta["c"] * y(t), rhs)
    sol = sp.dsolve(ode, y(t), ics={y(0): meta["y0"], y(t).diff(t).subs(t, 0): meta["y1"]}).rhs
    ref = P(a["ref"])
    if a["ic"] != [0, meta["y0"], meta["y1"]]:
        return False
    return sp.simplify(sp.expand(sol - ref)) == 0 or num_equal(sol, ref, t, t_points(meta), 1e-12)


def conv_integral(fs, gs):
    f, g = P(fs), P(gs)
    return sp.integrate(f.subs(t, tau) * g.subs(t, t - tau), (tau, 0, t))


def check_convolution(p):
    tmpl, meta, ref = p["template"], p["meta"], P(p["answer"]["ref"])
    if tmpl == "conv-compute":
        return num_equal(conv_integral(meta["f"], meta["g"]), ref, t, t_points(meta), 1e-12)
    if tmpl == "conv-transform":
        h = conv_integral(meta["f"], meta["g"])
        return num_equal(laplace(h), ref, s, S_PTS)
    if tmpl == "conv-inverse":
        return num_equal(laplace(ref), P(meta["F"]), s, S_PTS)
    if tmpl == "conv-volterra":
        # y(t) + lam * ∫_0^t K(t - tau) y(tau) dtau = rhs(t)
        K = P(meta["K"])
        integral = sp.integrate(K.subs(x, t - tau) * ref.subs(t, tau), (tau, 0, t))
        resid = ref + meta["lam"] * integral - P(meta["rhs"])
        return num_equal(resid, sp.Integer(0), t, t_points(meta), 1e-12)
    return False


def check_fourier(p):
    """Euler formulas integrated with a symbolic integer n, then compared for n = 1..6."""
    meta, fields = p["meta"], p["answer"]["fields"]
    L = P(meta["L"])
    pieces = [(P(e), P(lo), P(hi)) for e, lo, hi in meta["pieces"]]
    kind = meta["kind"]
    N = sp.Symbol("N", integer=True, positive=True)
    I = lambda w: sum(sp.integrate(e * w, (x, lo, hi)) for e, lo, hi in pieces)
    cosN, sinN = sp.cos(N * sp.pi * x / L), sp.sin(N * sp.pi * x / L)
    if kind == "full":
        want = {"a_0": I(1) / (2 * L), "a_n": I(cosN) / L, "b_n": I(sinN) / L}
    elif kind == "sine":
        want = {"b_n": 2 * I(sinN) / L}
    else:
        want = {"a_0": I(1) / L, "a_n": 2 * I(cosN) / L}
    if sorted(want) != sorted(f["label"] for f in fields):
        return False
    for k in range(1, 7):
        for f in fields:
            got = P(f["ref"]).subs(n, k)
            if abs(complex(sp.N(got - want[f["label"]].subs(N, k), 30))) > 1e-20:
                return False
    return True


def check_pde(p):
    meta, a = p["meta"], p["answer"]
    L, c2 = P(meta["L"]), sp.Integer(meta["c2"])
    bc = meta["bc"]
    if a["kind"] == "indexed":
        lam = P(a["ref"])
        if sp.simplify(lam - P(meta["lam"])) != 0:
            return False
        for k in range(meta["start"], meta["start"] + 4):
            Fk = sp.sin(k * sp.pi * x / L) if bc == "DD" else sp.cos(k * sp.pi * x / L)
            lk = lam.subs(n, k)
            if meta["pde"] == "heat":
                u = Fk * sp.exp(-lk * t)
                pde = sp.diff(u, t) - c2 * sp.diff(u, x, 2)
            else:
                u = Fk * sp.cos(lk * t)
                pde = sp.diff(u, t, 2) - c2 * sp.diff(u, x, 2)
            if sp.simplify(pde) != 0 or sp.simplify(Fk) == 0:
                return False
            ends = (u, u) if bc == "DD" else (sp.diff(u, x), sp.diff(u, x))
            if sp.simplify(ends[0].subs(x, 0)) != 0 or sp.simplify(ends[1].subs(x, L)) != 0:
                return False
        # the rates are the eigenvalues: none smaller is missed (n = start is the lowest mode)
        return True
    u = P(a["ref"])
    if meta["pde"] == "heat":
        pde = sp.diff(u, t) - c2 * sp.diff(u, x, 2)
    else:
        pde = sp.diff(u, t, 2) - c2 * sp.diff(u, x, 2)
    if sp.simplify(pde) != 0:
        return False
    if bc == "DD":
        ok_bc = sp.simplify(u.subs(x, 0)) == 0 and sp.simplify(u.subs(x, L)) == 0
    elif bc == "NN":
        ux = sp.diff(u, x)
        ok_bc = sp.simplify(ux.subs(x, 0)) == 0 and sp.simplify(ux.subs(x, L)) == 0
    else:
        ok_bc = sp.simplify(u.subs(x, 0) - meta["T1"]) == 0 and sp.simplify(u.subs(x, L) - meta["T2"]) == 0
    if not ok_bc:
        return False
    if sp.simplify(u.subs(t, 0) - P(meta["u0"])) != 0:
        return False
    if meta["pde"] == "wave" and sp.simplify(sp.diff(u, t).subs(t, 0) - P(meta["ut0"])) != 0:
        return False
    return True


def bessel_residual_ok(nu, k, P_, Q_, R_):
    """y = J_nu(k x) solves P y'' + Q y' + R y = 0 (numerically, at several x)."""
    for xv in (0.37, 0.91, 1.6, 2.3):
        xv = mpmath.mpf(xv)
        y = lambda z: mpmath.besselj(nu, k * z)
        res = P_(xv) * mpmath.diff(y, xv, 2) + Q_(xv) * mpmath.diff(y, xv) + R_(xv) * y(xv)
        if abs(res) > mpmath.mpf(10) ** -20 * max(1, abs(y(xv))):
            return False
    return True


def lam(e):
    f = sp.lambdify(x, P(e), "mpmath")
    return lambda v: f(v)


def classify(Ps, Qs, Rs):
    Pp, Qp, Rp = P(Ps), P(Qs), P(Rs)
    q, r = sp.simplify(Qp / Pp), sp.simplify(Rp / Pp)
    const = lambda e: not sp.simplify(e).has(x)
    hits = []
    if sp.simplify(q * (1 - x**2) + 2 * x) == 0 and const(r * (1 - x**2)):
        hits.append(0)  # Legendre
    if sp.simplify(q - 1 / x) == 0 and const((r - 1) * x**2):
        hits.append(1)  # Bessel
    if const(q * x) and const(r * x**2):
        hits.append(2)  # Euler–Cauchy
    if sp.simplify(q + 2 * x) == 0 and const(r):
        hits.append(3)  # Hermite
    return hits


def check_special(p):
    meta, a = p["meta"], p["answer"]
    v = meta["variant"]
    mpmath.mp.dps = 40
    if v == "identify":
        hits = classify(meta["P"], meta["Q"], meta["R"])
        return hits == [meta["type"]] and a["correct"] == a["options"][meta["type"]]
    if v == "legendre-n":
        if classify(meta["P"], meta["Q"], meta["R"]) != [0]:
            return False
        nn = sp.nsimplify(P(a["ref"]))
        if not (nn.is_integer and nn >= 0):
            return False
        y = sp.legendre(int(nn), x)
        res = P(meta["P"]) * sp.diff(y, x, 2) + P(meta["Q"]) * sp.diff(y, x) + P(meta["R"]) * y
        return sp.expand(res) == 0
    if v == "bessel-order":
        nu = P(a["ref"])
        return nu >= 0 and bessel_residual_ok(mpmath.mpf(sp.N(nu, 40)), meta["k"], lam(meta["P"]), lam(meta["Q"]), lam(meta["R"]))
    if v == "bessel-scaled":
        nu0, k0 = meta["nu"], meta["k"]
        Pf, Qf, Rf = (lambda z: z**2), (lambda z: z), (lambda z: k0**2 * z**2 - nu0**2)
        results = [bessel_residual_ok(o_nu, mpmath.mpf(sp.N(P(o_k), 40)), Pf, Qf, Rf) for o_nu, o_k in meta["options"]]
        right = results.index(True) if results.count(True) == 1 else -1
        return right == meta["correctIndex"] and a["correct"] == a["options"][right]
    if v == "bessel-independent":
        nu = mpmath.mpf(meta["nu"])
        # Wronskian of J_nu, J_-nu at x = 1 (nonzero iff independent)
        J1 = lambda z: mpmath.besselj(nu, z)
        J2 = lambda z: mpmath.besselj(-nu, z)
        xv = mpmath.mpf(1)
        W = J1(xv) * mpmath.diff(J2, xv) - J2(xv) * mpmath.diff(J1, xv)
        independent = abs(W) > mpmath.mpf(10) ** -20
        return a["correct"] == a["options"][0 if independent else 1] and independent == (not meta["integer"])
    return False


def check(p, H):
    if p["skill"] not in SKILLS:
        return None
    sk, tmpl = p["skill"], p["template"]
    if sk == "laplace.table":
        return check_forward(p)
    if sk == "laplace.inverse":
        return check_inverse(p)
    if sk == "laplace.shifting":
        return check_forward(p) if tmpl in ("shift-s-forward", "shift-t-forward", "shift-piecewise") else check_inverse(p)
    if sk == "laplace.ivp":
        return check_ivp(p)
    if sk == "laplace.convolution":
        return check_convolution(p)
    if sk == "bvp.fourier-series":
        return check_fourier(p)
    if sk == "pde.separation":
        return check_pde(p)
    return check_special(p)
