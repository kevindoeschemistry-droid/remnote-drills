"""Builds drills/problems/ht-final.yaml: the heat and mass transfer problem types the MAE 120 grid
(drills/matrices/heat-transfer.yaml) found open. Run: python3 scripts/ht_final_cases.py

Answers here follow the textbook route (Incropera Table 3.4 fin formulas, the one-term C1 formula,
the closed-form radiation-cooling time, the tabulated FD node equations). tests/verify/htcalc.py
checks each a different way (dsolve on the fin ODE, orthogonality integrals, numerical integration
of the cooling ODE, a control-volume balance per node).
"""
from pathlib import Path

import mpmath as mp
import yaml

mp.mp.dps = 30
OUT = Path(__file__).resolve().parent.parent / "drills/problems/ht-final.yaml"
SIG = mp.mpf("5.670374419e-8")
T = []


def F(v, d=10):
    return float(mp.nstr(v, d))


def tpl(name, skill, prompt, ask, unit, explain, cases, verify, tol=0.002, pace="quick"):
    T.append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
              "parts": [{"ask": f"{ask} ({unit})" if unit else ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}],
              "verify": {"expect": {"y": verify}}})


# ── fins: convective tip, prescribed tip temperature, effectiveness ──────────
def fin_A(h, k, D, L, th):
    P, Ac = mp.pi * D, mp.pi * D**2 / 4
    m = mp.sqrt(h * P / (k * Ac))
    M = mp.sqrt(h * P * k * Ac) * th
    r = h / (m * k)
    q = M * (mp.sinh(m * L) + r * mp.cosh(m * L)) / (mp.cosh(m * L) + r * mp.sinh(m * L))
    tip = th / (mp.cosh(m * L) + r * mp.sinh(m * L))
    return m, M, q, tip


rows = [("copper", 398, 5e-3, 0.05, 100, 100, 25), ("aluminium", 180, 10e-3, 0.08, 25, 80, 20), ("stainless steel", 15, 6e-3, 0.04, 30, 120, 20),
        ("brass", 110, 8e-3, 0.10, 40, 90, 25), ("carbon steel", 60, 10e-3, 0.05, 50, 150, 30)]
cases = []
for mat, k, D, L, h, Tb, Ti in rows:
    m, M, q, tip = fin_A(mp.mpf(h), mp.mpf(k), mp.mpf(D), mp.mpf(L), mp.mpf(Tb - Ti))
    for what, val in ((0, q), (1, tip + Ti)):
        cases.append({"mat": mat, "k": k, "D": D * 1000, "L": L * 1000, "h": h, "Tb": Tb, "Ti": Ti, "w": what, "wt": ["the fin heat rate", "the tip temperature"][what], "ans": F(val)})
tpl("ht-fin-conv-tip", "ht.fins",
    "A {{D}}-mm-diameter {{mat}} pin fin ($k = {{k}}$ W/m·K), {{L}} mm long, has its base at ${{Tb}}$ °C in fluid at ${{Ti}}$ °C with $h = {{h}}$ W/m²·K. With convection from the tip (the exact case, not the corrected length), find {{wt}}.",
    "Answer", "W or °C",
    "Case A: $q_f = M\\dfrac{\\sinh mL + (h/mk)\\cosh mL}{\\cosh mL + (h/mk)\\sinh mL}$, $\\theta_L/\\theta_b = 1/[\\cosh mL + (h/mk)\\sinh mL]$, with $m = \\sqrt{hP/kA_c}$, $M = \\sqrt{hPkA_c}\\,\\theta_b$, $P = \\pi D$, $A_c = \\pi D^2/4$. The corrected length $L_c = L + D/4$ in the adiabatic formula gives nearly the same heat rate",
    cases, "fin_q(0, h, k, D/1000, L/1000, Tb, Ti, 0, w)")

cases = []
for mat, k, D, L, h, Tb, Ti, TL in [("copper", 398, 5e-3, 0.10, 100, 100, 25, 40), ("aluminium", 180, 6e-3, 0.15, 50, 120, 20, 60),
                                     ("brass", 110, 5e-3, 0.12, 30, 90, 20, 50), ("carbon steel", 60, 8e-3, 0.20, 40, 150, 25, 80)]:
    P, Ac = mp.pi * D, mp.pi * D**2 / 4
    m = mp.sqrt(h * P / (k * Ac))
    M = mp.sqrt(h * P * k * Ac) * (Tb - Ti)
    q = M * (mp.cosh(m * L) - mp.mpf(TL - Ti) / (Tb - Ti)) / mp.sinh(m * L)
    cases.append({"mat": mat, "k": k, "D": D * 1000, "L": L * 1000, "h": h, "Tb": Tb, "Ti": Ti, "TL": TL, "ans": F(q)})
tpl("ht-fin-fixed-tip", "ht.fins",
    "A {{D}}-mm {{mat}} rod ($k = {{k}}$ W/m·K), {{L}} mm long, spans between a wall at ${{Tb}}$ °C and a second wall that holds its far end at ${{TL}}$ °C. Air at ${{Ti}}$ °C, $h = {{h}}$ W/m²·K. What heat rate leaves the first wall into the rod?",
    "Heat rate", "W",
    "Case C (prescribed tip temperature): $q_f = M\\dfrac{\\cosh mL - \\theta_L/\\theta_b}{\\sinh mL}$, with $\\theta = T - T_\\infty$. Check: as $L \\to \\infty$ it becomes $M$, the infinite fin",
    cases, "fin_q(1, h, k, D/1000, L/1000, Tb, Ti, TL, 0)")

cases = []
for mat, k, D, L, h in [("aluminium", 180, 5e-3, 0.05, 30), ("stainless steel", 15, 5e-3, 0.05, 30), ("copper", 398, 3e-3, 0.03, 100),
                        ("aluminium", 180, 10e-3, 0.05, 500), ("plastic", 0.2, 5e-3, 0.02, 30)]:
    _, _, q, _ = fin_A(mp.mpf(h), mp.mpf(k), mp.mpf(D), mp.mpf(L), mp.mpf(1))
    eff = q / (h * mp.pi * D**2 / 4 * 1)
    cases.append({"mat": mat, "k": k, "D": D * 1000, "L": L * 1000, "h": h, "ans": F(eff)})
tpl("ht-fin-effectiveness", "ht.fins",
    "What is the effectiveness of a {{D}}-mm-diameter, {{L}}-mm {{mat}} pin fin ($k = {{k}}$ W/m·K) in a fluid with $h = {{h}}$ W/m²·K (tip convecting)?",
    "Effectiveness", "",
    "$\\varepsilon_f = q_f/(hA_{c,b}\\theta_b)$: the heat rate with the fin over the rate from the bare base. Fins pay off when $\\varepsilon_f \\ge 2$, which needs high $k$ and low $h$: a poor conductor or a boiling liquid makes a fin nearly useless",
    cases, "fin_q(0, h, k, D/1000, L/1000, 1, 0, 0, 2)")

# ── one-term: cylinder and sphere surface temperature and energy ─────────────
def one_term(geom, Bi, Fo, r, what):
    Bi = mp.mpf(Bi)
    if geom == 1:
        z = mp.findroot(lambda z: z * mp.besselj(1, z) - Bi * mp.besselj(0, z), (0.01, 2.40), solver="anderson")
        C1 = 2 / z * mp.besselj(1, z) / (mp.besselj(0, z) ** 2 + mp.besselj(1, z) ** 2)
        th0 = C1 * mp.exp(-z**2 * Fo)
        return th0 * mp.besselj(0, z * r) if what == 0 else 1 - 2 * th0 / z * mp.besselj(1, z)
    z = mp.findroot(lambda z: (1 - Bi) * mp.sin(z) - z * mp.cos(z), (0.01, 3.14), solver="anderson")
    C1 = 4 * (mp.sin(z) - z * mp.cos(z)) / (2 * z - mp.sin(2 * z))
    th0 = C1 * mp.exp(-z**2 * Fo)
    if what == 0:
        return th0 * (mp.sin(z * r) / (z * r) if r else 1)
    return 1 - 3 * th0 / z**3 * (mp.sin(z) - z * mp.cos(z))


cases = []
for g, Bi, Fo, r, what in [(1, 1.0, 0.5, 1, 0), (1, 2.0, 0.3, 1, 0), (1, 0.5, 0.8, 1, 1), (1, 5.0, 0.4, 1, 1), (1, 1.0, 0.5, 0.5, 0),
                           (2, 1.0, 0.5, 1, 0), (2, 2.0, 0.3, 1, 0), (2, 0.5, 0.8, 1, 1), (2, 5.0, 0.4, 1, 1), (2, 1.0, 0.5, 0.5, 0)]:
    v = one_term(g, Bi, mp.mpf(Fo), mp.mpf(r), what)
    cases.append({"g": g, "gt": ["", "long cylinder", "sphere"][g], "Bi": Bi, "Fo": Fo, "r": r, "w": what,
                  "wt": ["the dimensionless temperature θ* = (T − T∞)/(Ti − T∞) at r/ro = " + str(r), "the fraction of the maximum energy transferred, Q/Q₀"][what], "ans": F(v)})
tpl("ht-ot-radial-more", "ht.transient-one-term",
    "A {{gt}} with Bi = $hr_o/k = {{Bi}}$ is plunged into a fluid. At Fo = $\\alpha t/r_o^2 = {{Fo}}$, use the one-term approximation to find {{wt}}.",
    "Value", "",
    "Find $\\zeta_1$ and $C_1$ for the Bi (cylinder: $\\zeta J_1(\\zeta)/J_0(\\zeta) = \\text{Bi}$; sphere: $1 - \\zeta\\cot\\zeta = \\text{Bi}$), $\\theta_0^* = C_1e^{-\\zeta_1^2\\text{Fo}}$. Off-centre: cylinder $\\theta^* = \\theta_0^*J_0(\\zeta_1r^*)$, sphere $\\theta_0^*\\sin(\\zeta_1r^*)/(\\zeta_1r^*)$. Energy: cylinder $Q/Q_0 = 1 - \\frac{2\\theta_0^*}{\\zeta_1}J_1(\\zeta_1)$, sphere $1 - \\frac{3\\theta_0^*}{\\zeta_1^3}[\\sin\\zeta_1 - \\zeta_1\\cos\\zeta_1]$",
    cases, "one_term(g, Bi, Fo, r, w)")

# ── semi-infinite: constant surface flux, surface convection ─────────────────
mats = {"steel": (60, 1.7e-5), "concrete": (1.4, 6.9e-7), "oak": (0.17, 1.31e-7), "soil": (0.52, 1.38e-7)}
cases = []
for mat, q0, t, x, Ti in [("steel", 2e4, 600, 0.01, 20), ("concrete", 1000, 3600, 0.02, 15), ("soil", 500, 7200, 0.05, 10), ("steel", 5e4, 120, 0.0, 25)]:
    k, a = mats[mat]
    s = mp.sqrt(a * t)
    Tx = Ti + 2 * q0 * s / (k * mp.sqrt(mp.pi)) * mp.exp(-x**2 / (4 * a * t)) - q0 * x / k * mp.erfc(x / (2 * s))
    cases.append({"mat": mat, "k": k, "al": a, "q0": q0, "t": t, "xp": x * 1000, "Ti": Ti, "ans": F(Tx)})
tpl("ht-erf-const-flux", "ht.semi-infinite",
    "A thick {{mat}} block ($k = {{k}}$ W/m·K, $\\alpha = {{al}}$ m²/s) at ${{Ti}}$ °C suddenly receives a constant surface heat flux of ${{q0}}$ W/m². What is the temperature {{xp}} mm below the surface after ${{t}}$ s?",
    "Temperature", "°C",
    "Case 2 (constant flux): $T - T_i = \\dfrac{2q_0''\\sqrt{\\alpha t/\\pi}}{k}e^{-x^2/4\\alpha t} - \\dfrac{q_0''x}{k}\\operatorname{erfc}\\dfrac{x}{2\\sqrt{\\alpha t}}$. At the surface only the first term survives, so $T_s$ grows like $\\sqrt t$",
    cases, "semi_flux_T(q0, k, al, t, xp/1000, Ti)")

cases = []
for mat, h, t, x, Ti, Tinf in [("concrete", 25, 3600, 0.0, 20, 80), ("concrete", 25, 3600, 0.02, 20, 80), ("soil", 50, 36000, 0.05, 15, -10),
                               ("oak", 10, 600, 0.0, 20, 400), ("steel", 500, 60, 0.005, 25, 300)]:
    k, a = mats[mat]
    s = mp.sqrt(a * t)
    eta = x / (2 * s)
    fr = mp.erfc(eta) - mp.exp(h * x / k + h**2 * a * t / k**2) * mp.erfc(eta + h * s / k)
    cases.append({"mat": mat, "k": k, "al": a, "h": h, "t": t, "xp": x * 1000, "Ti": Ti, "Tinf": Tinf, "ans": F(Ti + (Tinf - Ti) * fr)})
tpl("ht-erf-convection", "ht.semi-infinite",
    "A thick {{mat}} block ($k = {{k}}$ W/m·K, $\\alpha = {{al}}$ m²/s) at ${{Ti}}$ °C is suddenly exposed to fluid at ${{Tinf}}$ °C with $h = {{h}}$ W/m²·K. What is the temperature {{xp}} mm below the surface after ${{t}}$ s?",
    "Temperature", "°C",
    "Case 3 (surface convection): $\\dfrac{T - T_i}{T_\\infty - T_i} = \\operatorname{erfc}\\eta - \\exp\\!\\left(\\dfrac{hx}{k} + \\dfrac{h^2\\alpha t}{k^2}\\right)\\operatorname{erfc}\\!\\left(\\eta + \\dfrac{h\\sqrt{\\alpha t}}{k}\\right)$, $\\eta = x/2\\sqrt{\\alpha t}$. As $h \\to \\infty$ it becomes the fixed-surface case",
    cases, "semi_conv_T(h, k, al, t, xp/1000, Ti, Tinf)")

# ── lumped capacitance cooled by radiation alone ─────────────────────────────
cases = []
for what, rho, c, VA, eps, Ti, Tf, Ts in [("a 2-mm aluminium sheet radiating from both faces in space", 2700, 900, 0.001, 0.25, 500, 300, 0),
                                          ("a 10-mm steel sphere in a vacuum furnace", 7800, 470, 0.01 / 6, 0.8, 1100, 600, 300),
                                          ("a thin copper plate (V/A = 0.5 mm) in a cold vacuum chamber", 8900, 385, 0.0005, 0.6, 600, 400, 77),
                                          ("a 4-mm steel plate cooling from both faces to cold surroundings", 7800, 470, 0.002, 0.9, 900, 400, 300)]:
    Ti_, Tf_, Ts_ = mp.mpf(Ti), mp.mpf(Tf), mp.mpf(Ts)
    if Ts == 0:
        t = rho * c * VA / (3 * eps * SIG) * (1 / Tf_**3 - 1 / Ti_**3)
    else:
        t = rho * c * VA / (4 * eps * SIG * Ts_**3) * (mp.log(abs((Ts_ + Tf_) / (Ts_ - Tf_))) - mp.log(abs((Ts_ + Ti_) / (Ts_ - Ti_)))
                                                          + 2 * (mp.atan(Tf_ / Ts_) - mp.atan(Ti_ / Ts_)))
    cases.append({"what": what, "rho": rho, "c": c, "VA": VA, "eps": eps, "Ti": Ti, "Tf": Tf, "Ts": Ts, "ans": F(t)})
tpl("ht-lumped-radiation", "ht.lumped",
    "Find the time for {{what}} ($\\rho = {{rho}}$ kg/m³, $c = {{c}}$ J/kg·K, $V/A_s = {{VA}}$ m, $\\varepsilon = {{eps}}$) to cool from ${{Ti}}$ K to ${{Tf}}$ K by radiation alone, surroundings at ${{Ts}}$ K.",
    "Time", "s",
    "Lumped balance $\\rho Vc\\,dT/dt = -\\varepsilon\\sigma A_s(T^4 - T_{sur}^4)$, nonlinear. With $T_{sur} = 0$: $t = \\dfrac{\\rho Vc}{3\\varepsilon A_s\\sigma}\\left(\\dfrac{1}{T^3} - \\dfrac{1}{T_i^3}\\right)$; otherwise Incropera's closed form with ln and arctan terms. Kelvin throughout",
    cases, "lumped_rad_time(rho, c, VA, eps, Ti, Tf, Ts)")

# ── surfaces: solar and combined convection + radiation balances ─────────────
cases = []
for what, qin, h, Tinf, eps, Tsur in [("a roof (solar absorptivity 0.6, ε = 0.9) under 800 W/m² of sun, sky at 260 K", 480, 10, 300, 0.9, 260),
                                      ("a white-painted roof (solar absorptivity 0.2, ε = 0.9) under 800 W/m², sky at 260 K", 160, 10, 300, 0.9, 260),
                                      ("an electronics panel dissipating 1000 W/m² from one face", 1000, 15, 298, 0.8, 298),
                                      ("a heater plate supplying 2000 W/m² in still air", 2000, 8, 300, 0.5, 300),
                                      ("a solar collector plate absorbing 600 W/m² with little convection", 600, 3, 290, 0.1, 280)]:
    def bal(T):
        return qin - h * (T - Tinf) - eps * SIG * (T**4 - Tsur**4)
    T0 = mp.findroot(bal, 400)
    cases.append({"what": what, "qin": qin, "h": h, "Tinf": Tinf, "eps": eps, "Tsur": Tsur, "ans": F(T0)})
tpl("ht-surface-balance", "ht.enclosures",
    "Steady state: {{what}} absorbs ${{qin}}$ W/m² and loses heat by convection ($h = {{h}}$ W/m²·K to air at ${{Tinf}}$ K) and by radiation ($\\varepsilon = {{eps}}$, surroundings at ${{Tsur}}$ K), back insulated. What is its temperature?",
    "Temperature", "K",
    "Surface energy balance: $q''_{in} = h(T - T_\\infty) + \\varepsilon\\sigma(T^4 - T_{sur}^4)$, solved by iteration (guess, update, repeat). Solar gain uses the solar absorptivity $\\alpha_S$; emission uses the long-wave $\\varepsilon$, which is why white paint keeps a roof cool",
    cases, "surface_T(qin, h, Tinf, eps, Tsur)", tol=0.001)

# ── finite-difference boundary nodes ────────────────────────────────────────
cases = []
for kind, a, b, c, d, Bi, Tinf, kt in [(0, 100, 80, 90, 0, 0.5, 20, "on a plane surface exposed to convection; inside neighbour at 100 °C, neighbours along the surface at 80 and 90 °C"),
                                       (0, 150, 140, 120, 0, 2, 25, "on a plane surface exposed to convection; inside neighbour at 150 °C, neighbours along the surface at 140 and 120 °C"),
                                       (1, 60, 80, 0, 0, 0.5, 20, "at an external corner with convection on both faces; neighbours at 60 and 80 °C"),
                                       (2, 100, 120, 70, 90, 1, 30, "at an internal (re-entrant) corner with convection; full-cell neighbours at 100 and 120 °C, half-cell neighbours along the exposed faces at 70 and 90 °C"),
                                       (3, 100, 80, 90, 0, 0, 0, "on an insulated plane surface; inside neighbour at 100 °C, neighbours along the surface at 80 and 90 °C"),
                                       (3, 50, 60, 40, 0, 0, 0, "on an insulated plane surface; inside neighbour at 50 °C, neighbours along the surface at 60 and 40 °C")]:
    if kind == 0:
        Tn = (2 * a + b + c + 2 * Bi * Tinf) / (2 * (Bi + 2))
    elif kind == 1:
        Tn = (a + b + 2 * Bi * Tinf) / (2 * (Bi + 1))
    elif kind == 2:
        Tn = (2 * (a + b) + (c + d) + 2 * Bi * Tinf) / (2 * (3 + Bi))
    else:
        Tn = (2 * a + b + c) / 4
    cases.append({"kind": kind, "a": a, "b": b, "c": c, "d": d, "Bi": Bi, "Tinf": Tinf, "kt": kt, "ans": F(mp.mpf(Tn))})
tpl("ht-fd-boundary-node", "ht.finite-difference",
    "Steady 2-D conduction, square grid, no generation, $h\\Delta x/k = {{Bi}}$, fluid at ${{Tinf}}$ °C where there is convection. A node sits {{kt}}. What is its temperature?",
    "Temperature", "°C",
    "Write the energy balance on the node's own cell: full faces conduct $k\\Delta y$, faces of a half cell $k\\Delta y/2$, exposed faces convect $h\\ell(T_\\infty - T)$. Plane convective surface: $2T_{in} + T_a + T_b + 2\\text{Bi}T_\\infty - 2(\\text{Bi} + 2)T = 0$; external corner: $T_a + T_b + 2\\text{Bi}T_\\infty - 2(\\text{Bi} + 1)T = 0$; internal corner: $2(T_1 + T_2) + T_3 + T_4 + 2\\text{Bi}T_\\infty - 2(3 + \\text{Bi})T = 0$; insulated: a mirror node",
    cases, "fd_node(kind, a, b, c, d, Bi, Tinf)", tol=0.0001)

# ── internal flow with an external fluid; fouling ───────────────────────────
cases = []
for Tmi, Tinf, U, D, L, md, cp in [(80, 20, 25, 0.05, 10, 0.05, 4180), (150, 25, 10, 0.1, 30, 0.2, 1010), (5, 30, 50, 0.025, 5, 0.02, 4180), (60, 0, 15, 0.08, 20, 0.1, 4180)]:
    As = mp.pi * D * L
    Tmo = Tinf - (Tinf - Tmi) * mp.exp(-U * As / (md * cp))
    cases.append({"Tmi": Tmi, "Tinf": Tinf, "U": U, "D": D * 1000, "L": L, "md": md, "cp": cp, "ans": F(Tmo)})
tpl("ht-tube-external-fluid", "ht.internal-flow",
    "Fluid ($c_p = {{cp}}$ J/kg·K) enters a {{D}}-mm tube, {{L}} m long, at ${{Tmi}}$ °C and ${{md}}$ kg/s. The tube sits in surroundings at ${{Tinf}}$ °C with an overall coefficient $U = {{U}}$ W/m²·K (inside, wall and outside together). What is the outlet temperature?",
    "Outlet temperature", "°C",
    "With an external fluid instead of a fixed wall temperature: $\\dfrac{T_\\infty - T_{m,o}}{T_\\infty - T_{m,i}} = \\exp\\!\\left(-\\dfrac{\\bar UA_s}{\\dot mc_p}\\right)$, the constant-$T_s$ result with $T_\\infty$ and $U$ in place of $T_s$ and $h$",
    cases, "N(Tinf) - (N(Tinf) - N(Tmi))*exp(-N(U)*pi*N(D)/1000*N(L)/(N(md)*N(cp)))".replace("N(", "nsimplify("))

cases = []
for hi, ho, Rfi, Rfo, Rw in [(1000, 500, 0.0002, 0.0001, 0.0), (5000, 2000, 0.0001, 0.0001, 1e-5), (200, 50, 0.0004, 0.0, 0.0), (3000, 3000, 0.0002, 0.0002, 2e-5)]:
    U = 1 / (1 / mp.mpf(hi) + Rfi + Rw + Rfo + 1 / mp.mpf(ho))
    cases.append({"hi": hi, "ho": ho, "Rfi": Rfi, "Rfo": Rfo, "Rw": Rw, "ans": F(U)})
tpl("ht-U-fouling", "ht.heat-exchangers",
    "A thin-walled exchanger tube: $h_i = {{hi}}$ and $h_o = {{ho}}$ W/m²·K, fouling factors $R''_{f,i} = {{Rfi}}$ and $R''_{f,o} = {{Rfo}}$ m²·K/W, wall resistance ${{Rw}}$ m²·K/W. What is the overall coefficient $U$?",
    "U", "W/m²·K",
    "Thin wall, so areas are equal and resistances per area add in series: $1/U = 1/h_i + R''_{f,i} + R''_w + R''_{f,o} + 1/h_o$. Fouling grows in service; design with it, and note it matters most when both h are large",
    cases, "1/(1/nsimplify(hi) + nsimplify(Rfi) + nsimplify(Rw) + nsimplify(Rfo) + 1/nsimplify(ho))")

# ── transient mass diffusion ────────────────────────────────────────────────
cases = []
for what, Cs, Ci, C, x, D in [("carbon into steel (carburizing): surface held at 1.2 wt% C, initially 0.2 wt%; reach 0.8 wt%", 1.2, 0.2, 0.8, 0.5e-3, 2e-11),
                              ("carbon into steel: surface 1.0 wt%, initially 0.1 wt%; reach 0.45 wt%", 1.0, 0.1, 0.45, 1.0e-3, 4e-11),
                              ("a dopant into silicon: surface 1e20, initially 0 (per cm³); reach 1e19", 1.0, 0.0, 0.1, 1e-6, 1e-16),
                              ("hydrogen into a polymer sheet: surface 5, initially 0 (mol/m³); reach 2.5", 5, 0, 2.5, 1e-3, 1e-10)]:
    eta = mp.findroot(lambda e: mp.erf(e) - mp.mpf(C - Cs) / (Ci - Cs), 0.5)
    t = (x / (2 * eta)) ** 2 / D
    cases.append({"what": what, "Cs": Cs, "Ci": Ci, "C": C, "xp": x * 1000, "D": D, "ans": F(t)})
tpl("ht-mass-erf-time", "ht.mass-diffusion",
    "Diffusion of {{what}} at a depth of {{xp}} mm, $D_{AB} = {{D}}$ m²/s. Treating the solid as semi-infinite, how long does it take?",
    "Time", "s",
    "The heat-conduction solution carries over: $\\dfrac{C_A - C_{A,s}}{C_{A,i} - C_{A,s}} = \\operatorname{erf}\\dfrac{x}{2\\sqrt{D_{AB}t}}$. Invert erf for $\\eta$, then $t = (x/2\\eta)^2/D_{AB}$. Doubling the depth takes four times as long",
    cases, "mass_erf_time(Cs, Ci, C, xp/1000, D)")

# ── flat plate: unheated starting length, uniform surface flux (laminar, local) ─
cases = []
for fl, u, nu, k, Pr, x, xi, q, Tinf in [("air", 5, 1.589e-5, 0.0263, 0.707, 0.3, 0.1, 0, 0), ("air", 10, 1.589e-5, 0.0263, 0.707, 0.5, 0.25, 0, 0),
                                         ("water", 0.2, 8.57e-7, 0.613, 5.83, 0.2, 0.05, 0, 0), ("air", 4, 1.589e-5, 0.0263, 0.707, 0.4, 0, 500, 300),
                                         ("water", 0.3, 8.57e-7, 0.613, 5.83, 0.25, 0, 5000, 290)]:
    Re = mp.mpf(u) * x / nu
    if q == 0:
        Nu = mp.mpf("0.332") * mp.sqrt(Re) * mp.cbrt(Pr) / mp.cbrt(1 - (mp.mpf(xi) / x) ** mp.mpf("0.75"))
        val, wt = Nu * k / x, "the local coefficient $h_x$ (W/m²·K) at $x = {{xp}}$ m, the plate being unheated for the first {{xi}} m"
        kind = 0
    else:
        Nu = mp.mpf("0.453") * mp.sqrt(Re) * mp.cbrt(Pr)
        val, wt = Tinf + q / (Nu * k / x), "the surface temperature (K) at $x = {{xp}}$ m when the whole plate supplies a uniform ${{q}}$ W/m² (free stream at {{Tinf}} K)"
        kind = 1
    cases.append({"fl": fl, "u": u, "nu": nu, "k": k, "Pr": Pr, "xp": x, "xi": xi, "q": q, "Tinf": Tinf, "kind": kind, "wt": wt.replace("{{xp}}", str(x)).replace("{{xi}}", str(xi)).replace("{{q}}", str(q)).replace("{{Tinf}}", str(Tinf)), "ans": F(val)})
tpl("ht-plate-special", "ht.external-flow",
    "Laminar {{fl}} flow at ${{u}}$ m/s along a flat plate ($\\nu = {{nu}}$ m²/s, $k = {{k}}$ W/m·K, Pr = {{Pr}}). Find {{wt}}.",
    "Answer", "",
    "Unheated starting length ξ: $Nu_x = \\dfrac{0.332\\,Re_x^{1/2}Pr^{1/3}}{[1 - (\\xi/x)^{3/4}]^{1/3}}$, larger than the fully heated value because the thermal layer is thinner. Uniform surface flux: $Nu_x = 0.453\\,Re_x^{1/2}Pr^{1/3}$ (36% above 0.332), and $T_s(x) = T_\\infty + q''/h_x$ grows as $\\sqrt x$",
    cases, "plate_local(kind, u, nu, k, Pr, xp, xi, q, Tinf)")


def dump():
    head = "# " + "\n# ".join(__doc__.strip().splitlines()) + "\n# GENERATED: edit scripts/ht_final_cases.py, not this file.\n\n"
    OUT.write_text(head + yaml.dump(T, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=None))
    print(f"{len(T)} templates, {sum(len(t['cases']) for t in T)} cases -> {OUT}")


if __name__ == "__main__":
    dump()
