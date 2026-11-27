"""Second layer of the proof-side mathematics frameworks (Nov 2026): registers the Cambridge schedules for Analysis II,
Galois Theory, Algebraic Topology, Stochastic Financial Models and Geometry, adds one skill to each of four frameworks,
gives every pm skill a chapter in the source, and adds the new standards to the frameworks' bases. Idempotent.
Run after pm_setup.py (which writes the Geometry framework from pm_ge.py) and before insert_objs.py pm2_*.
Usage: python3 scripts/pm2_setup.py"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = lambda s: json.dumps(s, ensure_ascii=False)
CAM = "https://www.maths.cam.ac.uk/undergrad/course/schedules.pdf"
NOTE = ("Read Nov 2026 from the Faculty's Schedules of Lecture Courses for the Mathematical Tripos 2026-27, through an extraction that listed "
        "every topic the schedule names for this course, so read: part. Lectures and example sheets were not read. Items are our grouping of the schedule's topics, titled in our words. ")


def cam(sid, name, items, extra=""):
    return {"id": sid, "name": f"Cambridge Mathematical Tripos, {name} schedule", "publisher": "University of Cambridge, Faculty of Mathematics",
            "kind": "course", "read": "part", "url": CAM, "note": NOTE + extra, "items": [{"code": c, "title": t} for c, t in items]}


STDS = [
 cam("cambridge-ib-analysis-ii", "Part IB Analysis II", [
     ("U", "Uniform convergence: uniform limits, the M-test, power series, exchange of limits with integrals and derivatives"),
     ("M", "Metric and normed spaces: open and closed sets, sequential compactness, equivalence of norms"),
     ("D", "Differentiation in several variables: the derivative as a linear map, the Hessian, critical points, the mean-value inequality"),
     ("C", "Completeness and the contraction mapping theorem; inverse and implicit function theorems, Picard's theorem")],
     "The inverse and implicit function theorems are not drilled."),
 cam("cambridge-ii-galois-theory", "Part II Galois Theory", [
     ("E", "Field extensions: the tower law, algebraic extensions, splitting fields, separability"),
     ("F", "Finite fields and their Galois theory"), ("G", "Galois extensions, automorphism groups and the fundamental theorem; cyclotomic extensions"),
     ("S", "Solubility by radicals, cubics and quartics, the quintic and the classical construction problems")],
     "Kummer theory, trace and norm, and invariant theory are not drilled."),
 cam("cambridge-ii-algebraic-topology", "Part II Algebraic Topology", [
     ("H", "Homotopy, homotopy equivalence and the fundamental group"), ("V", "Covering spaces and their correspondence with subgroups"),
     ("K", "Free groups, presentations and the Seifert-Van Kampen theorem"),
     ("L", "Simplicial homology, homology of spheres, Brouwer, Mayer-Vietoris, Euler characteristic")],
     "Simplicial approximation, Mayer-Vietoris computations and the Lefschetz theorem are not drilled."),
 cam("cambridge-ii-stochastic-financial-models", "Part II Stochastic Financial Models", [
     ("MG", "Conditional expectation, martingales, stopping times and optional stopping"),
     ("BM", "Arbitrage, hedging and the binomial model; martingale measures"),
     ("BR", "Brownian motion: random-walk limit, reflection principle, change of drift, the heat equation"),
     ("BS", "The Black-Scholes formula and its sensitivities; barrier options")],
     "BS is not drilled: this is a mathematics framework, and the pricing items stop at the one-period model."),
 cam("cambridge-ib-geometry", "Part IB Geometry", [
     ("SPH", "Spherical geometry: lines, triangles and area, isometries, finite groups of isometries"),
     ("RIE", "Riemannian metrics on the plane and sphere: lengths, areas, geodesics"),
     ("HYP", "Hyperbolic geometry: the half-plane and disc models, isometries, triangles and area, parallels"),
     ("CUR", "Curvature of the sphere, the plane and the hyperbolic plane")]),
]
p = os.path.join(ROOT, "drills/standards.yaml")
t = open(p).read()
for s in STDS:
    if f'"id": "{s["id"]}"' not in t:
        t = t.rstrip("\n") + "\n- " + json.dumps(s, ensure_ascii=False) + "\n"
open(p, "w").write(t)

NEW = [("ra", "metric", "Uniform convergence, metric spaces, completeness and contractions", "Uniform convergence and metric spaces", ["ra.calculus"], "Real Analysis"),
       ("aa", "fields", "Field extensions, finite fields, the Galois correspondence and constructibility", "Fields and Galois theory", ["aa.rings"], "Abstract Algebra"),
       ("top", "homotopy", "Homotopy, the fundamental group, covering spaces and Betti numbers", "Fundamental group and homology", ["top.surfaces"], "Topology"),
       ("stoch", "martingales", "Martingales, optional stopping, binomial pricing and Brownian motion", "Martingales and Brownian motion", ["stoch.walks"], "Stochastic Processes")]
p = os.path.join(ROOT, "drills/skills.yaml")
L = open(p).read().split("\n")
for d, a, b, c, pr, _ in NEW:
    if not any(f"id: {d}.{a}," in ln for ln in L):
        i = max(k for k, ln in enumerate(L) if f"domain: {d}," in ln)
        L.insert(i + 1, f'  - {{ id: {d}.{a}, domain: {d}, title: {q(b)}, short: {q(c)}, prereqs: [{", ".join(pr)}] }}')
open(p, "w").write("\n".join(L))

# every dm/nt/aa/ra/top/stoch/ngeo skill needs a chapter in the source
sk = [(m.group(1), m.group(2)) for ln in open(p).read().split("\n")
      for m in [re.search(r"id: ((?:dm|nt|aa|ra|top|stoch|ngeo)\.[a-z-]+), domain: \w+, title: \"[^\"]*\", short: \"([^\"]*)\"", ln)] if m]
p = os.path.join(ROOT, "drills/sources/cambridge-tripos-schedules.yaml")
t = open(p).read().rstrip("\n")
n = max(int(x) for x in re.findall(r"n: (\d+)", t))
for sid, short in sk:
    if f"[{sid}]" not in t:
        n += 1
        t += f'\n  - {{ n: {n}, title: {q(short)}, skills: [{sid}] }}'
open(p, "w").write(t + "\n")

ALSO = {"real-analysis": "cambridge-ib-analysis-ii", "abstract-algebra": "cambridge-ii-galois-theory", "topology": "cambridge-ii-algebraic-topology",
        "stochastic-processes": "cambridge-ii-stochastic-financial-models"}
for fw, sid in ALSO.items():
    p = os.path.join(ROOT, f"drills/frameworks/{fw}.yaml")
    L = open(p).read().split("\n")
    if any(sid in ln for ln in L[:40] if ln.startswith("  also:")): continue
    i = next((k for k, ln in enumerate(L) if ln.startswith("  also:")), None)
    if i is None:
        j = next(k for k, ln in enumerate(L) if ln.startswith("  primary:"))
        L.insert(j + 1, f"  also: [{sid}]")
    else:
        L[i] = L[i].rstrip().rstrip("]") + f", {sid}]"
    open(p, "w").write("\n".join(L))
print("ok")
