"""Engineering Mechanics (MEC, Nov 2026): statics, dynamics and mechanics of materials. Structure in UNITS (written
by scripts/fw_setup.py), two question types per objective.

Basis: the NCEES FE Mechanical CBT exam specifications (effective July 2020), sections 6 (statics), 7 (dynamics,
kinematics and vibrations) and 8 (mechanics of materials), read to their lettered lines through an extraction of a
university copy of the PDF, so read: part. Cards compute by the handbook formula; verify expressions go back to the
equilibrium equation, an integral of the load, or the eigenvalues of the stress tensor."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "mec-mechanics", "engineering-mechanics", "P1"
M = "Symbol('m')"
FW = dict(id="engineering-mechanics", title="Engineering Mechanics", code="MEC", domain="mech", track="engineering", requires=["physics", "calculus"], level=3,
          primary="fe-mechanical", also=[], subject="Mechanical Engineering",
          note="Anchored on the NCEES FE Mechanical specification, sections 6-8, read to their lettered lines. Structures are described in words because no free-body or beam figure type exists yet, which limits trusses and shear and moment diagrams to their standard cases. Mechanisms (7G), machine design, thermodynamics, fluids and heat transfer sections of that exam are in other frameworks or not built.",
          header=["Forces on bodies at rest, bodies in motion, and what loads do to the material: equilibrium and",
                  "friction, rigid-body dynamics and vibration, then stress, strain, bending, torsion and buckling.",
                  "Particle mechanics is in Physics; this starts where bodies have size."],
          source=dict(id="fe-mechanical-outline", title="Engineering mechanics by FE Mechanical section (course outline)", short="FE Mechanical outline", field="mechanical engineering",
                      note=["The FE Mechanical sections 6-8 written as a source so the mech.* skills have a home.", "NOT a book: only the specification was read. Chapter numbers are ours."]))
_I = [("6A", "Resultants of force systems"), ("6B", "Concurrent force systems"), ("6C", "Equilibrium of rigid bodies"), ("6D", "Frames and trusses"), ("6E", "Centroids and moments of inertia"), ("6F", "Static friction"),
      ("7A", "Kinematics of particles"), ("7B", "Kinetic friction"), ("7C", "Newton's second law for particles"), ("7D", "Work-energy of particles"), ("7E", "Impulse-momentum of particles"),
      ("7F", "Kinematics of rigid bodies"), ("7G", "Kinematics of mechanisms"), ("7H", "Newton's second law for rigid bodies"), ("7I", "Work-energy of rigid bodies"),
      ("7J", "Impulse-momentum of rigid bodies"), ("7K", "Free and forced vibrations"),
      ("8A", "Shear and moment diagrams"), ("8B", "Stress transformations and Mohr's circle"), ("8C", "Stress and strain from axial loads"), ("8D", "Stress and strain from bending"),
      ("8E", "Stress and strain from torsion"), ("8F", "Stress and strain from shear"), ("8G", "Stress and strain from temperature change"), ("8H", "Combined loading"),
      ("8I", "Deformations"), ("8J", "Column buckling"), ("8K", "Statically indeterminate systems")]
STDS = [{"id": "fe-mechanical", "name": "NCEES FE Mechanical CBT Exam Specifications (effective July 2020)", "publisher": "NCEES", "kind": "exam-spec", "read": "part",
         "url": "https://www.bu.edu/eng/files/2020/02/FE-Mechanical-CBT-specs.pdf",
         "note": "Read Nov 2026 through an extraction of a university-hosted copy of the NCEES PDF: sections 6, 7 and 8 with their question ranges and lettered lines. The other sections were not read, so read: part. Items are the lettered lines of sections 6-8, titled in our words.",
         "items": [{"code": c, "title": t} for c, t in _I]}]
SKILLS = [("statics", "Resultants, moments, equilibrium, trusses, centroids, area moments and static friction", "Statics", []),
          ("dynamics", "Curvilinear motion, friction on inclines, energy and impulse, rigid-body rotation and rolling, vibration", "Dynamics and vibrations", ["mech.statics"]),
          ("materials", "Axial, thermal, torsional and bending stress, beam diagrams and deflection, Mohr's circle, pressure vessels and buckling", "Mechanics of materials", ["mech.statics"])]
IDEAS = [("FBD", "Isolate the body, then balance it", "Every statics and dynamics problem starts by cutting one body free and writing the forces and moments on it: zero for equilibrium, mass times acceleration otherwise."),
         ("STRESS", "Stress is load over the geometry that carries it", "Axial stress divides by area, bending by the section modulus, torsion by the polar moment: the material sees the same load very differently depending on shape.")]
PRACTICES = [("P1", "Compute", "Carry an equilibrium, energy or stress relation to a number with its unit."),
             ("P2", "Classify", "Name the case, the support condition or the rule that applies.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ST, DY, MT = ["mech." + s[0] for s in SKILLS]
E_ = lambda *s: [f"fe-mechanical:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UNITS = {
 1: ("statics", "Statics", E_("6A", "6B", "6C", "6D", "6E", "6F"), ["FBD"], {
   1: ("Bodies at rest", [
     ("A", E_("6A"), "Find the resultant of two forces and the moment of a force.",
      "Two forces at angle θ have a resultant of magnitude √(A² + B² + 2AB cos θ). The moment of a force about a point is the force times its perpendicular distance: M = F d sin θ.", "P1", [
       N("mec-resultant", ST, "Forces of {{ka}} N and {{kb}} N act at a point with an angle of {{kt}}° between them. Find the magnitude of their resultant in newtons.", "sqrt(ka^2 + kb^2 + 2*ka*kb*cos(kt*pi/180))",
         "sqrt((ka + kb*cos(kt*pi/180))**2 + (kb*sin(kt*pi/180))**2)", "Add components: put one force on the x-axis and resolve the other", tex="R",
         cases=C("ka kb kt", [(30, 40, 90), (100, 100, 60), (50, 80, 120), (20, 20, 90), (60, 25, 0)])),
       N("mec-moment", ST, "A {{kf}} N force acts on a wrench {{kd}} m from the bolt, at {{kt}}° to the handle. Find the moment about the bolt in N·m.", "kf*kd*sin(kt*pi/180)",
         "Abs(kd*kf*sin(kt*pi/180) - 0*kf*cos(kt*pi/180))", "Only the component perpendicular to the lever arm turns the bolt", tex="M",
         cases=C("kf kd kt", [(100, 0.3, 90), (80, 0.25, 30), (200, 0.4, 60), (50, 0.5, 45), (150, 0.2, 90)]))]),
     ("B", E_("6B"), "Solve a concurrent force system in equilibrium.",
      "For a particle in equilibrium the forces sum to zero in each direction. A weight hung from two identical cables at angle θ above the horizontal gives 2T sin θ = W.", "P1", [
       N("mec-cable-tension", ST, "A {{kw}} N weight hangs from two identical cables, each making {{kt}}° with the horizontal. Find the tension in each cable.", "kw/(2*sin(kt*pi/180))",
         f"solve(Eq(2*{M}*sin(kt*pi/180), kw), {M})[0]", "Vertical components of the two tensions carry the weight; shallow cables need large tensions", tex="T",
         cases=C("kw kt", [(1000, 30), (500, 45), (800, 60), (200, 10), (1200, 53.13)])),
       N("mec-third-force", ST, "A ring is pulled by {{ka}} N along +x and {{kb}} N along +y. Find the magnitude of the third force that holds it in equilibrium.", "sqrt(ka^2 + kb^2)",
         "sqrt((0 - ka)**2 + (0 - kb)**2)", "The balancing force is equal and opposite to the resultant of the other two", tex="F",
         cases=C("ka kb", [(30, 40), (5, 12), (80, 60), (7, 24), (100, 100)]))]),
     ("C", E_("6C"), "Find support reactions on a beam.",
      "Sum moments about one support to get the other reaction, then sum vertical forces. A uniform load acts at the middle of its length.", "P1", [
       N("mec-beam-reaction", ST, "A simply supported beam of span {{kl}} m carries a point load of {{kp}} kN at {{ka}} m from the left support. Find the reaction at the right support in kN.", "kp*ka/kl",
         f"solve(Eq({M}*kl - kp*ka, 0), {M})[0]", "Moments about the left support: the right reaction times the span balances the load times its distance", tex="R_B",
         cases=C("kl kp ka", [(6, 30, 2), (10, 50, 4), (4, 12, 3), (8, 40, 6), (5, 20, 1)])),
       N("mec-beam-reaction-udl", ST, "A simply supported beam of span {{kl}} m carries a uniform load of {{kw}} kN/m over its whole length plus a point load of {{kp}} kN at midspan. Find each support reaction in kN.", "(kw*kl + kp)/2",
         f"solve(Eq({M}*kl, integrate(kw*Y, (Y, 0, kl)) + kp*kl/Rational(2)), {M})[0]", "By symmetry each support takes half the total load; the check takes moments about one end", tex="R",
         cases=C("kl kw kp", [(6, 5, 20), (8, 10, 40), (4, 3, 12), (10, 2, 30), (5, 8, 10)]))]),
     ("D", E_("6D"), "Find member forces in a simple truss and state the truss assumptions.",
      "Truss members are two-force members joined by pins and loaded only at joints, so each carries pure tension or compression. At a joint the forces balance: in a symmetric triangular truss with a load P at the apex, each inclined member carries P ÷ (2 sin θ) in compression.", "P1", [
       N("mec-truss-member", ST, "A symmetric triangular truss carries a vertical load of {{kp}} kN at its apex. Each inclined member makes {{kt}}° with the horizontal. Find the compressive force in each inclined member in kN.", "kp/(2*sin(kt*pi/180))",
         f"solve(Eq(2*{M}*sin(kt*pi/180), kp), {M})[0]", "Method of joints at the apex: the two members' vertical components carry the load", tex="F",
         cases=C("kp kt", [(100, 30), (60, 45), (80, 60), (40, 53.13), (120, 36.87)])),
       F("mec-truss-rules", ST, [
           ("What kind of force can an ideal truss member carry?", "axial tension or compression only", "bending moment", "shear only", "torsion"),
           ("At an unloaded joint where only two non-collinear members meet, what are the member forces?", "both are zero", "equal and opposite", "equal to the support reaction", "cannot be found"),
           ("Three members meet at an unloaded joint and two are collinear. What is the force in the third?", "zero", "equal to the sum of the other two", "twice the others", "it depends on the span"),
           ("Where are loads assumed to act on an ideal truss?", "at the joints only", "at the middle of members", "uniformly along members", "at the supports only")],
         "Pins, straight members and joint loads are what make every member a two-force member")]),
     ("E", E_("6E"), "Locate a centroid and compute an area moment of inertia.",
      "The centroid of a composite area is the area-weighted average of its parts' centroids. A rectangle has I = b h³ ÷ 12 about its own centroidal axis; the parallel-axis theorem moves it: I = I_c + A d².", "P1", [
       N("mec-centroid-composite", ST, "A T-section is a flange {{kb}} mm wide and {{kt}} mm thick on top of a web {{kw}} mm wide and {{kh}} mm tall. Find the height of its centroid above the bottom of the web, in mm.", "(kw*kh*kh/2 + kb*kt*(kh + kt/2))/(kw*kh + kb*kt)",
         f"solve(Eq({M}*(kw*kh + kb*kt), integrate(kw*Y, (Y, 0, kh)) + integrate(kb*Y, (Y, kh, kh + kt))), {M})[0]", "Sum area times centroid height for the two rectangles and divide by the total area", tex="\\bar{y}",
         cases=C("kb kt kw kh", [(100, 20, 20, 100), (150, 25, 25, 150), (80, 10, 10, 60), (200, 40, 40, 160)])),
       N("mec-parallel-axis", ST, "A rectangle {{kb}} mm wide and {{kh}} mm tall has its centroid {{kd}} mm from an axis parallel to its width. Find its moment of inertia about that axis in mm⁴.", "kb*kh^3/12 + kb*kh*kd^2",
         "integrate(kb*Y**2, (Y, kd - kh/Rational(2), kd + kh/Rational(2)))", "Centroidal value plus area times distance squared", tex="I",
         cases=C("kb kh kd", [(20, 60, 50), (100, 20, 40), (30, 30, 30), (50, 120, 60), (10, 40, 25)]))]),
     ("F", E_("6F"), "Apply the laws of static friction.",
      "Static friction takes whatever value equilibrium needs up to μs N. A block on an incline is on the point of sliding when tan θ = μs.", "P1", [
       N("mec-angle-of-repose", ST, "The coefficient of static friction between a block and a plane is {{ku}}. Find the steepest incline angle in degrees at which the block stays at rest.", "atan(ku)*180/pi",
         f"atan2(ku, 1)*180/pi", "At impending slip the friction angle equals the incline angle", tex="\\theta",
         cases=C("ku", [(0.3,), (0.5,), (0.75,), (1,), (0.2,)])),
       N("mec-push-to-slide", ST, "A {{km}} kg crate rests on a level floor with μs = {{ku}}. Find the horizontal force in newtons needed to start it sliding (g = 9.81 m/s²).", "ku*km*9.81",
         f"solve(Eq({M}/(km*Rational(981, 100)), ku), {M})[0]", "The push must reach the maximum static friction, μs times the normal force", tex="F",
         cases=C("km ku", [(50, 0.4), (20, 0.6), (100, 0.25), (8, 0.5), (75, 0.3)]))])]),
 }),
 2: ("dynamics", "Dynamics and vibrations", E_("7A", "7B", "7C", "7D", "7E", "7F", "7H", "7I", "7K"), ["FBD"], {
   1: ("Bodies in motion", [
     ("A", E_("7A"), "Find velocity by integrating acceleration and the normal acceleration on a curve.",
      "Velocity is the integral of acceleration over time. On a curved path the acceleration has a tangential part dv/dt and a normal part v² ÷ ρ directed toward the centre of curvature.", "P1", [
       N("mec-velocity-from-accel", DY, "A particle starts from rest with acceleration a = {{ka}}t m/s² (t in seconds). Find its speed at t = {{kt}} s.", "ka*kt^2/2", "integrate(ka*Y, (Y, 0, kt))",
         "Integrate the acceleration from zero to t", tex="v",
         cases=C("ka kt", [(6, 2), (3, 4), (10, 1.5), (2, 5), (0.5, 8)])),
       N("mec-normal-acceleration", DY, "A car travels at {{kv}} m/s round a curve of radius {{kr}} m. Find its normal (centripetal) acceleration in m/s².", "kv^2/kr", f"solve(Eq({M}*kr, kv**2), {M})[0]",
         "v² over the radius of curvature, toward the centre", tex="a_n",
         cases=C("kv kr", [(20, 100), (30, 150), (15, 45), (25, 250), (10, 20)]))]),
     ("B", E_("7B", "7C"), "Apply Newton's second law with kinetic friction.",
      "On an incline at angle θ a sliding block accelerates at g (sin θ − μk cos θ) down the slope. On level ground a pushed block accelerates at (F − μk m g) ÷ m.", "P1", [
       N("mec-incline-acceleration", DY, "A block slides down a {{kt}}° incline with μk = {{ku}}. Find its acceleration in m/s² (g = 9.81 m/s²).", "9.81*(sin(kt*pi/180) - ku*cos(kt*pi/180))",
         f"solve(Eq(Rational(981, 100)*sin(kt*pi/180) - ku*Rational(981, 100)*cos(kt*pi/180), {M}), {M})[0]", "Gravity along the slope less friction, which is μk times the normal force m g cos θ", tex="a",
         cases=C("kt ku", [(30, 0.2), (45, 0.3), (20, 0.1), (60, 0.5), (37, 0.25)])),
       N("mec-pushed-block", DY, "A {{km}} kg block on a level floor with μk = {{ku}} is pushed horizontally with {{kf}} N. Find its acceleration in m/s² (g = 9.81 m/s²).", "(kf - ku*km*9.81)/km",
         f"solve(Eq(kf - ku*km*Rational(981, 100), km*{M}), {M})[0]", "Net force over mass", tex="a",
         cases=C("km ku kf", [(10, 0.2, 50), (5, 0.3, 40), (20, 0.1, 60), (2, 0.5, 30), (50, 0.25, 200)]))]),
     ("C", E_("7D", "7E"), "Use work-energy and impulse-momentum for a particle.",
      "The work done by all forces equals the change in kinetic energy. The impulse (force × time) equals the change in momentum.", "P1", [
       N("mec-speed-with-friction", DY, "A {{km}} kg block is released from rest and slides down a ramp, dropping {{kh}} m in height while friction does {{kw}} J of negative work. Find its speed at the bottom in m/s (g = 9.81 m/s²).", "sqrt(2*(km*9.81*kh - kw)/km)",
         f"Max(*solve(Eq(km*{M}**2/2, km*Rational(981, 100)*kh - kw), {M}))", "Gravity's work less the friction loss becomes kinetic energy", tex="v",
         cases=C("km kh kw", [(2, 5, 18), (10, 3, 94.3), (1, 2, 4.62), (5, 4, 46.2), (4, 10, 92.4)])),
       N("mec-impulse", DY, "A {{km}} kg ball moving at {{ka}} m/s is hit and leaves in the opposite direction at {{kb}} m/s. The contact lasts {{kt}} ms. Find the average force in newtons.", "km*(ka + kb)/(kt/1000)",
         f"solve(Eq({M}*kt/1000, km*kb - km*(-ka)), {M})[0]", "Change in momentum, counting the reversal, divided by the contact time", tex="F",
         cases=C("km ka kb kt", [(0.15, 30, 40, 2), (0.06, 20, 50, 5), (0.4, 10, 15, 10), (0.045, 0.5, 70, 0.5)]))]),
     ("D", E_("7F"), "Relate angular and linear motion and use rolling without slipping.",
      "A point at radius r on a body turning at ω moves at v = ω r. A wheel rolling without slipping has v = ω r at its centre; the contact point is momentarily at rest and the top moves at 2v.", "P1", [
       N("mec-rim-speed", DY, "A flywheel of radius {{kr}} m turns at {{kn}} rev/min. Find the speed of a point on its rim in m/s.", "kn*2*pi/60*kr", f"solve(Eq({M}/kr*60/(2*pi), kn), {M})[0]",
         "Convert rev/min to rad/s, then multiply by the radius", tex="v",
         cases=C("kr kn", [(0.5, 600), (0.2, 1500), (1, 120), (0.15, 3000), (0.3, 900)])),
       N("mec-rolling-top", DY, "A wheel of radius {{kr}} m rolls without slipping at an angular speed of {{kw}} rad/s. Find the speed of the top of the wheel in m/s.", "2*kw*kr",
         "kw*kr + kw*kr", "The contact point is the instantaneous centre, and the top is two radii from it", tex="v",
         cases=C("kr kw", [(0.3, 10), (0.5, 4), (0.25, 20), (0.4, 15), (1, 3)]))]),
     ("E", E_("7H", "7I"), "Apply Newton's second law to rotation and to rolling bodies.",
      "Torque = I α. A solid disc has I = ½ m r², a hoop m r², a solid sphere ⅖ m r². A body with I = k m r² rolling without slipping down an incline accelerates at g sin θ ÷ (1 + k).", "P1", [
       N("mec-angular-acceleration", DY, "A torque of {{kt}} N·m acts on a solid disc of mass {{km}} kg and radius {{kr}} m about its axis. Find the angular acceleration in rad/s².", "kt/(0.5*km*kr^2)",
         f"solve(Eq(kt, km*kr**2/2*{M}), {M})[0]", "α = τ/I with I = ½mr² for a disc", tex="\\alpha",
         cases=C("kt km kr", [(10, 5, 0.4), (2, 1, 0.2), (50, 20, 0.5), (0.6, 0.3, 0.1), (12, 8, 0.25)])),
       N("mec-rolling-incline", DY, "A solid sphere (I = 0.4 m r²) rolls without slipping down a {{kt}}° incline. Find its acceleration in m/s² (g = 9.81 m/s²).", "9.81*sin(kt*pi/180)/1.4",
         f"solve(Eq(Rational(981, 100)*sin(kt*pi/180) - Rational(2, 5)*{M}, {M}), {M})[0]", "Friction supplies the torque; the rotational inertia takes its share of the driving force", tex="a",
         cases=C("kt", [(30,), (20,), (45,), (10,), (37,)]))]),
     ("F", E_("7K"), "Find the natural frequency and damping ratio of a spring-mass system.",
      "Undamped natural frequency ωn = √(k ÷ m), so f = ωn ÷ 2π. Damping ratio ζ = c ÷ (2 √(k m)): below 1 the system oscillates, at 1 it is critically damped. A forcing frequency near the natural frequency gives resonance.", "P1", [
       N("mec-natural-frequency", DY, "A {{km}} kg mass hangs from a spring of stiffness {{kk}} N/m. Find its natural frequency in Hz.", "sqrt(kk/km)/(2*pi)",
         f"Max(*solve(Eq(km*(2*pi*{M})**2, kk), {M}))", "ωn = √(k/m), then divide by 2π", tex="f_n",
         cases=C("km kk", [(2, 800), (0.5, 200), (10, 4000), (1, 100), (4, 1600)])),
       N("mec-damping-ratio", DY, "A system has mass {{km}} kg, stiffness {{kk}} N/m and damping coefficient {{kd}} N·s/m. Find its damping ratio.", "kd/(2*sqrt(kk*km))",
         f"solve(Eq({M}*2*sqrt(kk*km), kd), {M})[0]", "Actual damping over critical damping, 2√(km)", tex="\\zeta",
         cases=C("km kk kd", [(2, 800, 16), (1, 100, 4), (10, 4000, 400), (0.5, 200, 2), (4, 1600, 40)]))])]),
 }),
 3: ("materials", "Mechanics of materials", E_("8A", "8B", "8C", "8D", "8E", "8G", "8H", "8I", "8J", "8K"), ["STRESS"], {
   1: ("Stress and deformation", [
     ("A", E_("8C"), "Compute axial stress and elongation.",
      "Normal stress σ = P ÷ A. Within the elastic range the elongation is δ = P L ÷ (A E).", "P1", [
       N("mec-axial-stress", MT, "A rod of cross-sectional area {{ka}} mm² carries an axial load of {{kp}} kN. Find the normal stress in MPa.", "1000*kp/ka", f"solve(Eq({M}*ka/1000, kp), {M})[0]",
         "Newtons per square millimetre are megapascals", tex="\\sigma",
         cases=C("ka kp", [(200, 30), (500, 100), (78.5, 15.7), (1000, 250), (314, 47.1)])),
       N("mec-elongation", MT, "A steel bar (E = 200 GPa) is {{kl}} m long with an area of {{ka}} mm² and carries {{kp}} kN in tension. Find its elongation in mm.", "kp*1000*kl*1000/(ka*200000)",
         f"solve(Eq({M}/(kl*1000)*200000, kp*1000/ka), {M})[0]", "Strain is stress over E; elongation is strain times length", tex="\\delta",
         cases=C("kl ka kp", [(2, 400, 80), (1.5, 300, 60), (3, 500, 100), (0.5, 100, 20), (4, 1000, 150)]))]),
     ("B", E_("8G", "8K"), "Compute thermal expansion and the stress in a constrained bar.",
      "A free bar changes length by δ = α ΔT L. If both ends are fixed the bar cannot expand, and the stress is σ = E α ΔT (compressive on heating), whatever its length or area.", "P1", [
       N("mec-thermal-expansion", MT, "A {{kl}} m aluminium rail (α = 23 × 10⁻⁶ per °C) warms by {{kt}} °C. Find its free expansion in mm.", "23e-6*kt*kl*1000",
         f"solve(Eq({M}/(kl*1000), Rational(23, 1000000)*kt), {M})[0]", "Thermal strain α ΔT times the length", tex="\\delta",
         cases=C("kl kt", [(10, 40), (25, 30), (4, 50), (12, 25), (100, 20)])),
       N("mec-thermal-stress", MT, "A steel bar (E = 200 GPa, α = 12 × 10⁻⁶ per °C) is held between rigid walls and heated by {{kt}} °C. Find the compressive stress in MPa.", "200000*12e-6*kt",
         f"solve(Eq({M}/200000, Rational(12, 1000000)*kt), {M})[0]", "The walls must push back the whole thermal strain: σ = E α ΔT", tex="\\sigma",
         cases=C("kt", [(50,), (30,), (80,), (25,), (100,)]))]),
     ("C", E_("8E"), "Compute torsional shear stress and angle of twist in a solid shaft.",
      "Maximum shear stress τ = T c ÷ J with J = π d⁴ ÷ 32 for a solid circular shaft, so τ = 16 T ÷ (π d³). Angle of twist φ = T L ÷ (G J).", "P1", [
       N("mec-torsion-stress", MT, "A solid circular shaft of diameter {{kd}} mm carries a torque of {{kt}} N·m. Find the maximum shear stress in MPa.", "16*kt*1000/(pi*kd^3)",
         f"(kt*1000)*(kd/Rational(2))/(pi*kd**4/32)", "τ = Tc/J; the check uses c = d/2 and J = πd⁴/32", tex="\\tau",
         cases=C("kd kt", [(40, 500), (25, 150), (50, 1200), (20, 60), (80, 4000)])),
       N("mec-angle-of-twist", MT, "A solid steel shaft (G = 80 GPa) of diameter {{kd}} mm and length {{kl}} m carries a torque of {{kt}} N·m. Find the angle of twist in degrees.", "kt*1000*kl*1000/(80000*pi*kd^4/32)*180/pi",
         f"solve(Eq({M}*pi/180*80000*pi*kd**4/32, kt*1000*kl*1000), {M})[0]", "φ = TL/(GJ) in radians, then convert", tex="\\phi",
         cases=C("kd kl kt", [(40, 2, 500), (25, 1, 150), (50, 3, 1200), (20, 0.5, 60), (80, 4, 4000)]))]),
     ("D", E_("8A"), "Find the maximum shear and bending moment in standard beams.",
      "Simply supported beam with a central point load P: maximum shear P ÷ 2, maximum moment P L ÷ 4. With a uniform load w: maximum shear w L ÷ 2, maximum moment w L² ÷ 8. A cantilever with an end load P: maximum moment P L at the wall.", "P1", [
       N("mec-max-moment-udl", MT, "A simply supported beam of span {{kl}} m carries a uniform load of {{kw}} kN/m. Find the maximum bending moment in kN·m.", "kw*kl^2/8",
         "integrate(kw*kl/Rational(2) - kw*Y, (Y, 0, kl/Rational(2)))", "The moment is the area under the shear diagram up to midspan, where the shear is zero", tex="M",
         cases=C("kl kw", [(6, 5), (8, 10), (4, 3), (10, 2), (5, 8)])),
       N("mec-max-moment-point", MT, "A simply supported beam of span {{kl}} m carries a point load of {{kp}} kN at midspan. Find the maximum bending moment in kN·m.", "kp*kl/4",
         "integrate(kp/Rational(2), (Y, 0, kl/Rational(2)))", "Half the load as a reaction, acting over half the span", tex="M",
         cases=C("kl kp", [(6, 30), (10, 50), (4, 12), (8, 40), (5, 20)]))]),
     ("E", E_("8D", "8I"), "Compute bending stress and a standard beam deflection.",
      "Bending stress σ = M c ÷ I; for a rectangle b × h this is 6M ÷ (b h²). A simply supported beam with a central load deflects P L³ ÷ (48 E I) at midspan.", "P1", [
       N("mec-bending-stress", MT, "A rectangular beam {{kb}} mm wide and {{kh}} mm deep carries a bending moment of {{km}} kN·m. Find the maximum bending stress in MPa.", "6*km*1e6/(kb*kh^2)",
         f"(km*10**6)*(kh/Rational(2))/(kb*kh**3/Rational(12))", "σ = Mc/I with c = h/2 and I = bh³/12", tex="\\sigma",
         cases=C("kb kh km", [(50, 100, 5), (100, 200, 40), (40, 80, 2), (150, 300, 90), (20, 60, 0.6)])),
       N("mec-midspan-deflection", MT, "A simply supported steel beam (E = 200 GPa) of span {{kl}} m with I = {{ki0}} × 10⁶ mm⁴ carries {{kp}} kN at midspan. Find the midspan deflection in mm.", "kp*1000*(kl*1000)^3/(48*200000*ki0*1e6)",
         f"solve(Eq({M}*48*200000*ki0*10**6, kp*1000*(kl*1000)**3), {M})[0]", "δ = PL³/(48EI), keeping newtons and millimetres throughout", tex="\\delta",
         cases=C("kl ki0 kp", [(4, 20, 30), (6, 80, 50), (3, 10, 12), (8, 200, 40), (5, 45, 20)]))]),
     ("F", E_("8B"), "Find principal stresses and the maximum in-plane shear stress.",
      "For plane stress the centre of Mohr's circle is (σx + σy) ÷ 2 and its radius is √(((σx − σy) ÷ 2)² + τxy²). The principal stresses are centre ± radius and the maximum in-plane shear stress is the radius.", "P1", [
       N("mec-principal-stress", MT, "At a point σx = {{ka}} MPa, σy = {{kb}} MPa and τxy = {{kt}} MPa. Find the larger principal stress in MPa.", "(ka + kb)/2 + sqrt(((ka - kb)/2)^2 + kt^2)",
         "Max(*Matrix([[ka, kt], [kt, kb]]).eigenvals().keys())", "Centre plus radius of Mohr's circle; the check takes the larger eigenvalue of the stress matrix", tex="\\sigma_1",
         cases=C("ka kb kt", [(80, 20, 40), (100, 0, 50), (60, -20, 30), (50, 50, 25), (120, 40, 30)])),
       N("mec-max-shear", MT, "At a point σx = {{ka}} MPa, σy = {{kb}} MPa and τxy = {{kt}} MPa. Find the maximum in-plane shear stress in MPa.", "sqrt(((ka - kb)/2)^2 + kt^2)",
         "(Max(*Matrix([[ka, kt], [kt, kb]]).eigenvals().keys()) - Min(*Matrix([[ka, kt], [kt, kb]]).eigenvals().keys()))/2", "The radius of Mohr's circle, half the difference of the principal stresses", tex="\\tau_{max}",
         cases=C("ka kb kt", [(80, 20, 40), (100, 0, 50), (60, -20, 30), (120, 40, 30), (90, 30, 40)]))]),
     ("G", E_("8H"), "Compute pressure-vessel stresses and combine axial and bending stress.",
      "A thin-walled cylinder under pressure p has hoop stress p r ÷ t and longitudinal stress p r ÷ (2t). Axial load and bending on the same section superpose: σ = P ÷ A ± M c ÷ I.", "P1", [
       N("mec-hoop-stress", MT, "A thin-walled cylindrical tank of radius {{kr}} mm and wall thickness {{kt}} mm holds a pressure of {{kp}} MPa. Find the hoop stress in MPa.", "kp*kr/kt",
         f"solve(Eq(2*{M}*kt, kp*2*kr), {M})[0]", "Cut the cylinder lengthwise: wall force 2σt balances pressure on the projected width 2r", tex="\\sigma_h",
         cases=C("kr kt kp", [(500, 10, 2), (250, 5, 1.5), (1000, 20, 0.8), (150, 3, 4), (600, 12, 1)])),
       N("mec-combined-stress", MT, "A rectangular section {{kb}} mm × {{kh}} mm carries an axial tension of {{kp}} kN and a bending moment of {{km}} kN·m about its strong axis. Find the maximum tensile stress in MPa.", "kp*1000/(kb*kh) + 6*km*1e6/(kb*kh^2)",
         f"kp*1000/Rational(kb*kh) + (km*10**6)*(kh/Rational(2))/(kb*kh**3/Rational(12))", "Add the uniform axial stress to the bending stress on the tension side", tex="\\sigma",
         cases=C("kb kh kp km", [(50, 100, 100, 5), (100, 200, 400, 40), (40, 80, 64, 2), (20, 60, 24, 0.6)]))]),
     ("H", E_("8J"), "Compute an Euler buckling load and choose the effective length factor.",
      "Critical load P = π² E I ÷ (K L)². K is 1 for pinned-pinned ends, 0.5 for fixed-fixed, about 0.7 for fixed-pinned and 2 for fixed-free. Buckling depends on stiffness and slenderness, not on strength.", "P1", [
       N("mec-euler-buckling", MT, "A pinned-pinned steel column (E = 200 GPa) is {{kl}} m long with I = {{ki0}} × 10⁶ mm⁴. Find its Euler buckling load in kN.", "pi^2*200000*ki0*1e6/(kl*1000)^2/1000",
         f"solve(Eq({M}*1000*(kl*1000)**2, pi**2*200000*ki0*10**6), {M})[0]", "π²EI/L² with K = 1", tex="P_{cr}",
         cases=C("kl ki0", [(4, 10), (3, 5), (6, 40), (5, 20), (2.5, 2)])),
       L("mec-effective-length", MT, "What is the theoretical effective length factor K? {{q}}", ["0.5", "0.7", "1", "2"], [
           ("Both ends pinned", 2), ("Both ends fixed", 0), ("One end fixed, the other pinned", 1), ("One end fixed, the other free (a flagpole)", 3)],
         "The more the ends are restrained, the shorter the column behaves")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
