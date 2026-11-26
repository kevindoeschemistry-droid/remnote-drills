"""Cite the UIL Number Sense Junior High and Elementary chart items on the objectives that already answer the same
topic on the High School chart. The three charts are the same ladder at three levels, so an objective that answers a
high-school item answers its junior-high or elementary twin; where a J or E item has no high-school twin, OVERRIDE
names its objectives by hand, and an item nothing answers is left open rather than cited loosely.

Add-only and idempotent. Usage: python3 scripts/uil_cite.py [--dry]
"""
import glob, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry" in sys.argv
S = yaml.safe_load(open(os.path.join(ROOT, "drills/standards.yaml")))
ITEMS = {i["code"]: i.get("parts", {}) for i in next(x for x in S if x["id"] == "uil-number-sense")["items"]}

# J and E items whose topic is not on the high-school chart, or whose twin is the wrong level.
OVERRIDE = {
 # junior high: topics the high-school chart words differently or does not carry
 "J1.7":  ["MM-1.7.C"],                  # Roman numerals
 "J1.9":  ["MM-1.11.A"],                 # sums of a finite series of whole numbers
 "J2.4":  ["MM-1.7.B"],                  # English/metric and time conversions
 "J2.11": ["MM-2.14.A"],                 # perimeter and area of square, rectangle, circle
 "J2.14": ["MM-1.5.A"],                  # multiplying by 101 and 111
 "J3.3":  ["MM-3.2.A"],                  # Pythagorean theorem
 "J3.7":  ["MM-2.14.A"],                 # area of parallelogram, rhombus, trapezoid, circle
 "J3.9":  ["MM-2.14.A", "MM-3.2.A"],     # basic geometry facts
 "J4.2":  ["MM-1.14.A"],                 # more number theory
 "J4.4":  ["MM-4.1.A"],                  # volume of cylinder, cone, sphere
 "J4.6":  ["MM-3.11.A"],                 # factorial
 # elementary: the K-8 framework is the right level for the arithmetic items
 "E1.1":  ["MK-3.2.E", "MK-4.2.B"],      # four operations on whole numbers
 "E1.2":  ["MK-3.2.C", "MK-4.2.A"],      # place value
 "E1.3":  ["MK-4.2.A", "MK-5.2.C"],      # rounding whole numbers
 "E1.6":  ["MK-3.1.C"],                  # even and odd numbers
 "E1.7":  ["MK-3.2.C", "MK-6.2.C"],      # expanded notation
 "E1.8":  ["MK-3.2.G"],                  # sums with regrouping
 "E1.9":  ["MK-3.2.G"],                  # differences with regrouping
 "E1.10": ["MM-1.7.C"],                  # Roman numerals
 "E2.1":  ["MK-5.3.D", "MK-5.3.E"],      # fractions with common denominators
 "E2.2":  ["MK-6.2.H"],                  # four operations on decimals
 "E2.4":  ["MM-1.7.A"],                  # fraction, decimal, percent
 "E2.9":  ["MM-1.14.A"],                 # prime numbers
 "E2.11": ["MM-1.7.B", "MK-4.4.B"],      # length, measurement and time conversions
 "E3.3":  ["MK-4.4.G", "MK-4.4.J"],      # perimeter and area of square, rectangle, triangle
 "E3.4":  ["MM-2.14.A"],                 # radius and diameter of a circle
 "E3.5":  ["MM-2.1.A", "MM-2.7.A"],      # powers and roots
 "E3.10": ["MK-6.4.E"],                  # volume of cube and rectangular box
 "E4.1":  ["MM-1.1.A", "MM-1.1.B"],      # four operations on integers
 "E4.3":  ["MK-4.4.E"],                  # basic geometry facts
 "E4.4":  ["MK-4.4.I"],                  # more area problems
 "E4.6":  ["MM-1.5.A", "MM-1.5.B"],      # more multiplication short-cuts
 "E4.7":  ["MM-2.7.A"],                  # more powers and roots
 "E4.11": ["MM-2.14.A"],                 # area of parallelogram, rhombus, trapezoid
}
# Build the high-school topic -> objectives map from the frameworks themselves.
cited = {}
FW = {}
PRIMARY = {}
for f in glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml")):
    txt = open(f).read()
    m = re.search(r"^code: *(\S+)", txt, re.M)
    if not m: continue
    FW[m.group(1)] = f
    primary = (yaml.safe_load(txt).get("basis") or {}).get("primary")
    PRIMARY[m.group(1)] = primary
    un = tn = None
    for ln in txt.split("\n"):
        mm = re.match(r"^    n: (\d+)", ln)
        if mm: un, tn = mm.group(1), None
        mm = re.match(r"^      - n: (\d+)", ln)
        if mm: tn = mm.group(1)
        mm = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        if mm:
            codes = re.findall(r"uil-number-sense:([A-Z0-9.]+)", ln)
            if primary == "uil-number-sense":
                # a framework whose primary basis is this standard cites it with bare codes
                mstd = re.search(r"std: \[([^\]]*)\]", ln)
                if mstd:
                    codes += [s.strip().strip('"') for s in mstd.group(1).split(",")
                              if re.fullmatch(r'"[HJE]\d(\.\d+)?"', s.strip())]
            for code in codes:
                cited.setdefault(code, []).append(f"{m.group(1)}-{un}.{tn}.{mm.group(1)}")

HS = {f"H{g}.{k}": v for g in "12345" for k, v in ITEMS.get(f"H{g}", {}).items()}
STOP = {"of", "on", "and", "a", "the", "to", "in", "or", "with", "for", "problems", "basic"}
def words(s):
    return {w for w in re.sub(r"[^a-z ]", " ", s.lower()).split() if w not in STOP and len(w) > 2}


def overlap(a, b):
    """Jaccard overlap of content words: the J and E charts reword the same topics, so shared nouns are the signal."""
    wa, wb = words(a), words(b)
    return len(wa & wb) / len(wa | wb) if wa | wb else 0.0
plan, twins = {}, {}
for chart, parts in ITEMS.items():
    if chart[0] not in "JE": continue
    for k, title in parts.items():
        code = f"{chart}.{k}"
        if code in cited: continue           # already answered
        if code in OVERRIDE:
            plan[code] = OVERRIDE[code]; twins[code] = (None, title, None); continue
        scored = sorted(((overlap(title, v), c) for c, v in HS.items()), reverse=True)
        if not scored or scored[0][0] < 0.45: continue
        twin = scored[0][1]
        if cited.get(twin): plan[code] = cited[twin]; twins[code] = (twin, HS[twin], round(scored[0][0], 2))

by = {}
for code, objs in plan.items():
    for o in objs:
        by.setdefault(o.split("-")[0], {}).setdefault(o, []).append(f"uil-number-sense:{code}")
if DRY:
    for code in sorted(plan):
        tw = twins.get(code)
        src = (f"via {tw[0]} ({tw[2]}) {tw[1][:44]}" if tw and tw[0] else f"by hand: {tw[1][:44]}") if tw else "?"
        print(f"{code:7s} {src:62s} -> {', '.join(plan[code])}")
    openleft = [f"{c}.{k}" for c, p in ITEMS.items() if c[0] in "JE" for k in p if f"{c}.{k}" not in plan and f"{c}.{k}" not in cited]
    print("still open:", len(openleft), openleft)
    print(len(plan), "of", sum(1 for c, p in ITEMS.items() if c[0] in "JE" for _ in p), "J/E items would be cited")
    sys.exit()

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
            code = f"{pre}-{un}.{tn}.{m.group(1)}"; done.add(code)
            # an objective's std may be a list, a bare scalar (one code), or absent
            m2 = re.search(r"std: \[([^\]]*)\]", ln)
            ms = None if m2 else re.search(r"std: ([^,}]+),", ln)   # scalar std
            if ms:
                merged = [ms.group(1).strip().strip('"')] + [s for s in std if s != ms.group(1).strip().strip('"')]
                L[i] = ln[:ms.start()] + f"std: [{', '.join(q(s) for s in merged)}]," + ln[ms.end():]
                n += 1
                continue
            have = [s.strip().strip('"') for s in m2.group(1).split(",") if s.strip()]
            new_codes = [c if PRIMARY.get(pre) != "uil-number-sense" else c.split(":", 1)[1] for c in codes[code]]
            have += [s for s in new_codes if s not in have]
            L[i] = ln[:m2.start()] + f"std: [{', '.join(q(s) for s in have)}]" + ln[m2.end():]
            n += 1
    missing = set(codes) - done
    if missing: sys.exit(f"objectives not found in {path}: {sorted(missing)}")
    open(path, "w").write("\n".join(L))
print("cited", len(plan), "UIL chart items on", n, "objectives")
