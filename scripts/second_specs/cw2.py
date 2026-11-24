"""Second question types for Cotton & Wilkinson (IA): calculations in reverse (Latimer steps, skeletal pairs, d and f counts,
18-electron counts, Landé g), and the per-metal facts asked the other way round (property → metal). Numeric keys go
through cwcalc and incalc."""
from opl_dsl import Q

FILE, FRAMEWORK = "cw-second-types", "inorganic-advanced"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
n = lambda v: f"nsimplify({v})"


def facts(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def which(name, rows, explain, skill="inorg.transition"):
    """property → metal"""
    return facts(name, skill, rows, explain)


ADD = [
    ("IA-1.1.A", facts("cw-hsab-predict", "inorg.cross-cutting", [
        ("Which halide does Ag⁺ bind most strongly?", "I⁻", "F⁻", "Cl⁻", "Br⁻"),
        ("In nature, mercury occurs mainly as which mineral?", "HgS (cinnabar)", "HgO", "HgCO₃", "HgF₂"),
        ("Which donor atom does Al³⁺ prefer?", "Oxygen or fluorine", "Sulfur", "Phosphorus", "Iodine"),
        ("Which ligand binds Pt(II) more strongly in water?", "A thioether (S donor)", "Water", "Fluoride", "Nitrate"),
    ], "Hard acids (small, highly charged) prefer hard bases (F, O); soft acids (large, polarisable) prefer soft bases (S, I, P)")),
    ("IA-1.1.B", Q("cw-latimer-missing", "inorg.cross-cutting", "{{pair}}: E°({{a}}, {{n1}} e⁻) = {{e1}} V and E°({{whole}}, {{nt}} e⁻) = {{Et}} V. What is E° for the remaining step, {{b}}, in V?",
        cases=[{"pair": "Iron", "a": "Fe³⁺/Fe²⁺", "n1": 1, "e1": 0.771, "whole": "Fe³⁺/Fe", "nt": 3, "Et": -0.037, "b": "Fe²⁺/Fe"},
               {"pair": "Copper", "a": "Cu²⁺/Cu⁺", "n1": 1, "e1": 0.153, "whole": "Cu²⁺/Cu", "nt": 2, "Et": 0.337, "b": "Cu⁺/Cu"},
               {"pair": "Manganese (acid)", "a": "MnO₄⁻/MnO₄²⁻", "n1": 1, "e1": 0.564, "whole": "MnO₄⁻/MnO₂", "nt": 3, "Et": 1.70, "b": "MnO₄²⁻/MnO₂"},
               {"pair": "Chromium", "a": "Cr³⁺/Cr²⁺", "n1": 1, "e1": -0.41, "whole": "Cr³⁺/Cr", "nt": 3, "Et": -0.74, "b": "Cr²⁺/Cr"}],
        value="(nt*Et - n1*e1)/(nt - n1)", tex="E^\\circ", verify=f"solve(Eq(cw_latimer(n1, e1, nt - n1, x), {n('Et')}), x)[0]",
        explain="Free energies add: n_tE_t = n₁E₁ + n₂E₂, so potentials are weighted by electrons, never simply added")),
    ("IA-1.1.C", facts("cw-disprop-cases", "inorg.cross-cutting", [
        ("What happens to MnO₄²⁻ when its alkaline solution is acidified?", "It disproportionates to MnO₄⁻ and MnO₂", "It is stable", "It is reduced to Mn²⁺ only", "It is oxidised to MnO₄⁻ only"),
        ("Hypochlorite is heated in base. What forms?", "Chloride and chlorate", "Chlorine gas", "Perchlorate only", "Chlorite only"),
        ("On a Latimer diagram, when does a species disproportionate?", "When the potential to its right exceeds the one to its left", "When both potentials are negative", "When the left potential is larger", "Never in water"),
    ], "A species is unstable when it is a better oxidant of itself than it is a reductant")),
    ("IA-2.1.A", facts("cw-hydride-identify", "inorg.main-group", [
        ("A white solid hydride reacts with water to give H₂ and a strong base, and its melt conducts. Which class?", "Saline (e.g. NaH)", "Molecular", "Metallic", "Polymeric covalent"),
        ("A metal takes up hydrogen to a non-stoichiometric composition near MH₀.₆ and stays metallic. Which?", "Palladium (a metallic hydride)", "Sodium", "Boron", "Carbon"),
        ("A volatile, electron-deficient hydride with bridging H atoms. Which?", "B₂H₆ (diborane)", "CH₄", "CaH₂", "LiH"),
    ], "Electropositive metals make ionic H⁻ salts; p-block elements make molecules; many d-block metals dissolve H interstitially")),
    ("IA-2.1.B", Q("cw-heavy-atom-shift", "inorg.main-group", "¹²C¹⁶O absorbs at 2143 cm⁻¹. Where does {{iso}} absorb, in cm⁻¹? (masses: ¹²C 12.000, ¹³C 13.003, ¹⁶O 15.995, ¹⁸O 17.999)",
        cases=[{"iso": "¹³C¹⁶O", "ma": 13.003, "mb": 15.995}, {"iso": "¹²C¹⁸O", "ma": 12.000, "mb": 17.999}, {"iso": "¹³C¹⁸O", "ma": 13.003, "mb": 17.999}],
        value="2143*sqrt((12*15.995/(12 + 15.995))/(ma*mb/(ma + mb)))", tex="\\tilde\\nu",
        verify=f"Max(*solve(Eq((x/2143)**2*{n('ma')}*{n('mb')}/({n('ma')} + {n('mb')}), 12*Rational(15995, 1000)/(12 + Rational(15995, 1000))), x))",
        explain="ν ∝ √(k/μ) with the same force constant; heavy-atom shifts are far smaller than H→D")),
    ("IA-3.1.B", facts("cw-group2-thermal", "inorg.main-group", [
        ("Why does BaCO₃ decompose at a higher temperature than MgCO₃?", "Large Ba²⁺ polarises carbonate less and gains less lattice energy from forming the oxide", "Ba is less reactive", "MgCO₃ is a covalent network", "BaO is less stable than MgO"),
        ("Heating group 2 nitrates gives which products?", "The oxide, NO₂ and O₂", "The nitrite and O₂", "The metal and N₂", "No change"),
        ("Which group 2 hydroxide is most soluble in water?", "Ba(OH)₂", "Mg(OH)₂", "Be(OH)₂", "Ca(OH)₂"),
    ], "Down group 2, cations grow: anion polarisation falls, so oxyanion salts get more stable; hydroxides get more soluble")),
    ("IA-3.1.C", facts("cw-diagonal-cases", "inorg.main-group", [
        ("Like magnesium, lithium forms which?", "A nitride on burning in air, and a carbonate that decomposes on heating", "A superoxide", "A soluble fluoride and carbonate", "A stable hydrogencarbonate solid"),
        ("Like aluminium, beryllium has which property?", "An amphoteric hydroxide and a covalent, bridged chloride", "A basic oxide only", "An ionic chloride", "A superoxide"),
        ("Like silicon, boron forms which?", "An acidic oxide that makes glasses, and volatile hydrides", "A basic oxide", "Ionic halides", "A metallic lustre and conductivity"),
    ], "Charge/radius ratios match across the diagonal, so the chemistry does too")),
    ("IA-4.1.A", Q("cw-skeletal-pairs", "inorg.main-group", "How many skeletal electron pairs does {{sp}} have?",
        cases=[{"sp": "B₆H₆²⁻", "nB": 6, "nH": 6, "ch": -2}, {"sp": "B₅H₉", "nB": 5, "nH": 9, "ch": 0}, {"sp": "B₄H₁₀", "nB": 4, "nH": 10, "ch": 0},
               {"sp": "B₁₀H₁₄", "nB": 10, "nH": 14, "ch": 0}, {"sp": "B₁₂H₁₂²⁻", "nB": 12, "nH": 12, "ch": -2}, {"sp": "B₅H₁₁", "nB": 5, "nH": 11, "ch": 0}],
        value="(nB + nH - ch)/2", tex="", final=True, verify="cw_wade(nB, nH, ch) + nB + 1",
        explain="Each BH unit gives 2 skeletal electrons, each extra H 1, each negative charge 1: n + 1 pairs closo, n + 2 nido, n + 3 arachno")),
    ("IA-4.1.B", facts("cw-bx3-consequence", "inorg.main-group", [
        ("Which forms the most stable adduct with NH₃?", "BBr₃", "BF₃", "BCl₃", "They are equal"),
        ("Why is BF₃ the weakest Lewis acid of the boron trihalides?", "Strong F→B π donation fills boron's empty p orbital and is lost on pyramidalisation", "F is least electronegative", "BF₃ is a dimer", "BF₃ has no empty orbital"),
        ("Why does AlCl₃ dimerise while BCl₃ does not?", "Al is large enough to take four chlorides and gains less from π bonding", "BCl₃ has no lone pairs", "Al is more electronegative", "AlCl₃ is ionic"),
    ], "Lewis acidity of BX₃ runs opposite to electronegativity because π back-donation must be broken")),
    ("IA-5.1.B", Q("cw-odd-electron-bond-order", "inorg.main-group", "What is the bond order of {{sp}}?",
        cases=[{"sp": "NO", "bo": 2.5, "a": "N", "b": "O", "q": 0}, {"sp": "CN", "bo": 2.5, "a": "C", "b": "N", "q": 0}, {"sp": "O₂⁺", "bo": 2.5, "a": "O", "b": "O", "q": 1},
               {"sp": "N₂⁻", "bo": 2.5, "a": "N", "b": "N", "q": -1}, {"sp": "CO⁺", "bo": 2.5, "a": "C", "b": "O", "q": 1}, {"sp": "NO⁻", "bo": 2, "a": "N", "b": "O", "q": -1}],
        value="bo", tex="", verify="cw_bond_order(a, b, q)",
        explain="One electron more or fewer than the N₂ count (10 valence): an electron removed from a bonding orbital or added to an antibonding one costs ½")),
    ("IA-6.1.B", Q("cw-ph-bonds", "inorg.main-group", "How many P–H bonds does {{acid}} have?",
        cases=[{"acid": "phosphinic (hypophosphorous) acid, H₃PO₂", "Ht": 3, "bas": 1}, {"acid": "phosphonic (phosphorous) acid, H₃PO₃", "Ht": 3, "bas": 2},
               {"acid": "phosphoric acid, H₃PO₄", "Ht": 3, "bas": 3}, {"acid": "pyrophosphoric acid, H₄P₂O₇", "Ht": 4, "bas": 4}, {"acid": "diphosphonic acid, H₄P₂O₅", "Ht": 4, "bas": 2}],
        value="Ht - bas", tex="", final=True, verify="Ht - bas", explain="Only P–OH hydrogens ionise; the rest are on phosphorus, which is why H₃PO₂ and H₃PO₃ are good reductants")),
    ("IA-6.1.C", Q("cw-group15-lone-pairs", "inorg.main-group", "How many lone pairs are on the central atom of {{f}}?",
        cases=[{"f": "PCl₄⁺", "V": 5, "L": 4, "q": 1}, {"f": "PCl₆⁻", "V": 5, "L": 6, "q": -1}, {"f": "NF₃", "V": 5, "L": 3, "q": 0},
               {"f": "SbCl₅²⁻", "V": 5, "L": 5, "q": -2}, {"f": "PF₅", "V": 5, "L": 5, "q": 0}, {"f": "BiI₄⁻", "V": 5, "L": 4, "q": -1}],
        value="(V - q - L)/2", tex="", final=True, verify="Rational(V - q - L, 2)", explain="Lone pairs decide the shape: PCl₄⁺ tetrahedral, SbCl₅²⁻ square pyramidal, BiI₄⁻ seesaw")),
    ("IA-8.1.A", Q("cw-interhalogen-sn", "inorg.main-group", "What is the steric number (bonded atoms + lone pairs) of the central atom of {{f}}?",
        cases=[{"f": "ICl₄⁻", "V": 7, "L": 4, "q": -1}, {"f": "IF₅", "V": 7, "L": 5, "q": 0}, {"f": "ClF₃", "V": 7, "L": 3, "q": 0},
               {"f": "IF₇", "V": 7, "L": 7, "q": 0}, {"f": "BrF₂⁺", "V": 7, "L": 2, "q": 1}, {"f": "I₃⁻", "V": 7, "L": 2, "q": -1}],
        value="L + (V - q - L)/2", tex="", final=True, verify="L + Rational(V - q - L, 2)", explain="Steric number sets the electron geometry; lone pairs then sit where they cost least")),
    ("IA-10.1.D", facts("cw-lability-why", "inorg.transition", [
        ("Why is [Cr(H₂O)₆]³⁺ inert while [Cr(H₂O)₆]²⁺ is labile?", "d³ has a large CFSE loss on reaching the transition state; high-spin d⁴ has an e_g electron and Jahn–Teller distortion", "Cr²⁺ is smaller", "Cr³⁺ has no d electrons", "Water binds Cr²⁺ more strongly"),
        ("Which is inert: [Co(NH₃)₆]³⁺ or [Co(NH₃)₆]²⁺?", "[Co(NH₃)₆]³⁺ (low-spin d⁶)", "[Co(NH₃)₆]²⁺", "Both labile", "Both inert"),
        ("Water exchange on 4d and 5d ions compared with their 3d congeners is usually…", "Slower, because of larger Δ and stronger bonds", "Faster", "The same", "Impossible"),
    ], "Inert: d³, low-spin d⁶ (and d⁸ square planar); labile: anything with e_g electrons or no CFSE")),
    ("IA-11.1.B", Q("cw-oxo-d-count", "inorg.transition", "What is the d-electron count of the metal in {{sp}}?",
        cases=[{"sp": "MnO₄⁻", "dd": 0, "f": "MnO4", "q": -1, "M": "Mn", "Zm": 25}, {"sp": "MnO₄²⁻", "dd": 1, "f": "MnO4", "q": -2, "M": "Mn", "Zm": 25}, {"sp": "FeO₄²⁻", "dd": 2, "f": "FeO4", "q": -2, "M": "Fe", "Zm": 26},
               {"sp": "CrO₄²⁻", "dd": 0, "f": "CrO4", "q": -2, "M": "Cr", "Zm": 24}, {"sp": "VO²⁺", "dd": 1, "f": "VO", "q": 2, "M": "V", "Zm": 23}, {"sp": "MnO₂", "dd": 3, "f": "MnO2", "q": 0, "M": "Mn", "Zm": 25}],
        value="dd", tex="", final=True, verify="pt_group(Zm) - ox_state(f, q, M)",
        explain="d count = group − oxidation state: permanganate d⁰ is coloured by charge transfer, manganate d¹ green")),
    ("IA-11.2.A", which("cw-ti-identify", [
        ("Which metal's dioxide is the main white pigment and its tetrachloride a fuming liquid?", "Titanium", "Zirconium", "Vanadium", "Tin"),
        ("A violet aqueous ion with one d electron, used as a reductant. Which?", "Ti³⁺", "V³⁺", "Cr³⁺", "Mn³⁺"),
    ], "Titanium: TiO₂ pigment, TiCl₄ by chlorination, Ti(III) violet and reducing")),
    ("IA-11.2.B", which("cw-v-identify", [
        ("Which metal's ions run yellow (V), blue (IV), green (III) and violet (II) on reduction with zinc?", "Vanadium", "Chromium", "Manganese", "Titanium"),
        ("Which metal's pentoxide catalyses SO₂ → SO₃ in the contact process?", "Vanadium", "Platinum only", "Iron", "Chromium"),
    ], "Vanadium: V₂O₅ catalysis and the four-colour reduction series")),
    ("IA-11.2.C", which("cw-cr-identify", [
        ("An orange oxoanion turns yellow in base. Which metal?", "Chromium", "Manganese", "Vanadium", "Iron"),
        ("Which metal gives a quadruply bonded acetate dimer M₂(O₂CCH₃)₄ and a +3 ion that exchanges water very slowly?", "Chromium", "Iron", "Nickel", "Copper"),
    ], "Chromium: dichromate–chromate equilibrium, inert Cr(III), Cr(II) acetate")),
    ("IA-11.2.D", which("cw-mn-identify", [
        ("Which metal shows every oxidation state from +2 to +7, with a pale pink d⁵ aqua ion?", "Manganese", "Iron", "Chromium", "Cobalt"),
        ("Which metal's dioxide is the cathode material in alkaline batteries?", "Manganese", "Nickel", "Lead", "Zinc"),
    ], "Manganese: MnO₄⁻ to Mn²⁺, MnO₂ in batteries, and the oxygen-evolving centre in photosystem II")),
    ("IA-11.2.E", which("cw-fe-identify", [
        ("Which metal is reduced from its oxide by CO in a blast furnace?", "Iron", "Aluminium", "Titanium", "Magnesium"),
        ("Which metal ion gives a blood-red colour with thiocyanate?", "Fe³⁺", "Co²⁺", "Cu²⁺", "Ni²⁺"),
    ], "Iron: blast furnace, Fe(III) thiocyanate, haem and the iron–sulfur proteins")),
    ("IA-11.2.F", which("cw-co-identify", [
        ("Which metal sits at the centre of vitamin B₁₂?", "Cobalt", "Iron", "Nickel", "Manganese"),
        ("Pink hexaaqua ion, blue tetrachloro complex on adding HCl. Which metal?", "Cobalt", "Copper", "Nickel", "Iron"),
    ], "Cobalt: the pink/blue octahedral–tetrahedral switch, inert Co(III) ammines, cobalamin")),
    ("IA-11.2.G", which("cw-ni-identify", [
        ("Which metal is purified as a volatile tetracarbonyl (the Mond process)?", "Nickel", "Iron", "Cobalt", "Copper"),
        ("Which metal's dimethylglyoxime complex is a red precipitate used in gravimetry?", "Nickel", "Palladium only", "Cobalt", "Iron"),
    ], "Nickel: Ni(CO)₄, the red Ni(dmg)₂ test, square-planar d⁸")),
    ("IA-11.2.H", which("cw-cu-identify", [
        ("Which metal's +1 ion disproportionates in water but is stabilised in CuI and in cyanide complexes?", "Copper", "Silver", "Gold", "Mercury"),
        ("Which metal's +2 aqua ion shows a strong Jahn–Teller distortion?", "Copper", "Nickel", "Zinc", "Manganese"),
    ], "Copper: Cu(I)/Cu(II) balance, Jahn–Teller d⁹, blue copper proteins")),
    ("IA-11.2.I", Q("cw-high-valent-d", "inorg.transition", "What is the d-electron count of the metal in {{sp}}?",
        cases=[{"sp": "CrO₃", "f": "CrO3", "q": 0, "M": "Cr", "Zm": 24, "dd": 0}, {"sp": "Mn₂O₇", "f": "Mn2O7", "q": 0, "M": "Mn", "Zm": 25, "dd": 0},
               {"sp": "K₂FeO₄ (the ferrate ion)", "f": "FeO4", "q": -2, "M": "Fe", "Zm": 26, "dd": 2}, {"sp": "VF₅", "f": "VF5", "q": 0, "M": "V", "Zm": 23, "dd": 0},
               {"sp": "CoF₃", "f": "CoF3", "q": 0, "M": "Co", "Zm": 27, "dd": 6}, {"sp": "CrF₅", "f": "CrF5", "q": 0, "M": "Cr", "Zm": 24, "dd": 1}],
        value="dd", tex="", final=True, verify="pt_group(Zm) - ox_state(f, q, M)", explain="High oxidation states need O or F, which also stabilise them by π donation")),
    ("IA-12.1.A", Q("cw-mm-after-redox", "inorg.transition", "What is the metal–metal bond order in {{sp}}?",
        cases=[{"sp": "[Re₂Cl₈]³⁻ (d⁴ and d⁵)", "d1": 4, "d2": 5}, {"sp": "[Re₂Cl₈]⁴⁻ (two d⁵)", "d1": 5, "d2": 5}, {"sp": "Rh₂(O₂CCH₃)₄ (two Rh(II), d⁷)", "d1": 7, "d2": 7},
               {"sp": "[Tc₂Cl₈]³⁻ (d⁴ and d⁵)", "d1": 4, "d2": 5}, {"sp": "Ru₂(O₂CCH₃)₄⁺ (d⁵ and d⁶)", "d1": 5, "d2": 6}],
        value="(d1 + d2 == 9) ? 3.5 : ((d1 + d2 == 10) ? 3 : ((d1 + d2 == 11) ? 2.5 : 1))", tex="", verify="cw_mm_bond(d1, d2)",
        explain="Fill σ, π, π, δ, then δ*, π*, π*, σ*: each electron past eight lowers the order by ½")),
    ("IA-12.1.B", facts("cw-heavy-tm-why", "inorg.transition", [
        ("Why are nearly all 4d and 5d octahedral complexes low spin?", "Δ is larger and pairing energy smaller for the more diffuse 4d/5d orbitals", "They have fewer d electrons", "They are tetrahedral", "Their ligands are different"),
        ("Which ligand has the strongest trans effect?", "CN⁻ (or CO, C₂H₄)", "H₂O", "NH₃", "Cl⁻"),
        ("Using the trans effect, which route makes cisplatin?", "Add 2 NH₃ to [PtCl₄]²⁻", "Add 2 Cl⁻ to [Pt(NH₃)₄]²⁺", "Heat trans-Pt(NH₃)₂Cl₂", "Oxidise Pt metal in NH₃"),
    ], "Chloride directs trans more strongly than NH₃, so the second NH₃ goes cis to the first")),
    ("IA-12.2.A", which("cw-zrhf-identify", [
        ("Which pair is so alike in size that they were separated only with great difficulty?", "Zirconium and hafnium", "Niobium and molybdenum", "Iron and cobalt", "Silver and gold"),
        ("Which metal's alloys clad nuclear fuel because it absorbs few neutrons?", "Zirconium", "Hafnium", "Cadmium", "Boron"),
    ], "The lanthanide contraction makes Hf the size of Zr; Hf, unlike Zr, is a strong neutron absorber")),
    ("IA-12.2.B", which("cw-nbta-identify", [
        ("Which metal makes capacitors and surgical implants because its oxide film is tough and inert?", "Tantalum", "Niobium", "Titanium", "Zirconium"),
        ("Which metal is the base of superconducting magnet wire (with tin or titanium)?", "Niobium", "Tantalum", "Vanadium", "Hafnium"),
    ], "Niobium and tantalum: the lanthanide-contraction twins of group 5")),
    ("IA-12.2.C", which("cw-mow-identify", [
        ("Which metal has the highest melting point of all metals?", "Tungsten", "Molybdenum", "Rhenium", "Osmium"),
        ("Which metal sits in nitrogenase's FeMo cofactor?", "Molybdenum", "Tungsten", "Vanadium only", "Chromium"),
    ], "Mo and W: polyoxometalates, MoS₂, nitrogenase, tungsten filaments")),
    ("IA-12.2.D", which("cw-tcre-identify", [
        ("Which element has no stable isotope, yet one of its metastable isotopes is the most used medical imaging nuclide?", "Technetium", "Rhenium", "Promethium", "Ruthenium"),
        ("Which metal forms [M₂Cl₈]²⁻, the first known quadruple bond?", "Rhenium", "Technetium", "Tungsten", "Osmium"),
    ], "⁹⁹ᵐTc for imaging; Re in the quadruple bond and in ReO₄⁻")),
    ("IA-12.2.E", which("cw-ruos-identify", [
        ("Which metal's volatile tetroxide is used to stain tissue for electron microscopy?", "Osmium", "Ruthenium", "Rhenium", "Iridium"),
        ("Which metal is in Grubbs' olefin metathesis catalysts?", "Ruthenium", "Osmium", "Rhodium", "Molybdenum only"),
    ], "Os and Ru reach +8 as MO₄; Ru carbenes do metathesis")),
    ("IA-12.2.F", which("cw-rhir-identify", [
        ("Which metal is the catalyst in Wilkinson's hydrogenation catalyst?", "Rhodium", "Iridium", "Ruthenium", "Palladium"),
        ("Which metal is the densest-known and most corrosion-resistant, with Vaska's complex its classic oxidative-addition example?", "Iridium", "Rhodium", "Platinum", "Osmium"),
    ], "Rh(I) and Ir(I) square-planar d⁸ complexes add H₂ and alkyl halides")),
    ("IA-12.2.G", which("cw-pdpt-identify", [
        ("Which metal catalyses the Heck, Suzuki and Stille couplings?", "Palladium", "Platinum", "Nickel only", "Gold"),
        ("Which metal is in an anticancer drug that crosslinks DNA?", "Platinum", "Palladium", "Gold", "Ruthenium"),
    ], "Pd(0)/Pd(II) cycles for coupling; cisplatin binds guanine N7")),
    ("IA-12.2.H", which("cw-agau-identify", [
        ("Which metal dissolves in cyanide solution with air, the basis of its extraction?", "Gold (as [Au(CN)₂]⁻)", "Platinum", "Copper only", "Palladium"),
        ("Which metal's halides darken in light, the basis of film photography?", "Silver", "Gold", "Copper", "Mercury"),
    ], "Ag(I) halides are photosensitive; Au(I) forms linear dicyanides; relativistic effects make gold yellow")),
    ("IA-12.2.I", Q("cw-heavy-high-valent-d", "inorg.transition", "What is the d-electron count of the metal in {{sp}}?",
        cases=[{"sp": "OsO₄", "f": "OsO4", "q": 0, "M": "Os", "Zm": 76, "dd": 0}, {"sp": "ReO₄⁻", "f": "ReO4", "q": -1, "M": "Re", "Zm": 75, "dd": 0},
               {"sp": "PtF₆", "f": "PtF6", "q": 0, "M": "Pt", "Zm": 78, "dd": 4}, {"sp": "IrF₆", "f": "IrF6", "q": 0, "M": "Ir", "Zm": 77, "dd": 3},
               {"sp": "WF₆", "f": "WF6", "q": 0, "M": "W", "Zm": 74, "dd": 0}, {"sp": "AuF₅", "f": "AuF5", "q": 0, "M": "Au", "Zm": 79, "dd": 6}],
        value="dd", tex="", final=True, verify="pt_group(Zm) - ox_state(f, q, M)", explain="The heavy metals reach higher states than their 3d congeners: Os(VIII), Pt(VI), Au(V)")),
    ("IA-13.1.A", Q("cw-ox-from-f", "inorg.f-block", "An ion of {{el}} (Z = {{Z}}) has the configuration {{cfg}}ⁿ with n = {{nf}}. What is its charge?",
        cases=[{"el": "cerium", "Z": 58, "cfg": "[Xe]4f", "nf": 0, "core_n": 54}, {"el": "europium", "Z": 63, "cfg": "[Xe]4f", "nf": 7, "core_n": 54},
               {"el": "gadolinium", "Z": 64, "cfg": "[Xe]4f", "nf": 7, "core_n": 54}, {"el": "ytterbium", "Z": 70, "cfg": "[Xe]4f", "nf": 14, "core_n": 54},
               {"el": "uranium", "Z": 92, "cfg": "[Rn]5f", "nf": 2, "core_n": 86}, {"el": "plutonium", "Z": 94, "cfg": "[Rn]5f", "nf": 4, "core_n": 86}],
        value="Z - core_n - nf", tex="q", final=True, verify="solve(Eq(cw_f_count(Z, 0, 'Ln' if core_n == 54 else 'An') - x, nf), x)[0]",
        explain="Ions lose the s and d electrons first; what remains past the core is f")),
    ("IA-13.1.B", Q("cw-lande-g", "inorg.f-block", "The ground term of {{ion}} has S = {{Sv}}, L = {{L}}, J = {{J}}. What is its Landé g factor?",
        cases=[{"ion": "Ce³⁺ (²F₅/₂)", "Sv": 0.5, "L": 3, "J": 2.5, "nf": 1}, {"ion": "Gd³⁺ (⁸S₇/₂)", "Sv": 3.5, "L": 0, "J": 3.5, "nf": 7},
               {"ion": "Tb³⁺ (⁷F₆)", "Sv": 3, "L": 3, "J": 6, "nf": 8}, {"ion": "Dy³⁺ (⁶H₁₅/₂)", "Sv": 2.5, "L": 5, "J": 7.5, "nf": 9}, {"ion": "Er³⁺ (⁴I₁₅/₂)", "Sv": 1.5, "L": 6, "J": 7.5, "nf": 11}],
        value="1 + (J*(J + 1) + Sv*(Sv + 1) - L*(L + 1))/(2*J*(J + 1))", tex="g_J",
        verify=f"cw_ln_moment(nf)/sqrt({n('J')}*({n('J')} + 1))", explain="μ_eff = g_J√(J(J + 1)): spin–orbit coupling is strong and the crystal field weak in 4f ions")),
    ("IA-14.1.A", Q("cw-carbonyl-n", "inorg.organometallic", "Assuming the 18-electron rule, what is n in {{f}}?",
        cases=[{"f": "Cr(CO)ₙ", "Zm": 24, "mm": 0}, {"f": "Fe(CO)ₙ", "Zm": 26, "mm": 0}, {"f": "Ni(CO)ₙ", "Zm": 28, "mm": 0}, {"f": "W(CO)ₙ", "Zm": 74, "mm": 0},
               {"f": "Mn₂(CO)ₙ (with a Mn–Mn bond)", "Zm": 25, "mm": 1}, {"f": "Co₂(CO)ₙ (with a Co–Co bond, all terminal for counting)", "Zm": 27, "mm": 1}],
        value="(Zm == 24 or Zm == 74) ? 6 : (Zm == 26 ? 5 : (Zm == 28 ? 4 : (Zm == 25 ? 10 : 8)))", tex="n", final=True,
        verify="(18 - pt_group(Zm) - mm)/2*(1 + mm)", explain="Each CO gives 2 electrons; a metal–metal bond gives each metal 1. Group 7 and 9 metals must dimerise")),
]
