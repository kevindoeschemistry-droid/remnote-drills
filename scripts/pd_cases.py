"""Builds sp-separations.yaml (framework separations, SP) and pd-design.yaml (framework process-design, PD).
Run: python3 scripts/pd_cases.py. Closed forms here; tests/verify/sepcalc.py checks another way.
"""
import math
import random
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent / "drills/problems"
OUT = {"sp": [], "pd": []}
rnd = random.Random(5)
R = lambda v: float(f"{v:.13g}")  # noqa: E731


def val(f, name, skill, prompt, ask, explain, cases, verify, tol=0.0005, pace="quick"):
    OUT[f].append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
                   "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(f, name, skill, prompt, options, explain, cases, verify, pace="recall"):
    OUT[f].append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
                   "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}], "verify": {"choices": {"y": verify}}})


# ════ separations ═══════════════════════════════════════════════════════════
cases = []
for PA, PB, x in [(101.3, 40.0, 0.4), (180.0, 75.0, 0.25), (95.0, 31.0, 0.6), (150.0, 100.0, 0.5)]:
    a = PA / PB
    cases.append({"PA": PA, "PB": PB, "xa": x, "ans": R(a * x / (1 + (a - 1) * x))})
val("sp", "sp-vle-alpha", "sep.vle", "An ideal binary liquid holds mole fraction {{xa}} of A. Pure-component vapour pressures are {{PA}} kPa (A) and {{PB}} kPa (B). What is A's mole fraction in the vapour?", "y_A",
    "Relative volatility α = P_A*/P_B*, and $y = \\dfrac{\\alpha x}{1 + (\\alpha - 1)x}$. The larger α, the easier the split; α near 1 means many stages",
    cases, "y_from_raoult(PA, PB, xa)")

cases = []
for a, xD, xB in [(2.5, 0.95, 0.05), (2.0, 0.99, 0.01), (1.5, 0.95, 0.05), (3.0, 0.98, 0.02), (1.2, 0.90, 0.10)]:
    cases.append({"alpha": a, "xD": xD, "xB": xB, "ans": R(math.log((xD / (1 - xD)) * ((1 - xB) / xB)) / math.log(a))})
val("sp", "sp-fenske", "sep.distillation", "A binary column with constant relative volatility α = {{alpha}} must make x_D = {{xD}} and x_B = {{xB}}. What is the minimum number of equilibrium stages (total reflux)?", "N_min",
    "Fenske: $N_{\\min} = \\dfrac{\\ln[(x_D/(1-x_D))((1-x_B)/x_B)]}{\\ln\\alpha}$, counting the reboiler as a stage. Halving α − 1 roughly doubles the stages",
    cases, "fenske_steps(alpha, xD, xB)")

cases = []
for a, xD, xF in [(2.5, 0.95, 0.40), (2.0, 0.99, 0.50), (3.0, 0.95, 0.30), (1.8, 0.90, 0.45)]:
    cases.append({"alpha": a, "xD": xD, "xF": xF, "ans": R((xD / xF - a * (1 - xD) / (1 - xF)) / (a - 1))})
val("sp", "sp-rmin", "sep.distillation", "A saturated-liquid feed with x_F = {{xF}} goes to a binary column (α = {{alpha}}) making x_D = {{xD}}. What is the minimum reflux ratio?", "R_min",
    "For a saturated-liquid feed, Underwood reduces to $R_{\\min} = \\dfrac{1}{\\alpha - 1}\\left[\\dfrac{x_D}{x_F} - \\dfrac{\\alpha(1 - x_D)}{1 - x_F}\\right]$. Graphically, the top operating line pinches the equilibrium curve on the q-line. Columns usually run at 1.2–1.5 R_min",
    cases, "rmin_pinch(alpha, xD, xF)")

cases = []
for A, f in [(1.4, 0.95), (2.0, 0.99), (1.2, 0.90), (1.5, 0.98), (3.0, 0.999)]:
    cases.append({"A": A, "f": f, "pct": round(f * 100, 3), "ans": R(math.log((A - f) / (1 - f)) / math.log(A) - 1)})
val("sp", "sp-kremser", "sep.absorption", "An absorber with absorption factor A = L/(mV) = {{A}} and solute-free solvent must remove {{pct}}% of the solute. How many equilibrium stages?", "N",
    "Kremser: fraction absorbed $= \\dfrac{A^{N+1} - A}{A^{N+1} - 1}$, so $N = \\dfrac{\\ln[(A - f)/(1 - f)]}{\\ln A} - 1$. With A < 1 the recovery is capped at A however many stages",
    cases, "kremser_stages(A, f)")

cases = []
for RH, ps, P in [(0.5, 3.17, 101.325), (0.8, 4.25, 101.325), (0.3, 7.38, 101.325), (1.0, 2.34, 101.325), (0.6, 3.17, 85.0)]:
    pw = RH * ps
    cases.append({"RH": RH, "pc": round(RH * 100, 2), "ps": ps, "P": P, "ans": R(pw / (P - pw) * 18.015 / 28.97)})
val("sp", "sp-humidity", "sep.humidification", "Air at {{P}} kPa has {{pc}}% relative humidity where water's vapour pressure is {{ps}} kPa. What is the absolute humidity (kg water per kg dry air)?", "H (kg/kg)",
    "p_w = RH × p*, then $H = \\dfrac{p_w}{P - p_w}\\dfrac{M_w}{M_{air}} = 0.622\\dfrac{p_w}{P - p_w}$. Saturation is RH = 100%; cooling air at constant H raises RH until dew forms",
    cases, "abs_humidity(RH, ps, P)")

cases = []
for F, x0, x1 in [(1000, 0.05, 0.25), (5000, 0.10, 0.50), (2000, 0.12, 0.40), (800, 0.08, 0.60)]:
    cases.append({"F": F, "x0": x0, "x1": x1, "p0": round(x0 * 100, 3), "p1": round(x1 * 100, 3), "ans": R(F * (1 - x0 / x1))})
val("sp", "sp-evaporator", "sep.humidification", "An evaporator concentrates {{F}} kg/h of a solution from {{p0}}% to {{p1}}% solids. How much water is evaporated (kg/h)?", "V (kg/h)",
    "Solids pass through unchanged: F x₀ = L x₁, so L = F x₀/x₁ and V = F − L. A balance on the non-volatile component always comes first",
    cases, "evaporated(F, x0, x1)")

# ════ process design, economics, safety, control ════════════════════════════
cases = []
for I, A, n, i, S in [(1e6, 250000, 6, 0.10, 0), (5e5, 120000, 5, 0.08, 50000), (2e6, 400000, 8, 0.12, 200000), (3e5, 60000, 10, 0.07, 0)]:
    pv = A * (1 - (1 + i) ** -n) / i + S * (1 + i) ** -n
    cases.append({"I": I, "A": A, "n": n, "i": i, "S": S, "pi": round(i * 100, 3), "ans": R(pv - I)})
val("pd", "pd-npv", "design.economics", "A project costs {{I}} dollars now and returns {{A}} dollars a year for {{n}} years, plus a {{S}} dollar salvage value at the end. At {{pi}}% interest, what is its net present value (dollars)?", "NPV",
    "NPV = −I + A·(P/A, i, n) + S(1 + i)⁻ⁿ, with the annuity factor (P/A) = [1 − (1 + i)⁻ⁿ]/i. Accept projects with NPV > 0 at the company's minimum rate",
    cases, "npv(I, A, n, i, S)", tol=0.0002)

cases = []
for I, flows in [(100000, [30000, 30000, 30000, 30000, 30000]), (250000, [40000, 70000, 90000, 100000, 100000]), (60000, [10000, 20000, 30000, 40000]), (500000, [150000, 150000, 150000, 150000])]:
    cum, yrs = -I, None
    for k, f in enumerate(flows, 1):
        if cum + f >= 0 and yrs is None:
            yrs = k - 1 + (-cum) / f
        cum += f
    cases.append({"I": I, "flows": flows, "ft": ", ".join(str(f) for f in flows), "ans": R(yrs)})
val("pd", "pd-payback", "design.economics", "An investment of {{I}} dollars returns {{ft}} dollars in successive years. What is the simple payback period (years)?", "Years",
    "Add the yearly cash flows until they cover the investment, interpolating within the final year. Payback ignores the time value of money and everything after the payback year",
    cases, "payback(I, flows)")

cases = []
for C1, S1, S2, n, I1, I2 in [(1e6, 100, 200, 0.6, 500, 600), (2.5e5, 50, 150, 0.6, 550, 800), (4e6, 1000, 500, 0.7, 700, 700), (8e5, 20, 60, 0.6, 600, 815)]:
    cases.append({"C1": C1, "S1": S1, "S2": S2, "n": n, "I1": I1, "I2": I2, "ans": R(C1 * (S2 / S1) ** n * I2 / I1)})
val("pd", "pd-cost-scaling", "design.economics", "Equipment of capacity {{S1}} cost {{C1}} dollars when the cost index was {{I1}}. Estimate a {{S2}}-capacity unit now (index {{I2}}) with a scaling exponent of {{n}}.", "Cost (dollars)",
    "Capacity: C₂ = C₁(S₂/S₁)ⁿ with n ≈ 0.6 (the six-tenths rule), reflecting economies of scale. Time: multiply by the ratio of cost indices (CEPCI) between the two dates",
    cases, "scaled_cost(C1, S1, S2, n, I1, I2)")

cases = []
for kind, P, S, n, k in [("sl", 100000, 10000, 10, 3), ("sl", 50000, 5000, 5, 2), ("ddb", 100000, 0, 10, 3), ("ddb", 80000, 0, 5, 2), ("ddb", 40000, 0, 8, 4)]:
    v = P - k * (P - S) / n if kind == "sl" else P * (1 - 2 / n) ** k
    cases.append({"kind": kind, "kw": {"sl": "straight-line", "ddb": "double-declining-balance"}[kind], "P": P, "S": S, "n": n, "k": k, "ans": R(v)})
val("pd", "pd-depreciation", "design.economics", "Equipment costs {{P}} dollars, has a {{n}}-year life and a salvage value of {{S}} dollars. What is its book value after {{k}} years of {{kw}} depreciation (dollars)?", "Book value",
    "Straight line takes (P − S)/n each year. Double-declining balance takes 2/n of the current book value each year (salvage ignored until the book value reaches it): faster write-off, earlier tax savings",
    cases, "book_value(kind, P, S, n, k)")

cases = []
for r, m in [(0.12, 12), (0.10, 4), (0.08, 365), (0.06, 2), (0.18, 12)]:
    cases.append({"r": r, "pr": round(r * 100, 3), "m": m, "ans": R((1 + r / m) ** m - 1)})
val("pd", "pd-effective-rate", "design.economics", "A loan charges a nominal {{pr}}% a year compounded {{m}} times a year. What is the effective annual rate (as a fraction)?", "i_eff",
    "$i_{eff} = (1 + r/m)^m - 1$; continuous compounding gives e^r − 1. Compare loans by effective rates, never nominal ones",
    cases, "effective_rate(r, m)")

cases = []
for names, ys, lfls in [(("methane", "ethane"), (0.8, 0.2), (5.0, 3.0)), (("methane", "propane", "butane"), (0.5, 0.3, 0.2), (5.0, 2.1, 1.8)),
                        (("hydrogen", "methane"), (0.4, 0.6), (4.0, 5.0)), (("propane", "butane"), (0.6, 0.4), (2.1, 1.8))]:
    cases.append({"mix": ", ".join(f"{int(y * 100)}% {n}" for n, y in zip(names, ys)), "lt": ", ".join(f"{n} {l}%" for n, l in zip(names, lfls)),
                  "ys": list(ys), "lfls": list(lfls), "ans": R(1 / sum(y / l for y, l in zip(ys, lfls)))})
val("pd", "pd-lfl-mixture", "design.safety", "A fuel gas is {{mix}} (fuel basis). Lower flammable limits in air: {{lt}}. What is the mixture's LFL (vol % fuel in air)?", "LFL (%)",
    "Le Chatelier: $LFL_{mix} = 1/\\sum (y_i/LFL_i)$, with yᵢ fractions of the fuel only. Keep a vessel below about 25% of the LFL (or inert it) to stay safe",
    cases, "lfl_mix(ys, lfls)")

cases = []
for cs, tlvs, names in [((20, 30), (50, 100), "toluene 20 ppm (TLV 50), xylene 30 ppm (TLV 100)"), ((40, 60), (50, 100), "toluene 40 ppm (TLV 50), xylene 60 ppm (TLV 100)"),
                        ((100, 150, 50), (500, 400, 200), "acetone 100 (TLV 500), MEK 150 (TLV 400)... with ethyl acetate 50 ppm (TLV 200)"),
                        ((2, 0.5), (5, 1), "chemical A 2 ppm (TLV 5), chemical B 0.5 ppm (TLV 1)")]:
    tot = sum(c / t for c, t in zip(cs, tlvs))
    cases.append({"cs": list(cs), "tlvs": list(tlvs), "names": names, "ans": 1 if tot > 1 else 0})
pick("pd", "pd-tlv-mixture", "design.safety", "Workers breathe {{names}}, all acting on the same organ. Is the combined exposure within the limit?", ["Within the limit", "Over the limit"],
     "For additive effects, sum Cᵢ/TLVᵢ: the mixture exceeds its limit if the sum is above 1, even when each component alone is below its own TLV",
     cases, "exposure_over(cs, tlvs)", pace="quick")

HZ = {"NO": "none of the design intent happens", "MORE": "a quantitative increase", "LESS": "a quantitative decrease", "REVERSE": "the logical opposite of the intent",
      "AS WELL AS": "something extra happens besides the intent", "PART OF": "only some of the intent happens", "OTHER THAN": "something completely different happens"}
cases = []
for k, v in HZ.items():
    wrong = [w for w in HZ.values() if w != v]
    rnd.shuffle(wrong)
    opts = [v] + wrong[:3]
    rnd.shuffle(opts)
    cases.append({"k": k, **{f"o{i + 1}": o for i, o in enumerate(opts)}, "ans": opts.index(v)})
pick("pd", "pd-hazop", "design.safety", "In a HAZOP study, what does the guide word {{k}} mean?", ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"],
     "Guide words are applied to each process parameter at each node (NO flow, MORE pressure, REVERSE flow…) to generate deviations; the team then lists causes, consequences and safeguards for each",
     cases, "hazop_pick(k, o1, o2, o3, o4)")

cases = []
for w, tau, f, t in [(0, 5, 0.632, 0), (0, 2, 0.95, 0), (0, 10, 0.99, 0), (1, 4, 0, 4), (1, 3, 0, 9), (1, 20, 0, 5)]:
    ans = -tau * math.log(1 - f) if w == 0 else 1 - math.exp(-t / tau)
    task = [f"How long (min) until the output reaches {f * 100:g}% of its final change?", f"What fraction of the final change has occurred after {t} min?"][w]
    cases.append({"w": w, "tau": tau, "f": f, "t": t, "task": task, "ans": R(ans)})
val("pd", "pd-first-order", "design.control", "A first-order process (time constant {{tau}} min, no dead time) gets a step in its input. {{task}}", "Answer",
    "τ dy/dt + y = K·Δu gives y = KΔu(1 − e^(−t/τ)): 63.2% at t = τ, 95% at 3τ, 99% at 4.6τ. The time constant is read off a step test at 63.2%",
    cases, "first_order(w, tau, f, t)")

for k, v in {"sp": "sp-separations.yaml", "pd": "pd-design.yaml"}.items():
    yaml.safe_dump(OUT[k], open(ROOT / v, "w"), allow_unicode=True, sort_keys=False, width=200)
    print(v, len(OUT[k]), "templates,", sum(len(t["cases"]) for t in OUT[k]), "cases")
