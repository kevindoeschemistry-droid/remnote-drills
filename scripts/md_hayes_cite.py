"""Cite the Hayes orientation and lambda-dynamics-examples items on the Molecular Simulation objectives they answer,
and the lettered Psi4NumPy sub-modules on the Electronic Structure objectives that already cite their module group.
Add-only and idempotent. Run after scripts/md_hayes.py. Usage: python3 scripts/md_hayes_cite.py

Four orientation items are deliberately uncited and say so in the standard's note: EXP, START, CL3 and ETC are lab
logistics (hours, group meeting, keys, ssh keys, conferences), not simulation science, so no card drills them."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CITE = {
 # Hayes orientation
 "hayes-orientation:CL1":  ["MD-13.3.A"],
 "hayes-orientation:CL2":  ["MD-13.4.B", "MD-13.4.C"],
 "hayes-orientation:CL4":  ["MD-13.1.A", "MD-13.1.B"],
 "hayes-orientation:LIT":  ["MD-10.1.A", "MD-14.1.B", "MD-14.2.A", "MD-14.2.B", "MD-14.2.C"],
 "hayes-orientation:TUT1": ["MD-5.1.C", "MD-6.1.D", "MD-6.2.A", "MD-6.2.C", "MD-9.3.B", "MD-13.2.B"],
 "hayes-orientation:TUT2": ["MD-2.2.A", "MD-10.1.B", "MD-11.3.A", "MD-11.3.B"],
 "hayes-orientation:TUT3": ["MD-10.3.A", "MD-10.3.B", "MD-10.4.B", "MD-11.1.A", "MD-11.1.B",
                            "MD-11.2.A", "MD-11.2.C", "MD-11.2.D", "MD-11.2.E"],
 "hayes-orientation:TUT4": ["MD-13.2.A", "MD-13.3.A"],
 "hayes-orientation:INST": ["MD-13.4.A"],
 # the example run files
 "hayes-lambda-examples:SYS":  ["MD-9.1.A", "MD-9.1.B"],
 "hayes-lambda-examples:PREP": ["MD-11.2.C", "MD-11.3.B"],
 "hayes-lambda-examples:TMPL": ["MD-11.2.A", "MD-11.2.B", "MD-13.1.A"],
 "hayes-lambda-examples:LIN":  ["MD-11.2.D", "MD-14.1.C"],
 # Psi4NumPy lettered sub-modules, on the objectives that already cite their group
 "psi4numpy-tutorials:03a": ["QC-2.1.A", "QC-2.1.B"],
 "psi4numpy-tutorials:03b": ["QC-2.3.A", "QC-2.3.B"],
 "psi4numpy-tutorials:03c": ["QC-1.2.A", "QC-1.2.B"],
 "psi4numpy-tutorials:03d": ["QC-1.2.A"],
 "psi4numpy-tutorials:04a": ["QC-5.2.B"],
 "psi4numpy-tutorials:04b": ["QC-5.1.A"],
 "psi4numpy-tutorials:04c": ["QC-5.1.A"],
 "psi4numpy-tutorials:04d": ["QC-5.2.A"],
 "psi4numpy-tutorials:04e": ["QC-5.1.B"],
 "psi4numpy-tutorials:05a": ["QC-4.1.A", "QC-4.1.B"],
 "psi4numpy-tutorials:05b": ["QC-4.1.A"],
}
by = {}
for item, codes in CITE.items():
    for c in codes:
        by.setdefault(c.split("-")[0], {}).setdefault(c, []).append(item)
FW = {}
for f in glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml")):
    m = re.search(r"^code: *(\S+)", open(f).read(), re.M)
    if m: FW[m.group(1)] = f
q = lambda x: '"' + x + '"'
n = 0
for pre, codes in by.items():
    path = FW[pre]; L = open(path).read().split("\n"); un = tn = None; done = set()
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        if m and f"{pre}-{un}.{tn}.{m.group(1)}" in codes:
            code = f"{pre}-{un}.{tn}.{m.group(1)}"; done.add(code); std = codes[code]
            m2 = re.search(r"std: \[([^\]]*)\]", ln)
            if m2:
                have = [s.strip().strip('"') for s in m2.group(1).split(",") if s.strip()]
                have += [s for s in std if s not in have]
                L[i] = ln[:m2.start()] + f"std: [{', '.join(q(s) for s in have)}]" + ln[m2.end():]
            else:
                L[i] = re.sub(r"^(\s+- \{ id: [A-Z]+, )", lambda mm: mm.group(1) + f"std: [{', '.join(q(s) for s in std)}], ", ln)
            n += 1
    missing = set(codes) - done
    if missing: sys.exit(f"objectives not found in {path}: {sorted(missing)}")
    open(path, "w").write("\n".join(L))
print("cited", n, "objectives")
