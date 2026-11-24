"""NGSS high-school framework (NG): one objective per performance expectation. PEs taught in the subject
frameworks point at a mix of their drills (chosen by citation level, then by word overlap with the PE
title); the fifteen PEs nothing taught get their own templates here."""
import glob, re
import yaml
from opl_dsl import Q, L, U

FW, FILE, IDEA = "NG", "ng-ngss", "PE"

ST = [s for s in yaml.safe_load(open("drills/standards.yaml")) if s["id"] == "ngss-hs"][0]
TITLES = {i["code"]: i["title"] for i in ST["items"]}
STOP = set("the a of and to for in on from with by that an as its or be is are use using into".split())


def words(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


CANDS = {}
DRILL_OF = {}
for f in sorted(glob.glob("drills/frameworks/*.yaml")):
    fw = yaml.safe_load(open(f))
    if fw["id"] == "ngss":
        continue
    for u in fw.get("units", []):
        us = [x for x in (u.get("std") or []) if str(x).startswith("ngss-hs:")]
        for t in u.get("topics", []):
            ts = [x for x in (t.get("std") or []) if str(x).startswith("ngss-hs:")]
            for lo in t.get("los", []):
                ls = lo.get("std") or []
                ls = [ls] if isinstance(ls, str) else ls
                ls = [x for x in ls if str(x).startswith("ngss-hs:")]
                dr = [d for d in lo.get("drills", []) if not d.startswith("~")]
                if not dr:
                    continue
                code = f"{fw['code']}-{u['n']}.{t['n']}.{lo['id']}"
                DRILL_OF[code] = dr[0]
                for lvl, lst in ((3, ls), (2, ts), (1, us)):
                    for c in lst:
                        CANDS.setdefault(c.split(":")[1], []).append((lvl, code, lo["do"], dr))


# where the word match picks badly, name the objectives by hand
OVERRIDE = {
    "PS2-1": ["PH-2.5.A", "PH-2.5.B", "PH-2.7.A", "PH-1.3.B"],
    "PS3-2": ["PH-3.3.A", "PH-9.1.B", "PH-9.4.A", "PH-10.4.A"],
    "LS2-1": ["BI-8.4.A", "BI-8.3.A", "BI-8.2.B"],
    "LS2-2": ["BI-8.5.A", "BI-8.3.A", "BI-8.4.A", "BI-8.2.B"],
    "LS2-6": ["BI-8.6.A", "BI-8.6.B", "BI-8.5.D", "BI-8.5.C"],
    "LS2-8": ["BI-8.1.B", "BI-8.1.A"],
    "LS3-3": ["BI-5.3.B", "BI-5.3.D", "BI-5.3.E", "BI-5.4.B"],
    "LS4-3": ["BI-7.5.A", "BI-7.1.B", "BI-7.5.C", "BI-7.2.A"],
    "ESS1-2": ["ES-1.3.A", "ES-1.3.B", "ES-1.2.A"],
    "ESS2-3": ["ES-2.1.B", "ES-2.1.A"],
}
def pick(pe, n=4):
    if pe in OVERRIDE:
        los = [c for c in OVERRIDE[pe] if c in DRILL_OF]
        return los, list(dict.fromkeys(DRILL_OF[c] for c in los))
    tw = words(TITLES[pe])
    cs = sorted(CANDS.get(pe, []), key=lambda c: (-c[0], -len(tw & words(c[2])), c[1]))
    los, drills = [], []
    for _, code, _, dr in cs:
        if code in los:
            continue
        los.append(code)
        if dr[0] not in drills:
            drills.append(dr[0])
        if len(los) == n:
            break
    return los, drills


NEW = {
    "PS2-3": Q("ng-collision-force", "ngss.physical-design", "A {{m}} kg crash-test dummy moving at {{v}} m/s is brought to rest. With no airbag it stops in {{t1}} s; an airbag stretches the stop to {{t2}} s. By what factor does the airbag reduce the average force?",
               given={"m": {"pick": [50, 70, 80]}, "v": {"pick": [10, 15, 20]}, "t1": {"pick": [0.005, 0.01, 0.02]}, "t2": {"pick": [0.1, 0.15, 0.2]}}, value="t2/t1", tex="F_1/F_2", tol=0.005,
               verify="(m*v/nsimplify(t1))/(m*v/nsimplify(t2))", explain="The momentum change is fixed by the crash; $\\bar F = \\Delta p/\\Delta t$, so lengthening the stop is the whole design idea behind airbags, crumple zones and helmets"),
    "PS2-6": Q("ng-designed-materials", "ngss.physical-design", "{{q}}", pace="recall",
               cases=[{"q": "Why is a cross-linked polymer (like vulcanised rubber) more rigid and heat-resistant than the same polymer without cross-links?", "ans": 0},
                      {"q": "Why do metals conduct electricity and bend without shattering?", "ans": 1},
                      {"q": "Why does a soap or detergent lift grease into water?", "ans": 2},
                      {"q": "Why is diamond harder than graphite, though both are pure carbon?", "ans": 3}],
               choice=["Covalent bonds tie the chains together so they cannot slide past each other", "Delocalised electrons move freely and the metal ions can slide while staying bonded",
                       "Each molecule has a nonpolar tail that dissolves in grease and a polar head that dissolves in water", "Every atom is held by four covalent bonds in three dimensions, not in weakly stacked sheets"],
               correct="ans", verify="authored", explain="A designed material's job follows from its structure at the molecular scale: what holds the particles together and how they can move"),
    "PS3-3": Q("ng-device-efficiency", "ngss.physical-design", "A student's small hydro generator is fed {{Q}} L/s of water falling {{h}} m and lights LEDs drawing {{P}} W. What is the device's efficiency? ($g = 9.81$, 1 L of water = 1 kg)",
               given={"Q": {"pick": [0.5, 1, 2]}, "h": {"pick": [1, 2, 3]}, "P": {"pick": [2, 3, 5]}}, value="P/(Q*9.81*h)", tex="\\eta", tol=0.005,
               verify="nsimplify(P)/(nsimplify(Q)*Rational(981, 100)*h)", explain="Useful output over the energy supplied per second ($\\dot m gh$). Designing a converter is choosing where the rest goes (friction, heat, sound) and how to cut it"),
    "PS4-2": Q("ng-digital-storage", "ngss.physical-design", "Audio is sampled {{f}} thousand times a second with {{b}}-bit samples in stereo (2 channels). How many megabytes does {{t}} minutes take, uncompressed (1 MB = 10⁶ bytes)?",
               given={"f": {"pick": [44.1, 48, 96]}, "b": {"pick": [16, 24]}, "t": {"pick": [1, 3, 5]}}, value="f*1000*b*2*t*60/8/1000000", tex="MB", tol=0.005,
               verify="nsimplify(f)*1000*b*2*t*60/8/10**6", explain="Bits = samples per second × bits per sample × channels × seconds. Digital signals can be copied and sent without adding noise, at the cost of these large numbers (hence compression)"),
    "PS4-5": Q("ng-wave-device", "ngss.physical-design", "A {{d}} uses electromagnetic waves at {{f}} GHz. What is the wavelength, in cm? ($c = 3.00\\times10^8$ m/s)",
               cases=[{"d": "Wi-Fi router", "f": 2.4}, {"d": "Wi-Fi router", "f": 5}, {"d": "microwave oven", "f": 2.45}, {"d": "GPS receiver", "f": 1.575}, {"d": "5G phone", "f": 28}],
               value="3e8/(f*1e9)*100", tex="\\lambda", tol=0.005, verify="3*10**8/(nsimplify(f)*10**9)*100",
               explain="$\\lambda = c/f$. Antennas are usually a quarter or half wavelength long, which is why higher-frequency devices can be smaller"),
    "LS2-7": Q("ng-species-area", "ngss.life-impact", "The species–area relation is $S = cA^{z}$ with $z = {{z}}$. If a habitat shrinks to {{f}} of its area, what fraction of its species is expected to be lost eventually?",
               given={"z": {"pick": [0.15, 0.25, 0.3]}, "f": {"pick": [0.1, 0.25, 0.5]}}, value="1 - f^z", tex="\\Delta S/S", tol=0.005,
               verify="1 - (Symbol('c')*nsimplify(f)**nsimplify(z))/Symbol('c')", explain="Species fall more slowly than area ($z < 1$), but losing 90% of a habitat still costs about a third to a half of its species: the basis for protecting large, connected areas"),
    "LS4-6": Q("ng-harvest-simulation", "ngss.life-impact", "A fish stock of {{N}} thousand grows {{r}}% a year before harvest, and {{H}} thousand are caught each year. Simulate two years: what is the stock after year 2, in thousands?",
               given={"N": {"pick": [100, 200]}, "r": {"pick": [10, 20, 30]}, "H": {"pick": [10, 20, 40]}}, value="(N*(1 + r/100) - H)*(1 + r/100) - H", tex="N_2", tol=0.005,
               verify="(N*(1 + Rational(r, 100)) - H)*(1 + Rational(r, 100)) - H", explain="Step the model a year at a time. Comparing catch limits this way is how a management rule is tested before it is used on a real population"),
    "ESS2-5": Q("ng-ice-expansion", "ngss.earth-resources", "{{V}} cm³ of water seeps into a rock crack and freezes. Ice is less dense than water (917 vs 1000 kg/m³). What volume does the ice take up, in cm³?",
               given={"V": {"pick": [10, 50, 100, 250]}}, value="V*1000/917", tex="V_{ice}", tol=0.005, verify="solve(Eq(x*917, V*1000), x)[0]",
               explain="Same mass, lower density: about 9% more volume. Repeated freezing wedges rock apart, one of the ways water's unusual properties shape the surface"),
    "ESS2-7": Q("ng-coevolution", "ngss.earth-resources", "{{q}}", pace="recall",
                cases=[{"q": "What first put large amounts of oxygen into Earth's atmosphere (the Great Oxidation Event, about 2.4 billion years ago)?", "ans": 0},
                       {"q": "How did land plants change Earth's surface after they spread, about 400 million years ago?", "ans": 1},
                       {"q": "What did the oxygen-rich atmosphere make possible high above the surface?", "ans": 2},
                       {"q": "Where did most of the limestone in the crust come from?", "ans": 3}],
                choice=["Photosynthesis by cyanobacteria", "Roots broke rock into soil and slowed erosion", "An ozone layer that blocks ultraviolet light", "Shells and skeletons of marine organisms"],
                correct="ans", verify="authored", explain="Life and the Earth system change each other: organisms alter the air, rocks and water, and those changes open or close niches for later life"),
    "ESS3-2": Q("ng-energy-return", "ngss.earth-resources", "A {{P}} MW solar farm runs at a {{cf}}% capacity factor for {{y}} years and costs {{C}} million dollars in total. What is its cost per kWh of energy delivered, in cents?",
                given={"P": {"pick": [50, 100]}, "cf": {"pick": [20, 25, 30]}, "y": {"pick": [20, 25, 30]}, "C": {"pick": [80, 120, 150]}}, value="C*1e6/(P*1000*cf/100*8760*y)*100", tex="LCOE", tol=0.005,
                verify="C*10**6*100/integrate(P*1000*Rational(cf, 100), (x, 0, 8760*y))", explain="Divide the lifetime cost by the lifetime energy. Comparing resources this way (and adding environmental and social costs) is the cost–benefit analysis the standard asks for"),
    "ESS3-4": Q("ng-scrubber", "ngss.earth-resources", "A power plant emits {{E}} tonnes of SO₂ a year. A scrubber that removes {{eta}}% is installed. How many tonnes a year does it still emit?",
                given={"E": {"pick": [1000, 5000, 20000]}, "eta": {"pick": [80, 90, 95, 98]}}, value="E*(1 - eta/100)", tex="E'", tol=0.005, verify="solve(Eq(E - x, E*Rational(eta, 100)), x)[0]",
                explain="What remains is the fraction not captured. Going from 90% to 99% halves nothing but cuts the remainder tenfold, which is why the last few percent are worth arguing over"),
    "ETS1-1": Q("ng-criteria-constraints", "ngss.engineering", "Designing a water filter for a village: is \"{{s}}\" a criterion or a constraint?", pace="recall",
                cases=[{"s": "it must cost less than 20 dollars per household", "ans": 1}, {"s": "the more bacteria it removes the better", "ans": 0}, {"s": "it must work with no electricity", "ans": 1},
                       {"s": "a higher flow rate is preferred", "ans": 0}, {"s": "it must use locally available materials", "ans": 1}, {"s": "it should be as easy to clean as possible", "ans": 0}],
                choice=["Criterion (a measure of how good a solution is)", "Constraint (a limit every solution must meet)"], correct="ans", verify="authored",
                explain="Constraints rule solutions in or out; criteria rank the solutions that are left. Writing both down before designing is the first step of engineering design"),
    "ETS1-2": Q("ng-subsystem-reliability", "ngss.engineering", "A device is broken into {{n}} subsystems in series, each working {{r}}% of the time, independently. What fraction of the time does the whole device work?",
                given={"n": {"int": [2, 6]}, "r": {"pick": [90, 95, 99]}}, value="(r/100)^n", tex="R", tol=0.005, verify="Rational(r, 100)**n",
                explain="Breaking a problem into parts lets each be designed and tested, but the parts multiply: many good parts in series make a mediocre whole. Redundancy (parts in parallel) is the fix"),
    "ETS1-3": Q("ng-decision-matrix", "ngss.engineering", "Two designs are scored 1–10 on cost (weight {{w1}}), safety (weight {{w2}}) and durability (weight {{w3}}). Design A scores {{a1}}, {{a2}}, {{a3}}. What is its weighted score?",
                given={"w1": {"pick": [0.2, 0.3]}, "w2": {"pick": [0.5, 0.4]}, "w3": {"pick": [0.3]}, "a1": {"int": [3, 9]}, "a2": {"int": [3, 9]}, "a3": {"int": [3, 9]}},
                value="w1*a1 + w2*a2 + w3*a3", tex="S_A", tol=0.005, verify="Matrix([nsimplify(w1), nsimplify(w2), nsimplify(w3)]).dot(Matrix([a1, a2, a3]))",
                explain="A decision matrix makes the trade-offs explicit: change the weights and see whether the winner changes. The weights are a value judgement, not a measurement"),
    "ETS1-4": Q("ng-impact-simulation", "ngss.engineering", "A city's emissions are {{E}} kt/yr. A programme cuts them {{p}}% each year from the previous year's level. Simulate: what are they after {{n}} years, in kt/yr?",
                given={"E": {"pick": [500, 1000, 2000]}, "p": {"pick": [3, 5, 8, 10]}, "n": {"pick": [5, 10, 20]}}, value="E*(1 - p/100)^n", tex="E_n", tol=0.005,
                verify="E*Rational(100 - p, 100)**n", explain="A computational model steps the rule forward year by year; a steady percentage cut is a geometric decay, never quite reaching zero"),
}

DCI = [("PS1", "Matter and its interactions"), ("PS2", "Motion and stability: forces and interactions"), ("PS3", "Energy"),
       ("PS4", "Waves and their applications in technologies for information transfer"), ("LS1", "From molecules to organisms: structures and processes"),
       ("LS2", "Ecosystems: interactions, energy and dynamics"), ("LS3", "Heredity: inheritance and variation of traits"),
       ("LS4", "Biological evolution: unity and diversity"), ("ESS1", "Earth's place in the universe"), ("ESS2", "Earth's systems"),
       ("ESS3", "Earth and human activity"), ("ETS1", "Engineering design")]

UNITS = []
for n, (dci, title) in enumerate(DCI, 1):
    los = []
    for pe in [c for c in TITLES if c.startswith(dci + "-")]:
        letter = chr(64 + int(pe.split("-")[1]))
        needs, drills = pick(pe)
        qs = [NEW[pe]] if pe in NEW else []
        ek = "Practised through: " + ", ".join(needs) + "." if needs else "Practised here; no subject framework reaches it yet."
        los.append(L(letter, f"{pe}: {TITLES[pe]}.", ek, [], qs, p="P2" if dci == "ETS1" or pe in NEW else "P1", std=[f"ngss-hs:{pe}"], drills=drills, needs=needs))
    UNITS.append(U(n, dci.lower(), f"{dci} · {title}", [(title[:1].upper() + title[1:], los)], std=[f"ngss-hs:{c}" for c in TITLES if c.startswith(dci + "-")][:3]))
missing = [pe for pe in TITLES if not pick(pe)[1] and pe not in NEW]
assert not missing, f"PEs with no drill: {missing}"
