"""Proof-side mathematics (Nov 2026): six frameworks written from scripts/second_specs/pm_*.py — Discrete Mathematics
(DM), Number Theory (NT), Abstract Algebra (AA), Real Analysis (RA), Topology (TP) and Stochastic Processes (STO).
Registers the standards they rest on, their skills, domains, library subject and one source, and writes each framework
file with empty drill lists. Idempotent; nothing is overwritten once it exists. Then run second_types.py.
Usage: python3 scripts/pm_setup.py"""
import importlib.util, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
q = lambda s: json.dumps(s, ensure_ascii=False)
fl = lambda xs: "[" + ", ".join(q(x) for x in xs) + "]"


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts/second_specs", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


MODS = [load(n) for n in ("pm_dm", "pm_nt", "pm_aa", "pm_ra", "pm_tp", "pm_sto", "pm_ge")]

CAM = "https://www.maths.cam.ac.uk/undergrad/course/schedules.pdf"
CAMNOTE = ("Read Nov 2026 from the Faculty's Schedules of Lecture Courses for the Mathematical Tripos 2026-27 (revised 19 August 2026), "
           "through an extraction that listed every topic the schedule names for this course, so read: part. The lectures and example sheets were not read. "
           "A proof-based course, so its theorems are drilled here as what they let you compute or decide. Items are the schedule's blocks, titled in our words. ")


def cam(sid, name, items, extra=""):
    return {"id": sid, "name": f"Cambridge Mathematical Tripos, {name} schedule", "publisher": "University of Cambridge, Faculty of Mathematics",
            "kind": "course", "read": "part", "url": CAM, "note": CAMNOTE + extra, "items": [{"code": c, "title": t} for c, t in items]}


STDS = [
 cam("cambridge-ia-groups", "Part IA Groups", [
     ("G1", "Examples of groups: axioms, symmetry groups, permutations, subgroups, homomorphisms, the Möbius group"),
     ("G2", "Lagrange's theorem: cosets, groups of small order, quaternions, Fermat-Euler"),
     ("G3", "Group actions: orbits and stabilisers, Cayley's theorem, conjugacy classes, Cauchy's theorem"),
     ("G4", "Quotient groups: normal subgroups and the isomorphism theorem"),
     ("G5", "Matrix groups: general, special, orthogonal groups and rotations"),
     ("G6", "Permutations: cycles, sign, conjugacy in the symmetric and alternating groups, simple groups")],
     "The Möbius-group topics are drilled in Engineering Math unit 15, not here."),
 cam("cambridge-ib-grm", "Part IB Groups, Rings and Modules", [
     ("GR", "Groups: isomorphism theorems, actions, centre, p-groups, Sylow theorems, groups of small order"),
     ("RI", "Rings: ideals, quotients, prime and maximal ideals, fields, unique factorisation, Gaussian integers, polynomial rings"),
     ("MO", "Modules: finitely generated modules over a Euclidean domain, abelian groups, Jordan normal form")],
     "Modules are only drilled through the classification of finite abelian groups."),
 cam("cambridge-ia-numbers-sets", "Part IA Numbers and Sets", [
     ("N1", "Number systems and logic: proof, counter-example, negation, contradiction"),
     ("N2", "Sets, relations and functions: injections, surjections, equivalence relations, counting, inclusion-exclusion"),
     ("N3", "The integers: induction, well-ordering, the binomial theorem"),
     ("N4", "Elementary number theory: primes, Euclid's algorithm, congruences, Chinese remainder, Wilson, Fermat-Euler, RSA"),
     ("N5", "The real numbers: least upper bounds, monotone sequences, irrationality, decimal expansions"),
     ("N6", "Countability and uncountability: countable unions, the reals, power sets")]),
 cam("cambridge-ii-number-theory", "Part II Number Theory", [
     ("T1", "Review: Euclid's algorithm, the fundamental theorem of arithmetic, congruences, Fermat and Euler"),
     ("T2", "Chinese remainder theorem, Lagrange's theorem, primitive roots"),
     ("T3", "Quadratic residues, the Legendre symbol, Euler's criterion, quadratic reciprocity"),
     ("T4", "The Jacobi symbol"), ("T5", "Binary quadratic forms and the primes they represent"),
     ("T6", "Distribution of primes: the zeta function, the prime number theorem (statement), Chebyshev"),
     ("T7", "Continued fractions and Pell's equation"), ("T8", "Primality testing and pseudoprimes"),
     ("T9", "Factorisation methods")],
     "T4, T5 and T9 are not drilled in draft 1."),
 cam("cambridge-ia-analysis-i", "Part IA Analysis I", [
     ("A1", "Limits and convergence: sequences and series, Bolzano-Weierstrass, Cauchy's principle, convergence tests"),
     ("A2", "Continuity: the intermediate value theorem, bounds attained on a closed interval"),
     ("A3", "Differentiability: Rolle, the mean value theorem, Taylor's theorem with remainder"),
     ("A4", "Power series: radius of convergence, the exponential and trigonometric functions"),
     ("A5", "Integration: the Riemann integral, integrable functions, the fundamental theorem, improper integrals")]),
 cam("cambridge-ib-topological-spaces", "Part IB Topological Spaces", [
     ("S1", "Topological spaces: open and closed sets, continuity, Hausdorff spaces, subspace, quotient and product topologies"),
     ("S2", "Connectedness and path-connectedness"), ("S3", "Compactness"),
     ("S4", "Topology of manifolds: spheres, tori, the projective plane, polygons with sides identified"),
     ("S5", "Triangulable surfaces: Euler characteristic, orientability, the classification (statement)")]),
 cam("cambridge-ib-markov-chains", "Part IB Markov Chains", [
     ("M1", "Discrete-time chains: transition matrices, classes, hitting probabilities and mean hitting times"),
     ("M2", "Recurrence and transience; simple random walks in one, two and three dimensions"),
     ("M3", "Invariant distributions, mean return times, convergence to equilibrium"),
     ("M4", "Time reversal, detailed balance, random walk on a graph")]),
 cam("cambridge-ii-applied-probability", "Part II Applied Probability", [
     ("P1", "Continuous-time chains on a finite state space, the Poisson process, birth and death processes"),
     ("P2", "General continuous-time chains: jump chains, recurrence, equilibrium, reversibility"),
     ("P3", "Queues: M/M/1, M/M/infinity, networks, M/G/1"), ("P4", "Renewal theory and Little's formula"),
     ("P5", "Spatial Poisson processes")],
     "P2, P4 and P5 are not drilled in draft 1."),
 cam("cambridge-ii-graph-theory", "Part II Graph Theory", [
     ("H1", "Basics: trees, bipartite graphs, Euler circuits, planar graphs"), ("H2", "Matchings and connectivity: Hall, Menger"),
     ("H3", "Extremal graph theory: Hamilton cycles, Turán"), ("H4", "Eigenvalue methods"),
     ("H5", "Colourings: chromatic polynomial, Brooks, Vizing, the four- and five-colour theorems"),
     ("H6", "Ramsey theory"), ("H7", "Probabilistic methods")],
     "Only H1 and H5 are drilled, with one Ramsey and one Hall item."),
 {"id": "cupm-2015-discrete", "name": "MAA CUPM Curriculum Guide 2015, Discrete Mathematics and Combinatorics course area report",
  "publisher": "Mathematical Association of America", "kind": "standard", "read": "part",
  "url": "https://www2.kenyon.edu/Depts/Math/schumacherc/public_html/Professional/CUPM/2015Guide/Course%20Groups/DiscreteMath.pdf",
  "note": "Read Nov 2026 through an extraction of the report's cognitive goals and its three sample syllabi (discrete mathematics, enumerative combinatorics, graph theory); the surrounding discussion was not read, so read: part. Items are the syllabus headings, titled in our words. The application topics (D6) belong to Computer Science and are cited there, not rebuilt.",
  "items": [{"code": c, "title": t} for c, t in [
     ("D1", "Basic logic and proof, with elementary number theory"), ("D2", "Sequences, induction and recursion"),
     ("D3", "Sets, functions and relations"), ("D4", "Combinatorics and discrete probability"), ("D5", "Graphs and trees"),
     ("D6", "Applications: circuits, algorithms, cryptography, automata"),
     ("C1", "Elementary counting principles"), ("C2", "Permutations, combinations and distributions"),
     ("C3", "Generating functions"), ("C4", "Inclusion-exclusion"), ("C5", "Recurrence relations"),
     ("GT1", "Graphs: paths, connectedness, isomorphism, planarity"), ("GT2", "Trees and spanning trees"),
     ("GT3", "Graph colouring"), ("GT4", "Eulerian and Hamiltonian circuits")]]},
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
for m in MODS:
    d = m.FW["domain"]
    if not any(f"id: {d}," in ln for ln in L):
        i = next(k for k, ln in enumerate(L) if "id: gc," in ln and "domain:" not in ln)
        L.insert(i + 1, f'  - {{ id: {d}, title: {q(m.FW["title"])} }}')
    if not any(f"domain: {d}," in ln for ln in L):
        i = max(k for k, ln in enumerate(L) if "domain: gc," in ln)
        L[i + 1:i + 1] = [f'  - {{ id: {d}.{a}, domain: {d}, title: {q(b)}, short: {q(c)}'
                          + (f', prereqs: [{", ".join(pr)}]' if pr else "") + " }" for a, b, c, pr in m.SKILLS]
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/library.yaml")
L = open(p).read().split("\n")
SUB = "Higher Mathematics"
if not any(ln.strip() == f'- "{SUB}"' for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.strip() == '- "Graduate ChemE Methods"')
    L.insert(i + 1, f'  - "{SUB}"')
for m in MODS:
    d = m.FW["domain"]
    if not any(ln.startswith(f"  {d}:") for ln in L):
        i = next(k for k, ln in enumerate(L) if ln.startswith("  gc:"))
        L.insert(i + 1, f'  {d}: "{SUB}"')
if not any(ln.startswith("  cambridge-tripos-schedules:") for ln in L):
    i = next(k for k, ln in enumerate(L) if ln.startswith("  cheme-grad-methods:"))
    L.insert(i + 1, f'  cambridge-tripos-schedules: "{SUB}"')
open(p, "w").write("\n".join(L))

p = os.path.join(ROOT, "drills/sources/cambridge-tripos-schedules.yaml")
if not os.path.exists(p):
    out = ["# The Cambridge Mathematical Tripos schedules (2026-27) for the proof-side courses, written as a source so the",
           "# dm/nt/aa/ra/top/stoch skills have a home. NOT a book: only the schedules were read, and the discrete-mathematics",
           "# chapters follow the MAA CUPM 2015 report's syllabus headings instead. Chapter numbers are ours.",
           "id: cambridge-tripos-schedules", 'title: "Cambridge Mathematical Tripos schedules (proof-side courses)"',
           'short: "Tripos schedules"', "year: 2026", "field: mathematics", "chapters:"]
    n = 0
    for m in MODS:
        for a, b, c, pr in m.SKILLS:
            n += 1
            out.append(f'  - {{ n: {n}, title: {q(m.FW["title"] + ": " + c)}, skills: [{m.FW["domain"]}.{a}] }}')
    open(p, "w").write("\n".join(out) + "\n")

for m in MODS:
    F = m.FW
    p = os.path.join(ROOT, f"drills/frameworks/{F['id']}.yaml")
    if os.path.exists(p): continue
    out = [f"# {F['title']} — curriculum framework (draft 1, for Kevin's markup)", "#"] + ["# " + ln for ln in F["header"]] + [
           f"id: {F['id']}", f"title: {F['title']}", f"code: {F['code']}", "draft: 1", "track: math",
           f"requires: [{', '.join(F['requires'])}]", f"level: {F['level']}", f"domains: [{F['domain']}]", "", "basis:",
           f"  primary: {F['primary']}"] + ([f"  also: [{', '.join(F['also'])}]"] if F["also"] else []) + [
           "  note: " + q(F["note"]), "", "big_ideas:"]
    for i, ti, tx in m.IDEAS:
        out += [f"  - id: {i}", f"    title: {q(ti)}", f"    text: {q(tx)}"]
    out += ["", "practices:", "  - id: P1", "    title: Compute",
            "    text: " + q("Carry the definition or theorem to a number, a count or an example."),
            "  - id: P2", "    title: Decide",
            "    text: " + q("Say whether a statement holds, which hypothesis fails, or which example breaks it."), "", "units:"]
    for n, (uid, ti, std, ideas, topics) in m.UNITS.items():
        out += [f"  - id: {uid}", f"    n: {n}", f"    title: {q(ti)}", f"    std: {fl(std)}", "    scope: core",
                f"    ideas: [{', '.join(ideas)}]", "    topics:"]
        for tn, (tt, los) in topics.items():
            out += [f"      - n: {tn}", f"        title: {q(tt)}", "        los:"]
            for lid, lstd, do, ek, pr, _qs in los:
                out.append(f"          - {{ id: {lid}, std: {fl(lstd)}, do: {q(do)}, ek: [{q(ek)}], p: [{pr}], drills: [] }}")
    open(p, "w").write("\n".join(out) + "\n")
print("ok")
