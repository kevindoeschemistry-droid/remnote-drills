"""Descriptive inorganic chemistry after Cotton & Wilkinson (framework inorganic-advanced).

Rule-based where a rule exists, each written here independently of scripts/cw_cases.py:
VSEPR shapes from valence-electron counting, diatomic bond orders and unpaired electrons from
filling a molecular-orbital ladder, Wade's rules from skeletal electron pairs, silicate O:Si from
shared corners, Latimer combinations through free energies, isotope frequency ratios from reduced
masses, fullerene rings from Euler's formula, 18-electron counts by the neutral-ligand method.
Facts with no rule are looked up in CW_FACTS, a table typed separately from the generator's.
"""
import sympy as sp

VALENCE = {"H": 1, "Li": 1, "Na": 1, "K": 1, "Be": 2, "Mg": 2, "B": 3, "Al": 3, "Ga": 3, "C": 4, "Si": 4, "Ge": 4,
           "Sn": 4, "Pb": 4, "N": 5, "P": 5, "As": 5, "Sb": 5, "O": 6, "S": 6, "Se": 6, "Te": 6, "F": 7, "Cl": 7,
           "Br": 7, "I": 7, "Xe": 8, "Kr": 8}
SHAPES = {(2, 0): "linear", (3, 0): "trigonal planar", (3, 1): "bent", (4, 0): "tetrahedral",
          (4, 1): "trigonal pyramidal", (4, 2): "bent", (5, 0): "trigonal bipyramidal", (5, 1): "seesaw",
          (5, 2): "T-shaped", (5, 3): "linear", (6, 0): "octahedral", (6, 1): "square pyramidal",
          (6, 2): "square planar", (7, 0): "pentagonal bipyramidal", (7, 1): "distorted octahedral"}


def check(p, H):
    return None


def _ligands(lig):
    """'F4' -> [('F', 4)], 'O2F2' -> [('O', 2), ('F', 2)]"""
    out, i = [], 0
    s = str(lig)
    while i < len(s):
        j = i + 1
        while j < len(s) and s[j].islower():
            j += 1
        el = s[i:j]
        k = j
        while k < len(s) and s[k].isdigit():
            k += 1
        out.append((el, int(s[j:k] or 1)))
        i = k
    return out


def cw_shape(centre, lig, q):
    """terminal O or S takes two of the centre's electrons (a double bond), everything else one"""
    ligs = _ligands(lig)
    n = sum(c for _, c in ligs)
    used = sum(c * (2 if el in ("O", "S") else 1) for el, c in ligs)
    lone = (VALENCE[str(centre)] - int(q) - used) // 2
    return SHAPES[(n + lone, lone)]


def cw_shape_pick(centre, lig, q, o1, o2, o3, o4):
    s = cw_shape(centre, lig, q)
    return sp.Integer([str(o) for o in (o1, o2, o3, o4)].index(s))


# σ2s σ*2s, then the 2p set in one of two orders
_LOW = [("s", 2, 1), ("s*", 2, -1), ("pi", 4, 1), ("sp", 2, 1), ("pi*", 4, -1), ("sp*", 2, -1)]   # B2, C2, N2
_HIGH = [("s", 2, 1), ("s*", 2, -1), ("sp", 2, 1), ("pi", 4, 1), ("pi*", 4, -1), ("sp*", 2, -1)]  # O2, F2, Ne2


def _mo(a, b, q):
    n = VALENCE[str(a)] + VALENCE[str(b)] - int(q)
    ladder = _LOW if n <= 10 else _HIGH
    bonding = anti = unpaired = 0
    for _, cap, sign in ladder:
        k = min(cap, n)
        n -= k
        if sign > 0:
            bonding += k
        else:
            anti += k
        if cap == 4:
            unpaired += k if k <= 2 else 4 - k   # Hund: two degenerate orbitals
        elif k == 1:
            unpaired += 1
    return sp.Rational(bonding - anti, 2), sp.Integer(unpaired)


def cw_bond_order(a, b, q):
    return _mo(a, b, q)[0]


def cw_unpaired_mo(a, b, q):
    return _mo(a, b, q)[1]


def cw_wade(nB, nH, q):
    """skeletal electron pairs = (3 per B + 1 per H − 2 per exo B–H − charge) / 2; closo n+1, nido n+2, arachno n+3"""
    pairs = sp.Rational(3 * int(nB) + int(nH) - 2 * int(nB) - int(q), 2)
    return sp.Integer(pairs - int(nB) - 1)


def cw_silicate_ratio(shared):
    """each SiO4 tetrahedron keeps its unshared O and half of every shared corner"""
    s = sp.Rational(shared)
    return (4 - s) + s / 2


def cw_latimer(n1, e1, n2, e2):
    """ΔG adds, potentials do not: E = (n1E1 + n2E2)/(n1 + n2) from −nFE"""
    F = sp.Symbol("F")
    dG = -int(n1) * F * sp.nsimplify(e1) - int(n2) * F * sp.nsimplify(e2)
    return sp.simplify(dG / (-(int(n1) + int(n2)) * F))


def cw_isotope_ratio(m1, m2, mX):
    """ν ∝ 1/√μ for the X–H and X–D stretch: ν_D/ν_H = √(μ_H/μ_D)"""
    m1, m2, mX = (sp.nsimplify(v) for v in (m1, m2, mX))
    mu = lambda m: m * mX / (m + mX)
    return sp.sqrt(mu(m1) / mu(m2))


def cw_fullerene_hex(n):
    """V − E + F = 2 with E = 3V/2 and only pentagons and hexagons, 12 of them pentagons"""
    V = int(n)
    E = sp.Rational(3 * V, 2)
    F = 2 - V + E
    return F - 12


CW_FACTS = {
    # hard and soft acids and bases
    "hsab:Fe3+": "Hard", "hsab:Al3+": "Hard", "hsab:Hg2+": "Soft", "hsab:Ag+": "Soft", "hsab:Cu2+": "Borderline",
    "hsab:F-": "Hard", "hsab:I-": "Soft", "hsab:Pt2+": "Soft", "hsab:Mg2+": "Hard",
    # hydrides
    "hydride:NaH": "Ionic (saline)", "hydride:CaH2": "Ionic (saline)", "hydride:CH4": "Covalent (molecular)",
    "hydride:NH3": "Covalent (molecular)", "hydride:PdH0.6": "Metallic (interstitial)", "hydride:TiH2": "Metallic (interstitial)",
    # alkali metals burning in air
    "burn:Li": "Li₂O", "burn:Na": "Na₂O₂", "burn:K": "KO₂", "burn:Rb": "RbO₂", "burn:Cs": "CsO₂",
    # carbonate decomposition, highest temperature
    "carb:Mg,Ca,Ba": "BaCO₃", "carb:Be,Mg,Sr": "SrCO₃", "carb:Ca,Sr,Ba": "BaCO₃",
    # boron trihalide Lewis acidity, strongest
    "bx3": "BBr₃",
    # more stable oxidation state, heaviest element of the group (inert pair)
    "inert:Tl": "+1", "inert:Pb": "+2", "inert:Bi": "+3", "inert:Sn": "+4",
    # carbides
    "carbide:CaC2": "Ionic (acetylide)", "carbide:Al4C3": "Ionic (methanide)", "carbide:SiC": "Covalent",
    "carbide:WC": "Interstitial",
    # oxoacid basicity (ionisable H)
    "basic:H3PO2": "1", "basic:H3PO3": "2", "basic:H3PO4": "3", "basic:H4P2O7": "4",
    # chlorine oxoacid strength, strongest
    "oxo:Cl": "HClO₄",
    # group 12
    "hg1": "Hg₂²⁺, with an Hg–Hg bond", "zno": "Amphoteric", "d10colour": "Colourless: a full d shell has no d–d transitions",
    # noble-gas fluorides made first or most easily
    "xe:first": "Xe",
    # diagonal relationship
    "diag:Li": "Mg", "diag:Be": "Al", "diag:B": "Si",
}


def cw_fact_pick(key, o1, o2, o3, o4):
    ans = CW_FACTS[str(key)]
    return sp.Integer([str(o) for o in (o1, o2, o3, o4)].index(ans))


FUNCS = {f.__name__: f for f in [cw_shape_pick, cw_bond_order, cw_unpaired_mo, cw_wade, cw_silicate_ratio, cw_latimer,
                                 cw_isotope_ratio, cw_fullerene_hex, cw_fact_pick]}

# ── transition elements, f block and organometallics ─────────────────────────
GROUP_TM = {"Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zr": 4, "Mo": 6, "W": 6, "Re": 7,
            "Ru": 8, "Os": 8, "Rh": 9, "Ir": 9, "Pd": 10, "Pt": 10, "Ta": 5, "Nb": 5, "Hf": 4}
DONATE = {"CO": 2, "PR3": 2, "PPh3": 2, "NH3": 2, "H2O": 2, "Cl": 1, "Br": 1, "I": 1, "H": 1, "CH3": 1, "Cp": 5,
          "C6H6": 6, "C2H4": 2, "NO": 3, "allyl": 3, "COD": 4, "CHR": 2, "Ph": 1, "acyl": 1}


def cw_electron_count(M, ligs, q):
    """neutral (covalent) method: group number + electrons each ligand brings as a neutral fragment − charge"""
    tot = GROUP_TM[str(M)]
    for part in str(ligs).split(","):
        name, n = part.split(":")
        tot += DONATE[name] * int(n)
    return sp.Integer(tot - int(q))


def cw_mm_bond(d1, d2):
    """σ, π, π, δ, δ*, π*, π*, σ* filled in order by the metals' d electrons; bonding minus antibonding over 2"""
    n = int(d1) + int(d2)
    b = a = 0
    for sign in (1, 1, 1, 1, -1, -1, -1, -1):
        k = min(2, n)
        n -= k
        if sign > 0:
            b += k
        else:
            a += k
    return sp.Rational(b - a, 2)


def _hund_f(n):
    """S, L, J of f^n by Hund's rules"""
    ml = [3, 2, 1, 0, -1, -2, -3]
    up = min(n, 7)
    down = n - up
    S = sp.Rational(up - down, 2)
    L = abs(sum(ml[:up]) + sum(ml[:down]))
    J = abs(L - S) if n < 7 else L + S
    return S, sp.Integer(L), J


def cw_ln_moment(n):
    """μ_eff = g_J √(J(J+1)) in Bohr magnetons for a free Ln³⁺ ion of configuration f^n"""
    S, L, J = _hund_f(int(n))
    g = 1 + (J * (J + 1) + S * (S + 1) - L * (L + 1)) / (2 * J * (J + 1))
    return g * sp.sqrt(J * (J + 1))


def cw_f_count(Z, q, series):
    """electrons beyond the noble-gas core minus the charge, all in f for these ions: Ln (core Xe, 54, plus 5d¹6s² → 4f = Z−54−3 for Ln³⁺)"""
    core = 54 if str(series) == "Ln" else 86
    return sp.Integer(int(Z) - core - int(q))


def cw_inert(d, spin):
    """Taube: octahedral d³ and low-spin d⁶ are substitution-inert (big LFSE loss on the way to a 5- or 7-coordinate state)"""
    d = int(d)
    return sp.Integer(0 if d == 3 or (d == 6 and str(spin) == "low") or (d in (4, 5) and str(spin) == "low") else 1)


def cw_jahn_teller(d, spin):
    """strong distortion when the e_g pair is unevenly filled"""
    d = int(d)
    t2g = min(d, 6) if str(spin) == "low" else min(d, 3) + max(0, min(d - 5, 3))
    eg = d - t2g
    return sp.Integer(0 if eg % 2 == 1 else 1)


CW_FACTS.update({
    "spectro:strongest:I,Cl,H2O,NH3,CN": "CN⁻", "spectro:strongest:F,OH,en,CO": "CO", "spectro:weakest:I,F,NH3,CN": "I⁻",
    "mn:acid": "Mn²⁺", "mn:neutral": "MnO₂", "mn:base": "MnO₄²⁻",
    "cr:acid": "Orange Cr₂O₇²⁻", "cr:base": "Yellow CrO₄²⁻",
    "radii:Zr,Hf": "Almost the same (lanthanide contraction)", "spin:4d5d": "Low spin",
    "trans:cisplatin": "Start from PtCl₄²⁻ and add NH₃: Cl⁻ trans-directs the second NH₃ cis",
    "ln:Ce": "+4", "ln:Eu": "+2", "ln:Yb": "+2", "ln:Tb": "+4", "ln:Sm": "+2",
    "an:U": "+6", "an:Np": "+7", "an:Th": "+4", "an:Am": "+3",
    "step:addH2": "Oxidative addition", "step:loseHH": "Reductive elimination", "step:COins": "Migratory insertion (1,1)",
    "step:betaH": "β-Hydride elimination", "step:olefinins": "Migratory insertion (1,2)",
    "cat:monsanto": "Rh with iodide (methanol carbonylation to acetic acid)", "cat:wacker": "Pd(II) with Cu(II) (ethene to acetaldehyde)",
    "cat:ziegler": "TiCl₄ with AlEt₃ (alkene polymerisation)", "cat:wilkinson": "RhCl(PPh₃)₃ (alkene hydrogenation)",
    "cat:hydroform": "Co or Rh carbonyls (alkene + CO + H₂ to aldehyde)", "cat:metathesis": "Ru or Mo alkylidenes (Grubbs, Schrock)",
    "betaH:need": "A vacant site cis to the alkyl and a β hydrogen",
})

FUNCS.update({f.__name__: f for f in [cw_electron_count, cw_mm_bond, cw_ln_moment, cw_f_count, cw_inert, cw_jahn_teller]})
