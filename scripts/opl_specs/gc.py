"""Graduate Chemical Engineering Core (GC): the UCI CBE graduate core by catalogue topic (uci-cbe-core).
Cards use the textbook closed forms; tests/verify/gccalc.py goes back to the governing equation (velocity
profiles from the ODE then integrated, complex potentials, numerical equations of state, diffusion-reaction
ODEs with their boundary conditions, step responses, characteristic equations on the imaginary axis)."""
import mpmath as mp

from opl_dsl import Q, L, U

FW, FILE, IDEA = "GC", "gc-core", "SOLVE"
S = lambda c: [f"uci-cbe-core:{c}"]

mp.mp.dps = 30
_R = mp.mpf("8.314462618")


def _pr(Tc, Pc, w, T, P, vap):
    Tc, Pc, w, T, P = (mp.mpf(str(v)) for v in (Tc, Pc, w, T, P))
    k = mp.mpf("0.37464") + mp.mpf("1.54226") * w - mp.mpf("0.26992") * w**2
    al = (1 + k * (1 - mp.sqrt(T / Tc))) ** 2
    a = mp.mpf("0.45724") * _R**2 * Tc**2 / Pc * al
    b = mp.mpf("0.07780") * _R * Tc / Pc
    A, B = a * P / (_R * T) ** 2, b * P / (_R * T)
    roots = [mp.re(r) for r in mp.polyroots([1, -(1 - B), A - 3 * B**2 - 2 * B, -(A * B - B**2 - B**3)]) if abs(mp.im(r)) < 1e-20]
    return float(max(roots) if vap else min(roots))


PR = []
for nm, Tc, Pc, w, T, P, vap in (("CO₂", 304.13, 7.377e6, 0.224, 300, 2e6, 1), ("methane", 190.56, 4.599e6, 0.011, 250, 5e6, 1),
                                  ("nitrogen", 126.2, 3.398e6, 0.037, 150, 2e6, 1), ("propane", 369.83, 4.248e6, 0.152, 300, 0.8e6, 1),
                                  ("propane", 369.83, 4.248e6, 0.152, 300, 2e6, 0), ("ammonia", 405.4, 11.333e6, 0.253, 300, 1.5e6, 1)):
    PR.append({"sp": nm, "Tc": Tc, "Pcm": Pc / 1e6, "om": w, "T": T, "Pm": P / 1e6, "vap": vap, "ph": "vapour" if vap else "liquid", "zz": _pr(Tc, Pc, w, T, P, vap)})

FOP = []
for tau in (1, 5, 10):
    for th in (0.5, 1, 2):
        f = lambda w: mp.atan(w * tau) + w * th - mp.pi
        lo, hi = mp.mpf("1e-9"), mp.pi / th
        for _ in range(200):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if f(m) < 0 else (lo, m)
        FOP.append({"tau": tau, "th": th, "wu": float((lo + hi) / 2)})

UNITS = [
U(1, "gc-momentum", "Momentum transport (CBE 220B)", [("Viscous, creeping and inviscid flow", [
    L("A", "Find the flow rate in an annulus from the Navier–Stokes equation in cylindrical coordinates.", "Solve (1/r)(r v′)′ = −(ΔP/L)/μ with no slip on both walls.", [], [
        Q("gc-annulus-flow", "fm.viscous", "Water ($\\mu = {{mu}}$ mPa·s) flows under a pressure gradient of {{G}} Pa/m through the annulus between a rod of radius {{k}}R and a pipe of radius R = {{Rc}} cm. What is the volumetric flow rate, in mL/s?",
          given={"mu": {"pick": [0.89, 1.0]}, "G": {"pick": [50, 100, 200]}, "k": {"pick": [0.25, 0.5, 0.75]}, "Rc": {"pick": [1, 2]}},
          value="pi*G*(Rc/100)^4/(8*mu/1000)*((1 - k^4) - (1 - k^2)^2/log(1/k))*1e6", tex="Q", verify="gc_annulus_Q(G, mu/1000, Rc/100, k)*10**6",
          explain="The profile is $v = \\frac{GR^2}{4\\mu}[1 - (r/R)^2 + (1-\\kappa^2)\\ln(r/R)/\\ln(1/\\kappa)]$; integrating $2\\pi r v$ gives the bracket in the BSL result. As κ → 0 it tends to Hagen–Poiseuille")], std=S("220B")),
    L("B", "Find the torque in circular Couette flow.", "v_θ = Ar + B/r; the torque on the inner cylinder is 4πμΩκ²R²/(1 − κ²) per unit length.", [], [
        Q("gc-couette-torque", "fm.viscous", "A cylinder of radius {{k}}R turns at {{Om}} rad/s inside a fixed cylinder of radius R = {{Rc}} cm, with oil of viscosity {{mu}} Pa·s between them. What torque per metre of length, in mN·m/m, keeps it turning?",
          given={"k": {"pick": [0.8, 0.9, 0.95]}, "Om": {"pick": [10, 20, 50]}, "Rc": {"pick": [2, 5]}, "mu": {"pick": [0.1, 0.5]}},
          value="4*pi*mu*Om*k^2*(Rc/100)^2/(1 - k^2)*1000", tex="\\mathcal{T}", verify="gc_couette_torque(mu, Om, Rc/100, k)*1000",
          explain="Only $A r + B/r$ satisfies the θ-momentum equation; the shear $\\tau_{r\\theta} = -\\mu r\\,d(v_\\theta/r)/dr$ comes from the $B/r$ part alone. A rigid rotation ($Ar$) carries no stress")], std=S("220B")),
    L("C", "Find the force in a squeeze film from lubrication theory.", "Thin gap: p(r) = 3μV(R² − r²)/h³; F = 3πμVR⁴/(2h³).", [], [
        Q("gc-squeeze-film", "fm.viscous", "Two discs of radius {{Rc}} cm approach at {{V}} mm/s with a {{h}} μm film of oil ($\\mu$ = {{mu}} Pa·s) between them. What force, in N, resists the motion?",
          given={"Rc": {"pick": [1, 2, 3]}, "V": {"pick": [0.1, 0.5, 1]}, "h": {"pick": [50, 100, 200]}, "mu": {"pick": [0.05, 0.2]}},
          value="3*pi*mu*(V/1000)*(Rc/100)^4/(2*(h*1e-6)^3)", tex="F", verify="gc_squeeze(mu, V/1000, Rc/100, h/10**6)",
          explain="The gap enters as h⁻³: halving it multiplies the force by eight, which is why squeeze films cushion so well and why joints and bearings stay lubricated")], std=S("220B")),
    L("D", "Find the friction drag of a laminar boundary layer.", "Blasius: local τ_w = 0.332ρU²/√Re_x; average C_f = 1.328/√Re_L.", [], [
        Q("gc-blasius-drag", "fm.external", "Air ($\\rho$ = 1.2 kg/m³, $\\nu = 1.5\\times10^{-5}$ m²/s) flows at {{U}} m/s along a flat plate {{L}} m long. What is the friction drag on one side per metre of width, in mN? (Flow stays laminar.)",
          given={"U": {"pick": [1, 2, 5]}, "L": {"pick": [0.2, 0.5, 1]}}, require=["U*L/1.5e-5 < 5e5"],
          value="0.5*1.2*U^2*L*1.328/sqrt(U*L/1.5e-5)*1000", tex="F", verify="gc_blasius_drag(Rational(12, 10), U, L, Rational(15, 10**6))*1000",
          explain="The wall stress falls as $x^{-1/2}$ because the layer thickens as $\\sqrt{x}$; integrating doubles the local coefficient 0.664 to 1.328")], std=S("220B")),
    L("E", "Find the pressure on a cylinder in potential flow.", "Surface speed 2U sin θ, so C_p = 1 − 4 sin²θ.", [], [
        Q("gc-cylinder-cp", "fm.external", "In inviscid flow past a circular cylinder, what is the pressure coefficient $C_p$ at {{th}}° from the front stagnation point?",
          given={"th": {"pick": [0, 30, 45, 60, 90, 120, 150]}}, value="1 - 4*sin(th*pi/180)^2", tex="C_p", verify="gc_cylinder_cp(th)",
          explain="From $w = U(z + a^2/z)$. $C_p$ = 1 at the stagnation points, −3 at the shoulders, and symmetric front to back, so the net drag is zero (d'Alembert)")], std=S("220B")),
    L("F", "Find the flow rate of a power-law fluid in a tube.", "Q = πR³ n/(3n + 1) (ΔP R/(2mL))^{1/n}.", [], [
        Q("gc-power-law-tube", "fm.viscous", "A power-law fluid (m = {{m}} Pa·sⁿ, n = {{n}}) flows through a tube of radius {{Rc}} mm under ΔP/L = {{G}} kPa/m. What is the flow rate, in mL/s?",
          given={"m": {"pick": [0.5, 2, 5]}, "n": {"pick": [0.4, 0.5, 0.8, 1]}, "Rc": {"pick": [2, 5]}, "G": {"pick": [5, 20, 50]}},
          value="pi*(Rc/1000)^3*n/(3*n + 1)*((G*1000)*(Rc/1000)/(2*m))^(1/n)*1e6", tex="Q", verify="gc_power_law_Q(G*1000, 1, m, n, Rc/1000)*10**6",
          explain="Shear stress is linear in r whatever the fluid; a shear-thinning fluid (n < 1) has a blunter profile and a flow rate that rises faster than linearly with pressure")], std=S("220B")),
    L("G", "Find the start-up time of viscous flow.", "The slowest mode of Couette start-up decays as exp(−π²νt/h²).", [], [
        Q("gc-startup-time", "fm.viscous", "One plate of a {{h}} mm gap filled with {{fl}} ($\\nu$ = {{nu}} mm²/s) starts moving suddenly. How long, in s, until the slowest transient term has decayed to 1% of its initial size?",
          cases=[{"fl": "water", "nu": 1.0}, {"fl": "glycerol", "nu": 1100}, {"fl": "light oil", "nu": 50}], given={"h": {"pick": [1, 5, 10]}},
          value="(h/1000)^2*log(100)/(pi^2*nu*1e-6)", tex="t", verify="log(100)/(pi**2*nsimplify(nu)/10**6/(Rational(h, 1000))**2)",
          explain="Momentum diffuses with ν, so the time scale is $h^2/\\nu$; viscous fluids reach steady flow faster, not slower")], std=S("220B")),
    L("H", "Use the turbulent log law.", "u⁺ = (1/0.41) ln y⁺ + 5.0, with u* = √(τ_w/ρ) and y⁺ = y u*/ν.", [], [
        Q("gc-log-law", "fm.similarity", "In turbulent water flow ($\\rho$ = 1000 kg/m³, $\\nu = 10^{-6}$ m²/s) the wall stress is {{tw}} Pa. What is the mean velocity {{y}} mm from the wall, in m/s?",
          given={"tw": {"pick": [1, 5, 20]}, "y": {"pick": [1, 5, 20]}}, require=["y/1000*sqrt(tw/1000)/1e-6 > 30"],
          value="sqrt(tw/1000)*(log(y/1000*sqrt(tw/1000)/1e-6)/0.41 + 5.0)", tex="u", verify="solve(Eq(x/sqrt(nsimplify(tw)/1000), log(Rational(y, 1000)*sqrt(nsimplify(tw)/1000)*10**6)/Rational(41, 100) + 5), x)[0]",
          explain="Check y⁺ > 30 before using the log law; nearer the wall (y⁺ < 5) the viscous sublayer has u⁺ = y⁺")], std=S("220B")),
    L("I", "Compare the fall of a drop with that of a rigid sphere.", "Hadamard–Rybczynski: drag 2πμaU(2 + 3λ)/(1 + λ), λ = μ_drop/μ.", [], [
        Q("gc-drop-drag", "fm.external", "A drop with viscosity ratio λ = {{lam}} (drop to surrounding fluid) settles in creeping flow. By what factor is its terminal velocity higher than a rigid sphere of the same size and density?",
          given={"lam": {"pick": [0, 0.01, 0.5, 1, 5]}}, value="3*(1 + lam)/(2 + 3*lam)", tex="U/U_s", verify="6*pi/(2*pi*(2 + 3*nsimplify(lam))/(1 + nsimplify(lam)))",
          explain="Internal circulation lets the interface move, cutting drag; a gas bubble (λ = 0) falls 1.5 times faster. Traces of surfactant immobilise the surface and bring it back to Stokes")], std=S("220B")),
])]),
U(2, "gc-transport", "Heat and mass transport (CBE 220A)", [("Scaling, unsteady and convective transport", [
    L("A", "Find the Taylor dispersion coefficient.", "K = D + U²a²/(48D) for laminar flow in a tube of radius a.", [], [
        Q("gc-taylor-dispersion", "mass.unsteady", "A solute (D = {{Dm}} × 10⁻⁹ m²/s) is carried at mean speed U through a capillary of radius {{a}} μm. At what U, in mm/s, does Taylor dispersion double the effective diffusivity?",
          given={"Dm": {"pick": [0.5, 1, 2]}, "a": {"pick": [50, 100, 250]}}, value="sqrt(48)*Dm*1e-9/(a*1e-6)*1000", tex="U",
          verify="Max(*solve(Eq(nsimplify(Dm)/10**9 + (x/1000)**2*(Rational(a, 10**6))**2/(48*nsimplify(Dm)/10**9), 2*nsimplify(Dm)/10**9), x))",
          explain="Shear spreads the solute along the tube and radial diffusion evens it out, so faster diffusion means less dispersion: K grows as 1/D")], std=S("220A")),
    L("B", "Find the temperature rise from viscous heating.", "Couette flow with both walls at T₀: ΔT_max = μV²/(8k).", [], [
        Q("gc-brinkman", "ht.heat-equation", "A lubricant ($\\mu$ = {{mu}} Pa·s, k = {{k}} W/m·K) is sheared in a {{h}} mm gap by a wall moving at {{V}} m/s; both walls are held at the same temperature. What is the maximum temperature rise, in K?",
          given={"mu": {"pick": [0.1, 0.5, 1]}, "k": {"pick": [0.13, 0.15]}, "h": {"pick": [0.5, 1]}, "V": {"pick": [2, 5, 10]}},
          value="mu*V^2/(8*k)", tex="\\Delta T", verify="gc_brinkman(mu, V, h/1000, k)",
          explain="The gap cancels: dissipation μ(V/h)² over a conduction length h². The Brinkman number μV²/(kΔT) says when viscous heating matters")], std=S("220A")),
    L("C", "Find a freezing time from the quasi-steady Stefan problem.", "ρL dδ/dt = kΔT/δ, so δ = √(2kΔT t/(ρL)).", [], [
        Q("gc-stefan-freeze", "ht.semi-infinite", "Water at 0 °C freezes onto a plate held at {{dT}} °C below freezing. Ice: k = 2.2 W/m·K, ρ = 917 kg/m³, L = 334 kJ/kg. How long, in minutes, until the ice is {{d}} mm thick? (Neglect the ice's sensible heat.)",
          given={"dT": {"pick": [5, 10, 20]}, "d": {"pick": [2, 5, 10]}}, value="917*334000*(d/1000)^2/(2*2.2*dT)/60", tex="t",
          verify="integrate(917*334000*Symbol('q')/(Rational(22, 10)*dT), (Symbol('q'), 0, Rational(d, 1000)))/60",
          explain="Time grows as thickness squared: the ice it has already made insulates the front. Fine when the Stefan number cΔT/L is small")], std=S("220A")),
    L("D", "Find the diffusion coefficient of a salt (ambipolar diffusion).", "Zero current couples the ions: D = 2D₊D₋/(D₊ + D₋) for a 1:1 salt.", [], [
        Q("gc-ambipolar", "mass.diffusivity", "Ion diffusivities (10⁻⁹ m²/s): {{ion1}} {{dp}}, {{ion2}} {{dm}}. What is the diffusion coefficient of dilute {{salt}} in water, in 10⁻⁹ m²/s?",
          cases=[{"salt": "NaCl", "ion1": "Na⁺", "ion2": "Cl⁻", "dp": 1.334, "dm": 2.032}, {"salt": "HCl", "ion1": "H⁺", "ion2": "Cl⁻", "dp": 9.31, "dm": 2.032},
                 {"salt": "KCl", "ion1": "K⁺", "ion2": "Cl⁻", "dp": 1.957, "dm": 2.032}, {"salt": "NaOH", "ion1": "Na⁺", "ion2": "OH⁻", "dp": 1.334, "dm": 5.27}],
          value="2*dp*dm/(dp + dm)", tex="D", verify="nsimplify(dp)*(1 + solve(Eq(nsimplify(dp)*(1 + x), nsimplify(dm)*(1 - x)), x)[0])",
          explain="The fast ion runs ahead and sets up a field that drags the slow one and holds itself back; the pair moves at a harmonic mean, close to the slower ion")], std=S("220A")),
    L("E", "Find a flux with a surface reaction that changes the moles.", "For A → 2B at a catalytic surface, N_B = −2N_A, so N_A = (cD/δ) ln(1 + y_A0).", [], [
        Q("gc-film-reaction-flux", "mass.steady", "Gas A diffuses through a {{dl}} mm film to a catalyst where it reacts instantly by A → 2B. With c = {{c}} mol/m³, D = {{Dm}} × 10⁻⁵ m²/s and bulk mole fraction y_A = {{y}}, what is the flux of A, in mol/(m²·s)?",
          given={"dl": {"pick": [0.5, 1, 2]}, "c": {"pick": [40, 41]}, "Dm": {"pick": [1, 2]}, "y": {"pick": [0.1, 0.3, 0.6, 0.9]}},
          value="c*Dm*1e-5/(dl/1000)*log(1 + y)", tex="N_A", verify="c*nsimplify(Dm)/10**5/(Rational(dl, 1000))*integrate(1/(1 + Symbol('q')), (Symbol('q'), 0, nsimplify(y)))",
          explain="The B flowing back opposes the A: N_A(1 + y_A) = −cD dy_A/dz. Compare stagnant B, where the factor is 1/(1 − y_A) and the flux is larger")], std=S("220A")),
    L("F", "Find an average mass-transfer coefficient on a flat plate.", "Local Sh_x = 0.332 Re_x^{1/2} Sc^{1/3}; the plate average is twice the local value at the end.", [], [
        Q("gc-plate-mass", "mass.interphase", "Naphthalene sublimes from a plate {{L}} cm long into air at {{U}} m/s ($\\nu = 1.5\\times10^{-5}$ m²/s, D = 6.1 × 10⁻⁶ m²/s, laminar). What is the average mass-transfer coefficient, in mm/s?",
          given={"L": {"pick": [5, 10, 20]}, "U": {"pick": [1, 2, 4]}},
          value="0.664*sqrt(U*L/100/1.5e-5)*(1.5e-5/6.1e-6)^(1/3)*6.1e-6/(L/100)*1000", tex="\\bar k_c",
          verify="integrate(Rational(332, 1000)*sqrt(U*Symbol('q', positive=True)/Rational(15, 10**6))*(Rational(15, 10**6)/Rational(61, 10**7))**Rational(1, 3)*Rational(61, 10**7)/Symbol('q', positive=True), (Symbol('q', positive=True), 0, Rational(L, 100)))/Rational(L, 100)*1000",
          explain="The heat–mass analogy: Sc replaces Pr. The local coefficient falls as $x^{-1/2}$, so the leading edge does most of the transfer")], std=S("220A")),
])]),
U(3, "gc-thermo", "Advanced thermodynamics (CBE 240)", [("Equations of state, mixtures and equilibria", [
    L("A", "Find a van der Waals critical temperature from its constants.", "dP/dV = d²P/dV² = 0 gives T_c = 8a/(27Rb).", [], [
        Q("gc-vdw-critical", "thermo.stability", "{{g}} has van der Waals constants a = {{a}} Pa·m⁶/mol² and b = {{b}} × 10⁻⁵ m³/mol. What critical temperature does the equation predict, in K? ($R = 8.314$)",
          cases=[{"g": "CO₂", "a": 0.3640, "b": 4.267}, {"g": "Methane", "a": 0.2283, "b": 4.278}, {"g": "Water", "a": 0.5536, "b": 3.049}, {"g": "Nitrogen", "a": 0.1370, "b": 3.870}],
          value="8*a/(27*8.314*b*1e-5)", tex="T_c", verify="gc_vdw_tc(a, b/10**5, Rational(8314, 1000))",
          explain="The critical point is where the isotherm's maximum and minimum merge into an inflection. vdW gets $T_c$ roughly right but predicts $Z_c$ = 0.375, well above real fluids' ≈ 0.27–0.29")], std=S("240")),
    L("B", "Find a compressibility factor from the Peng–Robinson equation.", "Solve the cubic in Z; take the largest root for vapour, the smallest for liquid.", [], [
        Q("gc-peng-robinson-z", "thermo.stability", "Using the Peng–Robinson equation, find Z for {{sp}} {{ph}} at {{T}} K and {{Pm}} MPa ($T_c$ = {{Tc}} K, $P_c$ = {{Pcm}} MPa, ω = {{om}}).",
          cases=PR, value="zz", tex="Z", verify="gc_pr_z(Tc, Pcm*10**6, om, T, Pm*10**6, vap)",
          explain="$A = aP/(RT)^2$, $B = bP/RT$, with $a$ scaled by α(T, ω). Where there are three real roots, the middle one is unphysical; which of the outer two is stable is decided by fugacity")], std=S("240")),
    L("C", "Decide whether a mixture splits into two liquids.", "One-constant Margules: ∂²(Δg_mix/RT)/∂x₁² = 1/x₁ + 1/x₂ − 2A; negative means unstable.", [], [
        Q("gc-margules-stability", "thermo.stability", "A binary liquid follows $g^E/RT = A x_1 x_2$ with A = {{A}}. Is a mixture at x₁ = {{x1}} stable against splitting into two liquids?",
          given={"A": {"pick": [1.5, 2.2, 2.8, 3.5]}, "x1": {"pick": [0.1, 0.3, 0.5]}}, require=["abs(1/x1 + 1/(1 - x1) - 2*A) > 0.05"],
          choice=["Stable (single phase)", "Unstable (it splits)"], correct="1/x1 + 1/(1 - x1) - 2*A > 0 ? 0 : 1",
          verify="0 if diff(Symbol('q')*log(Symbol('q')) + (1 - Symbol('q'))*log(1 - Symbol('q')) + nsimplify(A)*Symbol('q')*(1 - Symbol('q')), Symbol('q'), 2).subs(Symbol('q'), nsimplify(x1)) > 0 else 1",
          explain="Stability is curvature: Δg_mix must curve upward. The one-constant Margules model first splits at A = 2, at x₁ = ½ (the critical solution point)")], std=S("240")),
    L("D", "Find a residual enthalpy from the virial equation.", "H^R = P(B − T dB/dT) at low pressure.", [], [
        Q("gc-virial-residual-h", "thermo.maxwell", "A gas has B(T) = {{b0}} − {{b1}}/T (cm³/mol, T in K). What is its residual enthalpy $H^R$ at {{T}} K and {{P}} bar, in J/mol?",
          given={"b0": {"pick": [40, 60]}, "b1": {"pick": [20000, 40000]}, "T": {"pick": [300, 400]}, "P": {"pick": [5, 10, 20]}},
          value="P*1e5*((b0 - b1/T) - T*(b1/T^2))*1e-6", tex="H^R",
          verify="-Rational(8314, 1000)*T**2*integrate(diff(1 + (b0 - b1/Symbol('TT'))*Rational(1, 10**6)*Symbol('pp')/(Rational(8314, 1000)*Symbol('TT')), Symbol('TT')).subs(Symbol('TT'), T)/Symbol('pp'), (Symbol('pp'), 0, P*10**5))",
          explain="From $H^R/RT = -T\\int_0^P (\\partial Z/\\partial T)_P\\,dP/P$ with $Z = 1 + BP/RT$. Attractions (negative B) make $H^R$ negative: the real gas holds less enthalpy")], std=S("240")),
    L("E", "Solve simultaneous chemical equilibria.", "Each independent reaction has its own K; solve them together with the mole balance.", [], [
        Q("gc-series-equilibria", "thermo.chemical-equilibrium", "In an ideal liquid, A ⇌ B ($K_1$ = {{k1}}) and B ⇌ C ($K_2$ = {{k2}}) both reach equilibrium. What is the mole fraction of C?",
          given={"k1": {"pick": [0.5, 2, 5]}, "k2": {"pick": [0.2, 1, 3]}}, value="k1*k2/(1 + k1 + k1*k2)", tex="x_C",
          verify="solve([Eq(Symbol('b'), nsimplify(k1)*Symbol('a')), Eq(Symbol('c'), nsimplify(k2)*Symbol('b')), Eq(Symbol('a') + Symbol('b') + Symbol('c'), 1)], [Symbol('a'), Symbol('b'), Symbol('c')])[Symbol('c')]",
          explain="Every species' amount follows from A's through the chain of K's; the mole balance fixes A. With independent reactions the order of writing them does not matter")], std=S("240")),
    L("F", "Integrate the van 't Hoff equation with a heat-capacity change.", "d ln K/dT = ΔH(T)/RT², ΔH(T) = ΔH₀ + ΔCp(T − T₀).", [], [
        Q("gc-vant-hoff-cp", "thermo.chemical-equilibrium", "A reaction has K = {{K0}} at 298.15 K, ΔH° = {{dH}} kJ/mol and ΔCp = {{dCp}} J/(mol·K) (constant). What is K at {{T}} K? ($R = 8.314$)",
          given={"K0": {"pick": [0.01, 1, 50]}, "dH": {"pick": [-40, 20, 60]}, "dCp": {"pick": [-30, 15, 40]}, "T": {"pick": [350, 450, 600]}},
          value="K0*exp((dH*1000 - dCp*298.15)/8.314*(1/298.15 - 1/T) + dCp/8.314*log(T/298.15))", tex="K",
          verify="nsimplify(K0)*exp(integrate((dH*1000 + dCp*(Symbol('TT') - Rational(29815, 100)))/(Rational(8314, 1000)*Symbol('TT')**2), (Symbol('TT'), Rational(29815, 100), T)))",
          explain="With ΔCp ≠ 0, ln K is not linear in 1/T; the extra term is ΔCp[ln(T/T₀) + T₀/T − 1]/R, small over modest ranges")], std=S("240")),
    L("G", "Locate an azeotrope.", "At an azeotrope x = y, so γ₁P₁^sat = γ₂P₂^sat.", [], [
        Q("gc-azeotrope", "thermo.solutions", "A binary follows $g^E/RT = A x_1x_2$ with A = {{A}}; at the temperature of interest $P_1^{sat}/P_2^{sat}$ = {{r}}. At what x₁ is the azeotrope?",
          given={"A": {"pick": [1, 1.5, 2]}, "r": {"pick": [1.1, 1.3, 1.6]}}, require=["log(r)/A < 0.9"], value="(1 + log(r)/A)/2", tex="x_1^{az}",
          verify="solve(Eq(log(nsimplify(r)) + nsimplify(A)*(1 - x)**2 - nsimplify(A)*x**2, 0), x)[0]",
          explain="With ln γ₁ = A x₂² and ln γ₂ = A x₁², the condition is linear in x₁. Positive deviations (A > 0) give a maximum-pressure azeotrope when A exceeds |ln(P₁/P₂)|")], std=S("240")),
])]),
U(4, "gc-reactors", "Reaction engineering (CBE 210)", [("Stability, catalysis, optimisation and dispersed phases", [
    L("A", "Judge the stability of a CSTR steady state by the slope condition.", "Stable when the heat-removal line is steeper than the heat-generation curve: dR/dT > dG/dT.", [], [
        Q("gc-cstr-slope", "cre.nonisothermal", "At a steady state of a first-order exothermic CSTR, $k\\tau$ = {{kt}}, the adiabatic rise $\\Delta T_{ad}$ = {{J}} K, $E_a$ = {{Ea}} kJ/mol and T = {{T}} K. The heat-removal line R(T) has slope {{Rs}} (in G's units). Is the steady state stable?",
          given={"kt": {"pick": [0.2, 1, 4]}, "J": {"pick": [100, 200, 300]}, "Ea": {"pick": [60, 90]}, "T": {"pick": [350, 400]}, "Rs": {"pick": [1, 1.5, 2.5]}},
          require=["abs(J*kt/(1 + kt)^2*Ea*1000/(8.314*T^2) - Rs) > 0.05"],
          choice=["Stable", "Unstable (it moves to another steady state)"], correct="J*kt/(1 + kt)^2*Ea*1000/(8.314*T^2) < Rs ? 0 : 1",
          verify="0 if diff(J*Symbol('kk')/(1 + Symbol('kk')), Symbol('kk')).subs(Symbol('kk'), nsimplify(kt))*nsimplify(kt)*Ea*1000/(Rational(8314, 1000)*T**2) < nsimplify(Rs) else 1",
          explain="G(T) = ΔT_ad·kτ/(1 + kτ), so dG/dT = ΔT_ad·kτ/(1 + kτ)²·E/RT². The middle of three steady states always fails this test")], std=S("210")),
    L("B", "Find the optimum temperature for a reversible exothermic reaction.", "Maximise r = k₁(1 − X) − k₂X at fixed X: T_opt = (E₂ − E₁)/(R ln[A₂E₂X/(A₁E₁(1 − X))]).", [], [
        Q("gc-optimum-temperature", "cre.nonisothermal", "A ⇌ B: forward $A_1$ = {{a1}} s⁻¹, $E_1$ = {{e1}} kJ/mol; reverse $A_2$ = {{a2}} s⁻¹, $E_2$ = {{e2}} kJ/mol. At conversion X = {{X}}, which temperature maximises the net rate, in K? ($R = 8.314$)",
          given={"a1": {"pick": [1e6, 1e7]}, "e1": {"pick": [50, 60]}, "a2": {"pick": [1e12, 1e13]}, "e2": {"pick": [110, 130]}, "X": {"pick": [0.3, 0.5, 0.7]}},
          value="(e2 - e1)*1000/(8.314*log(a2*e2*X/(a1*e1*(1 - X))))", tex="T_{opt}", verify="gc_topt(a1, e1*1000, a2, e2*1000, X)",
          explain="Too cold and the forward rate is slow; too hot and equilibrium pulls X back. The optimum falls as conversion rises, which is why staged reactors cool between beds")], std=S("210")),
    L("C", "Combine internal and external resistances into an overall effectiveness.", "Ω = η/(1 + ηφ²/(3Bi)), η = 3(φ coth φ − 1)/φ² for a first-order sphere.", [], [
        Q("gc-overall-effectiveness", "cre.diffusion", "A first-order reaction runs in spherical pellets with Thiele modulus φ = {{phi}} and mass Biot number $Bi = k_cR/D_e$ = {{Bi}}. What is the overall effectiveness factor Ω (rate over k C_bulk V)?",
          given={"phi": {"pick": [0.5, 2, 5, 10]}, "Bi": {"pick": [1, 10, 100]}},
          value="(3*(phi*coth(phi) - 1)/phi^2)/(1 + (3*(phi*coth(phi) - 1)/phi^2)*phi^2/(3*Bi))", tex="\\Omega", verify="gc_overall_eff(phi, Bi)",
          explain="Resistances in series: the film sets the surface concentration, the pellet works at η of that. Large φ and small Bi together make the film control")], std=S("210")),
    L("D", "Find an enhancement factor for gas absorption with reaction.", "Film theory, pseudo-first order: E = Ha/tanh Ha, Ha = √(kD)/k_L.", [], [
        Q("gc-hatta-enhancement", "cre.diffusion", "A gas dissolves into a liquid where it reacts (pseudo-first order, k = {{k}} s⁻¹, D = {{Dm}} × 10⁻⁹ m²/s, $k_L$ = {{kl}} × 10⁻⁴ m/s). What is the enhancement factor E?",
          given={"k": {"pick": [10, 100, 1000]}, "Dm": {"pick": [1, 2]}, "kl": {"pick": [1, 2, 4]}},
          value="(sqrt(k*Dm*1e-9)/(kl*1e-4))/tanh(sqrt(k*Dm*1e-9)/(kl*1e-4))", tex="E", verify="gc_enhancement(sqrt(k*nsimplify(Dm)/10**9)/(nsimplify(kl)/10**4))",
          explain="Ha < 0.3: slow reaction, bulk liquid matters, E ≈ 1. Ha > 3: reaction finishes inside the film and E ≈ Ha, so the rate no longer depends on k_L")], std=S("210")),
    L("E", "Find the overall rate in a slurry reactor from resistances in series.", "C_gas/r = 1/(k_b a_b) + 1/(k_c a_p) + 1/(η k a_p)-type terms add.", [], [
        Q("gc-slurry-resistances", "cre.diffusion", "In a slurry reactor, the dissolved-gas concentration at saturation is {{ci}} mol/m³. Gas absorption $k_ba_b$ = {{kb}} s⁻¹, liquid-to-particle $k_ca_p$ = {{kc}} s⁻¹ and surface reaction $\\eta k a_p$ = {{kr}} s⁻¹ (all per reactor volume). What is the overall rate, in mol/(m³·s)?",
          given={"ci": {"pick": [5, 10, 20]}, "kb": {"pick": [0.05, 0.2, 1]}, "kc": {"pick": [0.1, 0.5]}, "kr": {"pick": [0.02, 0.1, 0.5]}},
          value="ci/(1/kb + 1/kc + 1/kr)", tex="r",
          verify="solve([Eq(Symbol('rr'), nsimplify(kb)*(ci - Symbol('cb'))), Eq(Symbol('rr'), nsimplify(kc)*(Symbol('cb') - Symbol('cs'))), Eq(Symbol('rr'), nsimplify(kr)*Symbol('cs'))], [Symbol('rr'), Symbol('cb'), Symbol('cs')])[Symbol('rr')]",
          explain="At steady state the same rate crosses every step, so the driving forces add and the resistances add. The largest 1/k term is the one to attack")], std=S("210")),
    L("F", "Find a conversion with a decaying catalyst.", "First-order decay a = e^{−k_d t}: ln[1/(1 − X)] = (k/k_d)(1 − e^{−k_d t}).", [], [
        Q("gc-deactivation", "cre.catalysis", "A batch reaction is first order (k = {{k}} h⁻¹) on a catalyst whose activity decays first order ($k_d$ = {{kd}} h⁻¹). What conversion is reached after {{t}} h?",
          given={"k": {"pick": [0.5, 1, 2]}, "kd": {"pick": [0.1, 0.3, 1]}, "t": {"pick": [1, 3, 10]}},
          value="1 - exp(-(k/kd)*(1 - exp(-kd*t)))", tex="X", verify="1 - exp(-integrate(nsimplify(k)*exp(-nsimplify(kd)*Symbol('tt')), (Symbol('tt'), 0, t)))",
          explain="Conversion levels off at 1 − e^{−k/k_d} however long you wait: once the catalyst is dead, time buys nothing")], std=S("210")),
])]),
U(5, "gc-control", "Process dynamics and control (CBE 200)", [("Responses, stability and tuning", [
    L("A", "Find a time from a first-order step response.", "y = KM(1 − e^{−t/τ}); 63.2% at τ, 95% at 3τ, 99% at 4.6τ.", [], [
        Q("gc-first-order-time", "design.control", "A first-order process with τ = {{tau}} min gets a step input. How long, in minutes, until the output has made {{p}}% of its final change?",
          given={"tau": {"pick": [2, 5, 12]}, "p": {"pick": [50, 90, 95, 99]}}, value="-tau*log(1 - p/100)", tex="t",
          verify="solve(Eq(1 - exp(-x/nsimplify(tau)), Rational(p, 100)), x)[0]", explain="The fraction remaining decays as e^{−t/τ} whatever the gain or the step size")], std=S("200")),
    L("B", "Find the overshoot of an underdamped second-order process.", "OS = exp(−πζ/√(1 − ζ²)), independent of τ.", [], [
        Q("gc-overshoot", "design.control", "A second-order process with damping ratio ζ = {{z}} gets a step. What is its fractional overshoot?",
          given={"z": {"pick": [0.1, 0.2, 0.3, 0.5, 0.7]}}, value="exp(-pi*z/sqrt(1 - z^2))", tex="OS", verify="gc_overshoot(z)",
          explain="Overshoot depends only on ζ; τ stretches time but not height. ζ = 0.5 gives about 16%, a common tuning target")], std=S("200")),
    L("C", "Find the offset under proportional control.", "Final value theorem: setpoint offset = 1/(1 + K K_c) for a first-order process.", [], [
        Q("gc-p-offset", "design.control", "A first-order process (gain K = {{K}}) is under proportional control with $K_c$ = {{Kc}}. After a unit setpoint step, what fraction of the step remains as steady-state offset?",
          given={"K": {"pick": [0.5, 2, 4]}, "Kc": {"pick": [0.5, 2, 5]}}, value="1/(1 + K*Kc)", tex="e_\\infty",
          verify="limit(Symbol('s')*(1 - nsimplify(K)*nsimplify(Kc)/(Symbol('tau')*Symbol('s') + 1)/(1 + nsimplify(K)*nsimplify(Kc)/(Symbol('tau')*Symbol('s') + 1)))/Symbol('s'), Symbol('s'), 0)",
          explain="A proportional controller needs an error to hold any output, so some offset remains; integral action removes it")], std=S("200")),
    L("D", "Find the ultimate gain of a third-order process.", "Substitute s = iω in 1 + K_cG = 0: the imaginary part fixes ω_u, the real part K_c,u.", [], [
        Q("gc-ultimate-gain", "design.control", "A process $G = K/[({{t1}}s + 1)({{t2}}s + 1)({{t3}}s + 1)]$ is under proportional control. Above what loop gain $K K_c$ does the loop go unstable?",
          given={"t1": {"pick": [1, 2]}, "t2": {"pick": [1, 3, 5]}, "t3": {"pick": [1, 4, 10]}},
          value="(t1 + t2 + t3)*(t1*t2 + t1*t3 + t2*t3)/(t1*t2*t3) - 1", tex="(KK_c)_u", verify="gc_ultimate(t1, t2, t3)",
          explain="Routh gives the same: with $a_3s^3 + a_2s^2 + a_1s + 1 + KK_c$, stability needs $a_1a_2 > a_3(1 + KK_c)$. Three equal lags give 8")], std=S("200")),
    L("E", "Find the ultimate period, then a Ziegler–Nichols setting.", "ω_u = √(a₁/a₃); P_u = 2π/ω_u; ZN PI: K_c = 0.45K_cu, τ_I = P_u/1.2.", [], [
        Q("gc-ultimate-period", "design.control", "For $G = K/[({{t1}}s + 1)({{t2}}s + 1)({{t3}}s + 1)]$ (times in min) under proportional control, what is the ultimate period, in minutes? (Ziegler–Nichols would then set the PI reset time to P_u/1.2.)",
          given={"t1": {"pick": [1, 2]}, "t2": {"pick": [1, 3, 5]}, "t3": {"pick": [1, 4, 10]}},
          value="2*pi/sqrt((t1 + t2 + t3)/(t1*t2*t3))", tex="P_u", verify="gc_ultimate_period(t1, t2, t3)",
          explain="At the ultimate gain the loop oscillates steadily at the frequency where the phase lag is 180°")], std=S("200")),
    L("F", "Find an amplitude ratio from the frequency response.", "First order: AR = K/√(1 + ω²τ²), phase −atan(ωτ).", [], [
        Q("gc-amplitude-ratio", "design.control", "A first-order process (K = {{K}}, τ = {{tau}} s) is driven by a sinusoid of {{w}} rad/s. What is the amplitude ratio?",
          given={"K": {"pick": [1, 2.5, 4]}, "tau": {"pick": [1, 5, 20]}, "w": {"pick": [0.05, 0.2, 1]}}, value="K/sqrt(1 + w^2*tau^2)", tex="AR",
          verify="Abs(nsimplify(K)/(I*nsimplify(w)*nsimplify(tau) + 1))", explain="Replace s by iω and take the modulus. Well above the corner frequency 1/τ the process filters the input out")], std=S("200")),
    L("G", "Find the crossover frequency of a first-order-plus-dead-time process.", "Phase −atan(ωτ) − ωθ = −π; no closed form.", [], [
        Q("gc-fopdt-crossover", "design.control", "A process $e^{-{{th}}s}/({{tau}}s + 1)$ (times in min) is under proportional control. At what frequency, in rad/min, is the phase lag 180°?",
          cases=FOP, value="wu", tex="\\omega_u", verify="gc_fopdt_wu(tau, th)",
          explain="Dead time adds lag without lowering the amplitude, so it limits how hard the loop can be pushed: the ultimate gain is $\\sqrt{1 + \\omega_u^2\\tau^2}/K$")], std=S("200")),
])]),
U(6, "gc-separations", "Separations past the McCabe–Thiele diagram", [("Batch distillation and absorption", [
    L("A", "Find what remains in a Rayleigh batch distillation.", "ln(W₀/W) = ∫ dx/(y − x) from x to x₀; with constant α it has a closed form.", [], [
        Q("gc-rayleigh", "sep.distillation", "A still holds a binary with relative volatility α = {{al}} at light-key mole fraction {{x0}}. Simple batch distillation continues until the liquid is at {{x1}}. What fraction of the original charge remains?",
          given={"al": {"pick": [1.5, 2.5, 4]}, "x0": {"pick": [0.5, 0.6]}, "x1": {"pick": [0.1, 0.2, 0.3]}},
          value="exp(-(log(x0/x1) + al*log((1 - x1)/(1 - x0)))/(al - 1))", tex="W/W_0", verify="gc_rayleigh(al, x0, x1)",
          explain="Each bit of vapour leaves richer than the liquid, so the pot strips the light key gradually; a small α needs most of the charge boiled off")], std=["pe-chemical:6.B"]),
    L("B", "Find the minimum absorbent rate.", "(L/G)_min = (y_in − y_out)/(x*_out − x_in), x*_out = y_in/m for a dilute linear system.", [], [
        Q("gc-min-absorbent", "sep.absorption", "A gas with {{yin}}% solute is scrubbed to {{yout}}% with solute-free liquid; equilibrium is y = {{m}}x. What is the minimum L/G?",
          given={"yin": {"pick": [2, 5]}, "yout": {"pick": [0.1, 0.25, 0.5]}, "m": {"pick": [0.5, 1.2, 2]}}, value="(yin - yout)/100/(yin/100/m)", tex="(L/G)_{min}",
          verify="solve(Eq(x*(nsimplify(yin)/100/nsimplify(m)), (nsimplify(yin) - nsimplify(yout))/100), x)[0]",
          explain="At minimum flow the liquid leaving is in equilibrium with the gas entering: a pinch at the rich end and infinitely many stages. Practice uses 1.2–1.5 times the minimum")], std=["pe-chemical:6.B"]),
    L("C", "Find where the feed line meets the rectifying line.", "q-line y = qx/(q − 1) − z/(q − 1); rectifying line y = Rx/(R + 1) + x_D/(R + 1).", [], [
        Q("gc-q-line-intersection", "sep.distillation", "A column runs at reflux ratio R = {{R}} with distillate $x_D$ = {{xd}}. The feed (z = {{z}}) is {{f}}% vapour by moles. At what x do the q-line and the rectifying line cross?",
          given={"R": {"pick": [1.5, 2, 3]}, "xd": {"pick": [0.9, 0.95]}, "z": {"pick": [0.4, 0.5]}, "f": {"pick": [25, 50, 75]}},
          value="(z/(1 - f/100 - 1) + xd/(R + 1))/((1 - f/100)/(1 - f/100 - 1) - R/(R + 1))", tex="x",
          verify="solve(Eq((1 - Rational(f, 100))*x/(-Rational(f, 100)) - nsimplify(z)/(-Rational(f, 100)), nsimplify(R)*x/(nsimplify(R) + 1) + nsimplify(xd)/(nsimplify(R) + 1)), x)[0]",
          explain="q is the liquid fraction of the feed (1 − vapour fraction). Saturated liquid (q = 1) gives a vertical q-line at x = z; saturated vapour a horizontal one at y = z")], std=["pe-chemical:6.B"]),
])]),
]

# ── second question types (Nov 2026), keyed (unit, topic, LO) ───────────────────────────────────────────
SECOND = {
    (1, 1, "A"): Q("gc-annulus-vs-pipe", "fm.viscous", "At the same pressure gradient and outer radius, what fraction of the Hagen–Poiseuille flow passes through an annulus whose inner radius is {{k}}R?",
                   given={"k": {"pick": [0.1, 0.25, 0.5, 0.75]}}, value="(1 - k^4) - (1 - k^2)^2/log(1/k)", tex="Q/Q_{pipe}",
                   verify="gc_annulus_Q(1, 1, 1, k)/(pi/8)", explain="Even a thin rod costs a lot: at κ = 0.1 the no-slip core removes far more than the 1% of area it blocks"),
    (1, 1, "B"): Q("gc-couette-shear-rate", "fm.viscous", "In circular Couette flow (inner cylinder radius {{k}}R turning at {{Om}} rad/s, outer fixed), what is the shear rate at the inner wall, in s⁻¹?",
                   given={"k": {"pick": [0.5, 0.8, 0.9, 0.95]}, "Om": {"pick": [5, 20, 50]}}, value="2*Om/(1 - k^2)", tex="\\dot\\gamma",
                   verify="gc_couette_shear(Om, k)", explain="Narrow gaps approach plane Couette flow, γ̇ ≈ ΩκR/((1 − κ)R); rheometers use them for a nearly uniform shear rate"),
    (1, 1, "C"): Q("gc-squeeze-time", "fm.viscous", "Two discs of radius {{Rc}} cm are pressed together by {{F}} N through oil ($\\mu$ = {{mu}} Pa·s). How long, in s, does the film take to thin from {{h1}} μm to {{h2}} μm?",
                   given={"Rc": {"pick": [1, 2]}, "F": {"pick": [10, 50, 200]}, "mu": {"pick": [0.1, 0.5]}, "h1": {"pick": [100, 50]}, "h2": {"pick": [20, 10]}},
                   value="3*pi*mu*(Rc/100)^4/(4*F)*(1/(h2*1e-6)^2 - 1/(h1*1e-6)^2)", tex="t",
                   verify="integrate(3*pi*nsimplify(mu)*(Rc/100)**4/(2*F)/Symbol('hh')**3, (Symbol('hh'), nsimplify(h2)/10**6, nsimplify(h1)/10**6))",
                   explain="Setting F = 3πμR⁴V/(2h³) with V = −dh/dt and integrating: the film never quite reaches zero thickness in finite force"),
    (1, 1, "D"): Q("gc-blasius-length-scaling", "fm.external", "A laminar flat plate is lengthened by a factor {{f}} at the same speed (still laminar). By what factor does the friction drag rise?",
                   given={"f": {"pick": [2, 4, 9]}}, value="sqrt(f)", tex="F_2/F_1", verify="gc_blasius_drag(1, 1, f, 1)/gc_blasius_drag(1, 1, 1, 1)",
                   explain="The added length sits under a thicker boundary layer with lower wall stress, so drag grows only as √L"),
    (1, 1, "E"): Q("gc-cylinder-pressure-drop", "fm.external", "Air ($\\rho$ = 1.2 kg/m³) flows at {{U}} m/s past a cylinder. In potential flow, how much lower is the pressure at the shoulders (90°) than at the front stagnation point, in Pa?",
                   given={"U": {"pick": [2, 5, 10, 20]}}, value="2*1.2*U^2", tex="\\Delta p", verify="(1 - gc_cylinder_cp(90))*Rational(1, 2)*Rational(12, 10)*U**2",
                   explain="The surface speed doubles at the shoulders, so the dynamic pressure there is four times the free stream's"),
    (1, 1, "F"): Q("gc-apparent-viscosity", "fm.viscous", "A power-law fluid has m = {{m}} Pa·sⁿ and n = {{n}}. What is its apparent viscosity at a shear rate of {{g}} s⁻¹, in Pa·s?",
                   given={"m": {"pick": [0.5, 2, 10]}, "n": {"pick": [0.3, 0.5, 0.8]}, "g": {"pick": [1, 10, 100, 1000]}}, value="m*g^(n - 1)", tex="\\eta",
                   verify="diff(nsimplify(m)*Symbol('gg')**nsimplify(n), Symbol('gg')).subs(Symbol('gg'), g)/nsimplify(n)",
                   explain="η = τ/γ̇ = m γ̇^{n−1}: a shear-thinning fluid (n < 1) is a hundred times thinner at 1000 s⁻¹ than at 1 s⁻¹ when n = 1/3"),
    (1, 1, "G"): Q("gc-stokes-first-problem", "fm.viscous", "A plate in {{fl}} ($\\nu$ = {{nu}} mm²/s) suddenly moves at speed U. What fraction of U has the fluid {{y}} mm away reached after {{t}} s?",
                   cases=[{"fl": "water", "nu": 1.0}, {"fl": "olive oil", "nu": 80}], given={"y": {"pick": [1, 2, 5]}, "t": {"pick": [1, 10, 60]}},
                   value="1 - erf(y/1000/(2*sqrt(nu*1e-6*t)))", tex="u/U", verify="erfc(Rational(y, 1000)/(2*sqrt(nsimplify(nu)/10**6*t)))",
                   explain="Stokes' first problem: momentum diffuses a distance of order √(νt), the same similarity solution as heat into a semi-infinite solid"),
    (1, 1, "H"): Q("gc-wall-region", "fm.similarity", "Water ($\\nu = 10^{-6}$ m²/s) flows with friction velocity {{us}} m/s. In which region of the wall layer is a point {{y}} μm from the wall?",
                   given={"us": {"pick": [0.02, 0.05, 0.1]}, "y": {"pick": [20, 100, 500, 2000]}}, require=["abs(y*1e-6*us/1e-6 - 5) > 0.5", "abs(y*1e-6*us/1e-6 - 30) > 2"],
                   choice=["Viscous sublayer (y⁺ < 5)", "Buffer layer (5 to 30)", "Log layer (y⁺ > 30)"], correct="y*us < 5 ? 0 : (y*us < 30 ? 1 : 2)",
                   verify="0 if Rational(y, 10**6)*nsimplify(us)*10**6 < 5 else (1 if Rational(y, 10**6)*nsimplify(us)*10**6 < 30 else 2)",
                   explain="Wall units y⁺ = yu*/ν decide the region; in the sublayer u⁺ = y⁺, in the log layer the log law, in between neither fits well"),
    (1, 1, "I"): Q("gc-bubble-terminal", "fm.external", "A small air bubble of radius {{a}} μm rises in water ($\\mu$ = 1.0 mPa·s, Δρ = 998 kg/m³). With a clean, mobile surface (Hadamard–Rybczynski, λ = 0), what is its terminal speed, in mm/s?",
                   given={"a": {"pick": [20, 50, 100]}}, value="998*9.81*(a*1e-6)^2/(3*1e-3)*1000", tex="U",
                   verify="solve(Eq(4*pi*Rational(1, 1000)*(Rational(a, 10**6))*x/1000, Rational(4, 3)*pi*(Rational(a, 10**6))**3*998*Rational(981, 100)), x)[0]",
                   explain="Drag 4πμaU instead of 6πμaU: 1.5 times faster than a rigid sphere. Real bubbles in tap water often behave as rigid because surfactants immobilise the surface"),
    (2, 1, "A"): Q("gc-taylor-coefficient", "mass.unsteady", "A solute with D = {{Dm}} × 10⁻⁹ m²/s flows at mean speed {{U}} mm/s through a tube of radius {{a}} μm. What is the Taylor dispersion coefficient, in 10⁻⁹ m²/s?",
                   given={"Dm": {"pick": [0.5, 1]}, "U": {"pick": [0.5, 1, 5]}, "a": {"pick": [50, 100, 250]}}, value="Dm + (U/1000)^2*(a*1e-6)^2/(48*Dm*1e-9)*1e9", tex="K",
                   verify="(nsimplify(Dm)/10**9 + (nsimplify(U)/1000)**2*(Rational(a, 10**6))**2/(48*nsimplify(Dm)/10**9))*10**9",
                   explain="The convective term usually dominates in microchannels: dispersion can exceed molecular diffusion by orders of magnitude"),
    (2, 1, "B"): Q("gc-brinkman-adiabatic", "ht.heat-equation", "A lubricant ($\\mu$ = {{mu}} Pa·s, k = {{k}} W/m·K) is sheared by a wall moving at {{V}} m/s; the stationary wall is at T₀ and the moving wall is insulated. What is the temperature rise at the insulated wall, in K?",
                   given={"mu": {"pick": [0.1, 0.5, 1]}, "k": {"pick": [0.13, 0.15]}, "V": {"pick": [2, 5, 10]}, "h": {"pick": [1]}}, value="mu*V^2/(2*k)", tex="\\Delta T",
                   verify="integrate(integrate(nsimplify(mu)*(V/(nsimplify(h)/1000))**2/nsimplify(k), (Symbol('ss'), Symbol('yy'), nsimplify(h)/1000)), (Symbol('yy'), 0, nsimplify(h)/1000))",
                   explain="With one wall insulated all the dissipated heat must leave through the other: four times the rise of the two-cold-walls case"),
    (2, 1, "C"): Q("gc-stefan-thickness", "ht.semi-infinite", "Water at 0 °C freezes onto a plate {{dT}} °C below freezing (ice k = 2.2 W/m·K, ρ = 917 kg/m³, L = 334 kJ/kg). How thick is the ice, in mm, after {{t}} min?",
                   given={"dT": {"pick": [5, 10, 20]}, "t": {"pick": [10, 30, 60]}}, value="sqrt(2*2.2*dT*t*60/(917*334000))*1000", tex="\\delta",
                   verify="solve(Eq(917*334000*(x/1000)**2/(2*Rational(22, 10)*dT), t*60), x)[1]", explain="δ ∝ √t: the second half-hour adds less than half as much ice as the first"),
    (2, 1, "D"): Q("gc-transference", "mass.diffusivity", "For dilute {{salt}} ({{ion1}} {{dp}}, {{ion2}} {{dm}} × 10⁻⁹ m²/s), what fraction of the current does the cation carry (its transference number)?",
                   cases=[{"salt": "NaCl", "ion1": "Na⁺", "ion2": "Cl⁻", "dp": 1.334, "dm": 2.032}, {"salt": "HCl", "ion1": "H⁺", "ion2": "Cl⁻", "dp": 9.31, "dm": 2.032},
                          {"salt": "KCl", "ion1": "K⁺", "ion2": "Cl⁻", "dp": 1.957, "dm": 2.032}, {"salt": "LiCl", "ion1": "Li⁺", "ion2": "Cl⁻", "dp": 1.029, "dm": 2.032}],
                   value="dp/(dp + dm)", tex="t_+", verify="solve(Eq(x*(nsimplify(dp) + nsimplify(dm)), nsimplify(dp)), x)[0]",
                   explain="Mobility ∝ D (Nernst–Einstein), so current splits in proportion to D for a 1:1 salt. KCl's near-equal split is why it fills salt bridges"),
    (2, 1, "E"): Q("gc-flux-model-ratio", "mass.steady", "With bulk mole fraction y_A = {{y}} and zero at the catalyst, how does the flux of A for A → 2B compare with diffusion through stagnant B (same film)? Give N(A → 2B)/N(stagnant).",
                   given={"y": {"pick": [0.1, 0.3, 0.6, 0.9]}}, value="log(1 + y)/log(1/(1 - y))", tex="N/N_{stag}",
                   verify="integrate(1/(1 + Symbol('q')), (Symbol('q'), 0, nsimplify(y)))/integrate(1/(1 - Symbol('q')), (Symbol('q'), 0, nsimplify(y)))",
                   explain="Counterflow of B fights A; a stagnant B lets the bulk flow help A along. The difference vanishes for dilute A"),
    (2, 1, "F"): Q("gc-plate-local-k", "mass.interphase", "On a laminar flat plate, the local mass-transfer coefficient at the trailing edge is what fraction of the plate-average coefficient?",
                   given={"L": {"pick": [5, 10, 20]}}, value="0.5", tex="k_L/\\bar k", verify="(1/sqrt(Symbol('q'))).subs(Symbol('q'), nsimplify(L))/(integrate(1/sqrt(Symbol('q')), (Symbol('q'), 0, nsimplify(L)))/nsimplify(L))",
                   explain="k ∝ x^{−1/2}, whose average over the length is twice the end value; the leading edge carries the transfer"),
    (3, 1, "A"): Q("gc-vdw-b", "thermo.stability", "{{g}} has $T_c$ = {{Tc}} K and $P_c$ = {{Pc}} MPa. What van der Waals b does that give, in 10⁻⁵ m³/mol? ($R = 8.314$)",
                   cases=[{"g": "CO₂", "Tc": 304.13, "Pc": 7.377}, {"g": "Methane", "Tc": 190.56, "Pc": 4.599}, {"g": "Nitrogen", "Tc": 126.2, "Pc": 3.398}, {"g": "Ammonia", "Tc": 405.4, "Pc": 11.333}],
                   value="8.314*Tc/(8*Pc*1e6)*1e5", tex="b",
                   verify="solve([Eq(Symbol('aa')/(27*Symbol('bb')**2), nsimplify(Pc)*10**6), Eq(8*Symbol('aa')/(27*Rational(8314, 1000)*Symbol('bb')), nsimplify(Tc))], [Symbol('aa'), Symbol('bb')], dict=True)[0][Symbol('bb')]*10**5",
                   explain="Fitting a and b to the critical point is the usual way to set them; b is roughly the excluded volume per mole"),
    (3, 1, "B"): Q("gc-pr-alpha", "thermo.stability", "In the Peng–Robinson equation, what is α(T) for a fluid with ω = {{om}} at reduced temperature $T_r$ = {{tr}}?",
                   given={"om": {"pick": [0.011, 0.152, 0.224, 0.345]}, "tr": {"pick": [0.7, 0.9, 1.2, 1.5]}},
                   value="(1 + (0.37464 + 1.54226*om - 0.26992*om^2)*(1 - sqrt(tr)))^2", tex="\\alpha",
                   verify="(1 + (Rational(37464, 10**5) + Rational(154226, 10**5)*nsimplify(om) - Rational(26992, 10**5)*nsimplify(om)**2)*(1 - sqrt(nsimplify(tr))))**2",
                   explain="α = 1 at the critical temperature; it grows below T_c so the attraction term strengthens, and ω tunes the slope so vapour pressures come out right"),
    (3, 1, "C"): Q("gc-spinodal-A", "thermo.stability", "For $g^E/RT = Ax_1x_2$, what is the smallest A at which a mixture with x₁ = {{x1}} becomes unstable (lies on the spinodal)?",
                   given={"x1": {"pick": [0.1, 0.2, 0.3, 0.5]}}, value="(1/x1 + 1/(1 - x1))/2", tex="A_s",
                   verify="solve(diff(Symbol('q')*log(Symbol('q')) + (1 - Symbol('q'))*log(1 - Symbol('q')) + x*Symbol('q')*(1 - Symbol('q')), Symbol('q'), 2).subs(Symbol('q'), nsimplify(x1)), x)[0]",
                   explain="The spinodal bounds the region where tiny fluctuations grow; it touches A = 2 only at x₁ = ½"),
    (3, 1, "D"): Q("gc-virial-fugacity", "thermo.maxwell", "A gas with second virial coefficient B = {{B}} cm³/mol is at {{T}} K and {{P}} bar. What is its fugacity coefficient?",
                   given={"B": {"pick": [-300, -100, -40, 20]}, "T": {"pick": [300, 400]}, "P": {"pick": [5, 10, 20]}}, value="exp(B*1e-6*P*1e5/(8.314*T))", tex="\\phi",
                   verify="exp(integrate((nsimplify(B)/10**6*Symbol('pp')/(Rational(8314, 1000)*T))/Symbol('pp'), (Symbol('pp'), 0, P*10**5)))",
                   explain="ln φ = ∫(Z − 1)dP/P = BP/RT: attractions (B < 0) give φ < 1, an 'escaping tendency' below the pressure"),
    (3, 1, "E"): Q("gc-parallel-equilibria", "thermo.chemical-equilibrium", "In an ideal liquid, A ⇌ B ($K_1$ = {{k1}}) and A ⇌ C ($K_2$ = {{k2}}). What is the equilibrium mole fraction of A?",
                   given={"k1": {"pick": [0.5, 2, 5]}, "k2": {"pick": [0.2, 1, 3]}}, value="1/(1 + k1 + k2)", tex="x_A",
                   verify="solve([Eq(Symbol('b'), nsimplify(k1)*Symbol('a')), Eq(Symbol('c'), nsimplify(k2)*Symbol('a')), Eq(Symbol('a') + Symbol('b') + Symbol('c'), 1)], [Symbol('a'), Symbol('b'), Symbol('c')])[Symbol('a')]",
                   explain="Isomers share one pool: each takes a share in proportion to its K relative to A"),
    (3, 1, "F"): Q("gc-k-equals-one", "thermo.chemical-equilibrium", "A reaction has K = {{K0}} at 298.15 K and ΔH° = {{dH}} kJ/mol (take ΔH° and ΔS° constant). At what temperature is K = 1, in K? ($R = 8.314$)",
                   given={"K0": {"pick": [1e-6, 1e-3, 1e3, 1e6]}, "dH": {"pick": [-90, -40, 40, 90]}}, require=["(K0 < 1 and dH > 0) or (K0 > 1 and dH < 0)"],
                   value="dH*1000/((dH*1000 + 8.314*298.15*log(K0))/298.15)", tex="T",
                   verify="1/(1/Rational(29815, 100) + Rational(8314, 1000)*log(nsimplify(K0))/(dH*1000))",
                   explain="K = 1 where ΔG° = 0, i.e. T = ΔH°/ΔS°: above it an endothermic reaction favours products, below it an exothermic one does"),
    (3, 1, "G"): Q("gc-azeotrope-pressure", "thermo.solutions", "A binary follows $g^E/RT = Ax_1x_2$ with A = {{A}}; $P_2^{sat}$ = {{p2}} kPa and $P_1^{sat}/P_2^{sat}$ = {{r}}. What is the azeotrope pressure, in kPa?",
                   given={"A": {"pick": [1, 1.5, 2]}, "r": {"pick": [1.1, 1.3]}, "p2": {"pick": [50, 100]}},
                   value="exp(A*(1 - (1 + log(r)/A)/2)^2)*r*p2", tex="P_{az}",
                   verify="exp(nsimplify(A)*(1 - solve(Eq(log(nsimplify(r)) + nsimplify(A)*(1 - x)**2 - nsimplify(A)*x**2, 0), x)[0])**2)*nsimplify(r)*p2",
                   explain="At the azeotrope P = γ₁P₁^sat = γ₂P₂^sat; positive deviations make it a pressure maximum (a minimum-boiling azeotrope)"),
    (4, 1, "A"): Q("gc-generation-slope", "cre.nonisothermal", "For a first-order exothermic CSTR at a steady state with kτ = {{kt}}, $\\Delta T_{ad}$ = {{J}} K, $E_a$ = {{Ea}} kJ/mol and T = {{T}} K, what heat-removal slope (in the same units) would put it exactly on the stability boundary?",
                   given={"kt": {"pick": [0.2, 1, 4]}, "J": {"pick": [100, 200, 300]}, "Ea": {"pick": [60, 90]}, "T": {"pick": [350, 400]}},
                   value="J*kt/(1 + kt)^2*Ea*1000/(8.314*T^2)", tex="dG/dT",
                   verify="diff(J*Symbol('kk')/(1 + Symbol('kk')), Symbol('kk')).subs(Symbol('kk'), nsimplify(kt))*nsimplify(kt)*Ea*1000/(Rational(8314, 1000)*T**2)",
                   explain="dG/dT peaks at kτ = 1; cooling must be steeper than that slope to hold a steady state in the middle of the S-curve"),
    (4, 1, "B"): Q("gc-equilibrium-temperature", "cre.nonisothermal", "A ⇌ B: forward $A_1$ = {{a1}} s⁻¹, $E_1$ = {{e1}} kJ/mol; reverse $A_2$ = {{a2}} s⁻¹, $E_2$ = {{e2}} kJ/mol. Above what temperature, in K, can conversion {{X}} not be reached at all?",
                   given={"a1": {"pick": [1e6, 1e7]}, "e1": {"pick": [50, 60]}, "a2": {"pick": [1e12, 1e13]}, "e2": {"pick": [110, 130]}, "X": {"pick": [0.3, 0.5, 0.7]}},
                   value="(e2 - e1)*1000/(8.314*log(a2*X/(a1*(1 - X))))", tex="T_{eq}", verify="gc_teq(a1, e1*1000, a2, e2*1000, X)",
                   explain="Equilibrium conversion falls with temperature for an exothermic reaction; the optimum temperature always lies below this line"),
    (4, 1, "C"): Q("gc-surface-concentration", "cre.diffusion", "Spherical pellets have Thiele modulus φ = {{phi}} and mass Biot number {{Bi}} (first order). What is the surface concentration as a fraction of the bulk?",
                   given={"phi": {"pick": [0.5, 2, 5, 10]}, "Bi": {"pick": [1, 10, 100]}},
                   value="1/(1 + (3*(phi*coth(phi) - 1)/phi^2)*phi^2/(3*Bi))", tex="C_s/C_b", verify="gc_surface_ratio(phi, Bi)",
                   explain="C_s near 1: the film is negligible. Near 0: external mass transfer controls and the pellet interior hardly matters"),
    (4, 1, "D"): Q("gc-hatta-regime", "cre.diffusion", "Gas absorption with pseudo-first-order reaction: k = {{k}} s⁻¹, D = {{Dm}} × 10⁻⁹ m²/s, $k_L$ = {{kl}} × 10⁻⁴ m/s. Which regime applies?",
                   given={"k": {"pick": [0.01, 1, 100, 10000]}, "Dm": {"pick": [1, 2]}, "kl": {"pick": [1, 2, 4]}},
                   require=["abs(sqrt(k*Dm*1e-9)/(kl*1e-4) - 0.3) > 0.03", "abs(sqrt(k*Dm*1e-9)/(kl*1e-4) - 3) > 0.3"],
                   choice=["Slow (Ha < 0.3): reaction in the bulk liquid", "Intermediate (0.3 to 3)", "Fast (Ha > 3): reaction within the film"],
                   correct="sqrt(k*Dm*1e-9)/(kl*1e-4) < 0.3 ? 0 : (sqrt(k*Dm*1e-9)/(kl*1e-4) < 3 ? 1 : 2)",
                   verify="0 if sqrt(k*nsimplify(Dm)/10**9)/(nsimplify(kl)/10**4) < Rational(3, 10) else (1 if sqrt(k*nsimplify(Dm)/10**9)/(nsimplify(kl)/10**4) < 3 else 2)",
                   explain="Ha² compares reaction in the film to diffusion across it; in the fast regime interfacial area, not liquid volume, sets the rate"),
    (4, 1, "E"): Q("gc-slurry-controlling", "cre.diffusion", "In a slurry reactor, gas absorption $k_ba_b$ = {{kb}}, liquid-to-particle $k_ca_p$ = {{kc}} and surface reaction $\\eta ka_p$ = {{kr}} s⁻¹. What fraction of the total resistance is gas absorption?",
                   given={"kb": {"pick": [0.05, 0.2, 1]}, "kc": {"pick": [0.1, 0.5]}, "kr": {"pick": [0.02, 0.1, 0.5]}}, value="(1/kb)/(1/kb + 1/kc + 1/kr)", tex="f_b",
                   verify="(1/nsimplify(kb))/(1/nsimplify(kb) + 1/nsimplify(kc) + 1/nsimplify(kr))",
                   explain="Plotting C_i/r against 1/(catalyst loading) separates the absorption term (intercept) from the particle terms (slope)"),
    (4, 1, "F"): Q("gc-deactivation-limit", "cre.catalysis", "A first-order batch reaction (k = {{k}} h⁻¹) runs on a catalyst decaying with $k_d$ = {{kd}} h⁻¹. What is the highest conversion it can ever reach?",
                   given={"k": {"pick": [0.5, 1, 2]}, "kd": {"pick": [0.1, 0.3, 1]}}, value="1 - exp(-k/kd)", tex="X_\\infty",
                   verify="limit(1 - exp(-(nsimplify(k)/nsimplify(kd))*(1 - exp(-nsimplify(kd)*Symbol('tt')))), Symbol('tt'), oo)",
                   explain="The catalyst can do only k/k_d 'first-order lifetimes' of work; to go further you must regenerate or replace it"),
    (5, 1, "A"): Q("gc-ramp-lag", "design.control", "A first-order process (K = 1, τ = {{tau}} min) is driven by a ramp input. Once transients die out, by how many minutes does the output lag the input?",
                   given={"tau": {"pick": [2, 5, 12]}}, value="tau", tex="t_{lag}", verify="limit(Symbol('tt') - (Symbol('tt') - tau*(1 - exp(-Symbol('tt')/tau))), Symbol('tt'), oo)",
                   explain="A first-order lag follows a ramp at the same slope but τ behind: a quick way to read τ from plant data"),
    (5, 1, "B"): Q("gc-zeta-from-overshoot", "design.control", "A second-order process overshoots by {{os}}% after a step. What is its damping ratio ζ?",
                   given={"os": {"pick": [5, 10, 16, 25, 40]}}, value="-log(os/100)/sqrt(pi^2 + log(os/100)^2)", tex="\\zeta",
                   verify="solve(Eq(-pi*x/sqrt(1 - x**2), log(Rational(os, 100))), x)[0]", explain="Invert OS = exp(−πζ/√(1 − ζ²)); reading ζ from a step test is how a process is identified"),
    (5, 1, "C"): Q("gc-kc-for-offset", "design.control", "A first-order process has gain K = {{K}}. What proportional gain $K_c$ keeps the setpoint offset at {{e}}% of the step?",
                   given={"K": {"pick": [0.5, 2, 4]}, "e": {"pick": [2, 5, 10, 20]}}, value="(100/e - 1)/K", tex="K_c",
                   verify="solve(Eq(1/(1 + nsimplify(K)*x), Rational(e, 100)), x)[0]", explain="Offset falls as 1/(1 + KK_c), but high gain costs stability once lags and dead time are present"),
    (5, 1, "D"): Q("gc-stability-check", "design.control", "A process $K/[({{t1}}s + 1)({{t2}}s + 1)({{t3}}s + 1)]$ runs under proportional control with loop gain $KK_c$ = {{kk}}. Is the closed loop stable?",
                   given={"t1": {"pick": [1, 2]}, "t2": {"pick": [1, 3]}, "t3": {"pick": [1, 4, 10]}, "kk": {"pick": [2, 5, 8, 12, 20]}},
                   require=["abs(kk - ((t1 + t2 + t3)*(t1*t2 + t1*t3 + t2*t3)/(t1*t2*t3) - 1)) > 0.2"],
                   choice=["Stable", "Unstable"], correct="kk < (t1 + t2 + t3)*(t1*t2 + t1*t3 + t2*t3)/(t1*t2*t3) - 1 ? 0 : 1",
                   verify="0 if kk < gc_ultimate(t1, t2, t3) else 1", explain="Compare with the ultimate gain from Routh or s = iω; well-separated lags allow a much higher gain than equal ones"),
    (5, 1, "E"): Q("gc-zn-reset", "design.control", "For $G = K/[({{t1}}s + 1)({{t2}}s + 1)({{t3}}s + 1)]$ (min), what reset time τ_I, in minutes, do the Ziegler–Nichols PI rules give (τ_I = P_u/1.2)?",
                   given={"t1": {"pick": [1, 2]}, "t2": {"pick": [1, 3, 5]}, "t3": {"pick": [1, 4, 10]}}, value="2*pi/sqrt((t1 + t2 + t3)/(t1*t2*t3))/1.2", tex="\\tau_I",
                   verify="gc_ultimate_period(t1, t2, t3)*Rational(5, 6)", explain="Ziegler–Nichols tunes from the ultimate gain and period; it gives quarter-decay responses, aggressive by modern standards"),
    (5, 1, "F"): Q("gc-phase-lag", "design.control", "A first-order process (τ = {{tau}} s) is driven at {{w}} rad/s. What is the phase lag of the output, in degrees?",
                   given={"tau": {"pick": [1, 5, 20]}, "w": {"pick": [0.05, 0.2, 1]}}, value="atan(w*tau)*180/pi", tex="\\phi",
                   verify="-arg(1/(I*nsimplify(w)*tau + 1))*180/pi", explain="A first-order lag never exceeds 90°; 45° at the corner frequency ω = 1/τ"),
    (5, 1, "G"): Q("gc-fopdt-ultimate-gain", "design.control", "A process $Ke^{-{{th}}s}/({{tau}}s + 1)$ (min) under P control: what is the ultimate loop gain $KK_{cu}$?",
                   cases=FOP, value="sqrt(1 + wu^2*tau^2)", tex="KK_{cu}", verify="sqrt(1 + gc_fopdt_wu(tau, th)**2*tau**2)",
                   explain="At the crossover frequency the loop gain must be 1/AR; dead time lowers the crossover and so the allowable gain"),
    (6, 1, "A"): Q("gc-rayleigh-distillate", "sep.distillation", "Batch distillation with α = {{al}} takes the still from {{x0}} to {{x1}}. What is the average light-key mole fraction of the collected distillate?",
                   given={"al": {"pick": [1.5, 2.5, 4]}, "x0": {"pick": [0.5, 0.6]}, "x1": {"pick": [0.1, 0.2, 0.3]}},
                   value="(x0 - x1*exp(-(log(x0/x1) + al*log((1 - x1)/(1 - x0)))/(al - 1)))/(1 - exp(-(log(x0/x1) + al*log((1 - x1)/(1 - x0)))/(al - 1)))", tex="\\bar x_D",
                   verify="(nsimplify(x0) - nsimplify(x1)*gc_rayleigh(al, x0, x1))/(1 - gc_rayleigh(al, x0, x1))",
                   explain="A light-key balance on the whole batch: what left the still is the distillate"),
    (6, 1, "B"): Q("gc-absorber-exit-liquid", "sep.absorption", "An absorber takes y from {{yin}}% to {{yout}}% with solute-free liquid at 1.5 times the minimum L/G (equilibrium y = {{m}}x). What is the exit liquid mole fraction?",
                   given={"yin": {"pick": [2, 5]}, "yout": {"pick": [0.1, 0.25, 0.5]}, "m": {"pick": [0.5, 1.2, 2]}},
                   value="(yin - yout)/100/(1.5*(yin - yout)/100/(yin/100/m))", tex="x_{out}",
                   verify="solve(Eq(Rational(3, 2)*((nsimplify(yin) - nsimplify(yout))/100/(nsimplify(yin)/100/nsimplify(m)))*x, (nsimplify(yin) - nsimplify(yout))/100), x)[0]",
                   explain="More liquid than the minimum leaves it less loaded: here at two-thirds of the equilibrium value"),
    (6, 1, "C"): Q("gc-q-line-slope", "sep.distillation", "A feed is {{f}}% vapour (by moles), saturated. What is the slope of its q-line on the McCabe–Thiele diagram?",
                   given={"f": {"pick": [10, 25, 50, 75, 90]}}, value="(1 - f/100)/((1 - f/100) - 1)", tex="q/(q-1)",
                   verify="solve(Eq(x*((1 - Rational(f, 100)) - 1), 1 - Rational(f, 100)), x)[0]",
                   explain="q = 1 − vapour fraction; the q-line is vertical for saturated liquid, horizontal for saturated vapour, and negative in between"),
}
for u in UNITS:
    for tn, (_, los) in enumerate(u.topics, 1):
        for lo in los:
            q = SECOND.get((u.n, tn, lo.id))
            if q is not None:
                lo.qs.append(q)
