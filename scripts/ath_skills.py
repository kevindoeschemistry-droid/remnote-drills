"""Create the swim.* and wushu.* drill skills, their domains and the library subject, and point the Swimming and
Wushu frameworks at them. Idempotent; run before second_types.py for scripts/second_specs/ath.py."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = lambda s: json.dumps(s, ensure_ascii=False)
SK = [("swim", "Swimming", [("rules", "World Aquatics rules, legal strokes and disqualifications", "Swim rules"),
                            ("pacing", "Race analysis: pace, splits, stroke rate and distance per cycle", "Race analysis"),
                            ("training", "Training science: CSS, intervals, volume and taper", "Swim training")]),
      ("wushu", "Wushu", [("judging", "Taolu judging: score structure, panel marks and the Duanwei ladder", "Wushu judging")])]
p = os.path.join(ROOT, "drills/skills.yaml"); L = open(p).read().split("\n")
for dom, title, skills in SK:
    if not any(f"id: {dom}," in ln for ln in L):
        i = next(k for k, ln in enumerate(L) if "id: cpd," in ln)
        L.insert(i + 1, f'  - {{ id: {dom}, title: {q(title)} }}')
    if not any(f"{dom}.{skills[0][0]}" in ln for ln in L):
        i = max(k for k, ln in enumerate(L) if "domain: cpd," in ln)
        L[i + 1:i + 1] = [f'  - {{ id: {dom}.{a}, domain: {dom}, title: {q(b)}, short: {q(c)} }}' for a, b, c in skills]
open(p, "w").write("\n".join(L))
p = os.path.join(ROOT, "drills/library.yaml"); L = open(p).read().split("\n")
if not any(ln.strip() == '- "Athletics"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Protein Design"')
    L.insert(i + 1, '  - "Athletics"')
for dom, _, _ in SK:
    if not any(ln.startswith(f"  {dom}:") for ln in L):
        i = next(k for k, ln in enumerate(L) if ln.startswith("  cpd:"))
        L.insert(i + 1, f'  {dom}: "Athletics"')
open(p, "w").write("\n".join(L))
for fw, dom in [("swimming", "swim"), ("wushu", "wushu")]:
    p = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml"); s = open(p).read()
    if "domains: []" in s: open(p, "w").write(s.replace("domains: []", f"domains: [{dom}]", 1))
print("ok")
