"""Builds drills/problems/co-olympiad.yaml (framework chemistry-olympiad, CO): USNCO-national and
IChO-level versions of AP topics. Run: python3 scripts/oly_cases.py

Equilibria are solved here by bisection on the full balances in mpmath; closed forms elsewhere.
tests/verify/olycalc.py solves with sympy and other routes.
"""
import itertools
import math
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/co-olympiad.yaml"
T = []
R = lambda v: float(f"{float(v):.13g}")  # noqa: E731
KW = mp.mpf("1e-14")


def val(name, skill, prompt, ask, explain, cases, verify, tol=0.0005, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def bisect(f, lo=-1, hi=15):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


# ── 1. aqueous equilibria ────────────────────────────────────────────────────
PHOS, CARB = [7.1e-3, 6.3e-8, 4.5e-13], [4.5e-7, 4.7e-11]
cases = []
for name, C, na, K in [("H₃PO₄", 0.10, 0, PHOS), ("NaH₂PO₄", 0.10, 1, PHOS), ("Na₂HPO₄", 0.050, 2, PHOS), ("Na₃PO₄", 0.010, 3, PHOS),
                       ("NaHCO₃", 0.10, 1, CARB), ("Na₂CO₃", 0.050, 2, CARB)]:
    Ks = [mp.mpf(k) for k in K]

    def f(ph):
        h = mp.mpf(10) ** -ph
        terms = [mp.mpf(1)]
        for k in Ks:
            terms.append(terms[-1] * k / h)
        D = sum(terms)
        return h + na * C - sum(i * t for i, t in enumerate(terms)) / D * C - KW / h
    cases.append({"name": name, "C": C, "na": na, "Kas": K, "kt": ", ".join(f"{k:g}" for k in K), "ans": R(bisect(f))})
val("co-polyprotic-ph", "olympiad.equilibria", "What is the pH of {{C}} M {{name}}? Acid constants of the parent acid: Kₐ = {{kt}}.", "pH",
    "Write the charge balance with every species: [H⁺] + [Na⁺] = Σ (charge × fraction) C + [OH⁻]. Amphiprotic salts (H₂PO₄⁻, HPO₄²⁻, HCO₃⁻) sit near ½(pKₐₙ + pKₐₙ₊₁); fully deprotonated ones hydrolyse as bases. The reference solves the balance exactly",
    cases, "polyprotic_ph(C, na, Kas)", tol=0.003, pace="workout")

cases = []
for Ca, Cb, Ka, nH, V, name in [(0.10, 0.10, 1.75e-5, 0.0010, 0.100, "acetic acid/acetate"), (0.050, 0.10, 1.75e-5, 0.0020, 0.200, "acetic acid/acetate"),
                                (0.20, 0.15, 5.6e-10, 0.0050, 0.500, "NH₄⁺/NH₃"), (0.10, 0.10, 6.3e-8, 0.0030, 0.100, "H₂PO₄⁻/HPO₄²⁻")]:
    cHA, cA, cCl = Ca, Cb, nH / V
    Kam = mp.mpf(Ka)
    f = lambda ph: mp.mpf(10) ** -ph + cA - cCl - (cHA + cA) * Kam / (Kam + mp.mpf(10) ** -ph) - KW / mp.mpf(10) ** -ph  # noqa: E731
    cases.append({"Ca": Ca, "Cb": Cb, "Ka": Ka, "nH": nH, "V": V, "name": name, "ans": R(bisect(f))})
val("co-buffer-acid", "olympiad.equilibria", "{{V}} L of a {{name}} buffer holds {{Ca}} M acid and {{Cb}} M base (Kₐ = {{Ka}}). What is the pH after adding {{nH}} mol HCl (no volume change)?", "pH",
    "Strong acid converts base to acid mole for mole: then Henderson–Hasselbalch on the new amounts. The reference solves the full charge balance; the two agree to a few thousandths whenever both forms stay well above [H⁺]",
    cases, "buffer_after(Ca, Cb, Ka, nH, V)", tol=0.003)

cases = []
for pH in (7.0, 3.0, 2.0, 4.0, 1.0):
    Ksp, Ka = 3.9e-11, 6.8e-4
    h = 10 ** -pH
    s = (Ksp * (1 + h / Ka) ** 2 / 4) ** (1 / 3)
    cases.append({"pH": pH, "Ksp": Ksp, "Ka": Ka, "ans": R(s)})
val("co-solubility-ph", "olympiad.equilibria", "What is the molar solubility of CaF₂ (K_sp = {{Ksp}}) in a solution buffered at pH {{pH}}? Kₐ(HF) = {{Ka}}.", "s (M)",
    "Total fluoride 2s splits into F⁻ and HF: [F⁻] = 2s·Kₐ/(Kₐ + [H⁺]). Then s(2s·α_F)² = K_sp gives s = [K_sp(1 + [H⁺]/Kₐ)²/4]^⅓. Salts of weak acids dissolve more in acid",
    cases, "ksp_acid(Ksp, Ka, pH)", tol=0.001)

cases = []
for Kp, P in [(0.15, 1.0), (0.15, 0.10), (0.15, 10.0), (1.0, 1.0), (0.050, 2.0)]:
    cases.append({"Kp": Kp, "P": P, "ans": R(math.sqrt(Kp / (4 * P + Kp)))})
val("co-dissociation", "olympiad.equilibria", "N₂O₄ ⇌ 2NO₂ has K_p = {{Kp}} (bar). Pure N₂O₄ is held at a total pressure of {{P}} bar. What fraction dissociates at equilibrium?", "α",
    "Per mole N₂O₄: 1 − α and 2α, total 1 + α. Then K_p = 4α²P/(1 − α²), so α = √(K_p/(4P + K_p)). Lower pressure, more dissociation: Le Chatelier in numbers",
    cases, "n2o4_alpha(Kp, P)")

cases = []
for Kc, Tt, dn, rx in [(0.50, 400, -2, "N₂ + 3H₂ ⇌ 2NH₃"), (4.6e-3, 298, 1, "N₂O₄ ⇌ 2NO₂"), (1.0e-4, 1000, 1, "PCl₅ ⇌ PCl₃ + Cl₂"), (2.5, 500, -1, "2SO₂ + O₂ ⇌ 2SO₃")]:
    cases.append({"Kc": Kc, "Tt": Tt, "dn": dn, "rx": rx, "ans": R(Kc * (0.08314462618 * Tt) ** dn)})
val("co-kp-kc", "olympiad.equilibria", "For {{rx}}, K_c = {{Kc}} at {{Tt}} K (concentrations in mol/L). What is K_p (pressures in bar)?", "K_p",
    "p = cRT, so K_p = K_c(RT)^Δn with Δn = gas moles of products − reactants and R = 0.08314 L·bar/(mol·K). Δn = 0 makes them equal",
    cases, "kp_from_kc(Kc, Tt, dn)")

# ── 2. electrochemistry and thermochemistry ──────────────────────────────────
cases = []
RTF = 8.314462618 * 298.15 / 96485.33212
for name, E0, Ksp, n in [("AgCl(s) + e⁻ → Ag(s) + Cl⁻", 0.7996, 1.8e-10, 1), ("AgBr(s) + e⁻ → Ag(s) + Br⁻", 0.7996, 5.0e-13, 1),
                         ("AgI(s) + e⁻ → Ag(s) + I⁻", 0.7996, 8.3e-17, 1), ("Hg₂Cl₂(s) + 2e⁻ → 2Hg(l) + 2Cl⁻", 0.7973, 1.4e-18, 2)]:
    cases.append({"name": name, "E0": E0, "Ksp": Ksp, "n": n, "ans": R(E0 + RTF / n * math.log(Ksp))})
val("co-e-from-ksp", "olympiad.electrochem", "Find E° (V) for {{name}}, given E° of the metal-ion couple = {{E0}} V and K_sp = {{Ksp}} at 298 K.", "E° (V)",
    "Add the reactions and their ΔG° = −nFE°: the new couple is the ion couple plus dissolution, so E° = E°(Mⁿ⁺/M) + (RT/nF) ln K_sp. Insoluble salts make the metal easier to oxidise",
    cases, "e_from_ksp(E0, Ksp, n)")

cases = []
for w, I, x, M, n, what in [(0, 2.00, 3600, 63.546, 2, "copper from Cu²⁺"), (0, 0.500, 1800, 107.868, 1, "silver from Ag⁺"), (0, 10.0, 7200, 26.982, 3, "aluminium from Al³⁺"),
                            (1, 1.50, 5.00, 63.546, 2, "copper from Cu²⁺"), (1, 3.00, 2.00, 58.693, 2, "nickel from Ni²⁺")]:
    F = 96485.33212
    ans = I * x / F / n * M if w == 0 else x * n * F / (I * M)
    task = [f"How many grams are deposited by {I} A in {x} s?", f"How many seconds does {I} A take to deposit {x} g?"][w]
    cases.append({"w": w, "I": I, "q": x, "M": M, "n": n, "what": what, "task": task, "ans": R(ans)})
val("co-electrolysis", "olympiad.electrochem", "Electroplating {{what}} (M = {{M}} g/mol). {{task}}", "Answer",
    "Charge Q = It; moles of electrons Q/F; moles of metal Q/(nF). Faraday's laws are just electron bookkeeping: the same charge deposits more silver than copper",
    cases, "electrolysis(w, I, q, M, n)")

cases = []
for salt, sub, ie, hd, ea, form in [("NaCl", 107.3, [495.8], 121.7, [-348.6], -411.2), ("KBr", 89.0, [418.8], 111.9, [-324.5], -393.8),
                                    ("MgO", 147.1, [737.7, 1450.7], 249.2, [-141.0, 744.0], -601.6), ("CaCl₂ (2 Cl)", 177.8, [589.8, 1145.4], 2 * 121.7, [-2 * 348.6], -795.4)]:
    cases.append({"salt": salt, "sub": sub, "ie": ie, "hd": hd, "ea": ea, "form": form, "it": " + ".join(map(str, ie)), "et": " + ".join(map(str, ea)),
                  "ans": R(form - sub - sum(ie) - hd - sum(ea))})
val("co-born-haber", "olympiad.thermochem", "Born–Haber for {{salt}} (kJ/mol): ΔH_f = {{form}}, metal sublimation {{sub}}, ionisation {{it}}, non-metal atomisation {{hd}}, electron gain {{et}}. What is the lattice-formation enthalpy (gaseous ions → solid)?", "ΔH_latt (kJ/mol)",
    "Hess around the cycle: ΔH_f = sublimation + ionisation + atomisation + electron gain + lattice. The second electron gain of O is endothermic (+744), so MgO's huge lattice energy pays for it",
    cases, "born_haber(sub, ie, hd, ea, form)")

BE = "C-H:413,O=O:498,C=O:799,O-H:463,C-C:348,C=C:614,H-H:436,N≡N:945,N-H:391,C-O:358,Cl-Cl:242,C-Cl:328,H-Cl:431"
cases = []
for rx, broken, formed in [("CH₄ + 2O₂ → CO₂ + 2H₂O", "C-H*4,O=O*2", "C=O*2,O-H*4"), ("C₂H₄ + H₂ → C₂H₆", "C=C*1,H-H*1", "C-C*1,C-H*2"),
                           ("N₂ + 3H₂ → 2NH₃", "N≡N*1,H-H*3", "N-H*6"), ("CH₄ + Cl₂ → CH₃Cl + HCl", "C-H*1,Cl-Cl*1", "C-Cl*1,H-Cl*1"),
                           ("C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O", "C-H*5,C-C*1,C-O*1,O-H*1,O=O*3", "C=O*4,O-H*6")]:
    tab = dict((k, float(v)) for k, v in (x.split(":") for x in BE.split(",")))
    tot = lambda s: sum(int(n) * tab[b] for b, n in (x.split("*") for x in s.split(",")))  # noqa: E731
    cases.append({"rx": rx, "br": broken, "fo": formed, "tab": BE, "ans": R(tot(broken) - tot(formed))})
val("co-bond-enthalpy", "olympiad.thermochem", "Estimate ΔH (kJ/mol) for {{rx}} (gas phase) from mean bond enthalpies (kJ/mol): C–H 413, O=O 498, C=O 799 (in CO₂), O–H 463, C–C 348, C=C 614, H–H 436, N≡N 945, N–H 391, C–O 358, Cl–Cl 242, C–Cl 328, H–Cl 431.", "ΔH (kJ/mol)",
    "ΔH ≈ Σ(bonds broken) − Σ(bonds formed). Mean values are averages over many molecules, so expect errors of a few percent, and none at all for phase changes (it assumes gases)",
    cases, "bond_enthalpy(br, fo, tab)")

# ── 3. kinetics and nuclear ──────────────────────────────────────────────────
cases = []
for order, k, C0, C in [(0, 0.010, 1.0, 0.25), (1, 0.050, 1.0, 0.10), (2, 0.50, 0.20, 0.050), (2, 0.020, 1.0, 0.10), (1, 1.2e-3, 0.50, 0.40)]:
    t = (C0 - C) / k if order == 0 else (math.log(C0 / C) / k if order == 1 else (1 / C - 1 / C0) / k)
    cases.append({"order": order, "k": k, "C0": C0, "Cc": C, "ans": R(t)})
val("co-integrated-rate", "olympiad.kinetics", "A reaction of order {{order}} in A has k = {{k}} (mol/L and s units). How long (s) does [A] take to fall from {{C0}} to {{Cc}} M?", "t (s)",
    "Integrate: zero order [A]₀ − [A] = kt; first order ln([A]₀/[A]) = kt; second order 1/[A] − 1/[A]₀ = kt. Second-order half-lives double each time; first-order ones stay fixed",
    cases, "rate_time(order, k, C0, Cc)")

cases = []
for N0, t1, t2, t, name in [(1e6, 10.0, 1.0, 5.0, "parent t½ = 10 h, daughter t½ = 1 h"), (1e6, 1.0, 10.0, 2.0, "parent t½ = 1 h, daughter t½ = 10 h"),
                            (1e9, 12.7, 2.24, 24.0, "⁹⁹Mo (t½ 66 h ≈ 2.75 d scaled) model: parent 12.7 h, daughter 2.24 h"), (5e5, 8.0, 4.0, 8.0, "parent t½ = 8 d, daughter t½ = 4 d")]:
    l1, l2 = math.log(2) / t1, math.log(2) / t2
    D = N0 * l1 / (l2 - l1) * (math.exp(-l1 * t) - math.exp(-l2 * t))
    cases.append({"N0": N0, "t1": t1, "t2": t2, "t": t, "name": name, "ans": R(D)})
for c in cases:
    if "Mo" in c["name"]:
        c["name"] = "parent t½ = 12.7 h, daughter t½ = 2.24 h"
val("co-decay-chain", "olympiad.kinetics", "A pure sample of {{N0}} parent atoms decays to a radioactive daughter ({{name}}), which decays to a stable product. How many daughter atoms are present after {{t}} (same time units)?", "N_D",
    "Bateman: $N_D = N_0\\dfrac{\\lambda_1}{\\lambda_2 - \\lambda_1}(e^{-\\lambda_1t} - e^{-\\lambda_2t})$. A short-lived daughter of a long-lived parent settles into transient or secular equilibrium (the basis of the ⁹⁹Mo/⁹⁹ᵐTc generator)",
    cases, "daughter_atoms(N0, t1, t2, t)")

# ── 4. solutions and spectra ─────────────────────────────────────────────────
cases = []
for dT, Kf, m, nu, name in [(0.200, 1.86, 0.100, 2, "a weak 1:1 acid HA"), (0.0217, 1.86, 0.0100, 2, "acetic acid"), (0.500, 1.86, 0.100, 3, "a 1:2 salt MX₂"), (0.335, 1.86, 0.100, 2, "a 1:1 salt")]:
    i = dT / (Kf * m)
    cases.append({"dT": dT, "Kf": Kf, "m": m, "nu": nu, "name": name, "ans": R((i - 1) / (nu - 1))})
val("co-vant-hoff", "olympiad.solutions", "A {{m}} mol/kg aqueous solution of {{name}} (ν = {{nu}} ions per formula unit when fully dissociated) freezes {{dT}} K below pure water (K_f = {{Kf}} K kg/mol). What is the degree of dissociation α?", "α",
    "ΔT_f = iK_f m gives i; then i = 1 + α(ν − 1). Strong electrolytes still show α < 1 at moderate concentration because ions pair, not because they fail to dissociate",
    cases, "vant_hoff_alpha(dT, Kf, m, nu)")

cases = []
for el, n, k in [("Cl", 1, 1), ("Cl", 2, 1), ("Cl", 2, 2), ("Br", 1, 1), ("Br", 2, 1), ("Cl", 3, 1)]:
    iso = {"Cl": (0.7576, 0.2424), "Br": (0.5069, 0.4931)}[el]
    ratio = math.comb(n, k) * (iso[1] / iso[0]) ** k
    cases.append({"el": el, "n": n, "k": k, "pk": f"M+{2 * k}", "ans": R(ratio)})
val("co-isotope-pattern", "olympiad.spectro", "A molecule contains {{n}} {{el}} atom(s) (³⁵Cl 75.76%, ³⁷Cl 24.24%; ⁷⁹Br 50.69%, ⁸¹Br 49.31%). What is the intensity of the {{pk}} peak relative to M?", "Ratio",
    "Peaks follow the binomial expansion of (a + b)ⁿ: M+2k relative to M is C(n,k)(b/a)ᵏ. One Cl gives 3:1, one Br 1:1, two Br 1:2:1 — patterns that identify halogens at a glance",
    cases, "isotope_ratio(el, n, k)")

cases = []
for n1, n2, eq, text, ans in [(3, 0, 0, "a CH₂ next to a CH₃ only", 4), (2, 3, 1, "a CH₂ between a CH₂ and a CH₃, equal J", 6), (2, 3, 0, "a CH₂ between a CH₂ and a CH₃, different J", 12),
                              (6, 0, 0, "the CH of an isopropyl group", 7), (1, 2, 0, "a vinyl H coupled to one H (J = 7) and two others (J = 3)", 6), (2, 2, 1, "a CH₂ between two CH₂ groups, equal J", 5)]:
    cases.append({"n1": n1, "n2": n2, "eq": eq, "text": text, "ans": ans})
val("co-nmr-multiplicity", "olympiad.spectro", "How many lines (first-order ¹H NMR) does {{text}} show?", "Lines",
    "n equivalent neighbours give n + 1 lines; two different sets give (n + 1)(m + 1) when their J differ, collapsing toward n + m + 1 when the J are equal",
    cases, "multiplet_lines(n1, n2, eq)", pace="recall")

yaml.safe_dump(T, open(OUT, "w"), allow_unicode=True, sort_keys=False, width=200)
print(len(T), "templates,", sum(len(t["cases"]) for t in T), "cases ->", OUT)
