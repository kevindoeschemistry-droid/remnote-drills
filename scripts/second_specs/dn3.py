"""Dental materials depth (INBDE unit 4, FK3): Weibull reliability, degree of conversion, filler fractions, ISO 4049
solubility, adhesive systems, bond-strength tests and zirconia versus glass ceramics. Two types per new objective.
Kevin sits on ADA materials committees and checks this content; the ISO 4049 limits and the strength bands were written
from memory of the standards and reviews, not read from the standards' text."""
from opl_dsl import Q

FILE, FRAMEWORK = "dn-materials-depth", "inbde"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"


def facts(name, rows, explain, pace="recall"):
    return Q(name, "dent.materials", "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("DN-4.1.C", Q("dn-weibull-failure", "dent.materials", "A ceramic has Weibull characteristic strength σ₀ = {{s0}} MPa and Weibull modulus m = {{m}}. What fraction of specimens fail at or below {{s0*f}} MPa, in %?",
        given={"s0": {"pick": [400, 900, 1200]}, "m": {"pick": [5, 8, 12]}, "f": {"pick": [0.6, 0.8, 1.0]}}, value="100*(1 - exp(-(f)^m))", tex="P_f",
        verify=f"100*(1 - exp(-({n('f')}*s0/s0)**m))", explain="P_f = 1 − exp(−(σ/σ₀)^m); at σ = σ₀ it is always 63.2%. Higher m means strengths cluster, so the material is more predictable")),
    ("DN-4.1.C", Q("dn-weibull-design-stress", "dent.materials", "A material has σ₀ = {{s0}} MPa and m = {{m}}. Below what stress, in MPa, do only {{pf}}% of specimens fail?",
        given={"s0": {"pick": [400, 900, 1200]}, "m": {"pick": [5, 8, 12]}, "pf": {"pick": [1, 5, 10]}}, value="s0*(-log(1 - pf/100))^(1/m)", tex="\\sigma",
        verify=f"s0*(log(1/(1 - Rational(pf, 100))))**Rational(1, m)", explain="Invert P_f: σ = σ₀(−ln(1 − P_f))^{1/m}. A low m drags the safe stress far below σ₀")),
    ("DN-4.2.C", Q("dn-degree-conversion", "dent.materials", "FTIR of a composite: the aliphatic C=C (1638 cm⁻¹) to aromatic (1608 cm⁻¹) peak ratio is {{ru}} before curing and {{rc}} after. What is the degree of conversion, in %?",
        given={"ru": {"pick": [1.2, 1.5, 1.8]}, "rc": {"pick": [0.45, 0.6, 0.75]}}, value="100*(1 - rc/ru)", tex="DC",
        verify=f"100*({n('ru')} - {n('rc')})/{n('ru')}", explain="The aromatic ring does not react, so it normalises the sample amount; dimethacrylate composites usually reach about 55–75%")),
    ("DN-4.2.C", Q("dn-ratio-for-dc", "dent.materials", "Uncured, the 1638/1608 cm⁻¹ peak ratio is {{ru}}. What cured ratio corresponds to a degree of conversion of {{dc}}%?",
        given={"ru": {"pick": [1.2, 1.5, 1.8]}, "dc": {"pick": [50, 60, 70]}}, value="ru*(1 - dc/100)", tex="R_c",
        verify=f"solve(Eq(1 - x/{n('ru')}, Rational(dc, 100)), x)[0]", explain="Unreacted fraction × uncured ratio: the remaining C=C is what the 1638 band still sees")),
    ("DN-4.2.D", Q("dn-filler-volume", "dent.materials", "A composite is {{w}}% filler by weight. Filler density {{rf}} g/cm³, resin {{rr}} g/cm³. What is the filler volume fraction, in %?",
        given={"w": {"pick": [60, 75, 85]}, "rf": {"pick": [2.5, 3.0]}, "rr": {"pick": [1.1, 1.2]}}, value="100*(w/rf)/(w/rf + (100 - w)/rr)", tex="\\varphi_v",
        verify=f"100/(1 + (100 - w)*{n('rf')}/(w*{n('rr')}))", explain="Divide each mass by its density to get volumes; dense glass fillers make volume % well below weight %")),
    ("DN-4.2.D", Q("dn-filler-weight", "dent.materials", "A composite must be {{v}}% filler by volume. Filler density {{rf}} g/cm³, resin {{rr}} g/cm³. What weight percentage of filler is that?",
        given={"v": {"pick": [50, 60, 70]}, "rf": {"pick": [2.5, 3.0]}, "rr": {"pick": [1.1, 1.2]}}, value="100*v*rf/(v*rf + (100 - v)*rr)", tex="w",
        verify=f"solve(Eq(100*(x/{n('rf')})/(x/{n('rf')} + (100 - x)/{n('rr')}), v), x)[0]", explain="Weight follows volume × density: manufacturers usually quote the larger weight figure")),
    ("DN-4.2.E", Q("dn-solubility", "dent.materials", "An ISO 4049 disc (15 mm across, {{h}} mm thick) weighs {{m1}} mg conditioned and {{m3}} mg after water storage and re-drying. What is its solubility, in µg/mm³?",
        given={"h": {"pick": [1]}, "m1": {"pick": [342.6, 355.1, 360.4]}, "m3": {"pick": [341.8, 341.2, 339.9]}}, value="(m1 - m3)*1000/(pi*7.5^2*h)", tex="W_{sl}",
        verify=f"({n('m1')} - {n('m3')})*1000/(pi*Rational(15, 2)**2*h)", explain="Solubility = (m₁ − m₃)/V: mass lost on re-drying per volume. ISO 4049 allows at most 7.5 µg/mm³")),
    ("DN-4.2.E", Q("dn-max-mass-loss", "dent.materials", "An ISO 4049 disc is 15 mm across and {{h}} mm thick. What is the largest mass loss, in mg, that still meets the 7.5 µg/mm³ solubility limit?",
        given={"h": {"pick": [1, 1.5, 2]}}, value="7.5*pi*7.5^2*h/1000", tex="\\Delta m", verify=f"solve(Eq(x*1000/(pi*Rational(15, 2)**2*{n('h')}), Rational(15, 2)), x)[0]",
        explain="Limit × volume: about 1.3 mg for a standard 1 mm disc, so weighing to 0.01 mg matters")),
    ("DN-4.4.C", facts("dn-adhesive-class", [
        ("Which system applies phosphoric acid, then a separate primer, then a bonding resin?", "Three-step etch-and-rinse", "Two-step self-etch", "One-step self-etch", "Glass ionomer"),
        ("What does 10-MDP add to an adhesive?", "Chemical bonding to calcium in hydroxyapatite (and to zirconia)", "Fluoride release only", "Opacity", "Faster light curing"),
        ("What is the hybrid layer?", "Resin infiltrated into demineralised dentin around the collagen network", "A layer of glass ionomer", "Enamel prisms after etching", "The smear layer"),
        ("A universal adhesive can be used how?", "In etch-and-rinse, selective-enamel-etch or self-etch mode", "Only after phosphoric acid", "Only without any acid", "Only on ceramics"),
    ], "Classify by how the smear layer is handled: removed by acid and rinsed, or dissolved and kept by acidic monomers")),
    ("DN-4.4.C", facts("dn-adhesive-scenario", [
        ("A mild self-etch adhesive is used on a large area of uncut enamel. What improves the enamel bond?", "Selective etching of the enamel with phosphoric acid first", "Air-drying the dentin hard", "Skipping light curing", "A eugenol liner"),
        ("With an acetone-based etch-and-rinse adhesive, how should the dentin be left after rinsing?", "Visibly moist, so the collagen does not collapse", "Desiccated with strong air", "Coated with ZOE", "Re-etched for 60 s"),
        ("A temporary cement containing eugenol was used before a resin restoration. Why does it matter?", "Residual eugenol can inhibit resin polymerization", "Eugenol strengthens the bond", "It has no effect", "It etches enamel"),
    ], "Most bonding failures are technique: enamel etching, dentin wetness and contamination")),
    ("DN-4.4.D", Q("dn-bond-strength", "dent.materials", "A {{test}} specimen with a bonded area of {{A}} mm² fails at {{F}} N. What is the bond strength, in MPa?",
        cases=[{"test": "microtensile", "A": 0.9}, {"test": "microtensile", "A": 1.1}, {"test": "shear", "A": 7.07}, {"test": "shear", "A": 3.14}],
        given={"F": {"pick": [18, 26, 35, 140]}}, value="F/A", tex="\\sigma", verify=f"solve(Eq(x*{n('A')}, F), x)[0]",
        explain="MPa = N/mm²: the small microtensile area puts the stress at the interface and spreads fewer defects across it")),
    ("DN-4.4.D", Q("dn-load-for-strength", "dent.materials", "An adhesive bonds at about {{s}} MPa in microtensile tests. Roughly what load, in N, breaks a beam of {{A}} mm²?",
        given={"s": {"pick": [25, 35, 45, 55]}, "A": {"pick": [0.8, 1.0, 1.2]}}, value="s*A", tex="F", verify=f"solve(Eq(x/{n('A')}, s), x)[0]",
        explain="F = σA: a 1 mm² beam at 40 MPa breaks near 40 N")),
    ("DN-4.4.E", facts("dn-ceramic-class", [
        ("Which material is strongest in flexure?", "3Y-TZP zirconia (about 1000 MPa or more)", "5Y zirconia (about 600–800 MPa)", "Lithium disilicate (about 350–450 MPa)", "Feldspathic porcelain (about 100 MPa)"),
        ("Why is 5Y zirconia more translucent but weaker than 3Y?", "More cubic phase, which scatters less light and cannot transformation-toughen", "It has more alumina", "It is a glass ceramic", "It is etched with HF"),
        ("What is transformation toughening in zirconia?", "Tetragonal grains near a crack tip turn monoclinic, expand and squeeze the crack shut", "Glass fills cracks", "Silane bonds the crack", "The crack is etched away"),
        ("Which ceramic can be etched with hydrofluoric acid and silanated?", "Lithium disilicate", "3Y-TZP zirconia", "Alumina", "5Y zirconia"),
    ], "Strength, translucency and bondability trade off: zirconia is strong and needs MDP; glass ceramics etch and silanate")),
    ("DN-4.4.E", facts("dn-ceramic-scenario", [
        ("A posterior bridge for a bruxer, with little room for thickness. Which material?", "3Y or 4Y zirconia", "Feldspathic veneers", "5Y zirconia thin connectors", "Composite resin only"),
        ("A thin anterior veneer where esthetics and adhesive bonding matter most. Which material?", "Lithium disilicate or feldspathic ceramic, etched and silanated", "3Y-TZP zirconia", "Base-metal alloy", "Zinc phosphate"),
        ("A zirconia crown must be bonded with resin cement. Which surface treatment?", "Low-pressure alumina air abrasion and an MDP-containing primer", "Hydrofluoric acid and silane", "Phosphoric acid only", "No treatment: it bonds itself"),
    ], "Choose by the clinical demand: strength for long spans and bruxers, translucency and etchability for veneers")),
]
