"""Independent checks for drills/problems/es-earth-space.yaml, ph-relativity-lagrange.yaml and mt-materials.yaml.

Generators answer with the closed forms on the cards (Kepler's third law, Wien's b/T, T = [S(1−α)/4σ]^¼,
γΔτ, (u + v)/(1 + uv/c²), a = (m₁ − m₂)g/(m₁ + m₂), Carothers). These functions reach the same numbers
another way: circular-orbit force balance, the maximum of Planck's law, energy-balance solves, the decay
ODE, Lorentz boosts and rapidities, sympy's Euler–Lagrange equations, weight-fraction averages and
functional-group counting.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
G = sp.Rational("6.67430e-11")
C = sp.Integer(299792458)
H = sp.Rational("6.62607015e-34")
KB = sp.Rational("1.380649e-23")
SIGMA = 2 * sp.pi**5 * KB**4 / (15 * C**2 * H**3)


def check(p, H_):
    return None


def orbit_period(M, a):
    """period from v²/r = GM/r², then T = 2πr/v"""
    v = sp.Symbol("v", positive=True)
    M, a = sp.nsimplify(M), sp.nsimplify(a)
    vv = sp.solve(sp.Eq(v**2 / a, G * M / a**2), v)[0]
    return 2 * sp.pi * a / vv


def escape_speed(M, r):
    v = sp.Symbol("v", positive=True)
    return sp.solve(sp.Rational(1, 2) * v**2 - G * sp.nsimplify(M) / sp.nsimplify(r), v)[0]


def wien_peak(T):
    """wavelength (nm) where Planck's law peaks: with x = hc/(λkT) the maximum solves 5(1 − e^(−x)) = x"""
    x = mp.findroot(lambda x: 5 * (1 - mp.exp(-x)) - x, 5)
    h, c, k = (mp.mpf(str(sp.N(q, 30))) for q in (H, C, KB))
    return sp.Float(h * c / (x * k * mp.mpf(str(sp.N(T, 30)))) * 1e9, 20)


def luminosity(R, T):
    return 4 * sp.pi * sp.nsimplify(R) ** 2 * SIGMA * sp.nsimplify(T) ** 4


def star_life(M):
    """lifetime relative to the Sun from fuel / burn rate with L ∝ M^3.5"""
    M = sp.nsimplify(M)
    return M / M ** sp.Rational(7, 2)


def hubble(w, H0, d=0, v=0):
    """w 0: recession speed (km/s) at distance d (Mpc); w 1: Hubble time (Gyr)"""
    H0 = sp.nsimplify(H0)
    if int(w) == 0:
        return H0 * sp.nsimplify(d)
    mpc_km = sp.Rational("3.0856775814913673e19")
    seconds = mpc_km / H0
    return seconds / (sp.Rational(365.25) * 86400 * 10**9)


def fusion_energy(n_in, m_in, m_out):
    """MeV released when n_in nuclei of atomic mass m_in (u) make one of m_out, via E = Δm c² in joules"""
    u = sp.Rational("1.66053906660e-27")
    dm = (int(n_in) * sp.nsimplify(m_in) - sp.nsimplify(m_out)) * u
    return dm * C**2 / sp.Rational("1.602176634e-13")


def decay_age(t_half, ratio):
    """age from dN/dt = −λN with N(t) = N0/(1 + D/P)"""
    t = sp.Symbol("t", positive=True)
    N = sp.Function("N")
    lam = sp.log(2) / sp.nsimplify(t_half)
    sol = sp.dsolve(sp.Eq(N(t).diff(t), -lam * N(t)), N(t), ics={N(0): 1}).rhs
    return sp.solve(sp.Eq(sol, 1 / (1 + sp.nsimplify(ratio))), t)[0]


def eq_temp(S, alb):
    """energy balance: absorbed S(1 − α)πR² = emitted 4πR²σT⁴"""
    T = sp.Symbol("T", positive=True)
    return sp.nsolve(sp.nsimplify(S) * (1 - sp.nsimplify(alb)) - 4 * SIGMA * T**4, T, 250)


def one_layer(S, alb):
    """surface and one absorbing layer: layer σTa⁴·2 = σTs⁴; top σTa⁴ = absorbed"""
    Ts, Ta = sp.symbols("Ts Ta", positive=True)
    Q = sp.nsimplify(S) * (1 - sp.nsimplify(alb)) / 4
    sol = sp.nsolve([SIGMA * Ta**4 - Q, 2 * SIGMA * Ta**4 - SIGMA * Ts**4], [Ts, Ta], [290, 250])
    return sol[0]


def co2_warming(C1, C0, lam_):
    c = sp.Symbol("c", positive=True)
    dF = sp.integrate(sp.Rational(535, 100) / c, (c, sp.nsimplify(C0), sp.nsimplify(C1)))
    return sp.nsimplify(lam_) * dF


def ppm_to_gtc(ppm):
    """mass of carbon in `ppm` of CO₂ spread through the atmosphere (5.148e18 kg of air, 28.97 g/mol)"""
    mol_air = sp.Rational("5.148e18") * 1000 / sp.Rational("28.97")
    return sp.nsimplify(ppm) * sp.Rational(1, 10**6) * mol_air * sp.Rational("12.011") / 10**15


def doubling_time(r):
    t = sp.Symbol("t", positive=True)
    return sp.nsolve((1 + sp.nsimplify(r)) ** t - 2, t, 1 / sp.N(r))


# ── relativity by boosts ─────────────────────────────────────────────────────
def _boost(beta):
    g = 1 / sp.sqrt(1 - beta**2)
    return sp.Matrix([[g, -g * beta], [-g * beta, g]])


def dilation(beta, tau):
    """lab time between ticks of a clock moving at β: transform the second tick (cτ, 0) back to the lab"""
    beta, tau = sp.nsimplify(beta), sp.nsimplify(tau)
    ev = _boost(-beta) * sp.Matrix([tau, 0])
    return ev[0]


def contraction(beta, L0):
    """length in the lab: ends at rest in the moving frame, read at one lab time"""
    beta, L0 = sp.nsimplify(beta), sp.nsimplify(L0)
    x = sp.Symbol("x")
    t0 = sp.Symbol("t0")
    # front end worldline in moving frame: x' = L0; lab: x' = γ(x − βt) → x = L0/γ + βt at t = 0
    g = 1 / sp.sqrt(1 - beta**2)
    return sp.solve(sp.Eq(g * (x - beta * 0), L0), x)[0]


def velocity_add(u, v):
    """compose by rapidities: tanh(artanh u + artanh v)"""
    return sp.tanh(sp.atanh(sp.nsimplify(u)) + sp.atanh(sp.nsimplify(v)))


def rel_energy(w, m_mev, beta):
    """w 0: kinetic energy (MeV); w 1: momentum (MeV/c), from E² = (pc)² + (mc²)² with E = γmc²"""
    m, beta = sp.nsimplify(m_mev), sp.nsimplify(beta)
    p = sp.Symbol("p", positive=True)
    E = m / sp.sqrt(1 - beta**2)
    if int(w) == 0:
        return E - m
    return sp.solve(sp.Eq(E**2, p**2 + m**2), p)[0]


def rel_doppler(f, beta):
    """approaching source: transform the wave 4-vector (ω, k) with k = ω/c by a boost"""
    beta = sp.nsimplify(beta)
    v = _boost(-beta) * sp.Matrix([sp.nsimplify(f), sp.nsimplify(f)])
    return v[0]


# ── Lagrangian mechanics by sympy's Euler–Lagrange equations ─────────────────
def lagr_eom(kind, a=0, b=0, c=0):
    t = sp.Symbol("t")
    q = sp.Function("q")(t)
    g = sp.Rational("981", 100)
    a, b, c = sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)
    kind = str(kind)
    if kind == "atwood":  # masses a, b on a string; q is how far a has fallen
        L = sp.Rational(1, 2) * (a + b) * q.diff(t) ** 2 + a * g * q - b * g * q
        want = "acc"
    elif kind == "roll":  # k = I/(m r²) = a, incline angle b degrees; q along the slope
        L = sp.Rational(1, 2) * (1 + a) * q.diff(t) ** 2 + g * sp.sin(b * sp.pi / 180) * q
        want = "acc"
    elif kind == "pendulum":  # length a; small oscillations
        L = sp.Rational(1, 2) * a**2 * q.diff(t) ** 2 + g * a * sp.cos(q)
        want = "omega"
    elif kind == "rod":  # uniform rod of length a pivoted at one end
        L = sp.Rational(1, 2) * (a**2 / 3) * q.diff(t) ** 2 + g * (a / 2) * sp.cos(q)
        want = "omega"
    elif kind == "springs":  # mass a between two springs b and c (both attached to walls)
        L = sp.Rational(1, 2) * a * q.diff(t) ** 2 - sp.Rational(1, 2) * (b + c) * q**2
        want = "omega"
    elif kind == "series":  # mass a on two springs b and c joined end to end: second coordinate eliminated
        y = sp.Function("y")(t)
        L = sp.Rational(1, 2) * a * q.diff(t) ** 2 - sp.Rational(1, 2) * b * y**2 - sp.Rational(1, 2) * c * (q - y) ** 2
        eqs = sp.euler_equations(L, [q, y], t)
        ysol = sp.solve(eqs[1].lhs, y)[0]
        e = eqs[0].lhs.subs(y, ysol)
        k = sp.simplify(-e.coeff(q) / a) if e.coeff(q) != 0 else None
        acc_coeff = sp.simplify(e.coeff(q.diff(t, 2)))
        return sp.sqrt(sp.simplify(e.subs(q.diff(t, 2), 0).coeff(q) / acc_coeff))
    eq = sp.euler_equations(L, [q], t)[0].lhs
    qdd = sp.solve(eq, q.diff(t, 2))[0]
    if want == "acc":
        return sp.simplify(qdd)
    z = sp.Symbol("z")
    lin = sp.diff(qdd.subs(q, z), z).subs(z, 0)  # linearise about q = 0
    return sp.sqrt(-lin)


# ── polymers and materials ───────────────────────────────────────────────────
def mol_avg(w, ns, Ms):
    """w 0: Mn, w 1: Mw, w 2: PDI, computed from weight fractions"""
    n = [sp.nsimplify(x) for x in ns]
    M = [sp.nsimplify(x) for x in Ms]
    mass = [a * b for a, b in zip(n, M)]
    tot = sum(mass)
    wf = [m / tot for m in mass]
    Mn = 1 / sum(f / m for f, m in zip(wf, M))
    Mw = sum(f * m for f, m in zip(wf, M))
    return [Mn, Mw, Mw / Mn][int(w)]


def carothers(p, r=1):
    """functional-group count: start with N_A = 1 and N_B = 1/r; after reaction to extent p of A groups"""
    p, r = sp.nsimplify(p), sp.nsimplify(r)
    NA, NB = sp.Integer(1), 1 / r
    molecules0 = (NA + NB) / 2
    reacted = p * NA  # each bond consumes one A and one B and removes one molecule
    return molecules0 / (molecules0 - reacted)


def band_gap_wavelength(Eg):
    """λ (nm) of a photon with the gap energy, E = hc/λ"""
    lam = sp.Symbol("lam", positive=True)
    E = sp.nsimplify(Eg) * sp.Rational("1.602176634e-19")
    return sp.solve(sp.Eq(H * C / lam, E), lam)[0] * 10**9


FUNCS = {f.__name__: f for f in [orbit_period, escape_speed, wien_peak, luminosity, star_life, hubble, fusion_energy, decay_age, eq_temp,
                                 one_layer, co2_warming, ppm_to_gtc, doubling_time, dilation, contraction, velocity_add, rel_energy,
                                 rel_doppler, lagr_eom, mol_avg, carothers, band_gap_wavelength]}

# ── facts, typed a second time (index into the card's literal option list) ──
ES_FACTS = {
    "origin": {"most helium-4": "big bang", "deuterium": "big bang", "carbon and oxygen": "stars", "iron and nickel": "stars", "gold and uranium": "capture",
               "barium and lead (s-process)": "capture", "lithium-6, beryllium and boron": "spallation"},
    "boundary": {"the Mid-Atlantic Ridge": "div", "the East African Rift": "div", "Iceland": "div", "the Andes": "conv", "the Himalaya": "conv", "the Mariana Trench": "conv",
                 "the San Andreas Fault": "trans"},
    "feedback": {"melting sea ice lowers albedo": "+", "warmer air holds more water vapour": "+", "thawing permafrost releases CH₄ and CO₂": "+",
                 "a warmer surface radiates more (Planck response)": "-", "faster rock weathering draws down CO₂ over ~100 kyr": "-"},
    "seismic": {"through the liquid outer core": "P", "through the mantle": "PS", "through the solid inner core (as P)": "P"},
    "dating": {"a 5000-year-old wooden tool": "C14", "bone collagen 20 000 years old": "C14", "a 2-million-year-old volcanic ash layer": "KAr",
               "a 4.4-billion-year-old zircon": "UPb", "the age of a meteorite": "UPb"},
    "growth": {"polyethylene": "chain", "PVC": "chain", "polystyrene": "chain", "PMMA": "chain", "nylon-6,6": "step", "PET": "step", "a polyurethane": "step", "polycarbonate": "step"},
    "thermal": {"polyethylene": "plastic", "PET": "plastic", "nylon": "plastic", "vulcanised rubber": "set", "epoxy resin": "set", "Bakelite": "set"},
}
ES_ORDER = {"origin": ["big bang", "stars", "capture", "spallation"], "boundary": ["div", "conv", "trans"], "feedback": ["+", "-"], "seismic": ["P", "PS", "none"],
            "dating": ["C14", "KAr", "UPb"], "growth": ["chain", "step"], "thermal": ["plastic", "set"]}


def es_fact(table, key):
    return ES_ORDER[str(table)].index(ES_FACTS[str(table)][str(key)])


FUNCS["es_fact"] = es_fact
