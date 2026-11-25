"""Write new objectives from a second-spec module's OBJS (code, [std items], do, ek) into its framework file, after the
last objective of their topic, and add a module's EXISTING {code: [std items]} citations to objectives already there.
Idempotent. Usage: python3 scripts/insert_objs.py st3"""
import glob, importlib, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
mod = importlib.import_module(sys.argv[1])
path = os.path.join(ROOT, f"drills/frameworks/{mod.FRAMEWORK}.yaml")
q = lambda x: '"' + x.replace('"', '\\"') + '"'


def walk(L):
    un = tn = None
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        if m: yield i, un, tn, m.group(1)


for code, std, do, ek in getattr(mod, "OBJS", []):
    u, t, lo = code.split("-", 1)[1].split(".")
    L = open(path).read().split("\n")
    hits = [(i, x) for i, uu, tt, x in walk(L) if (uu, tt) == (u, t)]
    if not hits:
        # a new topic: OBJS may name it in TOPICS {"u.t": title}; it goes after the unit's last objective
        title = getattr(mod, "TOPICS", {}).get(f"{u}.{t}")
        last = [i for i, uu, tt, x in walk(L) if uu == u]
        if not title or not last: sys.exit(f"{code}: topic not found and no TOPICS title for {u}.{t}")
        L[last[-1] + 1:last[-1] + 1] = [f"      - n: {t}", f"        title: {q(title)}", "        los:"]
        open(path, "w").write("\n".join(L))
        hits = [(last[-1] + 3, "")]
    if lo in [x for _, x in hits]: continue
    L = open(path).read().split("\n")
    L.insert(hits[-1][0] + 1, f'          - {{ id: {lo}, std: [{", ".join(q(s) for s in std)}], do: {q(do)}, ek: [{q(ek)}], p: [P1], drills: [] }}')
    open(path, "w").write("\n".join(L))
L = open(path).read().split("\n")
for code, std in getattr(mod, "EXISTING", {}).items():
    u, t, lo = code.split("-", 1)[1].split(".")
    for i, uu, tt, x in walk(L):
        if (uu, tt, x) == (u, t, lo):
            m = re.search(r"std: \[([^\]]*)\]", L[i])
            have = [s.strip().strip('"') for s in m.group(1).split(",") if s.strip()]
            have += [s for s in std if s not in have]
            L[i] = L[i][:m.start()] + f'std: [{", ".join(q(s) for s in have)}]' + L[i][m.end():]
open(path, "w").write("\n".join(L))
