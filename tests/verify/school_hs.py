"""
High school mathematics (gen-hs.ts: alg-, geo-, trig-, stats- templates) — every answer
recomputed from the problem's inputs, sharing no formula with the generator:

  algebra      equations, inequalities, systems and formulas solved by sympy (solve,
               solveset over the reals so extraneous roots drop out); polynomial division,
               expansion and factoring by sympy; vertex by setting the derivative to 0;
               inverses checked by composing f(f⁻¹(x)) = x; sequences regenerated term by term
  exp / log    sympy solve and limits; log identities checked numerically with u = log_b 2,
               v = log_b 3
  complex      sympy I arithmetic; vectors and matrices with sympy Matrix
  geometry     coordinates: shoelace areas, sympy Point / Line (reflections, rotations,
               parallels, perpendiculars, intersections); circle angles from vectors on a
               constructed circle; volumes and arc lengths by integration; conics by testing
               the focal-distance property on parametrised points
  trig         exact values by sympy; solutions by solveset on [0, 2π); amplitude / period by
               sampling and sympy periodicity
  statistics   statistics module; least squares by minimising the SSE with sympy; normal
               percentages from erf; probabilities by enumerating outcomes with itertools
"""
import itertools
import math
import re
import statistics
from fractions import Fraction as Fr

import sympy as sp

X, Y, T = sp.symbols("x y t")
N = sp.Symbol("n")
BASE = {"x": X, "y": Y, "t": T, "n": N, "pi": sp.pi, "sqrt": sp.sqrt, "abs": sp.Abs, "Abs": sp.Abs, "I": sp.I,
        "log": sp.log, "exp": sp.exp, "sin": sp.sin, "cos": sp.cos, "floor": sp.floor, "E": sp.E,
        "cbrt": lambda v: sp.real_root(v, 3), "asin": sp.asin, "acos": sp.acos}
RAD = sp.pi / 180


def S(s, extra=None):
    loc = dict(BASE)
    if extra:
        loc.update(extra)
    return sp.sympify(str(s).replace("^", "**"), locals=loc, rational=True)


def num(v):
    return complex(sp.N(v, 40))


def close(u, v, tol=1e-10):
    if getattr(sp.sympify(u), "free_symbols", None) or getattr(sp.sympify(v), "free_symbols", None):
        return sp.simplify(sp.sympify(u) - sp.sympify(v)) == 0
    a, b = num(u), num(v)
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def ans(p):
    a = p["answer"]
    k = a["kind"]
    if k == "expression":
        return S(a["ref"], {v: sp.Symbol(v) for v in a.get("vars", []) if v not in ("x", "n")})
    if k == "choice":
        return a["correct"]
    if k == "tuple":
        return [S(f["ref"]) for f in a["fields"]]
    if k == "roots":
        return a["ref"]
    raise KeyError(k)


def same_set(got, exp, tol=1e-9):
    g = sorted({round(float(v), 9) for v in got})
    e = sorted({round(float(sp.N(v)), 9) for v in exp})
    return len(g) == len(e) and all(abs(a - b) <= tol * max(1, abs(b)) for a, b in zip(g, e))


def rel_tol(p):
    a = p["answer"]
    return 1e-9 if a.get("rel") or a.get("kind") == "tuple" else 1e-10


def tri_by_angles(a_side, B_deg, C_deg):
    """B at origin, C at (a, 0); A where the rays at angles B and 180 - C meet (float geometry)."""
    b_, c_ = math.radians(B_deg), math.radians(180 - C_deg)
    # B + s(cos b, sin b) = C + t(cos c, sin c)
    det = math.cos(b_) * (-math.sin(c_)) + math.sin(b_) * math.cos(c_)
    s_ = (a_side * (-math.sin(c_))) / det
    return (s_ * math.cos(b_), s_ * math.sin(b_)), (0.0, 0.0), (float(a_side), 0.0)


def angle_at(P, A, B):
    """angle APB in degrees (float geometry)"""
    u = (A[0] - P[0], A[1] - P[1])
    v = (B[0] - P[0], B[1] - P[1])
    c = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def circ(deg):
    return (math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def halves_quartiles(xs):
    s = sorted(xs)
    n = len(s)
    return Fr(statistics.median(s[: n // 2])).limit_denominator(2), Fr(statistics.median(s[(n + 1) // 2:])).limit_denominator(2)


def deck():
    ranks = ["ace"] + [str(i) for i in range(2, 11)] + ["jack", "queen", "king"]
    names = {"7": "seven"}
    return [(names.get(r, r), s) for r in ranks for s in ("hearts", "diamonds", "clubs", "spades")]


def vol_by_slices(area_of_z, z0, z1):
    z = sp.Symbol("z")
    return sp.integrate(area_of_z(z), (z, z0, z1))


# ── expected answers ────────────────────────────────────────────────────────
def expected(p):
    me = p["meta"]
    mx = me["mx"]
    a = p["answer"]
    if mx == "expr":
        return S(me["e"])
    if mx == "solve":
        sols = sp.solve(S(me["eq"]), X)
        assert len(sols) == 1
        return sols[0]
    if mx == "literal":
        names = set(re.findall(r"[A-Za-z]+", me["eq"] + " " + a["ref"])) - {"pi"}
        syms = {nm: sp.Symbol(nm) for nm in names}
        sol = sp.solve(S(me["eq"], syms), syms[me["v"]])
        assert len(sol) == 1
        return ("same-expr", sol[0], syms)
    if mx == "ineq":
        rel = {"<": sp.Lt, "≤": sp.Le, ">": sp.Gt, "≥": sp.Ge}[me["rel"]]
        sol = sp.solve_univariate_inequality(rel(S(me["l"]), S(me["r"])), X, relational=False)
        for o in a["options"]:
            _, op, v = o.split()
            v = S(v)
            cand = {"<": sp.Interval.open(-sp.oo, v), "≤": sp.Interval(-sp.oo, v), ">": sp.Interval.open(v, sp.oo), "≥": sp.Interval(v, sp.oo)}[op]
            if cand == sol:
                return o
        return None
    if mx == "eval":
        return S(me["f"]).subs(X, me["at"])
    if mx == "recur":
        v = me["a1"]
        for _ in range(me["k"] - 1):
            v = me["mul"] * v + me["d"]
        return v
    if mx == "avg-rate":
        f = S(me["f"])
        return (f.subs(X, me["b"]) - f.subs(X, me["a"])) / (me["b"] - me["a"])
    if mx == "intercepts":
        e = S(me["e"])
        return [sp.solve(e.subs(Y, 0), X)[0], sp.solve(e.subs(X, 0), Y)[0]]
    if mx == "le-desc":
        t = me["txt"]
        return "Exponential" if ("%" in t or "doubles" in t) else "Linear"
    if mx == "le-table":
        ys = me["ys"]
        d = {b - a_ for a_, b in zip(ys, ys[1:])}
        rt = {Fr(b, a_) for a_, b in zip(ys, ys[1:]) if a_ != 0}
        return "Linear" if len(d) == 1 else "Exponential" if len(rt) == 1 and 0 not in ys else "Neither"
    if mx == "exp2":
        A, B = sp.symbols("A B", real=True)
        (x1, y1), (x2, y2) = me["p"], me["q"]
        sols = [s for s in sp.solve([A * B ** x1 - S(y1), A * B ** x2 - S(y2)], [A, B], dict=True) if s[B].is_positive]
        assert len(sols) == 1
        return [sols[0][A], sols[0][B]]
    if mx == "seq":
        t = [S(v) for v in me["terms"]]
        r_ = t[1] / t[0] if me["geo"] else t[1] - t[0]
        gen = [t[0]]
        for _ in range(7):
            gen.append(gen[-1] * r_ if me["geo"] else gen[-1] + r_)
        return ("seq", gen)
    if mx == "pct-rate":
        return (S(me["b"]) ** sp.Rational(1, me["per"]) - 1) * 100
    if mx == "exponent":
        base, e = sp.powsimp(S(me["e"]).subs(X, sp.Symbol("x", positive=True)), force=True).as_base_exp()
        return e
    if mx == "half-plane":
        ok = all(bool(S(q).subs({X: me["x"], Y: me["y"]})) for q in me["ineqs"])
        return "Yes" if ok else "No"
    if mx == "coeffs":
        cs = sp.Poly(sp.expand(S(me["e"])), X).all_coeffs()
        return [0] * (me["deg"] + 1 - len(cs)) + cs
    if mx in ("zeros", "lin-quad", "real-zeros", "solve-real", "trig-solve", "log-eq"):
        if mx == "zeros":
            sols = list(sp.roots(sp.Poly(S(me["e"]), X)).keys())
        elif mx == "lin-quad":
            sols = sp.solve(S(me["f"]) - S(me["g"]), X)
        elif mx == "real-zeros":
            sols = sp.real_roots(sp.Poly(S(me["e"]), X))
        elif mx == "solve-real":
            sols = list(sp.solveset(S(me["eq"]), X, sp.S.Reals))
        elif mx == "log-eq":
            xs = sp.Symbol("x", positive=True)
            sols = [s for s in sp.solve(sp.log(xs, me["b"]) + sp.log(xs - me["a"], me["b"]) - me["k"], xs) if (s - me["a"]).is_positive]
        else:
            f = sp.sin if me["fn"] == "sin" else sp.cos
            sols = list(sp.solveset(f(X) - S(me["v"]), X, sp.Interval.Ropen(0, 2 * sp.pi)))
        return ("set", sols)
    if mx == "vertex-form":
        h, k = sp.symbols("h k")
        sol = sp.solve(sp.Poly(sp.expand(S(me["e"]) - me["a"] * (X - h) ** 2 - k), X).all_coeffs(), [h, k], dict=True)
        return [sol[0][h], sol[0][k]]
    if mx == "nreal":
        return str(len(set(sp.real_roots(sp.Poly(S(me["e"]), X)))))
    if mx == "projectile":
        e = S(me["e"])
        if me["ask"] == 0:
            return [s for s in sp.solve(e, X) if s > 0][0]
        tv = sp.solve(sp.diff(e, X), X)[0]
        return e.subs(X, tv)
    if mx == "vertex":
        e = S(me["e"])
        h = sp.solve(sp.diff(e, X), X)[0]
        return [h, e.subs(X, h)]
    if mx == "transform-fn":
        f = S(me["f"])
        return ("same-fn", me["a"] * f.subs(X, X - me["h"]) + me["k"])
    if mx == "even-odd":
        e = S(me["e"])
        return "Even" if sp.simplify(e.subs(X, -X) - e) == 0 else "Odd" if sp.simplify(e.subs(X, -X) + e) == 0 else "Neither"
    if mx == "inverse":
        return ("inverse", S(me["f"]))
    if mx == "piecewise":
        f = sp.Piecewise((me["a"] * X + me["b"], X < me["c"]), (X ** 2 - me["p"], True))
        return f.subs(X, me["x"])
    if mx == "binom-coef":
        return sp.Poly(sp.expand(S(me["e"])), X).coeff_monomial(X ** me["k"])
    if mx == "remainder":
        return sp.div(S(me["e"]), X - me["a"], X)[1]
    if mx == "geo-sum":
        r_ = S(me["r"])
        return sum(me["a"] * r_ ** i for i in range(me["n"]))
    if mx == "polydiv":
        qq, rr = sp.div(S(me["num"]), X - me["d"], X)
        return [qq, rr]
    if mx == "rat-add":
        e = sp.cancel(sp.together(S(me["e"])) * S(me["den"]))
        P = sp.Poly(e, X)
        return [P.coeff_monomial(X), P.coeff_monomial(1)]
    if mx == "complex":
        v = sp.nsimplify(sp.simplify(S(me["e"])))
        return [sp.re(v), sp.im(v)] if a["kind"] == "tuple" else v
    if mx == "complex-roots":
        r_ = [z for z in sp.roots(sp.Poly(S(me["e"]), X)) if sp.im(z) > 0][0]
        return [sp.re(r_), sp.im(r_)]
    if mx == "exp-solve":
        b = sp.E if me["b"] == "E" else S(me["b"])
        sols = sp.solve(me["a"] * b ** (S(me["c"]) * T) - me["d"], T)
        return [s for s in sols if s.is_real][0]
    if mx == "exp-graph":
        e = S(me["e"])
        return [e.subs(X, 0), sp.limit(e, X, -sp.oo if me["grow"] else sp.oo)]
    if mx == "log-graph":
        b, h, k = me["b"], me["h"], me["k"]
        f = sp.log(X - h, b) + k
        dom = sp.solve_univariate_inequality(X - h > 0, X, relational=False)
        return [dom.inf, sp.solve(f, X)[0]]
    if mx == "cool":
        return me["Ta"] + me["D"] * sp.exp(-S(me["k"]) * me["t"])
    if mx == "cool-time":
        return [s for s in sp.solve(me["Ta"] + me["D"] * sp.exp(-S(me["k"]) * T) - me["T1"], T) if s.is_real][0]
    if mx == "compose-at":
        return S(me["f"]).subs(X, S(me["g"]).subs(X, me["at"]))
    if mx == "compose":
        return ("same-fn", S(me["f"]).subs(X, S(me["g"])))
    if mx == "log-uv":
        return ("log-uv", sp.log(S(me["N"]), me["b"]), me["b"])
    if mx == "rat-graph":
        num_, den = S(me["num"]), S(me["den"])
        g = sp.gcd(num_, den)
        red_den = sp.cancel(den / g)
        return [sp.solve(g, X)[0], sp.solve(red_den, X)[0], sp.limit(num_ / den, X, sp.oo)]
    if mx == "complex-dist":
        z1, z2 = me["z1"][0] + me["z1"][1] * sp.I, me["z2"][0] + me["z2"][1] * sp.I
        mid = (z1 + z2) / 2
        return [sp.Abs(z1 - z2), sp.re(mid), sp.im(mid)]
    if mx == "vec":
        op = me["op"]
        if op == "comp":
            v = sp.Matrix(me["Qp"]) - sp.Matrix(me["P"])
            return list(v)
        if op == "norm":
            return (me["k"] * sp.Matrix(me["u"])).norm()
        u, v, k = sp.Matrix(me["u"]), sp.Matrix(me["v"]), me["k"]
        return list(u + k * v) if op == "u+kv" else list(k * u - v)
    if mx == "vec-polar":
        s_ = me["m1"] * sp.Matrix([sp.cos(me["a1"] * RAD), sp.sin(me["a1"] * RAD)]) + me["m2"] * sp.Matrix([sp.cos(me["a2"] * RAD), sp.sin(me["a2"] * RAD)])
        ang = float(sp.N(sp.atan2(s_[1], s_[0]) * 180 / sp.pi)) % 360
        return [s_.norm(), ang]
    if mx == "mat":
        A = sp.Matrix(me["A"])
        op = me["op"]
        if op == "Av":
            return list(A * sp.Matrix(me["v"]))
        if op == "AB":
            return list(A * sp.Matrix(me["B"]))
        if op == "kA+B":
            return list(me["k"] * A + sp.Matrix(me["B"]))
        if op == "area":
            unit = sp.Polygon((0, 0), (1, 0), (1, 1), (0, 1))
            img = [A * sp.Matrix(v) for v in [(0, 0), (1, 0), (1, 1), (0, 1)]]
            pts = [sp.Point(m_[0], m_[1]) for m_ in img]
            area = abs(sp.Polygon(*pts).area) if len(set(pts)) == 4 and sp.Polygon(*pts).area != 0 else 0
            return area / abs(unit.area) * me["area"]
        return "Invertible" if A.rank() == 2 else "Not invertible"
    if mx == "geo-transform":
        P = sp.Point(me["x"], me["y"])
        for t in me["ts"]:
            P = [lambda q: q.reflect(sp.Line((0, 0), (1, 0))), lambda q: q.reflect(sp.Line((0, 0), (0, 1))), lambda q: q.reflect(sp.Line((0, 0), (1, 1))),
                 lambda q: q.rotate(sp.pi / 2), lambda q: q.rotate(sp.pi), lambda q: q.rotate(3 * sp.pi / 2), lambda q: q.translate(me["dx"], me["dy"])][t](P)
        return [P.x, P.y]
    if mx == "rot-sym":
        n = me["n"]
        V = [(math.cos(2 * math.pi * j / n), math.sin(2 * math.pi * j / n)) for j in range(n)]

        def maps(f):
            img = [f(v) for v in V]
            return all(any(abs(a_[0] - b[0]) < 1e-9 and abs(a_[1] - b[1]) < 1e-9 for b in V) for a_ in img)
        if me["ask"] == "angle":
            for j in range(1, 4 * n + 1):
                th = 2 * math.pi * j / (4 * n)
                if maps(lambda v: (v[0] * math.cos(th) - v[1] * math.sin(th), v[0] * math.sin(th) + v[1] * math.cos(th))):
                    return Fr(360 * j, 4 * n)
        cnt = 0
        for j in range(2 * n):
            ph = math.pi * j / (2 * n)
            c2, s2 = math.cos(2 * ph), math.sin(2 * ph)
            if maps(lambda v: (v[0] * c2 + v[1] * s2, v[0] * s2 - v[1] * c2)):
                cnt += 1
        return cnt
    if mx == "congruence":
        f = me["facts"]
        sides = [x for x in f if len(x) == 2]
        angs = [x for x in f if len(x) == 1]
        if len(sides) == 3:
            return "SSS"
        if len(sides) == 2:
            shared = set(sides[0]) & set(sides[1])
            return "SAS" if angs and angs[0] in shared else "Not enough information"
        if len(sides) == 1:
            return "ASA" if set(angs) == set(sides[0]) else "AAS"
        return "Not enough information"
    if mx == "angle-pair":
        e1, e2 = S(me["e1"]), S(me["e2"])
        supp = me["pair"] in ("same-side interior", "a linear pair", "consecutive (parallelogram)")
        return sp.solve(e1 + e2 - 180 if supp else e1 - e2, X)[0]
    if mx == "iso-base":
        b = sp.Symbol("b")
        return sp.solve(2 * b + me["v"] - 180, b)[0]
    if mx == "midsegment":
        A, B, C = sp.Point(*me["apex"]), sp.Point(0, 0), sp.Point(me["s"], 0)
        return A.midpoint(B).distance(A.midpoint(C))
    if mx == "diag-bisect":
        x0 = sp.solve(S(me["e1"]) - S(me["e2"]), X)[0]
        return S(me["e1"]).subs(X, x0) + S(me["e2"]).subs(X, x0)
    if mx == "dil-len":
        k = S(me["k"])
        P, Q = sp.Point(0, 0), sp.Point(me["L"], 0)
        return P.scale(k, k).distance(Q.scale(k, k))
    if mx == "dilate":
        k = S(me["k"])
        P2 = sp.Point(*me["P"]).scale(k, k, pt=sp.Point(*me["C"]))
        return [P2.x, P2.y]
    if mx == "similar":
        s = me["s"]
        return S(me["DE"]) / s[0] * s[1]
    if mx == "splitter":
        A, B, C = sp.Point(0, 0), sp.Point(me["ad"] + me["db"], 0), sp.Point(3, 7)
        D = sp.Point(me["ad"], 0)
        E = sp.Line(D, D + (C - B)).intersection(sp.Line(A, C))[0]
        t_ = A.distance(E) / A.distance(C)
        return me["ae"] * (1 - t_) / t_
    if mx == "right-side":
        P = sp.Point(me["h"] * sp.cos(me["A"] * RAD), me["h"] * sp.sin(me["A"] * RAD))
        return P.y if me["fn"] == "opp" else P.x
    if mx == "right-angle":
        return sp.atan2(me["a"], me["b"]) * 180 / sp.pi
    if mx == "cofunction":
        return ("pred", lambda v: 0 < float(v) < 90 and abs(math.sin(me["th"] * math.pi / 180) - math.cos(float(v) * math.pi / 180)) < 1e-12)
    if mx == "trig-ratio":
        a_, b_ = me["legs"]
        P = sp.Point(b_, a_)  # angle at the origin, opposite leg a_
        hyp = sp.Point(0, 0).distance(P)
        return {"sin": P.y / hyp, "cos": P.x / hyp, "tan": P.y / P.x}[me["fn"]]
    if mx == "cyl-mass":
        return S(me["rho"]) * vol_by_slices(lambda z: sp.pi * me["rad"] ** 2, 0, me["h"])
    if mx == "area-sas":
        C = sp.Point(0, 0)
        A = sp.Point(me["b"], 0)
        B = sp.Point(me["a"] * sp.cos(me["C"] * RAD), me["a"] * sp.sin(me["C"] * RAD))
        return abs(sp.Polygon(A, B, C).area)
    if mx == "law-sines":
        A_deg, B_deg = me["A"], me["B"]
        Apt, Bp, Cp = tri_by_angles(me["a"], B_deg, 180 - A_deg - B_deg)
        return math.dist(Apt, Cp)
    if mx == "law-cosines":
        A = sp.Point(0, 0)
        B = sp.Point(me["c"], 0)
        C = sp.Point(me["b"] * sp.cos(me["A"] * RAD), me["b"] * sp.sin(me["A"] * RAD))
        return B.distance(C)
    if mx == "volume":
        t, r_, h, s = me["t"], me["rad"], me["h"], me["s"]
        cyl = vol_by_slices(lambda z: sp.pi * r_ ** 2, 0, h)
        cone = vol_by_slices(lambda z: sp.pi * (r_ * z / h) ** 2, 0, h)
        return {"cylinder": cyl, "cone": cone, "sphere": vol_by_slices(lambda z: sp.pi * (r_ ** 2 - z ** 2), -r_, r_),
                "hemisphere": vol_by_slices(lambda z: sp.pi * (r_ ** 2 - z ** 2), 0, r_), "square pyramid": vol_by_slices(lambda z: (s * z / h) ** 2, 0, h),
                "cone on a cylinder": cyl + cone}[t]
    if mx == "cross":
        return {("a cylinder", "perpendicular to its axis"): "Circle", ("a cylinder", "parallel to its axis (through the axis)"): "Rectangle",
                ("a cone", "perpendicular to its axis"): "Circle", ("a cone", "through its apex, along the axis"): "Triangle",
                ("a cube", "parallel to a face"): "Square", ("a square pyramid", "parallel to the base"): "Square",
                ("a square pyramid", "perpendicular to the base through the apex"): "Triangle", ("a sphere", "through any plane that cuts it"): "Circle"}[(me["solid"], me["cut"])]
    if mx == "rotate-solid":
        return {"rectangle": "Cylinder", "right triangle": "Cone", "semicircle": "Sphere"}[me["shape"]]
    if mx == "par-perp":
        L = sp.Line(sp.Point(0, me["b1"]), sp.Point(1, S(me["m1"]) + me["b1"]))
        P = sp.Point(*me["P"])
        L2 = L.perpendicular_line(P) if me["perp"] else L.parallel_line(P)
        yy = sp.solve(L2.equation(x=X, y=Y), Y)[0]
        return [sp.diff(yy, X), yy.subs(X, 0)]
    if mx == "partition":
        A, B = sp.Point(*me["A"]), sp.Point(*me["B"])
        tt = sp.Symbol("tt", positive=True)
        P = A + (B - A) * tt
        d2 = lambda U, V: (U.x - V.x) ** 2 + (U.y - V.y) ** 2
        sol = [s for s in sp.solve(me["b"] ** 2 * d2(A, P) - me["a"] ** 2 * d2(B, P), tt) if 0 < s < 1][0]
        P = A + (B - A) * sol
        return [P.x, P.y]
    if mx == "polygon":
        poly_ = sp.Polygon(*[sp.Point(*v) for v in me["V"]])
        return poly_.perimeter if me["ask"] == "perimeter" else abs(poly_.area)
    if mx == "quad-class":
        A, B, C, D = [sp.Point(*v) for v in me["V"]]
        if A.midpoint(C) != B.midpoint(D):
            return "Not a parallelogram"
        return "Rectangle" if A.distance(C) == B.distance(D) else "Parallelogram (not a rectangle)"
    if mx == "parabola":
        fx, fy, dy = S(me["F"][0]), S(me["F"][1]), S(me["dy"])
        yy = sp.solve((X - fx) ** 2 + (Y - fy) ** 2 - (Y - dy) ** 2, Y)[0]
        h = sp.solve(sp.diff(yy, X), X)[0]
        return [sp.Poly(sp.expand(yy), X).coeff_monomial(X ** 2), h, yy.subs(X, h)]
    if mx == "inscribed":
        arc = me["arc"]
        A, B, P = circ(0), circ(arc), circ(arc + (360 - arc) / 2)
        return angle_at(P, A, B)
    if mx == "thales":
        # chord from A(-1, 0) at angle k meets the unit circle again at C
        k = math.radians(me["k"])
        tt = 2 * math.cos(k)  # |A + t d|^2 = 1  ->  t^2 - 2t cos k = 0
        A, B, C = (-1.0, 0.0), (1.0, 0.0), (-1 + tt * math.cos(k), tt * math.sin(k))
        return angle_at(B, C, A)
    if mx == "cyclic":
        A_, B_ = me["A"], me["B"]
        t_ = max(1, 2 * A_ + 2 * B_ - 360 + 1)
        a2, a3, a4 = 2 * A_ - t_, t_, 2 * B_ - t_
        a1 = 360 - a2 - a3 - a4
        assert min(a1, a2, a3, a4) > 0
        # vertices A, B, C, D in order; arcs AB = a1, BC = a2, CD = a3, DA = a4
        PA, PB, PC, PD = circ(0), circ(a1), circ(a1 + a2), circ(a1 + a2 + a3)
        assert abs(angle_at(PA, PB, PD) - A_) < 1e-9 and abs(angle_at(PB, PA, PC) - B_) < 1e-9
        return angle_at(PC, PB, PD)
    if mx == "arc":
        th = sp.Symbol("th")
        lim = sp.Rational(me["d"]) * RAD
        if me["sector"]:
            rho = sp.Symbol("rho")
            return sp.integrate(sp.integrate(rho, (rho, 0, me["rad"])), (th, 0, lim))
        return sp.integrate(me["rad"], (th, 0, lim))
    if mx == "circle-eq":
        f = X ** 2 + Y ** 2 + me["D"] * X + me["E"] * Y + me["F"]
        c = sp.solve([sp.diff(f, X), sp.diff(f, Y)], [X, Y])  # the centre minimises f
        return [c[X], c[Y], sp.sqrt(-f.subs(c))]
    if mx == "on-circle":
        C, P, Q = (sp.Point(*v) for v in (me["C"], me["P"], me["Q"]))
        r_, d = C.distance(P), C.distance(Q)
        return "On the circle" if d == r_ else "Inside" if d < r_ else "Outside"
    if mx == "conic":
        return ("conic", me["ell"], me["F"], me["s"])
    if mx == "to-rad":
        return sp.rad(me["d"])
    if mx == "to-deg":
        return sp.deg(S(me["rad"]) * sp.pi)
    if mx == "trig-exact":
        return {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[me["fn"]](me["d"] * RAD)
    if mx == "pyth-id":
        g = S(me["gv"])
        quad = me["quad"]
        base = sp.asin(g) if me["given"] == "sin" else sp.acos(g)
        cands = [base, sp.pi - base, -base, base + 2 * sp.pi, sp.pi + base, 2 * sp.pi - base] if me["given"] == "sin" else [base, -base, 2 * sp.pi - base, base + 2 * sp.pi]
        th = [c for c in cands if (float(sp.N(c)) % (2 * math.pi)) // (math.pi / 2) == quad - 1][0]
        return {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[me["want"]](th)
    if mx == "sinusoid":
        e = S(me["e"])
        P = sp.periodicity(e, X)
        span = sp.Interval(0, P)
        hi, lo = sp.calculus.util.maximum(e, X, span), sp.calculus.util.minimum(e, X, span)
        return [(hi - lo) / 2, P, (hi + lo) / 2]
    if mx == "sin-model":
        return ("sin-model", me["lo"], me["hi"], me["P"])
    if mx == "trig-sym":
        v = S(me["v"])
        th = sp.asin(v) if me["given"] == "sin" else sp.acos(v)
        return sp.nsimplify(sp.N(S(me["expr"], {"t": th}), 50), rational=True)
    if mx == "sum-formula":
        al, be = sp.asin(S(me["sa"])), sp.acos(S(me["cb"]))
        return {"sin(a+b)": sp.sin(al + be), "cos(a-b)": sp.cos(al - be), "sin(2a)": sp.sin(2 * al)}[me["which"]]
    if mx == "center":
        xs, t = me["xs"], me["t"]
        if t == "mean":
            return sp.Rational(sum(xs), len(xs))
        if t == "median":
            return sp.nsimplify(statistics.median(xs))
        if t == "IQR":
            q1, q3 = halves_quartiles(xs)
            return sp.Rational(q3 - q1)
        return statistics.pstdev(xs)
    if mx in ("fence", "is-outlier"):
        q1, q3 = halves_quartiles(me["xs"])
        fence = q3 + Fr(3, 2) * (q3 - q1)
        if mx == "fence":
            return sp.Rational(fence)
        return "Outlier" if me["v"] > fence else "Not an outlier"
    if mx == "two-way-hs":
        t, i, j = me["t"], me["i"], me["j"]
        tot = sum(sum(r_) for r_ in t)
        return [Fr(t[i][j], tot), Fr(t[0][j] + t[1][j], tot), Fr(t[i][j], sum(t[i]))][me["kind"]]
    if mx in ("lsq", "lsq-pred"):
        m_, b_ = sp.symbols("m_ b_")
        sse = sum((y - (m_ * x + b_)) ** 2 for x, y in zip(me["xs"], me["ys"]))
        sol = sp.solve([sp.diff(sse, m_), sp.diff(sse, b_)], [m_, b_])
        return [sol[m_], sol[b_]] if mx == "lsq" else sol[m_] * me["x0"] + sol[b_]
    if mx == "residual":
        return me["y"] - (S(me["m"]) * me["x"] + me["b"])
    if mx == "corr":
        xs, ys = me["xs"], me["ys"]
        mx_, my_ = statistics.mean(xs), statistics.mean(ys)
        return sum((a_ - mx_) * (b - my_) for a_, b in zip(xs, ys)) / math.sqrt(sum((a_ - mx_) ** 2 for a_ in xs) * sum((b - my_) ** 2 for b in ys))
    if mx == "zscore":
        return (S(me["x"]) - me["mu"]) / me["sd"]
    if mx == "empirical":
        cdf = lambda v: (1 + math.erf((v - me["mu"]) / (me["sd"] * math.sqrt(2)))) / 2
        hi = 1.0 if me["hi"] is None else cdf(me["hi"])
        return ("approx", 100 * (hi - cdf(me["lo"])), 0.6)
    if mx == "margin":
        n, k = me["n"], me["k"]
        p_ = k / n
        var = sum((j / n - p_) ** 2 * math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) + j * math.log(p_) + (n - j) * math.log(1 - p_)) for j in range(n + 1))
        return 200 * math.sqrt(var)
    if mx == "cards-or":
        D = deck()
        hit = [c for c in D if c[1] == me["suit"] or (c[0] in ("jack", "queen", "king") if me["other"] == "face" else c[0] == me["other"])]
        return Fr(len(hit), len(D))
    if mx == "die-or":
        return Fr(sum(1 for d in range(1, 7) if d % 2 == 0 or d > me["k"]), 6)
    if mx == "dice-cond":
        outs = list(itertools.product(range(1, 7), repeat=2))
        c = me["cond"]
        B = [o for o in outs if (o[0] % 2 == 0 if "even" in c else 3 in o if "3" in c else o[0] < 4 if "less" in c else o[0] == o[1])]
        return Fr(sum(1 for o in B if sum(o) == me["s"]), len(B))
    if mx == "cond-prob":
        return S(me["pab"]) / S(me["pb"])
    if mx == "independent":
        return "Independent" if S(me["pab"]) == S(me["pa"]) * S(me["pb"]) else "Not independent"
    if mx == "draw-all-red":
        bag = ["r"] * me["red"] + ["b"] * me["blue"]
        draws = list(itertools.product(range(len(bag)), repeat=me["k"])) if me["with"] else list(itertools.permutations(range(len(bag)), me["k"]))
        return Fr(sum(1 for d in draws if all(bag[i] == "r" for i in d)), len(draws))
    if mx == "committee":
        people = ["w"] * me["w"] + ["m"] * (me["n"] - me["w"])
        cs = list(itertools.combinations(range(me["n"]), me["k"]))
        return Fr(sum(1 for c in cs if all(people[i] == "w" for i in c)), len(cs))
    if mx == "bayes":
        pop = 1000000
        sick = S(me["prev"]) * pop
        tp, fp = sick * S(me["sens"]), (pop - sick) * (1 - S(me["spec"]))
        return tp / (tp + fp)
    if mx == "ev":
        return sum(x * S(p_) for x, p_ in zip(me["xs"], me["ps"]))
    if mx == "guess":
        n, pr = me["n"], Fr(1, me["k"])
        return sum(j * math.comb(n, j) * pr ** j * (1 - pr) ** (n - j) for j in range(n + 1))
    if mx == "game":
        w = S(me["win"])
        return w * (me["prize"] - me["cost"]) + (1 - w) * (-me["cost"])
    if mx == "insurance":
        pr = S(me["pr"])
        a_, b_ = me["pA"] + pr * me["dA"], me["pB"] + pr * me["dB"]
        return "Plan A" if a_ < b_ else "Plan B"
    raise KeyError(mx)


def check_one(p):
    exp = expected(p)
    got = ans(p)
    a = p["answer"]
    tol = rel_tol(p)
    if isinstance(exp, tuple):
        tag = exp[0]
        if tag == "set":
            return same_set(got, exp[1])
        if tag == "seq":
            return all(close(got.subs(N, i + 1), exp[1][i]) for i in range(8))
        if tag == "same-expr":
            names = set(re.findall(r"[A-Za-z]+", a["ref"])) - {"pi"}
            ref = S(a["ref"], {nm: exp[2].get(nm, sp.Symbol(nm)) for nm in names})
            return sp.simplify(ref - exp[1]) == 0
        if tag == "same-fn":
            return sp.simplify(got - exp[1]) == 0 or all(close(got.subs(X, v), exp[1].subs(X, v)) for v in (0.3, 1.1, 2.7, -1.6, 4.2))
        if tag == "inverse":
            f = exp[1]
            return all(close(f.subs(X, got.subs(X, v)), v) and close(got.subs(X, f.subs(X, v)), v) for v in (sp.Rational(3, 7), sp.Rational(9, 5), sp.Rational(13, 4)))
        if tag == "pred":
            return exp[1](got)
        if tag == "log-uv":
            b = exp[2]
            return close(got.subs({sp.Symbol("u"): sp.log(2, b), sp.Symbol("v"): sp.log(3, b)}), exp[1])
        if tag == "approx":
            return abs(float(got) - exp[1]) <= exp[2]
        if tag == "sin-model":
            A, B, k = got
            f = lambda v: float(sp.N(A * sp.sin(B * v) + k))
            lo, hi, P = exp[1], exp[2], exp[3]
            ys = [f(P * i / 400) for i in range(401)]
            return abs(max(ys) - hi) < 1e-9 and abs(min(ys) - lo) < 1e-9 and abs(f(0.37) - f(0.37 + P)) < 1e-9 and abs(f(0.37) - f(0.37 + P / 2)) > 1e-6
        if tag == "conic":
            _, ell, F, s = exp
            pp, qq = got
            pts = [(math.sqrt(pp) * math.cos(t_), math.sqrt(qq) * math.sin(t_)) if ell else (math.sqrt(pp) * math.cosh(t_), math.sqrt(qq) * math.sinh(t_)) for t_ in (0.2, 0.9, 1.7, 2.5)]
            d = lambda P, f: math.hypot(P[0] - f, P[1])
            return all(abs((d(P, F) + d(P, -F)) - s) < 1e-9 if ell else abs(abs(d(P, F) - d(P, -F)) - s) < 1e-9 for P in pts)
        raise KeyError(tag)
    if isinstance(exp, str):
        return got == exp
    if isinstance(exp, list):
        return len(exp) == len(got) and all(close(g, sp.nsimplify(e) if isinstance(e, Fr) else e, max(tol, 1e-9 if a["kind"] == "tuple" and any(f["mode"] == "number" for f in a["fields"]) else tol)) for g, e in zip(got, exp))
    if isinstance(exp, Fr):
        exp = sp.Rational(exp.numerator, exp.denominator)
    return close(got, exp, tol)


PREFIX = ("alg-", "geo-", "trig-", "stats-")


def check(p, H):
    me = p.get("meta") or {}
    if "mx" not in me or not str(p.get("template", "")).startswith(PREFIX):
        return None
    return check_one(p)
