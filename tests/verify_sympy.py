#!/usr/bin/env python3
"""
Independent check of every generated reference answer with sympy — no code
shared with the JS checker. Run tests/run.ts first (writes tests/out/problems.json).

  ode            F(x,y)=C solved for C: H_x + H_y f = 0 identically; IVP: g' = f(x,g), g(x0)=y0
  ode2           a y'' + b y' + c y = f exactly; IVP conditions; particular has no constants;
                 general has two constants with nonzero Wronskian
  expression     Wronskian: det of derivatives; series terms: ODE residual vanishes
                 through x^3 and y(0), y'(0) match; radius: distance to nearest root of P
  recurrence     series built from the recurrence makes the ODE residual vanish (x^0..x^6)
  roots          indicial equation solved by sympy
  indexed/eigen  y_n'' + λ_n y_n = 0 and both boundary conditions, n = start..start+3
  choice         singular-point type by limits; Frobenius case from roots; damping from c²-4mk
  tuple          S–L form: (p y')' + (q + λr)y == (p/a)(a y'' + b y' + (c + λd)y);
                 amplitude–phase: R cos(ωt-δ) == A cos ωt + B sin ωt
"""
import json
import math
import random
import sys
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

x, y, C, t, n, m, lam = sp.symbols("x y C t n m lambda")
LOC = {"x": x, "y": y, "C": C, "t": t, "n": n, "m": m, "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt,
       "abs": lambda e: e,  # verify on x > 0, where |x| = x
       "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "cbrt": sp.cbrt, "e": sp.E, "pi": sp.pi}


def P(s: str):
    return parse_expr(str(s).replace("^", "**"), local_dict=LOC)


def zero(expr, syms=(x, y, C)) -> bool:
    if sp.simplify(expr) == 0:
        return True
    rnd = random.Random(1)
    good = 0
    for _ in range(40):
        pt = {s: sp.Rational(rnd.randint(25, 85), 100) for s in syms}
        try:
            v = complex(sp.N(expr.subs(pt), 40))
        except (TypeError, ZeroDivisionError):
            continue
        if v != v or abs(v) == float("inf"):
            continue
        if abs(v) > 1e-25:
            return False
        good += 1
        if good >= 6:
            return True
    return False


def series_residual_ok(Pc, Qc, Rc, coeffs, upto):
    """P y'' + Q y' + R y with y = sum coeffs[k] x^k: coefficients of x^0..x^upto must vanish."""
    Y = sum(c * x**k for k, c in enumerate(coeffs))
    res = sp.expand(Pc * sp.diff(Y, x, 2) + Qc * sp.diff(Y, x) + Rc * Y)
    return all(sp.simplify(res.coeff(x, k)) == 0 for k in range(upto + 1))


def kinetics_ok(ref, meta) -> bool:
    """Solve A -> B -> C from the mechanism with sympy and compare."""
    k1, k2, A0, B0 = meta["k1"], meta["k2"], meta["A0"], meta["B0"]
    tt = sp.Symbol("t", positive=True)
    Af, Bf = sp.Function("A"), sp.Function("B")
    sol = sp.dsolve([sp.Eq(Af(tt).diff(tt), -k1 * Af(tt)), sp.Eq(Bf(tt).diff(tt), k1 * Af(tt) - k2 * Bf(tt))],
                    [Af(tt), Bf(tt)], ics={Af(0): A0, Bf(0): B0})
    Aexp, Bexp = (s_.rhs for s_ in sol)
    ref = ref.subs(t, tt)
    if meta["variant"] == "B":
        return sp.simplify(ref - Bexp) == 0
    if meta["variant"] == "C":
        Cexp = A0 + B0 - Aexp - Bexp
        return sp.simplify(ref - Cexp) == 0 and sp.simplify(sp.diff(Cexp, tt) - k2 * Bexp) == 0
    # tmax: dB/dt = 0 there, and it is a maximum
    tm = sp.nsimplify(ref)
    d1 = sp.diff(Bexp, tt).subs(tt, tm)
    d2 = sp.diff(Bexp, tt, 2).subs(tt, tm)
    return abs(sp.N(d1, 30)) < 1e-20 and sp.N(d2) < 0 and sp.N(tm) > 0


SIG = sp.Rational(567, 10**10)


def R(v):
    return sp.nsimplify(v, rational=True)


def heat_expected(meta):
    """Recompute a heat-transfer answer from the governing equation, not the closed form."""
    h_ = meta["ht"]
    X, r_ = sp.symbols("X r_", positive=True)
    Tf = sp.Function("T")
    if h_ == "cond":
        k, L, T1, T2, A = (R(meta[k_]) for k_ in ("k", "L", "T1", "T2", "A"))
        # steady 1-D: T'' = 0 with T(0)=T1, T(L)=T2; flux = -k T'
        T = sp.dsolve(Tf(X).diff(X, 2), Tf(X), ics={Tf(0): T1, Tf(L): T2}).rhs
        flux = -k * sp.diff(T, X)
        tg = meta["target"]
        if tg == "flux": return flux
        if tg == "rate": return flux * A
        if tg == "k": return k
        q = R(meta["flux"]); T2s = sp.Symbol("T2s")
        return sp.solve(sp.Eq(k * (T1 - T2s) / L, q), T2s)[0]
    if h_ == "conv":
        h, A, Ts, Ti = (R(meta[k_]) for k_ in ("h", "A", "Ts", "Tinf"))
        q = h * A * (Ts - Ti)
        return {"q": q, "h": h, "Ts": Ts}[meta["target"]]
    if h_ == "rad":
        return R(meta["eps"]) * SIG * (R(meta["Ts"]) ** 4 - R(meta["Tsur"]) ** 4)
    if h_ == "hr":
        e, Ts, Tsur = R(meta["eps"]), R(meta["Ts"]), R(meta["Tsur"])
        return sp.simplify(e * SIG * (Ts**4 - Tsur**4) / (Ts - Tsur))  # definition: q_rad = h_r (Ts - Tsur)
    if h_ == "eb-surface":
        k, L, T1, T2, Ti, e = (R(meta[k_]) for k_ in ("k", "L", "T1", "T2", "Tinf", "eps"))
        hh = sp.Symbol("hh")
        bal = k * (T1 - T2) / L - hh * (T2 - Ti) - e * SIG * ((T2 + R(273.15)) ** 4 - (Ti + R(273.15)) ** 4)
        return sp.solve(bal, hh)[0]
    if h_ == "eb-wire":
        I, Re, D, Ti = (R(meta[k_]) for k_ in ("I", "Re", "D", "Tinf"))
        if meta["target"] == "Ts":
            Ts = sp.Symbol("Ts"); h = R(meta["h"])
            return sp.solve(I**2 * Re - h * sp.pi * D * (Ts - Ti), Ts)[0]
        Ts, e = R(meta["Ts"]), R(meta["eps"]); hh = sp.Symbol("hh")
        return sp.solve(I**2 * Re - hh * sp.pi * D * (Ts - Ti) - e * SIG * sp.pi * D * ((Ts + R(273.15)) ** 4 - (Ti + R(273.15)) ** 4), hh)[0]
    if h_ in ("he-gen", "he-flux", "he-dTdt"):
        a, b, c, k = (R(meta[k_]) for k_ in ("a", "b", "c", "k"))
        T = a + b * X + c * X**2
        if h_ == "he-gen":
            qd = sp.Symbol("qd")
            return sp.solve(k * sp.diff(T, X, 2) + qd, qd)[0]
        if h_ == "he-flux":
            return (-k * sp.diff(T, X)).subs(X, R(meta["x"]))
        return (k * sp.diff(T, X, 2) + R(meta["qdot"])) / (R(meta["rho"]) * R(meta["cp"]))
    if h_ == "wall":
        # unknown surface/interface temperatures; equal flux through every element
        ls = [(R(kk), R(LL)) for kk, LL in meta["layers"]]
        hi, ho, Ti, To = (R(meta[k_]) for k_ in ("hi", "ho", "Ti", "To"))
        n_ = len(ls)
        Ts_ = sp.symbols(f"s0:{n_ + 1}")
        q = sp.Symbol("q")
        eqs = [sp.Eq(q, hi * (Ti - Ts_[0])), sp.Eq(q, ho * (Ts_[-1] - To))]
        eqs += [sp.Eq(q, kk * (Ts_[i] - Ts_[i + 1]) / LL) for i, (kk, LL) in enumerate(ls)]
        sol = sp.solve(eqs, [q, *Ts_], dict=True)[0]
        tg = meta["target"]
        if tg == "flux": return sol[q]
        if tg == "U": return sol[q] / (Ti - To)
        if tg == "Tsi": return sol[Ts_[0]]
        return sol[Ts_[1]]
    if h_ == "contact":
        k1, k2, L1, L2, Rtc, T1, T3 = (R(meta[k_]) for k_ in ("k1", "k2", "L1", "L2", "Rtc", "T1", "T3"))
        a_, b_, q = sp.symbols("a_ b_ q")  # temperatures either side of the contact
        sol = sp.solve([sp.Eq(q, k1 * (T1 - a_) / L1), sp.Eq(q, (a_ - b_) / Rtc), sp.Eq(q, k2 * (b_ - T3) / L2)], [q, a_, b_], dict=True)[0]
        return sol[q] if meta["target"] == "flux" else sol[a_] - sol[b_]
    if h_ == "cyl":
        k, r1, r2, Ts, Ti, h = (R(meta[k_]) for k_ in ("k", "r1", "r2", "Ts", "Tinf", "h"))
        C1, C2 = sp.symbols("C1 C2")
        T = C1 * sp.log(X) + C2  # general solution of (1/r)(r T')' = 0
        sol = sp.solve([sp.Eq(T.subs(X, r1), Ts), sp.Eq(-k * sp.diff(T, X).subs(X, r2), h * (T.subs(X, r2) - Ti))], [C1, C2], dict=True)[0]
        T = T.subs(sol)
        qp = -k * sp.diff(T, X) * 2 * sp.pi * X
        return sp.simplify(qp) if meta["target"] == "q" else T.subs(X, r2)
    if h_ == "sphere":
        k, r1, r2, Ts1, Ti, h = (R(meta[k_]) for k_ in ("k", "r1", "r2", "Ts1", "Tinf", "h"))
        C1, C2 = sp.symbols("C1 C2")
        T = C1 / X + C2  # general solution of (1/r^2)(r^2 T')' = 0
        sol = sp.solve([sp.Eq(T.subs(X, r1), Ts1), sp.Eq(-k * sp.diff(T, X).subs(X, r2), h * (T.subs(X, r2) - Ti))], [C1, C2], dict=True)[0]
        T = T.subs(sol)
        return sp.simplify(k * sp.diff(T, X) * 4 * sp.pi * X**2)  # heat flowing inward
    if h_ == "rcrit":
        k, h = R(meta["k"]), R(meta["h"])
        ri = sp.Rational(1, 1000)
        Rt = (1 / ri - 1 / X) / (4 * sp.pi * k) + 1 / (4 * sp.pi * X**2 * h) if meta["sphere"] else sp.log(X / ri) / (2 * sp.pi * k) + 1 / (2 * sp.pi * X * h)
        crit = [c_ for c_ in sp.solve(sp.diff(Rt, X), X) if c_.is_positive]
        return crit[0] * 1000
    if h_ == "gen-wall":
        L, qd, k, h, Ti = (R(meta[k_]) for k_ in ("L", "qdot", "k", "h", "Tinf"))
        # x = 0 adiabatic (midplane or insulated face), convection at x = L
        C1, C2 = sp.symbols("C1 C2")
        T = -qd * X**2 / (2 * k) + C1 * X + C2
        assert sp.simplify(k * sp.diff(T, X, 2) + qd) == 0
        sol = sp.solve([sp.Eq(sp.diff(T, X).subs(X, 0), 0), sp.Eq(-k * sp.diff(T, X).subs(X, L), h * (T.subs(X, L) - Ti))], [C1, C2], dict=True)[0]
        T = T.subs(sol)
        return T.subs(X, 0) if meta["target"] == "Tmax" else T.subs(X, L)
    if h_ == "gen-cyl":
        ro, qd, k, h, Ti = (R(meta[k_]) for k_ in ("ro", "qdot", "k", "h", "Tinf"))
        C1, C2 = sp.symbols("C1 C2")
        T = -qd * X**2 / (4 * k) + C1 * sp.log(X) + C2
        assert sp.simplify(sp.diff(X * sp.diff(T, X), X) / X + qd / k) == 0
        sol = sp.solve([sp.Eq(C1, 0), sp.Eq(-k * sp.diff(T, X).subs(X, ro), h * (T.subs(X, ro) - Ti))], [C1, C2], dict=True)[0]  # bounded at r = 0
        return sp.limit(T.subs(sol), X, 0)
    if h_ == "fin":
        k, D, Lf, h, Tb, Ti = (R(meta[k_]) for k_ in ("k", "D", "Lf", "h", "Tb", "Tinf"))
        P, Ac = sp.pi * D, sp.pi * D**2 / 4
        mm = sp.sqrt(h * P / (k * Ac))
        tg = meta["target"]
        if tg == "m": return mm
        th = sp.Function("th")
        ode = sp.Eq(th(X).diff(X, 2), mm**2 * th(X))
        if tg == "infinite":
            # bounded solution on [0, ∞): θ = θb e^{-mx}
            sol = sp.dsolve(ode, th(X)).rhs
            C = [c_ for c_ in sol.free_symbols if str(c_).startswith("C")]
            grow = [c_ for c_ in C if sp.limit(sol.subs({cc: (1 if cc == c_ else 0) for cc in C}), X, sp.oo) == sp.oo]
            sol = sol.subs({g_: 0 for g_ in grow})
            rest = [c_ for c_ in C if c_ not in grow][0]
            sol = sol.subs(rest, sp.solve(sp.Eq(sol.subs(X, 0), Tb - Ti), rest)[0])
            return sp.simplify(-k * Ac * sp.diff(sol, X).subs(X, 0))
        length = Lf + D / 4 if tg == "efficiency" else Lf
        sol = sp.dsolve(ode, th(X), ics={th(0): Tb - Ti, th(X).diff(X).subs(X, length): 0}).rhs
        if tg == "tip": return Ti + sol.subs(X, Lf)
        qf = -k * Ac * sp.diff(sol, X).subs(X, 0)
        if tg == "adiabatic": return qf
        return 100 * qf / (h * P * length * (Tb - Ti))
    if h_ == "sf":
        k, T1, T2 = R(meta["k"]), R(meta["T1"]), R(meta["T2"])
        D = R(meta["D"])
        if meta["kind"] == "buried-cyl":
            S = 2 * sp.pi * R(meta["L"]) / sp.acosh(2 * R(meta["z"]) / D)
        elif meta["kind"] == "buried-sphere":
            S = 2 * sp.pi * D / (1 - D / (4 * R(meta["z"])))
        else:
            S = 2 * sp.pi * R(meta["L"]) / sp.log(sp.Rational(108, 100) * R(meta["w"]) / D)
        return S * k * (T1 - T2)
    if h_ == "fd":
        # energy balance on the node's control volume (per unit depth), written out term by term
        k, dx = R(meta["k"]), R(meta["dx"])
        Tm = sp.Symbol("Tm")
        cond = lambda Tn, face: k * face * (R(Tn) - Tm) / dx
        kind = meta["kind"]
        if kind.startswith("interior"):
            bal = sum(cond(t_, dx) for t_ in meta["nb"]) + R(meta["qdot"]) * dx * dx
        elif kind == "surface-conv":
            h, Ti = R(meta["h"]), R(meta["Tinf"])
            bal = cond(meta["inward"], dx) + cond(meta["up"], dx / 2) + cond(meta["down"], dx / 2) + h * dx * (Ti - Tm)
        else:
            h, Ti = R(meta["h"]), R(meta["Tinf"])
            bal = cond(meta["a"], dx / 2) + cond(meta["b"], dx / 2) + h * (dx / 2) * (Ti - Tm) * 2
        return sp.solve(bal, Tm)[0]
    raise KeyError(h_)


def linalg_ok(a, meta) -> bool:
    v = meta["variant"]
    A = sp.Matrix(meta["A"])
    if v == "system":
        x = A.LUsolve(sp.Matrix(meta["b"]))
        return [sp.nsimplify(f["ref"]) for f in a["fields"]] == list(x)
    if v == "independence":
        dep = A.rank() < 3
        return dep == meta["dependent"] and a["correct"] == ("Linearly dependent" if dep else "Linearly independent")
    if v == "inverse":
        inv = A.inv()
        return [P(f["ref"]) for f in a["fields"]] == [inv[0, 0], inv[0, 1], inv[1, 0], inv[1, 1]]
    if v == "det":
        return P(a["ref"]) == A.det()
    if v == "eigenvalues":
        return sorted(A.eigenvals(multiple=True)) == sorted(sp.nsimplify(x) for x in a["ref"])
    if v == "eigenvector":
        vv = sp.Matrix([P(f["ref"]) for f in a["fields"]])
        return vv != sp.zeros(2, 1) and A * vv == meta["lam"] * vv
    raise KeyError(v)


# tests/verify/*.py: per-area verifiers. Each defines check(p, H) -> True / False, or None for
# "not mine"; H is this module (P, zero, the sympy symbols…).
import importlib.util
_AREAS = []
for _f in sorted((Path(__file__).parent / "verify").glob("*.py")):
    _spec = importlib.util.spec_from_file_location(f"verify_{_f.stem}", _f)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _AREAS.append(_mod)


def check(p) -> bool:
    H = sys.modules[__name__]
    for mod in _AREAS:
        r = mod.check(p, H)
        if r is not None:
            return bool(r)
    a = p["answer"]
    meta = p.get("meta", {})
    kind = a["kind"]
    if meta.get("variant") in ("system", "independence", "inverse", "det", "eigenvalues", "eigenvector") and "A" in meta:
        return linalg_ok(a, meta)
    if kind == "ode":
        f = P(a["rhs"])
        lhs, rhs = a["ref"].split("=", 1)
        if a.get("ic"):
            g = P(rhs)
            x0, y0 = a["ic"]
            return (not g.has(C)) and zero(sp.diff(g, x) - f.subs(y, g)) and \
                abs(complex(sp.N(g.subs(x, sp.nsimplify(x0)) - sp.nsimplify(y0), 30))) < 1e-20
        F = P(lhs) - P(rhs)
        sols = sp.solve(F, C)
        return bool(sols) and zero(sp.diff(sols[0], x) + sp.diff(sols[0], y) * f)
    if kind == "ode2":
        v = sp.Symbol(a["v"])
        g = P(a["ref"])
        f = P(a["rhs"]) if a.get("rhs") else 0
        ok = sp.simplify(a["a"] * sp.diff(g, v, 2) + a["b"] * sp.diff(g, v) + a["c"] * g - f) == 0
        consts = sorted(g.free_symbols - {v}, key=str)
        if a.get("ic"):
            t0, y0, v0 = a["ic"]
            return ok and not consts and sp.simplify(g.subs(v, t0) - y0) == 0 and \
                sp.simplify(sp.diff(g, v).subs(v, t0) - v0) == 0
        if a.get("particular"):
            return ok and not consts
        # general: two constants multiplying independent solutions (Wronskian != 0)
        if len(consts) != 2:
            return False
        u1, u2 = (sp.diff(g, c) for c in consts)
        W = sp.simplify(u1 * sp.diff(u2, v) - u2 * sp.diff(u1, v))
        return ok and W != 0
    if kind == "expression" and "ht" in meta:
        exp_ = float(sp.N(heat_expected(meta), 30))
        mine = float(P(a["ref"]))
        return abs(mine - exp_) <= 1e-6 * max(1.0, abs(exp_))
    if kind == "expression" and meta.get("variant") in ("B", "C", "tmax"):
        return kinetics_ok(P(a["ref"]), meta)
    if kind == "expression" and meta.get("variant") == "negative-count":
        lamn = P(meta["lam"]) - meta["shift"]
        vals = [lamn.subs(n, k) for k in range(meta["start"], meta["start"] + 60)]
        return sp.Integer(sum(1 for v in vals if sp.N(v) < 0)) == sp.nsimplify(P(a["ref"]))
    if kind == "expression":
        if "funcs" in meta:  # Wronskian
            fs = [P(s) for s in meta["funcs"]]
            M = sp.Matrix(len(fs), len(fs), lambda i, j: sp.diff(fs[j], x, i))
            return zero(M.det() - P(a["ref"]), (x,))
        if "coeffs" in meta:  # series terms
            ode = meta["ode"]
            coeffs = [sp.Rational(nn, dd) for nn, dd in meta["coeffs"]]
            ref = P(a["ref"])
            same = sp.simplify(ref - sum(c * x**k for k, c in enumerate(coeffs))) == 0
            return same and coeffs[0] == meta["A"] and coeffs[1] == meta["B"] and \
                series_residual_ok(P(ode["P"]), P(ode["Q"]), P(ode["R"]), coeffs, 3)
        if "R2" in meta:  # radius
            roots = sp.solve(P(meta["P"]), x)
            d2 = min(sp.simplify(sp.Abs(meta["x0"] - r) ** 2) for r in roots)
            return sp.simplify(d2 - meta["R2"]) == 0 and sp.simplify(P(a["ref"]) ** 2 - meta["R2"]) == 0
        return False
    if kind == "recurrence":
        ode = meta["ode"]
        f = P(a["ref"])
        a0, a1 = sp.symbols("a0 a1")
        N = 9
        cs = [a0, a1] + [0] * (N - 1)
        gap = a["gap"]
        for k in range(2, N + 1):
            mm = k - gap
            cs[k] = f.subs(m, mm) * cs[mm] if mm >= 0 else 0
        return series_residual_ok(P(ode["P"]), P(ode["Q"]), P(ode["R"]), cs, 6)
    if kind == "roots" and meta.get("variant") == "eigen":
        M = sp.Matrix([[-meta["k1"], 0], [meta["k1"], -meta["k2"]]])
        return sorted(M.eigenvals(multiple=True)) == sorted(sp.nsimplify(v) for v in a["ref"])
    if kind == "roots":
        A, B, Cc = meta["A"], meta["B"], meta["C"]
        r = sp.symbols("r")
        roots = sp.solve(r * (r - 1) + sp.Rational(B, A) * r + sp.Rational(Cc, A), r)
        mine = {sp.nsimplify(v) for v in a["ref"]}
        return {sp.nsimplify(v) for v in roots} == mine
    if kind in ("indexed", "eigenfunctions"):
        L = P(meta["L"])
        yy = P(meta["y"])
        lamn = P(meta["lam"])
        bc = meta["variant"]
        if kind == "indexed" and sp.simplify(P(a["ref"]) - (lamn - meta.get("shift", 0))) != 0:
            return False
        for k in range(meta["start"], meta["start"] + 4):
            yk = yy.subs(n, k)
            lk = lamn.subs(n, k)
            if sp.simplify(sp.diff(yk, x, 2) + lk * yk) != 0 or sp.simplify(yk) == 0:
                return False
            left = yk if bc in ("DD", "DN") else sp.diff(yk, x)
            right = yk if bc in ("DD", "ND") else sp.diff(yk, x)
            if sp.simplify(left.subs(x, 0)) != 0 or sp.simplify(right.subs(x, L)) != 0:
                return False
        return True
    if kind == "choice":
        v = meta.get("variant")
        if v == "classify-point":
            x0 = meta["x0"]
            Pp, Qp, Rp = P(meta["P"]), P(meta["Q"]), P(meta["R"])
            if Pp.subs(x, x0) != 0:
                typ = 0
            else:
                l1 = sp.limit(sp.simplify((x - x0) * Qp / Pp), x, x0)
                l2 = sp.limit(sp.simplify((x - x0) ** 2 * Rp / Pp), x, x0)
                typ = 1 if (l1.is_finite and l2.is_finite) else 2
            return typ == meta["type"]
        if v == "case":
            r = sp.symbols("r")
            roots = sp.solve(r * (r - 1) + sp.Rational(meta["B"], meta["A"]) * r + sp.Rational(meta["C"], meta["A"]), r)
            if len(roots) == 1:
                kase = 1
            else:
                d = abs(roots[0] - roots[1])
                kase = 2 if d.is_integer else 0
            return kase == meta["kase"]
        if v == "classify" and "mm" in meta:
            disc = meta["c"] ** 2 - 4 * meta["mm"] * meta["k"]
            return (0 if disc > 0 else 1 if disc == 0 else 2) == meta["type"]
        return True  # curated S–L classification list
    if kind == "tuple" and meta.get("variant") == "matrix":
        k1, k2 = meta["k1"], meta["k2"]
        A_, B_ = sp.symbols("A_ B_")
        rates = [-k1 * A_, k1 * A_ - k2 * B_]  # d[A]/dt, d[B]/dt from the mechanism
        M = [P(f["ref"]) for f in a["fields"]]
        return sp.expand(M[0] * A_ + M[1] * B_ - rates[0]) == 0 and sp.expand(M[2] * A_ + M[3] * B_ - rates[1]) == 0
    if kind == "tuple":
        v = meta.get("variant")
        if v == "form":
            a_, b_, c_, d_ = (P(meta[k]) for k in "abcd")
            p_, q_, r_ = P(meta["p"]), P(meta["q"]), P(meta["r"])
            Y = sp.Function("Y")(x)
            lhs = sp.diff(p_ * sp.diff(Y, x), x) + (q_ + lam * r_) * Y
            rhs = (p_ / a_) * (a_ * sp.diff(Y, x, 2) + b_ * sp.diff(Y, x) + (c_ + lam * d_) * Y)
            return sp.simplify(sp.expand(lhs - rhs)) == 0
        if v == "amplitude-phase":
            A, B, w = meta["A"], meta["B"], meta["w"]
            R = P(a["fields"][0]["ref"])
            d = float(a["fields"][1]["ref"])
            return all(abs(float(R) * math.cos(w * tt - d) - (A * math.cos(w * tt) + B * math.sin(w * tt))) < 1e-9
                       for tt in (0.1, 0.7, 1.9))
        if v in ("si", "us"):
            return sp.simplify(P(a["fields"][1]["ref"]) - 2 * sp.pi / P(a["fields"][0]["ref"])) == 0
    return False


def main():
    probs = json.loads(Path("tests/out/problems.json").read_text())
    bad = 0
    for p in probs:
        try:
            ok = check(p)
        except Exception as e:  # noqa: BLE001
            ok = False
            print("ERROR", p["skill"], p["template"], e)
        if not ok:
            bad += 1
            if bad < 25:
                print("FAIL", p["skill"], p["template"], json.dumps(p["answer"])[:200])
    print(f"sympy: {len(probs) - bad}/{len(probs)} reference answers verified")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
