"""Second question types for Polymers and Materials (MT): reverses, scalings and scenarios beside the first type of each
objective, recomputed by sympy along another route (a ratio of the law before and after, a count, the defining sum)."""
from opl_dsl import Q

FILE, FRAMEWORK = "mt-second-types", "materials"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
POL, SOL, COL = "materials.polymers", "materials.solids", "materials.colloids"


def facts(name, skill, rows, explain, pace="quick"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("MT-1.1.A", Q("mt-blend-mn", POL, "Equal masses of two monodisperse samples, M = {{m1}} and {{m2}} kg/mol, are blended. What is M_n of the blend, in kg/mol?",
        given={"m1": {"pick": [10, 20, 50]}, "m2": {"pick": [100, 200]}}, value="2/(1/m1 + 1/m2)", tex="M_n",
        verify="(1 + 1)/(Rational(1, m1) + Rational(1, m2))",
        explain="Per kilogram of each, the number of chains is 1/M: M_n = total mass ÷ total moles, a harmonic mean pulled toward the short chains")),
    ("MT-1.1.B", Q("mt-carothers-reverse", POL, "A step-growth polymerisation of a 1:1 A–A/B–B mixture must reach a number-average degree of polymerisation of {{Xn}}. What fractional conversion p is needed?",
        given={"Xn": {"pick": [20, 50, 100, 200]}}, value="1 - 1/Xn", tex="p", verify="solve(Eq(1/(1 - x), Xn), x)[0]",
        explain="Carothers: X_n = 1/(1 − p), so high polymer needs p above 0.99: why step growth demands exact stoichiometry and purity")),
    ("MT-1.1.C", facts("mt-growth-evidence", POL, [
        ("Early in a reaction, high-molar-mass chains already exist alongside unreacted monomer. Which mechanism?", "Chain growth", "Step growth", "Both equally", "Neither"),
        ("Monomer disappears quickly but molar mass stays low until conversion is near 99%. Which mechanism?", "Step growth", "Chain growth", "Living anionic", "Free radical"),
        ("Which polymerisation releases a small molecule such as water at each linkage?", "Condensation (a step-growth type)", "Free-radical addition", "Ring-opening of an epoxide by an initiator", "Anionic addition"),
        ("A living anionic polymerisation is stopped and more monomer added; chains keep growing. What does that show?", "Chain ends stay active (no termination)", "Step growth", "Crosslinking", "Depolymerisation"),
    ], "Chain growth builds long chains one at a time; step growth builds everything slowly together")),
    ("MT-1.1.D", facts("mt-thermoset-evidence", POL, [
        ("A cured epoxy chars instead of melting when heated. Why?", "Covalent crosslinks form a network that cannot flow", "Its chains are too short", "It is a thermoplastic", "It contains water"),
        ("A plastic swells in a good solvent but does not dissolve. What does that suggest?", "A crosslinked (thermoset or elastomer) network", "A low molar mass thermoplastic", "A crystal", "A ceramic"),
        ("Why can PET bottles be remelted and reformed?", "PET is a thermoplastic of linear chains", "PET is crosslinked", "PET is a thermoset", "PET is an elastomer only"),
        ("Dental composites cure into which kind of polymer?", "A crosslinked thermoset network of dimethacrylates", "A linear thermoplastic", "A natural rubber", "A silicone oil"),
    ], "Thermoplastics are linear or branched and flow when hot; thermosets are networks that only degrade")),
    ("MT-2.1.A", Q("mt-elongation", SOL, "A rod {{L}} m long with cross-section {{A}} mm² and Young's modulus {{E}} GPa carries a tensile load of {{F}} kN. How much does it stretch, in mm?",
        given={"L": {"pick": [0.5, 1, 2]}, "A": {"pick": [20, 50, 100]}, "E": {"pick": [70, 110, 200]}, "F": {"pick": [5, 10, 20]}},
        value="F*1000*L/(E*1e9*A*1e-6)*1000", tex="\\Delta L",
        verify="solve(Eq(nsimplify(E)*10**9, (F*1000/(nsimplify(A)/10**6))/(x/1000/nsimplify(L))), x)[0]",
        explain="Stress = F/A, strain = ΔL/L₀, E = stress/strain, so ΔL = FL₀/(EA)")),
    ("MT-2.1.B", Q("mt-gap-from-emission", SOL, "An LED emits at {{lam}} nm. What is the band gap of its semiconductor, in eV?",
        given={"lam": {"pick": [450, 525, 620, 850]}}, value="1239.841984/lam", tex="E_g",
        verify="Rational(1239841984, 10**6)/lam", explain="E = hc/λ with hc = 1239.84 eV·nm: blue LEDs need wide gaps (GaN), red and infrared narrower ones")),
    ("MT-3.1.B", Q("col-grahame-scale", COL, "At fixed surface potential, by what factor does the Grahame surface charge density change when 1:1 salt concentration rises from {{c1}} to {{c2}} mM?",
        given={"c1": {"pick": [1, 10]}, "c2": {"pick": [4, 100, 1000]}}, value="sqrt(c2/c1)", tex="\\sigma_2/\\sigma_1",
        verify="col_grahame(50, c2)/col_grahame(50, c1)",
        explain="σ ∝ √n∞ at fixed ψ₀ (the sinh term does not change): more salt packs the countercharge closer, so the surface holds more charge")),
    ("MT-3.2.B", Q("col-hamaker-same", COL, "Two identical particles with A₁₁ = {{a11}} zJ interact across a medium with A₃₃ = {{a33}} zJ. Estimate A₁₃₁ with the combining rule, in zJ.",
        given={"a11": {"pick": [40, 65, 150]}, "a33": {"pick": [37, 50]}}, value="(sqrt(a11) - sqrt(a33))^2", tex="A_{131}",
        verify="a11 + a33 - 2*sqrt(a11*a33)", explain="A₁₃₁ ≈ (√A₁₁ − √A₃₃)²: never negative, so identical particles always attract, weakly when the medium matches them")),
    ("MT-3.3.A", Q("col-edl-decay", COL, "The double-layer repulsion between two spheres is {{U1}} k_BT at a gap of {{D1}} nm. The Debye length is {{k}} nm. In the weak-overlap limit, what is it at {{D2}} nm?",
        given={"U1": {"pick": [10, 20, 40]}, "D1": {"pick": [2, 5]}, "k": {"pick": [1, 3, 10]}, "D2": {"pick": [8, 12]}},
        value="U1*exp(-(D2 - D1)/k)", tex="U", verify="nsimplify(U1)*exp(-(D2 - D1)/nsimplify(k))",
        explain="Weak overlap: U ∝ e^(−κD), so each Debye length of extra gap divides the repulsion by e")),
    ("MT-3.4.A", Q("col-diffusion-time", COL, "A particle has diffusion coefficient {{Dc}} µm²/s. Roughly how long, in s, does it take to wander {{xx}} µm (3-D, ⟨r²⟩ = 6Dt)?",
        given={"Dc": {"pick": [0.5, 2, 10]}, "xx": {"pick": [1, 5, 20]}}, value="xx^2/(6*Dc)", tex="t",
        verify="solve(Eq(6*nsimplify(Dc)*x, xx**2), x)[0]", explain="Diffusion time grows with the square of distance: ten times farther takes a hundred times longer")),
    ("MT-3.4.B", Q("col-coag-scale", COL, "Rapid coagulation of a dispersion has a half-life of {{t}} s. What is it if the particle concentration is {{f}}-fold and the temperature unchanged?",
        given={"t": {"pick": [60, 600]}, "f": {"pick": [2, 10, 0.5]}}, value="t/f", tex="t_{1/2}",
        verify="nsimplify(t)*(3*Rational(89, 100000)/(4*1*f))/(3*Rational(89, 100000)/(4*1*1))",
        explain="t₁/₂ = 3η/(4k_BT n₀): halving time with every doubling of concentration, because collisions scale with n₀")),
    ("MT-3.4.C", facts("col-nondlvo-scenario", COL, [
        ("Adding a polymer that adsorbs strongly and extends far into the solvent keeps particles apart even in high salt. Which force?", "Steric repulsion", "Depletion attraction", "Van der Waals attraction", "Double-layer repulsion"),
        ("Adding a non-adsorbing polymer makes large particles cluster. Which force?", "Depletion attraction", "Steric repulsion", "Hydration repulsion", "Electrostatic repulsion"),
        ("A small dose of long polymer that adsorbs on two particles at once floccules them. What mechanism?", "Bridging flocculation", "Depletion", "Hydration", "Electrophoresis"),
        ("Silica surfaces stay apart at very short range even when DLVO predicts contact. Which force?", "Hydration (structured water) repulsion", "Depletion attraction", "Bridging", "Gravity"),
    ], "DLVO counts only van der Waals and double-layer forces; polymers and water structure add more")),
]
