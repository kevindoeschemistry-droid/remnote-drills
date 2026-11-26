"""Write drills/frameworks/biochemistry.yaml from scripts/second_specs/bc.py (UNITS, IDEAS), register the ASBMB
standards in drills/standards.yaml, and add the biochem.* drill skills and the Lehninger source. Idempotent: the
framework is rewritten only when absent (second_types.py then fills each objective's `drills:`).
Usage: python3 scripts/bc_framework.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import bc  # noqa: E402

q = lambda s: json.dumps(s, ensure_ascii=False)
fl = lambda xs: "[" + ", ".join(q(x) for x in xs) + "]"

# ---- standards --------------------------------------------------------------------------------------------------
CORE = [("Evolution", 4), ("Matter and energy transformation", 3), ("Homeostasis", 3), ("Biological information", 4),
        ("Macromolecular structure and function", 4)]
core_items, n = [], 1
for concept, k in CORE:
    for j in range(k):
        core_items.append({"code": f"T{n}", "title": f"{concept}: statement {j + 1}"}); n += 1
cert_items = [{"code": f"{a}.{b}", "title": f"{t}: objective {b}"} for a, t, m in
              [(1, "Energy and metabolism", 6), (2, "Macromolecular structure and function", 5), (3, "Information storage and flow", 5)]
              for b in range(1, m + 1)]
STDS = [
    {"id": "asbmb-core-2013", "name": "ASBMB core concepts for biochemistry and molecular biology (Tansey et al., BAMBED 41:289, 2013)",
     "publisher": "American Society for Biochemistry and Molecular Biology", "kind": "standard", "read": "full",
     "url": "https://doi.org/10.1002/bmb.20727",
     "note": "Read through a summary of the paper (Nov 2026): five core concepts and their eighteen 'students should be able to' statements, numbered T1-T18 in concept order by us; the statements' own wording is not copied here.",
     "items": core_items},
    {"id": "asbmb-cert", "name": "ASBMB accreditation and certification exam: foundational concepts and learning objectives",
     "publisher": "American Society for Biochemistry and Molecular Biology", "kind": "exam-spec", "read": "part",
     "url": "https://www.asbmb.org/education/certification-exam",
     "note": "Concepts read on ASBMB's exam page and the numbered learning objectives (1.1-1.6, 2.1-2.5, 3.1-3.5) through their reproduction in the LibreTexts Fundamentals of Biochemistry (Jakubowski), Nov 2026; labels here name the concept area only.",
     "items": cert_items},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

# ---- skills -----------------------------------------------------------------------------------------------------
SK = [("acid-base", "Buffers, pKa shifts and peptide charge", "Acid–base"), ("proteins", "Protein structure and folding energetics", "Protein folding"),
      ("binding", "Ligand binding, cooperativity and allostery", "Binding"), ("enzymes", "Enzyme kinetics, inhibition and catalysis", "Enzymes"),
      ("bioenergetics", "Free energy, coupling and redox in the cell", "Bioenergetics"), ("membranes", "Membranes and transport energetics", "Membranes"),
      ("metabolism", "Metabolic pathways, yields and regulation", "Metabolism"), ("nucleic-acids", "DNA, mutation, expression and PCR", "Nucleic acids"),
      ("signalling", "Signal transduction and amplification", "Signalling"), ("methods", "Quantitation, electrophoresis and purification", "Methods"),
      ("evolution", "Molecular evolution and steady states", "Evolution")]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("biochem.acid-base" in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: biochem," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: biochem.{a}, domain: biochem, title: {q(b)}, short: {q(c)} }}' for a, b, c in SK]
    open(p, "w").write("\n".join(L))

# ---- source -----------------------------------------------------------------------------------------------------
p = os.path.join(ROOT, "drills/sources/lehninger-8e.yaml")
if not os.path.exists(p):
    CH = [(2, "Water", "acid-base"), (3, "Amino acids, peptides and proteins", "methods"), (4, "The three-dimensional structure of proteins", "proteins"),
          (5, "Protein function", "binding"), (6, "Enzymes", "enzymes"), (8, "Nucleotides and nucleic acids", "nucleic-acids"),
          (11, "Biological membranes and transport", "membranes"), (12, "Biochemical signaling", "signalling"),
          (13, "Introduction to metabolism", "bioenergetics"), (14, "Glycolysis, gluconeogenesis and the pentose phosphate pathway", "metabolism"),
          (19, "Oxidative phosphorylation", "bioenergetics"), (26, "DNA metabolism", "nucleic-acids"), (28, "Regulation of gene expression", "nucleic-acids")]
    out = ["# Nelson & Cox, Lehninger Principles of Biochemistry, 8th ed. (2021). Chapter titles from memory (Nov 2026), not",
           "# checked against the book; mapped to the biochem.* skills of the Biochemistry framework (BC).",
           "id: lehninger-8e", 'title: "Nelson & Cox — Lehninger Principles of Biochemistry, 8th ed."', 'short: "Lehninger 8e"',
           "year: 2021", "field: biochemistry", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(ti)}, skills: [biochem.{s}] }}' for n, ti, s in CH]
    out += ['  - { n: 1, title: "The foundations of biochemistry", skills: [biochem.evolution] }']
    open(p, "w").write("\n".join(out) + "\n")

# ---- framework --------------------------------------------------------------------------------------------------
p = os.path.join(ROOT, "drills/frameworks/biochemistry.yaml")
if not os.path.exists(p):
    out = ["# Biochemistry — curriculum framework (draft 1, for Kevin's markup)", "#",
           "# Basis: the ASBMB core concepts (Tansey et al. 2013; five concepts, eighteen statements numbered T1-T18 by us) and",
           "# the ASBMB exam's numbered learning objectives, both read through summaries; the AAMC MCAT outline (1A-1D, 5A-5E) as",
           "# also. Objectives and their order are a house list in Lehninger's chapter order, pitched quantitatively for protein",
           "# design: folding and binding free energies, ΔΔG of mutations, enzyme kinetics and inhibition, bioenergetics.",
           "# Structures drawn from memory live in Structures (ST); this framework drills reasoning and numbers.",
           "id: biochemistry", "title: Biochemistry", "code: BC", "draft: 1", "track: science", "requires: [chemistry, biology]",
           "level: 4", "domains: [biochem]", "", "basis:", "  primary: asbmb-core-2013", "  also: [asbmb-cert, aamc-mcat-outline]",
           '  note: "Concepts and statements from ASBMB (core concepts paper and exam objectives); the objective list is ours."', "",
           "big_ideas:"]
    for i, ti, tx in bc.IDEAS:
        out += [f"  - id: {i}", f"    title: {ti}", f"    text: {tx}"]
    out += ["", "practices:", "  - id: P1", "    title: Compute", "    text: Carry the calculation to a number with units.",
            "  - id: P2", "    title: Reason", "    text: Predict or explain an outcome from structure, energetics or regulation.", "", "units:"]
    for n, (uid, ti, std, ideas, topics) in bc.UNITS.items():
        out += [f"  - id: {uid}", f"    n: {n}", f"    title: {q(ti)}", f"    std: {fl(std)}", "    scope: core",
                f"    ideas: [{', '.join(ideas)}]", "    topics:"]
        for tn, (tt, los) in topics.items():
            out += [f"      - n: {tn}", f"        title: {q(tt)}", "        los:"]
            for lid, lstd, do, ek, pr in los:
                out.append(f"          - {{ id: {lid}, std: {fl(lstd)}, do: {q(do)}, ek: [{q(ek)}], p: [{pr}], drills: [] }}")
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
