"""Geometry, the intermediate steps (Nov 2026): 8 objectives between the ones draft 1 jumped across — the sphere in
latitude and longitude before lunes and excess, lengths and geodesics in the half-plane by formula before the
defect theorem, and curvature as something measured from a triangle or a circle before Gauss-Bonnet.
NEEDS rewires the framework. Basis unchanged: the Cambridge Part IB Geometry schedule."""
from math import acos, cos, degrees, radians, sin
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ge-steps", "geometry", "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SP, HY, CU = "ngeo.spherical", "ngeo.hyperbolic", "ngeo.curvature"
G = lambda *s: [f"cambridge-ib-geometry:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


def central(a1, o1, a2, o2):
    """spherical law of cosines (the verifier uses the dot product of the two position vectors instead)"""
    a1, o1, a2, o2 = map(radians, (a1, o1, a2, o2))
    return degrees(acos(sin(a1) * sin(a2) + cos(a1) * cos(a2) * cos(o1 - o2)))


TOPICS = {"1.2": "The sphere in coordinates", "2.2": "The half-plane by formula", "3.2": "Curvature you can measure"}
OBJS = [
 ("GE-1.2.A", G("SPH"), "Find the central angle between two points given by latitude and longitude.", "Write each point as a unit vector (cos φ cos λ, cos φ sin λ, sin φ); the central angle is the angle between the vectors, so cos c = sin φ₁ sin φ₂ + cos φ₁ cos φ₂ cos Δλ. On one meridian the angle is just the difference in latitude."),
 ("GE-1.2.B", G("SPH"), "Compare a circle of latitude with a great circle.", "The circle at latitude φ has radius R cos φ, so its length is 2πR cos φ. Only the equator is a great circle; travelling along any other parallel is longer than the great-circle route between the same points."),
 ("GE-1.2.C", G("SPH"), "Find the area of a spherical cap or zone.", "The cap within angular radius θ of a pole has area 2πR²(1 − cos θ), which is 2πR times its height (Archimedes). A cap is the spherical disc, and it has less area than the flat disc of the same radius."),
 ("GE-2.2.A", G("RIE", "HYP"), "Compute the length of a horizontal or vertical segment in the half-plane.", "With metric (dx² + dy²)/y², a horizontal segment of Euclidean length L at height y has length L/y, and a vertical segment from height a to b has length ln(b/a). Lengths grow without bound near the boundary y = 0."),
 ("GE-2.2.B", G("HYP"), "Find the geodesic through two points of the half-plane.", "If the points share an x-coordinate the geodesic is the vertical line. Otherwise it is the semicircle centred on the real axis at the point equidistant from both: solve (x₁ − c)² + y₁² = (x₂ − c)² + y₂²."),
 ("GE-2.2.C", G("HYP"), "Compute hyperbolic areas by integrating and by the angle defect.", "The area element is dx dy / y². The region above height h over a base of width w has finite area w/h although it extends to infinity. A geodesic n-gon has area (n − 2)π minus its angle sum."),
 ("GE-3.2.A", G("CUR"), "Estimate curvature from a measured geodesic triangle.", "For a small geodesic triangle, K ≈ (α + β + γ − π)/area. On a sphere this is exact and gives the radius: R = √(area/excess)."),
 ("GE-3.2.B", G("CUR"), "Estimate curvature from the circumference of a small circle.", "A geodesic circle of radius r has circumference 2πr(1 − Kr²/6 + …). Positive curvature shortens it, negative curvature lengthens it; K ≈ 3(2πr − C)/(πr³)."),
]
ADD = [
 ("GE-1.2.A", N("ge-meridian-distance", SP, "Two towns lie on the same meridian of a sphere of radius {{kr}} km, at latitudes {{k1}}° N and {{k2}}° N. Find the great-circle distance between them.", "kr*(k2 - k1)*pi/180", "kr*pm_sphere_angle(k1, 20, k2, 20)*pi/180",
    "A meridian is a great circle, so the central angle is the difference in latitude", tex="d",
    cases=[{"kr": 6371, "k1": 10, "k2": 40}, {"kr": 6371, "k1": 30, "k2": 60}, {"kr": 3390, "k1": 0, "k2": 45}, {"kr": 1737, "k1": 20, "k2": 80}])),
 ("GE-1.2.A", N("ge-central-angle", SP, "Find the central angle in degrees between the points at latitude {{k1}}°, longitude {{o1}}° and latitude {{k2}}°, longitude {{o2}}° on a sphere.", "kans", "pm_sphere_angle(k1, o1, k2, o2)",
    "cos c = sin φ₁ sin φ₂ + cos φ₁ cos φ₂ cos Δλ", tex="c", tol=0.005,
    cases=[{"k1": a, "o1": b, "k2": c, "o2": d, "kans": round(central(a, b, c, d), 6)} for a, b, c, d in [(0, 0, 0, 90), (45, 0, 45, 90), (60, 0, 60, 180), (30, 10, 60, 100), (0, 0, 90, 50), (45, 0, -45, 0)]])),
 ("GE-1.2.B", N("ge-latitude-circle", SP, "Find the length of the circle of latitude {{kd}}° on a sphere of radius {{kr}}.", "2*pi*kr*cos(kd*pi/180)", "integrate(kr*cos(kd*pi/180), (Y, 0, 2*pi))",
    "The parallel is a circle of radius R cos φ", tex="L",
    given={"kr": {"pick": [1, 6371, 10]}, "kd": {"pick": [30, 45, 60]}})),
 ("GE-1.2.B", N("ge-parallel-vs-great", SP, "Two points lie at latitude 60° on a unit sphere, {{kd}}° of longitude apart. How much longer is the route along the parallel than the great-circle route?", "kans", "cos(pi/3)*kd*pi/180 - pm_sphere_angle(60, 0, 60, kd)*pi/180",
    "Along the parallel the length is cos 60° × Δλ; the great-circle route is the central angle, which is shorter", tex="\\Delta", tol=0.005,
    cases=[{"kd": d, "kans": round(0.5 * radians(d) - radians(central(60, 0, 60, d)), 7)} for d in (60, 90, 120, 180)])),
 ("GE-1.2.C", N("ge-cap-area", SP, "Find the area of the cap of a sphere of radius {{kr}} lying within angular radius {{kd}}° of the north pole.", "2*pi*kr^2*(1 - cos(kd*pi/180))", "integrate(integrate(kr**2*sin(Y), (Y, 0, kd*pi/180)), (Z, 0, 2*pi))",
    "Integrate the area element R² sin θ dθ dφ, or use 2πR × height with height R(1 − cos θ)", tex="A",
    given={"kr": {"pick": [1, 2, 5]}, "kd": {"pick": [30, 60, 90, 120]}})),
 ("GE-1.2.C", N("ge-fraction-above-latitude", SP, "What fraction of a sphere's surface lies north of latitude {{kd}}°?", "(1 - sin(kd*pi/180))/2", "integrate(integrate(cos(Y), (Y, kd*pi/180, pi/2)), (Z, 0, 2*pi))/(4*pi)",
    "By Archimedes the area between two latitudes is proportional to the difference of their heights sin φ", tex="f",
    given={"kd": {"pick": [30, 45, 60, 15]}})),
 ("GE-2.2.A", N("ge-horizontal-length", HY, "In the upper half-plane with metric (dx² + dy²)/y², find the length of the horizontal segment from ({{ka}}, {{ky}}) to ({{kb}}, {{ky}}).", "(kb - ka)/ky", "integrate(1/nsimplify(ky), (Y, ka, kb))",
    "Along a horizontal line y is constant, so every Euclidean length is divided by y", tex="L",
    cases=[{"ka": 0, "kb": 4, "ky": 2}, {"ka": 1, "kb": 3, "ky": 0.5}, {"ka": -2, "kb": 2, "ky": 4}, {"ka": 0, "kb": 1, "ky": 0.1}, {"ka": 0, "kb": 10, "ky": 5}])),
 ("GE-2.2.A", N("ge-vertical-length", HY, "In the upper half-plane, find the hyperbolic length of the vertical segment from height {{ka}} to height {{kb}}.", "log(kb/ka)", "integrate(1/Y, (Y, nsimplify(ka), nsimplify(kb)))",
    "Integrate dy/y. Halving both heights leaves the length unchanged, which is why the boundary is infinitely far away", tex="L",
    cases=[{"ka": 1, "kb": 2}, {"ka": 0.5, "kb": 1}, {"ka": 1, "kb": 10}, {"ka": 0.01, "kb": 1}, {"ka": 2, "kb": 8}])),
 ("GE-2.2.B", N("ge-geodesic-centre", HY, "In the upper half-plane, the geodesic through ({{k1}}, {{k2}}) and ({{k3}}, {{k4}}) is a semicircle centred on the real axis. Find the x-coordinate of its centre.", "(k1^2 + k2^2 - k3^2 - k4^2)/(2*(k1 - k3))", "solve(Eq((k1 - Symbol('m'))**2 + k2**2, (k3 - Symbol('m'))**2 + k4**2), Symbol('m'))[0]",
    "The centre is the point of the real axis at equal Euclidean distance from both points", tex="c",
    cases=[{"k1": 0, "k2": 1, "k3": 2, "k4": 1}, {"k1": 0, "k2": 1, "k3": 1, "k4": 2}, {"k1": -1, "k2": 2, "k3": 3, "k4": 2}, {"k1": 0, "k2": 3, "k3": 4, "k4": 1}, {"k1": 1, "k2": 1, "k3": 3, "k4": 3}])),
 ("GE-2.2.B", N("ge-geodesic-radius", HY, "In the upper half-plane, the geodesic through ({{k1}}, {{k2}}) and ({{k3}}, {{k4}}) is a semicircle centred on the real axis. Find its Euclidean radius.", "sqrt((k1 - (k1^2 + k2^2 - k3^2 - k4^2)/(2*(k1 - k3)))^2 + k2^2)", "sqrt((k3 - solve(Eq((k1 - Symbol('m'))**2 + k2**2, (k3 - Symbol('m'))**2 + k4**2), Symbol('m'))[0])**2 + k4**2)",
    "Find the centre on the real axis first, then the radius is its distance to either point", tex="r",
    cases=[{"k1": 0, "k2": 1, "k3": 2, "k4": 1}, {"k1": 0, "k2": 1, "k3": 1, "k4": 2}, {"k1": -3, "k2": 4, "k3": 3, "k4": 4}, {"k1": 0, "k2": 3, "k3": 4, "k4": 1}])),
 ("GE-2.2.C", N("ge-strip-area", HY, "In the upper half-plane, find the hyperbolic area of the region {{ka}} ≤ x ≤ {{kb}}, y ≥ {{kh}}.", "(kb - ka)/kh", "integrate(integrate(1/Y**2, (Y, nsimplify(kh), oo)), (Z, ka, kb))",
    "Integrate dx dy / y²: the y-integral from h to infinity is 1/h, so the area is width/h, finite even though the region is unbounded", tex="A",
    cases=[{"ka": 0, "kb": 1, "kh": 1}, {"ka": 0, "kb": 3, "kh": 2}, {"ka": -1, "kb": 1, "kh": 0.5}, {"ka": 0, "kb": 2, "kh": 4}])),
 ("GE-2.2.C", N("ge-hyperbolic-polygon-area", HY, "A geodesic {{kn}}-gon in the hyperbolic plane has every interior angle equal to {{kd}}°. Find its area.", "(kn - 2)*pi - kn*kd*pi/180", "solve(Eq(kn*kd*pi/180 + Symbol('m'), (kn - 2)*pi), Symbol('m'))[0]",
    "Cut the polygon into n − 2 triangles: its area is the Euclidean angle sum (n − 2)π minus the actual angle sum", tex="A",
    cases=[{"kn": 4, "kd": 60}, {"kn": 5, "kd": 90}, {"kn": 6, "kd": 90}, {"kn": 8, "kd": 45}, {"kn": 3, "kd": 30}])),
 ("GE-3.2.A", N("ge-curvature-from-triangle", CU, "A geodesic triangle on a surface of constant curvature has angles summing to {{ks}}° and area {{ka}}. Find the curvature.", "(ks - 180)*pi/180/ka", "solve(Eq(ks*pi/180 - pi, Symbol('m')*nsimplify(ka)), Symbol('m'))[0]",
    "Excess (in radians) equals curvature times area; an angle sum below 180° gives negative curvature", tex="K",
    cases=[{"ks": 190, "ka": 2}, {"ks": 170, "ka": 0.5}, {"ks": 270, "ka": 1.5}, {"ks": 181, "ka": 10}, {"ks": 120, "ka": 1}])),
 ("GE-3.2.A", N("ge-radius-from-excess", CU, "Surveyors on a spherical planet measure a triangle of area {{ka}} km² whose angles sum to {{ks}}°. Find the planet's radius in km.", "sqrt(ka/((ks - 180)*pi/180))", "Max(*solve(Eq((ks - 180)*pi/180*Symbol('m')**2, ka), Symbol('m')))",
    "Area = excess × R², so R = √(area/excess) with the excess in radians", tex="R",
    cases=[{"ka": 1000000, "ks": 181.5}, {"ka": 500000, "ks": 180.7}, {"ka": 2000000, "ks": 190}, {"ka": 100000, "ks": 180.5}])),
 ("GE-3.2.B", N("ge-curvature-from-circle", CU, "On a surface, a geodesic circle of radius {{kr}} has circumference {{kc}}. Estimate the curvature from K ≈ 3(2πr − C)/(πr³).", "3*(2*pi*kr - kc)/(pi*kr^3)", "solve(Eq(nsimplify(kc), 2*pi*nsimplify(kr)*(1 - Symbol('m')*nsimplify(kr)**2/6)), Symbol('m'))[0]",
    "The formula inverts C ≈ 2πr(1 − Kr²/6). A circumference short of 2πr means positive curvature", tex="K",
    cases=[{"kr": 0.1, "kc": 0.6273}, {"kr": 0.5, "kc": 3.0}, {"kr": 0.2, "kc": 1.265}, {"kr": 1, "kc": 6.9}, {"kr": 0.5, "kc": 3.2}])),
 ("GE-3.2.B", N("ge-circumference-deficit", CU, "On a sphere of radius {{kb}}, a circle is drawn with geodesic radius {{kr}}. By what fraction is its circumference shorter than 2πr?", "1 - sin(kr/kb)/(kr/kb)", "1 - integrate(kb*sin(Rational(kr, kb)), (Y, 0, 2*pi))/(2*pi*kr)",
    "The circle's true radius in space is R sin(r/R), so its circumference is 2πR sin(r/R); for small r the shortfall is about r²/(6R²)", tex="f",
    cases=[{"kb": 1, "kr": 1}, {"kb": 2, "kr": 1}, {"kb": 10, "kr": 1}, {"kb": 6371, "kr": 1000}, {"kb": 4, "kr": 2}])),
]
NEEDS = {
 "GE-1.2.A": ["GE-1.1.A"], "GE-1.2.B": ["GE-1.2.A"], "GE-1.2.C": ["GE-1.2.B"], "GE-1.1.B": ["GE-1.2.C"],
 "GE-2.2.A": ["GE-1.2.B"], "GE-2.1.A": ["GE-2.2.A"], "GE-2.2.B": ["GE-2.1.A"], "GE-2.2.C": ["GE-2.2.A"], "GE-2.1.B": ["GE-2.2.C", "GE-2.2.B"],
 "GE-3.2.A": ["GE-1.1.B"], "GE-3.2.B": ["GE-2.1.C"], "GE-3.1.A": ["GE-3.2.A", "GE-3.2.B"],
}
