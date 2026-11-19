"""Structures to know cold in organic chemistry and biochemistry (beyond the amino acids).

Basis, stated plainly: no published standard lists which structures a chemist should be able to
draw from memory. The groups follow the chapters of Bruice, Organic Chemistry (8th ed.), parts 6-7
(benzene derivatives, heterocycles, carbohydrates, coenzymes, metabolic pathways, lipids, nucleic
acids); which compounds stand for each chapter is a house list, for Kevin's markup.

Every row carries a molecular formula written by hand, independently of its SMILES; the generator
refuses to run when the two disagree, and tests/verify/molecules.py recomputes the formula a third
way from the drawn atoms and bonds. None of that can tell isomers apart, so new rows are looked at.

Structures are flat skeletal drawings (no wedges) in the neutral, fully protonated form. Sugars are
Fischer projections built by fischer() below, since their stereochemistry is the point.

Run through scripts/mol.py --library (needs RDKit).
"""
import re
from pathlib import Path

# group id -> (skill, heading); rows: name, SMILES, formula, what to remember
GROUPS = {
    "group": ("orgo.functional-groups", "functional groups: the first things to trace (R = the rest of the molecule)", [
        ("an alcohol", "*O", "HOR", "R-OH"),
        ("a thiol", "*S", "HRS", "R-SH: an alcohol with sulfur"),
        ("an ether", "*O*", "OR2", "An oxygen between two carbons"),
        ("a primary amine", "*N", "H2NR", "R-NH2"),
        ("an aldehyde", "*C=O", "CHOR", "A C=O at the end of a chain: one R and one H on the carbonyl carbon"),
        ("a ketone", "*C(*)=O", "COR2", "A C=O inside a chain: two R groups on the carbonyl carbon"),
        ("a carboxylic acid", "*C(=O)O", "CHO2R", "A carbonyl carbon that also carries an OH"),
        ("an ester", "*C(=O)O*", "CO2R2", "A carboxylic acid with its H replaced by carbon"),
        ("a primary amide", "*C(N)=O", "CH2NOR", "A carbonyl carbon carrying an NH2"),
        ("an acyl chloride", "*C(Cl)=O", "CClOR", "A carbonyl carbon carrying a Cl"),
        ("an acid anhydride", "*C(=O)OC(*)=O", "C2O3R2", "Two acyl groups sharing one oxygen"),
        ("a thioester", "*C(=O)S*", "COR2S", "An ester with sulfur in place of the single-bonded oxygen (acetyl-CoA is one)"),
        ("a nitrile", "*C#N", "CNR", "A carbon triple-bonded to nitrogen"),
        ("a phosphate ester", "*OP(=O)(O)O", "H2O4PR", "R-O-P with one P=O and two P-OH (drawn fully protonated)"),
    ]),
    "aromatic": ("orgo.aromatics", "benzene derivatives and heterocycles (Bruice ch. 18-19)", [
        ("benzene", "c1ccccc1", "C6H6", "A six-membered ring with three alternating double bonds"),
        ("toluene", "Cc1ccccc1", "C7H8", "Benzene with a methyl"),
        ("phenol", "Oc1ccccc1", "C6H6O", "Benzene with an OH"),
        ("aniline", "Nc1ccccc1", "C6H7N", "Benzene with an NH2"),
        ("anisole", "COc1ccccc1", "C7H8O", "Benzene with an OCH3 (methoxybenzene)"),
        ("styrene", "C=Cc1ccccc1", "C8H8", "Benzene with a vinyl group"),
        ("benzaldehyde", "O=Cc1ccccc1", "C7H6O", "Benzene with a CHO"),
        ("benzoic acid", "OC(=O)c1ccccc1", "C7H6O2", "Benzene with a COOH"),
        ("acetophenone", "CC(=O)c1ccccc1", "C8H8O", "A methyl ketone on benzene"),
        ("naphthalene", "c1ccc2ccccc2c1", "C10H8", "Two benzene rings sharing one edge"),
        ("pyridine", "c1ccncc1", "C5H5N", "Benzene with one CH replaced by N; the lone pair is not part of the aromatic six"),
        ("pyrrole", "c1cc[nH]c1", "C4H5N", "A five-membered ring with one N-H; the nitrogen lone pair completes the aromatic six"),
        ("furan", "c1ccoc1", "C4H4O", "A five-membered aromatic ring with one O"),
        ("thiophene", "c1ccsc1", "C4H4S", "A five-membered aromatic ring with one S"),
        ("imidazole", "c1c[nH]cn1", "C3H4N2", "A five-membered ring with two nitrogens in a 1,3 relationship, one N-H and one pyridine-like (the histidine ring)"),
        ("indole", "c1ccc2[nH]ccc2c1", "C8H7N", "Benzene fused to pyrrole (the tryptophan ring)"),
        ("pyrimidine", "c1cncnc1", "C4H4N2", "A six-membered ring with nitrogens at 1 and 3 (the parent of C, T and U)"),
        ("purine", "c1ncc2nc[nH]c2n1", "C5H4N4", "Pyrimidine fused to imidazole (the parent of A and G)"),
    ]),
    "common": ("orgo.common-compounds", "solvents and small molecules known by common name", [
        ("acetone", "CC(C)=O", "C3H6O", "The simplest ketone: two methyls on a C=O"),
        ("acetic acid", "CC(O)=O", "C2H4O2", "A methyl on a COOH"),
        ("ethyl acetate", "CCOC(C)=O", "C4H8O2", "The ethyl ester of acetic acid"),
        ("diethyl ether", "CCOCC", "C4H10O", "Two ethyls on one oxygen"),
        ("tetrahydrofuran (THF)", "C1CCOC1", "C4H8O", "A saturated five-membered ring with one O"),
        ("dimethyl sulfoxide (DMSO)", "CS(C)=O", "C2H6OS", "Two methyls on an S=O"),
        ("N,N-dimethylformamide (DMF)", "CN(C)C=O", "C3H7NO", "Formamide with two methyls on the nitrogen"),
        ("acetonitrile", "CC#N", "C2H3N", "A methyl on a C≡N"),
        ("acetic anhydride", "CC(=O)OC(C)=O", "C4H6O3", "Two acetyl groups sharing one oxygen"),
        ("urea", "NC(N)=O", "CH4N2O", "A C=O carrying two NH2 groups"),
        ("chloroform", "ClC(Cl)Cl", "CHCl3", "Methane with three chlorines"),
        ("dichloromethane (DCM)", "ClCCl", "CH2Cl2", "Methane with two chlorines"),
    ]),
    "nucleo": ("biochem.nucleotides", "bases, a nucleoside and ATP (Bruice ch. 26)", [
        ("adenine", "Nc1ncnc2[nH]cnc12", "C5H5N5", "A purine with an NH2 at C-6"),
        ("guanine", "Nc1nc2[nH]cnc2c(=O)[nH]1", "C5H5N5O", "A purine with a C=O at C-6 and an NH2 at C-2"),
        ("cytosine", "Nc1cc[nH]c(=O)n1", "C4H5N3O", "A pyrimidine with a C=O at C-2 and an NH2 at C-4"),
        ("thymine", "Cc1c[nH]c(=O)[nH]c1=O", "C5H6N2O2", "Uracil with a methyl at C-5"),
        ("uracil", "O=c1cc[nH]c(=O)[nH]1", "C4H4N2O2", "A pyrimidine with C=O at C-2 and C-4"),
        ("adenosine", "Nc1ncnc2c1ncn2C1OC(CO)C(O)C1O", "C10H13N5O4", "Adenine joined through N-9 to C-1' of ribose"),
        ("ATP", "Nc1ncnc2c1ncn2C1OC(COP(=O)(O)OP(=O)(O)OP(=O)(O)O)C(O)C1O", "C10H16N5O13P3", "Adenosine with three phosphates in a row on the 5' oxygen (drawn fully protonated)"),
    ]),
    "metab": ("biochem.metabolites", "glycolysis and citric acid cycle intermediates (Bruice ch. 24)", [
        ("pyruvic acid", "CC(=O)C(O)=O", "C3H4O3", "Three carbons: methyl, ketone, acid"),
        ("lactic acid", "CC(O)C(O)=O", "C3H6O3", "Pyruvic acid with the ketone reduced to an OH"),
        ("glycerol", "OCC(O)CO", "C3H8O3", "Three carbons, an OH on each"),
        ("glyceraldehyde 3-phosphate", "O=CC(O)COP(=O)(O)O", "C3H7O6P", "Aldehyde, CH-OH, then CH2 carrying the phosphate"),
        ("dihydroxyacetone phosphate", "OCC(=O)COP(=O)(O)O", "C3H7O6P", "The ketone isomer of glyceraldehyde 3-phosphate: CH2OH, C=O, CH2-O-phosphate"),
        ("phosphoenolpyruvic acid", "C=C(OP(=O)(O)O)C(O)=O", "C3H5O6P", "Pyruvic acid trapped as its enol, with the phosphate on the enol oxygen"),
        ("oxaloacetic acid", "OC(=O)CC(=O)C(O)=O", "C4H4O5", "Four carbons: acid, CH2, ketone, acid"),
        ("citric acid", "OC(=O)CC(O)(CC(O)=O)C(O)=O", "C6H8O7", "A central carbon with an OH and a COOH, and a CH2-COOH arm on each side"),
        ("α-ketoglutaric acid", "OC(=O)CCC(=O)C(O)=O", "C5H6O5", "Five carbons: acid, two CH2, ketone, acid"),
        ("succinic acid", "OC(=O)CCC(O)=O", "C4H6O4", "Two CH2 between two acids"),
        ("fumaric acid", "OC(=O)/C=C/C(O)=O", "C4H4O4", "Succinic acid with a trans double bond"),
        ("malic acid", "OC(=O)CC(O)C(O)=O", "C4H6O5", "Fumaric acid with water added: succinic acid carrying one OH"),
    ]),
    "lipid": ("biochem.lipids-coenzymes", "fatty acids, cholesterol and coenzymes (Bruice ch. 23, 25)", [
        ("palmitic acid", "CCCCCCCCCCCCCCCC(O)=O", "C16H32O2", "A saturated 16-carbon chain ending in COOH"),
        ("stearic acid", "CCCCCCCCCCCCCCCCCC(O)=O", "C18H36O2", "A saturated 18-carbon chain ending in COOH"),
        ("oleic acid", "CCCCCCCC/C=C\\CCCCCCCC(O)=O", "C18H34O2", "18 carbons with one cis double bond between C-9 and C-10"),
        ("cholesterol", "CC(C)CCCC(C)C1CCC2C1(C)CCC1C2CC=C2CC(O)CCC12C", "C27H46O", "Four fused rings (6-6-6-5), an OH on C-3, a double bond at C-5, two methyls on the ring junctions and an eight-carbon tail on C-17"),
        ("nicotinamide", "NC(=O)c1cccnc1", "C6H6N2O", "Pyridine with a primary amide at C-3: the working end of NAD+"),
        ("pyridoxal phosphate (PLP)", "Cc1ncc(COP(=O)(O)O)c(C=O)c1O", "C8H10NO6P", "A pyridine ring carrying, in order, a methyl, an OH, an aldehyde and a CH2-O-phosphate"),
        ("biotin", "OC(=O)CCCCC1SCC2NC(=O)NC12", "C10H16N2O3S", "A cyclic urea fused to a sulfur-containing five-membered ring, with a five-carbon acid chain"),
        ("lipoic acid", "OC(=O)CCCCC1CCSS1", "C8H14O2S2", "A five-membered ring containing an S-S bond, with a five-carbon acid chain"),
    ]),
    "coenzyme": ("biochem.coenzymes", "the large coenzymes and heme, whole (Bruice ch. 23)", [
        ("NAD+", "NC(=O)c1ccc[n+](c1)C1OC(COP(O)(=O)OP(O)(=O)OCC2OC(C(O)C2O)n2cnc3c(N)ncnc23)C(O)C1O", "C21H28N7O14P2+", "Nicotinamide on a ribose, a diphosphate bridge, then adenosine. The pyridinium ring N carries the plus charge; C-4, opposite it, accepts the hydride"),
        ("NADH", "NC(=O)C1=CN(C=CC1)C1OC(COP(O)(=O)OP(O)(=O)OCC2OC(C(O)C2O)n2cnc3c(N)ncnc23)C(O)C1O", "C21H29N7O14P2", "NAD+ after taking a hydride at C-4: the ring is a 1,4-dihydropyridine with a CH2 at C-4, no charge, and no longer aromatic"),
        ("FAD", "Cc1cc2nc3c(=O)[nH]c(=O)nc-3n(CC(O)C(O)C(O)COP(O)(=O)OP(O)(=O)OCC3OC(C(O)C3O)n3cnc4c(N)ncnc34)c2cc1C", "C27H33N9O15P2", "A three-ring isoalloxazine (dimethylbenzene, pyrazine, a uracil-like ring) on a ribitol chain, a diphosphate bridge, then adenosine"),
        ("coenzyme A", "CC(C)(COP(O)(=O)OP(O)(=O)OCC1OC(C(O)C1OP(O)(O)=O)n1cnc2c(N)ncnc12)C(O)C(=O)NCCC(=O)NCCS", "C21H36N7O16P3S", "From the working end: a thiol on two carbons, an amide, beta-alanine, an amide, pantoic acid (OH, then a carbon with two methyls), a diphosphate, and adenosine with an extra phosphate on its 3' OH"),
        ("acetyl-CoA", "CC(=O)SCCNC(=O)CCNC(=O)C(O)C(C)(C)COP(O)(=O)OP(O)(=O)OCC1OC(C(O)C1OP(O)(O)=O)n1cnc2c(N)ncnc12", "C23H38N7O17P3S", "Coenzyme A with an acetyl group on the sulfur: a thioester"),
        ("thiamine pyrophosphate (TPP)", "Cc1ncc(C[n+]2csc(CCOP(O)(=O)OP(O)(O)=O)c2C)c(N)n1", "C12H19N4O7P2S+", "An aminopyrimidine joined by a CH2 to the N of a thiazolium ring; the ring carries a methyl and a two-carbon chain ending in the diphosphate. The acidic C-H sits between N+ and S"),
        ("protoporphyrin IX", "Cc1c(C=C)c2cc3nc(cc4[nH]c(cc5nc(cc1[nH]2)c(C)c5CCC(O)=O)c(CCC(O)=O)c4C)c(C=C)c3C", "C34H34N4O4", "Four pyrrole rings joined by four CH bridges. Round the edge: methyl, vinyl; methyl, vinyl; methyl, propionate; propionate, methyl"),
    ]),
}

# heme b is protoporphyrin IX with its two N-H hydrogens replaced by iron(II) held by all four nitrogens
HEME = ("heme b", "C34H32FeN4O4", "Protoporphyrin IX with Fe(II) in the middle, bonded to all four nitrogens (two of them drawn dashed, as coordinate bonds). In myoglobin the fifth position is the proximal histidine and O2 binds at the sixth")

# Fischer projections: name, formula, aldose or ketose, OH side at each stereocentre from the top
SUGARS = [
    ("D-glyceraldehyde", "C3H6O3", "aldose", "R", "The reference for D and L: OH on the right at the one stereocentre"),
    ("D-ribose", "C5H10O5", "aldose", "RRR", "All three OH groups on the right"),
    ("2-deoxy-D-ribose", "C5H10O4", "aldose", "HRR", "Ribose with no OH at C-2 (two H there)"),
    ("D-glucose", "C6H12O6", "aldose", "RLRR", "Right, left, right, right: only C-3 has its OH on the left"),
    ("D-galactose", "C6H12O6", "aldose", "RLLR", "The C-4 epimer of glucose: right, left, left, right"),
    ("D-mannose", "C6H12O6", "aldose", "LLRR", "The C-2 epimer of glucose: left, left, right, right"),
    ("D-fructose", "C6H12O6", "ketose", "LRR", "A ketone at C-2 with CH2OH above it; below, the same C-3 to C-5 pattern as glucose: left, right, right"),
]


def fischer(kind, sides):
    """atoms and bonds for a Fischer projection: carbons are the vertices of a vertical chain"""
    atoms, bonds = [], []

    def atom(x, y, lab=None):
        atoms.append([x, y] if lab is None else [x, y, lab])
        return len(atoms) - 1

    y = 0.0
    if kind == "aldose":
        top = atom(0, y)
        bonds.append([top, atom(0.8, y + 0.6, "O"), 2])
        bonds.append([top, atom(-0.8, y + 0.6, "H")])
    else:
        c1 = atom(0, y + 1)
        bonds.append([c1, atom(0.87, y + 1.5, "OH")])
        top = atom(0, y)
        bonds.append([c1, top])
        bonds.append([top, atom(1.0, y, "O"), 2])
    prev = top
    for side in sides:
        y -= 1
        c = atom(0, y)
        bonds.append([prev, c])
        bonds.append([c, atom(1.0, y, "H" if side in "LH" else "OH")])
        bonds.append([c, atom(-1.0, y, "H" if side in "RH" else "HO")])
        prev = c
    last = atom(0, y - 1)
    bonds.append([prev, last])
    bonds.append([last, atom(0.87, y - 1.5, "OH")])
    return atoms, bonds


def porphyrin(atoms, bonds):
    """Lay a porphyrin out square (RDKit pinches the macrocycle): four pyrroles on the compass points,
    the four CH bridges on the diagonals, substituents zigzagging outward. Works on the graph alone."""
    import math
    nb = {k: [] for k in range(len(atoms))}
    for b in bonds:
        nb[b[0]].append(b[1])
        nb[b[1]].append(b[0])
    is_n = lambda k: len(atoms[k]) > 2 and "N" in atoms[k][2]  # noqa: E731
    pos, ring_of = {}, {}
    n0 = next(k for k in nb if is_n(k))
    n, a_in = n0, nb[n0][0]
    for step in range(4):
        phi = math.radians(90 - 90 * step)
        u, v = (math.cos(phi), math.sin(phi)), (math.cos(phi - math.pi / 2), math.sin(phi - math.pi / 2))
        at = lambda r, t: (r * u[0] + t * v[0], r * u[1] + t * v[1])  # noqa: E731
        a_out = next(k for k in nb[n] if k != a_in)
        beta = lambda a: next(k for k in nb[a] if not is_n(k) and len(nb[k]) == 3)  # noqa: E731
        meso = next(k for k in nb[a_out] if not is_n(k) and len(nb[k]) == 2)
        pos[n], pos[a_in], pos[a_out] = at(1.45, 0), at(2.1, -0.8), at(2.1, 0.8)
        pos[beta(a_in)], pos[beta(a_out)] = at(3.05, -0.5), at(3.05, 0.5)
        m = math.radians(45 - 90 * step)
        pos[meso] = (2.4 * math.cos(m), 2.4 * math.sin(m))
        for k in (beta(a_in), beta(a_out)):
            ring_of[k] = at(2.4, 0)
        a_in = next(k for k in nb[meso] if k != a_out)
        n = next(k for k in nb[a_in] if is_n(k))

    def grow(k, theta, depth):
        kids = [c for c in nb[k] if c not in pos]
        turns = [math.radians(30) * (1 if depth % 2 else -1)] if len(kids) == 1 else [math.radians(60), -math.radians(60)]
        for c, turn in zip(kids, turns):
            pos[c] = (pos[k][0] + math.cos(theta + turn), pos[k][1] + math.sin(theta + turn))
        for c, turn in zip(kids, turns):
            grow(c, theta + turn, depth + 1)

    for k, c in ring_of.items():
        grow(k, math.atan2(pos[k][1] - c[1], pos[k][0] - c[0]) + math.radians(30), 1)
    new = [[round(pos[k][0], 2), round(pos[k][1], 2)] + at_[2:] for k, at_ in enumerate(atoms)]
    # ring double bonds are drawn as plain double lines here: the inside-the-ring hint came from the old layout
    return new, [b[:3] if len(b) > 3 else b for b in bonds]


HEAD = """# Structures to know cold: draw each from its name, and name each from its drawing.
# GENERATED by scripts/mol.py --library from scripts/mol_library.py: edit there, not here.
#
# Basis: the groups follow the chapters of Bruice, Organic Chemistry 8e (standards.yaml: bruice-8e,
# a textbook's table of contents). Which compounds stand for each chapter is a house list.
# Flat skeletal structures, neutral and fully protonated; sugars are Fischer projections.
# Each formula is recomputed from the atoms and bonds by tests/verify/molecules.py.
"""


def slug(name):
    name = name.split(" (")[0].replace("α", "alpha").replace("N,N-", "")
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def heavy(formula):
    return sum(int(n or 1) for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula) if el != "H")


def q(text):
    return text.replace("'", "''")


def write(block, emit, layout):
    out, count = [HEAD], 0
    groups = {g: (skill, head, [(n, f, hook, ("smiles", s)) for n, s, f, hook in rows]) for g, (skill, head, rows) in GROUPS.items()}
    groups["sugar"] = ("biochem.sugars", "sugars as Fischer projections (Bruice ch. 20)",
                       [(n, f, hook, ("fischer", (kind, sides))) for n, f, kind, sides, hook in SUGARS])
    groups["coenzyme"][2].append((HEME[0], HEME[1], HEME[2], ("heme", next(r[3][1] for r in groups["coenzyme"][2] if r[0] == "protoporphyrin IX"))))
    for g, (skill, head, rows) in groups.items():
        out.append(f"\n# ── {head} ──\n")
        for name, formula, hook, (how, spec) in rows:
            def fig(indent):
                if how == "smiles" and name != "protoporphyrin IX":
                    return block(spec, indent=indent, expect=formula)
                if how == "smiles" and name == "protoporphyrin IX":
                    _, atoms, bonds = layout(spec)
                    atoms, bonds = porphyrin(atoms, bonds)
                    atoms = [[at[0], at[1], "NH"] if len(at) > 2 and "N" in at[2] and "H" in at[2] else at for at in atoms]
                    return emit(formula, atoms, bonds, indent)
                if how == "heme":
                    _, atoms, bonds = layout(spec)
                    atoms, bonds = porphyrin(atoms, bonds)
                    ns = [k for k, at in enumerate(atoms) if len(at) > 2 and "N" in at[2]]
                    fe = len(atoms)
                    atoms = atoms + [[round(sum(atoms[k][0] for k in ns) / 4, 2), round(sum(atoms[k][1] for k in ns) / 4, 2), "Fe"]]
                    bonds = bonds + [[k, fe, 1 if "H" in atoms[k][2] else 0] for k in ns]
                    atoms = [[at[0], at[1], "N"] if k in ns else at for k, at in enumerate(atoms)]
                    return emit(formula, atoms, bonds, indent)
                atoms, bonds = fischer(*spec)
                return emit(formula, atoms, bonds, indent)
            what = "the Fischer projection of " + name if how == "fischer" else name + " from memory, as a skeletal structure"
            # look-alikes: the three others in the group closest in size
            others = sorted((r for r in rows if r[0] != name), key=lambda r: (abs(heavy(r[1]) - heavy(formula)), r[0]))[:3]
            opts = sorted([name] + [r[0] for r in others])
            tex = re.sub(r"(\d+)", r"_{\1}", formula)
            out.append(f"""- template: st-draw-{slug(name)}
  skill: {skill}
  pace: quick
  prompt: 'Draw {q(what)}.'
  parts:
    - ask: 'Draw it on paper, then compare'
      label: a
      draw: true
      solution:
{fig("        ")}      explain: '{q(hook)}. Formula $\\mathrm{{{tex}}}$'
- template: st-name-{slug(name)}
  skill: {skill}
  pace: recall
  prompt: 'Which compound is this?'
  figure:
{fig("    ")}  parts:
    - ask: 'Name it'
      label: a
      choice: [{", ".join('"' + o + '"' for o in opts)}]
      correct: "{opts.index(name)}"
      explain: '{q(name[0].upper() + name[1:])}. {q(hook)}'
  verify: {{ authored: true }}
""")
            count += 1
    path = Path(__file__).resolve().parents[1] / "drills/problems/st-structures.yaml"
    path.write_text("".join(out), encoding="utf8")
    print(f"wrote {path} ({count} structures)")
