"""Discrete Mathematics (DM, Nov 2026): logic and proof, induction and recursion, sets and relations, counting,
generating functions, graphs. Structure in UNITS (written to drills/frameworks/discrete-mathematics.yaml by
scripts/pm_setup.py) and two question types per objective.

Basis: the MAA CUPM 2015 Discrete Mathematics and Combinatorics report's three syllabi (read through an extraction),
with the Cambridge Numbers and Sets and Graph Theory schedules beside it. Answers here come from the formula the card
teaches; tests/verify/pmcalc.py recounts by enumeration."""
from math import comb, factorial
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "dm-discrete", "discrete-mathematics", "P1"
FW = dict(id="discrete-mathematics", title="Discrete Mathematics", code="DM", domain="dm", requires=["math-hs"], level=3,
          primary="cupm-2015-discrete", also=["cambridge-ia-numbers-sets", "cambridge-ii-graph-theory"],
          note="Anchored on the MAA CUPM 2015 report's discrete mathematics, enumerative combinatorics and graph theory syllabi (goals and syllabi read through an extraction). Computer Science keeps the algorithmic applications; this framework is the mathematics under them.",
          header=["Logic, proof, counting and graphs as mathematics. Until Nov 2026 these lived only inside Computer Science",
                  "(units 1-2), aimed at algorithms. A card cannot grade a proof, so proof objectives are drilled as what a",
                  "proof rests on: the negation, the contrapositive, the base case, the counterexample, and the count.",
                  "Not here: formal languages and automata (Computer Science), design theory, matroids, Pólya counting",
                  "beyond rotations (Abstract Algebra has Burnside)."])
SKILLS = [("logic", "Propositions, quantifiers, negation and methods of proof", "Logic and proof", []),
          ("induction", "Induction, closed forms and linear recurrences", "Induction and recursion", ["dm.logic"]),
          ("sets", "Sets, functions, relations and countability", "Sets, functions, relations", ["dm.logic"]),
          ("counting", "Permutations, combinations, distributions, inclusion-exclusion and pigeonhole", "Counting", ["dm.sets"]),
          ("gf", "Generating functions as counting machines", "Generating functions", ["dm.counting", "dm.induction"]),
          ("graphs", "Degrees, trees, circuits, colourings and planarity", "Graphs and trees", ["dm.counting"])]
IDEAS = [("PROOF", "A statement is exactly as strong as its quantifiers", "Negating, reversing or weakening a statement changes what has to be shown. Most wrong proofs prove a different statement."),
         ("COUNT", "Count by structure, not by listing", "Every count is a product, a sum, a quotient by symmetry or a complement. The work is choosing which.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
LG, IN, ST, CT, GF, GR = "dm.logic", "dm.induction", "dm.sets", "dm.counting", "dm.gf", "dm.graphs"
D = lambda *s: [f"cupm-2015-discrete:{x}" for x in s]
NS = lambda *s: [f"cambridge-ia-numbers-sets:{x}" for x in s]
GT = lambda *s: [f"cambridge-ii-graph-theory:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=True, verify=verify, explain=explain, **kw)


def change(n, coins=(1, 2, 5)):
    w = [1] + [0] * n
    for c in coins:
        for k in range(c, n + 1):
            w[k] += w[k - c]
    return w[n]


UNITS = {
 1: ("logic", "Logic and proof", D("D1") + NS("N1"), ["PROOF"], {
   1: ("Statements", [
     ("A", D("D1"), "Evaluate a compound proposition and count the cases in which it is true.",
      "A proposition in n variables has 2^n rows. p → q is false only when p is true and q is false; it is equivalent to (not p) or q.", "P1", [
       N("dm-truth-rows", LG, "In how many of the {{kr}} rows of its truth table is {{sh}} true?", "kans", "pm_tt_count(py, kv)",
         "Work row by row, or count the complement: an implication fails only where its hypothesis holds and its conclusion does not",
         tex="rows", cases=[
           {"sh": "p → q", "py": "(not p) or q", "kv": 2, "kr": 4, "kans": 3},
           {"sh": "(p and q) → r", "py": "(not (p and q)) or r", "kv": 3, "kr": 8, "kans": 7},
           {"sh": "(p or q) and not r", "py": "(p or q) and not r", "kv": 3, "kr": 8, "kans": 3},
           {"sh": "p ↔ q", "py": "p == q", "kv": 2, "kr": 4, "kans": 2},
           {"sh": "(p → q) and (q → r)", "py": "((not p) or q) and ((not q) or r)", "kv": 3, "kr": 8, "kans": 4},
           {"sh": "p → (q → r)", "py": "(not p) or ((not q) or r)", "kv": 3, "kr": 8, "kans": 7}]),
       F("dm-equivalent-forms", LG, [
           ("Which statement is logically equivalent to 'if it rains, the match is off'?", "If the match is on, it is not raining", "If the match is off, it is raining", "If it does not rain, the match is on", "It rains and the match is on"),
           ("The converse of 'if n is a multiple of 4 then n is even' is:", "If n is even then n is a multiple of 4", "If n is odd then n is not a multiple of 4", "If n is not a multiple of 4 then n is odd", "n is a multiple of 4 and n is odd"),
           ("'p → q' is equivalent to:", "(not p) or q", "p and q", "(not p) and q", "p or (not q)"),
           ("The negation of 'p and q' is:", "(not p) or (not q)", "(not p) and (not q)", "p or q", "(not p) and q"),
           ("The negation of 'p → q' is:", "p and (not q)", "(not p) → (not q)", "q → p", "(not p) and q")],
         "A statement and its contrapositive stand or fall together. The converse and the inverse are a different statement, equivalent to each other")]),
     ("B", D("D1") + NS("N1"), "Negate a quantified statement and say what a counterexample must be.",
      "Negation swaps 'for all' and 'there exists' and negates the inside. A universal claim falls to one counterexample; an existential claim needs one witness.", "P2", [
       F("dm-negate-quantifiers", LG, [
           ("The negation of 'every prime is odd' is:", "Some prime is not odd", "No prime is odd", "Every prime is even", "Some prime is odd"),
           ("The negation of 'there is a real x with x² = −1' is:", "For every real x, x² is not −1", "For some real x, x² is not −1", "For every real x, x² = −1", "There is a real x with x² = 1"),
           ("The negation of 'for every ε > 0 there is an N such that P holds' is:", "There is an ε > 0 such that for every N, P fails", "For every ε > 0 and every N, P fails", "There is an ε > 0 and an N such that P fails", "For every ε > 0 there is an N such that P fails"),
           ("The negation of 'for all x there is a y with x < y' is:", "There is an x such that every y has y ≤ x", "For all x and all y, y ≤ x", "There is an x and a y with y ≤ x", "For all x there is a y with y ≤ x")],
         "Push the 'not' through one quantifier at a time, flipping each one, and negate the final condition"),
       F("dm-counterexample", LG, [
           ("Which number is a counterexample to 'n² + n + 41 is prime for every natural number n'?", "n = 40", "n = 1", "n = 10", "n = 39"),
           ("Which pair is a counterexample to 'if ab is a multiple of 6 then a or b is a multiple of 6'?", "a = 2, b = 3", "a = 6, b = 5", "a = 12, b = 1", "a = 5, b = 7"),
           ("Which number is a counterexample to 'every odd number greater than 1 is prime'?", "9", "7", "2", "11"),
           ("Which function is a counterexample to 'every continuous function on the real line is differentiable'?", "|x|", "x²", "sin x", "e^x")],
         "A counterexample must satisfy the hypothesis and fail the conclusion. 40² + 40 + 41 = 41² is the classic one")]),
     ("C", D("D1"), "Choose a method of proof and state what it assumes and what it must reach.",
      "Direct: assume p, reach q. Contrapositive: assume not q, reach not p. Contradiction: assume p and not q, reach an impossibility. Induction: base case plus the step from k to k + 1.", "P2", [
       F("dm-proof-first-line", LG, [
           ("A proof by contrapositive of 'if n² is even then n is even' begins by assuming:", "n is odd", "n² is even", "n is even", "n² is even and n is odd"),
           ("A proof by contradiction that √2 is irrational begins by assuming:", "√2 = a/b in lowest terms", "√2 is irrational", "2 is prime", "a² = 2b² has no solutions"),
           ("A direct proof of 'the sum of two odd integers is even' begins by writing the integers as:", "2a + 1 and 2b + 1", "2a and 2b", "a and a + 2", "2a + 1 and 2a + 1"),
           ("Euclid's proof that there are infinitely many primes assumes a finite list p₁…pₙ and considers:", "p₁p₂…pₙ + 1", "p₁ + p₂ + … + pₙ", "the largest prime squared", "pₙ + 1")],
         "The first line of a proof is fixed by the method. Writing two odd numbers with the same letter proves the claim only for equal numbers"),
       F("dm-proof-flaw", LG, [
           ("A 'proof' shows the converse of the claim instead of the claim. What has been proved?", "A different statement", "The claim", "The contrapositive", "The negation"),
           ("An induction proof checks the step from k to k + 1 but no base case. What has been proved?", "Nothing: every case rests on an unchecked one", "The claim for all n", "The claim for large n", "The claim for n = 1"),
           ("To prove 'A if and only if B' you must show:", "A implies B and B implies A", "A implies B", "B implies A or A implies B", "A and B"),
           ("Checking a claim about all integers for n = 1 to 1000 proves:", "The claim for those 1000 values only", "The claim", "The claim for all positive n", "That no counterexample exists")],
         "Evidence is not proof, and a proof of the converse is a proof of something else")])]),
 }),
 2: ("induction", "Induction and recursion", D("D2", "C5") + NS("N3"), ["PROOF", "COUNT"], {
   1: ("Induction and recurrences", [
     ("A", D("D2") + NS("N3"), "Use a closed form established by induction and identify the inductive step.",
      "1 + 2 + … + n = n(n + 1)/2; the first n odd numbers sum to n²; 1² + … + n² = n(n + 1)(2n + 1)/6. The step adds the (k + 1)th term to the assumed formula for k.", "P1", [
       N("dm-sum-squares", IN, "Evaluate 1² + 2² + … + {{kn}}².", "kn*(kn + 1)*(2*kn + 1)/6", "summation(nn**2, (nn, 1, kn))",
         "The closed form n(n + 1)(2n + 1)/6 is proved by induction: adding (k + 1)² to the formula for k gives the formula for k + 1", tex="sum",
         given={"kn": {"pick": [6, 10, 12, 20]}}),
       N("dm-induction-step-term", IN, "In the inductive step for 1 + 3 + 5 + … + (2n − 1) = n², what is added to both sides to pass from n = {{kn}} to n = {{kn}} + 1?",
         "2*kn + 1", "(kn + 1)**2 - kn**2", "The next odd number is 2k + 1, and k² + 2k + 1 = (k + 1)², which is the whole proof", tex="term",
         given={"kn": {"pick": [7, 12, 20, 35]}})]),
     ("B", D("D2", "C5"), "Iterate a linear recurrence and solve it from its characteristic roots.",
      "f(n) = a f(n−1) + b f(n−2) has solutions rⁿ for the roots of r² = ar + b; distinct roots give f(n) = A r₁ⁿ + B r₂ⁿ with A and B fixed by the first two values.", "P1", [
       N("dm-recurrence-iterate", IN, "f(0) = {{k0}}, f(1) = {{k1}} and f(n) = {{ka}}f(n−1) + {{kb}}f(n−2). Find f(5).",
         "ka*(ka*(ka*(ka*k1 + kb*k0) + kb*k1) + kb*(ka*k1 + kb*k0)) + kb*(ka*(ka*k1 + kb*k0) + kb*k1)", "pm_recur(ka, kb, k0, k1, 5)",
         "Work up one term at a time: each new value uses only the two before it", tex="f(5)",
         given={"k0": {"pick": [1, 2, 3]}, "k1": {"pick": [1, 3]}, "ka": {"pick": [1, 2]}, "kb": {"pick": [1, 2, 3]}}),
       N("dm-recurrence-closed", IN, "f(0) = 0, f(1) = 1 and f(n) = {{ks}}f(n−1) − {{kp}}f(n−2), whose characteristic roots are {{kr1}} and {{kr2}}. Find f({{kn}}).",
         "(kr1^kn - kr2^kn)/(kr1 - kr2)", "pm_recur(ks, -kp, 0, 1, kn)",
         "With roots r₁ and r₂ the solution is A r₁ⁿ + B r₂ⁿ; f(0) = 0 and f(1) = 1 force f(n) = (r₁ⁿ − r₂ⁿ)/(r₁ − r₂)", tex="f(n)",
         cases=[{"kr1": 3, "kr2": 2, "ks": 5, "kp": 6, "kn": 6}, {"kr1": 4, "kr2": 1, "ks": 5, "kp": 4, "kn": 5},
                {"kr1": 5, "kr2": 2, "ks": 7, "kp": 10, "kn": 4}, {"kr1": 3, "kr2": 1, "ks": 4, "kp": 3, "kn": 7}])])]),
 }),
 3: ("sets", "Sets, functions and relations", D("D3") + NS("N2", "N6"), ["COUNT"], {
   1: ("Sets and functions", [
     ("A", D("D3") + NS("N2"), "Count unions, power sets and Cartesian products of finite sets.",
      "|A ∪ B| = |A| + |B| − |A ∩ B|; a set with n elements has 2^n subsets; |A × B| = |A||B|.", "P1", [
       N("dm-union-size", ST, "|A| = {{ka}}, |B| = {{kb}} and |A ∪ B| = {{ku}}. Find |A ∩ B|.", "ka + kb - ku", "solve(Eq(ka + kb - Symbol('m'), ku), Symbol('m'))[0]",
         "Adding the two sizes counts the overlap twice, so the overlap is what the sum exceeds the union by", tex="|A\\cap B|",
         given={"ka": {"pick": [12, 15, 20]}, "kb": {"pick": [9, 11, 14]}, "ku": {"pick": [18, 21, 23]}}, require="ka + kb > ku and ku >= ka"),
       N("dm-subsets-with-element", ST, "How many subsets of a {{kn}}-element set contain one particular element?", "2^(kn - 1)", "summation(binomial(kn - 1, nn - 1), (nn, 1, kn))",
         "Fix that element in; each of the other n − 1 elements is in or out freely. Half of all 2^n subsets contain any given element", tex="subsets",
         given={"kn": {"pick": [4, 6, 8, 10]}})]),
     ("B", D("D3") + NS("N2"), "Count functions, injections and surjections between finite sets.",
      "From an n-set to a k-set there are k^n functions, k(k−1)…(k−n+1) injections, and the surjections are counted by inclusion-exclusion: Σ (−1)^j C(k, j)(k − j)^n.", "P1", [
       N("dm-injections", ST, "How many injective functions are there from a {{kn}}-element set to a {{kk}}-element set?", "factorial(kk)/factorial(kk - kn)", "pm_inj(kn, kk)",
         "Choose the images one at a time without reuse: k choices, then k − 1, and so on for n factors", tex="injections",
         given={"kn": {"pick": [2, 3]}, "kk": {"pick": [4, 5, 6]}}),
       N("dm-surjections", ST, "How many surjective functions are there from a {{kn}}-element set onto a {{kk}}-element set?", "kans", "pm_surj(kn, kk)",
         "Subtract the functions that miss at least one target by inclusion-exclusion: k^n − C(k,1)(k−1)^n + C(k,2)(k−2)^n − …", tex="surjections",
         cases=[{"kn": n, "kk": k, "kans": sum((-1) ** j * comb(k, j) * (k - j) ** n for j in range(k + 1))} for n, k in [(3, 2), (4, 2), (4, 3), (5, 3), (5, 2), (6, 3)]])]),
     ("C", D("D3") + NS("N2"), "Test a relation for reflexivity, symmetry and transitivity, and count equivalence relations.",
      "An equivalence relation is reflexive, symmetric and transitive and is the same thing as a partition into classes; a 3-set has 5 and a 4-set has 15.", "P2", [
       Q("dm-relation-properties", ST, "On the integers, the relation '{{rel}}' is:", pace="recall", cases=[
           {"rel": "a ≤ b", "kc": 1}, {"rel": "a − b is a multiple of 5", "kc": 0}, {"rel": "a ≠ b", "kc": 2},
           {"rel": "a and b have the same parity", "kc": 0}, {"rel": "a divides b (on positive integers)", "kc": 1},
           {"rel": "|a − b| ≤ 1", "kc": 3}, {"rel": "a < b", "kc": 4}],
         choice=["An equivalence relation", "Reflexive and transitive, not symmetric", "Symmetric only", "Reflexive and symmetric, not transitive", "Transitive only"],
         correct="kc", verify="authored", explain="Check each property on its own: does a relate to itself, does the relation reverse, and does it chain? Closeness within 1 does not chain: 0 ~ 1 and 1 ~ 2 but 0 is not within 1 of 2"),
       N("dm-count-equivalence", ST, "How many equivalence relations are there on a set with {{kn}} elements?", "kans", "pm_relations(kn, 3)",
         "Count partitions by the shape of their blocks. For 4 elements: 1 (all together) + 4 (3+1) + 3 (2+2) + 6 (2+1+1) + 1 (singletons) = 15", tex="relations",
         cases=[{"kn": 2, "kans": 2}, {"kn": 3, "kans": 5}, {"kn": 4, "kans": 15}])]),
     ("D", D("D3") + NS("N6"), "Decide whether a set is countable and say what Cantor's diagonal argument shows.",
      "A set is countable if it can be listed. The integers, the rationals and any countable union of countable sets are countable; the reals and the power set of the naturals are not, and no set maps onto its own power set.", "P2", [
       Q("dm-countable-or-not", ST, "Is this set countable or uncountable: {{st}}?", pace="recall", cases=[
           {"st": "the rational numbers", "kc": 0}, {"st": "the real numbers between 0 and 1", "kc": 1}, {"st": "all finite strings of letters", "kc": 0},
           {"st": "all infinite sequences of 0s and 1s", "kc": 1}, {"st": "pairs of integers", "kc": 0}, {"st": "all subsets of the natural numbers", "kc": 1},
           {"st": "the algebraic numbers", "kc": 0}, {"st": "the irrational numbers", "kc": 1}, {"st": "all finite subsets of the natural numbers", "kc": 0}],
         choice=["Countable", "Uncountable"], correct="kc", verify="authored",
         explain="Anything describable by a finite string over a finite alphabet is countable. Infinite binary sequences are not: any list of them misses the sequence that differs from the nth entry in its nth place"),
       F("dm-cantor-facts", ST, [
           ("Cantor's diagonal argument shows directly that:", "No list of infinite binary sequences contains them all", "The rationals are countable", "Every infinite set is countable", "The reals are well-ordered"),
           ("Since the algebraic numbers are countable and the reals are not:", "Transcendental numbers exist", "Every real is algebraic", "π is algebraic", "The algebraic numbers are finite"),
           ("For any set X, a function from X to its power set cannot be:", "Surjective", "Injective", "Defined", "Constant"),
           ("A countable union of countable sets is:", "Countable", "Uncountable", "Finite", "Empty")],
         "The diagonal sequence is built to disagree with every listed one, so the list was not complete. The same idea gives no surjection from a set onto its power set")])]),
 }),
 4: ("counting", "Counting", D("D4", "C1", "C2", "C4") + NS("N2", "N3"), ["COUNT"], {
   1: ("Arrangements and selections", [
     ("A", D("C1", "C2"), "Count arrangements with repeated letters and selections under a constraint.",
      "n objects with repeats of sizes a, b, … have n!/(a! b! …) arrangements. 'At least one' is counted through the complement.", "P1", [
       N("dm-word-arrangements", CT, "How many distinct arrangements are there of the letters of {{wd}}?", "kans", "pm_words(wd)",
         "Divide n! by the factorial of each repeat count: swapping equal letters changes nothing", tex="arrangements",
         cases=[{"wd": w, "kans": a} for w, a in [("LEVEL", 30), ("BANANA", 60), ("LETTER", 180), ("PEPPER", 60), ("STATS", 30), ("ASSESS", 30), ("COFFEE", 180)]]),
       N("dm-committee-at-least", CT, "A committee of {{kk}} is chosen from {{km}} chemists and {{kw}} engineers. How many committees include at least one engineer?",
         "combinations(km + kw, kk) - combinations(km, kk)", "summation(binomial(kw, nn)*binomial(km, kk - nn), (nn, 1, kk))",
         "Count all committees and subtract those with no engineer. Summing over the number of engineers gives the same total with more work", tex="committees",
         given={"kk": {"pick": [3, 4]}, "km": {"pick": [5, 6, 7]}, "kw": {"pick": [3, 4]}})]),
     ("B", D("C2"), "Count distributions of identical objects by stars and bars.",
      "x₁ + … + x_k = n has C(n + k − 1, k − 1) solutions in non-negative integers and C(n − 1, k − 1) in positive integers.", "P1", [
       N("dm-stars-bars", CT, "How many solutions in non-negative integers has x + y + z = {{kn}}?", "combinations(kn + 2, 2)", "pm_solutions(kn, 3, 0)",
         "Lay out n stars and 2 bars in a row: the bars cut the stars into three groups, and any arrangement of the n + 2 symbols is one solution", tex="solutions",
         given={"kn": {"pick": [5, 7, 8, 10]}}),
       N("dm-stars-bars-positive", CT, "How many ways can {{kn}} identical sweets be shared among 3 children if every child gets at least one?", "combinations(kn - 1, 2)", "pm_solutions(kn, 3, 1)",
         "Give each child one first and distribute the rest freely, or place 2 bars in the n − 1 gaps between the sweets", tex="ways",
         given={"kn": {"pick": [6, 7, 9, 10]}})]),
     ("C", D("D4", "C2") + NS("N3"), "Use the binomial theorem to read off a coefficient or a sum.",
      "(a + b)^n = Σ C(n, k) a^k b^(n−k). Setting a = b = 1 gives Σ C(n, k) = 2^n; a = −1 gives the alternating sum 0.", "P1", [
       N("dm-binomial-coefficient", CT, "What is the coefficient of x^{{kk}} in ({{ka}}x + {{kb}})^{{kn}}?", "combinations(kn, kk)*ka^kk*kb^(kn - kk)", "pm_binom_coeff(ka, kb, kn, kk)",
         "The x^k term is C(n, k)(ax)^k b^(n−k): choose which k of the n brackets supply the x", tex="coefficient",
         given={"ka": {"pick": [1, 2, 3]}, "kb": {"pick": [1, 2]}, "kn": {"pick": [4, 5, 6]}, "kk": {"pick": [2, 3]}}),
       N("dm-even-subsets", CT, "How many subsets of a {{kn}}-element set have an even number of elements?", "2^(kn - 1)", "summation(binomial(kn, 2*nn - 2), (nn, 1, floor(kn/2) + 1))",
         "Put x = 1 and x = −1 in (1 + x)^n and add: the even-sized subsets are exactly half of all 2^n", tex="subsets",
         given={"kn": {"pick": [5, 6, 8, 9]}})]),
     ("D", D("C4") + NS("N2"), "Count with inclusion-exclusion, including derangements.",
      "|A ∪ B ∪ C| = Σ|A| − Σ|A ∩ B| + |A ∩ B ∩ C|. Derangements: n! Σ (−1)^k / k!, close to n!/e.", "P1", [
       N("dm-divisible-by-any", CT, "How many integers from 1 to {{kt}} are divisible by 2, 3 or 5?",
         "floor(kt/2) + floor(kt/3) + floor(kt/5) - floor(kt/6) - floor(kt/10) - floor(kt/15) + floor(kt/30)", "pm_divisible_any(kt, '2,3,5')",
         "Add the three single counts, subtract the three pairwise overlaps (multiples of 6, 10, 15), add back the multiples of 30", tex="integers",
         given={"kt": {"pick": [60, 100, 150, 200]}}),
       N("dm-derangements", CT, "{{kn}} people each put a hat in a pile and take one back at random. In how many of the {{kf}} outcomes does nobody get their own hat?", "kans", "pm_derange(kn)",
         "D(n) = n!(1 − 1/1! + 1/2! − … ± 1/n!), or use D(n) = (n − 1)(D(n−1) + D(n−2)) from D(1) = 0, D(2) = 1", tex="outcomes",
         cases=[{"kn": n, "kf": factorial(n), "kans": d} for n, d in [(3, 2), (4, 9), (5, 44), (6, 265), (7, 1854)]])]),
     ("E", D("D4"), "Apply the pigeonhole principle to find a guaranteed minimum.",
      "If more than kn objects go into n boxes, some box holds more than k. To force k + 1 in one box you need kn + 1 objects.", "P1", [
       N("dm-pigeonhole-force", CT, "A drawer holds socks in {{kc}} colours, many of each. How many must you take without looking to be sure of {{km}} of the same colour?", "kc*(km - 1) + 1", "solve(Eq((Symbol('m') - 1)/kc, km - 1), Symbol('m'))[0]",
         "The worst case is m − 1 of every colour; one more sock must push some colour to m", tex="socks",
         given={"kc": {"pick": [3, 4, 5]}, "km": {"pick": [2, 3, 4]}}),
       F("dm-pigeonhole-facts", CT, [
           ("Among any 13 people, at least two share:", "A birth month", "A birthday", "A birth year", "A first initial"),
           ("Among any n + 1 integers, two must have the same:", "Remainder on division by n", "Parity only if n is odd", "Sign", "Last digit"),
           ("Pick any 5 points in a unit square. Two of them are within what distance of each other?", "√2/2", "1/4", "1/2", "1"),
           ("In any group of 6 people there are 3 mutual friends or 3 mutual strangers. This says R(3, 3) is at most:", "6", "5", "3", "9")],
         "Name the pigeons and the holes. For five points, cut the square into four half-size squares: two points share one, whose diagonal is √2/2")])]),
 }),
 5: ("gf", "Generating functions", D("C3", "C5"), ["COUNT"], {
   1: ("Coefficients that count", [
     ("A", D("C3"), "Extract a coefficient from a product of geometric series.",
      "1/(1 − x)^k = Σ C(n + k − 1, k − 1) x^n: the coefficient of x^n counts selections of n objects from k types with repetition.", "P1", [
       N("dm-gf-coefficient", GF, "What is the coefficient of x^{{kn}} in 1/(1 − x)^{{kk}}?", "combinations(kn + kk - 1, kk - 1)", "pm_gf_coeff(py, kn)",
         "Each factor 1/(1 − x) = 1 + x + x² + … lets one type be chosen any number of times, so the coefficient is the stars-and-bars count", tex="coefficient",
         cases=[{"kn": n, "kk": k, "py": f"1/(1-t)**{k}"} for n, k in [(4, 3), (5, 3), (6, 2), (5, 4), (7, 3)]]),
       N("dm-gf-bounded", GF, "What is the coefficient of x^{{kn}} in (1 + x + x²)^{{kk}}?", "kans", "pm_gf_coeff(py, kn)",
         "Each bracket contributes 0, 1 or 2: the coefficient counts the ways k such numbers add to n", tex="coefficient",
         cases=[{"kn": 2, "kk": 2, "kans": 3, "py": "(1+t+t**2)**2"}, {"kn": 3, "kk": 3, "kans": 7, "py": "(1+t+t**2)**3"},
                {"kn": 2, "kk": 3, "kans": 6, "py": "(1+t+t**2)**3"}, {"kn": 4, "kk": 3, "kans": 6, "py": "(1+t+t**2)**3"},
                {"kn": 4, "kk": 4, "kans": 19, "py": "(1+t+t**2)**4"}])]),
     ("B", D("C3", "C5"), "Model a selection problem with a generating function and read off the count.",
      "A coin of value c contributes the factor 1/(1 − x^c); the number of ways to make n is the coefficient of x^n in the product.", "P1", [
       N("dm-gf-change", GF, "In how many ways can {{kn}} cents be made from 1-, 2- and 5-cent coins (order does not matter)?", "kans", "pm_gf_coeff('1/((1-t)*(1-t**2)*(1-t**5))', kn)",
         "The answer is the coefficient of x^n in 1/((1 − x)(1 − x²)(1 − x⁵)). By hand: fix the number of 5s, then count the 2s that fit", tex="ways",
         cases=[{"kn": n, "kans": change(n)} for n in (6, 8, 10, 12, 15)]),
       F("dm-gf-model", GF, [
           ("Which generating function counts ways to pick fruit with at most 2 apples and any number of pears?", "(1 + x + x²)/(1 − x)", "(1 + x)²/(1 − x)", "1/((1 − x)(1 − x²))", "(1 + x²)(1 + x)"),
           ("Which factor represents an item that must be used an even number of times?", "1/(1 − x²)", "1/(1 − x)", "1 + x²", "x/(1 − x²)"),
           ("Which factor represents an item that must be used at least once?", "x/(1 − x)", "1/(1 − x)", "1 + x", "1/(1 − x) + 1"),
           ("The generating function of the Fibonacci numbers (F₀ = 0, F₁ = 1) is:", "x/(1 − x − x²)", "1/(1 − x − x²)", "x/(1 − x)²", "1/(1 − 2x)")],
         "Write one factor per kind of object, listing the powers it may contribute, and multiply")])]),
 }),
 6: ("graphs", "Graphs and trees", D("D5", "GT1", "GT2", "GT3", "GT4") + GT("H1", "H5"), ["COUNT", "PROOF"], {
   1: ("Degrees, trees and circuits", [
     ("A", D("D5", "GT1") + GT("H1"), "Use the handshake lemma on a degree sequence.",
      "The degrees sum to twice the number of edges, so the number of odd-degree vertices is even.", "P1", [
       N("dm-handshake-edges", GR, "A graph has {{ka}} vertices of degree 3 and {{kb}} vertices of degree 4. How many edges does it have?", "(3*ka + 4*kb)/2", "solve(Eq(2*Symbol('m'), 3*ka + 4*kb), Symbol('m'))[0]",
         "Every edge is counted at both ends, so the degree sum is twice the edge count", tex="edges",
         given={"ka": {"pick": [2, 4, 6]}, "kb": {"pick": [1, 3, 5]}}),
       Q("dm-degree-sequence-possible", GR, "Can a simple graph have the degree sequence {{sq}}?", pace="recall", cases=[
           {"sq": "3, 3, 3, 3", "kc": 0}, {"sq": "3, 3, 3, 2", "kc": 1}, {"sq": "4, 1, 1, 1, 1", "kc": 0}, {"sq": "5, 2, 2, 2, 1", "kc": 1},
           {"sq": "2, 2, 2, 2, 2", "kc": 0}, {"sq": "3, 2, 1", "kc": 1}, {"sq": "3, 3, 1, 1", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="First check the sum is even, then that no degree exceeds n − 1, then that the largest degrees can be met: in 3, 3, 1, 1 the two degree-3 vertices must each join both degree-1 vertices and each other, giving those leaves degree 2")]),
     ("B", D("GT2") + GT("H1"), "Count the edges of a tree or forest and the spanning trees of a small graph.",
      "A tree on n vertices has n − 1 edges; a forest with c components has n − c. A cycle C_n has n spanning trees and the complete graph K_n has n^(n−2).", "P1", [
       N("dm-forest-edges", GR, "A forest has {{kn}} vertices and {{kc}} connected components. How many edges does it have?", "kn - kc", "solve(Eq(kn - Symbol('m'), kc), Symbol('m'))[0]",
         "Each component is a tree with one fewer edge than vertices, so the total is n minus the number of components", tex="edges",
         given={"kn": {"pick": [12, 15, 20, 30]}, "kc": {"pick": [2, 3, 5]}}),
       N("dm-spanning-trees", GR, "How many spanning trees has the graph with edges {{ge}}?", "kans", "pm_g_spanning(ge)",
         "Count the ways to delete edges until no cycle is left while staying connected. For a single cycle of length n, delete any one edge: n trees. Cayley's formula gives n^(n−2) for a complete graph", tex="trees",
         cases=[{"ge": "a-b,b-c,c-d,d-a", "kans": 4}, {"ge": "a-b,b-c,c-a,c-d", "kans": 3}, {"ge": "a-b,b-c,c-d,d-a,a-c", "kans": 8},
                {"ge": "a-b,a-c,a-d,b-c,b-d,c-d", "kans": 16}, {"ge": "a-b,b-c,c-d,d-e,e-a", "kans": 5}, {"ge": "a-b,b-c,c-a,c-d,d-e,e-c", "kans": 9}])]),
     ("C", D("GT4") + GT("H1"), "Decide whether a graph has an Euler circuit or trail from its degrees.",
      "A connected graph has an Euler circuit exactly when every degree is even, and an Euler trail exactly when two vertices have odd degree.", "P2", [
       N("dm-odd-vertices", GR, "How many vertices of odd degree has the graph with edges {{ge}}?", "kans", "pm_g_odd(ge)",
         "Tally the degree of each vertex. The count of odd ones is always even, and it decides between a circuit (0), a trail (2) and neither", tex="vertices",
         cases=[{"ge": "a-b,b-c,c-d,d-a,a-c", "kans": 2}, {"ge": "a-b,a-c,a-d,b-c,b-d,c-d", "kans": 4}, {"ge": "a-b,b-c,c-a,c-d", "kans": 2},
                {"ge": "a-b,b-c,c-d", "kans": 2}, {"ge": "a-b,a-c,a-d,a-e", "kans": 4}]),
       Q("dm-euler-classify", GR, "A connected graph has {{kv}} vertices of odd degree. It has:", pace="recall",
         cases=[{"kv": 0, "kc": 0}, {"kv": 2, "kc": 1}, {"kv": 4, "kc": 2}, {"kv": 6, "kc": 2}],
         choice=["An Euler circuit", "An Euler trail but no Euler circuit", "Neither"], correct="kc", verify="authored",
         explain="A closed walk using every edge once enters and leaves each vertex equally often, so all degrees are even. Two odd vertices can serve as the ends of an open trail; more than two cannot")]),
     ("D", D("GT3") + GT("H5"), "Find a chromatic number and count proper colourings.",
      "χ(G) is the fewest colours with adjacent vertices different. A tree on n vertices has k(k − 1)^(n−1) colourings; the cycle C_n has (k − 1)^n + (−1)^n (k − 1); an odd cycle needs 3 colours.", "P1", [
       N("dm-chromatic-number", GR, "What is the chromatic number of the graph with edges {{ge}}?", "kans", "pm_g_chromatic(ge)",
         "A triangle forces 3 and a K₄ forces 4; an odd cycle needs 3 even without a triangle; a graph with no odd cycle is bipartite and needs 2", tex="\\chi",
         cases=[{"ge": "a-b,b-c,c-d,d-a", "kans": 2}, {"ge": "a-b,b-c,c-d,d-e,e-a", "kans": 3}, {"ge": "a-b,a-c,a-d,b-c,b-d,c-d", "kans": 4},
                {"ge": "a-b,b-c,c-a,c-d", "kans": 3}, {"ge": "a-b,b-c,c-d,d-e", "kans": 2}, {"ge": "a-b,b-c,c-d,d-e,e-a,a-f,b-f,c-f,d-f,e-f", "kans": 4}]),
       N("dm-count-colourings", GR, "In how many ways can the vertices of a {{nm}} be properly coloured with {{kk}} colours?", "kans", "pm_g_colourings(ge, kk)",
         "Colour the vertices in order and count the choices left at each one. For a cycle the last vertex sees two neighbours, which gives (k − 1)^n + (−1)^n (k − 1)", tex="colourings",
         cases=[{"nm": "path on 4 vertices", "ge": "a-b,b-c,c-d", "kk": 3, "kans": 24}, {"nm": "triangle", "ge": "a-b,b-c,c-a", "kk": 4, "kans": 24},
                {"nm": "4-cycle", "ge": "a-b,b-c,c-d,d-a", "kk": 3, "kans": 18}, {"nm": "5-cycle", "ge": "a-b,b-c,c-d,d-e,e-a", "kk": 3, "kans": 30},
                {"nm": "star with 3 leaves", "ge": "a-b,a-c,a-d", "kk": 3, "kans": 24}, {"nm": "4-cycle", "ge": "a-b,b-c,c-d,d-a", "kk": 4, "kans": 84}])]),
     ("E", D("GT1") + GT("H1"), "Apply Euler's formula and the edge bound for planar graphs.",
      "A connected plane graph has V − E + F = 2. A simple planar graph with V ≥ 3 has E ≤ 3V − 6, and E ≤ 2V − 4 if it has no triangles; so K₅ and K₃,₃ are not planar.", "P1", [
       N("dm-euler-faces", GR, "A connected plane graph has {{kv}} vertices and {{ke}} edges. How many faces does it have, counting the outer one?", "2 - kv + ke", "solve(Eq(kv - ke + Symbol('m'), 2), Symbol('m'))[0]",
         "V − E + F = 2 for every connected plane drawing, whatever the drawing looks like", tex="F",
         given={"kv": {"pick": [6, 8, 10]}, "ke": {"pick": [9, 12, 15]}}, require="ke <= 3*kv - 6"),
       F("dm-planarity-facts", GR, [
           ("K₅ has 5 vertices and 10 edges. It is not planar because a simple planar graph on 5 vertices has at most how many edges?", "9", "10", "8", "12"),
           ("K₃,₃ has 6 vertices, 9 edges and no triangles. It is not planar because the triangle-free bound 2V − 4 equals:", "8", "12", "9", "6"),
           ("Kuratowski's theorem says a graph is planar exactly when it contains no subdivision of:", "K₅ or K₃,₃", "K₄", "Any odd cycle", "K₃,₃ only"),
           ("Every planar graph can be properly coloured with how many colours (the four colour theorem)?", "4", "5", "3", "6")],
         "The bound E ≤ 3V − 6 comes from Euler's formula with every face having at least 3 sides. It can show a graph is not planar but never that one is")]),
     ("F", D("GT4") + GT("H2", "H3", "H6"), "Recognise Hamilton cycles, matchings and the first Ramsey number.",
      "A Hamilton cycle visits every vertex once; Dirac: minimum degree at least n/2 guarantees one. Hall: a bipartite graph has a matching covering X exactly when every set S in X has at least |S| neighbours. R(3, 3) = 6.", "P2", [
       Q("dm-hamilton-or-not", GR, "Does the {{nm}} have a Hamilton cycle?", pace="recall", cases=[
           {"nm": "complete graph K₅", "kc": 0}, {"nm": "star with 4 leaves", "kc": 1}, {"nm": "cube graph", "kc": 0}, {"nm": "path on 5 vertices", "kc": 1},
           {"nm": "complete bipartite graph K₂,₃", "kc": 1}, {"nm": "complete bipartite graph K₃,₃", "kc": 0}, {"nm": "Petersen graph", "kc": 1}],
         choice=["Yes", "No"], correct="kc", verify="authored",
         explain="A bipartite graph can only have a Hamilton cycle if its two sides are equal, since the cycle alternates. A vertex of degree 1 rules one out. The Petersen graph is the standard 3-regular graph without one"),
       F("dm-hall-ramsey-facts", GR, [
           ("Three applicants are all qualified only for the same two jobs. Hall's condition fails because:", "A set of 3 applicants has only 2 neighbours", "The graph is not bipartite", "There are more jobs than applicants", "Some applicant has degree 2"),
           ("Dirac's theorem guarantees a Hamilton cycle in a graph on n ≥ 3 vertices when every degree is at least:", "n/2", "2", "n − 1", "log n"),
           ("The smallest n such that every red-blue colouring of the edges of K_n has a one-colour triangle is:", "6", "5", "4", "9"),
           ("A 5-cycle with its 5 diagonals coloured the other colour shows that R(3, 3) is greater than:", "5", "6", "3", "4")],
         "Hall's condition is obviously necessary; the theorem is that it is also enough")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
