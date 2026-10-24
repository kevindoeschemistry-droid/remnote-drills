"""
Classical thermodynamics: rebuild every reference answer from first principles with
sympy — never from the generator's closed form.

  fundamental eq.  differentiate S(U,V,N) / U(S,V,N); Euler by integrating along the
                   scaling path; Gibbs–Duhem integrated at constant T
  first law        w = -∫P dV along the path; adiabat from the ODE n C_V dT = -P dV
  Legendre         solve T = ∂U/∂S (or P = -∂U/∂V) numerically, form U - TS (U + PV);
                   natural variables read off the prompt's definition; derivatives of F, G
  Maxwell          partials as Jacobians of a concrete model (van der Waals F(T,V), or a
                   local G(T,P) whose second derivatives match α, κ_T, c_P); F = -∫P dV
  stability        Hessian of S(U,V); vdW ∂P/∂V; critical point from P_V = P_VV = 0
  phase            dsolve Clausius–Clapeyron dP/dT = ΔH P/(RT²); Clapeyron from dμ_α = dμ_β
  solutions        μ_i = μ_i° + RT ln(...) equalities; ΔS_mix = -∂ΔG_mix/∂T; Margules ∂G^ex/∂n_A
  equilibrium      Σ ν_i μ_i = 0 solved for ξ with nsolve; ΔG° = ΔH° - TΔS° for van 't Hoff
"""
import math
import re

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

Rg = sp.Rational(8314, 1000)
NAMES = ["U", "V", "N", "A", "S", "T", "P", "R", "a", "b"]
SY = {k: sp.Symbol(k, positive=True) for k in NAMES}
U, V, N, A, S, T, P, Rs, a, b = (SY[k] for k in NAMES)
LOC = {**SY, "log": sp.log, "ln": sp.log, "sqrt": sp.sqrt, "exp": sp.exp, "pi": sp.pi}


def parse(s):
    return parse_expr(str(s).replace("^", "**"), local_dict=LOC)


def Rat(v):
    """the decimal as written (0.00015 -> 3/20000), never the binary float"""
    return sp.Rational(repr(float(v))) if not isinstance(v, int) else sp.Integer(v)


def Num(v):
    """inputs as 40-digit floats: exp/log of large exact rationals is needlessly slow"""
    return sp.Float(repr(float(v)), 40)


def Qf(pair):
    return sp.Rational(pair[0], pair[1])


def close(x, y, tol=1e-6):
    x, y = float(x), float(y)
    return abs(x - y) <= tol * max(1e-300, abs(y)) or abs(x - y) < 1e-300


def same_fn(ref, expected, points):
    """ref and expected agree at every point (numerically, 30 digits)."""
    for pt in points:
        r_ = complex(sp.N(ref.subs(pt), 30))
        e_ = complex(sp.N(expected.subs(pt), 30))
        if abs(r_.imag) > 1e-20 or abs(e_.imag) > 1e-20 or not close(r_.real, e_.real, 1e-9):
            return False
    return True


PTS = [
    {U: sp.Rational(3, 2), V: sp.Rational(5, 2), N: sp.Rational(7, 10), A: sp.Rational(6, 5), S: sp.Rational(9, 10),
     T: sp.Rational(13, 10), P: sp.Rational(4, 5), Rs: sp.Rational(8314, 1000), a: sp.Rational(3, 7), b: sp.Rational(1, 9)},
    {U: sp.Rational(1, 3), V: sp.Rational(9, 2), N: sp.Rational(2), A: sp.Rational(1, 2), S: sp.Rational(5, 3),
     T: sp.Rational(7, 3), P: sp.Rational(11, 5), Rs: sp.Rational(1), a: sp.Rational(2), b: sp.Rational(1, 5)},
    {U: sp.Rational(5), V: sp.Rational(3), N: sp.Rational(1, 2), A: sp.Rational(3), S: sp.Rational(2, 7),
     T: sp.Rational(1, 2), P: sp.Rational(3, 10), Rs: sp.Rational(3, 2), a: sp.Rational(1, 4), b: sp.Rational(1, 3)},
]


def bisect(f, lo, hi, it=200):
    """root of a monotone f on [lo, hi] (log-spaced bisection, floats via mpmath)."""
    import mpmath as mp
    mp.mp.dps = 40
    flo = f(lo)
    for _ in range(it):
        mid = mp.sqrt(lo * hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return mp.sqrt(lo * hi)


def jac(X, Y, Z, u, v):
    """(∂X/∂Y)_Z with X, Y, Z functions of independent (u, v)."""
    num = sp.diff(X, u) * sp.diff(Z, v) - sp.diff(X, v) * sp.diff(Z, u)
    den = sp.diff(Y, u) * sp.diff(Z, v) - sp.diff(Y, v) * sp.diff(Z, u)
    return num / den


# ── per-case expected values ─────────────────────────────────────────────────
def expected_numeric(meta):
    th = meta["th"]
    if th == "fe-ideal":
        c, n_, U_, V_ = Rat(meta["c"]), Rat(meta["N"]), Rat(meta["U"]), Rat(meta["V"])
        Sx = N * Rg * (c * sp.log(U / N) + sp.log(V / N)) + N * sp.Symbol("s0")
        invT = sp.diff(Sx, U)
        Tv = 1 / invT
        Pv = Tv * sp.diff(Sx, V)
        sub = {U: U_, V: V_, N: n_}
        return (Tv if meta["target"] == "T" else Pv).subs(sub)
    if th == "fe-euler":
        lam = sp.Symbol("lam")
        T_, P_, V_, S_, n_ = (Rat(meta[k]) for k in ("T", "P", "V", "S", "N"))
        mu = sp.Symbol("mu")
        # U(λ) along λ(S, V, N) at fixed intensives: dU/dλ = T S - P V + μ N
        Uint = sp.integrate(T_ * S_ - P_ * V_ + mu * n_, (lam, 0, 1))
        if meta["target"] == "U":
            return Uint.subs(mu, Rat(meta["mu"]))
        return sp.solve(sp.Eq(Uint, Rat(meta["U"])), mu)[0]
    if th == "fe-gd":
        T_, P1, P2 = Rat(meta["T"]), Rat(meta["P1"]), Rat(meta["P2"])
        Pp = sp.Symbol("Pp", positive=True)
        # S dT - V dP + N dμ = 0 at dT = 0, ideal gas V/N = RT/P
        return sp.integrate(Rg * T_ / Pp, (Pp, P1, P2))
    if th in ("fl-iso", "fl-adia", "fl-isobaric", "fl-isochoric"):
        n_ = Rat(meta["n"])
        Vv = sp.Symbol("Vv", positive=True)
        if th == "fl-iso":
            T_, V1, V2 = Rat(meta["T"]), Rat(meta["V1"]), Rat(meta["V2"])
            w = -sp.integrate(n_ * Rg * T_ / Vv, (Vv, V1, V2))
            dU = 0  # U = n c R T, T fixed
            return w if meta["target"] == "w" else dU - w
        c = Rat(meta["c"])
        if th == "fl-adia":
            T1, V1, V2 = Rat(meta["T1"]), Rat(meta["V1"]), Rat(meta["V2"])
            Tf = sp.Function("Tf")
            # dU = δw: n c R dT = -(nRT/V) dV
            sol = sp.dsolve(sp.Eq(n_ * c * Rg * Tf(Vv).diff(Vv), -n_ * Rg * Tf(Vv) / Vv), Tf(Vv), ics={Tf(V1): T1}).rhs
            if meta["target"] == "T2":
                return sol.subs(Vv, V2)
            return -sp.integrate(n_ * Rg * sol / Vv, (Vv, V1, V2))
        if th == "fl-isobaric":
            P_, T1, T2 = Rat(meta["P"]), Rat(meta["T1"]), Rat(meta["T2"])
            V1, V2 = n_ * Rg * T1 / P_, n_ * Rg * T2 / P_
            w = -sp.integrate(P_, (Vv, V1, V2))
            dU = n_ * c * Rg * (T2 - T1)
            return {"w": w, "dU": dU, "q": dU - w}[meta["target"]]
        V_, T1, T2 = Rat(meta["V"]), Rat(meta["T1"]), Rat(meta["T2"])
        if meta["target"] == "q":
            w = 0  # -∫P dV with V fixed
            return n_ * c * Rg * (T2 - T1) - w
        return n_ * Rg * T2 / V_ / 1000
    if th in ("mx-meas", "mx-triple"):
        Tt, Pp = sp.symbols("Tt Pp")
        T0, P0 = Rat(meta["T"]), Rat(meta.get("P", 100000))
        V0, al, ka, Cp = Rat(meta["V"]), Rat(meta["alpha"]), Rat(meta["kappa"]), Rat(meta["Cp"])
        dT, dP = Tt - T0, Pp - P0
        S0 = 100
        G = -S0 * dT + V0 * dP + (-Cp / T0) * dT**2 / 2 + V0 * al * dT * dP + (-V0 * ka) * dP**2 / 2
        Sm, Vm = -sp.diff(G, Tt), sp.diff(G, Pp)
        Um = G + Tt * Sm - Pp * Vm
        Hm = G + Tt * Sm
        at = {Tt: T0, Pp: P0}
        if th == "mx-triple":
            return (jac(Pp, Tt, Vm, Tt, Pp).subs(at) * Rat(meta["dT"]) / 100000)
        tg = meta["target"]
        if tg == "dSdV": return jac(Sm, Vm, Tt, Tt, Pp).subs(at)
        if tg == "dSdP": return jac(Sm, Pp, Tt, Tt, Pp).subs(at)
        if tg == "dUdV": return jac(Um, Vm, Tt, Tt, Pp).subs(at)
        if tg == "dHdP": return jac(Hm, Pp, Tt, Tt, Pp).subs(at)
        CpM = Tt * jac(Sm, Tt, Pp, Tt, Pp)
        CvM = Tt * jac(Sm, Tt, Vm, Tt, Pp)
        return (CpM - CvM).subs(at)
    if th in ("st-tc", "st-kappa"):
        a_, b_ = Rat(meta["a"]), Rat(meta["b"])
        Pv = Rg * T / (V - b_) - a_ / V**2
        if th == "st-tc":
            sols = sp.solve([sp.diff(Pv, V), sp.diff(Pv, V, 2)], [T, V], dict=True)
            sols = [s_ for s_ in sols if s_[V] > b_]
            return sols[0][T]
        pt = {T: Rat(meta["T"]), V: Rat(meta["V"])}
        return (-1 / (V * sp.diff(Pv, V))).subs(pt)
    if th in ("pe-P", "pe-dH", "pe-T"):
        Tt = sp.Symbol("Tt", positive=True)
        Pf = sp.Function("Pf")
        dH = sp.Symbol("dH", positive=True)
        # Clapeyron with ΔV = RT/P (ideal vapor, liquid volume neglected)
        T1, P1 = Num(meta["T1"]), Num(meta["P1"])
        sol = sp.dsolve(sp.Eq(Pf(Tt).diff(Tt), dH / (Tt * (Rg * Tt / Pf(Tt)))), Pf(Tt), ics={Pf(T1): P1}).rhs
        if th == "pe-P":
            return sol.subs({dH: Num(meta["dH"]), Tt: Num(meta["T2"])}) / 1000
        if th == "pe-dH":
            f = sp.log(sol.subs(Tt, Num(meta["T2"]))) - sp.log(Num(meta["P2"]))
            return sp.nsolve(f, dH, (10**3, 10**6), solver="bisect", prec=40) / 1000
        f = sp.log(sol.subs(dH, Num(meta["dH"]))) - sp.log(Num(meta["P2"]))
        return sp.nsolve(f, Tt, (T1 / 2, 2 * T1), solver="bisect", prec=40)
    if th in ("pe-slope", "pe-shift"):
        slope, dTs = sp.symbols("slope dTs")
        sl, sg, vl, vg = sp.symbols("sl sg vl vg")
        T_, dH = Num(meta["T"]), Num(meta["dH"])
        # dμ_α = dμ_β along the line: -s_α dT + v_α dP = -s_β dT + v_β dP, with s_β - s_α = ΔH/T
        eq = sp.Eq(-sl + vl * slope, -sg + vg * slope)
        sv = sp.solve(eq, slope)[0]
        dV = Rg * T_ / Num(meta["P"]) if meta.get("phase") == "vap" else Num(meta["dV"])
        val = sv.subs({sg: sl + dH / T_}).subs({vg: vl + dV})
        val = sp.simplify(val)
        if th == "pe-slope":
            return val
        return Num(meta["dP"]) / val
    if th in ("so-dS", "so-dG"):
        nA, nB = Rat(meta["nA"]), Rat(meta["nB"])
        Tt = sp.Symbol("Tt", positive=True)
        n = nA + nB
        # μ_i - μ_i* = RT ln x_i
        Gmix = nA * Rg * Tt * sp.log(nA / n) + nB * Rg * Tt * sp.log(nB / n)
        if th == "so-dS":
            return -sp.diff(Gmix, Tt)
        return Gmix.subs(Tt, Rat(meta["T"]))
    if th == "so-raoult":
        RTs, mug, x_, p_, Pst = sp.symbols("RTs mug x_ p_ Pst", positive=True)
        mustar = mug + RTs * sp.log(Pst)  # pure liquid in equilibrium with its vapor at P*
        p_sol = sp.solve(sp.Eq(mustar + RTs * sp.log(x_), mug + RTs * sp.log(p_)), p_)[0]
        xA = Rat(meta["xA"])
        pA = p_sol.subs({x_: xA, Pst: Rat(meta["PA"])})
        pB = p_sol.subs({x_: 1 - xA, Pst: Rat(meta["PB"])})
        return (pA + pB) / 1000 if meta["target"] == "P" else pA / (pA + pB)
    if th == "so-henry":
        RTs, mug, x_, p_, K_ = sp.symbols("RTs mug x_ p_ K_", positive=True)
        mudag = mug + RTs * sp.log(K_)  # infinite-dilution reference, defines K_H
        eq = sp.Eq(mudag + RTs * sp.log(x_), mug + RTs * sp.log(p_))
        if meta["target"] == "x":
            return sp.solve(eq, x_)[0].subs({p_: Rat(meta["p"]), K_: Rat(meta["K"])})
        return sp.solve(eq, p_)[0].subs({x_: Rat(meta["x"]), K_: Rat(meta["K"])}) / 100000
    if th == "so-gamma":
        RTs, mug, gam = sp.symbols("RTs mug gam", positive=True)
        Pst, xA, pA = Rat(meta["PA"]), Rat(meta["xA"]), Rat(meta["pA"])
        eq = sp.Eq(mug + RTs * sp.log(Pst) + RTs * sp.log(gam * xA), mug + RTs * sp.log(pA))
        return sp.solve(eq, gam)[0]
    if th == "so-margules":
        nA, nB = sp.symbols("nA nB", positive=True)
        W, T_, xA = Rat(meta["W"]), Rat(meta["T"]), Rat(meta["xA"])
        Gex = W * nA * nB / (nA + nB)
        lng = sp.diff(Gex, nA).subs({nA: xA, nB: 1 - xA}) / (Rg * T_)
        return sp.exp(lng)
    if th in ("ce-K", "ce-dG"):
        Qs, dG = sp.symbols("Qs dG")
        T_ = Num(meta["T"])
        eq = sp.Eq(dG + Rg * T_ * sp.log(Qs), 0)  # ΔG = 0 at equilibrium, Q = K
        if th == "ce-K":
            return sp.solve(eq.subs(dG, Num(meta["dG"])), Qs)[0]
        return sp.solve(eq.subs(Qs, Num(meta["K"])), dG)[0] / 1000
    if th == "ce-vh":
        dH, dS = sp.symbols("dH dS")
        T1, T2, K1 = Num(meta["T1"]), Num(meta["T2"]), Num(meta["K1"])
        dG = lambda Tq: dH - Tq * dS  # constant ΔH°, ΔS°
        if meta["target"] == "K2":
            dSv = sp.solve(sp.Eq(-dG(T1) / (Rg * T1), sp.log(K1)), dS)[0].subs(dH, Num(meta["dH"]))
            return sp.exp(-dG(T2).subs({dH: Num(meta["dH"]), dS: dSv}) / (Rg * T2))
        K2 = Num(meta["K2"])
        sol = sp.solve([sp.Eq(-dG(T1) / (Rg * T1), sp.log(K1)), sp.Eq(-dG(T2) / (Rg * T2), sp.log(K2))], [dH, dS], dict=True)[0]
        return sol[dH] / 1000
    if th == "ce-extent":
        xi = sp.Symbol("xi")
        n0, Ptot, K = Num(meta["n0"]), Num(meta["P"]), Num(meta["K"])
        Tq = 298  # any T: μ° differences are fixed by K
        dG0 = -Rg * Tq * sp.log(K)
        rx = meta["rx"]
        if rx == "A=2B":
            species = [(-1, n0 - xi), (2, 2 * xi)]
        elif rx == "A=B+C":
            species = [(-1, n0 - xi), (1, xi), (1, xi)]
        else:
            species = [(-1, n0 - xi), (-1, n0 - xi), (2, 2 * xi)]
        ntot = sum(ni for _, ni in species)
        # Σ ν_i μ_i = ΔG° + RT Σ ν_i ln(p_i/P°) = 0
        f = dG0 + sum(nu * Rg * Tq * sp.log(ni / ntot * Ptot) for nu, ni in species)
        return sp.nsolve(f, xi, (n0 * sp.Rational(1, 10**9), n0 * (1 - sp.Rational(1, 10**9))), solver="bisect", prec=40)
    raise KeyError(th)


def expected_symbolic(meta):
    th = meta["th"]
    if th == "fe-S":
        g_, b_, c_ = Qf(meta["g"]), Qf(meta["b"]), Qf(meta["c"])
        Sx = A * U**g_ * V**b_ * N**c_
        Tv = 1 / sp.diff(Sx, U)
        return {"T": Tv, "P": Tv * sp.diff(Sx, V), "mu": -Tv * sp.diff(Sx, N)}[meta["target"]]
    if th == "fe-U":
        p_, q_, r_ = Qf(meta["p"]), Qf(meta["q"]), Qf(meta["r"])
        Ux = A * S**p_ * V**q_ * N**r_
        return {"T": sp.diff(Ux, S), "P": -sp.diff(Ux, V), "mu": sp.diff(Ux, N)}[meta["target"]]
    if th == "lg-derive":
        c = Rat(meta["c"])
        if meta["model"] == "vdw":
            F = -N * Rs * T * (sp.log((V - N * b) / N) + c * sp.log(T) + 1) - a * N**2 / V
        else:
            F = -N * Rs * T * (sp.log(V / N) + c * sp.log(T) + 1)
        return {"P": -sp.diff(F, V), "S": -sp.diff(F, T), "mu": sp.diff(F, N)}[meta["target"]]
    if th == "lg-gh":
        Gx = meta["a"] + meta["b"] * T + meta["c"] * (T * sp.log(T) if meta["form"] == "TlnT" else T**2)
        Sx = -sp.diff(Gx, T)
        return Sx if meta["target"] == "S" else Gx + T * Sx
    if th == "mx-eos":
        e = meta["eos"]
        Pv = {
            "vdw": Rs * T / (V - b) - a / V**2,
            "berthelot": Rs * T / (V - b) - a / (T * V**2),
            "virial": Rs * T / V + (b * Rs * T - a) / V**2,
            "rk": Rs * T / (V - b) - a / (sp.sqrt(T) * V * (V + b)),
        }[e]
        F = -sum(sp.integrate(term, V) for term in sp.Add.make_args(sp.apart(Pv, V)))  # + f(T), which drops out of both V-derivatives below
        Sx = -sp.diff(F, T)
        Ux = F + T * Sx
        return sp.diff(Sx, V) if meta["target"] == "dSdV" else sp.diff(Ux, V)
    raise KeyError(th)


def numeric_fn_check(ref, meta):
    """Legendre transforms and C_V: compare at sample points, solving the conjugate equation numerically."""
    import mpmath as mp
    mp.mp.dps = 40
    th = meta["th"]
    for pt in PTS:
        fv = {k: mp.mpf(sp.Rational(v).p) / sp.Rational(v).q for k, v in pt.items()}
        if th == "lg-F":
            p_, q_, r_ = (float(Qf(meta[k])) for k in "pqr")
            Ux = lambda s_: fv[A] * s_**p_ * fv[V]**q_ * fv[N]**r_
            dU = lambda s_: (Ux(s_ * (1 + mp.mpf(10)**-15)) - Ux(s_ * (1 - mp.mpf(10)**-15))) / (2 * s_ * mp.mpf(10)**-15)
            s_ = bisect(lambda s_: dU(s_) - fv[T], mp.mpf(10)**-20, mp.mpf(10)**20)
            want = Ux(s_) - fv[T] * s_
        elif th == "lg-H":
            p_, q_, r_ = (float(Qf(meta[k])) for k in "pqr")
            Ux = lambda v_: fv[A] * fv[S]**p_ * v_**q_ * fv[N]**r_
            Pm = lambda v_: -(Ux(v_ * (1 + mp.mpf(10)**-15)) - Ux(v_ * (1 - mp.mpf(10)**-15))) / (2 * v_ * mp.mpf(10)**-15)
            v_ = bisect(lambda v_: Pm(v_) - fv[P], mp.mpf(10)**-20, mp.mpf(10)**20)
            want = Ux(v_) + fv[P] * v_
        elif th == "st-cv":
            g_, b_, c_ = (float(Qf(meta[k])) for k in "gbc")
            dSdU = lambda u_, T_: fv[A] * g_ * u_**(g_ - 1) * fv[V]**b_ * fv[N]**c_ - 1 / T_
            Uof = lambda T_: bisect(lambda u_: -dSdU(u_, T_), mp.mpf(10)**-30, mp.mpf(10)**30)
            h = fv[T] * mp.mpf(10)**-12
            want = (Uof(fv[T] + h) - Uof(fv[T] - h)) / (2 * h)
        else:
            raise KeyError(th)
        got = sp.N(ref.subs(pt), 30)
        if not close(complex(got).real, float(want), 1e-6):
            return False
    return True


def natural_from_prompt(prompt):
    m_ = re.search(r"Define \$(.*?)\$", prompt)
    if not m_:
        return {"S", "V", "N"}
    rhs = m_.group(1).split("=")[1]
    rhs = rhs.replace("H", "U + PV").replace("F", "U - TS")
    nat = {"S", "V", "N"}
    if "TS" in rhs:
        nat = (nat - {"S"}) | {"T"}
    if "PV" in rhs:
        nat = (nat - {"V"}) | {"P"}
    if "\\mu N" in rhs:
        nat = (nat - {"N"}) | {"μ"}
    return nat


def maxwell_ok(meta, a_):
    """Partials of a van der Waals fluid from F(T, V) via Jacobians: the marked option equals
    the target and no other option does."""
    Tt, Vv = sp.symbols("Tt Vv", positive=True)
    aa, bb, c = sp.Rational(364, 1000), sp.Rational(4267, 10**8), sp.Rational(5, 2)
    F = -Rg * Tt * (sp.log(Vv - bb) + c * sp.log(Tt)) - aa / Vv
    fns = {"T": Tt, "V": Vv, "S": -sp.diff(F, Tt), "P": -sp.diff(F, Vv)}
    at = {Tt: 300, Vv: sp.Rational(1, 1000)}
    val = lambda X, Y, Z: float(sp.N(jac(fns[X], fns[Y], fns[Z], Tt, Vv).subs(at), 30))
    tgt = val(*meta["target"])
    hits = [i for i, (pp, s_) in enumerate(meta["options"]) if close(s_ * val(*pp), tgt, 1e-9)]
    texts = [("-" if s_ < 0 else "") + f"(∂{pp[0]}/∂{pp[1]})_{pp[2]}" for pp, s_ in meta["options"]]
    return hits == [meta["correct"]] and texts == a_["options"] and a_["options"][meta["correct"]] == a_["correct"]


def check(p, H):
    if not p["skill"].startswith("thermo."):
        return None
    a_ = p["answer"]
    meta = p.get("meta", {})
    th = meta.get("th")
    if a_["kind"] == "choice":
        if th == "lg-natural":
            want = natural_from_prompt(p["prompt"])
            return {x.strip() for x in a_["correct"].split(",")} == want
        if th == "mx-pick":
            return maxwell_ok(meta, a_)
        if th == "st-concave":
            g_, b_, c_ = Qf(meta["g"]), Qf(meta["b"]), Qf(meta["c"])
            Sx = U**g_ * V**b_  # A = N = 1
            Hm = sp.hessian(Sx, (U, V))
            stable = True
            for pt in ({U: 1, V: 1}, {U: 2, V: sp.Rational(1, 3)}, {U: sp.Rational(1, 5), V: 7}):
                h_ = Hm.subs(pt)
                if not (h_[0, 0] < 0 and h_.det() > 0):
                    stable = False
            return a_["correct"] == ("Stable" if stable else "Unstable")
        if th == "st-vdw":
            Pv = Rg * T / (V - Rat(meta["b"])) - Rat(meta["a"]) / V**2
            d = sp.diff(Pv, V).subs({T: Rat(meta["T"]), V: Rat(meta["V"])})
            return a_["correct"].startswith("Stable") == bool(d < 0)
        if th == "ce-dir":
            T_ = Rat(meta["T"])
            Qv = Rat(meta["pB"]) ** 2 / Rat(meta["pA"])
            dG = Rat(meta["dG"]) + Rg * T_ * sp.log(Qv)
            return a_["correct"].startswith("Forward") == bool(sp.N(dG) < 0)
        return False
    ref = parse(a_["ref"])
    if a_.get("rel"):
        return close(ref, sp.N(expected_numeric(meta), 30))
    if th in ("lg-F", "lg-H", "st-cv"):
        return numeric_fn_check(ref, meta)
    exp_ = expected_symbolic(meta)
    allowed = {SY[v] for v in a_.get("vars", [])}
    if not ref.free_symbols <= allowed:
        return False
    return same_fn(ref, exp_, PTS)
