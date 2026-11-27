"""Microbiology (MI, Nov 2026): the one-semester general microbiology course. Structure in UNITS (written by
scripts/fw_setup.py), two question types per objective.

Basis: the ASM Curriculum Guidelines for Undergraduate Microbiology (2024 revision), read through an extraction of the
JMBE paper that listed its six concept areas, 29 fundamental statements and eight skills; items are the concept areas
and the skills block, titled in our words, so read: part. General course level only: how microbes are built, grow,
exchange genes, live together and are counted and controlled. Nothing here is specific to making, enhancing or
handling a dangerous organism, and the Biosecurity framework's rule applies to this file too."""
from opl_dsl import Q

FILE, FRAMEWORK, PRACTICE = "mi-microbiology", "microbiology", "P1"
M = "Symbol('m')"
FW = dict(id="microbiology", title="Microbiology", code="MI", domain="micro", track="science", requires=["biology", "chemistry"], level=4,
          primary="asm-micro-2024", also=[], subject="Human Biology",
          note="Anchored on the ASM Curriculum Guidelines for Undergraduate Microbiology (2024), read through an extraction of its concept areas, fundamental statements and skills. A general course: structure, growth, genetics, ecology, control and laboratory counting. Organism-by-organism medical microbiology is not built; host defence is in Anatomy and Physiology unit 9.",
          header=["General microbiology at the level of the one-semester course health programmes require: what a bacterial",
                  "cell and a virus are made of, how populations grow and are counted, how genes move, how microbes live",
                  "with each other and with us, and how growth is controlled. Policy and defence are in Biosecurity."],
          source=dict(id="asm-micro-outline", title="General microbiology by ASM concept area (course outline)", short="Micro outline", field="biology",
                      note=["The ASM curriculum guideline concept areas written as a source so the micro.* skills have a home.", "NOT a book: only the guideline's statements were read. Chapter numbers are ours."]))
STDS = [{"id": "asm-micro-2024", "name": "ASM Curriculum Guidelines for Undergraduate Microbiology (2024 revision)", "publisher": "American Society for Microbiology", "kind": "standard", "read": "part",
         "url": "https://escholarship.org/uc/item/9bk8b81b",
         "note": "Read Nov 2026 through an extraction of the Journal of Microbiology and Biology Education paper presenting the revision: six concept areas holding 29 fundamental statements, and eight scientific thinking and laboratory skills. The statements were not checked word for word against the PDF, so read: part. Items are the concept areas and the skills block, titled in our words; no statement is copied.",
         "items": [{"code": c, "title": t} for c, t in [
             ("EV", "Evolution: common ancestry, diversity, selection and the evolution of resistance"),
             ("CS", "Cell structure and function: bacterial, archaeal and eukaryotic microbial cells, and viruses"),
             ("MP", "Metabolic pathways: metabolic diversity, growth and its control by the environment"),
             ("IF", "Information flow and genetics: mutation, gene transfer and regulation"),
             ("ME", "Microbial ecology: communities, biofilms, symbioses and the human microbiome"),
             ("IM", "Impact of microbes: health and disease, control, biotechnology and the environment"),
             ("LAB", "Scientific thinking and laboratory skills: microscopy, pure culture, counting, safety")]]}]
SKILLS = [("diversity", "Domains of life, classification and the evolution of microbial populations", "Diversity and evolution", []),
          ("structure", "Bacterial cell envelopes and appendages, eukaryotic microbes and viruses", "Cell structure and viruses", ["micro.diversity"]),
          ("growth", "Metabolic types, environmental limits and the arithmetic of exponential growth", "Metabolism and growth", ["micro.structure"]),
          ("genetics", "Plasmids, horizontal gene transfer and operon regulation", "Microbial genetics", ["micro.growth"]),
          ("ecology", "Biofilms, symbioses, nutrient cycles and the microbiome", "Microbial ecology", ["micro.growth"]),
          ("control", "Infection concepts, sterilisation and disinfection, antimicrobial targets, vaccines and uses of microbes", "Microbes and people", ["micro.genetics", "micro.ecology"]),
          ("lab", "Microscopy, staining, plate counts, dilutions, media and containment levels", "Laboratory skills", ["micro.structure"])]
IDEAS = [("SMALL", "Small, many and fast", "A microbe's power is in numbers: populations double in minutes to hours, so rare events (a mutation, a transfer) happen somewhere every generation."),
         ("ENV", "The environment selects", "Which microbes grow is set by oxygen, temperature, nutrients and what else is living there; the same rule explains enrichment media, the microbiome and resistance."),
         ("COUNT", "You know it when you can count it", "A colony stands for one cell that was plated; dilution arithmetic turns a plate into a concentration.")]
PRACTICES = [("P1", "Compute", "Carry a growth, dilution or optics relation to a number."),
             ("P2", "Identify", "Name the structure, process or category from a description.")]
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
DV, ST, GR, GN, EC, CT, LB = ["micro." + s[0] for s in SKILLS]
A = lambda *s: [f"asm-micro-2024:{x}" for x in s]


def F(name, skill, rows, explain):
    return Q(name, skill, "{{q}}", pace="recall", cases=[{"q": a, "o1": b, "o2": c, "o3": d, "o4": e} for a, b, c, d, e in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


def L(name, skill, prompt, options, rows, explain):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": a, "kc": k} for a, k in rows], choice=options, correct="kc", verify="authored", explain=explain)


def N(name, skill, prompt, value, verify, explain, tex="answer", **kw):
    return Q(name, skill, prompt, value=value, tex=tex, verify=verify, explain=explain, **kw)


def C(keys, rows):
    return [dict(zip(keys.split(), r)) for r in rows]


UNITS = {
 1: ("diversity", "Diversity and evolution", A("EV"), ["SMALL", "ENV"], {
   1: ("The microbial world", [
     ("A", A("EV"), "Place a microbe in its domain from its cell features.",
      "Bacteria and Archaea are prokaryotes (no nucleus, 70S ribosomes); Bacteria have peptidoglycan and ester-linked lipids, Archaea have no peptidoglycan and ether-linked lipids. Eukarya (fungi, protozoa, algae) have nuclei, organelles and 80S ribosomes. Viruses are not cells.", "P2", [
       L("mi-domain-pick", DV, "Which group does this describe? {{q}}", ["Bacteria", "Archaea", "Eukarya", "Viruses"], [
           ("Peptidoglycan cell wall, no nucleus", 0), ("No nucleus, ether-linked membrane lipids, no peptidoglycan", 1), ("Membrane-bound nucleus and mitochondria", 2),
           ("Nucleic acid in a protein coat, no ribosomes", 3), ("Yeasts and moulds", 2), ("Many methane producers and extreme halophiles", 1), ("Cannot replicate outside a host cell and has no metabolism of its own", 3)],
         "Nucleus or not, then wall and lipid chemistry; a virus has no cell at all"),
       F("mi-classification", DV, [
           ("Which molecule's sequence is the standard for placing prokaryotes on the tree of life?", "16S ribosomal RNA", "haemoglobin", "peptidoglycan", "ATP synthase protein only"),
           ("In the name Escherichia coli, what is 'coli'?", "the specific epithet", "the genus", "the family", "the strain"),
           ("Which ribosome size is found in bacteria?", "70S", "80S", "60S", "40S only"),
           ("Which group of microbes has chitin in its cell walls?", "fungi", "bacteria", "archaea", "protozoa")],
         "Ribosomal RNA is in every cell and changes slowly, so it compares everything with everything")]),
     ("B", A("EV"), "Explain how selection acts on mutations in a large population.",
      "Mutations arise at random, before any selection; in a large population a few resistant cells are already present, and a selective agent kills the rest so the survivors take over. Expected mutants = number of cells × mutation rate per cell.", "P1", [
       N("mi-expected-mutants", DV, "A culture holds 10^{{ka}} cells and a particular mutation arises at a rate of 10^-{{kb}} per cell. How many cells are expected to carry it?", "10^(ka - kb)", "10**ka/10**kb",
         "Rare per cell, common per culture: this is why a resistant mutant is usually already there", tex="n",
         cases=C("ka kb", [(9, 7), (10, 8), (8, 7), (9, 6), (11, 8)])),
       F("mi-selection", DV, [
           ("An antibiotic is added to a large culture and a resistant strain takes over. What did the antibiotic do?", "selected for mutants that were already present", "caused each cell to mutate toward resistance", "taught cells to adapt within their lifetime", "raised the mutation rate to 100%"),
           ("Why do microbial populations evolve quickly?", "short generation times and very large numbers", "they have more genes than animals", "they choose useful mutations", "they do not replicate their DNA accurately at all"),
           ("A resistance gene has a growth cost. Without the drug, what tends to happen to resistant cells over many generations?", "their share of the population falls", "they take over faster", "nothing can change", "they all revert in one generation"),
           ("What is the source of new alleles in a clonal bacterial population?", "mutation", "meiosis", "fertilisation", "crossing over between homologous chromosomes at meiosis")],
         "Mutation proposes, the environment disposes")])]),
 }),
 2: ("structure", "Cell structure and viruses", A("CS"), ["SMALL"], {
   1: ("Cells and viruses", [
     ("A", A("CS"), "Contrast the Gram-positive and Gram-negative cell envelopes.",
      "Gram-positive cells have a thick peptidoglycan layer with teichoic acids and no outer membrane. Gram-negative cells have a thin peptidoglycan layer in a periplasm beneath an outer membrane whose outer leaflet is lipopolysaccharide.", "P2", [
       L("mi-gram-feature", ST, "Gram-positive or Gram-negative? {{q}}", ["Gram-positive", "Gram-negative"], [
           ("Thick peptidoglycan layer", 0), ("Outer membrane with lipopolysaccharide", 1), ("Teichoic acids in the wall", 0),
           ("Periplasmic space between two membranes", 1), ("Stains pink after the Gram stain", 1), ("Keeps crystal violet and stains purple", 0)],
         "Thick wall holds the purple dye; an outer membrane and thin wall lets it wash out"),
       F("mi-envelope-parts", ST, [
           ("What polymer gives the bacterial cell wall its strength?", "peptidoglycan", "cellulose", "chitin", "lipopolysaccharide"),
           ("Which component of the Gram-negative outer membrane acts as endotoxin?", "the lipid A part of lipopolysaccharide", "teichoic acid", "porin protein", "peptidoglycan"),
           ("What do porins do?", "let small molecules cross the outer membrane", "anchor flagella", "make ATP", "cross-link peptidoglycan"),
           ("What does the enzyme lysozyme attack?", "peptidoglycan", "the outer membrane", "ribosomes", "DNA")],
         "Peptidoglycan is the load-bearing layer in both; the outer membrane is the extra barrier")]),
     ("B", A("CS"), "Match bacterial structures to their functions.",
      "Flagella give motility, pili and fimbriae attachment (and the sex pilus conjugation), a capsule protection from drying and phagocytosis, endospores survival of heat and chemicals. Plasmids carry extra genes.", "P2", [
       F("mi-structures", ST, [
           ("Which structure lets a bacterium swim?", "flagellum", "fimbria", "capsule", "endospore"),
           ("Which structure helps a bacterium avoid being engulfed by phagocytes?", "capsule", "flagellum", "ribosome", "plasmid"),
           ("Which structure mainly attaches a bacterium to surfaces?", "fimbriae", "flagella", "endospores", "inclusion bodies"),
           ("Which structure is a dormant form that survives boiling?", "endospore", "capsule", "cyst wall of a virus", "pilus")],
         "Move, stick, hide, survive"),
       F("mi-endospores", ST, [
           ("Why are endospores important in sterilisation?", "they are the hardest form of life to kill, so methods are judged against them", "they multiply during heating", "they are the easiest cells to kill", "they only form in the autoclave"),
           ("What triggers a cell to form an endospore?", "nutrient depletion", "abundant nutrients", "exposure to light", "cell division"),
           ("Is sporulation a form of reproduction?", "no: one cell makes one spore", "yes: one cell makes many spores", "yes: two spores per cell", "only in Gram-negative cells"),
           ("Which conditions does an autoclave use to kill endospores?", "steam at 121 °C under pressure for about 15 minutes", "boiling water for 1 minute", "dry air at 60 °C", "70% ethanol for 30 seconds")],
         "One cell, one spore: survival, not multiplication")]),
     ("C", A("CS"), "Tell the eukaryotic microbes apart and compare them with bacteria.",
      "Fungi are heterotrophs with chitin walls and ergosterol membranes (yeasts are single cells, moulds grow as hyphae); protozoa are single-celled and usually motile; algae photosynthesise. Their 80S ribosomes and sterol membranes make them harder to target without harming the host.", "P2", [
       L("mi-eukaryotic-microbe", ST, "Which kind of microbe? {{q}}", ["Fungus", "Protozoan", "Alga", "Bacterium"], [
           ("Grows as hyphae and absorbs nutrients", 0), ("Single eukaryotic cell that moves by cilia or pseudopodia", 1), ("Photosynthetic eukaryote with cellulose walls", 2),
           ("Single-celled budding yeast", 0), ("Prokaryote that divides by binary fission", 3), ("Chitin cell wall and ergosterol in the membrane", 0)],
         "Fungi absorb, protozoa ingest and move, algae photosynthesise"),
       F("mi-eukaryote-vs-bacteria", ST, [
           ("Why do many antibacterial drugs not harm human cells?", "they target structures bacteria have and we lack, such as peptidoglycan and 70S ribosomes", "human cells pump every drug out", "human cells have thicker walls", "bacteria are larger"),
           ("Why are fungal infections harder to treat selectively than bacterial ones?", "fungal cells are eukaryotic and share more targets with our cells", "fungi have no membranes", "fungi have peptidoglycan", "fungi are viruses"),
           ("Which membrane sterol do fungi have in place of cholesterol?", "ergosterol", "lanosterol only", "hopanoids", "none"),
           ("How do bacteria divide?", "binary fission", "mitosis", "meiosis", "budding from hyphae")],
         "Selective toxicity depends on a difference between the microbe and the host")]),
     ("D", A("CS"), "Describe a virus particle and the stages of viral replication.",
      "A virion is a genome (DNA or RNA) in a protein capsid, sometimes with a lipid envelope. Replication runs attachment, entry, synthesis, assembly, release. A lytic phage bursts its host; a temperate phage can integrate as a prophage (lysogeny).", "P2", [
       F("mi-virus-parts", ST, [
           ("What is the protein coat of a virus called?", "capsid", "envelope", "capsule", "cell wall"),
           ("Where does an enveloped virus get its envelope?", "from a host cell membrane", "it synthesises its own lipids", "from the capsid", "from the growth medium"),
           ("Which step of replication depends on a match between viral proteins and host receptors?", "attachment", "assembly", "release", "synthesis"),
           ("Why can viruses not be grown on nutrient agar alone?", "they need living host cells to replicate", "they need more sugar", "they need oxygen", "they grow too slowly to see")],
         "Genome, capsid, sometimes envelope; attachment decides the host range"),
       L("mi-lytic-lysogenic", ST, "Lytic or lysogenic cycle? {{q}}", ["Lytic", "Lysogenic"], [
           ("The host cell bursts and releases new phage", 0), ("Phage DNA integrates into the host chromosome", 1), ("The phage genome is copied each time the host divides", 1),
           ("Clear plaques appear on a bacterial lawn", 0), ("A prophage is present", 1)],
         "Lytic kills now; lysogenic waits inside the chromosome")])]),
 }),
 3: ("growth", "Metabolism and growth", A("MP"), ["ENV", "SMALL"], {
   1: ("Growth", [
     ("A", A("MP"), "Classify a microbe by its energy and carbon source.",
      "Phototrophs take energy from light, chemotrophs from chemicals (organotrophs from organic compounds, lithotrophs from inorganic ones). Autotrophs fix carbon dioxide; heterotrophs need organic carbon.", "P2", [
       L("mi-metabolic-type", GR, "Which metabolic type? {{q}}", ["Photoautotroph", "Chemoheterotroph", "Chemolithoautotroph", "Photoheterotroph"], [
           ("Cyanobacteria: light for energy, carbon dioxide for carbon", 0), ("Most bacteria that live on glucose", 1), ("Nitrifying bacteria: oxidise ammonia, fix carbon dioxide", 2),
           ("Uses light for energy but needs organic carbon", 3), ("Fungi decomposing wood", 1), ("Sulfur-oxidising bacteria at a hydrothermal vent", 2)],
         "First word is the energy source, last word is the carbon source"),
       F("mi-energy-carbon", GR, [
           ("What does 'autotroph' say about an organism?", "it gets its carbon from carbon dioxide", "it gets its energy from light", "it needs no nitrogen", "it cannot live alone"),
           ("What does 'lithotroph' say about an organism?", "it takes electrons from inorganic compounds", "it lives only on rock surfaces", "it uses light", "it eats lipids"),
           ("Which metabolic type includes all animals and most pathogens?", "chemoheterotroph", "photoautotroph", "chemolithoautotroph", "photoheterotroph"),
           ("Which process fixes most of the carbon in the ocean?", "photosynthesis by cyanobacteria and algae", "fermentation", "nitrification", "methanogenesis")],
         "Energy, electrons, carbon: three separate questions")]),
     ("B", A("MP"), "Predict where a microbe grows from its oxygen and temperature needs.",
      "Obligate aerobes need oxygen, obligate anaerobes are harmed by it, facultative anaerobes use it when present, microaerophiles need a little, aerotolerant anaerobes ignore it. Psychrophiles, mesophiles (body temperature) and thermophiles are named by optimum temperature.", "P2", [
       L("mi-oxygen-class", GR, "In a tube of thioglycollate broth, where does this organism grow? {{q}}", ["Only at the top", "Only at the bottom", "Throughout, densest at the top", "In a band just below the surface", "Evenly throughout"], [
           ("Obligate aerobe", 0), ("Obligate anaerobe", 1), ("Facultative anaerobe", 2), ("Microaerophile", 3), ("Aerotolerant anaerobe", 4)],
         "Oxygen falls from the top of the tube to the bottom, and each class sits where its needs are met"),
       F("mi-environment-limits", GR, [
           ("Which temperature class includes most human pathogens?", "mesophiles", "psychrophiles", "thermophiles", "hyperthermophiles"),
           ("Which enzymes protect aerobes from reactive oxygen species?", "catalase and superoxide dismutase", "lysozyme and amylase", "DNA polymerase", "nitrogenase"),
           ("Why does salting or sugaring preserve food?", "low water activity draws water out of cells", "salt is a nutrient", "it raises the pH", "it adds oxygen"),
           ("What is an organism that grows best at low pH called?", "acidophile", "alkaliphile", "halophile", "barophile")],
         "Every preservation method takes away something growth needs")]),
     ("C", A("MP"), "Read a growth curve and do the arithmetic of doubling.",
      "A batch culture shows lag, exponential (log), stationary and death phases. In exponential growth N = N0 × 2^n with n = time ÷ generation time, so the generation time is t × log 2 ÷ log(N/N0).", "P1", [
       N("mi-doubling-count", GR, "A culture starts with {{ka}} cells and doubles every {{kg}} minutes. How many cells are there after {{kt}} minutes of exponential growth?", "ka*2^(kt/kg)", "ka*exp((kt/kg)*log(2))",
         "Count the doublings first, then multiply by 2 that many times", tex="N",
         cases=C("ka kg kt", [(100, 20, 120), (50, 30, 180), (1000, 20, 60), (200, 40, 200), (10, 20, 200)])),
       N("mi-generation-time", GR, "A culture grows exponentially from {{ka}} to {{kb}} cells in {{kt}} minutes. Find the generation time in minutes.", "kt/log2(kb/ka)", "kt*log(2)/(log(kb) - log(ka))",
         "n = log2(N/N0) doublings took t minutes, so each took t/n", tex="g",
         cases=C("ka kb kt", [(1000, 8000, 90), (500, 16000, 150), (100, 6400, 120), (2000, 64000, 200), (300, 2400, 60)]))]),
     ("D", A("MP"), "Compare fermentation with respiration.",
      "Respiration passes electrons down a transport chain to a terminal acceptor (oxygen in aerobic, nitrate or sulfate in anaerobic respiration) and makes ATP mostly by oxidative phosphorylation. Fermentation has no chain: ATP comes from glycolysis alone, and an organic molecule takes the electrons to regenerate NAD+.", "P2", [
       L("mi-ferment-respire", GR, "Fermentation, aerobic respiration or anaerobic respiration? {{q}}", ["Fermentation", "Aerobic respiration", "Anaerobic respiration"], [
           ("Pyruvate is reduced to lactate to regenerate NAD+", 0), ("Oxygen is the terminal electron acceptor", 1), ("Nitrate is the terminal electron acceptor of an electron transport chain", 2),
           ("Yeast making ethanol and carbon dioxide", 0), ("About 2 ATP per glucose, all by substrate-level phosphorylation", 0), ("The highest ATP yield per glucose", 1)],
         "Ask what takes the electrons at the end, and whether a chain is involved"),
       F("mi-fermentation-facts", GR, [
           ("What is the purpose of the last step of fermentation?", "to regenerate NAD+ so glycolysis can continue", "to make most of the ATP", "to fix carbon dioxide", "to build a proton gradient"),
           ("Which product of lactic acid bacteria sours milk into yoghurt?", "lactic acid", "ethanol", "acetone", "methane"),
           ("Where is the electron transport chain in a bacterium?", "the cytoplasmic membrane", "the mitochondrion", "the cell wall", "the nucleoid"),
           ("A facultative anaerobe is moved from air to no oxygen with only glucose. What happens to its growth yield per glucose?", "it falls", "it rises", "it is unchanged", "it doubles")],
         "No chain, no gradient, little ATP: fermenters must burn far more sugar")])]),
 }),
 4: ("genetics", "Microbial genetics", A("IF"), ["SMALL"], {
   1: ("Genes on the move", [
     ("A", A("IF"), "Tell the three routes of horizontal gene transfer apart.",
      "Transformation is uptake of free DNA from the surroundings; transduction is transfer by a bacteriophage; conjugation is transfer by cell-to-cell contact through a pilus, usually of a plasmid. All three move genes between cells of the same generation.", "P2", [
       L("mi-hgt-route", GN, "Transformation, transduction or conjugation? {{q}}", ["Transformation", "Transduction", "Conjugation"], [
           ("A cell takes up DNA released by dead cells", 0), ("A phage carries bacterial genes to a new host", 1), ("A plasmid passes through a pilus between touching cells", 2),
           ("Transfer still happens when the DNA is free in solution but stops if DNase is added", 0), ("Transfer needs cell contact and is blocked by a filter between the strains", 2),
           ("Griffith's rough and smooth pneumococcus experiment", 0)],
         "Naked DNA, a virus, or contact"),
       F("mi-hgt-facts", GN, [
           ("What is a small, circular, self-replicating piece of DNA separate from the chromosome?", "plasmid", "prophage", "operon", "transposase"),
           ("Why does horizontal transfer matter for antibiotic resistance?", "one cell can pass a resistance gene to another, even of a different species", "it raises the mutation rate", "it destroys plasmids", "it only moves genes to daughter cells"),
           ("What is a cell that is able to take up free DNA called?", "competent", "lysogenic", "auxotrophic", "virulent"),
           ("What is a DNA segment that can move from place to place in a genome called?", "transposon", "codon", "promoter", "ribosome")],
         "Vertical transfer is parent to offspring; horizontal transfer is neighbour to neighbour")]),
     ("B", A("IF"), "Predict whether the lac operon is expressed.",
      "The lac repressor binds the operator and blocks transcription unless allolactose (from lactose) removes it. Strong expression also needs low glucose, when cAMP with its activator protein helps RNA polymerase bind. So the operon is fully on only with lactose present and glucose absent.", "P2", [
       L("mi-lac-state", GN, "With {{q}}, how strongly is the lac operon transcribed?", ["Strongly", "Weakly or not at all"], [
           ("lactose present and glucose absent", 0), ("lactose absent and glucose present", 1), ("lactose present and glucose present", 1),
           ("lactose absent and glucose absent", 1), ("a mutant repressor that cannot bind the operator, and glucose absent", 0)],
         "Two conditions: the repressor must be off and the activator must be on"),
       F("mi-operon-parts", GN, [
           ("To which DNA site does the lac repressor bind?", "operator", "promoter", "terminator", "origin of replication"),
           ("What is the inducer of the lac operon?", "allolactose", "glucose", "cAMP", "tryptophan"),
           ("What is an operon?", "a group of genes transcribed together from one promoter", "a single gene with introns", "a plasmid", "a ribosome binding site"),
           ("Why can transcription and translation be coupled in bacteria?", "there is no nuclear membrane separating them", "bacteria have no ribosomes", "bacterial mRNA is spliced first", "bacteria have no RNA polymerase")],
         "Regulating a whole pathway with one switch is economical")]),
     ("C", A("IF"), "Classify mutations and find a mutation frequency.",
      "A point mutation may be silent, missense or nonsense; an insertion or deletion not in threes shifts the reading frame. Mutation frequency is mutant colonies over total viable cells plated.", "P1", [
       L("mi-mutation-type", GN, "What kind of mutation? {{q}}", ["Silent", "Missense", "Nonsense", "Frameshift"], [
           ("A base change that leaves the amino acid the same", 0), ("A base change that swaps one amino acid for another", 1), ("A base change that creates a stop codon", 2),
           ("One base is deleted from the middle of a gene", 3), ("Two bases are inserted into a coding sequence", 3)],
         "Same, different, stop, or shifted"),
       N("mi-mutation-frequency", GN, "A plate with a selective agent grows {{km}} colonies from a sample that holds {{kt}} × 10^{{kp}} viable cells. Find the mutant frequency as mutants per 10^{{kp}} cells.", "km/kt", f"solve(Eq({M}*kt, km), {M})[0]",
         "Frequency is mutants over total cells; expressing it per 10^n keeps the number readable", tex="f",
         cases=C("km kt kp", [(30, 2, 8), (12, 4, 9), (45, 3, 8), (8, 2, 7), (50, 5, 9)]))])]),
 }),
 5: ("ecology", "Microbial ecology", A("ME"), ["ENV"], {
   1: ("Communities", [
     ("A", A("ME"), "Describe biofilms and classify symbioses.",
      "Most microbes live in biofilms: communities attached to a surface in a self-made matrix, coordinated by quorum sensing and far harder to remove than free cells. In mutualism both partners benefit, in commensalism one benefits and the other is unaffected, in parasitism one benefits at the other's cost.", "P2", [
       L("mi-symbiosis", EC, "Mutualism, commensalism or parasitism? {{q}}", ["Mutualism", "Commensalism", "Parasitism"], [
           ("Rhizobia fix nitrogen in legume root nodules and receive sugars", 0), ("Skin bacteria feed on shed cells without affecting the host", 1), ("A pathogen multiplies in host tissue and damages it", 2),
           ("Rumen microbes digest cellulose for a cow and are fed and housed", 0), ("Gut bacteria make vitamin K and receive nutrients", 0)],
         "Score each partner: plus, zero or minus"),
       F("mi-biofilm", EC, [
           ("What is a biofilm?", "a surface-attached community embedded in a matrix it secretes", "a single layer of dead cells", "a pure culture on agar", "a virus coat"),
           ("What is quorum sensing?", "cells sensing their population density through secreted signal molecules", "cells counting their own chromosomes", "phage choosing between cycles", "swimming toward nutrients"),
           ("Which is an everyday example of a biofilm?", "dental plaque", "a drop of sterile saline", "a colony's agar", "a virus particle"),
           ("Compared with free-floating cells, how do biofilm cells respond to disinfectants and antibiotics?", "they are much harder to kill", "they are easier to kill", "there is no difference", "they are always killed instantly")],
         "The matrix and slow growth inside it are what make a biofilm stubborn")]),
     ("B", A("ME"), "Assign microbes their steps in the nitrogen and carbon cycles.",
      "Nitrogen fixation turns N2 into ammonia; nitrification oxidises ammonia to nitrite and nitrate; denitrification returns nitrate to N2; decomposers release ammonia from organic matter. Photosynthesisers fix carbon; decomposers and methanogens return it.", "P2", [
       L("mi-nitrogen-step", EC, "Which step of the nitrogen cycle? {{q}}", ["Nitrogen fixation", "Nitrification", "Denitrification", "Ammonification"], [
           ("N2 gas is converted to ammonia", 0), ("Ammonia is oxidised to nitrate", 1), ("Nitrate is reduced to N2 gas", 2),
           ("Decomposers release ammonia from proteins", 3), ("Carried out by Rhizobium in root nodules", 0), ("Returns nitrogen to the atmosphere in waterlogged soil", 2)],
         "Fix it, oxidise it, breathe it away, or rot it loose"),
       F("mi-cycles", EC, [
           ("Which enzyme reduces N2 to ammonia?", "nitrogenase", "nitrate reductase", "rubisco", "catalase"),
           ("Which organisms are the only ones able to fix atmospheric nitrogen?", "certain bacteria and archaea", "all plants", "fungi", "animals"),
           ("Which group of archaea produces methane?", "methanogens", "halophiles", "cyanobacteria", "nitrifiers"),
           ("What is the role of decomposers in the carbon cycle?", "they return carbon in dead matter to carbon dioxide", "they fix carbon dioxide into sugar", "they store carbon as limestone", "they have none")],
         "Every element's cycle has steps that only microbes perform")]),
     ("C", A("ME"), "Describe the human microbiome and what it does for its host.",
      "The body carries resident microbes, densest in the large intestine and absent from normally sterile sites such as blood and cerebrospinal fluid. Residents compete with invaders (colonisation resistance), make vitamins, digest fibre and train the immune system; broad antibiotics disturb them.", "P2", [
       F("mi-microbiome-sites", EC, [
           ("Which body site carries the most microbes?", "large intestine", "stomach", "lungs", "blood"),
           ("Which of these is normally free of microbes in a healthy person?", "blood", "skin", "mouth", "colon"),
           ("Why does the stomach carry few microbes?", "its strong acid kills most of them", "it has no nutrients", "it is too cold", "it has no surface"),
           ("When does a newborn first acquire most of its microbiome?", "during and after birth", "at conception", "at weaning only", "at puberty")],
         "Wet, warm, fed and not acidic means many microbes"),
       F("mi-microbiome-roles", EC, [
           ("What is colonisation resistance?", "resident microbes out-competing incoming ones for space and nutrients", "the host's antibodies killing residents", "resistance of residents to antibiotics", "the skin's dryness"),
           ("Why can a course of broad-spectrum antibiotics be followed by overgrowth of an unusual organism?", "the normal competitors have been removed", "the antibiotic feeds it", "the immune system switches off", "it mutates into a virus"),
           ("Which vitamin do gut bacteria contribute to?", "vitamin K", "vitamin C", "vitamin D", "vitamin A"),
           ("What is a resident microbe that causes disease when defences are lowered called?", "opportunistic pathogen", "obligate pathogen", "commensal that never harms", "bacteriophage")],
         "The microbiome is a defence as well as a passenger")])]),
 }),
 6: ("control", "Microbes and people", A("IM"), ["ENV", "COUNT"], {
   1: ("Disease, control and use", [
     ("A", A("IM"), "Use the vocabulary of infection and tell endotoxin from exotoxin.",
      "Infection is growth of a microbe in a host; disease is damage that results. Koch's postulates tie one organism to one disease by isolating it, growing it in pure culture and reproducing the disease. Exotoxins are secreted proteins; endotoxin is the lipid A of Gram-negative outer membranes, released when cells break up.", "P2", [
       L("mi-toxin-type", CT, "Exotoxin or endotoxin? {{q}}", ["Exotoxin", "Endotoxin"], [
           ("A protein secreted by living cells", 0), ("Part of the Gram-negative outer membrane", 1), ("Inactivated by heat and can be made into a toxoid vaccine", 0),
           ("Lipid A of lipopolysaccharide", 1), ("Causes fever and shock in a similar way whatever the species", 1), ("Has a specific cell target and is potent in very small amounts", 0)],
         "Exotoxins are secreted proteins with specific targets; endotoxin is structural lipid with a general effect"),
       F("mi-infection-terms", CT, [
           ("Which of Koch's postulates requires growing the organism away from the host?", "isolating it in pure culture", "finding it in every case", "reproducing the disease in a new host", "re-isolating it"),
           ("What is an infection acquired in a hospital or clinic called?", "healthcare-associated (nosocomial)", "zoonotic", "latent", "congenital"),
           ("What is a disease transmitted from animals to humans called?", "zoonosis", "nosocomial infection", "vector", "fomite"),
           ("What is an inanimate object that carries microbes from one host to another called?", "fomite", "vector", "reservoir", "carrier")],
         "Reservoir, route, portal, host: each word names one link in the chain")]),
     ("B", A("IM"), "Tell sterilisation from disinfection and compute a decimal reduction.",
      "Sterilisation removes or kills all life including endospores; disinfection reduces microbes on objects; antisepsis does so on living tissue. Death is exponential: each D-value (decimal reduction time) cuts the population tenfold, so survivors = N0 × 10^(−t/D).", "P1", [
       L("mi-control-term", CT, "Sterilisation, disinfection or antisepsis? {{q}}", ["Sterilisation", "Disinfection", "Antisepsis"], [
           ("Autoclaving surgical instruments", 0), ("Wiping a bench with dilute bleach", 1), ("Swabbing skin with alcohol before an injection", 2),
           ("Filtering a heat-sensitive solution through a 0.2 micrometre membrane to remove all cells", 0), ("Washing hands with chlorhexidine", 2)],
         "All life gone, fewer microbes on a thing, fewer microbes on a person"),
       N("mi-decimal-reduction", CT, "A process has a D-value of {{kd}} minutes. Starting from 10^{{ka}} cells, how many are expected to survive {{kt}} minutes?", "10^(ka - kt/kd)", "10**ka*exp(-(kt/kd)*log(10))",
         "Each D-value removes 90%, so count the tenfold steps and subtract them from the exponent", tex="N",
         cases=C("kd ka kt", [(2, 6, 8), (1.5, 6, 6), (0.5, 8, 2), (3, 5, 9), (2, 9, 12)]))]),
     ("C", A("IM"), "Match antimicrobial drug classes to their targets and name general resistance mechanisms.",
      "Beta-lactams and glycopeptides block cell wall synthesis; aminoglycosides, tetracyclines and macrolides act on the 70S ribosome; fluoroquinolones on DNA gyrase; sulfonamides on folate synthesis. Resistance arises by destroying the drug, altering the target, pumping the drug out or keeping it out.", "P2", [
       F("mi-drug-targets", CT, [
           ("What do penicillins and other beta-lactams inhibit?", "peptidoglycan cross-linking", "protein synthesis", "DNA gyrase", "folate synthesis"),
           ("What do macrolides and tetracyclines inhibit?", "the bacterial ribosome", "cell wall synthesis", "DNA gyrase", "the cell membrane"),
           ("What do fluoroquinolones inhibit?", "DNA gyrase and topoisomerase", "peptidoglycan synthesis", "the 30S subunit", "folate synthesis"),
           ("What do sulfonamides inhibit?", "folic acid synthesis", "the 50S subunit", "cell wall synthesis", "RNA polymerase")],
         "Wall, ribosome, DNA, metabolism: four places bacteria differ from us"),
       L("mi-resistance-mechanism", CT, "Which general mechanism of resistance? {{q}}", ["Enzyme destroys the drug", "Target is altered", "Efflux pump", "Reduced uptake"], [
           ("A beta-lactamase cuts the drug's ring", 0), ("A changed ribosomal site no longer binds the drug", 1), ("A membrane protein exports the drug as fast as it enters", 2),
           ("Fewer or narrower porins in the outer membrane", 3), ("An altered penicillin-binding protein", 1)],
         "Break it, change the lock, bail it out, or shut the door")]),
     ("D", A("IM"), "Classify vaccines and explain why antibiotics do not treat viral infections.",
      "Live attenuated vaccines replicate weakly and give strong lasting immunity; inactivated vaccines cannot replicate; subunit, toxoid and conjugate vaccines use parts; mRNA vaccines have the host cell make the antigen. Antibiotics target bacterial structures that viruses lack.", "P2", [
       L("mi-vaccine-type", CT, "Which kind of vaccine? {{q}}", ["Live attenuated", "Inactivated (killed)", "Subunit, toxoid or conjugate", "mRNA"], [
           ("A weakened virus that still replicates in the recipient", 0), ("Whole virus treated so it cannot replicate", 1), ("An inactivated bacterial toxin", 2),
           ("A lipid nanoparticle carrying instructions for one viral protein", 3), ("A capsule polysaccharide linked to a carrier protein", 2)],
         "Whole and alive, whole and dead, a piece, or the recipe for a piece"),
       F("mi-antibiotic-virus", CT, [
           ("Why do antibiotics not cure viral infections?", "viruses have no cell wall, ribosomes or metabolism of their own to target", "viruses are too small to absorb drugs", "viruses pump antibiotics out", "viruses are resistant by mutation"),
           ("What do antiviral drugs typically target?", "steps specific to the virus, such as its polymerase or protease", "peptidoglycan", "the 70S ribosome", "bacterial DNA gyrase"),
           ("Why are live attenuated vaccines generally avoided in severely immunocompromised people?", "the weakened organism may still cause disease in them", "they contain antibiotics", "they do not contain antigen", "they are always ineffective"),
           ("What does an adjuvant in a vaccine do?", "strengthens the immune response to the antigen", "kills the pathogen", "replaces the antigen", "prevents memory cell formation")],
         "A drug needs a target; a virus borrows almost everything from its host")]),
     ("E", A("IM"), "Give uses of microbes in food, industry and the environment.",
      "Fermentations make bread, beer, wine, yoghurt, cheese and vinegar; engineered microbes make insulin and enzymes; microbes treat sewage and break down pollutants (bioremediation).", "P2", [
       F("mi-food-microbes", CT, [
           ("Which microbe raises bread and ferments beer?", "the yeast Saccharomyces cerevisiae", "Lactobacillus", "Acetobacter", "Penicillium"),
           ("Which group of bacteria makes yoghurt and sauerkraut?", "lactic acid bacteria", "nitrifying bacteria", "cyanobacteria", "methanogens"),
           ("Which process turns wine into vinegar?", "oxidation of ethanol to acetic acid by acetic acid bacteria", "lactic fermentation", "alcoholic fermentation", "nitrification"),
           ("Why does pasteurisation not sterilise milk?", "it uses mild heat that kills pathogens and most spoilage organisms but not all cells or spores", "it adds preservatives", "it removes water", "it uses filtration only")],
         "Fermentation preserves food by making acid or alcohol"),
       F("mi-industry-microbes", CT, [
           ("How is human insulin produced for medicine?", "by microbes carrying the human insulin gene", "by extraction from human donors", "by chemical synthesis from glucose", "from plant sap"),
           ("What is bioremediation?", "using microbes to break down pollutants", "sterilising soil with heat", "adding antibiotics to water", "growing crops without soil"),
           ("In sewage treatment, what do aerobic microbes in the activated sludge step do?", "oxidise dissolved organic matter", "add nitrogen", "kill all viruses", "remove salt"),
           ("Which heat-stable enzyme from a thermophile made PCR practical?", "Taq DNA polymerase", "lysozyme", "beta-galactosidase", "nitrogenase")],
         "Most microbes are useful, and a few are indispensable")])]),
 }),
 7: ("lab", "Laboratory skills", A("LAB"), ["COUNT"], {
   1: ("Seeing and counting", [
     ("A", A("LAB"), "Find magnification and the resolution limit of a light microscope.",
      "Total magnification is ocular × objective. The smallest resolvable distance is about 0.61 × wavelength ÷ numerical aperture, so shorter wavelengths and oil immersion (higher NA) resolve finer detail; about 0.2 micrometres is the practical limit.", "P1", [
       N("mi-magnification", LB, "A microscope has a {{ka}}× ocular lens and a {{kb}}× objective lens. Find the total magnification.", "ka*kb", f"solve(Eq({M}/ka, kb), {M})[0]",
         "Multiply the two lenses", tex="M", final=True,
         cases=C("ka kb", [(10, 40), (10, 100), (15, 40), (10, 4), (12, 100)])),
       N("mi-resolution", LB, "Light of wavelength {{kl}} nm is used with an objective of numerical aperture {{kn}}. Find the smallest resolvable distance in nm from d = 0.61 λ / NA.", "0.61*kl/kn", f"solve(Eq({M}*kn, Rational(61, 100)*kl), {M})[0]",
         "Shorter wavelength or larger aperture resolves smaller detail; oil raises the aperture", tex="d",
         cases=C("kl kn", [(550, 1.25), (500, 1.4), (450, 0.65), (600, 0.25), (400, 1.3)]))]),
     ("B", A("LAB"), "Order the Gram stain and choose a stain for a purpose.",
      "Crystal violet (primary stain), iodine (mordant), alcohol (decolouriser), safranin (counterstain). The decolouriser step is the one that separates the two groups. Acid-fast staining shows waxy mycolic acid walls; malachite green shows endospores; negative stains show capsules.", "P2", [
       F("mi-gram-steps", LB, [
           ("Which reagent is the primary stain in the Gram stain?", "crystal violet", "safranin", "iodine", "alcohol"),
           ("Which reagent is the mordant in the Gram stain?", "iodine", "crystal violet", "safranin", "acetone"),
           ("Which reagent is the counterstain in the Gram stain?", "safranin", "crystal violet", "iodine", "methylene blue"),
           ("If the alcohol step is left on far too long, what is the likely error?", "Gram-positive cells appear pink", "Gram-negative cells appear purple", "no cells take up any stain", "endospores turn green"),
           ("If the decolouriser is skipped, what colour are all cells?", "purple", "pink", "colourless", "green")],
         "Violet, iodine, alcohol, safranin; the alcohol step makes the difference"),
       F("mi-stain-choice", LB, [
           ("Which stain is used for cells with waxy, mycolic acid walls?", "acid-fast stain", "Gram stain only", "negative stain", "simple stain with safranin"),
           ("Which technique shows a capsule as a clear halo?", "negative staining with India ink or nigrosin", "acid-fast staining", "endospore staining", "heat fixing"),
           ("Which dye is driven into endospores with heat in the endospore stain?", "malachite green", "crystal violet", "carbol fuchsin", "safranin"),
           ("What is the purpose of heat-fixing a smear?", "to attach the cells to the slide and kill them", "to stain them", "to make them motile", "to dissolve the wall")],
         "Choose the stain for the structure you need to see")]),
     ("C", A("LAB"), "Turn a plate count and a dilution series into a concentration.",
      "Each colony comes from one viable cell or clump (a colony-forming unit). CFU per mL = colonies ÷ (volume plated × dilution). A serial dilution multiplies the factors of each step. Plates with roughly 30 to 300 colonies are counted.", "P1", [
       N("mi-cfu-per-ml", LB, "{{kv}} mL of a 10^-{{kd}} dilution is spread on a plate and {{kn}} colonies grow. Find the concentration of the original sample in CFU/mL.", "kn*10^kd/kv", f"solve(Eq({M}*kv/10**kd, kn), {M})[0]",
         "Divide by the volume plated, then undo the dilution", tex="c",
         cases=C("kv kd kn", [(0.1, 5, 42), (1, 6, 150), (0.1, 4, 215), (0.5, 3, 60), (0.1, 6, 87)])),
       N("mi-serial-dilution", LB, "{{ka}} mL of culture is added to {{kb}} mL of diluent, and the same step is repeated for a total of {{kn}} steps. By what factor has the original culture been diluted?", "((ka + kb)/ka)^kn",
         "exp(kn*(log(ka + kb) - log(ka)))", "Each step's factor is total volume over volume transferred; steps multiply", tex="factor",
         cases=C("ka kb kn", [(1, 9, 4), (1, 99, 3), (0.1, 9.9, 2), (1, 4, 3), (2, 18, 5)]))]),
     ("D", A("LAB"), "Choose a medium and name the principles of aseptic work and containment levels.",
      "A selective medium suppresses unwanted organisms; a differential medium makes groups look different; some do both. A streak plate thins cells until single colonies form a pure culture. Laboratories are graded biosafety level 1 to 4 by the risk of the agents handled, with practices and containment rising at each level.", "P2", [
       L("mi-medium-type", LB, "Selective, differential or both? {{q}}", ["Selective only", "Differential only", "Both selective and differential"], [
           ("Blood agar, where colonies show different patterns of haemolysis", 1), ("MacConkey agar: bile salts inhibit Gram-positives, lactose fermenters turn pink", 2),
           ("A nutrient medium with an antibiotic added so only resistant cells grow", 0), ("Mannitol salt agar: high salt, with a pH indicator for mannitol fermentation", 2)],
         "Selective stops some growing; differential makes those that grow look different"),
       F("mi-aseptic-containment", LB, [
           ("What is the purpose of a streak plate?", "to obtain isolated colonies from a mixed sample", "to count viable cells exactly", "to sterilise the loop", "to stain cells"),
           ("How many biosafety levels are there, and which is the most stringent?", "four; level 4", "three; level 1", "four; level 1", "five; level 5"),
           ("Which biosafety level suits teaching work with well-characterised agents not known to cause disease in healthy adults?", "BSL-1", "BSL-2", "BSL-3", "BSL-4"),
           ("Why is an inoculating loop flamed before and after each transfer?", "to avoid carrying unwanted organisms into or out of the culture", "to warm the culture", "to fix the cells", "to dry the agar")],
         "A pure culture is one kind of cell descended from one cell, and asepsis keeps it that way")])]),
 }),
}
ADD = [(f"{FW['code']}-{n}.{tn}.{lo[0]}", qq) for n, u in UNITS.items() for tn, (tt, los) in u[4].items() for lo in los for qq in lo[5]]
