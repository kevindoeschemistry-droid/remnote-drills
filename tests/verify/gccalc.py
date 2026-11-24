"""Independent checks for drills/problems/gc-core.yaml (framework graduate-chemical-engineering, GC).

The cards use the textbook closed forms; these functions go back to the governing equation instead:
velocity profiles from the Navier-Stokes or lubrication ODE and then integrated, complex potentials,
equations of state solved numerically, sphere and film diffusion-reaction ODEs with their boundary
conditions, step responses from the ODE, and characteristic equations evaluated on the imaginary axis.
"""
import mpmath as mp
import sympy as sp

N_ = sp.nsimplify
r_, s_, t_, w_ = sp.symbols("r_ s_ t_ w_", positive=True)


def check(p, H):
    return None


def gc_annulus_Q(G, mu, R, kap):
    """pressure-driven flow in an annulus kap*R < r < R: solve (1/r)(r v')' = -G/mu, integrate"""
    G, mu, R, kap = N_(G), N_(mu), N_(R), N_(kap)
    c1, c2 = sp.symbols("c1 c2")
    v = -G * r_**2 / (4 * mu) + c1 * sp.log(r_) + c2
    sol = sp.solve([v.subs(r_, kap * R), v.subs(r_, R)], [c1, c2], dict=True)[0]
    return sp.N(sp.integrate(2 * sp.pi * r_ * v.subs(sol), (r_, kap * R, R)), 30)


def gc_couette_torque(mu, Om, R, kap):
    """inner cylinder (radius kap*R) turning at Om, outer fixed: v = A r + B/r, torque per length on the inner"""
    mu, Om, R, kap = N_(mu), N_(Om), N_(R), N_(kap)
    A, B = sp.symbols("A B")
    v = A * r_ + B / r_
    sol = sp.solve([v.subs(r_, kap * R) - Om * kap * R, v.subs(r_, R)], [A, B], dict=True)[0]
    tau = -mu * r_ * sp.diff(v.subs(sol) / r_, r_)
    return sp.N(sp.Abs(tau.subs(r_, kap * R)) * 2 * sp.pi * (kap * R) ** 2, 30)


def gc_squeeze(mu, V, R, h):
    """disks approaching at V: Reynolds equation d/dr(r h^3/(12 mu) dp/dr) = V r, p(R) = 0, force = integral of p"""
    mu, V, R, h = N_(mu), N_(V), N_(R), N_(h)
    dpdr = -6 * mu * V * r_ / h**3          # from integrating once with a regular centre
    p = sp.integrate(dpdr, (r_, R, r_))      # p(R) = 0
    assert sp.simplify(sp.diff(r_ * h**3 / (12 * mu) * sp.diff(p, r_), r_) + V * r_) == 0
    return sp.N(sp.integrate(2 * sp.pi * r_ * p, (r_, 0, R)), 30)


def gc_blasius_drag(rho, U, L, nu):
    """one side of a plate: integrate the local Blasius wall stress 0.332 rho U^2 / sqrt(Re_x)"""
    rho, U, L, nu = N_(rho), N_(U), N_(L), N_(nu)
    x = sp.Symbol("xx", positive=True)
    tau = sp.Rational(332, 1000) * rho * U**2 / sp.sqrt(U * x / nu)
    return sp.N(sp.integrate(tau, (x, 0, L)), 30)


def gc_cylinder_cp(theta_deg):
    """potential flow past a cylinder: w = U(z + a^2/z); Cp = 1 - |dw/dz|^2/U^2 on the surface"""
    th = sp.pi * N_(theta_deg) / 180
    z = sp.exp(sp.I * th)
    dw = 1 - 1 / z**2
    return sp.N(1 - sp.Abs(sp.expand_complex(dw)) ** 2, 30)


def gc_power_law_Q(dP, L, m, n, R):
    """power-law fluid in a tube: tau = dP r/(2L) = m(-dv/dr)^n, integrate dv/dr from the wall, then the flow"""
    dP, L, m, n, R = N_(dP), N_(L), N_(m), N_(n), N_(R)
    dvdr = -(dP * r_ / (2 * m * L)) ** (1 / n)
    v = sp.integrate(dvdr, (r_, R, r_))
    return sp.N(sp.integrate(2 * sp.pi * r_ * v, (r_, 0, R)), 30)


def gc_brinkman(mu, V, h, k):
    """Couette flow with both walls at T0: k T'' = -mu (V/h)^2; maximum rise"""
    y = sp.Symbol("y")
    T = sp.Function("T")
    sol = sp.dsolve(sp.Eq(N_(k) * T(y).diff(y, 2), -N_(mu) * (N_(V) / N_(h)) ** 2), T(y), ics={T(0): 0, T(N_(h)): 0}).rhs
    return sp.N(sol.subs(y, N_(h) / 2), 30)


def gc_vdw_tc(a, b, R):
    """critical temperature of a van der Waals fluid from dP/dV = d2P/dV2 = 0"""
    a, b, R = N_(a), N_(b), N_(R)
    T, V = sp.symbols("T V", positive=True)
    P = R * T / (V - b) - a / V**2
    sol = sp.solve([sp.diff(P, V), sp.diff(P, V, 2)], [T, V], dict=True)
    return sp.N([s[T] for s in sol if s[V] > b][0], 30)


def gc_pr_z(Tc, Pc, w, T, P, vapour):
    """Peng-Robinson compressibility: solve P(V) = P numerically from an ideal-gas (vapour) or b-sized (liquid) start"""
    R = mp.mpf("8.314462618")
    Tc, Pc, w, T, P = (mp.mpf(str(v)) for v in (Tc, Pc, w, T, P))
    kap = mp.mpf("0.37464") + mp.mpf("1.54226") * w - mp.mpf("0.26992") * w**2
    alpha = (1 + kap * (1 - mp.sqrt(T / Tc))) ** 2
    a = mp.mpf("0.45724") * R**2 * Tc**2 / Pc * alpha
    b = mp.mpf("0.07780") * R * Tc / Pc
    Pf = lambda V: R * T / (V - b) - a / (V * (V + b) + b * (V - b))
    with mp.workdps(40):
        if int(vapour):          # walk down from the ideal-gas volume until P(V) exceeds P
            hi = 2 * R * T / P
            lo = R * T / P
            while Pf(lo) < P:
                hi, lo = lo, b + (lo - b) * mp.mpf("0.9")
        else:                    # walk up from just above b until P(V) falls below P
            lo = b * (1 + mp.mpf("1e-6"))
            hi = lo
            while Pf(hi) > P:
                lo, hi = hi, b + (hi - b) * mp.mpf("1.1")
        for _ in range(200):
            m = (lo + hi) / 2
            if Pf(m) > P:
                lo = m
            else:
                hi = m
        V = (lo + hi) / 2
    return sp.Float(str(P * V / (R * T)), 30)


def gc_overall_eff(phi, Bi):
    """first-order reaction in a sphere with an external film: solve De(C'' + 2C'/r) = kC, C'(R) De = kc (Cb - C(R)).
    Lengths scaled by R: phi^2 = k R^2/De, Bi = kc R/De. Returns rate / (k Cb V)."""
    phi, Bi = N_(phi), N_(Bi)
    A = sp.Symbol("A")
    C = A * sp.sinh(phi * r_) / r_
    eq = sp.Eq(sp.diff(C, r_).subs(r_, 1), Bi * (1 - C.subs(r_, 1)))
    Av = sp.solve(eq, A)[0]
    flux = sp.diff(C, r_).subs(r_, 1).subs(A, Av)            # dimensionless dC/dr at the surface
    rate = 4 * sp.pi * flux                                    # De Cb R x (4 pi R^2 flux / R) / ...
    return sp.N(rate / (phi**2 * sp.Rational(4, 3) * sp.pi), 30)


def gc_enhancement(Ha):
    """pseudo-first-order reaction in the liquid film: D c'' = k c, c(0) = 1, c(1) = 0 in film units; E = -c'(0)"""
    Ha = N_(Ha)
    y = sp.Symbol("y")
    c = sp.Function("c")
    sol = sp.dsolve(sp.Eq(c(y).diff(y, 2), Ha**2 * c(y)), c(y), ics={c(0): 1, c(1): 0}).rhs
    return sp.N(-sp.diff(sol, y).subs(y, 0), 30)


def gc_topt(A1, E1, A2, E2, X):
    """reversible exothermic A <-> B: temperature maximising r = k1(1-X) - k2 X at fixed X"""
    R = mp.mpf("8.314")
    A1, E1, A2, E2, X = (mp.mpf(str(v)) for v in (A1, E1, A2, E2, X))
    r = lambda T: A1 * mp.exp(-E1 / (R * T)) * (1 - X) - A2 * mp.exp(-E2 / (R * T)) * X
    with mp.workdps(40):
        dr = lambda T: mp.diff(r, T)
        lo, hi = mp.mpf(200), mp.mpf(2000)
        for _ in range(300):
            mid = (lo + hi) / 2
            if dr(mid) > 0:
                lo = mid
            else:
                hi = mid
    return sp.Float(str((lo + hi) / 2), 30)


def gc_overshoot(zeta):
    """step response of tau^2 y'' + 2 zeta tau y' + y = 1 (tau = 1), peak value minus 1"""
    z = N_(zeta)
    y = sp.Function("y")
    sol = sp.dsolve(sp.Eq(y(t_).diff(t_, 2) + 2 * z * y(t_).diff(t_) + y(t_), 1), y(t_), ics={y(0): 0, y(t_).diff(t_).subs(t_, 0): 0}).rhs
    f = sp.lambdify(t_, sol, "mpmath")
    with mp.workdps(40):
        lo, hi = mp.mpf("0.01"), mp.mpf(50)
        g = lambda t: mp.diff(f, t)
        # first maximum: derivative turns from + to -; scan then bisect
        tt, step = lo, mp.mpf("0.01")
        while g(tt + step) > 0:
            tt += step
        a, b = tt, tt + step
        for _ in range(200):
            m = (a + b) / 2
            if g(m) > 0:
                a = m
            else:
                b = m
        return sp.Float(str(f((a + b) / 2) - 1), 30)


def gc_ultimate(t1, t2, t3):
    """P control of K/((t1 s+1)(t2 s+1)(t3 s+1)): on s = i w the imaginary part vanishes at w_u; returns K Kc_u"""
    t1, t2, t3 = N_(t1), N_(t2), N_(t3)
    ch = sp.expand((t1 * sp.I * w_ + 1) * (t2 * sp.I * w_ + 1) * (t3 * sp.I * w_ + 1))
    wu = [w for w in sp.solve(sp.im(ch), w_) if w.is_positive][0]
    return sp.N(-sp.re(ch).subs(w_, wu), 30)


def gc_ultimate_period(t1, t2, t3):
    t1, t2, t3 = N_(t1), N_(t2), N_(t3)
    ch = sp.expand((t1 * sp.I * w_ + 1) * (t2 * sp.I * w_ + 1) * (t3 * sp.I * w_ + 1))
    wu = [w for w in sp.solve(sp.im(ch), w_) if w.is_positive][0]
    return sp.N(2 * sp.pi / wu, 30)


def gc_fopdt_wu(tau, theta):
    """phase crossover of e^{-theta s}/(tau s + 1): -atan(w tau) - w theta = -pi, by bisection"""
    tau, theta = mp.mpf(str(tau)), mp.mpf(str(theta))
    f = lambda w: mp.atan(w * tau) + w * theta - mp.pi
    with mp.workdps(40):
        lo, hi = mp.mpf("1e-9"), mp.pi / theta
        for _ in range(300):
            m = (lo + hi) / 2
            if f(m) < 0:
                lo = m
            else:
                hi = m
    return sp.Float(str((lo + hi) / 2), 30)


def gc_rayleigh(alpha, x0, x1):
    """batch distillation: ln(W0/W) = integral from x1 to x0 of dx/(y - x); returns W/W0 by quadrature"""
    a = mp.mpf(str(alpha))
    y = lambda x: a * x / (1 + (a - 1) * x)
    with mp.workdps(30):
        I = mp.quad(lambda x: 1 / (y(x) - x), [mp.mpf(str(x1)), mp.mpf(str(x0))])
    return sp.Float(str(mp.exp(-I)), 30)


FUNCS = {f.__name__: f for f in [gc_annulus_Q, gc_couette_torque, gc_squeeze, gc_blasius_drag, gc_cylinder_cp, gc_power_law_Q,
                                 gc_brinkman, gc_vdw_tc, gc_pr_z, gc_overall_eff, gc_enhancement, gc_topt, gc_overshoot,
                                 gc_ultimate, gc_ultimate_period, gc_fopdt_wu, gc_rayleigh]}
