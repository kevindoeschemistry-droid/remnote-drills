"""Independent sympy checks for calc.* prerequisites and ode1.exact / exact-if / modeling / recognize.

Every check recomputes from the defining property, never from the generator's formula:
  integrals        d/dx(antiderivative) == integrand
  partial fracs    A/(x-a) + B/(x-b) recombines to the given rational function
  complex          sympy complex arithmetic (exp(i*theta), powers, quadratic roots, re/im)
  index shifts     expand the original series and read off the coefficient of x^k
  partials         sympy diff; exactness via M_y == N_x
  exact ODEs       u_x == M, u_y == N; IVP constant from u(x0, y0)
  integrating fac  Kreyszig's R / R* test recomputed, F = exp(int R); solution: u_x Q - u_y P == 0
  modeling         sp.dsolve of the stated model (mixing, cooling, decay) or plug-in (logistic)
  recognize        property tests for each class; exactly one class must hold
"""
import sympy as sp

MINE = {
    "calc.u-sub", "calc.by-parts", "calc.partial-fractions", "calc.complex-euler", "calc.sigma-shift",
    "calc.multivariable", "ode1.exact", "ode1.exact-if", "ode1.modeling", "ode1.recognize",
}
k_ = sp.Symbol("k")
xr = sp.Symbol("x", real=True)
_PTS = [(sp.Rational(a_, 17), sp.Rational(b_, 13)) for a_, b_ in [(6, 5), (9, 11), (13, 4), (21, 17), (25, 8), (11, 20), (29, 15)]]


def _vals(e):
    """e at fixed points (x, y > 0), 30 digits; non-finite points skipped."""
    x, y = sp.Symbol("x"), sp.Symbol("y")
    out = []
    for px, py in _PTS:
        try:
            v = complex(sp.N(e.subs({x: px, y: py}), 30))
        except (TypeError, ZeroDivisionError, ValueError):
            continue
        if v == v and abs(v) != float("inf"):
            out.append(v)
    return out


def nzero(e):
    vs = _vals(e)
    return len(vs) >= 4 and all(abs(v) < 1e-18 for v in vs)


def nconst(e):
    vs = _vals(e)
    return len(vs) >= 4 and all(abs(v - vs[0]) < 1e-15 * max(1, abs(vs[0])) for v in vs)


def nvalue(e):
    return _vals(e)[0].real


def check(p, H):
    if p.get("skill") not in MINE:
        return None
    a = p["answer"]
    meta = p.get("meta", {})
    v = meta.get("variant", "")
    x, y, C, t = H.x, H.y, H.C, H.t
    Pp = lambda s: H.P(s).subs(sp.Symbol("k"), k_)
    zero = lambda e, syms=(x,): H.zero(e, syms)
    eq = lambda u, w: sp.simplify(u - w) == 0 or zero(u - w, tuple(sorted((u - w).free_symbols, key=str)) or (x,))

    # ── indefinite integrals (ode kind, y' = f(x)) ──
    if "integrand" in meta:
        f, F = Pp(meta["integrand"]), Pp(meta["F"])
        lhs, rhs = a["ref"].split("=", 1)
        return lhs.strip() == "y" and sp.simplify(Pp(rhs) - C - F) == 0 and zero(sp.diff(F, x) - f)

    if v == "pf-coeffs":
        A, B = (Pp(fl["ref"]) for fl in a["fields"])
        num = sum(c * x**i for i, c in enumerate(meta["num"]))
        ra, rb = meta["a"], meta["b"]
        return sp.simplify(A / (x - ra) + B / (x - rb) - num / ((x - ra) * (x - rb))) == 0

    # ── complex numbers ──
    if v == "euler-rect":
        z = sp.expand_complex(meta["R"] * sp.exp(sp.I * sp.pi * sp.Rational(meta["t"], 12)))
        A, B = (Pp(fl["ref"]) for fl in a["fields"])
        return sp.simplify(sp.re(z) - A) == 0 and sp.simplify(sp.im(z) - B) == 0
    if v == "euler-polar":
        z = Pp(meta["re"]) + sp.I * Pp(meta["im"])
        R = Pp(a["fields"][0]["ref"])
        th = Pp(a["fields"][1]["ref"])
        return sp.simplify(sp.Abs(z) - R) == 0 and sp.simplify(sp.expand_complex(R * sp.exp(sp.I * th)) - z) == 0
    if v == "euler-demoivre":
        z = sp.expand((meta["a0"] + meta["b0"] * sp.sqrt(meta["s"]) * sp.I) ** meta["n"])
        A, B = (Pp(fl["ref"]) for fl in a["fields"])
        return sp.simplify(sp.re(z) - A) == 0 and sp.simplify(sp.im(z) - B) == 0
    if v == "euler-quad":
        lam = sp.Symbol("lam")
        roots = sp.solve(lam**2 + meta["B"] * lam + meta["C"], lam)
        al, be = (Pp(fl["ref"]) for fl in a["fields"])
        return be > 0 and set(sp.nsimplify(r_) for r_ in roots) == {al + be * sp.I, al - be * sp.I}
    if v == "euler-reim":
        z = sp.expand_complex(sp.exp((meta["al"] + meta["be"] * sp.I) * xr))
        u, w = (Pp(fl["ref"]).subs(x, xr) for fl in a["fields"])
        return sp.simplify(sp.re(z) - u) == 0 and sp.simplify(sp.im(z) - w) == 0
    if v == "euler-combine":
        al, be = meta["al"], meta["be"]
        e1, e2 = sp.exp((al + be * sp.I) * xr), sp.exp((al - be * sp.I) * xr)
        val = (e1 + e2) / 2 if meta["plus"] else (e1 - e2) / (2 * sp.I)
        return sp.simplify(sp.expand_complex(val) - Pp(a["ref"]).subs(x, xr)) == 0

    # ── summation index shifts ──
    if v in ("sigma-reindex", "sigma-combine"):
        n_ = H.n
        S = 0
        for s_ in meta["sums"]:
            c = Pp(s_["coef"])
            S += sum(c.subs(n_, nn) * x ** (nn + s_["pow"]) for nn in range(s_["n0"], s_["n0"] + 16))
        S = sp.expand(S)
        k0 = meta["k0"]
        ck = Pp(a["fields"][1]["ref"]) if a["kind"] == "tuple" else Pp(a["ref"])
        if a["kind"] == "tuple":
            if Pp(a["fields"][0]["ref"]) != k0:
                return False
            lowest = min(i for i in range(0, 40) if S.coeff(x, i) != 0)
            if lowest != k0:
                return False
        return all(sp.simplify(S.coeff(x, kk) - ck.subs(k_, kk)) == 0 for kk in range(k0, k0 + 6))
    if v == "sigma-derivative":
        n_ = H.n
        b = Pp(meta["b"])
        Y = sum(b.subs(n_, nn) * x**nn for nn in range(0, 18))
        D = sp.expand(sp.diff(Y, x, meta["order"]))
        ck = Pp(a["ref"])
        return all(sp.simplify(D.coeff(x, kk) - ck.subs(k_, kk)) == 0 for kk in range(0, 6))

    # ── partial derivatives ──
    if v == "mv-partial":
        F = Pp(meta["F"])
        return eq(sp.diff(F, x if meta["wrt"] == "x" else y), Pp(a["ref"]))
    if v == "mv-mixed":
        F = Pp(meta["F"])
        return eq(sp.diff(F, x, y), Pp(a["ref"])) and sp.simplify(sp.diff(F, x, y) - sp.diff(F, y, x)) == 0
    if v == "mv-implicit":
        F = Pp(meta["F"])
        return eq(-sp.diff(F, x) / sp.diff(F, y), Pp(a["ref"]))
    if v == "mv-exact-test":
        M, N = Pp(meta["M"]), Pp(meta["N"])
        exact = sp.simplify(sp.diff(M, y) - sp.diff(N, x)) == 0
        return exact == meta["exact"] and a["correct"] == ("Exact" if exact else "Not exact")

    # ── exact equations ──
    if v.startswith("exact-"):
        M, N = Pp(meta["M"]), Pp(meta["N"])
        lhs, rhs = a["ref"].split("=", 1)
        U, Rv = Pp(lhs), Pp(rhs)
        ok = sp.simplify(sp.diff(M, y) - sp.diff(N, x)) == 0 and sp.simplify(sp.diff(U, x) - M) == 0 \
            and sp.simplify(sp.diff(U, y) - N) == 0 and sp.simplify(Pp(a["rhs"]) + M / N) == 0
        if a.get("ic"):
            x0, y0 = a["ic"]
            return ok and not Rv.has(C) and sp.simplify(U.subs({x: x0, y: y0}) - Rv) == 0
        return ok and Rv == C

    # ── integrating factors ──
    if v.startswith("if-"):
        Pe, Qe = Pp(meta["P"]), Pp(meta["Q"])
        Py, Qx = sp.diff(Pe, y), sp.diff(Qe, x)
        if sp.simplify(Py - Qx) == 0:
            return False
        R = sp.simplify((Py - Qx) / Qe)
        Rs = sp.simplify((Qx - Py) / Pe)
        okx = not R.has(y)
        oky = not Rs.has(x)
        if okx == oky:  # neither test, or both: ambiguous
            return False
        vv = "x" if okx else "y"
        if vv != meta["v"]:
            return False
        mu = sp.exp(sp.integrate(R, x)) if okx else sp.exp(sp.integrate(Rs, y))
        if sp.simplify(sp.diff(mu * Pe, y) - sp.diff(mu * Qe, x)) != 0:
            return False
        if v == "if-factor":
            ratio = sp.simplify(Pp(a["ref"]) / mu)
            return not ratio.has(x) and not ratio.has(y) and ratio != 0
        if v == "if-test":
            return a["correct"] == ("Integrating factor F(x)" if okx else "Integrating factor F*(y)")
        lhs, rhs = a["ref"].split("=", 1)
        U = Pp(lhs)
        return Pp(rhs) == C and U.has(y) and sp.simplify(sp.diff(U, x) * Qe - sp.diff(U, y) * Pe) == 0 \
            and sp.simplify(Pp(a["rhs"]) + Pe / Qe) == 0

    # ── modeling ──
    if v.startswith("model-"):
        T_ = sp.Symbol("T_")
        f_ = sp.Function("f")
        tt = t
        if v == "model-mixing":
            V, rate, c, y0 = meta["V"], meta["rate"], sp.nsimplify(meta["c"]), meta["y0"]
            sol = sp.dsolve(sp.Eq(f_(tt).diff(tt), rate * c - rate * f_(tt) / V), f_(tt), ics={f_(0): y0}).rhs
            tg = meta["target"]
            if tg == "fn":
                return sp.simplify(sol - Pp(a["ref"])) == 0
            if tg == "at":
                exp_ = sol.subs(tt, meta["T"])
            else:
                exp_ = sp.solve(sp.Eq(sol, sp.nsimplify(meta["yT"])), tt)[0]
            return abs(float(exp_) - float(Pp(a["ref"]))) < 1e-9 * max(1, abs(float(exp_)))
        if v == "model-cooling":
            kk = sp.Symbol("kk", positive=True)
            TA, T0, t1, T1 = meta["TA"], meta["T0"], meta["t1"], sp.nsimplify(meta["T1"])
            sol = sp.dsolve(sp.Eq(f_(tt).diff(tt), -kk * (f_(tt) - TA)), f_(tt), ics={f_(0): T0}).rhs
            kval = sp.solve(sp.Eq(sol.subs(tt, t1), T1), kk)[0]
            sol = sol.subs(kk, kval)
            tg = meta["target"]
            if tg == "k":
                exp_ = kval
            elif tg == "at":
                exp_ = sol.subs(tt, meta["t2"])
            else:
                exp_ = sp.solve(sp.Eq(sol, sp.nsimplify(meta["Tt"])), tt)[0]
            return abs(float(exp_) - float(Pp(a["ref"]))) < 1e-9 * max(1, abs(float(exp_)))
        if v == "model-decay":
            kk = sp.Symbol("kk", positive=True)
            y0 = meta.get("y0", 1)
            sgn = 1 if meta.get("growth") else -1
            sol = sp.dsolve(sp.Eq(f_(tt).diff(tt), sgn * kk * f_(tt)), f_(tt), ics={f_(0): y0}).rhs
            factor = 2 if meta.get("growth") else sp.Rational(1, 2)
            # numeric roots: sp.solve on exp(-5715 k) = 1/2 expands a huge polynomial
            kval = sp.nsolve(sol.subs(tt, meta["H"]) - factor * y0, kk, (0.01 / meta["H"], 10.0 / meta["H"]), solver="bisect")
            sol = sol.subs(kk, kval)
            if meta["target"] == "at":
                exp_ = sol.subs(tt, meta["T"])
            else:
                # numeric root of the model curve (sp.solve on the 5715-yr exponential is very slow)
                exp_ = sp.nsolve(sol - sp.nsimplify(meta["frac"]) * y0, tt, (1, 10 * meta["H"]), solver="bisect")
            return abs(float(exp_) - float(Pp(a["ref"]))) < 1e-9 * max(1, abs(float(exp_)))
        if v == "model-logistic":
            A, B = meta["A"], sp.Rational(*meta["B"])
            Y = Pp(a["ref"])
            return sp.simplify(sp.diff(Y, tt) - (A * Y - B * Y**2)) == 0 and sp.simplify(Y.subs(tt, 0) - meta["y0"]) == 0
        return False

    # ── which method? ──
    if v == "recognize":
        f = Pp(meta["f"])
        M = N = None
        if meta["form"] == "diff":
            M, N = Pp(meta["M"]), Pp(meta["N"])
            if not nzero(f + M / N):
                return False
        fx, fy = sp.diff(f, x), sp.diff(f, y)
        sep = nzero(f * sp.diff(f, x, y) - fx * fy)
        lin = nzero(sp.diff(f, y, 2))
        bern = False
        if not lin:
            h = f - y * fy  # = (1 - n) g(x) y^n for a Bernoulli right side
            nn = y * sp.diff(h, y) / h
            if nconst(nn):
                nv = nvalue(nn)
                if abs(nv) > 1e-6 and abs(nv - 1) > 1e-6:
                    bern = not nzero(f - h / (1 - sp.nsimplify(nv, rational=True, tolerance=1e-9)))  # linear part present
        homog = nzero(x * fx + y * fy)
        linarg = nconst(fx / fy)
        subst = homog or linarg
        exact = meta["form"] == "diff" and nzero(sp.diff(M, y) - sp.diff(N, x))
        flags = [sep, subst, lin, bern, exact]
        return sum(flags) == 1 and flags[meta["cls"]] and a["correct"] == a["options"][meta["cls"]]
    return False
