"""DAT Biology depth (Nov 2026): a second objective, with two question types, on every Biology subtopic of the
ADA DAT outline that rested on a single objective (see the ada-dat table in docs/coverage/standards.md).
OBJS lists the new objectives (code, outline item, do, ek); scripts/dat_objs.py writes them into dat.yaml.
Facts are standard introductory biology; numbers are recomputed by sympy along another route."""
from opl_dsl import Q

FILE, FRAMEWORK = "dat-bio-depth", "dat"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


OBJS = [
    ("DAT-1.1.M", "1.1.c", "Add free energies of coupled reactions and use ΔG = ΔG°′ + RT ln Q to decide whether a cellular step runs.",
     "ΔG values of coupled reactions add; ATP hydrolysis gives about −30.5 kJ/mol under standard conditions; a reaction with ΔG°′ > 0 can still run when Q is small."),
    ("DAT-1.1.N", "1.1.f", "Choose a microscope or stain for a cell-biology question and compute magnification and cell size.",
     "Total magnification = objective × eyepiece; light microscopes resolve about 0.2 µm, electron microscopes about 1 nm; cell size ≈ field diameter ÷ cells across it."),
    ("DAT-1.1.O", "1.1.g", "Identify a biomolecule from a chemical test and count the waters released when monomers polymerize.",
     "Benedict's: reducing sugars; biuret: peptide bonds; iodine: starch; Sudan/emulsion: lipids; n monomers joined by dehydration release n − 1 waters."),
    ("DAT-1.2.I", "1.2.a", "Distinguish viruses, viroids and prions and compute a phage titer from a plaque count.",
     "Viroids are naked RNA, prions misfolded protein; titer (PFU/mL) = plaques ÷ (dilution × volume plated)."),
    ("DAT-1.2.J", "1.2.b", "Match prokaryotic growth and habitats to Archaea or Bacteria and compute exponential growth from generation time.",
     "Extreme halophiles, methanogens and many thermophiles are archaea; N = N₀ · 2^(t/g) during log phase."),
    ("DAT-1.2.K", "1.2.d", "Place a fungus in its phylum and predict the effect of drugs or partnerships that act on fungal biology.",
     "Zygomycetes (bread mold), ascomycetes (yeast, sac), basidiomycetes (mushrooms, club); ergosterol in the membrane is the antifungal target; mycorrhizae and lichens are mutualisms."),
    ("DAT-1.2.L", "1.2.e", "Identify a protist by its locomotion, covering or disease and predict its physiology from its habitat.",
     "Amoebae: pseudopodia; Paramecium: cilia and a contractile vacuole; Euglena: flagellum and chloroplasts; diatoms: silica; Plasmodium (apicomplexan) causes malaria."),
    ("DAT-1.2.M", "1.2.f", "Relate plant tissues, transport and hormones to function and predict a plant's response to a stimulus.",
     "Xylem carries water up by transpiration pull; phloem moves sugar source to sink; auxin drives phototropism, gibberellin stem growth, abscisic acid stomatal closure, ethylene ripening; C4 and CAM limit photorespiration."),
    ("DAT-1.3.N", "1.3.a", "Identify skin cells, glands and layers and predict how skin responds to heat, cold and injury.",
     "Stratum basale divides; melanocytes make melanin; sebaceous glands oil hair, eccrine glands cool by sweat; vasodilation dumps heat, vasoconstriction keeps it."),
    ("DAT-1.3.O", "1.3.b", "Match bone and cartilage cells, tissue and joints to their roles.",
     "Osteocytes sit in lacunae of osteons (Haversian systems); red marrow makes blood cells; hyaline cartilage covers joints, fibrocartilage in discs, elastic in the ear; synovial joints move freely."),
    ("DAT-1.3.P", "1.3.c", "Compare skeletal, cardiac and smooth muscle and predict force from motor-unit recruitment and summation.",
     "Skeletal: striated, voluntary, multinucleate; cardiac: striated, intercalated discs, autorhythmic; smooth: unstriated, calmodulin; force rises by recruiting motor units and by summation to tetanus."),
    ("DAT-1.3.Q", "1.3.e", "Match antibody classes, antigen presentation and immunization type to the immune response they give.",
     "IgM first, IgG most abundant and crosses the placenta, IgA in secretions, IgE allergy; MHC I shows to CD8, MHC II to CD4; vaccines give active immunity, antibodies passed on give passive."),
    ("DAT-1.3.R", "1.3.f", "Match gut hormones and absorption sites to their actions and follow fat digestion and absorption.",
     "Gastrin raises acid; secretin brings bicarbonate; CCK releases bile and enzymes; most absorption in the small intestine, water and electrolytes also in the colon; fats leave as chylomicrons into lacteals."),
    ("DAT-1.3.S", "1.3.h", "Compute renal clearance from urine and plasma data and trace the renin–angiotensin–aldosterone response.",
     "Clearance = U × V̇ ÷ P; inulin clearance equals GFR; low pressure → renin → angiotensin II → aldosterone and vasoconstriction."),
    ("DAT-1.3.T", "1.3.k", "Trace gametes through the reproductive tracts and match pregnancy hormones to their roles.",
     "Sperm: seminiferous tubules → epididymis → vas deferens; fertilization in the oviduct; hCG keeps the corpus luteum; progesterone holds the endometrium; oxytocin drives labor."),
    ("DAT-1.4.M", "1.4.b", "Compute the risk that a child inherits a human single-gene disorder and match disorders to inheritance modes.",
     "Two carriers of an autosomal recessive: 1/4 affected, 2/3 of unaffected children are carriers; carrier mother of an X-linked recessive: 1/2 of sons affected."),
    ("DAT-1.4.N", "1.4.d", "Name the karyotype of common aneuploidies and count chromosomes and chromatids through the cell cycle.",
     "Down 47,+21; Turner 45,X; Klinefelter 47,XXY; a 2n cell has 2n chromosomes and 4n chromatids after S phase, n chromosomes with 2n chromatids after meiosis I."),
    ("DAT-1.4.O", "1.4.f", "Order early development and predict the outcome of a change in induction, Hox genes or apoptosis.",
     "Zygote → cleavage → morula → blastula (blastocyst) → gastrula; induction signals fate; Hox genes set body-axis identity; apoptosis sculpts digits."),
    ("DAT-1.4.P", "1.4.g", "Estimate how often a sequence occurs by chance in a genome and compare genome features across organisms.",
     "A specific n-base site appears about once every 4^n bases; prokaryotic genomes are compact with operons; eukaryotic genomes carry introns, repeats and much noncoding DNA."),
    ("DAT-1.4.Q", "1.4.i", "Predict Barr bodies and imprinted expression from a karyotype or parent of origin.",
     "Barr bodies = number of X chromosomes − 1; imprinted genes are expressed from one parent's copy only (Prader–Willi paternal loss, Angelman maternal loss of 15q11–13)."),
    ("DAT-1.5.I", "1.5.c", "Apply Hamilton's rule and classify social behaviors and communication signals.",
     "An altruistic gene spreads when r · B > C; full siblings r = 1/2, half siblings 1/4, cousins 1/8; pheromones, the honeybee waggle dance and territorial displays are signals."),
]

CELL, DIV, PHYS, MOLG, HER, EVO, ENER, MOL = ("bio.cells", "bio.diversity", "bio.physiology", "bio.molecular-genetics",
                                             "bio.heredity", "bio.evolution", "bio.energetics", "bio.molecules")

ADD = [
    # 1.1.M thermodynamics
    ("DAT-1.1.M", Q("dat-coupled-dg", ENER, "A cell couples a reaction with ΔG°′ = +{{g1}} kJ/mol to the hydrolysis of {{natp}} ATP (ΔG°′ = −30.5 kJ/mol each). What is ΔG°′ of the coupled reaction, in kJ/mol?",
        given={"g1": {"pick": [14.2, 16.7, 21.0, 33.0, 47.0]}, "natp": {"pick": [1, 2]}}, value="g1 - 30.5*natp", tex="\\Delta G",
        verify="solve(Eq(x + Rational(61, 2)*natp, nsimplify(g1)), x)[0]",
        explain="Free energies of coupled reactions add; a negative total means the coupled process is favourable")),
    ("DAT-1.1.M", Q("dat-dg-q", ENER, "A step has ΔG°′ = +{{g0}} kJ/mol. In the cell, Q = {{Qv}} at 310 K. What is ΔG, in kJ/mol? (R = 8.314 J/mol·K)",
        given={"g0": {"pick": [2, 5, 7.5]}, "Qv": {"pick": [0.001, 0.01, 0.05]}}, value="g0 + 8.314*310*log(Qv)/1000", tex="\\Delta G",
        verify="nsimplify(g0) + Rational(8314, 1000)*310*log(nsimplify(Qv))/1000",
        explain="ΔG = ΔG°′ + RT ln Q: keeping product low (small Q) pulls an uphill step forward")),
    # 1.1.N experimental
    ("DAT-1.1.N", Q("dat-cell-size", CELL, "Under a {{obj}}× objective and 10× eyepiece the field of view is {{fov}} µm across, and {{n}} cells laid end to end span it. About how long is one cell, in µm?",
        given={"obj": {"pick": [10, 40]}, "fov": {"pick": [400, 450, 1800, 2000]}, "n": {"pick": [8, 10, 20, 25]}}, value="fov/n", tex="L",
        verify="solve(Eq(x*n, fov), x)[0]", explain="Size = field diameter ÷ number of cells across it; total magnification here is the objective × 10")),
    ("DAT-1.1.N", facts("dat-scope-pick", CELL, [
        ("Which instrument shows the three-dimensional surface of a pollen grain at high resolution?", "Scanning electron microscope", "Transmission electron microscope", "Compound light microscope", "Phase-contrast microscope"),
        ("Which instrument shows ribosomes and the internal membranes of a mitochondrion in a thin section?", "Transmission electron microscope", "Scanning electron microscope", "Dissecting microscope", "Compound light microscope"),
        ("Which method watches unstained living cells move with good contrast?", "Phase-contrast light microscopy", "Transmission electron microscopy", "Scanning electron microscopy", "Gram staining"),
        ("Which method locates one tagged protein inside a living cell?", "Fluorescence microscopy with a GFP fusion", "Scanning electron microscopy", "Differential centrifugation", "Gel electrophoresis"),
    ], "Electron microscopes need fixed, dead samples (SEM surfaces, TEM sections); light methods keep cells alive")),
    # 1.1.O biomolecules
    ("DAT-1.1.O", Q("dat-dehydration-waters", MOL, "{{n}} {{mon}} are joined into one unbranched chain by dehydration synthesis. How many water molecules are released?",
        cases=[{"mon": "glucose units", "n": 12}, {"mon": "amino acids", "n": 150}, {"mon": "nucleotides", "n": 40}, {"mon": "amino acids", "n": 64}],
        value="n - 1", tex="N", final=True, verify="len(range(1, n))", explain="Each new bond releases one water, and a chain of n units has n − 1 bonds")),
    ("DAT-1.1.O", facts("dat-biomolecule-test", MOL, [
        ("A sample turns brick-red when heated with Benedict's reagent. What does it contain?", "A reducing sugar such as glucose", "Starch", "Protein", "Triglyceride"),
        ("A sample turns violet with biuret reagent. What does it contain?", "Protein (peptide bonds)", "Reducing sugar", "Starch", "Lipid"),
        ("A sample turns blue-black with iodine. What does it contain?", "Starch", "Glucose", "Protein", "DNA"),
        ("A sample leaves a translucent spot on paper and stains red with Sudan III. What does it contain?", "Lipid", "Starch", "Protein", "Sucrose"),
    ], "Sucrose is not a reducing sugar; iodine reports starch's amylose helix")),
    # 1.2.I viruses
    ("DAT-1.2.I", Q("dat-phage-titer", DIV, "{{vol}} mL of a 10⁻{{k}} dilution of a phage stock gives {{pl}} plaques. What is the titer of the stock, in PFU/mL?",
        given={"vol": {"pick": [0.1, 0.2]}, "k": {"pick": [6, 7, 8]}, "pl": {"pick": [45, 120, 230]}}, value="pl/(vol*10^(-k))", tex="\\text{titer}",
        verify="solve(Eq(x*nsimplify(vol)*Integer(10)**(-k), pl), x)[0]", explain="Titer = plaques ÷ (dilution × volume plated)")),
    ("DAT-1.2.I", facts("dat-acellular-agents", DIV, [
        ("An infectious agent survives nucleases and is a misfolded host protein. What is it?", "A prion", "A viroid", "A retrovirus", "A bacteriophage"),
        ("A plant pathogen is a short circular RNA with no capsid. What is it?", "A viroid", "A prion", "A plasmid", "A satellite bacterium"),
        ("A virus copies its RNA genome into DNA that integrates into the host chromosome. What enzyme does it carry?", "Reverse transcriptase", "RNA-dependent RNA polymerase only", "DNA ligase", "Restriction endonuclease"),
        ("Why do antibiotics not cure viral infections?", "Viruses lack the bacterial structures and enzymes antibiotics target", "Viruses are too large to absorb drugs", "Viruses have cell walls that block drugs", "Viruses replicate outside cells"),
    ], "Viruses are obligate intracellular parasites; prions carry no nucleic acid; viroids carry no protein")),
    # 1.2.J archaea / bacteria
    ("DAT-1.2.J", Q("dat-bacterial-growth", DIV, "A culture in log phase starts with {{N0}} cells and divides every {{g}} min. How many cells are there after {{t}} min?",
        given={"N0": {"pick": [100, 500, 1000]}, "g": {"pick": [20, 30]}, "t": {"pick": [60, 120, 180]}}, value="N0*2^(t/g)", tex="N", final=True,
        verify="N0*Integer(2)**Rational(t, g)", explain="N = N₀ · 2^(t/g): the number of generations is elapsed time ÷ generation time")),
    ("DAT-1.2.J", facts("dat-prokaryote-habitat", DIV, [
        ("A microbe makes methane in a cow's rumen. Which domain?", "Archaea", "Bacteria", "Eukarya", "It is a virus"),
        ("A cell grows in a salt evaporation pond at 25% NaCl and has ether-linked lipids. Which domain?", "Archaea", "Bacteria", "Eukarya", "Protista"),
        ("A cell has peptidoglycan in its wall and is killed by penicillin. Which domain?", "Bacteria", "Archaea", "Eukarya", "Fungi"),
        ("A nitrogen-fixing cell lives in root nodules of legumes. Which group?", "Bacteria (Rhizobium)", "Archaea", "Fungi", "Protista"),
    ], "Methanogens and extreme halophiles are archaea; peptidoglycan marks bacteria")),
    # 1.2.K fungi
    ("DAT-1.2.K", facts("dat-fungal-phylum", DIV, [
        ("A fungus forms spores in sac-like asci; baker's yeast belongs here. Which phylum?", "Ascomycota", "Basidiomycota", "Zygomycota", "Chytridiomycota"),
        ("A mushroom forms spores on club-shaped cells under its cap. Which phylum?", "Basidiomycota", "Ascomycota", "Zygomycota", "Chytridiomycota"),
        ("Black bread mold forms resistant zygosporangia. Which phylum?", "Zygomycota", "Ascomycota", "Basidiomycota", "Oomycota"),
        ("Which fungi have flagellated spores?", "Chytrids", "Basidiomycetes", "Ascomycetes", "Zygomycetes"),
    ], "Fungi are grouped by their sexual spore structure")),
    ("DAT-1.2.K", facts("dat-fungal-scenario", DIV, [
        ("An antifungal drug blocks ergosterol synthesis. What does it disrupt?", "The fungal cell membrane", "The fungal cell wall's chitin", "Fungal ribosomes", "Fungal DNA replication"),
        ("Pines grown in sterile soil lacking fungi grow poorly. Why?", "They lack mycorrhizae that supply phosphate and water", "The fungi fix nitrogen for them", "The fungi photosynthesize for them", "The fungi produce their auxin"),
        ("A lichen colonizes bare rock. What partners make it up?", "A fungus and a photosynthetic alga or cyanobacterium", "A fungus and a moss", "Two fungi", "A bacterium and a plant root"),
        ("Why does penicillin not kill fungi?", "Fungal walls are chitin, not peptidoglycan", "Fungi have no cell wall", "Fungi make penicillinase", "Fungi lack ribosomes"),
    ], "Ergosterol is to fungi what cholesterol is to animals; chitin, not peptidoglycan, stiffens the wall", pace="quick")),
    # 1.2.L protista
    ("DAT-1.2.L", facts("dat-protist-id", DIV, [
        ("A protist moves by pseudopodia and engulfs food by phagocytosis. What is it?", "Amoeba", "Paramecium", "Euglena", "Plasmodium"),
        ("A protist is covered in cilia and has a macronucleus and micronucleus. What is it?", "Paramecium", "Amoeba", "Diatom", "Trypanosoma"),
        ("A protist has a two-part silica shell and is a major marine photosynthesizer. What is it?", "Diatom", "Dinoflagellate", "Amoeba", "Paramecium"),
        ("A non-motile apicomplexan is carried by Anopheles mosquitoes. What is it?", "Plasmodium", "Giardia", "Trypanosoma", "Euglena"),
    ], "Protists are grouped by locomotion and covering in DAT questions")),
    ("DAT-1.2.L", facts("dat-protist-scenario", DIV, [
        ("A freshwater Paramecium is moved to seawater. What happens to its contractile vacuole?", "It pumps less often", "It pumps more often", "It bursts", "It begins photosynthesis"),
        ("Euglena is kept in the dark with organic nutrients. How does it feed?", "Heterotrophically, absorbing nutrients", "It dies at once", "By chemosynthesis", "By photosynthesis anyway"),
        ("A dinoflagellate bloom makes shellfish toxic. What is the bloom called?", "A red tide", "A lichen", "A plankton crash", "A mycorrhiza"),
        ("Why is malaria hard to treat with one drug?", "Plasmodium moves between liver and red-cell stages in the host", "Plasmodium is a bacterium", "Plasmodium has no ribosomes", "Plasmodium lives only in water"),
    ], "A contractile vacuole expels water gained by osmosis, so it slows when the outside is less dilute", pace="quick")),
    # 1.2.M plants
    ("DAT-1.2.M", facts("dat-plant-hormone", DIV, [
        ("A seedling bends toward a window. Which hormone moves to the shaded side?", "Auxin", "Gibberellin", "Abscisic acid", "Ethylene"),
        ("Leaves close their stomata during drought. Which hormone signals it?", "Abscisic acid", "Auxin", "Cytokinin", "Gibberellin"),
        ("A ripe banana speeds ripening of nearby fruit. Which hormone?", "Ethylene", "Auxin", "Abscisic acid", "Cytokinin"),
        ("A dwarf pea grows tall when sprayed. Which hormone?", "Gibberellin", "Ethylene", "Abscisic acid", "Auxin"),
    ], "Auxin: elongation and phototropism; gibberellin: stem growth, germination; ABA: dormancy, stomata; ethylene: ripening")),
    ("DAT-1.2.M", facts("dat-plant-transport", DIV, [
        ("Which tissue carries water from roots to leaves, and what drives it?", "Xylem, pulled by transpiration and water cohesion", "Phloem, pushed by root pressure only", "Xylem, pumped by companion cells", "Phloem, by transpiration"),
        ("Sugar moves from a leaf to a growing fruit. Through which tissue and by what?", "Phloem, by pressure flow from source to sink", "Xylem, by transpiration", "Phloem, by diffusion only", "Xylem, by capillarity"),
        ("A desert plant opens its stomata at night and stores CO₂ as malate. What pathway?", "CAM", "C4", "C3", "Photorespiration"),
        ("Which generation dominates the life cycle of a fern?", "The diploid sporophyte", "The haploid gametophyte", "Neither; they are equal", "The seed"),
    ], "Water moves passively in dead xylem; sugar actively loaded into living phloem", pace="quick")),
    # 1.3.N skin
    ("DAT-1.3.N", facts("dat-skin-cells", PHYS, [
        ("Which epidermal layer holds the dividing stem cells?", "Stratum basale", "Stratum corneum", "Stratum granulosum", "Hypodermis"),
        ("Which cells make the pigment that absorbs UV?", "Melanocytes", "Keratinocytes", "Langerhans cells", "Merkel cells"),
        ("Which glands secrete oil into hair follicles?", "Sebaceous glands", "Eccrine sweat glands", "Apocrine glands", "Ceruminous glands"),
        ("Which layer is mostly adipose tissue and insulates the body?", "Hypodermis (subcutaneous layer)", "Dermis", "Epidermis", "Stratum lucidum"),
    ], "Epidermis is avascular keratinized epithelium; dermis holds vessels, nerves and glands")),
    ("DAT-1.3.N", facts("dat-skin-thermo", PHYS, [
        ("Body temperature rises during exercise. What do skin arterioles do?", "Dilate to release heat", "Constrict to keep heat", "Close completely", "Nothing; only sweating changes"),
        ("A person steps into cold wind. What happens in the skin?", "Arterioles constrict and arrector pili contract", "Arterioles dilate", "Eccrine sweating rises", "Melanin production rises"),
        ("Why does sweating cool the body?", "Evaporation of water absorbs heat from the skin", "Sweat is colder than blood", "Salt in sweat absorbs heat", "Sweat reflects sunlight"),
        ("Why does a deep burn heal slowly from its centre?", "The dividing basal cells and follicles there were destroyed", "The dermis has no blood supply", "Melanocytes block healing", "Keratin prevents cell division"),
    ], "The hypothalamus sets skin blood flow and sweating as the thermostat's effectors", pace="quick")),
    # 1.3.O skeletal
    ("DAT-1.3.O", facts("dat-bone-tissue", PHYS, [
        ("Which cells sit in lacunae and maintain mature bone matrix?", "Osteocytes", "Osteoblasts", "Osteoclasts", "Chondrocytes"),
        ("What is the repeating unit of compact bone, built around a central canal?", "The osteon (Haversian system)", "The sarcomere", "The trabecula", "The epiphyseal plate"),
        ("Where are most blood cells made in an adult?", "Red marrow in spongy bone", "Yellow marrow in the shaft", "The periosteum", "Hyaline cartilage"),
        ("Where does a long bone grow in length?", "The epiphyseal (growth) plate", "The periosteum", "The diaphysis centre", "The articular cartilage"),
    ], "Compact bone is organized in osteons; spongy bone holds red marrow")),
    ("DAT-1.3.O", facts("dat-cartilage-joint", PHYS, [
        ("Which cartilage forms the intervertebral discs?", "Fibrocartilage", "Hyaline cartilage", "Elastic cartilage", "Compact bone"),
        ("Which cartilage keeps the outer ear flexible?", "Elastic cartilage", "Fibrocartilage", "Hyaline cartilage", "Spongy bone"),
        ("Which joint type is the knee, with a fluid-filled capsule?", "Synovial joint", "Fibrous joint (suture)", "Cartilaginous joint", "Gomphosis"),
        ("What holds a tooth in its socket?", "A gomphosis, through the periodontal ligament", "A synovial capsule", "A tendon", "A suture"),
    ], "Ligaments join bone to bone, tendons muscle to bone; a gomphosis is the fibrous joint of a tooth", pace="quick")),
    # 1.3.P muscular
    ("DAT-1.3.P", facts("dat-muscle-types", PHYS, [
        ("Which muscle is striated, involuntary and joined by intercalated discs?", "Cardiac", "Skeletal", "Smooth", "Both skeletal and smooth"),
        ("Which muscle has no sarcomeres and uses calmodulin to start contraction?", "Smooth", "Skeletal", "Cardiac", "All three"),
        ("Which muscle has long multinucleate fibres under voluntary control?", "Skeletal", "Cardiac", "Smooth", "Cardiac and smooth"),
        ("Which muscle cannot be tetanized because of its long refractory period?", "Cardiac", "Skeletal", "Smooth", "None"),
    ], "Only skeletal muscle is voluntary; cardiac's long refractory period protects the pump")),
    ("DAT-1.3.P", facts("dat-muscle-force", PHYS, [
        ("How does the nervous system lift a heavier weight with the same muscle?", "Recruits more motor units", "Makes each action potential larger", "Lengthens the sarcomeres", "Adds new fibres"),
        ("Stimuli arrive so fast a fibre cannot relax between twitches. What results?", "Summation, then sustained tetanus", "A smaller twitch", "No contraction", "Rigor"),
        ("After death muscles lock rigid. Why?", "Without ATP myosin cannot detach from actin", "Calcium is pumped out", "Tropomyosin covers actin", "Acetylcholine builds up"),
        ("Which fibres resist fatigue for posture and endurance?", "Slow-twitch (type I), rich in mitochondria and myoglobin", "Fast glycolytic (type IIb)", "Smooth muscle", "Cardiac muscle only"),
    ], "All-or-none applies to a fibre; graded force comes from recruitment and frequency", pace="quick")),
    # 1.3.Q immune
    ("DAT-1.3.Q", facts("dat-antibody-class", PHYS, [
        ("Which antibody appears first in a primary response, as a pentamer?", "IgM", "IgG", "IgA", "IgE"),
        ("Which antibody crosses the placenta?", "IgG", "IgM", "IgA", "IgD"),
        ("Which antibody guards mucosa and is in breast milk and saliva?", "IgA", "IgE", "IgM", "IgD"),
        ("Which antibody triggers mast cells in allergy?", "IgE", "IgG", "IgA", "IgM"),
    ], "Memory B cells switch to IgG for a faster, larger secondary response")),
    ("DAT-1.3.Q", facts("dat-immunity-type", PHYS, [
        ("A child gets a measles vaccine. What immunity results?", "Artificial active", "Natural passive", "Artificial passive", "Natural active"),
        ("A newborn receives antibodies through breast milk. What immunity?", "Natural passive", "Artificial active", "Natural active", "Artificial passive"),
        ("A patient gets antivenom after a snakebite. What immunity?", "Artificial passive", "Artificial active", "Natural active", "Natural passive"),
        ("A virus-infected cell shows viral peptide on MHC I. Which cell kills it?", "Cytotoxic (CD8+) T cell", "Helper (CD4+) T cell", "Plasma cell", "Mast cell"),
    ], "Active immunity makes memory; passive is borrowed antibody and fades in weeks", pace="quick")),
    # 1.3.R digestive
    ("DAT-1.3.R", facts("dat-gut-hormone", PHYS, [
        ("Acid chyme enters the duodenum. Which hormone brings bicarbonate from the pancreas?", "Secretin", "Gastrin", "CCK", "Ghrelin"),
        ("Fat enters the duodenum. Which hormone empties the gallbladder?", "Cholecystokinin (CCK)", "Secretin", "Gastrin", "Insulin"),
        ("Food stretches the stomach. Which hormone raises HCl secretion?", "Gastrin", "Secretin", "CCK", "Somatostatin"),
        ("Which hormone, from an empty stomach, raises hunger?", "Ghrelin", "Leptin", "CCK", "Secretin"),
    ], "Gastrin turns acid on; secretin and CCK coordinate the duodenum")),
    ("DAT-1.3.R", facts("dat-absorption-site", PHYS, [
        ("Where are most nutrients absorbed?", "Small intestine (jejunum and ileum)", "Stomach", "Large intestine", "Esophagus"),
        ("Where is vitamin B12 absorbed, bound to intrinsic factor?", "Terminal ileum", "Duodenum", "Stomach", "Colon"),
        ("Absorbed fats are packed into chylomicrons. Where do they go first?", "Lacteals of the lymphatic system", "The hepatic portal vein", "The colon", "The kidneys"),
        ("What does the colon mainly absorb?", "Water and electrolytes", "Most amino acids", "Most glucose", "Bile salts only"),
    ], "Villi and microvilli give the small intestine its surface; fat bypasses the liver via lymph", pace="quick")),
    # 1.3.S urinary
    ("DAT-1.3.S", Q("dat-clearance", PHYS, "Urine {{sub}} is {{U}} mg/mL, urine flow is {{V}} mL/min, and plasma {{sub}} is {{P}} mg/mL. What is the renal clearance, in mL/min?",
        cases=[{"sub": "inulin", "U": 30, "V": 1, "P": 0.24}, {"sub": "inulin", "U": 25, "V": 1.2, "P": 0.24}, {"sub": "creatinine", "U": 1.2, "V": 1.5, "P": 0.015}, {"sub": "urea", "U": 8, "V": 2, "P": 0.25}],
        value="U*V/P", tex="C", verify="solve(Eq(x*nsimplify(P), nsimplify(U)*nsimplify(V)), x)[0]",
        explain="C = U·V̇/P; inulin is filtered and neither reabsorbed nor secreted, so its clearance equals GFR (about 125 mL/min)")),
    ("DAT-1.3.S", facts("dat-raas", PHYS, [
        ("Blood pressure falls. Which cells release renin?", "Juxtaglomerular cells", "Podocytes", "Macula densa only", "Collecting-duct cells"),
        ("What converts angiotensin I to angiotensin II?", "ACE, mostly in the lungs", "Renin", "Aldosterone", "ADH"),
        ("What does aldosterone do in the distal nephron?", "Reabsorbs Na⁺ and secretes K⁺, raising blood volume", "Inserts aquaporins only", "Secretes Na⁺", "Lowers blood pressure"),
        ("A patient takes an ACE inhibitor. What happens to blood pressure?", "It falls", "It rises", "It does not change", "It rises, then stays high"),
    ], "Renin → angiotensin I → (ACE) angiotensin II → vasoconstriction and aldosterone", pace="quick")),
    # 1.3.T reproductive
    ("DAT-1.3.T", facts("dat-gamete-path", PHYS, [
        ("Where do sperm mature and gain motility?", "Epididymis", "Seminiferous tubules", "Vas deferens", "Prostate"),
        ("Which cells make testosterone?", "Leydig (interstitial) cells", "Sertoli cells", "Spermatogonia", "Granulosa cells"),
        ("Where does fertilization usually occur?", "The oviduct (fallopian tube)", "The uterus", "The ovary", "The cervix"),
        ("Which cells nourish developing sperm and respond to FSH?", "Sertoli cells", "Leydig cells", "Theca cells", "Acrosomes"),
    ], "Seminiferous tubules → epididymis → vas deferens → ejaculatory duct → urethra")),
    ("DAT-1.3.T", facts("dat-pregnancy-hormone", PHYS, [
        ("What does a pregnancy test detect?", "hCG from the early embryo", "LH from the pituitary", "Estrogen from the ovary", "Prolactin"),
        ("What keeps the corpus luteum alive in early pregnancy?", "hCG", "FSH", "Oxytocin", "Prolactin"),
        ("Which hormone maintains the endometrium during pregnancy?", "Progesterone", "FSH", "LH", "Testosterone"),
        ("Which hormone drives uterine contractions in labour by positive feedback?", "Oxytocin", "Progesterone", "Prolactin", "Relaxin"),
    ], "Without hCG the corpus luteum fails, progesterone drops and menstruation follows", pace="quick")),
    # 1.4.M human genetics
    ("DAT-1.4.M", Q("dat-human-risk", HER, "{{q}} What is the probability, in %?",
        cases=[{"q": "Two parents are carriers of cystic fibrosis (autosomal recessive). What is the chance their child is affected?", "pn": 1, "pd": 4},
               {"q": "Two carriers of an autosomal recessive disorder have an unaffected child. What is the chance that child is a carrier?", "pn": 2, "pd": 3},
               {"q": "A woman carries hemophilia A (X-linked recessive); her partner is unaffected. What is the chance a son is affected?", "pn": 1, "pd": 2},
               {"q": "A man with an autosomal dominant disorder (heterozygous) has a child with an unaffected partner. What is the chance the child is affected?", "pn": 1, "pd": 2},
               {"q": "A man with hemophilia A has a daughter with an unaffected, non-carrier partner. What is the chance the daughter is a carrier?", "pn": 1, "pd": 1},
               {"q": "Two carriers of an autosomal recessive disorder have two children. What is the chance both are affected?", "pn": 1, "pd": 16}],
        value="100*pn/pd", tex="P", verify="100*Rational(pn, pd)", explain="Draw the Punnett square; condition on what is already known (unaffected excludes aa)")),
    ("DAT-1.4.M", facts("dat-disorder-mode", HER, [
        ("Huntington's disease appears in every generation and in both sexes. Mode?", "Autosomal dominant", "Autosomal recessive", "X-linked recessive", "Mitochondrial"),
        ("Duchenne muscular dystrophy affects mostly boys born to unaffected mothers. Mode?", "X-linked recessive", "Autosomal dominant", "Y-linked", "Autosomal recessive"),
        ("Sickle-cell disease appears in children of two unaffected carriers. Mode?", "Autosomal recessive", "Autosomal dominant", "X-linked dominant", "Mitochondrial"),
        ("A disorder passes from an affected mother to all her children but never from an affected father. Mode?", "Mitochondrial", "X-linked dominant", "Autosomal dominant", "Y-linked"),
    ], "Skipped generations point to recessive; male excess to X-linked; maternal-only transmission to mitochondrial", pace="quick")),
    # 1.4.N chromosomal
    ("DAT-1.4.N", Q("dat-chromatid-count", HER, "A species has 2n = {{tn}}. How many {{what}}?",
        cases=[{"tn": 46, "what": "chromatids are in one cell at metaphase of mitosis", "fn": 2, "fd": 1}, {"tn": 46, "what": "chromosomes are in each cell just after meiosis I", "fn": 1, "fd": 2},
               {"tn": 8, "what": "chromatids are in each cell just after meiosis I", "fn": 1, "fd": 1}, {"tn": 78, "what": "chromosomes are in a gamete", "fn": 1, "fd": 2},
               {"tn": 24, "what": "chromatids are in one cell at metaphase of mitosis", "fn": 2, "fd": 1}, {"tn": 8, "what": "tetrads (bivalents) form at prophase I", "fn": 1, "fd": 2}],
        value="tn*fn/fd", tex="N", final=True, verify="tn*Rational(fn, fd)",
        explain="S phase doubles chromatids, not chromosomes; meiosis I halves chromosome number but each still has two chromatids")),
    ("DAT-1.4.N", facts("dat-karyotype", HER, [
        ("Which karyotype is Down syndrome?", "47,XX,+21 or 47,XY,+21", "45,X", "47,XXY", "47,XY,+18"),
        ("Which karyotype is Turner syndrome?", "45,X", "47,XXY", "47,XXX", "46,XY"),
        ("Which karyotype is Klinefelter syndrome?", "47,XXY", "45,X", "47,XYY", "47,+13"),
        ("A parent with a balanced 14;21 translocation has 45 chromosomes and is unaffected. What can their children inherit?", "Translocation Down syndrome", "Turner syndrome", "Nothing abnormal", "Triploidy"),
    ], "Aneuploidy comes from nondisjunction; a Robertsonian translocation carrier is balanced but can pass an unbalanced set", pace="quick")),
    # 1.4.O development
    ("DAT-1.4.O", facts("dat-dev-order", HER, [
        ("Which stage follows the morula?", "Blastula (blastocyst in mammals)", "Gastrula", "Zygote", "Neurula"),
        ("At which stage do the three germ layers form?", "Gastrulation", "Cleavage", "Fertilization", "Organogenesis"),
        ("Rapid divisions with no growth make smaller and smaller cells. Which stage?", "Cleavage", "Gastrulation", "Neurulation", "Blastocyst implantation"),
        ("Which mammalian blastocyst part becomes the embryo proper?", "Inner cell mass", "Trophoblast", "Blastocoel", "Zona pellucida"),
    ], "Zygote → cleavage → morula → blastula → gastrula → neurula → organogenesis")),
    ("DAT-1.4.O", facts("dat-dev-scenario", HER, [
        ("A fruit fly grows legs where antennae should be. Which genes are altered?", "Homeotic (Hox) genes", "Housekeeping genes", "Tumor suppressors", "rRNA genes"),
        ("Tissue that normally signals the lens is removed, and no lens forms. What process was blocked?", "Induction", "Apoptosis", "Cleavage", "Meiosis"),
        ("Webbing stays between a duck's toes but not a chicken's. Which process removes it in chickens?", "Apoptosis", "Induction", "Gastrulation", "Mitosis"),
        ("A neural tube fails to close. Which germ layer gave rise to it?", "Ectoderm", "Mesoderm", "Endoderm", "Trophoblast"),
    ], "Fate is set by signals between tissues and by master regulatory genes", pace="quick")),
    # 1.4.P genomics
    ("DAT-1.4.P", Q("dat-site-frequency", MOLG, "In random DNA with equal base frequencies, about how many base pairs separate occurrences of a particular {{nb}}-base restriction site?",
        given={"nb": {"pick": [4, 6, 8]}}, value="4^nb", tex="L", final=True, verify="Integer(4)**nb",
        explain="Each position matches with probability 1/4, so a given n-base site appears about once per 4ⁿ bases")),
    ("DAT-1.4.P", facts("dat-genome-features", MOLG, [
        ("Which genome has the most noncoding DNA per gene?", "Human", "E. coli", "Yeast", "A bacteriophage"),
        ("Why do bacterial genomes have high gene density?", "Few introns or repeats, and genes grouped in operons", "They have more chromosomes", "Their genes are shorter than RNA", "They lack promoters"),
        ("Two species share a gene of similar sequence descended from a common ancestor. What are the genes called?", "Orthologs", "Paralogs", "Pseudogenes", "Transposons"),
        ("Roughly what fraction of the human genome codes for protein?", "About 1–2%", "About 50%", "About 25%", "Over 90%"),
    ], "Genome size tracks noncoding DNA, not organism complexity (the C-value paradox)", pace="quick")),
    # 1.4.Q epigenetics
    ("DAT-1.4.Q", Q("dat-barr-bodies", MOLG, "How many Barr bodies are in a somatic cell of a person with karyotype {{k}}?",
        cases=[{"k": "46,XX", "nx": 2}, {"k": "47,XXY", "nx": 2}, {"k": "47,XXX", "nx": 3}, {"k": "48,XXXY", "nx": 3}, {"k": "49,XXXXY", "nx": 4}],
        value="nx - 1", tex="N", final=True, verify="len(range(1, nx))",
        explain="All but one X are inactivated as heterochromatin (Lyon hypothesis), whatever the sex")),
    ("DAT-1.4.Q", facts("dat-imprinting", MOLG, [
        ("Loss of the paternal copy of 15q11–13 causes which syndrome?", "Prader–Willi", "Angelman", "Turner", "Fragile X"),
        ("Loss of the maternal copy of 15q11–13 causes which syndrome?", "Angelman", "Prader–Willi", "Klinefelter", "Down"),
        ("A calico cat's patchy coat shows which process?", "Random X inactivation", "Genomic imprinting", "Incomplete dominance", "Codominance"),
        ("Methylating cytosines in a promoter usually does what?", "Silences the gene", "Activates the gene", "Mutates the sequence", "Removes histones"),
    ], "Imprinting silences one parent's copy; the sequence is unchanged, only its marks differ", pace="quick")),
    # 1.5.I behavior
    ("DAT-1.5.I", Q("dat-hamilton", EVO, "A helping act costs the helper {{Cc}} offspring and gives a {{rel}} {{Bn}} extra offspring. By Hamilton's rule, what is r·B − C (positive means favoured)?",
        cases=[{"rel": "full sibling", "rn": 1, "rd": 2, "Bn": 3, "Cc": 1}, {"rel": "half sibling", "rn": 1, "rd": 4, "Bn": 3, "Cc": 1}, {"rel": "first cousin", "rn": 1, "rd": 8, "Bn": 4, "Cc": 1},
               {"rel": "full sibling", "rn": 1, "rd": 2, "Bn": 5, "Cc": 2}, {"rel": "offspring", "rn": 1, "rd": 2, "Bn": 4, "Cc": 1}],
        value="rn/rd*Bn - Cc", tex="rB - C", verify="Rational(rn, rd)*Bn - Cc",
        explain="Altruism spreads when rB > C; relatedness is 1/2 for full siblings and offspring, 1/4 half siblings, 1/8 cousins")),
    ("DAT-1.5.I", facts("dat-social-behavior", EVO, [
        ("A honeybee's waggle dance tells nestmates what?", "Direction and distance to food", "The queen's location", "An alarm", "Mating readiness"),
        ("A worker bee is sterile but raises her sisters. What explains it?", "Kin selection", "Group selection only", "Reciprocal altruism", "Sexual selection"),
        ("A moth finds a mate kilometres away by smell. What is the signal?", "A pheromone", "A fixed action pattern", "Imprinting", "Habituation"),
        ("Vampire bats share blood with roost-mates that shared before. What behaviour?", "Reciprocal altruism", "Kin selection", "Imprinting", "Agonistic display"),
    ], "Kin selection works through relatives; reciprocal altruism through repeated exchange", pace="quick")),
]
