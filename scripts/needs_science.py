"""Prerequisite links (`needs`) for the upper-level science and engineering frameworks (Nov 2026). Add-only, idempotent.

Before this, Chemistry, Physics and Biology were linked objective to objective (525 of 578) and everything built on
them was not: Physical Chemistry 0 of 158, Thermodynamics 12 of 184, Heat Transfer 3 of 101, Fluid Mechanics 0 of 64,
and no objective anywhere named a prerequisite in another subject.

For each framework below, a hand-written graph of units, plus hand-chosen anchors in the frameworks it builds on:
  - inside a topic, each objective needs the one before it (file order, which ramp.py has put recall-first);
  - a topic's first objective needs the last objective of the topic before it in the same unit;
  - a unit's first objective needs the last objective of each prerequisite unit, and its outside anchors
    ("CH-6.9" = the last objective of Chemistry topic 6.9, "CH-6" = the last objective of unit 6).
The chains record teaching order; they are not a claim that every step is strictly required. The unit graph and the
anchors are the judgment calls. A link that would close a cycle with an existing one is skipped and reported.
Run after opl_fill.py and needs_links.py, before ramp.py --all.   Usage: python3 scripts/needs_science.py"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# framework id: (unit -> prerequisite units, unit -> outside anchors)
G = {
 "physical-chemistry": ({2: [1], 3: [1], 4: [2, 3], 5: [1], 6: [4], 7: [4, 6], 8: [7], 9: [4, 8], 11: [10], 12: [11], 13: [12], 14: [12], 15: [14], 16: [13, 15], 17: [15], 18: [14],
                         19: [1], 20: [3, 12, 19], 21: [1, 19], 22: [4]},
                        {1: ["CH-3.4", "CH-6.10", "PH-9.4", "CA-12.2"], 2: ["CH-6.9"], 3: ["CH-9.2"], 4: ["CH-9.5", "CH-7.3"], 5: ["CH-3.6"], 6: ["CH-6.5"], 7: ["CH-3.7"], 9: ["CH-9.9"],
                         10: ["CH-1.5", "PH-15.5", "PH-14.8"], 11: ["CA-7.2"], 12: ["PH-7.4", "PH-6.3"], 14: ["CH-1.9", "CA-13.7"], 15: ["CH-2.8"], 17: ["CH-2.7"], 18: ["PH-12.2"],
                         20: ["CA-10.2"], 21: ["CH-3.5"], 22: ["CH-5", "CA-7.8"]}),
 "thermodynamics": ({2: [1], 3: [2], 4: [2, 3], 5: [4], 6: [5], 7: [3], 8: [4, 7], 9: [8], 10: [9], 11: [1, 2], 12: [11], 13: [11], 14: [4, 11], 15: [10, 11], 16: [10, 11], 17: [9, 12],
                     19: [18], 20: [19], 21: [18], 22: [10, 19]},
                    {1: ["EM-1.3"], 2: ["EM-1.4", "CH-9.2"], 3: ["CH-6.10", "PH-9.4"], 7: ["CH-3.6"], 8: ["CH-6.5"], 9: ["CH-3.7"], 10: ["CH-9.5"], 12: ["PH-7.4"], 16: ["CH-5.6"],
                     18: ["CH-6.4", "PH-9.2"], 22: ["CH-6.8"]}),
 "heat-transfer": ({2: [1], 3: [2], 4: [3], 5: [3], 6: [3], 7: [3], 8: [3], 9: [8], 10: [8], 11: [1], 12: [3, 9], 13: [8], 14: [7, 8]},
                   {1: ["PH-9.3"], 2: ["EM-10.1"], 4: ["EM-2.1"], 5: ["EM-3.2"], 6: ["EM-10.4"], 7: ["EM-10.2"], 8: ["PH-8.4"], 11: ["PH-15.4"]}),
 "fluid-mechanics": ({2: [1], 3: [1], 4: [2, 3], 5: [3], 6: [4], 7: [3], 8: [2, 7], 9: [2], 10: [1, 4], 11: [1, 8], 12: [6, 8, 9], 13: [4, 10]},
                     {1: ["PH-8.2"], 3: ["PH-8.4"], 7: ["PH-4.3"], 8: ["EM-2.1"], 11: ["EM-12.1"], 12: ["EM-14.2"]}),
 "mass-transfer": ({2: [1], 3: [1], 4: [1], 5: [1, 4]}, {1: ["HT-14"], 2: ["EM-3.2"], 3: ["HT-7", "EM-10.2"], 4: ["HT-8"]}),
 "material-balances": ({2: [1], 3: [2], 4: [2], 5: [2], 6: [3]}, {1: ["CH-0.3"], 3: ["CH-4.5"], 4: ["CH-6.8"]}),
 "numerical-methods": ({4: [3]}, {1: ["CA-4.6"], 2: ["LA-1.1"], 3: ["CA-6.2"], 4: ["CA-7.5"], 5: ["CA-2.3"]}),
 "process-design": ({5: [1], 6: [2], 7: [5], 8: [1], 9: [8], 10: [3]}, {4: ["MB-1"], 5: ["MB-6"]}),
 "separations": ({2: [1]}, {1: ["MB-2", "TD-9"], 2: ["TD-21"]}),
 "reaction-engineering": ({2: [1], 3: [2], 4: [1], 5: [1], 6: [2], 7: [4], 8: [2], 9: [5]}, {1: ["MB-3"]}),
 "graduate-chemical-engineering": ({2: [1]}, {1: ["FM-8", "FM-12"], 2: ["HT-7", "MS-3"], 3: ["TD-5", "TD-10"], 4: ["RE-6", "RE-7"], 5: ["PD-3", "EM-7"], 6: ["TD-9", "MS-4"], 7: ["EM-9", "EM-10"]}),
 "biochemistry": ({2: [1], 3: [2], 4: [3], 5: [1], 6: [5], 7: [4, 5], 8: [1], 9: [3, 4], 10: [2, 8], 11: [7, 8]},
                  {1: ["CH-8.9", "BI-1.1"], 2: ["BI-1.5"], 3: ["CH-7.3"], 4: ["BI-3.2", "CH-5.10"], 5: ["CH-9.7"], 6: ["BI-2.6"], 7: ["BI-3.6"], 8: ["BI-6.4"], 9: ["BI-4.3"], 11: ["BI-7.5"]}),
 "structures": ({2: [1], 3: [1]}, {1: ["CH-2.5"]}),
 "organic-reactions": ({2: [1], 3: [1], 4: [3], 5: [4], 6: [1], 7: [4], 8: [1], 9: [8], 10: [4, 7]}, {1: ["CH-2.6", "ST-1"], 8: ["ST-3"], 9: ["CH-5.6"]}),
 "electronic-structure": ({2: [1], 3: [2], 4: [2, 3], 5: [2], 6: [2, 3]}, {1: ["CH-1.9", "CH-2.8"]}),
 "protein-design": ({2: [1], 3: [2], 4: [3], 5: [4], 6: [5], 7: [5], 8: [5], 9: [6], 10: [4, 6]}, {1: ["BC-2"], 3: ["MD-2"], 4: ["MD-7"], 6: ["BC-3"], 9: ["MD-9"]}),
 "electric-double-layers": ({2: [1], 3: [1], 4: [3], 5: [2, 4], 6: [3]}, {1: ["MT-3"], 2: ["TD-11"], 3: ["TD-12"], 4: ["TD-4"]}),
 "molecular-simulation": ({2: [1], 3: [2], 4: [1, 3], 5: [2], 6: [4, 5], 7: [6], 16: [7], 8: [16], 9: [8], 17: [9], 10: [9], 11: [10], 12: [7], 13: [6], 14: [11], 15: [2]}, {1: ["TD-11"]}),
 "materials": ({4: [2]}, {1: ["CH-3.1"], 2: ["CH-3.2"], 3: ["CH-3.1", "PH-10.5"], 4: ["CH-9.8"]}),
 "nuclear": ({2: [1], 3: [1], 4: [3], 5: [4], 6: [4], 7: [1, 2]}, {1: ["PH-15.8"]}),
 "particle-physics": ({2: [1]}, {1: ["PH-15.7"], 2: ["PH-29.2"], 3: ["PH-15.5"]}),
 "periodic-table": ({2: [1], 3: [2], 4: [1]}, {1: ["CH-0.4"], 4: ["CH-1.5"]}),
 "anchor-quantities": ({6: [4]}, {1: ["CH-0.2"], 2: ["CH-6.4"], 3: ["CH-1.5"], 4: ["CH-1.1"], 5: ["CH-2.1"]}),
 "inorganic-chemistry": ({2: [1], 4: [2]}, {1: ["PT-1"], 2: ["CH-4.9"], 3: ["PT-2", "CH-2.7"], 4: ["CH-9.8"], 5: ["CH-2.3"]}),
 "inorganic-advanced": ({2: [1], 3: [1], 4: [1], 5: [4], 6: [5], 7: [6], 8: [7], 9: [8], 11: [10], 12: [11], 13: [10], 14: [10], 15: [1]}, {1: ["IN-2"], 10: ["IN-3"]}),
 "analytical-chemistry": ({6: [1, 5]}, {1: ["CH-4.6", "CH-8.5"], 2: ["CH-4.5"], 3: ["CH-7"], 4: ["CH-3.9"], 5: ["CH-0.2"]}),
 "chemistry-olympiad": ({1: [10], 2: [8, 11], 3: [9], 4: [7], 15: [5, 8, 10, 11], 16: [1, 2, 3]},
                        {5: ["CH-4"], 6: ["IN-4"], 7: ["CH-3"], 8: ["CH-9"], 9: ["CH-5"], 10: ["CH-8"], 11: ["CH-9"], 12: ["CH-1"], 13: ["CH-2"]}),
 "earth-space": ({4: [3]}, {1: ["PH-6.6", "PH-15.4"], 2: ["PH-15.8"], 3: ["PH-9.3"]}),
}


def walk(L):
    un = tn = None
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        if m: yield i, un, tn, m.group(1)


files, code_of, requires = {}, {}, {}
for p in sorted(glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml"))):
    fid = os.path.basename(p)[:-5]; L = open(p).read().split("\n"); files[fid] = L
    code_of[fid] = next(re.match(r"^code: (\S+)", ln).group(1) for ln in L if ln.startswith("code: "))
    r = next((ln for ln in L if ln.startswith("requires:")), "requires: []")
    requires[fid] = [s.strip() for s in re.search(r"\[([^\]]*)\]", r).group(1).split(",") if s.strip()]
fw_of = {c: f for f, c in code_of.items()}


def closure(f, seen=None):
    seen = seen if seen is not None else set()
    for r in requires[f]:
        if r not in seen: seen.add(r); closure(r, seen)
    return seen


order, needs = {}, {}  # framework -> [(line, unit, topic, lo)], code -> set of codes
for f, L in files.items():
    order[f] = list(walk(L))
    for i, u, t, lo in order[f]:
        m = re.search(r"needs: \[([^\]]*)\]", L[i])
        needs[f"{code_of[f]}-{u}.{t}.{lo}"] = {s.strip() for s in m.group(1).split(",") if s.strip()} if m else set()


def last(anchor):
    c, where = anchor.split("-", 1); f = fw_of[c]
    hit = [x for x in order[f] if (f"{x[1]}.{x[2]}" == where if "." in where else x[1] == where)]
    if not hit: sys.exit(f"anchor {anchor}: nothing there")
    return f"{c}-{hit[-1][1]}.{hit[-1][2]}.{hit[-1][3]}"


def reaches(a, b):
    """does a (transitively) need b"""
    stack, seen = [a], set()
    while stack:
        x = stack.pop()
        if x == b: return True
        if x in seen: continue
        seen.add(x); stack.extend(needs.get(x, ()))
    return False


added = skipped = 0
touched = {}
for f, (graph, ext) in G.items():
    c, L, seq = code_of[f], files[f], order[f]
    units = {}
    for x in seq: units.setdefault(int(x[1]), []).append(x)
    ok = closure(f)
    for u in list(graph) + [p for ps in graph.values() for p in ps] + list(ext):
        if u not in units: sys.exit(f"{f}: no unit {u}")
    for u, los in units.items():
        for k, (i, un, tn, lo) in enumerate(los):
            me = f"{c}-{un}.{tn}.{lo}"
            if k:
                want = [f"{c}-{los[k - 1][1]}.{los[k - 1][2]}.{los[k - 1][3]}"]
            else:
                want = [f"{c}-{units[p][-1][1]}.{units[p][-1][2]}.{units[p][-1][3]}" for p in graph.get(u, [])]
                for a in ext.get(u, []):
                    if fw_of[a.split("-")[0]] not in ok: sys.exit(f"{f} unit {u}: anchor {a} is in a framework {f} does not require")
                    want.append(last(a))
            for w in want:
                if w in needs[me]: continue
                if reaches(w, me): skipped += 1; print("  skipped (would close a cycle):", me, "needs", w); continue
                needs[me].add(w); touched.setdefault((f, i), []).append(w); added += 1
for (f, i), new in touched.items():
    L = files[f]
    m = re.search(r"needs: \[([^\]]*)\]", L[i])
    if not m:
        L[i] = re.sub(r"(, drills: \[)", r", needs: [], drills: [", L[i], count=1)
        m = re.search(r"needs: \[([^\]]*)\]", L[i])
        if not m: sys.exit(f"{f} line {i + 1}: no place for needs")
    have = [s.strip() for s in m.group(1).split(",") if s.strip()]
    L[i] = L[i][:m.start()] + f"needs: [{', '.join(have + new)}]" + L[i][m.end():]
for f in {f for f, _ in touched}:
    open(os.path.join(ROOT, f"drills/frameworks/{f}.yaml"), "w").write("\n".join(files[f]))
print(f"needs_science: {added} links added, {skipped} skipped")
