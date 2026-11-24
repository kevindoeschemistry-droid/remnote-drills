"""Second question types for the DAT objectives whose drill no other framework shares (organic chemistry reasoning,
reading comprehension, quantitative reasoning, a few biology items and lab safety). Objectives that share their drill with
an AP objective took that objective's second type directly in dat.yaml."""
from opl_dsl import Q

FILE, FRAMEWORK = "dat-second-types", "dat"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
R_ = "Rational(8314, 1000)"


def facts(name, skill, rows, explain, prompt="{{q}}"):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def passage(name, rows, explain):
    return Q(name, "dat.reading", "{{p}} — {{q}}", pace="quick", cases=[{"p": p, "q": q, "o1": a, "o2": b, "o3": c, "o4": d} for p, q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


P1 = ("Fluoride protects teeth mainly at the surface, not from inside. When fluoride is present in saliva during an acid attack, "
      "it is taken up as enamel re-forms, making fluorapatite, which resists acid better than the original hydroxyapatite. Early "
      "studies credited fluoride swallowed during tooth formation, but later work found the topical effect on erupted teeth far "
      "larger. This is why frequent low doses, as from toothpaste and community water, matter more than a single large dose.")
P2 = ("Composite resins shrink as they cure, by roughly 2 to 3 percent of their volume. Bonded to cavity walls, the shrinking "
      "material pulls on the bond, and the stress can open a gap at the margin where bacteria and fluids enter. Clinicians "
      "reduce this by placing the material in thin increments, each cured before the next, so that each layer can shrink "
      "toward a free surface. Newer bulk-fill composites claim lower shrinkage stress, allowing thicker layers, though "
      "long-term clinical data remain limited.")
P3 = ("The oral microbiome contains several hundred species, most of them harmless. Disease follows less from the arrival of "
      "a single pathogen than from a shift in the community: frequent sugar exposure lowers plaque pH, favouring acid-tolerant "
      "species such as Streptococcus mutans, which in turn produce more acid. Researchers therefore describe caries as an "
      "ecological disease, and some argue that prevention should aim to restore a healthy community rather than to eliminate "
      "particular bacteria.")

ADD = [
    # ── biology ──────────────────────────────────────────────────────────
    ("DAT-1.1.K", facts("dat-cytoskeleton-drugs", "bio.cells", [
        ("Colchicine and taxol both act on which cytoskeletal element?", "Microtubules", "Actin microfilaments", "Intermediate filaments", "Cell junctions"),
        ("Cytochalasin blocks actin polymerisation. Which process stops?", "Cytokinesis (the cleavage furrow) and amoeboid movement", "Chromosome separation", "Cilia beating", "DNA replication"),
        ("Which junction lets ions pass directly between two heart muscle cells?", "Gap junction", "Tight junction", "Desmosome", "Hemidesmosome"),
        ("Which junction stops fluid leaking between gut epithelial cells?", "Tight junction", "Gap junction", "Desmosome", "Plasmodesma"),
    ], "Microtubules: spindle and cilia; actin: contraction and cleavage; intermediate filaments: strength")),
    ("DAT-1.1.L", facts("dat-technique-result", "bio.cells", [
        ("After centrifugation, a band of mitochondria appears in a pellet. Which technique separated them?", "Differential centrifugation (cell fractionation)", "Gel electrophoresis", "PCR", "Western blot"),
        ("A Western blot shows a band only in the treated cells. What does it show?", "The treated cells contain that protein", "The gene was mutated", "The cells divided faster", "DNA was absent"),
        ("A fluorescently tagged protein recovers quickly after part of a membrane is bleached. What does that suggest?", "The protein diffuses freely in the membrane", "It is fixed to the cytoskeleton", "It was destroyed", "The membrane is solid"),
    ], "Pick the technique by the question asked: separate, detect, locate or measure movement")),
    ("DAT-1.2.E", facts("dat-protist-feature", "bio.diversity", [
        ("Which protists carry out photosynthesis with chlorophyll a and c and have silica shells?", "Diatoms", "Amoebas", "Ciliates", "Apicomplexans"),
        ("Which protist group moves with many short cilia and has two kinds of nucleus?", "Ciliates (e.g. Paramecium)", "Diatoms", "Euglenids", "Kinetoplastids"),
        ("Trypanosoma, which causes sleeping sickness, belongs to which group?", "Kinetoplastids (flagellated)", "Ciliates", "Apicomplexans", "Diatoms"),
    ], "Protists share only being eukaryotes that are not plants, animals or fungi, so the group is not a clade")),
    ("DAT-1.2.H", facts("dat-vertebrate-class", "bio.diversity", [
        ("Which vertebrate class first had the amniotic egg?", "Reptiles (amniotes)", "Amphibians", "Bony fish", "Cartilaginous fish"),
        ("Which class has a four-chambered heart, feathers and hollow bones?", "Birds", "Mammals", "Reptiles", "Amphibians"),
        ("Which class has a skeleton of cartilage and no swim bladder?", "Cartilaginous fish (sharks, rays)", "Bony fish", "Amphibians", "Jawless fish"),
    ], "Classes are split by innovations: jaws, bone, limbs, the amniotic egg, feathers, hair and milk")),
    # ── chemistry ────────────────────────────────────────────────────────
    ("DAT-2.13.C", facts("dat-lab-hazard", "gchem.measurement", [
        ("A chemical splashes in your eye. What first?", "Flush at the eyewash station for at least 15 minutes", "Rub the eye", "Neutralise with a base", "Wait and see if it hurts"),
        ("A small beaker of solvent catches fire on the bench. What first?", "Cover it to cut off oxygen (watch glass or lid)", "Pour water on it", "Carry it to the sink", "Blow it out"),
        ("Where should volatile, toxic reagents be handled?", "In a fume hood", "On the open bench", "Near an open window", "In a closed drawer"),
    ], "Act first to limit harm, then report")),
    ("DAT-3.1.C", facts("dat-resonance-charge", "orgo.reasoning", [
        ("In the acetate ion, where is the negative charge in the resonance hybrid?", "Shared equally over both oxygens", "Only on the C=O oxygen", "On the methyl carbon", "On the carbonyl carbon"),
        ("In the allyl cation, which carbons carry the positive charge?", "The two end carbons", "Only the middle carbon", "All three equally", "None"),
        ("Why is the phenoxide ion more stable than an alkoxide?", "Its charge spreads into the ring by resonance", "It is smaller", "It has more H atoms", "It is not more stable"),
    ], "Resonance spreads charge; the hybrid is the average of the contributors")),
    ("DAT-3.1.D", Q("dat-radical-product-percent", "orgo.reasoning", "{{alk}} is {{hal}}ed by light. With relative reactivities per H of {{rel}}, what percentage of the monohalogenated product is {{prod}}?",
        cases=[{"alk": "Propane", "hal": "chlorinat", "rel": "1° : 2° = 1 : 3.8", "prod": "2-chloropropane", "na": 2, "ra": 3.8, "nb": 6, "rb": 1},
               {"alk": "Propane", "hal": "brominat", "rel": "1° : 2° = 1 : 82", "prod": "2-bromopropane", "na": 2, "ra": 82, "nb": 6, "rb": 1},
               {"alk": "2-Methylpropane", "hal": "chlorinat", "rel": "1° : 3° = 1 : 5", "prod": "2-chloro-2-methylpropane", "na": 1, "ra": 5, "nb": 9, "rb": 1},
               {"alk": "2-Methylpropane", "hal": "brominat", "rel": "1° : 3° = 1 : 1600", "prod": "2-bromo-2-methylpropane", "na": 1, "ra": 1600, "nb": 9, "rb": 1}],
        value="100*na*ra/(na*ra + nb*rb)", tex="\\%", verify="100/(1 + Rational(nb, 1)*nsimplify(rb)/(na*nsimplify(ra)))",
        explain="Multiply the number of each kind of H by its reactivity: bromination is far more selective than chlorination")),
    ("DAT-3.1.F", Q("dat-rate-doubling", "orgo.reasoning", "A reaction proceeds by {{mech}}. By what factor does the rate change when the nucleophile (or base) concentration is doubled and the substrate concentration is {{f}}?",
        cases=[{"mech": "SN2", "o": 1, "fs": 1, "f": "unchanged"}, {"mech": "SN1", "o": 0, "fs": 1, "f": "unchanged"}, {"mech": "E2", "o": 1, "fs": 2, "f": "doubled too"},
               {"mech": "E1", "o": 0, "fs": 2, "f": "doubled too"}, {"mech": "SN2", "o": 1, "fs": 3, "f": "tripled"}],
        value="2^o*fs", tex="r_2/r_1", final=True, verify="Integer(2)**o*fs",
        explain="SN2 and E2 are bimolecular (rate = k[substrate][Nu]); SN1 and E1 depend only on the substrate")),
    ("DAT-3.2.D", facts("dat-epoxide-stereo", "orgo.reasoning", [
        ("Cyclohexene oxide is opened by aqueous acid. What is the relative stereochemistry of the diol?", "Trans (anti opening)", "Cis", "A mixture with no preference", "Meso cis only"),
        ("An unsymmetrical epoxide is opened by a strong nucleophile under basic conditions. Where does the nucleophile attack?", "The less substituted carbon (SN2)", "The more substituted carbon", "The oxygen", "Both equally"),
        ("Diethyl ether is cleaved by excess HI. What are the products?", "Two equivalents of ethyl iodide (and water)", "Ethanol only", "Ethene", "No reaction"),
    ], "Backside attack makes ring openings anti; acid shifts attack toward the carbon that best holds positive charge")),
    ("DAT-3.2.J", facts("dat-reagent-choice", "orgo.reasoning", [
        ("Which reagent reduces an ester to a primary alcohol?", "LiAlH₄", "NaBH₄", "H₂ with Lindlar catalyst", "PCC"),
        ("Which reagent oxidises a primary alcohol to an aldehyde without going on to the acid?", "PCC", "KMnO₄ (hot)", "Na₂Cr₂O₇ in aqueous acid", "NaBH₄"),
        ("To make a Grignard from a molecule that also has an alcohol, what must be done first?", "Protect the OH (e.g. as a silyl ether)", "Add more Mg", "Use water as solvent", "Nothing"),
    ], "Choose the reagent strong enough for the target group and gentle enough to spare the others")),
    ("DAT-3.3.A", Q("dat-acid-base-keq", "orgo.reasoning", "{{rx}} The reactant acid has pKa {{p1}} and the product acid has pKa {{p2}}. What is K_eq?",
        cases=[{"rx": "Acetic acid is mixed with hydroxide.", "p1": 4.8, "p2": 15.7}, {"rx": "Ethanol is mixed with amide ion.", "p1": 16, "p2": 38},
               {"rx": "Phenol is mixed with bicarbonate.", "p1": 10, "p2": 6.4}, {"rx": "A terminal alkyne is mixed with hydroxide.", "p1": 25, "p2": 15.7}],
        value="10^(p2 - p1)", tex="K_{eq}", verify="Integer(10)**(nsimplify(p2) - nsimplify(p1))",
        explain="Equilibrium favours the weaker acid (higher pKa): phenol does not react usefully with bicarbonate, which is why bicarbonate separates acids from phenols")),
    ("DAT-3.3.B", Q("dat-ka-ratio", "orgo.reasoning", "{{a}} has pKa {{pa}} and {{b}} has pKa {{pb}}. How many times stronger an acid is {{a}}?",
        cases=[{"a": "Trifluoroacetic acid", "pa": 0.23, "b": "acetic acid", "pb": 4.76}, {"a": "p-Nitrophenol", "pa": 7.15, "b": "phenol", "pb": 9.99},
               {"a": "Chloroacetic acid", "pa": 2.86, "b": "acetic acid", "pb": 4.76}, {"a": "Ethanethiol", "pa": 10.6, "b": "ethanol", "pb": 16}],
        value="10^(pb - pa)", tex="K_a/K_a'", verify="Integer(10)**(nsimplify(pb))/Integer(10)**(nsimplify(pa))",
        explain="Each pKa unit is a factor of ten in Ka: induction, resonance and atom size each shift it")),
    ("DAT-3.3.D", Q("dat-amine-protonated", "orgo.reasoning", "An amine's conjugate acid has pKa {{pk}}. What percentage of the amine is protonated at pH {{pH}}?",
        given={"pk": {"pick": [4.6, 9.25, 10.6]}, "pH": {"pick": [2, 7.4, 12]}}, value="100/(1 + 10^(pH - pk))", tex="\\%",
        verify="100*Integer(10)**(nsimplify(pk))/(Integer(10)**(nsimplify(pk)) + Integer(10)**(nsimplify(pH)))", explain="Below the pKaH an amine is mostly protonated; aniline (4.6) is mostly neutral at body pH, alkylamines (~10.6) mostly charged")),
    ("DAT-3.4.A", facts("dat-property-rank", "orgo.reasoning", [
        ("Rank by boiling point, highest first: pentane, 1-butanol, diethyl ether.", "1-Butanol > diethyl ether > pentane", "Pentane > diethyl ether > 1-butanol", "Diethyl ether > 1-butanol > pentane", "All about equal"),
        ("Which isomer of C₅H₁₂ boils lowest?", "2,2-Dimethylpropane (most branched)", "Pentane", "2-Methylbutane", "They are equal"),
        ("Which is most soluble in water?", "Ethanol", "1-Hexanol", "Hexane", "Benzene"),
    ], "Hydrogen bonding raises boiling point most; branching lowers it; a long carbon chain lowers water solubility")),
    ("DAT-3.4.B", facts("dat-extraction-layer", "orgo.reasoning", [
        ("An ether solution of benzoic acid and naphthalene is shaken with aqueous NaOH. Where does benzoic acid go?", "Into the aqueous layer as benzoate", "It stays in the ether", "It precipitates at once", "It evaporates"),
        ("An ether solution containing an amine is washed with dilute HCl. Where does the amine go?", "Into the aqueous layer as the ammonium salt", "It stays in the ether", "It decomposes", "Into the vapour"),
        ("On a silica TLC plate, which runs farthest with a nonpolar eluent?", "The least polar compound", "The most polar compound", "The largest compound", "They all run together"),
    ], "Charged forms go to water; neutral organics stay in the organic layer; polar compounds stick to silica")),
    ("DAT-3.4.C", facts("dat-ir-where", "orgo.spectroscopy", [
        ("Where does a ketone's C=O stretch appear?", "About 1715 cm⁻¹", "About 3300 cm⁻¹", "About 2250 cm⁻¹", "About 1000 cm⁻¹"),
        ("Where does a nitrile's C≡N stretch appear?", "About 2250 cm⁻¹", "About 1715 cm⁻¹", "About 3400 cm⁻¹", "About 1600 cm⁻¹"),
        ("A carboxylic acid shows which O–H band?", "Very broad, about 2500–3300 cm⁻¹", "Sharp at 3600 cm⁻¹", "None", "At 1050 cm⁻¹"),
    ], "Carbonyls near 1700, triple bonds near 2200, O–H and N–H above 3000")),
    ("DAT-3.4.E", facts("dat-c13-shift", "orgo.spectroscopy", [
        ("In ¹³C NMR, where does a ketone carbonyl carbon appear?", "About 200 ppm", "About 20 ppm", "About 130 ppm", "About 70 ppm"),
        ("Where do aromatic carbons appear?", "About 110–160 ppm", "About 0–40 ppm", "About 200 ppm", "About 60–80 ppm"),
        ("Where does a carbon bonded to an alcohol oxygen appear?", "About 50–80 ppm", "About 200 ppm", "About 10 ppm", "About 140 ppm"),
    ], "Electronegative neighbours and sp² carbons move signals downfield")),
    ("DAT-3.5.A", Q("dat-carbons-from-name", "orgo.structure", "How many carbon atoms does {{name}} contain?",
        cases=[{"name": "3-ethyl-2-methylhexane", "parent": 6, "subs": 3}, {"name": "2,2,4-trimethylpentane", "parent": 5, "subs": 3},
               {"name": "4-isopropylheptane", "parent": 7, "subs": 3}, {"name": "cyclohexylmethanol", "parent": 1, "subs": 6}, {"name": "3-methylbutan-2-one", "parent": 4, "subs": 1}],
        value="parent + subs", tex="N_C", final=True, verify="parent + subs", explain="Parent chain plus every substituent's carbons: read names back into structures")),
    ("DAT-3.5.E", Q("dat-axial-equatorial", "orgo.structure", "A substituent with A-value {{A}} kcal/mol sits on cyclohexane. At 25 °C, what is the ratio of equatorial to axial conformers? (R = 1.987 cal/mol·K)",
        cases=[{"sub": "CH₃", "A": 1.7}, {"sub": "OH", "A": 0.9}, {"sub": "t-butyl", "A": 4.9}, {"sub": "Cl", "A": 0.5}],
        value="exp(A*1000/(1.987*298.15))", tex="K", verify="exp(nsimplify(A)*1000/(Rational(1987, 1000)*Rational(29815, 100)))",
        explain="A methyl group is about 95% equatorial; a tert-butyl essentially locks the ring")),
    ("DAT-3.5.F", Q("dat-pi-electron-count", "orgo.structure", "How many π electrons does the ring of {{mol}} hold, counting lone pairs that are part of the π system?",
        cases=[{"mol": "pyrrole", "db": 2, "lp": 1}, {"mol": "pyridine", "db": 3, "lp": 0}, {"mol": "furan", "db": 2, "lp": 1}, {"mol": "the cyclopentadienyl anion", "db": 2, "lp": 1},
               {"mol": "the tropylium cation", "db": 3, "lp": 0}, {"mol": "cyclooctatetraene", "db": 4, "lp": 0}],
        value="2*db + 2*lp", tex="N_\\pi", final=True, verify="2*(db + lp)",
        explain="Aromatic needs 4n + 2 (2, 6, 10…) in a flat, cyclic, conjugated ring; pyridine's lone pair lies in the plane and does not count")),
    ("DAT-3.5.G", Q("dat-bond-angle", "orgo.structure", "What is the ideal bond angle at {{q}}, in degrees?",
        cases=[{"q": "the carbon of a methyl group", "sn": 4}, {"q": "a carbonyl carbon", "sn": 3}, {"q": "the central carbon of an allene", "sn": 2},
               {"q": "a carbon of a benzene ring", "sn": 3}, {"q": "a nitrile carbon", "sn": 2}],
        value="sn == 4 ? 109.5 : (sn == 3 ? 120 : 180)", tex="\\theta", verify="Rational(1095, 10) if sn == 4 else (120 if sn == 3 else 180)",
        explain="sp³ 109.5°, sp² 120°, sp 180°: count the groups around the atom")),
    ("DAT-3.5.H", facts("dat-alkene-stability", "orgo.structure", [
        ("Which alkene is most stable?", "2,3-Dimethylbut-2-ene (tetrasubstituted)", "But-1-ene", "cis-But-2-ene", "Ethene"),
        ("Which is more stable, cis- or trans-but-2-ene, and why?", "Trans: less steric strain between the methyls", "Cis: closer methyls attract", "Equal", "Neither exists"),
        ("Which radical is most stable?", "The allyl or benzyl radical (resonance)", "A methyl radical", "A primary radical", "A vinyl radical"),
    ], "More substitution and resonance stabilise alkenes, radicals and carbocations")),
    # ── reading comprehension ────────────────────────────────────────────
    ("DAT-5.1.A", passage("dat-rc-detail-2", [
        (P1, "According to the passage, why does fluorapatite help?", "It resists acid better than hydroxyapatite", "It is swallowed during tooth formation", "It kills bacteria in saliva", "It makes enamel thicker"),
        (P2, "By how much do composites shrink as they cure?", "Roughly 2 to 3 percent of their volume", "About 10 percent", "They do not shrink", "Only in thick layers"),
    ], "Answer from the sentence that states it, not from general knowledge")),
    ("DAT-5.1.B", passage("dat-rc-main-idea-2", [
        (P3, "What is the main idea?", "Caries arises from a shift in the oral microbial community", "S. mutans is the only cause of caries", "The mouth holds several hundred species", "Sugar has little effect on plaque"),
        (P1, "What is the main idea?", "Fluoride works mainly at the tooth surface, so frequent low doses matter most", "Fluoride must be swallowed to work", "Hydroxyapatite is the hardest mineral", "Early studies were correct"),
    ], "The main idea covers the whole passage; details support it")),
    ("DAT-5.1.C", passage("dat-rc-vocab-2", [
        (P2, "As used in the passage, 'increments' most nearly means…", "Small separate portions added in turn", "Price increases", "Cracks", "Temperature steps"),
        (P3, "As used in the passage, 'ecological' most nearly means…", "Concerning relationships within a community of organisms", "Environmentally friendly", "Inexpensive", "Chemical"),
    ], "Read the word's sentence and pick the meaning that fits it there")),
    ("DAT-5.1.D", passage("dat-rc-supported-2", [
        (P2, "Is this statement supported, contradicted or not addressed: bulk-fill composites are proven to last longer?", "Contradicted: long-term data remain limited", "Supported", "Not addressed", "Both supported and contradicted"),
        (P3, "Is this statement supported, contradicted or not addressed: fluoride varnish prevents caries?", "Not addressed", "Supported", "Contradicted", "Supported indirectly by the sugar claim"),
    ], "Separate what the passage says, what it denies, and what it never mentions")),
    ("DAT-5.2.A", passage("dat-rc-inference-2", [
        (P3, "Which can be inferred?", "Cutting sugar frequency could help restore a healthier community", "S. mutans cannot live at neutral pH", "Most oral bacteria cause disease", "Antibiotics cure caries"),
        (P1, "Which can be inferred?", "An adult with fully erupted teeth still benefits from fluoride toothpaste", "Fluoride only helps children", "One large dose is best", "Fluorapatite dissolves easily"),
    ], "An inference must follow from what is stated, not just be plausible")),
    ("DAT-5.2.B", passage("dat-rc-tone-2", [
        (P2, "What is the author's attitude toward bulk-fill composites?", "Cautious: promising but not yet proven long-term", "Enthusiastic without reservation", "Dismissive", "Hostile"),
        (P3, "The author's purpose is mainly to…", "Explain a view of caries as an ecological disease", "Advertise a toothpaste", "Argue against all antibiotics", "Describe the history of dentistry"),
    ], "Hedges like 'claim' and 'remain limited' signal caution")),
    ("DAT-5.2.C", passage("dat-rc-sequence-2", [
        (P3, "In the passage's sequence, what follows frequent sugar exposure?", "Plaque pH falls, favouring acid-tolerant species that make more acid", "Bacteria die off", "Saliva neutralises it at once", "Fluoride is released"),
        (P2, "In the passage, what does curing shrinkage lead to?", "Stress on the bond that can open a marginal gap", "A stronger bond", "Faster curing", "Less bacteria"),
    ], "Trace each step to the next as the passage orders them")),
    # ── quantitative reasoning ───────────────────────────────────────────
    ("DAT-6.1.D", Q("dat-abs-interval", "dat.qr-reasoning", "How many integers x satisfy |x − {{a}}| ≤ {{b}}?",
        given={"a": {"int": [-5, 10]}, "b": {"int": [1, 8]}}, value="2*b + 1", tex="N", final=True,
        verify="(a + b) - (a - b) + 1", explain="|x − a| ≤ b is the interval a − b ≤ x ≤ a + b, which holds 2b + 1 integers")),
    ("DAT-6.2.B", facts("dat-sufficiency-more", "dat.qr-reasoning", [
        ("Is n even? (1) n² is even. (2) n + 3 is odd.", "Each statement alone is sufficient", "Statement (1) alone", "Statement (2) alone", "Neither, even together"),
        ("What is the area of a rectangle? (1) Its perimeter is 20. (2) Its diagonal is √52.", "Both together, but neither alone", "Statement (1) alone", "Statement (2) alone", "Neither, even together"),
        ("What is x + y? (1) 2x + 2y = 14. (2) x − y = 1.", "Statement (1) alone", "Statement (2) alone", "Both together, but neither alone", "Neither, even together"),
    ], "Ask whether each statement pins down a single value; test them alone, then together")),
    ("DAT-6.3.A", Q("dat-quant-compare-2", "dat.qr-reasoning", "Compare quantity A, {{A}}, with quantity B, {{B}}.",
        cases=[{"A": "$2^{10}$", "B": "$10^3$", "va": "2**10", "vb": "10**3", "ans": 0}, {"A": "$\\sqrt{50}$", "B": "$7$", "va": "sqrt(50)", "vb": "7", "ans": 0},
               {"A": "$\\frac{7}{9}$", "B": "$\\frac{8}{11}$", "va": "Rational(7, 9)", "vb": "Rational(8, 11)", "ans": 0}, {"A": "$15\\%$ of 80", "B": "$80\\%$ of 15", "va": "Rational(15, 100)*80", "vb": "Rational(80, 100)*15", "ans": 2},
               {"A": "$0.3^2$", "B": "$0.3$", "va": "Rational(3, 10)**2", "vb": "Rational(3, 10)", "ans": 1}],
        choice=["A is greater", "B is greater", "They are equal", "Cannot be determined"], correct="ans",
        verify="0 if sympify(va) > sympify(vb) else (1 if sympify(va) < sympify(vb) else 2)",
        explain="Estimate first: x% of y always equals y% of x; squaring a number between 0 and 1 shrinks it")),
    ("DAT-6.4.D", Q("dat-weighted-reverse", "dat.qr-reasoning", "A class of {{n1}} students averages {{m1}}. When a second group joins, the combined average of all {{nt}} students is {{mt}}. What is the second group's average?",
        given={"n1": {"pick": [10, 20]}, "m1": {"pick": [70, 80]}, "nt": {"pick": [30, 40]}, "mt": {"pick": [75, 78]}}, value="(nt*mt - n1*m1)/(nt - n1)", tex="\\bar x_2",
        verify="solve(Eq(n1*m1 + (nt - n1)*x, nt*mt), x)[0]", explain="Totals add: total of all = total of group 1 + total of group 2")),
    ("DAT-6.5.C", Q("dat-mixture-final", "dat.qr-reasoning", "{{v1}} L of a {{c1}}% solution is mixed with {{v2}} L of a {{c2}}% solution. What is the concentration of the mixture, in %?",
        given={"v1": {"pick": [2, 3, 5]}, "c1": {"pick": [10, 20]}, "v2": {"pick": [1, 3, 5]}, "c2": {"pick": [40, 50, 70]}}, value="(v1*c1 + v2*c2)/(v1 + v2)", tex="c",
        verify="solve(Eq((v1 + v2)*x, v1*c1 + v2*c2), x)[0]", explain="Solute amounts add; the mixture lies between the two, nearer the larger volume")),
]
