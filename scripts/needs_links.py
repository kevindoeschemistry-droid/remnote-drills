"""Prerequisite links (`needs`) for frameworks that had none (Nov 2026). Add-only and idempotent.

Two kinds. EXPLICIT: objective -> objectives, written by hand for the small proof-side frameworks. TOPICS: for Linear
Algebra and Statistics, a hand-written graph of topics; inside a topic each objective needs the one before it (the
file order, which ramp.py has already put recall-first), and a topic's first objective needs the last objective of
each prerequisite topic. The chain inside a topic records the teaching order, not a proof that each step is required.
Usage: python3 scripts/needs_links.py   (then ramp.py --all and npm run skills)"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPLICIT = {
 "number-theory": {
  "NT-1.1.A": ["DM-1.2.A"], "NT-1.1.B": ["NT-1.1.A"], "NT-1.1.C": ["NT-1.1.A"],
  "NT-2.1.A": ["NT-1.1.B"], "NT-2.1.B": ["NT-2.1.A", "NT-1.1.C"], "NT-2.1.C": ["NT-2.1.A"], "NT-2.1.D": ["NT-2.1.B"],
  "NT-3.1.A": ["NT-2.1.B"], "NT-3.1.B": ["NT-3.1.A"], "NT-3.1.C": ["NT-3.1.B"],
  "NT-4.1.A": ["NT-1.1.A"], "NT-4.1.B": ["NT-3.1.B"], "NT-4.1.C": ["NT-2.1.A"], "NT-4.1.D": ["NT-1.1.C"]},
 "topology": {
  "TP-1.1.A": ["RA-4.1.A"], "TP-1.1.B": ["TP-1.1.A"], "TP-1.1.C": ["TP-1.1.B"], "TP-1.1.D": ["TP-1.1.C"],
  "TP-2.1.A": ["TP-1.1.C"], "TP-2.1.B": ["TP-2.1.A", "RA-4.1.B"], "TP-3.1.A": ["TP-1.1.C", "RA-2.1.B"], "TP-3.1.B": ["TP-3.1.A", "TP-2.1.B"],
  "TP-4.1.A": ["TP-1.1.D"], "TP-4.1.B": ["TP-4.1.A"], "TP-4.1.C": ["TP-4.1.B"],
  "TP-5.1.A": ["TP-2.1.B", "TP-4.1.B"], "TP-5.1.B": ["TP-5.1.A"], "TP-5.1.C": ["TP-5.1.B", "TP-4.1.C"], "TP-5.1.D": ["TP-5.1.B", "TP-4.1.A"]},
 "stochastic-processes": {
  "STO-1.1.A": ["LA-2.2.A", "SS-2.1.A"], "STO-1.1.B": ["STO-1.1.A"], "STO-1.1.C": ["STO-1.1.B"],
  "STO-2.1.A": ["STO-1.1.C"], "STO-2.1.B": ["STO-2.1.A"],
  "STO-3.1.A": ["STO-1.1.B", "LA-5.1.A"], "STO-3.1.B": ["STO-3.1.A", "STO-1.1.C"], "STO-3.1.C": ["STO-3.1.A"], "STO-3.1.D": ["STO-3.1.B"],
  "STO-4.1.A": ["SS-6.3.A"], "STO-4.1.B": ["STO-4.1.A"], "STO-4.1.C": ["STO-4.1.B", "STO-3.1.C"],
  "STO-5.1.A": ["STO-2.1.A"], "STO-5.1.B": ["STO-5.1.A"], "STO-5.1.C": ["STO-5.1.A"], "STO-5.1.D": ["STO-5.1.B", "SS-6.3.A"]},
 "geometry": {
  "GE-1.1.B": ["GE-1.1.A"], "GE-1.1.C": ["GE-1.1.B"], "GE-2.1.A": ["GE-1.1.A"], "GE-2.1.B": ["GE-2.1.A", "GE-1.1.B"], "GE-2.1.C": ["GE-2.1.A"],
  "GE-3.1.A": ["GE-2.1.C"], "GE-3.1.B": ["GE-3.1.A", "GE-2.1.B"]},
}
TOPICS = {
 "linear-algebra": ("LA", {"1.2": ["1.1"], "2.2": ["1.1"], "2.1": ["2.2"], "2.3": ["2.1"], "3.1": ["2.2"], "3.2": ["3.1"], "4.1": ["1.1"], "4.2": ["1.2", "4.1"], "4.3": ["4.2"],
                           "5.1": ["3.2", "4.2"], "5.2": ["5.1"], "6.1": ["1.2"], "6.2": ["6.1"], "7.2": ["5.2", "6.2"], "7.1": ["7.2"], "7.3": ["7.1"],
                           "8.1": ["2.2", "4.2"], "8.2": ["8.1", "4.3"], "9.1": ["4.2", "8.1"], "9.2": ["5.2", "2.1"]}),
 "statistics": ("SS", {"1.2": ["1.1"], "2.1": ["1.1"], "2.2": ["2.1"], "3.1": ["2.2", "1.2"], "4.1": ["3.1"], "5.1": ["1.1"], "6.1": ["2.2"], "6.2": ["6.1"], "6.3": ["6.1"],
                       "7.1": ["1.2", "6.1"], "8.1": ["4.1", "6.3"], "8.2": ["8.1"], "9.1": ["5.1", "8.2"], "9.2": ["9.1"], "10.1": ["8.2"],
                       "11.1": ["6.2", "6.3"], "11.2": ["6.3"], "12.1": ["5.1", "6.1"]}),
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


def add(L, i, need):
    m = re.search(r"needs: \[([^\]]*)\]", L[i])
    if not m:
        L[i] = re.sub(r"(, drills: \[)", r", needs: [], drills: [", L[i], count=1)
        m = re.search(r"needs: \[([^\]]*)\]", L[i])
    have = [s.strip() for s in m.group(1).split(",") if s.strip()]
    have += [n for n in need if n not in have]
    L[i] = L[i][:m.start()] + f"needs: [{', '.join(have)}]" + L[i][m.end():]


total = 0
for fw, table in EXPLICIT.items():
    p = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml")
    L = open(p).read().split("\n")
    where = {f"{u}.{t}.{lo}": i for i, u, t, lo in walk(L)}
    for code, need in table.items():
        key = code.split("-", 1)[1]
        assert key in where, code
        add(L, where[key], need); total += 1
    open(p, "w").write("\n".join(L))
for fw, (code, graph) in TOPICS.items():
    p = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml")
    L = open(p).read().split("\n")
    topics = {}
    for i, u, t, lo in walk(L):
        topics.setdefault(f"{u}.{t}", []).append((i, lo))
    for pre in graph.values():
        for x in pre: assert x in topics, (fw, x)
    for tp, los in topics.items():
        for k, (i, lo) in enumerate(los):
            need = [f"{code}-{tp}.{los[k - 1][1]}"] if k else [f"{code}-{pt}.{topics[pt][-1][1]}" for pt in graph.get(tp, [])]
            if need: add(L, i, need); total += 1
    open(p, "w").write("\n".join(L))
print("needs written on", total, "objectives")
