"""Topology unit 5 (Nov 2026): homotopy, the fundamental group, covering spaces and a first look at homology, on the
Cambridge Part II Algebraic Topology schedule (read through an extraction of the 2026-27 Schedules)."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "tp-algebraic", "topology", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
HT = "top.homotopy"
B = ["cambridge-ii-algebraic-topology:H", "cambridge-ii-algebraic-topology:V", "cambridge-ii-algebraic-topology:K", "cambridge-ii-algebraic-topology:L"]
H, V, K, L = ([x] for x in B)


def F(name, rows, explain):
    return Q(name, HT, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, HT, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


UNITS = {"5": ("homotopy", "The fundamental group and homology", ["INV"], B)}
TOPICS = {"5.1": "Loops, coverings and holes"}
OBJS = [
 ("TP-5.1.A", H, "Recognise homotopy equivalence and say what a space deformation-retracts to.",
  "Two spaces are homotopy equivalent when each maps to the other with both composites homotopic to the identity. A deformation retraction shrinks a space onto a subspace: an annulus or a Möbius band onto a circle, a disc onto a point."),
 ("TP-5.1.B", H + K, "Name the fundamental group of a standard space and find the rank of the fundamental group of a graph.",
  "π₁ is trivial for a sphere (dimension ≥ 2) or a disc, Z for the circle, Z² for the torus, Z/2 for the projective plane, and free on n generators for a wedge of n circles. A connected graph has free fundamental group of rank E − V + 1."),
 ("TP-5.1.C", V, "Count sheets of a covering and use the multiplicativity of Euler characteristic.",
  "An n-sheeted covering has χ(cover) = n χ(base) and corresponds to a subgroup of index n in the fundamental group of the base. The real line covers the circle with infinitely many sheets; the sphere covers the projective plane twice."),
 ("TP-5.1.D", L, "Read Betti numbers and Euler characteristic and use the fixed-point theorems they give.",
  "χ = b₀ − b₁ + b₂ − … . A closed orientable surface of genus g has Betti numbers 1, 2g, 1; the sphere Sⁿ has homology only in degrees 0 and n. Brouwer: every continuous map of a closed ball to itself has a fixed point."),
]
ADD = [
 ("TP-5.1.A", Q("tp-homotopy-type", HT, "Up to homotopy equivalence, {{sp}} is:", pace="recall", cases=[
    {"sp": "a closed disc", "kc": 0}, {"sp": "an annulus", "kc": 1}, {"sp": "the plane with one point removed", "kc": 1}, {"sp": "the plane with two points removed", "kc": 2},
    {"sp": "a Möbius band", "kc": 1}, {"sp": "a solid torus", "kc": 1}, {"sp": "a torus with one point removed", "kc": 2}, {"sp": "three-dimensional space with one point removed", "kc": 3},
    {"sp": "the letter A", "kc": 1}, {"sp": "the letter B", "kc": 2}, {"sp": "a tree", "kc": 0}],
    choice=["A point", "A circle", "A wedge of two circles (figure eight)", "A 2-sphere"], correct="kc", verify="authored",
    explain="Thicken or shrink without tearing: count the independent holes a loop can go round. A punctured torus retracts onto its two core circles, which meet at a point")),
 ("TP-5.1.A", F("tp-homotopy-facts", [
    ("A space that is homotopy equivalent to a point is called:", "Contractible", "Compact", "Simply connected only", "Discrete"),
    ("Homotopy equivalent spaces must have the same:", "Fundamental group", "Dimension", "Number of points", "Compactness"),
    ("A disc and a point are homotopy equivalent but not homeomorphic. This shows homotopy equivalence is:", "Weaker than homeomorphism", "Stronger than homeomorphism", "The same as homeomorphism", "Unrelated to homeomorphism"),
    ("The circle is not contractible. One proof uses the fact that its fundamental group is:", "Z, which is not trivial", "Trivial", "Finite", "Z/2")],
    "Homotopy equivalence forgets dimension and thickness and keeps holes, which is what the algebraic invariants measure")),
 ("TP-5.1.B", N("tp-graph-rank", "A connected graph has edges {{ge}}. Its fundamental group is free; on how many generators?", "kans", "pm_g_cycle_rank(ge)",
    "Contract a spanning tree to a point: each of the E − (V − 1) leftover edges becomes a loop", tex="rank",
    cases=[{"ge": "a-b,b-c,c-a", "kans": 1}, {"ge": "a-b,b-c,c-a,c-d,d-a", "kans": 2}, {"ge": "a-b,a-c,a-d,b-c,b-d,c-d", "kans": 3},
           {"ge": "a-b,b-c,c-d,d-a,a-c", "kans": 2}, {"ge": "a-b,b-c,c-d,d-e,e-a,a-c,a-d", "kans": 3}, {"ge": "a-b,b-c,c-a,c-d,d-e,e-c", "kans": 2}])),
 ("TP-5.1.B", F("tp-fundamental-groups", [
    ("The fundamental group of the circle is:", "Z", "Trivial", "Z/2", "Z²"),
    ("The fundamental group of the torus is:", "Z²", "Z", "The free group on two generators", "Trivial"),
    ("The fundamental group of the real projective plane is:", "Z/2", "Z", "Trivial", "Z²"),
    ("The fundamental group of the figure eight is:", "The free group on two generators", "Z²", "Z", "Z/2"),
    ("The fundamental group of the 2-sphere is:", "Trivial", "Z", "Z/2", "Z²"),
    ("The torus and the figure eight both have two independent loops, but only the torus's loops:", "Commute", "Are contractible", "Have finite order", "Are homotopic to each other")],
    "On the torus the square with word a b a⁻¹ b⁻¹ fills in the commutator, forcing ab = ba; on the figure eight nothing does, so the group is free")),
 ("TP-5.1.C", N("tp-cover-genus", "A closed orientable surface of genus {{kg}} has a {{kn}}-sheeted covering by a closed orientable surface. What is the genus of the cover?", "kn*(kg - 1) + 1", "solve(Eq(2 - 2*Symbol('m'), kn*(2 - 2*kg)), Symbol('m'))[0]",
    "Euler characteristic multiplies by the number of sheets: 2 − 2g′ = n(2 − 2g), so g′ = n(g − 1) + 1. A torus is only ever covered by tori", tex="g'",
    given={"kg": {"pick": [1, 2, 3]}, "kn": {"pick": [2, 3, 5]}})),
 ("TP-5.1.C", F("tp-covering-facts", [
    ("The map t ↦ (cos 2πt, sin 2πt) from the real line to the circle is a covering with how many sheets?", "Infinitely many", "1", "2", "It is not a covering"),
    ("The map z ↦ zⁿ on the unit circle is a covering with how many sheets?", "n", "1", "2", "Infinitely many"),
    ("The 2-sphere covers the real projective plane with how many sheets?", "2", "1", "4", "Infinitely many"),
    ("Connected coverings of a space correspond to:", "Subgroups of its fundamental group, up to conjugacy", "Its homology groups", "Its open covers", "Its connected components"),
    ("A simply connected covering space of X is called its:", "Universal cover", "Double cover", "Quotient", "Suspension")],
    "The number of sheets is the index of the corresponding subgroup; the universal cover corresponds to the trivial subgroup")),
 ("TP-5.1.D", N("tp-betti-one", "A closed orientable surface has Euler characteristic {{kx}}. Find its first Betti number b₁.", "2 - kx", "solve(Eq(1 - Symbol('m') + 1, kx), Symbol('m'))[0]",
    "χ = b₀ − b₁ + b₂ with b₀ = b₂ = 1 for a closed connected orientable surface, so b₁ = 2 − χ = 2g", tex="b_1",
    given={"kx": {"pick": [-2, -4, -6, -8]}})),
 ("TP-5.1.D", F("tp-homology-facts", [
    ("The sphere Sⁿ (n ≥ 1) has non-zero homology in which degrees?", "0 and n only", "Every degree up to n", "n only", "0 only"),
    ("Brouwer's fixed-point theorem says every continuous map from a closed disc to itself:", "Has a fixed point", "Is a homeomorphism", "Is constant", "Has a periodic point of period 2"),
    ("There is no continuous retraction of a disc onto its boundary circle. This is proved by comparing:", "Their fundamental groups or first homology", "Their dimensions", "Their areas", "Their compactness"),
    ("The Euler characteristic can be computed from Betti numbers as:", "Their alternating sum", "Their sum", "Their product", "The largest of them"),
    ("Rⁿ and Rᵐ are not homeomorphic for n ≠ m. The proof removes a point and compares:", "The homology of the spheres that remain, up to homotopy", "The number of components", "Compactness", "Their bases")],
    "Homology turns 'there is a hole of dimension k' into a group, and maps between spaces into homomorphisms; a retraction would force an impossible factorisation of the identity on Z through 0")),
]
