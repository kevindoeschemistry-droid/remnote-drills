"""Independent checks for drills/problems/in-inorganic.yaml and an-analytical.yaml.

The generators (scripts/in_cases.py, scripts/an_cases.py) answer from look-up tables and closed forms;
these functions get there another way: oxidation states by charge balance from rules, d counts from
group minus oxidation state, unpaired electrons and CFSE by filling orbitals, stereoisomers by brute-force
enumeration over the rotation group, unit-cell contents and coordination from atom positions, titrations
by electron counting to the final reduced form, equilibria by nsolve. Facts (colours, tests, oxide
character) are a second, separately typed table: a typo in either fails the check.
"""
import itertools
import math
import re

import mpmath as mp
import sympy as sp

mp.mp.dps = 30


def check(p, H):
    return None


# ── formulas ─────────────────────────────────────────────────────────────────
MASS = {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085,
        "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098, "Ca": 40.078, "Cr": 51.996, "Mn": 54.938, "Fe": 55.845, "Co": 58.933,
        "Ni": 58.693, "Cu": 63.546, "Zn": 65.38, "Br": 79.904, "Ag": 107.868, "I": 126.904, "Ba": 137.327, "Pb": 207.2, "W": 183.84,
        "Mo": 95.95, "Po": 209.0, "Cs": 132.905}


def atoms(f):
    """element counts of a formula with parentheses and a dot for hydrates, e.g. 'Ni(C4H7N2O2)2', 'CuSO4.5H2O'"""
    def group(s, i):
        out = {}
        while i < len(s) and s[i] != ")":
            if s[i] == "(":
                inner, i = group(s, i + 1)
                i += 1  # past ')'
                m = re.match(r"\d+", s[i:])
                k = int(m.group()) if m else 1
                i += len(m.group()) if m else 0
                for e, n in inner.items():
                    out[e] = out.get(e, 0) + n * k
            else:
                m = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
                out[m.group(1)] = out.get(m.group(1), 0) + int(m.group(2) or 1)
                i += len(m.group())
        return out, i
    total = {}
    for part in str(f).split("."):
        m = re.match(r"^(\d*)(.*)$", part)
        g, _ = group(m.group(2), 0)
        for e, n in g.items():
            total[e] = total.get(e, 0) + n * int(m.group(1) or 1)
    return total


def molar_mass(f):
    return sum(MASS[k] * v for k, v in atoms(f).items())


# ── oxidation states by rule and charge balance ─────────────────────────────
RULE = {"F": -1, "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1, "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2, "Al": 3, "H": 1, "O": -2,
        "Cl": -1, "Br": -1, "I": -1}


def ox_state(formula, charge, target):
    """average oxidation state of `target`: every other element takes its rule value, then charge balance"""
    a = atoms(formula)
    rest = sum(RULE[e] * n for e, n in a.items() if e != target)
    return sp.Rational(int(charge) - rest, a[target])


def disprop_ratio(f0, q0, f_red, q_red, f_ox, q_ox, el):
    """atoms reduced per atom oxidized when `el` in f0 goes to f_red and f_ox (electron balance)"""
    s0, sr, so = ox_state(f0, q0, el), ox_state(f_red, q_red, el), ox_state(f_ox, q_ox, el)
    return (so - s0) / (s0 - sr)


def half_electrons(f_from, q_from, f_to, q_to, el, n_from=1, n_to=1):
    """electrons in a half-reaction: change in oxidation state times atoms of `el` that change"""
    s1, s2 = ox_state(f_from, q_from, el), ox_state(f_to, q_to, el)
    k = atoms(f_from)[el] * int(n_from)
    return abs(s1 - s2) * k


# ── coordination chemistry ───────────────────────────────────────────────────
GROUP = {"Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zn": 12, "Ru": 8, "Rh": 9, "Pd": 10, "Ag": 11,
         "Pt": 10, "Mo": 6, "W": 6, "Ir": 9, "Os": 8, "Au": 11}
LIG = {"CN": -1, "Cl": -1, "F": -1, "Br": -1, "I": -1, "OH": -1, "NO2": -1, "SCN": -1, "acac": -1, "ox": -2, "H2O": 0, "NH3": 0, "en": 0,
       "CO": 0, "py": 0, "PPh3": 0, "bpy": 0}


def d_count(M, ligs, q):
    """ligs written 'CN:6' or 'NH3:4,Cl:2'"""
    tot = 0
    for part in str(ligs).split(","):
        name, n = part.split(":")
        tot += LIG[name] * int(n)
    ox = int(q) - tot
    return GROUP[M] - ox


def _fill(d, geom, spin):
    """occupation of the lower and upper sets after filling d electrons"""
    lo_n, hi_n = (3, 2) if geom == "oct" else (2, 3)
    lo, hi = [0] * lo_n, [0] * hi_n
    order = []
    if spin == "high":
        order = [("lo", i) for i in range(lo_n)] + [("hi", i) for i in range(hi_n)]
        order = order + order
    else:
        order = [("lo", i) for i in range(lo_n)] * 2 + [("hi", i) for i in range(hi_n)] * 2
    for k in range(d):
        s, i = order[k]
        (lo if s == "lo" else hi)[i] += 1
    return lo, hi


def unpaired(d, geom="oct", spin="high"):
    lo, hi = _fill(int(d), str(geom), str(spin))
    return sum(1 for x in lo + hi if x == 1)


def spin_only(d, geom="oct", spin="high"):
    n = unpaired(d, geom, spin)
    return sp.sqrt(n * (n + 2))


def cfse(d, geom="oct", spin="high"):
    """in units of the splitting of that geometry; pairing energy left out"""
    lo, hi = _fill(int(d), str(geom), str(spin))
    if geom == "oct":
        return -sp.Rational(2, 5) * sum(lo) + sp.Rational(3, 5) * sum(hi)
    return -sp.Rational(3, 5) * sum(lo) + sp.Rational(2, 5) * sum(hi)


def _rotations(planar):
    mats = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for r, c in enumerate(perm):
                m[r][c] = signs[r]
            if round(sp.Matrix(m).det()) != 1:
                continue
            if planar and perm[2] != 2:
                continue
            mats.append(m)
    return mats


def stereoisomers(mono, chelates="", geom="oct"):
    """count stereoisomers (enantiomers counted separately) of an octahedral or square-planar complex.
    mono: 'A4B2' style counts of monodentate ligands; chelates: number of symmetric AA chelates."""
    planar = geom == "sq"
    pos = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)] + ([] if planar else [(0, 0, 1), (0, 0, -1)])
    rots = _rotations(planar)
    idx = {p: i for i, p in enumerate(pos)}
    perms = []
    for m in rots:
        perms.append([idx[tuple(sum(m[r][c] * p[c] for c in range(3)) for r in range(3))] for p in pos])
    labels = []
    for el, n in re.findall(r"([A-Z])(\d*)", str(mono)):
        labels += [el] * int(n or 1)
    nch = int(chelates or 0)
    cis = [(i, j) for i in range(len(pos)) for j in range(i + 1, len(pos)) if sum(a * b for a, b in zip(pos[i], pos[j])) == 0]
    seen = set()
    count = 0
    for edges in itertools.combinations(cis, nch):
        used = [x for e in edges for x in e]
        if len(set(used)) != len(used):
            continue
        free = [i for i in range(len(pos)) if i not in used]
        if len(free) != len(labels):
            continue
        for arr in set(itertools.permutations(labels)):
            lab = {free[k]: arr[k] for k in range(len(free))}
            def enc(p):
                ed = frozenset(frozenset((p[a], p[b])) for a, b in edges)
                return (ed, tuple(sorted((p[i], lab[i]) for i in free)))
            forms = {enc(p) for p in perms}
            key = min(forms, key=lambda f: (sorted(tuple(sorted(e)) for e in f[0]), f[1]))
            if key not in seen:
                seen.add(key)
                count += 1
    return sp.Integer(count)


# ── solids ───────────────────────────────────────────────────────────────────
F = sp.Rational
CELLS = {
    "sc": {"X": [(0, 0, 0)]},
    "bcc": {"X": [(0, 0, 0), (F(1, 2),) * 3]},
    "fcc": {"X": [(0, 0, 0), (F(1, 2), F(1, 2), 0), (F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2))]},
    "diamond": {"X": [(0, 0, 0), (F(1, 2), F(1, 2), 0), (F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2)),
                      (F(1, 4),) * 3, (F(3, 4), F(3, 4), F(1, 4)), (F(3, 4), F(1, 4), F(3, 4)), (F(1, 4), F(3, 4), F(3, 4))]},
    "NaCl": {"A": [(0, 0, 0), (F(1, 2), F(1, 2), 0), (F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2))],
             "B": [(F(1, 2), 0, 0), (0, F(1, 2), 0), (0, 0, F(1, 2)), (F(1, 2),) * 3]},
    "CsCl": {"A": [(F(1, 2),) * 3], "B": [(0, 0, 0)]},
    "ZnS": {"A": [(F(1, 4),) * 3, (F(3, 4), F(3, 4), F(1, 4)), (F(3, 4), F(1, 4), F(3, 4)), (F(1, 4), F(3, 4), F(3, 4))],
            "B": [(0, 0, 0), (F(1, 2), F(1, 2), 0), (F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2))]},
    "CaF2": {"A": [(0, 0, 0), (F(1, 2), F(1, 2), 0), (F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2))],
             "B": [tuple(F(a, 4) for a in t) for t in itertools.product((1, 3), repeat=3)]},
}


def cell_count(s, sp_="X"):
    return sp.Integer(len({tuple(c % 1 for c in p) for p in CELLS[str(s)][str(sp_)]}))


def _images(s, sp_):
    return [tuple(c + d for c, d in zip(p, sh)) for p in CELLS[s][sp_] for sh in itertools.product((-1, 0, 1), repeat=3)]


def coordination(s, centre="X", around=None):
    """nearest neighbours of the first `centre` atom among `around` atoms (same species if not given)"""
    s, centre = str(s), str(centre)
    around = str(around) if around else centre
    c0 = CELLS[s][centre][0]
    ds = []
    for p in _images(s, around):
        d2 = sum((a - b) ** 2 for a, b in zip(p, c0))
        if d2 > 0:
            ds.append(d2)
    m = min(ds)
    return sp.Integer(sum(1 for d in ds if d == m))


def packing(s):
    s = str(s)
    c0 = CELLS[s]["X"][0]
    m = min(sum((a - b) ** 2 for a, b in zip(p, c0)) for p in _images(s, "X") if p != c0)
    r = sp.sqrt(m) / 2
    return sp.nsimplify(cell_count(s) * sp.Rational(4, 3) * sp.pi * r**3)


def density(s, formula, a_pm):
    """g/cm³ from structure, formula unit and cubic edge in pm; formula units per cell counted from the cation positions"""
    s = str(s)
    z = cell_count(s, "X" if "X" in CELLS[s] else "A")
    NA = sp.Rational("6.02214076e23")
    return z * sp.nsimplify(molar_mass(formula)) / (NA * (sp.nsimplify(a_pm) * sp.Rational(1, 10**10)) ** 3)


def bragg(w, a_pm=0, h=0, k=0, l=0, lam=0, theta=0, n=1):
    """w 0: angle θ (degrees) for a cubic cell; w 1: spacing d (pm) from λ and θ"""
    x = sp.Symbol("x", positive=True)
    if int(w) == 0:
        d = sp.nsimplify(a_pm) / sp.sqrt(int(h) ** 2 + int(k) ** 2 + int(l) ** 2)
        sol = sp.nsolve(int(n) * sp.nsimplify(lam) - 2 * d * sp.sin(x * sp.pi / 180), x, 20)
        return sol
    return sp.solve(sp.Eq(int(n) * sp.nsimplify(lam), 2 * x * sp.sin(sp.nsimplify(theta) * sp.pi / 180)), x)[0]


def radius_ratio_cn(r):
    """option index (0 tetrahedral, 1 octahedral, 2 cubic) from the ratios at which the anions just touch"""
    o, c = sp.sqrt(2) - 1, sp.sqrt(3) - 1
    r = sp.nsimplify(r)
    return 0 if r < o else (1 if r < c else 2)


# ── facts, typed a second time ───────────────────────────────────────────────
FACTS = {
    "flame": {"Li": "crimson", "Na": "yellow-orange", "K": "lilac", "Ca": "orange-red", "Sr": "crimson", "Ba": "apple green", "Cu": "blue-green", "Cs": "blue-violet"},
    "burn": {"Li": "Li2O", "Na": "Na2O2", "K": "KO2", "Rb": "RbO2", "Mg": "MgO", "Ca": "CaO"},
    "oxide": {"Na2O": "basic", "MgO": "basic", "CaO": "basic", "Al2O3": "amphoteric", "ZnO": "amphoteric", "BeO": "amphoteric", "SiO2": "acidic",
              "P4O10": "acidic", "SO3": "acidic", "Cl2O7": "acidic", "CO2": "acidic", "CO": "neutral", "NO": "neutral", "N2O": "neutral", "CrO3": "acidic"},
    "colour": {"[Cu(H2O)6]2+": "pale blue", "[Cu(NH3)4(H2O)2]2+": "deep blue", "[CuCl4]2-": "yellow-green", "[Co(H2O)6]2+": "pink",
               "[CoCl4]2-": "blue", "[Ni(H2O)6]2+": "green", "[Fe(H2O)6]2+": "pale green", "MnO4-": "purple", "Cr2O7 2-": "orange",
               "CrO4 2-": "yellow", "[Zn(H2O)6]2+": "colourless", "[Fe(SCN)(H2O)5]2+": "blood red"},
    "ppt": {"AgCl": "white", "AgBr": "cream", "AgI": "yellow", "PbI2": "bright yellow", "BaSO4": "white", "Cu(OH)2": "pale blue",
            "Fe(OH)3": "red-brown", "Fe(OH)2": "dirty green", "Ni(OH)2": "green", "PbS": "black", "ZnS": "white", "Ag2CrO4": "brick red", "CdS": "yellow"},
    "amph": {"Al": 1, "Zn": 1, "Pb": 1, "Sn": 1, "Cr": 1, "Be": 1, "Fe": 0, "Mg": 0, "Cu": 0, "Ni": 0, "Mn": 0, "Ca": 0},
    "test": {"NH4+": "warm with NaOH: gas turns damp red litmus blue", "SO4 2-": "acidified BaCl2: white precipitate",
             "Cl-": "acidified AgNO3: white precipitate, dissolves in dilute NH3", "CO3 2-": "dilute acid: gas turns limewater milky",
             "Fe3+": "KSCN: blood-red solution", "Fe2+": "K3[Fe(CN)6]: dark blue precipitate", "I-": "acidified AgNO3: yellow precipitate, insoluble in conc. NH3",
             "NO3-": "Devarda's alloy and NaOH: ammonia given off"},
    "field": ["I-", "Br-", "Cl-", "F-", "OH-", "H2O", "NH3", "en", "NO2-", "CN-", "CO"],
    "instrument": {"trace lead in drinking water": "ICP-MS", "residual solvents in a drug": "GC", "a non-volatile drug and its impurities": "HPLC",
                   "water content of an oil": "Karl Fischer titration", "functional groups of an unknown": "IR spectroscopy",
                   "connectivity of an organic unknown": "NMR spectroscopy", "molar mass of a protein": "mass spectrometry",
                   "sodium in serum": "atomic emission (flame photometry)"},
}


def fact_pick(table, key, o1, o2, o3, o4):
    """index of the option that matches this table's own entry"""
    want = FACTS[str(table)][str(key)]
    opts = [str(o) for o in (o1, o2, o3, o4)]
    hits = [i for i, o in enumerate(opts) if o == str(want)]
    assert len(hits) == 1, (key, want, opts)
    return hits[0]


def fact_lit(table, key, options):
    """index of this table's entry in a literal option list written 'a|b|c'"""
    return str(options).split("|").index(FACTS[str(table)][str(key)])


def amph_pick(o1, o2, o3, o4):
    hits = [i for i, o in enumerate((o1, o2, o3, o4)) if FACTS["amph"][str(o)] == 1]
    assert len(hits) == 1
    return hits[0]


def field_pick(o1, o2, o3, o4):
    ranks = [FACTS["field"].index(str(o)) for o in (o1, o2, o3, o4)]
    return ranks.index(max(ranks))


# ── analytical ───────────────────────────────────────────────────────────────
def to_reduced(f, q, el, f_end, q_end, n_end=1):
    """electrons one formula unit gains on the way to its final reduced form (for back-counting titrations)"""
    k = atoms(f)[el]
    return (ox_state(f, q, el) - ox_state(f_end, q_end, el)) * k


def mass_percent_from_ppt(analyte, ppt, el, m_ppt, m_sample):
    """gravimetry by element balance: atoms of `el` in the precipitate become analyte units"""
    n_el = sp.nsimplify(m_ppt) / sp.nsimplify(molar_mass(ppt)) * atoms(ppt)[el]
    n_an = n_el / atoms(analyte)[el]
    return 100 * n_an * sp.nsimplify(molar_mass(analyte)) / sp.nsimplify(m_sample)


def ksp_common(Ksp, c, nu_common=1):
    """solubility s of an MX salt in c M of the common ion, from the full equation s(s + c) = Ksp"""
    s = sp.Symbol("s", positive=True)
    sols = sp.solve(s * (s + sp.nsimplify(c)) - sp.nsimplify(Ksp), s)
    return sols[0]


def complex_solubility(Ksp, Kf, L0):
    """AgX in ligand L (Ag(L)2+): solve the mass and charge balances numerically"""
    Ag, X, L, AgL2 = sp.symbols("Ag X L AgL2", positive=True)
    Ksp, Kf, L0 = map(sp.nsimplify, (Ksp, Kf, L0))
    eqs = [Ag * X - Ksp, AgL2 - Kf * Ag * L**2, L + 2 * AgL2 - L0, Ag + AgL2 - X]
    guess = [float(Ksp) ** 0.5 / 10, float((Ksp * Kf) ** sp.Rational(1, 2) * L0), float(L0) * 0.9, float((Ksp * Kf) ** sp.Rational(1, 2) * L0)]
    sol = sp.nsolve(eqs, [Ag, X, L, AgL2], guess, prec=30)
    return sol[1]


def weak_acid_ph(Ca, Va, Ka, Cb, Vb):
    """pH from the full charge balance of HA titrated with NaOH (nsolve in log[H+])"""
    y = sp.Symbol("y")
    Ca, Va, Ka, Cb, Vb = map(sp.nsimplify, (Ca, Va, Ka, Cb, Vb))
    V = Va + Vb
    cA, cNa = Ca * Va / V, Cb * Vb / V
    h = 10**(-y)
    Kw = sp.Rational(1, 10**14)
    f = h + cNa - cA * Ka / (Ka + h) - Kw / h
    lo, hi = 0.0, 14.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if float(f.subs(y, mid)) > 0:
            lo = mid
        else:
            hi = mid
    return sp.nsolve(f, y, (lo + hi) / 2, prec=30)


def indicator_pick(Ca, Va, Ka, Cb, Vb_eq):
    """which literal option (methyl orange 3.1-4.4, methyl red 4.4-6.2, bromothymol blue 6.0-7.6, phenolphthalein 8.2-10) contains the equivalence pH"""
    ph = float(weak_acid_ph(Ca, Va, Ka, Cb, Vb_eq)) if float(sp.nsimplify(Ka)) < 1 else 7.0
    ranges = [(3.1, 4.4), (4.4, 6.2), (6.0, 7.6), (8.2, 10.0)]
    hits = [i for i, (a, b) in enumerate(ranges) if a <= ph <= b]
    return hits[-1]


def extraction_left(Vaq, Vorg, D, n):
    """fraction left in water after n extractions, one at a time"""
    q = sp.Integer(1)
    for _ in range(int(n)):
        q = q * sp.nsimplify(Vaq) / (sp.nsimplify(Vaq) + sp.nsimplify(D) * sp.nsimplify(Vorg))
    return q


def two_component(e1x, e1y, e2x, e2y, A1, A2, w):
    cx, cy = sp.symbols("cx cy")
    s = sp.solve([sp.nsimplify(e1x) * cx + sp.nsimplify(e1y) * cy - sp.nsimplify(A1), sp.nsimplify(e2x) * cx + sp.nsimplify(e2y) * cy - sp.nsimplify(A2)], [cx, cy])
    return [s[cx], s[cy]][int(w)]


def std_addition(Ax, Vx, cs, Vs, Asp, Vtot):
    """unknown concentration from one standard addition: both signals proportional to concentration in the flask"""
    c = sp.Symbol("c", positive=True)
    k = sp.Symbol("k", positive=True)
    s = sp.solve([sp.nsimplify(Ax) - k * c * sp.nsimplify(Vx) / sp.nsimplify(Vtot),
                  sp.nsimplify(Asp) - k * (c * sp.nsimplify(Vx) + sp.nsimplify(cs) * sp.nsimplify(Vs)) / sp.nsimplify(Vtot)], [c, k], dict=True)[0]
    return s[c]


def calib_unknown(xs, ys, y0):
    """least squares by the normal equations as a matrix solve, then read the unknown off the line"""
    X = sp.Matrix([[1, sp.nsimplify(x)] for x in xs])
    Y = sp.Matrix([sp.nsimplify(y) for y in ys])
    b = (X.T * X).LUsolve(X.T * Y)
    return (sp.nsimplify(y0) - b[0]) / b[1]


QCRIT = {3: 0.970, 4: 0.829, 5: 0.710, 6: 0.625, 7: 0.568}


def q_test(vals):
    """1 = reject the suspect value (95%), 0 = keep"""
    v = sorted(float(x) for x in vals)
    gap = max(v[1] - v[0], v[-1] - v[-2])
    return 1 if gap / (v[-1] - v[0]) > QCRIT[len(v)] else 0


def rel_unc(kind, a, sa, b, sb):
    """uncertainty of a·b, a/b (relative, as a fraction) or a+b (absolute) by the general derivative formula"""
    x, y = sp.symbols("x y", positive=True)
    f = {"prod": x * y, "quot": x / y, "sum": x + y}[str(kind)]
    vals = {x: sp.nsimplify(a), y: sp.nsimplify(b)}
    s = sp.sqrt((sp.diff(f, x) * sp.nsimplify(sa)) ** 2 + (sp.diff(f, y) * sp.nsimplify(sb)) ** 2).subs(vals)
    return s if str(kind) == "sum" else s / f.subs(vals)


FUNCS = {f.__name__: f for f in [ox_state, disprop_ratio, half_electrons, d_count, unpaired, spin_only, cfse, stereoisomers,
                                 cell_count, coordination, packing, density, bragg, radius_ratio_cn, fact_pick, fact_lit, amph_pick, field_pick,
                                 to_reduced, mass_percent_from_ppt, ksp_common, complex_solubility, weak_acid_ph, indicator_pick, extraction_left,
                                 two_component, std_addition, calib_unknown, q_test, rel_unc]}
FUNCS["in_mass"] = molar_mass
