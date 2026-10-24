"""
Independent check of the Incropera Ch 5, 7-9, 11, 13 drills (src/drills/gen-heat2.ts).
No code is shared with the generator; each answer is recomputed from its governing
equation where one exists:

  lumped        dsolve  dT/dt = -hA(T - T_inf)/(rho V c), V and A_s from the geometry
  one-term      eigenvalue by nsolve on the transcendental equation; C1 from the
                orthogonality integrals (not the closed form); Fo > 0.2 enforced
  semi-infinite erf profile checked against the heat equation symbolically; flux by
                differentiating it; depth/time by nsolve; contact T by flux balance
  plate         h-bar = (1/L) * integral of the local h_x (laminar 0.332, turbulent 0.0296),
                and 0.332 itself from the Blasius equation (RK4 shooting, once)
  internal      Re from u_m = mdot/(rho A) (rho cancels); T_m(x) by dsolve of the slice
                balance; Nu = 48/11 from the fully developed energy equation; 3.66 as
                the rounded Graetz eigenvalue (series shooting, once)
  free          beta = -(1/rho) d rho/dT for an ideal gas; correlations as printed
  exchangers    LMTD cases: dsolve d(dT)/dA along the exchanger; eps-NTU cases: the
                two- (or three-, 1-2 shell-and-tube) stream ODE system by matrix
                exponential, with the counterflow / return-pass boundary conditions
  view factors  reciprocity + summation solved as a linear system; coaxial disks by
                quadrature of the view-factor integral
  enclosures    radiosity equations solved with sp.solve
Empirical correlations (Churchill-Bernstein, Whitaker, Dittus-Boelter, Churchill-Chu,
horizontal plates) have no derivation to redo; they are re-typed from the book.
"""
import mpmath as mp
import sympy as sp

MINE = {"ht.lumped", "ht.transient-one-term", "ht.semi-infinite", "ht.external-flow", "ht.internal-flow",
        "ht.free-convection", "ht.heat-exchangers", "ht.view-factors", "ht.enclosures"}
mp.mp.dps = 30
SIG = sp.Rational(567, 10**10)


def R(v):
    return sp.nsimplify(v, rational=True)


def F(x):
    return mp.mpf(str(x)) if not isinstance(x, (sp.Basic,)) else mp.mpf(str(sp.N(x, 40)))


# ── one-time first-principles constants ─────────────────────────────────────
def _blasius_fpp0() -> float:
    """f''' + f f''/2 = 0, f(0)=f'(0)=0, f'(inf)=1: shoot on f''(0) with RK4."""
    def end(s, H=12.0, n=4000):
        h = H / n
        y = [0.0, 0.0, s]
        f = lambda y: [y[1], y[2], -0.5 * y[0] * y[2]]
        for _ in range(n):
            k1 = f(y); k2 = f([a + h / 2 * b for a, b in zip(y, k1)])
            k3 = f([a + h / 2 * b for a, b in zip(y, k2)]); k4 = f([a + h * b for a, b in zip(y, k3)])
            y = [a + h / 6 * (b + 2 * c + 2 * d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
        return y[1] - 1
    a, b = 0.2, 0.5
    for _ in range(60):
        c = (a + b) / 2
        if (end(a) < 0) == (end(c) < 0): a = c
        else: b = c
    return (a + b) / 2


def _nu_flux():
    """Fully developed laminar, uniform q'': (1/r)(rT')' = u(r), u = 2(1 - r^2), r in [0, 1]."""
    r, s = sp.symbols("r s", positive=True)
    u = 2 * (1 - r**2)
    dT = sp.integrate((s * u.subs(r, s)), (s, 0, r)) / r          # r T' = int_0^r s u ds
    T = sp.integrate(dT, (r, 0, r))
    Tm = sp.integrate(u * T * r, (r, 0, 1)) / sp.integrate(u * r, (r, 0, 1))
    return sp.nsimplify(2 * dT.subs(r, 1) / (T.subs(r, 1) - Tm))   # Nu_D = h(2 r_o)/k


def _nu_graetz():
    """phi'' + phi'/r + lam^2 (1 - r^2) phi = 0, phi'(0) = 0, phi(1) = 0; Nu_D = lam^2/2."""
    def phi1(lam):
        c = [mp.mpf(1), mp.mpf(0)]
        for k in range(0, 160, 2):
            prev = c[k - 2] if k >= 2 else 0
            c += [-(lam**2) * (c[k] - prev) / (k + 2) ** 2, mp.mpf(0)]
        return sum(c)
    lam = mp.findroot(phi1, 2.7)
    return lam**2 / 2


FPP0 = _blasius_fpp0()
assert abs(FPP0 - 0.332) < 1e-3, FPP0                       # Eq. 7.23's 0.332
NU_FLUX = _nu_flux()
assert NU_FLUX == sp.Rational(48, 11), NU_FLUX               # Eq. 8.53
NU_TS_EXACT = _nu_graetz()
assert abs(NU_TS_EXACT - mp.mpf("3.66")) < 0.005, NU_TS_EXACT  # Eq. 8.55 (3.657 rounded)
NU_TS = sp.Rational(366, 100)

X, t_, x_ = sp.symbols("X t_ x_", positive=True)
Tf = sp.Function("T")


# ── Ch 5 ────────────────────────────────────────────────────────────────────
def lumped(M):
    D = R(M["D"]); ro = D / 2
    V, A = {"sphere": (sp.Rational(4, 3) * sp.pi * ro**3, 4 * sp.pi * ro**2),
            "cylinder": (sp.pi * ro**2, 2 * sp.pi * ro),         # per unit length
            "plate": (D, 2)}[M["shape"]]                         # per unit face area
    h, k = R(M["h"]), R(M["k"])
    Bi = h * (V / A) / k
    if M["target"] == "Bi":
        return Bi
    if not Bi < sp.Rational(1, 10):
        return None
    rho, c, Ti, Ti_ = R(M["rho"]), R(M["c"]), R(M["Ti"]), R(M["Tinf"])
    T = sp.dsolve(sp.Eq(Tf(t_).diff(t_), -h * A * (Tf(t_) - Ti_) / (rho * V * c)), Tf(t_), ics={Tf(0): Ti}).rhs
    if M["target"] == "T":
        return T.subs(t_, R(M["t"]))
    if M["target"] == "t":
        return sp.nsolve(T - R(M["T"]), t_, (0, 10**7), solver="bisect", prec=30)
    return sp.integrate(h * A * (T - Ti_), (t_, 0, R(M["t"])))  # Q


def one_term(M):
    geo = M["geo"]
    L, k, a, h = (F(M[n]) for n in ("L", "k", "alpha", "h"))
    Bi = h * L / k
    z = sp.Symbol("z")
    b = sp.Float(str(Bi), 30)
    # wall z tan z = Bi; cylinder z J1/J0 = Bi; sphere 1 - z cot z = Bi (each multiplied through)
    eq_, hi = {"wall": (z * sp.sin(z) - b * sp.cos(z), sp.pi / 2),
               "cyl": (z * sp.besselj(1, z) - b * sp.besselj(0, z), sp.Float("2.404825557695772768621631879", 30)),
               "sph": (sp.sin(z) - z * sp.cos(z) - b * sp.sin(z), sp.pi)}[geo]
    z1 = mp.mpf(str(sp.nsolve(eq_, z, (mp.mpf("1e-12"), F(hi) - mp.mpf("1e-25")), solver="bisect", prec=30)))
    Xf, w = {"wall": (lambda s: mp.cos(z1 * s), lambda s: 1),
             "cyl": (lambda s: mp.besselj(0, z1 * s), lambda s: s),
             "sph": (lambda s: mp.sinc(z1 * s), lambda s: s * s)}[geo]
    C1 = mp.quad(lambda s: Xf(s) * w(s), [0, 1]) / mp.quad(lambda s: Xf(s) ** 2 * w(s), [0, 1])
    Ti, Ti_ = F(M["Ti"]), F(M["Tinf"])
    if M["target"] == "t":
        th = (F(M["T0"]) - Ti_) / (Ti - Ti_)
        Fo = mp.findroot(lambda f: C1 * mp.exp(-z1**2 * f) - th, 0.5)
        return None if Fo <= 0.2 else Fo * L**2 / a
    Fo = a * F(M["t"]) / L**2
    if Fo <= 0.2:
        return None
    th = C1 * mp.exp(-z1**2 * Fo) * (Xf(1) if M["target"] == "Ts" else 1)
    return Ti_ + th * (Ti - Ti_)


_a, _k, _Ti, _Ts = sp.symbols("a_ k_ Ti_ Ts_", positive=True)
T_ERF = _Ts + (_Ti - _Ts) * sp.erf(x_ / (2 * sp.sqrt(_a * t_)))
assert sp.simplify(sp.diff(T_ERF, t_) - _a * sp.diff(T_ERF, x_, 2)) == 0          # solves the heat equation
assert sp.limit(T_ERF, x_, 0) == _Ts and sp.limit(T_ERF, t_, 0) == _Ti                # BC and IC
Q_SURF = sp.simplify((-_k * sp.diff(T_ERF, x_)).subs(x_, 0))                          # into the solid


def semi(M):
    k, rho, c = R(M["k"]), R(M["rho"]), R(M["c"])
    sub = {_a: k / (rho * c), _k: k, _Ti: R(M["Ti"]), _Ts: R(M["Ts"])}
    T = T_ERF.subs(sub)
    tg = M["target"]
    if tg == "T":
        return T.subs({x_: R(M["x"]), t_: R(M["t"])})
    if tg == "flux":
        return Q_SURF.subs(sub).subs(t_, R(M["t"]))
    if tg == "x":
        tt = R(M["t"])
        scale = float(sp.sqrt(sub[_a] * tt))
        x = sp.nsolve(T.subs(t_, tt) - R(M["T"]), x_, (1e-14, 12 * scale), solver="bisect", prec=30)
        return x * (1000 if M["unit"] == "mm" else 1)
    lt = sp.Symbol("lt")  # t = 10^lt
    tt = sp.nsolve(T.subs({x_: R(M["x"]), t_: 10**lt}) - R(M["T"]), lt, (-8, 14), solver="bisect", prec=30)
    return 10**tt / (3600 if M["unit"] == "h" else 1)


def contact(M):
    Tsurf = sp.Symbol("Tsurf")
    qa = Q_SURF.subs({_k: R(M["kA"]), _a: R(M["kA"]) / (R(M["rhoA"]) * R(M["cA"])), _Ti: R(M["TA"]), _Ts: Tsurf})
    qb = Q_SURF.subs({_k: R(M["kB"]), _a: R(M["kB"]) / (R(M["rhoB"]) * R(M["cB"])), _Ti: R(M["TB"]), _Ts: Tsurf})
    return sp.solve(sp.Eq(qa + qb, 0), Tsurf)[0]  # no net heat into the interface; t cancels


# ── Ch 7 ────────────────────────────────────────────────────────────────────
def plate(M):
    u, L, nu, k, Pr = (R(M[n]) for n in ("u", "L", "nu", "k", "Pr"))
    xc = 500000 * nu / u
    hl = sp.Rational(332, 1000) * k / X * (u * X / nu) ** sp.Rational(1, 2) * Pr ** sp.Rational(1, 3)
    ht = sp.Rational(296, 10000) * k / X * (u * X / nu) ** sp.Rational(4, 5) * Pr ** sp.Rational(1, 3)  # Eq. 7.36
    if L <= xc:
        hbar = sp.integrate(hl, (X, 0, L)) / L
    else:
        hbar = (sp.integrate(hl, (X, 0, xc)) + sp.integrate(ht, (X, xc, L))) / L
    return hbar if M["target"] == "h" else hbar * L * R(M["W"]) * (R(M["Ts"]) - R(M["Tinf"]))


def cyl_cb(M):
    V, D, nu, k, Pr = (F(M[n]) for n in ("V", "D", "nu", "k", "Pr"))
    Re = V * D / nu
    if Re * Pr <= 0.2: return None
    Nu = mp.mpf("0.3") + mp.mpf("0.62") * mp.sqrt(Re) * mp.cbrt(Pr) / (1 + (mp.mpf("0.4") / Pr) ** (mp.mpf(2) / 3)) ** mp.mpf("0.25") \
        * (1 + (Re / 282000) ** (mp.mpf(5) / 8)) ** (mp.mpf(4) / 5)
    h = Nu * k / D
    return h if M["target"] == "h" else h * mp.pi * D * (F(M["Ts"]) - F(M["Tinf"]))


def sphere_w(M):
    V, D, nu, k, Pr, mu, mus = (F(M[n]) for n in ("V", "D", "nu", "k", "Pr", "mu", "mus"))
    Re = V * D / nu
    if not (3.5 < Re < 7.6e4 and 1 <= mu / mus <= 3.2): return None
    Nu = 2 + (mp.mpf("0.4") * mp.sqrt(Re) + mp.mpf("0.06") * Re ** (mp.mpf(2) / 3)) * Pr ** mp.mpf("0.4") * (mu / mus) ** mp.mpf("0.25")
    h = Nu * k / D
    return h if M["target"] == "h" else h * mp.pi * D**2 * (F(M["Ts"]) - F(M["Tinf"]))


# ── Ch 8 ────────────────────────────────────────────────────────────────────
_rho = sp.Symbol("rho_", positive=True)


def reynolds(mdot, D, mu):
    um = R(mdot) / (_rho * sp.pi * R(D) ** 2 / 4)
    Re = sp.simplify(_rho * um * R(D) / R(mu))
    assert not Re.has(_rho)
    return Re


def int_re(M):
    Re = reynolds(M["mdot"], M["D"], M["mu"])
    if M["target"] == "Re": return Re
    if not Re < 2300: return None
    return sp.Rational(5, 100) * Re * R(M["D"]) * (R(M["Pr"]) if M["target"] == "xfdt" else 1)


def tm_flux(M):
    mdot, D, qs, Tmi, cp = (R(M[n]) for n in ("mdot", "D", "qs", "Tmi", "cp"))
    Tm = sp.dsolve(sp.Eq(Tf(X).diff(X), qs * sp.pi * D / (mdot * cp)), Tf(X), ics={Tf(0): Tmi}).rhs
    if M["target"] == "L":
        return sp.solve(sp.Eq(Tm, R(M["Tmo"])), X)[0]
    Tmo = Tm.subs(X, R(M["L"]))
    return Tmo if M["target"] == "Tmo" else Tmo + qs / R(M["h"])


def tm_ts(M):
    mdot, D, h, Ts, Tmi, cp = (R(M[n]) for n in ("mdot", "D", "h", "Ts", "Tmi", "cp"))
    Tm = sp.dsolve(sp.Eq(Tf(X).diff(X), h * sp.pi * D * (Ts - Tf(X)) / (mdot * cp)), Tf(X), ics={Tf(0): Tmi}).rhs
    if M["target"] == "L":
        return sp.nsolve(Tm - R(M["Tmo"]), X, (0, 10**4), solver="bisect", prec=30)
    L = R(M["L"])
    if M["target"] == "Tmo":
        return Tm.subs(X, L)
    return sp.integrate(h * sp.pi * D * (Ts - Tm), (X, 0, L))  # heat into the water along the tube


def dittus(M):
    Re = reynolds(M["mdot"], M["D"], M["mu"])
    if Re < 10000: return None
    n = sp.Rational(2, 5) if M["heating"] else sp.Rational(3, 10)
    return sp.Rational(23, 1000) * Re ** sp.Rational(4, 5) * R(M["Pr"]) ** n * R(M["k"]) / R(M["D"])


def lam_fd(M):
    if not reynolds(M["mdot"], M["D"], M["mu"]) < 2300: return None
    return (NU_FLUX if M["bc"] == "flux" else NU_TS) * R(M["k"]) / R(M["D"])


# ── Ch 9 ────────────────────────────────────────────────────────────────────
_T, _p, _Rg = sp.symbols("T_ p_ Rg_", positive=True)
_rho_ig = _p / (_Rg * _T)
BETA = sp.simplify(-sp.diff(_rho_ig, _T) / _rho_ig)  # = 1/T


def free(M):
    nu, al, k, Pr, Ts, Ti = (R(M[n]) for n in ("nu", "alpha", "k", "Pr", "Ts", "Tinf"))
    beta = BETA.subs(_T, R(M["Tf"]))
    geo = M["geo"]
    L = R(M["a"]) * R(M["b"]) / (2 * (R(M["a"]) + R(M["b"]))) if geo == "hplate" else R(M["L"])
    Ra = sp.Rational(98, 10) * beta * abs(Ts - Ti) * L**3 / (nu * al)
    if M["target"] == "Ra": return Ra
    ra = float(Ra)
    third = sp.Rational(1, 3)
    if geo == "vplate":
        Nu = (sp.Rational(825, 1000) + sp.Rational(387, 1000) * Ra ** sp.Rational(1, 6) / (1 + (sp.Rational(492, 1000) / Pr) ** sp.Rational(9, 16)) ** sp.Rational(8, 27)) ** 2
        area = L * R(M["W"])
    elif geo == "hcyl":
        if ra > 1e12: return None
        Nu = (sp.Rational(6, 10) + sp.Rational(387, 1000) * Ra ** sp.Rational(1, 6) / (1 + (sp.Rational(559, 1000) / Pr) ** sp.Rational(9, 16)) ** sp.Rational(8, 27)) ** 2
        area = sp.pi * L
    else:
        hot = Ts > Ti
        if M["up"] == hot:  # hot face up / cold face down
            if 1e4 <= ra <= 1e7: Nu = sp.Rational(54, 100) * Ra ** sp.Rational(1, 4)
            elif 1e7 < ra <= 1e11: Nu = sp.Rational(15, 100) * Ra**third
            else: return None
        else:
            if not 1e4 <= ra <= 1e9: return None
            Nu = sp.Rational(52, 100) * Ra ** sp.Rational(1, 5)
        area = R(M["a"]) * R(M["b"])
    h = Nu * k / L
    return h if M["target"] == "h" else h * area * (Ts - Ti)


# ── Ch 11 ───────────────────────────────────────────────────────────────────
def lmtd(M):
    Ch, Cc = R(M["mh"]) * R(M["cph"]), R(M["mc"]) * R(M["cpc"])
    Thi, Tho, Tci, U = R(M["Thi"]), R(M["Tho"]), R(M["Tci"]), R(M["U"])
    Tco = Tci + Ch * (Thi - Tho) / Cc
    a_ = sp.Symbol("a_", positive=True)
    # dTh = -U dT dA / Ch;  dTc = +U dT dA / Cc (parallel) or -U dT dA / Cc (counter, A from hot inlet)
    if M["flow"] == "parallel":
        rate, start, end = 1 / Ch + 1 / Cc, Thi - Tci, Tho - Tco
    else:
        rate, start, end = 1 / Ch - 1 / Cc, Thi - Tco, Tho - Tci
    kap, d0 = sp.symbols("kappa d0", real=True)
    dT = sp.dsolve(sp.Eq(Tf(a_).diff(a_), -kap * Tf(a_)), Tf(a_), ics={Tf(0): d0}).rhs.subs({kap: U * rate, d0: start})
    A = sp.nsolve(dT - end, a_, (0, 10**5), solver="bisect", prec=30)
    return A if M["target"] == "A" else A / (sp.pi * R(M["D"]))


def ntu(M):
    Ch, Cc = F(M["mh"]) * F(M["cph"]), F(M["mc"]) * F(M["cpc"])
    UA = F(M["U"]) * F(M["A"])
    Thi, Tci = F(M["Thi"]), F(M["Tci"])
    flow = M["flow"]
    if flow == "parallel":     # x along both streams, x = 0..1
        E = mp.expm(mp.matrix([[-UA / Ch, UA / Ch], [UA / Cc, -UA / Cc]]))
        Tho = E[0, 0] * Thi + E[0, 1] * Tci
        q = Ch * (Thi - Tho)
    elif flow == "counter":    # cold enters at x = 1; unknown cold outlet z at x = 0
        E = mp.expm(mp.matrix([[-UA / Ch, UA / Ch], [-UA / Cc, UA / Cc]]))
        z = (Tci - E[1, 0] * Thi) / E[1, 1]
        q = Cc * (z - Tci)
    else:                      # 1 shell pass (hot), 2 tube passes (cold): pass 1 along x, pass 2 back
        k = UA / 2
        E = mp.expm(mp.matrix([[-2 * k / Ch, k / Ch, k / Ch], [k / Cc, -k / Cc, 0], [-k / Cc, 0, k / Cc]]))
        # X(1) = E X(0), X(0) = [Thi, Tci, z]; the passes join at x = 1: t2(1) = t1(1)
        c0 = (E[2, 0] - E[1, 0]) * Thi + (E[2, 1] - E[1, 1]) * Tci
        z = -c0 / (E[2, 2] - E[1, 2])
        q = Cc * (z - Tci)
    tg = M["target"]
    if tg == "eps": return q / (min(Ch, Cc) * (Thi - Tci))
    if tg == "q": return q
    if tg == "Tco": return Tci + q / Cc
    return Thi - q / Ch


# ── Ch 13 ───────────────────────────────────────────────────────────────────
def _fd_quad(rho, a, L):
    """element at radius rho -> coaxial disk of radius a at distance L, straight from the definition:
    dF = cos(t1)cos(t2)/(pi S^2) dA2 with cos = L/S; the phi integral done analytically."""
    f = lambda s: 2 * L**2 * (L**2 + rho**2 + s**2) * s / ((L**2 + rho**2 + s**2) ** 2 - 4 * rho**2 * s**2) ** mp.mpf(1.5)
    return mp.quad(f, [0, rho, a] if 0 < rho < a else [0, a])


def _fd(rho, a, L):
    return (1 - (L**2 + rho**2 - a**2) / mp.sqrt((L**2 + rho**2 + a**2) ** 2 - 4 * rho**2 * a**2)) / 2


# the closed form of that integral, checked against the quadrature before it is used
for _r0, _a0, _L0 in [(0, 1, 1), (0.3, 0.25, 0.1), (0.2, 0.5, 0.05), (0.49, 0.5, 0.05), (0.05, 0.1, 0.5)]:
    assert abs(_fd_quad(mp.mpf(_r0), mp.mpf(_a0), mp.mpf(_L0)) - _fd(mp.mpf(_r0), mp.mpf(_a0), mp.mpf(_L0))) < 1e-20


def disk_vf(r1, r2, L):
    """F_12, coaxial parallel disks: area-average of the element view factor over disk 1."""
    r1, r2, L = F(r1), F(r2), F(L)
    return mp.quad(lambda rho: 2 * rho * _fd(rho, r2, L), [0, r2, r1] if r2 < r1 else [0, r1]) / r1**2


def solve_vf(areas, known):
    """all F_ij of an n-surface enclosure from summation + reciprocity + the known ones"""
    n = len(areas)
    Fm = sp.Matrix(n, n, lambda i, j: sp.Symbol(f"F{i}{j}"))
    eqs = [sp.Eq(sum(Fm[i, j] for j in range(n)), 1) for i in range(n)]
    eqs += [sp.Eq(areas[i] * Fm[i, j], areas[j] * Fm[j, i]) for i in range(n) for j in range(i + 1, n)]
    eqs += [sp.Eq(Fm[i, j], v) for (i, j), v in known.items()]
    sol = sp.solve(eqs, list(Fm), dict=True)
    assert len(sol) == 1
    return Fm.subs(sol[0])


def vf(M):
    c = M["case"]
    if c == "recip":
        Fm = solve_vf([R(M["A1"]), R(M["A2"])], {(0, 1): R(M["F12"]), (0, 0): 1 - R(M["F12"])})
        return Fm[1, 0]
    if c == "sum-recip":   # surfaces 1, 2, 3; only F_11 = 0 and F_12 known — F_31 is fixed by row 1 + reciprocity
        F13 = 1 - 0 - R(M["F12"])
        F31 = sp.Symbol("F31")
        return sp.solve(sp.Eq(R(M["A1"]) * F13, R(M["A3"]) * F31), F31)[0]
    if c == "concentric":
        D1, D2 = R(M["D1"]), R(M["D2"])
        A = [sp.pi * D1**2, sp.pi * D2**2] if M["sphere"] else [sp.pi * D1, sp.pi * D2]
        Fm = solve_vf(A, {(0, 0): 0})
        return Fm[1, 1] if M["target"] == "F22" else Fm[1, 0]
    if c == "duct":
        w = [R(v) for v in M["w"]]
        Fm = solve_vf(w, {(0, 0): 0, (1, 1): 0, (2, 2): 0})
        return Fm[M["i"], M["j"]]
    if c == "cavity":
        r, H = R(M["r"]), R(M["H"])
        F12 = R(sp.Float(str(disk_vf(M["r"], M["r"], M["H"])), 30))
        Fm = solve_vf([sp.pi * r**2, sp.pi * r**2, 2 * sp.pi * r * H], {(0, 0): 0, (1, 1): 0, (0, 1): F12})
        return {"F13": Fm[0, 2], "F31": Fm[2, 0], "F33": Fm[2, 2]}[M["target"]]
    raise KeyError(c)


def radiosity(areas, Fm, eps, Eb, rerad=()):
    """q_i = A_i sum_j F_ij (J_i - J_j); eps_i A_i (Eb_i - J_i) = (1 - eps_i) q_i, or q_i = 0 if reradiating"""
    n = len(areas)
    J = sp.symbols(f"J0:{n}")
    q = sp.symbols(f"q0:{n}")
    eqs = [sp.Eq(q[i], areas[i] * sum(Fm[i, j] * (J[i] - J[j]) for j in range(n))) for i in range(n)]
    for i in range(n):
        eqs.append(sp.Eq(q[i], 0) if i in rerad else sp.Eq(eps[i] * areas[i] * (Eb[i] - J[i]), (1 - eps[i]) * q[i]))
    sol = sp.solve(eqs, [*J, *q], dict=True)[0]
    return sol, J, q


def encl(M):
    c = M["case"]
    if c == "two":
        D1, D2 = R(M["D1"]), R(M["D2"])
        A = {"plates": [1, 1], "cyl": [sp.pi * D1, sp.pi * D2], "sph": [sp.pi * D1**2, sp.pi * D2**2]}[M["geo"]]
        known = {(0, 0): 0} if M["geo"] != "plates" else {(0, 0): 0, (1, 1): 0}
        Fm = solve_vf(A, known)
        sol, J, q = radiosity(A, Fm, [R(M["e1"]), R(M["e2"])], [SIG * R(M["T1"]) ** 4, SIG * R(M["T2"]) ** 4])
        return sol[q[0]]
    if c == "shield":
        e1, e2, ea, eb = (R(M[n]) for n in ("e1", "e2", "ea", "eb"))
        Eb3 = sp.Symbol("Eb3")
        J1, Ja, Jb, J2, q1, qa, qb, q2 = sp.symbols("J1 Ja Jb J2 q1 qa qb q2")
        Eb1, Eb2 = SIG * R(M["T1"]) ** 4, SIG * R(M["T2"]) ** 4
        eqs = [sp.Eq(q1, J1 - Ja), sp.Eq(qa, Ja - J1), sp.Eq(qb, Jb - J2), sp.Eq(q2, J2 - Jb),  # per area, F = 1
               sp.Eq(e1 * (Eb1 - J1), (1 - e1) * q1), sp.Eq(ea * (Eb3 - Ja), (1 - ea) * qa),
               sp.Eq(eb * (Eb3 - Jb), (1 - eb) * qb), sp.Eq(e2 * (Eb2 - J2), (1 - e2) * q2),
               sp.Eq(qa + qb, 0)]  # the shield has no other heat input
        sol = sp.solve(eqs, [J1, Ja, Jb, J2, q1, qa, qb, q2, Eb3], dict=True)[0]
        return sol[q1] if M["target"] == "q" else (sol[Eb3] / SIG) ** sp.Rational(1, 4)
    if c == "black-disks":
        r1, r2 = R(M["r1"]), R(M["r2"])
        F12 = R(sp.Float(str(disk_vf(M["r1"], M["r2"], M["L"])), 30))
        A1, A2 = sp.pi * r1**2, sp.pi * r2**2
        F21 = sp.solve(sp.Eq(A1 * F12, A2 * sp.Symbol("F21")), sp.Symbol("F21"))[0]
        return A1 * F12 * SIG * R(M["T1"]) ** 4 - A2 * F21 * SIG * R(M["T2"]) ** 4
    if c == "rerad":
        w = [R(v) for v in M["w"]]
        Fm = solve_vf(w, {(0, 0): 0, (1, 1): 0, (2, 2): 0})
        sol, J, q = radiosity(w, Fm, [R(M["e1"]), R(M["e2"]), 1], [SIG * R(M["T1"]) ** 4, SIG * R(M["T2"]) ** 4, 0], rerad=(2,))
        return sol[q[0]] if M["target"] == "q" else (sol[J[2]] / SIG) ** sp.Rational(1, 4)
    raise KeyError(c)


CASES = {"lumped": lumped, "one-term": one_term, "semi": semi, "contact-T": contact, "plate": plate, "cyl-cb": cyl_cb,
         "sphere-w": sphere_w, "int-re": int_re, "tm-flux": tm_flux, "tm-ts": tm_ts, "dittus": dittus, "lam-fd": lam_fd,
         "free": free, "lmtd": lmtd, "ntu": ntu, "vf": vf, "encl": encl}


def check(p, H):
    if p["skill"] not in MINE:
        return None
    M = p.get("meta") or {}
    fn = CASES.get(M.get("ht"))
    if fn is None or p["answer"]["kind"] != "expression":
        return False
    exp_ = fn(M)
    if exp_ is None:  # outside the method's validity range
        return False
    exp_ = float(sp.N(exp_, 30)) if isinstance(exp_, sp.Basic) else float(exp_)
    mine = float(p["answer"]["ref"])
    return abs(mine - exp_) <= 1e-6 * abs(exp_) + 1e-12
