"""Second question types for the two Math HS objectives that still had one drill (Nov 2026)."""
from opl_dsl import Q

FILE, FRAMEWORK = "mh-second-types-4", "math-hs"
ADD = [
 ("MH-7.5.B", Q("hs2-law-of-cosines-side", "geo.right-triangles", "In triangle ABC, a = {{ka}}, b = {{kb}} and the angle between them is C = {{kg}}°. Find c with the Law of Cosines.",
    cases=[{"ka": 5, "kb": 8, "kg": 60}, {"ka": 3, "kb": 5, "kg": 120}, {"ka": 7, "kb": 7, "kg": 90}, {"ka": 6, "kb": 10, "kg": 60}, {"ka": 4, "kb": 9, "kg": 45}],
    value="sqrt(ka^2 + kb^2 - 2*ka*kb*cos(kg*pi/180))", tex="c", verify="sqrt((kb*cos(kg*pi/180) - ka)**2 + (kb*sin(kg*pi/180))**2)",
    explain="c² = a² + b² − 2ab cos C. The proof puts C at the origin with a along the x-axis and uses the distance formula, which is the check here")),
 ("MH-10.1.D", Q("hs2-tangent-angle", "geo.circles", "A point is {{kd}} from the centre of a circle of radius {{kr}}. Find the angle between the two tangents from the point, in degrees.",
    cases=[{"kr": 5, "kd": 10}, {"kr": 3, "kd": 5}, {"kr": 5, "kd": 13}, {"kr": 1, "kd": 2}, {"kr": 6, "kd": 10}],
    value="2*asin(kr/kd)*180/pi", tex="\\theta", verify="2*acos(sqrt(kd**2 - kr**2)/kd)*180/pi", tol=0.001,
    explain="Each tangent meets its radius at a right angle, so the half-angle at the point has sine r/d. The construction finds the tangent points on the circle whose diameter joins the point to the centre")),
]
