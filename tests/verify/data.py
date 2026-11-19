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
         "c_cal": sp.Rational("4.184"), "c_atm": sp.Integer(101325),
         "c_M": {"H": sp.Rational("1.008"), "C": sp.Rational("12.011"), "N": sp.Rational("14.007"), "O": sp.Rational("15.999"),
                 "Na": sp.Rational("22.990"), "P": sp.Rational("30.974"), "S": sp.Rational("32.06"), "Cl": sp.Rational("35.45"),
                 "K": sp.Rational("39.098"), "Ca": sp.Rational("40.078"), "Fe": sp.Rational("55.845")}}
CONST["c_R"] = CONST["c_kB"] * CONST["c_NA"]
BASE.update(CONST)
BASE.update({"expand": sp.expand, "powsimp": sp.powsimp, "simplify": sp.simplify, "idiff": sp.idiff, "erf": sp.erf, "erfc": sp.erfc, "atan2": sp.atan2, "arg": sp.arg, "ceiling": sp.ceiling})
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
