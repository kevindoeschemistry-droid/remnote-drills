"""Rename the old ASBMB citations T1–T18 to the paper's theme codes and replace the asbmb-core-2013 standard's items with
its 26 themes (scripts/second_specs/bc2.py). Idempotent. Then run insert_objs.py bc2 and second_types.py."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts/second_specs"))
import bc2
for f in ["drills/frameworks/biochemistry.yaml", "scripts/second_specs/bc.py"]:
    p = os.path.join(ROOT, f); s = open(p).read()
    s = re.sub(r"asbmb-core-2013:(T\d+)\b", lambda m: "asbmb-core-2013:" + bc2.OLD[m.group(1)], s)
    open(p, "w").write(s)
# bc.py builds its citations with T(n): point it at the theme codes too
p = os.path.join(ROOT, "scripts/second_specs/bc.py"); s = open(p).read()
s = s.replace('T = lambda *n: [f"asbmb-core-2013:T{x}" for x in n]',
              '_OLD = ["1.1", "1.3", "1.4", "1.5", "2.2", "2.3", "2.4", "3.2", "3.5", "3.6", "4.1", "4.2", "4.3", "4.4", "5.1", "5.2", "5.3", "5.7"]\n'
              'T = lambda *n: [f"asbmb-core-2013:{_OLD[x - 1]}" for x in n]  # the paper\'s themes with a sample outcome, in order (bc2.py)')
open(p, "w").write(s)
items = [{"code": f"{c}.{i}", "title": f"{concept}: {t}"} for c, concept, ts in bc2.THEMES for i, t in enumerate(ts, 1)]
std = {"id": "asbmb-core-2013", "name": "ASBMB core concepts for biochemistry and molecular biology (Tansey et al., BAMBED 41:289, 2013)",
       "publisher": "American Society for Biochemistry and Molecular Biology", "kind": "standard", "read": "full",
       "url": "https://doi.org/10.1002/bmb.20727",
       "note": "Read in full (Nov 2026, open copy at core.ac.uk): five core concepts and 26 themes, eighteen of them with sample 'students should be able to' outcomes. The paper does not number them; codes 1.1-5.7 are ours and the titles paraphrase it.",
       "items": items}
p = os.path.join(ROOT, "drills/standards.yaml"); L = open(p).read().split("\n")
i = next(k for k, ln in enumerate(L) if '"id": "asbmb-core-2013"' in ln or "id: asbmb-core-2013," in ln)
L[i] = "- " + json.dumps(std, ensure_ascii=False)
open(p, "w").write("\n".join(L))
p = os.path.join(ROOT, "scripts/bc_framework.py"); s = open(p).read()
s = s.replace('"read": "part",\n     "url": "https://doi.org/10.1002/bmb.20727"', '"read": "full",\n     "url": "https://doi.org/10.1002/bmb.20727"')
open(p, "w").write(s)
print(len(items), "themes")
