#!/usr/bin/env python3
"""Lay out a skeletal structure for a `type: molecule` figure (drills/problems/*.yaml).

A dev tool, not part of the build: it needs RDKit (`pip install rdkit`). The committed YAML holds
plain coordinates, and tests/verify/molecules.py re-derives each formula from them without RDKit.

  python3 scripts/mol.py "C[C@H](N)C(=O)O"            one structure, printed as a solution block
  python3 scripts/mol.py --amino-acids                 rewrites drills/problems/bc-amino-acids.yaml
  python3 scripts/mol.py --library                     rewrites drills/problems/st-structures.yaml

Layout for an amino acid: amine on the left, carboxyl on the right, side chain up.
"""
import math
import sys
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

BACKBONE = Chem.MolFromSmarts("[NX3][CX4][CX3](=O)[OX2H1]")


def layout(smiles: str, amino=False):
    m = Chem.MolFromSmiles(smiles)
    formula = CalcMolFormula(m)
    Chem.Kekulize(m, clearAromaticFlags=True)
    rdDepictor.SetPreferCoordGen(False)
    rdDepictor.Compute2DCoords(m)
    conf = m.GetConformer()
    pts = [[conf.GetAtomPosition(i).x / 1.5, conf.GetAtomPosition(i).y / 1.5] for i in range(m.GetNumAtoms())]
    if amino:
        n_, ca, c_, _, _ = m.GetSubstructMatch(BACKBONE)
        th = -math.atan2(pts[c_][1] - pts[n_][1], pts[c_][0] - pts[n_][0])
        pts = [[x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)] for x, y in pts]
        side = [a.GetIdx() for a in m.GetAtomWithIdx(ca).GetNeighbors() if a.GetIdx() not in (n_, c_)]
        # side chain up; glycine has none, so put the alpha carbon down (the zigzag every other one gets)
        up = pts[side[0]][1] - pts[ca][1] if side else pts[n_][1] - pts[ca][1]
        if up < 0:
            pts = [[x, -y] for x, y in pts]
    atoms = []
    for a in m.GetAtoms():
        i, el, h = a.GetIdx(), a.GetSymbol(), a.GetTotalNumHs()
        if el == "*":  # a dummy atom in the SMILES is "the rest of the molecule"
            atoms.append([round(pts[i][0], 2), round(pts[i][1], 2), "R"])
            continue
        if el == "C":
            atoms.append([round(pts[i][0], 2), round(pts[i][1], 2)])
            continue
        hs = "" if h == 0 else "H" if h == 1 else f"H{h}"
        q = {1: "+", -1: "-", 0: ""}[a.GetFormalCharge()]
        # hydrogens go on the side away from the bonds
        dx = sum(pts[b.GetIdx()][0] for b in a.GetNeighbors()) / a.GetDegree() - pts[i][0]
        atoms.append([round(pts[i][0], 2), round(pts[i][1], 2), ((hs + el) if (hs and dx > 0.3) else (el + hs)) + q])
    ring = m.GetRingInfo()
    bonds = []
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        order = {Chem.BondType.SINGLE: 1, Chem.BondType.DOUBLE: 2, Chem.BondType.TRIPLE: 3}[b.GetBondType()]
        if order == 2 and b.IsInRing():
            r = next(r for r in ring.AtomRings() if i in r and j in r)
            cx, cy = sum(pts[k][0] for k in r) / len(r), sum(pts[k][1] for k in r) / len(r)
            ux, uy = pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]
            # the renderer offsets by (-uy, ux) in screen space, where y points down
            cross = ux * (cy - pts[i][1]) - uy * (cx - pts[i][0])
            bonds.append([i, j, 2, -1 if cross > 0 else 1])
        else:
            bonds.append([i, j] if order == 1 else [i, j, order])
    return formula, atoms, bonds


def emit(formula, atoms, bonds, indent="        "):
    fmt = lambda a: "[" + ", ".join(f'"{v}"' if isinstance(v, str) else str(v) for v in a) + "]"  # noqa: E731
    return (f"{indent}type: molecule\n{indent}formula: {formula}\n"
            f"{indent}atoms: [{', '.join(fmt(a) for a in atoms)}]\n{indent}bonds: [{', '.join(fmt(b) for b in bonds)}]\n")


def block(smiles, amino=False, indent="        ", expect=None):
    formula, atoms, bonds = layout(smiles, amino)
    # the formula written by hand in the table must agree with the one the SMILES gives
    if "*" in smiles:  # RDKit has no formula for an R group: the hand-written one stands, and molecules.py checks it
        formula = expect
    if expect is not None and expect != formula:
        raise SystemExit(f"{smiles}: table says {expect}, the SMILES is {formula}")
    return emit(formula, atoms, bonds, indent)


if __name__ == "__main__":
    if sys.argv[1:] == ["--amino-acids"]:
        sys.path.insert(0, str(Path(__file__).parent))
        from mol_amino import write
        write(block)
    elif sys.argv[1:] == ["--library"]:
        sys.path.insert(0, str(Path(__file__).parent))
        from mol_library import write
        write(block, emit, layout)
    else:
        print(block(sys.argv[1], amino="--amino" in sys.argv, indent=""))
