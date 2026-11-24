from opl_dsl import Q, L, U

FW, FILE, IDEA = "FM", "opl-fm", "HEAD"
G = "Rational(981, 100)"

UNITS = [
U(11, "kinematics", "Kinematics, statics extras and differential analysis", [
    ("Statics extras", [
        L("A", "Find the vertical force on a curved surface.", "The vertical component equals the weight of fluid above the surface.", ["FM2.4"], [
            Q("fm-curved-surface", "fm.statics", "A quarter-circle gate of radius {{R}} m and width {{w}} m holds water ($\\rho g = 9810$ N/m³) above it, the water surface level with the top of the arc. What is the vertical force on the gate, in kN?",
              given={"R": {"pick": [1, 2, 3]}, "w": {"pick": [1, 2, 4]}}, value="9810*(R^2 - pi*R^2/4)*w/1000", tex="F_V", tol=0.0001,
              verify="integrate(9810*w*(R - sqrt(R**2 - x**2)), (x, 0, R))/1000",
              explain="Count the water standing on the gate: the square $R \\times R$ less the quarter circle, times the width. The horizontal component is the force on the vertical projection")]),
        L("B", "Find pressure through layered fluids.", "Add ρgh layer by layer.", ["FM2.5"], [
            Q("fm-layered-pressure", "fm.statics", "A tank holds {{h1}} m of oil (SG {{s1}}) floating on {{h2}} m of water. What is the gauge pressure at the bottom, in kPa? ($g = 9.81$)",
              given={"h1": {"pick": [0.5, 1, 2]}, "s1": {"pick": [0.8, 0.85, 0.9]}, "h2": {"pick": [1, 2, 3]}}, value="9.81*(1000*s1*h1 + 1000*h2)/1000", tex="p", tol=0.0001,
              verify=f"(integrate({G}*1000*nsimplify(s1), (x, 0, nsimplify(h1))) + integrate({G}*1000, (x, nsimplify(h1), nsimplify(h1) + h2)))/1000",
              explain="Pressure grows at the rate $\\rho g$ of whichever fluid you are in; the lighter oil adds less per metre")]),
        L("C", "Find the free surface of a liquid in rigid-body rotation.", "The surface is a paraboloid; the rim stands ω²R²/2g above the centre.", ["FM2.7"], [
            Q("fm-rotating-tank", "fm.statics", "A cylinder of water with radius {{R}} m spins at {{w}} rad/s. How much higher is the surface at the wall than at the centre, in m? ($g = 9.81$)",
              given={"R": {"pick": [0.1, 0.2, 0.3]}, "w": {"pick": [5, 10, 15]}}, value="w^2*R^2/(2*9.81)", tex="\\Delta h", tol=0.0001,
              verify=f"integrate(w**2*x/{G}, (x, 0, nsimplify(R)))", explain="In the rotating frame the surface is perpendicular to the combined gravity and centrifugal field: $dz/dr = \\omega^2r/g$")]),
    ]),
    ("Kinematics", [
        L("A", "Find a streamline of a steady flow.", "Along a streamline dy/dx = v/u; in steady flow streamlines, pathlines and streaklines coincide.", ["FM1.4"], [
            Q("fm-streamline", "fm.viscous", "In the steady flow $u = {{a}}x$, $v = -{{a}}y$, the streamline through $({{x0}}, {{y0}})$ passes $x = {{x1}}$ at what $y$?",
              given={"a": {"pick": [1, 2, 3]}, "x0": {"pick": [1, 2]}, "y0": {"pick": [1, 2, 3]}, "x1": {"pick": [3, 4, 5]}}, value="x0*y0/x1", tex="y",
              verify="solve(Eq(log(x/y0), -log(Rational(x1, x0))), x)[0]",
              explain="$dy/dx = -y/x$ integrates to $xy = $ const, so $y = x_0y_0/x_1$: hyperbolas, the flow toward a stagnation point")]),
        L("B", "Find the convective acceleration of a steady flow.", "a = (V·∇)V; steady flow can still accelerate.", ["FM4.1"], [
            Q("fm-convective-acceleration", "fm.viscous", "A steady 1-D flow speeds up through a nozzle as $u = {{U}}(1 + x/{{Lz}})$ m/s. What is the fluid's acceleration at $x = {{xp}}$ m, in m/s²?",
              given={"U": {"pick": [2, 5, 10]}, "Lz": {"pick": [0.5, 1, 2]}, "xp": {"pick": [0.5, 1]}}, value="U*(1 + xp/Lz)*U/Lz", tex="a_x", tol=0.0001,
              verify="(U*(1 + Symbol('X')/nsimplify(Lz))*diff(U*(1 + Symbol('X')/nsimplify(Lz)), Symbol('X'))).subs(Symbol('X'), nsimplify(xp))",
              explain="Nothing changes in time at a fixed point, but a particle moving downstream finds faster fluid: $a = u\\,\\partial u/\\partial x$")]),
        L("C", "Use a stream function.", "u = ∂ψ/∂y, v = −∂ψ/∂x; ψ is constant along streamlines.", ["FM4.5"], [
            Q("fm-stream-function", "fm.viscous", "A flow has stream function $\\psi = {{a}}x^2y - {{b}}y^3$. Find $v$ at $(x, y) = ({{x0}}, {{y0}})$.",
              given={"a": {"pick": [1, 2, 3]}, "b": {"pick": [1, 2]}, "x0": {"pick": [1, 2, -1]}, "y0": {"pick": [1, 2, 3]}}, value="-2*a*x0*y0", tex="v",
              verify="-diff(a*x**2*Symbol('Y') - b*Symbol('Y')**3, x).subs({x: x0, Symbol('Y'): y0})", explain="$v = -\\partial\\psi/\\partial x$. Any ψ gives a flow that satisfies continuity automatically")]),
        L("D", "Compute vorticity.", "ω_z = ∂v/∂x − ∂u/∂y; irrotational flow has ω = 0.", ["FM4.6"], [
            Q("fm-vorticity", "fm.viscous", "For $u = {{a}}y$, $v = {{b}}x$, what is the vorticity $\\omega_z$?",
              given={"a": {"pick": [-3, -1, 1, 2, 4]}, "b": {"pick": [-2, 1, 2, 3]}}, require=["a != b"], value="b - a", tex="\\omega_z",
              verify="diff(b*x, x) - diff(a*Symbol('Y'), Symbol('Y'))", explain="Vorticity is twice the local rate of rotation. Couette flow ($v = 0$, $u \\propto y$) has vorticity even though its streamlines are straight")]),
        L("E", "Get velocities from a velocity potential.", "V = ∇φ in irrotational flow.", ["FM4.7"], [
            Q("fm-velocity-potential", "fm.viscous", "An irrotational flow has $\\phi = {{a}}(x^2 - y^2)$. Find $u$ at $x = {{x0}}$.",
              given={"a": {"pick": [0.5, 1, 2, 3]}, "x0": {"pick": [1, 2, 3]}}, value="2*a*x0", tex="u",
              verify="diff(nsimplify(a)*(x**2 - Symbol('Y')**2), x).subs(x, x0)", explain="$u = \\partial\\phi/\\partial x$, $v = \\partial\\phi/\\partial y$. This is flow into a corner; φ and ψ are harmonic conjugates")]),
        L("F", "Find viscous dissipation.", "In Couette flow, Φ = μ(du/dy)² per unit volume.", ["FM4.4"], [
            Q("fm-viscous-dissipation", "fm.viscous", "Oil ($\\mu = {{mu}}$ Pa·s) in a {{h}} mm gap is sheared by a plate at {{U}} m/s. What is the heating rate per unit volume, in kW/m³?",
              given={"mu": {"pick": [0.1, 0.3, 0.5]}, "h": {"pick": [0.5, 1, 2]}, "U": {"pick": [1, 2, 5]}}, value="mu*(U/(h/1000))^2/1000", tex="\\Phi", tol=0.0001,
              verify="nsimplify(mu)*diff(U*x/(nsimplify(h)/1000), x)**2/1000", explain="The energy equation's dissipation term turns shear work into heat; in bearings it sets the temperature rise")]),
    ]),
]),
U(12, "external-compressible", "Boundary layers, potential flow and compressible flow", [
    ("Similarity, angular momentum and diffusers", [
        L("A", "Compute a Froude number.", "Fr = V/√(gL): inertia over gravity, the group for free-surface flows.", ["FM5.2"], [
            Q("fm-froude", "fm.similarity", "A ship {{L}} m long moves at {{V}} m/s. What is its Froude number? ($g = 9.81$)",
              given={"L": {"pick": [50, 100, 200]}, "V": {"pick": [5, 8, 12]}}, value="V/sqrt(9.81*L)", tex="Fr", tol=0.0001, verify=f"V/sqrt({G}*L)",
              explain="Nondimensionalising the momentum equation leaves Re, Fr, Ma and others; which ones matter depends on which forces act")]),
        L("B", "Find a torque from an angular-momentum balance.", "T = ṁ r V_t for a jet leaving at radius r.", ["FM3.5"], [
            Q("fm-sprinkler-torque", "fm.momentum", "A lawn sprinkler's two arms of radius {{r}} m each discharge {{m}} kg/s tangentially at {{V}} m/s relative to the ground. What torque holds it still, in N·m?",
              given={"r": {"pick": [0.1, 0.15, 0.2]}, "m": {"pick": [0.1, 0.2, 0.5]}, "V": {"pick": [5, 10, 15]}}, value="2*m*r*V", tex="T", tol=0.0001,
              verify="2*nsimplify(m)*Matrix([nsimplify(r), 0, 0]).cross(Matrix([0, V, 0]))[2]", explain="Angular momentum leaves at $rV$ per kilogram from each arm; held still, the sprinkler must supply that torque")]),
        L("C", "Find the ideal pressure recovery of a diffuser.", "C_p = 1 − (A₁/A₂)² for frictionless incompressible flow.", ["FM6.11"], [
            Q("fm-diffuser", "fm.bernoulli", "A diffuser has area ratio $A_2/A_1 = {{ar}}$. What is the ideal pressure-recovery coefficient $C_p = \\Delta p/(\\tfrac12\\rho V_1^2)$?",
              given={"ar": {"pick": [1.5, 2, 3, 4]}}, value="1 - 1/ar^2", tex="C_p", tol=0.0001,
              verify="1 - (1/nsimplify(ar))**2", explain="Continuity slows the flow by the area ratio and Bernoulli turns the lost velocity head into pressure. Real diffusers recover less; too steep a wall separates")]),
    ]),
    ("Boundary layers", [
        L("A", "Estimate a laminar boundary-layer thickness.", "δ ≈ 5x/√Re_x (Blasius); the momentum-integral method gives 5.48.", ["FM7.1"], [
            Q("fm-boundary-thickness", "fm.external", "Air ($\\nu = 1.5\\times10^{-5}$ m²/s) flows at {{U}} m/s over a flat plate. Using $\\delta = 5x/\\sqrt{Re_x}$, how thick is the boundary layer {{xp}} m from the leading edge, in mm?",
              given={"U": {"pick": [1, 2, 5]}, "xp": {"pick": [0.1, 0.2, 0.5]}}, value="5*xp/sqrt(U*xp/0.000015)*1000", tex="\\delta", tol=0.0001,
              verify="5*sqrt(nsimplify(xp)*Rational(15, 1000000)/U)*1000", explain="δ grows as $\\sqrt x$. A momentum-integral estimate with a parabolic profile gives a slightly different constant (5.48)")]),
        L("B", "Predict the effect of a pressure gradient on a boundary layer.", "Adverse (rising) pressure slows the near-wall fluid and can separate it.", ["FM7.4"], [
            Q("fm-pressure-gradient", "fm.external", "{{q}}", pace="recall",
              cases=[{"q": "What happens to a boundary layer in a strong adverse pressure gradient (pressure rising downstream)?", "ans": 0},
                     {"q": "What does a favourable pressure gradient (pressure falling downstream) do to a boundary layer?", "ans": 1},
                     {"q": "Where on a cylinder in cross-flow does the pressure gradient become adverse?", "ans": 2}],
              choice=["It thickens and may separate, with reversed flow near the wall", "It thins and stays attached, delaying transition", "Past the shoulder, on the rear half"], correct="ans", verify="authored",
              explain="The near-wall fluid has little momentum; pushing against rising pressure stops it first. Separation is why bluff bodies have large pressure drag")]),
    ]),
    ("Potential flow", [
        L("A", "Find the velocity induced by a source.", "A 2-D source of strength m gives v_r = m/(2πr).", ["FM8.1"], [
            Q("fm-source-velocity", "fm.external", "A 2-D line source discharges {{m}} m²/s. What is the radial speed {{r}} m away, in m/s?",
              given={"m": {"pick": [1, 2, 5]}, "r": {"pick": [0.5, 1, 2]}}, value="m/(2*pi*r)", tex="v_r", tol=0.0001,
              verify="solve(Eq(2*pi*nsimplify(r)*x, m), x)[0]", explain="All the flow crosses a circle of circumference $2\\pi r$; sources, sinks, vortices and uniform flow are the building blocks")]),
        L("B", "Superpose a uniform stream and a source.", "The stagnation point sits where the source's outflow cancels the stream: x = −m/(2πU).", ["FM8.2"], [
            Q("fm-rankine-stagnation", "fm.external", "A uniform stream of {{U}} m/s meets a 2-D source of strength {{m}} m²/s at the origin. How far upstream is the stagnation point, in m?",
              given={"U": {"pick": [1, 2, 5]}, "m": {"pick": [1, 2, 5, 10]}}, value="m/(2*pi*U)", tex="|x_s|", tol=0.0001,
              verify="-solve(Eq(U + m/(2*pi*x), 0), x)[0]", explain="Superposition works because potential flow is linear; the dividing streamline through the stagnation point is the Rankine half-body's surface")]),
        L("C", "Use the potential flow past a cylinder.", "Surface speed 2U sin θ; C_p = 1 − 4 sin²θ.", ["FM8.3"], [
            Q("fm-cylinder-cp", "fm.external", "In ideal flow past a circular cylinder, what is the pressure coefficient on the surface at $\\theta = {{t}}°$ from the front stagnation point?",
              given={"t": {"pick": [30, 45, 60, 90]}}, value="1 - 4*sin(t*pi/180)^2", tex="C_p", tol=0.0001,
              verify="1 - (2*sin(t*pi/180))**2", explain="Bernoulli with surface speed $2U\\sin\\theta$; the minimum $C_p = -3$ sits at the shoulders. Ideal flow predicts zero drag, which real flow (with separation) breaks")]),
        L("D", "Use the Joukowski map.", "z = ζ + a²/ζ maps the circle |ζ| = a onto a flat plate from −2a to 2a.", ["FM8.4"], [
            Q("fm-joukowski", "fm.external", "The Joukowski map $z = \\zeta + {{a}}^2/\\zeta$ sends the circle $|\\zeta| = {{a}}$ to a straight segment. How long is it?",
              given={"a": {"pick": [0.5, 1, 2, 3]}}, value="4*a", tex="\\ell", tol=0.0001,
              verify="2*re(nsimplify(a) + nsimplify(a)**2/nsimplify(a))", explain="On the circle $\\zeta = ae^{i\\theta}$, so $z = 2a\\cos\\theta$. Shifted circles map to airfoil shapes")]),
        L("E", "Use thin-airfoil theory.", "c_l = 2πα (α in radians) for a thin symmetric airfoil.", ["FM8.5"], [
            Q("fm-thin-airfoil", "fm.external", "A thin symmetric airfoil is at {{a}}° angle of attack. What lift coefficient does thin-airfoil theory predict?",
              given={"a": {"pick": [2, 4, 5, 8]}}, value="2*pi*a*pi/180", tex="c_l", tol=0.0001,
              verify="2*pi*a*pi/180", explain="Lift grows linearly with angle until the flow separates (stall, typically 12–16°)")]),
        L("F", "Use the potential flow past a sphere.", "The surface speed peaks at 1.5U at the equator.", ["FM8.6"], [
            Q("fm-sphere-speed", "fm.external", "In ideal flow past a sphere with free-stream speed {{U}} m/s, what is the fastest speed on the surface, in m/s?",
              given={"U": {"pick": [2, 5, 10, 20]}}, value="1.5*U", tex="V_{max}", tol=0.0001,
              verify="Rational(3, 2)*U*sin(pi/2)", explain="A sphere disturbs the flow less than a cylinder (3D lets fluid go around in two directions): $1.5U$ against the cylinder's $2U$")]),
    ]),
    ("Compressible flow", [
        L("A", "Find a stagnation temperature.", "T₀ = T(1 + (k − 1)M²/2).", ["FM9.2"], [
            Q("fm-stagnation-temperature", "fm.compressible", "Air ($k = 1.4$) flows at Mach {{M}} with static temperature {{T}} K. What is its stagnation temperature, in K?",
              given={"M": {"pick": [0.5, 1, 2, 3]}, "T": {"pick": [220, 250, 300]}}, value="T*(1 + 0.2*M^2)", tex="T_0", tol=0.0001,
              verify="T + (nsimplify(M)*sqrt(Rational(7, 5)*287*T))**2/(2*1004.5)", explain="Bring the flow to rest adiabatically: $c_pT_0 = c_pT + V^2/2$. Re-entry heating is this effect at large Mach")]),
        L("B", "Use the area–Mach relation.", "A/A* = (1/M)[(2/(k+1))(1 + (k−1)M²/2)]^((k+1)/(2(k−1))).", ["FM9.3"], [
            Q("fm-area-mach", "fm.compressible", "Air ($k = 1.4$) flows isentropically. What area ratio $A/A^*$ gives Mach {{M}}?",
              given={"M": {"pick": [0.3, 0.5, 2, 3]}}, value="(1/M)*((2/2.4)*(1 + 0.2*M^2))^3", tex="A/A^*", tol=0.0001,
              verify="(1/nsimplify(M))*(Rational(5, 6)*(1 + nsimplify(M)**2/5))**3", explain="Subsonic flow speeds up in a converging duct, supersonic in a diverging one; both meet $A/A^* = 1$ at the throat")]),
        L("C", "Find the choking pressure ratio of a nozzle.", "P*/P₀ = (2/(k+1))^(k/(k−1)).", ["FM9.4"], [
            Q("fm-critical-pressure", "fm.compressible", "A converging nozzle fed from a tank at {{P0}} kPa discharges air ($k = 1.4$). Below what back pressure is it choked, in kPa?",
              given={"P0": {"pick": [200, 300, 500, 1000]}}, value="P0*(2/2.4)^3.5", tex="P^*", tol=0.0001,
              verify="P0*(1/(1 + Rational(1, 5)))**Rational(7, 2)", explain="At the throat $M = 1$; lowering the back pressure further cannot raise the mass flow")]),
        L("D", "Find the Mach number behind a normal shock.", "M₂² = (1 + (k−1)M₁²/2)/(kM₁² − (k−1)/2).", ["FM9.5"], [
            Q("fm-normal-shock", "fm.compressible", "A normal shock stands in air ($k = 1.4$) with upstream Mach {{M}}. What is the downstream Mach number?",
              given={"M": {"pick": [1.5, 2, 2.5, 3]}}, value="sqrt((1 + 0.2*M^2)/(1.4*M^2 - 0.2))", tex="M_2", tol=0.0001,
              verify="sqrt((1 + nsimplify(M)**2/5)/(Rational(7, 5)*nsimplify(M)**2 - Rational(1, 5)))", explain="A normal shock always leaves subsonic flow, with a jump in pressure and a loss of stagnation pressure")]),
        L("E", "Find a Mach angle.", "sin μ = 1/M: the weakest oblique wave.", ["FM9.6"], [
            Q("fm-mach-angle", "fm.compressible", "A supersonic projectile flies at Mach {{M}}. What is the half-angle of its Mach cone, in degrees?",
              given={"M": {"pick": [1.5, 2, 3, 5]}}, value="asin(1/M)*180/pi", tex="\\mu", tol=0.0001, verify="asin(1/nsimplify(M))*180/pi",
              explain="Disturbances spread at the speed of sound while the source outruns them; oblique shocks lie at steeper angles than μ")]),
        L("F", "Evaluate the Prandtl–Meyer function.", "ν(M) = √((k+1)/(k−1)) atan√((k−1)(M²−1)/(k+1)) − atan√(M²−1).", ["FM9.7"], [
            Q("fm-prandtl-meyer", "fm.compressible", "For air ($k = 1.4$), what is the Prandtl–Meyer angle $\\nu$ at Mach {{M}}, in degrees?",
              given={"M": {"pick": [1.5, 2, 2.5, 3]}}, value="(sqrt(6)*atan(sqrt((M^2 - 1)/6)) - atan(sqrt(M^2 - 1)))*180/pi", tex="\\nu", tol=0.0001,
              verify="(sqrt(6)*atan(sqrt((nsimplify(M)**2 - 1)/6)) - atan(sqrt(nsimplify(M)**2 - 1)))*180/pi",
              explain="Turning a supersonic flow away from itself by an angle θ raises ν by θ; read the new Mach number from ν")]),
        L("G", "Use Fanno flow (adiabatic duct with friction).", "4f̄L*/D = (1 − M²)/(kM²) + ((k+1)/(2k)) ln[(k+1)M²/(2 + (k−1)M²)].", ["FM9.8"], [
            Q("fm-fanno", "fm.compressible", "Air ($k = 1.4$) enters an adiabatic duct at Mach {{M}}. Find $\\bar f L^*/D$ (Darcy $\\bar f$), the friction length to choke.",
              given={"M": {"pick": [0.2, 0.3, 0.5, 2]}}, value="(1 - M^2)/(1.4*M^2) + (2.4/2.8)*log(2.4*M^2/(2 + 0.4*M^2))", tex="\\bar fL^*/D", tol=0.0001,
              verify="(1 - nsimplify(M)**2)/(Rational(7, 5)*nsimplify(M)**2) + Rational(6, 7)*log(Rational(12, 5)*nsimplify(M)**2/(2 + Rational(2, 5)*nsimplify(M)**2))",
              explain="Friction drives both subsonic and supersonic Fanno flow toward Mach 1; a longer duct than $L^*$ reduces the flow rate instead")]),
        L("H", "Use Rayleigh flow (frictionless duct with heat transfer).", "T₀/T₀* = 2(k+1)M²(1 + (k−1)M²/2)/(1 + kM²)².", ["FM9.9"], [
            Q("fm-rayleigh", "fm.compressible", "Air ($k = 1.4$) flows at Mach {{M}} in a frictionless duct. What is $T_0/T_0^*$, the fraction of the stagnation temperature at which heating would choke it?",
              given={"M": {"pick": [0.2, 0.4, 0.6, 2]}}, value="2*2.4*M^2*(1 + 0.2*M^2)/(1 + 1.4*M^2)^2", tex="T_0/T_0^*", tol=0.0001,
              verify="Rational(24, 5)*nsimplify(M)**2*(1 + nsimplify(M)**2/5)/(1 + Rational(7, 5)*nsimplify(M)**2)**2",
              explain="Adding heat drives the flow toward Mach 1 from either side; the most heat that can be added without choking raises $T_0$ to $T_0^*$")]),
    ]),
]),
U(13, "open-channel", "Open-channel flow and turbines", [
    ("Open channels", [
        L("A", "Find the critical depth of a rectangular channel.", "y_c = (q²/g)^(1/3) with q the flow per unit width.", ["FM10.1"], [
            Q("fm-critical-depth", "fm.energy", "A rectangular channel carries {{q}} m²/s per metre of width. What is the critical depth, in m? ($g = 9.81$)",
              given={"q": {"pick": [1, 2, 5, 10]}}, value="(q^2/9.81)^(1/3)", tex="y_c", tol=0.0001,
              verify=f"solve(Eq(diff(x + q**2/(2*{G}*x**2), x), 0), x)[0]", explain="Critical depth minimises the specific energy $E = y + q^2/2gy^2$; there $Fr = 1$")]),
        L("B", "Find uniform-flow velocity with Manning's equation.", "V = (1/n) R^(2/3) S^(1/2) (SI); Chézy V = C√(RS).", ["FM10.2"], [
            Q("fm-manning", "fm.energy", "A concrete channel ($n = 0.013$) has hydraulic radius {{R}} m and slope {{S}}. What is the uniform-flow velocity, in m/s?",
              given={"R": {"pick": [0.5, 1, 1.5]}, "S": {"pick": [0.0005, 0.001, 0.002]}}, value="R^(2/3)*sqrt(S)/0.013", tex="V", tol=0.0001,
              verify="nsimplify(R)**Rational(2, 3)*sqrt(nsimplify(S))/Rational(13, 1000)", explain="Gravity along the slope balances wall friction; Manning's $n$ is an empirical roughness")]),
        L("C", "Find the most efficient rectangular section.", "For a given area, the best rectangle is twice as wide as deep: R = y/2.", ["FM10.3"], [
            Q("fm-best-section", "fm.energy", "A rectangular channel must carry flow area {{A}} m². For the smallest wetted perimeter, what depth should it have, in m?",
              given={"A": {"pick": [2, 4.5, 8, 12.5]}}, value="sqrt(A/2)", tex="y", tol=0.0001,
              verify="Max(*solve(diff(nsimplify(A)/x + 2*x, x), x))", explain="Minimise $P = b + 2y$ with $b = A/y$: $b = 2y$. The least perimeter means the least friction and lining")]),
        L("D", "Read the slope of a gradually varied flow profile.", "dy/dx = (S₀ − S_f)/(1 − Fr²).", ["FM10.4"], [
            Q("fm-gradually-varied", "fm.energy", "In a gradually varied flow, $S_0 = {{S0}}$, the friction slope is $S_f = {{Sf}}$ and $Fr = {{Fr}}$. What is $dy/dx$?",
              given={"S0": {"pick": [0.001, 0.002]}, "Sf": {"pick": [0.0005, 0.003, 0.004]}, "Fr": {"pick": [0.4, 0.6, 1.5]}}, value="(S0 - Sf)/(1 - Fr^2)", tex="dy/dx", tol=0.0001,
              verify="(nsimplify(S0) - nsimplify(Sf))/(1 - nsimplify(Fr)**2)", explain="The sign tells whether the depth grows or falls downstream; it flips between subcritical and supercritical flow")]),
        L("E", "Find the depth after a hydraulic jump.", "y₂/y₁ = ½(−1 + √(1 + 8Fr₁²)).", ["FM10.5"], [
            Q("fm-hydraulic-jump", "fm.momentum", "Supercritical flow {{y1}} m deep with $Fr_1 = {{Fr}}$ jumps to subcritical. What is the depth after the jump, in m?",
              given={"y1": {"pick": [0.2, 0.3, 0.5]}, "Fr": {"pick": [2, 3, 4, 5]}}, value="y1/2*(-1 + sqrt(1 + 8*Fr^2))", tex="y_2", tol=0.0001,
              verify="Max(*solve(Eq(x**2 + nsimplify(y1)*x - 2*nsimplify(y1)**2*nsimplify(Fr)**2, 0), x))",
              explain="Momentum, not energy, is conserved across the jump; the turbulence dissipates the difference")]),
    ]),
    ("Turbines", [
        L("A", "Find the power of a hydraulic turbine.", "P = ηρgQH; a Pelton wheel works best with buckets at half the jet speed.", ["FM11.4"], [
            Q("fm-turbine-power", "fm.energy", "A hydro plant passes {{Q}} m³/s through a head of {{H}} m at overall efficiency {{eta}}. What is the power, in MW? ($\\rho g = 9810$ N/m³)",
              given={"Q": {"pick": [5, 10, 50]}, "H": {"pick": [20, 50, 100]}, "eta": {"pick": [0.85, 0.9]}}, value="eta*9810*Q*H/1000000", tex="P", tol=0.0001,
              verify="integrate(nsimplify(eta)*9810*Q, (x, 0, H))/1000000", explain="Water power $\\rho gQH$ times efficiency. High head and low flow suit Pelton wheels; low head and high flow suit Kaplan turbines")]),
    ]),
]),
]
