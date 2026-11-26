"""Scaffold a framework's path so it ramps from easy to hard (Nov 2026; the first step has to be a sure win and each
next step a small one). Within every topic, objectives are reordered recall → quick → workout by their slowest drill.
Stable: ties keep their file order. Drills inside an objective are left alone: a card picks among them at random, by
design.

Safe to run on any framework: an objective is never placed before one of its own `needs` in the same topic (the sort
is topological with pace as the tiebreak), so a stated prerequisite still comes first. Codes and letters never change
(RemNote ids are keyed by code); only line order moves. Unit order is set separately (a spec's UNIT_ORDER through
insert_objs.py).

Usage: python3 scripts/ramp.py <framework> [--dry]   or   python3 scripts/ramp.py --all [--dry]"""
import glob, os, re, sys, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RANK = {"recall": 0, "quick": 1, "workout": 2}
pace = {}
for f in glob.glob(os.path.join(ROOT, "drills/problems/*.yaml")):
    for t in yaml.safe_load(open(f)) or []:
        if isinstance(t, dict) and "template" in t:
            parts = t.get("parts") or []
            pace[t["template"]] = t.get("pace") or ("workout" if len(parts) > 1 else "quick")
rank = lambda d: RANK.get(pace.get(d, "workout"), 2)  # coded generators are guessed workouts, as the plugin does
LO = re.compile(r"^          - \{ id: ([A-Z]+),")


def lo_rank(ln):
    m = re.search(r"drills: \[([^\]]*)\]", ln)
    ds = [d.strip() for d in m.group(1).split(",") if d.strip()] if m else []
    return max((rank(d) for d in ds), default=2)


def needs_of(ln):
    m = re.search(r"needs: \[([^\]]*)\]", ln)
    return [s.strip() for s in m.group(1).split(",") if s.strip()] if m else []


def order(block, code, un, tn):
    """Stable topological sort of one topic's objective lines, pace as the priority."""
    letters = [LO.match(ln).group(1) for ln in block]
    here = {f"{code}-{un}.{tn}.{x}": x for x in letters}  # the codes that name an objective in this same topic
    dep = {x: set() for x in letters}
    for ln, x in zip(block, letters):
        for n in needs_of(ln):
            if n in here and here[n] != x: dep[x].add(here[n])
    by_letter = dict(zip(letters, block))
    ready = sorted(letters, key=lambda x: (lo_rank(by_letter[x]), letters.index(x)))
    out, done = [], set()
    while ready:
        for x in ready:
            if dep[x] <= done: break
        else:
            x = ready[0]  # a cycle among needs: leave the rest in file order rather than guess
        ready.remove(x); done.add(x); out.append(by_letter[x])
    return out


def run(fw):
    path = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml")
    L = open(path).read().split("\n")
    code = next((ln.split(":", 1)[1].strip() for ln in L if ln.startswith("code:")), fw.upper())
    moved, i, un, tn = 0, 0, None, None
    while i < len(L):
        m = re.match(r"^    n: (\d+)", L[i])
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", L[i])
        if m: tn = m.group(1)
        if not LO.match(L[i]): i += 1; continue
        j = i
        while j < len(L) and LO.match(L[j]): j += 1
        block = L[i:j]
        new = order(block, code, un, tn)
        if new != block: moved += 1; L[i:j] = new
        i = j
    if moved: print(f"{fw}: {moved} topics reordered")
    if "--dry" not in sys.argv and moved: open(path, "w").write("\n".join(L))
    return moved


if "--all" in sys.argv:
    tot = sum(run(os.path.basename(p)[:-5]) for p in sorted(glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml"))))
    print(f"total: {tot} topics reordered")
else:
    run(sys.argv[1])
