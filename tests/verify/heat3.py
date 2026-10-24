"""
Independent checks for src/drills/gen-heat3.ts (Incropera 8e Ch 6, §7.6, Ch 10, 12, 14).

Every answer is rebuilt from the governing physics, not from the generator's closed form:
  boundary layers  average h by integrating h_x over the plate; Re/transition by solving Re(x) = Re_c;
                   Colburn by solving C_f/2 = St Pr^(2/3) for h; the 0.332 in Nu_x checked against a
                   shooting solution of the Blasius equation
  tube banks       V_max from continuity through the narrowest flow area; outlet temperature by
                   dsolve of the air energy balance along the tube area; q' = m' c_p (T_o - T_i)
  boiling          Rohsenow solved for the unknown with sp.solve; regime from the boiling-curve limits
  condensation     vertical plate: Nusselt's film analysis (velocity profile -> Γ(δ) -> δ(x) from the
                   energy balance -> integrate k/δ); the printed 0.943 is checked against it, then used
  radiation        Wien constant from maximising Planck's law; σ from integrating it; band fractions
                   and band-averaged ε/α by numerical quadrature of Planck; balances via sp.solve/nsolve
  diffusion        Fick + species conservation as ODEs (dsolve), including Stefan flow with bulk motion
                   and first-order reaction
  mass convection  Sh/Sc^n = Nu/Pr^n with a symbolic length; plate Sh by integrating local Sh_x

Textbook constants that are rounded (2898, 5.67e-8, 0.943, 0.332) are checked against first principles
at their printed precision and then used as printed, so the comparison stays at 1e-6.
"""
import math
from functools import lru_cache

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
SKILLS = {"ht.boundary-layers", "ht.tube-banks", "ht.boiling", "ht.condensation",
          "ht.radiation-properties", "ht.mass-diffusion", "ht.mass-convection"}
RU = 8.314
C1 = mp.mpf("3.742e8")  # W·µm⁴/m²
C2 = mp.mpf(14388)       # µm·K
SIGMA = 5.67e-8
REGIMES = ["Free convection boiling", "Nucleate boiling", "Transition boiling", "Film boiling"]


def F(v):
    return sp.Float(v, 30)


def close(a, b, tol=1e-6):
    a, b = float(a), float(b)
    return abs(a - b) <= tol * max(abs(b), 1e-300)


# ── first-principles constants ───────────────────────────────────────────────
@lru_cache(None)
def blasius_fpp0():
    """f''' + f f''/2 = 0, f(0) = f'(0) = 0, f'(∞) = 1: shoot on f''(0) with RK4."""
    def fp_inf(s):
        y = [0.0, 0.0, s]
        h = 0.01
        for _ in range(1200):
            def d(v):
                return [v[1], v[2], -0.5 * v[0] * v[2]]
            k1 = d(y)
            k2 = d([y[i] + h / 2 * k1[i] for i in range(3)])
            k3 = d([y[i] + h / 2 * k2[i] for i in range(3)])
            k4 = d([y[i] + h * k3[i] for i in range(3)])
            y = [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)]
        return y[1] - 1
    lo, hi = 0.2, 0.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if fp_inf(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


@lru_cache(None)
def constants_ok():
    # Blasius: Nu_x = f''(0) Re^1/2 Pr^1/3 (Pohlhausen) -> printed 0.332
    ok = abs(blasius_fpp0() - 0.332) < 5e-4
    # Wien: d/dλ [λ^-5 / (exp(C2/λT) - 1)] = 0  <=>  x = 5(1 - e^-x), λT = C2/x  (printed 2898)
    lam = sp.Symbol("lam", positive=True)
    Eb = lam ** -5 / (sp.exp(F(1.439e4) / (lam * 1000)) - 1)
    lmax = sp.nsolve(sp.diff(Eb, lam), lam, 2.9)
    ok &= abs(float(lmax) * 1000 - 2898) < 1
    # Stefan–Boltzmann: ∫ Planck dλ / T^4 (printed 5.67e-8)
    T = 1000
    tot = mp.quad(lambda l: mp.mpf("3.742e8") / (l ** 5 * (mp.exp(mp.mpf("1.439e4") / (l * T)) - 1)), [0, 2, 5, 20, mp.inf])
    ok &= abs(float(tot) / T ** 4 / SIGMA - 1) < 1e-3
    # Nusselt film on a vertical plate -> printed 0.943
    ok &= abs(nusselt_coefficient() - 0.943) < 5e-4
    return bool(ok)


@lru_cache(None)
def nusselt_coefficient():
    """h̄_L / [g ρl(ρl-ρv) k³ h' / (μ ΔT L)]^(1/4) from Nusselt's analysis with unit properties."""
    y, d, s, x, L = sp.symbols("y delta s x L", positive=True)
    g = rl = rv_ = k = mu = hp = dT = 1
    rv_ = 0
    u = g * (rl - rv_) / mu * (d * y - y ** 2 / 2)          # film velocity profile
    Gam = rl * sp.integrate(u, (y, 0, d))                     # mass flow per unit width
    # energy: h' dΓ = (k ΔT / δ) dx  ->  ∫0^δ h' Γ'(s) s ds / k ΔT = x
    lhs = sp.integrate(hp * sp.diff(Gam, d).subs(d, s) * s, (s, 0, d)) / (k * dT)
    dx = sp.solve(sp.Eq(lhs, x), d)[0]
    hbar = sp.integrate(k / dx, (x, 0, L)) / L
    return float(sp.N((hbar * L ** sp.Rational(1, 4)), 20))


def planck(T):
    return lambda l: 1 / (l ** 5 * (mp.exp(C2 / (l * T)) - 1)) if l > 0 else mp.mpf(0)


def band(T, l1, l2):
    """∫_{l1}^{l2} E_bλ dλ / ∫_0^∞ E_bλ dλ (l2 < 0 means ∞)."""
    f = planck(T)
    peak = 2898.0 / T
    pts = [mp.mpf(0), peak / 4, peak, 4 * peak, 40 * peak, mp.inf]
    total = mp.quad(f, pts)
    hi = mp.inf if l2 < 0 else mp.mpf(l2)
    lo = mp.mpf(l1)
    seg = [lo] + [p for p in pts if lo < p < hi] + [hi]
    return mp.quad(f, seg) / total


# ── per case ────────────────────────────────────────────────────────────────
def vmax(meta):
    D, ST, SL, V = (F(meta[k]) for k in ("D", "ST", "SL", "V"))
    A_T = ST - D
    if meta["aligned"]:
        Amin = A_T
    else:
        SD = sp.sqrt(SL ** 2 + (ST / 2) ** 2)
        Amin = sp.Min(A_T, 2 * (SD - D))  # the flow splits into two diagonal gaps
    Vm = sp.Symbol("Vm")
    return sp.solve(sp.Eq(V * ST, Vm * Amin), Vm)[0]  # continuity per transverse pitch


def expected(p):
    mt = p["meta"]
    c = mt["ht3"]
    X = sp.Symbol("X", positive=True)
    tg = mt.get("target")
    if c == "bl-transition":
        nu, V = F(mt["nu"]), F(mt["V"])
        if tg == "xc":
            return sp.solve(sp.Eq(V * X / nu, F(mt["Rec"])), X)[0]
        return V * F(mt["L"]) / nu
    if c == "bl-average":
        L = F(mt["L"])
        k_ = mt["kind"]
        if k_ in ("laminar", "turbulent"):
            hx = F(mt["C"]) * X ** (-sp.Rational(1, 2) if k_ == "laminar" else -sp.Rational(1, 5))
        elif k_ == "trailing":
            Cc = sp.Symbol("Cc")
            Cv = sp.solve(sp.Eq(Cc * L ** sp.Rational(-1, 2), F(mt["hL"])), Cc)[0]
            hx = Cv * X ** sp.Rational(-1, 2)
        else:
            assert constants_ok()
            nu, k, Pr, V = (F(mt[q]) for q in ("nu", "k", "Pr", "V"))
            hx = k / X * F(0.332) * sp.sqrt(V * X / nu) * Pr ** sp.Rational(1, 3)
        return sp.integrate(hx, (X, 0, L)) / L
    if c == "bl-thickness":
        nu, Pr, V, x = (F(mt[q]) for q in ("nu", "Pr", "V", "x"))
        delta = 5 * x / sp.sqrt(V * x / nu)  # Blasius, δ at u/u∞ = 0.99 (Eq 7.19)
        assert 4.8 < blasius_eta99() < 5.0
        return 1000 * (delta if tg == "delta" else delta / Pr ** sp.Rational(1, 3))
    if c == "bl-colburn":
        Fd, L, W, V, rho, cp, Pr = (F(mt[q]) for q in ("F", "L", "W", "V", "rho", "cp", "Pr"))
        Cf = (Fd / (L * W)) / (rho * V ** 2 / 2)
        h = sp.Symbol("h")
        return sp.solve(sp.Eq(Cf / 2, h / (rho * cp * V) * Pr ** sp.Rational(2, 3)), h)[0]
    if c == "bl-groups":
        v = mt["v"]
        if v == "Nu":
            return F(mt["h"]) * F(mt["L"]) / F(mt["k"])
        if v == "h":
            h = sp.Symbol("h")
            return sp.solve(sp.Eq(h * F(mt["D"]) / F(mt["k"]), F(mt["Nu"])), h)[0]
        return F(mt["mu"]) * F(mt["cp"]) / F(mt["k"])
    if c == "tb-vmax":
        Vm = vmax(mt)
        return Vm if tg == "Vmax" else Vm * F(mt["D"]) / F(mt["nu"])
    if c == "tb-zukauskas":
        Vm = vmax(mt)
        Re = Vm * F(mt["D"]) / F(mt["nu"])
        assert 1e3 < Re < 2e5
        # Table 7.5 constants stated in the prompt must be the right ones for this bank and Re
        ST, SL = mt["ST"], mt["SL"]
        if mt["aligned"]:
            assert (mt["C"], mt["m"]) == (0.27, 0.63)
        elif ST / SL < 2:
            assert abs(mt["C"] - 0.35 * (ST / SL) ** 0.2) < 6e-4 and mt["m"] == 0.6
        else:
            assert (mt["C"], mt["m"]) == (0.40, 0.6)
        Pr, Prs = F(mt["Pr"]), F(mt["Prs"])
        Nu = F(mt["C2"]) * F(mt["C"]) * Re ** F(mt["m"]) * Pr ** F(0.36) * (Pr / Prs) ** sp.Rational(1, 4)
        return Nu * F(mt["k"]) / F(mt["D"])
    if c == "tb-outlet":
        D, ST, V, h, rho, cp, Ti, Ts = (F(mt[q]) for q in ("D", "ST", "V", "h", "rho", "cp", "Ti", "Ts"))
        NT, NL = mt["NT"], mt["NL"]
        mdot = rho * V * NT * ST                # per unit tube length, through the inlet face
        Tf = sp.Function("T")
        A, a_, b_, c_, d_ = sp.symbols("A a_ b_ c_ d_")
        sol = sp.dsolve(sp.Eq(a_ * Tf(A).diff(A), b_ * (c_ - Tf(A))), Tf(A), ics={Tf(0): d_}).rhs
        To = sol.subs({A: NT * NL * sp.pi * D, a_: mdot * cp, b_: h, c_: Ts, d_: Ti})
        return To if tg == "To" else mdot * cp * (To - Ti)
    if c == "rohsenow":
        mul, hfg, rl, rv, sig, cpl, Prl, Csf = (F(mt[q]) for q in ("mul", "hfg", "rl", "rv", "sig", "cpl", "Prl", "Csf"))
        g = F(9.8)
        dT, q = sp.symbols("dT q", positive=True)
        roh = sp.Eq(q, mul * hfg * sp.sqrt(g * (rl - rv) / sig) * (cpl * dT / (Csf * hfg * Prl ** mt["n"])) ** 3)
        qmax = F(0.149) * hfg * rv * (sig * g * (rl - rv) / rv ** 2) ** sp.Rational(1, 4)
        if tg == "Ts":
            d = sp.solve(roh.subs(q, F(mt["qs"])), dT)[0]
            assert 5 < d < 30 and mt["qs"] < qmax
            return 100 + d
        qs = sp.solve(roh.subs(dT, F(mt["dT"])), q)[0]
        assert 5 <= mt["dT"] <= 30 and qs < qmax
        return qs if tg == "flux" else qs * F(mt["A"])
    if c == "chf":
        hfg, rl, rv, sig, g = (F(mt[q]) for q in ("hfg", "rl", "rv", "sig", "g"))
        qm = F(0.149) * hfg * rv * (sig * g * (rl - rv) / rv ** 2) ** sp.Rational(1, 4)
        return qm if tg == "flux" else qm * F(mt["A"])
    if c in ("cond-plate", "cond-tube"):
        rl, rv, cpl, mul, kl, hfg, g, Ts = (F(mt[q]) for q in ("rl", "rv", "cpl", "mul", "kl", "hfg", "g", "Ts"))
        dT = F(mt["Tsat"]) - Ts
        hp = hfg + F(0.68) * cpl * dT          # Rohsenow's subcooling correction (Eq 10.26)
        if c == "cond-plate":
            assert constants_ok()
            L, b = F(mt["L"]), F(mt["b"])
            h = F(0.943) * (g * rl * (rl - rv) * kl ** 3 * hp / (mul * dT * L)) ** sp.Rational(1, 4)
            q = h * L * b * dT
            md = sp.Symbol("md")
            mdot = sp.solve(sp.Eq(md * hp, q), md)[0]   # latent heat released = heat to the wall
            Re = 4 * mdot / (mul * b)
            assert Re <= 30
            return {"h": h, "q": q, "mdot": mdot, "Re": Re}[tg]
        D = F(mt["D"])
        h = F(0.729) * (g * rl * (rl - rv) * kl ** 3 * hp / (mul * dT * D)) ** sp.Rational(1, 4)
        md = sp.Symbol("md")
        mp_ = sp.solve(sp.Eq(md * hp, h * sp.pi * D * dT), md)[0]
        return {"h": h, "mdot": mp_, "mdotL": mp_ * F(mt["Lt"]) * 3600}[tg]
    if c == "wien":
        assert constants_ok()
        return 2898 / F(mt["T"]) if tg == "lam" else 2898 / F(mt["lam"])
    if c == "stefan":
        assert constants_ok()
        eps = F(mt["eps"])
        if tg == "T":
            T = sp.Symbol("T", positive=True)
            return sp.solve(sp.Eq(eps * F(SIGMA) * T ** 4, F(mt["E"])), T)[0]
        Eb = F(SIGMA) * F(mt["T"]) ** 4
        return Eb if tg == "Eb" else eps * Eb * F(mt["A"])
    if c == "band":
        T = mt["T"]
        fr = band(T, mt["l1"], mt["l2"])
        return fr * SIGMA * T ** 4 if tg == "power" else fr
    if c == "spectral":
        T, lc, a1, a2 = mt["T"], mt["lc"], mt["a1"], mt["a2"]
        f = planck(T)
        peak = 2898.0 / T
        pts = sorted({0, peak / 4, peak, 4 * peak, 40 * peak})
        lo = [mp.mpf(p) for p in pts if p < lc] + [mp.mpf(lc)]
        hi = [mp.mpf(lc)] + [mp.mpf(p) for p in pts if p > lc] + [mp.inf]
        num = a1 * mp.quad(f, lo) + a2 * mp.quad(f, hi)
        avg = num / mp.quad(f, [mp.mpf(p) for p in pts] + [mp.inf])
        return avg * SIGMA * T ** 4 if tg == "E" else avg
    if c == "rad-balance":
        T = sp.Symbol("T", positive=True)
        sg = F(SIGMA)
        if tg == "solar":
            aS, eps, GS, h, Ti, Tsky = (F(mt[q]) for q in ("aS", "eps", "GS", "h", "Tinf", "Tsky"))
            bal = aS * GS + eps * sg * Tsky ** 4 - eps * sg * T ** 4 - h * (T - Ti)
            return sp.nsolve(bal, T, 300, prec=30)
        eps, G = F(mt["eps"]), F(mt["G"])
        alpha = eps                                   # Kirchhoff, gray diffuse
        if tg == "Teq":
            return sp.solve(sp.Eq(alpha * G, eps * sg * T ** 4), T)[0]
        Ts = F(mt["T"])
        J = eps * sg * Ts ** 4 + (1 - alpha) * G      # emitted + reflected
        return J if tg == "J" else J - G
    if c == "fick":
        x = sp.Symbol("x")
        Cf = sp.Function("C")
        if mt["kind"] == "solid":
            D, L = F(mt["D"]), F(mt["L"])
            Cx = sp.dsolve(Cf(x).diff(x, 2), Cf(x), ics={Cf(0): F(mt["C1"]), Cf(L): F(mt["C2"])}).rhs
            N = -D * sp.diff(Cx, x)
            return N * F(mt["M"]) if mt["mass"] else N
        D, L = F(mt["D"]), F(mt["L"])
        C = F(mt["p"]) / (RU * F(mt["T"]))
        NA = sp.Symbol("NA")
        xf = sp.Function("xa")
        # N_A = x_A (N_A + N_B) - C D dx_A/dz with N_B = -N_A
        sol = sp.dsolve(sp.Eq(NA, xf(x) * (NA - NA) - C * D * xf(x).diff(x)), xf(x), ics={xf(0): F(mt["x1"])}).rhs
        Nv = sp.solve(sp.Eq(sol.subs(x, L), F(mt["x2"])), NA)[0]
        rate = Nv * F(mt["A"])
        return rate if mt["kind"] == "gas" else rate * F(mt["M"])
    if c == "stefan-flow":
        D, L = F(mt["D"]), F(mt["L"])
        C = F(mt["p"]) / (RU * F(mt["T"]))
        NA, Cs, Ds, x0, z = sp.symbols("NA Cs Ds x0 z")
        xf = sp.Function("xa")
        # stagnant B: N_A = x_A N_A - C D dx_A/dz  (solved symbolically, numbers substituted after)
        sol = sp.dsolve(sp.Eq(NA, xf(z) * NA - Cs * Ds * xf(z).diff(z)), xf(z), ics={xf(0): x0}).rhs
        num = {Cs: C, Ds: D, x0: F(mt["xA0"])}
        roots = sp.solve(sp.Eq(sol.subs(z, L), F(mt["xAL"])), NA)
        Nv = [rt for rt in (sp.N(rt.subs(num), 30) for rt in roots) if rt.is_real][0]
        return Nv if tg == "N" else Nv * F(mt["A"]) * F(mt["M"]) * 3600
    if c == "membrane":
        S, D, L = F(mt["S"]), F(mt["D"]), F(mt["L"])
        x = sp.Symbol("x")
        Cf = sp.Function("C")
        Cx = sp.dsolve(Cf(x).diff(x, 2), Cf(x), ics={Cf(0): S * F(mt["p1"]), Cf(L): S * F(mt["p2"])}).rhs
        if tg == "Cs":
            return Cx.subs(x, 0)
        N = -D * sp.diff(Cx, x)
        return N if tg == "N" else N * F(mt["A"]) * F(mt["M"])
    if c == "reaction":
        D, k1, L, C0, x = sp.symbols("D k1 L C0 x", positive=True)
        Cf = sp.Function("C")
        Cx = sp.dsolve(D * Cf(x).diff(x, 2) - k1 * Cf(x), Cf(x),
                       ics={Cf(0): C0, Cf(x).diff(x).subs(x, L): 0}).rhs
        num = {D: F(mt["D"]), k1: F(mt["k1"]), L: F(mt["L"]), C0: F(mt["C0"])}
        out = Cx.subs(x, L) if tg == "CL" else (-D * sp.diff(Cx, x)).subs(x, 0)
        return out.subs(num)
    if c in ("analogy", "evap-cool"):
        Lc, nu, h, hm = sp.symbols("Lc nu h hm", positive=True)
        k, alpha, D = F(mt["k"]), F(mt["alpha"]), F(mt["D"])
        Pr, Sc = nu / alpha, nu / D
        third = sp.Rational(1, 3)
        # same geometry & flow: Sh / Sc^n = Nu / Pr^n
        rel = sp.Eq((hm * Lc / D) / Sc ** third, (h * Lc / k) / Pr ** third)
        if c == "analogy":
            if mt["reverse"]:
                return sp.solve(rel.subs(hm, F(mt["hm"])), h)[0]
            return sp.solve(rel.subs(h, F(mt["h"])), hm)[0]
        hm_of_h = sp.solve(rel, hm)[0]
        Tinf = sp.Symbol("Tinf")
        bal = sp.Eq(h * (Tinf - F(mt["Ts"])), hm_of_h * F(mt["hfg"]) * (F(mt["rhoAs"]) - 0))
        return sp.simplify(sp.solve(bal, Tinf)[0])
    if c == "evap":
        nA = F(mt["hm"]) * F(mt["A"]) * (F(mt["rhoAs"]) - F(mt["phi"]) * F(mt["rhoAinf"]))
        return nA * 3600 if tg == "rate" else nA * F(mt["hfg"])
    if c == "sherwood":
        nu, DAB, V = F(mt["nu"]), F(mt["DAB"]), F(mt["V"])
        Sc = nu / DAB
        if mt["geo"] == "sphere":
            D = F(mt["D"])
            Sh = 2 + F(0.6) * sp.sqrt(V * D / nu) * Sc ** sp.Rational(1, 3)
            return Sh * DAB / D
        assert constants_ok()
        L = F(mt["L"])
        hmx = DAB / X * F(0.332) * sp.sqrt(V * X / nu) * Sc ** sp.Rational(1, 3)
        hm = sp.integrate(hmx, (X, 0, L)) / L
        return hm if mt["geo"] == "plate" else hm * L * F(mt["W"]) * F(mt["rhoAs"])
    raise KeyError(c)


@lru_cache(None)
def blasius_eta99():
    """η where f' = 0.99 on the Blasius solution (Incropera rounds it to 5.0)."""
    s = blasius_fpp0()
    y = [0.0, 0.0, s]
    h = 0.001
    eta = 0.0
    while y[1] < 0.99:
        def d(v):
            return [v[1], v[2], -0.5 * v[0] * v[2]]
        k1 = d(y)
        k2 = d([y[i] + h / 2 * k1[i] for i in range(3)])
        k3 = d([y[i] + h / 2 * k2[i] for i in range(3)])
        k4 = d([y[i] + h * k3[i] for i in range(3)])
        y = [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(3)]
        eta += h
    return eta


def check(p, H):
    if p["skill"] not in SKILLS or "ht3" not in p.get("meta", {}):
        return None
    a = p["answer"]
    mt = p["meta"]
    if mt["ht3"] == "regime":
        dT = mt["dT"]
        k = 0 if dT < 5 else 1 if dT <= 30 else 2 if dT <= 120 else 3
        # keep clear of the fuzzy boundaries of the boiling curve
        if any(abs(dT - b) < mg for b, mg in ((5, 1), (30, 5), (120, 20))):
            return False
        return a["kind"] == "choice" and a["correct"] == REGIMES[k] and set(a["options"]) == set(REGIMES)
    exp_ = expected(p)
    return close(float(H.P(a["ref"])), float(sp.N(exp_, 30)))
