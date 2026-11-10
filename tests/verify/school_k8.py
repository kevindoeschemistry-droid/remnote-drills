"""
K–8 mathematics (gen-k8.ts) — every answer recomputed from the problem's inputs with
exact arithmetic (fractions.Fraction, decimal.Decimal, sympy) or brute force, sharing no
code with the generator:

  arithmetic       the stated expression evaluated exactly by sympy (meta.e), or the
                   answer substituted into the stated equation (meta.eq) and the equation
                   tested; comparisons by Fraction
  place value      digit position read off the numeral's string; rounding by Decimal
                   ROUND_HALF_UP; repeating decimals via a long Decimal expansion and
                   Fraction.limit_denominator
  measurement      unit conversions from an independent table; L-shapes, boxes and surface
                   areas by counting unit squares / cubes / exposed faces; clock times by
                   datetime
  geometry         polygon areas by the shoelace formula on the vertices; circles and
                   solids by integrating (sympy); transformations with sympy Point;
                   right triangles from the angle opposite the longest side
  algebra          equations and inequalities solved by sympy; systems by linsolve;
                   equivalence by simplify
  data/probability enumeration of outcomes with itertools; statistics module for centre;
                   quartiles as medians of the halves
"""
import itertools
import math
import statistics
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction as Fr

import sympy as sp

X = sp.Symbol("x")
LOC = {"x": X, "sqrt": sp.sqrt, "abs": sp.Abs, "pi": sp.pi}


def S(s):
    return sp.sympify(str(s), locals=LOC, rational=True)


def ans_val(a):
    return S(str(a).replace("^", "**"))


def same(u, v, tol=1e-12):
    u, v = sp.nsimplify(u) if not isinstance(u, sp.Basic) else u, v
    d = complex(sp.N(sp.sympify(u) - sp.sympify(v), 50))
    scale = max(1.0, abs(complex(sp.N(v, 30))))
    return abs(d) <= tol * scale


def eq_holds(eq, val):
    for part in eq.split(" and "):
        s = part.replace("?", f"({val})")
        for op in ("==", ">=", "<=", ">", "<"):
            if op in s:
                lhs, rhs = s.split(op, 1)
                L, R = S(lhs), S(rhs)
                ok = {"==": sp.simplify(L - R) == 0, ">=": L >= R, "<=": L <= R, ">": L > R, "<": L < R}[op]
                if not bool(ok):
                    return False
                break
        else:
            raise ValueError(part)
    return True


def answer(p):
    a = p["answer"]
    if a["kind"] == "expression":
        return ans_val(a["ref"])
    if a["kind"] == "choice":
        return a["correct"]
    if a["kind"] == "tuple":
        return [ans_val(f["ref"]) for f in a["fields"]]
    raise KeyError(a["kind"])


def tol_of(p):
    a = p["answer"]
    return 1e-9 if a.get("rel") else 1e-12


# ── independent tables ─────────────────────────────────────────────────────
SHAPE = {("triangle", "sides"): 3, ("triangle", "vertices"): 3, ("square", "corners"): 4, ("rectangle", "sides"): 4,
         ("pentagon", "sides"): 5, ("hexagon", "vertices"): 6, ("octagon", "sides"): 8, ("cube", "faces"): 6,
         ("cube", "edges"): 12, ("cube", "vertices"): 8, ("quadrilateral", "sides"): 4, ("rectangular prism", "faces"): 6}
BASE = {"km": (Fr(1000), "m"), "m": (Fr(1), "m"), "cm": (Fr(1, 100), "m"), "mm": (Fr(1, 1000), "m"),
        "kg": (Fr(1000), "g"), "g": (Fr(1), "g"), "L": (Fr(1000), "mL"), "mL": (Fr(1), "mL"),
        "ft": (Fr(12), "in"), "in": (Fr(1), "in"), "yd": (Fr(36), "in"), "lb": (Fr(16), "oz"), "oz": (Fr(1), "oz"),
        "h": (Fr(3600), "s"), "min": (Fr(60), "s"), "s": (Fr(1), "s"), "gal": (Fr(4), "qt"), "qt": (Fr(1), "qt")}
SYM_LINES = {"square": 4, "rectangle (not a square)": 2, "equilateral triangle": 3, "isosceles triangle (not equilateral)": 1,
             "regular pentagon": 5, "regular hexagon": 6, "parallelogram (not a rectangle or rhombus)": 0, "rhombus (not a square)": 2,
             "regular octagon": 8, "scalene triangle": 0}
# properties: (4 right angles, 4 equal sides, 2 pairs parallel, quadrilateral, ≥2 equal sides (tri), 3 equal sides (tri))
PROPS = {"square": {"quad", "par2", "right4", "eq4"}, "rectangle": {"quad", "par2", "right4"}, "rhombus": {"quad", "par2", "eq4"},
         "parallelogram": {"quad", "par2"}, "quadrilateral": {"quad"}, "trapezoid (exactly one pair of parallel sides)": {"quad", "par1"},
         "equilateral triangle": {"tri", "eq2", "eq3"}, "isosceles triangle": {"tri", "eq2"}}
PHRASE = {"at least": ">=", "at most": "<=", "more than": ">", "fewer than": "<", "no more than": "<=", "no fewer than": ">="}
SYMBOL = {"≥": ">=", "≤": "<=", ">": ">", "<": "<"}


def quartile_halves(xs):
    s = sorted(xs)
    n = len(s)
    lo, hi = s[: n // 2], s[(n + 1) // 2:]
    return Fr(statistics.median(lo)).limit_denominator(4), Fr(statistics.median(hi)).limit_denominator(4)


def voxels_box(dims, off=(0, 0, 0)):
    return {(off[0] + i, off[1] + j, off[2] + k) for i in range(dims[0]) for j in range(dims[1]) for k in range(dims[2])}


def exposed_faces(cells):
    n = 0
    for (i, j, k) in cells:
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (i + d[0], j + d[1], k + d[2]) not in cells:
                n += 1
    return n


def shoelace(vs):
    return abs(sp.Polygon(*[sp.Point(*v) for v in vs]).area)


def story(t, a, b):
    return {"add-result": a + b, "add-change": b - a, "add-start": b - a, "take-result": a - b, "take-change": a - b,
            "compare-diff": a - b, "compare-bigger": a + b, "groups-total": a * b, "share-each": Fr(a, b),
            "share-groups": Fr(a, b), "times": a * b, "times-part": Fr(a, b)}[t]


def expected(p):
    """The correct answer, recomputed. Returns a value, a list, an option string, or a predicate."""
    me = p["meta"]
    mx = me["mx"]
    a = p["answer"]
    if mx == "expr":
        return S(me["e"])
    if mx == "exprs":
        return [S(e) for e in me["es"]]
    if mx == "eq":
        return lambda v: eq_holds(me["eq"], v)
    if mx == "cmp":
        u, v = S(me["a"]), S(me["b"])
        return "=" if u == v else ">" if u > v else "<"
    if mx == "count-on":
        return list(range(me["n"], me["n"] + me["k"] + 1))[-1]
    if mx == "count-by":
        seq, s = me["seq"], me["s"]
        assert all(y - x == s for x, y in zip(seq, seq[1:]))
        return seq[-1] + s
    if mx == "tens-ones":
        d = str(me["n"])
        return [int(d[0]), int(d[1])]
    if mx == "digit-value":
        s, i = me["s"], me["i"]
        intlen = len(s.split(".")[0])
        digits = s.replace(".", "")
        return int(digits[i]) * Fr(10) ** (intlen - 1 - i)
    if mx == "round":
        unit = Decimal(10) ** me["t"]
        return S(str((Decimal(me["s"]) / unit).quantize(Decimal(1), rounding=ROUND_HALF_UP) * unit))
    if mx == "tf":
        return "True" if S(me["l"]) == S(me["r"]) else "False"
    if mx == "even-odd":
        return "Even" if me["n"] % 2 == 0 else "Odd"
    if mx == "story":
        return story(me["type"], me["a"], me["b"])
    if mx == "story2":
        return me["a"] * me["b"] + (me["c"] if me["plus"] else -me["c"])
    if mx == "rem":
        n, per = me["n"], me["per"]
        return [-(-n // per), n // per, n % per][me["t"]]
    if mx == "divmod":
        n, d = me["n"], me["d"]
        qt = 0
        while n - (qt + 1) * d >= 0:
            qt += 1
        return [qt, n - qt * d]
    if mx == "prime":
        return "Prime" if sp.isprime(me["n"]) else "Composite"
    if mx == "nfactors":
        return sp.divisor_count(me["n"])
    if mx == "pattern":
        v = me["a"]
        for _ in range(me["k"] - 1):
            v = 2 * v if me["mul"] else v + me["d"]
        return v
    if mx == "two-patterns":
        A = [me["a"] * i for i in range(me["k"])]
        B = [me["b"] * i for i in range(me["k"])]
        return [A[-1], B[-1]]
    if mx == "shape":
        return SHAPE[(me["s"], me["what"])]
    if mx == "elapsed":
        t1 = datetime(2026, 1, 1, me["h1"], me["m1"])
        t2 = datetime(2026, 1, 1, me["h2"], me["m2"])
        return int((t2 - t1).total_seconds() // 60)
    if mx == "time-after":
        t = datetime(2026, 1, 1, me["h"], me["mm"]) + timedelta(minutes=me["add"])
        return [int(t.strftime("%I")), t.minute]
    if mx == "money":
        return sum(c * v for c, v in zip(me["cnt"], (25, 10, 5, 1))) + 100 * me["dollars"]
    if mx == "convert":
        f1, u1 = BASE[me["from"]]
        f2, u2 = BASE[me["to"]]
        assert u1 == u2
        return Fr(me["x"]) * f1 / f2
    if mx == "rect":
        return me["l"] * me["w"] if me["ask"] == "area" else Fr(me["A"], me["l"])
    if mx == "lshape":
        W, H, w, h = me["W"], me["H"], me["w"], me["h"]
        return sum(1 for i in range(W) for j in range(H) if not (i >= W - w and j >= H - h))
    if mx == "angle-type":
        x = me["a"]
        return "Acute" if 0 < x < 90 else "Right" if x == 90 else "Obtuse" if x < 180 else "Straight"
    if mx == "sym-lines":
        return SYM_LINES[me["s"]]
    if mx == "hier":
        need = PROPS[me["b"]] - {"par1"}
        have = PROPS[me["a"]]
        return "True" if need <= have and not ("par1" in PROPS[me["b"]] and "par2" in have) else "False"
    if mx == "box":
        v = Fr(1)
        for d in me["dims"]:
            v *= Fr(d)
        return v
    if mx == "two-boxes":
        cells = voxels_box(me["a"]) | voxels_box(me["b"], (100, 0, 0))
        return len(cells)
    if mx == "box-sa":
        return exposed_faces(voxels_box((me["l"], me["w"], me["h"])))
    if mx == "graph":
        c = me["counts"]
        return sum(c) if me["ask"] == 0 else abs(c[me["i"]] - c[me["j"]])
    if mx == "lineplot":
        xs = [Fr(x) for x in me["xs"]]
        return sum(xs) / len(xs) if me["redistribute"] else max(xs) - min(xs)
    if mx == "ratio":
        return Fr(me["b"]) * me["x"] / me["a"]
    if mx == "prop":
        rs = {Fr(y) / x for x, y in zip(me["xs"], me["ys"])}
        return "Proportional" if len(rs) == 1 else "Not proportional"
    if mx == "quadrant":
        x, y = me["x"], me["y"]
        return {(1, 1): "I", (-1, 1): "II", (-1, -1): "III", (1, -1): "IV"}[(int(math.copysign(1, x)), int(math.copysign(1, y)))]
    if mx == "reflect":
        P = sp.Point(me["x"], me["y"])
        line = sp.Line((0, 0), (1, 0)) if me["ax"] == "x" else sp.Line((0, 0), (0, 1))
        Q = P.reflect(line)
        return [Q.x, Q.y]
    if mx == "dist":
        return sp.Point(*me["p"]).distance(sp.Point(*me["q"]))
    if mx == "lcm":
        k = 1
        while k % me["a"] or k % me["b"]:
            k += 1
        return k
    if mx == "gcf":
        return max(d for d in range(1, min(me["a"], me["b"]) + 1) if me["a"] % d == 0 and me["b"] % d == 0)
    if mx == "lin-form":
        P = sp.Poly(sp.expand(S(me["e"])), X)
        return [P.coeff_monomial(X), P.coeff_monomial(1)]
    if mx == "equiv":
        return "Equivalent" if sp.simplify(S(me["l"]) - S(me["r"])) == 0 else "Not equivalent"
    if mx == "coef":
        return sp.Poly(S(me["e"]), X).coeff_monomial(X ** me["p"])
    if mx == "solve":
        sols = sp.solve(S(me["eq"]), X)
        assert len(sols) == 1
        return sols[0]
    if mx == "which-solves":
        good = [o for o in a["options"] if sp.simplify(S(me["eq"]).subs(X, S(o))) == 0]
        assert len(good) == 1
        return good[0]
    if mx == "phrase":
        rel = PHRASE[me["ph"]]
        return next(o for o in a["options"] if SYMBOL[o.split()[1]] == rel)
    if mx == "ineq":
        e, rhs = S(me["e"]), S(me["rhs"])
        sol = sp.solve_univariate_inequality(e > rhs if me["rel"] == ">" else e < rhs, X, relational=False)
        for o in a["options"]:
            _, op, b = o.split()
            cand = sp.Interval.open(S(b), sp.oo) if op == ">" else sp.Interval.open(-sp.oo, S(b))
            if cand == sol:
                return o
        return None
    if mx == "isqrt":
        return math.isqrt(me["n"])
    if mx == "nsol":
        s = sp.solveset(sp.Eq(S(me["l"]), S(me["r"])), X, sp.S.Reals)
        return "No solution" if s == sp.S.EmptySet else "Infinitely many solutions" if s == sp.S.Reals else "One solution"
    if mx == "system":
        (a1, b1, c1), (a2, b2, c2) = me["rows"]
        y = sp.Symbol("y")
        (sol,) = sp.linsolve([a1 * X + b1 * y - c1, a2 * X + b2 * y - c2], [X, y])
        return list(sol)
    if mx == "tickets":
        A, C = sp.symbols("A C")
        sol = sp.solve([A + C - me["n"], me["pa"] * A + me["pc"] * C - me["total"]], [A, C])
        return [sol[A], sol[C]]
    if mx in ("slope", "line"):
        (x1, y1), (x2, y2) = me["p"], me["q"]
        L = sp.Line(sp.Point(x1, y1), sp.Point(x2, y2))
        m_ = L.slope
        return m_ if mx == "slope" else [m_, sp.solve(L.equation(x=X, y=sp.Symbol("y")).subs(X, 0), sp.Symbol("y"))[0]]
    if mx == "is-fn":
        seen = {}
        for x, y in me["pairs"]:
            if seen.setdefault(x, y) != y:
                return "Not a function"
        return "Function"
    if mx == "linear":
        e = S(me["e"])
        return "Linear" if e.is_polynomial(X) and sp.degree(e, X) <= 1 else "Not linear"
    if mx == "cmp-rate":
        pts = me["pts"]
        rates = {Fr(y2 - y1, x2 - x1) for (x1, y1), (x2, y2) in zip(pts, pts[1:])}
        assert len(rates) == 1
        g = rates.pop()
        return "Same" if g == me["f"] else "f" if me["f"] > g else "g"
    if mx == "shoelace":
        return shoelace(me["verts"])
    if mx == "circle":
        r_, th, rho = me["rad"], sp.Symbol("th"), sp.Symbol("rho")
        if me["area"]:
            return sp.integrate(sp.integrate(rho, (rho, 0, r_)), (th, 0, 2 * sp.pi))
        return sp.integrate(r_, (th, 0, 2 * sp.pi))  # arc length of (r cos θ, r sin θ)
    if mx == "tri-prism":
        return shoelace(me["tri"]) * me["L"]
    if mx == "transform":
        P = sp.Point(me["x"], me["y"])
        t = me["t"]
        Q = {"translate": lambda: P.translate(me["dx"], me["dy"]), "reflect-x": lambda: P.reflect(sp.Line((0, 0), (1, 0))),
             "reflect-y": lambda: P.reflect(sp.Line((0, 0), (0, 1))), "rot90": lambda: P.rotate(sp.pi / 2),
             "rot180": lambda: P.rotate(sp.pi), "dilate": lambda: P.scale(S(me["k"]), S(me["k"]))}[t]()
        return [Q.x, Q.y]
    if mx == "is-right":
        a_, b_, c_ = sorted(me["sides"])
        ang = sp.acos(sp.Rational(a_ ** 2 + b_ ** 2 - c_ ** 2, 2 * a_ * b_))
        return "Right triangle" if sp.simplify(ang - sp.pi / 2) == 0 else "Not a right triangle"
    if mx == "diag3":
        return sp.Point3D(0, 0, 0).distance(sp.Point3D(*me["dims"]))
    if mx == "solid":
        r_, h, z = me["rad"], me["h"], sp.Symbol("z")
        if me["t"] == "cylinder":
            return sp.integrate(sp.pi * r_ ** 2, (z, 0, h))
        if me["t"] == "cone":
            return sp.integrate(sp.pi * (r_ * z / h) ** 2, (z, 0, h))
        return sp.integrate(sp.pi * (r_ ** 2 - z ** 2), (z, -r_, r_))
    if mx == "stat":
        xs, t = me["xs"], me["t"]
        if t == "mean":
            return Fr(statistics.mean(Fr(x) for x in xs))
        if t == "median":
            return Fr(statistics.median(xs)).limit_denominator(2)
        if t == "range":
            return max(xs) - min(xs)
        if t == "IQR":
            q1, q3 = quartile_halves(xs)
            return q3 - q1
        mu = Fr(sum(xs), len(xs))
        return sum(abs(x - mu) for x in xs) / len(xs)
    if mx == "bag":
        marbles = [k for k, c in enumerate(me["cnt"]) for _ in range(c)]
        return Fr(sum(1 for k in marbles if k == me["i"]), len(marbles))
    if mx == "likely":
        pr = Fr(me["k"], me["tot"])
        return "Impossible" if pr == 0 else "Certain" if pr == 1 else "Equally likely as not" if pr == Fr(1, 2) else "Unlikely" if pr < Fr(1, 2) else "Likely"
    if mx == "predict":
        return me["n"] * Fr(1, me["sides"])
    if mx == "dice-sum":
        outs = list(itertools.product(range(1, 7), repeat=2))
        return Fr(sum(1 for o in outs if sum(o) == me["s"]), len(outs))
    if mx == "coins":
        outs = list(itertools.product("HT", repeat=me["n"]))
        return Fr(sum(1 for o in outs if o.count("H") == me["k"]), len(outs))
    if mx == "coin-die":
        outs = list(itertools.product("HT", range(1, 7)))
        return Fr(sum(1 for c, d in outs if c == "H" and d >= me["d"]), len(outs))
    if mx == "sample":
        return Fr(me["k"], me["n"]) * me["N"]
    if mx == "two-way":
        row = me["t"][me["row"]]
        return Fr(row[me["col"]], sum(row))
    if mx == "scaling":
        f, n = Fr(me["f"]), me["n"]
        return f"greater than {n}" if f * n > n else f"less than {n}" if f * n < n else f"equal to {n}"
    if mx == "terminates":
        n, d, seen = me["n"], me["d"], set()
        r = n % d
        while r and r not in seen:
            seen.add(r)
            r = (r * 10) % d
        return "Terminates" if r == 0 else "Repeats"
    if mx == "dec-digit":
        getcontext().prec = 60
        s = str(Decimal(me["n"]) / Decimal(me["d"]))
        return int((s.split(".")[1] + "0" * 60)[me["k"] - 1])
    if mx == "repeating":
        v = Fr(Decimal("0." + me["block"] * 30)).limit_denominator(1000)
        return [v.numerator, v.denominator]
    raise KeyError(mx)


def compare(p, exp):
    got = answer(p)
    tol = tol_of(p)
    if callable(exp):
        return exp(p["answer"]["ref"])
    if isinstance(exp, list):
        return len(exp) == len(got) and all(same(g, sp.nsimplify(e) if isinstance(e, Fr) else e, 1e-12) for g, e in zip(got, exp))
    if isinstance(exp, str):
        return got == exp
    e = sp.Rational(exp.numerator, exp.denominator) if isinstance(exp, Fr) else exp
    return same(got, e, tol)


def check(p, H):
    me = p.get("meta") or {}
    if "mx" not in me or not str(p.get("template", "")).startswith("k8-"):
        return None
    return compare(p, expected(p))
