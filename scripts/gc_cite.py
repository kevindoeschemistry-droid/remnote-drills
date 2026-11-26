#!/usr/bin/env python3
"""Cite the three new standards on objectives that already answer them (add-only, idempotent).

Graduate ChemE's own units cite the crosswalk from its spec (scripts/opl_specs/gc.py), because opl_fill.py
regenerates that framework's block and drops anything written into the YAML. What is left for a cite script:

  cheme-grad-core:MM.5  integral transforms and complex-variable methods, which Engineering Math already teaches
  cheme-grad-core:PS.3  process modelling, systems thinking and optimisation, which Process Design already teaches
  icheme-level-f:A2.6   Level F process safety, likewise Process Design's
  icheme-level-f:A2.7   Level F sustainability, economics and ethics, likewise
  aiche-bok:*           plant practice: it is staged by career rather than by degree, so it belongs on the
                        undergraduate-to-practice frameworks and never on the graduate one

RUN ORDER MATTERS. This script, like every other cite script, writes `std` lists into framework YAML, and
scripts/opl_fill.py regenerates the blocks between its markers from the specs. Run opl_fill.py FIRST and the
cite scripts after it, or the citations are silently dropped: that is how acs-accm-analytical's citations
vanished from chemistry-olympiad.yaml in Nov 2026.
"""
import glob, pathlib, re, sys, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

CITE = {
    # Integral transforms and complex-variable methods: the Laplace/Fourier work on PDEs, residue inversion,
    # and Cauchy's formula and residues themselves.
    "cheme-grad-core:MM.5": ["EM-10.5.A", "EM-10.5.B", "EM-11.1.B", "EM-11.1.E", "EM-14.3.A", "EM-14.3.D"],
    # Process modelling, systems thinking and optimisation.
    "cheme-grad-core:PS.3": ["PD-5.1.A", "PD-5.1.B", "PD-8.2.A", "PD-8.2.C"],
    # Level F process safety: the same principles with systems thinking on more complex problems.
    "icheme-level-f:A2.6": ["PD-2.1.C", "PD-6.1.A", "PD-6.1.D", "PD-6.3.A", "PD-6.3.B"],
    # Level F sustainability, economics and ethics in situations with conflicting requirements.
    "icheme-level-f:A2.7": ["PD-1.1.B", "PD-5.2.C", "PD-6.3.C", "PD-7.1.A", "PD-7.2.A"],
    # AIChE's technical skills, on the frameworks that teach them.
    "aiche-bok:T.BAL": ["PD-5.1.B", "TD-7.2.B"],
    "aiche-bok:T.EQ": ["TD-9.3.A", "TD-9.4.C", "TD-22.1.D"],
    "aiche-bok:T.FLOW": ["FM-4.2.A", "FM-4.2.B", "FM-10.1.C"],
    "aiche-bok:T.DES": ["PD-5.1.A", "PD-5.2.A", "PD-5.2.B"],
    "aiche-bok:T.INST": ["PD-5.1.C", "PD-10.2.A", "PD-10.2.B", "PD-10.2.C"],
    "aiche-bok:T.OPT": ["PD-8.2.C", "PD-10.1.A", "PD-10.1.C"],
    "aiche-bok:T.SU": ["PD-5.2.A", "FM-10.1.B"],
    "aiche-bok:X.SAFE": ["PD-2.1.A", "PD-2.1.B", "PD-6.1.A", "PD-5.2.D"],
}

# objective code -> the codes to add
WANT = {}
for std, codes in CITE.items():
    for c in codes:
        WANT.setdefault(c, []).append(std)


def main():
    files = sorted(glob.glob(str(ROOT / "drills" / "frameworks" / "*.yaml")))
    seen, added, lines_touched = set(), 0, 0
    for f in files:
        p = pathlib.Path(f)
        d = yaml.safe_load(p.read_text())
        code = d.get("code")
        if not code or not any(k.startswith(code + "-") for k in WANT):
            continue
        text = p.read_text()
        # Walk the parsed structure for the codes we want, then edit those exact lines, found by the objective's
        # own `do` text, which is unique within a file.
        out = text.splitlines(True)
        for u in d["units"]:
            for t in u["topics"]:
                for lo in t["los"]:
                    full = f"{code}-{u['n']}.{t['n']}.{lo['id']}"
                    if full not in WANT:
                        continue
                    seen.add(full)
                    cur = lo.get("std") or []
                    cur = [cur] if isinstance(cur, str) else list(cur)
                    new = [s for s in WANT[full] if s not in cur]
                    if not new:
                        continue
                    merged = cur + new
                    # The objective's own line, found by its `do` text, which is unique within a file.
                    needle = lo["do"].replace('"', '\\"')
                    hits = [i for i, l in enumerate(out) if f'id: {lo["id"]},' in l and needle in l]
                    if len(hits) != 1:
                        print(f"  ! {full}: {len(hits)} matching lines, skipped")
                        continue
                    i = hits[0]
                    line = out[i]
                    rendered = "[" + ", ".join(f'"{s}"' for s in merged) + "]"
                    if "std: [" in line:
                        line = re.sub(r"std: \[[^\]]*\]", "std: " + rendered, line, count=1)
                    elif re.search(r"std: \S+?,", line):
                        line = re.sub(r"std: [^,]+,", "std: " + rendered + ",", line, count=1)
                    else:
                        line = line.replace(f"{{ id: {lo['id']}, ", f"{{ id: {lo['id']}, std: {rendered}, ", 1)
                    assert line.count("std:") == 1, f"{full}: two std keys on one line"
                    out[i] = line
                    added += len(new)
                    lines_touched += 1
        new_text = "".join(out)
        if new_text != text:
            p.write_text(new_text)
            check = yaml.safe_load(p.read_text())
            assert check is not None, f"{p.name} no longer parses"
    missing = sorted(set(WANT) - seen)
    if missing:
        print("  ! objectives not found:", ", ".join(missing))
    print(f"  {added} citations added across {lines_touched} objective lines")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
