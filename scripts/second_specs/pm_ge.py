"""Geometry (GE, Nov 2026): spherical geometry, hyperbolic geometry and curvature. Structure in UNITS (written by
scripts/pm_setup.py), two question types per objective.

Basis: the Cambridge Part IB Geometry schedule (read through an extraction of the 2026-27 Schedules booklet). Cards
answer by the closed formula; verify expressions integrate the metric or solve the angle-sum relation instead."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "ge-geometry", "geometry", "P1"
FW = dict(id="geometry", title="Geometry", code="GE", domain="ngeo", requires=["calculus", "linear-algebra"], level=4,
          primary="cambridge-ib-geometry", also=[],
          note="Anchored on the Cambridge Part IB Geometry schedule (read through an extraction). The three constant-curvature geometries side by side. Axiomatic Euclidean geometry, projective geometry and the differential geometry of general surfaces are not built; K-12 geometry lives in the school mathematics frameworks.",
          header=["The sphere, the plane and the hyperbolic plane as three versions of one subject: what a straight line is,",
                  "how angle sums and circumferences change, and the single number, curvature, that accounts for all of it.",
                  "School geometry is in the K-12 frameworks; this is the college course that follows it."])
SKILLS = [("spherical", "Great circles, lunes, spherical triangles and rotations of the sphere", "Spherical geometry", []),
          ("hyperbolic", "The half-plane and disc models, geodesics, distance and hyperbolic triangles", "Hyperbolic geometry", ["ngeo.spherical"]),
          ("curvature", "Gaussian curvature of the model spaces and the Gauss-Bonnet relation", "Curvature", ["ngeo.hyperbolic"])]
IDEAS = [("LINE", "Straight means shortest", "A geodesic is a locally shortest path. On a sphere it is a great circle; in the half-plane model it is a vertical line or a semicircle meeting the boundary at right angles."),
         ("CURV", "Curvature is the angle surplus per area", "A triangle's angles exceed π on a sphere and fall short in the hyperbolic plane, by exactly the curvature times its area.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SP, HY, CU = "ngeo.spherical", "ngeo.hyperbolic", "ngeo.curvature"
G = lambda *s: [f"cambridge-ib-geometry:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", final=False, **kw):
    return Q(name, skill, prompt, value=value, tex=tex, final=final, verify=verify, explain=explain, **kw)


UNITS = {
 1: ("spherical", "Spherical geometry", G("SPH"), ["LINE", "CURV"], {
   1: ("Lines and triangles on the sphere", [
     ("A", G("SPH"), "Find great-circle distances and the areas of lunes.",
      "Spherical lines are great circles. The distance between two points is R times the angle they subtend at the centre, and a lune between two great circles meeting at angle θ has area 2θR².", "P1", [
       N("ge-great-circle-distance", SP, "Two points on a sphere of radius {{kr}} km subtend an angle of {{kd}}° at the centre. Find the great-circle distance between them.", "kr*kd*pi/180", "integrate(kr, (Y, 0, kd*pi/180))",
         "Arc length is radius times angle in radians. Any two points that are not antipodal lie on exactly one great circle", tex="d",
         given={"kr": {"pick": [6371, 1737, 3390]}, "kd": {"pick": [30, 45, 60, 90]}}),
       N("ge-lune-area", SP, "Two great circles on a sphere of radius {{kr}} meet at an angle of {{kd}}°. Find the area of one of the lunes between them.", "2*(kd*pi/180)*kr^2", "integrate(integrate(kr**2*sin(Y), (Y, 0, pi)), (Z, 0, kd*pi/180))",
         "A lune is the fraction θ/2π of the whole sphere's area 4πR², which is 2θR²", tex="A",
         given={"kr": {"pick": [1, 2, 3]}, "kd": {"pick": [30, 60, 90, 120]}})]),
     ("B", G("SPH"), "Use the angle excess of a spherical triangle or polygon.",
      "A spherical triangle with angles α, β, γ on a sphere of radius R has area (α + β + γ − π)R². An n-gon has area (angle sum − (n − 2)π)R².", "P1", [
       N("ge-spherical-triangle-area", SP, "A triangle on a sphere of radius {{kr}} has angles {{k1}}°, {{k2}}° and {{k3}}°. Find its area.", "(k1 + k2 + k3 - 180)*pi/180*kr^2", "solve(Eq((k1 + k2 + k3)*pi/180, pi + Symbol('m')/kr**2), Symbol('m'))[0]",
         "Area = excess × R², with the excess α + β + γ − π in radians. The octant with three right angles has excess π/2 and is one eighth of the sphere", tex="A",
         cases=[{"kr": 1, "k1": 90, "k2": 90, "k3": 90}, {"kr": 2, "k1": 80, "k2": 70, "k3": 60}, {"kr": 1, "k1": 120, "k2": 90, "k3": 60}, {"kr": 3, "k1": 100, "k2": 50, "k3": 40}, {"kr": 1, "k1": 90, "k2": 90, "k3": 30}]),
       N("ge-spherical-third-angle", SP, "A triangle on the unit sphere has area {{ka}} and two angles of {{k1}}° and {{k2}}°. Find the third angle in degrees.", "180 + ka*180/pi - k1 - k2", "solve(Eq((k1 + k2 + Symbol('m'))*pi/180 - pi, nsimplify(ka)), Symbol('m'))[0]",
         "The three angles sum to π plus the area on a unit sphere, so the third angle is π + A minus the other two", tex="\\gamma", tol=0.01,
         cases=[{"ka": 0.5, "k1": 80, "k2": 70}, {"ka": 1, "k1": 90, "k2": 90}, {"ka": 0.2, "k1": 60, "k2": 70}, {"ka": 1.5, "k1": 100, "k2": 110}])]),
     ("C", G("SPH"), "Describe the isometries of the sphere and its finite rotation groups.",
      "The isometries of the sphere are the orthogonal maps: rotations about an axis and their compositions with reflections. The finite groups of rotations are cyclic, dihedral, or the rotation groups of the tetrahedron (order 12), cube (24) and icosahedron (60).", "P2", [
       F("ge-sphere-isometries", SP, [
           ("Every orientation-preserving isometry of the sphere is:", "A rotation about some axis", "A reflection in a great circle", "The antipodal map", "A translation"),
           ("The antipodal map x ↦ −x of the 2-sphere is:", "Orientation-reversing", "A rotation by 180°", "Orientation-preserving", "Not an isometry"),
           ("The rotation group of the cube has order:", "24", "12", "48", "60"),
           ("The rotation group of the icosahedron is isomorphic to:", "A₅", "S₅", "A₄", "S₄"),
           ("Besides cyclic and dihedral groups, how many finite rotation groups of the sphere are there?", "3", "5", "1", "Infinitely many")],
         "The five Platonic solids give only three groups, because the cube and octahedron are dual, as are the dodecahedron and icosahedron"),
       N("ge-triangulation-count", SP, "A sphere is tiled by congruent spherical triangles with angles π/2, π/3 and π/{{kn}}. How many triangles are there?", "4/(1/2 + 1/3 + 1/kn - 1)", "solve(Eq(Symbol('m')*(pi/2 + pi/3 + pi/kn - pi), 4*pi), Symbol('m'))[0]",
         "Each triangle has area equal to its excess on the unit sphere, and together they cover 4π. The counts 24, 48 and 120 are the orders of the full symmetry groups of the tetrahedron, cube and icosahedron", tex="triangles", final=True,
         given={"kn": {"pick": [3, 4, 5]}})])]),
 }),
 2: ("hyperbolic", "Hyperbolic geometry", G("RIE", "HYP"), ["LINE", "CURV"], {
   1: ("The half-plane and disc models", [
     ("A", G("RIE", "HYP"), "Measure length in the upper half-plane and identify its geodesics.",
      "The half-plane metric is (dx² + dy²)/y². Geodesics are vertical lines and semicircles centred on the real axis; the distance from ai to bi is |ln(b/a)|.", "P1", [
       N("ge-hyperbolic-distance", HY, "In the upper half-plane model, find the hyperbolic distance between the points {{ka}}i and {{kb}}i.", "log(kb/ka)", "integrate(1/Y, (Y, ka, kb))",
         "Along the vertical geodesic the length element is dy/y, so the distance is ln(b/a). Equal Euclidean steps count for more the closer they are to the boundary", tex="d",
         cases=[{"ka": 1, "kb": 2}, {"ka": 1, "kb": 10}, {"ka": 2, "kb": 8}, {"ka": 3, "kb": 12}, {"ka": 1, "kb": 100}]),
       F("ge-hyperbolic-geodesics", HY, [
           ("In the upper half-plane model, the geodesics are vertical lines and:", "Semicircles centred on the real axis", "All Euclidean straight lines", "Horizontal lines", "Circles tangent to the real axis"),
           ("In the Poincaré disc model, the geodesics are diameters and:", "Circular arcs meeting the boundary circle at right angles", "All chords", "Circles inside the disc", "Arcs through the centre only"),
           ("Both Poincaré models are conformal, meaning that they show correctly:", "Angles", "Lengths", "Areas", "Straightness"),
           ("The boundary of the Poincaré disc is, in hyperbolic terms:", "Infinitely far from every interior point", "At distance 1 from the centre", "A geodesic", "A circle of finite circumference"),
           ("The isometries of the upper half-plane that preserve orientation are the Möbius maps z ↦ (az + b)/(cz + d) with a, b, c, d:", "Real, with ad − bc > 0", "Complex, with ad − bc = 1", "Integers", "Real, with ad − bc < 0")],
         "The models distort lengths but not angles, which is why hyperbolic triangles can be read off a picture")]),
     ("B", G("HYP"), "Use the angle defect of a hyperbolic triangle and compare parallels in the three geometries.",
      "A hyperbolic triangle with angles α, β, γ has area π − (α + β + γ), so no triangle has area above π; an ideal triangle has area exactly π. Through a point off a line there are infinitely many lines that never meet it.", "P1", [
       N("ge-hyperbolic-triangle-area", HY, "A triangle in the hyperbolic plane has angles {{k1}}°, {{k2}}° and {{k3}}°. Find its area.", "(180 - k1 - k2 - k3)*pi/180", "solve(Eq((k1 + k2 + k3)*pi/180, pi - Symbol('m')), Symbol('m'))[0]",
         "Area = π minus the angle sum, in radians. Unlike in the plane, the angles determine the size: similar triangles are congruent", tex="A",
         cases=[{"k1": 60, "k2": 60, "k3": 30}, {"k1": 90, "k2": 45, "k3": 30}, {"k1": 45, "k2": 45, "k3": 45}, {"k1": 90, "k2": 60, "k3": 20}, {"k1": 30, "k2": 30, "k3": 30}]),
       Q("ge-parallels", HY, "Through a point not on a given line, how many lines never meet the given line in {{gm}}?", pace="recall",
         cases=[{"gm": "the Euclidean plane", "kc": 1}, {"gm": "the hyperbolic plane", "kc": 2}, {"gm": "spherical geometry (great circles)", "kc": 0}],
         choice=["None", "Exactly one", "Infinitely many"], correct="kc", verify="authored",
         explain="Any two great circles meet, so the sphere has no parallels. In the hyperbolic plane there are two limiting parallels and infinitely many ultraparallels between them")]),
     ("C", G("RIE", "HYP"), "Compare circumferences of circles in the three geometries.",
      "A circle of geodesic radius r has circumference 2π sin r on the unit sphere, 2πr in the plane and 2π sinh r in the hyperbolic plane: less room than flat on the sphere, more in the hyperbolic plane.", "P1", [
       N("ge-circle-sphere", SP, "On the unit sphere, find the circumference of a circle of geodesic radius {{kr}}.", "2*pi*sin(kr)", "integrate(sin(nsimplify(kr)), (Y, 0, 2*pi))",
         "At polar angle r the circle of latitude has Euclidean radius sin r. The circumference grows until the equator and then shrinks", tex="C",
         given={"kr": {"pick": [0.5, 1, 1.5]}}),
       N("ge-circle-hyperbolic", HY, "In the hyperbolic plane, find the circumference of a circle of geodesic radius {{kr}}.", "2*pi*sinh(kr)", "integrate(sinh(nsimplify(kr)), (Y, 0, 2*pi))",
         "The hyperbolic circumference is 2π sinh r, which grows exponentially with the radius: most of a hyperbolic disc is near its edge", tex="C",
         given={"kr": {"pick": [0.5, 1, 2, 3]}})])]),
 }),
 3: ("curvature", "Curvature", G("CUR"), ["CURV"], {
   1: ("One number behind three geometries", [
     ("A", G("CUR"), "State the Gaussian curvature of the model spaces and how it scales.",
      "A sphere of radius R has curvature 1/R², the plane 0, and the hyperbolic plane −1. Scaling lengths by a factor c divides curvature by c².", "P1", [
       N("ge-sphere-curvature", CU, "Find the Gaussian curvature of a sphere of radius {{kr}}.", "1/kr^2", "limit(3*(2*pi*Y - 2*pi*kr*sin(Y/kr))/(pi*Y**3), Y, 0)",
         "K = 1/R². The same number comes out of how much a small circle's circumference falls short of 2πr: K = lim 3(2πr − C)/(πr³)", tex="K",
         given={"kr": {"pick": [2, 3, 5, 10]}}),
       Q("ge-curvature-sign", CU, "The Gaussian curvature of {{sf}} is:", pace="recall", cases=[
           {"sf": "a sphere", "kc": 0}, {"sf": "a plane", "kc": 1}, {"sf": "the hyperbolic plane", "kc": 2}, {"sf": "a cylinder", "kc": 1},
           {"sf": "a saddle at its centre", "kc": 2}, {"sf": "a cone away from its tip", "kc": 1}, {"sf": "the outer rim of a torus", "kc": 0}, {"sf": "the inner rim of a torus", "kc": 2}],
         choice=["Positive", "Zero", "Negative"], correct="kc", verify="authored",
         explain="A cylinder and a cone unroll flat without stretching, so their Gaussian curvature is zero although they look curved. Gaussian curvature is what a flat map cannot remove")]),
     ("B", G("CUR", "SPH", "HYP"), "Use the Gauss-Bonnet relation between curvature, area and angle sum.",
      "For a geodesic triangle, α + β + γ − π = ∫ K dA. For a closed surface, ∫ K dA = 2πχ: 4π for any sphere, 0 for a torus, 4π(1 − g) for genus g.", "P1", [
       N("ge-total-curvature", CU, "Find the total curvature ∫ K dA of a closed orientable surface of genus {{kg}}.", "4*pi*(1 - kg)", "2*pi*(2 - 2*kg)",
         "Gauss-Bonnet: the total is 2π times the Euler characteristic 2 − 2g, whatever the surface's shape", tex="\\int K\\,dA",
         given={"kg": {"pick": [2, 3, 4, 6]}}),
       N("ge-angle-sum-from-curvature", CU, "A geodesic triangle of area {{ka}} lies on a surface of constant curvature {{kc}}. Find the sum of its angles in degrees.", "180 + kc*ka*180/pi", "solve(Eq(Symbol('m')*pi/180 - pi, nsimplify(kc)*nsimplify(ka)), Symbol('m'))[0]",
         "Angle sum = π + K × area. Positive curvature opens triangles up, negative curvature pinches them", tex="sum", tol=0.01,
         cases=[{"ka": 0.5, "kc": 1}, {"ka": 0.5, "kc": -1}, {"ka": 2, "kc": 0.25}, {"ka": 1, "kc": -1}, {"ka": 3, "kc": -0.5}])])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
