"""Write the ACS Physical Chemistry content-map citations in scripts/accm_pchem.py (CITE) onto the objectives of the
physical-chemistry and anchor-quantities frameworks. Add-only and idempotent."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from accm_pchem import CITE
FW = {re.search(r"^code: *(\S+)", open(f).read(), re.M).group(1): f for f in glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml")) if re.search(r"^code: *(\S+)", open(f).read(), re.M)}
q = lambda x: '"' + x + '"'
by = {}
for code, items in CITE.items():
    by.setdefault(code.split("-")[0], {})[code] = [f"acs-accm-pchem:{i}" for i in items]
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
    missing = set(codes) - done
    if missing: sys.exit(f"objectives not found: {sorted(missing)}")
    open(path, "w").write("\n".join(L))
print("cited", sum(len(v) for v in by.values()), "objectives")
