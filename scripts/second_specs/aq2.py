"""Second question types for Anchor Quantities (AQ): each magnitude used once in a short calculation or asked in
reverse, checked against the CODATA constants and atomic weights in tests/verify/data.py (CONST, c_*)."""
from opl_dsl import Q

FILE, FRAMEWORK = "aq-second-types", "anchor-quantities"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"
R = "8.31446261815324"
FLOZ = "29.5735295625"  # US fluid ounce in mL, exact by definition
M = {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "Na": 22.990, "S": 32.06, "Cl": 35.45, "Ca": 40.078, "Fe": 55.845, "K": 39.098, "P": 30.974}

ADD = [
    ("AQ-1.1.A", Q("aq-kitchen-ratio", "k8.measurement", "From memory: how many {{small}} make one {{big}} (US)?", pace="recall",
        cases=[{"small": "teaspoons", "big": "tablespoon", "a": 1 / 6, "b": 1 / 2}, {"small": "tablespoons", "big": "fluid ounce", "a": 1 / 2, "b": 1},
               {"small": "tablespoons", "big": "cup", "a": 1 / 2, "b": 8}, {"small": "fluid ounces", "big": "cup", "a": 1, "b": 8},
               {"small": "teaspoons", "big": "fluid ounce", "a": 1 / 6, "b": 1}],
        value="b/a", tex="n", final=True, verify=f"({n('b')}*{FLOZ})/({n('a')}*{FLOZ})",
        explain="3 tsp = 1 tbsp, 2 tbsp = 1 fl oz, 8 fl oz = 1 cup (so 16 tbsp)")),
    ("AQ-1.1.B", Q("aq-spoons-per-mole", "k8.measurement", "About how many teaspoons (5 mL) of water make one mole?", pace="quick",
        cases=[{"ml": 5}], value=f"(2*{M['H']} + {M['O']})/ml", tex="n", tol=0.05,
        verify="(2*c_M['H'] + c_M['O'])/ml", explain="A mole of water is 18 g, about 18 mL: three and a half teaspoons")),
    ("AQ-2.1.A", Q("aq-rt-at-t", "stat.boltzmann", "Estimate RT at {{t}} °C, in kJ/mol.", pace="quick",
        given={"t": {"pick": [0, 37, 100, -196, 500]}}, value=f"{R}*(t + 273.15)/1000", tex="RT", tol=0.03,
        verify="c_R*(t + Rational(27315, 100))/1000", explain="RT is 2.48 kJ/mol at 25 °C; scale by the absolute temperature")),
    ("AQ-2.1.B", Q("aq-gap-for-ratio", "stat.boltzmann", "What energy gap, in units of k_BT, makes the upper state {{r}} times less populated than the lower one?", pace="quick",
        given={"r": {"pick": [10, 100, 1000, 1000000]}}, value="log(r)", tex="\\Delta E/k_BT", tol=0.05, verify="solve(Eq(exp(x), r), x)[0]",
        explain="Each factor of 10 costs ln 10 ≈ 2.3 k_BT")),
    ("AQ-2.2.A", Q("aq-dg-for-factor", "pchem.gibbs", "At 25 °C, how much must ΔG° change, in kJ/mol, to change K by a factor of {{f}}?", pace="quick",
        given={"f": {"pick": [100, 1000, 1000000]}}, value=f"{R}*298.15*log(f)/1000", tex="\\Delta\\Delta G", tol=0.03,
        verify="c_R*Rational(29815, 100)*log(f)/1000", explain="5.7 kJ/mol per factor of 10, so 11.4 for 100 and 34 for a million")),
    ("AQ-2.2.B", Q("aq-k-to-dg", "pchem.gibbs", "A reaction has K = 10^{{k}} at 25 °C. About what is ΔG°, in kJ/mol?", pace="quick",
        given={"k": {"pick": [-6, -3, 2, 5, 10]}}, value=f"-{R}*298.15*k*log(10)/1000", tex="\\Delta G^\\circ", tol=0.03,
        verify="-c_R*Rational(29815, 100)*log(Integer(10)**k)/1000", explain="ΔG° ≈ −5.7 × log₁₀K kJ/mol")),
    ("AQ-3.1.A", Q("aq-ev-to-nm", "quantum.origins", "A photon carries {{e}} eV. About what is its wavelength, in nm?", pace="quick",
        given={"e": {"pick": [1.5, 2.0, 2.5, 3.1, 4.0, 10]}}, value="1239.841984/e", tex="\\lambda", tol=0.03,
        verify=f"c_h*c_c/({n('e')}*c_e)*10**9", explain="λ(nm) ≈ 1240 / E(eV): 2 eV is red, 3 eV violet")),
    ("AQ-4.1.A", Q("aq-moles-in-flask", "pchem.real-gases", "About how many moles of an ideal gas fill {{V}} L at {{t}} °C and 1 atm?", pace="quick",
        given={"V": {"pick": [1, 5, 22.4]}, "t": {"pick": [0, 25, 37]}}, value=f"101325*V/1000/({R}*(t + 273.15))", tex="n", tol=0.03,
        verify="c_atm*nsimplify(V)/1000/(c_R*(t + Rational(27315, 100)))", explain="22.4 L/mol at 0 °C, 24.5 at 25 °C: divide the volume by the molar volume")),
    ("AQ-4.2.A", Q("aq-element-from-mass", "pchem.thermochemistry", "Which element has an atomic mass of about {{m}} g/mol?", pace="recall",
        cases=[{"m": M[e], "s1": e, "o1": e, "o2": a, "o3": b, "o4": c} for e, a, b, c in
               (("S", "P", "Cl", "O"), ("Cl", "S", "K", "Ar"), ("Ca", "K", "Fe", "Na"), ("Fe", "Ca", "Ni", "Cu"), ("Na", "Mg", "K", "Al"), ("P", "S", "Si", "N"), ("K", "Ca", "Na", "Cl"))],
        choice=MC, correct="0", verify="0 if Abs(c_M[s1] - nsimplify(m)) < Rational(1, 100) else 9",
        explain="Learn the dozen common masses to one decimal: Na 23.0, P 31.0, S 32.1, Cl 35.5, K 39.1, Ca 40.1, Fe 55.8")),
    ("AQ-4.2.B", Q("aq-mass-percent", "pchem.thermochemistry", "In your head: what percentage of the mass of {{f}} is {{el}}?", pace="quick",
        cases=[{"f": "water", "el": "oxygen", "nC": 0, "nH": 2, "nN": 0, "nO": 1, "w": "O", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["O"], "k": 1},
               {"f": "glucose, C₆H₁₂O₆", "el": "carbon", "nC": 6, "nH": 12, "nN": 0, "nO": 6, "w": "C", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["C"], "k": 6},
               {"f": "urea, CH₄N₂O", "el": "nitrogen", "nC": 1, "nH": 4, "nN": 2, "nO": 1, "w": "N", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["N"], "k": 2},
               {"f": "ethanol, C₂H₆O", "el": "carbon", "nC": 2, "nH": 6, "nN": 0, "nO": 1, "w": "C", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["C"], "k": 2},
               {"f": "carbon dioxide", "el": "carbon", "nC": 1, "nH": 0, "nN": 0, "nO": 2, "w": "C", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["C"], "k": 1},
               {"f": "ammonia", "el": "nitrogen", "nC": 0, "nH": 3, "nN": 1, "nO": 0, "w": "N", "mw": {"O": 15.999, "C": 12.011, "N": 14.007}["N"], "k": 1}],
        value=f"100*k*mw/({M['C']}*nC + {M['H']}*nH + {M['N']}*nN + {M['O']}*nO)",
        tex="\\%", tol=0.01,
        verify="100*k*c_M[w]/(c_M['C']*nC + c_M['H']*nH + c_M['N']*nN + c_M['O']*nO)", explain="Element mass × count ÷ molar mass")),
    ("AQ-5.1.A", Q("aq-dna-length", "quantum.model-systems", "About how long, in µm, is a stretch of B-DNA of {{kb}} kilobase pairs?", pace="quick",
        given={"kb": {"pick": [1, 10, 48.5, 4600]}}, value="kb*1000*0.34/1000", tex="L", tol=0.03,
        verify=f"{n('kb')}*1000*Rational(34, 100)/1000", explain="0.34 nm per base pair: E. coli's 4.6 Mbp genome is about 1.6 mm long")),
    ("AQ-6.1.A", Q("aq-ribosome-time", "stat.rates", "About how many seconds does a bacterial ribosome take to make a {{nres}}-residue protein?", pace="quick",
        given={"nres": {"pick": [150, 300, 600, 1200]}}, value="nres/15", tex="t", tol=0.34,
        verify="Rational(nres, 15)", explain="About 15 amino acids per second in bacteria: a typical protein in 20–40 s")),
    ("AQ-6.1.B", Q("aq-one-molecule-conc", "stat.binding", "One molecule sits in a volume of {{vol}} µm³. What concentration is that, in nM?", pace="quick",
        given={"vol": {"pick": [1, 0.1, 1000, 4000]}}, value="1/(6.02214076e23*vol*1e-15)*1e9", tex="c", tol=0.03,
        verify="1/(c_NA*nsimplify(vol)*Rational(1, 10**15))*10**9", explain="In an E. coli of 1 µm³, one copy is about 1.7 nM: a handy floor for any count")),
]
