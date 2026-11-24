"""Second question types for Inorganic Chemistry (IN): facts asked the other way round (observation → species), and each
calculation in reverse or as a comparison. Numeric keys go through incalc (ox_state, half_electrons, cfse, unpaired)."""
from opl_dsl import Q

FILE, FRAMEWORK = "in-second-types", "inorganic-chemistry"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"
NA_ = "Rational('6.02214076e23')"


def facts(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("IN-1.1.A", facts("in-flame-identify", "inorg.s-block", [
        ("A salt gives a lilac flame, best seen through blue cobalt glass. Which cation?", "K⁺", "Na⁺", "Li⁺", "Ba²⁺"),
        ("A salt gives an apple-green flame. Which cation?", "Ba²⁺", "Sr²⁺", "Ca²⁺", "K⁺"),
        ("A salt gives a persistent intense yellow flame. Which cation?", "Na⁺", "K⁺", "Li⁺", "Cu²⁺"),
        ("A salt gives a blue-green flame. Which cation?", "Cu²⁺", "Ba²⁺", "Na⁺", "Ca²⁺"),
    ], "Sodium's yellow masks the others; cobalt glass filters it out")),
    ("IN-1.1.B", facts("in-oxide-type", "inorg.s-block", [
        ("Which metal forms mainly a superoxide (MO₂) when burned in air?", "Potassium", "Lithium", "Sodium", "Magnesium"),
        ("What does sodium peroxide give with cold water?", "NaOH and H₂O₂", "NaOH and H₂", "Na₂O and O₂", "NaH"),
        ("Which alkali metal burns to the normal oxide M₂O and also reacts with nitrogen?", "Lithium", "Sodium", "Potassium", "Caesium"),
    ], "Large cations stabilise large anions: Li₂O, Na₂O₂, KO₂")),
    ("IN-2.1.A", Q("in-ion-charge", "inorg.redox", "In the oxoanion {{M}}O{{k}}ⁿ⁻, {{M}} is in the +{{s}} state. What is n?",
        cases=[{"M": "Cr", "k": 4, "s": 6}, {"M": "Mn", "k": 4, "s": 7}, {"M": "V", "k": 4, "s": 5}, {"M": "Fe", "k": 4, "s": 6}, {"M": "Cl", "k": 4, "s": 7},
               {"M": "S", "k": 3, "s": 4}, {"M": "N", "k": 3, "s": 5}],
        value="2*k - s", tex="n", final=True, verify="-(s + (-2)*k)",
        explain="Charge = oxidation state + (−2 × oxygens): −n = s − 2k")),
    ("IN-2.1.B", facts("in-disprop-which", "inorg.redox", [
        ("Which ion disproportionates in water?", "Cu⁺ (to Cu and Cu²⁺)", "Cu²⁺", "Fe³⁺", "Zn²⁺"),
        ("Cl₂ in cold dilute NaOH gives which pair?", "Cl⁻ and ClO⁻", "Cl⁻ and ClO₃⁻ only", "HCl and O₂", "ClO₂ and ClO₄⁻"),
        ("Which species can act as both oxidant and reductant and disproportionates to water and O₂?", "H₂O₂", "O₃", "OH⁻", "O₂"),
    ], "A species disproportionates when the state above and below it are both reachable and lower in free energy")),
    ("IN-2.2.A", Q("in-oxoacid-state", "inorg.p-block", "What is the oxidation state of the central atom in {{name}}?",
        cases=[{"name": "hypochlorous acid", "s": 1, "f": "HClO", "el": "Cl"}, {"name": "chlorous acid", "s": 3, "f": "HClO2", "el": "Cl"}, {"name": "chloric acid", "s": 5, "f": "HClO3", "el": "Cl"},
               {"name": "periodic acid (HIO₄)", "s": 7, "f": "HIO4", "el": "I"}, {"name": "sulfurous acid", "s": 4, "f": "H2SO3", "el": "S"}, {"name": "nitrous acid", "s": 3, "f": "HNO2", "el": "N"},
               {"name": "phosphoric acid", "s": 5, "f": "H3PO4", "el": "P"}],
        value="s",
        tex="", final=True, verify="ox_state(f, 0, el)", explain="hypo-…-ous, -ous, -ic, per-…-ic climb by two")),
    ("IN-2.2.B", facts("in-oxide-trend", "inorg.p-block", [
        ("Across period 3 from Na₂O to Cl₂O₇, the oxides change how?", "From basic, through amphoteric Al₂O₃, to acidic", "From acidic to basic", "All are basic", "All are amphoteric"),
        ("Which oxide gives an acidic solution in water?", "SO₃", "Na₂O", "MgO", "CaO"),
        ("Which oxide dissolves in both HCl and NaOH?", "Al₂O₃", "MgO", "SiO₂", "Na₂O"),
    ], "Ionic metal oxides are basic; covalent non-metal oxides are acidic; the boundary is amphoteric")),
    ("IN-3.1.A", Q("in-ox-from-d", "inorg.coordination", "A {{M}} ion in a complex has a d{{d}} configuration. What is the metal's oxidation state?",
        cases=[{"M": "Fe", "g": 8, "Zm": 26, "d": 5}, {"M": "Fe", "g": 8, "Zm": 26, "d": 6}, {"M": "Co", "g": 9, "Zm": 27, "d": 6}, {"M": "Cr", "g": 6, "Zm": 24, "d": 3}, {"M": "Mn", "g": 7, "Zm": 25, "d": 4},
               {"M": "Ni", "g": 10, "Zm": 28, "d": 8}, {"M": "Cu", "g": 11, "Zm": 29, "d": 9}, {"M": "Pt", "g": 10, "Zm": 78, "d": 8}],
        value="g - d", tex="", final=True, verify="pt_group(Zm) - d",
        explain="d count = group − oxidation state (no s electrons left in a complex)")),
    ("IN-3.1.B", Q("in-unpaired-from-moment", "inorg.coordination", "A complex has a spin-only magnetic moment of {{mu}} μ_B. How many unpaired electrons does it have?",
        cases=[{"mu": 1.73}, {"mu": 2.83}, {"mu": 3.87}, {"mu": 4.90}, {"mu": 5.92}], value="round(sqrt(1 + mu^2) - 1)", tex="n", final=True,
        verify=f"floor(sqrt(1 + {n('mu')}**2) - 1 + Rational(1, 2))", explain="μ = √(n(n + 2)): 1.73, 2.83, 3.87, 4.90, 5.92 for n = 1 to 5")),
    ("IN-3.1.C", Q("in-cfse-gain", "inorg.coordination", "For an octahedral d{{d}} ion, by how many Δ_o is the low-spin CFSE more stabilising than the high-spin CFSE (pairing energy left out)?",
        given={"d": {"pick": [4, 5, 6, 7]}}, value="d == 4 ? 1 : (d == 5 ? 2 : (d == 6 ? 2 : 1))", tex="\\Delta_o", final=True,
        verify="cfse(d, 'oct', 'high') - cfse(d, 'oct', 'low')", explain="Each electron moved from e_g to t₂g gains 1 Δ_o; low spin wins when Δ_o exceeds the pairing energy")),
    ("IN-3.1.D", facts("in-spectro-consequence", "inorg.coordination", [
        ("Which complex absorbs light of the shortest wavelength?", "[Co(CN)₆]³⁻", "[CoF₆]³⁻", "[Co(H₂O)₆]³⁺", "[Co(NH₃)₆]³⁺"),
        ("Which iron(III) complex is most likely high spin?", "[FeF₆]³⁻", "[Fe(CN)₆]³⁻", "[Fe(bpy)₃]³⁺", "[Fe(phen)₃]³⁺"),
        ("Replacing H₂O by NH₃ around Ni²⁺ shifts the absorption which way?", "To shorter wavelength (larger Δ_o)", "To longer wavelength", "No change", "It removes all absorption"),
    ], "Strong-field ligands (CN⁻, CO) give large Δ: shorter absorbed wavelength, low spin")),
    ("IN-3.2.A", facts("in-isomer-type", "inorg.coordination", [
        ("[Co(NH₃)₄Cl₂]⁺ shows which isomerism?", "Geometric only (cis and trans)", "Optical only", "Both, giving three isomers", "None"),
        ("[Co(en)₃]³⁺ shows which isomerism?", "Optical (Δ and Λ)", "Geometric (cis and trans)", "Linkage", "None"),
        ("[Co(NH₃)₃Cl₃] has which isomers?", "fac and mer", "cis and trans", "Δ and Λ", "None"),
        ("[Co(NH₃)₅(NO₂)]²⁺ and [Co(NH₃)₅(ONO)]²⁺ are what kind of isomers?", "Linkage", "Geometric", "Optical", "Ionisation"),
    ], "Two different ligand positions give geometric isomers; chelate rings in a propeller give enantiomers")),
    ("IN-3.2.B", facts("in-colour-identify", "inorg.coordination", [
        ("A deep purple solution of an oxoanion. Which?", "MnO₄⁻", "CrO₄²⁻", "Cr₂O₇²⁻", "VO₄³⁻"),
        ("An orange solution turns yellow when base is added. Which ion was present?", "Cr₂O₇²⁻ (to CrO₄²⁻)", "MnO₄⁻", "Fe³⁺", "Co²⁺"),
        ("A pale pink solution of a hydrated divalent ion. Which?", "Mn²⁺ (or Co²⁺, deeper)", "Cu²⁺", "Ni²⁺", "Fe²⁺"),
        ("A pale blue solution deepens to royal blue with excess ammonia. Which ion?", "Cu²⁺", "Ni²⁺", "Co²⁺", "Zn²⁺"),
    ], "Colours come from d–d or charge-transfer absorption: d⁰ oxoanions are coloured by charge transfer")),
    ("IN-4.1.A", Q("in-redox-ratio", "inorg.redox", "{{ox}} oxidises {{red}}. How many moles of the reductant react with one mole of the oxidant?",
        cases=[{"ox": "MnO₄⁻ (to Mn²⁺)", "red": "Fe²⁺ (to Fe³⁺)", "a1": "MnO4", "q1": -1, "a2": "Mn", "q2": 2, "e1": "Mn", "rt": 5, "b1": "Fe", "r1": 2, "b2": "Fe", "r2": 3, "e2": "Fe"},
               {"ox": "Cr₂O₇²⁻ (to Cr³⁺)", "red": "Fe²⁺ (to Fe³⁺)", "a1": "Cr2O7", "q1": -2, "a2": "Cr", "q2": 3, "e1": "Cr", "rt": 6, "b1": "Fe", "r1": 2, "b2": "Fe", "r2": 3, "e2": "Fe"},
               {"ox": "MnO₄⁻ (to Mn²⁺)", "red": "C₂O₄²⁻ (to CO₂)", "a1": "MnO4", "q1": -1, "a2": "Mn", "q2": 2, "e1": "Mn", "rt": 2.5, "b1": "C2O4", "r1": -2, "b2": "CO2", "r2": 0, "e2": "C"},
               {"ox": "IO₃⁻ (to I₂)", "red": "I⁻ (to I₂)", "a1": "IO3", "q1": -1, "a2": "I", "q2": 0, "e1": "I", "rt": 5, "b1": "I", "r1": -1, "b2": "I", "r2": 0, "e2": "I"}],
        value="rt", tex="", verify="half_electrons(a1, q1, a2, q2, e1)/half_electrons(b1, r1, b2, r2, e2)",
        explain="Electrons lost = electrons gained: divide the oxidant's electrons by the reductant's")),
    ("IN-4.1.B", Q("in-thiosulfate-volume", "inorg.redox", "{{V}} mL of {{c}} M {{ox}} is added to excess KI, and the iodine released is titrated with {{ct}} M Na₂S₂O₃. What volume of thiosulfate, in mL, is needed?",
        cases=[{"ox": "KIO₃ (with acid)", "k": 6}, {"ox": "K₂Cr₂O₇ (with acid)", "k": 6}, {"ox": "CuSO₄", "k": 1}, {"ox": "H₂O₂ (with acid)", "k": 2}],
        given={"V": {"pick": [10, 20, 25]}, "c": {"pick": [0.01, 0.02]}, "ct": {"pick": [0.05, 0.1]}}, value="V*c*k/ct", tex="V",
        verify=f"solve(Eq({n('ct')}*x, {n('V')}*{n('c')}*k), x)[0]", explain="One I₂ takes two thiosulfate; count I₂ per mole of oxidant (IO₃⁻ gives 3, Cu²⁺ gives ½)")),
    ("IN-4.2.A", facts("in-ammonia-dissolve", "inorg.qualitative", [
        ("Which hydroxide dissolves in excess aqueous ammonia (but not in excess NaOH)?", "Cu(OH)₂", "Al(OH)₃", "Fe(OH)₃", "Pb(OH)₂"),
        ("Which hydroxide dissolves in both excess NaOH and excess NH₃?", "Zn(OH)₂", "Fe(OH)₂", "Mg(OH)₂", "Al(OH)₃"),
        ("Which hydroxide dissolves in neither excess NaOH nor excess NH₃?", "Fe(OH)₃", "Zn(OH)₂", "Al(OH)₃", "Cu(OH)₂"),
    ], "Excess NaOH dissolves amphoteric hydroxides; excess NH₃ dissolves those of metals that form ammine complexes")),
    ("IN-4.2.B", facts("in-precipitate-identify", "inorg.qualitative", [
        ("Ag⁺ gives a pale yellow precipitate, insoluble even in concentrated NH₃. Which anion?", "I⁻", "Cl⁻", "Br⁻", "NO₃⁻"),
        ("OH⁻ gives a red-brown precipitate. Which cation?", "Fe³⁺", "Fe²⁺", "Cu²⁺", "Mg²⁺"),
        ("Ba²⁺ gives a white precipitate insoluble in dilute HCl. Which anion?", "SO₄²⁻", "CO₃²⁻", "SO₃²⁻", "Cl⁻"),
        ("OH⁻ gives a green precipitate that darkens in air. Which cation?", "Fe²⁺", "Fe³⁺", "Cu²⁺", "Zn²⁺"),
    ], "Work back from colour and solubility in acid or ammonia")),
    ("IN-4.2.C", facts("in-test-result", "inorg.qualitative", [
        ("A gas that turns damp red litmus blue is released when a salt is warmed with NaOH. Which ion?", "NH₄⁺", "NO₃⁻", "CO₃²⁻", "Cl⁻"),
        ("Dilute acid releases a gas that turns limewater milky. Which ion?", "CO₃²⁻", "SO₄²⁻", "NH₄⁺", "Cl⁻"),
        ("A solution turns blood-red with thiocyanate. Which ion?", "Fe³⁺", "Fe²⁺", "Cu²⁺", "Co²⁺"),
    ], "Each test pairs one reagent with one ion's distinctive response")),
    ("IN-5.1.A", Q("in-sites-count", "inorg.solids", "A cubic cell has A atoms on {{c}} corners, {{e}} edge centres, {{f}} face centres and {{b}} in the body. How many A atoms belong to one cell?",
        cases=[{"c": 8, "e": 0, "f": 6, "b": 0}, {"c": 8, "e": 0, "f": 0, "b": 1}, {"c": 0, "e": 12, "f": 0, "b": 1}, {"c": 8, "e": 12, "f": 0, "b": 0}, {"c": 0, "e": 0, "f": 6, "b": 0}],
        value="c/8 + e/4 + f/2 + b", tex="N", final=True, verify="Rational(c, 8) + Rational(e, 4) + Rational(f, 2) + b",
        explain="Corners are shared by 8 cells, edges by 4, faces by 2")),
    ("IN-5.1.B", facts("in-structure-from-cn", "inorg.solids", [
        ("Which structure has 8:8 coordination?", "CsCl", "NaCl", "Zinc blende", "Fluorite (CaF₂)"),
        ("Which structure has 4:4 coordination?", "Zinc blende (ZnS)", "NaCl", "CsCl", "Rutile"),
        ("Which structure has 8:4 coordination?", "Fluorite (CaF₂)", "Rutile (TiO₂)", "NaCl", "CsCl"),
        ("Which metal structure gives each atom 12 nearest neighbours?", "Cubic close packed (fcc)", "Body-centred cubic", "Simple cubic", "Diamond"),
    ], "Coordination numbers rise with the radius ratio: 4, 6, 8, and 12 for close-packed metals")),
    ("IN-5.1.C", Q("in-radius-from-edge", "inorg.solids", "A metal crystallises in a {{lat}} cell with edge {{a}} pm. What is its atomic radius, in pm?",
        cases=[{"lat": "simple cubic", "k": 1}, {"lat": "body-centred cubic", "k": 2}, {"lat": "face-centred cubic", "k": 3}], given={"a": {"pick": [286.6, 361.5, 408.6]}},
        value="k == 1 ? a/2 : (k == 2 ? sqrt(3)*a/4 : sqrt(2)*a/4)", tex="r",
        verify=f"{n('a')}/2 if k == 1 else ({n('a')}*sqrt(3)/4 if k == 2 else {n('a')}/(2*sqrt(2)))", explain="Atoms touch along the edge (sc), the body diagonal (bcc) or the face diagonal (fcc)")),
    ("IN-5.1.D", Q("in-edge-from-density", "inorg.solids", "{{el}} ({{lat}}, M = {{M}} g/mol) has density {{rho}} g/cm³. What is the cell edge, in pm? (N_A = 6.022 × 10²³)",
        cases=[{"el": "Copper", "lat": "fcc", "Z": 4, "M": 63.546, "rho": 8.96}, {"el": "Iron", "lat": "bcc", "Z": 2, "M": 55.845, "rho": 7.874},
               {"el": "Polonium", "lat": "simple cubic", "Z": 1, "M": 209, "rho": 9.2}, {"el": "NaCl", "lat": "rock salt, 4 formula units", "Z": 4, "M": 58.44, "rho": 2.165}],
        value="(Z*M/(rho*6.02214076e23))^(1/3)*1e10", tex="a",
        verify=f"(Z*{n('M')}/({n('rho')}*{NA_}))**Rational(1, 3)*10**10", explain="ρ = Z·M / (N_A·a³); cm³ to pm is a factor of 10³⁰")),
    ("IN-5.1.E", Q("in-ratio-limit", "inorg.solids", "What is the smallest radius ratio r₊/r₋ at which a cation still touches all {{cn}} anions around it ({{geo}})?",
        cases=[{"cn": 4, "geo": "tetrahedral"}, {"cn": 6, "geo": "octahedral"}, {"cn": 8, "geo": "cubic"}],
        value="cn == 4 ? sqrt(1.5) - 1 : (cn == 6 ? sqrt(2) - 1 : sqrt(3) - 1)", tex="r_+/r_-",
        verify="sqrt(Rational(3, 2)) - 1 if cn == 4 else (sqrt(2) - 1 if cn == 6 else sqrt(3) - 1)",
        explain="Anions touch each other along the cell's edge, face or body diagonal: 0.225, 0.414, 0.732")),
    ("IN-5.2.A", Q("in-bragg-edge", "inorg.solids", "X-rays of wavelength {{lam}} pm reflect from the ({{h}}{{k}}{{l}}) planes of a cubic crystal at θ = {{th}}° (first order). What is the cell edge, in pm?",
        cases=[{"h": 1, "k": 1, "l": 1}, {"h": 2, "k": 0, "l": 0}, {"h": 2, "k": 2, "l": 0}], given={"lam": {"pick": [154.06, 71.07]}, "th": {"pick": [12.5, 19.2, 21.7]}},
        value="lam/(2*sin(th*pi/180))*sqrt(h^2 + k^2 + l^2)", tex="a",
        verify=f"solve(Eq(2*(x/sqrt(h**2 + k**2 + l**2))*sin({n('th')}*pi/180), {n('lam')}), x)[0]", explain="d = λ/(2 sin θ), then a = d·√(h² + k² + l²)")),
]
