"""Multivariable calculus drills (drills/problems/mvd-*.yaml): the verifier's own routes to each
answer. Wherever a card uses a theorem (Green, Stokes, divergence, a change of coordinates), the
check here takes a different road: the line integral itself, the surface integral itself, or the
integral in the original coordinates. Case fields hold expressions as strings in x, y, z, t, u, v.
"""
import sympy as sp

x, y, z, t, u, v = sp.symbols("x y z t u v", real=True)
NS = {"x": x, "y": y, "z": z, "t": t, "u": u, "v": v, "pi": sp.pi, "E": sp.E}


def S(e):
    return sp.sympify(e, locals=NS) if isinstance(e, str) else sp.sympify(e)


def num(e):
    return sp.N(S(e).doit(), 30)


def vpick(target, options):
    """index of the only option (each a sympy expression string, e.g. an Integral) equal in value to
    the target"""
    want = num(target)
    hits = [i for i, o in enumerate(options) if abs(num(o) - want) < sp.Float("1e-12") * (1 + abs(want))]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} options equal {want}: {[num(o) for o in options]}")
    return hits[0]


def at(e, px, py, pz=0):
    return sp.nsimplify(S(e).subs({x: px, y: py, z: pz}))


def d(e, *vs):
    ex = S(e)
    for w in vs:
        ex = sp.diff(ex, NS[w])
    return ex


def crit_class(f, px, py):
    """0 local minimum, 1 local maximum, 2 saddle, 3 test inconclusive; refuses a non-critical point"""
    F = S(f)
    pt = {x: px, y: py}
    if sp.simplify(sp.diff(F, x).subs(pt)) != 0 or sp.simplify(sp.diff(F, y).subs(pt)) != 0:
        raise ValueError("not a critical point")
    fxx, fyy, fxy = (sp.diff(F, a, b).subs(pt) for a, b in ((x, x), (y, y), (x, y)))
    D = sp.simplify(fxx * fyy - fxy ** 2)
    if D > 0:
        return 0 if fxx > 0 else 1
    return 2 if D < 0 else 3


def n_critical(f):
    F = S(f)
    sols = sp.solve([sp.diff(F, x), sp.diff(F, y)], [x, y], dict=True)
    return len([s for s in sols if all(val.is_real for val in s.values())])


def lagrange(f, g, kind, three=False):
    """max (kind 1) or min (kind 0) of f on g = 0, from all real solutions of grad f = λ grad g"""
    lam = sp.Symbol("lam")
    vs = [x, y, z] if three else [x, y]
    F, G = S(f), S(g)
    eqs = [sp.diff(F, w) - lam * sp.diff(G, w) for w in vs] + [G]
    vals = []
    for s in sp.solve(eqs, vs + [lam], dict=True):
        if all(s[w].is_real for w in vs):
            vals.append(sp.nsimplify(F.subs(s)))
    return (sp.Max if kind == 1 else sp.Min)(*vals)


def lagrange2(f, g, h, kind):
    """max (kind 1) or min (kind 0) of f(x, y, z) on g = 0 and h = 0, from grad f = λ grad g + μ grad h"""
    lam, mu = sp.symbols("lam mu")
    vs = [x, y, z]
    F, G, H = S(f), S(g), S(h)
    eqs = [sp.diff(F, w) - lam * sp.diff(G, w) - mu * sp.diff(H, w) for w in vs] + [G, H]
    vals = [sp.nsimplify(F.subs(s)) for s in sp.solve(eqs, vs + [lam, mu], dict=True) if all(s[w].is_real for w in vs)]
    return (sp.Max if kind == 1 else sp.Min)(*vals)


def line_work(P, Q, R, rx, ry, rz, t0, t1):
    """∫ F · dr along r(t), t0 ≤ t ≤ t1"""
    r = [S(rx), S(ry), S(rz)]
    sub = {x: r[0], y: r[1], z: r[2]}
    integrand = sum(S(c).subs(sub, simultaneous=True) * sp.diff(ri, t) for c, ri in zip((P, Q, R), r))
    return sp.simplify(sp.integrate(sp.simplify(integrand), (t, S(t0), S(t1))))


def line_scalar(f, rx, ry, rz, t0, t1):
    """∫ f ds along r(t)"""
    r = [S(rx), S(ry), S(rz)]
    speed = sp.sqrt(sp.simplify(sum(sp.diff(ri, t) ** 2 for ri in r)))
    integrand = sp.simplify(S(f).subs({x: r[0], y: r[1], z: r[2]}, simultaneous=True) * speed)
    return sp.simplify(sp.integrate(integrand, (t, S(t0), S(t1))))


def closed_work(P, Q, pieces):
    """circulation of P dx + Q dy around a closed curve given as pieces 'rx|ry|t0|t1;…'"""
    total = 0
    for piece in pieces.split(";"):
        rx, ry, t0, t1 = piece.split("|")
        total += line_work(P, Q, "0", rx, ry, "0", t0, t1)
    return sp.simplify(total)


def closed_flux2(P, Q, pieces):
    """outward flux ∮ P dy − Q dx of a counterclockwise closed curve"""
    total = 0
    for piece in pieces.split(";"):
        rx, ry, t0, t1 = piece.split("|")
        X, Y = S(rx), S(ry)
        sub = {x: X, y: Y}
        integrand = S(P).subs(sub, simultaneous=True) * sp.diff(Y, t) - S(Q).subs(sub, simultaneous=True) * sp.diff(X, t)
        total += sp.integrate(sp.simplify(integrand), (t, S(t0), S(t1)))
    return sp.simplify(total)


def surface_flux(P, Q, R, sx, sy, sz, u0, u1, v0, v1, sign=1):
    """∬ F · (r_u × r_v) du dv, times sign (to orient it)"""
    r = sp.Matrix([S(sx), S(sy), S(sz)])
    n = r.diff(u).cross(r.diff(v))
    Fv = sp.Matrix([S(P), S(Q), S(R)]).subs({x: r[0], y: r[1], z: r[2]}, simultaneous=True)
    integrand = sp.simplify(Fv.dot(n)) * sign
    return sp.simplify(sp.integrate(integrand, (u, S(u0), S(u1)), (v, S(v0), S(v1))))


def surface_scalar(f, sx, sy, sz, u0, u1, v0, v1):
    """∬ f dS with dS = |r_u × r_v| du dv"""
    r = sp.Matrix([S(sx), S(sy), S(sz)])
    n = r.diff(u).cross(r.diff(v))
    mag = sp.sqrt(sp.simplify(n.dot(n)))
    integrand = sp.simplify(S(f).subs({x: r[0], y: r[1], z: r[2]}, simultaneous=True) * mag)
    return sp.simplify(sp.integrate(integrand, (u, S(u0), S(u1)), (v, S(v0), S(v1))))


def box_flux(P, Q, R, a):
    """outward flux through the six faces of the cube [0, a]³, face by face"""
    a = S(a)
    F = [S(P), S(Q), S(R)]
    tot = 0
    for i, w in enumerate((x, y, z)):
        others = [o for o in (x, y, z) if o != w]
        for val, sgn in ((a, 1), (0, -1)):
            tot += sgn * sp.integrate(F[i].subs(w, val), (others[0], 0, a), (others[1], 0, a))
    return sp.simplify(tot)


def jac(xe, ye):
    """|∂(x, y)/∂(u, v)| for x = x(u, v), y = y(u, v)"""
    X, Y = S(xe), S(ye)
    return sp.Abs(sp.simplify(sp.Matrix([[X.diff(u), X.diff(v)], [Y.diff(u), Y.diff(v)]]).det()))


def is_conservative(P, Q, R="0"):
    """0 if curl F = 0 everywhere it is defined, else 1"""
    F = [S(P), S(Q), S(R)]
    c = [sp.diff(F[2], y) - sp.diff(F[1], z), sp.diff(F[0], z) - sp.diff(F[2], x), sp.diff(F[1], x) - sp.diff(F[0], y)]
    return 0 if all(sp.simplify(ci) == 0 for ci in c) else 1


def _nint(I):
    """an Integral (nested, variable limits) by nested Gauss-Legendre quadrature, independent of sympy's antiderivatives"""
    import mpmath
    lims = list(I.limits)  # innermost first
    vars_ = [l[0] for l in lims]
    re_ = lambda g: (lambda *a: mpmath.re(g(*a)))  # noqa: E731 — sqrt of a rounding-negative 0 comes back complex
    f = re_(sp.lambdify(vars_, I.function, "mpmath"))
    bounds = [(re_(sp.lambdify(vars_, l[1], "mpmath")), re_(sp.lambdify(vars_, l[2], "mpmath"))) for l in lims]

    def level(k, vals):
        lo, hi = bounds[k]
        args = lambda w: [vals.get(j, w if j == k else 0) for j in range(len(vars_))]  # noqa: E731
        a, b = lo(*args(0)), hi(*args(0))
        if k == 0:
            return mpmath.quad(lambda w: f(*args(w)), [a, b])
        return mpmath.quad(lambda w: level(k - 1, {**vals, k: w}), [a, b])

    mpmath.mp.dps = 20
    return sp.Float(level(len(lims) - 1, {}), 15)


def quad(e):
    """evaluate an expression containing Integrals numerically, each Integral by _nint"""
    E_ = S(e)
    return sp.N(E_.replace(lambda q: isinstance(q, sp.Integral), _nint), 15)


FUNCS = {f.__name__: f for f in [lagrange2, vpick, crit_class, n_critical, lagrange, line_work, line_scalar, closed_work,
                                  closed_flux2, surface_flux, surface_scalar, box_flux, jac, is_conservative]}


def mv_eval(expr, P, Q, R):
    """evaluate a case's own verify expression (a sum of surface_flux pieces) with these field components"""
    return eval(expr, {"__builtins__": {}}, {**FUNCS, "P": P, "Q": Q, "R": R, "pi": sp.pi})


FUNCS["mv_eval"] = mv_eval
FUNCS.update({"denom": sp.denom, "cancel": sp.cancel, "combsimp": sp.combsimp, "quad": quad, "SE": S, "mv_at": at, "mv_d": d})


def check(p, H):
    """the multivariable cards are problems as data, checked by data.py with the functions above"""
    return None
