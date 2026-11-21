"""Builds drills/problems/mvd-depth.yaml: multivariable calculus in depth (CA units 12-14, MIT 18.02
units 2-4). Run: python3 scripts/mvd_cases.py

Each template carries many cases (different functions, regions, curves, surfaces), not one problem
with new numbers. Answers are computed here with sympy along the route the card teaches (Green,
Stokes, the divergence theorem, polar or spherical coordinates...); tests/verify/mvcalc.py checks
them along a different route (the line or surface integral itself, the original coordinates).
Setup cards show four integrals (A-D) in the prompt; exactly one equals the target, which the
generator asserts and the verifier re-checks.
"""
import sys
from pathlib import Path

import sympy as sp
import yaml

x, y, z, t, u, v, r, th, ph, rho = sp.symbols("x y z t u v r theta phi rho", real=True)
NS = {"x": x, "y": y, "z": z, "t": t, "u": u, "v": v, "pi": sp.pi, "E": sp.E}
OUT = Path(__file__).resolve().parent.parent / "drills/problems/mvd-depth.yaml"


def S(e):
    return sp.sympify(e, locals=NS)


def N(e):
    val = sp.N(sp.sympify(e).doit(), 17)
    return float(val)


def tex_ok(*ts):
    for s in ts:
        assert "{{" not in s, s


T = []


def template(name, skill, prompt, part, cases, verify, pace="quick", figure=None, explain=None):
    for c in cases:
        tex_ok(*[str(v) for v in c.values()])
    d = {"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt, "parts": [part], "verify": verify}
    T.append(d)


def value_part(ask, explain, tol=0.0001):
    return {"ask": ask, "label": "a", "value": "ans", "tol": tol, "explain": explain}


def choice_part(ask, opts, explain):
    return {"ask": ask, "label": "a", "choice": opts, "correct": "ans", "explain": explain}


ABCD = ["A", "B", "C", "D"]


def setup_cases(rows):
    """rows: (context fields, target sympy string, [4 (tex, sympy string)]); computes ans"""
    out = []
    for ctx, target, opts in rows:
        want = N(S(target))
        hits = [i for i, (_, e) in enumerate(opts) if abs(N(S(e)) - want) < 1e-9 * (1 + abs(want))]
        assert len(hits) == 1, (ctx, target, [N(S(e)) for _, e in opts], want)
        c = dict(ctx)
        c["target"] = target
        for k, (tx, e) in zip("ABCD", opts):
            c["t" + k], c["e" + k] = tx, e
        c["ans"] = hits[0]
        out.append(c)
    return out


SETUP_VERIFY = {"choices": {"a": "vpick(target, [eA, eB, eC, eD])"}}
SETUP_PROMPT_TAIL = ' (A) ${{tA}}$ (B) ${{tB}}$ (C) ${{tC}}$ (D) ${{tD}}$'

# ════════════════ unit 12 · partial derivatives ════════════════
rows = [
    ("x^2 y^3 + 4xy", "x**2*y**3 + 4*x*y", 1, 2),
    ("e^{xy}", "exp(x*y)", 1, 0),
    ("\\ln(x^2 + y^2)", "log(x**2 + y**2)", 1, 2),
    ("\\sin(x y^2)", "sin(x*y**2)", 0, 3),
    ("\\dfrac{x}{y}", "x/y", 3, 2),
    ("x\\sqrt{y}", "x*sqrt(y)", 2, 4),
    ("x^3 - 5xy + y^2", "x**3 - 5*x*y + y**2", 2, -1),
    ("\\arctan(y/x)", "atan(y/x)", 1, 1),
]
cases = []
for ftex, f, px, py in rows:
    for w in ("x", "y"):
        val = sp.diff(S(f), S(w)).subs({x: px, y: py})
        if val == 0:
            continue
        cases.append({"ftex": ftex, "f": f, "w": w, "px": px, "py": py, "ans": N(val)})
template("mvd-partial", "calc.multivariable",
         "For $f(x, y) = {{ftex}}$, what is $f_{{w}}({{px}}, {{py}})$?".replace("f_{{w}}", "f_{ {{w}} }"),
         value_part("Partial derivative", "Differentiate in that variable alone, treating the other as a constant, then substitute the point. $f_x$ is the slope of the surface in the $x$ direction"),
         cases, {"expect": {"a": "mv_at(mv_d(f, w), px, py)"}})

rows = [
    ("x^3 y^2", "x**3*y**2", 1, 2), ("e^{2x}\\sin y", "exp(2*x)*sin(y)", 0, 0), ("x^2 e^{y}", "x**2*exp(y)", 1, 0),
    ("\\ln(xy)", "log(x*y)", 1, 1), ("x\\cos(xy)", "x*cos(x*y)", 1, 0), ("y^2 \\sqrt{x}", "y**2*sqrt(x)", 4, 1),
]
cases = []
for ftex, f, px, py in rows:
    val = sp.diff(S(f), x, y).subs({x: px, y: py})
    if val != 0:
        cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "ans": N(val)})
template("mvd-mixed", "calc.multivariable", "For $f(x, y) = {{ftex}}$, what is $f_{xy}({{px}}, {{py}})$?",
         value_part("Mixed partial", "Differentiate in $x$, then in $y$ (or the other order: by Clairaut's theorem the mixed partials agree when they are continuous)"),
         cases, {"expect": {"a": "mv_at(mv_d(f, 'y', 'x'), px, py)"}})

rows = [
    ("x^2 + 3xy", "x**2 + 3*x*y", 1, 1, 3, 4), ("x e^{y}", "x*exp(y)", 2, 0, 1, 1), ("\\sin(x) + \\cos(y)", "sin(x) + cos(y)", 0, 0, 1, 2),
    ("x^2 y", "x**2*y", 1, 2, -1, 1), ("\\ln(x^2 + y^2)", "log(x**2 + y**2)", 1, 1, 1, 0), ("xy^2", "x*y**2", 2, 1, 0, -1),
    ("4 - x^2 - y^2", "4 - x**2 - y**2", 1, 1, 1, 1),
]
cases = []
for ftex, f, px, py, a, b in rows:
    g = [sp.diff(S(f), w).subs({x: px, y: py}) for w in (x, y)]
    val = (g[0] * a + g[1] * b) / sp.sqrt(a ** 2 + b ** 2)
    if val != 0:
        cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "va": a, "vb": b, "ans": N(val)})
template("mvd-directional", "calc.partials-apps",
         "What is the directional derivative of $f(x, y) = {{ftex}}$ at $({{px}}, {{py}})$ in the direction of $\\langle {{va}}, {{vb}} \\rangle$?",
         value_part("Directional derivative", "$D_{\\mathbf u}f = \\nabla f\\cdot\\mathbf u$ with $\\mathbf u$ a unit vector: divide the given direction by its length first. Forgetting to normalise is the usual error"),
         cases, {"expect": {"a": "(mv_at(mv_d(f, 'x'), px, py)*va + mv_at(mv_d(f, 'y'), px, py)*vb)/sqrt(va**2 + vb**2)"}})

cases = []
for ftex, f, px, py in [("x^2 + 3xy", "x**2 + 3*x*y", 1, 1), ("x e^{y}", "x*exp(y)", 2, 0), ("x^2 y", "x**2*y", 1, 2),
                        ("\\ln(x^2 + y^2)", "log(x**2 + y**2)", 1, 2), ("4 - x^2 - 2y^2", "4 - x**2 - 2*y**2", 1, 1), ("xy^2", "x*y**2", 2, 1)]:
    g = [sp.diff(S(f), w).subs({x: px, y: py}) for w in (x, y)]
    cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "ans": N(sp.sqrt(g[0] ** 2 + g[1] ** 2))})
template("mvd-max-rate", "calc.partials-apps", "At $({{px}}, {{py}})$, what is the greatest rate of increase of $f(x, y) = {{ftex}}$?",
         value_part("Maximum rate", "$f$ increases fastest in the direction of $\\nabla f$, at the rate $|\\nabla f|$; it decreases fastest in the opposite direction, and does not change along the level curve (perpendicular to $\\nabla f$)"),
         cases, {"expect": {"a": "sqrt(mv_at(mv_d(f, 'x'), px, py)**2 + mv_at(mv_d(f, 'y'), px, py)**2)"}})

cases = []
for ftex, f, px, py in [("x^2 + 4y^2", "x**2 + 4*y**2", 2, 1), ("xy", "x*y", 2, 3), ("x^2 - y^2", "x**2 - y**2", 3, 1),
                        ("x^3 + y^3", "x**3 + y**3", 1, 2), ("y e^{x}", "y*exp(x)", 0, 2), ("x^2 + xy + y^2", "x**2 + x*y + y**2", 1, 1)]:
    g = [sp.diff(S(f), w).subs({x: px, y: py}) for w in (x, y)]
    cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "ans": N(-g[0] / g[1])})
template("mvd-level-slope", "calc.partials-apps",
         "What is the slope of the level curve of $f(x, y) = {{ftex}}$ through $({{px}}, {{py}})$, at that point?",
         value_part("Slope", "Along a level curve $f$ is constant, so $f_x\\,dx + f_y\\,dy = 0$ and $dy/dx = -f_x/f_y$. Equivalently, the tangent is perpendicular to $\\nabla f$"),
         cases, {"expect": {"a": "-mv_at(mv_d(f, 'x'), px, py)/mv_at(mv_d(f, 'y'), px, py)"}})

cases = []
for ftex, f, px, py, dx, dy in [("x^2 y", "x**2*y", 2, 1, 0.1, -0.1), ("\\sqrt{x^2 + y^2}", "sqrt(x**2 + y**2)", 3, 4, 0.1, 0.2),
                                ("e^{x}\\cos y", "exp(x)*cos(y)", 0, 0, 0.1, 0.2), ("\\ln(x + 2y)", "log(x + 2*y)", 1, 0, 0.2, 0.1),
                                ("xy^2", "x*y**2", 1, 2, 0.05, 0.1), ("x^3 + y^3", "x**3 + y**3", 1, 1, -0.1, 0.1)]:
    F = S(f)
    L = F.subs({x: px, y: py}) + sp.diff(F, x).subs({x: px, y: py}) * sp.nsimplify(dx) + sp.diff(F, y).subs({x: px, y: py}) * sp.nsimplify(dy)
    cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "dx": dx, "dy": dy, "ans": N(L)})
template("mvd-linearize", "calc.partials-apps",
         "Use the tangent plane to $f(x, y) = {{ftex}}$ at $({{px}}, {{py}})$ to estimate $f({{px}} + {{dx}}, {{py}} + {{dy}})$.".replace("{{px}} + {{dx}}", "{{px + dx}}").replace("{{py}} + {{dy}}", "{{py + dy}}"),
         value_part("Estimate", "$L = f(a, b) + f_x(a, b)\\,\\Delta x + f_y(a, b)\\,\\Delta y$: the tangent plane, good for small steps. The error grows with the square of the step"),
         cases, {"expect": {"a": "mv_at(f, px, py) + mv_at(mv_d(f, 'x'), px, py)*nsimplify(dx) + mv_at(mv_d(f, 'y'), px, py)*nsimplify(dy)"}})

cases = []
for stex, F, p in [("x^2 + y^2 + z^2 = 14", "x**2 + y**2 + z**2 - 14", (1, 2, 3)), ("x^2 + 2y^2 + 3z^2 = 6", "x**2 + 2*y**2 + 3*z**2 - 6", (1, 1, 1)),
                   ("xyz = 6", "x*y*z - 6", (1, 2, 3)), ("z = x^2 + y^2", "x**2 + y**2 - z", (1, 2, 5)),
                   ("x^2 + y^2 - z^2 = 4", "x**2 + y**2 - z**2 - 4", (2, 1, 1)), ("z = xy", "x*y - z", (2, 3, 6))]:
    G = S(F)
    n = [sp.diff(G, w).subs({x: p[0], y: p[1], z: p[2]}) for w in (x, y, z)]
    g = sp.gcd_list(n) if all(k.is_integer for k in n) else 1
    n = [k / g for k in n]
    if n[0] < 0 or (n[0] == 0 and n[1] < 0):
        n = [-k for k in n]
    dval = sum(a * b for a, b in zip(n, p))
    cases.append({"stex": stex, "F": F, "px": p[0], "py": p[1], "pz": p[2], "na": int(n[0]), "nb": int(n[1]), "nc": int(n[2]), "ans": N(dval)})
template("mvd-tangent-plane-implicit", "calc.partials-apps",
         "The tangent plane to the surface ${{stex}}$ at $({{px}}, {{py}}, {{pz}})$ can be written ${{na}}x + {{nb}}y + {{nc}}z = d$. What is $d$?",
         value_part("d", "For a level surface $F(x, y, z) = c$ the normal is $\\nabla F$. The plane is $\\nabla F\\cdot(\\mathbf r - \\mathbf r_0) = 0$, so $d = \\mathbf n\\cdot\\mathbf r_0$. Write $z = f(x, y)$ as $f - z = 0$ first"),
         [c for c in cases if c["ans"] != 0], {"expect": {"a": "na*px + nb*py + nc*pz"}})

cases = []
for ztex, f, xt_tex, xt, yt_tex, yt, t0 in [
        ("x^2 y", "x**2*y", "t^2", "t**2", "3t", "3*t", 1), ("e^{x} \\sin y", "exp(x)*sin(y)", "\\ln t", "log(t)", "\\pi t", "pi*t", 1),
        ("xy + y^2", "x*y + y**2", "\\cos t", "cos(t)", "\\sin t", "sin(t)", 0), ("\\sqrt{x^2 + y^2}", "sqrt(x**2 + y**2)", "3t", "3*t", "4t^2", "4*t**2", 1),
        ("x/y", "x/y", "t^3", "t**3", "t + 1", "t + 1", 1), ("\\ln(x + y)", "log(x + y)", "e^{t}", "exp(t)", "t^2", "t**2", 0)]:
    Z = S(f).subs({x: S(xt), y: S(yt)}, simultaneous=True)
    val = sp.diff(Z, t).subs(t, t0)
    cases.append({"ztex": ztex, "f": f, "xtx": xt_tex, "xt": xt, "ytx": yt_tex, "yt": yt, "t0": t0, "ans": N(val)})
template("mvd-chain-t", "calc.multivariable",
         "$z = {{ztex}}$ with $x = {{xtx}}$ and $y = {{ytx}}$. What is $dz/dt$ at $t = {{t0}}$?",
         value_part("dz/dt", "$\\dfrac{dz}{dt} = z_x\\dfrac{dx}{dt} + z_y\\dfrac{dy}{dt}$: one term per path through the dependency tree, each evaluated at the point $(x(t_0), y(t_0))$"),
         cases, {"expect": {"a": "diff(SE(f).subs({SE('x'): SE(xt), SE('y'): SE(yt)}, simultaneous=True), SE('t')).subs(SE('t'), t0)"}})

cases = []
for ztex, f, xs_tex, xs, ys_tex, ys, s0, t0 in [
        ("x^2 + y^2", "x**2 + y**2", "s + t", "u + v", "s - t", "u - v", 1, 2), ("xy", "x*y", "s^2 t", "u**2*v", "s t^2", "u*v**2", 1, 1),
        ("e^{x + y}", "exp(x + y)", "st", "u*v", "s^2", "u**2", 1, 0), ("x^2 y", "x**2*y", "s\\cos t", "u*cos(v)", "s\\sin t", "u*sin(v)", 2, 0),
        ("\\ln(xy)", "log(x*y)", "s + 2t", "u + 2*v", "3s", "3*u", 1, 1)]:
    Z = S(f).subs({x: S(xs), y: S(ys)}, simultaneous=True)
    val = sp.diff(Z, u).subs({u: s0, v: t0})
    cases.append({"ztex": ztex, "f": f, "xstx": xs_tex, "xs": xs, "ystx": ys_tex, "ys": ys, "s0": s0, "t0": t0, "ans": N(val)})
template("mvd-chain-partial", "calc.multivariable",
         "$z = {{ztex}}$ with $x = {{xstx}}$ and $y = {{ystx}}$. What is $\\partial z/\\partial s$ at $(s, t) = ({{s0}}, {{t0}})$?",
         value_part("∂z/∂s", "$\\dfrac{\\partial z}{\\partial s} = z_x\\dfrac{\\partial x}{\\partial s} + z_y\\dfrac{\\partial y}{\\partial s}$, holding $t$ fixed"),
         [c for c in cases if c["ans"] != 0], {"expect": {"a": "diff(SE(f).subs({SE('x'): SE(xs), SE('y'): SE(ys)}, simultaneous=True), SE('u')).subs({SE('u'): s0, SE('v'): t0})"}})

cases = []
for etex, F, px, py in [("x^2 + xy + y^3 = 7", "x**2 + x*y + y**3 - 7", 2, 1), ("x^3 + y^3 = 6xy", "x**3 + y**3 - 6*x*y", 3, 3),
                        ("e^{xy} = x + y", "exp(x*y) - x - y", 0, 1), ("x \\sin y + y = 1", "x*sin(y) + y - 1", 0, 1), ("x^2 y^2 + y = 6", "x**2*y**2 + y - 6", 1, 2)]:
    G = S(F)
    assert sp.simplify(G.subs({x: px, y: py})) == 0, etex
    val = -sp.diff(G, x).subs({x: px, y: py}) / sp.diff(G, y).subs({x: px, y: py})
    cases.append({"etex": etex, "F": F, "px": px, "py": py, "ans": N(val)})
template("mvd-implicit", "calc.multivariable", "The curve ${{etex}}$ passes through $({{px}}, {{py}})$. What is $dy/dx$ there?",
         value_part("dy/dx", "With $F(x, y) = 0$: $dy/dx = -F_x/F_y$ (move everything to one side first). It is the slope of the level curve $F = 0$"),
         [c for c in cases if c["ans"] != 0], {"expect": {"a": "-mv_at(mv_d(F, 'x'), px, py)/mv_at(mv_d(F, 'y'), px, py)"}})

cases = []
for ftex, f, px, py in [("x^3 - 3x + y^2", "x**3 - 3*x + y**2", 1, 0), ("x^3 - 3x + y^2", "x**3 - 3*x + y**2", -1, 0),
                        ("x^2 + xy + y^2 - 3x", "x**2 + x*y + y**2 - 3*x", 2, -1), ("x^3 + y^3 - 3xy", "x**3 + y**3 - 3*x*y", 0, 0),
                        ("x^3 + y^3 - 3xy", "x**3 + y**3 - 3*x*y", 1, 1), ("4xy - x^4 - y^4", "4*x*y - x**4 - y**4", 1, 1),
                        ("4xy - x^4 - y^4", "4*x*y - x**4 - y**4", 0, 0), ("x^4 + y^4", "x**4 + y**4", 0, 0),
                        ("2 - x^2 - y^2 + 2x", "2 - x**2 - y**2 + 2*x", 1, 0), ("e^{-(x^2 + y^2)}", "exp(-(x**2 + y**2))", 0, 0)]:
    F = S(f)
    fxx, fyy, fxy = (sp.diff(F, a, b).subs({x: px, y: py}) for a, b in ((x, x), (y, y), (x, y)))
    D = fxx * fyy - fxy ** 2
    k = (0 if fxx > 0 else 1) if D > 0 else (2 if D < 0 else 3)
    cases.append({"ftex": ftex, "f": f, "px": px, "py": py, "ans": k})
template("mvd-classify", "calc.partials-apps", "$({{px}}, {{py}})$ is a critical point of $f(x, y) = {{ftex}}$. What does the second derivatives test say?",
         choice_part("Classification", ["Local minimum", "Local maximum", "Saddle point", "The test is inconclusive (D = 0)"],
                     "$D = f_{xx}f_{yy} - f_{xy}^2$ at the point. $D > 0$: an extremum, a minimum if $f_{xx} > 0$ and a maximum if $f_{xx} < 0$. $D < 0$: a saddle. $D = 0$: no conclusion ($x^4 + y^4$ has a minimum there anyway)"),
         cases, {"choices": {"a": "crit_class(f, px, py)"}})

cases = []
for ftex, f in [("x^3 - 3x + y^2", "x**3 - 3*x + y**2"), ("x^3 + y^3 - 3xy", "x**3 + y**3 - 3*x*y"), ("4xy - x^4 - y^4", "4*x*y - x**4 - y**4"),
                ("x^2 + y^2 - 2x + 4y", "x**2 + y**2 - 2*x + 4*y"), ("x^3 - 12x + y^3 - 3y", "x**3 - 12*x + y**3 - 3*y"), ("x^2 y - x^2 - y^2", "x**2*y - x**2 - y**2")]:
    F = S(f)
    sols = [s for s in sp.solve([sp.diff(F, x), sp.diff(F, y)], [x, y], dict=True) if all(val.is_real for val in s.values())]
    cases.append({"ftex": ftex, "f": f, "ans": len(sols)})
template("mvd-critical-count", "calc.partials-apps", "How many critical points does $f(x, y) = {{ftex}}$ have?",
         value_part("Critical points", "Solve $f_x = 0$ and $f_y = 0$ together. Factor and split into cases; a product equal to zero gives a separate branch for each factor"),
         cases, {"expect": {"a": "n_critical(f)"}})

cases = []
for ftex, f, gtex, g, kind, three in [
        ("x + y", "x + y", "x^2 + y^2 = 2", "x**2 + y**2 - 2", 1, False), ("xy", "x*y", "x + y = 10", "x + y - 10", 1, False),
        ("x^2 + y^2", "x**2 + y**2", "x + 2y = 5", "x + 2*y - 5", 0, False), ("x + 2y + 2z", "x + 2*y + 2*z", "x^2 + y^2 + z^2 = 9", "x**2 + y**2 + z**2 - 9", 1, True),
        ("xyz", "x*y*z", "x + y + z = 12", "x + y + z - 12", 1, True), ("3x + 4y", "3*x + 4*y", "x^2 + y^2 = 25", "x**2 + y**2 - 25", 0, False),
        ("x^2 + y^2 + z^2", "x**2 + y**2 + z**2", "x + y + z = 3", "x + y + z - 3", 0, True), ("x^2 y", "x**2*y", "x^2 + y^2 = 3", "x**2 + y**2 - 3", 1, False)]:
    lam = sp.Symbol("lam")
    vs = [x, y, z] if three else [x, y]
    eqs = [sp.diff(S(f), w) - lam * sp.diff(S(g), w) for w in vs] + [S(g)]
    vals = [S(f).subs(s) for s in sp.solve(eqs, vs + [lam], dict=True) if all(s[w].is_real for w in vs)]
    val = max(vals) if kind == 1 else min(vals)
    cases.append({"ftex": ftex, "f": f, "gtex": gtex, "g": g, "kind": kind, "three": int(three), "ans": N(val)})
template("mvd-lagrange", "calc.partials-apps", "What is the {{kind == 1 ? \"maximum\" : \"minimum\"}} of ${{ftex}}$ subject to ${{gtex}}$?",
         value_part("Extreme value", "Solve $\\nabla f = \\lambda\\nabla g$ with $g = 0$, list every candidate, and compare the values of $f$. At the answer the level curve of $f$ is tangent to the constraint"),
         cases, {"expect": {"a": "lagrange(f, g, kind, three == 1)"}})

template("mvd-two-path", "calc.multivariable", "Does $\\displaystyle\\lim_{(x, y)\\to(0, 0)} {{ltex}}$ exist?",
         choice_part("Limit", ["It exists", "It does not exist"],
                     "Try paths: along $y = mx$ and along $y = x^2$. Different answers on two paths prove there is no limit; to prove a limit exists, bound the expression (often with polar coordinates: if it is $r$ times something bounded, the limit is 0)"),
         [{"ltex": "\\dfrac{xy}{x^2 + y^2}", "ans": 1}, {"ltex": "\\dfrac{x^2 y}{x^4 + y^2}", "ans": 1}, {"ltex": "\\dfrac{x^2 y}{x^2 + y^2}", "ans": 0},
          {"ltex": "\\dfrac{x^2 - y^2}{x^2 + y^2}", "ans": 1}, {"ltex": "\\dfrac{\\sin(x^2 + y^2)}{x^2 + y^2}", "ans": 0}, {"ltex": "\\dfrac{xy^2}{x^2 + y^2}", "ans": 0},
          {"ltex": "\\dfrac{x y^2}{x^2 + y^4}", "ans": 1}, {"ltex": "\\dfrac{3x^2 y}{x^2 + y^2}", "ans": 0}],
         {"authored": True})

template("mvd-gradient-facts", "calc.partials-apps", "True or false: {{s}}",
         choice_part("Answer", ["True", "False"], "The gradient points in the direction of fastest increase, has length equal to that rate, and is perpendicular to the level curve or surface through the point. Critical points are where it vanishes (or fails to exist)"),
         [{"s": "The gradient of f at a point is perpendicular to the level curve of f through that point.", "ans": 0},
          {"s": "The directional derivative in the direction of the gradient equals the length of the gradient.", "ans": 0},
          {"s": "The directional derivative along a level curve is zero.", "ans": 0},
          {"s": "At a saddle point the gradient is nonzero.", "ans": 1},
          {"s": "The gradient of f(x, y) is a vector in three-dimensional space.", "ans": 1},
          {"s": "If f_x and f_y exist at a point, f must be differentiable there.", "ans": 1},
          {"s": "A local maximum of a differentiable f has gradient zero.", "ans": 0},
          {"s": "Moving opposite to the gradient decreases f fastest.", "ans": 0}],
         {"authored": True}, pace="recall")

# ════════════════ unit 13 · multiple integrals ════════════════
rows = [
    ({"rtex": "the region between $y = x^2$ and $y = x$", "ftex": "xy"}, "Integral(x*y, (y, x**2, x), (x, 0, 1))",
     [("\\int_0^1\\!\\int_{x^2}^{x} xy\\,dy\\,dx", "Integral(x*y, (y, x**2, x), (x, 0, 1))"), ("\\int_0^1\\!\\int_{x}^{x^2} xy\\,dy\\,dx", "Integral(x*y, (y, x, x**2), (x, 0, 1))"),
      ("\\int_0^1\\!\\int_{0}^{\\sqrt{y}} xy\\,dx\\,dy", "Integral(x*y, (x, 0, sqrt(y)), (y, 0, 1))"), ("\\int_0^1\\!\\int_{0}^{x} xy\\,dy\\,dx", "Integral(x*y, (y, 0, x), (x, 0, 1))")]),
    ({"rtex": "the triangle with vertices $(0, 0)$, $(2, 0)$ and $(2, 1)$", "ftex": "y"}, "Integral(y, (y, 0, x/2), (x, 0, 2))",
     [("\\int_0^2\\!\\int_0^{2x} y\\,dy\\,dx", "Integral(y, (y, 0, 2*x), (x, 0, 2))"), ("\\int_0^1\\!\\int_{2y}^{2} y\\,dx\\,dy", "Integral(y, (x, 2*y, 2), (y, 0, 1))"),
      ("\\int_0^1\\!\\int_0^{2y} y\\,dx\\,dy", "Integral(y, (x, 0, 2*y), (y, 0, 1))"), ("\\int_0^2\\!\\int_0^{1} y\\,dy\\,dx", "Integral(y, (y, 0, 1), (x, 0, 2))")]),
    ({"rtex": "the region in the first quadrant inside $x^2 + y^2 = 4$", "ftex": "x"}, "Integral(x, (y, 0, sqrt(4 - x**2)), (x, 0, 2))",
     [("\\int_0^2\\!\\int_0^{4 - x^2} x\\,dy\\,dx", "Integral(x, (y, 0, 4 - x**2), (x, 0, 2))"), ("\\int_0^2\\!\\int_0^{2} x\\,dy\\,dx", "Integral(x, (y, 0, 2), (x, 0, 2))"),
      ("\\int_0^2\\!\\int_0^{\\sqrt{4 - y^2}} x\\,dx\\,dy", "Integral(x, (x, 0, sqrt(4 - y**2)), (y, 0, 2))"), ("\\int_{-2}^2\\!\\int_0^{\\sqrt{4 - x^2}} x\\,dy\\,dx", "Integral(x, (y, 0, sqrt(4 - x**2)), (x, -2, 2))")]),
    ({"rtex": "the region bounded by $y = \\sqrt{x}$, $y = 0$ and $x = 4$", "ftex": "1"}, "Integral(1, (y, 0, sqrt(x)), (x, 0, 4))",
     [("\\int_0^2\\!\\int_{0}^{y^2} dx\\,dy", "Integral(1, (x, 0, y**2), (y, 0, 2))"), ("\\int_0^4\\!\\int_{0}^{x^2} dy\\,dx", "Integral(1, (y, 0, x**2), (x, 0, 4))"),
      ("\\int_0^2\\!\\int_{y^2}^{4} dx\\,dy", "Integral(1, (x, y**2, 4), (y, 0, 2))"), ("\\int_0^4\\!\\int_{\\sqrt{x}}^{2} dy\\,dx", "Integral(1, (y, sqrt(x), 2), (x, 0, 4))")]),
    ({"rtex": "the region between $y = x^2$ and $y = 2x$", "ftex": "x"}, "Integral(x, (y, x**2, 2*x), (x, 0, 2))",
     [("\\int_0^4\\!\\int_{y/2}^{\\sqrt{y}} x\\,dx\\,dy", "Integral(x, (x, y/2, sqrt(y)), (y, 0, 4))"), ("\\int_0^4\\!\\int_{\\sqrt{y}}^{y/2} x\\,dx\\,dy", "Integral(x, (x, sqrt(y), y/2), (y, 0, 4))"),
      ("\\int_0^2\\!\\int_{2x}^{x^2} x\\,dy\\,dx", "Integral(x, (y, 2*x, x**2), (x, 0, 2))"), ("\\int_0^4\\!\\int_{x^2}^{2x} x\\,dy\\,dx", "Integral(x, (y, x**2, 2*x), (x, 0, 4))")]),
]
template("mvd-region-setup", "calc.multiple-integrals",
         "Which integral equals $\\displaystyle\\iint_D {{ftex}}\\,dA$ for $D$ = {{rtex}}?" + SETUP_PROMPT_TAIL,
         choice_part("Setup", ABCD, "Sketch $D$. For $dy\\,dx$, the inner limits are the bottom and top curves as functions of $x$, the outer limits the extreme $x$ values; for $dx\\,dy$, left and right curves as functions of $y$. The outer limits are always constants"),
         setup_cases(rows), SETUP_VERIFY)

rows = [
    ({"itex": "\\int_0^1\\!\\int_{x}^{1} f\\,dy\\,dx"}, "Integral(x**2*y, (y, x, 1), (x, 0, 1))",
     [("\\int_0^1\\!\\int_0^{y} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, y), (y, 0, 1))"), ("\\int_0^1\\!\\int_y^{1} f\\,dx\\,dy", "Integral(x**2*y, (x, y, 1), (y, 0, 1))"),
      ("\\int_0^1\\!\\int_0^{1} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, 1), (y, 0, 1))"), ("\\int_0^1\\!\\int_0^{x} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, 1 - y), (y, 0, 1))")]),
    ({"itex": "\\int_0^4\\!\\int_{\\sqrt{x}}^{2} f\\,dy\\,dx"}, "Integral(x**2*y, (y, sqrt(x), 2), (x, 0, 4))",
     [("\\int_0^2\\!\\int_{y^2}^{4} f\\,dx\\,dy", "Integral(x**2*y, (x, y**2, 4), (y, 0, 2))"), ("\\int_0^2\\!\\int_0^{y^2} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, y**2), (y, 0, 2))"),
      ("\\int_0^4\\!\\int_0^{y^2} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, y**2), (y, 0, 4))"), ("\\int_0^2\\!\\int_{0}^{\\sqrt{y}} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, sqrt(y)), (y, 0, 2))")]),
    ({"itex": "\\int_0^2\\!\\int_0^{2y} f\\,dx\\,dy"}, "Integral(x**2*y, (x, 0, 2*y), (y, 0, 2))",
     [("\\int_0^4\\!\\int_0^{x/2} f\\,dy\\,dx", "Integral(x**2*y, (y, 0, x/2), (x, 0, 4))"), ("\\int_0^4\\!\\int_{x/2}^{2} f\\,dy\\,dx", "Integral(x**2*y, (y, x/2, 2), (x, 0, 4))"),
      ("\\int_0^2\\!\\int_{x/2}^{2} f\\,dy\\,dx", "Integral(x**2*y, (y, x/2, 2), (x, 0, 2))"), ("\\int_0^4\\!\\int_{2x}^{2} f\\,dy\\,dx", "Integral(x**2*y, (y, 2*x, 2), (x, 0, 1))")]),
    ({"itex": "\\int_0^1\\!\\int_{y^2}^{y} f\\,dx\\,dy"}, "Integral(x**2*y, (x, y**2, y), (y, 0, 1))",
     [("\\int_0^1\\!\\int_{x^2}^{x} f\\,dy\\,dx", "Integral(x**2*y, (y, x**2, x), (x, 0, 1))"), ("\\int_0^1\\!\\int_{x}^{\\sqrt{x}} f\\,dy\\,dx", "Integral(x**2*y, (y, x, sqrt(x)), (x, 0, 1))"),
      ("\\int_0^1\\!\\int_{\\sqrt{x}}^{x} f\\,dy\\,dx", "Integral(x**2*y, (y, sqrt(x), x), (x, 0, 1))"), ("\\int_0^1\\!\\int_{0}^{\\sqrt{x}} f\\,dy\\,dx", "Integral(x**2*y, (y, 0, sqrt(x)), (x, 0, 1))")]),
    ({"itex": "\\int_0^{1}\\!\\int_{e^{x}}^{e} f\\,dy\\,dx"}, "Integral(x**2*y, (y, exp(x), E), (x, 0, 1))",
     [("\\int_1^{e}\\!\\int_{0}^{\\ln y} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, log(y)), (y, 1, E))"), ("\\int_0^{e}\\!\\int_{0}^{\\ln y} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, log(y)), (y, 1, E)) + 1"),
      ("\\int_1^{e}\\!\\int_{\\ln y}^{1} f\\,dx\\,dy", "Integral(x**2*y, (x, log(y), 1), (y, 1, E))"), ("\\int_1^{e}\\!\\int_{0}^{e^{y}} f\\,dx\\,dy", "Integral(x**2*y, (x, 0, 1), (y, 1, E))")]),
]
template("mvd-reverse-setup", "calc.multiple-integrals",
         "Reverse the order of integration in ${{itex}}$, where $f = x^2 y$. Which integral is it?" + SETUP_PROMPT_TAIL,
         choice_part("Reversed", ABCD, "Draw the region from the given limits, then slice the other way: the new outer limits are the extreme values of the other variable, and the inner limits are the curves solved for the inner variable"),
         setup_cases(rows), SETUP_VERIFY)

cases = []
for rtex, f, ftex, lims in [
        ("between $y = x^2$ and $y = 2x$", "x*y", "xy", "Integral(x*y, (y, x**2, 2*x), (x, 0, 2))"),
        ("between $y = x$ and $y = \\sqrt{x}$", "x", "x", "Integral(x, (y, x, sqrt(x)), (x, 0, 1))"),
        ("the triangle with vertices $(0, 0)$, $(1, 0)$, $(0, 2)$", "x + y", "x + y", "Integral(x + y, (y, 0, 2 - 2*x), (x, 0, 1))"),
        ("under $y = \\sin x$ for $0 \\le x \\le \\pi$", "y", "y", "Integral(y, (y, 0, sin(x)), (x, 0, pi))"),
        ("between $x = y^2$ and $x = 4$", "x", "x", "Integral(x, (x, y**2, 4), (y, -2, 2))"),
        ("bounded by $y = e^{x}$, $y = 1$ and $x = 1$", "1", "1", "Integral(1, (y, 1, exp(x)), (x, 0, 1))")]:
    cases.append({"rtex": rtex, "f": f, "ftex": ftex, "lims": lims, "ans": N(S(lims))})
template("mvd-region-value", "calc.multiple-integrals", "Evaluate $\\displaystyle\\iint_D {{ftex}}\\,dA$, where $D$ is the region {{rtex}}.",
         value_part("Value", "Sketch the region, choose the order that gives single curves as limits, do the inner integral with the outer variable held fixed"),
         cases, {"expect": {"a": "quad(lims)"}})

rows = [
    ({"rtex": "the disc $x^2 + y^2 \\le 9$", "ftex": "x^2 + y^2"}, "Integral((x**2 + y**2), (y, -sqrt(9 - x**2), sqrt(9 - x**2)), (x, -3, 3))",
     [("\\int_0^{2\\pi}\\!\\int_0^3 r^3\\,dr\\,d\\theta", "Integral(r**3, (r, 0, 3), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^3 r^2\\,dr\\,d\\theta", "Integral(r**2, (r, 0, 3), (theta, 0, 2*pi))"),
      ("\\int_0^{\\pi}\\!\\int_0^3 r^3\\,dr\\,d\\theta", "Integral(r**3, (r, 0, 3), (theta, 0, pi))"), ("\\int_0^{2\\pi}\\!\\int_0^9 r^3\\,dr\\,d\\theta", "Integral(r**3, (r, 0, 9), (theta, 0, 2*pi))")]),
    ({"rtex": "the upper half of the disc $x^2 + y^2 \\le 4$", "ftex": "y"}, "Integral(y, (y, 0, sqrt(4 - x**2)), (x, -2, 2))",
     [("\\int_0^{2\\pi}\\!\\int_0^2 r^2\\sin\\theta\\,dr\\,d\\theta", "Integral(r**2*sin(theta), (r, 0, 2), (theta, 0, 2*pi))"), ("\\int_0^{\\pi}\\!\\int_0^2 r\\sin\\theta\\,dr\\,d\\theta", "Integral(r*sin(theta), (r, 0, 2), (theta, 0, pi))"),
      ("\\int_0^{\\pi}\\!\\int_0^2 r^2\\sin\\theta\\,dr\\,d\\theta", "Integral(r**2*sin(theta), (r, 0, 2), (theta, 0, pi))"), ("\\int_0^{\\pi/2}\\!\\int_0^2 r^2\\sin\\theta\\,dr\\,d\\theta", "Integral(r**2*sin(theta), (r, 0, 2), (theta, 0, pi/2))")]),
    ({"rtex": "the annulus $1 \\le x^2 + y^2 \\le 4$", "ftex": "1"}, "pi*4 - pi*1",
     [("\\int_0^{2\\pi}\\!\\int_1^2 r\\,dr\\,d\\theta", "Integral(r, (r, 1, 2), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_1^4 r\\,dr\\,d\\theta", "Integral(r, (r, 1, 4), (theta, 0, 2*pi))"),
      ("\\int_0^{2\\pi}\\!\\int_1^2 dr\\,d\\theta", "Integral(1, (r, 1, 2), (theta, 0, 2*pi))"), ("\\int_0^{\\pi}\\!\\int_1^2 r\\,dr\\,d\\theta", "Integral(r, (r, 1, 2), (theta, 0, pi))")]),
    ({"rtex": "the disc inside $r = 2\\cos\\theta$ (the circle $(x - 1)^2 + y^2 = 1$)", "ftex": "1"}, "pi",
     [("\\int_0^{2\\pi}\\!\\int_0^{2\\cos\\theta} r\\,dr\\,d\\theta", "Integral(r, (r, 0, 2*cos(theta)), (theta, 0, 2*pi))"), ("\\int_{-\\pi/2}^{\\pi/2}\\!\\int_0^{2\\cos\\theta} r\\,dr\\,d\\theta", "Integral(r, (r, 0, 2*cos(theta)), (theta, -pi/2, pi/2))"),
      ("\\int_{-\\pi/2}^{\\pi/2}\\!\\int_0^{2\\cos\\theta} dr\\,d\\theta", "Integral(1, (r, 0, 2*cos(theta)), (theta, -pi/2, pi/2))"), ("\\int_0^{\\pi/2}\\!\\int_0^{2\\cos\\theta} r\\,dr\\,d\\theta", "Integral(r, (r, 0, 2*cos(theta)), (theta, 0, pi/2))")]),
    ({"rtex": "the first-quadrant part of the disc $x^2 + y^2 \\le 1$", "ftex": "e^{x^2 + y^2}"}, "Integral(exp(x**2 + y**2), (y, 0, sqrt(1 - x**2)), (x, 0, 1))",
     [("\\int_0^{\\pi/2}\\!\\int_0^1 e^{r^2}\\,dr\\,d\\theta", "Integral(exp(r**2), (r, 0, 1), (theta, 0, pi/2))"), ("\\int_0^{2\\pi}\\!\\int_0^1 r e^{r^2}\\,dr\\,d\\theta", "Integral(r*exp(r**2), (r, 0, 1), (theta, 0, 2*pi))"),
      ("\\int_0^{\\pi/2}\\!\\int_0^1 r e^{r^2}\\,dr\\,d\\theta", "Integral(r*exp(r**2), (r, 0, 1), (theta, 0, pi/2))"), ("\\int_0^{\\pi}\\!\\int_0^1 r e^{r^2}\\,dr\\,d\\theta", "Integral(r*exp(r**2), (r, 0, 1), (theta, 0, pi))")]),
]
template("mvd-polar-setup", "calc.multiple-integrals",
         "Which polar integral equals $\\displaystyle\\iint_D {{ftex}}\\,dA$ for $D$ = {{rtex}}?" + SETUP_PROMPT_TAIL,
         choice_part("Setup", ABCD, "Use $x = r\\cos\\theta$, $y = r\\sin\\theta$, $x^2 + y^2 = r^2$ and $dA = r\\,dr\\,d\\theta$. The θ range covers the region once: a full disc is $0$ to $2\\pi$, the circle $r = 2\\cos\\theta$ is traced once for $-\\pi/2 \\le \\theta \\le \\pi/2$"),
         setup_cases(rows), SETUP_VERIFY)

cases = []
for rtex, ftex, polar, cart in [
        ("the disc $x^2 + y^2 \\le 4$", "e^{-(x^2 + y^2)}", "Integral(r*exp(-r**2), (r, 0, 2), (theta, 0, 2*pi))", "Integral(exp(-(x**2 + y**2)), (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))"),
        ("the annulus $1 \\le x^2 + y^2 \\le 9$", "\\dfrac{1}{x^2 + y^2}", "Integral(1/r, (r, 1, 3), (theta, 0, 2*pi))", "2*pi*log(3)"),
        ("the upper half of $x^2 + y^2 \\le 9$", "\\sqrt{x^2 + y^2}", "Integral(r**2, (r, 0, 3), (theta, 0, pi))", "Integral(sqrt(x**2 + y**2), (y, 0, sqrt(9 - x**2)), (x, -3, 3))"),
        ("the first-quadrant part of $x^2 + y^2 \\le 4$", "xy", "Integral(r**3*cos(theta)*sin(theta), (r, 0, 2), (theta, 0, pi/2))", "Integral(x*y, (y, 0, sqrt(4 - x**2)), (x, 0, 2))"),
        ("the disc inside $r = 2\\cos\\theta$", "x", "Integral(r**2*cos(theta), (r, 0, 2*cos(theta)), (theta, -pi/2, pi/2))", "Integral(x, (y, -sqrt(1 - (x - 1)**2), sqrt(1 - (x - 1)**2)), (x, 0, 2))"),
        ("the region inside the cardioid $r = 1 + \\cos\\theta$", "1", "Integral(r, (r, 0, 1 + cos(theta)), (theta, 0, 2*pi))", "3*pi/2")]:
    val = N(S(polar).subs({}) if False else sp.sympify(polar, locals={"r": r, "theta": th, "pi": sp.pi}))
    cases.append({"rtex": rtex, "ftex": ftex, "cart": cart, "ans": val})
template("mvd-polar-value", "calc.multiple-integrals", "Evaluate $\\displaystyle\\iint_D {{ftex}}\\,dA$ over {{rtex}}.",
         value_part("Value", "Switch to polar: $dA = r\\,dr\\,d\\theta$, and $x^2 + y^2 = r^2$. The extra factor of $r$ is what makes $e^{-r^2}$ integrable"),
         cases, {"expect": {"a": "quad(cart)"}})

template("mvd-coordinates", "calc.multiple-integrals", "Which coordinates make this integral easiest: {{s}}?",
         choice_part("Coordinates", ["Rectangular (x, y, z)", "Cylindrical (r, θ, z)", "Spherical (ρ, φ, θ)"],
                     "Match the coordinates to the boundary: planes and boxes, rectangular; anything with x² + y² (cylinders, paraboloids, discs extruded upward), cylindrical; anything with x² + y² + z² or a cone from the origin (balls, shells, ice-cream cones), spherical"),
         [{"s": "the volume of the box 0 ≤ x ≤ 2, 0 ≤ y ≤ 3, 0 ≤ z ≤ 1", "ans": 0}, {"s": "the mass of a solid ball with density depending on distance from the center", "ans": 2},
          {"s": "the volume under z = 4 − x² − y² and above z = 0", "ans": 1}, {"s": "the volume inside the cylinder x² + y² = 1 between z = 0 and z = 2", "ans": 1},
          {"s": "the volume of the ice-cream cone inside x² + y² + z² = 4 and above z = √(x² + y²)", "ans": 2},
          {"s": "the volume of the tetrahedron x + y + z ≤ 1 in the first octant", "ans": 0}, {"s": "the integral of z over the spherical shell 1 ≤ ρ ≤ 2", "ans": 2},
          {"s": "the volume between the paraboloids z = x² + y² and z = 8 − x² − y²", "ans": 1}],
         {"authored": True}, pace="recall")

cases = []
for xs, ys, xtex, ytex in [("(u + v)/2", "(u - v)/2", "x = \\tfrac{u + v}{2}", "y = \\tfrac{u - v}{2}"), ("2*u", "3*v", "x = 2u", "y = 3v"),
                           ("u*cos(v)", "u*sin(v)", "x = u\\cos v", "y = u\\sin v"), ("u + v", "v", "x = u + v", "y = v"),
                           ("u/v", "v", "x = u/v", "y = v"), ("2*u - v", "u + 3*v", "x = 2u - v", "y = u + 3v")]:
    X, Y = S(xs), S(ys)
    J = sp.Abs(sp.simplify(sp.Matrix([[X.diff(u), X.diff(v)], [Y.diff(u), Y.diff(v)]]).det()))
    cases.append({"xtex": xtex, "ytex": ytex, "xs": xs, "ys": ys, "ans": N(J.subs({u: 2, v: 1}))})
template("mvd-jacobian", "calc.multiple-integrals",
         "For the change of variables ${{xtex}}$, ${{ytex}}$, what is the area factor $\\left|\\partial(x, y)/\\partial(u, v)\\right|$ at $(u, v) = (2, 1)$?",
         value_part("Jacobian", "$dA = |J|\\,du\\,dv$ with $J = x_u y_v - x_v y_u$. For $x = u\\cos v$, $y = u\\sin v$ it is $u$: polar coordinates' extra $r$. A linear map scales every area by the same $|\\det|$"),
         cases, {"expect": {"a": "jac(xs, ys).subs({SE('u'): 2, SE('v'): 1})"}})

rows = [
    ({"stex": "the tetrahedron $x, y, z \\ge 0$, $x + y + z \\le 1$"}, "Rational(1, 6)",
     [("\\int_0^1\\!\\int_0^{1-x}\\!\\int_0^{1-x-y} dz\\,dy\\,dx", "Integral(1, (z, 0, 1 - x - y), (y, 0, 1 - x), (x, 0, 1))"), ("\\int_0^1\\!\\int_0^{1}\\!\\int_0^{1-x-y} dz\\,dy\\,dx", "Integral(1, (z, 0, Max(0, 1 - x - y)), (y, 0, 1), (x, 0, 1)) + 1/10"),
      ("\\int_0^1\\!\\int_0^{1-x}\\!\\int_0^{1} dz\\,dy\\,dx", "Integral(1, (z, 0, 1), (y, 0, 1 - x), (x, 0, 1))"), ("\\int_0^1\\!\\int_0^{1}\\!\\int_0^{1} dz\\,dy\\,dx", "1")]),
    ({"stex": "the solid under $z = 4 - x^2 - y^2$ and above $z = 0$"}, "8*pi",
     [("\\int_0^{2\\pi}\\!\\int_0^2\\!\\int_0^{4 - r^2} r\\,dz\\,dr\\,d\\theta", "Integral(r, (z, 0, 4 - r**2), (r, 0, 2), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^2\\!\\int_0^{4 - r^2} dz\\,dr\\,d\\theta", "Integral(1, (z, 0, 4 - r**2), (r, 0, 2), (theta, 0, 2*pi))"),
      ("\\int_0^{2\\pi}\\!\\int_0^4\\!\\int_0^{4 - r^2} r\\,dz\\,dr\\,d\\theta", "Integral(r, (z, 0, 4 - r**2), (r, 0, 4), (theta, 0, 2*pi))"), ("\\int_0^{\\pi}\\!\\int_0^2\\!\\int_0^{4 - r^2} r\\,dz\\,dr\\,d\\theta", "Integral(r, (z, 0, 4 - r**2), (r, 0, 2), (theta, 0, pi))")]),
    ({"stex": "the ball $x^2 + y^2 + z^2 \\le 9$"}, "4*pi*27/3",
     [("\\int_0^{2\\pi}\\!\\int_0^{\\pi}\\!\\int_0^3 \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2*sin(phi), (rho, 0, 3), (phi, 0, pi), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^{2\\pi}\\!\\int_0^3 \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2*Abs(sin(phi)), (rho, 0, 3), (phi, 0, 2*pi), (theta, 0, 2*pi))"),
      ("\\int_0^{2\\pi}\\!\\int_0^{\\pi}\\!\\int_0^3 \\rho\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho*sin(phi), (rho, 0, 3), (phi, 0, pi), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^{\\pi}\\!\\int_0^3 \\rho^2\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2, (rho, 0, 3), (phi, 0, pi), (theta, 0, 2*pi))")]),
    ({"stex": "the ice-cream cone inside $\\rho = 2$ and above the cone $\\varphi = \\pi/4$"}, "Integral(rho**2*sin(phi), (rho, 0, 2), (phi, 0, pi/4), (theta, 0, 2*pi))",
     [("\\int_0^{2\\pi}\\!\\int_{\\pi/4}^{\\pi}\\!\\int_0^2 \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2*sin(phi), (rho, 0, 2), (phi, pi/4, pi), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^{\\pi/4}\\!\\int_0^2 \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2*sin(phi), (rho, 0, 2), (phi, 0, pi/4), (theta, 0, 2*pi))"),
      ("\\int_0^{\\pi/4}\\!\\int_0^{2\\pi}\\!\\int_0^2 \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho**2*Abs(sin(phi)), (rho, 0, 2), (phi, 0, 2*pi), (theta, 0, pi/4))"), ("\\int_0^{2\\pi}\\!\\int_0^{\\pi/4}\\!\\int_0^2 \\rho\\,d\\rho\\,d\\varphi\\,d\\theta", "Integral(rho, (rho, 0, 2), (phi, 0, pi/4), (theta, 0, 2*pi))")]),
    ({"stex": "the cylinder $x^2 + y^2 \\le 9$, $0 \\le z \\le 3$, with density $z$"}, "Integral(z, (z, 0, 3), (y, -sqrt(9 - x**2), sqrt(9 - x**2)), (x, -3, 3))",
     [("\\int_0^{2\\pi}\\!\\int_0^3\\!\\int_0^3 z\\,dz\\,dr\\,d\\theta", "Integral(z, (z, 0, 3), (r, 0, 3), (theta, 0, 2*pi))"), ("\\int_0^{2\\pi}\\!\\int_0^3\\!\\int_0^3 zr\\,dz\\,dr\\,d\\theta", "Integral(z*r, (z, 0, 3), (r, 0, 3), (theta, 0, 2*pi))"),
      ("\\int_0^{2\\pi}\\!\\int_0^9\\!\\int_0^3 zr\\,dz\\,dr\\,d\\theta", "Integral(z*r, (z, 0, 3), (r, 0, 9), (theta, 0, 2*pi))"), ("\\int_0^{\\pi}\\!\\int_0^3\\!\\int_0^3 zr\\,dz\\,dr\\,d\\theta", "Integral(z*r, (z, 0, 3), (r, 0, 3), (theta, 0, pi))")]),
]
def rename(e):
    """setup strings in r, theta, rho, phi -> the verifier's x, u, t, v (sympify-safe names)"""
    import re
    e = re.sub(r"\btheta\b", "u", e)
    e = re.sub(r"\brho\b", "t", e)
    e = re.sub(r"\bphi\b", "v", e)
    e = re.sub(r"\br\b", "x", e)
    return e


trip = [(c, rename(tg) if "Integral" in tg else tg, [(tx, rename(e)) for tx, e in opts]) for c, tg, opts in rows]
template("mvd-triple-setup", "calc.multiple-integrals",
         "Which integral gives the volume (or the mass, where a density is given) of {{stex}}?" + SETUP_PROMPT_TAIL,
         choice_part("Setup", ABCD, "Cylindrical: $dV = r\\,dz\\,dr\\,d\\theta$. Spherical: $dV = \\rho^2\\sin\\varphi\\,d\\rho\\,d\\varphi\\,d\\theta$ with $0 \\le \\varphi \\le \\pi$ measured down from the $+z$ axis. Rectangular: inner limits are surfaces, middle limits curves, outer limits numbers"),
         setup_cases(trip), SETUP_VERIFY)

cases = []
for stex, card, check in [
        ("the solid under $z = 4 - x^2 - y^2$ and above the $xy$-plane", "Integral(r*(4 - r**2), (r, 0, 2), (theta, 0, 2*pi))", "Integral(4 - x**2 - y**2, (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))"),
        ("the ice-cream cone inside $x^2 + y^2 + z^2 = 4$ and above $z = \\sqrt{x^2 + y^2}$", "Integral(rho**2*sin(phi), (rho, 0, 2), (phi, 0, pi/4), (theta, 0, 2*pi))", "Integral(2*pi*x*(sqrt(4 - x**2) - x), (x, 0, sqrt(2)))"),
        ("the region between $z = x^2 + y^2$ and $z = 8 - x^2 - y^2$", "Integral(r*(8 - 2*r**2), (r, 0, 2), (theta, 0, 2*pi))", "Integral(8 - 2*x**2 - 2*y**2, (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))"),
        ("the spherical shell $1 \\le x^2 + y^2 + z^2 \\le 4$", "Integral(rho**2*sin(phi), (rho, 1, 2), (phi, 0, pi), (theta, 0, 2*pi))", "4*pi*(8 - 1)/3"),
        ("the solid inside $x^2 + y^2 = 1$ between $z = 0$ and $z = 2 - x$", "Integral(r*(2 - r*cos(theta)), (r, 0, 1), (theta, 0, 2*pi))", "Integral(2 - x, (y, -sqrt(1 - x**2), sqrt(1 - x**2)), (x, -1, 1))"),
        ("the tetrahedron bounded by the coordinate planes and $2x + 3y + z = 6$", "Integral(6 - 2*x - 3*y, (y, 0, (6 - 2*x)/3), (x, 0, 3))", "6"),
        ("the solid inside the cone $z = \\sqrt{x^2 + y^2}$ below $z = 3$", "Integral(r*(3 - r), (r, 0, 3), (theta, 0, 2*pi))", "pi*9*3/3")]:
    val = N(sp.sympify(card, locals={"r": r, "theta": th, "rho": rho, "phi": ph, "pi": sp.pi}))
    cases.append({"stex": stex, "check": check, "ans": val})
template("mvd-triple-value", "calc.multiple-integrals", "Find the volume of {{stex}}.",
         value_part("Volume", "Choose the coordinates that match the boundaries, find where the surfaces meet (that sets the outer region), and include the volume factor ($r$ or $\\rho^2\\sin\\varphi$)"),
         cases, {"expect": {"a": "quad(check)"}})

cases = []
for ltex, dens, region, comp, ans in [
        ("the upper half disc $x^2 + y^2 \\le 9$, $y \\ge 0$, uniform density", "1", "half disc radius 3", "ybar", 4 * 3 / (3 * sp.pi)),
        ("the triangle with vertices $(0, 0)$, $(3, 0)$, $(0, 3)$, uniform density", "1", "", "xbar", 1),
        ("the square $0 \\le x \\le 2$, $0 \\le y \\le 2$ with density $x$", "x", "", "xbar", sp.Rational(4, 3)),
        ("the region under $y = x^2$ for $0 \\le x \\le 1$, uniform density", "1", "", "xbar", sp.Rational(3, 4)),
        ("the region under $y = x^2$ for $0 \\le x \\le 1$, uniform density", "1", "", "ybar", sp.Rational(3, 10)),
        ("the quarter disc $x^2 + y^2 \\le 4$ in the first quadrant, uniform density", "1", "", "xbar", 8 / (3 * sp.pi))]:
    cases.append({"ltex": ltex, "comp": comp, "ans": N(ans)})
checks = {
    "the upper half disc $x^2 + y^2 \\le 9$, $y \\ge 0$, uniform density": "Integral(y, (y, 0, sqrt(9 - x**2)), (x, -3, 3))/Integral(1, (y, 0, sqrt(9 - x**2)), (x, -3, 3))",
    "the triangle with vertices $(0, 0)$, $(3, 0)$, $(0, 3)$, uniform density": "Integral(x, (y, 0, 3 - x), (x, 0, 3))/Integral(1, (y, 0, 3 - x), (x, 0, 3))",
    "the square $0 \\le x \\le 2$, $0 \\le y \\le 2$ with density $x$": "Integral(x*x, (y, 0, 2), (x, 0, 2))/Integral(x, (y, 0, 2), (x, 0, 2))",
    "the quarter disc $x^2 + y^2 \\le 4$ in the first quadrant, uniform density": "Integral(x, (y, 0, sqrt(4 - x**2)), (x, 0, 2))/Integral(1, (y, 0, sqrt(4 - x**2)), (x, 0, 2))",
}
for c in cases:
    if c["ltex"].startswith("the region under"):
        c["check"] = ("Integral(x, (y, 0, x**2), (x, 0, 1))/Integral(1, (y, 0, x**2), (x, 0, 1))" if c["comp"] == "xbar"
                      else "Integral(y, (y, 0, x**2), (x, 0, 1))/Integral(1, (y, 0, x**2), (x, 0, 1))")
    else:
        c["check"] = checks[c["ltex"]]
    c["ck"] = 0 if c["comp"] == "xbar" else 1
    del c["comp"]
template("mvd-center-mass", "calc.multiple-integrals", "Find {{ck == 0 ? \"x̄\" : \"ȳ\"}}, the center-of-mass coordinate, for {{ltex}}.",
         value_part("Coordinate", "$\\bar x = \\dfrac{1}{M}\\iint x\\,\\delta\\,dA$, $\\bar y = \\dfrac{1}{M}\\iint y\\,\\delta\\,dA$, $M = \\iint\\delta\\,dA$. Use symmetry first: a coordinate on an axis of symmetry is known without integrating"),
         cases, {"expect": {"a": "quad(check)"}})

# ════════════════ unit 14 · vector calculus ════════════════
cases = []
for Ftex, P, Q, R in [
        ("\\langle 2xy,\\ x^2 \\rangle", "2*x*y", "x**2", "0"), ("\\langle y,\\ -x \\rangle", "y", "-x", "0"), ("\\langle e^{x}\\cos y,\\ -e^{x}\\sin y \\rangle", "exp(x)*cos(y)", "-exp(x)*sin(y)", "0"),
        ("\\langle x + y,\\ x - y \\rangle", "x + y", "x - y", "0"), ("\\langle y^2,\\ xy \\rangle", "y**2", "x*y", "0"), ("\\langle 3x^2 y,\\ x^3 + 2y \\rangle", "3*x**2*y", "x**3 + 2*y", "0"),
        ("\\langle yz,\\ xz,\\ xy \\rangle", "y*z", "x*z", "x*y"), ("\\langle y,\\ z,\\ x \\rangle", "y", "z", "x"), ("\\langle 2x,\\ 2y,\\ 2z \\rangle", "2*x", "2*y", "2*z"),
        ("\\langle y,\\ x + z,\\ y \\rangle", "y", "x + z", "y"), ("\\langle z,\\ 0,\\ -x \\rangle", "z", "0", "-x")]:
    c = [sp.diff(S(R), y) - sp.diff(S(Q), z), sp.diff(S(P), z) - sp.diff(S(R), x), sp.diff(S(Q), x) - sp.diff(S(P), y)]
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "ans": 0 if all(sp.simplify(k) == 0 for k in c) else 1})
template("mvd-conservative", "calc.vector-calculus", "Is $\\mathbf F = {{Ftex}}$ conservative (on all of space)?",
         choice_part("Conservative?", ["Yes: curl F = 0 on a simply connected domain", "No"],
                     "In the plane, test $\\partial Q/\\partial x = \\partial P/\\partial y$; in space, test curl F = 0. On a simply connected domain that is enough for a potential to exist"),
         cases, {"choices": {"a": "is_conservative(P, Q, R)"}})

cases = []
for Ftex, P, Q, R, A, B, rx, ry, rz in [
        ("\\langle 2xy,\\ x^2 \\rangle", "2*x*y", "x**2", "0", "(0, 0)", "(2, 3)", "2*t", "3*t", "0"),
        ("\\langle e^{x}\\cos y,\\ -e^{x}\\sin y \\rangle", "exp(x)*cos(y)", "-exp(x)*sin(y)", "0", "(0, 0)", "(1, \\pi)", "t", "pi*t", "0"),
        ("\\langle 3x^2 y,\\ x^3 + 2y \\rangle", "3*x**2*y", "x**3 + 2*y", "0", "(1, 1)", "(2, 3)", "1 + t", "1 + 2*t", "0"),
        ("\\langle yz,\\ xz,\\ xy \\rangle", "y*z", "x*z", "x*y", "(0, 0, 0)", "(1, 2, 3)", "t", "2*t", "3*t"),
        ("\\langle 2x,\\ 2y,\\ 2z \\rangle", "2*x", "2*y", "2*z", "(1, 0, 0)", "(0, 2, 2)", "1 - t", "2*t", "2*t"),
        ("\\langle y,\\ x + z,\\ y \\rangle", "y", "x + z", "y", "(0, 0, 0)", "(1, 1, 1)", "t", "t", "t")]:
    val = line_val = sp.integrate(sum(S(c).subs({x: S(rx), y: S(ry), z: S(rz)}, simultaneous=True) * sp.diff(S(ri), t) for c, ri in zip((P, Q, R), (rx, ry, rz))), (t, 0, 1))
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "A": A, "B": B, "rx": rx, "ry": ry, "rz": rz, "ans": N(val)})
template("mvd-potential-work", "calc.vector-calculus",
         "$\\mathbf F = {{Ftex}}$ is conservative. What is $\\displaystyle\\int_C \\mathbf F\\cdot d\\mathbf r$ along any path from ${{A}}$ to ${{B}}$?",
         value_part("Work", "Find a potential $f$ with $\\nabla f = \\mathbf F$ (integrate $P$ in $x$, then fix the constant with $Q$ and $R$). Then the work is $f(B) - f(A)$, whatever the path"),
         cases, {"expect": {"a": "line_work(P, Q, R, rx, ry, rz, 0, 1)"}})

cases = []
for Ftex, P, Q, ctex, rx, ry, t0, t1 in [
        ("\\langle -y,\\ x \\rangle", "-y", "x", "the quarter circle $x^2 + y^2 = 4$ from $(2, 0)$ to $(0, 2)$, counterclockwise", "2*cos(t)", "2*sin(t)", "0", "pi/2"),
        ("\\langle y,\\ x^2 \\rangle", "y", "x**2", "the parabola $y = x^2$ from $(0, 0)$ to $(1, 1)$", "t", "t**2", "0", "1"),
        ("\\langle y,\\ x^2 \\rangle", "y", "x**2", "the straight segment from $(0, 0)$ to $(1, 1)$", "t", "t", "0", "1"),
        ("\\langle xy,\\ y^2 \\rangle", "x*y", "y**2", "the segment from $(0, 0)$ to $(2, 1)$", "2*t", "t", "0", "1"),
        ("\\langle y^2,\\ x \\rangle", "y**2", "x", "the upper half of the unit circle from $(1, 0)$ to $(-1, 0)$", "cos(t)", "sin(t)", "0", "pi"),
        ("\\langle x - y,\\ x + y \\rangle", "x - y", "x + y", "the full circle $x^2 + y^2 = 9$, counterclockwise", "3*cos(t)", "3*sin(t)", "0", "2*pi")]:
    val = sp.integrate(sp.simplify(S(P).subs({x: S(rx), y: S(ry)}, simultaneous=True) * sp.diff(S(rx), t) + S(Q).subs({x: S(rx), y: S(ry)}, simultaneous=True) * sp.diff(S(ry), t)), (t, S(t0), S(t1)))
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "ctex": ctex, "rx": rx, "ry": ry, "t0": t0, "t1": t1, "ans": N(val)})
template("mvd-work", "calc.vector-calculus", "Compute $\\displaystyle\\int_C \\mathbf F\\cdot d\\mathbf r$ for $\\mathbf F = {{Ftex}}$ along {{ctex}}.",
         value_part("Work", "Parametrise $C$ as $\\mathbf r(t)$, then integrate $\\mathbf F(\\mathbf r(t))\\cdot\\mathbf r'(t)\\,dt$. For a field that is not conservative, different paths between the same points give different answers (compare the parabola and the segment)"),
         cases, {"expect": {"a": "line_work(P, Q, '0', rx, ry, '0', t0, t1)"}})

cases = []
for ftex, f, ctex, rx, ry, rz, t0, t1 in [
        ("x + y", "x + y", "the segment from $(0, 0)$ to $(3, 4)$", "3*t", "4*t", "0", "0", "1"),
        ("x^2 + y^2", "x**2 + y**2", "the circle of radius 2 about the origin", "2*cos(t)", "2*sin(t)", "0", "0", "2*pi"),
        ("z", "z", "the helix $\\langle\\cos t, \\sin t, t\\rangle$, $0 \\le t \\le 2\\pi$", "cos(t)", "sin(t)", "t", "0", "2*pi"),
        ("y", "y", "the upper half of the unit circle", "cos(t)", "sin(t)", "0", "0", "pi"),
        ("xy", "x*y", "the quarter circle of radius 3 in the first quadrant", "3*cos(t)", "3*sin(t)", "0", "0", "pi/2"),
        ("1", "1", "the curve $\\langle t^2, t^3 \\rangle$, $0 \\le t \\le 1$ (its length)", "t**2", "t**3", "0", "0", "1")]:
    rv = [S(rx), S(ry), S(rz)]
    val = sp.integrate(sp.simplify(S(f).subs({x: rv[0], y: rv[1], z: rv[2]}, simultaneous=True) * sp.sqrt(sum(sp.diff(k, t) ** 2 for k in rv))), (t, S(t0), S(t1)))
    cases.append({"ftex": ftex, "f": f, "ctex": ctex, "rx": rx, "ry": ry, "rz": rz, "t0": t0, "t1": t1, "ans": N(val)})
template("mvd-scalar-line", "calc.vector-calculus", "Compute $\\displaystyle\\int_C {{ftex}}\\,ds$ along {{ctex}}.",
         value_part("Integral", "$ds = |\\mathbf r'(t)|\\,dt$: the speed, not $dt$. A scalar line integral does not depend on direction; $\\int_C ds$ is the length"),
         cases, {"expect": {"a": "line_scalar(f, rx, ry, rz, t0, t1)"}})

cases = []
for Ftex, P, Q, ctex, green, pieces in [
        ("\\langle -y,\\ x \\rangle", "-y", "x", "the circle of radius 3, counterclockwise", "Integral(2*r, (r, 0, 3), (theta, 0, 2*pi))", "3*cos(t)|3*sin(t)|0|2*pi"),
        ("\\langle xy,\\ x^2 \\rangle", "x*y", "x**2", "the boundary of the square $[0, 1]\\times[0, 1]$, counterclockwise", "Integral(x, (x, 0, 1), (y, 0, 1))", "t|0|0|1;1|t|0|1;1 - t|1|0|1;0|1 - t|0|1"),
        ("\\langle y^2,\\ 3xy \\rangle", "y**2", "3*x*y", "the boundary of the triangle $(0, 0)$, $(1, 0)$, $(0, 1)$, counterclockwise", "Integral(y, (y, 0, 1 - x), (x, 0, 1))", "t|0|0|1;1 - t|t|0|1;0|1 - t|0|1"),
        ("\\langle x - y,\\ x + y \\rangle", "x - y", "x + y", "the circle of radius 2, counterclockwise", "Integral(2*r, (r, 0, 2), (theta, 0, 2*pi))", "2*cos(t)|2*sin(t)|0|2*pi"),
        ("\\langle -y^3,\\ x^3 \\rangle", "-y**3", "x**3", "the unit circle, counterclockwise", "Integral(3*r**3, (r, 0, 1), (theta, 0, 2*pi))", "cos(t)|sin(t)|0|2*pi"),
        ("\\langle e^{x} - y,\\ \\cos y + 2x \\rangle", "exp(x) - y", "cos(y) + 2*x", "the ellipse $x^2/4 + y^2 = 1$, counterclockwise", "3*pi*2*1", "2*cos(t)|sin(t)|0|2*pi"),
        ("\\langle -y,\\ x \\rangle", "-y", "x", "the circle of radius 3, clockwise", "-Integral(2*r, (r, 0, 3), (theta, 0, 2*pi))", "3*cos(t)|-3*sin(t)|0|2*pi")]:
    val = N(sp.sympify(green, locals={"r": r, "theta": th, "pi": sp.pi}))
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "ctex": ctex, "pieces": pieces, "ans": val})
template("mvd-green", "calc.vector-calculus", "Use Green's theorem to find $\\displaystyle\\oint_C \\mathbf F\\cdot d\\mathbf r$ for $\\mathbf F = {{Ftex}}$ around {{ctex}}.",
         value_part("Circulation", "$\\oint_C P\\,dx + Q\\,dy = \\iint_D (Q_x - P_y)\\,dA$ for $C$ counterclockwise (the region on the left); clockwise flips the sign. When $Q_x - P_y$ is constant, the answer is that constant times the area"),
         cases, {"expect": {"a": "closed_work(P, Q, pieces)"}})

cases = []
for Ftex, P, Q, ctex, div_int, pieces in [
        ("\\langle x,\\ y \\rangle", "x", "y", "the circle of radius 2", "2*pi*4", "2*cos(t)|2*sin(t)|0|2*pi"),
        ("\\langle x^2,\\ y^2 \\rangle", "x**2", "y**2", "the boundary of the square $[0, 1]\\times[0, 1]$", "Integral(2*x + 2*y, (x, 0, 1), (y, 0, 1))", "t|0|0|1;1|t|0|1;1 - t|1|0|1;0|1 - t|0|1"),
        ("\\langle 3x,\\ -y \\rangle", "3*x", "-y", "the circle of radius 3", "2*pi*9", "3*cos(t)|3*sin(t)|0|2*pi"),
        ("\\langle xy,\\ y \\rangle", "x*y", "y", "the boundary of the triangle $(0, 0)$, $(2, 0)$, $(0, 2)$", "Integral(y + 1, (y, 0, 2 - x), (x, 0, 2))", "2*t|0|0|1;2 - 2*t|2*t|0|1;0|2 - 2*t|0|1"),
        ("\\langle x^3,\\ y^3 \\rangle", "x**3", "y**3", "the unit circle", "Integral(3*r**3, (r, 0, 1), (theta, 0, 2*pi))", "cos(t)|sin(t)|0|2*pi")]:
    val = N(sp.sympify(div_int, locals={"r": r, "theta": th, "pi": sp.pi}))
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "ctex": ctex, "pieces": pieces, "ans": val})
template("mvd-flux-plane", "calc.vector-calculus", "Find the outward flux of $\\mathbf F = {{Ftex}}$ across {{ctex}}.",
         value_part("Flux", "Green's theorem in flux form: $\\oint_C \\mathbf F\\cdot\\mathbf n\\,ds = \\oint_C P\\,dy - Q\\,dx = \\iint_D (P_x + Q_y)\\,dA$, the divergence summed over the inside"),
         cases, {"expect": {"a": "closed_flux2(P, Q, pieces)"}})

cases = []
for Ftex, P, Q, R, px, py, pz, comp in [
        ("\\langle x^2 y,\\ yz,\\ xz^2 \\rangle", "x**2*y", "y*z", "x*z**2", 1, 2, 1, "div"),
        ("\\langle e^{x},\\ \\sin y,\\ z^3 \\rangle", "exp(x)", "sin(y)", "z**3", 0, 0, 1, "div"),
        ("\\langle xy,\\ y^2,\\ yz \\rangle", "x*y", "y**2", "y*z", 1, 1, 1, "div"),
        ("\\langle yz,\\ xz,\\ xy \\rangle", "y*z", "x*z", "x*y", 1, 2, 3, "curlz"),
        ("\\langle -y,\\ x,\\ 0 \\rangle", "-y", "x", "0", 3, 1, 0, "curlz"),
        ("\\langle y^2,\\ xz,\\ x \\rangle", "y**2", "x*z", "x", 1, 2, 3, "curlz"),
        ("\\langle z,\\ x,\\ y \\rangle", "z", "x", "y", 0, 0, 0, "curlx"),
        ("\\langle xyz,\\ x^2,\\ y \\rangle", "x*y*z", "x**2", "y", 1, 1, 1, "curlx")]:
    Pv, Qv, Rv = S(P), S(Q), S(R)
    ex = {"div": sp.diff(Pv, x) + sp.diff(Qv, y) + sp.diff(Rv, z), "curlz": sp.diff(Qv, x) - sp.diff(Pv, y), "curlx": sp.diff(Rv, y) - sp.diff(Qv, z)}[comp]
    val = ex.subs({x: px, y: py, z: pz})
    if val == 0:
        continue
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "px": px, "py": py, "pz": pz, "ck": {"div": 0, "curlz": 1, "curlx": 2}[comp], "ans": N(val)})
template("mvd-div-curl", "calc.vector-calculus",
         "For $\\mathbf F = {{Ftex}}$, what is {{ck == 0 ? \"div F\" : (ck == 1 ? \"the z-component of curl F\" : \"the x-component of curl F\")}} at $({{px}}, {{py}}, {{pz}})$?",
         value_part("Value", "div F $= P_x + Q_y + R_z$ (a scalar: net outflow per volume). curl F $= \\langle R_y - Q_z,\\ P_z - R_x,\\ Q_x - P_y\\rangle$ (a vector: twice the local rotation rate)"),
         cases, {"expect": {"a": "[mv_at(mv_d(P, 'x') + mv_d(Q, 'y') + mv_d(R, 'z'), px, py, pz), mv_at(mv_d(Q, 'x') - mv_d(P, 'y'), px, py, pz), mv_at(mv_d(R, 'y') - mv_d(Q, 'z'), px, py, pz)][ck]"}})

template("mvd-div-curl-facts", "calc.vector-calculus", "{{s}}",
         choice_part("Answer", ["Always zero", "Not always zero", "Meaningless: wrong kind of input"],
                     "curl(grad f) = 0 and div(curl F) = 0 for smooth fields: the two identities behind conservative fields and vector potentials. grad takes a scalar, div and curl take vector fields; div produces a scalar, curl a vector"),
         [{"s": "curl(∇f) for a smooth scalar function f is…", "ans": 0}, {"s": "div(curl F) for a smooth vector field F is…", "ans": 0},
          {"s": "div(∇f), the Laplacian of f, is…", "ans": 1}, {"s": "curl(div F) is…", "ans": 2}, {"s": "∇(div F), the gradient of the divergence, is…", "ans": 1},
          {"s": "div(f) for a scalar function f is…", "ans": 2}, {"s": "curl(curl F) is…", "ans": 1}],
         {"authored": True}, pace="recall")

cases = []
for stex, f, sx, sy, sz, u0, u1, v0, v1, card in [
        ("the sphere of radius 3", "1", "3*sin(u)*cos(v)", "3*sin(u)*sin(v)", "3*cos(u)", "0", "pi", "0", "2*pi", "4*pi*9"),
        ("the part of the plane $z = 2 + x + y$ above the square $[0, 1]\\times[0, 1]$", "1", "u", "v", "2 + u + v", "0", "1", "0", "1", "sqrt(3)"),
        ("the paraboloid $z = x^2 + y^2$ below $z = 1$", "1", "u*cos(v)", "u*sin(v)", "u**2", "0", "1", "0", "2*pi", "pi*(5*sqrt(5) - 1)/6"),
        ("the cone $z = \\sqrt{x^2 + y^2}$ for $0 \\le z \\le 2$", "1", "u*cos(v)", "u*sin(v)", "u", "0", "2", "0", "2*pi", "sqrt(2)*pi*4"),
        ("the cylinder $x^2 + y^2 = 4$ for $0 \\le z \\le 5$", "1", "2*cos(v)", "2*sin(v)", "u", "0", "5", "0", "2*pi", "2*pi*2*5"),
        ("the upper hemisphere of radius 2, with $f = z$", "z", "2*sin(u)*cos(v)", "2*sin(u)*sin(v)", "2*cos(u)", "0", "pi/2", "0", "2*pi", "8*pi")]:
    cases.append({"stex": stex, "f": f, "sx": sx, "sy": sy, "sz": sz, "u0": u0, "u1": u1, "v0": v0, "v1": v1, "ans": N(S(card))})
template("mvd-surface-integral", "calc.vector-calculus", "Compute $\\displaystyle\\iint_S f\\,dS$ for {{stex}} (with $f = 1$ unless stated, which gives the area).",
         value_part("Value", "Parametrise $S$ by $\\mathbf r(u, v)$; then $dS = |\\mathbf r_u\\times\\mathbf r_v|\\,du\\,dv$. Sphere of radius $a$: $a^2\\sin\\varphi$. Graph $z = g(x, y)$: $\\sqrt{1 + g_x^2 + g_y^2}$. Cylinder of radius $a$: $a$"),
         cases, {"expect": {"a": "surface_scalar(f, sx, sy, sz, u0, u1, v0, v1)"}})

cases = []
for Ftex, P, Q, R, stex, sx, sy, sz, u0, u1, v0, v1, sign, card in [
        ("\\langle x, y, z\\rangle", "x", "y", "z", "the sphere of radius 2, outward", "2*sin(u)*cos(v)", "2*sin(u)*sin(v)", "2*cos(u)", "0", "pi", "0", "2*pi", 1, "2*4*pi*4"),
        ("\\langle 0, 0, z\\rangle", "0", "0", "z", "the upper hemisphere of radius 1, outward (upward)", "sin(u)*cos(v)", "sin(u)*sin(v)", "cos(u)", "0", "pi/2", "0", "2*pi", 1, "2*pi/3"),
        ("\\langle x, y, 0\\rangle", "x", "y", "0", "the cylinder $x^2 + y^2 = 1$, $0 \\le z \\le 3$, outward", "cos(v)", "sin(v)", "u", "0", "3", "0", "2*pi", -1, "2*pi*3"),
        ("\\langle 0, 0, 3\\rangle", "0", "0", "3", "the disc $x^2 + y^2 \\le 4$ in the plane $z = 1$, upward", "u*cos(v)", "u*sin(v)", "1", "0", "2", "0", "2*pi", 1, "3*pi*4"),
        ("\\langle y, -x, z\\rangle", "y", "-x", "z", "the paraboloid $z = 4 - x^2 - y^2$, $z \\ge 0$, upward", "u*cos(v)", "u*sin(v)", "4 - u**2", "0", "2", "0", "2*pi", 1, "8*pi"),
        ("\\langle x, 0, 0\\rangle", "x", "0", "0", "the plane $x + y + z = 1$ in the first octant, upward", "u", "v", "1 - u - v", "0", "1", "0", "1 - u", 1, "Rational(1, 6)")]:
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "stex": stex, "sx": sx, "sy": sy, "sz": sz, "u0": u0, "u1": u1, "v0": v0, "v1": v1, "sgn": sign, "ans": N(S(card))})
# the last row's v-limits depend on u: integrate over v first in the verifier by swapping, so rewrite it as a graph over the triangle
cases[-1].update({"sx": "u", "sy": "v*(1 - u)", "sz": "1 - u - v*(1 - u)", "v1": "1"})
template("mvd-flux", "calc.vector-calculus", "Find the flux $\\displaystyle\\iint_S \\mathbf F\\cdot\\mathbf n\\,dS$ of $\\mathbf F = {{Ftex}}$ through {{stex}}.",
         value_part("Flux", "$\\iint_S \\mathbf F\\cdot\\mathbf n\\,dS = \\iint_D \\mathbf F(\\mathbf r(u, v))\\cdot(\\mathbf r_u\\times\\mathbf r_v)\\,du\\,dv$, with the cross product pointing the way the orientation asks (flip the sign if not). For a graph $z = g$, upward: $\\iint(-Pg_x - Qg_y + R)\\,dA$"),
         cases, {"expect": {"a": "surface_flux(P, Q, R, sx, sy, sz, u0, u1, v0, v1, sgn)"}})

cases = []
for Ftex, P, Q, R, a, card in [
        ("\\langle x, y, z\\rangle", "x", "y", "z", 2, "3*8"), ("\\langle x^2, y^2, z^2\\rangle", "x**2", "y**2", "z**2", 1, "3"),
        ("\\langle xy, yz, zx\\rangle", "x*y", "y*z", "z*x", 2, "Integral(x + y + z, (x, 0, 2), (y, 0, 2), (z, 0, 2))"), ("\\langle 2x, -y, 3z\\rangle", "2*x", "-y", "3*z", 3, "4*27"),
        ("\\langle x^3, 0, 0\\rangle", "x**3", "0", "0", 1, "Integral(3*x**2, (x, 0, 1), (y, 0, 1), (z, 0, 1))"), ("\\langle e^{x}, 0, z\\rangle", "exp(x)", "0", "z", 1, "Integral(exp(x) + 1, (x, 0, 1), (y, 0, 1), (z, 0, 1))")]:
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "side": a, "ans": N(S(card))})
template("mvd-divergence-theorem", "calc.vector-calculus", "Use the divergence theorem to find the outward flux of $\\mathbf F = {{Ftex}}$ through the surface of the cube $[0, {{side}}]^3$.",
         value_part("Flux", "Outward flux through a closed surface $= \\iiint_E \\operatorname{div}\\mathbf F\\,dV$. When div F is constant the answer is that constant times the volume"),
         cases, {"expect": {"a": "box_flux(P, Q, R, side)"}})

cases = []
for Ftex, P, Q, R, ctex, card, rx, ry, rz in [
        ("\\langle -y,\\ x,\\ z \\rangle", "-y", "x", "z", "the circle $x^2 + y^2 = 4$ in the plane $z = 3$, counterclockwise seen from above", "2*pi*4", "2*cos(t)", "2*sin(t)", "3"),
        ("\\langle y,\\ z,\\ x \\rangle", "y", "z", "x", "the unit circle in the $xy$-plane, counterclockwise seen from above", "-pi", "cos(t)", "sin(t)", "0"),
        ("\\langle z,\\ x,\\ y \\rangle", "z", "x", "y", "the unit circle in the plane $z = 2$, counterclockwise seen from above", "pi", "cos(t)", "sin(t)", "2"),
        ("\\langle x^2,\\ xy + z,\\ e^{z} \\rangle", "x**2", "x*y + z", "exp(z)", "the circle of radius 3 in the $xy$-plane, counterclockwise seen from above", "0", "3*cos(t)", "3*sin(t)", "0"),
        ("\\langle -y^3,\\ x^3,\\ 0 \\rangle", "-y**3", "x**3", "0", "the unit circle in the plane $z = 5$, counterclockwise seen from above", "3*pi/2", "cos(t)", "sin(t)", "5"),
        ("\\langle -y,\\ x,\\ z \\rangle", "-y", "x", "z", "the circle $x^2 + y^2 = 4$ in the plane $z = 3$, clockwise seen from above", "-2*pi*4", "2*cos(t)", "-2*sin(t)", "3")]:
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "ctex": ctex, "rx": rx, "ry": ry, "rz": rz, "ans": N(S(card))})
template("mvd-stokes", "calc.vector-calculus", "Use Stokes' theorem to find $\\displaystyle\\oint_C \\mathbf F\\cdot d\\mathbf r$ for $\\mathbf F = {{Ftex}}$ around {{ctex}}.",
         value_part("Circulation", "$\\oint_C \\mathbf F\\cdot d\\mathbf r = \\iint_S (\\nabla\\times\\mathbf F)\\cdot\\mathbf n\\,dS$ for any surface $S$ with boundary $C$; the right-hand rule ties the direction of $C$ to $\\mathbf n$. Pick the flattest $S$ (here the disc), where $\\mathbf n = \\pm\\mathbf k$"),
         [c for c in cases if c["ans"] != 0] + [], {"expect": {"a": "line_work(P, Q, R, rx, ry, rz, 0, 2*pi)"}})

template("mvd-orientation", "calc.vector-calculus", "{{s}}",
         choice_part("Answer", ["Region kept on the left (counterclockwise for an outer boundary)", "Outward normal", "By the right-hand rule: fingers along C, thumb along n", "The sign of the answer flips"],
                     "Every big theorem comes with an orientation: Green's needs C counterclockwise, the divergence theorem the outward normal, Stokes' a curve and normal matched by the right-hand rule. Reversing the orientation reverses the sign"),
         [{"s": "Which way must C run for Green's theorem as usually written?", "ans": 0}, {"s": "Which normal does the divergence theorem use?", "ans": 1},
          {"s": "In Stokes' theorem, how are the direction of C and the normal n linked?", "ans": 2}, {"s": "You parametrise a closed curve clockwise instead. What happens to a circulation?", "ans": 3},
          {"s": "Your r_u × r_v points into a closed surface. What happens to the flux if you use it?", "ans": 3}, {"s": "For a region with a hole, which way must its inner boundary run in Green's theorem?", "ans": 0}],
         {"authored": True}, pace="recall")

template("mvd-which-theorem", "calc.vector-calculus", "{{s}}",
         choice_part("Tool", ["The fundamental theorem for line integrals (potential)", "Green's theorem", "Stokes' theorem", "The divergence theorem"],
                     "Match the integral to the theorem: a line integral of a gradient field → potential; a closed plane curve → Green; a closed space curve, or the flux of a curl → Stokes; flux through a closed surface → divergence"),
         [{"s": "∫_C ∇f · dr along a curve from A to B", "ans": 0}, {"s": "The circulation of a field around a closed curve in the xy-plane, as a double integral", "ans": 1},
          {"s": "The outward flux through the surface of a solid", "ans": 3}, {"s": "The circulation around a closed curve in space, as a flux of curl F", "ans": 2},
          {"s": "The flux of curl F through a hemisphere, traded for a line integral", "ans": 2}, {"s": "The area of a region from a line integral around its boundary", "ans": 1},
          {"s": "The total charge inside a closed surface from the flux of E", "ans": 3}, {"s": "The work of a conservative force between two points", "ans": 0}],
         {"authored": True}, pace="recall")


# ════════════════ the cells the first pass left open (drills/matrices/mvc.yaml) ════════════════
cases = []
for stex, F, p in [("x^2 + y^2 + z^2 = 14", "x**2 + y**2 + z**2 - 14", (1, 2, 3)), ("xyz + z^3 = 10", "x*y*z + z**3 - 10", (1, 1, 2)),
                   ("x^2 z + y z^2 = 5", "x**2*z + y*z**2 - 5", (2, 1, 1)), ("e^{xz} + y z = 3", "exp(x*z) + y*z - 3", (0, 2, 1)),
                   ("x + y^2 + z^2 - xz = 4", "x + y**2 + z**2 - x*z - 4", (1, 1, 2))]:
    G = S(F)
    sub = {x: p[0], y: p[1], z: p[2]}
    assert sp.simplify(G.subs(sub)) == 0, stex
    for w, wv in (("x", x), ("y", y)):
        # differentiate F(x, y, z(x, y)) = 0 and solve for z_w (the route the card teaches)
        zf = sp.Function("zf")(x, y)
        dz = sp.solve(sp.diff(G.subs(z, zf), wv), sp.diff(zf, wv))[0].subs(zf, z).subs(sub)
        if dz != 0:
            cases.append({"stex": stex, "F": F, "px": p[0], "py": p[1], "pz": p[2], "w": w, "ans": N(dz)})
template("mvd-implicit-3", "calc.multivariable",
         "The surface ${{stex}}$ defines $z$ as a function of $x$ and $y$ near $({{px}}, {{py}}, {{pz}})$. What is $\\partial z/\\partial {{w}}$ there?",
         value_part("Partial", "Differentiate $F(x, y, z(x, y)) = 0$ in that variable: $F_x + F_z z_x = 0$, so $z_x = -F_x/F_z$ (and $z_y = -F_y/F_z$). The minus sign is the usual slip"),
         cases, {"expect": {"a": "-mv_at(mv_d(F, w), px, py, pz)/mv_at(mv_d(F, 'z'), px, py, pz)"}})

cases = []
for ftex, f, gtex, g, htex, h, kind, ans in [
        ("z", "z", "x + y + z = 1", "x + y + z - 1", "x^2 + y^2 = 1", "x**2 + y**2 - 1", 1, "1 + sqrt(2)"),
        ("x + 2y + 3z", "x + 2*y + 3*z", "x - y + z = 1", "x - y + z - 1", "x^2 + y^2 = 1", "x**2 + y**2 - 1", 1, "3 + sqrt(29)"),
        ("x^2 + y^2 + z^2", "x**2 + y**2 + z**2", "x + y = 1", "x + y - 1", "y + z = 2", "y + z - 2", 0, "2"),
        ("z", "z", "x + y + z = 1", "x + y + z - 1", "x^2 + y^2 = 1", "x**2 + y**2 - 1", 0, "1 - sqrt(2)"),
        ("x + y + z", "x + y + z", "x^2 + y^2 = 2", "x**2 + y**2 - 2", "x + z = 1", "x + z - 1", 1, "1 + sqrt(2)")]:
    cases.append({"ftex": ftex, "f": f, "gtex": gtex, "g": g, "htex": htex, "h": h, "kind": kind, "ans": N(S(ans))})
template("mvd-lagrange-two", "calc.partials-apps",
         "What is the {{kind == 1 ? \"maximum\" : \"minimum\"}} of ${{ftex}}$ on the curve where ${{gtex}}$ meets ${{htex}}$?",
         value_part("Extreme value", "With two constraints, $\\nabla f = \\lambda\\nabla g + \\mu\\nabla h$ plus both constraints: five equations in $x, y, z, \\lambda, \\mu$. Often quicker: parametrise the curve of intersection (here the cylinder gives $x = \\cos t$, $y = \\sin t$) and maximise in one variable"),
         cases, {"expect": {"a": "lagrange2(f, g, h, kind)"}})

cases = []
for rtex, ftex, utex, uv_int, xy_int in [
        ("the parallelogram bounded by $y = x$, $y = x + 2$, $y = -x$ and $y = -x + 4$", "x + y", "u = x + y,\\ v = y - x",
         "Integral(u/2, (u, 0, 4), (v, 0, 2))", "Integral(x + y, (y, -x, x + 2), (x, -1, 0)) + Integral(x + y, (y, x, x + 2), (x, 0, 1)) + Integral(x + y, (y, x, 4 - x), (x, 1, 2))"),
        ("the ellipse $\\dfrac{x^2}{9} + \\dfrac{y^2}{4} \\le 1$", "1", "x = 3u,\\ y = 2v", "6*pi", "Integral(1, (y, -2*sqrt(1 - x**2/9), 2*sqrt(1 - x**2/9)), (x, -3, 3))"),
        ("the ellipse $\\dfrac{x^2}{4} + y^2 \\le 1$", "x^2", "x = 2u,\\ y = v", "Integral(4*x**2*cos(u)**2*2*x, (x, 0, 1), (u, 0, 2*pi))", "Integral(x**2, (y, -sqrt(1 - x**2/4), sqrt(1 - x**2/4)), (x, -2, 2))"),
        ("the square with vertices $(0, 0)$, $(1, 1)$, $(2, 0)$, $(1, -1)$", "(x + y)^2", "u = x + y,\\ v = x - y", "Integral(u**2/2, (u, 0, 2), (v, 0, 2))",
         "Integral((x + y)**2, (y, -x, x), (x, 0, 1)) + Integral((x + y)**2, (y, x - 2, 2 - x), (x, 1, 2))"),
        ("the region $1 \\le xy \\le 3$, $1 \\le y/x \\le 4$ in the first quadrant", "1", "u = xy,\\ v = y/x", "Integral(1/(2*x), (u, 1, 3), (x, 1, 4))",
         "Integral(1, (y, 1/x, 4*x), (x, Rational(1, 2), sqrt(3)/2)) + Integral(1, (y, 1/x, 3/x), (x, sqrt(3)/2, 1)) + Integral(1, (y, x, 3/x), (x, 1, sqrt(3)))")]:
    val = sp.sympify(uv_int, locals={"x": x, "u": u, "pi": sp.pi}) if "Integral" in uv_int else S(uv_int)
    cases.append({"rtex": rtex, "ftex": ftex, "utex": utex, "check": xy_int, "ans": N(val)})
template("mvd-change-variables", "calc.multiple-integrals",
         "Use ${{utex}}$ to evaluate $\\displaystyle\\iint_R {{ftex}}\\,dA$ over {{rtex}}.",
         value_part("Value", "Map the boundary curves to the $uv$-plane (they should become a rectangle), find $|\\partial(x, y)/\\partial(u, v)|$, which is $1/|\\partial(u, v)/\\partial(x, y)|$ when $u, v$ are given in terms of $x, y$, then integrate $f\\,|J|\\,du\\,dv$"),
         cases, {"expect": {"a": "quad(check)"}})

rows = [
    ({"stex": "the tetrahedron $x, y, z \\ge 0$, $x + y + z \\le 1$, integrating $f = x$ in the order $dx\\,dz\\,dy$"}, "Integral(x, (z, 0, 1 - x - y), (y, 0, 1 - x), (x, 0, 1))",
     [("\\int_0^1\\!\\int_0^{1-y}\\!\\int_0^{1-y-z} x\\,dx\\,dz\\,dy", "Integral(x, (x, 0, 1 - y - z), (z, 0, 1 - y), (y, 0, 1))"), ("\\int_0^1\\!\\int_0^{1}\\!\\int_0^{1-y-z} x\\,dx\\,dz\\,dy", "Integral(x, (x, 0, 1 - y - z), (z, 0, 1), (y, 0, 1))"),
      ("\\int_0^1\\!\\int_0^{1-y}\\!\\int_0^{1-y} x\\,dx\\,dz\\,dy", "Integral(x, (x, 0, 1 - y), (z, 0, 1 - y), (y, 0, 1))"), ("\\int_0^1\\!\\int_0^{1-z}\\!\\int_0^{1-y-z} x\\,dx\\,dz\\,dy", "Integral(x, (x, 0, 1 - y - z), (z, 0, 1 - y), (y, 0, 1)) + 1")]),
    ({"stex": "the solid under $z = 1 - y^2$ above $0 \\le x \\le 2$, $-1 \\le y \\le 1$, integrating $f = z$ in the order $dy\\,dz\\,dx$"}, "Integral(z, (z, 0, 1 - y**2), (y, -1, 1), (x, 0, 2))",
     [("\\int_0^2\\!\\int_0^1\\!\\int_{-\\sqrt{1-z}}^{\\sqrt{1-z}} z\\,dy\\,dz\\,dx", "Integral(z, (y, -sqrt(1 - z), sqrt(1 - z)), (z, 0, 1), (x, 0, 2))"), ("\\int_0^2\\!\\int_0^1\\!\\int_{0}^{\\sqrt{1-z}} z\\,dy\\,dz\\,dx", "Integral(z, (y, 0, sqrt(1 - z)), (z, 0, 1), (x, 0, 2))"),
      ("\\int_0^2\\!\\int_0^1\\!\\int_{-1}^{1} z\\,dy\\,dz\\,dx", "Integral(z, (y, -1, 1), (z, 0, 1), (x, 0, 2))"), ("\\int_0^2\\!\\int_0^1\\!\\int_{-(1-z)}^{1-z} z\\,dy\\,dz\\,dx", "Integral(z, (y, z - 1, 1 - z), (z, 0, 1), (x, 0, 2))")]),
    ({"stex": "the solid $0 \\le z \\le x$, $0 \\le x \\le 1$, $0 \\le y \\le 2$, integrating $f = y$ in the order $dx\\,dy\\,dz$"}, "Integral(y, (z, 0, x), (y, 0, 2), (x, 0, 1))",
     [("\\int_0^1\\!\\int_0^2\\!\\int_z^{1} y\\,dx\\,dy\\,dz", "Integral(y, (x, z, 1), (y, 0, 2), (z, 0, 1))"), ("\\int_0^1\\!\\int_0^2\\!\\int_0^{z} y\\,dx\\,dy\\,dz", "Integral(y, (x, 0, z), (y, 0, 2), (z, 0, 1)) + Rational(1, 7)"),
      ("\\int_0^1\\!\\int_0^2\\!\\int_0^{1} y\\,dx\\,dy\\,dz", "Integral(y, (x, 0, 1), (y, 0, 2), (z, 0, 1))"), ("\\int_0^2\\!\\int_0^2\\!\\int_z^{1} y\\,dx\\,dy\\,dz", "Integral(y, (x, z, 1), (y, 0, 2), (z, 0, 2))")]),
    ({"stex": "the region inside the cylinder $y^2 + z^2 \\le 4$ for $0 \\le x \\le 3$, integrating $f = x$ in the order $dz\\,dy\\,dx$"}, "18*pi",
     [("\\int_0^3\\!\\int_{-2}^{2}\\!\\int_{-\\sqrt{4-y^2}}^{\\sqrt{4-y^2}} x\\,dz\\,dy\\,dx", "Integral(x, (z, -sqrt(4 - y**2), sqrt(4 - y**2)), (y, -2, 2), (x, 0, 3))"), ("\\int_0^3\\!\\int_{-2}^{2}\\!\\int_{0}^{\\sqrt{4-y^2}} x\\,dz\\,dy\\,dx", "Integral(x, (z, 0, sqrt(4 - y**2)), (y, -2, 2), (x, 0, 3))"),
      ("\\int_0^3\\!\\int_{-2}^{2}\\!\\int_{-2}^{2} x\\,dz\\,dy\\,dx", "Integral(x, (z, -2, 2), (y, -2, 2), (x, 0, 3))"), ("\\int_0^3\\!\\int_{-4}^{4}\\!\\int_{-\\sqrt{4-y^2}}^{\\sqrt{4-y^2}} x\\,dz\\,dy\\,dx", "Integral(x, (z, -sqrt(Max(0, 4 - y**2)), sqrt(Max(0, 4 - y**2))), (y, -4, 4), (x, 0, 3)) + 1")]),
]
template("mvd-triple-order", "calc.multiple-integrals",
         "Which integral gives $\\iiint_E f\\,dV$ for {{stex}}?" + SETUP_PROMPT_TAIL,
         choice_part("Setup", ABCD, "Project the solid onto the plane of the two outer variables; that shadow sets the middle and outer limits. The inner limits are the two surfaces that bound the solid in the innermost direction, solved for that variable"),
         setup_cases([(c, rename(tg), [(tx, rename(e)) for tx, e in opts]) for c, tg, opts in rows]), SETUP_VERIFY)

cases = []
for rtex, ftex, num_card, area_card, check in [
        ("the square $[0, 2]\\times[0, 2]$", "xy", "Integral(x*y, (x, 0, 2), (y, 0, 2))", "4", "Integral(x*y, (y, 0, 2), (x, 0, 2))/4"),
        ("the disc $x^2 + y^2 \\le 4$", "x^2 + y^2", "Integral(r**3, (r, 0, 2), (theta, 0, 2*pi))", "4*pi", "Integral(x**2 + y**2, (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))/(4*pi)"),
        ("the triangle with vertices $(0, 0)$, $(1, 0)$, $(0, 1)$", "x", "Rational(1, 6)", "Rational(1, 2)", "Integral(x, (y, 0, 1 - x), (x, 0, 1))/Integral(1, (y, 0, 1 - x), (x, 0, 1))"),
        ("the unit ball", "x^2 + y^2 + z^2", "Integral(rho**4*sin(phi), (rho, 0, 1), (phi, 0, pi), (theta, 0, 2*pi))", "4*pi/3",
         "Integral(x**2 + y**2 + z**2, (z, -sqrt(1 - x**2 - y**2), sqrt(1 - x**2 - y**2)), (y, -sqrt(1 - x**2), sqrt(1 - x**2)), (x, -1, 1))/(4*pi/3)"),
        ("the cube $[0, 1]^3$", "x + y + z", "Rational(3, 2)", "1", "Integral(x + y + z, (z, 0, 1), (y, 0, 1), (x, 0, 1))"),
        ("the cylinder $x^2 + y^2 \\le 1$, $0 \\le z \\le 2$", "z", "Integral(r*z, (z, 0, 2), (r, 0, 1), (theta, 0, 2*pi))", "2*pi",
         "Integral(z, (z, 0, 2), (y, -sqrt(1 - x**2), sqrt(1 - x**2)), (x, -1, 1))/(2*pi)")]:
    loc = {"r": r, "theta": th, "rho": rho, "phi": ph, "pi": sp.pi, "x": x, "y": y, "z": z}
    val = sp.sympify(num_card, locals=loc) / sp.sympify(area_card, locals=loc)
    cases.append({"rtex": rtex, "ftex": ftex, "check": check, "ans": N(val)})
template("mvd-average", "calc.multiple-integrals", "What is the average value of $f = {{ftex}}$ over {{rtex}}?",
         value_part("Average", "$f_{\\text{avg}} = \\dfrac{1}{\\text{area}}\\iint_D f\\,dA$ (or $\\dfrac{1}{\\text{volume}}\\iiint_E f\\,dV$). Use the coordinates that suit the region for both integrals"),
         cases, {"expect": {"a": "quad(check)"}})

cases = []
for ltex, card, check in [
        ("the solid upper hemisphere of radius 2 (uniform density); find $\\bar z$", "Rational(3, 8)*2",
         "Integral(z, (z, 0, sqrt(4 - x**2 - y**2)), (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))/Integral(1, (z, 0, sqrt(4 - x**2 - y**2)), (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))"),
        ("the solid cone $\\sqrt{x^2 + y^2} \\le z \\le 3$ (uniform density); find $\\bar z$", "Rational(9, 4)",
         "Integral(z*pi*z**2, (z, 0, 3))/Integral(pi*z**2, (z, 0, 3))"),
        ("the solid paraboloid $x^2 + y^2 \\le z \\le 4$ (uniform density); find $\\bar z$", "Rational(8, 3)",
         "Integral(z*pi*z, (z, 0, 4))/Integral(pi*z, (z, 0, 4))"),
        ("the cube $[0, 1]^3$ with density $\\delta = z$; find $\\bar z$", "Rational(2, 3)", "Integral(z*z, (z, 0, 1))/Integral(z, (z, 0, 1))"),
        ("the tetrahedron $x, y, z \\ge 0$, $x + y + z \\le 1$ (uniform density); find $\\bar x$", "Rational(1, 4)",
         "Integral(x, (z, 0, 1 - x - y), (y, 0, 1 - x), (x, 0, 1))/Integral(1, (z, 0, 1 - x - y), (y, 0, 1 - x), (x, 0, 1))")]:
    cases.append({"ltex": ltex, "check": check, "ans": N(S(card))})
template("mvd-center-mass-solid", "calc.multiple-integrals", "Centre of mass of {{ltex}}.",
         value_part("Coordinate", "$\\bar z = \\dfrac{1}{M}\\iiint z\\,\\delta\\,dV$. Symmetry gives $\\bar x = \\bar y = 0$ for solids of revolution about the $z$-axis; slicing by $z$ (disc area times $dz$) is often quickest. Hemisphere: $3a/8$; cone from its tip: $3h/4$"),
         cases, {"expect": {"a": "quad(check)"}})

cases = []
for ltex, card, check in [
        ("the disc of radius 2 (density 1) about its centre, $I_0 = \\iint (x^2 + y^2)\\,dA$", "Integral(r**3, (r, 0, 2), (theta, 0, 2*pi))", "Integral(x**2 + y**2, (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2))"),
        ("the square $[0, 1]\\times[0, 1]$ (density 1) about the $x$-axis, $I_x = \\iint y^2\\,dA$", "Rational(1, 3)", "Integral(y**2, (y, 0, 1), (x, 0, 1))"),
        ("the rectangle $[0, 3]\\times[0, 2]$ (density 1) about the $y$-axis, $I_y = \\iint x^2\\,dA$", "18", "Integral(x**2, (y, 0, 2), (x, 0, 3))"),
        ("the triangle $(0, 0)$, $(1, 0)$, $(0, 1)$ with density $x$, about the $x$-axis", "Integral(x*y**2, (x, 0, 1 - y), (y, 0, 1))", "Integral(x*y**2, (y, 0, 1 - x), (x, 0, 1))"),
        ("the annulus $1 \\le r \\le 2$ (density 1) about its centre", "Integral(r**3, (r, 1, 2), (theta, 0, 2*pi))", "Integral(x**2 + y**2, (y, -sqrt(4 - x**2), sqrt(4 - x**2)), (x, -2, 2)) - Integral(x**2 + y**2, (y, -sqrt(1 - x**2), sqrt(1 - x**2)), (x, -1, 1))")]:
    val = sp.sympify(card, locals={"r": r, "theta": th, "pi": sp.pi, "x": x, "y": y})
    cases.append({"ltex": ltex, "check": check, "ans": N(val)})
template("mvd-inertia", "calc.multiple-integrals", "Find the moment of inertia of {{ltex}}.",
         value_part("Moment of inertia", "$I_x = \\iint y^2\\delta\\,dA$ (distance to the $x$-axis is $|y|$), $I_y = \\iint x^2\\delta\\,dA$, $I_0 = I_x + I_y$. A disc of mass $M$, radius $a$: $I_0 = Ma^2/2$"),
         cases, {"expect": {"a": "quad(check)"}})

cases = []
for Ftex, P, Q, R, ctex, rx, ry, rz, t1 in [
        ("\\langle -y,\\ x,\\ z \\rangle", "-y", "x", "z", "the helix $\\langle\\cos t, \\sin t, t\\rangle$, $0 \\le t \\le 2\\pi$", "cos(t)", "sin(t)", "t", "2*pi"),
        ("\\langle z,\\ x,\\ y \\rangle", "z", "x", "y", "the helix $\\langle\\cos t, \\sin t, t\\rangle$, $0 \\le t \\le \\pi$", "cos(t)", "sin(t)", "t", "pi"),
        ("\\langle y,\\ z,\\ x \\rangle", "y", "z", "x", "the curve $\\langle t, t^2, t^3\\rangle$, $0 \\le t \\le 1$", "t", "t**2", "t**3", "1"),
        ("\\langle xy,\\ yz,\\ zx \\rangle", "x*y", "y*z", "z*x", "the curve $\\langle t, t^2, t^3\\rangle$, $0 \\le t \\le 1$", "t", "t**2", "t**3", "1"),
        ("\\langle y^2,\\ x,\\ z^2 \\rangle", "y**2", "x", "z**2", "the segment from $(0, 0, 0)$ to $(1, 2, 3)$", "t", "2*t", "3*t", "1")]:
    rv = [S(rx), S(ry), S(rz)]
    val = sp.integrate(sp.expand(sum(S(c).subs({x: rv[0], y: rv[1], z: rv[2]}, simultaneous=True) * sp.diff(k, t) for c, k in zip((P, Q, R), rv))), (t, 0, S(t1)))
    if val != 0:
        cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "ctex": ctex, "rx": rx, "ry": ry, "rz": rz, "t1": t1, "ans": N(val)})
template("mvd-work-space", "calc.vector-calculus", "Compute $\\displaystyle\\int_C \\mathbf F\\cdot d\\mathbf r$ for $\\mathbf F = {{Ftex}}$ along {{ctex}}.",
         value_part("Work", "Substitute $x(t), y(t), z(t)$ into all three components, dot with $\\mathbf r'(t) = \\langle x', y', z'\\rangle$, integrate in $t$. These fields are not conservative, so there is no shortcut"),
         cases, {"expect": {"a": "line_work(P, Q, R, rx, ry, rz, 0, t1)"}})

cases = []
for ctex, area, pieces in [
        ("the ellipse $x = 3\\cos t$, $y = 2\\sin t$", "6*pi", "3*cos(t)|2*sin(t)|0|2*pi"),
        ("the astroid $x = \\cos^3 t$, $y = \\sin^3 t$", "3*pi/8", "cos(t)**3|sin(t)**3|0|2*pi"),
        ("the triangle $(0, 0)$, $(4, 0)$, $(0, 3)$", "6", "4*t|0|0|1;4 - 4*t|3*t|0|1;0|3 - 3*t|0|1"),
        ("the cardioid-like loop $x = \\cos t + \\cos^2 t$, $y = \\sin t + \\sin t\\cos t$", "3*pi/2", "cos(t) + cos(t)**2|sin(t) + sin(t)*cos(t)|0|2*pi"),
        ("the region between $y = x^2$ and $y = x$ (boundary run counterclockwise)", "Rational(1, 6)", "t|t**2|0|1;1 - t|1 - t|0|1")]:
    cases.append({"ctex": ctex, "pieces": pieces, "ans": N(S(area))})
template("mvd-green-area", "calc.vector-calculus", "Use a line integral to find the area enclosed by {{ctex}}.",
         value_part("Area", "Green's theorem with $Q_x - P_y = 1$: area $= \\oint_C x\\,dy = -\\oint_C y\\,dx = \\tfrac12\\oint_C (x\\,dy - y\\,dx)$, with $C$ counterclockwise. Useful when the boundary is a parametrised curve"),
         cases, {"expect": {"a": "closed_work('-y/2', 'x/2', pieces)"}})

cases = []
for Ftex, P, Q, R, stex, div_card, verify in [
        ("\\langle x^3,\\ y^3,\\ z^3 \\rangle", "x**3", "y**3", "z**3", "the sphere of radius 1", "Integral(3*rho**4*sin(phi), (rho, 0, 1), (phi, 0, pi), (theta, 0, 2*pi))",
         "surface_flux(P, Q, R, 'sin(u)*cos(v)', 'sin(u)*sin(v)', 'cos(u)', 0, pi, 0, 2*pi, 1)"),
        ("\\langle x,\\ y,\\ z \\rangle", "x", "y", "z", "the sphere of radius 3", "3*4*pi*27/3",
         "surface_flux(P, Q, R, '3*sin(u)*cos(v)', '3*sin(u)*sin(v)', '3*cos(u)', 0, pi, 0, 2*pi, 1)"),
        ("\\langle x,\\ y,\\ z^2 \\rangle", "x", "y", "z**2", "the closed cylinder $x^2 + y^2 \\le 1$, $0 \\le z \\le 2$ (side, top and bottom)", "Integral((2 + 2*z)*r, (z, 0, 2), (r, 0, 1), (theta, 0, 2*pi))",
         "surface_flux(P, Q, R, 'cos(v)', 'sin(v)', 'u', 0, 2, 0, 2*pi, -1) + surface_flux(P, Q, R, 'u*cos(v)', 'u*sin(v)', '2', 0, 1, 0, 2*pi, 1) + surface_flux(P, Q, R, 'u*cos(v)', 'u*sin(v)', '0', 0, 1, 0, 2*pi, -1)"),
        ("\\langle xz,\\ yz,\\ 1 \\rangle", "x*z", "y*z", "1", "the closed cylinder $x^2 + y^2 \\le 4$, $0 \\le z \\le 1$", "Integral(2*z*r, (z, 0, 1), (r, 0, 2), (theta, 0, 2*pi))",
         "surface_flux(P, Q, R, '2*cos(v)', '2*sin(v)', 'u', 0, 1, 0, 2*pi, -1) + surface_flux(P, Q, R, 'u*cos(v)', 'u*sin(v)', '1', 0, 2, 0, 2*pi, 1) + surface_flux(P, Q, R, 'u*cos(v)', 'u*sin(v)', '0', 0, 2, 0, 2*pi, -1)"),
        ("\\langle 0,\\ 0,\\ z \\rangle", "0", "0", "z", "the closed upper half ball of radius 2 (dome and flat base)", "2*pi*8/3",
         "surface_flux(P, Q, R, '2*sin(u)*cos(v)', '2*sin(u)*sin(v)', '2*cos(u)', 0, pi/2, 0, 2*pi, 1) + surface_flux(P, Q, R, 'u*cos(v)', 'u*sin(v)', '0', 0, 2, 0, 2*pi, -1)")]:
    val = sp.sympify(div_card, locals={"r": r, "theta": th, "rho": rho, "phi": ph, "z": z, "pi": sp.pi})
    cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "stex": stex, "ans": N(val), "_v": verify})
template("mvd-divergence-curved", "calc.vector-calculus", "Use the divergence theorem to find the outward flux of $\\mathbf F = {{Ftex}}$ through {{stex}}.",
         value_part("Flux", "Flux out $= \\iiint_E \\operatorname{div}\\mathbf F\\,dV$ in the coordinates of the solid: spherical for a ball, cylindrical for a cylinder. The theorem needs the whole closed surface: for an open one, add a lid and subtract its flux"),
         [{**{k: v for k, v in c.items() if k != "_v"}, "vexp": c["_v"]} for c in cases], {"expect": {"a": "mv_eval(vexp, P, Q, R)"}})

cases = []
for Ftex, P, Q, R, stex, sx, sy, sz, u1, ctex, rx, ry, rz in [
        ("\\langle -y,\\ x,\\ z \\rangle", "-y", "x", "z", "the upper hemisphere $x^2 + y^2 + z^2 = 4$, $z \\ge 0$, oriented upward", "2*sin(u)*cos(v)", "2*sin(u)*sin(v)", "2*cos(u)", "pi/2", "", "2*cos(t)", "2*sin(t)", "0"),
        ("\\langle y,\\ z,\\ x \\rangle", "y", "z", "x", "the paraboloid $z = 1 - x^2 - y^2$, $z \\ge 0$, oriented upward", "u*cos(v)", "u*sin(v)", "1 - u**2", "1", "", "cos(t)", "sin(t)", "0"),
        ("\\langle z^2,\\ x,\\ y^2 \\rangle", "z**2", "x", "y**2", "the cone $z = \\sqrt{x^2 + y^2}$, $0 \\le z \\le 1$, oriented downward-outward... ", "u*cos(v)", "u*sin(v)", "u", "1", "", "cos(t)", "-sin(t)", "1"),
        ("\\langle x^2 z,\\ xy,\\ e^{z} \\rangle", "x**2*z", "x*y", "exp(z)", "the upper unit hemisphere, oriented upward", "sin(u)*cos(v)", "sin(u)*sin(v)", "cos(u)", "pi/2", "", "cos(t)", "sin(t)", "0"),
        ("\\langle -y^3,\\ x^3,\\ z \\rangle", "-y**3", "x**3", "z", "the paraboloid $z = 4 - x^2 - y^2$, $z \\ge 0$, oriented upward", "u*cos(v)", "u*sin(v)", "4 - u**2", "2", "", "2*cos(t)", "2*sin(t)", "0")]:
    if "cone" in stex:
        continue
    Pv, Qv, Rv = S(P), S(Q), S(R)
    cP, cQ, cR = sp.diff(Rv, y) - sp.diff(Qv, z), sp.diff(Pv, z) - sp.diff(Rv, x), sp.diff(Qv, x) - sp.diff(Pv, y)
    rr = sp.Matrix([S(sx), S(sy), S(sz)])
    nn = rr.diff(u).cross(rr.diff(v))
    Fv = sp.Matrix([cP, cQ, cR]).subs({x: rr[0], y: rr[1], z: rr[2]}, simultaneous=True)
    val = sp.integrate(sp.simplify(Fv.dot(nn)), (u, 0, S(u1)), (v, 0, 2 * sp.pi))
    if sp.simplify(val) != 0:
        cases.append({"Ftex": Ftex, "P": P, "Q": Q, "R": R, "stex": stex, "rx": rx, "ry": ry, "rz": rz, "ans": N(val)})
template("mvd-stokes-surface", "calc.vector-calculus", "Find $\\displaystyle\\iint_S (\\nabla\\times\\mathbf F)\\cdot\\mathbf n\\,dS$ for $\\mathbf F = {{Ftex}}$ and $S$ = {{stex}}.",
         value_part("Flux of the curl", "By Stokes' theorem this equals $\\oint_C \\mathbf F\\cdot d\\mathbf r$ around the boundary circle (counterclockwise from above for an upward normal), and equally the flux of the curl through the flat disc with the same boundary. Either is easier than the curved surface"),
         cases, {"expect": {"a": "line_work(P, Q, R, rx, ry, rz, 0, 2*pi)"}})

def dump():
    head = __doc__.strip().splitlines()
    text = "# " + "\n# ".join(l for l in head) + "\n# GENERATED: edit scripts/mvd_cases.py, not this file.\n\n"
    text += yaml.dump(T, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=None)
    OUT.write_text(text)
    print(f"{len(T)} templates, {sum(len(t['cases']) for t in T)} cases -> {OUT}")


if __name__ == "__main__":
    dump()
