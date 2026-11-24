"""Second question types for DAT Perceptual Ability, built on the figures of dat-pat.yaml (run after pat_cases.py).

Each new template reuses a first template's cases and figure and asks a different question about the same drawing:
  pat-angle-largest       which of the four angles is largest            (rank_code, last label)
  pat-cube-total          how many cubes the figure holds in all         (sum of the column heights)
  pat-punch-half          how many holes land in one half of the sheet   (pat_punch_half: layers under the punch, per half)
  pat-net-adjacent        are two named faces opposite or adjacent       (net_opposite)
The generator answers from the case data (the hole list, the opposite face, the heights); the verifier recomputes
from the fold sequence, the net cells and the heights. Writes drills/problems/dat-pat-second.yaml.
"""
import copy, os, random, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = yaml.safe_load(open(os.path.join(ROOT, "drills/problems/dat-pat.yaml")))
by = {t["template"]: t for t in src}
out = []

# ── angles: which is largest ─────────────────────────────────────────────
t = copy.deepcopy(by["pat-angle-ranking"])
t["template"] = "pat-angle-largest"
t["pace"] = "recall"
t["prompt"] = "Which of the four angles is the largest? Type its label (1, 2, 3 or 4)."
t["parts"] = [{"ask": "Largest angle", "label": "r", "tex": "\\text{label}", "value": "mod(ord, 10)", "tol": 1e-05, "final": True,
               "explain": "Compare only the openings at the vertices, never the arm lengths. The angles are ${{base + d1}}^\\circ$, ${{base + d2}}^\\circ$, ${{base + d3}}^\\circ$ and ${{base + d4}}^\\circ$"}]
t["verify"] = {"expect": {"r": "rank_code([d1, d2, d3, d4]) % 10"}}
out.append(t)

# ── cubes: total count ───────────────────────────────────────────────────
t = copy.deepcopy(by["pat-cube-counting"])
t["template"] = "pat-cube-total"
t["prompt"] = "The cubes are cemented together; some are hidden behind or under others. How many cubes are in the figure?"
t["parts"] = [{"ask": "Number of cubes", "label": "r", "tex": "n", "value": "tot", "tol": 1e-05, "final": True,
               "explain": "Count column by column: each visible top stands on a full stack down to the table, so hidden cubes are counted by height. Total ${{tot}}$"}]
hs = ", ".join(f"h{r}{c}" for r in (1, 2, 3) for c in (1, 2, 3))
t["verify"] = {"expect": {"r": " + ".join(f"h{r}{c}" for r in (1, 2, 3) for c in (1, 2, 3))}}
for c in t["cases"]:
    assert c["tot"] == sum(c[f"h{r}{k}"] for r in (1, 2, 3) for k in (1, 2, 3)), c
seen, uniq = set(), []
for c in t["cases"]:
    key = tuple(c[f"h{r}{k}"] for r in (1, 2, 3) for k in (1, 2, 3))
    if key not in seen:
        seen.add(key); uniq.append(c)
t["cases"] = uniq
out.append(t)

# ── hole punching: holes in one half ─────────────────────────────────────
t = copy.deepcopy(by["pat-hole-punching"])
t["template"] = "pat-punch-half"
t["prompt"] = ("A square sheet (dashed outline, a 4 by 4 grid) is folded: {{how}} The solid outline is the folded paper. A hole is punched at the dot. "
               "When the sheet is unfolded, how many holes are in its {{half}} half?")
cases = []
for c in t["cases"]:
    holes = [tuple(int(v) for v in re.findall(r"\d+", h)) for h in c["where"].split(";")]
    assert len(holes) == c["n"], c
    left = sum(1 for r, col in holes if col <= 2)
    right = c["n"] - left
    for half, code, cnt in (("left", -1, left), ("right", 1, right)):
        if cnt:
            d = dict(c, half=half, hs=code, m=cnt)
            cases.append(d)
t["cases"] = cases
t["parts"] = [{"ask": "Holes in that half", "label": "r", "tex": "n", "value": "m", "tol": 1e-05, "final": True,
               "explain": "Unfold in reverse, mirroring each hole across each fold line, then look only at the columns asked about. Holes at: {{where}} (rows from the top, columns from the left)"}]
t["verify"] = {"expect": {"r": "pat_punch_half([fd for fd in [(a1, l1, s1), (a2, l2, s2)] if fd[2] != 0], px, py, hs)"}}
out.append(t)

# ── cube nets: opposite or adjacent ──────────────────────────────────────
t = copy.deepcopy(by["pat-cube-net-opposite"])
t["template"] = "pat-net-adjacent"
t["pace"] = "quick"
t["prompt"] = "This flat pattern folds into a cube. When folded, are faces {{face}} and {{other}} opposite each other or adjacent?"
L = "ABCDEF"
rng = random.Random(4)
cases = []
for c in t["cases"]:
    others = [i for i in range(6) if i not in (c["q"], c["ans"])]
    for y in (c["ans"], rng.choice(others)):
        cases.append(dict(c, y=y, other=L[y], adj=0 if y == c["ans"] else 1))
t["cases"] = cases
t["parts"] = [{"ask": "Opposite or adjacent", "label": "a", "choice": ["Opposite", "Adjacent"], "correct": "adj",
               "explain": "Every face touches four others and is opposite exactly one. Squares in a line with one square between them are opposite; any two squares sharing an edge, or meeting at a fold, are adjacent. {{face}} is opposite {{opp}}"}]
t["verify"] = {"choices": {"a": "0 if net_opposite([(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)], q) == y else 1"}}
out.append(t)

head = "# Generated by scripts/pat_second.py from dat-pat.yaml: edit the script, not this file.\n# Second question types on the same Perceptual Ability figures.\n\n"
open(os.path.join(ROOT, "drills/problems/dat-pat-second.yaml"), "w").write(
    head + yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=10000, default_flow_style=False))
print("pat second types:", ", ".join(f"{t['template']} ({len(t['cases'])} cases)" for t in out))
