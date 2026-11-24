"""Second question types for AP Biology, units 6-10."""
from opl_dsl import Q

FILE, FRAMEWORK = "bi-second-types-2", "biology"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]


def facts(name, skill, rows, explain, prompt="{{q}}"):
    return Q(name, skill, prompt, pace="recall", cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


MG, EVO, ECO, PHY, DIV = "bio.molecular-genetics", "bio.evolution", "bio.ecology", "bio.physiology", "bio.diversity"

ADD = [
    # ── unit 6 gene expression ───────────────────────────────────────────
    ("BI-6.1.A", facts("bi-genome-scenario", MG, [
        ("A cell has one circular chromosome plus small extra rings of DNA. What is it?", "A bacterium with plasmids", "A human cell", "A plant cell nucleus", "A virus"),
        ("Why do eukaryotes wrap DNA around histones?", "To pack long linear chromosomes and help control access to genes", "To make proteins", "To replicate RNA", "To store glucose"),
        ("Which genome has more noncoding DNA per gene?", "A typical eukaryote's", "A typical bacterium's", "They are equal", "Neither has any"),
    ], "Prokaryotes: compact, circular, operons, plasmids; eukaryotes: linear chromosomes on histones with much noncoding DNA")),
    ("BI-6.1.B", facts("bi-dna-experiment", MG, [
        ("Griffith's heat-killed smooth bacteria made rough ones deadly. What did this show?", "A heritable 'transforming principle' could pass between cells", "Proteins are genes", "Viruses make bacteria", "Heat creates life"),
        ("Avery's team destroyed DNA in the extract and transformation stopped. What did that show?", "DNA is the transforming principle", "Protein is the gene", "RNA is the gene", "Lipids carry heredity"),
        ("Why was DNA suited to carry heredity?", "Its base sequence stores information and pairing lets it be copied", "It is a protein", "It is unstable", "It has 20 kinds of monomer"),
    ], "Transformation, enzyme destruction and the phage experiments together pinned heredity on DNA")),
    ("BI-6.2.A", facts("bi-replication-defect", MG, [
        ("A cell lacks DNA ligase. What is left behind?", "Unjoined Okazaki fragments", "No primers", "Unwound DNA that cannot be copied", "Extra telomeres"),
        ("Which enzyme relieves the supercoiling ahead of the fork?", "Topoisomerase", "Helicase", "Primase", "Ligase"),
        ("Why does DNA polymerase need a primer?", "It can only add to an existing 3′ end", "It needs RNA as template", "It binds only RNA", "It works backwards"),
    ], "Each enzyme fixes one problem: unwinding, supercoiling, starting, extending, joining")),
    ("BI-6.2.B", Q("bi-okazaki-count", MG, "A replication fork travels {{L}} kb on a eukaryotic chromosome, and lagging-strand fragments average {{f}} nucleotides. About how many Okazaki fragments are made on that stretch?",
        given={"L": {"pick": [10, 50, 100]}, "f": {"pick": [100, 200]}}, value="L*1000/f", tex="N",
        verify="solve(Eq(x*f, L*1000), x)[0]", explain="The leading strand is one continuous piece; the lagging strand needs a new primer every fragment")),
    ("BI-6.2.C", Q("bi-meselson-heavy-fraction", MG, "Cells with fully ¹⁵N DNA are moved to ¹⁴N medium for {{n}} generations. What fraction of DNA molecules is hybrid (¹⁵N/¹⁴N)?",
        given={"n": {"pick": [1, 2, 3, 4]}}, value="2/2^n", tex="f", verify="2/Integer(2)**n",
        explain="Semiconservative: the two original strands end up in two hybrid molecules out of 2ⁿ")),
    ("BI-6.3.A", facts("bi-strand-identify", MG, [
        ("An mRNA reads 5′-AUG GCU-3′. What does the coding strand of DNA read?", "5′-ATG GCT-3′", "3′-TAC CGA-5′ as the coding strand", "5′-UAC CGA-3′", "5′-AGC GTA-3′"),
        ("Which DNA strand does RNA polymerase read?", "The template strand, 3′ to 5′", "The coding strand", "Both at once", "Neither"),
        ("RNA polymerase builds mRNA in which direction?", "5′ to 3′", "3′ to 5′", "Both", "Middle outward"),
    ], "mRNA matches the coding strand (with U for T) and is complementary to the template")),
    ("BI-6.3.B", Q("bi-splice-variants", MG, "A gene has {{n}} internal exons, each of which can be kept or skipped independently, plus fixed first and last exons. How many different mRNAs can alternative splicing make?",
        given={"n": {"pick": [2, 3, 5]}}, value="2^n", tex="N", final=True, verify="Integer(2)**n",
        explain="One gene, many proteins: humans have about 20 000 genes but far more proteins")),
    ("BI-6.4.A", Q("bi-codons-for-protein", MG, "A protein has {{n}} amino acids. How many nucleotides does its mRNA coding region contain, including the stop codon?",
        given={"n": {"pick": [100, 300, 1200]}}, value="3*(n + 1)", tex="N_{nt}", final=True, verify="3*n + 3",
        explain="Three nucleotides per codon, plus one stop codon that codes for no amino acid")),
    ("BI-6.4.B", facts("bi-ribosome-site-scenario", MG, [
        ("A new tRNA carrying an amino acid enters which site?", "A site", "P site", "E site", "Nucleus"),
        ("The tRNA holding the growing chain sits in which site?", "P site", "A site", "E site", "Golgi"),
        ("A stop codon reaches the A site. What binds?", "A release factor", "A tRNA", "DNA polymerase", "A primer"),
    ], "Aminoacyl in at A, chain held at P, empty tRNA out at E")),
    ("BI-6.5.A", facts("bi-epigenetic-predict", MG, [
        ("A drug blocks histone deacetylases. What happens to many genes?", "They become more active (chromatin stays open)", "They are silenced", "They are deleted", "No effect"),
        ("A promoter becomes heavily methylated. What usually happens?", "The gene is silenced", "The gene is overexpressed", "The gene is mutated", "Nothing"),
        ("Why can identical twins differ in disease risk?", "Epigenetic marks change with environment", "Their DNA sequences differ", "They have different chromosomes", "They cannot differ"),
    ], "Acetylation opens chromatin; methylation of DNA tends to close it")),
    ("BI-6.5.B", facts("bi-operon-scenario", MG, [
        ("A lac repressor that cannot bind lactose (allolactose). What happens?", "The lac genes stay off even with lactose present", "They are always on", "They turn on without lactose", "No change"),
        ("The lac operator is mutated so the repressor cannot bind. What happens?", "The lac genes are on all the time", "They are always off", "Only on without lactose", "No change"),
        ("High tryptophan in a cell does what to the trp operon?", "Turns it off (trp activates the repressor)", "Turns it on", "Deletes it", "Nothing"),
    ], "Inducible: repressor removed by inducer; repressible: repressor activated by corepressor")),
    ("BI-6.6.A", Q("bi-tf-combinations", MG, "A cell can express any combination of {{n}} different activator proteins at an enhancer. How many distinct combinations (including none) are possible?",
        given={"n": {"pick": [3, 5, 10]}}, value="2^n", tex="N", final=True, verify="summation(binomial(n, Symbol('k')), (Symbol('k'), 0, n))",
        explain="Combinatorial control: a few factors give many distinct expression patterns")),
    ("BI-6.6.B", facts("bi-differentiation-scenario", MG, [
        ("A liver cell and a neuron from one person have what in common?", "The same genome", "The same expressed genes", "The same proteins", "Nothing"),
        ("Why does a liver cell make albumin but a neuron does not?", "Different transcription factors are active", "The neuron lacks the gene", "Albumin is made in the nucleus", "Random chance"),
        ("Cloning Dolly from an udder cell showed what?", "Differentiated cells keep the full genome", "Cells lose genes when they specialise", "DNA changes in every tissue", "Only embryos have genomes"),
    ], "Cell types differ by which genes they express, not which genes they have")),
    ("BI-6.7.A", facts("bi-mutation-predict", MG, [
        ("A single base is deleted near the start of a gene. Which outcome is most likely?", "A frameshift that garbles the rest of the protein", "A silent change", "One amino acid changed", "A longer normal protein"),
        ("A codon changes from UAC (Tyr) to UAA. What kind of mutation?", "Nonsense", "Missense", "Silent", "Frameshift"),
        ("A codon changes from CUU to CUC (both Leu). What kind?", "Silent", "Missense", "Nonsense", "Frameshift"),
        ("Three bases are deleted in a row. What happens to the reading frame?", "It is kept; one amino acid is lost", "It shifts", "It stops at once", "It doubles"),
    ], "Deletions or insertions not in multiples of three shift the frame")),
    ("BI-6.7.B", facts("bi-genotype-phenotype", MG, [
        ("In sickle-cell anaemia, which change starts the chain of effects?", "Glu → Val at position 6 of β-globin", "A missing chromosome", "A change in the cell membrane lipids", "A virus"),
        ("Why do heterozygotes for sickle cell survive malaria better?", "Their red cells are a poorer host for the parasite", "They have no hemoglobin", "They are immune to all disease", "They make more red cells"),
        ("Cystic fibrosis comes from a faulty chloride channel. What is the visible result?", "Thick mucus in lungs and gut", "Short stature", "Blue skin", "Extra fingers"),
    ], "Genotype → protein change → cell change → phenotype")),
    ("BI-6.7.C", facts("bi-variation-source-scenario", MG, [
        ("A bacterium picks up a resistance plasmid from another species. What process?", "Horizontal gene transfer", "Mutation", "Meiosis", "Natural selection"),
        ("Two flu strains infect one cell and swap segments. What results?", "A new reassortant strain", "Identical strains", "No virus", "A bacterium"),
        ("Why do RNA viruses mutate fast?", "Their polymerases lack proofreading", "They have no genome", "They use DNA", "They are huge"),
    ], "Mutation, gene transfer and recombination supply the variation selection acts on")),
    ("BI-6.8.B", Q("bi-pcr-cycles-needed", MG, "PCR doubles the target each cycle. How many cycles does it take to turn {{n0}} copies into at least {{N}} copies?",
        given={"n0": {"pick": [1, 10, 100]}, "N": {"pick": [10**6, 10**9]}}, value="ceil(log(N/n0)/log(2))", tex="n", final=True,
        verify="ceiling(log(Rational(N, n0), 2))", explain="About 30 cycles turn a single molecule into a billion copies")),
    ("BI-6.8.C", facts("bi-cloning-scenario", MG, [
        ("After transformation, bacteria are grown on ampicillin. Why?", "Only cells that took up the plasmid (with its resistance gene) survive", "To kill all bacteria", "To cut the DNA", "To make proteins"),
        ("Why cut the gene and plasmid with the same restriction enzyme?", "Their sticky ends match and can be ligated", "It makes the DNA longer", "It kills bacteria", "It is cheaper"),
        ("Which enzyme seals the gene into the plasmid?", "DNA ligase", "Restriction enzyme", "Helicase", "RNA polymerase"),
    ], "Cut, paste, transform, select")),
    # ── unit 7 evolution ─────────────────────────────────────────────────
    ("BI-7.1.A", facts("bi-selection-missing", EVO, [
        ("A population of clones is exposed to a toxin. Why can't it evolve resistance by selection?", "There is no heritable variation", "There is no overproduction", "There is no environment", "It can"),
        ("A trait varies but is caused entirely by diet. Can selection change it across generations?", "No: the variation is not heritable", "Yes, always", "Only in plants", "Only in bacteria"),
        ("Which is required for natural selection?", "Heritable variation that affects reproduction", "Individuals changing during life", "A large population only", "Mutation on demand"),
    ], "Selection needs variation, inheritance, overproduction and differential success")),
    ("BI-7.1.B", Q("bi-fitness-ratio", EVO, "Genotype A leaves on average {{a}} surviving offspring and genotype B leaves {{b}}. What is B's relative fitness, with the best genotype set to 1?",
        given={"a": {"pick": [2, 3, 4]}, "b": {"pick": [1, 1.5, 3]}}, value="b/max(a, b)", tex="w_B",
        verify="nsimplify(b)/Max(nsimplify(a), nsimplify(b))", explain="Fitness is relative reproductive success, not strength or lifespan")),
    ("BI-7.2.A", facts("bi-selection-type-scenario", EVO, [
        ("Human birth weights cluster near the middle, with extremes surviving less. What selection?", "Stabilising", "Directional", "Disruptive", "Sexual"),
        ("Finches with large or small beaks do better than medium ones. What selection?", "Disruptive", "Stabilising", "Directional", "None"),
        ("Bacteria shift toward higher antibiotic resistance each generation. What selection?", "Directional", "Stabilising", "Disruptive", "Balancing"),
    ], "Which part of the distribution does better decides the type")),
    ("BI-7.3.A", facts("bi-human-selection", EVO, [
        ("Cabbage, broccoli and kale came from one wild mustard. How?", "Artificial selection on different traits", "Natural selection in the wild", "Genetic drift", "Mutation alone"),
        ("Fishing that removes the largest fish leads to what?", "Populations maturing at smaller sizes", "Bigger fish", "No change", "More species"),
        ("Overusing antibiotics does what to bacteria?", "Selects for resistant strains", "Makes them weaker", "Has no effect", "Kills all strains forever"),
    ], "Humans act as a selective agent, on purpose or not")),
    ("BI-7.3.B", facts("bi-analogy-homology", EVO, [
        ("Bird and bat wings evolved separately for flight. What are they as wings?", "Analogous (convergent)", "Homologous", "Vestigial", "Identical genes"),
        ("Sharks and dolphins have similar streamlined bodies. Why?", "Similar selection in water", "Close common ancestry", "Drift", "They are fish"),
        ("A human arm and a whale flipper share bones. What are they?", "Homologous", "Analogous", "Convergent", "Vestigial"),
    ], "Convergent traits share function, not ancestry")),
    ("BI-7.4.A", facts("bi-drift-scenario", EVO, [
        ("A storm kills 90% of a population at random. What is this?", "A bottleneck", "Founder effect", "Gene flow", "Natural selection"),
        ("A few birds colonise an island and carry a rare allele common in their descendants. What is this?", "Founder effect", "Bottleneck", "Gene flow", "Mutation"),
        ("Pollen blows in from another population. What is this?", "Gene flow", "Drift", "Selection", "Mutation"),
    ], "Drift is chance; gene flow is migration")),
    ("BI-7.4.B", Q("bi-drift-loss", EVO, "A neutral allele has frequency {{p}}. In a small population, what is the probability that drift eventually fixes it (equal to its current frequency)?",
        given={"p": {"pick": [0.05, 0.2, 0.5]}}, value="p", tex="P_{fix}", verify="1 - (1 - nsimplify(p))",
        explain="Drift is unbiased for neutral alleles, so the chance of fixation equals the frequency; it acts faster in small populations")),
    ("BI-7.4.C", Q("bi-gene-flow-mix", EVO, "An island population with allele frequency {{p0}} receives migrants so that {{m}}% of each generation's breeders come from the mainland (frequency {{pm}}). What is the frequency after one generation?",
        given={"p0": {"pick": [0.1, 0.8]}, "m": {"pick": [5, 10, 20]}, "pm": {"pick": [0.5, 0.3]}}, value="(1 - m/100)*p0 + m/100*pm", tex="p_1",
        verify="nsimplify(p0) + Rational(m, 100)*(nsimplify(pm) - nsimplify(p0))", explain="Gene flow pulls populations toward each other")),
    ("BI-7.5.A", Q("bi-hw-carriers", EVO, "A recessive disease affects 1 in {{n}} people. If the population is in Hardy–Weinberg equilibrium, what fraction are carriers?",
        given={"n": {"pick": [2500, 10000, 100]}}, value="2*sqrt(1/n)*(1 - sqrt(1/n))", tex="2pq",
        verify="2*(1 - sqrt(Rational(1, n)))*sqrt(Rational(1, n))", explain="q = √(q²); carriers far outnumber affected people when q is small")),
    ("BI-7.5.B", facts("bi-hw-violation", EVO, [
        ("Peahens prefer males with large tails. Which HW condition is broken?", "Random mating", "No mutation", "Large population", "No gene flow"),
        ("A small island population of 20 deer. Which condition is broken?", "Large population (drift acts)", "Random mating", "No selection", "No mutation"),
        ("Moths with dark wings survive better on soot. Which condition is broken?", "No natural selection", "No gene flow", "Random mating", "Large population"),
    ], "Each broken condition is a mechanism of evolution")),
    ("BI-7.6.A", facts("bi-evidence-type", EVO, [
        ("Whales have tiny hip bones. What kind of evidence?", "Vestigial structures (anatomy)", "Biogeography", "Fossil only", "Molecular"),
        ("Island species resemble those on the nearest mainland. What kind?", "Biogeography", "Embryology", "Vestigial structures", "Molecular"),
        ("Humans and chimps share about 98% of DNA sequence. What kind?", "Molecular", "Fossil", "Anatomical", "Behavioural"),
    ], "Fossils, anatomy, embryology, biogeography and molecules agree")),
    ("BI-7.7.A", facts("bi-universal-feature-identify", EVO, [
        ("Which feature is shared by every living cell?", "DNA genome and a nearly universal genetic code", "A nucleus", "Mitochondria", "Cell walls"),
        ("Which pathway is found in nearly all organisms?", "Glycolysis", "Photosynthesis", "The Calvin cycle", "Fermentation to ethanol"),
        ("All cells use which molecule as energy currency?", "ATP", "Glucose only", "Starch", "Creatine"),
    ], "Universal features are best explained by one shared ancestor")),
    ("BI-7.7.B", facts("bi-eukaryote-shared", EVO, [
        ("Which feature is shared by all eukaryotes but not prokaryotes?", "Membrane-bound nucleus", "Ribosomes", "DNA", "Plasma membrane"),
        ("Linear chromosomes and introns appear in which group?", "Eukaryotes", "Bacteria only", "All prokaryotes", "Viruses only"),
        ("A cytoskeleton of microtubules and actin is characteristic of what?", "Eukaryotes", "Only animals", "Only plants", "Bacteria"),
    ], "Shared eukaryotic features point to a common eukaryotic ancestor")),
    ("BI-7.8.A", facts("bi-ongoing-example", EVO, [
        ("Bedbugs became resistant to common insecticides within decades. What does this show?", "Evolution observed in real time", "Insecticides cause mutations on demand", "Bedbugs adapt by learning", "Nothing"),
        ("HIV evolves drug resistance within a patient. Why is combination therapy used?", "Resistance to several drugs at once is far less likely", "One drug is too weak", "It is cheaper", "Viruses cannot evolve"),
        ("Why do flu vaccines change yearly?", "The virus's surface proteins evolve", "The vaccine expires", "People change", "Flu is new each year"),
    ], "Short generations and strong selection make evolution visible")),
    ("BI-7.9.A", facts("bi-molecular-preferred", EVO, [
        ("Two animals look alike but their DNA differs a lot. Which evidence is preferred for relatedness?", "The DNA sequence data", "The appearance", "Both equally", "Neither"),
        ("Why can morphology mislead about relatedness?", "Convergent evolution makes unrelated species look alike", "It never misleads", "Morphology is not inherited", "Fossils are always wrong"),
        ("Fewer amino acid differences in cytochrome c between two species means what?", "More recent common ancestor", "More distant ancestor", "No relation", "Faster mutation"),
    ], "Molecules carry many independent characters, so they outweigh a few look-alike traits")),
    ("BI-7.9.B", facts("bi-tree-reading", EVO, [
        ("On a tree, which taxa are sister groups?", "The two that share a node no other taxon shares", "Any two at the tips", "The two tips drawn closest together", "The two oldest"),
        ("A trait appears at a node and is kept by all descendants. What is it for that clade?", "A shared derived character", "An outgroup trait", "Convergent", "Ancestral to all life"),
        ("Rotating branches around a node changes what?", "Nothing about relationships", "Who is related to whom", "The root", "Divergence times"),
    ], "Read relationships from the nodes, not from the order of the tips")),
    ("BI-7.9.C", Q("bi-tree-count", EVO, "How many distinct rooted, bifurcating trees are possible for {{n}} taxa? ((2n − 3)!!)",
        given={"n": {"pick": [3, 4, 5, 6]}}, value="factorial(2*n - 2)/(2^(n - 1)*factorial(n - 1))", tex="N", final=True,
        verify="binomial(2*n - 2, n - 1)*factorial(n - 1)/Integer(2)**(n - 1)", explain="Possible trees explode with taxa, which is why parsimony needs search, not listing")),
    ("BI-7.10.A", facts("bi-speciation-scenario", EVO, [
        ("A canyon splits a squirrel population, and the two sides diverge. What kind of speciation?", "Allopatric", "Sympatric", "None", "Hybridisation"),
        ("A plant becomes tetraploid and cannot breed with its diploid parents. What kind?", "Sympatric (polyploidy)", "Allopatric", "Geographic", "Not speciation"),
        ("Two populations look different but mate and have fertile offspring. Are they separate biological species?", "No", "Yes", "Only if they live apart", "Only if they look alike"),
    ], "The biological species concept turns on reproductive isolation")),
    ("BI-7.10.B", facts("bi-tempo-scenario", EVO, [
        ("Fossils show long stasis broken by quick change. Which model?", "Punctuated equilibrium", "Gradualism", "Lamarckism", "Steady state"),
        ("Many new mammal groups appeared after the dinosaurs died out. What is this?", "Adaptive radiation", "Convergence", "Stasis", "Bottleneck"),
        ("Small changes accumulating steadily over long times. Which model?", "Gradualism", "Punctuated equilibrium", "Saltation", "Radiation"),
    ], "Rates vary: open niches can drive bursts")),
    ("BI-7.10.C", facts("bi-barrier-classify", EVO, [
        ("A horse and donkey produce a sterile mule. What barrier?", "Postzygotic: hybrid sterility", "Prezygotic: temporal", "Prezygotic: habitat", "No barrier"),
        ("Two frog species breed in different months. What barrier?", "Prezygotic: temporal isolation", "Postzygotic", "Mechanical", "Gametic"),
        ("Sperm of one sea urchin species cannot fertilise eggs of another. What barrier?", "Prezygotic: gametic isolation", "Postzygotic", "Behavioural", "Habitat"),
    ], "Before or after a zygote forms decides the class")),
    ("BI-7.11.A", facts("bi-extinction-risk", EVO, [
        ("Which species is most at risk of extinction?", "A small population with low genetic diversity and a narrow niche", "A widespread generalist", "A species with many populations", "A fast-breeding pest"),
        ("Why is low genetic diversity dangerous?", "Fewer variants to cope with new diseases or change", "It speeds evolution", "It has no effect", "It increases population size"),
        ("Which is a driver of extinction?", "Habitat loss", "Gene flow", "Large population size", "Many offspring"),
    ], "Small, uniform, specialised populations are most vulnerable")),
    ("BI-7.11.B", facts("bi-rate-of-change", EVO, [
        ("Why does rapid climate change raise extinction risk more than slow change?", "Populations have less time to adapt or move", "Fast change helps adaptation", "Rate does not matter", "It reduces competition"),
        ("Long-lived species with long generations are hit hardest by fast change. Why?", "Selection acts per generation, so they adapt slowly", "They have more mutations", "They move faster", "They are immune"),
        ("How do current extinction rates compare with the background rate?", "Many times higher", "Lower", "About the same", "Unknown"),
    ], "Adaptation runs on generations; fast change outruns it")),
    ("BI-7.13.A", facts("bi-origin-evidence", EVO, [
        ("Miller and Urey made amino acids from simple gases and sparks. What did that show?", "Organic monomers can form without life", "Life arose in a flask", "Proteins came first", "DNA formed spontaneously"),
        ("Why is the RNA world hypothesis attractive?", "RNA can both store information and catalyse reactions", "RNA is a protein", "DNA came first", "RNA cannot replicate"),
        ("Lipids in water form vesicles on their own. Why does that matter?", "It suggests how early cell-like compartments formed", "It proves life is lipid", "It makes DNA", "It is irrelevant"),
    ], "Monomers, polymers, replicators and compartments each have experimental support")),
    # ── unit 8 ecology ───────────────────────────────────────────────────
    ("BI-8.1.B", facts("bi-behavior-scenario", ECO, [
        ("Honeybees dance to tell nestmates where food is. What does this signal do?", "Raises the colony's foraging success", "Attracts predators", "Defends territory", "Nothing"),
        ("A ground squirrel gives an alarm call that puts it at risk. Why can this be favoured?", "It helps relatives who share its genes (kin selection)", "It never helps", "It attracts mates only", "It confuses predators always"),
        ("Pheromones are an example of what kind of signal?", "Chemical", "Visual", "Auditory", "Tactile"),
    ], "Communication and cooperation evolve when they raise inclusive fitness")),
    ("BI-8.2.A", Q("bi-metabolic-scaling", ECO, "Whole-animal metabolic rate scales roughly as M^0.75. By what factor does metabolic rate per gram change when body mass rises {{f}}-fold?",
        given={"f": {"pick": [10, 100, 10000]}}, value="f^(-0.25)", tex="\\text{ratio}",
        verify="(nsimplify(f)*Symbol('M'))**Rational(3, 4)/(nsimplify(f)*Symbol('M'))/(Symbol('M')**Rational(3, 4)/Symbol('M'))", explain="Small endotherms burn far more energy per gram, partly because of their high SA/V")),
    ("BI-8.2.B", facts("bi-energy-change", ECO, [
        ("A drought cuts primary production in half. What happens to top predators?", "Their numbers fall most, since energy shrinks up every level", "They increase", "No change", "Only producers are affected"),
        ("Light reaching a lake rises after trees are cut. What happens first?", "Algae and producers increase", "Fish decline", "Nothing", "Decomposers vanish"),
        ("Why can't a food chain have dozens of levels?", "Too little energy remains after each transfer", "Predators are too large", "Producers die", "There is no limit"),
    ], "Energy input sets how much life and how many levels an ecosystem supports")),
    ("BI-8.2.C", Q("bi-producer-needed", ECO, "With {{e}}% transfer between levels, how much primary production, in kJ, supports {{t}} kJ at the {{lev}}?",
        cases=[{"lev": "secondary consumer level", "k": 2}, {"lev": "tertiary consumer level", "k": 3}], given={"e": {"pick": [10, 5]}, "t": {"pick": [10, 100]}},
        value="t/(e/100)^k", tex="E_0", verify="solve(Eq(x*Rational(e, 100)**k, t), x)[0]", explain="Divide by the efficiency once per step down the pyramid")),
    ("BI-8.2.D", facts("bi-cycle-scenario", ECO, [
        ("Which organisms turn atmospheric N₂ into ammonia?", "Nitrogen-fixing bacteria", "Plants directly", "Animals", "Fungi only"),
        ("Phosphorus differs from carbon and nitrogen in having no what?", "Major atmospheric reservoir", "Biological role", "Rock reservoir", "Ocean store"),
        ("Burning fossil fuels moves carbon from where to where?", "From rock reservoirs to the atmosphere", "From air to rocks", "From oceans to rocks", "Nowhere"),
        ("Denitrifying bacteria return nitrogen to where?", "The atmosphere as N₂", "Rocks", "Plants as protein", "Animals"),
    ], "Each element cycles through living and non-living stores at different rates")),
    ("BI-8.3.A", Q("bi-population-after-year", ECO, "A population of {{N}} has a per-capita birth rate of {{b}} and death rate of {{d}} per year. What is its size after one year (discrete)?",
        given={"N": {"pick": [500, 1000, 2000]}, "b": {"pick": [0.3, 0.2]}, "d": {"pick": [0.1, 0.25]}}, value="N*(1 + b - d)", tex="N_1",
        verify="N + N*nsimplify(b) - N*nsimplify(d)", explain="r = b − d; a negative r means decline")),
    ("BI-8.3.B", Q("bi-doubling-time", ECO, "A population grows exponentially with r = {{r}} per year. How long does it take to double, in years?",
        given={"r": {"pick": [0.02, 0.05, 0.1, 0.7]}}, value="log(2)/r", tex="t_d", verify="1/nsimplify(r)*log(2)",
        explain="About 70/r% years: at 2% a year, 35 years")),
    ("BI-8.4.A", Q("bi-logistic-max-rate", ECO, "A logistic population has K = {{K}} and r_max = {{r}} per year. At what population size is growth fastest, and what is that rate (individuals per year)? Give the rate.",
        given={"K": {"pick": [500, 1000, 5000]}, "r": {"pick": [0.1, 0.5, 1]}}, value="r*K/4", tex="(dN/dt)_{max}",
        verify="nsimplify(r)*Symbol('n')*(K - Symbol('n'))/K".replace("Symbol('n')", "(K/Integer(2))"), explain="Growth peaks at N = K/2, where it is r_maxK/4")),
    ("BI-8.4.B", facts("bi-limiting-scenario", ECO, [
        ("A disease spreads faster in crowded populations. What kind of limit?", "Density-dependent", "Density-independent", "Neither", "Abiotic only"),
        ("A hurricane kills 40% of a population regardless of its size. What kind?", "Density-independent", "Density-dependent", "Competition", "Predation"),
        ("Competition for nest sites grows as the population grows. What kind?", "Density-dependent", "Density-independent", "Random", "None"),
    ], "Density-dependent factors tighten as the population grows, giving regulation toward K")),
    ("BI-8.5.A", Q("bi-simpson-two", ECO, "A community has two species with {{a}} and {{b}} individuals. What is Simpson's diversity index 1 − Σ(n/N)²?",
        given={"a": {"pick": [10, 50, 90]}, "b": {"pick": [10, 50]}}, value="1 - (a/(a + b))^2 - (b/(a + b))^2", tex="D",
        verify="2*a*b/(a + b)**2", explain="Maximum (0.5 for two species) when they are equally common")),
    ("BI-8.5.B", facts("bi-interaction-scenario", ECO, [
        ("Clownfish shelter in anemones and keep them clean. What interaction?", "Mutualism (+/+)", "Commensalism", "Parasitism", "Competition"),
        ("Barnacles ride on a whale without affecting it. What interaction?", "Commensalism (+/0)", "Mutualism", "Parasitism", "Predation"),
        ("A tapeworm lives in a host's gut. What interaction?", "Parasitism (+/−)", "Mutualism", "Commensalism", "Competition"),
        ("Two bird species eat the same seeds. What interaction?", "Competition (−/−)", "Mutualism", "Predation", "Commensalism"),
    ], "Score each partner +, − or 0")),
    ("BI-8.5.C", facts("bi-community-scenario", ECO, [
        ("In a lynx–hare cycle, which population peaks first?", "The hares", "The lynx", "Both together", "Neither"),
        ("Two paramecium species grown together: one dies out. What principle?", "Competitive exclusion", "Mutualism", "Resource partitioning", "Succession"),
        ("Warblers feed in different parts of the same tree. What is this?", "Resource partitioning", "Competitive exclusion", "Predation", "Commensalism"),
    ], "Predators lag prey; species with identical niches cannot coexist, so they split resources")),
    ("BI-8.5.D", facts("bi-succession-scenario", ECO, [
        ("A lava flow cools to bare rock. Which succession follows?", "Primary", "Secondary", "None", "Tertiary"),
        ("A forest regrows after a fire, with soil intact. Which succession?", "Secondary", "Primary", "None", "Climax only"),
        ("What are usually the first colonisers of bare rock?", "Lichens and mosses", "Oak trees", "Grazing mammals", "Shrubs"),
    ], "Primary starts without soil; secondary starts with it")),
    ("BI-8.6.A", facts("bi-diversity-resilience", ECO, [
        ("Why is a diverse grassland more stable through drought?", "Some species tolerate drought and keep production going", "Diverse systems use no water", "Drought cannot affect them", "They have fewer species"),
        ("A monoculture crop is hit by one pest. Why is damage severe?", "Every plant is equally susceptible", "Pests prefer diversity", "Crops are immune", "Weather"),
        ("Functional redundancy means what?", "Several species can fill the same role", "One species fills many roles", "No species fill roles", "Species never overlap"),
    ], "More species means more ways for function to survive a disturbance")),
    ("BI-8.6.B", facts("bi-keystone-scenario", ECO, [
        ("Sea otters are removed from a kelp forest. What follows?", "Urchins boom and kelp collapses", "Kelp grows more", "No change", "Urchins vanish"),
        ("Wolves returned to Yellowstone. What happened to riverside willows?", "They recovered as elk grazing pressure fell", "They died off", "No change", "They moved upstream"),
        ("Removing the main producer from a system does what?", "Collapses the food web above it", "Helps consumers", "Has no effect", "Adds energy"),
    ], "Keystone species have effects far larger than their numbers")),
    ("BI-8.7.A", facts("bi-preexisting-variation", ECO, [
        ("Some bacteria survive an antibiotic. When did their resistance arise?", "Before the drug, by chance mutation", "Because of the drug", "During treatment on demand", "Never"),
        ("Dark peppered moths increased during industrial pollution. Where did the dark form come from?", "It already existed at low frequency", "Soot caused it", "Moths chose it", "It was introduced"),
        ("Why can a population adapt to a sudden change at all?", "Variation already present lets some survive", "Individuals change their genes", "Environment creates new genes", "It cannot"),
    ], "Environment selects among variants; it does not create them")),
    ("BI-8.7.B", facts("bi-invasive-scenario", ECO, [
        ("Why do invasive species often spread fast?", "They escape their natural predators and diseases", "They are always larger", "They need no resources", "Native species help them"),
        ("Cane toads in Australia poison native predators. What is the effect?", "Native predator populations decline", "Predators thrive", "No effect", "Toads decline at once"),
        ("Zebra mussels filter huge volumes of water. What happens to native plankton feeders?", "They lose food", "They gain food", "No change", "They become mussels"),
    ], "Without coevolved checks, invaders outcompete or prey on natives")),
    ("BI-8.7.C", Q("bi-biomagnification", ECO, "A toxin concentrates {{f}}-fold at each step up a food chain. If water holds {{c}} ppb, what concentration, in ppb, reaches the {{n}}th trophic level (producers are level 1)?",
        given={"f": {"pick": [5, 10]}, "c": {"pick": [0.001, 0.01]}, "n": {"pick": [3, 4]}}, value="c*f^n", tex="C_n", verify="nsimplify(c)*exp(n*log(f))",
        explain="Persistent fat-soluble toxins like DDT and mercury build up most in top predators")),
    ("BI-8.7.D", facts("bi-disturbance-scenario", ECO, [
        ("A volcanic eruption blankets a region in ash. What can follow globally?", "Short-term cooling from blocked sunlight", "Warming", "No effect", "More photosynthesis at once"),
        ("El Niño warms Pacific surface waters. What happens to upwelling-fed fisheries?", "They decline as nutrients drop", "They boom", "No change", "They move inland"),
        ("A flood deposits new sediment on a river plain. What can follow?", "Secondary succession on fertile soil", "Primary succession on rock", "Nothing", "Desertification"),
    ], "Geological and weather events reset and reshape ecosystems")),
    # ── unit 9 physiology ────────────────────────────────────────────────
    ("BI-9.1.A", facts("bi-action-potential-predict", PHY, [
        ("Tetrodotoxin blocks voltage-gated Na⁺ channels. What happens?", "No action potentials fire", "Neurons fire continuously", "Resting potential reverses", "Myelin dissolves"),
        ("Why does a myelinated axon conduct faster?", "The signal jumps between nodes (saltatory conduction)", "It has more Na⁺", "It is shorter", "It uses no ions"),
        ("Which ion rushes in during depolarisation?", "Na⁺", "K⁺", "Cl⁻", "Ca²⁺ only"),
    ], "Na⁺ in to rise, K⁺ out to fall; myelin speeds the jump")),
    ("BI-9.2.A", facts("bi-hormone-scenario", PHY, [
        ("Which hormone acts within seconds through a second messenger?", "Epinephrine", "Cortisol", "Testosterone", "Estrogen"),
        ("Which hormone changes gene expression by binding an intracellular receptor?", "Cortisol", "Insulin", "Glucagon", "Epinephrine"),
        ("Why do steroid effects take hours?", "They work through transcription and new protein synthesis", "They travel slowly", "They are large proteins", "They need second messengers"),
    ], "Peptides act fast at the surface; steroids act slowly through genes")),
    ("BI-9.3.A", facts("bi-contraction-predict", PHY, [
        ("After death, muscles lock in rigor mortis. Why?", "No ATP to release myosin from actin", "Too much Ca²⁺ removal", "Myosin disappears", "Actin dissolves"),
        ("What does Ca²⁺ do to start contraction?", "Binds troponin and moves tropomyosin off actin's binding sites", "Binds myosin directly", "Makes ATP", "Breaks actin"),
        ("During contraction, what shortens?", "The sarcomere (filaments slide; they do not shorten)", "The actin filaments", "The myosin filaments", "Nothing"),
    ], "Ca²⁺ uncovers the sites; ATP powers and releases each cross-bridge")),
    ("BI-9.4.A", facts("bi-circulation-scenario", PHY, [
        ("Which vessels have the thickest muscular walls?", "Arteries", "Veins", "Capillaries", "Lymph vessels"),
        ("Which chamber pumps blood to the body?", "Left ventricle", "Right ventricle", "Left atrium", "Right atrium"),
        ("Why do veins have valves?", "Blood pressure is low, so valves stop backflow", "To raise pressure", "To exchange gases", "To filter blood"),
    ], "Pressure falls along the path; structures match the pressure they carry")),
    ("BI-9.4.B", facts("bi-bohr-predict", PHY, [
        ("Exercising muscle is warm, acidic and high in CO₂. What happens to O₂ unloading?", "It increases (curve shifts right)", "It decreases", "No change", "It stops"),
        ("At high altitude, 2,3-BPG rises in red cells. What does it do?", "Shifts the curve right, releasing more O₂ to tissues", "Shifts it left", "Removes hemoglobin", "Nothing"),
        ("Carbon monoxide binds hemoglobin tightly. What is the effect?", "Less O₂ carried and released", "More O₂ released", "No effect", "More CO₂ carried"),
    ], "Conditions in active tissue lower hemoglobin's O₂ affinity just where O₂ is needed")),
    ("BI-9.4.C", facts("bi-breathing-control", PHY, [
        ("What mainly drives the urge to breathe?", "Rising blood CO₂ (falling pH)", "Falling O₂", "Lung stretch only", "Heart rate"),
        ("Hyperventilating before diving is dangerous. Why?", "It lowers CO₂ so the urge to breathe comes too late", "It raises CO₂", "It fills lungs with water", "It stops the heart"),
        ("Where does gas exchange happen in the lungs?", "Alveoli", "Trachea", "Bronchi", "Diaphragm"),
    ], "Chemoreceptors watch CO₂ and pH more than O₂")),
    ("BI-9.5.A", facts("bi-immunity-classify", PHY, [
        ("Neutrophils engulf any bacterium at a wound. Which immunity?", "Innate", "Adaptive", "Humoral", "Passive"),
        ("A second exposure to measles triggers a fast, strong response. Which immunity?", "Adaptive, with memory", "Innate", "Neither", "Passive"),
        ("Antibodies passed through breast milk are what kind of immunity?", "Passive", "Innate", "Active", "Cell-mediated"),
    ], "Innate is fast and general; adaptive is specific and remembers")),
    ("BI-9.5.B", facts("bi-lymphocyte-scenario", PHY, [
        ("Which cells kill virus-infected body cells?", "Cytotoxic T cells", "B cells", "Plasma cells", "Red cells"),
        ("HIV destroys helper T cells. Why does that weaken both arms of immunity?", "Helper T cells activate both B cells and cytotoxic T cells", "They make antibodies", "They kill viruses directly", "They do not"),
        ("Why does a vaccine protect for years?", "Memory B and T cells persist", "Antibodies last forever", "The vaccine stays in the body", "It changes your genes"),
    ], "Helper T cells coordinate; B cells make antibodies; cytotoxic T cells kill infected cells")),
    ("BI-9.6.A", facts("bi-digestion-scenario", PHY, [
        ("A person lacks lactase. What happens after drinking milk?", "Undigested lactose is fermented by gut bacteria, causing gas", "Lactose is absorbed whole", "Proteins are not digested", "Fat is not absorbed"),
        ("Where does most nutrient absorption happen?", "Small intestine", "Stomach", "Large intestine", "Esophagus"),
        ("Bile does what to fats?", "Emulsifies them so lipase can act", "Digests them chemically", "Absorbs them", "Turns them into protein"),
    ], "Each class has its enzymes; the small intestine absorbs most products")),
    ("BI-9.7.A", facts("bi-cycle-hormones", PHY, [
        ("What triggers ovulation?", "A surge of LH", "A drop in estrogen", "Progesterone rising", "FSH falling to zero"),
        ("After ovulation, the corpus luteum secretes mainly what?", "Progesterone", "LH", "FSH", "Testosterone"),
        ("If no pregnancy occurs, why does menstruation start?", "The corpus luteum degenerates and progesterone falls", "LH rises", "Estrogen surges", "FSH stops"),
    ], "Rising estrogen flips to positive feedback for the LH surge; falling progesterone ends the cycle")),
    ("BI-9.7.B", Q("bi-gametes-per-meiosis", PHY, "Starting from {{n}} primary cells, how many functional gametes are produced by {{proc}}?",
        cases=[{"proc": "spermatogenesis", "k": 4}, {"proc": "oogenesis", "k": 1}], given={"n": {"pick": [10, 100]}}, value="n*k", tex="N", final=True,
        verify="n*k", explain="Oogenesis keeps the cytoplasm in one egg and discards polar bodies; spermatogenesis makes four sperm")),
    # ── unit 10 development and diversity ────────────────────────────────
    ("BI-10.1.A", Q("bi-cleavage-cells", DIV, "A zygote divides synchronously during cleavage. How many cells are there after {{n}} divisions?",
        given={"n": {"pick": [3, 5, 7]}}, value="2^n", tex="N", final=True, verify="Integer(2)**n",
        explain="Cleavage divides without growth, so cells get smaller each round until the blastula forms")),
    ("BI-10.1.B", facts("bi-germ-layer-scenario", DIV, [
        ("A defect in ectoderm would most affect which organ?", "Brain and spinal cord", "Heart", "Liver", "Lungs"),
        ("Muscle and bone come from which layer?", "Mesoderm", "Ectoderm", "Endoderm", "None"),
        ("The lining of the gut comes from which layer?", "Endoderm", "Mesoderm", "Ectoderm", "Mesoderm and ectoderm"),
    ], "Ectoderm: skin and nerves; mesoderm: muscle, bone, blood; endoderm: gut and its glands")),
    ("BI-10.2.A", facts("bi-development-control-scenario", DIV, [
        ("A fruit fly has legs where antennae should be. Which genes are involved?", "Homeotic (Hox) genes", "Housekeeping genes", "rRNA genes", "Mitochondrial genes"),
        ("Webbing between human fingers disappears before birth. How?", "Programmed cell death (apoptosis)", "Necrosis", "Cell fusion", "Infection"),
        ("One group of cells signals neighbours to become a lens. What is this?", "Induction", "Apoptosis", "Mutation", "Meiosis"),
    ], "Signals, master control genes and cell death shape the body")),
    ("BI-10.3.A", facts("bi-virus-scenario", DIV, [
        ("A phage's DNA joins the bacterial chromosome and is copied quietly. Which cycle?", "Lysogenic", "Lytic", "Retroviral only", "None"),
        ("HIV makes DNA from its RNA genome. Which enzyme does that?", "Reverse transcriptase", "DNA polymerase", "RNA polymerase", "Ligase"),
        ("Why are antibiotics useless against viruses?", "Viruses lack the bacterial structures antibiotics target", "Viruses are too big", "Antibiotics kill cells only", "Viruses are bacteria"),
    ], "Lytic kills fast; lysogenic hides; retroviruses reverse-transcribe")),
    ("BI-10.4.B", Q("bi-generation-time", DIV, "A bacterial culture grows from {{N0}} to {{N}} cells in {{t}} min by binary fission. What is the generation time, in min?",
        given={"N0": {"pick": [100, 1000]}, "N": {"pick": [12800, 102400]}, "t": {"pick": [140, 200]}}, value="t/(log(N/N0)/log(2))", tex="g",
        verify="t*log(2)/(log(N) - log(N0))", explain="Generations = log₂(N/N₀); divide the time by that")),
    ("BI-10.5.B", facts("bi-plant-innovation", DIV, [
        ("Which innovation let plants grow tall?", "Vascular tissue (xylem and phloem)", "Seeds", "Flowers", "Spores"),
        ("Which innovation freed plant fertilisation from water?", "Pollen and seeds", "Vascular tissue", "Leaves", "Roots"),
        ("In mosses, which generation is dominant?", "Gametophyte", "Sporophyte", "Both equal", "Neither"),
    ], "Bryophytes → ferns (vascular) → gymnosperms (seeds) → angiosperms (flowers, fruit)")),
    ("BI-10.5.C", facts("bi-body-plan-classify", DIV, [
        ("An animal has radial symmetry and two germ layers. What group?", "Cnidarians (jellyfish)", "Arthropods", "Chordates", "Annelids"),
        ("In which group does the blastopore become the anus?", "Deuterostomes (echinoderms, chordates)", "Protostomes", "Sponges", "Cnidarians"),
        ("Which animals lack true tissues?", "Sponges", "Cnidarians", "Flatworms", "Molluscs"),
    ], "Symmetry, germ layers, body cavity and the blastopore's fate sort the animals")),
]
