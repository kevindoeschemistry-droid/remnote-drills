"""Graduate mass transfer (framework mass-transfer, MS): a house list on BSL 2e chapters 17-24, anchored
on PE Chemical area 6. Not an OPL subject, so no `opl` sections: objectives cite pe-chemical directly."""
from opl_dsl import Q, L, U

FW, FILE, IDEA = "MS", "ms-mass-transfer", "FLUX"
A, B = ["pe-chemical:6.A"], ["pe-chemical:6.B"]

UNITS = [
U(1, "diffusivity", "Diffusivities and fluxes", [
    ("Estimating diffusivities", [
        L("A", "Scale a gas diffusivity with temperature and pressure.", "Chapman–Enskog: D_AB ∝ T^{3/2}/(P σ² Ω_D); ignoring the collision integral, D ∝ T^{3/2}/P.", [], [
            Q("ms-gas-diffusivity-scaling", "mass.diffusivity", "A gas-pair diffusivity is {{D1}} cm²/s at {{T1}} K and 1 atm. Ignoring the change in the collision integral, estimate it at {{T2}} K and {{P}} atm.",
              given={"D1": {"pick": [0.1, 0.2, 0.6]}, "T1": {"pick": [300, 350]}, "T2": {"pick": [400, 500, 600]}, "P": {"pick": [0.5, 2, 5]}}, value="D1*(T2/T1)^1.5/P", tex="D", tol=0.01,
              verify="nsimplify(D1)*((T2**Rational(3, 2)/nsimplify(P))/(T1**Rational(3, 2)/1))", explain="Kinetic theory: faster molecules (√T) and a longer mean free path (T/P) give $T^{3/2}/P$. Gas diffusivities are about 0.1 cm²/s; liquids about 10⁻⁵")], std=A),
        L("B", "Scale a liquid diffusivity with temperature and viscosity.", "Stokes–Einstein: D = kT/(6πμa), so D μ/T is constant.", [], [
            Q("ms-liquid-diffusivity-scaling", "mass.diffusivity", "A solute has $D = {{D1}}\\times10^{-9}$ m²/s in water at {{T1}} K ($\\mu = {{mu1}}$ mPa·s). Estimate $D$ at {{T2}} K, where $\\mu = {{mu2}}$ mPa·s, in units of $10^{-9}$ m²/s.",
              cases=[{"T1": 298, "mu1": 0.89, "T2": 310, "mu2": 0.69}, {"T1": 298, "mu1": 0.89, "T2": 323, "mu2": 0.55}, {"T1": 293, "mu1": 1.0, "T2": 343, "mu2": 0.40}],
              given={"D1": {"pick": [0.5, 1, 2]}}, value="D1*(T2/T1)*(mu1/mu2)", tex="D", tol=0.01,
              verify="nsimplify(D1)*(T2/nsimplify(mu2))/(T1/nsimplify(mu1))", explain="Heating a liquid helps twice: more thermal energy and a lower viscosity, which falls much faster than $T$ rises")], std=A),
        L("C", "Estimate a Knudsen diffusivity and decide the regime.", "D_K = (d/3)√(8RT/πM); Knudsen diffusion takes over when the pore is smaller than the mean free path.", [], [
            Q("ms-knudsen", "mass.diffusivity", "Find the Knudsen diffusivity of a gas with $M = {{M}}$ g/mol in a pore {{d}} nm across at {{T}} K, in cm²/s.",
              given={"M": {"pick": [2, 28, 44]}, "d": {"pick": [5, 10, 50]}, "T": {"pick": [300, 500, 700]}}, value="(d*1e-9/3)*sqrt(8*8.314*T/(pi*M/1000))*1e4", tex="D_K", tol=0.01,
              verify="(Rational(d, 10**9)/3)*sqrt(8*Rational(8314, 1000)*T/(pi*Rational(M, 1000)))*10**4", explain="Molecules hit walls more often than each other, so the pore size replaces the mean free path. $D_K$ does not depend on pressure and goes as $\\sqrt{T/M}$")], std=A),
        L("D", "Find an effective diffusivity in a porous solid.", "D_eff = D ε/τ.", [], [
            Q("ms-effective-diffusivity", "mass.diffusivity", "A catalyst pellet has porosity {{e}} and tortuosity {{t}}; the pore diffusivity is {{D}} cm²/s. What is $D_{eff}$, in cm²/s?",
              given={"e": {"pick": [0.3, 0.4, 0.5]}, "t": {"pick": [2, 3, 4]}, "D": {"pick": [0.01, 0.05, 0.1]}}, value="D*e/t", tex="D_{eff}", tol=0.01,
              verify="solve(Eq(x*nsimplify(t), nsimplify(D)*nsimplify(e)), x)[0]", explain="Only the pore fraction carries flux, along paths longer than the pellet: divide by τ (typically 2–6)")], std=A),
    ]),
    ("Fluxes and reference frames", [
        L("A", "Find the flux for diffusion through a stagnant gas.", "N_A = (cD/L) ln[(1 − x_A2)/(1 − x_A1)] (Stefan tube).", [], [
            Q("ms-stagnant-film", "mass.steady", "Vapour A diffuses through {{L}} cm of stagnant air in a tube: $x_A = {{x1}}$ at the liquid surface and 0 at the top. With $c = 40.9$ mol/m³ and $D = {{D}}\\times10^{-5}$ m²/s. Find $N_A$, in mmol/(m²·s).",
              given={"L": {"pick": [5, 10, 20]}, "x1": {"pick": [0.1, 0.3, 0.5]}, "D": {"pick": [1, 1.5, 2.5]}}, value="40.9*D*1e-5/(L/100)*log(1/(1 - x1))*1000", tex="N_A", tol=0.01,
              verify="integrate(Rational(409, 10)*nsimplify(D)/10**5/(1 - x), (x, 0, nsimplify(x1)))/(Rational(L, 100))*1000",
              explain="B is stagnant, so A carries B's share of the bulk flow: $N_A = -cD\\,\\frac{dx_A}{dz}/(1 - x_A)$. Integrating gives the log; for dilute A it reduces to Fick")], std=A),
        L("B", "Compare stagnant-film and equimolar fluxes.", "N_stagnant/N_equimolar = 1/x_B,lm.", [], [
            Q("ms-bulk-flow-factor", "mass.steady", "Across a film, $x_A$ falls from {{x1}} to {{x2}}. By what factor is the flux through stagnant B larger than for equimolar counterdiffusion with the same $c$, $D$ and thickness?",
              given={"x1": {"pick": [0.2, 0.4, 0.6, 0.8]}, "x2": {"pick": [0.0, 0.1]}}, value="log((1 - x2)/(1 - x1))/(x1 - x2)", tex="N/N_{eq}", tol=0.01,
              verify="integrate(1/(1 - x), (x, nsimplify(x2), nsimplify(x1)))/integrate(1, (x, nsimplify(x2), nsimplify(x1)))",
              explain="The bulk flow drags A along; the factor is $1/x_{B,lm}$. It matters only when A is concentrated")], std=A),
    ]),
]),
U(2, "steady", "Steady diffusion with reaction and geometry", [
    ("Shell balances", [
        L("A", "Find the effectiveness factor of a catalyst slab.", "η = tanh φ / φ with φ = L√(k/D_eff).", [], [
            Q("ms-effectiveness-slab", "mass.steady", "A catalyst slab of half-thickness {{L}} mm runs a first-order reaction with $k = {{k}}$ s⁻¹ and $D_{eff} = {{D}}\\times10^{-6}$ m²/s. Find the effectiveness factor.",
              given={"L": {"pick": [1, 2, 5]}, "k": {"pick": [1, 5, 20]}, "D": {"pick": [0.5, 1, 5]}}, value="tanh((L/1000)*sqrt(k/(D*1e-6)))/((L/1000)*sqrt(k/(D*1e-6)))", tex="\\eta", tol=0.01,
              verify="(nsimplify(D)/10**6*diff(cosh(sqrt(k/(nsimplify(D)/10**6))*x)/cosh(sqrt(k/(nsimplify(D)/10**6))*Rational(L, 1000)), x).subs(x, Rational(L, 1000)))/(k*Rational(L, 1000))",
              explain="Solve $D c'' = kc$ with $c = c_s$ at the surface and no flux at the centre: $c = c_s\\cosh(z\\sqrt{k/D})/\\cosh\\phi$. η is the actual rate (the surface flux) over the rate if the whole slab saw $c_s$")], std=A),
        L("B", "Find the effectiveness factor of a spherical pellet.", "η = (3/φ²)(φ coth φ − 1) with φ = R√(k/D_eff).", [], [
            Q("ms-effectiveness-sphere", "mass.steady", "A spherical pellet has Thiele modulus $\\phi = R\\sqrt{k/D_{eff}} = {{phi}}$. Find its effectiveness factor.",
              given={"phi": {"pick": [0.5, 1, 2, 5, 10]}}, value="3/phi^2*(phi/tanh(phi) - 1)", tex="\\eta", tol=0.01,
              verify="3*diff(sinh(nsimplify(phi)*x)/(x*sinh(nsimplify(phi))), x).subs(x, 1)/nsimplify(phi)**2",
              explain="The sphere's profile is $\\sinh(\\phi r)/(r\\sinh\\phi)$; η is $3/\\phi^2$ times the dimensionless surface gradient. Large φ gives η ≈ 3/φ: only a thin shell works")], std=A),
        L("C", "Find steady diffusion through a spherical shell.", "Ẇ = 4πD(c₁ − c₂)/(1/r₁ − 1/r₂).", [], [
            Q("ms-spherical-shell", "mass.steady", "A solute diffuses outward through a spherical shell from $r_1 = {{r1}}$ cm ($c = {{c1}}$ mol/m³) to $r_2 = {{r2}}$ cm ($c = 0$); $D = {{D}}\\times10^{-9}$ m²/s. Find the rate, in nmol/s.",
              given={"r1": {"pick": [1, 2]}, "r2": {"pick": [3, 4, 5]}, "c1": {"pick": [10, 50, 100]}, "D": {"pick": [0.5, 1, 2]}}, value="4*pi*D*1e-9*c1/(1/(r1/100) - 1/(r2/100))*1e9", tex="\\dot W", tol=0.01,
              verify="solve(Eq(integrate(x/(4*pi*nsimplify(D)/10**9*Symbol('r')**2), (Symbol('r'), Rational(r1, 100), Rational(r2, 100))), c1), x)[0]*10**9",
              explain="The rate through every shell is the same, so $c$ falls as $1/r$. Letting $r_2 \\to \\infty$ gives Sh = 2 for an isolated sphere")], std=A),
        L("D", "Find the lifetime of an evaporating droplet.", "Quasi-steady, Sh = 2: d(d²)/dt is constant (the d² law).", [], [
            Q("ms-droplet-lifetime", "mass.steady", "A water droplet of diameter {{d0}} µm evaporates into dry still air. With $D = 2.5\\times10^{-5}$ m²/s, saturated vapour concentration {{cs}} kg/m³ at the surface and liquid density 1000 kg/m³, how long does it last, in s?",
              given={"d0": {"pick": [20, 50, 100]}, "cs": {"pick": [0.017, 0.023, 0.03]}}, value="1000*(d0*1e-6)^2/(8*2.5e-5*cs)", tex="t", tol=0.01,
              verify="integrate(1000*Symbol('r')/(Rational(25, 10**6)*nsimplify(cs)), (Symbol('r'), 0, Rational(d0, 2*10**6)))",
              explain="The evaporation rate $4\\pi rDc_s$ shrinks the droplet: $\\rho\\,r\\,dr/dt = -Dc_s$, so $r^2$ falls linearly. Lifetime goes as $d_0^2$")], std=A),
        L("E", "Find the absorption coefficient into a falling film.", "Penetration theory: k̄ = 2√(D/πt) with contact time t = L/v_max.", [], [
            Q("ms-film-absorption", "mass.interphase", "A gas is absorbed into a liquid film whose surface moves at {{v}} m/s over a length {{L}} cm. With $D = {{D}}\\times10^{-9}$ m²/s, find the average mass-transfer coefficient, in µm/s.",
              given={"v": {"pick": [0.1, 0.3, 0.5]}, "L": {"pick": [5, 10, 50]}, "D": {"pick": [1, 2]}}, value="2*sqrt(D*1e-9/(pi*(L/100)/v))*1e6", tex="\\bar k", tol=0.01,
              verify="integrate(sqrt(nsimplify(D)/10**9/(pi*x)), (x, 0, Rational(L, 100)/nsimplify(v)))/(Rational(L, 100)/nsimplify(v))*10**6",
              explain="Each surface element is exposed for $t = L/v$ and absorbs like a semi-infinite liquid, local $k = \\sqrt{D/\\pi t}$. Averaging over the exposure doubles it")], std=B),
    ]),
]),
U(3, "unsteady", "Unsteady diffusion", [
    ("Time scales and transients", [
        L("A", "Estimate a diffusion time from L²/D.", "t ~ L²/D; penetration depth ~ √(4Dt).", [], [
            Q("ms-diffusion-time", "mass.unsteady", "Roughly how long does a solute with $D = {{D}}$ cm²/s take to diffuse {{L}} {{u}}, using $t \\approx L^2/D$, in seconds?",
              cases=[{"L": 1, "u": "µm", "f": 1e-4}, {"L": 1, "u": "mm", "f": 0.1}, {"L": 1, "u": "cm", "f": 1}, {"L": 10, "u": "µm", "f": 1e-4}],
              given={"D": {"pick": [1e-5, 1e-6, 0.1]}}, value="(L*f)^2/D", tex="t", tol=0.01, verify="(L*nsimplify(f))**2/nsimplify(D)",
              explain="Diffusion is fast over a cell (milliseconds) and hopelessly slow over centimetres in a liquid (hours). Stirring wins at large scales")], std=A),
        L("B", "Find the amount absorbed by a semi-infinite medium.", "M/A = 2c₀√(Dt/π).", [], [
            Q("ms-semi-infinite-uptake", "mass.unsteady", "A surface held at $c_0 = {{c0}}$ mol/m³ contacts a deep, initially clean liquid ($D = {{D}}\\times10^{-9}$ m²/s). How much solute enters per m² in {{t}} s, in mmol?",
              given={"c0": {"pick": [10, 40, 100]}, "D": {"pick": [1, 2]}, "t": {"pick": [10, 60, 600]}}, value="2*c0*sqrt(D*1e-9*t/pi)*1000", tex="M/A", tol=0.01,
              verify="integrate(c0*sqrt(nsimplify(D)/10**9/(pi*x)), (x, 0, t))*1000",
              explain="The surface flux is $c_0\\sqrt{D/\\pi t}$, infinite at first and decaying; integrate in time. Uptake grows as $\\sqrt t$")], std=A),
        L("C", "Find the slowest decay time of a slab.", "Long-time behaviour: c ∝ exp(−π²Dt/(4L²)) for half-thickness L with fixed surfaces.", [], [
            Q("ms-slab-time-constant", "mass.unsteady", "A slab of half-thickness {{L}} mm ($D = {{D}}\\times10^{-10}$ m²/s) is suddenly held at zero surface concentration. What is the time constant of the slowest mode, in hours?",
              given={"L": {"pick": [0.5, 1, 2]}, "D": {"pick": [1, 5, 10]}}, value="4*(L/1000)^2/(pi^2*D*1e-10)/3600", tex="\\tau", tol=0.01,
              verify="1/(nsimplify(D)/10**10*solve(Eq(cos(x*Rational(L, 1000)), 0), x)[0]**2)/3600",
              explain="Separation of variables gives modes $\\cos(\\lambda_n z)$ with $\\lambda_n L = (n - \\tfrac12)\\pi$; the first, $\\lambda_1 = \\pi/2L$, decays slowest, with $\\tau = 1/(D\\lambda_1^2)$")], std=A),
    ]),
]),
U(4, "interphase", "Interphase mass transfer", [
    ("Coefficients and resistances", [
        L("A", "Combine film coefficients into an overall coefficient.", "1/K_y = 1/k_y + m/k_x.", [], [
            Q("ms-overall-coefficient", "mass.interphase", "Gas-film $k_y = {{ky}}$ and liquid-film $k_x = {{kx}}$ mol/(m²·s); the equilibrium slope is $m = {{m}}$. Find $K_y$.",
              given={"ky": {"pick": [0.02, 0.05, 0.1]}, "kx": {"pick": [0.5, 1, 2]}, "m": {"pick": [0.5, 2, 10, 40]}}, value="1/(1/ky + m/kx)", tex="K_y", tol=0.01,
              verify="solve(Eq(1/x, 1/nsimplify(ky) + nsimplify(m)/nsimplify(kx)), x)[0]",
              explain="Resistances in series, with the liquid side scaled by $m$. A very soluble gas (small m) is gas-film controlled; a sparingly soluble one (large m) is liquid-film controlled")], std=B),
        L("B", "Find the fraction of the resistance in the gas film.", "Gas share = (1/k_y)/(1/k_y + m/k_x).", [], [
            Q("ms-resistance-fraction", "mass.interphase", "With $k_y = {{ky}}$, $k_x = {{kx}}$ mol/(m²·s) and $m = {{m}}$, what fraction of the total resistance lies in the gas film?",
              given={"ky": {"pick": [0.02, 0.05, 0.1]}, "kx": {"pick": [0.5, 1, 2]}, "m": {"pick": [0.5, 2, 10, 40]}}, value="(1/ky)/(1/ky + m/kx)", tex="f_G", tol=0.01,
              verify="(1/nsimplify(ky))*solve(Eq(1/x, 1/nsimplify(ky) + nsimplify(m)/nsimplify(kx)), x)[0]",
              explain="Improve the controlling side: more gas turbulence helps only a gas-film-controlled system")], std=B),
        L("C", "Use a sphere mass-transfer correlation.", "Ranz–Marshall: Sh = 2 + 0.6 Re^{1/2} Sc^{1/3}.", [], [
            Q("ms-ranz-marshall", "mass.interphase", "A sphere in a flow has $Re = {{Re}}$ and $Sc = {{Sc}}$. Find the Sherwood number from Ranz–Marshall.",
              given={"Re": {"pick": [1, 10, 100, 500]}, "Sc": {"pick": [0.7, 1, 600, 1000]}}, value="2 + 0.6*sqrt(Re)*Sc^(1/3)", tex="Sh", tol=0.01,
              verify="2 + Rational(3, 5)*sqrt(Re)*nsimplify(Sc)**Rational(1, 3)", explain="The 2 is pure diffusion to a sphere in still fluid; the second term is convection. Liquids (Sc ~ 1000) gain much more from flow than gases")], std=B),
        L("D", "Predict how k depends on D under each model.", "Film theory: k ∝ D; penetration and surface renewal: k ∝ D^{1/2}; boundary layers: k ∝ D^{2/3}.", [], [
            Q("ms-model-scaling", "mass.interphase", "If the diffusivity rises by a factor of {{f}}, by what factor does $k$ rise according to {{mdl}}?", pace="recall",
              cases=[{"mdl": "film theory", "p": 1}, {"mdl": "penetration theory", "p": 0.5}, {"mdl": "surface-renewal theory", "p": 0.5}, {"mdl": "laminar boundary-layer theory", "p": 0.6666666666666666}],
              given={"f": {"pick": [4, 8, 9, 16]}}, value="f^p", tex="k_2/k_1", tol=0.01, verify="nsimplify(f)**nsimplify(p)",
              explain="Experiments usually find exponents between ½ and ⅔, which is why film theory, though simple, is the least physical")], std=B),
        L("E", "Find a packed-height from HTU and NTU.", "Z = H_OG N_OG; for dilute systems with straight lines, N_OG = (y₁ − y₂)/Δy_lm.", [], [
            Q("ms-htu-ntu", "mass.interphase", "A dilute absorber reduces $y$ from {{y1}} to {{y2}}; the driving forces $y - y^*$ are {{d1}} at the bottom and {{d2}} at the top. With $H_{OG} = {{H}}$ m, how tall must the packing be, in m?",
              given={"y1": {"pick": [0.02, 0.05]}, "y2": {"pick": [0.001, 0.002]}, "d1": {"pick": [0.008, 0.01, 0.015]}, "d2": {"pick": [0.001, 0.0015]}, "H": {"pick": [0.5, 0.8, 1.2]}},
              value="H*(y1 - y2)/((d1 - d2)/log(d1/d2))", tex="Z", tol=0.01,
              verify="nsimplify(H)*(nsimplify(y1) - nsimplify(y2))*log(nsimplify(d1)/nsimplify(d2))/(nsimplify(d1) - nsimplify(d2))",
              explain="NTU counts how many times the average driving force fits into the change in $y$; HTU carries the coefficient and flows. Hard separations need many transfer units")], std=B),
    ]),
]),
U(5, "multicomponent", "Multicomponent diffusion and membranes", [
    ("Mixtures and membranes", [
        L("A", "Find an effective diffusivity of A in a stagnant mixture.", "D_Am = (1 − x_A)/Σ_{j≠A}(x_j/D_Aj) (Wilke).", [], [
            Q("ms-wilke-mixture", "mass.diffusivity", "A diffuses through stagnant B and C. Locally $x_A = {{xa}}$, $x_B = {{xb}}$, and the rest is C; $D_{AB} = {{dab}}$ and $D_{AC} = {{dac}}$ cm²/s. Find $D_{Am}$.",
              given={"xa": {"pick": [0.1, 0.2, 0.3]}, "xb": {"pick": [0.3, 0.4, 0.5]}, "dab": {"pick": [0.1, 0.2]}, "dac": {"pick": [0.05, 0.3, 0.6]}},
              value="(1 - xa)/(xb/dab + (1 - xa - xb)/dac)", tex="D_{Am}", tol=0.01,
              verify="1/((nsimplify(xb)/(1 - nsimplify(xa)))/nsimplify(dab) + ((1 - nsimplify(xa) - nsimplify(xb))/(1 - nsimplify(xa)))/nsimplify(dac))",
              explain="A harmonic mean weighted by the stagnant species' share; it follows from Maxwell–Stefan when only A moves")], std=A),
        L("B", "Find a membrane flux and selectivity.", "N = P Δp / ℓ; ideal selectivity = P_A/P_B.", [], [
            Q("ms-membrane-flux", "mass.steady", "A dense membrane {{l}} µm thick has permeability {{P}} Barrer for O₂ (1 Barrer = $3.35\\times10^{-16}$ mol·m/(m²·s·Pa)). The O₂ partial-pressure difference is {{dp}} kPa. Find the flux, in µmol/(m²·s).",
              given={"l": {"pick": [0.1, 0.5, 1]}, "P": {"pick": [1, 10, 600]}, "dp": {"pick": [20, 50, 100]}}, value="P*3.35e-16*dp*1000/(l*1e-6)*1e6", tex="N", tol=0.01,
              verify="nsimplify(P)*Rational(335, 10**18)*dp*1000/(nsimplify(l)/10**6)*10**6",
              explain="Solution–diffusion: permeability = solubility × diffusivity. Thin skins (sub-micron) are what make polymer membranes practical")], std=B),
    ]),
]),
]

# ── second question types (Nov 2026): one more type per objective, keyed (unit, topic, LO) ──────────────
SECOND = {
    (1, 1, "A"): Q("ms-diffusivity-temperature-reverse", "mass.diffusivity", "A gas pair has D = {{D1}} cm²/s at {{T1}} K and 1 atm. At what temperature, in K, does D reach {{D2}} cm²/s at the same pressure? (Ignore the collision integral.)",
                   given={"D1": {"pick": [0.1, 0.16, 0.25]}, "T1": {"pick": [298, 300]}, "f": {"pick": [1.2, 1.5, 2]}}, let={"D2": "D1*f"},
                   value="T1*(D2/D1)^(2/3)", tex="T_2", verify="solve(Eq(nsimplify(D1)*(x/T1)**Rational(3, 2), nsimplify(D1)*nsimplify(f)), x)[0]",
                   explain="Invert D ∝ T^{3/2}: a 50% rise in D needs only about a 31% rise in absolute temperature"),
    (1, 1, "B"): Q("ms-stokes-einstein-radius", "mass.diffusivity", "A protein has $D = {{D}}\\times10^{-11}$ m²/s in water at 298 K ($\\mu$ = 0.89 mPa·s). What hydrodynamic radius does Stokes–Einstein give, in nm? ($k_B = 1.381\\times10^{-23}$ J/K)",
                   given={"D": {"pick": [4, 6, 9, 12]}}, value="1.381e-23*298/(6*pi*0.89e-3*D*1e-11)*1e9", tex="a",
                   verify="solve(Eq(nsimplify(D)/10**11, Rational(1381, 10**26)*298/(6*pi*Rational(89, 10**5)*x/10**9)), x)[0]",
                   explain="Run D = kT/(6πμa) backwards: diffusion measurements (DLS, NMR) report size this way"),
    (1, 1, "C"): Q("ms-knudsen-crossover", "mass.diffusivity", "A gas (M = {{M}} g/mol) at {{T}} K has molecular diffusivity {{Dm}} cm²/s. Below what pore diameter, in nm, is the Knudsen diffusivity smaller than that? ($R = 8.314$)",
                   given={"M": {"pick": [28, 44, 2]}, "T": {"pick": [300, 500]}, "Dm": {"pick": [0.1, 0.2, 0.5]}}, value="3*Dm*1e-4/sqrt(8*8.314*T/(pi*M/1000))*1e9", tex="d",
                   verify="solve(Eq(x/10**9/3*sqrt(8*Rational(8314, 1000)*T/(pi*nsimplify(M)/1000)), nsimplify(Dm)/10**4), x)[0]",
                   explain="D_K grows linearly with pore size; where it equals the molecular value the transition region begins. Hydrogen's fast molecules push the crossover to larger pores"),
    (1, 1, "D"): Q("ms-tortuosity-from-deff", "mass.diffusivity", "A pellet of porosity {{e}} shows $D_{eff}$ = {{De}} × 10⁻⁷ m²/s for a gas whose pore diffusivity is {{D}} × 10⁻⁶ m²/s. What tortuosity does that imply?",
                   given={"e": {"pick": [0.3, 0.4, 0.5]}, "De": {"pick": [2, 3, 5]}, "D": {"pick": [4, 6]}}, require=["e*D*10/De > 1"], value="e*D*1e-6/(De*1e-7)", tex="\\tau",
                   verify="solve(Eq(nsimplify(De)/10**7, nsimplify(D)/10**6*nsimplify(e)/x), x)[0]", explain="Measured D_eff fixes ε/τ together; values of τ from 2 to 6 are usual, and below 1 means the model is wrong"),
    (1, 2, "A"): Q("ms-stefan-tube-time", "mass.steady", "In a Stefan tube the liquid level falls from {{l1}} cm to {{l2}} cm below the top as it evaporates into stagnant air (c = 40.9 mol/m³, D = {{D}} × 10⁻⁵ m²/s, surface mole fraction {{xs}}, zero at the top). The liquid's molar density is {{rl}} kmol/m³. How long does that take, in hours?",
                   given={"l1": {"pick": [2, 3]}, "l2": {"pick": [4, 5, 6]}, "D": {"pick": [1, 1.5]}, "xs": {"pick": [0.1, 0.3, 0.5]}, "rl": {"pick": [10, 15]}},
                   value="rl*1000*((l2/100)^2 - (l1/100)^2)/(2*40.9*D*1e-5*log(1/(1 - xs)))/3600", tex="t",
                   verify="integrate(rl*1000*Symbol('zz')/(Rational(409, 10)*nsimplify(D)/10**5*log(1/(1 - nsimplify(xs)))), (Symbol('zz'), Rational(l1, 100), Rational(l2, 100)))/3600",
                   explain="Quasi-steady: the flux at each level is the stagnant-film flux over the current path length z, and ρ_L dz/dt equals it, so z² grows linearly in time. This is how D is measured"),
    (1, 2, "B"): Q("ms-log-mean-xb", "mass.steady", "Across a film, x_A is {{x1}} on one side and {{x2}} on the other, with B stagnant. What is the log-mean mole fraction of B?",
                   given={"x1": {"pick": [0.2, 0.4, 0.6, 0.8]}, "x2": {"pick": [0.01, 0.05, 0.1]}}, value="((1 - x2) - (1 - x1))/log((1 - x2)/(1 - x1))", tex="x_{B,lm}",
                   verify="(nsimplify(x1) - nsimplify(x2))/integrate(1/(1 - Symbol('q')), (Symbol('q'), nsimplify(x2), nsimplify(x1)))",
                   explain="x_B,lm sits between the end values; when it is close to 1 the bulk-flow correction can be dropped"),
    (2, 1, "A"): Q("ms-slab-size-effect", "mass.steady", "A first-order reaction in a catalyst slab has Thiele modulus φ = {{phi}}. If the slab is made {{f}} times thicker (same k and $D_{eff}$), by what factor does the rate per unit catalyst volume change?",
                   given={"phi": {"pick": [0.5, 1, 3, 10]}, "f": {"pick": [2, 3]}}, value="(tanh(f*phi)/(f*phi))/(tanh(phi)/phi)", tex="r_2/r_1",
                   verify="(tanh(nsimplify(f)*nsimplify(phi))/(nsimplify(f)*nsimplify(phi)))/(tanh(nsimplify(phi))/nsimplify(phi))",
                   explain="Rate per volume ∝ η. Under strong diffusion control (φ > 3) η ≈ 1/φ, so a thicker slab wastes catalyst in proportion: the classic test for pore-diffusion limits"),
    (2, 1, "B"): Q("ms-sphere-observed-rate", "mass.steady", "Pellets of radius {{R}} mm run a first-order reaction with k = {{k}} s⁻¹ and $D_{eff}$ = {{D}} × 10⁻⁷ m²/s at surface concentration {{c}} mol/m³. What is the observed rate per pellet volume, in mol/(m³·s)?",
                   given={"R": {"pick": [1, 2, 3]}, "k": {"pick": [0.5, 2, 10]}, "D": {"pick": [5, 10]}, "c": {"pick": [10, 50]}},
                   value="3/(R/1000*sqrt(k/(D*1e-7)))^2*((R/1000*sqrt(k/(D*1e-7)))*coth(R/1000*sqrt(k/(D*1e-7))) - 1)*k*c", tex="r_{obs}",
                   verify="4*pi*(nsimplify(D)/10**7)*(Rational(R, 1000))*c*(sqrt(k/(nsimplify(D)/10**7))*Rational(R, 1000)*cosh(sqrt(k/(nsimplify(D)/10**7))*Rational(R, 1000))/sinh(sqrt(k/(nsimplify(D)/10**7))*Rational(R, 1000)) - 1)/(Rational(4, 3)*pi*(Rational(R, 1000))**3)",
                   explain="Same answer two ways: η k c, or the diffusive flux 4πR²D_e(dc/dr)_R through the surface divided by the volume"),
    (2, 1, "C"): Q("ms-shell-vs-slab", "mass.steady", "Diffusion through a spherical shell from $r_1$ = {{r1}} cm to $r_2$ = {{r2}} cm is estimated as a flat slab of the same thickness and the outer area. What is the ratio true rate / slab estimate?",
                   given={"r1": {"pick": [1, 2, 4]}, "r2": {"pick": [5, 6, 8]}}, value="r1/r2", tex="\\dot W/\\dot W_{slab}",
                   verify="(4*pi*r1*r2/(r2 - r1))/(4*pi*r2**2/(r2 - r1))", explain="Flux spreads outward, so the inner surface throttles the rate; the slab estimate with the outer area overstates it by r₂/r₁"),
    (2, 1, "D"): Q("ms-droplet-fraction-time", "mass.steady", "An evaporating droplet follows the d² law. What fraction of its total lifetime does it take to shrink to {{p}}% of its initial diameter?",
                   given={"p": {"pick": [25, 50, 75, 90]}}, value="1 - (p/100)^2", tex="t/t_{life}",
                   verify="integrate(Symbol('q'), (Symbol('q'), Rational(p, 100), 1))/integrate(Symbol('q'), (Symbol('q'), 0, 1))",
                   explain="d² falls linearly in time, so shrinking to half the diameter uses three quarters of the life"),
    (2, 1, "E"): Q("ms-penetration-scaling", "mass.interphase", "In penetration theory, by what factor does the average coefficient change if the contact length grows {{f}}-fold and the surface speed {{g}}-fold?",
                   given={"f": {"pick": [2, 4]}, "g": {"pick": [0.5, 2, 4]}}, value="sqrt(g/f)", tex="k_2/k_1", verify="sqrt(nsimplify(g)/nsimplify(f))",
                   explain="k ∝ √(D/t) with t = L/v, so k ∝ √(v/L): faster or shorter contact renews the surface more often"),
    (3, 1, "A"): Q("ms-diffusion-distance", "mass.unsteady", "Roughly how far, in mm, does a solute with D = {{D}} × 10⁻⁹ m²/s spread in {{t}} using $L \\approx \\sqrt{Dt}$?",
                   cases=[{"t": "one minute", "s": 60}, {"t": "one hour", "s": 3600}, {"t": "one day", "s": 86400}], given={"D": {"pick": [0.5, 1, 2]}},
                   value="sqrt(D*1e-9*s)*1000", tex="L", verify="Max(*solve(Eq((x/1000)**2, nsimplify(D)/10**9*s), x))", explain="Diffusion distance grows as √t: a day only gets you about ten times further than fifteen minutes"),
    (3, 1, "B"): Q("ms-uptake-time", "mass.unsteady", "A deep liquid with D = {{D}} × 10⁻⁹ m²/s takes up gas held at the surface at {{c0}} mol/m³. How long, in s, until {{m}} mmol/m² has been absorbed?",
                   given={"D": {"pick": [1, 2]}, "c0": {"pick": [10, 40]}, "m": {"pick": [1, 5, 10]}}, value="pi*((m/1000)/(2*c0))^2/(D*1e-9)", tex="t",
                   verify="solve(Eq(2*c0*sqrt(nsimplify(D)/10**9*x/pi), Rational(m, 1000)), x)[0]", explain="Uptake grows as √t, so absorbing twice as much takes four times as long"),
    (3, 1, "C"): Q("ms-slab-time-scaling", "mass.unsteady", "A slab dries by diffusion. If its thickness changes by a factor {{f}} and the diffusivity by {{g}}, by what factor does the time to reach the same average content change?",
                   given={"f": {"pick": [0.5, 2, 3]}, "g": {"pick": [0.5, 2, 4]}}, value="f^2/g", tex="t_2/t_1", verify="nsimplify(f)**2/nsimplify(g)",
                   explain="Every diffusion time scales with L²/D; that is the whole of the dimensional argument"),
    (4, 1, "A"): Q("ms-liquid-coefficient-reverse", "mass.interphase", "An absorber has measured $K_y$ = {{K}} and gas-film $k_y$ = {{ky}} mol/(m²·s), with equilibrium slope m = {{m}}. What liquid-film $k_x$, in mol/(m²·s), does that imply?",
                   given={"K": {"pick": [0.5, 1, 2]}, "ky": {"pick": [3, 5, 10]}, "m": {"pick": [0.5, 2, 5]}}, value="m/(1/K - 1/ky)", tex="k_x",
                   verify="solve(Eq(1/nsimplify(K), 1/nsimplify(ky) + nsimplify(m)/x), x)[0]", explain="Resistances add; subtract the gas film from the overall to find the liquid film"),
    (4, 1, "B"): Q("ms-controlling-film", "mass.interphase", "With $k_y$ = {{ky}}, $k_x$ = {{kx}} mol/(m²·s) and m = {{m}}, which film controls (holds over 80% of the resistance)?",
                   given={"ky": {"pick": [1, 5, 20]}, "kx": {"pick": [1, 5, 20]}, "m": {"pick": [0.01, 1, 50]}},
                   choice=["Gas film controls", "Liquid film controls", "Neither (both matter)"],
                   correct="(1/ky)/(1/ky + m/kx) > 0.8 ? 0 : ((m/kx)/(1/ky + m/kx) > 0.8 ? 1 : 2)",
                   verify="0 if (1/nsimplify(ky))/(1/nsimplify(ky) + nsimplify(m)/nsimplify(kx)) > Rational(8, 10) else (1 if (nsimplify(m)/nsimplify(kx))/(1/nsimplify(ky) + nsimplify(m)/nsimplify(kx)) > Rational(8, 10) else 2)",
                   explain="Very soluble gases (small m, e.g. NH₃ in water) are gas-film controlled; sparingly soluble ones (large m, e.g. O₂) are liquid-film controlled"),
    (4, 1, "C"): Q("ms-stagnant-sphere", "mass.interphase", "A sphere {{d}} mm across dissolves in perfectly still water (D = {{D}} × 10⁻⁹ m²/s). What mass-transfer coefficient applies, in μm/s?",
                   given={"d": {"pick": [0.1, 0.5, 1, 2]}, "D": {"pick": [0.8, 1, 1.5]}}, value="2*D*1e-9/(d/1000)*1e6", tex="k_c",
                   verify="integrate(1/(4*pi*Symbol('rr')**2), (Symbol('rr'), Rational(1, 2)*nsimplify(d)/1000, oo))**-1/(4*pi*(nsimplify(d)/2000)**2)*nsimplify(D)/10**9*10**6",
                   explain="Sh = 2 is the pure-diffusion limit (Re → 0): steady diffusion from a sphere into an infinite medium, the floor that every sphere correlation starts from"),
    (4, 1, "D"): Q("ms-model-exponent", "mass.interphase", "Changing the solute raises D by a factor {{f}} and the measured k by {{g}}. What exponent n in k ∝ Dⁿ does that give?",
                   cases=[{"f": 2, "g": 1.414}, {"f": 4, "g": 2.52}, {"f": 2, "g": 2}, {"f": 3, "g": 1.732}, {"f": 4, "g": 4}], value="log(g)/log(f)", tex="n",
                   verify="solve(Eq(nsimplify(f)**x, nsimplify(g)), x)[0]", explain="n ≈ 1 points to film theory, ½ to penetration or surface renewal, ⅔ to a laminar boundary layer"),
    (4, 1, "E"): Q("ms-colburn-ntu", "mass.interphase", "A dilute absorber with solute-free liquid takes y from {{y1}} to {{y2}}; equilibrium y = {{m}}x and absorption factor A = L/(mG) = {{Af}}. What is N_OG?",
                   given={"y1": {"pick": [0.02, 0.05]}, "y2": {"pick": [0.001, 0.002]}, "m": {"pick": [0.5, 1]}, "Af": {"pick": [1.25, 1.5, 2]}},
                   value="log((1 - 1/Af)*y1/y2 + 1/Af)/(1 - 1/Af)", tex="N_{OG}",
                   verify="integrate(1/(Symbol('yy') - nsimplify(m)*(Symbol('yy') - nsimplify(y2))/(nsimplify(Af)*nsimplify(m))), (Symbol('yy'), nsimplify(y2), nsimplify(y1)))",
                   explain="The Colburn equation is the integral of dy/(y − y*) along straight operating and equilibrium lines; A near 1 makes N_OG blow up"),
    (5, 1, "A"): Q("ms-trace-mixture-d", "mass.diffusivity", "A trace of A diffuses in a B–C mixture with B:C = {{b}}:{{c}} by moles; $D_{AB}$ = {{dab}} and $D_{AC}$ = {{dac}} cm²/s. What is $D_{Am}$?",
                   given={"b": {"pick": [1, 2, 3]}, "c": {"pick": [1, 2]}, "dab": {"pick": [0.1, 0.2]}, "dac": {"pick": [0.3, 0.6]}}, value="1/((b/(b + c))/dab + (c/(b + c))/dac)", tex="D_{Am}",
                   verify="limit((1 - Symbol('xa'))/((1 - Symbol('xa'))*Rational(b, b + c)/nsimplify(dab) + (1 - Symbol('xa'))*Rational(c, b + c)/nsimplify(dac)), Symbol('xa'), 0)",
                   explain="At trace levels Wilke's formula is a harmonic mean weighted by the solvent's own composition"),
    (5, 1, "B"): Q("ms-membrane-permeate", "mass.steady", "A membrane with ideal O₂/N₂ selectivity {{al}} is fed air (21% O₂) at a very high pressure ratio and low recovery. What is the O₂ mole fraction in the permeate?",
                   given={"al": {"pick": [2, 4, 6, 8]}}, value="al*0.21/(1 + (al - 1)*0.21)", tex="y_{O_2}",
                   verify="solve(Eq(x/(1 - x), nsimplify(al)*Rational(21, 79)), x)[0]", explain="With the permeate pressure negligible, the flux ratio is the permeability ratio times the feed partial-pressure ratio. Real modules fall short because of finite pressure ratio and stage cut"),
}
for u in UNITS:
    for tn, (_, los) in enumerate(u.topics, 1):
        for lo in los:
            q = SECOND.get((u.n, tn, lo.id))
            if q is not None:
                lo.qs.append(q)
