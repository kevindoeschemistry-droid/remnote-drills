"""
Statistical mechanics (gen-stat.ts) — recomputed from first principles, sharing no
formula with the generator:

  counting        brute-force enumeration with itertools (permutations, combinations,
                  coin/die outcome tuples, compositions of q quanta over oscillators)
  Boltzmann/q     explicit sums over microstates (degeneracies expanded into states)
  U, S, F, Cv     U = <E> from the sum, S = -k sum p ln p (Gibbs), F = U - TS,
                  Cv = dU/dT by differentiating the summed U (sympy, or mpmath for the
                  infinite oscillator ladder, truncated far past convergence)
  fluctuations    <E^2> - <E>^2 from the same weights; ideal gas from d^2 lnQ/dbeta^2
                  with Q from the momentum Gaussian integral
  ideal gas       Lambda from the momentum integral; rotor I about the centre of mass;
                  q_rot high-T limit as the integral over J; q_vib by summing levels
  ensembles       grand-canonical / isobaric weights summed over every state
  binding         site partition functions; Hill n_H by solving the two Hill equations
  rates           Arrhenius pairs solved for (A, Ea); Eyring from dG = dH - T dS
"""
from functools import lru_cache
from itertools import combinations, permutations, product

import mpmath as mp
import sympy as sp

KB = sp.Rational("1.380649e-23")
HP = sp.Rational("6.62607015e-34")
NA = sp.Rational("6.02214076e23")
RG = sp.Rational("8.314")
AMU = sp.Rational("1.6605390666e-27")
CCM = sp.Rational("2.99792458e10")
x = sp.Symbol("x")


def Rn(v):
    return sp.Rational(str(v))


def compositions(q, n):
    """all tuples of n nonnegative ints summing to q"""
    if n == 1:
        yield (q,)
        return
    for first in range(q + 1):
        for rest in compositions(q - first, n - 1):
            yield (first,) + rest


def states(levels):
    """[(E, g), ...] -> one entry per microstate"""
    return [E for E, g_ in levels for _ in range(g_)]


def close(a, b, rel=1e-6):
    a, b = float(a), float(b)
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


def same_x(expr, expect, H):
    return H.zero(sp.sympify(expr) - expect, (x,))


def ladder(xv, power=1, shift=0, n=4000):
    """sum_v E_v^power e^{-x v} / sum_v e^{-x v}, E_v = v + shift (units of the quantum)"""
    num = mp.mpf(0)
    den = mp.mpf(0)
    for v in range(n):
        w = mp.e ** (-xv * v)
        num += (v + shift) ** power * w
        den += w
        if w < mp.mpf(10) ** -60:
            break
    return num / den


@lru_cache(maxsize=None)
def fluct_identity_holds():
    """<E^2> - <E>^2 == k T^2 dU/dT for a generic 3-level system (symbolic)."""
    T, k = sp.symbols("T k", positive=True)
    Es = sp.symbols("E0:3", real=True)
    w = [sp.exp(-E / (k * T)) for E in Es]
    Z = sum(w)
    U = sum(E * wi for E, wi in zip(Es, w)) / Z
    E2 = sum(E**2 * wi for E, wi in zip(Es, w)) / Z
    return sp.simplify(E2 - U**2 - k * T**2 * sp.diff(U, T)) == 0


def expected(p):
    me = p["meta"]
    sm = me["sm"]
    # ── counting ──────────────────────────────────────────────────────────
    if sm == "perm":
        return sp.Integer(sum(1 for _ in permutations(range(me["n"]), me["k"])))
    if sm == "comb":
        return sp.Integer(sum(1 for _ in combinations(range(me["n"]), me["k"])))
    if sm in ("binom", "atleast"):
        a, b, n = me["a"], me["b"], me["n"]
        hits = 0
        for out in product(range(b), repeat=n):
            s = sum(1 for o in out if o < a)  # faces 0..a-1 count as success
            hits += (s == me["k"]) if sm == "binom" else (s >= 1)
        return sp.Rational(hits, b**n)
    if sm == "anagram":
        seq = [i for i, c in enumerate(me["counts"]) for _ in range(c)]
        return sp.Integer(len(set(permutations(seq))))
    if sm == "two-state":
        return sp.Integer(sum(1 for s in product((0, 1), repeat=me["N"]) if sum(s) == me["n"]))
    if sm == "einstein":
        return sp.Integer(sum(1 for _ in compositions(me["q"], me["N"])))
    if sm == "dS-two-state":
        W = lambda n_: sum(1 for s in product((0, 1), repeat=me["N"]) if sum(s) == n_)
        return sp.log(sp.Rational(W(me["n2"]), W(me["n1"])))
    if sm == "dS-volume":
        # 3 molecules on M = 2V cells: W = number of placements; per molecule ln(W2/W1)/3
        Nm = 3
        W1 = sum(1 for _ in product(range(2 * me["V1"]), repeat=Nm))
        W2 = sum(1 for _ in product(range(2 * me["V2"]), repeat=Nm))
        return Rn(me["nmol"]) * RG * sp.log(sp.Rational(W2, W1)) / Nm
    if sm == "einstein-share":
        nA, nB, q, qA = me["NA"], me["NB"], me["q"], me["qA"]
        tot = hit = 0
        for c in compositions(q, nA + nB):
            tot += 1
            hit += sum(c[:nA]) == qA
        return sp.Rational(hit, tot)
    # ── Boltzmann ─────────────────────────────────────────────────────────
    if sm == "bz-ratio":
        T = Rn(me["T"])
        if "nu" in me:
            E2, beta = HP * CCM * Rn(me["nu"]), 1 / (KB * T)
        else:
            E2, beta = Rn(me["dE"]) * 1000, 1 / (RG * T)
        lv1 = states([(0, me["g1"])])
        lv2 = states([(E2, me["g2"])])
        return sum(sp.exp(-beta * E) for E in lv2) / sum(sp.exp(-beta * E) for E in lv1)
    if sm in ("bz-fraction", "pf-q"):
        beta = 1 / (RG * Rn(me["T"]))
        levels = [(Rn(E) * 1000, g_) for E, g_ in zip(me["Es"], me["gs"])]
        Z = sum(sp.exp(-beta * E) for E in states(levels))
        if sm == "pf-q":
            return Z
        E_, g_ = levels[me["which"]]
        return sum(sp.exp(-beta * E) for E in states([(E_, g_)])) / Z
    if sm == "bz-T":
        T = sp.Symbol("T", positive=True)
        E = Rn(me["dE"]) * 1000
        ratio = sum(sp.exp(-E / (RG * T)) for _ in range(me["g2"])) / me["g1"]
        # N2/N1 = ratio; take logs of both sides and solve numerically
        eq = sp.expand_log(sp.log(sp.simplify(ratio)), force=True) - sp.log(Rn(me["ratio"]))
        return sp.solve(eq, T)[0]
    if sm in ("bz-exact", "fl-exact"):
        f = sp.Rational(1, me["a"])  # e^{-eps/kT}
        micro = states([(j, g_) for j, g_ in enumerate(me["gs"])])
        Z = sum(f**E for E in micro)
        if sm == "bz-exact":
            return sum(f**E for E in micro if E == me["j"]) / Z
        m1 = sum(E * f**E for E in micro) / Z
        m2 = sum(E**2 * f**E for E in micro) / Z
        return m2 - m1**2
    # ── partition functions, symbolic in x = eps/kT ───────────────────────
    if sm in ("pf-U2", "pf-S2", "fl-two"):
        micro = states([(0, me["g0"]), (1, me["g1"])])
        Z = sum(sp.exp(-x * E) for E in micro)
        ps = [sp.exp(-x * E) / Z for E in micro]
        if sm == "pf-U2":
            return sum(E * pi for E, pi in zip(micro, ps))
        if sm == "pf-S2":
            return -sum(pi * sp.log(pi) for pi in ps)
        m1 = sum(E * pi for E, pi in zip(micro, ps))
        return sum(E**2 * pi for E, pi in zip(micro, ps)) - m1**2
    if sm == "cv-two":
        T, eps, k = sp.symbols("T epsilon k", positive=True)
        micro = states([(0, me["g0"]), (eps, me["g1"])])
        Z = sum(sp.exp(-E / (k * T)) for E in micro)
        U = sum(E * sp.exp(-E / (k * T)) for E in micro) / Z
        cv = sp.diff(U, T) / k
        return sp.simplify(cv.subs(T, eps / (k * x)))
    if sm == "pf-F":
        T = Rn(me["T"])
        micro = states([(0, me["g0"]), (Rn(me["E1"]) * 1000, me["g1"])])
        Z = sum(sp.exp(-E / (RG * T)) for E in micro)
        ps = [sp.exp(-E / (RG * T)) / Z for E in micro]
        U = sum(E * pi for E, pi in zip(micro, ps))
        S = -RG * sum(pi * sp.log(pi) for pi in ps)
        return (U - T * S) / 1000
    # ── ideal gas ─────────────────────────────────────────────────────────
    if sm in ("ig-lambda", "ig-qtrans"):
        pp = sp.Symbol("p", real=True)
        mass, T = Rn(me["M"]) * AMU, Rn(me["T"])
        per_len = sp.integrate(sp.exp(-pp**2 / (2 * mass * KB * T)), (pp, -sp.oo, sp.oo)) / HP  # = 1/Lambda
        if sm == "ig-lambda":
            return 1 / per_len * sp.Integer(10) ** 12
        return Rn(me["V"]) * per_len**3
    if sm == "ig-theta-rot":
        m1, m2, r = Rn(me["m1"]) * AMU, Rn(me["m2"]) * AMU, Rn(me["r"]) / sp.Integer(10) ** 12
        com = m2 * r / (m1 + m2)
        I = m1 * com**2 + m2 * (r - com) ** 2
        hbar = HP / (2 * sp.pi)
        EJ = lambda J: J * (J + 1) * hbar**2 / (2 * I)
        return (EJ(1) - EJ(0)) / (2 * KB)  # E_1 - E_0 = 2 k theta
    if sm == "ig-qrot":
        th, T = float(me["th"]), float(me["T"])
        val = mp.quad(lambda J: (2 * J + 1) * mp.e ** (-J * (J + 1) * th / T), [0, mp.inf])
        return sp.Float(val / me["s"], 30)
    if sm == "ig-qvib":
        th = (HP * CCM * Rn(me["nu"])) / KB  # (E_1 - E_0)/k for E_v = v h c nu
        if me["variant"] == "theta":
            return th
        xv = mp.mpf(str(sp.N(th / Rn(me["T"]), 40)))
        q = mp.mpf(0)
        for v in range(4000):
            w = mp.e ** (-xv * v)
            q += w
            if w < mp.mpf(10) ** -60:
                break
        return sp.Float(q if me["variant"] == "q" else 1 - 1 / q, 30)
    # ── heat capacity ─────────────────────────────────────────────────────
    if sm == "cv-equip":
        terms = 3  # translational kinetic energy
        rot = 0 if me["atoms"] == 1 else (2 if me["linear"] else 3)
        terms += rot
        if me["high"]:
            terms += 2 * (3 * me["atoms"] - 3 - rot)
        return sp.Rational(terms, 2)
    if sm in ("cv-einstein", "cv-gas"):
        th = float(me["thE"] if sm == "cv-einstein" else me["th"])
        Rf = mp.mpf("8.314")

        def U(T):
            vib = Rf * th * ladder(th / T)  # molar, E_v = v R theta
            return 3 * vib if sm == "cv-einstein" else mp.mpf(3) / 2 * Rf * T + Rf * T + vib

        return sp.Float(mp.diff(U, mp.mpf(me["T"])), 30)
    # ── checked pointwise in x (infinite ladders) ────────────────────────
    raise KeyError(sm)


def pointwise(p, H):
    """oscillator answers in x: compare the reference with summed ladders at sample x."""
    me = p["meta"]
    sm = me["sm"]
    ref = H.P(p["answer"]["ref"])
    for xv in ("0.3", "0.55", "0.9", "1.4", "2.3"):
        X = mp.mpf(xv)
        if sm == "pf-Uho":
            want = ladder(X, 1, 0.5 if me["zp"] else 0)
        elif sm == "fl-ho":
            sh = 0.5 if me["zp"] else 0
            want = ladder(X, 2, sh) - ladder(X, 1, sh) ** 2
        else:  # cv-ho: C/k = dU/dT with eps = k = 1, T = 1/x, times k independent directions
            want = me["k"] * mp.diff(lambda T: ladder(1 / T, 1, 0.5), 1 / X)
        got = mp.mpf(str(sp.N(ref.subs(x, sp.Rational(xv)), 40)))
        if abs(got - want) > mp.mpf(10) ** -20 * max(1, abs(want)):
            return False
    return True


def check(p, H):
    me = p.get("meta") or {}
    if not str(p.get("skill", "")).startswith("stat.") or "sm" not in me:
        return None
    mp.mp.dps = 50
    sm = me["sm"]
    a = p["answer"]
    if sm in ("pf-Uho", "fl-ho", "cv-ho"):
        return pointwise(p, H)
    # the rest: compute independently, compare
    if sm == "fl-rel":
        beta, N, m_, pp = sp.symbols("beta N m p", positive=True)
        Q1 = sp.integrate(sp.exp(-beta * pp**2 / (2 * m_)), (pp, -sp.oo, sp.oo)) ** 3  # momentum part of q
        lnQ = N * sp.log(Q1)  # N!, h and V are beta-independent
        E = -sp.diff(lnQ, beta)
        var = sp.diff(lnQ, beta, 2)
        want = sp.simplify(sp.sqrt(var) / E).subs(N, Rn(me["N"]))
    elif sm == "fl-cv":
        if not fluct_identity_holds():
            return False
        T = Rn(me["T"])
        want = sp.sqrt(RG * T**2 * Rn(me["Cv"]) * 1000) / 1000  # per mole of molecules, kJ/mol
    elif sm == "ens-site":
        beta = 1 / (RG * Rn(me["T"]))
        mu, eps = Rn(me["mu"]) * 1000, Rn(me["eps"]) * 1000
        st = [(0, 0), (1, -eps)]  # (n, E_n)
        w = [sp.exp(-beta * (E - mu * n_)) for n_, E in st]
        Xi = sum(w)
        want = w[0] / Xi if me["empty"] else sum(n_ * wi for (n_, _), wi in zip(st, w)) / Xi
    elif sm in ("ens-lattice", "ens-nfluct"):
        lam, f = sp.Rational(1, me["zd"]), sp.Integer(me["f"])
        Xi = s1 = s2 = 0
        for occ in product((0, 1), repeat=me["M"]):
            Nn = sum(occ)
            w = lam**Nn * f**Nn  # e^{beta mu N} e^{-beta E}, E = -N eps
            Xi += w
            s1 += Nn * w
            s2 += Nn**2 * w
        want = s1 / Xi if sm == "ens-lattice" else s2 / Xi - (s1 / Xi) ** 2
    elif sm == "ens-pair":
        y, w = sp.Rational(*me["y"]), sp.Rational(*me["w"])
        Xi = s1 = 0
        for occ in product((0, 1), repeat=2):
            Nn = sum(occ)
            wt = y**Nn * (w if Nn == 2 else 1)
            Xi += wt
            s1 += Nn * wt
        want = s1 / Xi
    elif sm == "ens-isobaric":
        beta = 1 / (RG * Rn(me["T"]))
        pr = Rn(me["p"]) * 10**5
        A = (0, 0)
        B = (Rn(me["dE"]) * 1000, Rn(me["dV"]) / 10**6)
        wt = lambda s: sp.exp(-beta * (s[0] + pr * s[1]))
        Delta = wt(A) + wt(B)
        want = (wt(B) / Delta) / (wt(A) / Delta)
    elif sm in ("bind-theta", "bind-p", "bind-hill"):
        if sm == "bind-hill":
            n_ = me["n"]
            z = sp.Rational(*me["c"]) / me["K"]
            sites = {0: 1, n_: z**n_}  # all-or-none: 0 or n ligands
            want = sum(k_ * w for k_, w in sites.items()) / sum(sites.values()) / n_
        else:
            K = sp.Rational(*me["K"]) if sm == "bind-theta" else Rn(me["K"])
            s_ = sp.Symbol("s", positive=True)
            occ = lambda X_: (K * X_) / (1 + K * X_)  # site sum: empty 1, bound K X
            if sm == "bind-theta":
                want = occ(sp.Rational(*me["x"]))
            else:
                want = sp.solve(sp.Eq(occ(s_), Rn(me["th"])), s_)[0]
    elif sm == "bind-nh":
        n_, L = sp.symbols("n L")
        eqs = [sp.Eq(sp.log(Rn(t) / (1 - Rn(t))), n_ * (sp.log(Rn(c)) - L)) for c, t in ((me["c1"], me["t1"]), (me["c2"], me["t2"]))]
        want = sp.solve(eqs, [n_, L], dict=True)[0][n_]
    elif sm == "bind-dg":
        T = Rn(me["T"])
        if me["variant"] == "dG":
            Ka = 1 / Rn(me["Kd"])
            want = -RG * T * sp.log(Ka) / 1000
        else:
            wb = Rn(me["c"]) * sp.exp(-Rn(me["dG"]) * 1000 / (RG * T))  # (c/1 M) e^{-beta dG}
            want = wb / (1 + wb)
    elif sm in ("rate-ea", "rate-k2", "rate-factor"):
        Aa, Ea = sp.symbols("A E_a", positive=True)
        k = lambda T_: Aa * sp.exp(-Ea / (RG * T_))
        T1, T2 = Rn(me["T1"]), Rn(me["T2"])
        if sm == "rate-ea":
            lnA = sp.Symbol("lnA")
            lnk = lambda T_: sp.expand_log(sp.log(k(T_)), force=True).subs(sp.log(Aa), lnA)
            sol = sp.solve([lnk(T1) - sp.log(Rn(me["k1"])), lnk(T2) - sp.log(Rn(me["k2"]))], [lnA, Ea], dict=True)[0]
            want = sol[Ea] / 1000
        elif sm == "rate-k2":
            Asol = sp.solve(sp.Eq(k(T1).subs(Ea, Rn(me["Ea"]) * 1000), Rn(me["k1"])), Aa)[0]
            want = k(T2).subs({Ea: Rn(me["Ea"]) * 1000, Aa: Asol})
        elif me["variant"] == "factor":
            want = sp.simplify(k(T2) / k(T1)).subs(Ea, Rn(me["Ea"]) * 1000)
        else:
            # k2/k1 = fac; logs of both sides are linear in Ea
            ratio = sp.expand_log(sp.log(sp.simplify(k(T2) / k(T1))), force=True)
            want = sp.solve(ratio - sp.log(me["fac"]), Ea)[0] / 1000
    elif sm == "rate-eyring":
        T = Rn(me["T"])
        G = Rn(me["dH"]) * 1000 - T * Rn(me["dS"])  # G = H - TS
        want = KB * T / HP * sp.exp(-G / (RG * T))
    elif sm == "rate-dg":
        T = Rn(me["T"])
        G = sp.Symbol("G")
        eyring = KB * T / HP * sp.exp(-G / (RG * T))
        want = sp.nsolve(sp.log(eyring) - sp.log(Rn(me["k"])), G, 80000, prec=40) / 1000
    else:
        want = expected(p)

    ref = H.P(a["ref"])
    if (a.get("vars") or []) == ["x"] or ref.has(x):
        return same_x(ref, want, H)
    if a.get("rel"):
        return close(sp.N(want, 30), sp.N(ref, 30))
    # exact numbers: equal as exact values
    return sp.simplify(sp.nsimplify(ref) - sp.nsimplify(want)) == 0 if not want.has(sp.log) else \
        abs(sp.N(ref - want, 40)) < 1e-30
