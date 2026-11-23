"""Independent checks for drills/problems/sp-separations.yaml and pd-design.yaml.

Generators use the textbook closed forms (Fenske, Underwood for a saturated-liquid binary feed, Kremser
solved for N, H = 0.622 p/(P − p), the annuity factor, Le Chatelier's mixing rule, t = −τ ln(1 − f)).
These reach the same numbers another way: stage-to-stage at total reflux, the pinch geometry on the
McCabe–Thiele diagram, the fraction-absorbed equation solved numerically, mole bookkeeping, explicit
cash-flow sums, solving for the mixture's lower limit, dsolve.
"""
import sympy as sp


def check(p, H):
    return None


N_ = sp.nsimplify


def fenske_steps(alpha, xD, xB):
    """at total reflux the ratio x/(1 − x) grows by α each stage: solve α^N r_B = r_D"""
    rD, rB, a = N_(xD) / (1 - N_(xD)), N_(xB) / (1 - N_(xB)), N_(alpha)
    lo, hi = sp.Integer(0), sp.Integer(1)
    while a**hi * rB < rD:  # bracket by whole stages, then bisect the fractional last stage
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sp.N(a**mid * rB, 40) < rD else (lo, mid)
    return sp.N((lo + hi) / 2, 20)


def rmin_pinch(alpha, xD, xF):
    """saturated-liquid feed: the q-line is x = x_F; the operating line touches equilibrium there"""
    a, xF, xD = N_(alpha), N_(xF), N_(xD)
    ystar = a * xF / (1 + (a - 1) * xF)
    slope = (xD - ystar) / (xD - xF)  # R/(R + 1)
    return slope / (1 - slope)


def kremser_stages(A, f):
    """stages for fraction absorbed f with solute-free solvent: solve f = (A^(N+1) − A)/(A^(N+1) − 1)"""
    N = sp.Symbol("N", positive=True)
    A, f = N_(A), N_(f)
    return sp.nsolve(f * (A ** (N + 1) - 1) - (A ** (N + 1) - A), N, 4)


def y_from_raoult(PA, PB, x):
    """vapour mole fraction of A from partial pressures over an ideal liquid"""
    pA, pB = N_(PA) * N_(x), N_(PB) * (1 - N_(x))
    return pA / (pA + pB)


def abs_humidity(RH, psat, P):
    """kg water per kg dry air from moles: n_w/n_air = p_w/(P − p_w), times molar masses"""
    pw = N_(RH) * N_(psat)
    return pw / (N_(P) - pw) * sp.Rational("18.015") / sp.Rational("28.97")


def evaporated(F, x0, x1):
    """water evaporated from a feed F at solids fraction x0 to x1 (solids balance, solved)"""
    V, L = sp.symbols("V L", positive=True)
    s = sp.solve([N_(F) - V - L, N_(F) * N_(x0) - L * N_(x1)], [V, L], dict=True)[0]
    return s[V]


def npv(I, A, n, i, S=0):
    """net present value as an explicit sum of discounted cash flows"""
    i = N_(i)
    return -N_(I) + sum(N_(A) / (1 + i) ** k for k in range(1, int(n) + 1)) + N_(S) / (1 + i) ** int(n)


def payback(I, flows):
    """years until cumulative cash flow covers the investment, interpolating within the year"""
    cum = -N_(I)
    for k, f in enumerate(flows, 1):
        f = N_(f)
        if cum + f >= 0:
            return k - 1 + (-cum) / f
        cum += f
    return sp.oo


def scaled_cost(C1, S1, S2, n, I1, I2):
    """cost ratio from capacity and index ratios, built as a product of the two corrections"""
    return N_(C1) * sp.exp(N_(n) * sp.log(N_(S2) / N_(S1))) * N_(I2) / N_(I1)


def book_value(kind, P, S, n, k):
    """book value after k years: straight line or double-declining balance, one year at a time"""
    v = N_(P)
    for _ in range(int(k)):
        if str(kind) == "sl":
            v -= (N_(P) - N_(S)) / int(n)
        else:
            v -= v * 2 / int(n)
    return v


def effective_rate(r, m):
    """compound m times a year for one year"""
    v = sp.Integer(1)
    for _ in range(int(m)):
        v *= 1 + N_(r) / int(m)
    return v - 1


def lfl_mix(ys, lfls):
    """lower flammable limit of a fuel mixture: the total fuel % c at which Σ (c y_i / LFL_i) = 1"""
    c = sp.Symbol("c", positive=True)
    return sp.solve(sum(c * N_(y) / N_(L) for y, L in zip(ys, lfls)) - 1, c)[0]


def exposure_over(cs, tlvs):
    tot = 0
    for c, t in zip(cs, tlvs):
        tot += N_(c) / N_(t)
    return 1 if tot > 1 else 0


def first_order(w, tau, f=0, t=0):
    """τ dy/dt + y = 1 from y(0) = 0: w 0 → time to reach fraction f; w 1 → y at time t"""
    tt = sp.Symbol("tt", positive=True)
    y = sp.Function("y")
    sol = sp.dsolve(sp.Eq(N_(tau) * y(tt).diff(tt) + y(tt), 1), y(tt), ics={y(0): 0}).rhs
    if int(w) == 0:
        return sp.solve(sp.Eq(sol, N_(f)), tt)[0]
    return sol.subs(tt, N_(t))


HAZOP = {"NO": "none of the design intent happens", "MORE": "a quantitative increase", "LESS": "a quantitative decrease",
         "REVERSE": "the logical opposite of the intent", "AS WELL AS": "something extra happens besides the intent",
         "PART OF": "only some of the intent happens", "OTHER THAN": "something completely different happens"}


def hazop_pick(k, o1, o2, o3, o4):
    hits = [i for i, o in enumerate((o1, o2, o3, o4)) if str(o) == HAZOP[str(k)]]
    assert len(hits) == 1
    return hits[0]


FUNCS = {f.__name__: f for f in [fenske_steps, rmin_pinch, kremser_stages, y_from_raoult, abs_humidity, evaporated, npv, payback, scaled_cost,
                                 book_value, effective_rate, lfl_mix, exposure_over, first_order, hazop_pick]}
