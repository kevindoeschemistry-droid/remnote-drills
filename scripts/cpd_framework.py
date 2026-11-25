"""Write the Computational Protein Design framework (CPD) from scripts/second_specs/cpd.py: the five standards it
rests on, the design.* drill skills, the domain and library subject, the PyRosetta workshop "source", and the
framework file itself. Idempotent; nothing is overwritten once it exists. Then run second_types.py to fill the drills.
Usage: python3 scripts/cpd_framework.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import cpd

q = lambda s: json.dumps(s, ensure_ascii=False)
fl = lambda xs: "[" + ", ".join(q(x) for x in xs) + "]"

# ---- standards --------------------------------------------------------------------------------------------------
PN_ITEMS = [("1", "Getting started"), ("2", "Introduction to PyRosetta: poses, residues, geometry, visualisation"),
            ("2.1", "Pose basics"), ("2.2", "Working with pose residues"), ("2.4", "Spatial features of a pose"),
            ("2.5", "Protein geometry"), ("3", "Energy score functions"), ("4.1", "Basic folding algorithm"),
            ("4.2", "Low-resolution scoring and fragments"), ("5.1", "High-resolution movers"), ("5.2", "Refinement protocol"),
            ("6.1", "Side-chain conformations and Dunbrack energies"), ("6.2", "Packing and relax"),
            ("6.3", "Design with a resfile and FastRelax"), ("6.4", "Protein design 2"), ("6.5", "Hydrogen-bond networks before design"),
            ("6.6", "De novo parametric backbone design"), ("6.7", "De novo protein design"), ("6.8", "Point mutation scan"),
            ("7.1", "Fourier-transform-based docking"), ("7.2", "Docking moves"), ("8.1", "Global ligand docking"),
            ("8.2", "Ligand docking with a Cartesian score function"), ("9.1", "Loop modelling with generalised kinematic closure"),
            ("10", "Symmetry"), ("11", "Working with density"), ("12.1", "Antibody framework modelling"),
            ("12.2", "Antibody design"), ("13", "Carbohydrates"), ("14", "RNA"), ("15.1", "Setting up a membrane protein"),
            ("15.2", "Predicting ΔΔG of single point mutations"), ("16", "Running in parallel and reproducible distribution")]
RF_ITEMS = [("form", "The score as a weighted linear sum of terms"), ("table", "The terms and their published weights"),
            ("ref", "Per-amino-acid reference energies and their role in design"),
            ("units", "Units: parameterisation in kcal/mol rather than arbitrary energy units"),
            ("guidance", "Interpreting energies: per-term decomposition, residue and atom-pair tables, ΔΔG of mutation, interface energies"),
            ("fa_dun", "Backbone-dependent rotamer energy")]
DL_ITEMS = [("WS01", "Neural networks from scratch"), ("WS02", "Neural networks in a framework"),
            ("WS03", "Convolutional networks"), ("WS04", "Language models for text and protein sequences"),
            ("WS05", "Language-model embeddings and transfer learning"), ("WS06", "Structure prediction as a black box: inputs and confidence metrics"),
            ("WS07", "Graph neural networks for proteins"), ("WS08", "Denoising diffusion models"),
            ("WS09", "End-to-end design: diffusion, inverse folding and structure prediction"),
            ("WS10", "All-atom diffusion for small-molecule binders")]
KB_ITEMS = [("1", "Introduction: prediction and the inverse problem"), ("2", "Navigating energy landscapes: minimisation, Monte Carlo, molecular dynamics"),
            ("3", "Folding forces, energy functions and multi-resolution modelling"),
            ("4", "Structure prediction: templates, fragments, coevolution, deep learning"),
            ("5", "Protein design: de novo, template-based, sequence optimisation, negative and multi-state, interfaces, ligands"),
            ("6", "Validating computational predictions"), ("7", "Applications and open challenges")]
STDS = [
    {"id": "pyrosetta-notebooks", "name": "PyRosetta Jupyter Notebooks (RosettaCommons), taught as JHU 545.614 / 540.414",
     "publisher": "Rosetta Commons / Gray lab, Johns Hopkins University", "kind": "course", "read": "part",
     "url": "https://github.com/RosettaCommons/PyRosetta.notebooks",
     "note": "The complete table of contents (16 chapters and every notebook title) was read from the repository page in Nov 2026; the notebooks themselves were not run, so the objectives under each are ours. Published as Le et al., The Biophysicist 2 (2021) 108, which reports over ten years of use as a university course. Item titles paraphrase the notebook titles.",
     "items": [{"code": c, "title": t} for c, t in PN_ITEMS]},
    {"id": "rosetta-ref15", "name": "Alford et al., The Rosetta all-atom energy function for macromolecular modeling and design, JCTC 13 (2017) 3031",
     "publisher": "American Chemical Society", "kind": "reference", "read": "part",
     "url": "https://doi.org/10.1021/acs.jctc.7b00125",
     "note": "Read from the open copy at core.ac.uk (Nov 2026): the functional form, every term, the weight table, the reference energies, the units and the guidance on interpreting energies. The later protocol captures and the supporting information were not read. The paper calls the function beta_nov15, which became the default as REF2015.",
     "items": [{"code": c, "title": t} for c, t in RF_ITEMS]},
    {"id": "dl4proteins", "name": "Chungyoun et al., DL4Proteins Jupyter Notebooks (Gray lab), arXiv 2511.02128",
     "publisher": "Gray lab, Johns Hopkins University", "kind": "course", "read": "part",
     "url": "https://arxiv.org/abs/2511.02128",
     "note": "The ten workshop titles and what each covers were read in full from the paper (Nov 2026); the notebooks were not run. Items are the ten workshops, paraphrased.",
     "items": [{"code": c, "title": t} for c, t in DL_ITEMS]},
    {"id": "kuhlman-bradley", "name": "Kuhlman & Bradley, Advances in protein structure prediction and design, Nat Rev Mol Cell Biol 20 (2019) 681",
     "publisher": "Springer Nature", "kind": "reference", "read": "part",
     "url": "https://doi.org/10.1038/s41580-019-0163-x",
     "note": "Section outline and key concepts read from the PMC copy (Nov 2026), through the applications and outlook; the boxes' full text and the reference list were not read. Items are its sections, paraphrased.",
     "items": [{"code": c, "title": t} for c, t in KB_ITEMS]},
    {"id": "jhu-545614", "name": "Johns Hopkins 545.614 Computational Protein Structure Prediction and Design (course topic list)",
     "publisher": "Johns Hopkins University", "kind": "course", "read": "part",
     "url": "https://ep.jhu.edu/courses/545614-computational-protein-structure-prediction-and-design/",
     "note": "The public course page's description and topic list were read (Nov 2026): folding and docking, design of ligand-binding sites, turns and folds, and interfaces, taught with PyRosetta. No syllabus, assessment or learning outcomes are published, so this is a scope check rather than a basis.",
     "items": [{"code": "T1", "title": "Protein folding and docking"}, {"code": "T2", "title": "Design of ligand-binding sites"},
               {"code": "T3", "title": "Design of turns and folds"}, {"code": "T4", "title": "Design of protein interfaces"},
               {"code": "T5", "title": "Structure, biophysics, optimisation and informatics underlying the field"}]},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t and f'id: {s["id"]},' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

# ---- skills -----------------------------------------------------------------------------------------------------
SK = [("structure", "Protein geometry, dihedrals and rotamers", "Geometry and rotamers", []),
      ("representation", "Poses, numbering and coarse-grained versus all-atom models", "Representation", ["design.structure"]),
      ("energy", "All-atom energy terms, weights, reference energies and reading a score", "Energy function", ["design.representation"]),
      ("sampling", "Monte Carlo, annealing, packing, minimisation and relax", "Sampling and packing", ["design.energy"]),
      ("sequence", "Design specifications, mutational scans and sequence optimisation", "Sequence design", ["design.sampling"]),
      ("interfaces", "Docking, interface energies and binding-site design", "Interfaces and ligands", ["design.sequence"]),
      ("denovo", "De novo backbones, hydrogen-bond networks and negative design", "De novo design", ["design.sequence"]),
      ("ml", "Learned structure prediction, inverse folding and diffusion design", "Deep learning for design", ["design.representation"]),
      ("validation", "Testing designs and choosing between a score and a free energy", "Validation", ["design.sequence"])]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("id: cpd," in ln for ln in L):
    i = next(k for k, ln in enumerate(L) if "id: compchem," in ln)
    L.insert(i + 1, '  - { id: cpd, title: "Computational protein design" }')
if not any("design.structure" in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: md," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: design.{a}, domain: cpd, title: {q(b)}, short: {q(c)}'
                      + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in SK]
open(p, "w").write("\n".join(L))

# ---- library (subject + domain) ---------------------------------------------------------------------------------
p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
if not any(ln.strip() == '- "Protein Design"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Computational Chemistry"')
    L.insert(i + 1, '  - "Protein Design"')
if not any(ln.startswith("  cpd:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  compchem:"))
    L.insert(i + 1, '  cpd: "Protein Design"')
open(p, "w").write("\n".join(L))

# ---- source (the PyRosetta workshops, as a "textbook" of chapters) ----------------------------------------------
p = os.path.join(ROOT, "drills/sources/pyrosetta-workshops.yaml")
if not os.path.exists(p):
    CH = [(2, "Introduction to PyRosetta: poses and geometry", "representation"), (3, "Energy score functions", "energy"),
          (2.5, "Protein geometry and rotamers", "structure"), (6.9, "Learned prediction and design pipelines", "ml"),
          (4, "Introduction to folding", "sampling"), (5, "Structure refinement", "sampling"),
          (6, "Packing and design", "sequence"), (7, "Docking", "interfaces"), (8, "Ligand refinement", "interfaces"),
          (9, "Loop modelling", "denovo"), (12, "Working with antibodies", "interfaces"),
          (15, "Modelling membrane proteins", "validation"), (16, "Running Rosetta in parallel", "validation")]
    out = ["# The PyRosetta Jupyter Notebook workshops (RosettaCommons/PyRosetta.notebooks), read as a table of contents in",
           "# Nov 2026 and mapped to the design.* skills of the Computational Protein Design framework (CPD). Chapter 1 is",
           "# installation and chapters 10, 11, 13 and 14 (symmetry, density, carbohydrates, RNA) are not drilled here.",
           "id: pyrosetta-workshops", 'title: "PyRosetta Jupyter Notebook workshops"', 'short: "PyRosetta notebooks"',
           "year: 2021", "field: protein-design", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(ti)}, skills: [design.{s}] }}' for n, ti, s in CH]
    open(p, "w").write("\n".join(out) + "\n")

# ---- framework --------------------------------------------------------------------------------------------------
p = os.path.join(ROOT, "drills/frameworks/protein-design.yaml")
if not os.path.exists(p):
    out = ["# Computational Protein Design — curriculum framework (draft 1, for Kevin's markup)", "#",
           "# Built for a protein-design PhD track: the structure-prediction-and-design side of the work that the",
           "# Molecular Simulation framework (MD) covers from the free-energy side. The two meet in unit 9, where a",
           "# score-function ΔΔG hands over to an alchemical calculation.",
           "#",
           "# Basis: the PyRosetta notebook workshops (table of contents read in full; taught as a JHU course for over ten",
           "# years) as primary, with the all-atom energy function paper, the DL4Proteins workshops, the Kuhlman & Bradley",
           "# review and the JHU course topic list as also. No accredited standard exists for this subject, so the",
           "# objectives and their order are a house list; the ramp runs geometry → representation → energy → sampling →",
           "# sequence → interfaces → de novo → deep learning → validation.",
           "#", "# Experimental methods, crystallography and wet-lab protocol live outside this framework; unit 9 covers",
           "# only what a designer must know to plan and read the experiments.",
           "id: protein-design", "title: Computational Protein Design", "code: CPD", "draft: 1", "track: science",
           "requires: [biochemistry, molecular-simulation]", "level: 5", "domains: [cpd]", "", "basis:",
           "  primary: pyrosetta-notebooks", "  also: [rosetta-ref15, dl4proteins, kuhlman-bradley, jhu-545614]",
           '  note: "No accredited standard exists. The notebook workshops are the closest published curriculum; the energy-function paper, the deep-learning workshops and the review fix the content of the later units. Objectives are ours."',
           "", "big_ideas:"]
    for i, ti, tx in cpd.IDEAS:
        out += [f"  - id: {i}", f"    title: {q(ti)}", f"    text: {q(tx)}"]
    out += ["", "practices:", "  - id: P1", "    title: Compute",
            "    text: " + q("Carry the calculation to a number with units, and say what it does not settle."),
            "  - id: P2", "    title: Decide",
            "    text: " + q("Choose a representation, protocol or method for a stated problem, and name the failure it avoids."), "", "units:"]
    for n, (uid, ti, std, ideas, topics) in cpd.UNITS.items():
        out += [f"  - id: {uid}", f"    n: {n}", f"    title: {q(ti)}", f"    std: {fl(std)}", "    scope: core",
                f"    ideas: [{', '.join(ideas)}]", "    topics:"]
        for tn, (tt, los) in topics.items():
            out += [f"      - n: {tn}", f"        title: {q(tt)}", "        los:"]
            for lid, lstd, do, ek, pr in los:
                out.append(f"          - {{ id: {lid}, std: {fl(lstd)}, do: {q(do)}, ek: [{q(ek)}], p: [{pr}], drills: [] }}")
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
