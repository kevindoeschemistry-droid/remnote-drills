"""Builds drills/problems/in-inorganic.yaml (framework inorganic-chemistry, IN). Run: python3 scripts/in_cases.py

Answers come from look-up tables typed here (oxidation states, d counts, spin tables, isomer counts,
unit-cell constants, colours and tests) and closed forms (spin-only formula, Bragg). tests/verify/incalc.py
reaches each one another way: charge balance from rules, orbital filling, enumeration over the rotation
group, atom positions, and a second typed table for facts.
"""
import math
import random
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent / "drills/problems/in-inorganic.yaml"
T = []
rnd = random.Random(7)


def val(name, skill, prompt, ask, explain, cases, verify, tol=0.0001, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(name, skill, prompt, options, explain, cases, verify, pace="recall"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}],
              "verify": {"choices": {"y": verify}}})


def shuffled(right, wrong, extra):
    """four options (right + three wrong), shuffled; returns case fields o1..o4 and ans"""
    opts = [right] + wrong[:3]
    rnd.shuffle(opts)
    return {**extra, **{f"o{i + 1}": o for i, o in enumerate(opts)}, "ans": opts.index(right)}


def fact_cases(table, data, prompt_key="k"):
    cases = []
    values = sorted(set(data.values()))
    for k, v in data.items():
        wrong = [w for w in values if w != v]
        rnd.shuffle(wrong)
        cases.append(shuffled(v, wrong, {prompt_key: k, "tb": table}))
    return cases


O4 = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]

# ── 1. s block ───────────────────────────────────────────────────────────────
FLAME = {"Li": "crimson", "Na": "yellow-orange", "K": "lilac", "Ca": "orange-red", "Sr": "crimson", "Ba": "apple green", "Cu": "blue-green", "Cs": "blue-violet"}
cases = []
for k, v in FLAME.items():
    wrong = [w for w in sorted(set(FLAME.values())) if w != v]
    rnd.shuffle(wrong)
    cases.append(shuffled(v, wrong, {"k": k}))
pick("in-flame-colour", "inorg.s-block", "What colour does {{k}} give in a flame test?", O4,
     "Heat promotes an electron; it falls back with a photon whose energy is fixed by the element. Li and Sr are both red (Li crimson, Sr crimson-red; tell them apart with a spectroscope), Na's yellow swamps the rest, so view K's lilac through blue cobalt glass",
     cases, 'fact_pick("flame", k, o1, o2, o3, o4)')

BURN = {"Li": "Li2O", "Na": "Na2O2", "K": "KO2", "Rb": "RbO2", "Mg": "MgO", "Ca": "CaO"}
cases = []
for k, v in BURN.items():
    opts = {"Li": ["Li2O2", "LiO2", "Li3N"], "Na": ["Na2O", "NaO2", "NaOH"], "K": ["K2O", "K2O2", "KOH"], "Rb": ["Rb2O", "Rb2O2", "RbOH"],
            "Mg": ["MgO2", "Mg(OH)2", "Mg2O"], "Ca": ["CaO2", "Ca(OH)2", "Ca2O"]}[k]
    cases.append(shuffled(v, opts, {"k": k}))
pick("in-s-block-oxygen", "inorg.s-block", "What is the main product when {{k}} burns in excess oxygen?", O4,
     "Down group 1 the cation grows, and a big cation stabilises a big anion: Li gives the oxide O²⁻, Na the peroxide O₂²⁻, K, Rb and Cs the superoxide O₂⁻. Group 2 metals give the oxide MO",
     cases, 'fact_pick("burn", k, o1, o2, o3, o4)')

# ── 2. p block and oxidation states ──────────────────────────────────────────
OX = [("Cr2O7", -2, "Cr", 6, "Cr₂O₇²⁻"), ("MnO4", -1, "Mn", 7, "MnO₄⁻"), ("S2O3", -2, "S", 2, "S₂O₃²⁻ (average)"), ("S4O6", -2, "S", 2.5, "S₄O₆²⁻ (average)"),
      ("NH4", 1, "N", -3, "NH₄⁺"), ("N2O5", 0, "N", 5, "N₂O₅"), ("ClO4", -1, "Cl", 7, "ClO₄⁻"), ("H2PO2", -1, "P", 1, "H₂PO₂⁻"),
      ("Fe3O4", 0, "Fe", 8 / 3, "Fe₃O₄ (average)"), ("XeOF4", 0, "Xe", 6, "XeOF₄"), ("IO3", -1, "I", 5, "IO₃⁻"), ("H2O2", 0, "O", -1, "H₂O₂"),
      ("OF2", 0, "O", 2, "OF₂"), ("POCl3", 0, "P", 5, "POCl₃"), ("NaH", 0, "H", -1, "NaH"), ("KO2", 0, "O", -0.5, "KO₂ (average)"),
      ("HN3", 0, "N", -1 / 3, "HN₃ (average)"), ("CaC2", 0, "C", -1, "CaC₂")]
cases = [{"fm": fm, "q": q, "el": el, "show": show, "ans": float(a)} for fm, q, el, a, show in OX]
val("in-ox-state", "inorg.p-block", "What is the oxidation state of {{el}} in {{show}}?", "Oxidation state",
    "Fix the elements with firm rules (F −1, group 1 +1, group 2 +2, H +1 with non-metals, O −2 unless bonded to F or in a peroxide or superoxide), then the charge balance gives the rest. A fractional answer is an average over non-equivalent atoms",
    cases, "ox_state(fm, q, el)", pace="recall")

OXO = [("HClO", "hypochlorous acid", ["chlorous acid", "chloric acid", "perchloric acid"]), ("HClO2", "chlorous acid", ["hypochlorous acid", "chloric acid", "perchloric acid"]),
       ("HClO3", "chloric acid", ["chlorous acid", "perchloric acid", "hypochlorous acid"]), ("HClO4", "perchloric acid", ["chloric acid", "chlorous acid", "hydrochloric acid"]),
       ("H2SO3", "sulfurous acid", ["sulfuric acid", "hyposulfurous acid", "persulfuric acid"]), ("HNO2", "nitrous acid", ["nitric acid", "hyponitrous acid", "pernitric acid"]),
       ("HBrO3", "bromic acid", ["bromous acid", "perbromic acid", "hypobromous acid"]), ("HIO4", "periodic acid", ["iodic acid", "iodous acid", "hypoiodous acid"])]
cases = []
for fm, right, wrong in OXO:
    cases.append(shuffled(right, wrong, {"fm": fm, "hal": {"Cl": 1, "S": 0, "N": 0, "Br": 1, "I": 1}[[e for e in ("Cl", "S", "N", "Br", "I") if e in fm][0]]}))
pick("in-oxoacid-name", "inorg.p-block", "Name {{fm}}.", O4,
     "Within a family the suffix tracks the oxidation state: hypo-…-ous (lowest), -ous, -ic, per-…-ic (highest). For the halogens +1, +3, +5, +7; for S and N the -ic acid is the common one (H₂SO₄, HNO₃) and the -ous acid has one O fewer",
     cases, None)
T[-1]["verify"] = {"authored": True}

OXIDE = {"Na2O": "basic", "MgO": "basic", "CaO": "basic", "Al2O3": "amphoteric", "ZnO": "amphoteric", "BeO": "amphoteric", "SiO2": "acidic",
         "P4O10": "acidic", "SO3": "acidic", "Cl2O7": "acidic", "CO2": "acidic", "CO": "neutral", "NO": "neutral", "N2O": "neutral", "CrO3": "acidic"}
LIT = ["acidic", "basic", "amphoteric", "neutral"]
cases = [{"k": k, "lit": "|".join(LIT), "ans": LIT.index(v)} for k, v in OXIDE.items()]
pick("in-oxide-character", "inorg.p-block", "How does {{k}} behave toward acids and bases?", LIT,
     "Across a period oxides go from basic (ionic, metal) through amphoteric (Al, also Be and Zn) to acidic (covalent, non-metal). A metal in a high oxidation state gives an acidic oxide (CrO₃, Mn₂O₇). CO, NO and N₂O are neutral: they form no acid with water",
     cases, 'fact_lit("oxide", k, lit)')

DIS = [("Cl2", 0, "Cl", -1, "ClO3", -1, "Cl", "Cl₂ in hot NaOH gives Cl⁻ and ClO₃⁻", 5), ("Cl2", 0, "Cl", -1, "ClO", -1, "Cl", "Cl₂ in cold NaOH gives Cl⁻ and ClO⁻", 1),
       ("Br2", 0, "Br", -1, "BrO3", -1, "Br", "Br₂ in hot NaOH gives Br⁻ and BrO₃⁻", 5), ("P4", 0, "PH3", 0, "H2PO2", -1, "P", "P₄ in hot NaOH gives PH₃ and H₂PO₂⁻", 1 / 3),
       ("NO2", 0, "NO2", -1, "NO3", -1, "N", "NO₂ in water gives NO₂⁻ (as HNO₂) and NO₃⁻", 1), ("H2O2", 0, "H2O", 0, "O2", 0, "O", "H₂O₂ decomposes to H₂O and O₂", 1),
       ("MnO4", -2, "MnO2", 0, "MnO4", -1, "Mn", "MnO₄²⁻ in acid gives MnO₂ and MnO₄⁻", 0.5)]
cases = [{"f0": a, "q0": b, "fr": c, "qr": d, "fo": e, "qo": f, "el": g, "text": t, "ans": float(n)} for a, b, c, d, e, f, g, t, n in DIS]
val("in-disproportionation", "inorg.p-block", "{{text}}. How many {{el}} atoms are reduced for each one oxidised?", "Ratio",
    "Electrons lost must equal electrons gained. Find each product's oxidation state; atoms reduced per atom oxidised = (rise in the oxidised product) ÷ (fall in the reduced one). Cl₂ → Cl⁻ + ClO₃⁻: up 5, down 1, so 5 Cl⁻ per ClO₃⁻",
    cases, "disprop_ratio(f0, q0, fr, qr, fo, qo, el)")

# ── 3. d block and coordination ──────────────────────────────────────────────
GROUP = {"Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zn": 12, "Pt": 10, "Rh": 9, "Ru": 8, "Mo": 6}
CPX = [("[Fe(CN)6]4-", "Fe", "CN:6", -4, 6), ("[Fe(CN)6]3-", "Fe", "CN:6", -3, 5), ("[Co(NH3)6]3+", "Co", "NH3:6", 3, 6), ("[CoCl4]2-", "Co", "Cl:4", -2, 7),
       ("[Ni(CO)4]", "Ni", "CO:4", 0, 10), ("[Cr(H2O)6]3+", "Cr", "H2O:6", 3, 3), ("[Cu(NH3)4(H2O)2]2+", "Cu", "NH3:4,H2O:2", 2, 9),
       ("[PtCl2(NH3)2]", "Pt", "Cl:2,NH3:2", 0, 8), ("[Mn(H2O)6]2+", "Mn", "H2O:6", 2, 5), ("[Ti(H2O)6]3+", "Ti", "H2O:6", 3, 1),
       ("[Fe(ox)3]3-", "Fe", "ox:3", -3, 5), ("[Co(en)2Cl2]+", "Co", "en:2,Cl:2", 1, 6), ("[Mo(CO)6]", "Mo", "CO:6", 0, 6), ("[RhCl(PPh3)3]", "Rh", "Cl:1,PPh3:3", 0, 8)]
cases = [{"cx": cx, "M": M, "ligs": ligs, "q": q, "ans": d} for cx, M, ligs, q, d in CPX]
val("in-d-count", "inorg.coordination", "How many d electrons does the metal have in {{cx}}?", "d electrons",
    "Oxidation state from the charges (ligand charges: CN⁻, Cl⁻ and ox²⁻ count; H₂O, NH₃, en, CO and PPh₃ are neutral), then dⁿ = group number − oxidation state. Fe(II) is d⁶, Co(III) d⁶, Cu(II) d⁹, Ni(0) d¹⁰",
    cases, "d_count(M, ligs, q)", pace="recall")

HS = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
LS = [0, 1, 2, 3, 2, 1, 0, 1, 2, 1, 0]
SPIN = [("[Fe(H2O)6]2+", 6, "oct", "high"), ("[Fe(CN)6]4-", 6, "oct", "low"), ("[Fe(CN)6]3-", 5, "oct", "low"), ("[Mn(H2O)6]2+", 5, "oct", "high"),
        ("[CoF6]3-", 6, "oct", "high"), ("[Co(NH3)6]3+", 6, "oct", "low"), ("[Cr(H2O)6]3+", 3, "oct", "high"), ("[CoCl4]2-", 7, "tet", "high"),
        ("[Ni(H2O)6]2+", 8, "oct", "high"), ("[Cu(H2O)6]2+", 9, "oct", "high"), ("[Mn(CN)6]3-", 4, "oct", "low"), ("[Cr(H2O)6]2+", 4, "oct", "high")]
cases = []
for cx, d, g, s in SPIN:
    n = HS[d] if s == "high" or g == "tet" else LS[d]
    cases.append({"cx": cx, "d": d, "geom": g, "spin": s, "gw": {"oct": "octahedral", "tet": "tetrahedral"}[g], "ans": round(math.sqrt(n * (n + 2)), 12)})
val("in-spin-only", "inorg.coordination", "{{cx}} is a {{spin}}-spin {{gw}} d{{d}} complex. What is its spin-only magnetic moment (μ_B)?", "μ (μ_B)",
    "Count unpaired electrons: octahedral sets are t₂g (3) below e_g (2); high spin puts one electron in each of the five before pairing, low spin fills t₂g first. Then $\\mu = \\sqrt{n(n+2)}$: 1.73, 2.83, 3.87, 4.90, 5.92 for n = 1–5",
    cases, "spin_only(d, geom, spin)", tol=0.001)

CF_HS = [0, -0.4, -0.8, -1.2, -0.6, 0, -0.4, -0.8, -1.2, -0.6, 0]
CF_LS = [0, -0.4, -0.8, -1.2, -1.6, -2.0, -2.4, -1.8, -1.2, -0.6, 0]
cases = []
for d, s in [(4, "high"), (4, "low"), (5, "low"), (6, "low"), (6, "high"), (7, "low"), (3, "high"), (8, "high"), (9, "high"), (5, "high")]:
    cases.append({"d": d, "spin": s, "geom": "oct", "ans": (CF_HS if s == "high" else CF_LS)[d]})
val("in-cfse", "inorg.coordination", "What is the crystal-field stabilisation energy of a {{spin}}-spin octahedral d{{d}} ion, in units of Δ_o (ignore pairing energy)?", "CFSE (Δ_o)",
    "Each t₂g electron is −0.4Δ_o and each e_g electron +0.6Δ_o. Low-spin d⁶ (t₂g⁶) is the maximum, −2.4Δ_o, which is why Co(III) and Fe(II) with strong-field ligands are so inert",
    cases, "cfse(d, geom, spin)", pace="recall")

ISO = [("MA₄B₂ (octahedral)", "A4B2", 0, "oct", 2), ("MA₃B₃ (octahedral)", "A3B3", 0, "oct", 2), ("MA₂B₂C₂ (octahedral)", "A2B2C2", 0, "oct", 6),
       ("M(AA)₃ (octahedral, AA a symmetric chelate)", "", 3, "oct", 2), ("M(AA)₂B₂ (octahedral)", "B2", 2, "oct", 3), ("MA₂B₂ (square planar)", "A2B2", 0, "sq", 2),
       ("MABCD (square planar)", "ABCD", 0, "sq", 3), ("MA₅B (octahedral)", "A5B", 0, "oct", 1), ("M(AA)B₄ (octahedral)", "B4", 1, "oct", 1),
       ("M(AA)₂BC (octahedral)", "BC", 2, "oct", 3)]
cases = [{"cx": cx, "mono": m, "nch": c, "geom": g, "ans": n} for cx, m, c, g, n in ISO]
val("in-isomer-count", "inorg.coordination", "How many stereoisomers does {{cx}} have, counting each enantiomer separately?", "Stereoisomers",
    "List geometric isomers by which ligands are trans, then check each for a mirror plane. MA₄B₂ and MA₃B₃: 2 (cis/trans, fac/mer). MA₂B₂C₂: 5 geometric, one of them chiral, so 6. M(AA)₃: Δ and Λ. A planar complex is never chiral",
    cases, "stereoisomers(mono, nch, geom)")

COL = {"[Cu(H2O)6]2+": "pale blue", "[Cu(NH3)4(H2O)2]2+": "deep blue", "[CuCl4]2-": "yellow-green", "[Co(H2O)6]2+": "pink", "[CoCl4]2-": "blue",
       "[Ni(H2O)6]2+": "green", "[Fe(H2O)6]2+": "pale green", "MnO4-": "purple", "Cr2O7 2-": "orange", "CrO4 2-": "yellow", "[Zn(H2O)6]2+": "colourless",
       "[Fe(SCN)(H2O)5]2+": "blood red"}
cases = []
for k, v in COL.items():
    wrong = [w for w in sorted(set(COL.values())) if w != v]
    rnd.shuffle(wrong)
    cases.append(shuffled(v, wrong, {"k": k}))
pick("in-ion-colour", "inorg.coordination", "What colour is {{k}} in water?", O4,
     "Colour is the complement of what is absorbed. d⁰ and d¹⁰ ions (Sc³⁺, Zn²⁺) have no d–d transition and are colourless; MnO₄⁻ and Cr₂O₇²⁻ are d⁰ but coloured by charge transfer. Swapping water for Cl⁻ or NH₃ shifts the colour (pink Co²⁺ to blue CoCl₄²⁻, pale blue Cu²⁺ to deep blue)",
     cases, 'fact_pick("colour", k, o1, o2, o3, o4)')

FIELD = ["I-", "Br-", "Cl-", "F-", "OH-", "H2O", "NH3", "en", "NO2-", "CN-", "CO"]
cases = []
for _ in range(8):
    four = rnd.sample(FIELD, 4)
    best = max(four, key=FIELD.index)
    cases.append({"o1": four[0], "o2": four[1], "o3": four[2], "o4": four[3], "ans": four.index(best)})
pick("in-spectrochemical", "inorg.coordination", "Which ligand gives the largest Δ_o with the same metal ion?", O4,
     "Spectrochemical series: I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O < NH₃ < en < NO₂⁻ < CN⁻ < CO. π-donors (halides) are weak, π-acceptors (CN⁻, CO) are strong",
     cases, "field_pick(o1, o2, o3, o4)")

# ── 4. redox, qualitative analysis ───────────────────────────────────────────
HALF = [("MnO4", -1, "Mn", 2, "Mn", 1, "MnO₄⁻ → Mn²⁺ (acid)", 5), ("Cr2O7", -2, "Cr", 3, "Cr", 1, "Cr₂O₇²⁻ → 2 Cr³⁺", 6),
        ("MnO4", -1, "MnO2", 0, "Mn", 1, "MnO₄⁻ → MnO₂ (base)", 3), ("C2O4", -2, "CO2", 0, "C", 1, "C₂O₄²⁻ → 2 CO₂", 2),
        ("NO3", -1, "NO", 0, "N", 1, "NO₃⁻ → NO", 3), ("IO3", -1, "I2", 0, "I", 2, "2 IO₃⁻ → I₂", 10),
        ("H2O2", 0, "O2", 0, "O", 1, "H₂O₂ → O₂", 2), ("S2O3", -2, "S4O6", -2, "S", 2, "2 S₂O₃²⁻ → S₄O₆²⁻", 2)]
cases = [{"f": a, "q": b, "fto": c, "qto": d, "el": e, "nf": f, "text": t, "ans": n} for a, b, c, d, e, f, t, n in HALF]
val("in-half-electrons", "inorg.redox", "How many electrons appear in the balanced half-equation {{text}}?", "Electrons",
    "Change in oxidation state × number of atoms that change. Balance O with H₂O and H with H⁺ (or OH⁻ in base) only after the electrons are set: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O",
    cases, "half_electrons(f, q, fto, qto, el, nf)", pace="recall")

IODO = [("Cu²⁺ (2Cu²⁺ + 4I⁻ → 2CuI + I₂)", "Cu", 2, "Cu", "Cu", 1, 1), ("IO₃⁻ (IO₃⁻ + 5I⁻ + 6H⁺ → 3I₂ + 3H₂O)", "IO3", -1, "I", "I", -1, 6),
        ("Cr₂O₇²⁻ (reduced to 2Cr³⁺)", "Cr2O7", -2, "Cr", "Cr", 3, 6), ("ClO⁻ (ClO⁻ + 2I⁻ + 2H⁺ → Cl⁻ + I₂ + H₂O)", "ClO", -1, "Cl", "Cl", -1, 2)]
cases = []
for what, f, q, el, fe, qe, eq in IODO:
    for vt, ct, va in [(18.40, 0.1000, 25.00), (22.75, 0.0500, 20.00), (12.30, 0.0800, 10.00)]:
        cases.append({"what": what, "f": f, "q": q, "el": el, "fe": fe, "qe": qe, "vt": vt, "ct": ct, "va": va, "ans": round(vt * ct / eq / va, 12)})
val("in-iodometry", "inorg.redox", "{{va}} mL of a solution of {{what}} is treated with excess KI; the I₂ formed takes {{vt}} mL of {{ct}} M thiosulfate (I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻). What is the oxidant's concentration (M)?", "Concentration (M)",
    "Iodide is only a go-between: count electrons from the oxidant to its final reduced form, one thiosulfate per electron. Cu²⁺ → CuI takes 1; Cr₂O₇²⁻ → 2Cr³⁺ takes 6; IO₃⁻ → I⁻ takes 6 (its own iodine ends as iodide too); ClO⁻ → Cl⁻ takes 2",
    cases, "nsimplify(vt)*nsimplify(ct)/to_reduced(f, q, el, fe, qe)/nsimplify(va)")

AMPH = ["Al", "Zn", "Pb", "Sn", "Cr", "Be"]
NOT = ["Fe", "Mg", "Cu", "Ni", "Mn", "Ca"]
cases = []
for a in AMPH:
    w = rnd.sample(NOT, 3)
    cases.append(shuffled(a, w, {}))
pick("in-amphoteric", "inorg.qualitative", "Each metal's hydroxide is precipitated with a little NaOH. Which one redissolves in excess NaOH?", O4,
     "Amphoteric hydroxides dissolve as hydroxo anions: Al(OH)₄⁻, Zn(OH)₄²⁻, Pb(OH)₄²⁻, Sn(OH)₄²⁻, Cr(OH)₆³⁻, Be(OH)₄²⁻. Fe, Mg, Cu, Ni and Mn hydroxides stay put (Cu, Ni and Zn dissolve in excess NH₃ instead, as ammine complexes)",
     cases, "amph_pick(o1, o2, o3, o4)")

PPT = {"AgCl": "white", "AgBr": "cream", "AgI": "yellow", "PbI2": "bright yellow", "BaSO4": "white", "Cu(OH)2": "pale blue", "Fe(OH)3": "red-brown",
       "Fe(OH)2": "dirty green", "Ni(OH)2": "green", "PbS": "black", "ZnS": "white", "Ag2CrO4": "brick red", "CdS": "yellow"}
cases = []
for k, v in PPT.items():
    wrong = [w for w in sorted(set(PPT.values())) if w != v and not (v in ("yellow", "bright yellow") and w in ("yellow", "bright yellow"))]
    rnd.shuffle(wrong)
    cases.append(shuffled(v, wrong, {"k": k}))
pick("in-precipitate-colour", "inorg.qualitative", "What colour is the precipitate {{k}}?", O4,
     "Silver halides darken down the group (white, cream, yellow) and their solubility in NH₃ falls with them. Hydroxides take the ion's colour: Cu blue, Fe(II) green turning brown in air, Fe(III) red-brown. Most metal sulfides are black; ZnS is white and CdS yellow",
     cases, 'fact_pick("ppt", k, o1, o2, o3, o4)')

TEST = {"NH4+": "warm with NaOH: gas turns damp red litmus blue", "SO4 2-": "acidified BaCl2: white precipitate", "Cl-": "acidified AgNO3: white precipitate, dissolves in dilute NH3",
        "CO3 2-": "dilute acid: gas turns limewater milky", "Fe3+": "KSCN: blood-red solution", "Fe2+": "K3[Fe(CN)6]: dark blue precipitate",
        "I-": "acidified AgNO3: yellow precipitate, insoluble in conc. NH3", "NO3-": "Devarda's alloy and NaOH: ammonia given off"}
cases = []
for k, v in TEST.items():
    wrong = [w for w in TEST.values() if w != v]
    rnd.shuffle(wrong)
    cases.append(shuffled(v, wrong, {"k": k}))
pick("in-ion-test", "inorg.qualitative", "Which test identifies {{k}}?", O4,
     "Acidify before BaCl₂ or AgNO₃ so carbonate cannot precipitate too. Halides are told apart by the colour of the silver salt and whether NH₃ dissolves it. Nitrate is reduced to NH₃ by Devarda's alloy; ammonium itself gives NH₃ with warm NaOH",
     cases, 'fact_pick("test", k, o1, o2, o3, o4)')

# ── 5. solids ────────────────────────────────────────────────────────────────
ZC = {"sc": (1, "simple cubic"), "bcc": (2, "body-centred cubic"), "fcc": (4, "face-centred cubic"), "diamond": (8, "diamond")}
cases = [{"s": s_, "sw": w, "spc": "X", "who": "atoms", "ans": z} for s_, (z, w) in ZC.items()]
cases += [{"s": "NaCl", "sw": "rock-salt (NaCl)", "spc": "A", "who": "cations", "ans": 4}, {"s": "CsCl", "sw": "CsCl", "spc": "A", "who": "cations", "ans": 1},
          {"s": "ZnS", "sw": "zinc blende (ZnS)", "spc": "A", "who": "cations", "ans": 4}, {"s": "CaF2", "sw": "fluorite (CaF₂)", "spc": "B", "who": "anions", "ans": 8}]
val("in-cell-contents", "inorg.solids", "In the {{sw}} structure, how many {{who}} does one cubic unit cell contain?", "Per cell",
    "Corners count 1/8, edges 1/4, faces 1/2, the body 1. sc 1, bcc 2, fcc 4, diamond 8 atoms; NaCl and ZnS 4 formula units; CsCl 1; fluorite 4 Ca²⁺ and 8 F⁻",
    cases, "cell_count(s, spc)", pace="recall")

CN = [("sc", "X", "X", "simple cubic metal", 6), ("bcc", "X", "X", "bcc metal", 8), ("fcc", "X", "X", "fcc (ccp) metal", 12), ("diamond", "X", "X", "diamond", 4),
      ("NaCl", "A", "B", "rock salt, Na⁺ surrounded by Cl⁻", 6), ("CsCl", "A", "B", "CsCl, Cs⁺ surrounded by Cl⁻", 8), ("ZnS", "A", "B", "zinc blende, Zn²⁺ surrounded by S²⁻", 4),
      ("CaF2", "A", "B", "fluorite, Ca²⁺ surrounded by F⁻", 8), ("CaF2", "B", "A", "fluorite, F⁻ surrounded by Ca²⁺", 4)]
cases = [{"s": s, "c0": a, "c1": b, "sw": w, "ans": n} for s, a, b, w, n in CN]
val("in-coordination-number", "inorg.solids", "What is the coordination number in {{sw}}?", "Coordination number",
    "Count nearest neighbours: sc 6, bcc 8, fcc 12, diamond 4. In ionic structures the cation sits in a hole of the anion lattice: octahedral (NaCl, 6), cubic (CsCl, 8), tetrahedral (ZnS, 4); fluorite is 8:4",
    cases, "coordination(s, c0, c1)", pace="recall")

PF = {"sc": math.pi / 6, "bcc": math.pi * math.sqrt(3) / 8, "fcc": math.pi / (3 * math.sqrt(2)), "diamond": math.pi * math.sqrt(3) / 16}
cases = [{"s": s, "sw": ZC[s][1], "ans": round(v, 12)} for s, v in PF.items()]
val("in-packing", "inorg.solids", "What fraction of space is filled by touching spheres in a {{sw}} lattice?", "Packing fraction",
    "Find where spheres touch (sc along the edge, bcc the body diagonal, fcc the face diagonal), so r in terms of a, then Z·(4/3)πr³ / a³: 0.524, 0.680, 0.740, 0.340",
    cases, "packing(s)")

DEN = [("fcc", "Cu", 361.5, "copper (fcc)"), ("bcc", "Fe", 286.7, "α-iron (bcc)"), ("fcc", "Ag", 408.6, "silver (fcc)"), ("NaCl", "NaCl", 564.0, "NaCl (rock salt)"),
       ("bcc", "W", 316.5, "tungsten (bcc)"), ("CsCl", "CsCl", 412.3, "CsCl"), ("CaF2", "CaF2", 546.3, "CaF₂ (fluorite)")]
MASS = {"Cu": 63.546, "Fe": 55.845, "Ag": 107.868, "Na": 22.990, "Cl": 35.45, "W": 183.84, "Cs": 132.905, "Ca": 40.078, "F": 18.998}
Z = {"fcc": 4, "bcc": 2, "NaCl": 4, "CsCl": 1, "CaF2": 4}
FM = {"Cu": 63.546, "Fe": 55.845, "Ag": 107.868, "NaCl": 22.990 + 35.45, "W": 183.84, "CsCl": 132.905 + 35.45, "CaF2": 40.078 + 2 * 18.998}
cases = []
for s, f, a, w in DEN:
    rho = Z[s] * FM[f] / (6.02214076e23 * (a * 1e-10) ** 3)
    cases.append({"s": s, "f": f, "a": a, "sw": w, "ans": round(rho, 10)})
val("in-density", "inorg.solids", "{{sw}} has a cubic cell edge of {{a}} pm. What is its density (g/cm³)?", "ρ (g/cm³)",
    "ρ = Z·M / (N_A·a³), with a in cm (1 pm = 10⁻¹⁰ cm) and Z the formula units per cell (fcc 4, bcc 2, rock salt 4, CsCl 1, fluorite 4)",
    cases, "density(s, f, a)", tol=0.0002)

cases = []
for w, a, h, k, l, lam, th in [(0, 361.5, 1, 1, 1, 154.06, 0), (0, 361.5, 2, 0, 0, 154.06, 0), (0, 564.0, 2, 0, 0, 154.06, 0), (0, 404.9, 2, 2, 0, 154.06, 0),
                              (1, 0, 0, 0, 0, 154.06, 22.3), (1, 0, 0, 0, 0, 71.07, 15.0), (1, 0, 0, 0, 0, 154.06, 38.5)]:
    if w == 0:
        d = a / math.sqrt(h * h + k * k + l * l)
        ans = math.degrees(math.asin(lam / (2 * d)))
        cases.append({"w": w, "a": a, "h": h, "k": k, "l": l, "lam": lam, "th": 0, "task": f"cubic cell a = {a} pm: at what angle θ (degrees) does the ({h}{k}{l}) reflection appear with λ = {lam} pm, first order?", "ans": round(ans, 10)})
    else:
        ans = lam / (2 * math.sin(math.radians(th)))
        cases.append({"w": w, "a": 0, "h": 0, "k": 0, "l": 0, "lam": lam, "th": th, "task": f"A first-order reflection of {lam} pm X-rays appears at θ = {th}°. What is the plane spacing d (pm)?", "ans": round(ans, 10)})
val("in-bragg", "inorg.solids", "Bragg diffraction. {{task}}", "Answer",
    "$n\\lambda = 2d\\sin\\theta$, and for a cubic cell $d_{hkl} = a/\\sqrt{h^2 + k^2 + l^2}$. θ is half the angle between incident and diffracted beams (2θ is what a diffractometer reports)",
    cases, "bragg(w, a, h, k, l, lam, th)")

RR = [("Na⁺/Cl⁻", 0.52, 1), ("Cs⁺/Cl⁻", 0.93, 2), ("Zn²⁺/S²⁻", 0.40, 0), ("Mg²⁺/O²⁻", 0.51, 1), ("Li⁺/I⁻", 0.35, 0), ("K⁺/F⁻", 1.0, 2), ("Be²⁺/O²⁻", 0.26, 0)]
LIT2 = ["4 (tetrahedral)", "6 (octahedral)", "8 (cubic)"]
cases = [{"pair": p, "r": r, "ans": n} for p, r, n in RR]
pick("in-radius-ratio", "inorg.solids", "{{pair}} has radius ratio r₊/r₋ = {{r}}. What coordination number does the radius-ratio rule predict for the cation?", LIT2,
     "The cation must touch its anions without the anions overlapping. The limits are 0.225 (tetrahedral), 0.414 (octahedral) and 0.732 (cubic): √(3/2) − 1, √2 − 1 and √3 − 1. Real structures often break the rule (Li⁺/I⁻, ZnS), so treat it as a guide",
     cases, "radius_ratio_cn(r)")

yaml.safe_dump(T, open(OUT, "w"), allow_unicode=True, sort_keys=False, width=200)
print(len(T), "templates,", sum(len(t["cases"]) for t in T), "cases ->", OUT)
