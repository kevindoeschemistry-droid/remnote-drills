"""Scaffold a framework's path so it ramps from easy to hard (Nov 2026; the first step has to be a sure win and each
next step a small one). Within every topic, objectives are reordered recall → quick → workout by their slowest drill.
Stable: ties keep their file order. Drills inside an objective are left alone: a card picks among them at random, by
design. Run it only on frameworks whose letter order carries no hidden prerequisite. Codes and letters are not
changed (RemNote ids are keyed by code); only line order moves, and the path's topological sort still puts any
`needs` first. Unit order is set separately (a spec's UNIT_ORDER through insert_objs.py).
Usage: python3 scripts/ramp.py nclex-rn [--dry]"""
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
def run(fw):
  path = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml")
  L = open(path).read().split("\n")
  LO = re.compile(r"^          - \{ id: [A-Z]+,")
  moved = 0
  i = 0
  while i < len(L):  # objectives within each topic (a run of consecutive objective lines)
      if not LO.match(L[i]): i += 1; continue
      j = i
      while j < len(L) and LO.match(L[j]): j += 1
      def lo_rank(ln):
          m = re.search(r"drills: \[([^\]]*)\]", ln)
          ds = [d.strip() for d in m.group(1).split(",") if d.strip()] if m else []
          return max((rank(d) for d in ds), default=2)
      block = L[i:j]; new = sorted(block, key=lo_rank)
      if new != block: moved += 1; L[i:j] = new
      i = j
  print(f"{fw}: {moved} topics or objectives reordered")
  if "--dry" not in sys.argv: open(path, "w").write("\n".join(L))

run(sys.argv[1])
