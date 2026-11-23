"""Builds three problem files (run: python3 scripts/es_cases.py):
  drills/problems/es-earth-space.yaml       framework earth-space (ES), on NGSS HS ESS and IB
  drills/problems/ph-relativity-lagrange.yaml  physics units 29-30 (special relativity, Lagrangian mechanics)
  drills/problems/mt-materials.yaml         framework materials (MT): polymers and materials

Answers use the closed forms on the cards; tests/verify/escalc.py recomputes by another route
(force balance, the Planck maximum, energy-balance solves, the decay ODE, Lorentz boosts and
rapidities, Euler-Lagrange equations, weight fractions, functional-group counting), and a second
typed table for the factual picks.
"""
import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent / "drills/problems"
G, C, H, KB = 6.67430e-11, 299792458.0, 6.62607015e-34, 1.380649e-23
SIGMA = 2 * math.pi**5 * KB**4 / (15 * C**2 * H**3)
WIEN_X = 4.965114231744276
OUT = {"es": [], "ph": [], "mt": []}


def val(f, name, skill, prompt, ask, explain, cases, verify, tol=0.0002, pace="quick"):
    OUT[f].append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
                   "parts": [{"ask": ask, "label": "y", "value": "ans", "tol": tol, "explain": explain}], "verify": {"expect": {"y": verify}}})


def pick(f, name, skill, prompt, options, explain, cases, verify, pace="recall"):
    OUT[f].append({"template": name, "skill": skill, "pace": pace, "cases": cases, "prompt": prompt,
                   "parts": [{"ask": "Answer", "label": "y", "choice": options, "correct": "ans", "explain": explain}], "verify": {"choices": {"y": verify}}})


R = lambda v: float(f"{v:.13g}")  # noqa: E731

# ════ Earth and space ═══════════════════════════════════════════════════════
cases = []
for body, M, a, unit, div in [("Earth around the Sun", 1.989e30, 1.496e11, "days", 86400), ("Mars around the Sun", 1.989e30, 2.279e11, "days", 86400),
                              ("the Moon around Earth", 5.972e24, 3.844e8, "days", 86400), ("a satellite at 7000 km from Earth's centre", 5.972e24, 7.0e6, "minutes", 60),
                              ("Jupiter around the Sun", 1.989e30, 7.785e11, "years", 86400 * 365.25)]:
    cases.append({"body": body, "M": M, "a": a, "unit": unit, "div": div, "ans": R(2 * math.pi * math.sqrt(a**3 / (G * M)) / div)})
val("es", "es-kepler", "space.orbits", "Find the orbital period of {{body}}: central mass {{M}} kg, orbit radius {{a}} m (circular), G = 6.674×10⁻¹¹. Answer in {{unit}}.", "T",
    "Kepler's third law from gravity: $T = 2\\pi\\sqrt{a^3/GM}$. The orbiting mass drops out, so a satellite and the Moon at the same radius would share a period",
    cases, "orbit_period(M, a)/nsimplify(div)")

cases = []
for body, M, r in [("Earth", 5.972e24, 6.371e6), ("the Moon", 7.342e22, 1.737e6), ("Mars", 6.417e23, 3.390e6), ("Jupiter", 1.898e27, 6.991e7)]:
    cases.append({"body": body, "M": M, "r": r, "ans": R(math.sqrt(2 * G * M / r) / 1000)})
val("es", "es-escape", "space.orbits", "What is the escape speed from the surface of {{body}} (M = {{M}} kg, R = {{r}} m), in km/s?", "v (km/s)",
    "Kinetic energy must cover the gravitational well: ½v² = GM/R, so $v = \\sqrt{2GM/R}$, √2 times the speed of a circular orbit at the surface",
    cases, "escape_speed(M, r)/1000")

cases = []
for star, T in [("the Sun", 5772), ("Betelgeuse", 3600), ("Sirius A", 9940), ("Rigel", 12100), ("a red dwarf", 3000)]:
    cases.append({"star": star, "T": T, "ans": R(H * C / (WIEN_X * KB * T) * 1e9)})
val("es", "es-wien", "space.stars", "{{star}} has a surface temperature of about {{T}} K. At what wavelength (nm) does its spectrum peak?", "λ_max (nm)",
    "Wien's law: $\\lambda_{\\max} = b/T$ with $b = 2.898\\times10^{-3}$ m·K. Hot stars peak in the blue or UV, cool ones in the red or IR, which is how colour gives temperature",
    cases, "wien_peak(T)")

cases = []
for star, R_, T in [("the Sun", 6.957e8, 5772), ("Sirius A", 1.19e9, 9940), ("a red dwarf", 2.1e8, 3000), ("a white dwarf", 5.8e6, 25000)]:
    L = 4 * math.pi * R_**2 * SIGMA * T**4
    cases.append({"star": star, "Rs": R_, "T": T, "ans": R(L / 3.828e26)})
val("es", "es-luminosity", "space.stars", "Find the luminosity of {{star}} (radius {{Rs}} m, T = {{T}} K) in units of the Sun's, L☉ = 3.828×10²⁶ W.", "L/L☉",
    "Stefan–Boltzmann over the whole surface: $L = 4\\pi R^2\\sigma T^4$. Temperature enters to the fourth power, so a small hot star can outshine a big cool one",
    cases, "luminosity(Rs, T)/nsimplify('3.828e26')")

cases = [{"M": m, "ans": R(m ** -2.5)} for m in (2, 5, 10, 0.5, 20)]
val("es", "es-star-life", "space.stars", "If luminosity scales as M³·⁵, how long does a {{M}} M☉ star live on the main sequence, relative to the Sun?", "t/t☉",
    "Lifetime ∝ fuel ÷ burn rate ∝ M/L ∝ M/M³·⁵ = M⁻²·⁵. Massive stars live millions of years, not billions; red dwarfs outlast the present age of the universe",
    cases, "star_life(M)", pace="recall")

cases = []
for w, H0, d in [(0, 70, 100), (0, 70, 450), (0, 67.4, 1000), (1, 70, 0), (1, 67.4, 0), (1, 73, 0)]:
    ans = H0 * d if w == 0 else 3.0856775814913673e19 / H0 / (365.25 * 86400 * 1e9)
    task = [f"How fast does a galaxy {d} Mpc away recede (km/s), with H₀ = {H0} km/s/Mpc?", f"What is the Hubble time 1/H₀ (Gyr) for H₀ = {H0} km/s/Mpc?"][w]
    cases.append({"w": w, "H0": H0, "d": d, "task": task, "ans": R(ans)})
val("es", "es-hubble", "space.cosmology", "{{task}}", "Answer",
    "Hubble's law v = H₀d is the evidence for expansion (with the cosmic microwave background and light-element abundances). 1/H₀ ≈ 14 Gyr is a first estimate of the age of the universe",
    cases, "hubble(w, H0, d)")

cases = [{"proc": "4 ¹H → ⁴He (pp chain, atomic masses)", "n": 4, "mi": 1.00782503207, "mo": 4.00260325413},
         {"proc": "3 ⁴He → ¹²C (triple-alpha)", "n": 3, "mi": 4.00260325413, "mo": 12.0},
         {"proc": "2 ¹²C → ²⁴Mg", "n": 2, "mi": 12.0, "mo": 23.985041697}]
for c in cases:
    c["ans"] = R((c["n"] * c["mi"] - c["mo"]) * 931.49410242)
val("es", "es-fusion-energy", "space.stars", "How much energy (MeV) is released in {{proc}}? Atomic masses (u): reactant {{mi}}, product {{mo}}; 1 u = 931.494 MeV/c².", "Q (MeV)",
    "Q = (mass in − mass out) c². Fusion releases energy up to iron-56, where binding energy per nucleon peaks; heavier elements need neutron capture (s- and r-process) in AGB stars, supernovae and neutron-star mergers",
    cases, "fusion_energy(n, mi, mo)", tol=0.001)

ES_FACTS_DATA = {
    "origin": (["Big Bang nucleosynthesis", "fusion in stellar cores", "neutron capture in AGB stars, supernovae and mergers", "cosmic-ray spallation"],
               {"most helium-4": 0, "deuterium": 0, "carbon and oxygen": 1, "iron and nickel": 1, "gold and uranium": 2, "barium and lead (s-process)": 2, "lithium-6, beryllium and boron": 3}),
    "boundary": (["divergent", "convergent", "transform"], {"the Mid-Atlantic Ridge": 0, "the East African Rift": 0, "the Andes": 1, "the Himalaya": 1, "the Mariana Trench": 1, "the San Andreas Fault": 2, "Iceland": 0}),
    "feedback": (["amplifies warming (positive)", "damps warming (negative)"], {"melting sea ice lowers albedo": 0, "warmer air holds more water vapour": 0,
                 "a warmer surface radiates more (Planck response)": 1, "thawing permafrost releases CH₄ and CO₂": 0, "faster rock weathering draws down CO₂ over ~100 kyr": 1}),
    "seismic": (["P waves only", "both P and S waves", "neither"], {"through the liquid outer core": 0, "through the mantle": 1, "through the solid inner core (as P)": 0}),
    "dating": (["radiocarbon (¹⁴C)", "potassium–argon or argon–argon", "uranium–lead"], {"a 5000-year-old wooden tool": 0, "a 2-million-year-old volcanic ash layer": 1,
               "a 4.4-billion-year-old zircon": 2, "bone collagen 20 000 years old": 0, "the age of a meteorite": 2}),
}
for table, (opts, data) in ES_FACTS_DATA.items():
    cases = [{"k": k, "tb": table, "ans": v} for k, v in data.items()]
    spec = {"origin": ("es-element-origin", "space.cosmology", "Where were {{k}} made?",
                       "Big Bang: H, He, a little Li. Stars fuse up to Fe. Beyond iron, neutron capture: slow (s) in AGB stars, rapid (r) in supernovae and neutron-star mergers. Li, Be and B are mostly from cosmic rays splitting heavier nuclei"),
            "boundary": ("es-plate-boundary", "earth.interior", "What kind of plate boundary is {{k}}?",
                         "Divergent: plates part, new crust (ridges, rifts). Convergent: subduction (trenches, volcanic arcs) or collision (mountain belts). Transform: plates slide past (strike-slip faults, earthquakes but little volcanism)"),
            "feedback": ("es-feedback", "earth.climate", "Feedback: {{k}}. Does it amplify or damp warming?",
                         "A positive feedback loops the change back on itself (ice-albedo, water vapour, permafrost carbon); a negative one opposes it (more radiation from a warmer surface; slow silicate weathering, the long-term thermostat)"),
            "seismic": ("es-seismic", "earth.interior", "Which body waves travel {{k}}?",
                        "S waves are shear waves and cannot cross a liquid, so the outer core casts an S-wave shadow beyond 104°; P waves bend in it and leave a shadow from 104° to 140°. This is how the core was found to be liquid"),
            "dating": ("es-dating-method", "earth.history", "Which dating method fits {{k}}?",
                       "Pick a clock whose half-life suits the age: ¹⁴C (5730 y) for organic material to ~50 000 years; K–Ar (1.25 Gy) for volcanic rocks; U–Pb (0.7 and 4.5 Gy) in zircons and meteorites for the oldest ages")}[table]
    pick("es", spec[0], spec[1], spec[2], opts, spec[3], cases, 'es_fact(tb, k)')

cases = []
for iso, th, ratio in [("⁴⁰K → ⁴⁰Ar (t½ = 1.25 Gy)", 1.25e9, 0.10), ("²³⁸U → ²⁰⁶Pb (t½ = 4.468 Gy)", 4.468e9, 0.8), ("⁸⁷Rb → ⁸⁷Sr (t½ = 48.8 Gy)", 4.88e10, 0.065),
                       ("¹⁴C → ¹⁴N (t½ = 5730 y)", 5730, 3.0), ("²³⁵U → ²⁰⁷Pb (t½ = 0.704 Gy)", 7.04e8, 1.0)]:
    cases.append({"iso": iso, "th": th, "ratio": ratio, "ans": R(th / math.log(2) * math.log(1 + ratio))})
val("es", "es-radiometric", "earth.history", "A mineral holds radiogenic daughter and parent in the ratio D/P = {{ratio}} for {{iso}}, with no daughter at the start. How old is it (years)?", "Age (y)",
    "N = N₀e^(−λt) and D = N₀ − N, so $t = \\dfrac{t_{1/2}}{\\ln 2}\\ln(1 + D/P)$. D/P = 1 means one half-life; D/P = 3 two half-lives",
    cases, "decay_age(th, ratio)", tol=0.0005)

cases = []
for planet, S, alb in [("Earth", 1361, 0.30), ("Venus", 2601, 0.76), ("Mars", 586, 0.25), ("Earth with albedo 0.35", 1361, 0.35), ("the Moon", 1361, 0.11)]:
    cases.append({"planet": planet, "S": S, "alb": alb, "ans": R((S * (1 - alb) / (4 * SIGMA)) ** 0.25)})
val("es", "es-equilibrium-temp", "earth.climate", "What is the radiative-equilibrium temperature (K) of {{planet}}: solar constant {{S}} W/m², albedo {{alb}}, no greenhouse effect?", "T_e (K)",
    "Absorbed S(1 − α)πR² equals emitted 4πR²σT⁴, so $T_e = [S(1-\\alpha)/4\\sigma]^{1/4}$. Earth's 255 K against an actual 288 K is the 33 K greenhouse effect; Venus's 230 K against 735 K is a runaway one",
    cases, "eq_temp(S, alb)")
cases = [{"planet": p, "S": S, "alb": a, "ans": R(2 ** 0.25 * (S * (1 - a) / (4 * SIGMA)) ** 0.25)} for p, S, a in [("Earth", 1361, 0.30), ("Mars", 586, 0.25), ("Earth with albedo 0.35", 1361, 0.35)]]
val("es", "es-one-layer", "earth.climate", "Model {{planet}} (S = {{S}} W/m², albedo {{alb}}) with one atmospheric layer that absorbs all infrared and is transparent to sunlight. What is the surface temperature (K)?", "T_s (K)",
    "The layer radiates σT_a⁴ both up and down; balancing the top gives T_a = T_e, balancing the layer gives σT_s⁴ = 2σT_a⁴, so $T_s = 2^{1/4}T_e$. Too warm for Earth (303 K), because the real atmosphere absorbs only part of the infrared",
    cases, "one_layer(S, alb)")

cases = [{"C1": c1, "C0": c0, "lam": l, "ans": R(l * 5.35 * math.log(c1 / c0))} for c1, c0, l in [(560, 280, 0.8), (420, 280, 0.8), (420, 280, 0.5), (800, 280, 0.8), (350, 280, 1.0)]]
val("es", "es-co2-forcing", "earth.climate", "With radiative forcing ΔF = 5.35 ln(C/C₀) W/m² and climate sensitivity λ = {{lam}} K per W/m², how much warming (K) does CO₂ at {{C1}} ppm give relative to {{C0}} ppm, at equilibrium?", "ΔT (K)",
    "Forcing grows with the logarithm of concentration, so each doubling adds the same 3.7 W/m². ΔT = λΔF; λ ≈ 0.8 gives about 3 K per doubling, the middle of the IPCC range",
    cases, "co2_warming(C1, C0, lam)")

cases = [{"ppm": p, "ans": R(p * 1e-6 * 5.148e18 * 1000 / 28.97 * 12.011 / 1e15)} for p in (1, 2.4, 140, 10)]
val("es", "es-carbon-mass", "earth.climate", "How many gigatonnes of carbon correspond to {{ppm}} ppm of CO₂ in the atmosphere (air mass 5.148×10¹⁸ kg, 28.97 g/mol)?", "GtC",
    "Moles of air × mole fraction × 12.011 g/mol: about 2.13 GtC per ppm. Fossil emissions of ~10 GtC per year would add ~4.7 ppm if it all stayed; about half does",
    cases, "ppm_to_gtc(ppm)")

cases = [{"r": r, "pct": round(r * 100, 3), "ans": R(math.log(2) / math.log(1 + r))} for r in (0.01, 0.02, 0.035, 0.07, 0.005)]
val("es", "es-doubling", "earth.resources", "A population or a resource demand grows {{pct}}% a year. How many years does it take to double?", "Years",
    "(1 + r)ᵗ = 2, so t = ln 2 / ln(1 + r) ≈ 70/(percent growth): the rule of 70. Steady growth means each doubling consumes as much as all the history before it",
    cases, "doubling_time(r)")

# ════ physics: special relativity and Lagrangian mechanics ══════════════════
cases = []
for beta, tau in [(0.6, 1.0), (0.8, 2.2), (0.995, 2.2), (0.99, 1.0), (0.5, 10.0)]:
    cases.append({"beta": beta, "tau": tau, "ans": R(tau / math.sqrt(1 - beta**2))})
val("ph", "ph-time-dilation", "physics.relativity", "A clock moves at {{beta}}c. It ticks every {{tau}} μs in its own frame. How long between ticks in the lab (μs)?", "Δt (μs)",
    "Δt = γΔτ, γ = 1/√(1 − β²). Muons with a 2.2 μs proper lifetime reach the ground because the lab sees them live ten times longer (and they see the atmosphere contracted)",
    cases, "dilation(beta, tau)")
cases = [{"beta": b, "L0": L, "ans": R(L * math.sqrt(1 - b * b))} for b, L in [(0.6, 10), (0.8, 100), (0.99, 1), (0.5, 4)]]
val("ph", "ph-length-contraction", "physics.relativity", "A rod of rest length {{L0}} m moves along its length at {{beta}}c. How long is it in the lab (m)?", "L (m)",
    "L = L₀/γ, only along the motion. Both ends must be marked at the same lab time, which is why contraction and dilation come together",
    cases, "contraction(beta, L0)")
cases = [{"u": u, "v": v, "ans": R((u + v) / (1 + u * v))} for u, v in [(0.5, 0.5), (0.9, 0.9), (0.6, 0.3), (0.99, 0.5), (0.8, -0.5)]]
val("ph", "ph-velocity-addition", "physics.relativity", "A ship moving at {{u}}c fires a probe forward at {{v}}c relative to the ship. How fast is the probe in the original frame (in units of c)?", "Speed (c)",
    "$w = \\dfrac{u + v}{1 + uv/c^2}$; it never exceeds c. Rapidities (artanh β) simply add, which is the same rule",
    cases, "velocity_add(u, v)")
cases = []
for w in (0, 1):
    for name, m, b in [("a proton", 938.272, 0.6), ("an electron", 0.51099895, 0.99), ("a proton", 938.272, 0.9)]:
        g = 1 / math.sqrt(1 - b * b)
        cases.append({"w": w, "name": name, "m": m, "beta": b, "wt": ["kinetic energy (MeV)", "momentum (MeV/c)"][w], "ans": R([(g - 1) * m, g * m * b][w])})
val("ph", "ph-rel-energy", "physics.relativity", "{{name}} (mc² = {{m}} MeV) moves at {{beta}}c. What is its {{wt}}?", "Answer",
    "E = γmc², K = (γ − 1)mc², p = γmv; check with E² = (pc)² + (mc²)². ½mv² underestimates K badly above ~0.3c",
    cases, "rel_energy(w, m, beta)")
cases = [{"f": f, "beta": b, "ans": R(f * math.sqrt((1 + b) / (1 - b)))} for f, b in [(100, 0.6), (500, 0.1), (5e14, 0.2), (1000, 0.8)]]
val("ph", "ph-rel-doppler", "physics.relativity", "A source emitting at {{f}} Hz approaches at {{beta}}c. What frequency is received?", "f (Hz)",
    "$f = f_0\\sqrt{\\dfrac{1+\\beta}{1-\\beta}}$ approaching (swap signs receding). Unlike sound, only the relative speed matters",
    cases, "rel_doppler(f, beta)")

cases = []
for kind, a, b, c, text, ans in [("atwood", 3, 2, 0, "An Atwood machine holds 3 kg and 2 kg on a massless pulley. Find the acceleration (m/s²).", 9.81 / 5),
                                 ("atwood", 5, 1, 0, "An Atwood machine holds 5 kg and 1 kg. Find the acceleration (m/s²).", 9.81 * 4 / 6),
                                 ("roll", 0.5, 30, 0, "A solid cylinder (I = ½mr²) rolls without slipping down a 30° incline. Find its acceleration (m/s²).", 9.81 * 0.5 / 1.5),
                                 ("roll", 0.4, 20, 0, "A solid sphere (I = ⅖mr²) rolls without slipping down a 20° incline. Find its acceleration (m/s²).", 9.81 * math.sin(math.radians(20)) / 1.4),
                                 ("roll", 1.0, 15, 0, "A thin hoop (I = mr²) rolls without slipping down a 15° incline. Find its acceleration (m/s²).", 9.81 * math.sin(math.radians(15)) / 2),
                                 ("pendulum", 2.0, 0, 0, "A simple pendulum is 2.0 m long. Find its small-oscillation angular frequency (rad/s).", math.sqrt(9.81 / 2)),
                                 ("rod", 1.5, 0, 0, "A uniform rod 1.5 m long swings from one end. Find its small-oscillation angular frequency (rad/s).", math.sqrt(3 * 9.81 / 3.0)),
                                 ("springs", 2, 10, 30, "A 2 kg mass sits between two springs (10 and 30 N/m) fixed to opposite walls. Find ω (rad/s).", math.sqrt(40 / 2)),
                                 ("series", 2, 10, 30, "A 2 kg mass hangs on springs of 10 and 30 N/m joined end to end. Find ω (rad/s).", math.sqrt(7.5 / 2))]:
    cases.append({"kind": kind, "a": a, "b": b, "c": c, "text": text, "ans": R(ans)})
val("ph", "ph-lagrangian", "physics.lagrangian", "Use g = 9.81 m/s². {{text}}", "Answer",
    "Write L = T − V in one generalised coordinate, apply d/dt(∂L/∂q̇) = ∂L/∂q, and read off q̈ (or, linearised, ω² = −∂q̈/∂q). Constraint forces never appear, which is the point",
    cases, "lagr_eom(kind, a, b, c)")

# ════ polymers and materials ════════════════════════════════════════════════
cases = []
for w in (0, 1, 2):
    for ns, Ms in [([10, 20, 5], [1e4, 2e4, 5e4]), ([1, 1], [1e4, 1e5]), ([50, 30, 20], [2e4, 4e4, 8e4])]:
        mass = [n * m for n, m in zip(ns, Ms)]
        Mn = sum(mass) / sum(ns)
        Mw = sum(n * m * m for n, m in zip(ns, Ms)) / sum(mass)
        cases.append({"w": w, "ns": ns, "Ms": Ms, "nt": ", ".join(map(str, ns)), "mt": ", ".join(f"{m:g}" for m in Ms), "wt": ["M_n", "M_w", "the dispersity Đ = M_w/M_n"][w], "ans": R([Mn, Mw, Mw / Mn][w])})
val("mt", "mt-molar-mass-averages", "materials.polymers", "A polymer sample holds {{nt}} moles of chains with molar masses {{mt}} g/mol. What is {{wt}}?", "Answer",
    "M_n = ΣnᵢMᵢ/Σnᵢ (counts chains; colligative properties). M_w = ΣnᵢMᵢ²/ΣnᵢMᵢ (weights by mass; light scattering, viscosity). Đ ≥ 1, and equals 1 only for a single chain length",
    cases, "mol_avg(w, ns, Ms)")
cases = [{"p": p, "r": r, "ans": R((1 + r) / (1 + r - 2 * r * p))} for p, r in [(0.99, 1), (0.995, 1), (0.9, 1), (0.99, 0.98), (0.999, 0.99), (0.98, 1)]]
val("mt", "mt-carothers", "materials.polymers", "A step-growth (condensation) polymerisation reaches extent p = {{p}} with stoichiometric ratio r = {{r}}. What is the number-average degree of polymerisation?", "X_n",
    "Carothers: $X_n = \\dfrac{1 + r}{1 + r - 2rp}$, which is 1/(1 − p) at r = 1. High polymer needs p > 0.99 and near-perfect stoichiometry, unlike chain growth where long chains form from the start",
    cases, "carothers(p, r)")
MT_FACTS = {"growth": (["chain-growth (addition)", "step-growth (condensation)"], {"polyethylene": 0, "PVC": 0, "nylon-6,6": 1, "PET": 1, "polystyrene": 0, "a polyurethane": 1, "polycarbonate": 1, "PMMA": 0}),
            "thermal": (["thermoplastic", "thermoset"], {"polyethylene": 0, "vulcanised rubber": 1, "epoxy resin": 1, "PET": 0, "Bakelite": 1, "nylon": 0})}
for table, (opts, data) in MT_FACTS.items():
    cases = [{"k": k, "tb": table, "ans": v} for k, v in data.items()]
    if table == "growth":
        pick("mt", "mt-growth-type", "materials.polymers", "Is {{k}} made by chain growth or step growth?", opts,
             "Chain growth adds monomers one at a time to an active end (radical, ionic, coordination) with no by-product: vinyl polymers. Step growth joins any two species with complementary groups, often losing water or HCl: polyesters, polyamides, polycarbonates, polyurethanes",
             cases, "es_fact(tb, k)")
    else:
        pick("mt", "mt-thermoset", "materials.polymers", "Is {{k}} a thermoplastic or a thermoset?", opts,
             "Thermoplastics are separate chains that soften and flow when heated and can be remoulded. Thermosets are cross-linked networks that char instead of melting",
             cases, "es_fact(tb, k)")
cases = [{"mat": m, "Eg": e, "ans": R(H * C / (e * 1.602176634e-19) * 1e9)} for m, e in [("silicon", 1.12), ("GaAs", 1.42), ("GaN", 3.4), ("CdSe", 1.74), ("germanium", 0.66)]]
val("mt", "mt-band-gap", "materials.solids", "{{mat}} has a band gap of {{Eg}} eV. What is the longest wavelength (nm) it absorbs, or the wavelength an LED of it emits?", "λ (nm)",
    "λ = hc/E_g ≈ 1239.84/E_g(eV) nm. Wide gaps (GaN) give blue LEDs; narrow gaps absorb into the infrared, which is why silicon solar cells use most of sunlight",
    cases, "band_gap_wavelength(Eg)")
cases = [{"F": F, "A": A, "L0": L0, "dL": dL, "ans": R(F / A / (dL / L0) / 1e9)} for F, A, L0, dL in [(1000, 1e-5, 2.0, 0.001), (5000, 2e-5, 1.0, 0.0035), (200, 1e-6, 0.5, 0.0005), (2.0e4, 1e-4, 3.0, 0.003)]]
val("mt", "mt-youngs-modulus", "materials.solids", "A wire of cross-section {{A}} m² and length {{L0}} m stretches {{dL}} m under {{F}} N. What is Young's modulus (GPa)?", "E (GPa)",
    "E = stress/strain = (F/A)/(ΔL/L₀), valid in the linear elastic region. Steel ~200 GPa, aluminium ~70, glass ~70, polymers 0.01–4",
    cases, "nsimplify(F)/nsimplify(A)/(nsimplify(dL)/nsimplify(L0))/10**9")

NAMES = {"es": "es-earth-space.yaml", "ph": "ph-relativity-lagrange.yaml", "mt": "mt-materials.yaml"}
for k, v in OUT.items():
    yaml.safe_dump(v, open(ROOT / NAMES[k], "w"), allow_unicode=True, sort_keys=False, width=200)
    print(NAMES[k], len(v), "templates,", sum(len(t["cases"]) for t in v), "cases")
