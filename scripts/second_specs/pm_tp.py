"""Topology (TP, Nov 2026): topological spaces, connectedness, compactness and surfaces. Structure in UNITS (written
by scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IB Topological Spaces schedule (read through an extraction of the 2026-27 Schedules
booklet). Finite spaces make the axioms checkable on a card; tests/verify/pmcalc.py tests every union and
intersection, and glues polygon corners to count vertices."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "tp-topology", "topology", "P1"
FW = dict(id="topology", title="Topology", code="TP", domain="top", requires=["real-analysis"], level=4,
          primary="cambridge-ib-topological-spaces", also=[],
          note="Anchored on the Cambridge Topological Spaces schedule (read through an extraction). Point-set topology to compactness, then surfaces by Euler characteristic. The fundamental group, homology and knot theory are not built.",
          header=["Open sets, connectedness, compactness and the classification of surfaces. Small finite spaces carry the",
                  "definitions, because every axiom can be checked by hand on four points; the standard spaces (intervals,",
                  "the circle, the torus, the projective plane) carry the theorems."])
SKILLS = [("spaces", "Open and closed sets, closure, continuity, Hausdorff spaces and constructions", "Topological spaces", []),
          ("connected", "Connectedness, components and path-connectedness", "Connectedness", ["top.spaces"]),
          ("compact", "Open covers, Heine-Borel and what compactness guarantees", "Compactness", ["top.spaces"]),
          ("surfaces", "Polygons with sides identified, Euler characteristic and orientability", "Surfaces", ["top.connected", "top.compact"])]
IDEAS = [("OPEN", "The open sets are the structure", "Continuity, convergence, connectedness and compactness are all statements about open sets; distances are optional."),
         ("INV", "Invariants tell spaces apart", "To show two spaces differ, find a property homeomorphisms preserve that one has and the other lacks.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SP, CO, KP, SU = "top.spaces", "top.connected", "top.compact", "top.surfaces"
S = lambda *s: [f"cambridge-ib-topological-spaces:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def opens(sets):
    return {frozenset() if s == "0" else frozenset(s) for s in sets.split("|")}


def show(sets):
    return ", ".join("∅" if s == "0" else "{" + ", ".join(s) + "}" for s in sets.split("|"))


def is_top(points, sets):
    X, T = frozenset(points), opens(sets)
    return frozenset() in T and X in T and all(a | b in T and a & b in T for a in T for b in T)


def generated(points, sets):
    T = opens(sets) | {frozenset(), frozenset(points)}
    while True:
        new = {a | b for a in T for b in T} | {a & b for a in T for b in T}
        if new <= T: return len(T)
        T |= new


def closure(points, sets, sub):
    X, A = frozenset(points), frozenset(sub)
    return len(frozenset.intersection(*[X - u for u in opens(sets) if A <= X - u]))


def interior(sets, sub):
    return len(frozenset().union(*[u for u in opens(sets) if u <= frozenset(sub)]))


TOPS = ["0|a|abc", "0|a|b|abc", "0|a|ab|abc", "0|ab|bc|abc", "0|a|b|ab|abc", "0|a|bc|abc", "0|ab|ac|abc", "0|b|ab|bc|abc"]
T4 = "0|a|ab|abc|abcd"
T5 = "0|a|b|ab|abcd"

UNITS = {
 1: ("spaces", "Topological spaces", S("S1"), ["OPEN"], {
   1: ("Open sets and continuity", [
     ("A", S("S1"), "Check the axioms of a topology on a small set and generate a topology from given sets.",
      "A topology contains the empty set and the whole space and is closed under arbitrary unions and finite intersections.", "P2", [
       Q("tp-is-topology", SP, "On X = {a, b, c}, is this collection a topology: {{sh}}?", pace="recall",
         cases=[{"sh": show(t), "kc": 0 if is_top("abc", t) else 1} for t in TOPS],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Check every pairwise union and intersection. {a} and {b} force {a, b}; {a, b} and {b, c} force {b}"),
       N("tp-generated-topology", SP, "On X = {{px}}, how many open sets has the smallest topology containing {{sh}}?", "kans", "pm_top_generated(pts, sts)",
         "Add ∅ and X, then keep adding unions and intersections until nothing new appears", tex="open sets",
         cases=[{"pts": p, "px": "{" + ", ".join(p) + "}", "sts": t, "sh": show(t), "kans": generated(p, t)} for p, t in [
             ("abc", "a|b"), ("abc", "ab|bc"), ("abcd", "ab|bc"), ("abcd", "a|b|c"), ("abcd", "ab|cd"), ("abc", "a|bc")]])]),
     ("B", S("S1"), "Find the closure and interior of a subset.",
      "The closure is the smallest closed set containing A (closed means the complement is open); the interior is the largest open set inside A.", "P1", [
       N("tp-closure-size", SP, "X = {a, b, c, d} has open sets {{sh}}. How many points are in the closure of {{sa}}?", "kans", "pm_closure_size('abcd', sts, sub)",
         "List the closed sets by taking complements of the open ones, then intersect those that contain A", tex="points",
         cases=[{"sts": t, "sh": show(t), "sub": a, "sa": "{" + ", ".join(a) + "}", "kans": closure("abcd", t, a)} for t, a in [
             (T4, "a"), (T4, "b"), (T4, "d"), (T4, "c"), (T5, "a"), (T5, "c"), (T5, "ab")]]),
       N("tp-interior-size", SP, "X = {a, b, c, d} has open sets {{sh}}. How many points are in the interior of {{sa}}?", "kans", "pm_interior_size('abcd', sts, sub)",
         "Take the union of every open set that fits inside A", tex="points",
         cases=[{"sts": t, "sh": show(t), "sub": a, "sa": "{" + ", ".join(a) + "}", "kans": interior(t, a)} for t, a in [
             (T4, "abd"), (T4, "acd"), (T4, "abc"), (T5, "acd"), (T5, "abc"), (T5, "bd")]])]),
     ("C", S("S1"), "Recognise continuity, homeomorphism and topological properties, including the Hausdorff property.",
      "f is continuous when preimages of open sets are open. A homeomorphism is a continuous bijection with continuous inverse; properties it preserves are topological. In a Hausdorff space distinct points have disjoint open neighbourhoods, so limits are unique.", "P2", [
       Q("tp-topological-property", SP, "Is '{{pr}}' a topological property (preserved by every homeomorphism)?", pace="recall", cases=[
           {"pr": "compact", "kc": 0}, {"pr": "bounded", "kc": 1}, {"pr": "connected", "kc": 0}, {"pr": "complete as a metric space", "kc": 1},
           {"pr": "Hausdorff", "kc": 0}, {"pr": "having finite diameter", "kc": 1}, {"pr": "having exactly two path components", "kc": 0}, {"pr": "being a straight line", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="(0, 1) and the whole real line are homeomorphic, yet one is bounded and incomplete and the other unbounded and complete. Anything defined from distances alone is suspect"),
       F("tp-hausdorff-facts", SP, [
           ("An infinite set with the cofinite topology (open = empty or finite complement) is not Hausdorff because:", "Any two non-empty open sets meet", "Points are not closed", "It is not connected", "It is not compact"),
           ("A finite topological space is Hausdorff exactly when it is:", "Discrete", "Connected", "Indiscrete", "Compact"),
           ("In a Hausdorff space, a convergent sequence has:", "Exactly one limit", "At least two limits", "No limit points", "A constant tail"),
           ("Every metric space is Hausdorff because two distinct points at distance d are separated by:", "Open balls of radius d/2", "Closed balls of radius d", "Their complements", "A continuous function"),
           ("A function into a space with the indiscrete topology (only ∅ and X open) is:", "Always continuous", "Never continuous", "Continuous only if constant", "Continuous only if injective")],
         "Hausdorff is the weakest condition under which limits behave as in analysis")]),
     ("D", S("S1", "S4"), "Describe subspace, product and quotient topologies and identify a quotient of an interval or square.",
      "A subspace takes the intersections of open sets with it; a product is generated by products of open sets; a quotient makes a set open when its preimage is. Gluing the ends of an interval gives a circle; gluing opposite sides of a square gives a torus.", "P2", [
       F("tp-quotient-identify", SP, [
           ("Gluing the two ends of the interval [0, 1] together gives:", "A circle", "A line", "A sphere", "A point"),
           ("Gluing each pair of opposite sides of a square in the same direction gives:", "A torus", "A sphere", "A Klein bottle", "A cylinder"),
           ("Gluing one pair of opposite sides of a square in the same direction gives:", "A cylinder", "A Möbius band", "A torus", "A disc"),
           ("Gluing one pair of opposite sides of a square with a half twist gives:", "A Möbius band", "A cylinder", "A torus", "A projective plane"),
           ("Collapsing the boundary circle of a closed disc to a single point gives:", "A sphere", "A torus", "A circle", "A disc"),
           ("Gluing antipodal points of a sphere together gives:", "The real projective plane", "A torus", "A hemisphere with boundary", "A Klein bottle")],
         "Draw the square with arrows on its sides: matching arrows in the same direction roll up, opposed arrows twist"),
       N("tp-product-discrete", SP, "X has {{km}} points and Y has {{kn}} points, both with the discrete topology. How many open sets has the product X × Y?", "2^(km*kn)", "2**pm_inj(1, km*kn)",
         "The product of discrete spaces is discrete, so every one of the subsets of the mn points is open", tex="open sets",
         given={"km": {"pick": [2, 3]}, "kn": {"pick": [2, 3, 4]}})])]),
 }),
 2: ("connected", "Connectedness", S("S2"), ["INV"], {
   1: ("Connected and path-connected spaces", [
     ("A", S("S2"), "Decide whether a space is connected and count its components.",
      "A space is connected when it is not the union of two disjoint non-empty open sets. Removing a point disconnects the line but not the plane, which is one way to tell them apart.", "P1", [
       N("tp-components-line", CO, "How many connected components has the real line with {{kk}} points removed?", "kk + 1", "summation(1, (nn, 1, kk)) + 1",
         "Each removed point cuts one interval into two. In the plane the same removal leaves a single component, so the line and the plane are not homeomorphic", tex="components",
         given={"kk": {"pick": [1, 2, 3, 5]}}),
       Q("tp-connected-or-not", CO, "Is this space connected: {{sp}}?", pace="recall", cases=[
           {"sp": "the rational numbers, as a subspace of the real line", "kc": 1}, {"sp": "the plane with one point removed", "kc": 0}, {"sp": "the real line with one point removed", "kc": 1},
           {"sp": "the circle with one point removed", "kc": 0}, {"sp": "the union of [0, 1] and [2, 3]", "kc": 1}, {"sp": "invertible 2×2 real matrices", "kc": 1},
           {"sp": "a two-point set with the indiscrete topology", "kc": 0}, {"sp": "a two-point set with the discrete topology", "kc": 1}, {"sp": "the plane with a circle removed", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Look for a continuous function onto {0, 1}: the sign of the determinant splits the invertible matrices, and comparison with an irrational splits the rationals")]),
     ("B", S("S2"), "Relate connectedness, path-connectedness and continuous images.",
      "A continuous image of a connected space is connected (the intermediate value theorem is the case of an interval). Path-connected implies connected; the converse holds for open subsets of Euclidean space but fails for the topologist's sine curve.", "P2", [
       F("tp-connected-theorems", CO, [
           ("The intermediate value theorem is the statement that the continuous image of an interval is:", "Connected", "Compact", "Closed", "Open"),
           ("The closure of the graph of sin(1/x) for x > 0 (the topologist's sine curve) is:", "Connected but not path-connected", "Path-connected", "Neither connected nor path-connected", "Compact and path-connected"),
           ("For an open subset of Euclidean space, connected and path-connected are:", "Equivalent", "Unrelated", "Never both true", "Equivalent only in the plane"),
           ("There is no continuous map from [0, 1] onto {0, 1} with the discrete topology because [0, 1] is:", "Connected", "Compact", "Hausdorff", "Uncountable"),
           ("The product of two connected spaces is:", "Connected", "Connected only if both are compact", "Never connected", "Path-connected")],
         "Connectedness passes forward along continuous maps, which is why it works as an invariant"),
       Q("tp-homeomorphic-or-not", CO, "Are {{sa}} and {{sb}} homeomorphic?", pace="recall", cases=[
           {"sa": "(0, 1)", "sb": "the real line", "kc": 0}, {"sa": "[0, 1]", "sb": "(0, 1)", "kc": 1}, {"sa": "the real line", "sb": "the plane", "kc": 1},
           {"sa": "a circle", "sb": "a square's boundary", "kc": 0}, {"sa": "a circle", "sb": "[0, 1]", "kc": 1}, {"sa": "the letter X", "sb": "the letter Y", "kc": 1},
           {"sa": "a coffee cup with one handle", "sb": "a doughnut", "kc": 0}, {"sa": "[0, 1)", "sb": "(0, 1)", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="Remove a point and count components: an interior point cuts an interval in two but no point cuts a circle; the centre of X leaves four pieces and no point of Y leaves more than three. Compactness separates [0, 1] from (0, 1)")])]),
 }),
 3: ("compact", "Compactness", S("S3"), ["INV", "OPEN"], {
   1: ("Compact spaces", [
     ("A", S("S3"), "Decide whether a space is compact.",
      "Compact means every open cover has a finite subcover. Heine-Borel: a subset of Euclidean space is compact exactly when it is closed and bounded.", "P2", [
       Q("tp-compact-or-not", KP, "Is this space compact: {{sp}}?", pace="recall", cases=[
           {"sp": "the closed interval [0, 1]", "kc": 0}, {"sp": "the open interval (0, 1)", "kc": 1}, {"sp": "the real line", "kc": 1}, {"sp": "the unit circle", "kc": 0},
           {"sp": "the set {0} ∪ {1/n : n ≥ 1}", "kc": 0}, {"sp": "the set {1/n : n ≥ 1}", "kc": 1}, {"sp": "the rationals in [0, 1]", "kc": 1}, {"sp": "the unit sphere", "kc": 0},
           {"sp": "any finite space", "kc": 0}, {"sp": "the closed half-line [0, ∞)", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="In Euclidean space check closed and bounded. {1/n} is bounded but misses its limit point 0; adding 0 makes it compact"),
       N("tp-cover-count", KP, "What is the smallest number of open intervals of length {{kl}} that can cover the closed interval [0, {{ka}}]?", "floor(ka/kl) + 1", "pm_first_n('1/n', 0, nsimplify(kl)/ka)",
         "n open intervals of length ℓ cover strictly less than nℓ of a closed interval, so nℓ must exceed a. Compactness is what guarantees finitely many are ever enough", tex="intervals",
         cases=[{"ka": 1, "kl": 0.3}, {"ka": 2, "kl": 0.5}, {"ka": 5, "kl": 1}, {"ka": 3, "kl": 0.7}, {"ka": 10, "kl": 3}])]),
     ("B", S("S3"), "Use what compactness guarantees.",
      "Closed subsets of compact spaces are compact; compact subsets of Hausdorff spaces are closed; continuous images of compact spaces are compact; a continuous bijection from a compact space to a Hausdorff space is a homeomorphism.", "P2", [
       F("tp-compact-theorems", KP, [
           ("A continuous real-valued function on a compact space is bounded and attains its bounds because its image is:", "A compact subset of the real line", "An open interval", "Connected", "Countable"),
           ("A continuous bijection from a compact space onto a Hausdorff space is automatically:", "A homeomorphism", "Constant", "A contraction", "Open but not closed"),
           ("A compact subset of a Hausdorff space is always:", "Closed", "Open", "Finite", "Connected"),
           ("The map t ↦ (cos t, sin t) from [0, 2π) onto the circle is a continuous bijection but not a homeomorphism. Which hypothesis fails?", "[0, 2π) is not compact", "The circle is not Hausdorff", "The map is not continuous", "The map is not surjective"),
           ("A metric space is compact exactly when:", "Every sequence has a convergent subsequence", "It is bounded", "It is complete", "It is closed")],
         "Most uses of compactness are one of these four facts, usually the image fact"),
       Q("tp-cover-no-finite", KP, "Does the open cover {{cv}} of {{sp}} have a finite subcover?", pace="recall", cases=[
           {"cv": "{(1/n, 1) : n ≥ 2}", "sp": "(0, 1)", "kc": 1}, {"cv": "{(−n, n) : n ≥ 1}", "sp": "the real line", "kc": 1}, {"cv": "{(−n, n) : n ≥ 1}", "sp": "[0, 5]", "kc": 0},
           {"cv": "{(x − 1, x + 1) : x an integer}", "sp": "[0, 10]", "kc": 0}, {"cv": "{(1/n, 2) : n ≥ 1}", "sp": "(0, 1]", "kc": 1}, {"cv": "{(1/n, 2) : n ≥ 1} with (−1, 0.01) added", "sp": "[0, 1]", "kc": 0}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="A nested cover has a finite subcover only if one of its sets already covers everything. On (0, 1) the sets (1/n, 1) never reach 0, and that single failing cover is enough to show (0, 1) is not compact")])]),
 }),
 4: ("surfaces", "Surfaces", S("S4", "S5"), ["INV"], {
   1: ("Polygons, Euler characteristic and classification", [
     ("A", S("S5"), "Compute an Euler characteristic and the genus it implies.",
      "χ = V − E + F for any triangulation or polygonal division. A closed orientable surface of genus g has χ = 2 − 2g: sphere 2, torus 0, double torus −2.", "P1", [
       N("tp-euler-characteristic", SU, "A closed surface is divided into {{kf}} faces with {{ke}} edges and {{kv}} vertices. Find its Euler characteristic.", "kv - ke + kf", "pm_inj(1, kv + kf) - ke",
         "χ = V − E + F, and the result does not depend on how the surface was cut up", tex="\\chi",
         cases=[{"kv": 8, "ke": 12, "kf": 6}, {"kv": 12, "ke": 30, "kf": 20}, {"kv": 6, "ke": 15, "kf": 10}, {"kv": 4, "ke": 6, "kf": 4}, {"kv": 10, "ke": 30, "kf": 18}, {"kv": 7, "ke": 21, "kf": 12}]),
       N("tp-genus-from-chi", SU, "A closed orientable surface has Euler characteristic {{kx}}. What is its genus?", "(2 - kx)/2", "solve(Eq(2 - 2*Symbol('m'), kx), Symbol('m'))[0]",
         "χ = 2 − 2g, so g = (2 − χ)/2: each handle lowers the Euler characteristic by 2", tex="g",
         given={"kx": {"pick": [-2, -4, -6, -10]}})]),
     ("B", S("S4"), "Read a polygon with sides identified: count its vertices and name the surface.",
      "Follow each corner round the gluing to see which corners become one point. With one face and n edge pairs, χ = V − n + 1. Standard words: a a⁻¹ sphere, a a projective plane, a b a⁻¹ b⁻¹ torus, a b a b⁻¹ Klein bottle.", "P1", [
       N("tp-polygon-vertices", SU, "A polygon has its sides glued according to the word {{sh}}. How many distinct points do its corners become?", "kans", "pm_surface_vertices(wd)",
         "Start at one corner and chase it through each identification until you return; repeat for corners not yet reached", tex="vertices",
         cases=[{"wd": "a b A B", "sh": "a b a⁻¹ b⁻¹", "kans": 1}, {"wd": "a A", "sh": "a a⁻¹", "kans": 2}, {"wd": "a a", "sh": "a a", "kans": 1},
                {"wd": "a b a B", "sh": "a b a b⁻¹", "kans": 1}, {"wd": "a b B A", "sh": "a b b⁻¹ a⁻¹", "kans": 3}, {"wd": "a b A B c d C D", "sh": "a b a⁻¹ b⁻¹ c d c⁻¹ d⁻¹", "kans": 1},
                {"wd": "a b c A B C", "sh": "a b c a⁻¹ b⁻¹ c⁻¹", "kans": 2}]),
       F("tp-polygon-surface", SU, [
           ("The square with sides glued by the word a b a⁻¹ b⁻¹ is:", "A torus", "A Klein bottle", "A sphere", "A projective plane"),
           ("The square with sides glued by the word a b a b⁻¹ is:", "A Klein bottle", "A torus", "A sphere", "A projective plane"),
           ("The two-sided polygon with word a a is:", "A projective plane", "A sphere", "A torus", "A Möbius band"),
           ("The square with sides glued by the word a b b⁻¹ a⁻¹ is:", "A sphere", "A torus", "A Klein bottle", "A projective plane"),
           ("The octagon with word a b a⁻¹ b⁻¹ c d c⁻¹ d⁻¹ is:", "A double torus", "A torus", "A Klein bottle", "A sphere")],
         "A letter that appears twice in the same direction makes the surface non-orientable; a commutator a b a⁻¹ b⁻¹ is one handle")]),
     ("C", S("S5"), "Use orientability and the Euler characteristic to classify a closed surface.",
      "Every closed surface is a sphere with g handles (χ = 2 − 2g) or a sphere with k crosscaps (χ = 2 − k). Orientability and χ together determine the surface. A connected sum has χ(A # B) = χ(A) + χ(B) − 2.", "P1", [
       N("tp-chi-from-word", SU, "Find the Euler characteristic of the closed surface given by the polygon word {{sh}}.", "kans", "pm_surface_chi(wd)",
         "One face, half as many edges as letters, and the vertex count from gluing corners: χ = V − E + 1", tex="\\chi",
         cases=[{"wd": "a A", "sh": "a a⁻¹", "kans": 2}, {"wd": "a a", "sh": "a a", "kans": 1}, {"wd": "a b A B c d C D", "sh": "a b a⁻¹ b⁻¹ c d c⁻¹ d⁻¹", "kans": -2},
                {"wd": "a a b b c c", "sh": "a a b b c c", "kans": -1}, {"wd": "a b c A B C", "sh": "a b c a⁻¹ b⁻¹ c⁻¹", "kans": 0},
                {"wd": "a b A B c d C D e f E F", "sh": "a b a⁻¹ b⁻¹ c d c⁻¹ d⁻¹ e f e⁻¹ f⁻¹", "kans": -4}, {"wd": "a a b b c c d d", "sh": "a a b b c c d d", "kans": -2}]),
       N("tp-connected-sum", SU, "A surface is the connected sum of a genus-{{kg}} orientable surface and {{kk}} projective planes. Find its Euler characteristic.", "2 - 2*kg - kk", "(2 - 2*kg) + kk*1 - 2*kk",
         "Each connected sum removes a disc from both surfaces and glues, costing 2: start from 2 − 2g and add (1 − 2) for each projective plane", tex="\\chi",
         given={"kg": {"pick": [1, 2, 3]}, "kk": {"pick": [1, 2, 3]}})])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
