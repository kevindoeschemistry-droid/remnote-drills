"""Topology, the intermediate steps (Nov 2026): 11 objectives between the ones draft 1 jumped across — distances and
open sets on the real line before abstract topologies, continuity checked on finite spaces, covers counted by hand,
and surfaces by Euler's formula before polygon words. NEEDS rewires the framework. Basis unchanged."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "tp-steps", "topology", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SP, CO, KP, SU = "top.spaces", "top.connected", "top.compact", "top.surfaces"
S = lambda *s: [f"cambridge-ib-topological-spaces:{x}" for x in s]
M = ["cambridge-ib-analysis-ii:M"]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=True, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


def opens(sets):
    return {frozenset() if s == "0" else frozenset(s) for s in sets.split("|")}


def show(sets):
    return ", ".join("∅" if s == "0" else "{" + ", ".join(s) + "}" for s in sets.split("|"))


def cont(sets, fmap, tsets):
    f = dict(pr.split(">") for pr in fmap.split(","))
    return all(frozenset(a for a in f if f[a] in u) in opens(sets) for u in opens(tsets))


SIER = "0|x|xy"          # Sierpinski space on {x, y}
T3 = "0|a|ab|abc"
MAPS = [(T3, "a>x,b>y,c>y", SIER), (T3, "a>y,b>x,c>x", SIER), (T3, "a>x,b>x,c>y", SIER), (T3, "a>y,b>y,c>x", SIER), ("0|a|b|ab|abc", "a>x,b>x,c>y", SIER), ("0|a|b|ab|abc", "a>x,b>y,c>x", SIER)]


def mshow(m):
    return ", ".join(pr.replace(">", " ↦ ") for pr in m.split(","))


TOPICS = {"1.2": "Distances and open sets on the line", "2.2": "Continuity on small spaces", "3.2": "Covers by hand", "4.2": "Surfaces by Euler's formula"}
OBJS = [
 ("TP-1.2.A", M + S("S1"), "Check the axioms of a metric and compute distances in different metrics.", "A metric is non-negative, zero only between equal points, symmetric, and satisfies the triangle inequality. The Euclidean, taxicab and maximum metrics on the plane give different distances but the same open sets."),
 ("TP-1.2.B", S("S1"), "Decide whether a subset of the real line is open, closed, both or neither.", "A set is open if every point has a small interval around it inside the set, and closed if its complement is open. Only the empty set and the whole line are both; a half-open interval is neither."),
 ("TP-1.2.C", S("S1"), "Find the boundary, interior and closure of a union of intervals.", "The interior drops every endpoint, the closure adds every endpoint, and the boundary is the closure minus the interior: the endpoints and isolated points."),
 ("TP-1.2.D", S("S1"), "Identify the limit points of a set and relate them to closedness.", "x is a limit point of A if every neighbourhood of x meets A in a point other than x. A set is closed exactly when it contains all its limit points."),
 ("TP-2.2.A", S("S1"), "Test a map between finite spaces for continuity by pulling back open sets.", "f is continuous when the preimage of every open set is open. Into the two-point Sierpinski space, a continuous map is the same thing as a choice of open set."),
 ("TP-2.2.B", S("S1"), "Generate a topology from a basis or subbasis.", "A subbasis generates the topology whose open sets are unions of finite intersections of its members; it is the smallest topology in which those sets are open."),
 ("TP-3.2.A", S("S3"), "Extract a smallest subcover from a cover.", "A subcover keeps some of the cover's sets and still covers the space. Compactness says a finite one always exists; finding the smallest is a counting problem."),
 ("TP-3.2.B", S("S2"), "Count the connected components of a graph or a union of intervals.", "Components are the maximal connected pieces. For a graph, V − E + (number of independent cycles) counts them; for intervals on a line, pieces that overlap or touch merge."),
 ("TP-4.2.A", S("S5"), "Use Euler's formula on the sphere and on other surfaces.", "A division of a surface into faces satisfies V − E + F = χ: 2 on a sphere, 0 on a torus. So a map on a torus has two fewer faces than the same vertex and edge counts would give on a sphere."),
 ("TP-4.2.B", S("S5"), "Count handles or crosscaps from the Euler characteristic.", "An orientable closed surface has g = (2 − χ)/2 handles; a non-orientable one has k = 2 − χ crosscaps. One crosscap is the projective plane, two the Klein bottle."),
 ("TP-4.2.C", S("S4", "S5"), "Name a closed surface from its orientability and Euler characteristic.", "The pair (orientable or not, χ) determines a closed surface: orientable χ = 2 sphere, 0 torus, −2 double torus; non-orientable χ = 1 projective plane, 0 Klein bottle."),
]
ADD = [
 ("TP-1.2.A", N("tp-metric-distance", SP, "Find the {{nm}} distance between (0, 0) and ({{ka}}, {{kb}}).", "kans", "calc(vy)",
    "Euclidean: √(a² + b²). Taxicab: |a| + |b|. Maximum: the larger of |a| and |b|", tex="d",
    cases=[{"nm": "taxicab", "ka": 3, "kb": 4, "kans": 7, "vy": "Abs(3) + Abs(4)"}, {"nm": "Euclidean", "ka": 3, "kb": 4, "kans": 5, "vy": "sqrt(3**2 + 4**2)"}, {"nm": "maximum", "ka": 3, "kb": 4, "kans": 4, "vy": "Max(3, 4)"},
           {"nm": "taxicab", "ka": 5, "kb": 12, "kans": 17, "vy": "5 + 12"}, {"nm": "Euclidean", "ka": 5, "kb": 12, "kans": 13, "vy": "sqrt(5**2 + 12**2)"}, {"nm": "maximum", "ka": 8, "kb": 6, "kans": 8, "vy": "Max(8, 6)"}])),
 ("TP-1.2.A", Q("tp-is-metric", SP, "Is d(x, y) = {{dd}} a metric on the real line?", pace="recall", cases=[
    {"dd": "|x − y|", "kc": 0}, {"dd": "(x − y)²", "kc": 1}, {"dd": "|x² − y²|", "kc": 1}, {"dd": "1 if x and y differ, 0 if they are equal", "kc": 0},
    {"dd": "x − y", "kc": 1}, {"dd": "√|x − y|", "kc": 0}, {"dd": "2|x − y|", "kc": 0}, {"dd": "|x − y|/(1 + |x − y|)", "kc": 0}],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="(x − y)² fails the triangle inequality (0, 1, 2 gives 4 > 1 + 1); |x² − y²| is zero for x = −y; x − y can be negative. Concave increasing functions of a metric that vanish at 0, such as √ and t/(1 + t), give metrics again")),
 ("TP-1.2.B", Q("tp-open-closed-line", SP, "As a subset of the real line, {{st}} is:", pace="recall", cases=[
    {"st": "(0, 1)", "kc": 0}, {"st": "[0, 1]", "kc": 1}, {"st": "[0, 1)", "kc": 3}, {"st": "the whole real line", "kc": 2}, {"st": "the integers", "kc": 1},
    {"st": "the rationals", "kc": 3}, {"st": "(0, 1) ∪ (2, 3)", "kc": 0}, {"st": "{1/n : n ≥ 1}", "kc": 3}, {"st": "{0} ∪ {1/n : n ≥ 1}", "kc": 1}, {"st": "(0, ∞)", "kc": 0}, {"st": "[0, ∞)", "kc": 1}],
    choice=["Open, not closed", "Closed, not open", "Both open and closed", "Neither"], correct="kc", verify="authored",
    explain="Check each endpoint and each accumulation point: is it in the set (needed for closed), and does every point have room around it (needed for open)?")),
 ("TP-1.2.B", F("tp-open-closed-facts", SP, [
    ("An arbitrary union of open sets is:", "Open", "Closed", "Neither in general", "Compact"),
    ("The intersection of the open intervals (−1/n, 1/n) over all n ≥ 1 is {0}, which shows that an infinite intersection of open sets:", "Need not be open", "Is always open", "Is always empty", "Is never closed"),
    ("The complement of a closed set is:", "Open", "Closed", "Compact", "Bounded"),
    ("In the real line, the sets that are both open and closed are:", "Only the empty set and the whole line", "All intervals", "The finite sets", "None"),
    ("A finite set of points in the real line is:", "Closed", "Open", "Both", "Neither")],
    "Open and closed are not opposites: most sets are neither, and in a connected space only two are both")),
 ("TP-1.2.C", N("tp-boundary-count", SP, "How many boundary points has the set {{sh}} in the real line?", "kans", "pm_boundary_count(pcs)",
    "List every endpoint and isolated point, then discard any that lie inside another piece", tex="points",
    cases=[{"pcs": "(0,1);[2,3)", "sh": "(0, 1) ∪ [2, 3)", "kans": 4}, {"pcs": "(0,1);{5}", "sh": "(0, 1) ∪ {5}", "kans": 3}, {"pcs": "[0,2];(1,3)", "sh": "[0, 2] ∪ (1, 3)", "kans": 2},
           {"pcs": "(0,1);(1,2)", "sh": "(0, 1) ∪ (1, 2)", "kans": 3}, {"pcs": "{1};{2};{3}", "sh": "{1, 2, 3}", "kans": 3}, {"pcs": "(0,4);{2}", "sh": "(0, 4) ∪ {2}", "kans": 2}])),
 ("TP-1.2.C", F("tp-closure-interior-line", SP, [
    ("The closure of (0, 1) ∪ (1, 2) in the real line is:", "[0, 2]", "(0, 2)", "[0, 1) ∪ (1, 2]", "(0, 1) ∪ (1, 2)"),
    ("The interior of [0, 1] ∪ {2} is:", "(0, 1)", "[0, 1]", "(0, 1) ∪ {2}", "Empty"),
    ("The closure of the rationals in the real line is:", "The whole real line", "The rationals", "The irrationals", "Empty"),
    ("The interior of the rationals in the real line is:", "Empty", "The rationals", "The whole real line", "The integers"),
    ("The boundary of the rationals in the real line is:", "The whole real line", "Empty", "The rationals", "The irrationals")],
    "A dense set with dense complement has empty interior and everything as its boundary")),
 ("TP-1.2.D", Q("tp-limit-point-count", SP, "How many limit points has the set {{st}} in the real line?", pace="recall", cases=[
    {"st": "{1/n : n ≥ 1}", "kc": 1}, {"st": "the integers", "kc": 0}, {"st": "{1, 2, 3}", "kc": 0}, {"st": "{1/n + 1/m : n, m ≥ 1}", "kc": 3},
    {"st": "{(−1)ⁿ + 1/n : n ≥ 1}", "kc": 2}, {"st": "the open interval (0, 1)", "kc": 3}, {"st": "{n + 1/n : n ≥ 1}", "kc": 0}],
    choice=["None", "Exactly one", "Exactly two", "Infinitely many"], correct="kc", verify="authored",
    explain="{1/n} accumulates only at 0. {1/n + 1/m} accumulates at 0 and at every 1/n. Every point of [0, 1] is a limit point of (0, 1)")),
 ("TP-1.2.D", F("tp-limit-point-facts", SP, [
    ("A set is closed exactly when it contains:", "All its limit points", "No limit points", "At least one limit point", "Only isolated points"),
    ("0 is a limit point of {1/n : n ≥ 1}. Is 0 in the set?", "No, so the set is not closed", "Yes", "No, but the set is closed anyway", "It depends on n"),
    ("A point of a set that is not a limit point of it is called:", "An isolated point", "A boundary point", "An interior point", "A cluster point"),
    ("The closure of a set is the set together with:", "Its limit points", "Its interior", "Its complement", "Its isolated points")],
    "Limit points are where the set piles up; closing a set means adding them")),
 ("TP-2.2.A", Q("tp-finite-continuous", SP, "X = {a, b, c} has open sets {{s1}}; Y = {x, y} has open sets {{s2}}. Is the map {{mp}} continuous?", pace="recall",
    cases=[{"s1": show(a), "s2": show(c), "mp": mshow(b), "kc": 0 if cont(a, b, c) else 1} for a, b, c in MAPS],
    choice=["Yes", "No"], correct="kc", verify="authored",
    explain="Only one non-trivial open set of Y needs checking: {x}. The map is continuous exactly when the points sent to x form an open set of X")),
 ("TP-2.2.A", F("tp-continuity-finite-facts", SP, [
    ("Every map out of a space with the discrete topology is:", "Continuous", "Constant", "Open", "A homeomorphism"),
    ("Every map into a space with the indiscrete topology is:", "Continuous", "Constant", "Injective", "Never continuous"),
    ("A constant map between topological spaces is:", "Always continuous", "Continuous only if the target is discrete", "Never continuous", "A homeomorphism"),
    ("The identity map from the real line with the usual topology to the real line with the discrete topology is:", "Not continuous", "Continuous", "A homeomorphism", "Constant"),
    ("Continuity can be checked on:", "A subbasis of the target", "A single open set always", "Closed sets only", "Points only")],
    "More open sets in the source, or fewer in the target, make continuity easier")),
 ("TP-2.2.B", N("tp-subbasis-topology", SP, "On X = {{px}}, the sets {{sh}} are taken as a subbasis. How many open sets has the topology they generate?", "kans", "pm_top_generated(pts, sts)",
    "Form all finite intersections, then all unions, and include ∅ and X", tex="open sets",
    cases=[{"pts": p, "px": "{" + ", ".join(p) + "}", "sts": t, "sh": show(t), "kans": k} for p, t, k in [("abc", "ab|bc", 5), ("abcd", "abc|bcd", 5), ("abcd", "ab|bc|cd", 9), ("abc", "a|bc", 4), ("abcd", "abc|cd", 5)]])),
 ("TP-2.2.B", F("tp-basis-facts", SP, [
    ("A basis for the usual topology on the real line is the set of all:", "Open intervals", "Closed intervals", "Single points", "Half-lines only"),
    ("A subbasis for the usual topology on the real line is the set of all:", "Open half-lines (a, ∞) and (−∞, b)", "Closed intervals", "Single points", "Finite sets"),
    ("The topology generated by a subbasis is the:", "Smallest topology containing it", "Largest topology containing it", "Discrete topology", "Indiscrete topology"),
    ("A basis for the discrete topology on a set is the set of all:", "Single points", "Pairs of points", "Cofinite sets", "The whole set only"),
    ("The product topology on X × Y has as a basis the sets:", "U × V with U and V open", "All subsets of X × Y", "U × Y only", "Graphs of continuous functions")],
    "A basis lets you describe a topology by a manageable family: every open set is a union of basic ones")),
 ("TP-3.2.A", N("tp-min-subcover", KP, "X = {{px}} is covered by the sets {{sh}}. What is the smallest number of them that still covers X?", "kans", "pm_min_cover(pts, sts)",
    "Look for points that lie in only one set (that set is forced), then cover what remains as cheaply as possible", tex="sets",
    cases=[{"pts": p, "px": "{" + ", ".join(p) + "}", "sts": t, "sh": show(t), "kans": k} for p, t, k in [("abcd", "ab|bc|cd|a|d", 2), ("abcde", "abc|cd|de|a|e", 2), ("abcd", "a|b|c|d|ab", 3), ("abcdef", "ab|cd|ef|abc|def", 2), ("abcde", "ab|bc|cd|de", 3)]])),
 ("TP-3.2.A", N("tp-unit-interval-cover", KP, "The closed interval [0, 1] is covered by the open intervals (k/{{kn}} − 1/{{kn}}, k/{{kn}} + 1/{{kn}}) for all integers k. How many of them are needed to cover [0, 1]?", "kn + 1", "summation(1, (nn, 0, kn))",
    "The interval centred at k/n is needed to cover the point k/n itself, since no other interval of the family contains it; that forces k = 0, 1, …, n", tex="intervals",
    given={"kn": {"pick": [2, 3, 5, 10]}})),
 ("TP-3.2.B", N("tp-graph-components", CO, "A graph has {{kv}} vertices and edges {{ge}}. How many connected components does it have?", "kans", "pm_g_components(ge, kv)",
    "Group the vertices joined by paths; vertices that appear in no edge are components by themselves", tex="components",
    cases=[{"kv": 6, "ge": "a-b,b-c,d-e", "kans": 3}, {"kv": 5, "ge": "a-b,c-d", "kans": 3}, {"kv": 7, "ge": "a-b,b-c,c-a,d-e,e-f", "kans": 3}, {"kv": 4, "ge": "a-b,b-c,c-d", "kans": 1}, {"kv": 8, "ge": "a-b,c-d,e-f", "kans": 5}])),
 ("TP-3.2.B", N("tp-interval-components", CO, "How many connected components has {{sh}} as a subspace of the real line?", "kans", "pm_interval_components(pcs)",
    "Intervals that overlap or share an included endpoint merge; a gap of even one missing point separates", tex="components",
    cases=[{"pcs": "(0,1);(1,2)", "sh": "(0, 1) ∪ (1, 2)", "kans": 2}, {"pcs": "(0,1);[1,2)", "sh": "(0, 1) ∪ [1, 2)", "kans": 1}, {"pcs": "[0,1];[2,3];{5}", "sh": "[0, 1] ∪ [2, 3] ∪ {5}", "kans": 3},
           {"pcs": "(0,2);(1,3);(4,5)", "sh": "(0, 2) ∪ (1, 3) ∪ (4, 5)", "kans": 2}, {"pcs": "{1};{2};{3};{4}", "sh": "{1, 2, 3, 4}", "kans": 4}])),
 ("TP-4.2.A", N("tp-faces-on-surface", SU, "A connected graph with {{kv}} vertices and {{ke}} edges is drawn on a {{nm}} so that every face is a disc. How many faces are there?", "kx - kv + ke", "solve(Eq(kv - ke + Symbol('m'), kx), Symbol('m'))[0]",
    "V − E + F equals the surface's Euler characteristic: 2 for a sphere, 0 for a torus, −2 for a double torus", tex="F",
    cases=[{"nm": "sphere", "kx": 2, "kv": 8, "ke": 12}, {"nm": "torus", "kx": 0, "kv": 7, "ke": 21}, {"nm": "torus", "kx": 0, "kv": 9, "ke": 18}, {"nm": "sphere", "kx": 2, "kv": 20, "ke": 30}, {"nm": "double torus", "kx": -2, "kv": 6, "ke": 16}])),
 ("TP-4.2.A", F("tp-euler-formula-facts", SU, [
    ("The complete graph K₇ (7 vertices, 21 edges) can be drawn on a torus with every face a triangle. How many faces?", "14", "16", "12", "21"),
    ("For a convex polyhedron, V − E + F equals:", "2", "0", "1", "4"),
    ("A soccer ball has 12 pentagons and 20 hexagons. Its number of edges is:", "90", "60", "120", "32"),
    ("The Euler characteristic of a surface is a topological invariant, meaning it:", "Does not depend on how the surface is divided up", "Changes under stretching", "Depends on the number of faces chosen", "Is defined only for polyhedra")],
    "Count edges from the faces: (12 · 5 + 20 · 6)/2 = 90, since each edge borders two faces")),
 ("TP-4.2.B", N("tp-crosscaps", SU, "A closed non-orientable surface has Euler characteristic {{kx}}. How many crosscaps (projective planes in its connected sum) does it have?", "2 - kx", "solve(Eq(2 - Symbol('m'), kx), Symbol('m'))[0]",
    "χ = 2 − k for a sphere with k crosscaps: each one lowers the Euler characteristic by 1", tex="k",
    given={"kx": {"pick": [1, -1, -2, -3, -5]}})),
 ("TP-4.2.B", N("tp-sum-genus", SU, "The connected sum of a genus-{{ka}} and a genus-{{kb}} orientable surface has what genus?", "ka + kb", "solve(Eq(2 - 2*Symbol('m'), (2 - 2*ka) + (2 - 2*kb) - 2), Symbol('m'))[0]",
    "Handles add. In terms of Euler characteristic, χ(A # B) = χ(A) + χ(B) − 2", tex="g",
    given={"ka": {"pick": [1, 2, 3]}, "kb": {"pick": [1, 2, 4]}})),
 ("TP-4.2.C", Q("tp-name-surface", SU, "Which closed surface is {{ori}} with Euler characteristic {{kx}}?", pace="recall", cases=[
    {"ori": "orientable", "kx": 2, "kc": 0}, {"ori": "orientable", "kx": 0, "kc": 1}, {"ori": "non-orientable", "kx": 1, "kc": 2}, {"ori": "non-orientable", "kx": 0, "kc": 3}, {"ori": "orientable", "kx": -2, "kc": 4}],
    choice=["Sphere", "Torus", "Projective plane", "Klein bottle", "Double torus"], correct="kc", verify="authored",
    explain="Orientable: χ = 2 − 2g gives sphere, torus, double torus. Non-orientable: χ = 2 − k gives the projective plane for one crosscap and the Klein bottle for two")),
 ("TP-4.2.C", F("tp-classification-facts", SU, [
    ("The torus and the Klein bottle both have Euler characteristic 0. They are told apart by:", "Orientability", "Compactness", "Connectedness", "The number of faces"),
    ("A Möbius band is a projective plane with what removed?", "A disc", "A point pair", "A handle", "A circle through the centre"),
    ("The connected sum of two projective planes is:", "A Klein bottle", "A torus", "A sphere", "A projective plane"),
    ("The connected sum of a torus and a projective plane is the same surface as the connected sum of:", "Three projective planes", "Two tori", "A Klein bottle and a sphere", "A sphere and a torus"),
    ("Every closed surface can be embedded in three-dimensional space without self-intersection only if it is:", "Orientable", "Non-orientable", "Of genus 0", "Simply connected")],
    "Two invariants classify closed surfaces completely, which is rare in topology")),
]
NEEDS = {
 "TP-1.2.A": ["RA-6.2.A"], "TP-1.2.B": ["TP-1.2.A", "RA-4.1.A"], "TP-1.2.C": ["TP-1.2.B"], "TP-1.2.D": ["TP-1.2.C", "RA-2.2.B"], "TP-1.1.A": ["TP-1.2.B"], "TP-1.1.B": ["TP-1.2.C"],
 "TP-2.2.A": ["TP-1.1.A"], "TP-2.2.B": ["TP-1.1.A"], "TP-1.1.C": ["TP-2.2.A"], "TP-1.1.D": ["TP-2.2.B"],
 "TP-3.2.B": ["TP-1.2.B"], "TP-2.1.A": ["TP-3.2.B"], "TP-3.2.A": ["TP-1.2.B"], "TP-3.1.A": ["TP-3.2.A", "TP-1.2.D"],
 "TP-4.2.A": ["TP-1.1.D"], "TP-4.1.A": ["TP-4.2.A"], "TP-4.2.B": ["TP-4.1.A"], "TP-4.2.C": ["TP-4.2.B"], "TP-4.1.C": ["TP-4.2.C"],
}
