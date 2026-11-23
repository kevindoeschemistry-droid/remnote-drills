"""Builds drills/problems/re-depth.yaml: Chemical Reaction Engineering past the isothermal liquid
basics (framework reaction-engineering, RE), on Fogler 5e chapters 3–18. Run: python3 scripts/re_cases.py

Answers follow the closed forms each card teaches (ε-corrected design equations, (1 − αW)^½,
(k1/k2)^(k2/(k2 − k1)), τ_opt = 1/√(k1k2), Michaelis–Menten, the adiabatic energy-balance line,
η = (3/φ²)(φ coth φ − 1), Danckwerts' closed form…). tests/verify/recalc.py checks each by another
route: mole tables, ODE integration, PSSH solves, dsolve on the BVPs, root counting.
"""
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/re-depth.yaml"
R = mp.mpf("8.314462618")
T = []


def F(v):
    return float(mp.nstr(mp.mpf(v), 12))


def sig(v, n=4):
    """round for display; the answer is then computed from the rounded number"""
    return float(mp.nstr(mp.mpf(v), n))


def val(name, skill, prompt, ask, explain, cases, verify, tol=0.0001, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(name, skill, prompt, options, explain, cases, verify=None, pace="recall"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}],
              "verify": {"choices": {"y": verify}} if verify else {"authored": True}})


M = mp.mpf

# ── 1. Rates, stoichiometry, rate data (Fogler 3, 4, 7) ─────────────────────
cases = []
for rx, a, co, sp_, verb, rA in [("2A + B → 3C", 2, 3, "C", "formed", 0.6), ("2A + B → 3C", 2, 1, "B", "consumed", 0.6),
                                 ("A + 3B → 2C", 1, 2, "C", "formed", 1.5), ("A + 3B → 2C", 1, 3, "B", "consumed", 0.4),
                                 ("3A → 2B + D", 3, 2, "B", "formed", 0.9), ("3A → 2B + D", 3, 1, "D", "formed", 1.2)]:
    cases.append({"rx": rx, "a": a, "co": co, "sp": sp_, "verb": verb, "rA": rA, "ans": F(M(co) / a * M(str(rA)))})
val("re-relative-rates", "cre.stoichiometry", "For {{rx}}, A is consumed at ${{rA}}$ mol/(L·s). At what rate is {{sp}} {{verb}}, in mol/(L·s)?", "Rate",
    "Divide each rate by its stoichiometric coefficient and they are all equal: $\\dfrac{-r_A}{a} = \\dfrac{-r_B}{b} = \\dfrac{r_C}{c}$. So the rate for {{sp}} is ${{co}}/{{a}}$ of the rate for A",
    cases, "nsimplify(co)/nsimplify(a)*nsimplify(rA)", pace="recall")

cases = []
for K in (1, 3, 0.5, 9):
    cases.append({"kind": 0, "rx": "A ⇌ B", "K": K, "ku": "", "CA0": 1, "feed": "Pure A is fed.", "ans": F(M(str(K)) / (1 + M(str(K))))})
for K, C0 in [(2, 1), (10, 0.5), (0.5, 2), (4, 1)]:
    k = M(str(K)) * M(str(C0))
    cases.append({"kind": 1, "rx": "A + B ⇌ C", "K": K, "ku": " L/mol", "CA0": C0, "feed": f"A and B are fed equimolar at $C_{{A0}} = {C0}$ mol/L.",
                  "ans": F(((2 * k + 1) - mp.sqrt(4 * k + 1)) / (2 * k))})
val("re-equil-conversion", "cre.rate-laws", "The liquid reaction {{rx}} has $K_C = {{K}}${{ku}}. {{feed}} What is the equilibrium conversion of A?", "X_e",
    "Write every concentration in terms of X from the stoichiometric table, set the rate to zero (or $K_C$ = products over reactants) and solve. For A ⇌ B, $X_e = K/(1 + K)$; for A + B ⇌ C from an equimolar feed, $K_C C_{A0}(1 - X)^2 = X$, a quadratic whose root below 1 is the answer. No reactor can beat $X_e$",
    cases, "eq_X(kind, K, CA0)")

cases = []
for rx, a, dn, yA0, feed in [("A → 2B", 1, 1, 1, "pure A"), ("A → 3B", 1, 2, 0.5, "half A, half inert"), ("2A → B", 2, -1, 0.8, "80% A, 20% inert"),
                             ("A + B → C", 1, -1, 0.5, "A and B equimolar, no inert"), ("A → B + C", 1, 1, 0.25, "25% A, 75% inert"), ("N₂ + 3H₂ → 2NH₃ (A = N₂)", 1, -2, 0.25, "stoichiometric N₂ and H₂")]:
    cases.append({"rx": rx, "a": a, "dn": dn, "yA0": yA0, "feed": feed, "ans": F(M(str(yA0)) * dn / a)})
val("re-epsilon", "cre.stoichiometry", "The gas-phase reaction {{rx}} is fed as {{feed}}. What is $\\varepsilon$, the fractional change in total moles at complete conversion of A?", "ε",
    "$\\varepsilon = y_{A0}\\,\\delta$, with $\\delta$ = (moles of gas formed − moles of gas consumed) per mole of A. Inerts dilute the change, so they shrink $|\\varepsilon|$. A negative $\\varepsilon$ means the gas contracts and the reactor holds A longer",
    cases, "nsimplify(yA0)*nsimplify(dn)/nsimplify(a)", pace="recall")

cases = []
for rx, a, dn, yA0, feed, CA0, X, Pr, T0, T1 in [("A → 2B", 1, 1, 1, "pure A", 0.2, 0.5, 1, 500, 500), ("A → 2B", 1, 1, 0.5, "50% A in inert", 0.1, 0.6, 0.8, 500, 500),
                                                ("2A → B", 2, -1, 1, "pure A", 0.3, 0.5, 1, 400, 450), ("A + B → C", 1, -1, 0.5, "equimolar A and B", 0.25, 0.8, 0.9, 600, 600),
                                                ("A → B + C", 1, 1, 0.4, "40% A in inert", 0.08, 0.75, 0.7, 450, 500)]:
    eps = M(str(yA0)) * dn / a
    v = M(str(CA0)) * (1 - M(str(X))) / (1 + eps * M(str(X))) * M(str(Pr)) * M(T0) / M(T1)
    cases.append({"rx": rx, "a": a, "dn": dn, "yA0": yA0, "feed": feed, "CA0": CA0, "X": X, "Pr": Pr, "T0": T0, "T1": T1, "ans": F(v)})
val("re-gas-conc", "cre.stoichiometry", "The gas-phase reaction {{rx}} is fed as {{feed}} with $C_{A0} = {{CA0}}$ mol/L at ${{T0}}$ K. At $X = {{X}}$ the pressure is ${{Pr}}P_0$ and the temperature ${{T1}}$ K. What is $C_A$ (mol/L)?", "C_A",
    "$C_A = C_{A0}\\dfrac{1 - X}{1 + \\varepsilon X}\\dfrac{P}{P_0}\\dfrac{T_0}{T}$, $\\varepsilon = y_{A0}\\delta$. The volumetric flow grows with moles and temperature and shrinks with pressure, and C_A is moles over that flow",
    cases, "gas_CA(CA0, yA0, a, dn, X, Pr, T0, T1)")

cases = []
ts = [0, 5, 10, 15, 20, 30]
for n, k in [(0, 0.05), (0, 0.06), (1, 0.05), (1, 0.08), (2, 0.05), (2, 0.1), (1, 0.04), (2, 0.07)]:
    C0 = M(2)
    Cs = [sig([C0 - k * t, C0 * mp.exp(-k * t), C0 / (1 + k * C0 * t)][n]) for t in ts]
    cases.append({"tt": ", ".join(map(str, ts)), "cc": ", ".join(str(c) for c in Cs), "ts": ts, "Cs": Cs, "ans": n})
pick("re-integral-plot", "cre.rate-data", "A batch run gives $t$ (min): {{tt}} and $C_A$ (mol/L): {{cc}}. Which plot is a straight line?",
     ["C_A against t (zero order)", "ln C_A against t (first order)", "1/C_A against t (second order)"],
     "Integral method: guess the order, linearise, test. Zero order loses equal amounts per time; first order loses equal fractions per time (check $C_{i+1}/C_i$ over equal steps); second order gains equal amounts of $1/C$. The slope of the straight plot is $-k$, $-k$ or $+k$",
     cases, "plot_order(ts, Cs)", pace="quick")

cases = []
for n, k, C1, C2 in [(2, 0.1, 1, 2), (0, 0.02, 1, 0.5), (3, 0.05, 1, 2), (0.5, 0.1, 1, 4), (2, 0.5, 0.2, 0.8)]:
    th = lambda C: (M(2) ** (n - 1) - 1) / ((n - 1) * k * M(str(C)) ** (n - 1)) if n != 1 else mp.log(2) / k  # noqa: E731
    t1, t2 = sig(th(C1)), sig(th(C2))
    cases.append({"C1": C1, "C2": C2, "t1": t1, "t2": t2, "ans": F(1 - mp.log(M(str(t2)) / M(str(t1))) / mp.log(M(str(C2)) / M(str(C1))))})
val("re-half-life-order", "cre.rate-data", "Starting at $C_{A0} = {{C1}}$ mol/L the half-life is ${{t1}}$ min; starting at ${{C2}}$ mol/L it is ${{t2}}$ min. What is the reaction order?", "Order n",
    "For order $n$, $t_{1/2} \\propto C_{A0}^{\\,1 - n}$, so $n = 1 - \\dfrac{\\ln(t_2/t_1)}{\\ln(C_2/C_1)}$. A half-life that shortens as you start higher means $n > 1$; one that does not change means first order",
    cases, "1 - power_exponent(nsimplify(t2)/nsimplify(t1), nsimplify(C2)/nsimplify(C1))", tol=0.005)

cases = []
for m, nb, CA1, CB1, CA2, CB2, k in [(1, 2, 0.1, 0.1, 0.2, 0.2, 5), (2, 1, 0.5, 0.5, 1.0, 0.25, 0.4), (1, 0, 0.2, 0.1, 0.4, 0.3, 2), (1, 0.5, 0.1, 0.1, 0.3, 0.4, 3), (2, 2, 0.1, 0.2, 0.05, 0.4, 10)]:
    r1 = sig(k * M(str(CA1)) ** m * M(str(CB1)) ** nb)
    r2 = sig(k * M(str(CA2)) ** m * M(str(CB2)) ** nb)
    cases.append({"m": m, "CA1": CA1, "CB1": CB1, "CA2": CA2, "CB2": CB2, "r1": r1, "r2": r2,
                  "ans": F(mp.log(M(str(r2)) / M(str(r1)) / (M(str(CA2)) / M(str(CA1))) ** m) / mp.log(M(str(CB2)) / M(str(CB1))))})
val("re-initial-rates", "cre.rate-data", "The rate is order ${{m}}$ in A. Initial rates: ${{r1}}$ mol/(L·s) at $C_A = {{CA1}}$, $C_B = {{CB1}}$; ${{r2}}$ at $C_A = {{CA2}}$, $C_B = {{CB2}}$ (mol/L). What is the order in B?", "Order in B",
    "Divide the two rate laws: $\\dfrac{r_2}{r_1} = \\left(\\dfrac{C_{A2}}{C_{A1}}\\right)^{m}\\left(\\dfrac{C_{B2}}{C_{B1}}\\right)^{n}$. Take out the A factor you already know, then $n$ is a log ratio. Both concentrations changed, so the A factor cannot be ignored",
    cases, "power_exponent(nsimplify(r2)/nsimplify(r1)/(nsimplify(CA2)/nsimplify(CA1))**m, nsimplify(CB2)/nsimplify(CB1))", tol=0.005)

# ── 2. Isothermal reactors (Fogler 5, 6) ────────────────────────────────────
cases = []
for k, C0, tau in [(0.5, 2, 5), (0.1, 1, 10), (2, 0.5, 4), (0.05, 2, 20), (1, 1, 1)]:
    Da = M(str(k)) * M(str(C0)) * M(str(tau))
    cases.append({"k": k, "CA0": C0, "tau": tau, "ans": F((1 + 2 * Da - mp.sqrt(1 + 4 * Da)) / (2 * Da))})
val("re-cstr-second-order", "cre.cstr", "A liquid second-order reaction, $-r_A = kC_A^2$ with $k = {{k}}$ L/(mol·min), runs in a CSTR with $C_{A0} = {{CA0}}$ mol/L and $\\tau = {{tau}}$ min. What is the conversion?", "X",
    "Mole balance with the rate at exit conditions: $\\tau k C_{A0} = \\dfrac{X}{(1 - X)^2}$. With $Da = \\tau k C_{A0}$, $X = \\dfrac{1 + 2Da - \\sqrt{1 + 4Da}}{2Da}$. Take the root below 1",
    cases, "cstr_X(2, nsimplify(k)*nsimplify(CA0)*nsimplify(tau))")

cases = []
for n, rx, feed, eps, k, v0, C0, X in [(1, "A → 2B", "pure A", 1, 0.2, 10, 0.1, 0.8), (1, "A → 3B", "half A, half inert", 1, 0.5, 5, 0.05, 0.9),
                                      (1, "2A → B", "pure A", -0.5, 0.1, 20, 0.2, 0.7), (2, "A → 2B", "pure A", 1, 2, 10, 0.1, 0.8),
                                      (2, "A + B → C", "equimolar A and B (rate $kC_A^2$)", -0.5, 5, 4, 0.1, 0.6), (1, "A → B + C", "25% A, 75% inert", 0.25, 0.3, 6, 0.05, 0.95)]:
    e, Xm = M(str(eps)), M(str(X))
    if n == 1:
        V = M(v0) / M(str(k)) * ((1 + e) * mp.log(1 / (1 - Xm)) - e * Xm)
    else:
        V = M(v0) / (M(str(k)) * M(str(C0))) * (2 * e * (1 + e) * mp.log(1 - Xm) + e**2 * Xm + (1 + e) ** 2 * Xm / (1 - Xm))
    cases.append({"n": n, "rx": rx, "feed": feed, "eps": eps, "k": k, "v0": v0, "CA0": C0, "X": X, "ku": ["min⁻¹", "L/(mol·min)"][n - 1], "ans": F(V)})
val("re-pfr-gas-eps", "cre.pfr", "The isothermal gas-phase reaction {{rx}}, $-r_A = kC_A^{ {{n}} }$ with $k = {{k}}$ {{ku}}, is fed as {{feed}} at $v_0 = {{v0}}$ L/min, $C_{A0} = {{CA0}}$ mol/L, no pressure drop. What PFR volume (L) reaches $X = {{X}}$?", "V (L)",
    "$V = F_{A0}\\int_0^X \\dfrac{dX}{-r_A}$ with $C_A = C_{A0}\\dfrac{1 - X}{1 + \\varepsilon X}$. First order: $V = \\dfrac{v_0}{k}\\left[(1 + \\varepsilon)\\ln\\dfrac1{1 - X} - \\varepsilon X\\right]$. Second order: $V = \\dfrac{v_0}{kC_{A0}}\\left[2\\varepsilon(1 + \\varepsilon)\\ln(1 - X) + \\varepsilon^2X + \\dfrac{(1 + \\varepsilon)^2X}{1 - X}\\right]$. Expansion ($\\varepsilon > 0$) speeds the gas through, so it needs more volume",
    cases, "pfr_V(n, k, v0, CA0, eps, X)", tol=0.0002, pace="workout")

cases = []
for k, v0, X1, X2 in [(0.2, 10, 0.5, 0.9), (0.1, 5, 0.6, 0.95), (1, 2, 0.3, 0.8), (0.5, 20, 0.7, 0.9)]:
    V = M(v0) / M(str(k)) * (M(str(X1)) / (1 - M(str(X1))) + mp.log((1 - M(str(X1))) / (1 - M(str(X2)))))
    cases.append({"k": k, "v0": v0, "X1": X1, "X2": X2, "ans": F(V)})
val("re-cstr-then-pfr", "cre.pfr", "A liquid first-order reaction ($k = {{k}}$ min⁻¹, $v_0 = {{v0}}$ L/min) runs in a CSTR to $X = {{X1}}$, then in a PFR to $X = {{X2}}$. What is the total volume (L)?", "V total (L)",
    "Size each reactor on the Levenspiel plot $F_{A0}/(-r_A) = \\dfrac{v_0}{k(1 - X)}$: the CSTR is the rectangle $\\dfrac{v_0X_1}{k(1 - X_1)}$, the PFR the area $\\dfrac{v_0}{k}\\ln\\dfrac{1 - X_1}{1 - X_2}$. For positive-order kinetics, put the PFR first if you are free to choose",
    cases, "cstr_pfr_V(k, v0, X1, X2)")

cases = []
for w in (0, 1):
    for k, v0, al, W in [(0.5, 10, 0.004, 100), (0.2, 5, 0.002, 300), (1, 20, 0.01, 60), (0.3, 4, 0.0005, 1000)]:
        aw = M(str(al)) * W
        y = mp.sqrt(1 - aw)
        X = 1 - mp.exp(-M(str(k)) / v0 * 2 / (3 * M(str(al))) * (1 - (1 - aw) ** M(1.5)))
        cases.append({"w": w, "wt": ["pressure ratio $y = P/P_0$", "conversion"][w], "k": k, "v0": v0, "al": al, "W": W, "ans": F([y, X][w])})
val("re-pbr-pressure-drop", "cre.pbr", "A first-order gas reaction with no change in moles ($\\varepsilon = 0$), $k' = {{k}}$ L/(kg·min), runs isothermally in a packed bed with $v_0 = {{v0}}$ L/min and pressure-drop parameter $\\alpha = {{al}}$ kg⁻¹. What is the {{wt}} after $W = {{W}}$ kg of catalyst?", "Value",
    "With $\\varepsilon = 0$ the Ergun equation integrates to $y = (1 - \\alpha W)^{1/2}$. Then $\\dfrac{dX}{dW} = \\dfrac{k'}{v_0}(1 - X)y$, so $\\ln\\dfrac1{1 - X} = \\dfrac{k'}{v_0}\\dfrac{2}{3\\alpha}\\left[1 - (1 - \\alpha W)^{3/2}\\right]$. Falling pressure lowers $C_A$, so the bed converts less than it would without the drop",
    cases, "pbr(w, k, v0, al, W)", pace="workout")

cases = []
for tau, k, fr in [(10, 0.1, 0.99), (5, 0.5, 0.99), (20, 0.05, 0.95), (2, 1, 0.99), (8, 0.25, 0.9)]:
    cases.append({"tau": tau, "k": k, "fr": fr, "pc": int(fr * 100), "ans": F(M(tau) * mp.log(1 / (1 - M(str(fr)))) / (1 + M(tau) * M(str(k))))})
val("re-cstr-startup", "cre.cstr", "A CSTR full of solvent starts receiving feed. The reaction is first order with $k = {{k}}$ min⁻¹ and $\\tau = {{tau}}$ min. How long (min) until the exit $C_A$ reaches {{pc}}% of its steady value?", "t (min)",
    "Unsteady balance: $\\dfrac{dC_A}{dt} = \\dfrac{C_{A0} - C_A}{\\tau} - kC_A$, so $C_A = C_{As}\\left[1 - e^{-(1 + \\tau k)t/\\tau}\\right]$ and $t = \\dfrac{\\tau}{1 + \\tau k}\\ln\\dfrac{1}{1 - f}$. For 99% that is about $4.6\\tau/(1 + \\tau k)$: reaction shortens the start-up",
    cases, "cstr_startup(tau, k, fr)")

# ── 3. Multiple reactions (Fogler 8) ────────────────────────────────────────
cases = []
for k1, k2, C0 in [(0.5, 0.1, 2), (0.2, 0.4, 1), (1, 0.25, 1.5), (0.1, 0.05, 1), (0.3, 0.9, 2)]:
    cases.append({"k1": k1, "k2": k2, "CA0": C0, "ans": F(M(str(C0)) * (M(str(k1)) / M(str(k2))) ** (M(str(k2)) / (M(str(k2)) - M(str(k1)))))})
val("re-series-bmax", "cre.multiple", "In a batch reactor A → B → C, both steps first order with $k_1 = {{k1}}$ and $k_2 = {{k2}}$ min⁻¹, starting from pure A at ${{CA0}}$ mol/L. What is the highest $C_B$ reached (mol/L)?", "C_B,max",
    "$C_B = \\dfrac{k_1C_{A0}}{k_2 - k_1}(e^{-k_1t} - e^{-k_2t})$ peaks at $t = \\dfrac{\\ln(k_2/k_1)}{k_2 - k_1}$, where $\\dfrac{C_{B,\\max}}{C_{A0}} = \\left(\\dfrac{k_1}{k_2}\\right)^{k_2/(k_2 - k_1)}$. A slow second step lets B pile up",
    cases, "nsimplify(CA0)*series_cb_max(k1, k2)", tol=0.0002)

cases = []
for w in (0, 1):
    for k1, k2, C0 in [(0.5, 0.1, 2), (0.2, 0.4, 1), (1, 0.25, 1.5), (0.1, 0.05, 1)]:
        tau = 1 / mp.sqrt(M(str(k1)) * M(str(k2)))
        cb = M(str(C0)) * M(str(k1)) * tau / ((1 + M(str(k1)) * tau) * (1 + M(str(k2)) * tau))
        cases.append({"w": w, "wt": ["space time (min) that maximises $C_B$", "largest exit $C_B$ (mol/L)"][w], "k1": k1, "k2": k2, "CA0": C0, "ans": F([tau, cb][w])})
val("re-cstr-series-opt", "cre.multiple", "A → B → C runs in one CSTR, both steps first order, $k_1 = {{k1}}$, $k_2 = {{k2}}$ min⁻¹, pure A fed at ${{CA0}}$ mol/L. What is the {{wt}}?", "Value",
    "Balances at exit: $C_A = \\dfrac{C_{A0}}{1 + k_1\\tau}$, $C_B = \\dfrac{k_1\\tau C_{A0}}{(1 + k_1\\tau)(1 + k_2\\tau)}$. Setting $dC_B/d\\tau = 0$ gives $\\tau_{\\rm opt} = 1/\\sqrt{k_1k_2}$. A CSTR always gives less B than a batch or PFR with the same rate constants",
    cases, "[cstr_series(0, k1, k2), nsimplify(CA0)*cstr_series(1, k1, k2)][w]")

cases = []
for kind in (0, 1):
    for k1, a1, k2, a2, C0, X in [(1, 1, 0.5, 2, 2, 0.8), (0.2, 2, 1, 1, 1, 0.6), (2, 1, 1, 0.5, 1, 0.9), (0.5, 2, 0.5, 1, 2, 0.75)]:
        phi = lambda C: k1 * C**a1 / (k1 * C**a1 + k2 * C**a2)  # noqa: E731
        CA = M(str(C0)) * (1 - M(str(X)))
        CD = (M(str(C0)) - CA) * phi(CA) if kind == 0 else mp.quad(phi, [CA, M(str(C0))])
        cases.append({"kind": kind, "rt": ["one CSTR", "a PFR"][kind], "k1": k1, "a1": a1, "k2": k2, "a2": a2, "CA0": C0, "X": X, "ans": F(CD)})
val("re-parallel-overall", "cre.multiple", "Parallel liquid reactions A → D ($r_D = {{k1}}\\,C_A^{ {{a1}} }$) and A → U ($r_U = {{k2}}\\,C_A^{ {{a2}} }$) run in {{rt}} fed pure A at ${{CA0}}$ mol/L to $X = {{X}}$. What is the exit $C_D$ (mol/L)?", "C_D",
    "The instantaneous yield is $\\phi = \\dfrac{r_D}{r_D + r_U}$. A CSTR runs entirely at exit $C_A$, so $C_D = (C_{A0} - C_A)\\,\\phi(C_A)$. A PFR passes through every concentration, so $C_D = \\int_{C_A}^{C_{A0}}\\phi\\,dC_A$. Whichever reaction has the higher order favours high concentration (PFR); the lower order favours the CSTR",
    cases, "parallel_overall(kind, k1, a1, k2, a2, CA0, X)", tol=0.0002, pace="workout")

# ── 4. Catalysis (Fogler 10) ────────────────────────────────────────────────
cases = []
for kind, k, KA, PA, KB, PB in [(0, 0.5, 2, 1, 1, 0.5), (0, 2, 0.5, 4, 3, 1), (1, 1, 1, 2, 2, 1), (1, 0.8, 3, 0.5, 0.5, 2), (0, 1, 10, 2, 0, 0), (1, 5, 0.2, 3, 1, 0.5)]:
    th = 1 / (1 + M(str(KA)) * M(str(PA)) + M(str(KB)) * M(str(PB)))
    r = M(str(k)) * M(str(KA)) * M(str(PA)) * th * (th if kind else 1)
    cases.append({"kind": kind, "mech": ["adsorbed A reacting on its own site (single site)", "adsorbed A reacting with an adjacent vacant site (dual site)"][kind],
                  "k": k, "KA": KA, "PA": PA, "KB": KB, "PB": PB, "ans": F(r)})
val("re-lh-rate", "cre.catalysis", "A surface reaction is rate-limiting, with {{mech}}. $k = {{k}}$ mol/(kg·s), $K_A = {{KA}}$ and $K_B = {{KB}}$ atm⁻¹; $P_A = {{PA}}$ and $P_B = {{PB}}$ atm. What is $-r'_A$ (mol/(kg·s))?", "−r′_A",
    "Adsorption steps at equilibrium give $\\theta_A = K_AP_A\\theta_v$, $\\theta_B = K_BP_B\\theta_v$, and the site balance gives $\\theta_v = \\dfrac{1}{1 + K_AP_A + K_BP_B}$. Single site: $-r' = kK_AP_A\\theta_v$. Dual site: $-r' = kK_AP_A\\theta_v^2$, the squared denominator. Adsorbed product B only slows the rate",
    cases, "lh_rate(kind, k, KA, PA, KB, PB)")

cases = [{"law": "\\dfrac{k(P_A - P_B/K_P)}{1 + K_BP_B}", "ans": 0}, {"law": "\\dfrac{k(P_A - P_B/K_P)}{1 + K_AP_A + K_BP_B}", "ans": 1},
         {"law": "\\dfrac{k(P_A - P_B/K_P)}{1 + K'P_A}", "ans": 2}, {"law": "\\dfrac{kP_A}{1 + K_AP_A + K_BP_B}", "ans": 1}]
pick("re-rls-pick", "cre.catalysis", "For A ⇌ B on a catalyst (adsorb A, react on the surface, desorb B), the measured rate fits $-r'_A = {{law}}$. Which step limits the rate?",
     ["Adsorption of A", "Surface reaction", "Desorption of B"],
     "Read the denominator: it holds a term for every species adsorbed in equilibrium. If adsorption of A is slow, A·S is not in equilibrium with gas A, so $P_A$ drops out of the denominator. If desorption of B is slow, B·S is set by A's equilibria and the denominator shows only $P_A$. A surface-reaction limit keeps both $K_AP_A$ and $K_BP_B$",
     cases)

# ── 5. Mechanisms and bioreactions (Fogler 9) ───────────────────────────────
cases = []
for k1, k2, k3, Cc in [(2, 5, 1, 0.5), (1, 1, 10, 2), (0.5, 4, 0.2, 1), (3, 2, 2, 0.1)]:
    cases.append({"k1": k1, "k2": k2, "k3": k3, "Cc": Cc, "ans": F(M(str(k1)) * M(str(k3)) * M(str(Cc)) ** 2 / (M(str(k2)) * M(str(Cc)) + M(str(k3))))})
val("re-lindemann", "cre.mechanisms", "Gas A decomposes by A + A → A* + A ($k_1 = {{k1}}$), A* + A → A + A ($k_2 = {{k2}}$), A* → products ($k_3 = {{k3}}$), concentrations in mol/L and time in s. With the PSSH on A*, what is the rate of formation of products at $C_A = {{Cc}}$ mol/L?", "Rate (mol/(L·s))",
    "PSSH: $k_1C_A^2 - k_2C_AC_{A^*} - k_3C_{A^*} = 0$, so $C_{A^*} = \\dfrac{k_1C_A^2}{k_2C_A + k_3}$ and $r_P = k_3C_{A^*} = \\dfrac{k_1k_3C_A^2}{k_2C_A + k_3}$. The active intermediate never appears in the final law",
    cases, "lind_rate(k1, k2, k3, Cc)")
cases = [{"k1": 1, "k2": 10, "k3": 0.01, "Cc": 5, "ans": 1}, {"k1": 1, "k2": 10, "k3": 100, "Cc": 0.01, "ans": 2},
         {"k1": 2, "k2": 1, "k3": 1000, "Cc": 0.05, "ans": 2}, {"k1": 2, "k2": 50, "k3": 0.1, "Cc": 10, "ans": 1}]
pick("re-lindemann-order", "cre.mechanisms", "With $r = \\dfrac{k_1k_3C_A^2}{k_2C_A + k_3}$, $k_2 = {{k2}}$ L/(mol·s), $k_3 = {{k3}}$ s⁻¹, what is the apparent order at $C_A = {{Cc}}$ mol/L?",
     ["Zero order", "First order", "Second order"],
     "Compare $k_2C_A$ with $k_3$. High concentration ($k_2C_A \\gg k_3$): deactivation by collision wins and $r \\to (k_1k_3/k_2)C_A$, first order. Low concentration: $r \\to k_1C_A^2$, second order. This is why unimolecular gas reactions fall off at low pressure",
     cases, "lind_order(k1, k2, k3, Cc)", pace="quick")

cases = []
for k1, km1, k2, Et, Sc in [(1e6, 100, 50, 1e-6, 1e-4), (2e7, 400, 100, 2e-7, 5e-5), (5e5, 10, 40, 1e-5, 2e-4), (1e8, 1000, 500, 1e-8, 1e-5)]:
    Km = (M(str(km1)) + k2) / M(str(k1))
    cases.append({"k1": k1, "km1": km1, "k2": k2, "Et": Et, "Sc": Sc, "ans": F(k2 * M(str(Et)) * M(str(Sc)) / (Km + M(str(Sc))))})
val("re-mm-steps", "cre.bio", "E + S ⇌ E·S → E + P with $k_1 = {{k1}}$ L/(mol·s), $k_{-1} = {{km1}}$ s⁻¹, $k_2 = {{k2}}$ s⁻¹, total enzyme ${{Et}}$ M. What is the rate (M/s) at $S = {{Sc}}$ M?", "Rate (M/s)",
    "PSSH on E·S plus the enzyme balance give $r = \\dfrac{V_{\\max}S}{K_m + S}$ with $V_{\\max} = k_2E_t$ and $K_m = \\dfrac{k_{-1} + k_2}{k_1}$. At $S = K_m$ the rate is half of $V_{\\max}$",
    cases, "mm_pssh(k1, km1, k2, Et, Sc)")

cases = []
for w in (0, 1):
    for Vm, Km, S1, S2 in [(10, 2, 1, 8), (0.5, 0.1, 0.05, 0.5), (100, 25, 10, 100), (4, 0.8, 0.4, 4)]:
        v1, v2 = sig(M(Vm) * S1 / (Km + M(str(S1)))), sig(M(Vm) * S2 / (Km + M(str(S2))))
        sl = (1 / M(str(v2)) - 1 / M(str(v1))) / (1 / M(str(S2)) - 1 / M(str(S1)))
        ic = 1 / M(str(v1)) - sl / M(str(S1))
        cases.append({"w": w, "wt": ["$V_{\\max}$", "$K_m$"][w], "S1": S1, "v1": v1, "S2": S2, "v2": v2, "ans": F([1 / ic, sl / ic][w])})
val("re-mm-fit", "cre.bio", "An enzyme gives rate ${{v1}}$ at $S = {{S1}}$ and ${{v2}}$ at $S = {{S2}}$ (consistent units). Assuming Michaelis–Menten kinetics, what is {{wt}}?", "Value",
    "Lineweaver–Burk: $\\dfrac1r = \\dfrac{K_m}{V_{\\max}}\\dfrac1S + \\dfrac1{V_{\\max}}$. Two points fix the line: intercept $1/V_{\\max}$, slope $K_m/V_{\\max}$. With real data, prefer a nonlinear fit, since the reciprocal plot magnifies low-S scatter",
    cases, "mm_fit(w, S1, v1, S2, v2)", tol=0.0005)

cases = [{"how": "$K_m$ rises, $V_{\\max}$ is unchanged", "ans": 0}, {"how": "$K_m$ and $V_{\\max}$ both fall by the same factor", "ans": 1},
         {"how": "$V_{\\max}$ falls, $K_m$ is unchanged", "ans": 2}, {"how": "Lineweaver–Burk lines cross on the 1/r axis", "ans": 0},
         {"how": "Lineweaver–Burk lines are parallel", "ans": 1}, {"how": "Lineweaver–Burk lines cross on the 1/S axis", "ans": 2}]
pick("re-inhibition-type", "cre.bio", "With an inhibitor present, {{how}}. What kind of inhibition is it?",
     ["Competitive", "Uncompetitive", "Noncompetitive"],
     "Competitive: I takes the active site, so more S overcomes it ($K_m$ up, same $V_{\\max}$; lines meet on the 1/r axis). Uncompetitive: I binds only E·S ($K_m$ and $V_{\\max}$ fall together; parallel lines). Noncompetitive: I binds E and E·S alike ($V_{\\max}$ falls, same $K_m$; lines meet on the 1/S axis)",
     cases)

cases = []
for w in (0, 1, 2):
    for mm_, Ks, S0, Dl, Yx in [(0.5, 2, 20, 0.3, 0.5), (1.2, 0.5, 10, 0.8, 0.4), (0.3, 1, 30, 0.1, 0.6)]:
        v = [M(str(mm_)) * S0 / (Ks + M(S0)), Ks * M(str(Dl)) / (M(str(mm_)) - M(str(Dl))), M(str(Yx)) * (S0 - Ks * M(str(Dl)) / (M(str(mm_)) - M(str(Dl))))][w]
        cases.append({"w": w, "wt": ["washout dilution rate (h⁻¹)", "steady substrate concentration (g/L)", "steady cell concentration (g/L)"][w],
                      "mm": mm_, "Ks": Ks, "S0": S0, "Dl": Dl, "Yx": Yx, "ans": F(v)})
val("re-chemostat", "cre.bio", "A chemostat with Monod growth, $\\mu_{\\max} = {{mm}}$ h⁻¹, $K_s = {{Ks}}$ g/L, yield $Y_{X/S} = {{Yx}}$, is fed sterile substrate at ${{S0}}$ g/L with dilution rate $D = {{Dl}}$ h⁻¹. What is the {{wt}}?", "Value",
    "At steady state $\\mu = D$, so $S = \\dfrac{K_sD}{\\mu_{\\max} - D}$ (the feed strength does not enter), and $X = Y_{X/S}(S_0 - S)$. Washout happens when even feed-strength substrate cannot grow cells as fast as they leave: $D_{\\max} = \\dfrac{\\mu_{\\max}S_0}{K_s + S_0}$",
    cases, "chemostat(w, mm, Ks, S0, Dl, Yx)")

# ── 6. Nonisothermal reactors (Fogler 11–13) ────────────────────────────────
cases = []
for w in (0, 1):
    for T0, dH, cp, X, Tg in [(300, -50000, 200, 0.6, 400), (350, -80000, 400, 0.8, 450), (500, 40000, 150, 0.3, 450), (320, -20000, 100, 0.9, 380)]:
        v = [M(T0) - M(dH) * M(str(X)) / cp, M(cp) * (Tg - T0) / -M(dH)][w]
        if 0 < v < 1 or w == 0:
            cases.append({"w": w, "wt": [f"temperature (K) at $X = {X}$", f"conversion when the outlet is at ${Tg}$ K"][w], "T0": T0, "dH": dH, "cp": cp, "X": X, "Tg": Tg, "ans": F(v)})
val("re-adiabatic-T", "cre.nonisothermal", "A reaction with $\\Delta H_{\\rm rx} = {{dH}}$ J/mol A (constant, $\\Delta C_p = 0$) runs adiabatically. The feed enters at ${{T0}}$ K with $\\sum\\Theta_iC_{p,i} = {{cp}}$ J/(mol A·K). What is the {{wt}}?", "Value",
    "Adiabatic energy balance: $T = T_0 + \\dfrac{(-\\Delta H_{\\rm rx})X}{\\sum\\Theta_iC_{p,i}}$, a straight line in the X–T plane for any adiabatic reactor, batch or flow. Endothermic reactions cool as they go",
    cases, "[adiabatic_T(T0, dH, cp, X), nsimplify(cp)*(nsimplify(Tg) - nsimplify(T0))/(-nsimplify(dH))][w]")

cases = []
for K1, T1, dH, cp, T0 in [(3.03, 333, -6900, 159, 330), (10, 300, -40000, 300, 300), (5, 400, -30000, 150, 380), (50, 350, -60000, 400, 350), (3.03, 333, -6900, 159, 300)]:
    K = lambda T: M(str(K1)) * mp.exp(-M(dH) / R * (1 / T - 1 / M(T1)))  # noqa: E731
    xe = lambda T: K(T) / (1 + K(T))  # noqa: E731
    xb = lambda T: cp * (T - T0) / -M(dH)  # noqa: E731
    lo, hi = M(T0), M(T0) - M(dH) / cp
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if xb(mid) < xe(mid) else (lo, mid)
    cases.append({"K1": K1, "T1": T1, "dH": dH, "cp": cp, "T0": T0, "ans": F(xb((lo + hi) / 2))})
val("re-adiabatic-xe", "cre.nonisothermal", "The exothermic liquid reaction A ⇌ B has $K_C = {{K1}}$ at ${{T1}}$ K and $\\Delta H_{\\rm rx} = {{dH}}$ J/mol. Pure A enters an adiabatic reactor at ${{T0}}$ K with $\\sum\\Theta_iC_{p,i} = {{cp}}$ J/(mol·K). What is the adiabatic equilibrium conversion?", "X_e",
    "Two curves: the energy balance $X_{EB} = \\dfrac{\\sum\\Theta_iC_{p,i}(T - T_0)}{-\\Delta H_{\\rm rx}}$ and equilibrium $X_e = \\dfrac{K}{1 + K}$ with $K(T) = K_1\\exp\\!\\left[-\\dfrac{\\Delta H}{R}\\left(\\dfrac1T - \\dfrac1{T_1}\\right)\\right]$. They cross once; iterate on T. Cooling between stages (or a colder feed) gets past it",
    cases, "adiabatic_xe(K1, T1, dH, cp, T0)", tol=0.0002, pace="workout")


def cstr_roots(tau, k1, T1, E, dH, cp, T0):
    k = lambda T: M(str(k1)) * mp.exp(-M(E) / R * (1 / T - 1 / M(T1)))  # noqa: E731
    g = lambda T: M(str(tau)) * k(T) / (1 + M(str(tau)) * k(T)) - cp * (T - T0) / -M(dH)  # noqa: E731
    top = M(T0) - M(dH) / cp
    grid = [M(T0) + (top - T0) * i / 4000 for i in range(4001)]
    out = []
    for a, b in zip(grid, grid[1:]):
        if g(a) == 0:
            out.append(a)
        elif g(a) * g(b) < 0:
            lo, hi = a, b
            for _ in range(120):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if g(lo) * g(mid) > 0 else (lo, mid)
            out.append((lo + hi) / 2)
    return out


cands = [(10, 0.01, 350, 100000, -100000, 500, 300), (10, 0.01, 350, 100000, -100000, 500, 340), (10, 0.01, 350, 100000, -100000, 500, 380),
         (1, 0.1, 400, 80000, -60000, 300, 330), (2, 0.2, 350, 60000, -50000, 250, 300), (2, 0.2, 350, 60000, -50000, 250, 340),
         (1, 0.1, 350, 50000, -30000, 200, 330), (3, 0.1, 350, 60000, -40000, 400, 320), (5, 0.5, 350, 50000, -30000, 300, 320),
         (2, 0.05, 350, 40000, -30000, 300, 320), (1, 0.5, 350, 30000, -20000, 200, 300)]
mss, single = [], []
for tau, k1, T1, E, dH, cp, T0 in cands:
    r = cstr_roots(tau, k1, T1, E, dH, cp, T0)
    base = {"tau": tau, "k1": k1, "T1": T1, "Ea": E, "dH": dH, "cp": cp, "T0": T0}
    if len(r) in (1, 3):
        mss.append({**base, "ans": {1: 0, 3: 1}[len(r)]})
    if len(r) == 1:
        single.append({**base, "ans": F(r[0])})
CSTR = "A first-order liquid reaction runs in an adiabatic CSTR: $\\tau = {{tau}}$ min, $k = {{k1}}$ min⁻¹ at ${{T1}}$ K, $E = {{Ea}}$ J/mol, $\\Delta H_{\\rm rx} = {{dH}}$ J/mol, $\\sum\\Theta_iC_{p,i} = {{cp}}$ J/(mol·K), feed at ${{T0}}$ K."
pick("re-mss-count", "cre.nonisothermal", CSTR + " How many steady states are there?", ["One", "Three"],
     "Steady states are where heat generated, $G(T) = (-\\Delta H)\\dfrac{\\tau k}{1 + \\tau k}$, meets heat removed, $R(T) = \\sum\\Theta_iC_{p,i}(T - T_0)$. The sigmoid G can cut the line R once (low or high) or three times; the middle one of three is unstable. Raising $T_0$ slides the line right and can ignite the reactor",
     mss, "cstr_adiabatic(0, tau, k1, T1, Ea, dH, cp, T0)", pace="workout")
val("re-cstr-adiabatic-T", "cre.nonisothermal", CSTR + " It has a single steady state. What is its temperature (K)?", "T (K)",
    "Solve $X_{MB}(T) = \\dfrac{\\tau k(T)}{1 + \\tau k(T)}$ together with $X_{EB}(T) = \\dfrac{\\sum\\Theta_iC_{p,i}(T - T_0)}{-\\Delta H}$ by iterating on T. Check the answer sits between $T_0$ and the adiabatic limit $T_0 - \\Delta H/\\sum\\Theta_iC_{p,i}$",
    single, "cstr_adiabatic(1, tau, k1, T1, Ea, dH, cp, T0)", tol=0.00002, pace="workout")

# ── 7. Diffusion and reaction (Fogler 14, 15) ───────────────────────────────
cases = []
for kc, kr, Cb in [(0.01, 0.01, 2), (0.05, 0.005, 1), (0.002, 0.1, 5), (0.02, 0.06, 0.5)]:
    cases.append({"kc": kc, "kr": kr, "Cb": Cb, "ans": F(M(str(Cb)) / (1 / M(str(kc)) + 1 / M(str(kr))))})
val("re-ext-mt", "cre.diffusion", "A first-order surface reaction ($k_r = {{kr}}$ m/s) sits behind a film with $k_c = {{kc}}$ m/s. The bulk concentration is ${{Cb}}$ mol/m³. What is the rate per area (mol/(m²·s))?", "−r″_A",
    "Steady state: what crosses the film reacts, $k_c(C_b - C_s) = k_rC_s$. Eliminate $C_s$: $-r''_A = \\dfrac{C_b}{1/k_c + 1/k_r}$, resistances in series. The smaller of $k_c$ and $k_r$ controls; if mass transfer controls, raising the temperature barely helps but raising the velocity does",
    cases, "ext_mt(kc, kr, Cb)")

cases = []
for kc, a, L, U in [(0.002, 600, 1, 0.5), (0.001, 1200, 0.5, 1), (0.005, 300, 2, 2), (0.0005, 2000, 1.5, 0.4)]:
    cases.append({"kc": kc, "a": a, "Lb": L, "U": U, "ans": F(1 - mp.exp(-M(str(kc)) * a * M(str(L)) / M(str(U))))})
val("re-mt-bed", "cre.diffusion", "A fast reaction in a packed bed is limited entirely by external mass transfer: $k_c = {{kc}}$ m/s, $a_c = {{a}}$ m²/m³, bed length ${{Lb}}$ m, superficial velocity ${{U}}$ m/s. What is the conversion?", "X",
    "With $C_s \\approx 0$, a balance on a slice gives $U\\dfrac{dC}{dz} = -k_ca_cC$, so $X = 1 - \\exp\\!\\left(-\\dfrac{k_ca_cL}{U}\\right)$. Doubling $U$ halves the exponent only partly, since $k_c$ grows roughly as $U^{1/2}$",
    cases, "mt_bed(kc, a, Lb, U)")

cases = []
for geom, Rp, k, De in [(1, 0.5, 4, 0.01), (1, 0.2, 1, 0.04), (0, 0.3, 2, 0.02), (0, 0.1, 10, 0.05), (1, 0.05, 0.5, 0.01), (0, 0.5, 0.1, 0.1)]:
    phi = M(str(Rp)) * mp.sqrt(M(str(k)) / M(str(De)))
    e = 3 / phi**2 * (phi * mp.coth(phi) - 1) if geom else mp.tanh(phi) / phi
    cases.append({"geom": geom, "shape": ["slab catalyst sealed on one face, half-thickness", "spherical pellet of radius"][geom], "Rp": Rp, "k": k, "De": De, "ans": F(e)})
val("re-effectiveness", "cre.diffusion", "A first-order reaction ($k = {{k}}$ s⁻¹ per pellet volume) runs in a {{shape}} ${{Rp}}$ cm, effective diffusivity ${{De}}$ cm²/s. What is the internal effectiveness factor η?", "η",
    "Thiele modulus $\\phi = L\\sqrt{k/D_e}$ (length = half-thickness or radius). Slab: $\\eta = \\dfrac{\\tanh\\phi}{\\phi}$; sphere: $\\eta = \\dfrac{3}{\\phi^2}(\\phi\\coth\\phi - 1)$. Large φ: η → 1/φ (slab) or 3/φ (sphere), and the apparent activation energy is halved",
    cases, "eta(geom, nsimplify(Rp)*sqrt(nsimplify(k)/nsimplify(De)))")

cases = []
for Rp, k, De in [(0.5, 4, 0.01), (0.2, 1, 0.04), (0.05, 0.5, 0.01), (0.3, 0.02, 0.05), (1, 2, 0.02)]:
    phi = M(str(Rp)) * mp.sqrt(M(str(k)) / M(str(De)))
    cases.append({"Rp": Rp, "k": k, "De": De, "ans": F(3 / phi**2 * (phi * mp.coth(phi) - 1) * phi**2)})
val("re-weisz-prater", "cre.diffusion", "A spherical pellet (radius ${{Rp}}$ cm, $D_e = {{De}}$ cm²/s) runs a first-order reaction with intrinsic $k = {{k}}$ s⁻¹. What is the Weisz–Prater parameter $C_{WP}$?", "C_WP",
    "$C_{WP} = \\dfrac{-r'_{\\rm obs}\\rho_cR^2}{D_eC_{As}}$ uses only observed quantities; for first order it equals $\\eta\\phi^2$. $C_{WP} \\ll 1$: no internal limitation. $C_{WP} \\gg 1$: severe limitation",
    cases, "cwp(Rp, k, De)")

cases = []
for kc, a, et, k, Cb in [(0.01, 100, 0.5, 2, 1), (0.002, 500, 0.8, 0.5, 2), (0.05, 50, 0.2, 10, 0.5), (0.001, 1000, 0.9, 0.1, 3)]:
    cases.append({"kc": kc, "a": a, "et": et, "k": k, "Cb": Cb, "ans": F(M(str(Cb)) / (1 / (M(str(kc)) * a) + 1 / (M(str(et)) * M(str(k)))))})
val("re-overall-eff", "cre.diffusion", "A first-order reaction ($k = {{k}}$ s⁻¹ per reactor volume, internal η = ${{et}}$) sits behind an external film, $k_c = {{kc}}$ m/s, $a_c = {{a}}$ m²/m³. Bulk $C_A = {{Cb}}$ mol/m³. What is the rate per reactor volume (mol/(m³·s))?", "Rate",
    "In series: $k_ca_c(C_b - C_s) = \\eta kC_s$, so the rate is $\\dfrac{C_b}{1/(k_ca_c) + 1/(\\eta k)}$, which is $\\Omega kC_b$ with overall effectiveness $\\Omega = \\dfrac{\\eta}{1 + \\eta k/(k_ca_c)}$",
    cases, "overall_rate(kc, a, et, k, Cb)")

# ── 8. Residence times and nonideal reactors (Fogler 16–18) ─────────────────
cases = []
for w in (0, 1):
    for dt, Cs in [(1, (0, 1, 5, 8, 10, 8, 6, 4, 3, 2.2, 1.5, 0.6, 0)), (2, (0, 3, 6, 5, 4, 3, 2, 1, 0)), (5, (0, 2, 4, 6, 4, 2, 0)), (3, (0, 1, 3, 6, 6, 4, 2, 1, 0))]:
        ts = [i * dt for i in range(len(Cs))]
        s0 = sum(M(str(c)) for c in Cs)
        tm = sum(t * M(str(c)) for t, c in zip(ts, Cs)) / s0
        var = sum((t - tm) ** 2 * M(str(c)) for t, c in zip(ts, Cs)) / s0
        cases.append({"w": w, "wt": ["mean residence time $t_m$ (min)", "variance $\\sigma^2$ (min²)"][w], "tt": ", ".join(map(str, ts)), "cc": ", ".join(map(str, Cs)),
                      "ts": ts, "Cs": [float(c) for c in Cs], "ans": F([tm, var][w])})
val("re-rtd-moments", "cre.rtd", "A tracer pulse gives exit readings at $t$ (min): {{tt}}; $C$ (mg/L): {{cc}}. What is the {{wt}}?", "Value",
    "$E(t) = C/\\int C\\,dt$; $t_m = \\int tE\\,dt$; $\\sigma^2 = \\int(t - t_m)^2E\\,dt$. With equal steps and zero ends the integrals are plain sums. $t_m = V/v_0$ if there is no dead volume, so a short $t_m$ flags stagnant zones",
    cases, "rtd_moments(w, ts, Cs)", pace="workout")

cases = []
for w in (0, 1):
    for n, tau, tt in [(1, 10, 5), (1, 4, 8), (2, 10, 5), (2, 6, 9), (3, 9, 3), (3, 12, 18)]:
        th = M(n) * tt / tau
        Fv = 1 - mp.exp(-th) * sum(th**i / mp.factorial(i) for i in range(n))
        cases.append({"w": w, "n": n, "tau": tau, "tt": tt, "wt": ["less", "more"][w], "rx": ["one ideal CSTR", "two equal CSTRs in series", "three equal CSTRs in series"][n - 1], "ans": F([Fv, 1 - Fv][w])})
val("re-tanks-F", "cre.rtd", "Fluid flows through {{rx}} with total mean residence time ${{tau}}$ min. What fraction of it spends {{wt}} than ${{tt}}$ min inside?", "Fraction",
    "For one CSTR $F(t) = 1 - e^{-t/\\tau}$; for $n$ equal tanks, $F = 1 - e^{-n\\theta}\\sum_{i=0}^{n-1}\\dfrac{(n\\theta)^i}{i!}$ with $\\theta = t/\\tau$. A single CSTR sends 63% of the fluid out before $\\tau$; more tanks narrow the spread toward plug flow",
    cases, "tanks_F(n, tau, tt, w)")

cases = []
for kind, n, Da in [(0, 1, 2), (0, 2, 2), (0, 3, 1), (0, 4, 3), (1, 1, 1), (1, 1, 4), (1, 1, 0.5), (1, 1, 10)]:
    if kind == 0:
        v = 1 - (1 + M(Da) / n) ** -n
    else:
        v = mp.quad(lambda t: M(Da) * t / (1 + M(Da) * t) * mp.exp(-t), [0, mp.inf])
    cases.append({"kind": kind, "n": n, "Da": Da, "what": ["a first-order reaction with $k\\tau = {{Da}}$".replace("{{Da}}", str(Da)) + (" and the RTD of " + ["one CSTR", "two equal tanks in series", "three equal tanks in series", "four equal tanks in series"][n - 1]),
                                                           f"a second-order reaction with $kC_{{A0}}\\tau = {Da}$ and the RTD of one CSTR"][kind], "ans": F(v)})
val("re-segregation", "cre.rtd", "Use the segregation model for {{what}}. What is the mean conversion?", "X̄",
    "Each fluid element is a little batch reactor: $\\bar X = \\int_0^\\infty X_{\\rm batch}(t)E(t)\\,dt$. For first order this equals the ideal result for the same RTD, since mixing does not matter for linear kinetics. For second order, segregation beats the ideal CSTR (maximum mixedness) because unmixed elements keep their high concentration",
    cases, "seg_X(kind, Da, n)")

cases = []
for tm, s2, k in [(10, 50, 0.2), (12, 36, 0.1), (8, 16, 0.25), (20, 100, 0.05), (6, 6, 0.5)]:
    n = int(round(tm**2 / s2))
    cases.append({"tm": tm, "s2": s2, "k": k, "ans": F(1 - (1 + M(str(k)) * tm / n) ** -n)})
val("re-tis-model", "cre.rtd", "A reactor's RTD has $t_m = {{tm}}$ min and $\\sigma^2 = {{s2}}$ min². Model it as equal tanks in series. What conversion does a first-order reaction with $k = {{k}}$ min⁻¹ reach?", "X",
    "Tanks-in-series: $n = t_m^2/\\sigma^2$, here a whole number. Then $X = 1 - \\dfrac{1}{(1 + kt_m/n)^n}$. One tank is the CSTR; $n \\to \\infty$ is plug flow, $1 - e^{-kt_m}$",
    cases, "tis_X(nsimplify(tm)**2/nsimplify(s2), nsimplify(k)*nsimplify(tm))")

cases = []
for Pe, Da in [(10, 2), (1, 1), (50, 3), (5, 0.5), (20, 4)]:
    q = mp.sqrt(1 + 4 * M(Da) / Pe)
    pe = M(Pe)
    X = 1 - 4 * q * mp.exp(pe / 2) / ((1 + q) ** 2 * mp.exp(pe * q / 2) - (1 - q) ** 2 * mp.exp(-pe * q / 2))
    cases.append({"Pe": Pe, "Da": Da, "ans": F(X)})
val("re-dispersion", "cre.rtd", "A first-order reaction ($Da = k\\tau = {{Da}}$) runs in a closed–closed vessel described by the dispersion model with $Pe_r = {{Pe}}$. What is the conversion?", "X",
    "Danckwerts' boundary conditions give $X = 1 - \\dfrac{4q\\,e^{Pe/2}}{(1 + q)^2e^{Pe\\,q/2} - (1 - q)^2e^{-Pe\\,q/2}}$ with $q = \\sqrt{1 + 4Da/Pe}$. Large Pe tends to plug flow, small Pe to a CSTR",
    cases, "disp_X(Pe, Da)", pace="workout")

yaml.safe_dump(T, open(OUT, "w"), allow_unicode=True, sort_keys=False, width=200)
print(len(T), "templates,", sum(len(t["cases"]) for t in T), "cases ->", OUT)
print("mss cases:", [c["ans"] for c in mss], "single:", [c["ans"] for c in single])
