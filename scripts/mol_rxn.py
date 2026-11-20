"""Predict the product: the core reactions of a two-semester organic course, as draw-from-memory cards.

Basis, stated plainly: no published standard lists which reactions to know. The families follow the
reaction chapters of Bruice, Organic Chemistry (8th ed.); which reactions and which substrates stand for
each is a house list, for Kevin's markup.

Every row gives the reactant, the reagents, the product and, written separately, what the reagents add
to or take from the molecule (`delta`, e.g. +HBr, -H2, +O -H2). The generator refuses to run unless
formula(product) = formula(reactant) + delta, and tests/verify/molecules.py recomputes each drawn
formula a third way. That catches a dropped or extra atom. It cannot tell regiochemistry or
stereochemistry apart, so the products were looked at once and the rule that fixes each is in the hook.
Structures are flat (no wedges); stereochemistry is stated in words.

Run through scripts/mol.py --reactions (needs RDKit).
"""
import re
from collections import Counter
from pathlib import Path

# family -> (skill, heading, rows); row: slug, substrate name, substrate SMILES, reagents, product SMILES, delta, what the reagent does, rule
FAMILIES = {
    "alkene": ("orgo.alkene-reactions", "additions to alkenes (Bruice ch. 6)", [
        ("hbr", "2-methylpropene", "CC(C)=C", "HBr", "CC(C)(C)Br", "+HBr", "adds H and Br, Br on the more substituted carbon", "Markovnikov: the proton goes to the carbon with more hydrogens, because that leaves the more stable (here tertiary) carbocation"),
        ("hbr-peroxide", "2-methylpropene", "CC(C)=C", "HBr with a peroxide (ROOR)", "CC(C)CBr", "+HBr", "adds H and Br, Br on the less substituted carbon", "A radical chain: Br· adds first, to the less substituted carbon, giving the more stable radical. Anti-Markovnikov, and only HBr does it"),
        ("hydration", "1-methylcyclohexene", "CC1=CCCCC1", "H2O with H2SO4", "CC1(O)CCCCC1", "+H2O", "adds H and OH, OH on the more substituted carbon", "Acid-catalysed hydration is Markovnikov and goes through a carbocation, so watch for rearrangements"),
        ("hydroboration", "1-methylcyclohexene", "CC1=CCCCC1", "1. BH3·THF  2. H2O2, NaOH", "CC1CCCCC1O", "+H2O", "adds H and OH, OH on the less substituted carbon, syn", "Boron goes to the less hindered carbon and is then replaced by OH: anti-Markovnikov, syn addition, no rearrangement (the methyl and OH end up trans)"),
        ("bromination", "cyclohexene", "C1=CCCCC1", "Br2 in CH2Cl2", "BrC1CCCCC1Br", "+Br2", "adds a Br to each carbon, anti", "A bromonium ion is opened from the back by bromide: anti addition, so the trans dibromide"),
        ("bromohydrin", "1-methylcyclohexene", "CC1=CCCCC1", "Br2 in H2O", "CC1(O)CCCCC1Br", "+BrOH", "adds Br and OH, OH on the more substituted carbon", "Water, the solvent, opens the bromonium ion at the more substituted carbon: OH there, Br on the other carbon, anti"),
        ("hydrogenation", "1-methylcyclohexene", "CC1=CCCCC1", "H2 with Pd/C", "CC1CCCCC1", "+H2", "adds two hydrogens, syn", "Both hydrogens are delivered from the metal surface to the same face"),
        ("epoxidation", "cyclohexene", "C1=CCCCC1", "mCPBA", "C1CCC2OC2C1", "+O", "adds one oxygen across the double bond", "A peroxyacid hands over one oxygen in a single step: an epoxide, with the alkene geometry kept"),
        ("dihydroxylation", "cyclohexene", "C1=CCCCC1", "1. OsO4  2. NaHSO3, H2O", "OC1CCCCC1O", "+H2O2", "adds two OH groups, syn", "A cyclic osmate ester puts both oxygens on the same face: the cis diol. (Epoxide opening with water gives the trans diol.)"),
        ("ozonolysis", "1-methylcyclohexene", "CC1=CCCCC1", "1. O3  2. (CH3)2S", "CC(=O)CCCCC=O", "+O2", "cuts the C=C and caps each carbon with =O", "Erase the double bond and write =O on each carbon. A ring opens into one chain; a carbon that carried an H becomes an aldehyde"),
    ]),
    "alkyne": ("orgo.alkyne-reactions", "alkynes (Bruice ch. 7)", [
        ("lindlar", "but-2-yne", "CC#CC", "H2 with Lindlar catalyst", "C/C=C\\C", "+H2", "stops at the cis alkene", "A poisoned catalyst adds one H2, syn: the cis (Z) alkene"),
        ("dissolving-metal", "but-2-yne", "CC#CC", "Na in liquid NH3", "C/C=C/C", "+H2", "gives the trans alkene", "Electrons add one at a time and the vinyl radical anion takes the trans shape: the trans (E) alkene"),
        ("hydration", "pent-1-yne", "CCCC#C", "H2O, H2SO4, HgSO4", "CCCC(C)=O", "+H2O", "makes a methyl ketone", "Markovnikov hydration gives an enol, which tautomerises: a terminal alkyne becomes a methyl ketone"),
        ("hydroboration", "pent-1-yne", "CCCC#C", "1. disiamylborane  2. H2O2, NaOH", "CCCCC=O", "+H2O", "makes an aldehyde", "Anti-Markovnikov enol, then tautomerisation: a terminal alkyne becomes an aldehyde"),
        ("alkylation", "pent-1-yne", "CCCC#C", "1. NaNH2  2. CH3I", "CCCC#CC", "+CH2", "adds a carbon to the alkyne end", "NaNH2 (pKa 38) removes the terminal alkyne proton (pKa 25); the acetylide is a carbon nucleophile for SN2 on a methyl or primary halide"),
    ]),
    "sub": ("orgo.substitution-elimination", "alcohols and alkyl halides (Bruice ch. 9-10)", [
        ("pbr3", "butan-1-ol", "CCCCO", "PBr3", "CCCCBr", "+Br -OH", "swaps OH for Br", "Turns OH into a good leaving group and displaces it by SN2: inversion, no rearrangement"),
        ("socl2", "butan-1-ol", "CCCCO", "SOCl2 with pyridine", "CCCCCl", "+Cl -OH", "swaps OH for Cl", "Same idea as PBr3: the by-products SO2 and HCl leave as gases"),
        ("tosylation", "butan-1-ol", "CCCCO", "TsCl with pyridine", "CCCCOS(=O)(=O)c1ccc(C)cc1", "+C7H6SO2", "turns OH into OTs", "The C–O bond is not touched, so the configuration is kept; OTs then leaves like a halide"),
        ("pcc", "butan-1-ol", "CCCCO", "PCC in CH2Cl2", "CCCC=O", "-H2", "oxidises a primary alcohol and stops at the aldehyde", "No water, so no hydrate, so no second oxidation: primary alcohol to aldehyde"),
        ("jones", "butan-1-ol", "CCCCO", "H2CrO4 (Na2Cr2O7, H2SO4, H2O)", "CCCC(=O)O", "+O -H2", "oxidises a primary alcohol all the way to the acid", "In water the aldehyde forms a hydrate, which is oxidised again: primary alcohol to carboxylic acid"),
        ("jones-secondary", "cyclohexanol", "OC1CCCCC1", "H2CrO4", "O=C1CCCCC1", "-H2", "oxidises a secondary alcohol to a ketone", "A secondary alcohol has one H on the carbinol carbon, so it stops at the ketone. Tertiary alcohols do not react"),
        ("cyanide", "1-bromobutane", "CCCCBr", "NaCN in DMSO", "CCCCC#N", "+CN -Br", "swaps Br for CN, adding a carbon", "A good nucleophile, a primary halide and a polar aprotic solvent: SN2"),
        ("e2-zaitsev", "2-bromo-2-methylbutane", "CCC(C)(C)Br", "NaOCH2CH3 in ethanol, heat", "CC=C(C)C", "-HBr", "eliminates to the more substituted alkene", "A strong, small base on a tertiary halide: E2, giving the more substituted (Zaitsev) alkene"),
        ("e2-hofmann", "2-bromo-2-methylbutane", "CCC(C)(C)Br", "KOC(CH3)3 in tert-butanol", "CCC(C)=C", "-HBr", "eliminates to the less substituted alkene", "A bulky base takes the most accessible proton: the less substituted (Hofmann) alkene"),
        ("williamson", "butan-1-ol", "CCCCO", "1. NaH  2. CH3I", "CCCCOC", "+CH2", "makes an ether", "Alkoxide plus a methyl or primary halide, SN2. Put the hindered group on the alkoxide, never on the halide"),
        ("grignard-co2", "bromobenzene", "Brc1ccccc1", "1. Mg, ether  2. CO2  3. H3O+", "OC(=O)c1ccccc1", "+CO2H -Br", "swaps Br for CO2H", "Mg turns the carbon from electrophile to nucleophile; it attacks CO2: a carboxylic acid with one more carbon"),
    ]),
    "carbonyl": ("orgo.carbonyl-reactions", "aldehydes and ketones (Bruice ch. 16)", [
        ("nabh4", "cyclohexanone", "O=C1CCCCC1", "1. NaBH4  2. H3O+", "OC1CCCCC1", "+H2", "reduces a ketone to an alcohol", "Hydride adds to the carbonyl carbon. NaBH4 reduces aldehydes and ketones only"),
        ("grignard", "cyclohexanone", "O=C1CCCCC1", "1. CH3MgBr  2. H3O+", "CC1(O)CCCCC1", "+CH4", "adds a carbon group to C=O, giving an alcohol", "A carbon nucleophile adds once to a ketone: a tertiary alcohol"),
        ("wittig", "cyclohexanone", "O=C1CCCCC1", "Ph3P=CH2", "C=C1CCCCC1", "+CH2 -O", "swaps C=O for C=C", "The ylide carbon replaces the oxygen exactly where the carbonyl was: no regiochemistry to guess"),
        ("acetal", "cyclohexanone", "O=C1CCCCC1", "HOCH2CH2OH with catalytic H+", "C1CCC2(CC1)OCCO2", "+C2H4O", "protects C=O as a cyclic acetal", "Two OR groups replace the C=O and water leaves. Stable to base, hydride and Grignards; aqueous acid takes it off"),
        ("imine", "cyclohexanone", "O=C1CCCCC1", "CH3NH2 with catalytic H+", "CN=C1CCCCC1", "+CH3N -O", "swaps C=O for C=N", "A primary amine gives an imine and water. A secondary amine gives an enamine"),
        ("reductive-amination", "cyclohexanone", "O=C1CCCCC1", "CH3NH2 with NaBH3CN", "CNC1CCCCC1", "+CH5N -O", "turns C=O into C–N", "Imine formed and reduced in the same pot: the reliable way to make an amine"),
        ("wolff-kishner", "acetophenone", "CC(=O)c1ccccc1", "H2NNH2, KOH, heat", "CCc1ccccc1", "+H2 -O", "removes the carbonyl oxygen completely", "C=O becomes CH2 under basic conditions (Clemmensen does the same in acid)"),
        ("lda-alkylation", "cyclohexanone", "O=C1CCCCC1", "1. LDA, −78 °C  2. CH3I", "CC1CCCCC1=O", "+CH2", "adds a carbon next to the carbonyl", "LDA makes the enolate completely; the α-carbon then does SN2 on the halide"),
    ]),
    "acyl": ("orgo.acyl-reactions", "carboxylic acids and their derivatives (Bruice ch. 15)", [
        ("acid-chloride", "benzoic acid", "OC(=O)c1ccccc1", "SOCl2", "O=C(Cl)c1ccccc1", "+Cl -OH", "turns an acid into an acyl chloride", "The most reactive acyl derivative: from here you can make any of the others"),
        ("fischer", "benzoic acid", "OC(=O)c1ccccc1", "CH3OH (excess) with H2SO4", "COC(=O)c1ccccc1", "+CH2", "turns an acid into an ester", "An equilibrium: push it with excess alcohol or by removing water"),
        ("amide", "benzoyl chloride", "O=C(Cl)c1ccccc1", "NH3 (2 equivalents)", "NC(=O)c1ccccc1", "+NH2 -Cl", "turns an acyl chloride into an amide", "Addition then elimination of chloride. The second equivalent mops up the HCl"),
        ("saponification", "ethyl benzoate", "CCOC(=O)c1ccccc1", "1. NaOH, H2O  2. H3O+", "OC(=O)c1ccccc1", "-C2H4", "hydrolyses an ester to the acid", "Hydroxide adds, alkoxide leaves, and the acid is deprotonated at once, which makes it irreversible"),
        ("lah-ester", "ethyl benzoate", "CCOC(=O)c1ccccc1", "1. LiAlH4  2. H3O+", "OCc1ccccc1", "+H4 -C2H6O", "reduces an ester to a primary alcohol", "Hydride adds twice: the first addition ejects ethoxide to give an aldehyde, which is reduced again. NaBH4 will not do this"),
        ("grignard-ester", "methyl benzoate", "COC(=O)c1ccccc1", "1. CH3MgBr (2 equivalents)  2. H3O+", "CC(C)(O)c1ccccc1", "+C2H8 -CH4O", "adds two carbon groups to an ester, giving a tertiary alcohol", "The first addition gives a ketone, which is more reactive than the ester, so it adds again: two identical groups on the carbinol carbon"),
        ("lah-amide", "N,N-dimethylbenzamide", "CN(C)C(=O)c1ccccc1", "1. LiAlH4  2. H2O", "CN(C)Cc1ccccc1", "+H2 -O", "reduces an amide to an amine", "The one acyl reduction that keeps the heteroatom: C=O becomes CH2"),
        ("claisen", "ethyl acetate (2 equivalents)", "CCOC(C)=O", "1. NaOCH2CH3  2. H3O+", "CCOC(=O)CC(C)=O", "+C2H2O", "joins two esters into a β-keto ester", "An ester enolate attacks a second ester and ethoxide leaves: a 1,3-dicarbonyl"),
    ]),
    "aromatic": ("orgo.aromatic-reactions", "benzene and substituted benzenes (Bruice ch. 18)", [
        ("bromination", "benzene", "c1ccccc1", "Br2 with FeBr3", "Brc1ccccc1", "+Br -H", "puts Br on the ring", "The Lewis acid makes Br+; the ring attacks and then loses H+ to become aromatic again. Substitution, not addition"),
        ("nitration", "benzene", "c1ccccc1", "HNO3 with H2SO4", "O=[N+]([O-])c1ccccc1", "+NO2 -H", "puts NO2 on the ring", "The electrophile is the nitronium ion, NO2+"),
        ("acylation", "benzene", "c1ccccc1", "CH3COCl with AlCl3", "CC(=O)c1ccccc1", "+C2H2O", "puts an acyl group on the ring", "An acylium ion: no rearrangement and no second substitution, unlike Friedel–Crafts alkylation"),
        ("nitration-toluene", "toluene", "Cc1ccccc1", "HNO3 with H2SO4", "Cc1ccc(cc1)[N+](=O)[O-]", "+NO2 -H", "puts NO2 para (and ortho) to the methyl", "An alkyl group donates electrons: activating, ortho/para directing. Para is drawn; ortho forms too"),
        ("bromination-nitrobenzene", "nitrobenzene", "O=[N+]([O-])c1ccccc1", "Br2 with FeBr3", "O=[N+]([O-])c1cccc(Br)c1", "+Br -H", "puts Br meta to the nitro group", "A nitro group withdraws electrons: deactivating, meta directing"),
        ("nitro-reduction", "nitrobenzene", "O=[N+]([O-])c1ccccc1", "1. Sn, HCl  2. NaOH", "Nc1ccccc1", "+H2 -O2", "reduces NO2 to NH2", "How an amino group gets onto a ring: nitrate first, then reduce. It also turns a meta director into an ortho/para director"),
        ("side-chain-oxidation", "toluene", "Cc1ccccc1", "KMnO4, heat, then H3O+", "OC(=O)c1ccccc1", "+O2 -H2", "oxidises the side chain to CO2H", "Any alkyl group with a benzylic hydrogen is cut back to CO2H, whatever its length"),
        ("benzylic-bromination", "toluene", "Cc1ccccc1", "NBS with light or peroxide", "BrCc1ccccc1", "+Br -H", "puts Br on the benzylic carbon", "A radical chain at the benzylic position, where the radical is stabilised by the ring. The ring itself is untouched"),
    ]),
    "cc": ("orgo.enolate-reactions", "carbon–carbon bond formation (Bruice ch. 8, 17)", [
        ("aldol-condensation", "acetaldehyde (2 equivalents)", "CC=O", "NaOH, then heat", "C/C=C/C=O", "+C2H2", "joins two carbonyls into an α,β-unsaturated carbonyl", "An enolate adds to a second carbonyl (a β-hydroxy aldehyde), then heat removes water. The new C=C sits between the α and β carbons"),
        ("diels-alder", "buta-1,3-diene", "C=CC=C", "maleic anhydride, heat", "O=C1OC(=O)C2CC=CCC12", "+C4H2O3", "builds a cyclohexene ring", "Diene plus dienophile, one step: two new σ bonds and one new π bond in the middle of what was the diene. The cis geometry of the dienophile is kept"),
    ]),
}

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
ELEM = re.compile(r"([A-Z][a-z]?)(\d*)")


def count(formula):
    c = Counter()
    for el, n in ELEM.findall(formula.replace("+", "").replace("-", "")):
        c[el] += int(n or 1)
    return c


def apply(c, delta):
    c = Counter(c)
    for part in delta.split():
        for el, n in count(part[1:]).items():
            c[el] += n if part[0] == "+" else -n
    return +c


HEAD = '''# Predict the product: organic reactions as draw-from-memory cards and reagent recall.
# GENERATED by scripts/mol_rxn.py (python3 scripts/mol.py --reactions): edit the table there, not this file.
# Each product formula equals the reactant formula plus the stated change; regiochemistry and
# stereochemistry are not machine-checked. Structures are flat.
'''
q = lambda s: s.replace("'", "''")
pretty = lambda s: re.sub(r"(?<=[A-Za-z\)])(\d)", lambda m: m.group(1).translate(SUB), s)


def write(layout, emit):
    out, n = [HEAD], 0
    for fam, (skill, head, rows) in FAMILIES.items():
        out.append(f"\n# ── {head} ──\n")
        for slug, name, rs, reagents, ps, delta, does, rule in rows:
            fr, ar, br = layout(rs)
            fp, ap, bp = layout(ps)
            if apply(count(fr), delta) != count(fp):
                raise SystemExit(f"{fam}-{slug}: {fr} {delta} is not {fp}")
            others = [r[6] for r in rows if r[6] != does]
            k = sum(map(ord, slug)) % max(1, len(others))
            opts = sorted([does] + (others[k:] + others[:k])[:3])
            tex = re.sub(r"(\d+)", r"_{\1}", fp)
            out.append(f"""- template: rx-predict-{fam}-{slug}
  skill: {skill}
  pace: quick
  prompt: 'Predict the major organic product and draw it: {q(name)} with {q(pretty(reagents))}.'
  figure:
{emit(fr, ar, br, "    ")}  parts:
    - ask: 'Draw the product on paper, then compare'
      label: a
      draw: true
      solution:
{emit(fp, ap, bp, "        ")}      explain: 'It {q(does)}. {q(rule)}. Product $\\mathrm{{{tex}}}$'
- template: rx-reagent-{fam}-{slug}
  skill: {skill}
  pace: recall
  prompt: 'What does this do? {q(pretty(reagents))}, acting on {q(name)}.'
  parts:
    - ask: 'It'
      label: a
      choice: [{", ".join('"' + o + '"' for o in opts)}]
      correct: "{opts.index(does)}"
      explain: '{q(rule)}'
  verify: {{ authored: true }}
""")
            n += 1
    path = Path(__file__).resolve().parents[1] / "drills/problems/rx-reactions.yaml"
    path.write_text("".join(out), encoding="utf8")
    print(f"wrote {path}: {n} reactions, {2 * n} templates")
