"""Problems as data (drills/problems/*.yaml): the generic verifier.

Each template's `verify` block is solved here from the problem's givens alone; nothing in it is
the generator's formula. For every part, the value the generator claims must match.

  ode        the governing equation in T(var); dsolve gives the general solution
  bcs        "lhs = rhs" with T(v), dT(v) = T'(v), lim0(e) = limit var -> 0+; fixes the constants
  expect     label -> expression in the solved T, dT and the givens; must equal the part's value
  residuals  balances that must vanish (part labels stand for the claimed values); a residual
             with the variable left in must vanish at every point
"""
import json
import random
from pathlib import Path

import sympy as sp

_GEN = Path(__file__).resolve().parents[2] / "src/drills/skills.generated.json"
TEMPLATES = {t["template"]: t for t in json.loads(_GEN.read_text()).get("problems", [])}

BASE = {"diff": sp.diff, "pi": sp.pi, "log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt, "Abs": sp.Abs,
        "solve": sp.solve, "sin": sp.sin, "cos": sp.cos, "tanh": sp.tanh, "cosh": sp.cosh, "sinh": sp.sinh}


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


def check(p, H):
    meta = p.get("meta", {})
    name = meta.get("data")
    if name is None:
        return None
    t = TEMPLATES[name]
    v = t["verify"]
    # radial coordinates are positive (log r, limits at 0+); a Cartesian x may be negative
    var = sp.Symbol(v.get("var", "x"), positive=True) if v.get("var") == "r" else sp.Symbol(v.get("var", "x"), real=True)
    labels = [q["label"] for q in t["parts"]]
    claimed = {lab: num(float(part["answer"]["ref"])) for lab, part in zip(labels, p["parts"])
               if part["answer"]["kind"] == "expression"}
    ns = {**BASE, **{k: num(x) for k, x in meta["given"].items()}, v.get("var", "x"): var}
    ns_parts = {**ns, **claimed}

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
        want = float(ev(expr, ns_parts))
        got = float(claimed[lab])
        if abs(want - got) > 1e-6 * max(1.0, abs(want)):
            print(f"  {name}: {lab} claimed {got}, verifier gets {want}")
            return False
    for res in v.get("residuals") or []:
        if not vanishes(ev(res, ns_parts), var):
            print(f"  {name}: residual {res} = {float(ev(res, ns_parts)) if var not in ev(res, ns_parts).free_symbols else '…'}")
            return False
    # every numeric part was checked by something above (the build enforces it; make sure here too)
    used = json.dumps([v.get("ode"), v.get("bcs"), v.get("residuals"), list((v.get("expect") or {}).keys())])
    return all(lab in used for lab in claimed)
