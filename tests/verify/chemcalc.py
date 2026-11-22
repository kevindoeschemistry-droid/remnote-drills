"""General chemistry checks for the second-type cards (ac-second-types.yaml): a formula parser with its
own atomic weights (IUPAC conventional values), electronegativities (Pauling), and VSEPR counts for
AXn molecules with single-bonded terminal atoms. Kept apart from the numbers the templates print.
"""
import re

import sympy as sp

W = {"H": "1.008", "He": "4.0026", "Li": "6.94", "Be": "9.0122", "B": "10.81", "C": "12.011", "N": "14.007", "O": "15.999",
     "F": "18.998", "Ne": "20.180", "Na": "22.990", "Mg": "24.305", "Al": "26.982", "Si": "28.085", "P": "30.974",
     "S": "32.06", "Cl": "35.45", "Ar": "39.95", "K": "39.098", "Ca": "40.078", "Cr": "51.996", "Mn": "54.938",
     "Fe": "55.845", "Co": "58.933", "Ni": "58.693", "Cu": "63.546", "Zn": "65.38", "Br": "79.904", "Sr": "87.62",
     "Ag": "107.87", "Sn": "118.71", "I": "126.90", "Xe": "131.29", "Ba": "137.33", "Pb": "207.2"}
W = {k: sp.Rational(v) for k, v in W.items()}
Z = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10, "Na": 11, "Mg": 12, "Al": 13,
     "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "I": 53, "Xe": 54}
VALENCE = {"H": 1, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Si": 4, "P": 5, "S": 6, "Cl": 7, "Br": 7, "I": 7, "Xe": 8, "Be": 2}
EN = {"H": 2.20, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98, "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90, "P": 2.19,
      "S": 2.58, "Cl": 3.16, "K": 0.82, "Ca": 1.00, "Br": 2.96, "I": 2.66, "Li": 0.98, "Cs": 0.79}


def _parse(tokens, i):
    """parse until ')' or the end; returns (counts, next index)"""
    out = {}
    while i < len(tokens) and tokens[i] != ")":
        tok = tokens[i]
        if tok == "(":
            grp, i = _parse(tokens, i + 1)
            i += 1  # the ')'
        else:
            grp, i = {tok: 1}, i + 1
        n = 1
        if i < len(tokens) and tokens[i].isdigit():
            n, i = int(tokens[i]), i + 1
        for k, v in grp.items():
            out[k] = out.get(k, 0) + v * n
    return out, i


def counts(formula):
    """atom counts of a formula with parentheses and hydrate dots, e.g. Al2(SO4)3 or CuSO4.5H2O"""
    total = {}
    for part in formula.split("."):
        m = re.match(r"^(\d+)(.*)$", part)
        mult, part = (int(m.group(1)), m.group(2)) if m else (1, part)
        got, _ = _parse(re.findall(r"[A-Z][a-z]?|\(|\)|\d+", part), 0)
        for k, v in got.items():
            total[k] = total.get(k, 0) + v * mult
    return total


def molar_mass(formula):
    return sum(W[k] * n for k, n in counts(formula).items())


def atoms_per_unit(formula):
    return sum(counts(formula).values())


def mass_pct(formula, el):
    return W[el] * counts(formula)[el] / molar_mass(formula) * 100


def argmax(xs):
    vals = [sp.N(v) for v in xs]
    return vals.index(max(vals))


def argmin(xs):
    vals = [sp.N(v) for v in xs]
    return vals.index(min(vals))


def most_atoms(formulas, grams):
    """index of the sample with the most atoms, grams of each given"""
    return argmax([g / molar_mass(f) * atoms_per_unit(f) for f, g in zip(formulas, grams)])


def closest_metal(rest_mass, options):
    """which of the options has an atomic weight closest to rest_mass"""
    return argmin([abs(W[o] - sp.nsimplify(rest_mass)) for o in options])


def electrons(sym, charge):
    return Z[sym] - charge


def iso_pick(target_sym, target_q, syms, qs):
    want = electrons(target_sym, target_q)
    hits = [i for i, (s, q) in enumerate(zip(syms, qs)) if electrons(s, q) == want]
    assert len(hits) == 1, hits
    return hits[0]


def most_polar(pairs):
    """pairs like 'H-F'; index of the largest electronegativity difference"""
    return argmax([abs(sp.nsimplify(EN[a]) - sp.nsimplify(EN[b])) for a, b in (p.split("-") for p in pairs)])


def lone_pairs(central, n_terminal, charge):
    """lone pairs on the central atom of AXn, every X single-bonded and taking one electron (H or a halogen)"""
    return sp.Rational(VALENCE[central] - n_terminal - charge, 2)


def hybrid(central, n_terminal, charge):
    """0 sp, 1 sp2, 2 sp3, 3 sp3d, 4 sp3d2 from the steric number"""
    return int(n_terminal + lone_pairs(central, n_terminal, charge)) - 2


def empirical_sub(formula, el):
    """subscript of el in the empirical formula: divide every count by their gcd"""
    c = counts(formula)
    return c[el] // sp.igcd(*c.values())


def formal_charge(sym, nonbonding, bonds):
    return VALENCE[sym] - nonbonding - bonds


FUNCS = {f.__name__: f for f in [empirical_sub, formal_charge, counts, molar_mass, atoms_per_unit, mass_pct, argmax, argmin, most_atoms, closest_metal,
                                 electrons, iso_pick, most_polar, lone_pairs, hybrid]}
