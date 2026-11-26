"""Biochemistry on the ASBMB core-concepts paper read in full (Nov 2026; Tansey et al., BAMBED 41:289, 2013): items are its
26 themes under five core concepts, numbered by us 1.1…5.7 (the paper does not number them). The old T1–T18 were the
eighteen themes that carry a sample outcome, in order; scripts/bc_asbmb.py renames them and registers the themes.
EXISTING cites the themes without an outcome; 2.2.D answers 5.6, which nothing did."""
from opl_dsl import Q

FILE, FRAMEWORK = "bc-asbmb", "biochemistry"
PRACTICE = "P1"
C = lambda *t: [f"asbmb-core-2013:{x}" for x in t]
THEMES = [
    ("1", "Evolution", ["The central importance of evolution to the biological sciences", "The basics of Darwin's theory", "Natural selection",
                        "Evidence for evolution", "The molecular basis of natural selection"]),
    ("2", "Matter and energy transformation", ["Forms of energy in biological processes", "Catalysis", "Coupling exergonic and endergonic processes",
                                               "The nature of biological energy"]),
    ("3", "Homeostasis", ["Biological needs for homeostasis", "Linked steady-state processes", "Quantifying homeostasis",
                          "Organisation of chemical processes", "Control mechanisms", "Cellular and organismal homeostasis"]),
    ("4", "Biological information", ["The genome", "Information in the gene: sequence to function", "Genome transmission between generations",
                                     "Genome maintenance"]),
    ("5", "Macromolecular structure and function", ["Macromolecules are large and complex", "Structure is set by several factors",
                                                    "Structure and function are related", "Macromolecular interactions", "Structures are dynamic",
                                                    "Some macromolecules are intrinsically unstructured", "Function is regulated"]),
]
OLD = {f"T{n}": c for n, c in enumerate(["1.1", "1.3", "1.4", "1.5", "2.2", "2.3", "2.4", "3.2", "3.5", "3.6", "4.1", "4.2", "4.3", "4.4",
                                          "5.1", "5.2", "5.3", "5.7"], 1)}
EXISTING = {
    "BC-1.1.A": C("3.1", "3.3"), "BC-1.1.B": C("3.1"), "BC-1.2.B": C("5.2"),
    "BC-2.1.A": C("5.1"), "BC-2.1.B": C("5.2"), "BC-2.2.A": C("5.5"), "BC-2.2.C": C("5.2", "5.5"),
    "BC-3.1.A": C("5.4"), "BC-3.1.B": C("5.4"), "BC-3.2.A": C("5.4"),
    "BC-5.2.A": C("2.1"), "BC-5.2.B": C("2.1"), "BC-6.1.A": C("2.1"), "BC-6.1.B": C("2.1"),
    "BC-7.1.A": C("3.4"), "BC-7.1.B": C("3.4"), "BC-7.3.A": C("3.5", "3.6"), "BC-7.3.B": C("3.4"),
    "BC-8.1.A": C("4.1"), "BC-8.3.A": C("4.2"), "BC-8.3.B": C("4.3"),
    "BC-11.1.A": C("1.2"), "BC-11.1.B": C("1.2"), "BC-11.2.A": C("3.3"),
}
OBJS = [("BC-2.2.D", C("5.6"), "Recognise intrinsically disordered proteins from their composition and say how they still function.",
         "Few hydrophobic residues and high net charge keep a chain unfolded; disordered regions bind by folding on contact, often to many partners, and are common in signalling.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ADD = [
    ("BC-2.2.D", Q("bc-idp-facts", "biochem.proteins", "{{q}}", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in [
        ("An intrinsically disordered region is typically rich in:", "Charged and polar residues, poor in bulky hydrophobic ones", "Bulky hydrophobic residues", "Cysteines in disulfides", "Aromatic residues"),
        ("Many disordered regions bind their partners by:", "Folding on binding (coupled folding and binding)", "Never binding anything", "Staying fully unfolded in the complex always", "Covalent cross-links"),
        ("Disordered regions are especially common in proteins for:", "Signalling and regulation", "Structural collagen", "Membrane pores only", "Storage"),
        ("One advantage of disorder for a hub protein is:", "Binding many different partners with modest affinity", "Higher thermal stability", "Faster folding to one fixed shape", "Resistance to proteases"),
        ("In a crystal structure, a disordered loop usually appears as:", "Missing density (unmodelled residues)", "A long α-helix", "A β-sheet", "Extra bound water"),
    ]], choice=MC, correct="0", verify="authored", pace="recall", explain="Low hydrophobicity and high net charge keep a chain unfolded; it can still bind by folding on contact")),
    ("BC-2.2.D", Q("bc-idp-charge", "biochem.proteins", "A {{n}}-residue segment has {{kp}} Lys/Arg and {{ne}} Asp/Glu. What is its net charge per residue at pH 7 (count +1 and −1 only)?",
        given={"n": {"pick": [40, 50, 80]}, "kp": {"pick": [4, 10, 14]}, "ne": {"pick": [3, 6, 18]}}, value="abs(kp - ne)/n", tex="|q|/n",
        verify="Abs(kp - ne)/Rational(n)", explain="High net charge per residue (with low hydrophobicity) favours disorder: like charges repel, and there is little to bury")),
]
