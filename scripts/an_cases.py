"""Builds drills/problems/an-analytical.yaml (framework analytical-chemistry, AN). Run: python3 scripts/an_cases.py

Answers follow the stoichiometric chains and closed forms the cards teach (mole ratios, gravimetric
factors, the quadratic for a common-ion solubility, q = (V/(V + DV'))ⁿ, Cramer's rule for two components,
the summation formulas for least squares). tests/verify/incalc.py checks each another way: element
balances, sympy solves of the full equilibria, extraction one step at a time, a matrix solve.
"""
import math
import random
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/an-analytical.yaml"
T = []
rnd = random.Random(11)
M = {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "P": 30.974, "S": 32.06, "Cl": 35.45,
     "K": 39.098, "Ca": 40.078, "Fe": 55.845, "Ni": 58.693, "Cu": 63.546, "Ag": 107.868, "Ba": 137.327, "Mn": 54.938}


def mm(d):
    return sum(M[k] * v for k, v in d.items())


MM = {"CaCO3": mm({"Ca": 1, "C": 1, "O": 3}), "Fe": M["Fe"], "Cl": M["Cl"], "AgCl": mm({"Ag": 1, "Cl": 1}), "BaSO4": mm({"Ba": 1, "S": 1, "O": 4}),
      "SO4": mm({"S": 1, "O": 4}), "Fe2O3": mm({"Fe": 2, "O": 3}), "Ni(C4H7N2O2)2": mm({"Ni": 1, "C": 8, "H": 14, "N": 4, "O": 4}), "Ni": M["Ni"],
      "Mg2P2O7": mm({"Mg": 2, "P": 2, "O": 7}), "MgO": mm({"Mg": 1, "O": 1}), "P": M["P"], "N": M["N"], "Al2O3": mm({"Al": 2, "O": 3}), "Al": M["Al"],
      "NaCl": mm({"Na": 1, "Cl": 1}), "Mg": M["Mg"]}


def val(name, skill, prompt, ask, explain, cases, verify, tol=0.0002, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(name, skill, prompt, options, explain, cases, verify, pace="recall"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}],
              "verify": {"choices": {"y": verify}}})


R = lambda v: round(v, 12)  # noqa: E731

# ── 1. titrations ────────────────────────────────────────────────────────────
cases = []
for m, c_hcl, v_hcl, c_naoh, v_naoh in [(0.2500, 0.1000, 50.00, 0.1000, 12.40), (0.5000, 0.2000, 50.00, 0.1500, 21.30), (0.3000, 0.1500, 40.00, 0.1000, 15.85), (0.1800, 0.1000, 50.00, 0.0950, 17.20)]:
    n_hcl = c_hcl * v_hcl / 1000
    n_left = c_naoh * v_naoh / 1000
    pct = (n_hcl - n_left) / 2 * MM["CaCO3"] / m * 100
    cases.append({"m": m, "ch": c_hcl, "vh": v_hcl, "cn": c_naoh, "vn": v_naoh, "ans": R(pct)})
val("an-back-titration", "anal.titration", "A {{m}} g limestone sample is dissolved in {{vh}} mL of {{ch}} M HCl (excess). The leftover acid takes {{vn}} mL of {{cn}} M NaOH. What is the mass percent of CaCO₃?", "% CaCO₃",
    "HCl added − HCl left = HCl used by the carbonate; CaCO₃ + 2HCl, so mol CaCO₃ is half of that. Back titration suits a sample that dissolves slowly or has no sharp end point of its own",
    cases, "100*(nsimplify(ch)*nsimplify(vh)/1000 - nsimplify(cn)*nsimplify(vn)/1000)/2*molar_mass('CaCO3')/nsimplify(m)")

cases = []
for kind, m, c, v in [(0, 0.4000, 0.02000, 28.45), (0, 0.6500, 0.02150, 31.20), (1, 0.2500, 0.02000, 24.60), (1, 0.3100, 0.01850, 30.15)]:
    if kind == 0:  # Fe2+ + MnO4-: 5 Fe per MnO4
        ans = c * v / 1000 * 5 * M["Fe"] / m * 100
        cases.append({"kind": 0, "m": m, "c": c, "v": v, "what": "iron (titrated as Fe²⁺)", "rx": "MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O", "ans": R(ans)})
    else:  # oxalate: 2 MnO4 per 5 C2O4; analyte reported as Ca precipitated as CaC2O4
        ans = c * v / 1000 * 5 / 2 * M["Ca"] / m * 100
        cases.append({"kind": 1, "m": m, "c": c, "v": v, "what": "calcium (precipitated as CaC₂O₄, then the oxalate titrated)", "rx": "2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O", "ans": R(ans)})
val("an-permanganate", "anal.titration", "A {{m}} g sample is analysed for {{what}} with {{v}} mL of {{c}} M KMnO₄ ({{rx}}). What is the mass percent?", "Mass %",
    "Electrons decide the ratio: MnO₄⁻ takes 5, Fe²⁺ gives 1, C₂O₄²⁻ gives 2. Permanganate is its own indicator: the first lasting pink is the end point",
    cases, "[100*nsimplify(c)*nsimplify(v)/1000*half_electrons('MnO4', -1, 'Mn', 2, 'Mn')/half_electrons('Fe', 2, 'Fe', 3, 'Fe')*molar_mass('Fe')/nsimplify(m), "
           "100*nsimplify(c)*nsimplify(v)/1000*half_electrons('MnO4', -1, 'Mn', 2, 'Mn')/half_electrons('C2O4', -2, 'CO2', 0, 'C')*molar_mass('Ca')/nsimplify(m)][kind]")

cases = []
for vs, ce, ve in [(100.0, 0.01000, 18.35), (50.00, 0.01000, 12.10), (100.0, 0.005000, 31.60), (25.00, 0.01000, 6.45)]:
    ppm = ce * ve / 1000 * MM["CaCO3"] * 1000 / (vs / 1000)
    cases.append({"vs": vs, "ce": ce, "ve": ve, "ans": R(ppm)})
val("an-edta-hardness", "anal.titration", "A {{vs}} mL water sample at pH 10 takes {{ve}} mL of {{ce}} M EDTA to the Eriochrome Black T end point. What is the hardness, as mg CaCO₃ per litre (ppm)?", "Hardness (ppm CaCO₃)",
    "EDTA binds every metal ion 1:1, so mol (Ca + Mg) = mol EDTA; hardness is reported as if it were all CaCO₃ (100.09 g/mol), in mg per litre of sample",
    cases, "nsimplify(ce)*nsimplify(ve)/1000*molar_mass('CaCO3')*1000/(nsimplify(vs)/1000)")

cases = []
for m, c, v in [(0.2000, 0.1000, 21.40), (0.5000, 0.1000, 30.25), (0.3000, 0.0500, 40.10), (0.1500, 0.0800, 20.75)]:
    cases.append({"m": m, "c": c, "v": v, "ans": R(c * v / 1000 * M["Cl"] / m * 100)})
val("an-mohr", "anal.titration", "A {{m}} g sample is titrated with {{v}} mL of {{c}} M AgNO₃ to the Mohr end point (brick-red Ag₂CrO₄). What is the mass percent of chloride?", "% Cl",
    "Ag⁺ + Cl⁻ → AgCl, 1:1. The chromate indicator only precipitates once Cl⁻ is used up, because Ag₂CrO₄ is more soluble than AgCl. Work near neutral pH: in acid chromate becomes dichromate, in base Ag₂O forms",
    cases, "100*nsimplify(c)*nsimplify(v)/1000*molar_mass('Cl')/nsimplify(m)")

cases = []
for m, ca, va, cb, vb, f in [(0.5000, 0.1000, 50.00, 0.1000, 22.15, 6.25), (0.8000, 0.1000, 50.00, 0.1000, 16.80, 6.25), (0.6000, 0.0500, 50.00, 0.0500, 9.40, 6.38), (0.2500, 0.1000, 25.00, 0.1000, 11.35, 5.70)]:
    nN = ca * va / 1000 - cb * vb / 1000
    pctN = nN * M["N"] / m * 100
    cases.append({"m": m, "ca": ca, "va": va, "cb": cb, "vb": vb, "f": f, "ans": R(pctN * f)})
val("an-kjeldahl", "anal.titration", "Kjeldahl: the NH₃ from {{m}} g of food is distilled into {{va}} mL of {{ca}} M HCl; the excess acid takes {{vb}} mL of {{cb}} M NaOH. With a nitrogen-to-protein factor of {{f}}, what is the percent protein?", "% protein",
    "Digestion turns organic N into NH₄⁺, which is distilled as NH₃ into a known excess of acid. mol N = acid added − acid left; % protein = % N × the factor (6.25 for typical protein at 16% N)",
    cases, "nsimplify(f)*100*(nsimplify(ca)*nsimplify(va) - nsimplify(cb)*nsimplify(vb))/1000*molar_mass('N')/nsimplify(m)")


def ha_ph(Ca, Va, Ka, Cb, Vb):
    """full charge balance by bisection on pH (generator route)"""
    V = Va + Vb
    cA, cNa = Ca * Va / V, Cb * Vb / V
    f = lambda p: 10**-p + cNa - cA * Ka / (Ka + 10**-p) - 1e-14 / 10**-p  # noqa: E731
    lo, hi = mp.mpf(0), mp.mpf(14)
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


cases = []
for Ka, name in [(1.75e-5, "acetic acid"), (6.3e-5, "benzoic acid"), (1.8e-4, "formic acid")]:
    for frac in (0.0, 0.5, 1.0, 1.2):
        Ca, Va, Cb = 0.1000, 25.00, 0.1000
        Vb = Va * Ca / Cb * frac
        ph = ha_ph(mp.mpf(Ca), mp.mpf(Va), mp.mpf(Ka), mp.mpf(Cb), mp.mpf(Vb))
        cases.append({"Ka": Ka, "name": name, "Ca": Ca, "Va": Va, "Cb": Cb, "Vb": round(Vb, 4), "ans": float(mp.nstr(ph, 14))})
val("an-titration-ph", "anal.titration", "{{Va}} mL of {{Ca}} M {{name}} (Kₐ = {{Ka}}) is titrated with {{Cb}} M NaOH. What is the pH after {{Vb}} mL of base?", "pH",
    "Before any base: the weak-acid equilibrium. In the buffer region: Henderson–Hasselbalch (at halfway, pH = pKₐ). At equivalence: the conjugate base hydrolyses, so pH > 7. Past it: excess OH⁻ sets the pH. The reference answer solves the full charge balance; the usual approximations land within a few hundredths",
    cases, "weak_acid_ph(Ca, Va, Ka, Cb, Vb)", tol=0.01, pace="workout")

LIT = ["methyl orange (3.1–4.4)", "methyl red (4.4–6.2)", "bromothymol blue (6.0–7.6)", "phenolphthalein (8.2–10.0)"]
cases = []
for Ka, name in [(1.75e-5, "0.1 M acetic acid with 0.1 M NaOH"), (6.3e-5, "0.1 M benzoic acid with 0.1 M NaOH"), (1.8e-4, "0.1 M formic acid with 0.1 M NaOH"),
                 (10.0, "0.1 M HCl with 0.1 M NaOH")]:
    cases.append({"Ka": Ka, "name": name, "ans": 3 if Ka < 1 else 2})
pick("an-indicator", "anal.titration", "Which indicator suits the titration of {{name}}?", LIT,
     "Choose an indicator whose colour change brackets the equivalence-point pH. A weak acid with strong base ends above 7 (conjugate base), so phenolphthalein; strong acid with strong base ends at 7, where the curve is so steep that bromothymol blue (and in practice phenolphthalein or methyl red) all work",
     cases, "indicator_pick(nsimplify('0.1'), 25, Ka, nsimplify('0.1'), 25)")

# ── 2. gravimetry ────────────────────────────────────────────────────────────
GRAV = [("Cl", "AgCl", "Cl", 1, 1, 0.3500, 0.6120, "chloride, weighed as AgCl"), ("SO4", "BaSO4", "S", 1, 1, 0.5000, 0.7340, "sulfate, weighed as BaSO₄"),
        ("Fe", "Fe2O3", "Fe", 2, 1, 0.8000, 0.2860, "iron, weighed as Fe₂O₃"), ("Ni", "Ni(C4H7N2O2)2", "Ni", 1, 1, 0.4500, 0.1840, "nickel, weighed as Ni(DMG)₂"),
        ("MgO", "Mg2P2O7", "Mg", 2, 1, 0.6000, 0.3120, "magnesium as MgO, weighed as Mg₂P₂O₇"), ("Al", "Al2O3", "Al", 2, 1, 0.9000, 0.1550, "aluminium, weighed as Al₂O₃")]
cases = []
for an, ppt, el, k_ppt, k_an, ms, mp_, what in GRAV:
    gf = k_ppt * MM[an] / (k_an * MM[ppt]) if an != "MgO" else 2 * MM["MgO"] / MM["Mg2P2O7"]
    cases.append({"an": an, "ppt": ppt, "el": el, "ms": ms, "mp": mp_, "what": what, "ans": R(mp_ * gf / ms * 100)})
val("an-gravimetric", "anal.gravimetry", "A {{ms}} g sample is analysed for {{what}}; the dried precipitate weighs {{mp}} g. What is the mass percent?", "Mass %",
    "Gravimetric factor = (M of analyte × atoms of the element in the precipitate) ÷ (M of precipitate × atoms of it in the analyte): Fe in Fe₂O₃ is 2 × 55.845 / 159.69. Then % = factor × m(ppt) / m(sample) × 100",
    cases, "mass_percent_from_ppt(an, ppt, el, mp, ms)")

# ── 3. equilibria in analysis ────────────────────────────────────────────────
cases = []
for salt, Ksp, ion, c in [("AgCl", 1.8e-10, "NaCl", 0.010), ("AgCl", 1.8e-10, "NaCl", 1e-5), ("BaSO4", 1.1e-10, "Na₂SO₄", 0.0010), ("AgBr", 5.0e-13, "KBr", 1e-6), ("CaF2", 0, "", 0)]:
    if not Ksp:
        continue
    s = (-c + math.sqrt(c * c + 4 * Ksp)) / 2
    cases.append({"salt": salt, "Ksp": Ksp, "ion": ion, "c": c, "ans": float(f"{s:.14g}")})
val("an-common-ion", "anal.equilibria", "What is the molar solubility of {{salt}} (K_sp = {{Ksp}}) in {{c}} M {{ion}}?", "s (M)",
    "s(s + c) = K_sp. When c ≫ s the shortcut s ≈ K_sp/c is fine; at trace levels of the common ion keep the quadratic, s = [−c + √(c² + 4K_sp)]/2",
    cases, "ksp_common(Ksp, c)", tol=0.001)

cases = []
for Ksp, Kf, L in [(1.8e-10, 1.7e7, 1.0), (1.8e-10, 1.7e7, 0.10), (5.0e-13, 1.7e7, 1.0), (5.0e-13, 1.7e7, 3.0)]:
    K = Ksp * Kf
    # s = K^(1/2) (L - 2s): s = sqrt(K) L / (1 + 2 sqrt(K)); Ag+ left out (Ksp/s, negligible) -> solve exactly with it included
    s_sym = mp.findroot(lambda s: s - Ksp / s - Kf * (Ksp / s) * (L - 2 * (s - Ksp / s)) ** 2, mp.sqrt(K) * L / (1 + 2 * mp.sqrt(K)))
    cases.append({"Ksp": Ksp, "Kf": Kf, "L": L, "salt": "AgCl" if Ksp > 1e-11 else "AgBr", "ans": float(mp.nstr(s_sym, 14))})
val("an-complex-solubility", "anal.equilibria", "What is the molar solubility of {{salt}} (K_sp = {{Ksp}}) in {{L}} M NH₃ (β₂ for Ag(NH₃)₂⁺ = {{Kf}})?", "s (M)",
    "Combine the equilibria: AgX + 2NH₃ ⇌ Ag(NH₃)₂⁺ + X⁻ with K = K_sp·β₂. Then s²/(L − 2s)² = K. This is why AgCl dissolves in dilute ammonia and AgBr barely does",
    cases, "complex_solubility(Ksp, Kf, L)", tol=0.001)

# ── 4. separations ───────────────────────────────────────────────────────────
cases = []
for Vaq, Vorg, D, n in [(100, 50, 3.0, 1), (100, 25, 3.0, 2), (100, 10, 5.0, 5), (50, 50, 1.5, 3), (100, 100, 4.0, 1), (100, 20, 4.0, 5)]:
    q = (Vaq / (Vaq + D * Vorg)) ** n
    cases.append({"Vaq": Vaq, "Vorg": Vorg, "D": D, "n": n, "ans": R(q)})
val("an-extraction", "anal.separations", "A solute with distribution ratio D = {{D}} (organic/aqueous) is extracted from {{Vaq}} mL of water with {{n}} portion(s) of {{Vorg}} mL organic solvent. What fraction stays in the water?", "Fraction left",
    "Each extraction leaves the fraction V_aq/(V_aq + D·V_org); n extractions multiply it: q = [V_aq/(V_aq + D V_org)]ⁿ. Several small portions beat one large one with the same total volume",
    cases, "extraction_left(Vaq, Vorg, D, n)")

cases = []
for w, tr, wb, tm, tr2, wb2 in [(0, 8.40, 0.42, 0, 9, 1), (0, 12.6, 0.50, 0, 13, 1), (1, 8.40, 0.42, 1.10, 9, 1), (1, 5.25, 0.30, 0.80, 6, 1),
                                (2, 8.40, 0.42, 0, 9.10, 0.46), (2, 4.10, 0.20, 0, 4.45, 0.24)]:
    ans = 16 * (tr / wb) ** 2 if w == 0 else ((tr - tm) / tm if w == 1 else 2 * (tr2 - tr) / (wb + wb2))
    tm = tm or 1  # unused by this case; keeps the verifier's list from dividing by zero
    task = [f"A peak elutes at {tr} min with a baseline width of {wb} min. How many theoretical plates N does the column have?",
            f"A peak elutes at {tr} min; an unretained marker comes out at {tm} min. What is the retention factor k?",
            f"Two peaks elute at {tr} and {tr2} min with baseline widths {wb} and {wb2} min. What is the resolution R_s?"][w]
    cases.append({"w": w, "tr": tr, "wb": wb, "tm": tm, "tr2": tr2, "wb2": wb2, "task": task, "ans": R(ans)})
val("an-chromatography", "anal.separations", "Chromatography. {{task}}", "Answer",
    "N = 16(t_R/W)² from the baseline width (5.54(t_R/W½)² from the half-height width); k = (t_R − t_M)/t_M; R_s = 2Δt_R/(W₁ + W₂), and R_s ≥ 1.5 is baseline separation",
    cases, "[16*(nsimplify(tr)/nsimplify(wb))**2, (nsimplify(tr) - nsimplify(tm))/nsimplify(tm), 2*(nsimplify(tr2) - nsimplify(tr))/(nsimplify(wb) + nsimplify(wb2))][w]")

# ── 5. measurement and data ──────────────────────────────────────────────────
cases = []
for w, e1x, e1y, e2x, e2y, A1, A2 in [(0, 5000, 1200, 800, 4000, 0.620, 0.480), (1, 5000, 1200, 800, 4000, 0.620, 0.480), (0, 9000, 300, 1500, 6000, 0.455, 0.700),
                                       (1, 9000, 300, 1500, 6000, 0.455, 0.700), (0, 3500, 2500, 600, 5100, 0.410, 0.380)]:
    det = e1x * e2y - e1y * e2x
    cx = (A1 * e2y - e1y * A2) / det
    cy = (e1x * A2 - A1 * e2x) / det
    cases.append({"w": w, "wt": ["X", "Y"][w], "e1x": e1x, "e1y": e1y, "e2x": e2x, "e2y": e2y, "A1": A1, "A2": A2, "ans": float(f"{[cx, cy][w]:.14g}")})
val("an-two-component", "anal.measurement", "A mixture of X and Y in a 1.00 cm cell reads A = {{A1}} at λ₁ and {{A2}} at λ₂. Molar absorptivities (L mol⁻¹ cm⁻¹): X {{e1x}} and Y {{e1y}} at λ₁; X {{e2x}} and Y {{e2y}} at λ₂. What is [{{wt}}] (M)?", "Concentration (M)",
    "Absorbances add: A₁ = ε₁ₓb[X] + ε₁ᵧb[Y], A₂ = ε₂ₓb[X] + ε₂ᵧb[Y]. Two equations, two unknowns; pick wavelengths where each component dominates one of them",
    cases, "two_component(e1x, e1y, e2x, e2y, A1, A2, w)", tol=0.001)

cases = []
for Ax, Vx, cs, Vs, Asp, Vt in [(0.235, 10.0, 50.0, 1.00, 0.412, 50.0), (0.180, 20.0, 100.0, 0.50, 0.305, 50.0), (0.420, 5.0, 25.0, 2.00, 0.655, 25.0), (0.090, 25.0, 10.0, 5.00, 0.215, 100.0)]:
    c = Ax * cs * Vs / (Vx * (Asp - Ax))
    cases.append({"Ax": Ax, "Vx": Vx, "cs": cs, "Vs": Vs, "Asp": Asp, "Vt": Vt, "ans": R(c)})
val("an-standard-addition", "anal.measurement", "{{Vx}} mL of sample is diluted to {{Vt}} mL and reads {{Ax}}. A second {{Vx}} mL portion plus {{Vs}} mL of a {{cs}} ppm standard, also diluted to {{Vt}} mL, reads {{Asp}}. What is the analyte concentration in the original sample (ppm)?", "c (ppm)",
    "Both flasks share the same matrix and volume, so signal ∝ analyte in the flask: A_x/A_spiked = c V_x/(c V_x + c_s V_s). Solve: c = A_x c_s V_s / [V_x (A_spiked − A_x)]. Standard addition cancels matrix effects that would bias an external calibration",
    cases, "std_addition(Ax, Vx, cs, Vs, Asp, Vt)")

cases = []
for xs, ys, y0 in [([0, 2, 4, 6, 8], [0.002, 0.164, 0.318, 0.487, 0.641], 0.402), ([1, 2, 3, 4], [0.110, 0.205, 0.318, 0.402], 0.260),
                   ([0, 5, 10, 15, 20], [0.010, 0.250, 0.505, 0.740, 0.990], 0.610), ([2, 4, 6, 8, 10], [0.15, 0.31, 0.44, 0.62, 0.76], 0.53)]:
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx, sxy = sum(a * a for a in xs), sum(a * b for a, b in zip(xs, ys))
    m = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    b = (sy - m * sx) / n
    cases.append({"xs": xs, "ys": ys, "xt": ", ".join(map(str, xs)), "yt": ", ".join(map(str, ys)), "y0": y0, "ans": float(f"{(y0 - b) / m:.14g}")})
val("an-calibration", "anal.measurement", "Standards at {{xt}} ppm read {{yt}}. An unknown reads {{y0}}. Using the least-squares line, what is the unknown's concentration (ppm)?", "c (ppm)",
    "Slope m = (nΣxy − ΣxΣy)/(nΣx² − (Σx)²), intercept b = (Σy − mΣx)/n, then x = (y − b)/m. Read unknowns inside the calibrated range only",
    cases, "calib_unknown(xs, ys, y0)", tol=0.001, pace="workout")

QC = {3: 0.970, 4: 0.829, 5: 0.710, 6: 0.625, 7: 0.568}
cases = []
for vals in [[10.11, 10.15, 10.13, 10.40], [5.02, 5.04, 5.06, 5.20], [0.402, 0.410, 0.405, 0.408, 0.392], [12.47, 12.51, 12.49, 12.62, 12.50],
             [3.12, 3.15, 3.13, 3.14, 3.11, 3.32], [20.1, 20.3, 19.9, 20.2, 21.0], [7.30, 7.32, 7.28, 7.45]]:
    v = sorted(vals)
    gap = max(v[1] - v[0], v[-1] - v[-2])
    cases.append({"vals": vals, "vt": ", ".join(map(str, vals)), "n": len(vals), "qc": QC[len(vals)], "ans": 1 if gap / (v[-1] - v[0]) > QC[len(vals)] else 0})
pick("an-q-test", "anal.measurement", "Replicates: {{vt}}. Dixon's Q-test at 95% confidence (Q_crit = {{qc}} for n = {{n}}): keep or reject the most extreme value?", ["Keep", "Reject"],
     "Q = gap / range, where the gap is between the suspect value and its nearest neighbour. Reject only if Q > Q_crit, and only once: the test is for one outlier",
     cases, "q_test(vals)", pace="quick")

cases = []
for kind, a, sa, b, sb, text in [("prod", 2.50, 0.02, 4.10, 0.03, "y = a × b"), ("quot", 0.4520, 0.0003, 25.00, 0.03, "y = a / b"), ("sum", 12.35, 0.02, 4.18, 0.01, "y = a + b"),
                                 ("quot", 18.24, 0.02, 0.1022, 0.0002, "y = a / b"), ("sum", 50.00, 0.05, 25.00, 0.03, "y = a − b")]:
    if kind == "sum":
        ans = math.sqrt(sa * sa + sb * sb)
        ask = "absolute uncertainty in y"
    else:
        ans = math.sqrt((sa / a) ** 2 + (sb / b) ** 2)
        ask = "relative uncertainty in y (as a fraction)"
    cases.append({"kind": kind, "a": a, "sa": sa, "b": b, "sb": sb, "text": text, "ask": ask, "ans": R(ans)})
val("an-uncertainty", "anal.measurement", "a = {{a}} ± {{sa}} and b = {{b}} ± {{sb}} (independent random errors). For {{text}}, what is the {{ask}}?", "Uncertainty",
    "Sums and differences add absolute uncertainties in quadrature; products and quotients add relative uncertainties in quadrature. Both are the general rule σ_y² = Σ(∂y/∂xᵢ)²σᵢ² applied to the two cases",
    cases, "rel_unc(kind, a, sa, b, sb)", tol=0.001)

INSTR = {"trace lead in drinking water": "ICP-MS", "residual solvents in a drug": "GC", "a non-volatile drug and its impurities": "HPLC",
         "water content of an oil": "Karl Fischer titration", "functional groups of an unknown": "IR spectroscopy",
         "connectivity of an organic unknown": "NMR spectroscopy", "molar mass of a protein": "mass spectrometry", "sodium in serum": "atomic emission (flame photometry)"}
cases = []
for k, v in INSTR.items():
    wrong = [w for w in INSTR.values() if w != v]
    rnd.shuffle(wrong)
    opts = [v] + wrong[:3]
    rnd.shuffle(opts)
    cases.append({"k": k, **{f"o{i + 1}": o for i, o in enumerate(opts)}, "ans": opts.index(v)})
pick("an-instrument", "anal.measurement", "Which technique fits best: {{k}}?", ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"],
     "Match the question to the property measured: elements at trace level by atomic spectrometry (ICP-MS lowest), volatile organics by GC, non-volatile or thermally fragile ones by HPLC, structure by NMR and IR, mass by MS, water specifically by Karl Fischer",
     cases, 'fact_pick("instrument", k, o1, o2, o3, o4)')

yaml.safe_dump(T, open(OUT, "w"), allow_unicode=True, sort_keys=False, width=200)
print(len(T), "templates,", sum(len(t["cases"]) for t in T), "cases ->", OUT)
