"""Second question types for AP Biology, units 1-5. Conceptual objectives get a scenario or prediction item (a second
angle on the same idea); quantitative ones a reverse or scaling item verified by sympy."""
from opl_dsl import Q

FILE, FRAMEWORK = "bi-second-types", "biology"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]


def facts(name, skill, rows, explain, prompt="{{q}}"):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


MOL, CELL, EN, SIG, HER = "bio.molecules", "bio.cells", "bio.energetics", "bio.signaling", "bio.heredity"

ADD = [
    # ── unit 1 chemistry of life ─────────────────────────────────────────
    ("BI-1.1.A", facts("bi-water-solutes", MOL, [
        ("Which dissolves readily in water?", "Glucose: its OH groups hydrogen-bond to water", "Hexane", "Cholesterol", "A triglyceride"),
        ("Why does table salt dissolve in water?", "Water's partial charges surround and separate Na⁺ and Cl⁻", "Water forms covalent bonds to the ions", "Salt is nonpolar", "Water is an ion itself"),
        ("Which part of a water molecule faces a Cl⁻ ion?", "The hydrogens (partial positive)", "The oxygen (partial negative)", "The lone pairs", "Neither: water does not orient"),
    ], "Polar and charged solutes are hydrated because water's δ+ hydrogens and δ− oxygen line up with their charges")),
    ("BI-1.1.B", facts("bi-water-scenario", MOL, [
        ("A lake's temperature changes little between day and night. Which property of water explains this?", "High specific heat", "Cohesion", "Low density of ice", "Adhesion"),
        ("Water rises up a thin glass tube against gravity. Which properties are at work?", "Adhesion to the glass and cohesion between water molecules", "High specific heat", "Ice floating", "Evaporative cooling only"),
        ("Fish survive under an ice-covered pond in winter. Why?", "Ice is less dense than liquid water, so it floats and insulates", "Water's high heat of fusion", "Cohesion", "Adhesion to the pond bed"),
        ("Sweating cools the body. Which property of water does this depend on?", "High heat of vaporisation", "Low density of ice", "Adhesion", "Being a good solvent"),
    ], "Each property traces back to hydrogen bonding among water molecules")),
    ("BI-1.2.A", facts("bi-element-source", MOL, [
        ("A plant lacking nitrogen will have trouble making which molecules?", "Proteins and nucleic acids", "Starch and cellulose", "Triglycerides", "Glucose"),
        ("Which element is found in nucleic acids and phospholipids but not in most proteins?", "Phosphorus", "Sulfur", "Nitrogen", "Carbon"),
        ("Which macromolecule class is built only from C, H and O?", "Carbohydrates", "Proteins", "Nucleic acids", "Phospholipids"),
    ], "C, H, O everywhere; N in proteins and nucleic acids; P in nucleic acids and phospholipids; S in some amino acids")),
    ("BI-1.2.B", facts("bi-label-experiment", MOL, [
        ("Hershey and Chase labelled phage protein coats. Which isotope did they use?", "³⁵S", "³²P", "¹⁵N", "¹⁴C"),
        ("Bacteria grown on ³²P will label which molecule most strongly?", "DNA", "Protein", "Starch", "Cholesterol"),
        ("Which label would mark both proteins and nucleic acids?", "¹⁵N", "³⁵S", "³²P", "¹⁸O in fats only"),
    ], "Pick the element that only one class contains: S for protein, P for DNA")),
    ("BI-1.3.A", facts("bi-reaction-direction", MOL, [
        ("Digestion of a protein in the stomach is an example of what?", "Hydrolysis", "Dehydration synthesis", "Phosphorylation", "Oxidation"),
        ("Joining two glucose molecules into maltose releases what?", "One water molecule", "Two water molecules", "Carbon dioxide", "ATP"),
        ("Which reaction adds water across a bond to break a polymer?", "Hydrolysis", "Condensation", "Dehydration", "Polymerisation"),
    ], "Building polymers removes water (dehydration); breaking them adds it back (hydrolysis)")),
    ("BI-1.3.B", Q("bi-polymer-mass", MOL, "{{n}} monomers, each of mass {{m}} g/mol, are joined into a linear polymer by dehydration. What is the polymer's mass, in g/mol? (water 18.015 g/mol)",
        given={"n": {"pick": [3, 10, 100]}, "m": {"pick": [110, 180.16, 330]}}, value="n*m - (n - 1)*18.015", tex="M",
        verify="n*nsimplify(m) - summation(Rational(18015, 1000), (Symbol('k'), 1, n - 1))", explain="n monomers form n − 1 bonds, each losing one water")),
    ("BI-1.4.A", facts("bi-bond-identify", MOL, [
        ("A bond links the carboxyl group of one monomer to the amino group of the next. What is it?", "Peptide bond", "Glycosidic linkage", "Phosphodiester bond", "Ester bond in a fat"),
        ("Which bond joins nucleotides into a strand?", "Phosphodiester bond", "Peptide bond", "Glycosidic linkage", "Hydrogen bond"),
        ("Which bond joins glycerol to fatty acids?", "Ester linkage", "Peptide bond", "Glycosidic linkage", "Phosphodiester bond"),
    ], "Each polymer class has its own linking bond, formed by dehydration")),
    ("BI-1.4.B", facts("bi-side-chain-placement", MOL, [
        ("In a soluble protein, where are leucine and valine side chains usually found?", "Buried in the hydrophobic core", "On the surface, facing water", "Bound to DNA", "Inside the active site only"),
        ("A transmembrane helix crosses the lipid bilayer. What side chains line its outer face?", "Nonpolar ones", "Charged ones", "Only glycine", "Polar ones"),
        ("Lysine and glutamate side chains on a protein's surface can pair. What interaction is that?", "Ionic bond (salt bridge)", "Disulfide bridge", "Peptide bond", "Hydrophobic interaction"),
    ], "Nonpolar side chains hide from water; charged and polar ones face it")),
    ("BI-1.4.C", facts("bi-lipid-scenario", MOL, [
        ("Which fat is most likely liquid at room temperature?", "One with several cis double bonds", "One with saturated chains", "A long-chain saturated fat", "A trans fat"),
        ("Which lipid has a hydrophilic head and two hydrophobic tails?", "Phospholipid", "Triglyceride", "Steroid", "Wax"),
        ("Testosterone and cholesterol share which structure?", "Four fused carbon rings (steroid)", "Glycerol backbone", "A phosphate head", "Three fatty acid chains"),
    ], "Kinks from cis double bonds stop chains packing; phospholipids are amphipathic; steroids are ring systems")),
    ("BI-1.4.D", facts("bi-polysaccharide-scenario", MOL, [
        ("Humans can digest starch but not cellulose. Why?", "Our enzymes break α-glycosidic links but not β", "Cellulose has no glucose", "Starch is a protein", "Cellulose is too small"),
        ("Which storage polysaccharide is the most highly branched?", "Glycogen", "Amylose", "Cellulose", "Chitin"),
        ("What makes cellulose fibres strong?", "Straight β-linked chains hydrogen-bonded side by side", "Branching every few units", "Ionic bonds between chains", "Peptide cross-links"),
    ], "Linkage geometry decides use: α links coil for storage, β links stay straight for structure")),
    ("BI-1.5.A", facts("bi-structure-level", MOL, [
        ("Urea disrupts hydrogen bonds between backbone groups. Which level is most directly lost?", "Secondary (α-helices and β-sheets)", "Primary", "Only quaternary", "None"),
        ("Hemoglobin has four polypeptide chains. Which level describes how they fit together?", "Quaternary", "Tertiary", "Secondary", "Primary"),
        ("A reducing agent breaks disulfide bridges. Which level is mainly affected?", "Tertiary (and quaternary if chains are linked)", "Primary", "Secondary only", "None"),
        ("Boiling an egg denatures its proteins. Which level survives?", "Primary", "Secondary", "Tertiary", "Quaternary"),
    ], "Primary is the covalent sequence; higher levels are held by weaker interactions that heat and chemicals break")),
    ("BI-1.5.B", facts("bi-substitution-predict", MOL, [
        ("A glutamate on a protein's surface is replaced by valine. What is the likeliest consequence?", "A hydrophobic patch that can make proteins stick together", "No change ever", "A stronger peptide bond", "Faster transcription"),
        ("A cysteine that forms a disulfide bridge is replaced by serine. What happens?", "The bridge is lost and the fold may weaken", "A stronger bridge forms", "The protein gets a new phosphate", "Nothing changes"),
        ("An adenine in a gene's promoter is replaced by guanine. Where would the effect show first?", "In how strongly the gene is transcribed", "In the protein's amino acid sequence", "In the lipid membrane", "In the cell wall"),
    ], "One substitution matters when it changes shape, charge or a binding site")),
    ("BI-1.5.C", facts("bi-direction-scenario", MOL, [
        ("A DNA strand reads 5′-ATGC-3′. Which end carries a free phosphate?", "The 5′ end", "The 3′ end", "Both ends", "Neither"),
        ("New nucleotides are always added to which end of a growing strand?", "The 3′ end", "The 5′ end", "Either end", "The middle"),
        ("A protein is made from which end to which?", "N-terminus to C-terminus", "C-terminus to N-terminus", "Both at once", "Middle outward"),
    ], "Polymerases add to the 3′-OH; ribosomes add each amino acid to the growing chain's C-terminus")),
    ("BI-1.6.A", facts("bi-nucleic-identify", MOL, [
        ("A nucleic acid contains uracil. What is it?", "RNA", "DNA", "Either", "A protein"),
        ("A sample has equal amounts of A and T, and of G and C. What is it likely to be?", "Double-stranded DNA", "Single-stranded RNA", "Single-stranded DNA", "Protein"),
        ("Which sugar has an OH on its 2′ carbon?", "Ribose", "Deoxyribose", "Glucose", "Both nucleic acid sugars"),
    ], "DNA: deoxyribose, thymine, usually double-stranded; RNA: ribose, uracil, usually single-stranded")),
    # ── unit 2 cells ─────────────────────────────────────────────────────
    ("BI-2.1.A", facts("bi-ribosome-scenario", CELL, [
        ("An antibiotic blocks bacterial ribosomes but not human ones. Why is it possible?", "Bacterial (70S) ribosomes differ in structure from human cytosolic (80S) ones", "Humans have no ribosomes", "Bacterial ribosomes make lipids", "It blocks DNA instead"),
        ("Why can such antibiotics still harm human mitochondria?", "Mitochondrial ribosomes resemble bacterial ones", "Mitochondria have no ribosomes", "They target the nucleus", "They block glycolysis"),
        ("Ribosomes in all cells are made of what?", "rRNA and protein", "DNA and protein", "Lipid only", "Carbohydrate"),
    ], "Shared but slightly different ribosomes are both a drug target and evidence of common ancestry")),
    ("BI-2.1.B", facts("bi-organelle-scenario", CELL, [
        ("Liver cells detoxify drugs. Which organelle is especially abundant there?", "Smooth ER", "Rough ER", "Chloroplast", "Central vacuole"),
        ("Pancreatic cells secrete digestive enzymes. Which organelle is especially abundant?", "Rough ER", "Smooth ER", "Lysosome", "Chloroplast"),
        ("Muscle cells use a lot of ATP. Which organelle is especially abundant?", "Mitochondria", "Golgi", "Lysosomes", "Peroxisomes"),
        ("White blood cells destroy engulfed bacteria. Which organelle do they rely on?", "Lysosomes", "Chloroplasts", "Smooth ER", "Central vacuole"),
    ], "A cell's job shows in which organelles it has most of")),
    ("BI-2.2.A", facts("bi-secretion-block", CELL, [
        ("A drug stops vesicles leaving the Golgi. Where does a secreted protein pile up?", "In the Golgi", "In the nucleus", "In the cytosol", "Outside the cell"),
        ("A protein lacking its ER signal sequence ends up where?", "In the cytosol", "Secreted", "In the plasma membrane", "In the lysosome"),
        ("What is the order for a secreted protein?", "Rough ER → Golgi → vesicle → plasma membrane", "Golgi → rough ER → nucleus", "Nucleus → Golgi → ER", "Smooth ER → lysosome → membrane"),
    ], "Blocking one step traps the protein in the compartment before it")),
    ("BI-2.2.B", facts("bi-structure-to-function", CELL, [
        ("Why does a nuclear envelope have pores?", "To let mRNA out and proteins in", "To let DNA leave", "To make ATP", "To store water"),
        ("Why is the inner mitochondrial membrane folded into cristae?", "More area for the electron transport chain and ATP synthase", "To store DNA", "To make ribosomes", "To hold starch"),
        ("Why do lysosomes keep an acidic interior?", "Their hydrolases work best at low pH", "To make ATP", "To store calcium", "To pump water"),
    ], "Form follows function: area for reactions, pores for traffic, a matched environment for enzymes")),
    ("BI-2.2.C", Q("bi-cristae-area-gain", CELL, "Folding raises a mitochondrion's inner membrane area {{f}}-fold. If ATP output scales with membrane area, how many times more ATP can it make than with an unfolded membrane?",
        given={"f": {"pick": [3, 5, 8]}}, value="f", tex="\\text{gain}", verify="(f*Symbol('A0')*Symbol('kk'))/(Symbol('A0')*Symbol('kk'))",
        explain="The ETC and ATP synthase sit in the membrane, so area sets the capacity")),
    ("BI-2.3.A", Q("bi-sav-scaling", CELL, "A cubic cell's edge grows by a factor of {{f}}. By what factor does its surface-to-volume ratio change?",
        given={"f": {"pick": [2, 3, 10]}}, value="1/f", tex="(SA/V)_2/(SA/V)_1",
        verify="(6*(f*Symbol('s'))**2/(f*Symbol('s'))**3)/(6*Symbol('s')**2/Symbol('s')**3)", explain="SA ∝ s² and V ∝ s³, so SA/V ∝ 1/s")),
    ("BI-2.3.B", facts("bi-sav-predict", CELL, [
        ("Which cell exchanges materials fastest per unit volume?", "The smallest one", "The largest one", "They are all equal", "The roundest large one"),
        ("Why do elephants have large ears full of blood vessels?", "To shed heat their low SA/V body cannot", "To hear better only", "To store water", "To make red cells"),
        ("A cell grows without dividing. What happens to its SA/V?", "It falls, so exchange can no longer keep up", "It rises", "It stays the same", "It doubles"),
    ], "Large bodies and cells lose surface relative to volume, which limits exchange and heat loss")),
    ("BI-2.3.C", Q("bi-microvilli-gain", CELL, "A flat cell surface carries {{n}} microvilli per μm², each a cylinder {{d}} μm across and {{h}} μm tall. By what factor do they raise the surface area (count each microvillus's side and top in place of its base)?",
        given={"n": {"pick": [10, 30]}, "d": {"pick": [0.08, 0.1]}, "h": {"pick": [1, 2]}}, value="1 + n*pi*d*h", tex="A/A_0",
        verify="(1 - n*pi*(nsimplify(d)/2)**2 + n*(pi*nsimplify(d)*nsimplify(h) + pi*(nsimplify(d)/2)**2))", explain="Each microvillus adds its side wall πdh; gut epithelium gains roughly twentyfold this way")),
    ("BI-2.4.A", facts("bi-bilayer-scenario", CELL, [
        ("Phospholipids are shaken in water. What do they form spontaneously?", "Bilayer vesicles with tails inside", "A monolayer with tails in water", "Separate dissolved molecules", "Crystals"),
        ("Where do integral membrane proteins have nonpolar side chains?", "In the part that crosses the bilayer core", "Only outside the cell", "Only in the cytosol", "Nowhere"),
        ("What drives bilayer formation?", "The hydrophobic effect: tails escape water", "Covalent bonds between lipids", "ATP hydrolysis", "Protein pumps"),
    ], "Amphipathic lipids hide their tails from water; proteins match that pattern")),
    ("BI-2.4.B", facts("bi-fluidity-predict", CELL, [
        ("Fish living in cold water have membranes rich in what?", "Unsaturated fatty acids", "Saturated fatty acids", "Cellulose", "Extra proteins only"),
        ("Cholesterol at low temperature does what to a membrane?", "Keeps it from becoming too rigid", "Makes it solid", "Dissolves it", "Has no effect"),
        ("Raising temperature does what to membrane fluidity?", "Increases it", "Decreases it", "No change", "Makes it permanent"),
    ], "Organisms tune fluidity with saturation and cholesterol to suit their temperature")),
    ("BI-2.5.A", facts("bi-crossing-rank", CELL, [
        ("Which crosses a bare bilayer fastest?", "O₂", "Glucose", "Na⁺", "A protein"),
        ("Which needs a protein to cross a membrane at a useful rate?", "K⁺", "CO₂", "Ethanol", "Steroid hormones"),
        ("Water crosses membranes faster than expected for a polar molecule. Why?", "Aquaporin channels", "It is nonpolar", "It is pumped by ATP", "It dissolves the bilayer"),
    ], "Small nonpolar molecules diffuse through; ions and large polar molecules need proteins")),
    ("BI-2.5.B", facts("bi-wall-scenario", CELL, [
        ("Penicillin blocks peptidoglycan synthesis. Why does that kill growing bacteria?", "Without a strong wall they burst osmotically", "They cannot make ATP", "Their DNA unwinds", "They lose their ribosomes"),
        ("A plant cell is placed in pure water. Why doesn't it burst?", "Its cellulose wall resists the turgor pressure", "Water cannot enter", "It pumps water out with ATP", "Its membrane is impermeable"),
        ("What are fungal cell walls made of?", "Chitin", "Cellulose", "Peptidoglycan", "Keratin"),
    ], "Walls bear the pressure that water uptake builds")),
    ("BI-2.6.A", facts("bi-transport-identify", CELL, [
        ("Glucose enters a red blood cell down its gradient through GLUT1. What kind of transport is this?", "Facilitated diffusion (passive)", "Active transport", "Endocytosis", "Simple diffusion"),
        ("A cell keeps K⁺ thirty times higher inside than outside. What must it use?", "Active transport", "Simple diffusion", "Osmosis", "Facilitated diffusion only"),
        ("A poison stops ATP production. Which transport stops first?", "Pumps like the Na⁺/K⁺-ATPase", "Diffusion of O₂", "Osmosis", "Channel flow down gradients"),
    ], "Down the gradient needs no energy; up the gradient needs ATP or another gradient")),
    ("BI-2.6.B", facts("bi-bulk-scenario", CELL, [
        ("A macrophage engulfs a whole bacterium. What process is that?", "Phagocytosis", "Pinocytosis", "Exocytosis", "Diffusion"),
        ("Cells take in LDL cholesterol particles bound to specific surface proteins. What process?", "Receptor-mediated endocytosis", "Phagocytosis", "Simple diffusion", "Exocytosis"),
        ("A nerve terminal releases neurotransmitter. What process?", "Exocytosis", "Endocytosis", "Pinocytosis", "Active transport through a pump"),
    ], "Bulk transport moves things too big for proteins by wrapping them in membrane")),
    ("BI-2.7.A", facts("bi-protein-transport", CELL, [
        ("Which transporter changes shape for each molecule it moves?", "A carrier protein", "An ion channel", "An aquaporin", "A pore in the bilayer"),
        ("Which moves ions fastest, millions per second?", "An open ion channel", "A carrier", "A pump", "Endocytosis"),
        ("A gated channel opens. Which way do ions flow?", "Down their electrochemical gradient", "Always inward", "Against the gradient", "Nowhere without ATP"),
    ], "Channels are open tunnels; carriers bind and flip, which is slower and saturable")),
    ("BI-2.7.B", Q("bi-carrier-saturation", CELL, "A carrier moves glucose with V_max = {{V}} μmol/min and K = {{K}} mM. What uptake rate, in μmol/min, does it give at {{c}} mM glucose?",
        given={"V": {"pick": [10, 50]}, "K": {"pick": [1, 5]}, "c": {"pick": [0.5, 5, 50]}}, value="V*c/(K + c)", tex="v",
        verify="nsimplify(V)*(1 - nsimplify(K)/(nsimplify(K) + nsimplify(c)))", explain="Carrier-mediated uptake saturates; simple diffusion would keep rising linearly")),
    ("BI-2.8.A", facts("bi-tonicity-scenario", CELL, [
        ("Red blood cells are put into distilled water. What happens?", "They swell and burst", "They shrink", "Nothing", "They divide"),
        ("A plant cell is put in concentrated salt solution. What happens?", "Plasmolysis: the membrane pulls away from the wall", "It bursts", "It becomes more turgid", "Nothing"),
        ("Why is IV saline 0.9% NaCl?", "It is isotonic with blood", "It kills bacteria", "It is hypertonic to cells", "It feeds cells"),
    ], "Water moves toward higher solute concentration (lower water potential)")),
    ("BI-2.8.B", Q("bi-concentration-from-psi", CELL, "What molar concentration of {{sol}} (i = {{i}}) gives a solute potential of {{ps}} MPa at {{T}} °C? (R = 0.00831 L·MPa/(mol·K))",
        cases=[{"sol": "sucrose", "i": 1}, {"sol": "NaCl", "i": 2}, {"sol": "CaCl₂", "i": 3}], given={"ps": {"pick": [-0.5, -1, -2]}, "T": {"pick": [20, 25]}},
        value="-ps/(i*0.00831*(T + 273))", tex="C", verify="solve(Eq(-i*x*Rational(831, 100000)*(T + 273), nsimplify(ps)), x)[0]",
        explain="ψs = −iCRT, solved for C; salts count each ion")),
    ("BI-2.8.C", facts("bi-osmoregulation-scenario", CELL, [
        ("A freshwater protist has a contractile vacuole. What does it pump out?", "Excess water that keeps entering", "Salt", "Glucose", "Proteins"),
        ("A saltwater fish drinks seawater. What must its gills do?", "Pump excess salt out", "Absorb more salt", "Release water", "Nothing"),
        ("Antidiuretic hormone (ADH) rises when you are dehydrated. What does it do?", "Makes kidneys reabsorb more water", "Makes urine more dilute", "Raises blood glucose", "Stops sweating"),
    ], "Organisms balance water against their surroundings with pumps, walls and kidneys")),
    ("BI-2.9.A", Q("bi-pump-charge", CELL, "The Na⁺/K⁺-ATPase runs {{n}} cycles. How many net positive charges does it move out of the cell?",
        given={"n": {"pick": [10, 100, 1000]}}, value="n", tex="q", final=True, verify="n*(3 - 2)",
        explain="Each cycle sends 3 Na⁺ out and brings 2 K⁺ in, using one ATP: a net charge of +1 out, which helps make the inside negative")),
    ("BI-2.9.B", facts("bi-cotransport-scenario", CELL, [
        ("The Na⁺/glucose symporter moves glucose into gut cells against its gradient. What powers it?", "The Na⁺ gradient made by the Na⁺/K⁺ pump", "Direct ATP hydrolysis by the symporter", "Glucose's own gradient", "Osmosis"),
        ("A drug stops the Na⁺/K⁺ pump. What happens to glucose uptake by the symporter?", "It slows as the Na⁺ gradient runs down", "It speeds up", "No change", "It reverses immediately"),
        ("In plants, sucrose is loaded into phloem by cotransport with which ion?", "H⁺", "Na⁺", "Cl⁻", "Ca²⁺"),
    ], "Cotransport spends one gradient to build another: indirect active transport")),
    ("BI-2.10.A", facts("bi-compartment-scenario", CELL, [
        ("Lysosomal enzymes leak into the cytosol (pH 7.2). What happens to their activity?", "It drops: they need the acid of the lysosome", "It rises", "Unchanged", "They make DNA"),
        ("Why are fatty acid synthesis and breakdown kept in different compartments?", "To stop the two pathways undoing each other", "Because one needs light", "To save space", "They are not"),
        ("Peroxisomes hold enzymes that make H₂O₂. Why is that useful?", "The toxic product is made and destroyed in one place", "It makes ATP", "It stores DNA", "It speeds diffusion"),
    ], "Compartments keep incompatible conditions and reactions apart")),
    ("BI-2.10.B", facts("bi-internal-membrane-area", CELL, [
        ("Which membrane in a plant cell carries the light reactions?", "Thylakoid", "Plasma membrane", "Outer chloroplast membrane", "Tonoplast"),
        ("Why does a liver cell have so much ER membrane?", "Membrane-bound enzymes need surface to work on", "To store glucose", "To make chlorophyll", "To divide faster"),
        ("Prokaryotes lack internal membranes. Where does their ETC sit?", "In the plasma membrane", "In mitochondria", "In the nucleus", "In the cell wall"),
    ], "Membrane-bound reactions scale with membrane area, which internal membranes multiply")),
    ("BI-2.11.A", facts("bi-cell-type-identify", CELL, [
        ("A cell has 70S ribosomes, a circular chromosome and no nucleus. What is it?", "A prokaryote", "A plant cell", "An animal cell", "A fungus"),
        ("A cell has a nucleus, a cell wall, chloroplasts and a large central vacuole. What is it?", "A plant cell", "A bacterium", "An animal cell", "An archaeon"),
        ("Which feature do prokaryotes and eukaryotes share?", "Ribosomes and a plasma membrane", "A nucleus", "Mitochondria", "Linear chromosomes"),
    ], "Nucleus and membrane-bound organelles mark eukaryotes; all cells have ribosomes and a membrane")),
    ("BI-2.11.B", facts("bi-endosymbiosis-evidence", CELL, [
        ("Which observation supports mitochondria descending from bacteria?", "They have their own circular DNA and 70S-like ribosomes", "They make glucose", "They lack membranes", "They are in all prokaryotes"),
        ("Chloroplasts have two membranes. How does endosymbiosis explain this?", "The inner from the bacterium, the outer from the engulfing cell", "Both from the nucleus", "Both from the ER", "It does not"),
        ("Mitochondria divide how?", "By binary fission, like bacteria", "By mitosis", "By meiosis", "They do not divide"),
    ], "Own DNA, own ribosomes, double membranes and fission all point to engulfed prokaryotes")),
    # ── unit 3 energetics ────────────────────────────────────────────────
    ("BI-3.1.A", facts("bi-specificity-scenario", EN, [
        ("A molecule shaped like the substrate binds the active site but does not react. What is it?", "A competitive inhibitor", "A cofactor", "A product", "An allosteric activator"),
        ("Why does sucrase act on sucrose but not lactose?", "The active site's shape and charge fit only sucrose", "Lactose is too large to exist", "Sucrase is a lipid", "Lactose has no bonds"),
        ("A mutation changes an active-site Asp to Asn. What is the likeliest effect?", "Loss of a charge the substrate needs, lowering activity", "Higher activity always", "No change", "The enzyme becomes DNA"),
    ], "Shape and chemistry of the active site decide which substrate binds")),
    ("BI-3.2.A", Q("bi-enzyme-speedup", EN, "An enzyme lowers a reaction's activation energy by {{dE}} kJ/mol at 37 °C. By roughly what factor does it speed the reaction? (R = 8.314 J/mol·K)",
        given={"dE": {"pick": [10, 20, 40]}}, value="exp(dE*1000/(8.314*310))", tex="k_{cat}/k_{uncat}",
        verify="exp(-Rational(8314, 1000)*0 - (-dE*1000)/(Rational(8314, 1000)*310))", explain="Rate depends exponentially on the barrier; ΔG of the reaction is unchanged")),
    ("BI-3.2.B", Q("bi-product-after-time", EN, "An enzyme reaction makes product at a steady initial rate of {{r}} μmol/min. How much product, in μmol, forms in the first {{t}} min (still in the linear range)?",
        given={"r": {"pick": [0.5, 2, 5]}, "t": {"pick": [2, 5, 10]}}, value="r*t", tex="P",
        verify="integrate(nsimplify(r), (Symbol('tt'), 0, t))", explain="The initial rate is the slope; the curve bends later as substrate runs down")),
    ("BI-3.3.A", Q("bi-q10-rate", EN, "An enzyme reaction has Q₁₀ = {{q}}. Below its optimum, by what factor does its rate change when the temperature rises by {{dT}} °C?",
        given={"q": {"pick": [2, 2.5, 3]}, "dT": {"pick": [5, 10, 20]}}, value="q^(dT/10)", tex="r_2/r_1",
        verify="exp(log(nsimplify(q))*dT/10)", explain="Rates roughly double per 10 °C until the enzyme starts to denature, then fall")),
    ("BI-3.3.B", facts("bi-inhibitor-predict", EN, [
        ("Adding a lot of substrate restores full activity. What kind of inhibitor was present?", "Competitive", "Noncompetitive", "Irreversible covalent", "None"),
        ("An inhibitor binds away from the active site and lowers V_max. What kind?", "Noncompetitive (allosteric)", "Competitive", "A substrate", "A coenzyme"),
        ("In feedback inhibition, the end product of a pathway usually binds where?", "An allosteric site on an early enzyme", "The last enzyme's active site", "DNA", "The membrane"),
    ], "Competitive inhibitors can be outcompeted; noncompetitive ones lower the maximum")),
    ("BI-3.3.C", Q("bi-rate-from-curve", EN, "An enzyme has V_max = {{V}} μmol/min and K_m = {{K}} mM. What substrate concentration, in mM, gives {{f}}% of V_max?",
        given={"V": {"pick": [10, 50]}, "K": {"pick": [0.5, 2, 5]}, "f": {"pick": [25, 50, 80]}}, value="f/(100 - f)*K", tex="[S]",
        verify="solve(Eq(V*x/(nsimplify(K) + x), V*Rational(f, 100)), x)[0]", explain="K_m is the concentration at half V_max")),
    ("BI-3.4.A", Q("bi-coupled-dg", EN, "A reaction with ΔG = +{{g}} kJ/mol is coupled to ATP hydrolysis (ΔG = −30.5 kJ/mol). What is ΔG of the coupled reaction, in kJ/mol?",
        given={"g": {"pick": [14, 20, 25]}}, value="g - 30.5", tex="\\Delta G", verify="nsimplify(g) + Rational(-305, 10)",
        explain="Free energies add: the pair runs if the sum is negative")),
    ("BI-3.4.B", facts("bi-energy-input-scenario", EN, [
        ("A mouse stops eating. Which energy store does it use first?", "Glycogen", "Muscle protein", "DNA", "Cell walls"),
        ("Why do cells die quickly without ATP production?", "Pumps fail, gradients collapse, and repair stops", "They overheat", "DNA melts", "Ribosomes become ATP"),
        ("Living things stay ordered despite the second law. How?", "They take in energy and release heat and disorder to the surroundings", "They break the second law", "They store entropy", "They need no energy"),
    ], "Order is maintained only by a continuous energy flow")),
    ("BI-3.5.A", Q("bi-photosynthesis-stoich", EN, "How many grams of glucose can be made from {{m}} g of CO₂ by photosynthesis? (CO₂ 44.01 g/mol, glucose 180.16 g/mol)",
        given={"m": {"pick": [44.01, 100, 264.06]}}, value="m/44.01/6*180.16", tex="m_{glucose}",
        verify="solve(Eq(6*x/Rational(18016, 100), nsimplify(m)/Rational(4401, 100)), x)[0]", explain="6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂: six carbons per glucose")),
    ("BI-3.5.B", facts("bi-light-reaction-predict", EN, [
        ("DCMU blocks electron flow out of PSII. What stops?", "O₂ release and NADPH production", "Only the Calvin cycle's CO₂ uptake", "Glycolysis", "Nothing"),
        ("Where does the O₂ released by plants come from?", "Split water", "CO₂", "Glucose", "Chlorophyll"),
        ("The thylakoid membrane is made leaky to H⁺. What fails?", "ATP synthesis", "Light absorption", "Water splitting", "CO₂ fixation directly"),
    ], "Electrons flow water → PSII → ETC → PSI → NADPH; the proton gradient drives ATP synthase")),
    ("BI-3.5.C", Q("bi-calvin-turns", EN, "How many ATP and NADPH together does the Calvin cycle spend to make {{n}} molecules of glucose?",
        given={"n": {"pick": [1, 2, 5]}}, value="n*(18 + 12)", tex="N", final=True, verify="6*n*(3 + 2)",
        explain="Each CO₂ fixed costs 3 ATP and 2 NADPH; a glucose needs six")),
    ("BI-3.5.D", Q("bi-rf-distance", EN, "A pigment has R_f = {{rf}} in a solvent whose front ran {{d}} cm. How far did the pigment move, in cm?",
        given={"rf": {"pick": [0.15, 0.4, 0.95]}, "d": {"pick": [8, 10, 12]}}, value="rf*d", tex="d_p",
        verify="solve(Eq(x/d, nsimplify(rf)), x)[0]", explain="R_f = pigment distance / solvent distance; carotenes run near the front, chlorophyll b lowest")),
    ("BI-3.6.A", Q("bi-atp-from-glucose", EN, "Using about 30 ATP per glucose in aerobic respiration and 2 in fermentation, how many glucose molecules must a fermenting cell use to match the ATP from {{n}} glucose respired aerobically?",
        given={"n": {"pick": [1, 2, 10]}}, value="15*n", tex="N", final=True, verify="solve(Eq(2*x, 30*n), x)[0]",
        explain="Fermentation yields about one fifteenth as much, which is why anaerobic tissues burn glucose so fast")),
    ("BI-3.6.B", facts("bi-chemiosmosis-predict", EN, [
        ("Where is the proton concentration highest in an active mitochondrion?", "The intermembrane space", "The matrix", "The cytosol", "Inside the cristae membrane"),
        ("What would happen to ATP synthesis without O₂?", "It stops as the ETC backs up", "It speeds up", "It moves to the nucleus", "No change"),
        ("Where does the O₂ we breathe end up?", "In water at the end of the ETC", "In CO₂", "In glucose", "In ATP"),
    ], "O₂ takes the electrons at the end of the chain; the H⁺ gradient powers ATP synthase")),
    ("BI-3.6.C", facts("bi-uncoupler-predict", EN, [
        ("An uncoupler lets H⁺ leak back across the inner membrane. What happens to O₂ use?", "It rises", "It stops", "No change", "It reverses"),
        ("With an uncoupler, where does the energy of electron transport go?", "Heat", "ATP", "Glucose", "Light"),
        ("Cyanide blocks complex IV. What happens to O₂ use and ATP?", "Both drop", "O₂ use rises, ATP drops", "Both rise", "No change"),
        ("Oligomycin blocks ATP synthase. What happens to O₂ use in coupled mitochondria?", "It falls as the gradient builds up", "It rises", "No change", "It doubles"),
    ], "Inhibitors stop flow; uncouplers let it run free, burning fuel as heat (brown fat does this on purpose)")),
    ("BI-3.6.D", facts("bi-fermentation-scenario", EN, [
        ("Why does fermentation make lactate or ethanol rather than stopping at pyruvate?", "To regenerate NAD⁺ for glycolysis", "To make more ATP", "To fix CO₂", "To make O₂"),
        ("Yeast in bread dough make which gas?", "CO₂", "O₂", "N₂", "H₂"),
        ("A sprinter's muscles produce lactate. What does that show?", "Glycolysis outran O₂ supply", "The muscles stopped glycolysis", "Muscles make O₂", "The Krebs cycle sped up"),
    ], "Fermentation is glycolysis plus a step to recycle NAD⁺")),
    ("BI-3.6.E", Q("bi-respirometer-moles", EN, "A respirometer shows {{v}} mL of O₂ taken up in {{t}} min by {{g}} g of seeds. What is the rate in μmol O₂ per gram per minute? (gas molar volume 24.5 L/mol)",
        given={"v": {"pick": [0.5, 1, 2]}, "t": {"pick": [10, 20]}, "g": {"pick": [5, 10]}}, value="v/1000/24.5*1e6/(g*t)", tex="r",
        verify="(nsimplify(v)/1000)/Rational(245, 10)*10**6/(nsimplify(g)*t)", explain="Convert volume to moles; KOH in the tube absorbs CO₂, so the change is O₂ alone")),
    ("BI-3.7.A", facts("bi-variant-environment", EN, [
        ("Why do some fish have antifreeze proteins?", "They bind ice crystals and stop them growing in cold water", "They make ATP", "They raise body temperature", "They store oxygen"),
        ("Why do deep-diving mammals have lots of myoglobin?", "To store O₂ in muscle for long dives", "To float", "To digest fish", "To see in the dark"),
        ("Fetal hemoglobin binds O₂ more tightly than adult hemoglobin. Why is that useful?", "It pulls O₂ from the mother's blood", "It releases more O₂", "It carries CO₂", "It is cheaper to make"),
    ], "Variant molecules suit organisms to their surroundings")),
    # ── unit 4 signalling and the cell cycle ─────────────────────────────
    ("BI-4.1.A", facts("bi-contact-scenario", SIG, [
        ("Two adjacent plant cells exchange molecules through channels in their walls. What are they?", "Plasmodesmata", "Gap junctions", "Desmosomes", "Hormones"),
        ("A T cell recognises an antigen displayed on another cell's MHC. What kind of signalling is this?", "Direct contact", "Endocrine", "Paracrine", "Synaptic"),
        ("Insulin travels in blood from the pancreas to muscle. What kind of signalling?", "Endocrine (secreted, long distance)", "Direct contact", "Gap junction", "Autocrine"),
    ], "Cells signal by touching (junctions, surface molecules) or by releasing chemicals")),
    ("BI-4.1.B", facts("bi-signal-range-scenario", SIG, [
        ("A cell releases a growth factor that binds its own receptors. What type?", "Autocrine", "Paracrine", "Endocrine", "Synaptic"),
        ("Bacteria switch on light production only when crowded. What is this?", "Quorum sensing", "Endocrine signalling", "Synaptic signalling", "Contact signalling"),
        ("Histamine from a mast cell acts on nearby blood vessels. What type?", "Paracrine", "Endocrine", "Autocrine", "Synaptic"),
    ], "Range sets the class: self, neighbours, synapse or bloodstream")),
    ("BI-4.2.A", facts("bi-stage-identify", SIG, [
        ("Epinephrine binds a receptor on a liver cell. Which stage?", "Reception", "Transduction", "Response", "Termination"),
        ("Protein kinases relay the signal inside the cell. Which stage?", "Transduction", "Reception", "Response", "Secretion"),
        ("Glycogen is broken down to glucose. Which stage?", "Response", "Reception", "Transduction", "Amplification only"),
    ], "Reception, transduction, response")),
    ("BI-4.2.B", facts("bi-receptor-location", SIG, [
        ("Steroid hormones bind receptors where?", "Inside the cell", "On the cell surface only", "In the cell wall", "In the blood"),
        ("Why can't insulin enter cells to act?", "It is a large polar protein, so it acts through a surface receptor", "It is a lipid", "Cells lack membranes", "It is broken down in blood"),
        ("A receptor phosphorylates itself after two copies pair up. What is it?", "Receptor tyrosine kinase", "GPCR", "Ion channel", "Intracellular receptor"),
    ], "Hydrophobic signals cross the membrane; hydrophilic ones need surface receptors")),
    ("BI-4.3.A", Q("bi-cascade-amplification", SIG, "In a cascade, one receptor activates {{a}} G proteins, each G protein's enzyme makes {{b}} cAMP, and each cAMP-activated kinase phosphorylates {{c}} targets. How many targets are phosphorylated per receptor?",
        given={"a": {"pick": [10, 100]}, "b": {"pick": [100, 1000]}, "c": {"pick": [10, 50]}}, value="a*b*c", tex="N", final=True,
        verify="exp(log(a) + log(b) + log(c))", explain="Each step multiplies: a few hormone molecules move millions of target molecules")),
    ("BI-4.3.B", facts("bi-response-kind", SIG, [
        ("A signal makes a cell switch on a gene. What kind of response?", "Change in gene expression", "Change in enzyme activity only", "Cell death", "No response"),
        ("A signal opens ion channels within milliseconds. What kind of response?", "A fast change in membrane potential", "Gene expression", "Cell division", "Secretion of DNA"),
        ("Growth factors lead to which response?", "Cell division", "Glycogen storage", "Apoptosis only", "Muscle contraction"),
    ], "The same pathway logic can end in enzyme changes, gene expression, division or death")),
    ("BI-4.4.A", facts("bi-pathway-defect", SIG, [
        ("Ras is stuck in its GTP-bound (on) state. What happens?", "Continuous growth signalling, as in many cancers", "No growth at all", "Normal regulation", "The cell dies"),
        ("A cell lacks phosphodiesterase, which breaks cAMP down. What happens?", "The response lasts longer", "No response", "Normal response", "Receptors disappear"),
        ("A drug blocks the receptor. Can adding more hormone restore the response?", "Only if the block is competitive", "Always", "Never", "Only for steroids"),
    ], "Predict effects by asking which step is stuck on or off")),
    ("BI-4.5.A", facts("bi-feedback-scenario", SIG, [
        ("Rising blood glucose triggers insulin, which lowers glucose. What kind of feedback?", "Negative", "Positive", "None", "Feedforward"),
        ("Oxytocin strengthens contractions, which release more oxytocin. What kind?", "Positive", "Negative", "None", "Neutral"),
        ("Ripening fruit releases ethylene, which ripens neighbouring fruit. What kind?", "Positive", "Negative", "None", "Inhibitory"),
    ], "Negative feedback opposes a change; positive feedback amplifies it")),
    ("BI-4.5.B", facts("bi-set-point", SIG, [
        ("Body temperature drops. Which response restores it?", "Shivering and constricting skin blood vessels", "Sweating", "Dilating skin vessels", "Panting"),
        ("Blood glucose falls. Which hormone rises?", "Glucagon", "Insulin", "ADH", "Oxytocin"),
        ("Blood CO₂ rises. What happens to breathing?", "It speeds up", "It slows", "It stops", "No change"),
    ], "Each deviation triggers the response that undoes it")),
    ("BI-4.5.C", facts("bi-positive-end", SIG, [
        ("What ends the positive feedback of childbirth?", "Delivery removes the stretch stimulus", "Insulin", "Falling temperature", "Nothing"),
        ("What ends the positive feedback of blood clotting?", "The wound is sealed and anticoagulants act", "More platelets", "Fever", "Nothing"),
        ("Why are positive feedback loops usually brief?", "They run to completion of an event, not to a set point", "They are slow", "They need DNA", "They are negative"),
    ], "Positive feedback drives an event to finish; something external stops it")),
    ("BI-4.6.A", Q("bi-dna-content-phase", SIG, "A diploid cell has {{c}} pg of DNA in G1. How much DNA, in pg, does it have in {{ph}}?",
        cases=[{"ph": "G2", "f": 2}, {"ph": "metaphase of mitosis", "f": 2}, {"ph": "each daughter cell after mitosis", "f": 1}, {"ph": "late S phase (complete)", "f": 2}],
        given={"c": {"pick": [3, 6, 7]}}, value="c*f", tex="DNA", verify="nsimplify(c)*f", explain="DNA doubles in S and halves when the cell divides")),
    ("BI-4.6.B", facts("bi-mitosis-scenario", SIG, [
        ("A drug stops spindle microtubules forming. Where do cells arrest?", "In metaphase (chromosomes cannot line up and separate)", "G1", "S", "Cytokinesis"),
        ("In which phase do sister chromatids separate?", "Anaphase", "Prophase", "Metaphase", "Telophase"),
        ("In which phase do nuclear envelopes re-form?", "Telophase", "Anaphase", "Metaphase", "Prophase"),
    ], "PMAT: condense, line up, separate, rebuild")),
    ("BI-4.6.C", Q("bi-cells-in-phase", SIG, "A cell cycle lasts {{T}} h and mitosis takes {{m}} h. In a field of {{N}} cells growing asynchronously, about how many are in mitosis?",
        given={"T": {"pick": [20, 24]}, "m": {"pick": [0.5, 1, 2]}, "N": {"pick": [200, 500]}}, value="N*m/T", tex="n",
        verify="solve(Eq(x/N, nsimplify(m)/T), x)[0]", explain="The fraction of cells in a phase equals the fraction of time spent there")),
    ("BI-4.7.A", facts("bi-checkpoint-scenario", SIG, [
        ("DNA is damaged in G1. What does p53 do?", "Halts the cycle for repair, or triggers apoptosis", "Speeds division", "Copies the DNA", "Nothing"),
        ("Cyclin levels rise and fall. What stays roughly constant?", "CDK levels", "Cyclin levels", "DNA levels", "Nothing"),
        ("At the metaphase checkpoint, what is checked?", "That every chromosome is attached to the spindle", "DNA replication", "Cell size", "Nutrients"),
    ], "Checkpoints check; cyclin–CDK complexes drive passage when the check passes")),
    ("BI-4.7.B", facts("bi-cancer-genes", SIG, [
        ("A gene that promotes division becomes overactive. What is it called?", "An oncogene", "A tumour suppressor", "A housekeeping gene", "A pseudogene"),
        ("Both copies of p53 are lost. What follows?", "Damaged cells keep dividing", "Cells stop dividing", "No effect", "Cells become plants"),
        ("Why does cancer usually need several mutations?", "Multiple brakes and accelerators must fail", "One is always enough", "Mutations cannot cause cancer", "Only viruses cause cancer"),
    ], "Cancer is division escaping control: accelerators stuck on, brakes removed")),
    # ── unit 5 heredity ──────────────────────────────────────────────────
    ("BI-5.1.A", Q("bi-meiosis-chromatids", HER, "A diploid cell has 2n = {{n2}}. How many chromatids are in each cell at {{st}}?",
        cases=[{"st": "metaphase I", "f": 2}, {"st": "metaphase II", "f": 1}, {"st": "the end of meiosis II (each gamete)", "f": 0.5}],
        given={"n2": {"pick": [8, 24, 46]}}, value="n2*f", tex="N", verify="n2*nsimplify(f)", explain="Replication doubles chromatids; meiosis I halves chromosomes, meiosis II separates sisters")),
    ("BI-5.1.B", facts("bi-mitosis-meiosis-scenario", HER, [
        ("Which process makes cells genetically identical to the parent?", "Mitosis", "Meiosis", "Both", "Neither"),
        ("In which division do homologous chromosomes pair?", "Meiosis I", "Mitosis", "Meiosis II", "Both mitosis and meiosis II"),
        ("How many cells does meiosis produce from one?", "Four haploid cells", "Two diploid cells", "Two haploid cells", "Four diploid cells"),
    ], "Mitosis copies; meiosis halves and shuffles")),
    ("BI-5.2.A", Q("bi-zygote-combinations", HER, "Ignoring crossing over, how many genetically different zygotes can two parents with n = {{n}} chromosome pairs produce?",
        given={"n": {"pick": [2, 3, 23]}}, value="(2^n)^2", tex="N", final=True, verify="Integer(4)**n", explain="2ⁿ kinds of gamete from each parent; for humans 2²³ × 2²³ ≈ 7 × 10¹³ before crossing over")),
    ("BI-5.3.A", facts("bi-conserved-scenario", HER, [
        ("Yeast cells can be rescued by a human cell-cycle gene. What does that suggest?", "The process is conserved from a common ancestor", "Yeast are human", "Genes never change", "Nothing"),
        ("Which process is shared by all eukaryotes?", "Meiosis in sexual reproduction", "Photosynthesis", "Flight", "Lactation"),
        ("Why does the genetic code being nearly universal matter?", "It points to one shared origin", "It proves nothing", "It shows convergence", "It changes every generation"),
    ], "Shared machinery across distant groups is inherited, not reinvented")),
    ("BI-5.3.B", Q("bi-testcross-fraction", HER, "A plant of unknown genotype (A_) is crossed with aa. Out of {{N}} offspring, how many show the recessive phenotype if the unknown parent is heterozygous?",
        given={"N": {"pick": [40, 100, 200]}}, value="N/2", tex="n", verify="N*Rational(1, 2)*1",
        explain="A testcross shows the hidden allele: Aa × aa gives 1:1, AA × aa gives no recessives")),
    ("BI-5.3.C", Q("bi-trihybrid-prob", HER, "In the cross AaBbCc × AaBbCc (independent genes), what is the probability of an aabbcc offspring?",
        given={"k": {"pick": [1]}}, value="1/64", tex="P", verify="Rational(1, 4)**3", explain="Multiply the single-gene probabilities: (1/4)³")),
    ("BI-5.3.E", Q("bi-expected-dihybrid", HER, "A dihybrid cross gives {{N}} offspring. How many are expected in the double-recessive class under 9:3:3:1?",
        given={"N": {"pick": [160, 320, 800]}}, value="N/16", tex="E", verify="N*Rational(1, 4)*Rational(1, 4)",
        explain="Expected counts come first; then χ² = Σ(O − E)²/E with df = classes − 1")),
    ("BI-5.4.A", facts("bi-blood-type-cross", HER, [
        ("A parent with type AB has a child with a parent of type O. Which blood types are possible?", "A or B", "AB or O", "O only", "AB only"),
        ("Red (RR) × white (WW) snapdragons give pink. What does pink × pink give?", "1 red : 2 pink : 1 white", "All pink", "3 red : 1 white", "All red"),
        ("Type A (I^A i) × type B (I^B i). What fraction of children are type O?", "1/4", "0", "1/2", "3/4"),
    ], "Codominance shows both; incomplete dominance blends; multiple alleles widen the choices")),
    ("BI-5.4.B", facts("bi-x-linked-scenario", HER, [
        ("A carrier mother and an unaffected father. What fraction of sons are colour-blind?", "1/2", "0", "1/4", "All"),
        ("An affected father and a non-carrier mother. What fraction of daughters are carriers?", "All", "1/2", "0", "1/4"),
        ("Why are X-linked recessive traits more common in males?", "Males have one X, so one allele shows", "Males have two X", "The Y carries the trait", "They are not"),
    ], "Sons get their X from their mother; daughters get their father's X")),
    ("BI-5.4.C", Q("bi-recombinants-expected", HER, "Two genes are {{d}} map units apart. In a testcross of {{N}} offspring, how many recombinants are expected?",
        given={"d": {"pick": [5, 12, 30]}, "N": {"pick": [200, 500, 1000]}}, value="N*d/100", tex="n", verify="solve(Eq(x/N*100, d), x)[0]",
        explain="1 map unit = 1% recombinant offspring; distances near 50 look unlinked")),
    ("BI-5.4.D", facts("bi-maternal-scenario", HER, [
        ("A mitochondrial disease appears in all children of an affected mother but none of an affected father. Why?", "Mitochondria come from the egg", "It is X-linked", "It is dominant", "It is polygenic"),
        ("Human height varies continuously. Why?", "Many genes plus environment add up", "One gene with two alleles", "Mitochondrial inheritance", "X-linkage"),
        ("Chloroplast traits in plants usually follow which parent?", "The maternal (seed) parent", "The pollen parent", "Both equally", "Neither"),
    ], "Organelle genes follow the egg; polygenic traits give bell curves")),
    ("BI-5.5.A", facts("bi-plasticity-scenario", HER, [
        ("Hydrangeas are blue in acid soil and pink in alkaline soil. What does this show?", "Environment changes phenotype for the same genotype", "A mutation", "Two species", "Codominance"),
        ("Himalayan rabbits have dark fur only on cold extremities. Why?", "A temperature-sensitive pigment enzyme", "Two genotypes in one rabbit", "Diet only", "Sunlight"),
        ("A person with PKU eats a low-phenylalanine diet. What does that show?", "Environment can change a genetic disease's outcome", "PKU is not genetic", "Diet changes the genotype", "Nothing"),
    ], "Phenotype is genotype acting in an environment")),
    ("BI-5.6.A", facts("bi-nondisjunction-count", HER, [
        ("Nondisjunction in meiosis I. What fraction of the four gametes are abnormal?", "All four", "Half", "None", "One"),
        ("Nondisjunction in meiosis II (one cell). What fraction are abnormal?", "Half", "All four", "None", "One quarter"),
        ("A gamete with an extra chromosome 21 fertilises a normal egg. What results?", "Trisomy 21 (Down syndrome)", "Monosomy 21", "Turner syndrome", "Klinefelter syndrome"),
    ], "Errors in meiosis I affect every gamete; in meiosis II only those from the affected cell")),
    ("BI-5.6.B", facts("bi-karyotype-read", HER, [
        ("A karyotype shows 45 chromosomes with a single X. What is it?", "Turner syndrome", "Klinefelter syndrome", "Down syndrome", "Normal male"),
        ("A karyotype shows 47, XXY. What is it?", "Klinefelter syndrome", "Turner syndrome", "Normal female", "Trisomy 18"),
        ("A karyotype shows 46, XY. What is it?", "Normal male", "Normal female", "Turner syndrome", "Klinefelter syndrome"),
    ], "Count the chromosomes, then read the sex chromosomes")),
]
