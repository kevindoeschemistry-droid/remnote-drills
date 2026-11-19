"""Skeletal structures (figures of `type: molecule`): the drawing must be the molecule it claims.

A structure is stored as atoms and bonds. Here the molecular formula is rebuilt from that graph
alone (a carbon vertex takes 4 minus its bond orders in hydrogens; a labelled atom carries the
hydrogens its label shows) and compared with the `formula` the item states. Each labelled atom's
valence is checked too, so a missing bond or a wrong label is caught. Nothing here uses the tool
that laid the structure out (scripts/mol.py).

This cannot tell isomers apart (leucine and isoleucine share a formula): connectivity is checked
by eye against the basis, IUPAC-IUB 1983 Table 1.
"""
import json
import re
from collections import Counter
from pathlib import Path

_GEN = Path(__file__).resolve().parents[2] / "src/drills/skills.generated.json"
# allowed total bond orders (hydrogens included) for a neutral atom
VALENCE = {"H": {1}, "C": {4}, "N": {3}, "O": {2}, "S": {2, 4, 6}, "P": {3, 5}, "F": {1}, "Cl": {1}, "Br": {1}, "I": {1}, "Fe": None, "R": {1}, "Si": {4}}  # a metal centre takes whatever is drawn to it


def read_label(lab):
    """'H2N' / 'NH2' / 'OH' / 'O' / 'N+' / 'O-' -> (element, hydrogens, charge)"""
    m = re.fullmatch(r"(?:H(\d*))?(Cl|Br|Fe|Si|[HCNOSPFIR])(?:H(\d*))?([+-]?)", lab)
    if not m:
        raise ValueError(f"label {lab!r}")
    h = sum(int(g or 1) for g in (m.group(1), m.group(3)) if g is not None)
    return m.group(2), h, {"+": 1, "-": -1, "": 0}[m.group(4)]


def hill(counts):
    order = (["C", "H"] if counts.get("C") else []) + sorted(k for k in counts if not (counts.get("C") and k in ("C", "H")))
    return "".join(f"{k}{counts[k] if counts[k] > 1 else ''}" for k in order if counts.get(k))


def formula(fig):
    bonded = Counter()
    for b in fig["bonds"]:
        i, j, order = b[0], b[1], (b[2] if len(b) > 2 else 1)
        if i == j or not (0 <= i < len(fig["atoms"]) and 0 <= j < len(fig["atoms"])):
            raise ValueError(f"bond {b}")
        bonded[i] += order
        bonded[j] += order
    counts, charge = Counter(), 0
    for k, a in enumerate(fig["atoms"]):
        el, h, q = read_label(a[2]) if len(a) > 2 and a[2] else ("C", 4 - bonded[k], 0)
        # a cation of N, O, S or P holds one more bond, an anion one fewer
        if h < 0 or (VALENCE[el] is not None and bonded[k] + h - q not in VALENCE[el]):
            raise ValueError(f"atom {k} ({el}) has {bonded[k]} bonds, {h} H and charge {q}")
        counts[el] += 1
        counts["H"] += h
        charge += q
    return hill(counts) + ("+" if charge == 1 else "-" if charge == -1 else "" if charge == 0 else f"{charge:+d}")


def check(p, H):
    """not a per-problem verifier: the structures are checked once, by run()"""
    return None


def run():
    ok = bad = 0
    for t in json.loads(_GEN.read_text()).get("problems", []):
        figs = [t.get("figure")] + [p.get("solution") for p in t.get("parts", [])]
        # a scheme's panels are checked one by one: every state of a mechanism states the same formula,
        # so an atom or a charge lost between steps shows up here
        figs = [q for fig in figs if fig for q in (fig.get("panels", []) if fig.get("type") == "scheme" else [fig])]
        for fig in figs:
            if not fig or fig.get("type") != "molecule":
                continue
            try:
                got = formula(fig)
            except ValueError as e:
                got = f"error: {e}"
            if got == fig["formula"]:
                ok += 1
            else:
                bad += 1
                print(f"  {t['template']}: states {fig['formula']}, the drawing is {got}")
    return ok, bad


if __name__ == "__main__":
    ok, bad = run()
    print(f"molecules: {ok} structures match their formulas, {bad} do not")
    raise SystemExit(1 if bad else 0)
