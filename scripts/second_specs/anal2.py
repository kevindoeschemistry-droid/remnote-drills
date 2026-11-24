"""Second question types for Analytical Chemistry (AN): each objective's first item computes the textbook result; these
run it in reverse, as a scaling, or as the reasoning behind the method."""
from opl_dsl import Q

FILE, FRAMEWORK = "an-second-types", "analytical-chemistry"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"


def facts(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("AN-1.1.A", Q("an-back-titration-volume", "anal.titration", "A {{m}} g sample of pure CaCO₃ (M = 100.09 g/mol) is dissolved in {{V1}} mL of {{c1}} M HCl, an excess. What volume of {{c2}} M NaOH, in mL, titrates the HCl left over?",
        given={"m": {"pick": [0.3, 0.45, 0.6]}, "V1": {"pick": [50, 60]}, "c1": {"pick": [0.5]}, "c2": {"pick": [0.2, 0.25]}},
        value="(V1*c1 - 2*m/100.09*1000)/c2", tex="V", verify=f"solve(Eq({n('c2')}*x + 2*{n('m')}*1000/Rational(10009, 100), {n('V1')}*{n('c1')}), x)[0]",
        explain="Acid added = acid used by the carbonate (2 per CaCO₃) + acid left for the base")),
    ("AN-1.1.B", Q("an-dichromate-for-permanganate", "anal.titration", "An iron(II) sample needs {{V}} mL of {{c}} M KMnO₄. How many mL of {{c}} M K₂Cr₂O₇ would the same sample need?",
        given={"V": {"pick": [18, 24, 30]}, "c": {"pick": [0.02, 0.0167]}}, value="V*5/6", tex="V",
        verify=f"{n('V')}*{n('c')}*half_electrons('MnO4', -1, 'Mn', 2, 'Mn')/({n('c')}*half_electrons('Cr2O7', -2, 'Cr', 3, 'Cr'))",
        explain="Same electrons: each permanganate takes 5, each dichromate 6")),
    ("AN-1.1.C", Q("an-edta-volume", "anal.titration", "Water with hardness {{Hd}} mg CaCO₃/L is titrated with {{c}} M EDTA. What volume of EDTA, in mL, does a {{Vs}} mL sample need? (CaCO₃ 100.09 g/mol)",
        given={"Hd": {"pick": [120, 180, 250]}, "c": {"pick": [0.01, 0.02]}, "Vs": {"pick": [50, 100]}}, value="Hd*Vs/1000/100.09/c", tex="V",
        verify=f"solve(Eq({n('c')}*x, {n('Hd')}*{n('Vs')}/1000/Rational(10009, 100)), x)[0]", explain="EDTA binds each Ca²⁺ or Mg²⁺ 1:1, so mmol EDTA = mmol 'CaCO₃'")),
    ("AN-1.1.D", facts("an-argentometry-why", "anal.titration", [
        ("Why is a Mohr titration run near neutral pH?", "In acid, chromate turns to dichromate and the end point comes late; in base, silver oxide precipitates", "Silver chloride dissolves in acid", "Chloride is oxidised in base", "The indicator is a pH indicator"),
        ("In a Volhard titration, what is titrated at the end?", "The excess Ag⁺, with SCN⁻ and an Fe³⁺ indicator", "Chloride, with chromate", "Ag⁺ with EDTA", "Fe³⁺ with thiocyanate in base"),
        ("How does a Fajans (adsorption) indicator signal the end point?", "It adsorbs on the charged precipitate surface once the charge reverses, changing colour", "It precipitates with Ag⁺", "It changes with pH", "It forms a complex with chloride"),
    ], "Each argentometric method differs only in how it sees the first excess of silver")),
    ("AN-1.1.E", Q("an-kjeldahl-ammonia", "anal.titration", "A food is {{P}}% protein (Kjeldahl factor 6.25). How many mmol of NH₃ does a {{m}} g sample release on digestion? (N 14.007 g/mol)",
        given={"P": {"pick": [8, 12.5, 20]}, "m": {"pick": [0.5, 1, 1.5]}}, value="P/100*m/6.25/14.007*1000", tex="n",
        verify=f"{n('P')}/100*{n('m')}*Rational(4, 25)*1000/Rational(14007, 1000)", explain="Protein × (1/6.25) is nitrogen; each N gives one NH₃")),
    ("AN-1.2.A", Q("an-quarter-equivalence", "anal.titration", "A weak acid with pKa {{pk}} is titrated with NaOH. What is the pH when {{f}} of the base needed for equivalence has been added?",
        cases=[{"f": "one quarter", "fr": 0.25}, {"f": "three quarters", "fr": 0.75}, {"f": "one tenth", "fr": 0.1}], given={"pk": {"pick": [3.75, 4.76, 7.2]}},
        value="pk + log10(fr/(1 - fr))", tex="\\mathrm{pH}", verify=f"{n('pk')} + log({n('fr')}/(1 - {n('fr')}))/log(10)",
        explain="Before equivalence the solution is a buffer: pH = pKa + log(base/acid)")),
    ("AN-1.2.B", facts("an-indicator-titration", "anal.titration", [
        ("Phenolphthalein (range 8.2–10) suits which titration?", "A weak acid with a strong base", "A weak base with a strong acid", "Two weak partners", "None"),
        ("Methyl orange (range 3.1–4.4) suits which titration?", "A weak base with a strong acid", "A weak acid with a strong base", "Acetic acid with ammonia", "None"),
        ("Why is a weak acid–weak base titration hard to follow with an indicator?", "The pH changes too gently at equivalence", "No equivalence exists", "Indicators react with weak acids", "The pH never changes"),
    ], "The equivalence pH sits on the side of the stronger partner; the indicator's range must sit inside the steep part")),
    ("AN-2.1.A", Q("an-gravimetric-expected", "anal.gravimetry", "A {{m}} g sample is {{pct}}% {{an}} by mass. What mass of {{ppt}}, in g, should precipitate? ({{an}} {{Ma}} g/mol, {{ppt}} {{Mp}} g/mol)",
        cases=[{"an": "sulfate", "ppt": "BaSO₄", "Ma": 96.06, "Mp": 233.39}, {"an": "chloride", "ppt": "AgCl", "Ma": 35.45, "Mp": 143.32},
               {"an": "nickel", "ppt": "Ni(DMG)₂", "Ma": 58.693, "Mp": 288.91}],
        given={"m": {"pick": [0.25, 0.5, 0.8]}, "pct": {"pick": [10, 25, 40]}}, value="m*pct/100/Ma*Mp", tex="m",
        verify=f"solve(Eq(x/{n('Mp')}, {n('m')}*{n('pct')}/100/{n('Ma')}), x)[0]", explain="Mass of precipitate = mass of analyte × (M precipitate / M analyte), with the formula ratio")),
    ("AN-3.1.A", Q("an-common-ion-factor", "anal.equilibria", "AgCl has Ksp {{K}}. By what factor is its solubility in {{c}} M NaCl smaller than in pure water? (Solve the quadratic.)",
        given={"K": {"pick": [1.8e-10]}, "c": {"pick": [0.001, 0.01, 0.1]}}, value="sqrt(K)/(2*K/(c + sqrt(c^2 + 4*K)))", tex="s_0/s",
        verify=f"sqrt({n('K')})/Max(*solve(Eq(x*(x + {n('c')}), {n('K')}), x))", explain="With a common ion, s ≈ Ksp/c, which is far below √Ksp")),
    ("AN-3.1.B", facts("an-complex-dissolve", "anal.equilibria", [
        ("Which reagent dissolves AgCl but not AgI?", "Aqueous ammonia", "Thiosulfate", "Nitric acid", "Water"),
        ("Why does photographic 'hypo' (thiosulfate) fix film?", "It dissolves unexposed silver halide as [Ag(S₂O₃)₂]³⁻", "It reduces Ag⁺ to silver", "It oxidises silver", "It precipitates more AgBr"),
        ("Adding a large excess of chloride to AgCl does what?", "Slightly raises its solubility, by forming AgCl₂⁻", "Always lowers it further", "Has no effect", "Oxidises it"),
    ], "A ligand that binds the cation pulls the dissolution equilibrium to the right")),
    ("AN-4.1.A", Q("an-extractions-needed", "anal.separations", "A solute with distribution ratio D = {{Dd}} is extracted from {{Vw}} mL of water with {{Vo}} mL portions of organic solvent. How many extractions leave less than {{f}}% in the water?",
        given={"Dd": {"pick": [2, 3, 5]}, "Vw": {"pick": [100]}, "Vo": {"pick": [25, 50]}, "f": {"pick": [1, 5]}},
        value="ceil(log(f/100)/log(Vw/(Vw + Dd*Vo)))", tex="n", final=True,
        verify=f"ceiling(log({n('f')}/100)/log({n('Vw')}/({n('Vw')} + {n('Dd')}*{n('Vo')})))", explain="Each extraction leaves the same fraction Vw/(Vw + D·Vo); repeat until the product falls below the target")),
    ("AN-4.1.B", Q("an-resolution-length", "anal.separations", "Two peaks are resolved with Rs = {{R1}}. The column is made {{f}} times longer (same packing). What is the new resolution?",
        given={"R1": {"pick": [0.8, 1.0, 1.2]}, "f": {"pick": [2, 3, 4]}}, value="R1*sqrt(f)", tex="R_s",
        verify=f"Max(*solve(Eq((x/{n('R1')})**2, {n('f')}), x))", explain="Rs grows with √N and N with length, so doubling the column gives only √2")),
    ("AN-5.1.A", Q("an-beer-reverse", "anal.measurement", "A solution has absorbance {{A}} in a {{b}} cm cell at a wavelength where ε = {{eps}} L/(mol·cm). What is its concentration, in μmol/L?",
        given={"A": {"pick": [0.25, 0.48, 0.73]}, "b": {"pick": [1, 2]}, "eps": {"pick": [6000, 15000, 22000]}}, value="A/(eps*b)*1e6", tex="c",
        verify=f"solve(Eq({n('eps')}*{n('b')}*x/10**6, {n('A')}), x)[0]", explain="A = εbc; keep absorbances between about 0.1 and 1 for the best precision")),
    ("AN-5.1.B", Q("an-spike-signal", "anal.measurement", "An unknown at {{cx}} ppm gives a signal of {{S1}}. A spike raises the concentration by {{dc}} ppm with negligible volume change. What signal is expected?",
        given={"cx": {"pick": [2, 4, 5]}, "S1": {"pick": [0.2, 0.35]}, "dc": {"pick": [1, 2, 5]}}, value="S1*(cx + dc)/cx", tex="S_2",
        verify=f"solve(Eq(x/({n('cx')} + {n('dc')}), {n('S1')}/{n('cx')}), x)[0]", explain="Signal is proportional to concentration in the same matrix, which is the point of adding the standard to the sample")),
    ("AN-5.1.C", Q("an-detection-limit", "anal.measurement", "A calibration line has slope {{m}} per ppm, and replicate blanks have standard deviation {{s}}. What is the detection limit (3s/slope), in ppm?",
        given={"m": {"pick": [0.052, 0.125, 0.31]}, "s": {"pick": [0.0012, 0.003, 0.005]}}, value="3*s/m", tex="\\mathrm{LOD}",
        verify=f"solve(Eq({n('m')}*x, 3*{n('s')}), x)[0]", explain="The smallest concentration whose signal stands three blank standard deviations above the blank")),
    ("AN-5.2.A", Q("an-q-value", "anal.measurement", "Replicates are {{v1}}, {{v2}}, {{v3}}, {{v4}} and {{v5}}, with {{v1}} suspect. What is Q?",
        cases=[{"v1": 10.02, "v2": 10.20, "v3": 10.24, "v4": 10.25, "v5": 10.29}, {"v1": 4.71, "v2": 4.86, "v3": 4.88, "v4": 4.90, "v5": 4.92},
               {"v1": 0.512, "v2": 0.530, "v3": 0.531, "v4": 0.534, "v5": 0.537}],
        value="(v2 - v1)/(v5 - v1)", tex="Q", verify=f"({n('v2')} - {n('v1')})/({n('v5')} - {n('v1')})",
        explain="Q = gap to the nearest neighbour ÷ range; reject only if Q exceeds the table value")),
    ("AN-5.2.B", Q("an-uncertainty-product", "anal.measurement", "A result is the product of {{k}} measured quantities, each with {{r}}% relative uncertainty (independent). What is the result's relative uncertainty, in %?",
        given={"k": {"pick": [2, 3, 4]}, "r": {"pick": [0.5, 1, 2]}}, value="r*sqrt(k)", tex="\\%", verify=f"sqrt({n('k')}*{n('r')}**2)",
        explain="Relative uncertainties add in quadrature for products and quotients")),
    ("AN-5.2.C", facts("an-technique-measures", "anal.measurement", [
        ("What does ICP-MS measure?", "Trace elements, by mass of their ions", "Molecular structure", "Functional groups", "Optical rotation"),
        ("What does gas chromatography separate?", "Volatile compounds, by partition between a gas and a stationary phase", "Proteins by size", "Ions by charge in a gel", "Metals in solution"),
        ("What does atomic absorption spectroscopy measure?", "One element at a time, by light absorbed by free atoms", "Molecular mass", "Several bonds at once", "Crystal structure"),
    ], "Match the technique to what it sees: atoms, ions, molecules or structure")),
]
