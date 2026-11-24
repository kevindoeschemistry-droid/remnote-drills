"""Apply a WeBWorK OPL section map to the frameworks: adds "webwork-opl:<section>" to each objective's std list.

The map is drills/standards/opl-map.yaml: { "LA1.1": ["LA-1.1.A", ...], "LA1.7": [] } (empty = a gap).
Objectives are found by code (FW-unit.topic.letter) in drills/frameworks/*.yaml; only flow-style objective
lines are edited. Running it twice changes nothing.
"""
import re, sys, glob, yaml
from collections import defaultdict
m = yaml.safe_load(open("drills/standards/opl-map.yaml"))
want = defaultdict(list)
for sec, los in m.items():
    for lo in los or []: want[lo].append(f"webwork-opl:{sec}")
files = {}
for f in glob.glob("drills/frameworks/*.yaml"):
    code = re.search(r"^code: *(\S+)", open(f).read(), re.M)
    if code: files[code.group(1)] = f
by_file = defaultdict(dict)
for lo, cites in want.items():
    fw, rest = lo.split("-", 1)
    u, t, l = rest.split(".")
    by_file[files[fw]][(int(u), int(t), l)] = cites
missing = []
for f, targets in by_file.items():
    lines = open(f).read().split("\n")
    unit = topic = None; in_units = False
    for i, ln in enumerate(lines):
        if ln.startswith("units:"): in_units = True; continue
        if not in_units: continue
        mu = re.match(r"^    n: (\d+)\s*$", ln) or re.match(r"^  - \{?.*\bn: (\d+)", ln)
        if re.match(r"^    n: (\d+)", ln): unit = int(re.match(r"^    n: (\d+)", ln).group(1)); topic = None; continue
        mt = re.match(r"^      - n: (\d+)", ln)
        if mt: topic = int(mt.group(1)); continue
        ml = re.match(r"^(\s+)- \{ id: ([A-Z]+),(.*)$", ln)
        if ml and (unit, topic, ml.group(2)) in targets:
            cites = targets.pop((unit, topic, ml.group(2)))
            rest = ml.group(3)
            sc = re.match(r"^ std: ([^\[\s,][^,]*),(.*)$", rest)
            if sc: rest = f' std: ["{sc.group(1).strip()}"],{sc.group(2)}'
            ms = re.match(r"^( std: \[)([^\]]*)(\].*)$", rest)
            if ms:
                have = [x.strip() for x in ms.group(2).split(",") if x.strip()]
                add = [f'"{c}"' for c in cites if f'"{c}"' not in have and c not in have]
                new = ", ".join(have + add)
                rest = ms.group(1) + new + ms.group(3)
            else:
                rest = " std: [" + ", ".join(f'"{c}"' for c in cites) + "]," + rest
            lines[i] = f"{ml.group(1)}- {{ id: {ml.group(2)},{rest}"
    open(f, "w").write("\n".join(lines))
    missing += [f"{f}: {k}" for k in targets]
gaps = [s for s, los in m.items() if not los]
print(f"opl: {len(m)} sections mapped, {len(gaps)} gaps; {sum(len(v) for v in want.values())} citations")
if missing: print("NOT FOUND:", *missing, sep="\n  "); sys.exit(1)
