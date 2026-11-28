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
 "anatomy-physiology": ({2: [1], 3: [2], 4: [3], 5: [4], 6: [5], 7: [5], 8: [7], 9: [8], 10: [8], 11: [2], 12: [8, 10], 13: [7]},
                        {1: ["BI-4.5"], 5: ["BI-2.9"], 10: ["CH-3.4"], 12: ["CH-8.9"]}),
 "microbiology": ({2: [1], 3: [2], 4: [3], 5: [3], 6: [4, 5], 7: [2]}, {1: ["BI-2.11"], 3: ["BI-3.6"], 4: ["BI-6.5"]}),
 "managerial-accounting": ({2: [1], 3: [1], 4: [3], 5: [2, 4], 6: [5], 7: [3]}, {1: ["FA-2"]}),
 "microeconomics": ({2: [1], 3: [2], 4: [3], 5: [3], 6: [4]}, {1: ["MH-2.3"], 2: ["MH-2.7"]}),
 "pharmacology": ({2: [1], 3: [2], 4: [1], 5: [4], 6: [4], 7: [3], 8: [5]}, {2: ["CH-8.9"], 4: ["HP-5.3"], 5: ["HP-8.3", "HP-12.1"], 8: ["HP-7.1"]}),
 "electric-circuits": ({2: [1], 3: [2], 4: [3], 5: [1], 6: [2], 7: [3]}, {1: ["PH-11.7"], 2: ["EM-1.2"], 3: ["EM-7.3", "PH-11.8"]}),
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
 # third pass: professional, computing and practice frameworks
 "accounting-far": ({2: [1], 3: [2]}, {}),
 "ai-basics": ({2: [1], 3: [2], 4: [3], 5: [3], 6: [4], 7: [4], 8: [7], 9: [6], 10: [9]}, {}),
 "biosecurity": ({7: [1], 2: [1], 3: [7], 4: [7], 5: [4], 6: [2, 3, 4, 5], 8: [3, 5]}, {1: ["BI-10.3"], 7: ["SS-2.1"]}),
 "inbde": ({1: [10, 12], 2: [1, 4, 8, 11], 3: [13], 6: [5], 7: [5], 10: [7, 9], 11: [5, 6], 12: [8]}, {}),
 "mental-math": ({2: [1], 3: [2], 4: [3], 5: [4], 6: [1]}, {}),
 "sql": ({2: [1], 3: [2], 4: [3], 5: [1], 6: [5], 7: [6], 8: [3, 4]}, {}),
 "dat": ({}, {1: ["BI-1.1"], 2: ["CH-0"]}),
 "ai-safety": ({2: [1], 3: [2], 4: [1], 5: [1], 6: [5], 7: [3, 6], 8: [6], 9: [8], 10: [9], 11: [4], 12: [7]}, {1: ["CA-12.5"]}),
 "swimming": ({2: [1], 3: [2], 4: [2], 5: [1], 9: [7, 8], 10: [2, 3, 4, 5], 11: [9], 12: [10, 11]}, {}),
 "information-systems": ({2: [1], 3: [2], 4: [3], 5: [2], 6: [5], 7: [1], 8: [1]}, {4: ["CS-7"], 5: ["CS-10"], 6: ["CS-11"]}),
 "basketball": ({2: [1], 3: [1], 4: [2, 3], 5: [3], 6: [1, 3], 9: [5, 8], 10: [1, 3]}, {}),
 "wushu": ({2: [1], 3: [1], 4: [1], 5: [2], 6: [1], 7: [6], 8: [2, 7], 9: [1], 10: [1]}, {}),
 "nclex-rn": ({5: [2], 3: [5], 4: [3], 6: [5], 7: [6], 8: [7], 1: [4, 8]}, {}),
 "computer-science": ({2: [1], 3: [2], 4: [3], 5: [4], 7: [3], 9: [8], 10: [9], 11: [10], 12: [5], 13: [1, 4], 14: [9], 15: [6], 17: [4], 18: [10, 14], 19: [13]}, {}),
 "engineering-math": ({2: [1], 3: [2], 4: [3], 5: [3, 8], 6: [3], 7: [3], 9: [3], 10: [9], 11: [9], 13: [5], 14: [1], 15: [14]},
                      {1: ["CA-6.9"], 2: ["CA-7.6"], 8: ["LA-5.1"], 10: ["CA-12.2"], 12: ["CA-14.5"]}),
 "speaking": ({2: [1], 3: [2], 5: [4], 6: [4], 7: [3, 4], 9: [2], 10: [3, 6], 11: [3]}, {}),
 "calculus": ({2: [1], 3: [2], 4: [3], 5: [3], 6: [5], 7: [6], 8: [6], 9: [8], 10: [6], 12: [3, 11], 13: [8, 12], 14: [13], 15: [3], 16: [8], 17: [8], 18: [9, 10]}, {}),
 "chemistry": ({1: [0], 2: [1], 3: [2], 4: [0], 5: [4], 6: [4], 7: [5], 8: [7], 9: [6, 7]}, {}),
 "biology": ({2: [1], 3: [2], 4: [2], 5: [4], 6: [5], 7: [5], 8: [7], 9: [2], 10: [6]}, {1: ["CH-3.1"]}),
 "programming": ({2: [1], 3: [2], 4: [3], 6: [5], 7: [4], 8: [7]}, {}),
 "physics": ({2: [1], 3: [2], 4: [2], 5: [2], 6: [3, 5], 7: [3], 8: [2], 9: [3], 10: [2], 11: [10], 12: [10], 14: [7], 15: [10, 14], 16: [1], 17: [2, 16], 18: [3], 19: [4], 20: [5], 21: [6], 22: [7], 23: [10], 24: [23], 25: [10], 26: [11], 27: [12], 28: [27], 30: [18]}, {}),
}
# frameworks that were already linked objective by objective: only an objective with no prerequisite at all gets one
FILL = {"programming", "computer-science", "engineering-math", "speaking", "calculus", "chemistry", "biology", "physics"}

# The foundation's own cross-subject links (fourth pass). Before this, Chemistry, Physics, Calculus, Statistics and
# Linear Algebra named no prerequisite in mathematics at all, and Math HS named none in K-8. Keys are a unit ("8") or a
# topic ("8.2"); the first objective there (file order) needs the last objective of each anchor. Hand-chosen: the one
# piece of earlier mathematics or chemistry the topic cannot be done without. An anchor here is an exact objective code.
ANCHORS = {
 "mental-math": {"1.1": ["MK-6.3.D"], "1.5": ["MK-6.2.F"], "1.8": ["MK-7.2.D"], "1.9": ["MK-7.1.E"], "1.10": ["MK-7.5.F"], "2.6": ["MK-8.1.E"], "2.10": ["MK-8.3.D"], "3.1": ["MK-9.2.A"], "3.2": ["MK-9.4.G"]},
 "math-hs": {"1.1": ["MK-7.1.F"], "1.2": ["MK-7.3.D"], "1.3": ["MK-9.2.H"], "2.1": ["MK-9.3.A"], "2.3": ["MK-9.2.E"], "2.6": ["MK-9.2.A"], "2.7": ["MK-9.2.J"], "3.1": ["MK-7.5.F"], "3.2": ["MK-9.5.D"],
             "4.1": ["MK-8.3.A"], "5.1": ["MK-9.1.A"], "6.1": ["MK-9.4.A"], "7.1": ["MK-9.4.D"], "7.3": ["MK-9.4.G"], "8.1": ["MK-9.4.I"], "9.1": ["MK-9.4.H"], "11.1": ["MK-8.5.H"], "12.1": ["MK-9.2.B"],
             "19.1": ["MH-7.3.C"], "19.4": ["MH-2.7.B"]},
 "calculus": {"1.1": ["MH-2.2.C"], "1.6": ["MH-12.5.B"], "2.5": ["MH-2.6.B"], "2.7": ["MH-17.1.C"], "3.1": ["MH-16.1.A"], "3.3": ["MH-16.1.C"], "3.4": ["MH-17.2.B"], "7.8": ["MH-14.1.A"], "8.7": ["MH-8.1.B"],
              "9.7": ["MH-18.1.B"], "10.2": ["MH-12.4.A"], "11.1": ["MH-19.2.D"], "15.1": ["MH-2.6.C"]},
 "linear-algebra": {"1.1": ["MH-2.7.B"], "1.2": ["MH-19.2.D"], "2.2": ["MH-19.4.C"]},
 "statistics": {"1.1": ["MH-3.1.B"], "2.1": ["MH-11.2.B"], "3.1": ["MH-15.3.B"], "5.1": ["MH-3.3.A"], "6.1": ["MH-21.1.B"], "6.3": ["MH-15.1.A"]},
 "chemistry": {"0.2": ["MK-9.2.D"], "0.3": ["MH-1.1.A"], "3.4": ["MH-1.4.D"], "5.3": ["MH-14.1.A"], "7.4": ["MH-4.3.D"], "8.2": ["MH-16.2.A"], "9.5": ["MH-16.2.B"]},
 "physics": {"1.1": ["MH-19.1.A"], "1.2": ["MH-2.3.B"], "1.5": ["MH-7.3.C"], "5.1": ["MH-13.1.A"], "7.1": ["MH-13.2.A"], "13.3": ["MH-17.2.B"], "15.8": ["MH-14.1.A"],
             "16.2": ["CA-4.2.A"], "17.9": ["CA-7.6.A"], "18.2": ["CA-6.7.A"], "19.2": ["CA-6.7.A"], "20.4": ["CA-8.3.A"], "22.1": ["CA-7.2.A"], "23.4": ["CA-8.3.A"], "23.5": ["CA-14.7.B"],
             "24.2": ["CA-14.2.B"], "26.8": ["CA-7.8.A"], "27.4": ["CA-14.2.B"], "28.2": ["CA-3.1.A"], "28.6": ["CA-7.2.A"], "29.1": ["PH-1.4.A"], "30.1": ["CA-12.2.B"]},
 "biology": {"1.3": ["CH-2.5.A"], "2.8": ["CH-3.14.C"], "3.1": ["CH-5.11.A"], "3.4": ["CH-9.7.A"], "3.6": ["CH-4.9.B"]},
 "programming": {"1.2": ["MK-5.2.A"], "2.8": ["MH-2.4.C"], "8.1": ["MH-19.4.C"]},
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
            if f in FILL and needs[me]: continue
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
for f, table in ANCHORS.items():
    c, seq, ok = code_of[f], order[f], closure(f) | {f}
    for key, anc in table.items():
        hit = [x for x in seq if (f"{x[1]}.{x[2]}" == key if "." in key else x[1] == key)]
        if not hit: sys.exit(f"{f}: nothing at {key}")
        i, un, tn, lo = hit[0]; me = f"{c}-{un}.{tn}.{lo}"
        for a in anc:
            if fw_of[a.split("-")[0]] not in ok: sys.exit(f"{f} {key}: anchor {a} is in a framework {f} does not require")
            w = a if re.fullmatch(r"[A-Z]+-\d+\.\d+\.[A-Z]+", a) else last(a)
            if w not in needs: sys.exit(f"{f} {key}: no objective {w}")
            if w in needs[me] or w == me: continue
            if reaches(w, me): skipped += 1; print("  skipped (would close a cycle):", me, "needs", w); continue
            needs[me].add(w); touched.setdefault((f, i), []).append(w); added += 1
for (f, i), new in touched.items():
    L = files[f]
    m = re.search(r"needs: \[([^\]]*)\]", L[i])
    if not m:
        L[i] = re.sub(r"(, drills: \[)", r", needs: [], drills: [", L[i], count=1)
        if not re.search(r"needs: \[([^\]]*)\]", L[i]): L[i] = re.sub(r" \}\s*$", ", needs: [] }", L[i], count=1)
        m = re.search(r"needs: \[([^\]]*)\]", L[i])
        if not m: sys.exit(f"{f} line {i + 1}: no place for needs")
    have = [s.strip() for s in m.group(1).split(",") if s.strip()]
    L[i] = L[i][:m.start()] + f"needs: [{', '.join(have + new)}]" + L[i][m.end():]
for f in {f for f, _ in touched}:
    open(os.path.join(ROOT, f"drills/frameworks/{f}.yaml"), "w").write("\n".join(files[f]))
print(f"needs_science: {added} links added, {skipped} skipped")
