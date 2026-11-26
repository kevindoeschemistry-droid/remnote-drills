"""Write new objectives from a second-spec module's OBJS (code, [std items], do, ek, and optionally a practice id)
into its framework file, after the
last objective of their topic, and add a module's EXISTING {code: [std items]} citations to objectives already there.
NEEDS {code: [codes]} adds prerequisites; UNIT_ORDER [unit ids] reorders unit blocks without renumbering. Idempotent. Usage: python3 scripts/insert_objs.py st3"""
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


for entry in getattr(mod, "OBJS", []):
    # a 5th element overrides the module's PRACTICE for that objective
    code, std, do, ek = entry[:4]
    prac = entry[4] if len(entry) > 4 else getattr(mod, "PRACTICE", "P1")
    u, t, lo = code.split("-", 1)[1].split(".")
    L = open(path).read().split("\n")
    hits = [(i, x) for i, uu, tt, x in walk(L) if (uu, tt) == (u, t)]
    if not hits:
        # a new topic: OBJS may name it in TOPICS {"u.t": title}; it goes after the unit's last objective
        title = getattr(mod, "TOPICS", {}).get(f"{u}.{t}")
        last = [i for i, uu, tt, x in walk(L) if uu == u]
        unit = getattr(mod, "UNITS", {}).get(u)
        if not last and unit and title:
            # a new unit: UNITS {"u": (id, title, [ideas], [std])}; appended at the end of the file (units: is last)
            uid, utitle, ideas, ustd = unit
            while L and not L[-1].strip(): L.pop()
            L += [f"  - id: {uid}", f"    n: {u}", f"    title: {q(utitle)}", f"    std: [{', '.join(q(s) for s in ustd)}]",
                  "    scope: extension", f"    ideas: [{', '.join(ideas)}]", "    topics:",
                  f"      - n: {t}", f"        title: {q(title)}", "        los:", ""]
            open(path, "w").write("\n".join(L))
            L = open(path).read().split("\n")
            last = [len(L) - 5]  # so the topic is added after this unit's (empty) los line below
            hits = [(len(L) - 2, "")]
            if lo in [x for _, x in hits]: continue
            L.insert(hits[-1][0] + 1, f'          - {{ id: {lo}, std: [{", ".join(q(s) for s in std)}], do: {q(do)}, ek: [{q(ek)}], p: [{prac}], drills: [] }}')
            open(path, "w").write("\n".join(L))
            continue
        if not title or not last: sys.exit(f"{code}: topic not found and no TOPICS title for {u}.{t}")
        L[last[-1] + 1:last[-1] + 1] = [f"      - n: {t}", f"        title: {q(title)}", "        los:"]
        open(path, "w").write("\n".join(L))
        hits = [(last[-1] + 3, "")]
    if lo in [x for _, x in hits]: continue
    L = open(path).read().split("\n")
    L.insert(hits[-1][0] + 1, f'          - {{ id: {lo}, std: [{", ".join(q(s) for s in std)}], do: {q(do)}, ek: [{q(ek)}], p: [{prac}], drills: [] }}')
    open(path, "w").write("\n".join(L))
L = open(path).read().split("\n")
for code, std in getattr(mod, "EXISTING", {}).items():
    u, t, lo = code.split("-", 1)[1].split(".")
    for i, uu, tt, x in walk(L):
        if (uu, tt, x) == (u, t, lo):
            m = re.search(r"std: \[([^\]]*)\]", L[i])
            if not m:  # no std yet: add one after the id
                L[i] = L[i].replace(f"id: {lo},", f"id: {lo}, std: [],", 1)
                m = re.search(r"std: \[([^\]]*)\]", L[i])
            have = [s.strip().strip('"') for s in m.group(1).split(",") if s.strip()]
            have += [s for s in std if s not in have]
            L[i] = L[i][:m.start()] + f'std: [{", ".join(q(s) for s in have)}]' + L[i][m.end():]
# NEEDS {code: [prerequisite codes]}: add-only prerequisites, which the path's topological sort honours
fw_code = None
for code, need in getattr(mod, "NEEDS", {}).items():
    u, t, lo = code.split("-", 1)[1].split(".")
    for i, uu, tt, x in walk(L):
        if (uu, tt, x) != (u, t, lo): continue
        m = re.search(r"needs: \[([^\]]*)\]", L[i])
        if not m:
            L[i] = re.sub(r"(, drills: \[)", r", needs: [], drills: [", L[i], count=1)
            m = re.search(r"needs: \[([^\]]*)\]", L[i])
        have = [s.strip() for s in m.group(1).split(",") if s.strip()]
        have += [n for n in need if n not in have]
        L[i] = L[i][:m.start()] + f"needs: [{', '.join(have)}]" + L[i][m.end():]
        break
    else:
        sys.exit(f"NEEDS: {code} not found")
# UNIT_ORDER [unit ids]: reorder whole unit blocks in the file (codes keep their n, so card ids are unchanged)
order = getattr(mod, "UNIT_ORDER", None)
if order:
    start = L.index("units:") + 1
    blocks, cur = {}, None
    for ln in L[start:]:
        m = re.match(r"^  - id: (\S+)", ln)
        if m: cur = m.group(1); blocks[cur] = []
        if cur: blocks[cur].append(ln)
    assert sorted(order) == sorted(blocks), (order, list(blocks))
    L = L[:start] + [ln for uid in order for ln in blocks[uid]]
open(path, "w").write("\n".join(L))
