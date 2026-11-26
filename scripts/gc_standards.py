#!/usr/bin/env python3
"""Rebase Graduate ChemE off UCI's catalogue descriptions.

No published standard maps graduate chemical engineering content. ABET covers undergraduate programmes only; the
Engineering Council's AHEP4 master's outcomes (M1-M18) are competency statements with no technical content; AIChE's
Body of Knowledge is staged by career rather than by degree and says so. The two things that do exist:

  icheme-level-f  the only accreditation standard that formally separates master's-level chemical engineering from
                  bachelor's. Its Level F outcomes are written as extensions of the Level B column, so they anchor
                  depth rather than new topics: the same principles on more complex problems, with the limits of the
                  assumptions and of commercial software interrogated. That is what a graduate core course is.

  cheme-grad-core OUR crosswalk of fifteen departments' published core-course requirements. Labelled a house list
                  because it is one: the fifteen pages are published, the synthesis is ours.

aiche-bok is registered too, but it belongs on Process Design (plant practice, career stages), not here.

Append-only and idempotent. standards.yaml is written one flow-style entry per line and carries a comment header,
so this script appends text rather than round-tripping the file through yaml.safe_dump: a dump reflows all 95
entries and silently dropped psi4numpy-tutorials item "08" when it unquoted the code.
"""
import json, pathlib, re, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ST = ROOT / "drills" / "standards.yaml"
FW = ROOT / "drills" / "frameworks"

# Fifteen departments whose published graduate core-course requirements were read in full (Nov 2026). The count on
# each item is how many of the fifteen require that course; a department that publishes only a partial core set
# (Minnesota names two core courses, Houston marks two as core) is counted only where its page actually says so.
DEPTS = ("Carnegie Mellon, Northwestern, Michigan Tech, NC State, UMass Lowell, NJIT, Colorado State, "
         "Wisconsin-Madison, Rhode Island, Minnesota, Houston, Tufts, Puerto Rico-Mayaguez, Illinois Chicago "
         "and Drexel")

CROSSWALK = {
    "id": "cheme-grad-core",
    "name": "Graduate chemical engineering core curriculum (crosswalk of fifteen departments' published requirements)",
    "publisher": "house",
    "kind": "course",
    "read": "full",
    "url": "https://www.cheme.engineering.cmu.edu/education/graduate-programs/phd/phd-requirements.html",
    "note": (
        "A HOUSE LIST, and the reason is worth recording: no body publishes an itemised graduate chemical "
        "engineering content standard. ABET's programme criteria are undergraduate. AHEP4's master's outcomes are "
        "competency statements with no technical content. AIChE's Body of Knowledge is staged by career, not by "
        "degree, and states that students heading to graduate school share Stage 1 skills with new hires. So this "
        "crosswalk is ours, synthesised Nov 2026 from the published core-course requirements and preliminary-exam "
        "pages of fifteen US departments (" + DEPTS + "), each read in full. The convergence is the finding: four "
        "courses recur almost everywhere and a fifth at one. Counts per item say how many of the fifteen require "
        "it. Topic sub-items come from the course descriptions those same pages give, not from any syllabus. "
        "Berkeley's preliminary-exam page names the texts per area (Bird Stewart & Lightfoot, Denn and Cussler for "
        "transport; Fogler for kinetics; Smith & Van Ness, Koretsky and Elliott & Lira for thermodynamics) and "
        "those thermodynamics texts are undergraduate, which matches Drexel's and Montana's statements that their "
        "qualifying exams test undergraduate chemical engineering. FE Chemical already closes that layer, so this "
        "crosswalk is scoped to the graduate coursework above it."
    ),
    "items": [
        {"code": "MM", "title": "Mathematical methods / applied mathematics for chemical engineers (15 of 15)"},
        {"code": "MM.1", "title": "Scaling and non-dimensionalisation; which terms a limit lets you drop"},
        {"code": "MM.2", "title": "Perturbation and asymptotic methods; regular and singular limits, boundary layers"},
        {"code": "MM.3", "title": "Similarity solutions and combination of variables"},
        {"code": "MM.4", "title": "Eigenfunction expansions and Sturm-Liouville problems in non-Cartesian geometry"},
        {"code": "MM.5", "title": "Integral transforms and complex-variable methods"},
        {"code": "MM.6", "title": "Numerical and computer methods, and the limits of standard commercial software"},
        {"code": "TR", "title": "Advanced / intermediate transport phenomena (14 of 15)"},
        {"code": "TR.1", "title": "Equations of change for multicomponent, multiphase systems"},
        {"code": "TR.2", "title": "Creeping, laminar, viscous and inviscid flow; lubrication and boundary layers"},
        {"code": "TR.3", "title": "Coupled transport with chemical reaction"},
        {"code": "TH", "title": "Advanced chemical engineering thermodynamics (14 of 15)"},
        {"code": "TH.1", "title": "Equilibrium and stability criteria"},
        {"code": "TH.2", "title": "Equations of state and real mixtures; phase and chemical equilibria"},
        {"code": "TH.3", "title": "Classical and statistical thermodynamics of real fluids"},
        {"code": "KN", "title": "Advanced kinetics and reactor design (11 of 15)"},
        {"code": "KN.1", "title": "Reactor stability and multiplicity"},
        {"code": "KN.2", "title": "Diffusion in heterogeneous catalysis; catalysis and surface processes"},
        {"code": "KN.3", "title": "Optimal operation and dispersed-phase reactors"},
        {"code": "PS", "title": "Advanced process systems engineering (1 of 15; Carnegie Mellon)"},
        {"code": "PS.1", "title": "Process dynamics, measurement and control"},
        {"code": "PS.2", "title": "Separations past the graphical constructions"},
        {"code": "PS.3", "title": "Process modelling, systems thinking and optimisation"},
    ],
}

ICHEME = {
    "id": "icheme-level-f",
    "name": "IChemE Accreditation of Chemical Engineering Programmes, Appendix A Level F (advanced / Other Master's)",
    "publisher": "Institution of Chemical Engineers",
    "kind": "standard",
    "read": "part",
    "url": "https://www.icheme.org/media/26729/university-accreditation-guide.pdf",
    "note": (
        "Read Nov 2026 from IChemE's own accreditation guide: sections 3.6, 3.7, 4.1.4 and 4.2.1 and the Level F "
        "column of Appendix A. The only accreditation standard that formally distinguishes master's-level chemical "
        "engineering from bachelor's. Its Level F outcomes are written as extensions of the Level B column rather "
        "than as new topics, so what they anchor is DEPTH: applying the same underlying principles to more complex "
        "problems while critically evaluating the limits of the assumptions made, and selecting and adapting "
        "computational techniques while recognising the limits of standard commercial software. Section 3.7 defines "
        "'complex' as problems with many interacting factors needing deep understanding. The Level B content "
        "columns the outcomes build on are already covered by FE Chemical, so these seven codes are cited here for "
        "the level, not for the topics. The guide's Appendix A text is jumbled where the A2.3/A2.4 and A2.5/A2.6 "
        "columns sit side by side, so read is 'part': outcomes were matched to codes by content, and the "
        "application documents were not read."
    ),
    "items": [
        {"code": "A1", "title": "Level F: comprehensive mathematics and science, shown by application to complex problems"},
        {"code": "A2.2", "title": "Level F fundamentals: the same underlying principles on more complex problems, with the limits of the assumptions critically evaluated"},
        {"code": "A2.3", "title": "Level F modelling: select and adapt computational and analytical techniques; recognise the limits of standard commercial software"},
        {"code": "A2.4", "title": "Level F process and product technology: complex and novel unit operations, and problems with conflicting requirements"},
        {"code": "A2.5", "title": "Level F systems: combine and adapt systems thinking for complex and novel processes"},
        {"code": "A2.6", "title": "Level F process safety: the same principles with systems thinking on more complex problems; limits of current and emerging technology"},
        {"code": "A2.7", "title": "Level F sustainability, economics and ethics applied to novel and complex situations with conflicting requirements"},
    ],
}

AICHE = {
    "id": "aiche-bok",
    "name": "AIChE Body of Knowledge for Chemical Engineers (2022 matrix)",
    "publisher": "American Institute of Chemical Engineers",
    "kind": "standard",
    "read": "part",
    "url": "https://www.aiche.org/sites/default/files/docs/pages/aiche_body_of_knowledge_2022.pdf",
    "note": (
        "Read Nov 2026: the matrix's structure, its seven subgroups and their counts, the four career stages, and "
        "the Chemical Engineering Technical Skills rows with their Chemical Process Industries ranks. The lead "
        "society's own body of knowledge, and the nearest chemical engineering analogue to the ACS content maps. "
        "Three Bloom domains over about 63 rows: 24 chemical engineering technical skills, 11 basic technical "
        "knowledge, 6 cross-functional, 8 human, 6 professional, 4 psychomotor, 4 beliefs and values. Rows are "
        "named, not numbered, so our codes below are ours. Grid cells hold ability ranks against four career "
        "stages (minimal experience, some experience, significant experience, expert), Stage 2 being the level the "
        "document names for professional licensure. It does NOT distinguish graduate from entry-level knowledge, "
        "which is why it anchors Process Design's plant practice rather than the graduate framework. The full "
        "matrix of ranks per industry column was not read."
    ),
    "items": [
        {"code": "T.BAL", "title": "Energy balances involving the first and second law; heat balances with and without reactions"},
        {"code": "T.EQ", "title": "Equilibria, chemical and phase"},
        {"code": "T.FLOW", "title": "Fluid flow; pump and compressor sizing and selection; packed beds"},
        {"code": "T.DES", "title": "Plant design: flow configuration and optimisation"},
        {"code": "T.INST", "title": "Plant design: instrumentation"},
        {"code": "T.OPT", "title": "Plant operations and optimisation"},
        {"code": "T.SU", "title": "Plant scale-up"},
        {"code": "X.SAFE", "title": "Cross-functional: safety analyses, modelling, procedural policies and regulations"},
    ],
}

GC_BASIS_OLD = """basis:
  primary: uci-cbe-core
  also: [pe-chemical]
  note: "UCI's graduate core courses by catalogue description (read in part); no syllabus or past comprehensive exam was read, so the objectives are ours. PE Chemical is the nearest published exam and stops below this level."
"""

GC_BASIS_NEW = """basis:
  primary: cheme-grad-core
  also: [icheme-level-f, uci-cbe-core, pe-chemical]
  note: "No body publishes an itemised graduate chemical engineering content standard, so the primary basis is our own crosswalk of fifteen departments' published core-course requirements, each read in full. IChemE Level F carries the level this framework sits at: its outcomes are the same principles on more complex problems with the limits of the assumptions interrogated. UCI's catalogue descriptions, which this framework used to rest on alone, are now one department among the fifteen. PE Chemical is the nearest published exam and stops below this level, and FE Chemical closes the undergraduate layer that several departments' qualifying exams actually test."
"""

UNIT_TITLES = [
    ('    title: "Momentum transport (CBE 220B)"', '    title: "Momentum transport"'),
    ('    title: "Heat and mass transport (CBE 220A)"', '    title: "Heat and mass transport"'),
    ('    title: "Advanced thermodynamics (CBE 240)"', '    title: "Advanced thermodynamics"'),
    ('    title: "Reaction engineering (CBE 210)"', '    title: "Advanced kinetics and reactor design"'),
    ('    title: "Process dynamics and control (CBE 200)"', '    title: "Process dynamics and control"'),
    ('    title: "Separations past the McCabe–Thiele diagram"',
     '    title: "Separations past the graphical constructions"'),
]

GC_HEADER = """# Graduate Chemical Engineering Core — curriculum framework (draft 2, for Kevin's markup)
#
# Basis: our own crosswalk of fifteen US departments' published graduate core-course requirements, each read in
# full (drills/standards.yaml, cheme-grad-core). Nobody publishes an itemised graduate chemical engineering
# content standard — ABET is undergraduate, AHEP4's master's outcomes carry no technical content, and AIChE's
# Body of Knowledge is staged by career rather than by degree and says so — so the crosswalk is labelled a house
# list. What the fifteen agree on: mathematical methods (15 of 15), advanced transport phenomena (14), advanced
# thermodynamics (14), advanced kinetics and reactor design (11), and process systems engineering (1).
#
# IChemE Level F sets the level rather than the topics: the same principles on more complex problems, with the
# limits of the assumptions and of commercial software interrogated. Several departments' qualifying exams test
# undergraduate material, which FE Chemical already closes, so this framework is scoped above it — the FE-level
# content lives in Fluid Mechanics, Heat Transfer, Mass Transfer, Thermodynamics, Reaction Engineering and
# Process Design, and the Kreyszig-level mathematics in Engineering Math.
#
# Draft 1 rested on UCI's five catalogue descriptions alone and named each unit after a course number, which
# attributed a process-control unit to CBE 200 — the applied-mathematics course. Unit codes are unchanged (the
# Library's RemNote ids are keyed by code), so the mathematical-methods unit the crosswalk opens is appended as
# unit 7 rather than inserted first. Generated by scripts/opl_fill.py from scripts/opl_specs/gc.py; the unit
# block below is replaced on every run.
"""


def flow(entry):
    """One standards.yaml entry, in the file's own one-line flow style."""
    return "- " + json.dumps(entry, ensure_ascii=False) + "\n"


def main():
    text = ST.read_text()
    existing = {s["id"] for s in yaml.safe_load(text)}
    added = []
    for new in (CROSSWALK, ICHEME, AICHE):
        if new["id"] in existing:
            print(f"  {new['id']} already registered, leaving it alone")
            continue
        if not text.endswith("\n"):
            text += "\n"
        text += flow(new)
        added.append(f"{new['id']} ({len(new['items'])} items)")
    ST.write_text(text)
    # The append must not have disturbed anything: same ids plus what we added, and every entry still parses.
    after = {s["id"] for s in yaml.safe_load(ST.read_text())}
    assert existing <= after, f"lost: {sorted(existing - after)}"
    assert len(after) == len(existing) + len(added), f"{len(after)} ids, expected {len(existing) + len(added)}"
    print("  added:", ", ".join(added) or "none")

    p = FW / "graduate-chemical-engineering.yaml"
    t = p.read_text()
    if GC_BASIS_OLD in t:
        t = t.replace(GC_BASIS_OLD, GC_BASIS_NEW)
        print("  GC basis -> cheme-grad-core")
    n = sum(1 for old, new in UNIT_TITLES if old in t)
    for old, new in UNIT_TITLES:
        t = t.replace(old, new)
    t = re.sub(r"\A# Graduate Chemical Engineering Core.*?\n(?=id: graduate-chemical-engineering)",
               GC_HEADER, t, flags=re.S)
    p.write_text(t)
    assert yaml.safe_load(p.read_text())["basis"]["primary"] == "cheme-grad-core"
    print(f"  GC: {n} unit titles cleared of course numbers, header rewritten")

    p = FW / "process-design.yaml"
    t = p.read_text()
    if "aiche-bok" not in t:
        t = t.replace("  also: [pe-chemical, nspe-ethics, osha-psm]\n",
                      "  also: [pe-chemical, nspe-ethics, osha-psm, aiche-bok]\n")
        p.write_text(t)
        assert "aiche-bok" in yaml.safe_load(p.read_text())["basis"]["also"]
        print("  process-design also += aiche-bok")
    else:
        print("  process-design already cites aiche-bok")


if __name__ == "__main__":
    main()
