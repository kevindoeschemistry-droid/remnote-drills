"""Write the Electronic Structure framework (QC) from scripts/second_specs/qc.py: the three standards it rests on, the
qchem.* drill skills, the domain and library subject, the Psi4NumPy "source", and the framework file itself.
Idempotent; nothing is overwritten once it exists. Then run second_types.py to fill the drills.
Usage: python3 scripts/qc_framework.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import qc

q = lambda s: json.dumps(s, ensure_ascii=False)
fl = lambda xs: "[" + ", ".join(q(x) for x in xs) + "]"

PSI_ITEMS = [("01", "Psi4NumPy basics: molecules, wavefunctions and integrals"),
             ("03a", "Restricted Hartree-Fock"), ("03b", "Direct inversion of the iterative subspace"),
             ("03c", "Unrestricted Hartree-Fock"), ("03d", "Restricted open-shell Hartree-Fock"),
             ("04a", "Density functional theory: grids and quadrature"), ("04b", "LDA kernel"),
             ("04c", "GGA and meta-GGA kernels"), ("04d", "VV10 non-local correlation"), ("04e", "DFT with exact exchange"),
             ("05a", "Conventional MP2"), ("05b", "Density-fitted MP2"),
             ("06", "Molecular properties: dipoles, polarisabilities and response"),
             ("07", "Symmetry-adapted perturbation theory"), ("08", "CEPA0 and coupled-cluster doubles"),
             ("11", "One- and two-electron integrals and density fitting")]
QM_ITEMS = [("1", "Geometry optimisation"), ("2", "Intramolecular potential energy surfaces"),
            ("3", "Intermolecular potential energy surfaces"), ("4", "Basis-set convergence of geometries"),
            ("5", "Basis-set convergence of vibrational frequencies"), ("6", "Standard redox potentials"),
            ("7", "Version control for computational projects")]
SO_ITEMS = [("1", "Mathematical review and notation"), ("2", "Many-electron wavefunctions and operators"),
            ("3", "The Hartree-Fock approximation"), ("4", "Configuration interaction"),
            ("5", "Pair and coupled-pair theories"), ("6", "Many-body perturbation theory"),
            ("7", "The one-particle Green's function")]
STDS = [
 {"id": "psi4numpy-tutorials", "name": "Psi4NumPy interactive tutorials (Smith et al., JCTC 14 (2018) 3504)",
  "publisher": "The Psi4 project / American Chemical Society", "kind": "course", "read": "part",
  "url": "https://github.com/psi4/psi4numpy",
  "note": "The module numbering and titles were confirmed in Nov 2026 from the project README, a port's module-by-module progress list and a documentation wiki. The notebooks themselves were not run and the companion paper's text was not read, so the objectives under each module are ours. Item titles paraphrase the module titles.",
  "items": [{"code": c, "title": t} for c, t in PSI_ITEMS]},
 {"id": "molssi-qm-tools", "name": "MolSSI Education, Quantum Mechanics Tools (lesson)",
  "publisher": "The Molecular Sciences Software Institute", "kind": "course", "read": "full",
  "url": "https://education.molssi.org/qm-tools/",
  "note": "All seven episodes read from the lesson page in Nov 2026. Episodes 1-6 are in scope; the version-control episode is covered by the Programming framework, not here. The lesson publishes episode titles and objectives but no assessment, so it fixes scope rather than depth.",
  "items": [{"code": c, "title": t} for c, t in QM_ITEMS]},
 {"id": "szabo-ostlund", "name": "Szabo & Ostlund, Modern Quantum Chemistry (Dover, 1996)",
  "publisher": "Dover Publications", "kind": "textbook", "read": "none",
  "url": "https://store.doverpublications.com/products/9780486691862",
  "note": "Chapter structure written from memory, so this is a textbook crosswalk and not a curriculum: it is never cited on an item, only listed as the standard reference for the theory behind the Hartree-Fock and correlation units.",
  "items": [{"code": c, "title": t} for c, t in SO_ITEMS]},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t and f'id: {s["id"]},' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

SK = [("orbitals", "Electron counts, determinants, spin states and method labels", "Orbitals and references", []),
      ("hartree-fock", "The SCF procedure, its energy pieces, convergence and what it misses", "Hartree-Fock",
       ["qchem.orbitals"]),
      ("basis", "Basis-set composition, polarisation and diffuse functions, convergence and superposition error",
       "Basis sets", ["qchem.hartree-fock"]),
      ("correlation", "Perturbation theory, coupled cluster, configuration interaction and interaction-energy decomposition",
       "Correlation methods", ["qchem.basis"]),
      ("dft", "Functional families, exact exchange, dispersion corrections and numerical grids", "Density functional theory",
       ["qchem.hartree-fock"]),
      ("properties", "Geometries, frequencies, derived properties and reporting a calculation", "Geometries and properties",
       ["qchem.correlation"])]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
if not any("id: qchem," in ln for ln in L):
    i = next(k for k, ln in enumerate(L) if "id: cpd," in ln)
    L.insert(i + 1, '  - { id: qchem, title: "Electronic structure" }')
if not any("qchem.orbitals" in ln for ln in L):
    i = max(k for k, ln in enumerate(L) if "domain: cpd," in ln)
    L[i + 1:i + 1] = [f'  - {{ id: qchem.{a}, domain: qchem, title: {q(b)}, short: {q(c)}'
                      + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in SK]
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
if not any(ln.strip() == '- "Electronic Structure"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Protein Design"')
    L.insert(i + 1, '  - "Electronic Structure"')
if not any(ln.startswith("  qchem:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  cpd:"))
    L.insert(i + 1, '  qchem: "Electronic Structure"')
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/sources/psi4numpy.yaml")
if not os.path.exists(p):
    CH = [(1, "Psi4NumPy basics: molecules, wavefunctions and integrals", "orbitals"),
          (3, "Hartree-Fock: RHF, DIIS, UHF and ROHF", "hartree-fock"),
          (11, "One- and two-electron integrals and density fitting", "basis"),
          (5, "Moller-Plesset perturbation theory", "correlation"),
          (8, "CEPA0 and coupled-cluster doubles", "correlation"),
          (4, "Density functional theory: grids, kernels and exact exchange", "dft"),
          (6, "Molecular properties and response", "properties"),
          (7, "Symmetry-adapted perturbation theory", "correlation")]
    out = ["# The Psi4NumPy interactive tutorial modules (psi4/psi4numpy), read as a module list in Nov 2026 and mapped",
           "# to the qchem.* skills of the Electronic Structure framework (QC). Modules 02, 09, 10 and 12 and up are not",
           "# drilled here. Chapter numbers follow the module numbering, not a book.",
           "id: psi4numpy", 'title: "Psi4NumPy interactive tutorials"', 'short: "Psi4NumPy"',
           "year: 2018", "field: computational-chemistry", "chapters:"]
    out += [f'  - {{ n: {n}, title: {q(ti)}, skills: [qchem.{s}] }}' for n, ti, s in CH]
    open(p, "w").write("\n".join(out) + "\n")

p = os.path.join(ROOT, "drills/frameworks/electronic-structure.yaml")
if not os.path.exists(p):
    out = ["# Electronic Structure — curriculum framework (draft 1, for Kevin's markup)", "#",
           "# The method side of computational chemistry: what a Hartree-Fock, post-Hartree-Fock or DFT calculation is,",
           "# what each approximation costs, and how to read and report one. Molecular Simulation (MD) keeps the",
           "# classical-dynamics and free-energy side; Protein Design (CPD) keeps the structure-prediction side. The three",
           "# meet when a design decision needs a quantum number: a barrier, a charge or a spectroscopic property.",
           "#",
           "# Basis: the Psi4NumPy tutorial modules (module list read; published as a JCTC paper and used as a teaching",
           "# set) as primary, with MolSSI's Quantum Mechanics Tools lesson (read in full) as also. Szabo & Ostlund is",
           "# listed as the theory reference but is never cited on an item, since its chapters were written from memory.",
           "# No accredited standard covers this subject at graduate level, so the objectives and their order are a house",
           "# list; the ramp runs counting and notation -> Hartree-Fock -> basis sets -> correlation -> DFT -> properties.",
           "#", "# Relativistic methods, multireference methods (CASSCF, MRCI) and periodic DFT are out of scope for draft 1",
           "# and are named as such rather than half-covered.",
           "id: electronic-structure", "title: Electronic Structure", "code: QC", "draft: 1", "track: science",
           "requires: [chemistry, molecular-simulation]", "level: 5", "domains: [qchem]", "", "basis:",
           "  primary: psi4numpy-tutorials", "  also: [molssi-qm-tools, szabo-ostlund]",
           '  note: "No accredited standard exists at this level. The Psi4NumPy modules are the closest published curriculum and the MolSSI lesson fixes the practical units; Szabo & Ostlund is a theory reference only. Objectives are ours."',
           "", "big_ideas:"]
    for i, ti, tx in qc.IDEAS:
        out += [f"  - id: {i}", f"    title: {q(ti)}", f"    text: {q(tx)}"]
    out += ["", "practices:", "  - id: P1", "    title: Compute",
            "    text: " + q("Carry the calculation to a number with units, and say what it does not settle."),
            "  - id: P2", "    title: Decide",
            "    text: " + q("Choose a method, basis or protocol for a stated problem, and name the failure it avoids."),
            "", "units:"]
    for n, (uid, ti, std, ideas, topics) in qc.UNITS.items():
        out += [f"  - id: {uid}", f"    n: {n}", f"    title: {q(ti)}", f"    std: {fl(std)}", "    scope: core",
                f"    ideas: [{', '.join(ideas)}]", "    topics:"]
        for tn, (tt, los) in topics.items():
            out += [f"      - n: {tn}", f"        title: {q(tt)}", "        los:"]
            for lid, lstd, do, ek, pr in los:
                out.append(f"          - {{ id: {lid}, std: {fl(lstd)}, do: {q(do)}, ek: [{q(ek)}], p: [{pr}], drills: [] }}")
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
