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
