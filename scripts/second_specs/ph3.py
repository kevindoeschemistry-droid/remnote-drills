"""AP Physics on the 2024 CEDs (Nov 2026): every learning objective of Physics 1, 2, C: Mechanics and C: E&M is an item of
`ap-physics` (codes P1/P2/CM/CEM). OBJS close the ten the framework did not answer: apparent weight and inertial versus
gravitational mass, gravity with altitude and inside a uniform sphere, springs in series and parallel, simple circuits.
Two types each; numbers recomputed by sympy."""
from opl_dsl import Q

FILE, FRAMEWORK = "ph-ap-gaps", "physics"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
TOPICS = {"11.2": "Simple circuits"}
PRACTICE = "2B"


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


OBJS = [
    ("PH-2.6.C", ["P1 2.6.C", "P1 2.6.D", "CM 2.6.C", "CM 2.6.D"], "Find apparent weight in an accelerating frame and tell inertial from gravitational mass.",
     "A scale reads the normal force: N = m(g + a) with a positive upward; in free fall N = 0 (weightless) though gravity still acts; inertial and gravitational mass are equal to high precision."),
    ("PH-2.6.D", ["P1 2.6.B", "CM 2.6.B", "CM 2.6.E"], "Decide when g is constant and find g above a planet or inside a uniform sphere.",
     "Outside: g = GM/r², nearly constant when the height is small next to the radius; inside a uniform sphere g = GMr/R³, growing linearly from zero at the centre."),
    ("PH-2.8.B", ["CM 2.8.B"], "Combine springs in series and in parallel.",
     "Parallel: k = k₁ + k₂ (same stretch); series: 1/k = 1/k₁ + 1/k₂ (same force)."),
    ("PH-11.2.A", ["P2 11.2.A", "CEM 11.2.A"], "Tell open, closed and short circuits apart and predict what a single-loop circuit does.",
     "Current needs a closed loop; an open switch stops it everywhere in that loop; a short (near-zero resistance path) carries almost all the current; in one loop the current is the same everywhere."),
]

DY, CI = "physics.dynamics", "physics.circuits"

ADD = [
    ("PH-2.6.C", Q("ph-elevator-scale", DY, "A {{m}} kg person stands on a scale in an elevator that is {{mot}} at {{a}} m/s². What does the scale read, in newtons? (g = 9.8 m/s²)",
        cases=[{"m": 60, "mot": "speeding up going up", "sg": 1, "a": 2}, {"m": 60, "mot": "slowing down going up", "sg": -1, "a": 2}, {"m": 75, "mot": "speeding up going down", "sg": -1, "a": 1.5},
               {"m": 75, "mot": "slowing down going down", "sg": 1, "a": 1.5}, {"m": 50, "mot": "in free fall (cable cut), accelerating down", "sg": -1, "a": 9.8}],
        value="m*(9.8 + sg*a)", tex="N", verify="solve(Eq(x - m*Rational(98, 10), m*sg*nsimplify(a)), x)[0]",
        explain="Newton's second law on the person: N − mg = ma (up positive). Speeding up upward or slowing down downward both mean a points up")),
    ("PH-2.6.C", facts("ph-weightless", DY, [
        ("Astronauts on the space station float. Why?", "They and the station fall together around Earth, so no normal force acts", "Gravity there is zero", "They are outside Earth's field", "The station pushes them up"),
        ("A heavy and a light ball dropped together hit the ground together (no air). Which fact explains it?", "Inertial mass equals gravitational mass", "Heavy objects feel less gravity", "Air pushes the light ball", "Gravity depends on volume"),
        ("A scale in an elevator reads more than your weight. What do you know?", "The acceleration points upward", "The elevator moves up", "The elevator moves down", "The elevator is at rest"),
        ("Where does gravitational force on you from Earth vanish?", "Nowhere outside Earth; it weakens with distance but never becomes zero", "At 100 km altitude", "In orbit", "In an elevator"),
    ], "Apparent weight is the support force, not the gravitational force", pace="quick")),
    ("PH-2.6.D", Q("ph-g-altitude", DY, "At what height above Earth's surface, as a fraction of Earth's radius R, does g fall to {{f}} of its surface value?",
        cases=[{"f": "1/4", "fn": 1, "fd": 4}, {"f": "1/9", "fn": 1, "fd": 9}, {"f": "1/2", "fn": 1, "fd": 2}, {"f": "0.99", "fn": 99, "fd": 100}],
        value="sqrt(fd/fn) - 1", tex="h/R", verify="Max(*[r for r in solve(Eq(1/(1 + x)**2, Rational(fn, fd)), x) if r.is_real])",
        explain="g ∝ 1/r², so (R/(R + h))² = f; g drops 1% only at h ≈ 0.005R (about 32 km), which is why g is taken as constant near the surface")),
    ("PH-2.6.D", Q("ph-g-inside", DY, "Treat a planet as a uniform sphere with surface gravity {{gs}} m/s². What is g at {{fr}} of the way from the centre to the surface?",
        given={"gs": {"pick": [9.8, 3.7, 24.8]}, "fr": {"pick": [0.25, 0.5, 0.75]}}, value="gs*fr", tex="g",
        verify="nsimplify(gs)*(nsimplify(fr))**3/nsimplify(fr)**2",
        explain="Only the mass inside r pulls (shell theorem): M(r) = M r³/R³, so g = GM(r)/r² = g_s · r/R")),
    ("PH-2.8.B", Q("ph-springs-combine", DY, "Springs of {{k1}} N/m and {{k2}} N/m are joined in {{how}}. What is the equivalent spring constant, in N/m?",
        cases=[{"k1": 200, "k2": 300, "how": "parallel (side by side)", "w": 0}, {"k1": 200, "k2": 300, "how": "series (end to end)", "w": 1},
               {"k1": 400, "k2": 400, "how": "series (end to end)", "w": 1}, {"k1": 150, "k2": 50, "how": "parallel (side by side)", "w": 0}],
        value="w == 0 ? k1 + k2 : k1*k2/(k1 + k2)", tex="k", verify="[k1 + k2, 1/(Rational(1, k1) + Rational(1, k2))][w]",
        explain="Parallel springs share the load and add; series springs carry the same force and their stretches add, so compliances add")),
    ("PH-2.8.B", Q("ph-spring-cut", DY, "A spring of constant {{k}} N/m is cut into {{n}} equal pieces. What is the spring constant of one piece, in N/m?",
        given={"k": {"pick": [100, 250, 400]}, "n": {"pick": [2, 3, 4]}}, value="n*k", tex="k'", final=True, verify="solve(Eq(Rational(1, k), n/x), x)[0]",
        explain="The whole spring is n pieces in series: 1/k = n/k′, so each piece is n times stiffer")),
    ("PH-11.2.A", facts("ph-simple-circuit", CI, [
        ("A switch in a single loop is opened. What happens to the current?", "It stops everywhere in the loop", "It stops only after the switch", "It doubles", "It flows backward"),
        ("In a single loop with a battery and two bulbs, how does the current compare at different points?", "The same everywhere", "Largest near the positive terminal", "Used up by the first bulb", "Zero after the second bulb"),
        ("A wire is connected directly across one of two series bulbs. What happens?", "That bulb goes out and the other gets brighter", "Both go out", "Both get dimmer", "Nothing changes"),
        ("Why does a bulb light only when connected to both battery terminals?", "Charge needs a complete loop to flow", "One terminal holds all the energy", "Bulbs need two wires for heat", "The battery only works upside down"),
    ], "Current needs a closed path and is the same all around a single loop", pace="quick")),
    ("PH-11.2.A", Q("ph-short-current", CI, "A {{emf}} V battery with internal resistance {{r}} Ω is connected to a {{R}} Ω resistor. What current flows, in A, and how much if a wire shorts the resistor? Give the current {{case}}.",
        cases=[{"emf": 9, "r": 0.5, "R": 8.5, "case": "with the resistor", "w": 0}, {"emf": 9, "r": 0.5, "R": 8.5, "case": "when shorted", "w": 1},
               {"emf": 12, "r": 0.2, "R": 5.8, "case": "with the resistor", "w": 0}, {"emf": 1.5, "r": 0.3, "R": 2.7, "case": "when shorted", "w": 1}],
        value="w == 0 ? emf/(R + r) : emf/r", tex="I", verify="[nsimplify(emf)/(nsimplify(R) + nsimplify(r)), nsimplify(emf)/nsimplify(r)][w]",
        explain="I = ε/(R + r); shorting removes R, so only the small internal resistance limits the current, which is why shorts heat batteries")),
]
