"""Independent checks for drills/problems/co-olympiad.yaml (framework chemistry-olympiad, CO).

The generator solves each equilibrium by bisection on its own charge or mass balance and uses the
textbook closed forms elsewhere; these functions solve with sympy (nsolve on the balances), add Gibbs
energies, close Hess cycles as equations, enumerate isotopes and spin states, and dsolve rate laws.
"""
import itertools

import sympy as sp

N_ = sp.nsimplify
KW = sp.Rational(1, 10**14)


def check(p, H):
    return None


def _bisect_log(f, lo=-1.0, hi=15.0):
    """f(pH) decreasing; return pH root by bisection then polish with nsolve"""
    y = sp.Symbol("y")
    for _ in range(200):
        mid = (lo + hi) / 2
        if float(f(mid)) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def polyprotic_ph(C, Na_per, Kas):
    """pH of C M of an acid HₙA with Na_per sodium per formula unit (NaH₂PO₄ → 1); charge balance"""
    Ks = [N_(k) for k in Kas]
    C, Na = N_(C), N_(Na_per) * N_(C)

    def f(ph):
        h = sp.Float(10) ** (-ph)
        terms = [sp.Integer(1)]
        for k in Ks:
            terms.append(terms[-1] * k / h)
        D = sum(terms)
        charge = sum(i * t for i, t in enumerate(terms)) / D * C
        return h + Na - charge - KW / h
    ph = _bisect_log(f)
    y = sp.Symbol("y")
    h = 10 ** (-y)
    terms = [sp.Integer(1)]
    for k in Ks:
        terms.append(terms[-1] * k / h)
    D = sum(terms)
    expr = h + Na - sum(i * t for i, t in enumerate(terms)) / D * C - KW / h
    return sp.nsolve(expr, y, ph, prec=30)


def buffer_after(Ca, Cb, Ka, nH, V):
    """pH of a buffer (Ca weak acid, Cb conjugate base, mol/L in V L) after nH mol strong acid: charge balance"""
    y = sp.Symbol("y")
    V = N_(V)
    cHA, cA, cCl = N_(Ca), N_(Cb), N_(nH) / V
    Ka = N_(Ka)
    tot = cHA + cA
    h = 10 ** (-y)
    expr = h + cA - cCl - tot * Ka / (Ka + h) - KW / h
    ph0 = float(-sp.log(Ka * (cHA + cCl) / (cA - cCl), 10))
    return sp.nsolve(expr, y, ph0, prec=30)


def ksp_acid(Ksp, Ka, pH):
    """CaF₂ at fixed pH: [Ca] = s, total fluoride 2s split between F⁻ and HF"""
    h = 10 ** (-N_(pH))
    frac = N_(Ka) / (N_(Ka) + h)
    g = lambda s: s * (2 * s * frac) ** 2 - N_(Ksp)  # noqa: E731  increasing in s
    lo, hi = sp.Integer(-12), sp.Integer(1)  # bisect on log10 s
    for _ in range(120):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sp.N(g(sp.Integer(10) ** mid), 40) < 0 else (lo, mid)
    return sp.N(sp.Integer(10) ** ((lo + hi) / 2), 25)


def e_from_ksp(E0, Ksp, n=1):
    """AgCl(s) + e⁻ → Ag + Cl⁻ as Ag⁺/Ag plus dissolution: add ΔG = −nFE° and −RT ln Ksp"""
    R, T, F = N_("8.314462618"), N_("298.15"), N_("96485.33212")
    dG = -int(n) * F * N_(E0) - R * T * sp.log(N_(Ksp))
    return -dG / (int(n) * F)


def electrolysis(w, I, t_or_m, M, n):
    """w 0: mass (g) deposited by I amps for t s; w 1: time (s) to deposit m g — charge counted in electrons"""
    F = N_("96485.33212")
    if int(w) == 0:
        return N_(I) * N_(t_or_m) / F / int(n) * N_(M)
    t = sp.Symbol("t", positive=True)
    return sp.solve(N_(I) * t / F / int(n) * N_(M) - N_(t_or_m), t)[0]


def born_haber(sub, ie, half_diss, ea, form):
    """lattice enthalpy (formation of the lattice from gaseous ions, negative) closing the cycle"""
    U = sp.Symbol("U")
    total = sum(N_(v) for v in ie) if isinstance(ie, list) else N_(ie)
    eq = sp.Eq(N_(form), N_(sub) + total + N_(half_diss) + (sum(N_(e) for e in ea) if isinstance(ea, list) else N_(ea)) + U)
    return sp.solve(eq, U)[0]


def bond_enthalpy(broken, formed, table):
    """ΔH = Σ broken − Σ formed, with bonds written 'C-H:4,O=O:2'"""
    T = dict((k, N_(v)) for k, v in (x.split(":") for x in str(table).split(",")))
    def tot(spec):
        return sum(int(n) * T[b] for b, n in (x.split("*") for x in str(spec).split(",")))
    return tot(broken) - tot(formed)


def rate_time(order, k, C0, C):
    """time for [A] to fall from C0 to C: dsolve d[A]/dt = −k[A]^n, then solve"""
    t = sp.Symbol("t", positive=True)
    A = sp.Function("A")
    n = int(order)
    sol = sp.dsolve(sp.Eq(A(t).diff(t), -N_(k) * A(t) ** n), A(t), ics={A(0): N_(C0)})
    sol = sol[0] if isinstance(sol, list) else sol
    roots = sp.solve(sp.Eq(sol.rhs, N_(C)), t)
    return [r for r in roots if r.is_positive][0]


def daughter_atoms(N0, t1, t2, t):
    """parent → daughter → (stable): solve the linear ODE system; daughter atoms at time t"""
    tt = sp.Symbol("tt", positive=True)
    P, D = sp.Function("P"), sp.Function("D")
    l1, l2 = sp.log(2) / N_(t1), sp.log(2) / N_(t2)
    sol = sp.dsolve([sp.Eq(P(tt).diff(tt), -l1 * P(tt)), sp.Eq(D(tt).diff(tt), l1 * P(tt) - l2 * D(tt))], [P(tt), D(tt)], ics={P(0): N_(N0), D(0): 0})
    Dsol = [s for s in sol if s.lhs == D(tt)][0].rhs
    return Dsol.subs(tt, N_(t))


def vant_hoff_alpha(dTf, Kf, m, nu):
    """degree of dissociation from ΔT_f = i K_f m with i = 1 + α(ν − 1), solved for α"""
    a = sp.Symbol("a")
    return sp.solve(sp.Eq(N_(dTf), (1 + a * (int(nu) - 1)) * N_(Kf) * N_(m)), a)[0]


ISO = {"Cl": [(35, N_("0.7576")), (37, N_("0.2424"))], "Br": [(79, N_("0.5069")), (81, N_("0.4931"))]}


def isotope_ratio(el, n, k):
    """intensity of the M + 2k peak relative to M for n atoms of Cl or Br, by enumerating every combination"""
    iso = ISO[str(el)]
    peaks = {}
    for combo in itertools.product(iso, repeat=int(n)):
        m = sum(a for a, _ in combo)
        p = sp.Integer(1)
        for _, w in combo:
            p *= w
        peaks[m] = peaks.get(m, 0) + p
    base = min(peaks)
    return peaks[base + 2 * int(k)] / peaks[base]


def multiplet_lines(n1, n2=0, J_equal=0):
    """lines from coupling to n1 and n2 spin-½ neighbours: count distinct total shifts (J values 7 and 3, or equal)"""
    J1, J2 = 7, (7 if int(J_equal) else 3)
    shifts = set()
    for s1 in itertools.product((-1, 1), repeat=int(n1)):
        for s2 in itertools.product((-1, 1), repeat=int(n2)):
            shifts.add(J1 * sum(s1) + J2 * sum(s2))
    return sp.Integer(len(shifts))


def kp_from_kc(Kc, T, dn):
    """build Kp from partial pressures p = cRT for a reaction with Δn gas moles (R in L·bar/(mol·K))"""
    R = N_("0.08314462618")
    return N_(Kc) * (R * N_(T)) ** int(dn)


def n2o4_alpha(Kp, P):
    """N₂O₄ ⇌ 2NO₂ at total pressure P: solve Kp = (2α/(1+α))²P / ((1−α)/(1+α))"""
    a = sp.Symbol("a", positive=True)
    return sp.nsolve((2 * a / (1 + a)) ** 2 * N_(P) / ((1 - a) / (1 + a)) - N_(Kp), a, 0.5, prec=30)


FUNCS = {f.__name__: f for f in [polyprotic_ph, buffer_after, ksp_acid, e_from_ksp, electrolysis, born_haber, bond_enthalpy, rate_time,
                                 daughter_atoms, vant_hoff_alpha, isotope_ratio, multiplet_lines, kp_from_kc, n2o4_alpha]}
