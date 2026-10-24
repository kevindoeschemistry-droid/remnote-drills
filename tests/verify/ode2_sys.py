"""
Independent sympy checks for the ode2-sys area (src/drills/gen-ode2-sys.ts). Nothing here reuses the
generator's formulas — every answer is tested by the property that defines it:

  ode2 (+coef)   Σ coef_i(v) g^(n-i) = rhs exactly (50-digit evaluation at random points); IVP: no
                 constants and g^(j)(t0) = ic; particular: no constants; general: n constants, each
                 multiplying a solution, with nonzero Wronskian. Reduction of order: the given y1 solves too.
  roots          Euler–Cauchy: substitute y = x^m into the equation and solve for m;
                 higher order: roots of the characteristic polynomial; systems: eigenvalues of A
  expression     steady state: solves the forced equation and is periodic; amplitude: solve for the
                 trig coefficients of y_p and take sqrt(a² + b²); practical resonance: maximise that
                 amplitude over ω
  tuple+system   y' = Ay componentwise; IVP values; general: Wronskian of the two constant directions
  choice         phase type from p = tr A, q = det A, Δ = p² − 4q (Kreyszig's criteria)
"""
import random

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

MINE = {"ode2.reduction", "ode2.euler-cauchy", "ode2.spring-forced", "ode2.variation",
        "ode2.higher-order", "odesys.eigenvalue", "odesys.phase"}


def _parse(H, s):
    loc = dict(H.LOC)
    loc.update({"atan": sp.atan, "log": sp.log, "tan": sp.tan, "x": H.x, "t": H.t})
    return parse_expr(str(s).replace("^", "**"), local_dict=loc)


def _nzero(expr, syms, lo=0.3, hi=2.0):
    """expr == 0 at 8 random rational points (50 digits); variables in [lo, hi], constants in [-2, 2]."""
    rnd = random.Random(7)
    good = 0
    for _ in range(30):
        pt = {}
        for i, s_ in enumerate(syms):
            a, b = (lo, hi) if i == 0 else (-2, 2)
            pt[s_] = sp.Rational(rnd.randint(int(a * 100), int(b * 100)), 100)
        try:
            v = complex(sp.N(expr.subs(pt), 50))
        except (TypeError, ZeroDivisionError):
            continue
        if v != v or abs(v) == float("inf"):
            continue
        if abs(v) > 1e-30:
            return False
        good += 1
        if good >= 8:
            return True
    return False


def _num_eq(a, b):
    return abs(complex(sp.N(sp.sympify(a) - sp.sympify(b), 40))) < 1e-25


def _wronskian_nonzero(fs, v):
    n = len(fs)
    W = sp.Matrix(n, n, lambda i, j: sp.diff(fs[j], v, i)).det()
    for x0 in (sp.Rational(7, 10), sp.Rational(13, 10)):
        val = complex(sp.N(W.subs(v, x0), 40))
        if abs(val) > 1e-12:
            return True
    return False


def ode_ok(p, H):
    a, meta = p["answer"], p.get("meta", {})
    v = sp.Symbol(a["v"])
    g = _parse(H, a["ref"]).subs(sp.Symbol(a["v"]), v)
    coef = [_parse(H, c) for c in a["coef"]] if a.get("coef") else [a["a"], a["b"], a["c"]]
    n = len(coef) - 1
    f = _parse(H, a["rhs"]) if a.get("rhs") else 0
    L = lambda y_: sum(c * sp.diff(y_, v, n - i) for i, c in enumerate(coef))  # noqa: E731
    consts = sorted(g.free_symbols - {v}, key=str)
    if not _nzero(L(g) - f, [v] + consts):
        return False
    if meta.get("y1"):  # reduction of order: the handed-out solution must be one
        y1 = _parse(H, meta["y1"])
        if not _nzero(L(y1), [v]) or sp.simplify(y1) == 0:
            return False
    if a.get("ic"):
        t0, *vals = a["ic"]
        if consts or len(vals) != n:
            return False
        return all(_num_eq(sp.diff(g, v, j).subs(v, sp.nsimplify(t0)), sp.nsimplify(vals[j])) for j in range(n))
    if a.get("particular"):
        return not consts and f != 0
    if len(consts) != n:
        return False
    basis = [sp.diff(g, c) for c in consts]
    if any(b.free_symbols & set(consts) for b in basis):  # constants must enter linearly
        return False
    return all(_nzero(L(b), [v]) for b in basis) and _wronskian_nonzero(basis, v)


def system_ok(p, H):
    a = p["answer"]
    S = a["system"]
    v = sp.Symbol(S["v"])
    A = sp.Matrix(S["A"])
    Y = sp.Matrix([_parse(H, f["ref"]) for f in a["fields"]])
    consts = sorted(set().union(*[e.free_symbols for e in Y]) - {v}, key=str)
    res = Y.diff(v) - A * Y
    if not all(_nzero(r_, [v] + consts, 0.0, 1.5) for r_ in res):
        return False
    if S.get("ic"):
        t0, *vals = S["ic"]
        return not consts and all(_num_eq(Y[i].subs(v, t0), vals[i]) for i in range(len(vals)))
    if len(consts) != 2:
        return False
    cols = [Y.diff(c) for c in consts]
    W = sp.Matrix.hstack(*cols).det()
    return any(abs(complex(sp.N(W.subs(v, x0), 30))) > 1e-12 for x0 in (0, sp.Rational(1, 2)))


def phase_class(A):
    """Kreyszig Table 4.1/4.2 from p = tr A, q = det A."""
    p_, q_ = A.trace(), A.det()
    D = p_**2 - 4 * q_
    if q_ < 0:
        return "saddle", "unstable"
    if q_ == 0:
        raise ValueError("degenerate")
    if D >= 0:
        return "node", ("stable" if p_ < 0 else "unstable")
    if p_ == 0:
        return "center", "neutral"
    return "spiral", ("stable" if p_ < 0 else "unstable")


def label_class(label):
    lo = label.lower()
    stab = "neutral" if "not attractive" in lo else "unstable" if "unstable" in lo else "stable"
    typ = next((k for k in ("node", "saddle", "center", "spiral") if k in lo), None)
    return typ, stab


def forced_expected(meta, H, target):
    """Steady-state coefficients by substitution (undetermined coefficients done by sympy)."""
    t = H.t
    a_, b_, W = sp.symbols("a_ b_ W", real=True)
    mm, c, k, F0 = (sp.Integer(meta[q]) for q in ("mm", "c", "k", "F0"))
    w = W if target == "practical" else sp.Integer(meta["w"])
    fn = sp.cos if meta.get("fn", "cos") == "cos" else sp.sin
    yp = a_ * sp.cos(w * t) + b_ * sp.sin(w * t)
    res = mm * yp.diff(t, 2) + c * yp.diff(t) + k * yp - F0 * fn(w * t)
    sol = sp.solve([res.subs(t, 0), res.subs(t, sp.pi / (2 * w))], [a_, b_], dict=True)[0]
    amp2 = sp.simplify(sol[a_] ** 2 + sol[b_] ** 2)
    if target == "amplitude":
        return sp.sqrt(amp2)
    crit = [r_ for r_ in sp.solve(sp.diff(amp2, W), W) if r_.is_positive]
    best = max(crit, key=lambda r_: float(amp2.subs(W, r_)))
    return best


def check(p, H):
    if p["skill"] not in MINE:
        return None
    a, meta = p["answer"], p.get("meta", {})
    kind = a["kind"]
    if kind == "ode2":
        return ode_ok(p, H)
    if kind == "tuple" and a.get("system"):
        return system_ok(p, H)
    if kind == "roots":
        ref = {sp.nsimplify(r_) for r_ in a["ref"]}
        v = meta["variant"]
        if v == "ec-roots":
            mS = sp.Symbol("m")
            x = H.x
            y_ = x**mS
            expr = sp.simplify((meta["A"] * x**2 * y_.diff(x, 2) + meta["B"] * x * y_.diff(x) + meta["C"] * y_) / y_)
            return set(sp.solve(sp.expand(expr), mS)) == ref
        if v == "hi-roots":
            lamS = sp.Symbol("lam")
            roots = sp.roots(sp.Poly(meta["coef"], lamS))
            return set(roots) == ref and all(r_.is_real for r_ in roots)
        if v == "sys-eigen":
            return set(sp.Matrix(meta["A"]).eigenvals()) == ref
        return False
    if kind == "expression":
        v = meta.get("variant")
        if v == "forced-steady":
            t = H.t
            g = _parse(H, a["ref"])
            if g.free_symbols - {t}:
                return False
            w = sp.Integer(meta["w"])
            fn = sp.cos if meta["fn"] == "cos" else sp.sin
            res = meta["mm"] * g.diff(t, 2) + meta["c"] * g.diff(t) + meta["k"] * g - meta["F0"] * fn(w * t)
            periodic = g.subs(t, t + 2 * sp.pi / w) - g
            return _nzero(res, [t]) and _nzero(periodic, [t])
        if v == "forced-amplitude":
            return _num_eq(forced_expected(meta, H, "amplitude"), _parse(H, a["ref"]))
        if v == "forced-practical":
            return _num_eq(forced_expected(meta, H, "practical"), _parse(H, a["ref"]))
        return False
    if kind == "choice":
        A = sp.Matrix(meta["A"])
        typ, stab = phase_class(A)
        if meta["variant"] == "phase-stability":
            want = {"stable": "asymptotically stable", "neutral": "stable, not attractive", "unstable": "unstable"}[stab]
            return a["correct"].lower() == want
        # every option must name a distinct class, and the correct one must match
        classes = [label_class(o) for o in a["options"]]
        return len(set(classes)) == len(classes) and label_class(a["correct"]) == (typ, stab if typ != "saddle" else "unstable")
    return False
