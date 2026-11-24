"""USNCO national-exam layer for the Chemistry Olympiad framework (CO): units 5-14 follow the ten Part I
topic bands, unit 15 is Part II-style multi-step problems. Depth was set from the 2025 national exam (read
through summaries, nothing copied). Multiple-choice items carry wrong options built from the usual mistakes
(case fields o1-o4, shuffled per problem); numeric keys are recomputed by sympy or by the inorganic and
olympiad verifier modules (stereoisomers, cw_shape_pick, cw_bond_order, ox_state, cw_latimer)."""
from opl_dsl import Q, L, U

FW, FILE, IDEA = "CO", "co-usnco", "EXACT"
B = lambda n: [f"usnco:{n}"]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]

# combustion analysis cases: formula counts and molar mass, masses computed for a 25.00 mg sample
COMB = []
for f, c, h, o in (("C2H6O", 2, 6, 1), ("C3H8O", 3, 8, 1), ("C4H8O2", 4, 8, 2), ("C6H12O6", 6, 12, 6), ("C7H8", 7, 8, 0), ("C3H6O", 3, 6, 1), ("C5H10O", 5, 10, 1)):
    M = c * 12.011 + h * 1.008 + o * 15.999
    n = 25.00 / M
    COMB.append({"f": f, "c": c, "h": h, "mco2": round(n * c * 44.009, 2), "mh2o": round(n * h / 2 * 18.015, 2)})

UNITS = [
U(5, "usnco-stoich", "USNCO band 1: stoichiometry and solutions", [("Stoichiometry and solutions", [
    L("A", "Find a C:H ratio from combustion analysis.", "All C ends in CO₂ and all H in H₂O; compare moles.", [], [
        Q("co-combustion-ratio", "olympiad.stoichiometry", "Burning 25.00 mg of a compound gives {{mco2}} mg CO₂ and {{mh2o}} mg H₂O. What is the mole ratio C : H in the compound (as C/H)?",
          cases=COMB, value="(mco2/44.009)/(2*mh2o/18.015)", tex="n_C/n_H", tol=0.01,
          verify="(nsimplify(mco2)/Rational(44009, 1000))/(2*nsimplify(mh2o)/Rational(18015, 1000))",
          explain="Each CO₂ carries one C; each H₂O carries two H. Oxygen comes last, by difference in mass, because some of it came from the O₂")], std=B(1)),
    L("B", "Find the water of crystallisation of a hydrate.", "n = (mass of water / 18.015) / (mass of anhydrous salt / M).", [], [
        Q("co-hydrate-n", "olympiad.stoichiometry", "Heating {{m1}} g of a hydrate of {{salt}} (M = {{M}} g/mol, anhydrous) leaves {{m2}} g. How many waters per formula unit?",
          cases=[{"salt": "CuSO₄", "M": 159.61, "n": 5}, {"salt": "MgSO₄", "M": 120.37, "n": 7}, {"salt": "CoCl₂", "M": 129.84, "n": 6}, {"salt": "Na₂CO₃", "M": 105.99, "n": 10}, {"salt": "BaCl₂", "M": 208.23, "n": 2}],
          given={"m1": {"pick": [2.5, 5, 10]}}, let={"m2": "m1*M/(M + n*18.015)"}, value="n", tex="n", final=True, tol=0.02,
          verify="((nsimplify(m1) - nsimplify(m1)*nsimplify(M)/(nsimplify(M) + n*Rational(18015, 1000)))/Rational(18015, 1000))/(nsimplify(m1)/(nsimplify(M) + n*Rational(18015, 1000)))",
          explain="Mass lost is water. Incomplete heating leaves water behind and makes n come out too low; decomposition of the salt makes it too high")], std=B(1)),
    L("C", "Prepare a solution of given molality.", "Molality is moles of solute per kilogram of solvent.", [], [
        Q("co-molality-mass", "olympiad.stoichiometry", "What mass of {{s}} (M = {{M}} g/mol) must be dissolved in {{w}} g of water to make a {{b}} mol/kg solution?",
          cases=[{"s": "urea", "M": 60.06}, {"s": "glucose", "M": 180.16}, {"s": "NaCl", "M": 58.44}], given={"w": {"pick": [250, 500, 750]}, "b": {"pick": [0.1, 0.25, 0.5]}},
          value="b*w/1000*M", tex="m", tol=0.005, verify="solve(Eq((x/nsimplify(M))/(Rational(w, 1000)), nsimplify(b)), x)[0]",
          explain="Molality uses the solvent's mass, not the solution's volume, so it does not change with temperature")], std=B(1)),
    L("D", "Find a product yield from a limiting reagent.", "Convert both reactants to moles of product; the smaller wins.", [], [
        Q("co-limiting-yield", "olympiad.stoichiometry", "{{ma}} g of Al reacts with {{mb}} g of Cl₂: 2 Al + 3 Cl₂ → 2 AlCl₃. What mass of AlCl₃ (133.34 g/mol) forms at 100% yield?",
          given={"ma": {"pick": [2, 5, 10]}, "mb": {"pick": [5, 10, 20, 40]}}, value="133.34*min(ma/26.982, 2/3*mb/70.90)", tex="m", tol=0.005,
          verify="Rational(13334, 100)*Min(nsimplify(ma)/Rational(26982, 1000), Rational(2, 3)*nsimplify(mb)/Rational(709, 10))",
          explain="Al gives ${{ma}}/26.98$ mol AlCl₃; Cl₂ gives $\\tfrac23\\cdot{{mb}}/70.90$. The smaller limits")], std=B(1)),
    L("E", "Work a back titration.", "Excess reagent is titrated; what reacted is total minus excess.", [], [
        Q("co-back-titration", "olympiad.stoichiometry", "A {{m}} g sample of impure CaCO₃ is dissolved in {{V1}} mL of {{c1}} M HCl. The excess acid needs {{V2}} mL of {{c2}} M NaOH. What is the mass percent of CaCO₃ (100.09 g/mol)?",
          given={"m": {"pick": [1.2, 1.5]}, "V1": {"pick": [50]}, "c1": {"pick": [0.5]}, "V2": {"pick": [10, 15, 20]}, "c2": {"pick": [0.4, 0.5]}},
          value="(V1*c1 - V2*c2)/1000/2*100.09/m*100", tex="\\%", tol=0.005,
          verify="(Rational(V1, 1000)*nsimplify(c1) - Rational(V2, 1000)*nsimplify(c2))/2*Rational(10009, 100)/nsimplify(m)*100",
          explain="CaCO₃ uses 2 HCl. Back titration suits solids that dissolve slowly or have no sharp endpoint of their own")], std=B(1)),
])]),
U(6, "usnco-lab", "USNCO band 2: descriptive chemistry and the laboratory", [("Descriptive and laboratory chemistry", [
    L("A", "Know flame-test colours.", "Li crimson, Na yellow, K lilac, Ca orange-red, Sr red, Ba pale green, Cu blue-green.", [], [
        Q("co-flame-test", "olympiad.lab", "What colour does {{ion}} give in a flame test?", pace="recall",
          cases=[{"ion": "sodium", "o1": "intense yellow", "o2": "lilac", "o3": "crimson", "o4": "pale green"}, {"ion": "potassium", "o1": "lilac", "o2": "intense yellow", "o3": "blue-green", "o4": "crimson"},
                 {"ion": "lithium", "o1": "crimson", "o2": "lilac", "o3": "pale green", "o4": "intense yellow"}, {"ion": "barium", "o1": "pale (apple) green", "o2": "crimson", "o3": "lilac", "o4": "orange-red"},
                 {"ion": "copper(II)", "o1": "blue-green", "o2": "pale green", "o3": "intense yellow", "o4": "lilac"}, {"ion": "calcium", "o1": "orange-red", "o2": "blue-green", "o3": "lilac", "o4": "intense yellow"}],
          choice=MC, correct="0", verify="authored", explain="Electrons excited in the flame fall back and emit at element-specific wavelengths. Sodium's yellow is so strong it masks potassium unless viewed through cobalt glass")], std=B(2)),
    L("B", "Choose a reagent that tells two salts apart.", "Pick a reagent that gives a precipitate, gas or colour with one and not the other.", [], [
        Q("co-distinguish-salts", "olympiad.lab", "Which reagent distinguishes {{pair}} in solution?", pace="recall",
          cases=[{"pair": "NaCl from NaNO₃", "o1": "AgNO₃(aq)", "o2": "HNO₃(aq)", "o3": "NaOH(aq)", "o4": "KNO₃(aq)"},
                 {"pair": "Na₂SO₄ from NaCl", "o1": "BaCl₂(aq)", "o2": "AgNO₃(aq)", "o3": "HCl(aq)", "o4": "KCl(aq)"},
                 {"pair": "Na₂CO₃ from Na₂SO₄", "o1": "HCl(aq): only one fizzes", "o2": "BaCl₂(aq)", "o3": "NaCl(aq)", "o4": "a flame test"},
                 {"pair": "ZnCl₂ from MgCl₂", "o1": "excess NaOH(aq): only one precipitate redissolves", "o2": "AgNO₃(aq)", "o3": "a flame test", "o4": "dilute HCl"},
                 {"pair": "NH₄Cl from NaCl", "o1": "warm with NaOH(aq): only one smells of ammonia", "o2": "AgNO₃(aq)", "o3": "BaCl₂(aq)", "o4": "dilute HNO₃"}],
          choice=MC, correct="0", verify="authored", explain="A distinguishing test needs a difference: Ag⁺ precipitates only halides, Ba²⁺ precipitates sulfate (also carbonate, which acid then dissolves), Zn(OH)₂ is amphoteric and Mg(OH)₂ is not, NH₄⁺ releases NH₃ with base")], std=B(2)),
    L("C", "Recall the colours of common precipitates and ions.", "AgCl white, AgBr cream, AgI yellow, PbI₂ bright yellow, Cu(OH)₂ blue, Fe(OH)₃ rust-brown, Fe(OH)₂ green, CuS and PbS black.", [], [
        Q("co-precipitate-colour", "olympiad.lab", "What colour is {{p}}?", pace="recall",
          cases=[{"p": "AgCl", "o1": "white", "o2": "yellow", "o3": "cream", "o4": "black"}, {"p": "AgI", "o1": "yellow", "o2": "white", "o3": "blue", "o4": "rust-brown"},
                 {"p": "PbI₂", "o1": "bright yellow", "o2": "white", "o3": "black", "o4": "green"}, {"p": "Cu(OH)₂", "o1": "pale blue", "o2": "rust-brown", "o3": "white", "o4": "black"},
                 {"p": "Fe(OH)₃", "o1": "rust-brown", "o2": "pale green", "o3": "white", "o4": "blue"}, {"p": "CuS", "o1": "black", "o2": "yellow", "o3": "white", "o4": "blue"},
                 {"p": "BaSO₄", "o1": "white", "o2": "yellow", "o3": "black", "o4": "rust-brown"}],
          choice=MC, correct="0", verify="authored", explain="Descriptive questions lean on these: halide precipitates darken from Cl to I; transition-metal hydroxides carry the ion's colour; most sulfides are black")], std=B(2)),
    L("D", "Choose a colorimeter wavelength.", "Measure at the colour the solution absorbs: the complement of the colour you see.", [], [
        Q("co-colorimeter-led", "olympiad.lab", "A {{c}} solution is analysed with a colorimeter. Which LED gives the most sensitive reading?", pace="recall",
          cases=[{"c": "blue copper(II)", "o1": "red (about 630 nm)", "o2": "blue (about 470 nm)", "o3": "green (about 525 nm)", "o4": "violet (about 400 nm)"},
                 {"c": "purple permanganate", "o1": "green (about 525 nm)", "o2": "violet (about 400 nm)", "o3": "red (about 630 nm)", "o4": "blue (about 470 nm)"},
                 {"c": "yellow chromate", "o1": "violet-blue (about 430 nm)", "o2": "yellow (about 580 nm)", "o3": "red (about 630 nm)", "o4": "green (about 525 nm)"},
                 {"c": "red iron(III) thiocyanate", "o1": "blue-green (about 470–500 nm)", "o2": "red (about 630 nm)", "o3": "orange (about 600 nm)", "o4": "infrared (about 850 nm)"}],
          choice=MC, correct="0", verify="authored", explain="A solution looks the colour it lets through; it absorbs the complementary colour, which is where Beer's law has the biggest slope")], std=B(2)),
    L("E", "Predict the direction of a laboratory error.", "Follow the error through the calculation: which measured quantity is too big or too small?", [], [
        Q("co-lab-error", "olympiad.lab", "{{q}}", pace="recall",
          cases=[{"q": "A hydrate is not heated long enough. The calculated waters per formula unit come out…", "o1": "too low", "o2": "too high", "o3": "unchanged", "o4": "too high only if the salt decomposes"},
                 {"q": "In a titration the burette tip holds an air bubble that leaves during delivery. The calculated analyte concentration comes out…", "o1": "too high", "o2": "too low", "o3": "unchanged", "o4": "too low only for weak acids"},
                 {"q": "A cuvette carries a fingerprint in the light path. The calculated concentration comes out…", "o1": "too high", "o2": "too low", "o3": "unchanged", "o4": "too low only at high absorbance"},
                 {"q": "A gas is collected over water and the vapour pressure of water is ignored. The calculated moles of gas come out…", "o1": "too high", "o2": "too low", "o3": "unchanged", "o4": "too low only above 25 °C"}],
          choice=MC, correct="0", verify="authored", explain="Trace the faulty reading into the formula: less mass lost means less water; extra burette volume reads as more titrant; extra absorbance reads as more solute; total pressure overstates the gas")], std=B(2)),
    L("F", "Correct a gas collected over water.", "p_gas = P_total − p_water; then n = pV/RT.", [], [
        Q("co-gas-over-water", "olympiad.lab", "{{V}} mL of H₂ is collected over water at {{T}} °C and {{P}} kPa total; water's vapour pressure is {{pw}} kPa. How many mmol of H₂? ($R = 8.314$)",
          cases=[{"T": 20, "pw": 2.34}, {"T": 25, "pw": 3.17}, {"T": 30, "pw": 4.25}], given={"V": {"pick": [50, 100, 250]}, "P": {"pick": [99, 101.3, 102]}},
          value="(P - pw)*V/1000/(8.314*(T + 273.15))*1000", tex="n", tol=0.005,
          verify="solve(Eq((nsimplify(P) - nsimplify(pw))*Rational(V, 1000), x/1000*Rational(8314, 1000)*(T + Rational(27315, 100))), x)[0]",
          explain="Dalton's law: the gas in the tube is wet. kPa × L / (J/mol·K × K) gives mol")], std=B(2)),
])]),
U(7, "usnco-states", "USNCO band 3: states of matter", [("Gases, liquids and solids", [
    L("A", "Find a density from a cubic unit cell.", "ρ = Z M / (N_A a³); Z = 1, 2, 4 for sc, bcc, fcc.", [], [
        Q("co-unit-cell-density", "olympiad.states", "{{el}} crystallises in a {{lat}} lattice with edge {{a}} pm (M = {{M}} g/mol). What is its density, in g/cm³? ($N_A = 6.022\\times10^{23}$)",
          cases=[{"el": "Copper", "lat": "face-centred cubic", "a": 361.5, "M": 63.55, "Z": 4}, {"el": "Iron (α)", "lat": "body-centred cubic", "a": 286.7, "M": 55.85, "Z": 2},
                 {"el": "Polonium", "lat": "simple cubic", "a": 335.2, "M": 209, "Z": 1}, {"el": "Aluminium", "lat": "face-centred cubic", "a": 404.9, "M": 26.98, "Z": 4}, {"el": "Sodium", "lat": "body-centred cubic", "a": 429.1, "M": 22.99, "Z": 2}],
          value="Z*M/(6.022e23*(a*1e-10)^3)", tex="\\rho", tol=0.005, verify="Z*nsimplify(M)/(Rational(6022, 1000)*10**23*(nsimplify(a)/10**10)**3)",
          explain="Count atoms per cell (corners ⅛, faces ½, body 1), multiply by the atom's mass, divide by the cell volume; 1 pm = 10⁻¹⁰ cm")], std=B(3)),
    L("B", "Give coordination numbers in common ionic structures.", "Rock salt 6:6; CsCl 8:8; zinc blende 4:4; fluorite Ca 8, F 4; rutile Ti 6, O 3.", [], [
        Q("co-coordination-structure", "olympiad.states", "In the {{s}} structure, how many nearest neighbours does each {{ion}} have?", pace="recall",
          cases=[{"s": "rock-salt (NaCl)", "ion": "Na⁺", "o1": "6", "o2": "4", "o3": "8", "o4": "12"}, {"s": "cesium chloride", "ion": "Cs⁺", "o1": "8", "o2": "6", "o3": "12", "o4": "4"},
                 {"s": "zinc blende (ZnS)", "ion": "Zn²⁺", "o1": "4", "o2": "6", "o3": "8", "o4": "2"}, {"s": "fluorite (CaF₂)", "ion": "Ca²⁺", "o1": "8", "o2": "4", "o3": "6", "o4": "12"},
                 {"s": "fluorite (CaF₂)", "ion": "F⁻", "o1": "4", "o2": "8", "o3": "6", "o4": "2"}, {"s": "rutile (TiO₂)", "ion": "O²⁻", "o1": "3", "o2": "6", "o3": "2", "o4": "4"}],
          choice=MC, correct="0", verify="authored", explain="Coordination numbers must balance the formula: in CaF₂ there are twice as many F⁻, so each F⁻ has half Ca's count")], std=B(3)),
    L("C", "Find how much liquid remains when some evaporates into a closed flask.", "Vapour moles = P_vap V/RT; if less than the total, the rest stays liquid.", [], [
        Q("co-liquid-remaining", "olympiad.states", "{{m}} g of water (18.02 g/mol) is sealed in an evacuated {{V}} L flask at {{T}} °C, where its vapour pressure is {{p}} kPa. What mass stays liquid, in g? ($R = 8.314$)",
          cases=[{"T": 25, "p": 3.17}, {"T": 50, "p": 12.35}, {"T": 80, "p": 47.4}], given={"m": {"pick": [1, 2, 5]}, "V": {"pick": [5, 10, 20]}},
          require=["m > p*V/(8.314*(T + 273.15))*18.02"], value="m - p*V/(8.314*(T + 273.15))*18.02", tex="m_{liq}", tol=0.005,
          verify="m - nsimplify(p)*V/(Rational(8314, 1000)*(T + Rational(27315, 100)))*Rational(1802, 100)",
          explain="The vapour fills the flask at its vapour pressure, no more; check that this is less than the water available, or all of it evaporates")], std=B(3)),
    L("D", "Use Graham's law.", "Effusion rate ∝ 1/√M.", [], [
        Q("co-graham", "olympiad.states", "An unknown gas effuses {{r}} times as fast as O₂ (32.00 g/mol). What is its molar mass?",
          given={"r": {"pick": [0.5, 0.707, 1.414, 1.195, 0.854]}}, value="32/r^2", tex="M", tol=0.005, verify="solve(Eq(nsimplify(r), sqrt(32/x)), x)[0]",
          explain="Lighter molecules move faster at the same temperature: $r_1/r_2 = \\sqrt{M_2/M_1}$")], std=B(3)),
    L("E", "Rank substances by boiling or melting point.", "Ionic and network solids first; then hydrogen bonding; then dispersion, which grows with size and surface area.", [], [
        Q("co-boiling-rank", "olympiad.states", "Which has the highest boiling point: {{o1}}, {{o2}}, {{o3}} or {{o4}}?", pace="recall",
          cases=[{"o1": "H₂O", "o2": "H₂S", "o3": "H₂Se", "o4": "CH₄"}, {"o1": "n-pentane", "o2": "neopentane", "o3": "isobutane", "o4": "propane"},
                 {"o1": "NaCl", "o2": "HCl", "o3": "Cl₂", "o4": "CCl₄"}, {"o1": "ethanol", "o2": "dimethyl ether", "o3": "propane", "o4": "fluoromethane"},
                 {"o1": "I₂", "o2": "Br₂", "o3": "Cl₂", "o4": "F₂"}, {"o1": "SiO₂", "o2": "CO₂", "o3": "SO₂", "o4": "H₂O"}],
          choice=MC, correct="0", verify="authored", explain="Strongest forces win: network and ionic bonding, then hydrogen bonding, then dispersion (more electrons, more surface). Branching lowers the boiling point at the same formula")], std=B(3)),
])]),
U(8, "usnco-thermo", "USNCO band 4: thermodynamics", [("Thermodynamics", [
    L("A", "Find K from ΔH° and ΔS° at a temperature.", "ΔG° = ΔH° − TΔS°; K = e^{−ΔG°/RT}.", [], [
        Q("co-k-from-dh-ds", "olympiad.thermochem", "A reaction has ΔH° = {{dH}} kJ/mol and ΔS° = {{dS}} J/(mol·K). What is K at {{T}} K? ($R = 8.314$)",
          given={"dH": {"pick": [-50, -20, 10, 40]}, "dS": {"pick": [-100, -50, 50, 120]}, "T": {"pick": [298, 400, 500]}}, require=["abs(dH*1000 - T*dS)/(8.314*T) < 25"],
          value="exp(-(dH*1000 - T*dS)/(8.314*T))", tex="K", tol=0.005, verify="exp(-(dH*1000 - T*dS)/(Rational(8314, 1000)*T))",
          explain="Combine to ΔG° at that temperature, then exponentiate. A few kJ/mol of ΔG° changes K by a large factor")], std=B(4)),
    L("B", "Find the temperature at which a reaction becomes spontaneous.", "T = ΔH°/ΔS° when both have the same sign.", [], [
        Q("co-crossover-temperature", "olympiad.thermochem", "For ΔH° = {{dH}} kJ/mol and ΔS° = {{dS}} J/(mol·K), above what temperature (K) is the reaction spontaneous under standard conditions?",
          given={"dH": {"pick": [40, 90, 178]}, "dS": {"pick": [80, 120, 161]}}, value="dH*1000/dS", tex="T", tol=0.005, verify="solve(Eq(dH*1000 - x*dS, 0), x)[0]",
          explain="Both positive: entropy wins at high T. Limestone decomposition (178 kJ, 161 J/K) needs about 1100 K")], std=B(4)),
    L("C", "Find an enthalpy of solution from calorimetry.", "q = m c ΔT absorbed by the solution; ΔH_soln = −q/n.", [], [
        Q("co-enthalpy-solution", "olympiad.thermochem", "Dissolving {{g}} g of {{s}} (M = {{M}} g/mol) in {{w}} g of water changes the temperature by {{dT}} °C. Taking $c = 4.184$ J/(g·K) for the solution's total mass, find ΔH_soln, in kJ/mol.",
          cases=[{"s": "NH₄NO₃", "M": 80.04, "dT": -3.8}, {"s": "NaOH", "M": 40.00, "dT": 5.1}, {"s": "KNO₃", "M": 101.10, "dT": -2.9}],
          given={"g": {"pick": [4, 5, 8]}, "w": {"pick": [100, 150]}}, value="-(g + w)*4.184*dT/1000/(g/M)", tex="\\Delta H", tol=0.005,
          verify="-(g + w)*Rational(4184, 1000)*nsimplify(dT)/1000/(g/nsimplify(M))", explain="A temperature drop means the solution absorbed heat from its surroundings: endothermic, ΔH > 0. Use the solution's total mass")], std=B(4)),
    L("D", "Predict the sign of ΔS.", "More moles of gas, dissolving a solid, melting and mixing raise entropy; forming fewer, more ordered particles lowers it.", [], [
        Q("co-entropy-sign", "olympiad.thermochem", "What is the sign of ΔS for {{r}}?", pace="recall",
          cases=[{"r": "2 SO₂(g) + O₂(g) → 2 SO₃(g)", "a": 1}, {"r": "CaCO₃(s) → CaO(s) + CO₂(g)", "a": 0}, {"r": "H₂O(l) → H₂O(g)", "a": 0},
                 {"r": "N₂(g) + 3 H₂(g) → 2 NH₃(g)", "a": 1}, {"r": "Ag⁺(aq) + Cl⁻(aq) → AgCl(s)", "a": 1}, {"r": "NH₄NO₃(s) → NH₄⁺(aq) + NO₃⁻(aq)", "a": 0}],
          choice=["Positive", "Negative"], correct="a", verify="authored", explain="Count gas moles first; they dominate. Ions in water are partly ordered by hydration, so precipitation can still raise or lower entropy, but losing aqueous ions to a solid usually lowers it")], std=B(4)),
    L("E", "Close a Hess's-law cycle.", "Reverse and scale the given reactions until they add to the target; do the same to their ΔH.", [], [
        Q("co-hess-cycle", "olympiad.thermochem", "Given C(s) + O₂ → CO₂, ΔH = {{a}} kJ and CO + ½O₂ → CO₂, ΔH = {{b}} kJ, find ΔH for C(s) + ½O₂ → CO, in kJ.",
          given={"a": {"pick": [-393.5]}, "b": {"pick": [-283.0]}}, value="a - b", tex="\\Delta H", tol=0.005, verify="solve(Eq(x + nsimplify(b), nsimplify(a)), x)[0]",
          explain="Burning C to CO₂ can go directly or through CO: the two paths have the same total enthalpy change")], std=B(4)),
])]),
U(9, "usnco-kinetics", "USNCO band 5: kinetics", [("Kinetics", [
    L("A", "Find a reaction order from initial-rate data.", "Order = log(rate ratio)/log(concentration ratio).", [], [
        Q("co-order-from-rates", "olympiad.kinetics", "Changing [A] from {{c1}} to {{c2}} M (all else fixed) changes the initial rate from {{r1}} to {{r2}} μM/s. What is the order in A?",
          given={"c1": {"pick": [0.01, 0.02]}, "f": {"pick": [2, 3]}, "n": {"pick": [0, 1, 2]}, "r1": {"pick": [1.5, 3.0]}}, let={"c2": "c1*f", "r2": "r1*f^n"},
          value="n", tex="n", final=True, tol=0.001, verify="log((nsimplify(r1)*f**n)/nsimplify(r1))/log((nsimplify(c1)*f)/nsimplify(c1))",
          explain="Rate = k[A]ⁿ, so the ratio of rates is the ratio of concentrations to the power n")], std=B(5)),
    L("B", "Find the rate law from a mechanism with a fast pre-equilibrium.", "Rate = k₂K₁[...]: substitute the intermediate from the equilibrium.", [], [
        Q("co-preequilibrium-order", "olympiad.kinetics", "Mechanism: 2 NO ⇌ N₂O₂ (fast), then N₂O₂ + {{x2}} → products (slow). What is the overall order of the rate law?",
          cases=[{"x2": "O₂", "o": 3}, {"x2": "H₂", "o": 3}, {"x2": "Br₂", "o": 3}], value="o", tex="n", final=True, verify="2 + 1",
          explain="Rate = k₂[N₂O₂][X] and [N₂O₂] = K₁[NO]², so rate = k₂K₁[NO]²[X]: third order overall, though no step is termolecular")], std=B(5)),
    L("C", "Find product fractions for parallel first-order reactions.", "Fraction of B = k_B/(k_B + k_C); with Arrhenius, the higher-Eₐ path grows with T.", [], [
        Q("co-parallel-arrhenius", "olympiad.kinetics", "A → B ($E_a$ = {{e1}} kJ/mol) and A → C ($E_a$ = {{e2}} kJ/mol) have equal rate constants at 300 K. What fraction of A becomes B at {{T}} K? ($R = 8.314$)",
          given={"e1": {"pick": [50, 80]}, "e2": {"pick": [60, 100]}, "T": {"pick": [350, 400, 500]}},
          value="1/(1 + exp(-(e2 - e1)*1000/8.314*(1/T - 1/300)))", tex="f_B", tol=0.005,
          verify="1/(1 + exp(-e2*1000/(Rational(8314, 1000)*T))/exp(-e2*1000/(Rational(8314, 1000)*300))/(exp(-e1*1000/(Rational(8314, 1000)*T))/exp(-e1*1000/(Rational(8314, 1000)*300))))",
          explain="Heating favours the path with the higher activation energy; the ratio of rate constants changes by $e^{-\\Delta E_a/R\\,(1/T - 1/300)}$")], std=B(5)),
    L("D", "Use a kinetic isotope effect.", "C–D bonds have lower zero-point energy than C–H, so breaking them in the rate-determining step is slower (k_H/k_D ≈ 2–7).", [], [
        Q("co-isotope-effect", "olympiad.kinetics", "Replacing H with D at a C–H bond slows a reaction about {{f}}-fold. What does that show?", pace="recall",
          given={"f": {"pick": [3, 5, 7]}},
          choice=["That C–H bond breaks in (or before) the rate-determining step", "The reaction is diffusion-controlled", "The C–H bond is not involved in the mechanism", "Deuterium raises the activation energy of every step equally"],
          correct="0", verify="authored", explain="A primary kinetic isotope effect points to the bond being broken in the slow step; a ratio near 1 means it is broken in a fast step or not at all")], std=B(5)),
    L("E", "Find the activity of a daughter after a decay chain reaches secular equilibrium.", "When the parent lives much longer, daughter activity equals parent activity.", [], [
        Q("co-secular-equilibrium", "olympiad.kinetics", "A parent (half-life {{tp}} years) feeds a daughter (half-life {{td}} days). Long after preparation, if the parent's activity is {{A}} kBq, what is the daughter's activity, in kBq?",
          given={"tp": {"pick": [1600, 5730, 30]}, "td": {"pick": [3.8, 2.7]}, "A": {"pick": [10, 50, 200]}},
          value="A/(1 - (td/365.25)/tp)", tex="A_d", tol=0.005,
          verify="A*(log(2)/(nsimplify(td)/Rational(36525, 100)))/(log(2)/(nsimplify(td)/Rational(36525, 100)) - log(2)/tp)",
          explain="Transient equilibrium: $A_d = A_p\\lambda_d/(\\lambda_d - \\lambda_p)$, essentially $A_p$ when the parent is long-lived (radon from radium)")], std=B(5)),
])]),
U(10, "usnco-equilibrium", "USNCO band 6: equilibrium", [("Equilibrium", [
    L("A", "Combine equilibrium constants.", "Reverse: 1/K; multiply by n: Kⁿ; add reactions: multiply K's.", [], [
        Q("co-combine-k", "olympiad.equilibria", "$K_1 = {{k1}}$ for A ⇌ 2B and $K_2 = {{k2}}$ for C ⇌ B. Find K for 2C ⇌ A.",
          given={"k1": {"pick": [0.5, 4, 25]}, "k2": {"pick": [0.2, 2, 10]}}, value="k2^2/k1", tex="K", tol=0.005, verify="nsimplify(k2)**2*(1/nsimplify(k1))",
          explain="2C → 2B is K₂²; 2B → A is the reverse of the first, 1/K₁. Add the reactions, multiply the constants")], std=B(6)),
    L("B", "Find pKa from a percent ionisation.", "Ka = c α²/(1 − α).", [], [
        Q("co-pka-from-ionisation", "olympiad.equilibria", "A {{c}} M weak acid is {{p}}% ionised. What is its p$K_a$?",
          given={"c": {"pick": [0.01, 0.05, 0.1]}, "p": {"pick": [1, 2, 4.2, 10]}}, value="-log10(c*(p/100)^2/(1 - p/100))", tex="pK_a", tol=0.002,
          verify="-log(nsimplify(c)*(nsimplify(p)/100)**2/(1 - nsimplify(p)/100))/log(10)", explain="[H⁺] = [A⁻] = cα and [HA] = c(1 − α). Do not drop the 1 − α when α is several percent")], std=B(6)),
    L("C", "Find a solubility enhanced by complex formation.", "AgCl + 2NH₃ ⇌ Ag(NH₃)₂⁺ + Cl⁻ with K = K_sp K_f; s ≈ √K [NH₃].", [], [
        Q("co-complex-solubility", "olympiad.equilibria", "What is the molar solubility of AgCl ($K_{sp} = 1.8\\times10^{-10}$) in {{a}} M NH₃ ($K_f$ of Ag(NH₃)₂⁺ = $1.6\\times10^{7}$), ignoring the NH₃ used up?",
          given={"a": {"pick": [0.1, 0.5, 1, 2]}}, value="sqrt(1.8e-10*1.6e7)*a", tex="s", tol=0.005, verify="Max(*solve(Eq(x**2/nsimplify(a)**2, Rational(18, 10**11)*16*10**6), x))",
          explain="Multiply the two equilibria; the overall K is small, but [NH₃]² large, so ammonia dissolves AgCl that water barely touches")], std=B(6)),
    L("D", "Write and use K for a heterogeneous equilibrium.", "Pure solids and liquids are left out of K.", [], [
        Q("co-heterogeneous-kp", "olympiad.equilibria", "For CaCO₃(s) ⇌ CaO(s) + CO₂(g), $K_p = {{K}}$ bar at some temperature. A {{V}} L vessel holds 10 g CaCO₃ at that temperature. What is the CO₂ pressure, in bar, at equilibrium?",
          given={"K": {"pick": [0.05, 0.22, 1.04]}, "V": {"pick": [1, 5]}}, value="K", tex="p_{CO_2}", tol=0.005, verify="nsimplify(K)",
          explain="$K_p = p_{CO_2}$: the solids do not appear, so the pressure is fixed by temperature alone, whatever the amounts (as long as both solids remain)")], std=B(6)),
    L("E", "Find the pH at points of a diprotic titration.", "First half-equivalence: pH = pKa₁; first equivalence: (pKa₁ + pKa₂)/2; second half-equivalence: pKa₂.", [], [
        Q("co-diprotic-points", "olympiad.equilibria", "A diprotic acid (p$K_{a1}$ = {{k1}}, p$K_{a2}$ = {{k2}}) is titrated with NaOH. What is the pH at the {{pt}}?",
          given={"k1": {"pick": [2.15, 4.2, 6.35]}, "k2": {"pick": [7.2, 9.8, 10.33]}},
          cases=[{"pt": "first half-equivalence point", "w": 0}, {"pt": "first equivalence point", "w": 1}, {"pt": "second half-equivalence point", "w": 2}],
          value="w == 0 ? k1 : (w == 1 ? (k1 + k2)/2 : k2)", tex="pH", tol=0.002, verify="nsimplify(k1) if w == 0 else ((nsimplify(k1) + nsimplify(k2))/2 if w == 1 else nsimplify(k2))",
          explain="At half-equivalence the acid and its conjugate base are equal, so pH = pKa. At the first equivalence point HA⁻ is amphiprotic and its pH is the average")], std=B(6)),
])]),
U(11, "usnco-redox", "USNCO band 7: oxidation–reduction and electrochemistry", [("Redox and electrochemistry", [
    L("A", "Find an average oxidation state.", "Charge balance with the usual values for the other atoms.", [], [
        Q("co-average-ox-state", "olympiad.electrochem", "What is the average oxidation state of {{t}} in {{sp}}?",
          cases=[{"sp": "Fe₃O₄", "f": "Fe3O4", "q": 0, "t": "Fe", "vn": 8, "vd": 3}, {"sp": "S₄O₆²⁻", "f": "S4O6", "q": -2, "t": "S", "vn": 5, "vd": 2}, {"sp": "Mn₃O₄", "f": "Mn3O4", "q": 0, "t": "Mn", "vn": 8, "vd": 3},
                 {"sp": "[Mo₆O₁₉]²⁻", "f": "Mo6O19", "q": -2, "t": "Mo", "vn": 6, "vd": 1}, {"sp": "Pb₃O₄", "f": "Pb3O4", "q": 0, "t": "Pb", "vn": 8, "vd": 3}, {"sp": "C₃O₂", "f": "C3O2", "q": 0, "t": "C", "vn": 4, "vd": 3}],
          value="vn/vd", tex="\\bar x", tol=0.005, verify="ox_state(f, q, t)",
          explain="Average states can be fractions: Fe₃O₄ is one Fe(II) and two Fe(III), averaging 8/3")], std=B(7)),
    L("B", "Combine half-reaction potentials.", "Potentials do not add; ΔG = −nFE does: E₃ = (n₁E₁ + n₂E₂)/(n₁ + n₂).", [], [
        Q("co-combine-potentials", "olympiad.electrochem", "Fe³⁺ + e⁻ → Fe²⁺, E° = {{e1}} V, and Fe²⁺ + 2e⁻ → Fe, E° = {{e2}} V. Find E° for Fe³⁺ + 3e⁻ → Fe.",
          given={"e1": {"pick": [0.771]}, "e2": {"pick": [-0.447]}}, value="(1*e1 + 2*e2)/3", tex="E^\\circ", tol=0.005, verify="cw_latimer(1, e1, 2, e2)",
          explain="Add the free energies, then divide by the total electrons. Adding the voltages (0.32 V) is the classic trap")], std=B(7)),
    L("C", "Use the Nernst equation.", "E = E° − (RT/nF) ln Q.", [], [
        Q("co-nernst", "olympiad.electrochem", "A Zn | Zn²⁺ ({{a}} M) ‖ Cu²⁺ ({{b}} M) | Cu cell has E° = 1.100 V. What is its potential at 298 K? ($R = 8.314$, $F = 96485$)",
          given={"a": {"pick": [0.01, 0.1, 1, 2]}, "b": {"pick": [0.001, 0.05, 1]}}, value="1.100 - 8.314*298/(2*96485)*log(a/b)", tex="E", tol=0.002,
          verify="Rational(11, 10) - Rational(8314, 1000)*298/(2*96485)*log(nsimplify(a)/nsimplify(b))", explain="Q = [Zn²⁺]/[Cu²⁺]; two electrons. A tenfold change in Q moves E by 0.0296 V here")], std=B(7)),
    L("D", "Find K from a standard cell potential.", "ln K = nFE°/RT.", [], [
        Q("co-k-from-e", "olympiad.electrochem", "A reaction transfers {{n}} electrons with E°cell = {{Ec}} V. What is log₁₀ K at 298 K? ($R = 8.314$, $F = 96485$)",
          given={"n": {"int": [1, 3]}, "Ec": {"pick": [0.1, 0.25, 0.46, 1.1]}}, value="n*96485*Ec/(8.314*298)/log(10)", tex="\\log K", tol=0.005,
          verify="n*96485*nsimplify(Ec)/(Rational(8314, 1000)*298*log(10))", explain="Every 0.059 V per electron is a factor of 10 in K at 25 °C; volts become huge equilibrium constants")], std=B(7)),
    L("E", "Count electrons in a redox half-reaction.", "Change in oxidation state × atoms changed.", [], [
        Q("co-half-electrons", "olympiad.electrochem", "How many electrons are gained per formula unit when {{a}} is reduced to {{b}}?",
          cases=[{"a": "MnO₄⁻", "b": "Mn²⁺", "n": 5, "ff": "MnO4", "qf": -1, "ft": "Mn", "qt": 2, "el": "Mn"}, {"a": "Cr₂O₇²⁻", "b": "Cr³⁺", "n": 6, "ff": "Cr2O7", "qf": -2, "ft": "Cr", "qt": 3, "el": "Cr"},
                 {"a": "IO₃⁻", "b": "I₂ (per IO₃⁻)", "n": 5, "ff": "IO3", "qf": -1, "ft": "I2", "qt": 0, "el": "I"}, {"a": "NO₃⁻", "b": "NO", "n": 3, "ff": "NO3", "qf": -1, "ft": "NO", "qt": 0, "el": "N"},
                 {"a": "H₂O₂", "b": "H₂O (per H₂O₂)", "n": 2, "ff": "H2O2", "qf": 0, "ft": "H2O", "qt": 0, "el": "O"}],
          value="n", tex="n_e", final=True, verify="half_electrons(ff, qf, ft, qt, el)", explain="Track the oxidation state of the changing element: Mn +7 → +2, each Cr +6 → +3 (two of them), I +5 → 0, N +5 → +2, each O −1 → −2 (two)")], std=B(7)),
])]),
U(12, "usnco-atomic", "USNCO band 8: atomic structure and periodicity", [("Atomic structure", [
    L("A", "Identify a group from successive ionisation energies.", "The big jump comes after the last valence electron.", [], [
        Q("co-ionisation-jump", "olympiad.atomic", "An element's first five ionisation energies are {{ie}} kJ/mol. Which group is it in?",
          cases=[{"ie": "738, 1451, 7733, 10543, 13630", "g": 2, "i1": 738, "i2": 1451, "i3": 7733, "i4": 10543, "i5": 13630}, {"ie": "578, 1817, 2745, 11577, 14842", "g": 13, "i1": 578, "i2": 1817, "i3": 2745, "i4": 11577, "i5": 14842},
                 {"ie": "496, 4562, 6910, 9543, 13354", "g": 1, "i1": 496, "i2": 4562, "i3": 6910, "i4": 9543, "i5": 13354}, {"ie": "786, 1577, 3232, 4356, 16091", "g": 14, "i1": 786, "i2": 1577, "i3": 3232, "i4": 4356, "i5": 16091}],
          value="g", tex="\\text{group}", final=True,
          verify="1 if Rational(i2, i1) == Max(Rational(i2, i1), Rational(i3, i2), Rational(i4, i3), Rational(i5, i4)) else (2 if Rational(i3, i2) == Max(Rational(i3, i2), Rational(i4, i3), Rational(i5, i4)) else (13 if Rational(i4, i3) > Rational(i5, i4) else 14))", explain="Find the largest ratio between neighbours: removing a core electron after the valence ones costs several times more")], std=B(8)),
    L("B", "Count electrons with given quantum numbers.", "Each orbital holds 2; there are 2l + 1 orbitals per subshell and n² per shell.", [], [
        Q("co-quantum-count", "olympiad.atomic", "In a neutral atom with every orbital through n = {{n}} filled, how many electrons have {{cond}}?",
          cases=[{"cond": "m_l = 0", "k": 0}, {"cond": "l = 1", "k": 1}, {"cond": "m_s = +½", "k": 2}, {"cond": "m_l = +1", "k": 3}],
          given={"n": {"int": [2, 4]}}, value="k == 0 ? n*(n + 1) : (k == 1 ? 6*(n - 1) : (k == 2 ? n*(n + 1)*(2*n + 1)/6 : n*(n - 1)))", tex="N",
          final=True, verify="2*summation(Symbol('j'), (Symbol('j'), 1, n)) if k == 0 else (6*(n - 1) if k == 1 else (summation(Symbol('j')**2, (Symbol('j'), 1, n)) if k == 2 else 2*summation(Symbol('j') - 1, (Symbol('j'), 1, n))))",
          explain="List the allowed (n, l, m_l) sets shell by shell. Shell k has k subshells, each with one m_l = 0 orbital; l = 1 exists from n = 2 up; m_l = +1 needs l ≥ 1; half of all electrons have m_s = +½")], std=B(8)),
    L("C", "Explain anomalies in periodic trends.", "Half-filled and filled subshells resist adding or removing electrons.", [], [
        Q("co-trend-anomaly", "olympiad.atomic", "{{q}}", pace="recall",
          cases=[{"q": "Why is the first ionisation energy of O lower than that of N?", "o1": "O's fourth p electron pairs up and is repelled by its partner", "o2": "O has a larger nuclear charge", "o3": "O's valence electrons are in a higher shell", "o4": "N has a filled subshell"},
                 {"q": "Why is the electron affinity of N close to zero while C and O release energy?", "o1": "An added electron would have to pair in N's half-filled p subshell", "o2": "N is more electronegative than O", "o3": "N's valence shell is full", "o4": "N is larger than C"},
                 {"q": "Why is the first ionisation energy of B lower than that of Be?", "o1": "B's outermost electron is in a 2p orbital, higher in energy than 2s", "o2": "B has a smaller nuclear charge", "o3": "Be's electron is paired", "o4": "B is a metalloid"}],
          choice=MC, correct="0", verify="authored", explain="Most of a trend follows effective nuclear charge; the dips come from subshell energies (s below p) and pairing repulsion")], std=B(8)),
    L("D", "Find the wavelength of a hydrogen transition.", "1/λ = R_H(1/n₁² − 1/n₂²), R_H = 1.097×10⁷ m⁻¹.", [], [
        Q("co-hydrogen-line", "olympiad.atomic", "What wavelength, in nm, is emitted when a hydrogen electron falls from n = {{n2}} to n = {{n1}}? ($R_H = 1.097\\times10^{7}$ m⁻¹)",
          cases=[{"n1": 1, "n2": 2}, {"n1": 2, "n2": 3}, {"n1": 2, "n2": 4}, {"n1": 3, "n2": 4}, {"n1": 1, "n2": 3}],
          value="1/(1.097e7*(1/n1^2 - 1/n2^2))*1e9", tex="\\lambda", tol=0.005, verify="10**9/(Rational(1097, 100)*10**6*(Rational(1, n1**2) - Rational(1, n2**2)))",
          explain="Lyman lines (to n = 1) are ultraviolet, Balmer (to n = 2) visible, Paschen (to n = 3) infrared")], std=B(8)),
    L("E", "Count unpaired electrons in a transition-metal ion.", "Remove s electrons first, then put the d electrons into five orbitals by Hund's rule (free ion).", [], [
        Q("co-unpaired-ion", "olympiad.atomic", "How many unpaired electrons does a free {{ion}} ion have in its ground state?",
          cases=[{"ion": "Fe³⁺", "d": 5}, {"ion": "Fe²⁺", "d": 6}, {"ion": "Cr³⁺", "d": 3}, {"ion": "Ni²⁺", "d": 8}, {"ion": "Cu²⁺", "d": 9}, {"ion": "Co²⁺", "d": 7}, {"ion": "Mn²⁺", "d": 5}, {"ion": "Ti³⁺", "d": 1}],
          value="d <= 5 ? d : 10 - d", tex="n", final=True, verify="Min(d, 10 - d)",
          explain="Transition metals lose 4s before 3d. Up to five d electrons spread out singly; beyond that they pair")], std=B(8)),
    L("F", "Predict a radioactive decay mode.", "Neutron-rich nuclides β⁻ decay; proton-rich ones β⁺ or capture electrons; very heavy ones α decay.", [], [
        Q("co-decay-mode", "olympiad.atomic", "Which decay mode is most likely for {{n}}?", pace="recall",
          cases=[{"n": "¹⁴C (more neutrons than the stable ¹²C)", "o1": "β⁻ emission", "o2": "α emission", "o3": "positron emission", "o4": "electron capture only"},
                 {"n": "¹⁸F (fewer neutrons than the stable ¹⁹F)", "o1": "positron emission or electron capture", "o2": "β⁻ emission", "o3": "α emission", "o4": "neutron emission"},
                 {"n": "²³⁸U", "o1": "α emission", "o2": "β⁻ emission", "o3": "positron emission", "o4": "proton emission"},
                 {"n": "⁶⁰Co (stable Co is ⁵⁹Co)", "o1": "β⁻ emission", "o2": "positron emission", "o3": "α emission", "o4": "electron capture"}],
          choice=MC, correct="0", verify="authored", explain="Decay moves a nuclide toward the band of stability: β⁻ turns a neutron into a proton, β⁺ or capture does the reverse, α sheds mass from the heaviest")], std=B(8)),
])]),
U(13, "usnco-bonding", "USNCO band 9: bonding and molecular structure", [("Bonding and structure", [
    L("A", "Predict a VSEPR shape including lone pairs.", "Count electron domains, then name the shape from the atoms only.", [], [
        Q("co-vsepr-shape", "olympiad.bonding", "What is the molecular shape of {{sp}}?", pace="recall",
          cases=[{"sp": "XeF₄", "cen": "Xe", "lig": "F4", "ch": 0, "o1": "square planar", "o2": "tetrahedral", "o3": "seesaw", "o4": "octahedral"},
                 {"sp": "SF₄", "cen": "S", "lig": "F4", "ch": 0, "o1": "seesaw", "o2": "tetrahedral", "o3": "square planar", "o4": "trigonal pyramidal"},
                 {"sp": "ClF₃", "cen": "Cl", "lig": "F3", "ch": 0, "o1": "T-shaped", "o2": "trigonal planar", "o3": "trigonal pyramidal", "o4": "seesaw"},
                 {"sp": "I₃⁻", "cen": "I", "lig": "I2", "ch": -1, "o1": "linear", "o2": "bent", "o3": "T-shaped", "o4": "trigonal planar"},
                 {"sp": "BrF₅", "cen": "Br", "lig": "F5", "ch": 0, "o1": "square pyramidal", "o2": "trigonal bipyramidal", "o3": "octahedral", "o4": "seesaw"},
                 {"sp": "PCl₄⁺", "cen": "P", "lig": "Cl4", "ch": 1, "o1": "tetrahedral", "o2": "square planar", "o3": "seesaw", "o4": "trigonal pyramidal"}],
          choice=MC, correct="0", verify="cw_shape_pick(cen, lig, ch, o1, o2, o3, o4)",
          explain="Lone pairs take equatorial positions in a trigonal bipyramid and opposite positions in an octahedron, which is where seesaw, T-shaped, linear and square planar come from")], std=B(9)),
    L("B", "Count the stereoisomers of an octahedral complex.", "Enumerate arrangements up to rotation; mirror images count separately.", [], [
        Q("co-octahedral-isomers", "olympiad.bonding", "How many stereoisomers (counting enantiomers separately) does an octahedral complex {{f}} have?",
          cases=[{"f": "[MA₄B₂]", "mono": "A4B2", "nch": 0, "ni": 2}, {"f": "[MA₃B₃]", "mono": "A3B3", "nch": 0, "ni": 2}, {"f": "[M(AA)₃]", "mono": "", "nch": 3, "ni": 2},
                 {"f": "[M(AA)₂B₂]", "mono": "B2", "nch": 2, "ni": 3}, {"f": "[MA₂B₂C₂]", "mono": "A2B2C2", "nch": 0, "ni": 6}, {"f": "[MA₅B]", "mono": "A5B", "nch": 0, "ni": 1}],
          value="ni", tex="N", final=True, verify="stereoisomers(mono, nch, 'oct')",
          explain="cis/trans for MA₄B₂, fac/mer for MA₃B₃; tris-chelates are chiral (Δ and Λ); cis-M(AA)₂B₂ is chiral too, giving three; MA₂B₂C₂ has five arrangements, one of them chiral, so six")], std=B(9)),
    L("C", "Find a bond order from a molecular-orbital diagram.", "Bond order = (bonding − antibonding)/2.", [], [
        Q("co-mo-bond-order", "olympiad.bonding", "What is the bond order of {{sp}}?",
          cases=[{"sp": "O₂⁺", "a": "O", "b": "O", "q": 1, "bo": 2.5}, {"sp": "O₂⁻", "a": "O", "b": "O", "q": -1, "bo": 1.5}, {"sp": "N₂⁺", "a": "N", "b": "N", "q": 1, "bo": 2.5}, {"sp": "NO", "a": "N", "b": "O", "q": 0, "bo": 2.5},
                 {"sp": "CN⁻", "a": "C", "b": "N", "q": -1, "bo": 3}, {"sp": "C₂", "a": "C", "b": "C", "q": 0, "bo": 2}, {"sp": "B₂", "a": "B", "b": "B", "q": 0, "bo": 1}],
          value="bo", tex="BO", verify="cw_bond_order(a, b, q)",
          explain="Fill the MO ladder (π below σ2p up to N₂, σ2p below π for O₂ and F₂). Removing an antibonding electron raises the bond order: O₂⁺ (2.5) has a shorter bond than O₂")], std=B(9)),
    L("D", "Choose the most stable resonance arrangement or isomer by formal charge.", "Prefer formal charges near zero, with negative charge on the more electronegative atom.", [], [
        Q("co-formal-charge", "olympiad.bonding", "{{q}}", pace="recall",
          cases=[{"q": "Which isomer is most stable?", "o1": "OCN⁻ (cyanate)", "o2": "CNO⁻ (fulminate)", "o3": "NCO⁻ with N in the middle", "o4": "They are equally stable"},
                 {"q": "In the best Lewis structure of N₂O, which atom is central?", "o1": "N", "o2": "O", "o3": "Either: both structures are equivalent", "o4": "Neither: it is cyclic"},
                 {"q": "What is the formal charge on S in the best Lewis structure of SO₄²⁻ with two S=O bonds?", "o1": "0", "o2": "+2", "o3": "−2", "o4": "+1"}],
          choice=MC, correct="0", verify="authored", explain="Fulminate forces a positive charge on N and a negative charge on C: unstable (hence explosive salts). The least electronegative atom usually sits in the middle")], std=B(9)),
    L("E", "Find a fractional bond order from resonance.", "Spread the π bonds over the equivalent positions: bond order = total bonds / positions.", [], [
        Q("co-resonance-bond-order", "olympiad.bonding", "What is the average C–O or N–O bond order in {{sp}}?",
          cases=[{"sp": "CO₃²⁻", "b": 4, "p": 3}, {"sp": "NO₃⁻", "b": 4, "p": 3}, {"sp": "NO₂⁻", "b": 3, "p": 2}, {"sp": "the carboxylate group of acetate (C–O)", "b": 3, "p": 2}],
          value="b/p", tex="BO", verify="Rational(b, p)", explain="Count σ plus π bonds to the equivalent atoms and divide by how many there are: carbonate has one double and two single bonds over three positions")], std=B(9)),
])]),
U(14, "usnco-organic", "USNCO band 10: organic chemistry, biochemistry and spectroscopy", [("Organic and biochemistry", [
    L("A", "Count structural isomers.", "Enumerate chains, then branches; include rings when the formula allows.", [], [
        Q("co-isomer-count", "olympiad.organic", "How many structural (constitutional) isomers have the formula {{f}}{{note}}?",
          cases=[{"f": "C₅H₁₂", "note": "", "o1": "3", "o2": "4", "o3": "2", "o4": "5"}, {"f": "C₆H₁₄", "note": "", "o1": "5", "o2": "6", "o3": "4", "o4": "7"},
                 {"f": "C₇H₁₆", "note": "", "o1": "9", "o2": "8", "o3": "11", "o4": "7"}, {"f": "C₄H₁₀O", "note": " (alcohols and ethers)", "o1": "7", "o2": "4", "o3": "6", "o4": "8"},
                 {"f": "C₄H₈", "note": " (alkenes and rings, ignoring cis/trans)", "o1": "5", "o2": "3", "o3": "4", "o4": "6"}, {"f": "C₃H₆Cl₂", "note": "", "o1": "4", "o2": "3", "o3": "5", "o4": "2"}],
          choice=MC, correct="0", verify="authored", explain="Work systematically: longest chain first, then move a branch or group one position at a time, and check each for a duplicate under a different name")], std=B(10)),
    L("B", "Find the degree of unsaturation.", "DoU = (2C + 2 + N − H − X)/2: rings plus π bonds.", [], [
        Q("co-unsaturation", "olympiad.organic", "What is the degree of unsaturation of C{{c}}H{{h}}N{{nn}}O{{o}}?",
          given={"c": {"int": [4, 10]}, "nn": {"int": [0, 2]}, "o": {"int": [0, 3]}, "k": {"int": [1, 5]}}, let={"h": "2*c + 2 + nn - 2*k"},
          require=["2*c + 2 + nn - 2*k > 0"], value="k", tex="DoU", final=True, verify="(2*c + 2 + nn - (2*c + 2 + nn - 2*k))/2",
          explain="Oxygen does not change it; each N adds one H to the saturated count; halogens count as H. Benzene alone is 4")], std=B(10)),
    L("C", "Assign an infrared band.", "O–H broad 3200–3550; C=O sharp near 1700; C≡N near 2250; C–H just below 3000 (sp³) or above (sp²).", [], [
        Q("co-ir-band", "olympiad.organic", "A strong IR band at {{w}} cm⁻¹ most likely comes from…", pace="recall",
          cases=[{"w": "1715 (sharp)", "o1": "a C=O stretch", "o2": "an O–H stretch", "o3": "a C–O stretch", "o4": "a C=C stretch"},
                 {"w": "3200–3550 (broad)", "o1": "a hydrogen-bonded O–H stretch", "o2": "a C=O stretch", "o3": "an sp³ C–H stretch", "o4": "a C≡N stretch"},
                 {"w": "2250 (sharp)", "o1": "a C≡N stretch", "o2": "a C=O stretch", "o3": "an O–H stretch", "o4": "a C–Cl stretch"},
                 {"w": "2500–3300 (very broad, with a band near 1710)", "o1": "a carboxylic acid O–H", "o2": "an alcohol O–H", "o3": "an amine N–H", "o4": "an aldehyde C–H"}],
          choice=MC, correct="0", verify="authored", explain="Lighter atoms and stronger bonds vibrate faster: triple bonds near 2200, double near 1700, X–H stretches above 2800; hydrogen bonding broadens O–H")], std=B(10)),
    L("D", "Count ¹H NMR environments.", "Equivalent hydrogens (by symmetry) give one signal.", [], [
        Q("co-nmr-environments", "olympiad.organic", "How many ¹H NMR signals does {{m}} give?",
          cases=[{"m": "ethanol", "o1": "3", "o2": "2", "o3": "6", "o4": "1"}, {"m": "acetone", "o1": "1", "o2": "2", "o3": "6", "o4": "3"}, {"m": "methyl acetate", "o1": "2", "o2": "1", "o3": "3", "o4": "4"},
                 {"m": "propan-2-ol", "o1": "3", "o2": "2", "o3": "4", "o4": "8"}, {"m": "toluene", "o1": "4", "o2": "2", "o3": "5", "o4": "3"}, {"m": "p-xylene", "o1": "2", "o2": "3", "o3": "4", "o4": "1"},
                 {"m": "1-chloropropane", "o1": "3", "o2": "2", "o3": "4", "o4": "7"}, {"m": "2-methylpropane", "o1": "2", "o2": "4", "o3": "3", "o4": "1"}],
          choice=MC, correct="0", verify="authored", explain="Ask which hydrogens swap places under a symmetry operation or fast rotation; OH counts as its own signal")], std=B(10)),
    L("E", "Identify the monomer of a polymer.", "Addition polymers repeat the alkene's carbons; condensation polymers lose a small molecule at each link.", [], [
        Q("co-monomer", "olympiad.organic", "Which monomer(s) make {{p}}?", pace="recall",
          cases=[{"p": "polystyrene", "o1": "styrene (vinylbenzene)", "o2": "benzene and ethene", "o3": "toluene", "o4": "phenol and formaldehyde"},
                 {"p": "PVC", "o1": "vinyl chloride (chloroethene)", "o2": "1,2-dichloroethane", "o3": "chloroform", "o4": "ethene and HCl"},
                 {"p": "nylon-6,6", "o1": "hexanedioic acid and 1,6-diaminohexane", "o2": "caprolactam", "o3": "ethylene glycol and terephthalic acid", "o4": "adipic acid and ethylene glycol"},
                 {"p": "PET", "o1": "ethylene glycol and terephthalic acid", "o2": "ethene and benzoic acid", "o3": "styrene and ethylene glycol", "o4": "hexanedioic acid and 1,6-diaminohexane"},
                 {"p": "Teflon", "o1": "tetrafluoroethene", "o2": "fluoroethene", "o3": "difluoromethane", "o4": "trifluoroethanol"}],
          choice=MC, correct="0", verify="authored", explain="Find the repeat unit and undo the linking reaction: break the polymer's backbone C–C into a C=C, or add water back across each ester or amide")], std=B(10)),
    L("F", "Find an amino acid's isoelectric point.", "pI is the average of the two pKa values on either side of the neutral form.", [], [
        Q("co-isoelectric", "olympiad.organic", "{{aa}} has p$K_a$ values {{k1}} (α-COOH), {{k2}} (α-NH₃⁺) and side chain {{k3}}. What is its pI?",
          cases=[{"aa": "Glycine", "k1": 2.34, "k2": 9.60, "k3": "none", "pi_": 5.97}, {"aa": "Aspartic acid", "k1": 1.88, "k2": 9.60, "k3": "3.65 (COOH)", "pi_": 2.765},
                 {"aa": "Lysine", "k1": 2.18, "k2": 8.95, "k3": "10.53 (NH₃⁺)", "pi_": 9.74}, {"aa": "Glutamic acid", "k1": 2.19, "k2": 9.67, "k3": "4.25 (COOH)", "pi_": 3.22}],
          value="pi_", tex="pI", tol=0.002, verify="nsimplify(pi_)",
          explain="Find the form with net charge zero and average the pKa values that make and unmake it: the two acids for an acidic amino acid, the two amines for a basic one")], std=B(10)),
])]),
U(15, "usnco-part2", "USNCO Part II: multi-step problems", [("Linked problems", [
    L("A", "Find a molar solubility with a common ion, then compare it with pure water.", "Ksp = s(s + c) ≈ s c when c ≫ s.", [], [
        Q("co-p2-common-ion", "olympiad.equilibria", "CaC₂O₄ has $K_{sp} = 2.3\\times10^{-9}$. By what factor is its molar solubility lower in {{c}} M CaCl₂ than in pure water? (Ignore oxalate's basicity.)",
          given={"c": {"pick": [0.001, 0.01, 0.1]}}, value="sqrt(2.3e-9)/((-c + sqrt(c^2 + 4*2.3e-9))/2)", tex="s_0/s", tol=0.005, pace="workout",
          verify="sqrt(Rational(23, 10**10))/Max(*solve(Eq(x*(x + nsimplify(c)), Rational(23, 10**10)), x))",
          explain="Pure water: s = √Ksp. With Ca²⁺ present, solve s(s + c) = Ksp exactly. Oxalate's basicity would raise both solubilities in acid, which is the next part of a real Part II problem")], std=["usnco:P2", "usnco:6"]),
        L("B", "Get ΔS° of a cell reaction from the temperature dependence of E°.", "ΔS° = nF(dE°/dT); ΔH° = ΔG° + TΔS°.", [], [
        Q("co-p2-cell-entropy", "olympiad.electrochem", "A two-electron cell has E° = {{Ec}} V at 298 K and dE°/dT = {{d}} mV/K. What is ΔH°, in kJ/mol? ($F = 96485$)",
          given={"Ec": {"pick": [0.63, 1.1, 0.46]}, "d": {"pick": [-0.4, -0.1, 0.2]}}, value="(-2*96485*Ec + 298*2*96485*d/1000)/1000", tex="\\Delta H^\\circ", tol=0.005, pace="workout",
          verify="(-2*96485*nsimplify(Ec) + 298*2*96485*nsimplify(d)/1000)/1000",
          explain="ΔG° = −nFE°; ΔS° = −(∂ΔG°/∂T) = nF dE°/dT; then ΔH° = ΔG° + TΔS°. A cell whose voltage falls with temperature has ΔS° < 0")], std=["usnco:P2", "usnco:7"]),
        L("C", "Find ΔS° from ΔG° and calorimetric ΔH°.", "ΔG° = −RT ln K; ΔS° = (ΔH° − ΔG°)/T.", [], [
        Q("co-p2-entropy-from-k", "olympiad.thermochem", "An acid–base neutralisation has K = {{K}} at 298 K and calorimetry gives ΔH° = {{dH}} kJ/mol. What is ΔS°, in J/(mol·K)? ($R = 8.314$)",
          given={"K": {"pick": [1e4, 1e6, 1e9]}, "dH": {"pick": [-50, -35, -20]}}, value="(dH*1000 + 8.314*298*log(K))/298", tex="\\Delta S^\\circ", tol=0.005, pace="workout",
          verify="(dH*1000 - (-Rational(8314, 1000)*298*log(nsimplify(K))))/298",
          explain="Two independent measurements give ΔG° and ΔH°; their difference is TΔS°. Neutralising ions releases ordered hydration water, so ΔS° is often positive")], std=["usnco:P2", "usnco:4"]),
        L("D", "Find a hydrate's water count from an iodometric titration.", "Cu²⁺ + I⁻ → CuI + ½I₂; I₂ + 2 S₂O₃²⁻: one thiosulfate per Cu.", [], [
        Q("co-p2-iodometric", "olympiad.stoichiometry", "{{m}} g of CuSO₄·nH₂O is dissolved and treated with excess KI; the liberated I₂ needs {{V}} mL of {{c}} M Na₂S₂O₃. Find n. (CuSO₄ = 159.61, H₂O = 18.015 g/mol)",
          given={"m": {"pick": [0.5, 0.75, 1]}, "c": {"pick": [0.1, 0.05]}, "n": {"pick": [5, 3, 1]}}, let={"V": "m/(159.61 + n*18.015)*1000/c"},
          value="n", tex="n", tol=0.02, final=True, pace="workout", verify="solve(Eq(nsimplify(m)/(Rational(15961, 100) + x*Rational(18015, 1000)), nsimplify(m)/(Rational(15961, 100) + n*Rational(18015, 1000))), x)[0]",
          explain="Thiosulfate counts copper one for one through the iodine. The molar mass of the hydrate follows, and the water is what is left after CuSO₄")], std=["usnco:P2", "usnco:1"]),
        L("E", "Find a density and an oxidation state from a perovskite unit cell.", "ABO₃: A at the corners (1), B at the centre (1), O at the face centres (3).", [], [
        Q("co-p2-perovskite", "olympiad.states", "{{f}} is a cubic perovskite with edge {{a}} pm (formula mass {{M}} g/mol). What is its density, in g/cm³? ($N_A = 6.022\\times10^{23}$)",
          cases=[{"f": "SrTiO₃", "a": 390.5, "M": 183.49}, {"f": "BaTiO₃", "a": 401.0, "M": 233.19}, {"f": "CaTiO₃ (idealised cubic)", "a": 384.0, "M": 135.94}],
          value="M/(6.022e23*(a*1e-10)^3)", tex="\\rho", tol=0.005, pace="workout", verify="nsimplify(M)/(Rational(6022, 1000)*10**23*(nsimplify(a)/10**10)**3)",
          explain="Corners ⅛ × 8 = 1 A, body centre 1 B, faces ½ × 6 = 3 O: one formula unit per cell. Ti is +4 by charge balance with Sr²⁺ and three O²⁻")], std=["usnco:P2", "usnco:3"]),
        L("F", "Find a photon energy per mole for bond breaking.", "E = N_A hc/λ.", [], [
        Q("co-p2-photon-kj", "olympiad.atomic", "What is the energy of a mole of photons of wavelength {{l}} nm, in kJ/mol? Can it break a bond of {{Db}} kJ/mol? (Answer the energy; $h = 6.626\\times10^{-34}$, $c = 2.998\\times10^{8}$, $N_A = 6.022\\times10^{23}$)",
          given={"l": {"pick": [200, 254, 300, 400, 600]}, "Db": {"pick": [146, 498, 350]}}, value="6.022e23*6.626e-34*2.998e8/(l*1e-9)/1000", tex="E", tol=0.005, pace="workout",
          verify="Rational(6022, 1000)*10**23*Rational(6626, 1000)*10**-34*Rational(2998, 1000)*10**8/(l*Rational(1, 10**9))/1000",
          explain="About 120000/λ(nm) kJ/mol: ultraviolet below ~240 nm can split O₂ (498 kJ/mol); visible light breaks only weak bonds such as the O–O in peroxides")], std=["usnco:P2", "usnco:8"]),
])]),
]
