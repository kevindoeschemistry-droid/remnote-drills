#!/usr/bin/env python3
"""Complex analysis past Engineering Math unit 14: register the basis and the two skills unit 15 needs.

Basis: the Cambridge Mathematical Tripos Part IB Complex Analysis schedule, read in full as reproduced at the head
of a student's published lecture notes: four blocks (analytic functions; contour integration and Cauchy's theorem;
expansions and singularities; the residue theorem). The MAA CUPM 2015 course-area report on complex analysis is
registered as wanted: its PDF would not load (Nov 2026). Text edits only; idempotent.
"""
import json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
ST, SK = ROOT / "drills/standards.yaml", ROOT / "drills/skills.yaml"
SRC, FW = ROOT / "drills/sources/kreyszig-10e.yaml", ROOT / "drills/frameworks/engineering-math.yaml"
IB = {"id": "cambridge-ib-complex", "name": "Cambridge Mathematical Tripos Part IB, Complex Analysis schedule",
      "publisher": "University of Cambridge, Faculty of Mathematics", "kind": "course", "read": "full",
      "url": "https://dec41.user.srcf.net/notes/IB_L/complex_analysis.pdf",
      "note": "Read Nov 2026: the whole schedule (four blocks, 16 lectures) as reproduced at the head of a student's published lecture notes; the lectures themselves were not read. A proof-based course, so its theorems are drilled here as what they let you compute. Items are the four blocks, titled in our words.",
      "items": [{"code": "A", "title": "Analytic functions: complex differentiation, Cauchy-Riemann, conformal maps, branch points of log z and z^c"},
                {"code": "C", "title": "Contour integration and Cauchy's theorem: contour integrals, Cauchy's theorem and integral formula, maximum modulus, Liouville, the fundamental theorem of algebra, Morera"},
                {"code": "S", "title": "Expansions and singularities: Taylor and Laurent expansions, isolated zeros, residues, classifying isolated singularities"},
                {"code": "R", "title": "The residue theorem: winding numbers, the residue theorem, Jordan's lemma, definite integrals, Rouche and the argument principle"}]}
CUPM = {"id": "cupm-2015-complex", "name": "MAA CUPM Curriculum Guide 2015, Complex Analysis course area report",
        "publisher": "Mathematical Association of America", "kind": "standard", "read": "none"}
t = ST.read_text()
for s in (IB, CUPM):
    if f'"id": "{s["id"]}"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"; print("  added", s["id"])
ST.write_text(t); yaml.safe_load(ST.read_text())
t = SK.read_text()
if "id: cplx.contour" not in t:
    anchor = [l for l in t.split("\n") if l.startswith("  - { id: cplx.series,")][0]
    t = t.replace(anchor, anchor + '\n  - { id: cplx.conformal, domain: calc, title: "Conformal maps, Möbius maps and branches of log and powers", short: "Conformal maps", prereqs: [cplx.analytic] }\n  - { id: cplx.contour, domain: calc, title: "Contour integration, Cauchy\'s theorems, residues and real integrals", short: "Contours and residues", prereqs: [cplx.series] }')
    SK.write_text(t); print("  skills: cplx.conformal, cplx.contour")
t = SRC.read_text()
if "cplx.contour" not in t:
    t = t.replace('    title: "Laurent Series. Residue Integration"\n    skills: [cplx.series]', '    title: "Laurent Series. Residue Integration"\n    skills: [cplx.series, cplx.contour]\n  - n: 17\n    title: "Conformal Mapping"\n    skills: [cplx.conformal]')
    assert "cplx.contour" in t; SRC.write_text(t); print("  kreyszig: ch 16 += cplx.contour, ch 17 conformal (title from memory)")
t = FW.read_text()
if "cambridge-ib-complex" not in t:
    old = "also: [fe-chemical, webwork-opl]"
    assert old in t, "EM basis line not found"
    t = t.replace(old, "also: [fe-chemical, webwork-opl, cambridge-ib-complex]\n  wanted: [cupm-2015-complex]", 1)
    FW.write_text(t); print("  engineering-math basis: also cambridge-ib-complex, wanted cupm-2015-complex")
yaml.safe_load(FW.read_text())
