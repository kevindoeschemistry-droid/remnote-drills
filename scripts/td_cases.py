"""Builds drills/problems/td-depth.yaml: the Thermodynamics and Statistical Mechanics objectives
(framework thermodynamics, TD) that had no drills. Run: python3 scripts/td_cases.py

Answers follow the textbook formula (equal-area construction, ln φ = BP/RT, the regular-solution
closed forms, λ₊ = e^βJ cosh βh + √(…), χ_c = ½(1 + 1/√N)²…); tests/verify/tdcalc.py checks by another
route (equal G, the ∫(Z−1)/P integral, Gibbs–Duhem integrated, transfer-matrix eigenvalues, the
critical point from derivatives).
"""
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/td-depth.yaml"
R = mp.mpf("1.380649e-23") * mp.mpf("6.02214076e23")
T = []


def F(v):
    return float(mp.nstr(v, 12))


def val(name, skill, prompt, ask, explain, cases, verify, tol=0.0001, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(name, skill, prompt, options, explain, cases, verify=None, pace="recall"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}],
              "verify": {"choices": {"y": verify}} if verify else {"authored": True}})


# 1.1.D Stirling
cases = [{"N": n, "ans": F(n * mp.log(n) - n)} for n in (100, 1000, 50, 10000, 6.02e23)]
val("td-stirling", "stat.multiplicity", "Use Stirling's approximation to estimate $\\ln N!$ for $N = {{N}}$.", "ln N!",
    "$\\ln N! \\approx N\\ln N - N$, from $\\ln N! = \\sum\\ln k \\approx \\int_1^N \\ln x\\,dx$. Already within 1% at N = 100; for a mole of particles it is exact for all purposes, which is why entropy formulas use it",
    cases, "nsimplify(N)*log(nsimplify(N)) - nsimplify(N)", tol=0.0002)

cases = []
for N, n in [(100, 50), (100, 20), (1000, 500), (60, 15)]:
    cases.append({"N": N, "n": n, "ans": F(N * mp.log(N) - n * mp.log(n) - (N - n) * mp.log(N - n))})
val("td-stirling-lnw", "stat.multiplicity", "With Stirling's approximation, what is $\\ln W$ for $W = \\binom{ {{N}} }{ {{n}} }$ (choosing {{n}} of {{N}} sites)?", "ln W",
    "$\\ln W \\approx N\\ln N - n\\ln n - (N - n)\\ln(N - n) = -N[x\\ln x + (1 - x)\\ln(1 - x)]$ with $x = n/N$: the mixing-entropy form",
    cases, "N*log(N) - n*log(n) - (N - n)*log(N - n)")

# 1.2.C mean and variance
cases = []
for xs, ps in [((0, 1, 2), (0.25, 0.5, 0.25)), ((1, 2, 3, 4), (0.1, 0.2, 0.3, 0.4)), ((-1, 1), (0.3, 0.7)), ((0, 1, 2, 3), (0.4, 0.3, 0.2, 0.1))]:
    m = sum(x * p for x, p in zip(xs, ps))
    v = sum(x * x * p for x, p in zip(xs, ps)) - m * m
    for w, a in ((0, m), (1, v)):
        if abs(a) > 1e-12:
            cases.append({"xs": ", ".join(map(str, xs)), "ps": ", ".join(map(str, ps)), "X": list(xs), "P": list(ps), "w": w, "wt": ["mean", "variance"][w], "ans": F(mp.mpf(a))})
val("td-mean-variance", "stat.probability", "A variable takes the values {{xs}} with probabilities {{ps}}. What is its {{wt}}?", "Value",
    "$\\langle x\\rangle = \\sum p_ix_i$; $\\sigma^2 = \\langle x^2\\rangle - \\langle x\\rangle^2$. The variance is the mean-square fluctuation, the quantity behind heat capacities and compressibilities",
    cases, "[wsum(P, X), wsum(P, X, 2) - wsum(P, X)**2][w]")

# 2.2.B / 2.2.C / 4.2.C / 8.1 / 8.3.A concept picks
pick("td-max-entropy-equal", "thermo.fundamental-equation", "Two subsystems can exchange {{what}}. Maximising the total entropy makes which quantity equal on both sides?",
     ["Temperature", "Pressure (with T)", "Chemical potential (with T)"],
     "Set dS_total = 0 for the exchange: energy gives 1/T₁ = 1/T₂; volume gives P₁/T₁ = P₂/T₂; particles give μ₁/T₁ = μ₂/T₂. Each conserved quantity that can move pairs with an intensive variable that equalises",
     [{"what": "energy only (rigid, impermeable wall)", "ans": 0}, {"what": "energy and volume (a movable piston)", "ans": 1}, {"what": "energy and particles (a permeable wall)", "ans": 2}])
pick("td-max-s-min-u", "thermo.fundamental-equation", "{{s}}", ["True", "False"],
     "The entropy maximum principle at fixed U and the energy minimum principle at fixed S describe the same equilibrium: because (∂S/∂U) = 1/T > 0, a state that is not an energy minimum at fixed S can lower U and return the energy as heat, raising S at fixed U",
     [{"s": "At fixed S, V and N, an equilibrium state minimises U.", "ans": 0}, {"s": "At fixed U, V and N, an equilibrium state minimises S.", "ans": 1},
      {"s": "Maximum entropy at fixed energy and minimum energy at fixed entropy pick out the same state.", "ans": 0}, {"s": "The energy minimum principle needs (∂S/∂U) to be negative.", "ans": 1}])
pick("td-potential-choice", "thermo.legendre", "A system is held at fixed {{c}}. Which function is minimised at equilibrium?",
     ["U (internal energy)", "H (enthalpy)", "A (Helmholtz)", "G (Gibbs)", "Ω = A − μN (grand potential)"],
     "Each potential is minimised when its natural variables are fixed: U(S,V,N), H(S,P,N), A(T,V,N), G(T,P,N), Ω(T,V,μ). A bath fixes T; a piston at constant external pressure fixes P; a reservoir of particles fixes μ",
     [{"c": "T, V and N", "ans": 2}, {"c": "T, P and N", "ans": 3}, {"c": "S, V and N", "ans": 0}, {"c": "S, P and N", "ans": 1}, {"c": "T, V and μ", "ans": 4}])
cases = []
for C, P, sys in [(1, 1, "pure water, liquid only"), (1, 2, "pure water at its boiling point"), (2, 1, "a single-phase mixture of ethanol and water"), (2, 2, "a two-phase ethanol–water mixture"), (3, 2, "three components in two phases")]:
    cases.append({"C": C, "Pn": P, "sys": sys, "ans": C - P + 2})
val("td-phase-rule", "thermo.phase-equilibrium", "How many intensive variables can be changed independently in {{sys}}?", "Degrees of freedom",
    "Gibbs phase rule: $F = C - P + 2$ (C components, P phases, no reactions). A pure substance has F = 1 along a coexistence line (T fixes P) and 0 at the triple point",
    cases, "C - Pn + 2", tol=0.000001)
pick("td-transition-order", "thermo.phase-equilibrium", "{{s}}", ["First-order", "Second-order (continuous)"],
     "First-order: a first derivative of G (S, V, magnetisation) jumps, so there is a latent heat. Continuous: the first derivatives are smooth and a second derivative (C_p, compressibility, susceptibility) diverges or jumps",
     [{"s": "Boiling water at 1 atm, with a latent heat", "ans": 0}, {"s": "A ferromagnet losing its magnetisation smoothly at the Curie point, with a diverging susceptibility", "ans": 1},
      {"s": "Melting ice: the volume jumps", "ans": 0}, {"s": "A liquid–gas system exactly at its critical point", "ans": 1}, {"s": "Helium-4 at the lambda point (C_p diverges, no latent heat)", "ans": 1}])

# 2.3.C extensive
pick("td-extensive", "thermo.fundamental-equation", "Is $S = {{stex}}$ an acceptable (first-order homogeneous) fundamental equation?", ["No", "Yes"],
     "Scale every extensive variable by λ: S must become λS. Check the powers: a ratio like U/N or V/N is intensive, and a product of extensive variables must be raised to total power 1",
     [{"stex": "N\\ln(UV/N^2)", "e": "N*log(U*V/N**2)", "ans": 1}, {"stex": "(UVN)^{1/3}", "e": "(U*V*N)**(1/3)", "ans": 1}, {"stex": "(UV)^{1/2}", "e": "(U*V)**(1/2)", "ans": 1},
      {"stex": "N\\ln(UV)", "e": "N*log(U*V)", "ans": 0}, {"stex": "U^2V/N^2", "e": "U**2*V/N**2", "ans": 1}, {"stex": "(U^2V)^{1/3}", "e": "(U**2*V)**(1/3)", "ans": 1}, {"stex": "UV", "e": "U*V", "ans": 0}],
     "homogeneous(e)")

# 3.2.A total entropy, 3.2.B Carnot
cases = []
for m, c, T1, T2 in [(1, 4184, 373.15, 293.15), (0.5, 900, 500, 300), (2, 385, 300, 400), (1, 4184, 273.15, 323.15)]:
    dS = m * c * (mp.log(mp.mpf(T2) / T1) + (mp.mpf(T1) - T2) / T2)
    cases.append({"m": m, "c": c, "T1": T1, "T2": T2, "ans": F(dS)})
val("td-total-entropy", "thermo.first-law", "A ${{m}}$ kg block ($c = {{c}}$ J/kg·K) at ${{T1}}$ K is dropped into a large bath at ${{T2}}$ K and comes to equilibrium. What is the total entropy change of block plus bath (J/K)?", "ΔS_total",
    "Block: $mc\\ln(T_2/T_1)$ along any reversible path. Bath at constant T: $-Q/T_2 = mc(T_1 - T_2)/T_2$. The sum is always positive for $T_1 \\ne T_2$: heat flowing across a finite ΔT is irreversible",
    cases, "integrate(m*c/Symbol('TT'), (Symbol('TT'), nsimplify(T1), nsimplify(T2))) - m*c*(nsimplify(T2) - nsimplify(T1))/nsimplify(T2)")
cases = []
for kind, Th, Tc in [(0, 600, 300), (0, 800, 290), (1, 298, 273), (1, 295, 255), (2, 293, 273), (2, 298, 268)]:
    v = [1 - mp.mpf(Tc) / Th, mp.mpf(Tc) / (Th - Tc), mp.mpf(Th) / (Th - Tc)][kind]
    cases.append({"kind": kind, "Th": Th, "Tc": Tc, "kt": ["the maximum efficiency of a heat engine", "the maximum COP of a refrigerator", "the maximum COP of a heat pump"][kind], "ans": F(v)})
val("td-carnot", "thermo.first-law", "Between reservoirs at ${{Th}}$ K and ${{Tc}}$ K, what is {{kt}}?", "Value",
    "Reversible limits: engine $1 - T_c/T_h$; refrigerator $T_c/(T_h - T_c)$; heat pump $T_h/(T_h - T_c)$. Small temperature lifts give large COPs",
    cases, "[1 - Rational(Tc, Th), Rational(Tc, Th - Tc), Rational(Th, Th - Tc)][kind]")

# 3.3.A steady flow: isentropic turbine/compressor
cases = []
for dev, T1, P1, P2, cp in [("turbine", 1000, 1000, 100, 29.1), ("compressor", 300, 100, 800, 29.1), ("nozzle", 800, 500, 100, 32.0), ("compressor", 290, 100, 400, 37.1)]:
    T2 = T1 * (mp.mpf(P2) / P1) ** (R / cp)
    cases.append({"dev": dev, "T1": T1, "P1": P1, "P2": P2, "cp": cp, "ans": F(T2)})
val("td-isentropic-outlet", "thermo.first-law", "An ideal gas with molar $c_p = {{cp}}$ J/mol·K (R = 8.314) enters a reversible adiabatic {{dev}} at ${{T1}}$ K and ${{P1}}$ kPa and leaves at ${{P2}}$ kPa. What is the outlet temperature?",
    "T₂ (K)",
    "Reversible and adiabatic means isentropic: $c_p\\ln(T_2/T_1) = R\\ln(P_2/P_1)$, so $T_2 = T_1(P_2/P_1)^{R/c_p}$. The steady-flow energy balance then gives the shaft work, $\\dot W = \\dot m c_p(T_1 - T_2)$",
    cases, "isentropic_T2(T1, P1, P2, cp)")

# 4.1.A exact differentials, 4.1.B triple product
pick("td-exact", "thermo.maxwell", "Is $({{M}})\\,dx + ({{Nn}})\\,dy$ an exact differential?", ["No", "Yes"],
     "Exact (the change of a state function) exactly when $\\partial M/\\partial y = \\partial N/\\partial x$. Heat and work are not exact; δQ/T is",
     [{"M": "2xy", "Nn": "x^2", "Mx": "2*x*y", "Ny": "x**2", "ans": 1}, {"M": "y", "Nn": "-x", "Mx": "y", "Ny": "-x", "ans": 0}, {"M": "y^2", "Nn": "2xy", "Mx": "y**2", "Ny": "2*x*y", "ans": 1},
      {"M": "e^{x}y", "Nn": "e^{x}", "Mx": "exp(x)*y", "Ny": "exp(x)", "ans": 1}, {"M": "x + y", "Nn": "x - y", "Mx": "x + y", "Ny": "x - y", "ans": 1}, {"M": "xy", "Nn": "xy", "Mx": "x*y", "Ny": "x*y", "ans": 0}],
     "exact(Mx, Ny)", pace="quick")
cases = []
for a, b, T_, V in [(0.1382, 3.19e-5, 300, 1e-3), (0.3658, 4.29e-5, 350, 5e-4), (0.0, 0.0, 300, 0.0249)]:
    # (∂V/∂T)_P = −(∂P/∂T)_V / (∂P/∂V)_T for vdW
    dPdT = R / (V - b)
    dPdV = -R * T_ / (V - b) ** 2 + 2 * a / V**3
    cases.append({"a": a, "b": b, "T0": T_, "V": V, "gas": "an ideal gas" if a == 0 else "a van der Waals gas", "ans": F(-dPdT / dPdV)})
val("td-triple-product", "thermo.maxwell", "For {{gas}} ($a = {{a}}$ Pa·m⁶/mol², $b = {{b}}$ m³/mol) at $T = {{T0}}$ K, $V = {{V}}$ m³/mol, find $(\\partial V/\\partial T)_P$ (m³/mol·K) using the triple product rule.", "(∂V/∂T)_P",
    "$(\\partial V/\\partial T)_P = -\\dfrac{(\\partial P/\\partial T)_V}{(\\partial P/\\partial V)_T}$: both derivatives come straight from $P(T, V)$, so no need to solve the cubic for V",
    cases, "-diff((c_R*Symbol('TT')/(Symbol('VV') - b) - a/Symbol('VV')**2), Symbol('TT'))/diff((c_R*Symbol('TT')/(Symbol('VV') - b) - a/Symbol('VV')**2), Symbol('VV'))".replace("Symbol('TT')", "Symbol('TT')").replace("(c_R", "(c_R") + "", tol=0.0001)
T[-1]["verify"]["expect"]["y"] = "(-diff(c_R*Symbol('TT')/(Symbol('VV') - nsimplify(b)) - nsimplify(a)/Symbol('VV')**2, Symbol('TT'))/diff(c_R*Symbol('TT')/(Symbol('VV') - nsimplify(b)) - nsimplify(a)/Symbol('VV')**2, Symbol('VV'))).subs({Symbol('TT'): T0, Symbol('VV'): nsimplify(V)})"

# 5.2.C cp − cv, 5.2.D (∂U/∂V)_T and Joule–Thomson
cases = []
for sub, Tt, Vm, al, kap in [("water at 25 °C", 298.15, 1.807e-5, 2.57e-4, 4.52e-10), ("copper at 25 °C", 298.15, 7.11e-6, 4.95e-5, 7.3e-12), ("ethanol at 20 °C", 293.15, 5.84e-5, 1.12e-3, 1.11e-9), ("mercury at 20 °C", 293.15, 1.48e-5, 1.81e-4, 4.0e-11)]:
    cases.append({"sub": sub, "Tt": Tt, "Vm": Vm, "al": al, "kap": kap, "ans": F(mp.mpf(Tt) * Vm * al**2 / kap)})
val("td-cp-cv", "thermo.maxwell", "For {{sub}}: $V_m = {{Vm}}$ m³/mol, $\\alpha = {{al}}$ K⁻¹, $\\kappa_T = {{kap}}$ Pa⁻¹. What is $C_{p,m} - C_{V,m}$ (J/mol·K)?", "C_p − C_V",
    "$C_p - C_V = TV\\alpha^2/\\kappa_T$, from Maxwell relations. For an ideal gas it gives R; for water near 4 °C (α = 0) it vanishes, and for solids it is small",
    cases, "nsimplify(Tt)*nsimplify(Vm)*nsimplify(al)**2/nsimplify(kap)")
cases = []
for gas, a, b, Tt, Vm, cp, w in [("N₂", 0.137, 3.87e-5, 300, 1e-3, 29.1, 1), ("CO₂", 0.364, 4.27e-5, 300, 5e-4, 37.1, 1), ("N₂", 0.137, 3.87e-5, 300, 1e-3, 29.1, 0), ("CO₂", 0.364, 4.27e-5, 300, 5e-4, 37.1, 0), ("He", 0.00346, 2.38e-5, 300, 1e-3, 20.8, 1)]:
    v = (2 * mp.mpf(a) / (R * Tt) - b) / cp if w else mp.mpf(a) / Vm**2
    cases.append({"gas": gas, "a": a, "b": b, "Tt": Tt, "Vm": Vm, "cp": cp, "w": w,
                  "wt": [f"the internal pressure $(\\partial U/\\partial V)_T$ (Pa) at $V_m = {Vm}$ m³/mol", "the low-pressure Joule–Thomson coefficient (K/Pa)"][w], "ans": F(v)})
val("td-vdw-derivatives", "thermo.maxwell", "For {{gas}} as a van der Waals gas ($a = {{a}}$ Pa·m⁶/mol², $b = {{b}}$ m³/mol, $C_{p,m} = {{cp}}$ J/mol·K) at ${{Tt}}$ K, find {{wt}}.", "Value",
    "Thermodynamic equation of state: $(\\partial U/\\partial V)_T = T(\\partial P/\\partial T)_V - P = a/V_m^2$ for vdW. Joule–Thomson at low pressure: $\\mu_{JT} \\approx (2a/RT - b)/C_p$; positive (cools on throttling) below the inversion temperature $2a/Rb$. Helium inverts far below room temperature",
    cases, "[nsimplify(a)/nsimplify(Vm)**2, (2*nsimplify(a)/(c_R*Tt) - nsimplify(b))/nsimplify(cp)][w]")

# 6.2.B spinodal, 6.3.A coexistence
cases = []
for Tr, Vr in [(0.9, 1.0), (0.9, 0.5), (0.9, 3.0), (0.85, 1.2), (0.95, 0.8), (1.1, 1.0), (0.8, 0.6)]:
    dPdV = -24 * mp.mpf(Tr) / (3 * Vr - 1) ** 2 + 6 / mp.mpf(Vr) ** 3
    cases.append({"Tr": Tr, "Vr": Vr, "ans": 1 if dPdV > 0 else 0})
pick("td-spinodal", "thermo.stability", "In reduced van der Waals units ($P_r = \\dfrac{8T_r}{3V_r - 1} - \\dfrac{3}{V_r^2}$), is the state $T_r = {{Tr}}$, $V_r = {{Vr}}$ mechanically unstable (inside the spinodal)?",
     ["No: stable or metastable", "Yes: unstable"],
     "Mechanical stability needs $(\\partial P/\\partial V)_T < 0$. Where the slope turns positive the state is inside the spinodal and splits at once; between spinodal and binodal it is metastable (superheated liquid, supercooled vapour). Above $T_r = 1$ nothing is unstable",
     cases, "vdw_reduced_unstable(Tr, Vr)", pace="quick")
cases = []
for Tr in (0.9, 0.85, 0.95, 0.8):
    Tr_ = mp.mpf(Tr)
    P = lambda V: 8 * Tr_ / (3 * V - 1) - 3 / V**2  # noqa: E731
    # spinodal volumes: 4 Tr V³ = (3V − 1)², the loop's turning points
    sv = sorted(r.real for r in mp.polyroots([4 * Tr_, -9, 6, -1]) if abs(r.imag) < 1e-20 and r.real > mp.mpf(1) / 3)
    lo, hi = max(P(sv[0]), mp.mpf("1e-12")), P(sv[1])

    def area(Pt):  # ∫ (P − Pt) dV between the outer roots of 3Pt V³ − (Pt + 8Tr)V² + 9V − 3 = 0
        r = sorted(z.real for z in mp.polyroots([3 * Pt, -(Pt + 8 * Tr_), 9, -3]) if abs(z.imag) < 1e-20)
        return mp.quad(lambda V: P(V) - Pt, [r[0], r[1], r[2]])
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if area(mid) > 0 else (lo, mid)
    Vl = None
    cases.append({"Tr": Tr, "ans": F((lo + hi) / 2)})
val("td-vdw-coexistence", "thermo.stability", "Use Maxwell's equal-area construction on the reduced van der Waals isotherm $T_r = {{Tr}}$. What is the reduced vapour pressure $P_r$?", "P_r,sat",
    "The flat coexistence line cuts the loop so the two areas between it and the isotherm are equal, which is the same as equal molar Gibbs energy (equal μ) of liquid and vapour. Iterate on P until the areas match. At $T_r = 0.9$, $P_r ≈ 0.647$",
    cases, "vdw_psat(Tr)", pace="workout")

# 7.1.A μ of ideal gases, 7.2.A–D nonideal gases
cases = []
for Tt, P1, P2, y in [(298.15, 1, 10, 1), (298.15, 1, 0.1, 1), (300, 1, 5, 0.21), (350, 2, 2, 0.5)]:
    v = R * Tt * mp.log(mp.mpf(P2) * y / P1) / 1000
    if abs(v) > 1e-9:
        cases.append({"Tt": Tt, "P1": P1, "P2": P2, "yy": y, "ans": F(v)})
val("td-mu-ideal", "thermo.phase-equilibrium", "An ideal gas at ${{Tt}}$ K goes from pure at ${{P1}}$ bar to mole fraction ${{yy}}$ in a mixture at ${{P2}}$ bar. What is Δμ (kJ/mol)?", "Δμ",
    "$\\mu_i = \\mu_i^\\circ + RT\\ln(y_iP/P^\\circ)$: pressure and dilution enter only through the partial pressure. Diluting always lowers μ, which is why gases mix spontaneously",
    cases, "c_R*nsimplify(Tt)*log(nsimplify(P2)*nsimplify(yy)/nsimplify(P1))/1000")
cases = []
for gas, B, P, Tt in [("N₂", -4.5e-6, 1e6, 300), ("CO₂", -1.2e-4, 2e6, 300), ("CH₄", -4.3e-5, 5e6, 300), ("Ar", -1.6e-5, 1e7, 300), ("He", 1.2e-5, 1e7, 300)]:
    Z = 1 + mp.mpf(B) * P / (R * Tt)
    for w, v in ((0, Z), (1, mp.exp(mp.mpf(B) * P / (R * Tt)))):
        cases.append({"gas": gas, "B": B, "P": P, "Tt": Tt, "w": w, "wt": ["compressibility factor Z", "fugacity coefficient φ"][w], "ans": F(v)})
val("td-virial", "thermo.phase-equilibrium", "With the truncated virial equation $Z = 1 + BP/RT$, $B = {{B}}$ m³/mol, find the {{wt}} of {{gas}} at ${{P}}$ Pa and ${{Tt}}$ K.", "Value",
    "$Z = 1 + BP/RT$; then $\\ln\\varphi = \\int_0^P (Z - 1)\\,dP/P = BP/RT$. Negative B (attractions win) gives Z < 1 and φ < 1; helium's positive B means repulsions win at room temperature",
    cases, "[1 + nsimplify(B)*nsimplify(P)/(c_R*Tt), ln_phi_virial(B, P, Tt)][w]")
cases = []
for sig, lam, e in [(3.4e-10, 1.5, 0.5), (3.4e-10, 1.5, 1.5), (3.0e-10, 1.0, 0.0), (3.7e-10, 1.6, 1.0)]:
    B2 = 2 * mp.pi * mp.mpf("6.02214076e23") * mp.mpf(sig) ** 3 / 3 * (1 - (mp.mpf(lam) ** 3 - 1) * (mp.e ** e - 1))
    cases.append({"sig": sig, "lam": lam, "e": e, "ans": F(B2)})
val("td-b2-square-well", "thermo.phase-equilibrium", "A square-well gas: hard core $\\sigma = {{sig}}$ m, well out to ${{lam}}\\sigma$ with depth $\\varepsilon$, $\\varepsilon/kT = {{e}}$. What is $B_2$ (m³/mol)?", "B₂",
    "$B_2 = -2\\pi N_A\\int_0^\\infty (e^{-u/kT} - 1)r^2dr = \\dfrac{2\\pi N_A\\sigma^3}{3}[1 - (\\lambda^3 - 1)(e^{\\varepsilon/kT} - 1)]$. The core gives a positive excluded volume (hard spheres: λ = 1); the well subtracts more as T falls. B₂ = 0 at the Boyle temperature",
    cases, "b2_square_well(sig, lam, e)")
cases = []
for comp, ys, Tcs, Pcs in [("70% CH₄, 30% C₂H₆", (0.7, 0.3), (190.6, 305.3), (45.99, 48.72)), ("50% N₂, 50% CO₂", (0.5, 0.5), (126.2, 304.2), (33.98, 73.83)), ("80% H₂, 20% CH₄", (0.8, 0.2), (33.2, 190.6), (13.0, 45.99))]:
    for w in (0, 1):
        v = sum(y * t for y, t in zip(ys, Tcs)) if w == 0 else sum(y * p for y, p in zip(ys, Pcs))
        cases.append({"comp": comp, "Y": list(ys), "TC": list(Tcs), "PC": list(Pcs), "w": w, "wt": ["pseudocritical temperature (K)", "pseudocritical pressure (bar)"][w],
                      "tcs": ", ".join(map(str, Tcs)), "pcs": ", ".join(map(str, Pcs)), "ans": F(mp.mpf(v))})
val("td-kay-rule", "thermo.phase-equilibrium", "By Kay's rule, what is the {{wt}} of {{comp}} (critical T: {{tcs}} K; critical P: {{pcs}} bar)?", "Value",
    "Kay's rule: mole-fraction averages, $T_{pc} = \\sum y_iT_{c,i}$, $P_{pc} = \\sum y_iP_{c,i}$. Then the reduced conditions $T/T_{pc}$, $P/P_{pc}$ go into the generalised Z chart: corresponding states for a mixture",
    cases, "[wsum(Y, TC), wsum(Y, PC)][w]")

# 9.2.A partial molar, 9.2.B Gibbs–Duhem, 9.3.C bubble/dew/flash, 9.4.B–C, 9.5.A, 9.6.A
cases = []
for Vtex, Vexp, n in [("1003 + 16.6n + 1.77n^{3/2} + 0.12n^2", "1003 + 16.6*m + 1.77*m**(3/2) + 0.12*m**2", 0.5), ("1003 + 16.6n + 1.77n^{3/2} + 0.12n^2", "1003 + 16.6*m + 1.77*m**(3/2) + 0.12*m**2", 1.0),
                      ("1000 + 20n + 3n^2", "1000 + 20*m + 3*m**2", 2.0), ("1000 + 35n - 2n^2", "1000 + 35*m - 2*m**2", 1.5)]:
    m = mp.mpf(n)
    d = mp.diff(lambda mm: eval(Vexp.replace("m", "mm"), {"mm": mm}), m)
    cases.append({"Vtex": Vtex, "Vexp": Vexp, "n": n, "ans": F(d)})
val("td-partial-molar", "thermo.solutions", "The volume (cm³) of a solution of $n$ mol of solute in 1 kg of water is $V = {{Vtex}}$. What is the solute's partial molar volume at $n = {{n}}$ (cm³/mol)?", "V̄",
    "$\\bar V_2 = (\\partial V/\\partial n_2)_{T,P,n_1}$: the slope of total V against moles of solute (the tangent-intercept idea). It can even be negative when the solute packs water tighter",
    cases, "diff(sympify(Vexp, locals={'m': Symbol('m')}), Symbol('m')).subs(Symbol('m'), nsimplify(n))")
cases = []
for A, x1 in [(1.2, 0.3), (0.8, 0.5), (2.0, 0.7), (-0.5, 0.4), (1.5, 0.9)]:
    cases.append({"A": A, "x1": x1, "ans": F(mp.e ** (mp.mpf(A) * x1**2))})
val("td-gibbs-duhem", "thermo.solutions", "A binary mixture has $\\ln\\gamma_1 = {{A}}x_2^2$. Use Gibbs–Duhem to find $\\gamma_2$ at $x_1 = {{x1}}$.", "γ₂",
    "Gibbs–Duhem: $x_1\\,d\\ln\\gamma_1 + x_2\\,d\\ln\\gamma_2 = 0$. Integrating from pure 2 gives $\\ln\\gamma_2 = Ax_1^2$: the one-parameter Margules model is symmetric. Data that fail this test are thermodynamically inconsistent",
    cases, "gamma2_from_margules(A, x1)")
cases = []
for kind, x1, P1, P2 in [(0, 0.4, 100, 40), (0, 0.7, 150, 60), (1, 0.4, 100, 40), (1, 0.6, 120, 30)]:
    v = x1 * P1 + (1 - x1) * P2 if kind == 0 else 1 / (x1 / P1 + (1 - x1) / P2)
    cases.append({"kind": kind, "x1": x1, "P1": P1, "P2": P2, "kt": ["bubble-point pressure of a liquid with", "dew-point pressure of a vapour with"][kind], "ans": F(mp.mpf(v))})
val("td-bubble-dew", "thermo.solutions", "By Raoult's law ($P_1^{sat} = {{P1}}$ kPa, $P_2^{sat} = {{P2}}$ kPa), what is the {{kt}} mole fraction ${{x1}}$ of component 1 (kPa)?", "P",
    "Bubble: $P = \\sum x_iP_i^{sat}$ (first bubble of vapour). Dew: $1/P = \\sum y_i/P_i^{sat}$ (first drop of liquid). Between them the mixture is two-phase",
    cases, "[nsimplify(x1)*P1 + (1 - nsimplify(x1))*P2, 1/(nsimplify(x1)/P1 + (1 - nsimplify(x1))/P2)][kind]")
cases = []
for z1, K1, K2 in [(0.5, 2.0, 0.5), (0.4, 3.0, 0.4), (0.6, 1.8, 0.3), (0.3, 4.0, 0.6)]:
    psi = (z1 * (K1 - 1) + (1 - z1) * (K2 - 1)) / (-(K1 - 1) * (K2 - 1))  # binary closed form
    cases.append({"z1": z1, "K1": K1, "K2": K2, "ans": F(mp.mpf(psi))})
val("td-flash", "thermo.solutions", "An isothermal flash of a binary feed with $z_1 = {{z1}}$ has $K_1 = {{K1}}$ and $K_2 = {{K2}}$. What fraction of the feed leaves as vapour?", "V/F",
    "Rachford–Rice: $\\sum \\dfrac{z_i(K_i - 1)}{1 + \\psi(K_i - 1)} = 0$. For two components it solves in closed form; then $x_i = z_i/(1 + \\psi(K_i - 1))$ and $y_i = K_ix_i$",
    cases, "flash_vf(z1, K1, K2)")
cases = []
for A, Tc_ in [(800, 0), (1200, 0), (900, 0), (500, 0)]:
    cases.append({"A": A, "ans": A / 2})
val("td-regular-solution-tc", "thermo.solutions", "A regular solution has $\\Delta G_{mix}/RT = x\\ln x + (1 - x)\\ln(1 - x) + \\chi x(1 - x)$ with $\\chi = {{A}}/T$. Below what temperature (K) does it split into two liquids?", "T_c",
    "The lattice model with nearest-neighbour exchange energy gives $\\chi = zw/kT$. Phase separation begins where $\\partial^2\\Delta G/\\partial x^2 = 0$ at $x = 1/2$: $\\chi_c = 2$, so $T_c = {{A}}/2$",
    cases, "solve(diff(log(Symbol('q')) + 0*Symbol('q'), Symbol('q')) - 0 + (2 - A/Symbol('TT')), Symbol('TT'))[0]")
T[-1]["verify"]["expect"]["y"] = "solve((1/Symbol('q') + 1/(1 - Symbol('q')) - 2*A/Symbol('TT')).subs(Symbol('q'), Rational(1, 2)), Symbol('TT'))[0]"
cases = []
for A, P1, P2 in [(1.5, 100, 80), (1.0, 120, 100), (-1.2, 100, 80), (2.0, 60, 50)]:
    x = mp.findroot(lambda x: A * (1 - x) ** 2 + mp.log(P1) - A * x**2 - mp.log(P2), 0.5)
    if 0 < x < 1:
        cases.append({"A": A, "P1": P1, "P2": P2, "ans": F(x)})
val("td-azeotrope", "thermo.solutions", "Modified Raoult's law with one-parameter Margules ($\\ln\\gamma_1 = {{A}}x_2^2$, $\\ln\\gamma_2 = {{A}}x_1^2$), $P_1^{sat} = {{P1}}$, $P_2^{sat} = {{P2}}$ kPa. At what $x_1$ is there an azeotrope?", "x₁",
    "At an azeotrope $y_1 = x_1$, so $\\gamma_1P_1^{sat} = \\gamma_2P_2^{sat}$: $\\ln(P_1^{sat}/P_2^{sat}) = A(x_1^2 - x_2^2) = A(2x_1 - 1)$. Positive A gives a maximum-pressure azeotrope, negative A a minimum",
    cases, "azeotrope_x1(A, P1, P2)")
cases = []
for kind, sol, i, conc, K in [(0, "0.10 mol/kg NaCl in water", 2, 0.10, 1.86), (0, "0.050 mol/kg CaCl₂ in water", 3, 0.050, 1.86), (1, "0.20 mol/kg glucose in water", 1, 0.20, 0.512), (2, "0.010 M glucose at 298 K", 1, 0.010, 0), (2, "0.15 M NaCl (saline) at 310 K", 2, 0.15, 0)]:
    if kind == 2:
        Tt = 298.15 if "298" in sol else 310.15
        v = i * conc * 1000 * R * Tt / 1e5
    else:
        v = i * conc * K
    cases.append({"kind": kind, "sol": sol, "i": i, "conc": conc, "K": K, "kt": ["freezing-point depression (K)", "boiling-point elevation (K)", "osmotic pressure (bar)"][kind], "ans": F(mp.mpf(v))})
val("td-colligative", "thermo.solutions", "For {{sol}} (ideal, van 't Hoff factor ${{i}}$; $K_f = 1.86$, $K_b = 0.512$ K·kg/mol), what is the {{kt}}?", "Value",
    "$\\Delta T_f = iK_fm$, $\\Delta T_b = iK_bm$, $\\Pi = icRT$: all come from lowering the solvent's chemical potential by $RT\\ln x_{solvent}$, so they count dissolved particles. Osmotic pressure is the biggest effect by far",
    cases, "[nsimplify(i)*nsimplify(conc)*nsimplify(K), nsimplify(i)*nsimplify(conc)*nsimplify(K), nsimplify(i)*nsimplify(conc)*1000*c_R*(Rational(29815, 100) if conc < 0.1 else Rational(31015, 100))/100000][kind]")
cases = []
for logK, Tt in [(2.0, 298.15), (3.5, 298.15), (-1.0, 298.15), (1.2, 310.15)]:
    cases.append({"logK": logK, "Tt": Tt, "ans": F(-R * Tt * logK * mp.log(10) / 1000)})
val("td-transfer", "thermo.solutions", "A solute's octanol/water partition coefficient is $\\log_{10}K = {{logK}}$ at ${{Tt}}$ K. What is the free energy of transfer from water to octanol (kJ/mol)?", "ΔG_transfer",
    "$\\Delta G_{w\\to o} = -RT\\ln K = -2.303RT\\log K$. Each log unit is about 5.7 kJ/mol at room temperature: the hydrophobic driving force in drug partitioning and protein folding",
    cases, "-c_R*nsimplify(Tt)*nsimplify(logK)*log(10)/1000")

# 10.2.B pressure shifts an equilibrium
cases = []
for K, P in [(1.0, 1), (1.0, 10), (0.5, 4), (4.0, 1), (0.1, 0.5)]:
    xi = mp.sqrt(K / (K + 4 * P))
    cases.append({"K": K, "P": P, "ans": F(xi)})
val("td-pressure-shift", "thermo.chemical-equilibrium", "For the ideal-gas reaction A ⇌ 2B with $K_p = {{K}}$ (bar), starting from 1 mol of pure A at ${{P}}$ bar total, what is the extent of reaction at equilibrium?", "ξ",
    "$K_p = \\dfrac{y_B^2}{y_A}P$ with $y_A = \\dfrac{1 - \\xi}{1 + \\xi}$, $y_B = \\dfrac{2\\xi}{1 + \\xi}$, giving $\\xi = \\sqrt{K/(K + 4P)}$. Raising P favours fewer gas moles (lower ξ); adding inert at fixed P acts like lowering P",
    cases, "[s for s in solve(Eq(4*Symbol('xi')**2/((1 - Symbol('xi'))*(1 + Symbol('xi')))*nsimplify(P), nsimplify(K)), Symbol('xi')) if s > 0][0]")

# 10.4.A, 11.2.E partition functions
cases = []
for qA, qB, dE in [(1e3, 2e3, 0.0), (5e2, 5e2, 2.0), (1e4, 3e3, -1.0), (2e2, 8e2, 1.5)]:
    cases.append({"qA": qA, "qB": qB, "dE": dE, "ans": F(mp.mpf(qB) / qA * mp.e ** (-dE))})
val("td-k-from-q", "stat.partition-function", "For the isomerisation A ⇌ B, the molecular partition functions (each from its own ground state) are $q_A = {{qA}}$ and $q_B = {{qB}}$, and B's ground state lies $\\Delta\\varepsilon_0 = {{dE}}\\,kT$ above A's. What is K?", "K",
    "$K = \\dfrac{q_B}{q_A}e^{-\\Delta\\varepsilon_0/kT}$: an entropy factor (how many states each side can reach) times an energy factor. A floppier isomer can win even uphill",
    cases, "nsimplify(qB)/nsimplify(qA)*exp(-nsimplify(dE))")
cases = []
for Nn, q, ind in [(100, 1e5, 1), (100, 1e5, 0), (1000, 1e8, 1), (50, 1e3, 0), (50, 1e3, 1)]:
    v = Nn * mp.log(q) - (mp.loggamma(Nn + 1) if ind else 0)
    cases.append({"Nn": Nn, "q": q, "ind": ind, "it": ["distinguishable (localized, like atoms in a crystal)", "indistinguishable (a gas)"][ind], "ans": F(v)})
val("td-big-q", "stat.partition-function", "What is $\\ln Q$ for ${{Nn}}$ {{it}} particles, each with molecular partition function $q = {{q}}$?", "ln Q",
    "Distinguishable: $Q = q^N$. Indistinguishable: $Q = q^N/N!$, dividing out the N! relabelings (use Stirling for large N). Getting this factor wrong breaks the entropy of mixing (Gibbs' paradox)",
    cases, "Nn*log(nsimplify(q)) - ind*log(factorial(Nn))")

# 12.1.C Sackur–Tetrode, 12.3.F Debye, 12.4.A–B, 12.5.A
cases = []
for gas, M, Tt, P in [("Ar", 0.039948, 298.15, 1e5), ("He", 0.0040026, 298.15, 1e5), ("Ne", 0.020180, 298.15, 1e5), ("Ar", 0.039948, 500, 1e5), ("Kr", 0.083798, 298.15, 1e5)]:
    kB, h, NA = mp.mpf("1.380649e-23"), mp.mpf("6.62607015e-34"), mp.mpf("6.02214076e23")
    m = M / NA
    lam = h / mp.sqrt(2 * mp.pi * m * kB * Tt)
    S = R * (mp.log(kB * Tt / (P * lam**3)) + mp.mpf(5) / 2)
    cases.append({"gas": gas, "M": M, "Tt": Tt, "P": P, "ans": F(S)})
val("td-sackur-tetrode", "stat.ideal-gas", "Use the Sackur–Tetrode equation to find the molar entropy of {{gas}} ($M = {{M}}$ kg/mol) at ${{Tt}}$ K and ${{P}}$ Pa (J/mol·K).", "S_m",
    "$S = R\\left[\\ln\\dfrac{kT}{P\\Lambda^3} + \\dfrac52\\right]$, $\\Lambda = h/\\sqrt{2\\pi mkT}$, from $Q = q^N/N!$ with translational q. Argon at 298 K, 1 bar: 154.8 J/mol·K, matching calorimetry",
    cases, "c_R*(log(c_kB*nsimplify(Tt)/(nsimplify(P)*(c_h/sqrt(2*pi*nsimplify(M)/c_NA*c_kB*nsimplify(Tt)))**3)) + Rational(5, 2))")
cases = []
for sol, Tt, th in [("copper", 10, 343), ("diamond", 20, 2230), ("lead", 5, 105), ("aluminium", 15, 428)]:
    cases.append({"sol": sol, "Tt": Tt, "th": th, "ans": F(mp.mpf(12) * mp.pi**4 / 5 * R * (mp.mpf(Tt) / th) ** 3)})
val("td-debye-t3", "stat.heat-capacity", "Debye temperature of {{sol}}: ${{th}}$ K. Use the Debye $T^3$ law for its molar heat capacity at ${{Tt}}$ K (J/mol·K).", "C_V",
    "$C_V = \\dfrac{12\\pi^4}{5}R\\left(\\dfrac{T}{\\Theta_D}\\right)^3$ for $T \\ll \\Theta_D$. Long-wavelength phonons can always be excited, so C_V falls as T³; Einstein's single frequency gives an exponential fall, far too fast",
    cases, "Rational(12, 5)*pi**4*c_R*Rational(Tt, th)**3")
cases = []
for gas, M, Tt in [("N₂", 0.028014, 298.15), ("He", 0.0040026, 298.15), ("O₂", 0.031998, 500), ("CO₂", 0.04401, 300)]:
    a = M / (2 * R * Tt)
    for w, v in ((0, mp.sqrt(1 / a)), (1, mp.sqrt(8 * R * Tt / (mp.pi * M))), (2, mp.sqrt(3 * R * Tt / M))):
        cases.append({"gas": gas, "M": M, "Tt": Tt, "w": w, "wt": ["most probable", "mean", "root-mean-square"][w], "ans": F(v)})
val("td-maxwell-speeds", "stat.ideal-gas", "What is the {{wt}} speed of {{gas}} molecules ($M = {{M}}$ kg/mol) at ${{Tt}}$ K (m/s)?", "Speed",
    "From $f(v) \\propto v^2e^{-Mv^2/2RT}$: $v_{mp} = \\sqrt{2RT/M}$ (the peak), $\\bar v = \\sqrt{8RT/\\pi M}$, $v_{rms} = \\sqrt{3RT/M}$, in the ratio 1 : 1.128 : 1.225",
    cases, "maxwell_speed(M, Tt, w)")
cases = [{"r": r, "ans": r} for r in (1, 2, 5, 10, 0.5)]
val("td-classical-q", "stat.partition-function", "Classically, $q = \\dfrac{1}{h}\\iint e^{-\\beta H}\\,dx\\,dp$. For a 1-D harmonic oscillator with $kT/\\hbar\\omega = {{r}}$, what is q?", "q",
    "Both integrals are Gaussian: $\\int e^{-\\beta p^2/2m}dp = \\sqrt{2\\pi m/\\beta}$, $\\int e^{-\\beta m\\omega^2x^2/2}dx = \\sqrt{2\\pi/\\beta m\\omega^2}$, so $q = kT/\\hbar\\omega$: equipartition gives kT of energy. The quantum $q$ approaches this when $kT \\gg \\hbar\\omega$",
    cases, "ho_classical_q(r)")
cases = []
for kind, a, Tt, W, sub in [(0, 1e-5, 15, 1, "a solid whose $C_p = aT^3$ with $a = $ 1e-5 J/mol·K⁴ below 15 K"), (0, 2e-4, 10, 1, "a solid with $C_p = aT^3$, a = 2e-4 J/mol·K⁴, up to 10 K"),
                            (1, 0, 0, 2, "crystalline CO (each molecule frozen in one of 2 orientations)"), (1, 0, 0, 1.5, "ice (Pauling's count, W = (3/2)^N)")]:
    v = mp.mpf(a) * Tt**3 / 3 if kind == 0 else R * mp.log(W)
    cases.append({"kind": kind, "a": a, "Tt": Tt, "W": W, "sub": sub, "ans": F(v)})
val("td-third-law", "stat.heat-capacity", "What molar entropy (J/mol·K) does the third law assign to {{sub}}?", "S",
    "Absolute entropy: $S(T) = \\int_0^T C_p/T\\,dT$ (+ phase changes), and with $C_p = aT^3$ that is $aT^3/3$. A disordered crystal keeps a residual entropy $R\\ln W$ per mole at 0 K: R ln 2 = 5.76 for CO, R ln 1.5 = 3.37 for ice",
    cases, "[integrate(nsimplify(a)*Symbol('TT')**2, (Symbol('TT'), 0, Tt)), c_R*log(nsimplify(W))][kind]")

# 14.3.A Gibbs entropy
cases = []
for ps in [(0.5, 0.5), (0.25, 0.25, 0.25, 0.25), (0.7, 0.2, 0.1), (0.9, 0.1), (0.5, 0.25, 0.25)]:
    cases.append({"pt": ", ".join(map(str, ps)), "P": list(ps), "ans": F(-sum(mp.mpf(p) * mp.log(p) for p in ps))})
val("td-gibbs-entropy", "stat.ensembles", "A system occupies microstates with probabilities {{pt}}. What is its entropy in units of k?", "S/k",
    "Gibbs: $S = -k\\sum p_i\\ln p_i$. For W equally likely states it is $k\\ln W$ (Boltzmann); any bias lowers it. Maximising it with constraints gives each ensemble: fixed ⟨E⟩ gives the Boltzmann distribution",
    cases, "gibbs_S(P)")

# 15.2.D Ising
cases = []
for bJ, bh in [(0.5, 0), (1.0, 0), (0.2, 0.3), (0.5, 0.5), (-0.5, 0.2)]:
    lam = mp.e**bJ * mp.cosh(bh) + mp.sqrt(mp.e ** (2 * bJ) * mp.sinh(bh) ** 2 + mp.e ** (-2 * bJ))
    cases.append({"bJ": bJ, "bh": bh, "ans": F(mp.log(lam))})
val("td-ising-1d", "stat.binding", "1-D Ising chain with $\\beta J = {{bJ}}$ and $\\beta h = {{bh}}$. With the transfer matrix, what is $-\\beta f = \\lim \\frac{1}{N}\\ln Z$?", "ln λ₊",
    "$Z = \\operatorname{Tr}T^N \\approx \\lambda_+^N$ with $T = \\begin{pmatrix} e^{\\beta(J+h)} & e^{-\\beta J} \\\\ e^{-\\beta J} & e^{\\beta(J-h)}\\end{pmatrix}$, $\\lambda_+ = e^{\\beta J}\\cosh\\beta h + \\sqrt{e^{2\\beta J}\\sinh^2\\beta h + e^{-2\\beta J}}$. At h = 0, $\\lambda_+ = 2\\cosh\\beta J$: no phase transition in 1-D",
    cases, "ising_ln_lambda(bJ, bh)")
cases = [{"z": z, "J": J, "ans": F(mp.mpf(z) * J / mp.mpf("1.380649e-23"))} for z, J in [(4, 1e-21), (6, 2e-21), (8, 5e-22), (6, 1.5e-21)]]
val("td-mean-field-tc", "stat.binding", "In mean-field theory, what is the Curie temperature (K) of an Ising magnet with coordination number ${{z}}$ and coupling $J = {{J}}$ J?", "T_c",
    "Mean field replaces neighbours by their average: $m = \\tanh(\\beta zJm)$, which has a nonzero solution when $\\beta zJ > 1$, so $kT_c = zJ$. It overestimates T_c (the 2-D square lattice exact value is about 0.57 zJ/k) and wrongly predicts a transition in 1-D",
    cases, "z*nsimplify(J)/c_kB")

# 16.2.C detailed balance
cases = []
for kf, dG, Tt in [(1e3, -10, 298.15), (5e2, 5, 298.15), (1e6, -20, 310.15), (2.0, 0.0, 298.15)]:
    K = mp.e ** (-dG * 1000 / (R * Tt))
    cases.append({"kf": kf, "dG": dG, "Tt": Tt, "ans": F(kf / K)})
val("td-detailed-balance", "stat.rates", "A reaction A ⇌ B has $k_f = {{kf}}$ s⁻¹ and $\\Delta G^\\circ = {{dG}}$ kJ/mol at ${{Tt}}$ K. What is $k_r$ (s⁻¹)?", "k_r",
    "At equilibrium the forward and reverse fluxes balance: $k_f/k_r = K = e^{-\\Delta G^\\circ/RT}$. On a free-energy profile the reverse barrier is higher by ΔG°, so $k_r = k_f/K$",
    cases, "nsimplify(kf)/exp(-nsimplify(dG)*1000/(c_R*nsimplify(Tt)))")

# 17.1.A Debye–Hückel, 17.2.A Flory–Huggins, 17.3.A Metropolis
cases = []
for sol, cs, zs, zp, zm in [("0.010 m NaCl", (0.01, 0.01), (1, -1), 1, 1), ("0.005 m CaCl₂", (0.005, 0.01), (2, -1), 2, 1), ("0.001 m MgSO₄", (0.001, 0.001), (2, -2), 2, 2), ("0.002 m Na₂SO₄", (0.004, 0.002), (1, -2), 1, 2)]:
    I = mp.mpf(1) / 2 * sum(c * z * z for c, z in zip(cs, zs))
    cases.append({"sol": sol, "C": list(cs), "Zs": list(zs), "zp": zp, "zm": zm, "ans": F(10 ** (-mp.mpf("0.509") * zp * zm * mp.sqrt(I)))})
val("td-debye-huckel", "thermo.chemical-equilibrium", "Use the Debye–Hückel limiting law ($\\log_{10}\\gamma_\\pm = -0.509|z_+z_-|\\sqrt I$ at 25 °C) for {{sol}}. What is $\\gamma_\\pm$?", "γ±",
    "Ionic strength $I = \\tfrac12\\sum c_iz_i^2$ (count every ion, including the 2 Cl⁻ of CaCl₂). Highly charged ions deviate fastest. Valid only below about 0.01 m",
    cases, "10**(-Rational('0.509')*zp*zm*sqrt(ionic_strength(C, Zs)))")
cases = [{"Nn": n, "ans": F(mp.mpf(1) / 2 * (1 + 1 / mp.sqrt(n)) ** 2)} for n in (1, 100, 1000, 10000, 50)]
val("td-flory-huggins", "thermo.solutions", "In Flory–Huggins theory, what is the critical $\\chi$ for a polymer of ${{Nn}}$ segments in a small-molecule solvent?", "χ_c",
    "$\\Delta G_{mix}/kT = \\frac{\\phi}{N}\\ln\\phi + (1 - \\phi)\\ln(1 - \\phi) + \\chi\\phi(1 - \\phi)$; the critical point (second and third derivatives zero) gives $\\chi_c = \\tfrac12(1 + 1/\\sqrt N)^2$, at $\\phi_c = 1/(1 + \\sqrt N)$. Long chains demix at χ just above ½; N = 1 recovers the regular solution's 2",
    cases, "fh_chi_c(Nn)")
cases = [{"dE": dE, "ans": F(min(mp.mpf(1), mp.e ** (-dE)))} for dE in (0.5, 1.0, 2.0, 3.0, 0.1)]
val("td-metropolis", "stat.ensembles", "A Metropolis Monte Carlo move raises the energy by $\\Delta E = {{dE}}\\,kT$. With what probability is it accepted?", "Acceptance",
    "$p_{acc} = \\min(1, e^{-\\beta\\Delta E})$: downhill always, uphill with the Boltzmann factor. That rule satisfies detailed balance, so the chain samples the canonical ensemble; averages over the sampled states are ensemble averages",
    cases, "Min(1, exp(-nsimplify(dE)))")


def dump():
    head = "# " + "\n# ".join(__doc__.strip().splitlines()) + "\n# GENERATED: edit scripts/td_cases.py, not this file.\n\n"
    OUT.write_text(head + yaml.dump(T, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=None))
    print(f"{len(T)} templates, {sum(len(t['cases']) for t in T)} cases -> {OUT}")


if __name__ == "__main__":
    dump()
