#!/usr/bin/env python3
"""Make Graduate ChemE's `gc` domain real, for the mathematical-methods unit the crosswalk opens.

The framework has carried `domains: [gc]` as a placeholder since draft 1: its units borrow skills from fm, mass,
thermo, cre, design and sep, so no skill ever had domain gc. Unit 7 is the first material with no home anywhere —
scaling, perturbation and asymptotics, similarity solutions, and curvilinear eigenfunction expansions are in no
other framework, and Engineering Math stops at Kreyszig. The software-limits objectives reuse nm.* rather than
duplicating Numerical Methods.

Idempotent. Writes the skills, the domain, the library subject and the source file, then leaves the rest alone.
"""
import pathlib, re, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SK = ROOT / "drills" / "skills.yaml"
LIB = ROOT / "drills" / "library.yaml"
SRC = ROOT / "drills" / "sources" / "cheme-grad-methods.yaml"
SUBJECT = "Graduate ChemE Methods"

SKILLS = [
    ("gc.scaling", "Scaling and non-dimensionalisation", "Scaling", ["pde.separation"]),
    ("gc.perturbation", "Perturbation and asymptotic methods", "Perturbation", ["gc.scaling"]),
    ("gc.similarity", "Similarity solutions and combination of variables", "Similarity", ["gc.scaling"]),
    ("gc.eigen", "Eigenfunction expansions in curvilinear geometry", "Curvilinear eigenfunctions",
     ["bvp.sl-eigenfunctions"]),
]

SOURCE = """# The mathematical-methods course every one of the fifteen departments in cheme-grad-core requires, written as a
# source so the gc.* skills have a home. This is NOT a book: no graduate methods text was read. The "chapters" are
# the MM items of the crosswalk, which were themselves taken from those departments' own course descriptions. The
# canonical texts in this area are well known, but since none was read none is claimed here.
id: cheme-grad-methods
title: "Graduate chemical engineering mathematical methods (course areas)"
short: "Grad ChemE methods"
year: 2026
field: chemical engineering
chapters:
  - { n: 1, title: "Scaling and non-dimensionalisation; which terms a limit lets you drop", skills: [gc.scaling] }
  - { n: 2, title: "Perturbation and asymptotic methods; regular and singular limits, boundary layers", skills: [gc.perturbation] }
  - { n: 3, title: "Similarity solutions and combination of variables", skills: [gc.similarity] }
  - { n: 4, title: "Eigenfunction expansions and Sturm-Liouville problems in non-Cartesian geometry", skills: [gc.eigen] }
"""


def main():
    t = SK.read_text()
    if "id: gc.scaling" in t:
        print("  gc.* skills already present")
    else:
        # Domain, in the domains list.
        if not re.search(r"^\s+- \{ id: gc,", t, re.M) and "id: gc," not in t:
            dom = '  - { id: gc, title: "Graduate ChemE methods past Kreyszig" }\n'
            t, n = re.subn(r"(\n\s+- \{ id: nm,[^\n]*\n)", lambda m: m.group(1) + dom, t, count=1)
            if not n:
                t, n = re.subn(r"(^domains:\n)", lambda m: m.group(1) + dom, t, count=1, flags=re.M)
            assert n, "could not find the domains list"
        lines = "".join(
            f'  - {{ id: {i}, domain: gc, title: "{ti}", short: "{sh}", prereqs: [{", ".join(pr)}] }}\n'
            for i, ti, sh, pr in SKILLS)
        t = t.rstrip("\n") + "\n" + lines
        SK.write_text(t)
        d = yaml.safe_load(SK.read_text())
        doms = {x["id"] for x in d["domains"]}
        got = {s["id"] for s in d["skills"] if s.get("domain") == "gc"}
        assert "gc" in doms, "domain gc not registered"
        assert got == {s[0] for s in SKILLS}, got
        print(f"  skills: domain gc + {len(got)} skills")

    t = LIB.read_text()
    if SUBJECT not in t:
        t = re.sub(r'(\n  - "Numerical Methods"\n)', lambda m: m.group(1) + f'  - "{SUBJECT}"\n', t, count=1)
        t = re.sub(r'(\n  nm: "Numerical Methods"\n)', lambda m: m.group(1) + f'  gc: "{SUBJECT}"\n', t, count=1)
        t = re.sub(r'(\n  chapra-canale-7e: "Numerical Methods"\n)',
                   lambda m: m.group(1) + f'  cheme-grad-methods: "{SUBJECT}"\n', t, count=1)
        LIB.write_text(t)
        l = yaml.safe_load(LIB.read_text())
        assert SUBJECT in l["subjects"], "subject not added"
        assert l["domains"].get("gc") == SUBJECT, l["domains"].get("gc")
        assert l["books"].get("cheme-grad-methods") == SUBJECT
        print(f"  library: subject {SUBJECT!r}, domain gc, book cheme-grad-methods")
    else:
        print(f"  library already has {SUBJECT!r}")

    if not SRC.exists():
        SRC.write_text(SOURCE)
        print(f"  source: {SRC.name}")
    else:
        print(f"  source {SRC.name} already exists")


if __name__ == "__main__":
    main()
