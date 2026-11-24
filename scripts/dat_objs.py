"""Write the new DAT objectives listed in scripts/second_specs/dat3.py (OBJS) into drills/frameworks/dat.yaml,
after the last objective of their topic. Idempotent: an objective already present is left alone."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import dat3
path = os.path.join(ROOT, "drills/frameworks/dat.yaml")
for code, sub, do, ek in dat3.OBJS:
    u, t, lo = code.split("-")[1].split(".")
    L = open(path).read().split("\n"); un = tn = None; last = None; have = False
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        if un == u and tn == t:
            m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
            if m:
                last = i
                if m.group(1) == lo: have = True
    if have: continue
    q = lambda x: '"' + x.replace('"', '\\"') + '"'
    L.insert(last + 1, f'          - {{ id: {lo}, std: ["ada-dat:{sub}"], do: {q(do)}, ek: [{q(ek)}], p: [P1, P2], drills: [] }}')
    open(path, "w").write("\n".join(L))
