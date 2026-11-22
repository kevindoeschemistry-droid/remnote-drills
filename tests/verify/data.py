"""Problems as data (drills/problems/*.yaml): the generic verifier.

Each template's `verify` block is solved here from the problem's givens alone; nothing in it is
the generator's formula. For every part, the value the generator claims must match.

  ode        the governing equation in T(var); dsolve gives the general solution
  bcs        "lhs = rhs" with T(v), dT(v) = T'(v), lim0(e) = limit var -> 0+; fixes the constants
  expect     label -> expression in the solved T, dT and the givens; must equal the part's value
  choices    label -> expression giving the 0-based index of the right option
  (a part may be symbolic: its reference is an expression in var, compared at sample points)
  residuals  balances that must vanish (part labels stand for the claimed values); a residual
             with the variable left in must vanish at every point
"""
import json
import random
from pathlib import Path

import functools
import sympy as sp

_GEN = Path(__file__).resolve().parents[2] / "src/drills/skills.generated.json"
TEMPLATES = {t["template"]: t for t in json.loads(_GEN.read_text()).get("problems", [])}

BASE = {"diff": sp.diff, "pi": sp.pi, "log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt, "Abs": sp.Abs,
        "solve": sp.solve, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "tanh": sp.tanh, "cosh": sp.cosh, "sinh": sp.sinh,
        "integrate": sp.integrate, "limit": sp.limit, "oo": sp.oo, "atan": sp.atan, "asin": sp.asin, "acos": sp.acos,
        "sec": sp.sec, "csc": sp.csc, "cot": sp.cot, "Rational": sp.Rational, "Symbol": sp.Symbol, "Eq": sp.Eq,
        "Min": sp.Min, "Max": sp.Max, "Sum": sp.Sum, "sum": sum, "range": range, "all": all, "any": any, "sorted": sorted, "len": len, "legendre": sp.legendre, "I": sp.I, "re": sp.re, "im": sp.im, "Y": sp.Symbol("y"), "Z": sp.Symbol("z"), "acos": sp.acos, "nn": sp.Symbol("n", integer=True, positive=True), "series": sp.series, "summation": sp.summation, "Matrix": sp.Matrix, "factorial": sp.factorial, "gcd": sp.gcd, "lcm": sp.lcm, "divisors": sp.divisors, "binomial": sp.binomial, "floor": sp.floor, "interpolate": sp.interpolate, "jzero": lambda order, k: sp.Float(__import__("mpmath").besseljzero(order, k), 12)}

# CODATA 2022 (exact SI values where the SI fixes them) and standard atomic weights, transcribed here
# independently of the templates: an anchor item's own numbers are checked against these.
CONST = {"c_kB": sp.Rational("1.380649e-23"), "c_NA": sp.Rational("6.02214076e23"), "c_h": sp.Rational("6.62607015e-34"),
         "c_c": sp.Integer(299792458), "c_e": sp.Rational("1.602176634e-19"), "c_Eh": sp.Rational("4.3597447222060e-18"),
         "c_me": sp.Rational("9.1093837015e-31"), "c_cal": sp.Rational("4.184"), "c_atm": sp.Integer(101325),
         "c_M": {"H": sp.Rational("1.008"), "C": sp.Rational("12.011"), "N": sp.Rational("14.007"), "O": sp.Rational("15.999"),
                 "Na": sp.Rational("22.990"), "P": sp.Rational("30.974"), "S": sp.Rational("32.06"), "Cl": sp.Rational("35.45"),
                 "K": sp.Rational("39.098"), "Ca": sp.Rational("40.078"), "Fe": sp.Rational("55.845")}}
CONST["c_R"] = CONST["c_kB"] * CONST["c_NA"]
BASE.update(CONST)
BASE.update({"Integer": sp.Integer, "nsimplify": sp.nsimplify, "expand": sp.expand, "powsimp": sp.powsimp, "simplify": sp.simplify, "idiff": sp.idiff, "erf": sp.erf, "erfc": sp.erfc, "atan2": sp.atan2, "arg": sp.arg, "ceiling": sp.ceiling})
# calc("c_R*298.15/1000"): evaluate a case's own formula string against the constants above
BASE["calc"] = lambda q: sp.sympify(eval(q, {"__builtins__": {}}, BASE))  # noqa: S307 — our own repo's YAML


def parse(ref, var):
    """a symbolic part's reference (mathjs syntax) as a sympy expression in the template's variable"""
    from sympy.parsing.sympy_parser import parse_expr
    loc = {var.name: var, "log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
           "atan": sp.atan, "asin": sp.asin, "acos": sp.acos, "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
           "abs": sp.Abs, "pi": sp.pi, "e": sp.E}
    return parse_expr(str(ref).replace("^", "**"), local_dict=loc)


def same(want, got, var) -> bool:
    want, got = sp.sympify(want), sp.sympify(got)
    free = sorted((want - got).free_symbols | want.free_symbols, key=lambda q: q.name)
    if free:
        rnd = random.Random(5)
        for _ in range(6):
            pt = {q: sp.Rational(rnd.randint(23, 193), 100) for q in free}
            d = complex(sp.N((want - got).subs(pt), 30))
            if abs(d) > 1e-9 * max(1.0, abs(complex(sp.N(want.subs(pt), 30)))):
                return False
        return True
    return abs(float(want) - float(got)) <= 1e-6 * max(1.0, abs(float(want)))


def ev(expr, ns):
    return sp.sympify(eval(expr, {"__builtins__": {}}, ns))  # noqa: S307 — our own repo's YAML


def num(v):
    return sp.nsimplify(v, rational=True) if isinstance(v, (int, float)) else v


def vanishes(res, var) -> bool:
    res = sp.sympify(res)
    if var in res.free_symbols:
        rnd = random.Random(3)
        return all(vanishes(res.subs(var, sp.Rational(rnd.randint(1, 99), 1000)), var) for _ in range(5))
    terms = sp.Add.make_args(sp.expand(res))
    scale = max([abs(float(t)) for t in terms] + [1.0])
    return abs(float(res)) <= 1e-7 * scale


# ── spatial helpers for the DAT perceptual-ability items (written independently of scripts/pat_cases.py) ──
def cube_tally(heights, k):
    """cubes with exactly k painted faces: every exposed face is painted except the one resting on the table"""
    hs = [[int(v) for v in row] for row in heights]
    at = lambda r, c: hs[r][c] if 0 <= r < len(hs) and 0 <= c < len(hs[0]) else 0  # noqa: E731
    count = 0
    for r in range(len(hs)):
        for c in range(len(hs[0])):
            for z in range(hs[r][c]):
                painted = (1 if z == hs[r][c] - 1 else 0) + sum(1 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if at(r + dr, c + dc) <= z)
                count += painted == int(k)
    return sp.Integer(count)


def punch_count(folds, px, py):
    """holes in a 4 x 4 sheet after unfolding: count the layers under the punch.
    folds: [(axis, line, side)] in order; axis 0 = vertical fold line x = line, 1 = horizontal y = line;
    side -1 folds the part below the line onto the part above it, +1 the other way. (px, py): punched cell centre."""
    pts = [(sp.Rational(2 * i + 1, 2), sp.Rational(2 * j + 1, 2)) for i in range(4) for j in range(4)]
    def image(p):
        for axis, line, side in folds:
            v = p[int(axis)]
            if (v - line) * int(side) > 0:
                v = 2 * line - v
            p = (v, p[1]) if int(axis) == 0 else (p[0], v)
        return p
    return sp.Integer(sum(1 for p in pts if image(p) == (sp.nsimplify(px), sp.nsimplify(py))))


def net_opposite(cells, q):
    """index of the face opposite face q when the six-square net `cells` [(x, y)] is folded into a cube"""
    cells = [(int(x), int(y)) for x, y in cells]
    # roll a cube over the net: each cell records which cube face (as an outward normal) lands on it
    start = int(q)
    state = {start: ((0, 0, -1), (1, 0, 0), (0, 1, 0))}  # (down, east, north) normals
    todo = [start]
    while todo:
        i = todo.pop()
        d, e, nn = state[i]
        neg = lambda v: tuple(-a for a in v)  # noqa: E731
        for j, (x, y) in enumerate(cells):
            if j in state:
                continue
            dx, dy = x - cells[i][0], y - cells[i][1]
            if (abs(dx), abs(dy)) not in ((1, 0), (0, 1)):
                continue
            if dx == 1: state[j] = (e, neg(d), nn)
            elif dx == -1: state[j] = (neg(e), d, nn)
            elif dy == 1: state[j] = (nn, e, neg(d))
            else: state[j] = (neg(nn), e, d)
            todo.append(j)
    want = tuple(-a for a in state[start][0])
    return sp.Integer(next(j for j, st in state.items() if st[0] == want))


def _view_columns(heights, which):
    """depth columns of an orthographic view of a cube stack (row 0 at the back, column 0 at the left), nearest first"""
    hs = [[int(v) for v in row] for row in heights]
    R, C, top = len(hs), len(hs[0]), max(1, max(max(r) for r in hs))
    if which == 0:
        return [[[hs[r][c] > top - 1 - d for d in range(top)] for c in range(C)] for r in range(R)]
    if which == 1:
        return [[[hs[R - 1 - d][c] > top - 1 - v for d in range(R)] for c in range(C)] for v in range(top)]
    return [[[hs[R - 1 - u][C - 1 - d] > top - 1 - v for d in range(C)] for u in range(R)] for v in range(top)]


def _view_lines(heights, which):
    """(solid, dashed) unit segments of a view, shifted so the drawing starts at the origin"""
    occ = _view_columns(heights, which)
    Hh, W = len(occ), len(occ[0])
    col = lambda v, u: occ[v][u] if 0 <= v < Hh and 0 <= u < W else [False] * len(occ[0][0])  # noqa: E731
    first = lambda a: a.index(True) if True in a else -1  # noqa: E731
    solid, dash = set(), set()
    def put(a, b, seg):
        if a == b:
            return
        (solid if first(a) != first(b) else dash).add(seg)
    for v in range(Hh + 1):
        for u in range(W):
            put(col(v - 1, u), col(v, u), (u, v, u + 1, v))
    for v in range(Hh):
        for u in range(W + 1):
            put(col(v, u - 1), col(v, u), (u, v, u, v + 1))
    pts = [(x, y) for g in (solid, dash) for (x1, y1, x2, y2) in g for (x, y) in ((x1, y1), (x2, y2))]
    mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
    sh = lambda g: frozenset((x1 - mx, y1 - my, x2 - mx, y2 - my) for (x1, y1, x2, y2) in g)  # noqa: E731
    return sh(solid), sh(dash)


def view_identify(heights, shown, which):
    """which view of `heights` (0 top, 1 front, 2 end) equals view `which` of `shown`; 3 if none. Must be unique."""
    target = _view_lines(shown, int(which))
    hits = [k for k in range(3) if _view_lines(heights, k) == target]
    if len(hits) > 1:
        raise ValueError("view matches more than one direction")
    return sp.Integer(hits[0] if hits else 3)


def keyhole_fit(heights, mask, any_direction=False):
    """direction (0 top, 1 front, 2 end) whose silhouette equals the opening after any turn or flip; 3 if none"""
    def trim(g):
        g = [list(r) for r in g if any(r)]
        keep = [j for j in range(len(g[0])) if any(r[j] for r in g)]
        return tuple(tuple(1 if r[j] else 0 for j in keep) for r in g)
    def turns(g):
        res = set()
        for _ in range(4):
            g = tuple(zip(*g[::-1]))
            res.add(trim(g)); res.add(trim([r[::-1] for r in g]))
        return res
    want = turns(trim([[int(v) for v in row] for row in mask]))
    hits = [k for k in range(3) if trim([[any(c) for c in row] for row in _view_columns(heights, k)]) in want]
    if any_direction:
        return bool(hits)
    if len(hits) > 1:
        raise ValueError("opening fits more than one direction")
    return sp.Integer(hits[0] if hits else 3)


# quarks and particles: (charge, baryon number, electron number, muon number), written apart from the cases
_QUARK = {"u": sp.Rational(2, 3), "c": sp.Rational(2, 3), "t": sp.Rational(2, 3), "d": -sp.Rational(1, 3), "s": -sp.Rational(1, 3), "b": -sp.Rational(1, 3)}
_PARTICLE = {"p": (1, 1, 0, 0), "n": (0, 1, 0, 0), "e": (-1, 0, 1, 0), "nue": (0, 0, 1, 0), "mu": (-1, 0, 0, 1), "numu": (0, 0, 0, 1),
             "gamma": (0, 0, 0, 0), "pi+": (1, 0, 0, 0), "pi-": (-1, 0, 0, 0), "pi0": (0, 0, 0, 0)}


def pp_charge(quarks):
    return sum(_QUARK[q] if q.islower() else -_QUARK[q.lower()] for q in str(quarks))


def pp_baryon(quarks):
    return sum(sp.Rational(1, 3) if q.islower() else -sp.Rational(1, 3) for q in str(quarks))


def pp_balance(lhs, rhs):
    """0 balanced; otherwise the first of charge (1), baryon number (2), a lepton number (3) that fails"""
    def total(side):
        t = [0, 0, 0, 0]
        for name in str(side).split():
            anti = name.endswith("bar")
            v = _PARTICLE[name[:-3] if anti else name]
            t = [a + (-b if anti else b) for a, b in zip(t, v)]
        return t
    L, R = total(lhs), total(rhs)
    if L[0] != R[0]:
        return sp.Integer(1)
    if L[1] != R[1]:
        return sp.Integer(2)
    return sp.Integer(0 if L[2:] == R[2:] else 3)


def ra_chain(Z, A, n_alpha, n_beta):
    """(Z, A) after the stated alpha and beta-minus decays, one decay at a time"""
    Z, A = int(Z), int(A)
    for _ in range(int(n_alpha)):
        Z, A = Z - 2, A - 4
    for _ in range(int(n_beta)):
        Z += 1
    return sp.Integer(Z), sp.Integer(A)


def basis_count(nH, nHeavy, kind):
    """basis functions for H and second-row atoms: 0 STO-3G, 1 6-31G, 2 6-31G(d) with six d functions"""
    shells_H = {0: ["s"], 1: ["s", "s"], 2: ["s", "s"]}[int(kind)]
    shells_X = {0: ["s", "s", "p"], 1: ["s", "s", "s", "p", "p"], 2: ["s", "s", "s", "p", "p", "d"]}[int(kind)]
    size = {"s": 1, "p": 3, "d": 6}
    return sp.Integer(int(nH) * sum(size[t] for t in shells_H) + int(nHeavy) * sum(size[t] for t in shells_X))


def sn_e(sub, nuc):
    """dominant pathway for an alkyl halide: 0 SN2, 1 E2, 2 SN1 with E1 (a lookup table, written apart from the template's rule)"""
    table = {("methyl", "nucleophile"): 0, ("methyl", "small-base"): 0, ("methyl", "bulky-base"): 0,
             ("primary", "nucleophile"): 0, ("primary", "small-base"): 0, ("primary", "bulky-base"): 1,
             ("secondary", "nucleophile"): 0, ("secondary", "small-base"): 1, ("secondary", "bulky-base"): 1, ("secondary", "weak"): 2,
             ("tertiary", "small-base"): 1, ("tertiary", "bulky-base"): 1, ("tertiary", "weak"): 2}
    return sp.Integer(table[(str(sub), str(nuc))])


# exceptions to the filling order, as valence strings (the generator lists every atom's counts instead)
_CONFIG_EXC = {"Cr": "d5 s1", "Cu": "d10 s1", "Nb": "d4 s1", "Mo": "d5 s1", "Ru": "d7 s1", "Rh": "d8 s1", "Pd": "d10 s0",
               "Ag": "d10 s1", "Pt": "d9 s1", "Au": "d10 s1",
               "La": "f0 d1 s2", "Ce": "f1 d1 s2", "Gd": "f7 d1 s2",
               "Ac": "f0 d1 s2", "Th": "f0 d2 s2", "Pa": "f2 d1 s2", "U": "f3 d1 s2", "Np": "f4 d1 s2", "Cm": "f7 d1 s2"}


def pt_madelung(sym):
    """(f, d, s) valence counts if the shells simply filled in order: s, then f, then d"""
    period, i = _pt_place(pt_Z(sym))
    n = len(_PT[period])
    after_s = i - 1  # electrons beyond ns2
    if n == 18:
        return (0, after_s, 2)
    if n == 32:
        return (min(after_s, 14), max(0, after_s - 14), 2)
    raise ValueError("no d or f shell filling in this period")


def pt_config(sym):
    """(f, d, s) of the ground-state atom; a filled 4f shell under the 5d metals is part of the core, so it reads 0 there"""
    f, d, s_ = pt_madelung(sym)
    if str(sym) in _CONFIG_EXC:
        got = {t[0]: int(t[1:]) for t in _CONFIG_EXC[str(sym)].split()}
        f, d, s_ = got.get("f", f), got["d"], got["s"]
    period, i = _pt_place(pt_Z(sym))
    return (f, d, s_)


# the periodic table by period, written separately from scripts/pt_cases.py's flat list
_PERIODS = ["H He", "Li Be B C N O F Ne", "Na Mg Al Si P S Cl Ar",
            "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr",
            "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe",
            "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn",
            "Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og"]
_PT = [row.split() for row in _PERIODS]
assert [len(r) for r in _PT] == [2, 8, 8, 18, 18, 32, 32]


def pt_Z(sym):
    flat = [e for r in _PT for e in r]
    return sp.Integer(flat.index(str(sym)) + 1)


def _pt_place(z):
    z = int(z)
    for period, r in enumerate(_PT):
        if z <= len(r):
            return period, z - 1
        z -= len(r)
    raise ValueError("no such element")


def pt_group(z):
    """IUPAC group 1-18 from the position in the period; the fifteen-wide f rows have none"""
    period, i = _pt_place(z)
    n = len(_PT[period])
    if n == 2:
        return sp.Integer(1 if i == 0 else 18)
    if n == 8:
        return sp.Integer(i + 1 if i < 2 else i + 11)
    if n == 18:
        return sp.Integer(i + 1)
    if i < 2:
        return sp.Integer(i + 1)
    if i < 17:
        raise ValueError("f-block element: no group asked")
    return sp.Integer(i - 13)


def pt_below(z):
    """the element in the same group one period down"""
    period, i = _pt_place(z)
    g = pt_group(z)
    start = sum(len(r) for r in _PT[:period + 1])
    for k in range(len(_PT[period + 1])):
        try:
            if pt_group(start + k + 1) == g:
                return sp.Integer(start + k + 1)
        except ValueError:
            continue
    raise ValueError("nothing below")


def _unpack(code):
    d = str(int(code))[1:].rjust(9, "0")
    return tuple(tuple(int(d[r * 3 + c]) for c in range(3)) for r in range(3))


@functools.lru_cache(maxsize=None)
def _possible_views(hcode, miss):
    """every drawing the missing view could be, over all 3 x 3 stacks that share the two given views"""
    h, miss = _unpack(hcode), int(miss)
    given = [k for k in range(3) if k != miss]
    want = [_view_lines(h, k) for k in given]
    top = max(max(r) for r in h)
    res = set()
    def walk(i, g):
        if i == 9:
            if max(max(r) for r in g) == top and all(_view_lines(g, k) == w for k, w in zip(given, want)):
                res.add(_view_lines(g, miss))
            return
        r, c = divmod(i, 3)
        for v in range(top + 1):
            if 0 in given and (v == 0) != (h[r][c] == 0):
                continue  # the top view fixes which squares are empty
            if 1 in given and v > max(h[q][c] for q in range(3)):
                continue  # taller than the front view allows in this column
            if 2 in given and v > max(h[r]):
                continue  # taller than the end view allows in this row
            g[r][c] = v
            walk(i + 1, g)
        g[r][c] = 0
    walk(0, [[0] * 3 for _ in range(3)])
    return frozenset(res)


def view_missing(hcode, options, miss):
    """index of the one lettered drawing that can be the missing view (0 top, 1 front, 2 end)"""
    ok = _possible_views(int(hcode), int(miss))
    hits = [i for i, o in enumerate(options) if _view_lines(_unpack(o), int(miss)) in ok]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} of the lettered views are possible")
    return sp.Integer(hits[0])


def keyhole_pick(hcode, masks):
    """index of the one lettered opening the stack fits through"""
    hits = [i for i, m in enumerate(masks) if keyhole_fit(_unpack(hcode), _unpack(m), True)]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} of the lettered openings fit")
    return sp.Integer(hits[0])


def _profile(code):
    return [(int(ch, 16) >> 2, int(ch, 16) & 3) for ch in "%x" % int(code)][1:]


def _inside(P, x, z):
    """is the point in the closed polygon? exact arithmetic, boundary counts"""
    hit = False
    for i in range(len(P)):
        (x1, z1), (x2, z2) = P[i], P[(i + 1) % len(P)]
        cross = (x2 - x1) * (z - z1) - (z2 - z1) * (x - x1)
        if cross == 0 and min(x1, x2) <= x <= max(x1, x2) and min(z1, z2) <= z <= max(z1, z2):
            return True
        if (z1 > z) != (z2 > z) and x < x1 + sp.Rational((x2 - x1)) * (z - z1) / (z2 - z1):
            hit = not hit
    return hit


def _poly_key(P):
    mx, mz = min(p[0] for p in P), min(p[1] for p in P)
    Q = [(x - mx, z - mz) for x, z in P]
    return min(tuple(q[i:] + q[:i]) for q in (Q, Q[::-1]) for i in range(len(Q)))


def _poly_turns(P):
    out = set()
    for sx in (1, -1):
        for sz in (1, -1):
            out.add(_poly_key([(sx * x, sz * z) for x, z in P]))
            out.add(_poly_key([(sz * z, sx * x) for x, z in P]))
    return out


def _prism_view(code, D, which):
    """a comparable description of one view of a prism; corners are found by scanning inward from outside the profile"""
    P, D, which = _profile(code), int(D), int(which)
    xs, zs = [p[0] for p in P], [p[1] for p in P]
    W, Hh = max(xs) - min(xs), max(zs) - min(zs)
    box = [(0, 0), (W, 0), (W, Hh), (0, Hh)]
    steps = [sp.Rational(k, 6) for k in range(18, -1, -1)]  # edges between whole-number corners cross grid lines at sixths
    if which == 1:
        return ("rect", W, Hh, (), ()) if _poly_key(P) == _poly_key(box) else ("poly", _poly_key(P))
    if which == 0:
        lines = []
        for x in sorted(set(xs)):
            if min(xs) < x < max(xs):
                first = next(z for z in steps if _inside(P, x, z))
                lines.append((x - min(xs), 1 if (x, first) in P else 2))
        return ("rect", W, D, tuple(lines), ())
    lines = []
    for z in set(zs):
        if min(zs) < z < max(zs):
            first = next(x for x in steps if _inside(P, x, z))
            lines.append((max(zs) - z, 1 if (first, z) in P else 2))
    return ("rect", D, Hh, (), tuple(sorted(lines)))


def prism_identify(code, D, shown, Dshown, which):
    target = _prism_view(shown, Dshown, which)
    hits = [k for k in range(3) if _prism_view(code, D, k) == target]
    if len(hits) > 1:
        raise ValueError("view matches more than one direction")
    return sp.Integer(hits[0] if hits else 3)


def prism_keyhole(code, D, options):
    P, D = _profile(code), int(D)
    W, Hh = max(p[0] for p in P) - min(p[0] for p in P), max(p[1] for p in P) - min(p[1] for p in P)
    fits = _poly_turns(P) | _poly_turns([(0, 0), (W, 0), (W, D), (0, D)]) | _poly_turns([(0, 0), (D, 0), (D, Hh), (0, Hh)])
    hits = [i for i, o in enumerate(options) if _poly_key(_profile(o)) in fits]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} of the lettered openings fit")
    return sp.Integer(hits[0])


@functools.lru_cache(maxsize=None)
def sph_L2(l, m):
    """eigenvalue of L^2 (in hbar^2) found by applying the angular operator to Y_l^m"""
    th, ph = sp.symbols("theta phi", real=True)
    Y = sp.Ynm(int(l), int(m), th, ph).expand(func=True)
    L2 = -(sp.diff(sp.sin(th) * sp.diff(Y, th), th) / sp.sin(th) + sp.diff(Y, ph, 2) / sp.sin(th) ** 2)
    return sp.nsimplify(sp.simplify(L2 / Y).subs({th: sp.Rational(7, 10), ph: sp.Rational(3, 10)}).evalf(), rational=True, tolerance=1e-9)


def fc_strongest(S):
    """v' with the largest Poisson Franck-Condon factor S^v e^-S / v!"""
    S = sp.nsimplify(S)
    vals = [sp.N(S ** v * sp.exp(-S) / sp.factorial(v)) for v in range(30)]
    return sp.Integer(max(range(30), key=lambda v: vals[v]))


def hf_energy(h, J, K):
    """closed-shell Hartree-Fock energy summed over spin orbitals: sum h + 1/2 sum (J - K if same spin)"""
    orbs = [(i, s) for i in range(len(h)) for s in (0, 1)]
    E = sum(sp.nsimplify(h[i]) for i, _ in orbs)
    for (i, s) in orbs:
        for (j, t) in orbs:
            if (i, s) == (j, t):
                continue
            E += sp.Rational(1, 2) * (sp.nsimplify(J[i][j]) - (sp.nsimplify(K[i][j]) if s == t else 0))
    return E


def hund_ground(l, ne):
    """(2S + 1, L, J) of the ground level of l^ne: fill m_l from the top, spin up first"""
    l, ne = int(l), int(ne)
    slots = [(m, sp.Rational(1, 2)) for m in range(l, -l - 1, -1)] + [(m, -sp.Rational(1, 2)) for m in range(l, -l - 1, -1)]
    used = slots[:ne]
    L, S = abs(sum(m for m, _ in used)), sum(s for _, s in used)
    J = L + S if ne > 2 * l + 1 else abs(L - S)
    return int(2 * S + 1), int(L), J


def hund_choice(l, ne, labels):
    mult, L, _ = hund_ground(l, ne)
    sup = {"1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶"}
    return sp.Integer(list(labels).index(sup[str(mult)] + "SPDFGH"[L]))


def mo_fill(ne):
    """(bond order, unpaired electrons) of a second-row diatomic with ne electrons in all; the 2p sigma lies above the pi pair up to 14 electrons"""
    ne = int(ne)
    low = [("b", 1), ("a", 1), ("b", 1), ("a", 1)]
    upper = [("b", 2), ("b", 1), ("a", 2), ("a", 1)] if ne <= 14 else [("b", 1), ("b", 2), ("a", 2), ("a", 1)]
    nb = na = unpaired = 0
    for kind, deg in low + upper:
        take = min(ne, 2 * deg)
        ne -= take
        nb += take if kind == "b" else 0
        na += take if kind == "a" else 0
        unpaired += take if take <= deg else 2 * deg - take
    return sp.Rational(nb - na, 2), unpaired


@functools.lru_cache(maxsize=None)
def commutes(pair):
    """True when the two operators commute, tested on a polynomial (a harmonic well stands in for any central potential)"""
    X, Y, Z = sp.symbols("X Y Z", real=True)
    I = sp.I
    px = lambda g: -I * sp.diff(g, X)  # noqa: E731
    py = lambda g: -I * sp.diff(g, Y)  # noqa: E731
    pz = lambda g: -I * sp.diff(g, Z)  # noqa: E731
    Lx = lambda g: Y * pz(g) - Z * py(g)  # noqa: E731
    Ly = lambda g: Z * px(g) - X * pz(g)  # noqa: E731
    Lz = lambda g: X * py(g) - Y * px(g)  # noqa: E731
    L2 = lambda g: Lx(Lx(g)) + Ly(Ly(g)) + Lz(Lz(g))  # noqa: E731
    H = lambda g: -(sp.diff(g, X, 2) + sp.diff(g, Y, 2) + sp.diff(g, Z, 2)) / 2 + (X ** 2 + Y ** 2 + Z ** 2) * g / 2  # noqa: E731
    ops = {"x": lambda g: X * g, "px": px, "py": py, "L2": L2, "Lz": Lz, "Lx": Lx, "Ly": Ly, "H": H}
    a, b = (ops[k] for k in pair.split(","))
    g = X ** 3 * Y + 2 * X * Y * Z ** 2 + Z ** 3 - X * Y ** 2 + 5 * X + Y * Z
    return sp.expand(a(b(g)) - b(a(g))) == 0


def box_degeneracy(E):
    """number of (nx, ny, nz), positive integers, with nx^2 + ny^2 + nz^2 = E"""
    E = int(E)
    return sp.Integer(sum(1 for a in range(1, 12) for b in range(1, 12) for c in range(1, 12) if a * a + b * b + c * c == E))


def huckel_chain(N, k):
    """x in alpha + x*beta for the k-th lowest pi orbital of a linear chain: k-th largest eigenvalue of the adjacency matrix"""
    N, k = int(N), int(k)
    M = sp.Matrix(N, N, lambda i, j: 1 if abs(i - j) == 1 else 0)
    vals = sorted((sp.re(sp.N(v)) for v, mult in M.eigenvals().items() for _ in range(mult)), reverse=True)
    return vals[k - 1]


def rank_code(values):
    """labels 1..n written smallest value first, as one integer: [74, 70, 82, 78] -> 2143"""
    order = sorted(range(len(values)), key=lambda j: values[j])
    return sp.Integer(int("".join(str(j + 1) for j in order)))


BASE.update({"cube_tally": cube_tally, "punch_count": punch_count, "net_opposite": net_opposite, "rank_code": rank_code, "box_degeneracy": box_degeneracy, "huckel_chain": huckel_chain, "view_identify": view_identify, "keyhole_fit": keyhole_fit, "sph_L2": sph_L2, "fc_strongest": fc_strongest, "hf_energy": hf_energy, "hund_ground": hund_ground, "hund_choice": hund_choice, "mo_fill": mo_fill, "commutes": commutes, "view_missing": view_missing, "keyhole_pick": keyhole_pick, "prism_identify": prism_identify, "prism_keyhole": prism_keyhole, "pt_Z": pt_Z, "pt_group": pt_group, "pt_below": pt_below, "pt_config": pt_config, "pt_madelung": pt_madelung, "sn_e": sn_e, "pp_charge": pp_charge, "pp_baryon": pp_baryon, "pp_balance": pp_balance, "ra_chain": ra_chain, "basis_count": basis_count})


# ── accounting (fa-*): periodic inventory cost flow, written as a unit-by-unit queue ──
def fa_inventory(method, layers, sold):
    """ending inventory cost; method 0 FIFO, 1 LIFO, 2 weighted average (all periodic)"""
    units = []
    for q, c in layers:
        units += [sp.nsimplify(c)] * int(q)
    left = len(units) - int(sold)
    if method == 0:
        return sum(units[len(units) - left:])
    if method == 1:
        return sum(units[:left])
    return sp.Rational(sum(units)) / len(units) * left


import sys as _sys  # noqa: E402
_sys.path.insert(0, str(Path(__file__).parent))
from sql import FUNCS as _SQL, check_tables as _sql_tables  # noqa: E402
BASE.update(_SQL)
BASE["fa_inventory"] = fa_inventory
from progcode import FUNCS as _CODE  # noqa: E402
BASE.update(_CODE)
from csalgo import FUNCS as _CSA  # noqa: E402
BASE.update(_CSA)
from mvcalc import FUNCS as _MV  # noqa: E402
BASE.update(_MV)
from nursing import FUNCS as _NR  # noqa: E402
BASE.update(_NR)
from dental import FUNCS as _DN  # noqa: E402
BASE.update(_DN)
_bad = _sql_tables(TEMPLATES)
if _bad:
    raise SystemExit(f"SQL figures differ from tests/verify/sql.py TABLES: {_bad}")


def check(p, H):
    meta = p.get("meta", {})
    name = meta.get("data")
    if name is None:
        return None
    t = TEMPLATES[name]
    v = t.get("verify") or {}
    # radial coordinates are positive (log r, limits at 0+); a Cartesian x may be negative
    var = sp.Symbol(v.get("var", "x"), positive=True) if v.get("var") == "r" else sp.Symbol(v.get("var", "x"), real=True)
    labels = [q["label"] for q in t["parts"]]
    def _claim(ref):
        try:
            return num(float(ref))
        except (TypeError, ValueError):
            return parse(ref, var)
    claimed = {lab: _claim(part["answer"]["ref"]) for lab, part in zip(labels, p["parts"])
               if part["answer"]["kind"] == "expression"}
    ns = {**BASE, "S": lambda q: parse(q, var), **{k: num(x) for k, x in meta["given"].items()}, v.get("var", "x"): var}
    ns_parts = {**ns, **claimed}

    # ode parts (antiderivatives, first-order solutions): differentiate the claimed y and compare with
    # the right-hand side; an initial condition must hold and leaves no constant
    yS, CS = sp.Symbol("y"), sp.Symbol("C")
    for part in p["parts"]:
        a = part["answer"]
        if a["kind"] != "ode":
            continue
        from sympy.parsing.sympy_parser import parse_expr
        loc = {var.name: var, "y": yS, "C": CS, "log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos,
               "tan": sp.tan, "atan": sp.atan, "asin": sp.asin, "sec": sp.sec, "abs": sp.Abs, "pi": sp.pi, "e": sp.E}
        f = parse_expr(a["rhs"].replace("^", "**"), local_dict=loc)
        g = parse_expr(a["ref"].split("=", 1)[1].replace("^", "**"), local_dict=loc)
        res = sp.diff(g, var) - f.subs(yS, g)
        rnd = random.Random(7)
        for _ in range(6):
            pt = {var: sp.Rational(rnd.randint(23, 193), 100), CS: sp.Rational(rnd.randint(11, 97), 50)}
            if abs(complex(sp.N(res.subs(pt), 30))) > 1e-9 * max(1.0, abs(complex(sp.N(f.subs(yS, g).subs(pt), 30)))):
                print(f"  {name}: claimed solution does not satisfy y' = {a['rhs']}")
                return False
        if a.get("ic"):
            x0, y0 = [sp.nsimplify(q, rational=True) for q in a["ic"]]
            if g.has(CS) or abs(complex(sp.N(g.subs(var, x0) - y0, 30))) > 1e-9:
                print(f"  {name}: claimed solution misses the initial condition")
                return False
        elif not g.has(CS):
            print(f"  {name}: a general solution needs its constant")
            return False

    if v.get("ode"):
        Tf = sp.Function("T")
        general = sp.dsolve(ev(v["ode"], {**ns_parts, "T": Tf}), Tf(var)).rhs
        consts = sorted((s for s in general.free_symbols if s.name.startswith("C") and s not in ns_parts.values()),
                        key=lambda s: s.name)
        lim0 = lambda e: sp.limit(e, var, 0, "+")  # noqa: E731

        def fns(sol):
            return {"T": lambda a: sol.subs(var, a), "dT": lambda a: sp.diff(sol, var).subs(var, a), "lim0": lim0}

        eqs = []
        for bc in v.get("bcs", []):
            lhs, rhs = bc.split("=", 1)
            g = {**ns_parts, **fns(general)}
            eqs.append(sp.Eq(ev(lhs, g), ev(rhs, g)))
        sol = sp.solve(eqs, consts, dict=True)
        if len(sol) != 1:
            return False
        Tsol = general.subs(sol[0])
        ns_parts = {**ns_parts, **fns(Tsol)}

    for lab, expr in (v.get("expect") or {}).items():
        want = ev(expr, ns_parts)
        if not same(want, claimed[lab], var):
            print(f"  {name}: {lab} claimed {claimed[lab]}, verifier gets {want}")
            return False
    # choice parts: the index the generator marked correct must be the one the verifier computes
    for lab, expr in (v.get("choices") or {}).items():
        want = int(ev(expr, ns_parts))
        got = int(meta["values"][lab])
        if want != got:
            print(f"  {name}: choice {lab} marked {got}, verifier gets {want}")
            return False
    for res in v.get("residuals") or []:
        if not vanishes(ev(res, ns_parts), var):
            print(f"  {name}: residual {res} = {float(ev(res, ns_parts)) if var not in ev(res, ns_parts).free_symbols else '…'}")
            return False
    # every numeric part was checked by something above (the build enforces it; make sure here too)
    used = json.dumps([v.get("ode"), v.get("bcs"), v.get("residuals"), list((v.get("expect") or {}).keys())])
    return all(lab in used for lab in claimed)
