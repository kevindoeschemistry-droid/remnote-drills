"""Second question types for the Periodic Table framework (PT): each recall objective asked the other way round
(number → element, group → element, count → ion), plus unpaired electrons and pick-the-configuration items. The element
list is read from scripts/pt_cases.py and configurations from pt-periodic.yaml; the verifier works from its own
period-by-period table (pt_Z, pt_group, pt_config)."""
import os, random
import yaml
from opl_dsl import Q

FILE, FRAMEWORK = "pt-second-types", "periodic-table"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ns = {}
exec(open(os.path.join(HERE, "pt_cases.py")).read().split("\nout = [")[0], ns)
EL, SYM, DBLOCK, FBLOCK, MAIN, dgroup = ns["EL"], ns["SYM"], ns["DBLOCK"], ns["FBLOCK"], ns["MAIN"], ns["dgroup"]
PT = {t["template"]: t for t in yaml.safe_load(open(os.path.join(os.path.dirname(HERE), "drills/problems/pt-periodic.yaml")))}
rng = random.Random(11)
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
G3 = {57, 71, 89, 103}  # group 3 below yttrium is never asked


def name(z):
    return f"{EL[z - 1][0]} ({SYM[z - 1]})"


def pick(z, pool, k=3):
    """three distractors near z in the pool"""
    near = sorted((p for p in pool if p != z), key=lambda p: (abs(p - z), rng.random()))[:6]
    return rng.sample(near, k)


def z_to_element(zs):
    rows = []
    for z in zs:
        d = pick(z, zs)
        rows.append({"Zn": z, "o1": name(z), "o2": name(d[0]), "o3": name(d[1]), "o4": name(d[2]), "s1": SYM[z - 1]})
    return rows


ADD = [
    ("PT-1.1.A", Q("pt-element-from-z-main", "ptable.numbers", "Which main-group element has atomic number {{Zn}}?", pace="recall",
        cases=z_to_element([z for z in MAIN if z <= 88]), choice=MC, correct="0", verify="0 if pt_Z(s1) == Zn else 9",
        explain="Anchor on the noble gases (2, 10, 18, 36, 54, 86) and count along the period")),
    ("PT-1.1.B", Q("pt-p6-next", "ptable.numbers", "In the sixth period's p block, which element comes right after {{prev}}?", pace="recall",
        cases=[{"prev": name(z), "zp": z, "o1": name(z + 1), **{f"o{k + 2}": name(w) for k, w in enumerate(rng.sample([w for w in range(81, 87) if w not in (z, z + 1)], 2) + [z + 1 - 32])}, "s1": SYM[z]}
               for z in range(81, 86)], choice=MC, correct="0", verify="0 if pt_Z(s1) == zp + 1 else 9",
        explain="Tl, Pb, Bi, Po, At, Rn: groups 13 to 18, under In, Sn, Sb, Te, I, Xe")),
    ("PT-2.1.A", Q("pt-element-from-z-d", "ptable.d-block", "Which transition metal has atomic number {{Zn}}?", pace="recall",
        cases=z_to_element([z for z in DBLOCK if z not in G3]), choice=MC, correct="0", verify="0 if pt_Z(s1) == Zn else 9",
        explain="3d runs 21–30, 4d 39–48, 5d 72–80, 6d 104–112")),
    ("PT-2.1.B", Q("pt-metal-in-group", "ptable.d-block", "Which {{row}} metal is in group {{g}}?", pace="recall",
        cases=[{"row": r, "g": dgroup(z), "o1": name(z), "o2": name(d[0]), "o3": name(d[1]), "o4": name(d[2]), "s1": SYM[z - 1]}
               for r, zs in (("3d", range(21, 31)), ("4d", range(39, 49)), ("5d", range(72, 81))) for z in zs for d in [pick(z, list(zs))]],
        choice=MC, correct="0", verify="0 if pt_group(pt_Z(s1)) == g else 9", explain="Group = position in the d row + 2 (Sc, Y in 3; Zn, Cd, Hg in 12)")),
    ("PT-2.2.A", Q("pt-ox-from-d", "ptable.d-block", "{{nm}} ({{sy}}) is in a compound as a d{{dn}} ion. What is its oxidation state?", pace="recall",
        cases=[{"nm": EL[z - 1][0], "sy": SYM[z - 1], "dn": dn, "g": dgroup(z)} for z in list(range(22, 30)) + [40, 42, 44, 46, 74, 76, 78]
               for dn in sorted({dgroup(z) - k for k in (2, 3, 4)}) if 0 < dgroup(z) - dn <= 8 and dn >= 0],
        value="g - dn", tex="", final=True, verify="pt_group(pt_Z(sy)) - dn", explain="Oxidation state = group − d count")),
    ("PT-3.1.A", Q("pt-element-from-z-f", "ptable.f-block", "Which lanthanoid or actinoid has atomic number {{Zn}}?", pace="recall",
        cases=z_to_element([z for z in FBLOCK if z not in G3]), choice=MC, correct="0", verify="0 if pt_Z(s1) == Zn else 9",
        explain="La 57 to Lu 71, Ac 89 to Lr 103: Gd (64) and Cm (96) sit at the half-filled middle")),
    ("PT-3.1.C", Q("pt-ln-from-f", "ptable.f-block", "Which lanthanoid ion M³⁺ has exactly {{fn}} 4f electrons?", pace="recall",
        cases=[{"fn": z - 57, "o1": name(z) + "³⁺", "o2": name(d[0]) + "³⁺", "o3": name(d[1]) + "³⁺", "o4": name(d[2]) + "³⁺", "s1": SYM[z - 1]}
               for z in range(58, 71) for d in [pick(z, list(range(58, 71)))]],
        choice=MC, correct="0", verify="0 if pt_Z(s1) - 3 - pt_Z('Xe') == fn else 9", explain="Ln³⁺ has Z − 57 4f electrons: Ce³⁺ f¹ … Gd³⁺ f⁷ … Lu³⁺ f¹⁴")),
]

# configurations: unpaired electrons, and choose the right configuration
d_cases = PT["pt-config-anomaly"]["cases"]
unp = [{"nm": c["nm"], "sy": c["sy"], "u": (c["dn"] if c["dn"] <= 5 else 10 - c["dn"]) + (1 if c["sn"] == 1 else 0)} for c in d_cases if c["sy"] not in ("Lu", "Lr")]
ADD.append(("PT-4.1.B", Q("pt-unpaired-atom", "ptable.configurations", "How many unpaired electrons does a ground-state {{nm}} atom ({{sy}}) have?", pace="quick",
    cases=[c for c in unp if c["u"] > 0], value="u", tex="", final=True,
    verify="(pt_config(sy)[1] if pt_config(sy)[1] <= 5 else 10 - pt_config(sy)[1]) + (1 if pt_config(sy)[2] == 1 else 0)",
    explain="Fill the d set by Hund's rule (one in each before pairing) and count a lone s electron; Cr (d⁵s¹) has six")))


def sup(k):
    return "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(ch)] for ch in str(k))


def cfg(core, dl, d, sl, s, fl="", f=0):
    parts = [core] + ([f"{fl}{sup(f)}"] if f else []) + ([f"{dl}{sup(d)}"] if d else []) + ([f"{sl}{sup(s)}"] if s else [])
    return " ".join(parts)


rows = []
for c in d_cases:
    if c["sy"] in ("Lu", "Lr"):
        continue
    dl, sl = c["dt"].rstrip("⁰¹²³⁴⁵⁶⁷⁸⁹"), c["st"].rstrip("⁰¹²³⁴⁵⁶⁷⁸⁹")
    right = cfg(c["core"], dl, c["dn"], sl, c["sn"])
    alts = {cfg(c["core"], dl, c["dn"] + 1, sl, c["sn"] - 1) if c["sn"] >= 1 and c["dn"] < 10 else None,
            cfg(c["core"], dl, c["dn"] - 1, sl, c["sn"] + 1) if c["sn"] < 2 and c["dn"] >= 1 else None,
            cfg(c["core"], dl, c["dn"] + c["sn"], sl, 0) if c["dn"] + c["sn"] <= 10 else None,
            cfg(c["core"], dl, max(c["dn"] - 2, 0), sl, 2) + "*",
            cfg(c["core"], dl, c["dn"] + 1, sl, c["sn"]) + "*"} - {None, right}
    alts = [a.rstrip("*") for a in alts if a.rstrip("*") != right][:3]
    if len(alts) == 3:
        rows.append({"nm": c["nm"], "sy": c["sy"], "o1": right, "o2": alts[0], "o3": alts[1], "o4": alts[2]})
ADD.append(("PT-4.1.C", Q("pt-config-pick-d", "ptable.configurations", "Which is the ground-state configuration of {{nm}} ({{sy}})?", pace="quick",
    cases=rows, choice=MC, correct="0", verify="authored",
    explain="Count electrons past the core: s² then d, except Cr, Cu and their 4d relatives (and Pd, Pt, Au), which move an s electron into d")))

f_cases = PT["pt-config-f-count"]["cases"]
ADD.append(("PT-4.2.A", Q("pt-atom-from-f", "ptable.configurations", "Which lanthanoid or actinoid atom has exactly {{fn}} f electrons in its ground state, with {{dn}} d electron(s)?", pace="quick",
    cases=[{"fn": c["fn"], "dn": c["dn"], "o1": f'{c["nm"]} ({c["sy"]})', **{f"o{k + 2}": f'{o["nm"]} ({o["sy"]})' for k, o in enumerate(
        rng.sample([o for o in f_cases if (o["fn"], o["dn"]) != (c["fn"], c["dn"]) and o["sy"] not in ("Lu", "Lr") and (o["sy"] in SYM[56:71]) == (c["sy"] in SYM[56:71])], 3))}, "s1": c["sy"]}
        for c in f_cases if c["sy"] not in ("Lu", "Lr")],
    choice=MC, correct="0", verify="0 if pt_config(s1)[0] == fn and pt_config(s1)[1] == dn else 9",
    explain="Most lanthanoids are [Xe]4fⁿ6s² with n = Z − 56; La, Ce, Gd keep a 5d electron, and the early actinoids prefer 6d")))

frows = []
for c in f_cases:
    if c["sy"] in ("Lu", "Lr"):
        continue
    fl = "4f" if c["sy"] in SYM[56:71] else "5f"
    dl = "5d" if fl == "4f" else "6d"
    sl = "6s" if fl == "4f" else "7s"
    right = cfg(c["core"], dl, c["dn"], sl, 2, fl, c["fn"])
    alts = []
    if c["dn"]:
        alts.append(cfg(c["core"], dl, 0, sl, 2, fl, c["fn"] + 1))
    else:
        alts.append(cfg(c["core"], dl, 1, sl, 2, fl, c["fn"] - 1) if c["fn"] else cfg(c["core"], dl, 2, sl, 1))
    alts.append(cfg(c["core"], dl, c["dn"], sl, 2, fl, c["fn"] + 2))
    alts.append(cfg(c["core"], dl, c["dn"], sl, 1, fl, c["fn"] + 1))
    alts = [a for a in dict.fromkeys(alts) if a != right]
    if len(alts) == 3:
        frows.append({"nm": c["nm"], "sy": c["sy"], "o1": right, "o2": alts[0], "o3": alts[1], "o4": alts[2]})
ADD.append(("PT-4.2.B", Q("pt-config-pick-f", "ptable.configurations", "Which is the ground-state configuration of {{nm}} ({{sy}})?", pace="quick",
    cases=frows, choice=MC, correct="0", verify="authored",
    explain="Count f electrons as Z − 56 (or Z − 88), then check the exceptions that keep a d electron: La, Ce, Gd; Ac, Th, Pa, U, Np, Cm")))
