"""Electric double layers (framework electric-double-layers, EL) on Petsev, van Swol and Frink, Molecular Theory of
Electric Double Layers (IOP, 2021). Units follow the book's parts: foundations (ch 1-2), continuum theory (ch 3),
liquid-state theory (ch 4-5), density functional theory (ch 6-7), molecular structure of the EDL (ch 8-13) and
simulation and numerics (ch 14-16, appendix A). Calculations are recomputed in tests/verify/edlcalc.py or by sympy
along another route; the results chapters (8-13) are conceptual multiple choice drawn from the book's conclusions."""
from opl_dsl import Q, L, U

FW, FILE, IDEA = "EL", "el-edl", "PB"
C = lambda *ch: [f"petsev-edl:{c}" for c in ch]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
# constants (SI), the same in the card value (mathjs) and the verifier (exact decimals)
E, KB, NA, EPS0, T = "1.602176634e-19", "1.380649e-23", "6.02214076e23", "8.8541878128e-12", "298.15"
e_, kb_, na_, ep_, T_ = (f"Rational('{v}')" for v in (E, KB, NA, EPS0, T))
KT = f"({KB}*{T})"
kT_ = f"({kb_}*{T_})"
CONSTS = "(e = 1.602 × 10⁻¹⁹ C, k_B = 1.381 × 10⁻²³ J/K, ε₀ = 8.854 × 10⁻¹² F/m, N_A = 6.022 × 10²³)"


def facts(name, skill, prompt, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


# Debye length for a z:z salt at molarity c, relative permittivity er, 25 °C
def debye(c="c", z="z", er="er", sym=False):
    if sym:
        return f"sqrt({er}*{ep_}*{kT_}/(2*{na_}*nsimplify({c})*1000*({z}*{e_})**2))"
    return f"sqrt({er}*{EPS0}*{KT}/(2*{NA}*{c}*1000*({z}*{E})^2))"


UNITS = [
U(1, "el-foundations", "Foundations: fields, the double layer and the origin of surface charge (ch. 1–2)", [("Charges, fields and the double-layer concept", [
    L("A", "Compute the Coulomb force between ions in a dielectric.", "F = z₁z₂e²/(4πεε₀r²); water's ε ≈ 78 cuts it about 80-fold.", [], [
        Q("el-coulomb-force", "edl.foundations", "Two ions of charge numbers {{z1}} and {{z2}} sit {{r}} nm apart in {{med}} (ε = {{er}}). What is the magnitude of the force between them, in pN? " + CONSTS,
          cases=[{"med": "water", "er": 78.4}, {"med": "methanol", "er": 32.7}, {"med": "vacuum", "er": 1}], given={"z1": {"pick": [1, 2]}, "z2": {"pick": [-1, -2, 1]}, "r": {"pick": [0.5, 1, 2]}},
          value=f"abs(z1*z2)*{E}^2/(4*pi*er*{EPS0}*(r*1e-9)^2)*1e12", tex="F",
          verify=f"Abs(z1*z2)*{e_}**2/(4*pi*nsimplify(er)*{ep_}*(nsimplify(r)/10**9)**2)*10**12",
          explain="Coulomb's law (1.1) with k_e = 1/(4πεε₀): the solvent's permittivity is what lets ions separate in water at all")], std=C(1)),
    L("B", "Relate surface charge to the field at the surface and treat the Helmholtz layer as a capacitor.", "Gauss: E = σ/(εε₀) at a charged wall; Helmholtz: C = εε₀/d.", [], [
        Q("el-helmholtz-capacitance", "edl.foundations", "A Helmholtz layer {{d}} nm thick has an inner dielectric constant of {{er}}. What capacitance per area does the parallel-plate model give, in μF/cm²? " + CONSTS,
          given={"d": {"pick": [0.3, 0.5, 1]}, "er": {"pick": [6, 10, 30]}}, value=f"er*{EPS0}/(d*1e-9)*100", tex="C_H",
          verify=f"nsimplify(er)*{ep_}/(nsimplify(d)/10**9)*100", explain="Helmholtz pictured all counterions on one plane: a molecular capacitor. Reduced permittivity of oriented water near the wall (ε ~ 6–10) gives the tens of μF/cm² seen at electrodes"),
        Q("el-surface-field", "edl.foundations", "A surface carries {{s}} μC/cm² in contact with water (ε = 78.4). What electric field acts in the liquid right at the surface, in MV/m? " + CONSTS,
          given={"s": {"pick": [1, 5, 10, 20]}}, value=f"s*1e-2/(78.4*{EPS0})/1e6", tex="E",
          verify=f"solve(Eq(nsimplify(s)/100, Rational(784, 10)*{ep_}*x*10**6), x)[0]", explain="σ = −εε₀(∇ψ·n) (equation 1.10): even modest surface charges give fields of tens of MV/m, which is why the first water layers orient")], std=C(1)),
    L("C", "Use the Schulze–Hardy rule.", "Critical coagulation concentration ∝ z⁻⁶ for highly charged particles, ∝ z⁻² at low potential.", [], [
        Q("el-schulze-hardy", "edl.foundations", "Compared with a monovalent counterion, by what factor is the critical coagulation concentration lower for a counterion of valence {{z}}, for {{reg}}?",
          cases=[{"reg": "strongly charged particles (z⁻⁶ law)", "n": 6}, {"reg": "particles at low surface potential (z⁻² law)", "n": 2}], given={"z": {"pick": [2, 3]}},
          value="z^n", tex="CCC_1/CCC_z", final=True, verify="z**n", explain="DLVO reproduces both laws (chapter 1): z⁻⁶ when the surface potential is saturated, z⁻² when the Debye–Hückel limit applies")], std=C(1)),
    L("D", "Place electrolyte models in the book's hierarchy.", "Primitive: ions in a dielectric continuum. Semi-primitive: explicit neutral solvent spheres. Civilized: explicit dipolar solvent.", [], [
        facts("el-model-hierarchy", "edl.foundations", "{{q}}", [
            ("Ions as charged spheres in a structureless dielectric continuum. Which model class?", "Primitive", "Semi-primitive", "Civilized", "Gouy–Chapman only"),
            ("Ions and neutral solvent spheres with excluded volume and van der Waals attraction, but no solvent dipoles. Which model class?", "Semi-primitive", "Primitive", "Civilized", "Helmholtz"),
            ("Ions and solvent molecules carrying dipoles, so ion–dipole and dipole–dipole forces act. Which model class?", "Civilized", "Semi-primitive", "Primitive", "Restricted primitive"),
            ("Which early model first added a layer of finite-size ions with specific adsorption next to the wall, keeping Gouy–Chapman beyond it?", "Stern", "Helmholtz", "Debye–Hückel", "Ornstein–Zernike"),
            ("Who first analysed neutral solvent molecules in the layer next to the wall?", "Grahame", "Gouy", "Chapman", "Verwey"),
        ], "The book's argument is that the solvent, usually far denser than the ions, sets the structure near the wall: only semi-primitive and civilized models can show it")], p="P2", std=C(1)),
]), ("Charge regulation and adsorption", [
    L("A", "Compute the Nernst potential of a charge-regulating surface.", "ψ_N = (ln 10 kT/e)(pI − pH_b): about 59.2 mV per pH unit at 25 °C.", [], [
        Q("el-nernst-potential", "edl.foundations", "A surface has its isoelectric point at pI = {{pI}} and the bulk pH is {{pH}}. What is the Nernst potential ψ_N at 25 °C, in mV? " + CONSTS,
          given={"pI": {"pick": [2, 4, 7, 9]}, "pH": {"pick": [3, 5, 7.5, 10]}}, require=["pI != pH"], value=f"log(10)*{KT}/{E}*(pI - pH)*1000", tex="\\psi_N",
          verify=f"log(10)*{kT_}/{e_}*(nsimplify(pI) - nsimplify(pH))*1000", explain="Equation (2.7): the PDI concentration sets ψ_N. A real surface reaches only part of it because its charge also depends on site density and the double layer (charge regulation)")], std=C(2)),
    L("B", "Use the low-potential charge-regulation law.", "For δ ≪ 1: σ = e²Γδ(ψ_N − ψ_s)/kT.", [], [
        Q("el-regulation-linear", "edl.foundations", "A surface has Γ = {{G}} sites/nm² and δ = 2√(K₋/K₊) = {{d}}. With ψ_N − ψ_s = {{dp}} mV, what surface charge does the linear regulation law give, in μC/cm²? " + CONSTS,
          given={"G": {"pick": [2, 5, 8]}, "d": {"pick": [0.01, 0.05, 0.1]}, "dp": {"pick": [-40, -20, 20, 40]}}, value=f"{E}^2*G*1e18*d*dp/1000/{KT}*100", tex="\\sigma",
          verify=f"{e_}*nsimplify(G)*10**18*nsimplify(d)*diff(sinh(Symbol('u')), Symbol('u')).subs(Symbol('u'), 0)*{e_}*nsimplify(dp)/1000/{kT_}*100", explain="Equation (2.9) is the small-argument limit of σ = eΓδ sinh[e(ψ_N − ψ_s)/kT]: the charge follows the potential difference linearly (the small-argument limit of the sinh law)")], std=C(2)),
    L("C", "Compute Stern-layer occupancy from a modified Langmuir isotherm.", "θ = K/(1 + K), K = v₀ρ exp[(−φ − zeψ_St)/kT].", [], [
        Q("el-stern-langmuir", "edl.foundations", "An ion with charge number {{z}} adsorbs at a Stern plane at potential {{psi}} mV. Its non-electrostatic adsorption energy is {{phi}} kT and v₀ρ = {{vr}}. What fraction of Stern sites does it occupy (one species, 25 °C)? " + CONSTS,
          given={"z": {"pick": [1, -1, 2]}, "psi": {"pick": [-50, -25, 25]}, "phi": {"pick": [-3, -1, 0]}, "vr": {"pick": [0.001, 0.01, 0.05]}},
          value=f"vr*exp(-phi - z*{E}*psi/1000/{KT})/(1 + vr*exp(-phi - z*{E}*psi/1000/{KT}))", tex="\\theta",
          verify=f"solve(Eq(x/(1 - x), nsimplify(vr)*exp(-phi - z*{e_}*nsimplify(psi)/1000/{kT_})), x)[0]",
          explain="Equation (2.13): specific (non-Coulombic) attraction and the Stern potential both enter the Boltzmann factor; counterions crowd a strongly charged plane")], std=C(2)),
])]),
U(2, "el-continuum", "Continuum theory: Poisson–Boltzmann, interactions and electrokinetics (ch. 3)", [("The single flat double layer", [
    L("A", "Compute the Debye screening length.", "κ² = 2ρ₀q²/(εε₀kT); κ⁻¹ ≈ 0.304/√c nm for 1:1 salt in water at 25 °C.", [], [
        Q("el-debye-length", "edl.continuum", "What is the Debye length of a {{z}}:{{z}} salt at {{c}} mol/L in water (ε = 78.4) at 25 °C, in nm? " + CONSTS,
          given={"z": {"pick": [1, 2]}, "c": {"pick": [0.001, 0.01, 0.1]}}, value=debye(er="78.4") + "*1e9", tex="\\kappa^{-1}",
          verify=f"1/sqrt(2*{na_}*nsimplify(c)*1000*(z*{e_})**2/(Rational(784, 10)*{ep_}*{kT_}))*10**9",
          explain="Screening length falls as 1/(z√c): 9.6 nm at 1 mM 1:1, 0.96 nm at 0.1 M. It is the one length scale of the continuum theory")], std=C(3)),
    L("B", "Relate surface charge to surface potential with the Grahame equation.", "σ̃ = 2 sinh(ψ̃_s/2), i.e. σ = √(8εε₀ρ₀kT) sinh(eψ_s/2kT) for 1:1.", [], [
        Q("el-grahame", "edl.continuum", "A flat surface sits at ψ_s = {{psi}} mV in {{c}} M 1:1 salt (ε = 78.4, 25 °C). What surface charge does Gouy–Chapman give, in μC/cm²? " + CONSTS,
          given={"psi": {"pick": [25, 50, 100, 150]}, "c": {"pick": [0.001, 0.01, 0.1]}},
          value=f"sqrt(8*78.4*{EPS0}*c*1000*{NA}*{KT})*sinh({E}*psi/1000/(2*{KT}))*100", tex="\\sigma",
          verify=f"Rational(784, 10)*{ep_}*({kT_}/{e_})*sqrt(2*{na_}*nsimplify(c)*1000*{e_}**2/(Rational(784, 10)*{ep_}*{kT_}))*sqrt(2*(cosh({e_}*nsimplify(psi)/1000/{kT_}) - 1))*100",
          explain="From the first integral (3.7): dψ̃/dz = −κ√(2(cosh ψ̃ − 1)) = −2κ sinh(ψ̃/2). Charge grows exponentially with potential once ψ̃_s > 2")], std=C(3)),
    L("C", "Evaluate the Gouy–Chapman potential profile.", "ψ̃(z) = 4 artanh[γ e^{−κz}], γ = tanh(ψ̃_s/4).", [], [
        Q("el-gouy-chapman-profile", "edl.continuum", "A flat double layer has reduced surface potential ψ̃_s = eψ_s/kT = {{ps}} (1:1 salt). What is ψ̃ at κz = {{kz}}?",
          given={"ps": {"pick": [1, 2, 4, 6]}, "kz": {"pick": [0.5, 1, 2, 3]}}, value="4*atanh(tanh(ps/4)*exp(-kz))", tex="\\tilde\\psi",
          verify="edl_gc_psi(ps, kz)", explain="Far out the profile decays like 4γ e^{−κz}: a highly charged wall looks, from afar, like one at ψ̃ = 4 at most (potential saturation)")], std=C(3)),
    L("D", "Judge the error of the linearised (Debye–Hückel) profile.", "Linear: ψ̃ = ψ̃_s e^{−κz}; error = (exact − linear)/exact.", [], [
        Q("el-linear-error", "edl.continuum", "For ψ̃_s = {{ps}}, by what percentage does the linear Debye–Hückel profile ψ̃_s e^{−κz} misstate the exact Gouy–Chapman potential at κz = {{kz}}? (Give (exact − linear)/exact × 100.)",
          given={"ps": {"pick": [1, 2, 4]}, "kz": {"pick": [0.5, 1, 2, 4]}}, value="(4*atanh(tanh(ps/4)*exp(-kz)) - ps*exp(-kz))/(4*atanh(tanh(ps/4)*exp(-kz)))*100", tex="\\text{Error}",
          verify="(edl_gc_psi(ps, kz) - ps*exp(-kz))/edl_gc_psi(ps, kz)*100",
          explain="Equation (3.15): the linear theory overshoots near a highly charged wall (negative error) and undershoots far away (positive), because nonlinear screening is stronger close in")], std=C(3)),
]), ("Interacting and curved double layers", [
    L("A", "Find the double-layer pressure from the midplane potential.", "Π = 2ρ₀kT[cosh ψ̃_m − 1] for a symmetric 1:1 gap.", [], [
        Q("el-midplane-pressure", "edl.continuum", "Between two identical plates in {{c}} M 1:1 salt at 25 °C, the reduced midplane potential is ψ̃_m = {{pm}}. What is the disjoining pressure, in kPa? " + CONSTS,
          given={"c": {"pick": [0.001, 0.01, 0.1]}, "pm": {"pick": [0.1, 0.5, 1, 2]}}, value=f"2*c*1000*{NA}*{KT}*(cosh(pm) - 1)/1000", tex="\\Pi",
          verify=f"integrate(2*nsimplify(c)*1000*{na_}*{kT_}*sinh(Symbol('pp')), (Symbol('pp'), 0, nsimplify(pm)))/1000",
          explain="At the midplane the field vanishes, so the pressure is just the excess osmotic pressure of the ions there (3.25): the mutual repulsion is an osmotic effect")], std=C(3)),
    L("B", "Use the weak-overlap approximation.", "Π ≈ 64ρ₀kT γ² e^{−κh}: superpose the two isolated profiles at the midplane.", [], [
        Q("el-weak-overlap", "edl.continuum", "Two plates at ψ̃_s = {{ps}} face each other at κh = {{kh}} in 1:1 salt. What is the weak-overlap pressure, in units of ρ₀kT?",
          given={"ps": {"pick": [1, 2, 4, 8]}, "kh": {"pick": [2, 3, 5]}}, value="64*tanh(ps/4)^2*exp(-kh)", tex="\\Pi/\\rho_0 kT",
          verify="(2*4*tanh(nsimplify(ps)/4)*exp(-nsimplify(kh)/2))**2",
          explain="Each plate alone contributes 4γ e^{−κh/2} at the midplane; doubling it and using cosh ψ̃_m − 1 ≈ ψ̃_m²/2 gives 64γ².")], std=C(3)),
    L("C", "Track the charge of plates held at constant potential as they approach.", "Linear PB: σ̃ = ψ̃_s tanh(κh/2) per plate.", [], [
        Q("el-constant-potential-charge", "edl.continuum", "Two plates held at the same low potential approach to κh = {{kh}}. What fraction of its isolated-plate charge does each keep (linear PB)?",
          given={"kh": {"pick": [0.5, 1, 2, 4]}}, value="tanh(kh/2)", tex="\\sigma(h)/\\sigma(\\infty)",
          verify="(-diff(cosh(Symbol('zz') - nsimplify(kh)/2)/cosh(nsimplify(kh)/2), Symbol('zz')).subs(Symbol('zz'), 0))",
          explain="At constant potential the surfaces shed charge as the layers overlap; at constant charge the potential rises instead. Real surfaces regulate in between")], std=C(3)),
    L("D", "Compute the charge on a weakly charged sphere.", "Debye–Hückel sphere: σ = εε₀ψ_s(1 + κR)/R.", [], [
        Q("el-sphere-charge", "edl.continuum", "A sphere of radius {{R}} nm at ψ_s = {{psi}} mV sits in salt with κ⁻¹ = {{kd}} nm (ε = 78.4). What surface charge does the linearised theory give, in μC/cm²? " + CONSTS,
          given={"R": {"pick": [2, 10, 100]}, "psi": {"pick": [10, 20]}, "kd": {"pick": [1, 3, 10]}}, value=f"78.4*{EPS0}*psi/1000*(1 + R/kd)/(R*1e-9)*100", tex="\\sigma",
          verify=f"-Rational(784, 10)*{ep_}*diff(nsimplify(psi)/1000*Rational(R, 10**9)/Symbol('rr')*exp(-(Symbol('rr') - Rational(R, 10**9))/(nsimplify(kd)/10**9)), Symbol('rr')).subs(Symbol('rr'), Rational(R, 10**9))*100",
          explain="Curvature adds the 1/R term: small particles need less charge for the same potential, and as κR → ∞ the flat-plate result σ = εε₀κψ_s returns")], std=C(3)),
    L("E", "Convert plate interactions to sphere interactions with the Derjaguin approximation.", "F(h) = 2π[R₁R₂/(R₁ + R₂)] f(h): πR f for equal spheres.", [], [
        Q("el-derjaguin-force", "edl.continuum", "Two flat surfaces have interaction free energy {{f}} mJ/m² at separation h. What force, in nN, acts between spheres of radii {{R1}} and {{R2}} μm at the same closest separation?",
          given={"f": {"pick": [0.1, 0.5, 2]}, "R1": {"pick": [0.5, 1, 5]}, "R2": {"pick": [1, 5, 1000000]}}, value="2*pi*R1*R2/(R1 + R2)*1e-6*f*1e-3*1e9", tex="F",
          verify="2*pi*(1/(1/nsimplify(R1) + 1/nsimplify(R2)))/10**6*nsimplify(f)/1000*10**9",
          explain="Equations (3.61)–(3.63): valid when the range of the force is small compared with the radii. A sphere near a flat wall (R₂ → ∞) gets 2πR")], std=C(3)),
    L("F", "Combine van der Waals and double-layer terms in DLVO.", "Sphere–sphere van der Waals at short range: Φ = −A R₁R₂/[6h(R₁ + R₂)].", [], [
        Q("el-vdw-spheres", "edl.continuum", "Two spheres of radius {{R}} nm with Hamaker constant {{A}} × 10⁻²⁰ J are {{h}} nm apart (h ≪ R). What is their van der Waals energy, in kT at 25 °C? " + CONSTS,
          given={"R": {"pick": [50, 100, 500]}, "A": {"pick": [0.5, 1, 4]}, "h": {"pick": [1, 2, 5]}}, value=f"-A*1e-20*R/(12*h)/{KT}", tex="\\Phi_{vdW}",
          verify=f"2*pi*(nsimplify(R)/2)*integrate(-nsimplify(A)/10**20/(12*pi*Symbol('zz')**2), (Symbol('zz'), nsimplify(h), oo))/{kT_}",
          explain="Integrating the plate law −A/(12πh²) with Derjaguin's weighting gives −AR/(12h) for equal spheres; DLVO adds the double-layer repulsion to this (3.70)")], std=C(3)),
]), ("Beyond Boltzmann and electrokinetics", [
    L("A", "Compute electroosmotic and electrophoretic speeds.", "Smoluchowski: v = εε₀ζE/η (κR ≫ 1). Hückel: v = 2εε₀ζE/(3η) (κR ≪ 1).", [], [
        Q("el-electrophoresis", "edl.continuum", "A particle with ζ = {{z}} mV moves in water (ε = 78.4, η = 0.89 mPa·s) under {{E}} V/cm. Using the {{lim}} limit, what is its speed, in μm/s? " + CONSTS,
          cases=[{"lim": "Smoluchowski (κR ≫ 1)", "f": 1}, {"lim": "Hückel (κR ≪ 1)", "f": 0.6666666666666666}], given={"z": {"pick": [-50, -25, 30]}, "E": {"pick": [5, 10, 20]}},
          value=f"f*78.4*{EPS0}*abs(z)/1000*E*100/0.89e-3*1e6", tex="v",
          verify=f"nsimplify(f, tolerance=1e-12)*Rational(784, 10)*{ep_}*Abs(z)/1000*E*100/Rational(89, 10**5)*10**6",
          explain="Henry's function f_H(κR) interpolates between 2/3 (Hückel) and 1 (Smoluchowski); both assume the double layer is not polarised by the field")], std=C(3)),
    L("B", "Choose the right electrokinetic limit.", "κR ≫ 1: Smoluchowski. κR ≪ 1: Hückel. In between: Henry; with strong polarisation (large ζ, thin layers): the full electrokinetic equations.", [], [
        Q("el-ek-limit", "edl.continuum", "A particle of radius {{R}} nm is in salt with Debye length {{kd}} nm. Which limit applies?",
          given={"R": {"pick": [2, 20, 500, 5000]}, "kd": {"pick": [1, 10, 30]}}, require=["abs(log10(R/kd)) > 1"],
          choice=["Smoluchowski (κR ≫ 1)", "Hückel (κR ≪ 1)"], correct="R/kd > 1 ? 0 : 1", verify="0 if Rational(R, 1)/kd > 1 else 1",
          explain="Compare the particle with the double layer: a thin layer hugging a big particle behaves like flat-wall electroosmosis seen in reverse")], p="P2", std=C(3)),
    L("C", "Know when Boltzmann statistics fail for charge carriers.", "Degenerate carriers follow Fermi–Dirac; the crossover is the Fermi temperature T_F = ħ²(3π²N)^{2/3}/(2m*k_B).", [], [
        Q("el-fermi-temperature", "edl.continuum", "A doped semiconductor has carrier density {{N}} × 10²⁴ m⁻³ and effective mass {{mr}} m_e. What is its Fermi temperature, in K? (ħ = 1.0546 × 10⁻³⁴ J·s, m_e = 9.109 × 10⁻³¹ kg, k_B = 1.381 × 10⁻²³ J/K)",
          given={"N": {"pick": [0.1, 1, 10]}, "mr": {"pick": [0.07, 0.26, 1]}}, value=f"(1.054571817e-34)^2*(3*pi^2*N*1e24)^(2/3)/(2*mr*9.1093837e-31*{KB})", tex="T_F",
          verify=f"Rational('1.054571817e-34')**2*(3*pi**2*nsimplify(N)*10**24)**Rational(2, 3)/(2*nsimplify(mr)*Rational('9.1093837e-31')*{kb_})",
          explain="Well above T_F the Fermi integral reduces to the Boltzmann exponential (3.78), and the space-charge layer obeys PB; below it, degeneracy matters")], std=C(3)),
])]),
U(3, "el-liquid-state", "Liquid-state theory: correlation functions, closures and perturbation theory (ch. 4–5)", [("Integral equations", [
    L("A", "Use the Ornstein–Zernike equation in Fourier space.", "ĥ = ĉ/(1 − ρĉ); S(0) = 1/(1 − ρĉ(0)) is the reduced compressibility.", [], [
        Q("el-oz-structure-factor", "edl.liquid-state", "A fluid has ρĉ(k = 0) = {{rc}}. What is its structure factor S(0) = 1 + ρĥ(0)?",
          given={"rc": {"pick": [-20, -5, -1, 0.5]}}, value="1/(1 - rc)", tex="S(0)", verify="1 + nsimplify(rc)/(1 - nsimplify(rc))",
          explain="The OZ convolution becomes a product in k-space (4.5). Dense liquids have large negative ρĉ(0) and small S(0): they are nearly incompressible")], std=C(4)),
    L("B", "Compare the hard-sphere equations of state.", "PY virial (1 + 2η + 3η²)/(1 − η)²; PY compressibility (1 + η + η²)/(1 − η)³; Carnahan–Starling (1 + η + η² − η³)/(1 − η)³.", [], [
        Q("el-hs-pressure", "edl.liquid-state", "What is βp/ρ for hard spheres at packing fraction η = {{eta}} from the {{route}}?",
          cases=[{"route": "PY virial route", "w": 0}, {"route": "PY compressibility route", "w": 1}, {"route": "Carnahan–Starling equation", "w": 2}], given={"eta": {"pick": [0.1, 0.3, 0.45]}},
          value="w == 0 ? (1 + 2*eta + 3*eta^2)/(1 - eta)^2 : (w == 1 ? (1 + eta + eta^2)/(1 - eta)^3 : (1 + eta + eta^2 - eta^3)/(1 - eta)^3)", tex="\\beta p/\\rho",
          verify="1 + 4*nsimplify(eta)*(1 + nsimplify(eta)/2)/(1 - nsimplify(eta))**2 if w == 0 else ((1 + nsimplify(eta) + nsimplify(eta)**2)/(1 - nsimplify(eta))**3 if w == 1 else (1 + nsimplify(eta) + nsimplify(eta)**2 - nsimplify(eta)**3)/(1 - nsimplify(eta))**3)",
          explain="The virial route is 1 + 4ηg(d) with the PY contact value (1 + η/2)/(1 − η)²; the two PY routes disagree, and Carnahan–Starling sits between them, close to simulation")], std=C(4)),
    L("C", "Recognise the common closures.", "PY: c = g(1 − e^{βφ}). HNC: c = h − ln y (i.e. g − 1 − ln y). MSA: g = 0 inside the core, c = −βφ outside.", [], [
        facts("el-closures", "edl.liquid-state", "{{q}}", [
            ("Which closure sets c(r) = −βφ(r) outside the core and g(r) = 0 inside?", "Mean spherical approximation (MSA)", "Percus–Yevick", "Hypernetted chain", "Debye–Hückel"),
            ("Which closure writes c(r) = g(r) − 1 − ln y(r)?", "Hypernetted chain (HNC)", "Percus–Yevick", "MSA", "Random phase approximation"),
            ("Which closure writes c(r) = f(r)y(r) and gives an analytic solution for hard spheres?", "Percus–Yevick (PY)", "HNC", "MSA", "Kirkwood superposition"),
            ("Why does the OZ equation need a closure at all?", "It relates two unknown functions, h and c", "It has no solution for hard spheres", "It ignores three-body correlations", "It only applies to ideal gases"),
        ], "For electrolytes, HNC handles the long-range Coulomb tail best; MSA gives analytic thermodynamics used later in DFT (section 7.4)")], p="P2", std=C(4)),
    L("D", "Compute packing fraction from number density and diameter.", "η = πρd³/6; ξ₃ for mixtures.", [], [
        Q("el-packing-fraction", "edl.liquid-state", "A solvent modelled as hard spheres of diameter {{d}} nm has number density {{rho}} nm⁻³. What is its packing fraction?",
          given={"d": {"pick": [0.28, 0.3, 0.425]}, "rho": {"pick": [10, 20, 33.4]}}, require=["pi*rho*d^3/6 < 0.6"], value="pi*rho*d^3/6", tex="\\eta",
          verify="integrate(4*pi*Symbol('rr')**2, (Symbol('rr'), 0, nsimplify(d)/2))*nsimplify(rho)", explain="η is the fraction of space filled; liquids sit near 0.4–0.5 and hard spheres freeze above 0.494")], std=C(4)),
]), ("Virial, perturbation and mean-field theory", [
    L("A", "Compute second virial coefficients.", "B₂ = −2π∫(e^{−βφ} − 1)r²dr: 2πd³/3 for hard spheres; square well B₂ = B₂^hs[1 − (λ³ − 1)(e^{βε} − 1)].", [], [
        Q("el-b2-square-well", "edl.liquid-state", "A square-well fluid has core diameter d, well width λ = {{lam}} and depth βε = {{be}}. What is B₂ in units of the hard-sphere value 2πd³/3?",
          given={"lam": {"pick": [1.2, 1.5, 2]}, "be": {"pick": [0.2, 0.5, 1]}}, value="1 - (lam^3 - 1)*(exp(be) - 1)", tex="B_2/B_2^{hs}",
          verify="(-2*pi*(integrate(-Symbol('rr')**2, (Symbol('rr'), 0, 1)) + integrate((exp(nsimplify(be)) - 1)*Symbol('rr')**2, (Symbol('rr'), 1, nsimplify(lam)))))/(2*pi/3)",
          explain="The core adds excluded volume, the well subtracts with weight e^{βε} − 1; B₂ changes sign at the Boyle temperature")], std=C(5)),
    L("B", "Use the van der Waals equation in reduced form.", "p̃ = 8ρ̃T̃/(3 − ρ̃) − 3ρ̃².", [], [
        Q("el-vdw-reduced", "edl.liquid-state", "In reduced van der Waals units, what is p̃ at ρ̃ = {{r}} and T̃ = {{t}}?",
          given={"r": {"pick": [0.5, 1, 1.5, 2]}, "t": {"pick": [0.85, 0.95, 1, 1.1]}}, value="8*r*t/(3 - r) - 3*r^2", tex="\\tilde p",
          verify="(Symbol('rh')/(1 - Rational(1, 3)*Symbol('rh'))*Rational(8, 3)*nsimplify(t) - 3*Symbol('rh')**2).subs(Symbol('rh'), nsimplify(r))",
          explain="Mean-field attraction (−aρ²) on top of a hard-core pressure; below T̃ = 1 the isotherm has a loop, cured by the equal-area rule (5.41)")], std=C(5)),
    L("C", "Solve the mean-field (Weiss) equation of the Ising model.", "m = tanh(βJqm): a nonzero root exists below kT_c = Jq.", [], [
        Q("el-mean-field-m", "edl.liquid-state", "In the Weiss mean-field Ising model at zero field, what is the spontaneous magnetisation m at T/T_c = {{t}}?",
          cases=[{"t": 0.5, "m": 0.9575040240772688}, {"t": 0.8, "m": 0.7104117834878704}, {"t": 0.9, "m": 0.5254295126580087}, {"t": 0.3, "m": 0.9974138168919748}],
          value="m", tex="m", verify="edl_mf_m(t)",
          explain="A transcendental equation solved graphically or numerically (figure 5.7); near T_c, m ∝ (1 − T/T_c)^{1/2}, the mean-field exponent β = ½")], std=C(5)),
    L("D", "Use scaled-particle results for hard spheres.", "Probability of an empty cavity of radius σ/2: p₀ = 1 − η, so βW = −ln(1 − η); G(σ/2) = 1/(1 − η).", [], [
        Q("el-spt-cavity", "edl.liquid-state", "In a hard-sphere fluid at η = {{eta}}, what is the reversible work βW to open a cavity that excludes sphere centres from a radius σ/2?",
          given={"eta": {"pick": [0.1, 0.3, 0.45]}}, value="-log(1 - eta)", tex="\\beta W",
          verify="integrate(4*pi*Symbol('ll')**2*Symbol('rh')/(1 - Rational(4, 3)*pi*Symbol('rh')*Symbol('ll')**3), (Symbol('ll'), 0, Rational(1, 2))).subs(Symbol('rh'), 6*nsimplify(eta)/pi)",
          explain="Small cavities hold at most one centre, so p₀ is exact up to σ/2 (5.71); integrating ρG4πλ² reproduces −ln(1 − η)")], std=C(5)),
    L("E", "Use the exact one-dimensional hard-rod fluid.", "Tonks: βp/ρ = 1/(1 − ρσ).", [], [
        Q("el-tonks", "edl.liquid-state", "Hard rods of length σ on a line have linear density ρσ = {{rs}}. What is βp/ρ?",
          given={"rs": {"pick": [0.2, 0.5, 0.8, 0.9]}}, value="1/(1 - rs)", tex="\\beta p/\\rho", verify="1 + nsimplify(rs)*(1/(1 - nsimplify(rs)))",
          explain="Exact in 1D: the virial route βp/ρ = 1 + ρσG(σ) with G = (1 − ρσ)⁻¹ (5.102). No phase transition occurs in one dimension")], std=C(5)),
    L("F", "Split a pair potential for perturbation theory.", "WCA: split at the LJ minimum r_min = 2^{1/6}σ; Barker–Henderson: split at σ and use d = ∫₀^σ(1 − e^{−βφ})dr.", [], [
        Q("el-wca-split", "edl.liquid-state", "A Lennard-Jones fluid has σ = {{s}} nm. Where does the WCA theory split the potential into repulsive and attractive parts, in nm?",
          given={"s": {"pick": [0.3, 0.34, 0.425]}}, value="2^(1/6)*s", tex="r_{min}",
          verify="Max(*[q for q in solve(diff((nsimplify(s)/x)**12 - (nsimplify(s)/x)**6, x), x) if q.is_positive])",
          explain="WCA keeps all the repulsive force in the reference fluid, so the perturbation is smooth; first-order Zwanzig then works well (5.19)")], std=C(5)),
])]),
U(4, "el-dft", "Density functional theory for electrolytes (ch. 6–7)", [("DFT fundamentals", [
    L("A", "Minimise the ideal-gas functional in an external field.", "δΩ/δρ = 0 with F_id = kT∫ρ[ln(Λ³ρ) − 1] gives ρ(r) = ρ_b e^{−βV_ext(r)}.", [], [
        Q("el-ideal-functional", "edl.dft", "An ideal fluid feels an external potential of {{V}} kT at a point. What is its density there relative to the bulk?",
          given={"V": {"pick": [-2, -0.5, 1, 3]}}, value="exp(-V)", tex="\\rho/\\rho_b",
          verify="solve(Eq(log(x) + nsimplify(V), 0), x)[0]",
          explain="The Euler–Lagrange equation kT ln(Λ³ρ) + V_ext = μ: for point ions with V = zeψ this is the Boltzmann distribution behind Poisson–Boltzmann (7.15)")], std=C(6)),
    L("B", "Compute a surface excess adsorption.", "Γ^ex = ∫[ρ(r) − ρ_b]dr; for ρ = ρ_b(1 + A e^{−z/λ}), Γ^ex = ρ_bAλ.", [], [
        Q("el-surface-excess", "edl.dft", "Near a wall a species follows ρ(z) = ρ_b(1 + {{A}}e^{−z/λ}) with ρ_b = {{rb}} nm⁻³ and λ = {{lam}} nm. What is its surface excess, in nm⁻²?",
          given={"A": {"pick": [-0.5, 1, 3]}, "rb": {"pick": [0.06, 0.6, 33]}, "lam": {"pick": [0.3, 1, 2]}}, value="rb*A*lam", tex="\\Gamma^{ex}",
          verify="integrate(nsimplify(rb)*nsimplify(A)*exp(-Symbol('zz')/nsimplify(lam)), (Symbol('zz'), 0, oo))",
          explain="Equation (6.57); the Gibbs adsorption sum rule links it to −∂Ω^ex/∂μ (6.79), so DFT gives adsorption two ways that must agree")], std=C(6)),
    L("C", "Convert a pair correlation to a potential of mean force.", "W(r) = −kT ln g(r).", [], [
        Q("el-pmf", "edl.dft", "At some distance the radial distribution function is g = {{g}}. What is the potential of mean force there, in kJ/mol at 25 °C? (R = 8.314 J/mol·K)",
          given={"g": {"pick": [0.2, 0.8, 1.5, 3]}}, value="-8.314*298.15*log(g)/1000", tex="W", verify="-Rational(8314, 1000)*Rational(29815, 100)*log(nsimplify(g))/1000",
          explain="Fixing one particle as a 'wall' turns the density profile into g(r) (6.72); W includes all the averaged effects of the other molecules")], std=C(6)),
    L("D", "Relate wetting to interfacial free energies.", "Young: cos θ = (Ω^ex_WV − Ω^ex_WL)/γ_LV.", [], [
        Q("el-contact-angle", "edl.dft", "A wall–vapour excess free energy is {{wv}} mJ/m², the wall–liquid one {{wl}} mJ/m², and the liquid–vapour tension {{g}} mJ/m². What contact angle results, in degrees?",
          given={"wv": {"pick": [40, 60]}, "wl": {"pick": [20, 50, 70]}, "g": {"pick": [72, 50]}}, require=["abs(wv - wl) < g"], value="acos((wv - wl)/g)*180/pi", tex="\\theta",
          verify="Min(*[q for q in solve(Eq(cos(x*pi/180)*g, wv - wl), x) if q.is_positive])", explain="Equation (6.69): c-DFT gives all three excess free energies from density profiles, so solvophilic or solvophobic walls (chapter 10) come out of the model")], std=C(6)),
    L("E", "Scale the Thomas–Fermi kinetic energy.", "T_TF ∝ ∫ρ^{5/3}dr.", [], [
        Q("el-thomas-fermi-scaling", "edl.dft", "In Thomas–Fermi theory, by what factor does the kinetic-energy density change if the local electron density rises by a factor {{f}}?",
          given={"f": {"pick": [2, 3, 8]}}, value="f^(5/3)", tex="t_2/t_1", verify="nsimplify(f)**Rational(5, 3)",
          explain="The first orbital-free functional (6.8): kinetic energy written directly as a functional of density, the idea c-DFT inherits")], std=C(6)),
]), ("Classical DFT for electrolytes", [
    L("A", "Compute the Bjerrum length and Debye length from it.", "λ_B = e²/(4πεε₀kT) ≈ 0.71 nm in water; κ² = 4πλ_BΣz_i²ρ_i.", [], [
        Q("el-bjerrum", "edl.dft", "What is the Bjerrum length in a solvent with ε = {{er}} at 25 °C, in nm? " + CONSTS,
          given={"er": {"pick": [78.4, 32.7, 24.5, 2]}}, value=f"{E}^2/(4*pi*er*{EPS0}*{KT})*1e9", tex="\\lambda_B",
          verify=f"solve(Eq({e_}**2/(4*pi*nsimplify(er)*{ep_}*x/10**9), {kT_}), x)[0]", explain="The distance at which two unit charges interact with kT; in low-ε solvents it is long, and ions pair"),
        Q("el-debye-from-bjerrum", "edl.dft", "With Bjerrum length {{lb}} nm and a 1:1 salt at {{rho}} ion pairs per nm³, what is the Debye length, in nm?",
          given={"lb": {"pick": [0.7, 1.5]}, "rho": {"pick": [0.0006, 0.006, 0.06]}}, value="1/sqrt(4*pi*lb*2*rho)", tex="\\kappa^{-1}",
          verify=f"1/sqrt(2*nsimplify(rho)*10**27*(1*{e_})**2/((nsimplify(lb)/10**9*4*pi*{kT_}/{e_}**2)**-1*{kT_}))*10**9",
          explain="κ² = 4πλ_BΣz²ρ is the same screening as in chapter 3, rewritten with the Bjerrum length (equation 7.16 in reduced units)")], std=C(7)),
    L("B", "Apply the contact theorem at a charged wall.", "kTΣρ_i(0) = p_b + σ²/(2εε₀); for an ideal 1:1 bulk p_b = 2ρ₀kT.", [], [
        Q("el-contact-theorem", "edl.dft", "A wall with σ = {{s}} μC/cm² faces {{c}} M 1:1 point-ion salt (ε = 78.4, 25 °C). What is the total ion density at contact, in mol/L? " + CONSTS,
          given={"s": {"pick": [1, 5, 10]}, "c": {"pick": [0.01, 0.1]}}, value=f"(2*c*1000*{NA}*{KT} + (s/100)^2/(2*78.4*{EPS0}))/{KT}/{NA}/1000", tex="\\sum\\rho_i(0)",
          verify=f"2*nsimplify(c)*cosh(2*log((nsimplify(s)/100)/sqrt(8*Rational(784, 10)*{ep_}*nsimplify(c)*1000*{na_}*{kT_}) + sqrt(((nsimplify(s)/100)/sqrt(8*Rational(784, 10)*{ep_}*nsimplify(c)*1000*{na_}*{kT_}))**2 + 1)))",
          explain="Equation (7.21): the contact density balances the bulk pressure plus the Maxwell stress of the field. The check uses the Grahame surface potential and 2c cosh ψ̃_s, a different route")], std=C(7)),
    L("C", "Evaluate the Carnahan–Starling hard-sphere free energy.", "βf_ex = η(4 − 3η)/(1 − η)² per particle.", [], [
        Q("el-cs-free-energy", "edl.dft", "What is the Carnahan–Starling excess free energy per particle, in kT, at packing fraction η = {{eta}}?",
          given={"eta": {"pick": [0.1, 0.2, 0.3, 0.4]}}, value="eta*(4 - 3*eta)/(1 - eta)^2", tex="\\beta f_{ex}",
          verify="integrate(((1 + Symbol('ee') + Symbol('ee')**2 - Symbol('ee')**3)/(1 - Symbol('ee'))**3 - 1)/Symbol('ee'), (Symbol('ee'), 0, nsimplify(eta)))",
          explain="Integrating (Z − 1)/η from zero density gives (7.31), the local-density hard-sphere term the first electrolyte DFTs used before FMT")], std=C(7)),
    L("D", "Know what fundamental-measure theory weights.", "n₃ is the local packing fraction (volume weight θ(R − |r|)), n₂ the surface weight δ(R − |r|), n₁ and n₀ scaled versions, plus vector weights.", [], [
        facts("el-fmt-weights", "edl.dft", "{{q}}", [
            ("Which FMT weighted density is the local packing fraction?", "n₃ (step-function volume weight)", "n₂ (surface delta weight)", "n₀", "the vector weight n_V2"),
            ("Which weight function is a delta shell δ(R − |r − r′|)?", "The surface weight for n₂", "The volume weight for n₃", "The tensor weight only", "None: all FMT weights are smooth"),
            ("What does FMT reproduce exactly for a uniform hard-sphere mixture (Rosenfeld form)?", "The Percus–Yevick compressibility equation of state", "The Carnahan–Starling equation", "The virial expansion to all orders", "The ideal-gas law"),
            ("Why add tensor weights (White Bear, Tarazona) to Rosenfeld's functional?", "To get freezing and strongly confined (0-D) limits right", "To include Coulomb correlations", "To speed up the calculation", "To model solvent dipoles"),
        ], "FMT builds the excess free energy from a few geometric averages of the density, which is why it handles layering next to walls, the solvent structure chapters 8–13 rely on")], p="P2", std=C(7)),
    L("E", "Compute the MSA screening parameter.", "Restricted primitive model: 2Γd = √(1 + 2κd) − 1; Γ → κ/2 at low density.", [], [
        Q("el-msa-gamma", "edl.dft", "In the restricted primitive model with ion diameter d and κd = {{kd}}, what is Γd from the MSA?",
          given={"kd": {"pick": [0.1, 0.5, 1, 3]}}, value="(sqrt(1 + 2*kd) - 1)/2", tex="\\Gamma d",
          verify="Max(*solve(Eq(4*x**2 + 4*x - 2*nsimplify(kd), 0), x))",
          explain="Γ plays the role of κ/2 but includes ion size: for κd ≪ 1, Γd ≈ κd/2; MSA energies feed the electrostatic correlation functionals of section 7.4")], std=C(7)),
    L("F", "Model a charge-regulating surface with Langmuir site equilibria.", "Fraction of sites bound: θ = ρ_F(r_s)/(ρ_F(r_s) + K).", [], [
        Q("el-site-binding", "edl.dft", "A surface site binds a cation with dissociation constant K = {{K}} mM. If the cation density at the surface plane is {{rs}} mM, what fraction of sites is bound?",
          given={"K": {"pick": [0.1, 1, 10]}, "rs": {"pick": [0.05, 1, 20]}}, value="rs/(rs + K)", tex="\\theta",
          verify="solve(Eq(nsimplify(K)*x, nsimplify(rs)*(1 - x)), x)[0]",
          explain="It is the local density at the wall, not the bulk one, that sets the surface reaction (7.86); that density comes out of the DFT, which is how solvent and ion structure reach the surface charge")], std=C(7)),
])]),
U(5, "el-molecular", "Molecular structure of the double layer (ch. 8–13)", [("Solvent, solvation and surface interactions", [
    L("A", "Explain the solvent's role in a single double layer.", "The solvent is far denser than the ions, so it sets the structure; the surface reaction involves only the PDIs, but their local density depends on every species.", [], [
        facts("el-solvent-structure", "edl.molecular", "{{q}}", [
            ("Why does the book treat the solvent as the most important species for EDL structure?", "Its density is far greater than the ions', so it dominates packing and layering", "It carries most of the charge", "It sets the Debye length", "It is the only species that reacts with the surface"),
            ("The surface chemical reaction involves only the PDIs. What decides how many PDIs reach the wall?", "Every species in the solution, through structure and interactions", "Only the bulk pH", "Only the surface site density", "Only the Debye length"),
            ("What does the solution structure couple to in a charge-regulating EDL?", "The surface reaction, and hence the surface charge and potential", "Only the electrokinetic shear plane", "Nothing: structure and charge are independent", "Only the Hamaker constant"),
        ], "Chapter 8's conclusion: an accurate surface chemistry and an accurate near-wall solution structure are both needed")], p="P2", std=C(8)),
    L("B", "Predict how solvation of each ion changes the surface charge.", "Poorly solvated PDIs crowd the wall and neutralise it; strongly solvated PDIs stay away and the negative charge grows.", [], [
        facts("el-solvation-effects", "edl.molecular", "{{q}}", [
            ("The potential-determining ions are poorly solvated. What happens to a negatively charged regulating surface?", "PDI density at the wall rises and the charge is partly neutralised", "The charge magnitude grows", "Nothing changes", "The surface becomes positive in all cases"),
            ("The potential-determining ions are strongly solvated. What happens to the negative surface charge?", "Its magnitude increases, since fewer PDIs reach the wall", "It is neutralised", "It becomes zero", "It oscillates in sign"),
            ("How do non-PDI ions affect the surface charge?", "Indirectly: their local density attracts or repels the PDIs and shifts the surface equilibrium", "Directly, by reacting with surface sites", "They have no effect", "Only through the Debye length"),
            ("Solvent–solvent attraction is weak. What happens near the surface?", "The wall layer saturates with solvent and excluded volume expels the PDIs", "PDIs accumulate and neutralise the surface", "The solvent leaves the wall entirely", "Ions form a crystal"),
            ("Solvent–solvent attraction is strong. What happens?", "It favours partial neutralisation of the surface by PDIs", "It expels the PDIs", "It has no effect on charge", "It doubles the Debye length"),
        ], "Chapter 9: solvation shifts local densities, and the mass-action law at the surface turns that into a change of charge")], p="P2", std=C(9)),
    L("C", "Predict effects of non-Coulombic surface interactions.", "Solvophilic walls attract solvent strongly; PDIs compete with other species for the finite space at the wall; ion–surface attraction feeds the Stern layer.", [], [
        facts("el-surface-interactions", "edl.molecular", "{{q}}", [
            ("Glass is hydrophilic toward water. Toward mercury it is…", "Solvophobic: wettability depends on the pair of materials", "Also solvophilic", "Neutral", "Undefined"),
            ("Why do non-Coulombic wall interactions change the surface charge?", "PDIs compete with every other species for the finite space at the wall", "They change the bulk pH", "They change the solvent's dielectric constant everywhere", "They don't: only Coulomb forces matter"),
            ("Non-Coulombic attraction between ions and the wall mainly changes…", "Adsorption, and so the Stern-layer composition", "The Debye length", "The bulk osmotic pressure", "The solvent's density far from the wall"),
        ], "Chapter 10: the wall–liquid interaction energy is a material property that also sets wetting and contact angles")], p="P2", std=C(10)),
]), ("Potential, valency and ion size", [
    L("A", "Interpret the classical double-layer planes molecularly.", "With c-DFT charge profiles in Poisson's equation, the Helmholtz planes, Stern and Grahame layers and the shear plane get molecular meanings.", [], [
        facts("el-planes", "edl.molecular", "{{q}}", [
            ("How does the book get the potential profile from c-DFT?", "Feed the DFT fluid charge density into Poisson's equation (1.8)", "Solve Poisson–Boltzmann with a corrected κ", "Fit the Grahame equation", "Measure the zeta potential"),
            ("Which classical quantities does the molecular charge profile give an interpretation to?", "The Helmholtz planes, the Stern and Grahame layers, and the plane of shear", "Only the Debye length", "Only the Hamaker constant", "Only the isoelectric point"),
            ("Compared with Poisson–Boltzmann, what does the molecular potential profile show near the wall?", "Structure (oscillations, layer-by-layer features) from solvent and ion packing", "A pure exponential decay", "A constant potential", "A discontinuity at the Debye length"),
        ], "Chapter 11: once the charge density is known in molecular detail, Poisson's equation alone gives the potential; no Boltzmann closure is needed")], p="P2", std=C(11)),
    L("B", "Predict the effect of multivalent ions.", "Valency changes Coulomb strength and its balance with non-Coulombic forces; multivalent counterions screen far more strongly, as in the Schulze–Hardy rule.", [], [
        facts("el-multivalent", "edl.molecular", "{{q}}", [
            ("Why do EDL properties depend on which specific ions are present, not just ionic strength?", "Ions differ in charge, size and non-Coulombic interactions with solvent, wall and each other", "Ionic strength already captures everything", "Only the anion matters", "Only valence enters PB, so they don't"),
            ("Multivalent counterions in a double layer typically…", "Screen and neutralise the surface charge far more effectively than monovalent ones", "Have no effect beyond ionic strength", "Increase the Debye length", "Are excluded from the wall"),
            ("Which classic empirical rule reflects the strong effect of counterion valence on colloid stability?", "The Schulze–Hardy rule", "The Hofmeister series", "Raoult's law", "Fick's law"),
        ], "Chapter 12: valence sets Coulomb interaction strength, and its interplay with excluded volume and solvation shapes the profiles")], p="P2", std=C(12)),
    L("C", "Predict the effect of ion size.", "The main effects are excluded volume and packing at the charged wall, which change the local PDI density and so the surface reaction.", [], [
        facts("el-ion-size", "edl.molecular", "{{q}}", [
            ("According to chapter 13, what mainly drives ion-size effects in the EDL?", "Excluded volume and packing constraints near the charged wall", "Changes in the bulk dielectric constant", "Quantum effects", "Gravity"),
            ("How do ion-size effects reach the surface charge?", "They change the local density of the PDIs at the regulating surface", "They change the number of surface sites", "They change the surface pKa directly", "They don't affect charge"),
            ("What nonphysical result does ignoring ion size in PB give near a highly charged wall?", "Counterion densities far above close packing", "Negative ion densities", "A Debye length of zero", "An uncharged wall"),
        ], "Chapter 13: size is another non-Coulombic effect, and it couples to the charge regulation reaction through packing")], p="P2", std=C(13)),
])]),
U(6, "el-simulation", "Simulation and numerical methods (ch. 14–16, appendix A)", [("Molecular simulation", [
    L("A", "Apply the Metropolis acceptance rule.", "Accept a move with probability min(1, e^{−βΔU}).", [], [
        Q("el-metropolis", "edl.simulation", "A Monte Carlo trial move changes the energy by {{dU}} kT. With what probability is it accepted?",
          given={"dU": {"pick": [-1, 0.5, 1, 2, 5]}}, value="min(1, exp(-dU))", tex="P_{acc}", verify="Min(1, exp(-nsimplify(dU)))",
          explain="Downhill moves are always taken; uphill ones with the Boltzmann weight, which samples the canonical ensemble")], std=C(14)),
    L("B", "Compute an excess chemical potential by Widom insertion.", "βμ_ex = −ln⟨e^{−βΔU}⟩ over random test insertions.", [], [
        Q("el-widom", "edl.simulation", "Random test-particle insertions give ⟨e^{−βΔU}⟩ = {{w}}. What is βμ_ex?",
          given={"w": {"pick": [0.01, 0.2, 0.9, 1.5]}}, value="-log(w)", tex="\\beta\\mu_{ex}", verify="solve(Eq(exp(-x), nsimplify(w)), x)[0]",
          explain="The potential distribution theorem (14.23); in an inhomogeneous fluid ln ρ(z) − ln⟨e^{−βU_t}⟩ must be constant, a check on any simulation")], std=C(14)),
    L("C", "Find the collision time of two hard spheres.", "Solve |r_ij + v_ij t| = σ_ij for the smallest positive t.", [], [
        Q("el-collision-time", "edl.simulation", "Two hard spheres with contact distance σ = {{s}} are {{r}} apart along x and approach head-on with relative speed {{v}} (consistent units). When do they collide?",
          given={"s": {"pick": [1]}, "r": {"pick": [1.5, 2, 3]}, "v": {"pick": [0.5, 1, 2]}}, value="(r - s)/v", tex="t_c",
          verify="Min(*[t for t in solve(Eq((nsimplify(r) - nsimplify(v)*x)**2, s**2), x) if t > 0])",
          explain="Event-driven MD jumps straight from collision to collision, solving this quadratic for every approaching pair")], std=C(14)),
    L("D", "Compute the coupling parameter of a one-component plasma.", "Γ = (Ze)²/(4πε₀akT), a the Wigner–Seitz radius.", [], [
        Q("el-ocp-gamma", "edl.simulation", "A one-component plasma of charge Z = {{Z}} has Wigner–Seitz radius {{a}} nm at {{T}} K (vacuum). What is its coupling parameter Γ? " + CONSTS,
          given={"Z": {"pick": [1, 2, 10]}, "a": {"pick": [0.5, 1, 5]}, "T": {"pick": [300, 1000, 10000]}}, value=f"(Z*{E})^2/(4*pi*{EPS0}*a*1e-9*{KB}*T)", tex="\\Gamma",
          verify=f"(Z*{e_})**2/(4*pi*{ep_}*nsimplify(a)/10**9*{kb_}*T)", explain="Γ > 1 means Coulomb energy beats thermal energy and the plasma becomes liquid-like; it crystallises near Γ ≈ 175")], std=C(15)),
    L("E", "Use the Debye–Hückel limiting law.", "log₁₀γ± = −0.509|z₊z₋|√I in water at 25 °C.", [], [
        Q("el-dh-limiting", "edl.simulation", "What is the mean activity coefficient of a {{zp}}:{{zm}} salt at ionic strength {{I}} M in water at 25 °C (limiting law)?",
          given={"zp": {"pick": [1, 2]}, "zm": {"pick": [1, 2]}, "I": {"pick": [0.001, 0.005, 0.01]}}, value="10^(-0.509*zp*zm*sqrt(I))", tex="\\gamma_\\pm",
          verify="exp(-Rational(509, 1000)*zp*zm*sqrt(nsimplify(I))*log(10))", explain="Simulations of the restricted primitive model test where this limiting law fails, typically above a few mM for 2:2 salts")], std=C(15)),
]), ("Numerical methods for c-DFT and transport", [
    L("A", "Take a damped Picard step.", "x^{k+1} = (1 − α)x^k + αg(x^k).", [], [
        Q("el-picard", "edl.simulation", "A Picard iteration has x^k = {{xk}} and g(x^k) = {{g}}. With mixing parameter α = {{a}}, what is x^{k+1}?",
          given={"xk": {"pick": [1, 2.5]}, "g": {"pick": [0.5, 3, 4]}, "a": {"pick": [0.05, 0.1, 0.5]}}, value="(1 - a)*xk + a*g", tex="x^{k+1}",
          verify="nsimplify(xk) + nsimplify(a)*(nsimplify(g) - nsimplify(xk))", explain="Small α trades speed for stability; strongly coupled Poisson and Euler–Lagrange equations often need α of a few percent, which is why Newton methods win (16.1.3)")], std=C(16)),
    L("B", "Take a Newton step on a nonlinear residual.", "J Δx = −R.", [], [
        Q("el-newton-pb", "edl.simulation", "To find ψ̃ with 2 sinh(ψ̃/2) = {{s}} (Grahame, reduced), take one Newton step from ψ̃₀ = {{p0}}. What is ψ̃₁?",
          given={"s": {"pick": [1, 3, 10]}, "p0": {"pick": [1, 2]}}, value="p0 - (2*sinh(p0/2) - s)/cosh(p0/2)", tex="\\tilde\\psi_1",
          verify="nsimplify(p0) - (2*sinh(Symbol('pp')/2) - s).subs(Symbol('pp'), nsimplify(p0))/diff(2*sinh(Symbol('pp')/2) - s, Symbol('pp')).subs(Symbol('pp'), nsimplify(p0))",
          explain="Newton converges quadratically near the root; in c-DFT the Jacobian couples densities, potential and nonlocal weighted densities (16.17–16.22)")], std=C(16)),
    L("C", "Reduce a block system with the Schur complement.", "S = A₂₂ − A₂₁A₁₁⁻¹A₁₂, then Sx₂ = b₂ − A₂₁A₁₁⁻¹b₁.", [], [
        Q("el-schur", "edl.simulation", "For [[{{a}}, {{b}}], [{{c}}, {{d}}]]·[x₁, x₂] = [{{p}}, {{q}}], eliminate x₁ with the Schur complement. What is x₂?",
          given={"a": {"pick": [2, 4]}, "b": {"pick": [1, -1]}, "c": {"pick": [1, 3]}, "d": {"pick": [5, 6]}, "p": {"pick": [1, 2]}, "q": {"pick": [3, -2]}},
          value="(q - c*p/a)/(d - c*b/a)", tex="x_2", verify="Matrix([[a, b], [c, d]]).solve(Matrix([p, q]))[1]",
          explain="The book's real-space Newton solver splits off the density unknowns this way and solves the smaller Schur system with GMRES (16.24–16.26)")], std=C(16)),
    L("D", "Compute a Nernst–Planck flux.", "J = −D(dc/dx + zc dψ̃/dx): diffusion plus migration.", [], [
        Q("el-nernst-planck", "edl.simulation", "An ion of charge number {{z}} (D = {{D}} × 10⁻⁹ m²/s) has local concentration {{c}} mol/m³, gradient {{dc}} mol/m⁴ and reduced potential gradient dψ̃/dx = {{dp}} m⁻¹. What is its flux, in μmol/(m²·s)?",
          given={"z": {"pick": [1, -1, 2]}, "D": {"pick": [1, 2]}, "c": {"pick": [1, 10]}, "dc": {"pick": [-100, 100]}, "dp": {"pick": [-1000, 500]}},
          value="-D*1e-9*(dc + z*c*dp)*1e6", tex="J",
          verify="-nsimplify(D)/10**9*nsimplify(c)*diff(log(Symbol('cc')) + z*Symbol('pp'), Symbol('cc')).subs(Symbol('cc'), nsimplify(c))*nsimplify(dc)*10**6 - nsimplify(D)/10**9*nsimplify(c)*z*nsimplify(dp)*10**6",
          explain="Flux follows the gradient of the electrochemical potential, J = −(Dc/kT)∇(μ + zeψ) (16.3), which for an ideal solution splits into diffusion and migration")], std=["petsev-edl:16", "petsev-edl:A"]),
])]),
]
