"""Cite the FE Chemical specification items that other frameworks already answer but nothing pointed at. These are the
spec's shared-fundamentals areas (mathematics, statics and dynamics, electricity, chemistry, biology) and two transport
areas whose content lives in Mass Transfer and Separations. Add-only and idempotent.

Items left open on purpose after this pass are the ones nothing in the Library answers yet: 4.B and 4.C (material types,
compatibility and corrosion), 5.E (bioprocessing) and 15.B and 15.C (control strategies, loop design and hardware).

Usage: python3 scripts/fe_cite.py
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CITE = {
 "1.A": ["MH-7.3.C", "MH-13.1.A", "MH-14.1.A", "MH-17.1.A", "CA-17.1.B"],
 "3.A": ["PH-1.3.B", "PH-2.5.A", "PH-2.9.A", "PH-4.3.A", "PH-5.6.A"],
 "3.B": ["PH-3.2.A", "PH-3.2.C", "PH-3.5.A", "PH-4.4.A"],
 "3.C": ["PH-11.2.A", "PH-11.3.A", "PH-11.4.A"],
 "5.B": ["OR-1.1.A", "OR-2.1.A", "OR-6.1.A"],
 "5.C": ["AN-1.1.A", "AN-2.1.A", "AN-6.1.A"],
 "5.D": ["BC-1.1.A", "BC-4.1.A", "BC-6.1.A"],
 "10.B": ["MS-4.1.A", "MS-4.1.B"],
 "10.E": ["MS-4.1.E", "SP-1.1.A"],
}
FW, PRIMARY = {}, {}
for f in glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml")):
    txt = open(f).read()
    m = re.search(r"^code: *(\S+)", txt, re.M)
    if m:
        FW[m.group(1)] = f
        p = re.search(r"^  primary: *(\S+)", txt, re.M)
        PRIMARY[m.group(1)] = p.group(1) if p else None
by = {}
for item, codes in CITE.items():
    for c in codes:
        by.setdefault(c.split("-")[0], {}).setdefault(c, []).append(item)
q = lambda x: '"' + x + '"'
n = 0
for pre, codes in by.items():
    if pre not in FW: sys.exit(f"no framework with code {pre}")
    path = FW[pre]; L = open(path).read().split("\n"); un = tn = None; done = set()
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        if m and f"{pre}-{un}.{tn}.{m.group(1)}" in codes:
            code = f"{pre}-{un}.{tn}.{m.group(1)}"; done.add(code)
            # a bare code would be credited to this framework's own primary, so FE citations are always prefixed
            std = [f"fe-chemical:{x}" for x in codes[code]]
            # an objective's std may be a list, a bare scalar (one code), or absent
            m2 = re.search(r"std: \[([^\]]*)\]", ln)
            ms = None if m2 else re.search(r"std: ([^,}]+),", ln)   # scalar std
            if ms:
                merged = [ms.group(1).strip().strip('"')] + [s for s in std if s != ms.group(1).strip().strip('"')]
                L[i] = ln[:ms.start()] + f"std: [{', '.join(q(s) for s in merged)}]," + ln[ms.end():]
                n += 1
                continue
            if m2:
                have = [s.strip().strip('"') for s in m2.group(1).split(",") if s.strip()]
                have += [s for s in std if s not in have]
                L[i] = ln[:m2.start()] + f"std: [{', '.join(q(s) for s in have)}]" + ln[m2.end():]
            else:
                # the objective carries no std list yet: add one right after its id
                L[i] = re.sub(r"^(\s+- \{ id: [A-Z]+, )", lambda mm: mm.group(1) + f"std: [{', '.join(q(s) for s in std)}], ", ln)
            n += 1
    missing = set(codes) - done
    if missing: sys.exit(f"objectives not found in {path}: {sorted(missing)}")
    open(path, "w").write("\n".join(L))
print("cited", len(CITE), "FE items on", n, "objectives")
