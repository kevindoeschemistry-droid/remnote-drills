"""Register the ACS general, organic, inorganic and analytical content maps in drills/standards.yaml (from scripts/accm_maps.py)
and write their citations onto the Library objectives (add-only, idempotent). Usage: python3 scripts/accm_cite2.py"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from accm_maps import MAPS
import accm_anal
MAPS = dict(MAPS); MAPS["acs-accm-analytical"] = (accm_anal.ITEMS, accm_anal.CITE)

META = {
    "acs-accm-general": ("ACS Exams Institute Anchoring Concepts Content Map: General Chemistry (Holme, Luxford & Murphy, J. Chem. Educ. 2015, 92, 1115)",
                         "https://pubs.acs.org/doi/10.1021/ed500712k",
                         "The updated map's supporting information was read in full (Nov 2026; Kevin supplied the file), as was the 2012 map it supersedes (Holme & Murphy, ed300050q). Items are the 140 subdisciplinary articulations plus the three enduring understandings that have none (III.C–E); titles are our paraphrases. Citations are kept in scripts/accm_maps.py."),
    "acs-accm-organic": ("ACS Exams Institute Anchoring Concepts Content Map: Organic Chemistry (Raker, Holme & Murphy, J. Chem. Educ. 2013, 90, 1443)",
                         "https://pubs.acs.org/doi/10.1021/ed400175w",
                         "The supporting-information outline was read in full (Nov 2026; Kevin supplied the PDF). Items are the 93 subdisciplinary articulations plus the eleven enduring understandings that have none; titles are our paraphrases. Citations are kept in scripts/accm_maps.py."),
    "acs-accm-inorganic": ("ACS Exams Institute Anchoring Concepts Content Map: Inorganic Chemistry (Marek, Raker, Holme & Murphy, J. Chem. Educ. 2018, 95, 233)",
                           "https://pubs.acs.org/doi/10.1021/acs.jchemed.7b00498",
                           "The supporting-information outline was read in full (Nov 2026; Kevin supplied the PDF): 201 subdisciplinary articulations; titles are our paraphrases. Citations are kept in scripts/accm_maps.py."),
    "acs-accm-analytical": ("ACS Exams Institute Anchoring Concepts Content Map: Analytical Chemistry (Holme, Bauer, Trate, Reed, Raker & Murphy, J. Chem. Educ. 2020, ed9b00856)",
                            "https://pubs.acs.org/doi/10.1021/acs.jchemed.9b00856",
                            "The supporting-information outline (April 2020 version) was read in full (Nov 2026; Kevin supplied the PDF): 109 subdisciplinary articulations; titles are our paraphrases. Citations are kept in scripts/accm_anal.py."),
}

sp = os.path.join(ROOT, "drills/standards.yaml"); S = open(sp).read()
for sid, (items, _) in MAPS.items():
    name, url, note = META[sid]
    line = "- " + json.dumps({"id": sid, "name": name, "publisher": "ACS Exams Institute", "kind": "standard", "read": "full", "url": url, "note": note,
                              "items": [{"code": c, "title": t} for c, t in items]}, ensure_ascii=False)
    S = re.sub(rf"^- \{{\"id\": \"{sid}\".*$\n?", "", S, flags=re.M)
    S = S.rstrip("\n") + "\n" + line + "\n"
open(sp, "w").write(S)

FW = {}
for f in glob.glob(os.path.join(ROOT, "drills/frameworks/*.yaml")):
    m = re.search(r"^code: *(\S+)", open(f).read(), re.M)
    if m: FW[m.group(1)] = f
by = {}
for sid, (_, cite) in MAPS.items():
    for item, codes in cite.items():
        for code in codes:
            by.setdefault(code.split("-")[0], {}).setdefault(code, []).append(f"{sid}:{item}")
q = lambda x: '"' + x + '"'
missing = []
for pre, codes in by.items():
    path = FW[pre]; L = open(path).read().split("\n"); un = tn = None; done = set()
    for i, ln in enumerate(L):
        m = re.match(r"^    n: (\d+)", ln)
        if m: un, tn = m.group(1), None
        m = re.match(r"^      - n: (\d+)", ln)
        if m: tn = m.group(1)
        m = re.match(r"^          - \{ id: ([A-Z]+),", ln)
        code = m and f"{pre}-{un}.{tn}.{m.group(1)}"
        if code in codes:
            done.add(code); std = codes[code]
            m2 = re.search(r"std: \[([^\]]*)\]", ln)
            if m2:
                have = [s.strip().strip('"') for s in m2.group(1).split(",") if s.strip()]
                have += [s for s in std if s not in have]
                L[i] = ln[:m2.start()] + f"std: [{', '.join(q(s) for s in have)}]" + ln[m2.end():]
            else:
                L[i] = re.sub(r"^(\s+- \{ id: [A-Z]+, )", lambda mm: mm.group(1) + f"std: [{', '.join(q(s) for s in std)}], ", ln)
    missing += sorted(set(codes) - done)
    open(path, "w").write("\n".join(L))
    # the framework's basis must name every standard it cites
    T = open(path).read(); sids = sorted({s.split(":")[0] for v in codes.values() for s in v})
    m = re.search(r"^basis:\n((?:  .*\n)+)", T, re.M)
    blk = m.group(1); prim = re.search(r"primary: *(\S+)", blk); prim = prim and prim.group(1)
    am = re.search(r"^  also: \[([^\]]*)\]", blk, re.M)
    also = [s.strip() for s in am.group(1).split(",") if s.strip()] if am else []
    add = [s for s in sids if s != prim and s not in also]
    if add:
        new = f"  also: [{', '.join(also + add)}]"
        blk2 = blk.replace(am.group(0), new) if am else blk.replace(f"  primary: {prim}\n", f"  primary: {prim}\n{new}\n")
        T = T.replace(blk, blk2, 1); open(path, "w").write(T)
if missing: sys.exit(f"objectives not found: {missing}")
print("cited", sum(len(v) for v in by.values()), "objectives across", len(by), "frameworks")
