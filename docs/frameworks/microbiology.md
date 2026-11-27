# Microbiology — curriculum framework (draft 1)

Generated from `drills/frameworks/microbiology.yaml` by `scripts/framework.mjs`. ● drilled · ◐ partly · ○ no drills yet.

**25 learning objectives** in 7 units (25 core): 25 drilled, 0 partly, 0 with no drills. Core: 25 / 25 drilled.

## Big ideas

- **SMALL · Small, many and fast.** A microbe's power is in numbers: populations double in minutes to hours, so rare events (a mutation, a transfer) happen somewhere every generation.
- **ENV · The environment selects.** Which microbes grow is set by oxygen, temperature, nutrients and what else is living there; the same rule explains enrichment media, the microbiome and resistance.
- **COUNT · You know it when you can count it.** A colony stands for one cell that was plated; dilution arithmetic turns a plate into a concentration.

## Practices

- **P1 · Compute.** Carry a growth, dilution or optics relation to a number.
- **P2 · Identify.** Name the structure, process or category from a description.

## Units at a glance

| Unit | Scope | Est. weight | LOs | ● | ◐ | ○ |
|---|---|---|---|---|---|---|
| 1 · Diversity and evolution | core | — | 2 | 2 | 0 | 0 |
| 2 · Cell structure and viruses | core | — | 4 | 4 | 0 | 0 |
| 3 · Metabolism and growth | core | — | 4 | 4 | 0 | 0 |
| 4 · Microbial genetics | core | — | 3 | 3 | 0 | 0 |
| 5 · Microbial ecology | core | — | 3 | 3 | 0 | 0 |
| 6 · Microbes and people | core | — | 5 | 5 | 0 | 0 |
| 7 · Laboratory skills | core | — | 4 | 4 | 0 | 0 |

## Unit 1 · Diversity and evolution

Big ideas: SMALL, ENV

### 1.1 The microbial world



- ● **MI-1.1.A** (asm-micro-2024:EV) Place a microbe in its domain from its cell features.
  - EK: Bacteria and Archaea are prokaryotes (no nucleus, 70S ribosomes); Bacteria have peptidoglycan and ester-linked lipids, Archaea have no peptidoglycan and ether-linked lipids. Eukarya (fungi, protozoa, algae) have nuclei, organelles and 80S ribosomes. Viruses are not cells.
  - Needs: BI-2.11.B
  - P2 · drills: mi-domain-pick, mi-classification
- ● **MI-1.1.B** (asm-micro-2024:EV) Explain how selection acts on mutations in a large population.
  - EK: Mutations arise at random, before any selection; in a large population a few resistant cells are already present, and a selective agent kills the rest so the survivors take over. Expected mutants = number of cells × mutation rate per cell.
  - Needs: MI-1.1.A
  - P1 · drills: mi-expected-mutants, mi-selection

## Unit 2 · Cell structure and viruses

Big ideas: SMALL

### 2.1 Cells and viruses



- ● **MI-2.1.A** (asm-micro-2024:CS) Contrast the Gram-positive and Gram-negative cell envelopes.
  - EK: Gram-positive cells have a thick peptidoglycan layer with teichoic acids and no outer membrane. Gram-negative cells have a thin peptidoglycan layer in a periplasm beneath an outer membrane whose outer leaflet is lipopolysaccharide.
  - Needs: MI-1.1.B
  - P2 · drills: mi-gram-feature, mi-envelope-parts
- ● **MI-2.1.B** (asm-micro-2024:CS) Match bacterial structures to their functions.
  - EK: Flagella give motility, pili and fimbriae attachment (and the sex pilus conjugation), a capsule protection from drying and phagocytosis, endospores survival of heat and chemicals. Plasmids carry extra genes.
  - Needs: MI-2.1.A
  - P2 · drills: mi-structures, mi-endospores
- ● **MI-2.1.C** (asm-micro-2024:CS) Tell the eukaryotic microbes apart and compare them with bacteria.
  - EK: Fungi are heterotrophs with chitin walls and ergosterol membranes (yeasts are single cells, moulds grow as hyphae); protozoa are single-celled and usually motile; algae photosynthesise. Their 80S ribosomes and sterol membranes make them harder to target without harming the host.
  - Needs: MI-2.1.B
  - P2 · drills: mi-eukaryotic-microbe, mi-eukaryote-vs-bacteria
- ● **MI-2.1.D** (asm-micro-2024:CS) Describe a virus particle and the stages of viral replication.
  - EK: A virion is a genome (DNA or RNA) in a protein capsid, sometimes with a lipid envelope. Replication runs attachment, entry, synthesis, assembly, release. A lytic phage bursts its host; a temperate phage can integrate as a prophage (lysogeny).
  - Needs: MI-2.1.C
  - P2 · drills: mi-virus-parts, mi-lytic-lysogenic

## Unit 3 · Metabolism and growth

Big ideas: ENV, SMALL

### 3.1 Growth



- ● **MI-3.1.A** (asm-micro-2024:MP) Classify a microbe by its energy and carbon source.
  - EK: Phototrophs take energy from light, chemotrophs from chemicals (organotrophs from organic compounds, lithotrophs from inorganic ones). Autotrophs fix carbon dioxide; heterotrophs need organic carbon.
  - Needs: MI-2.1.D, BI-3.6.E
  - P2 · drills: mi-metabolic-type, mi-energy-carbon
- ● **MI-3.1.B** (asm-micro-2024:MP) Predict where a microbe grows from its oxygen and temperature needs.
  - EK: Obligate aerobes need oxygen, obligate anaerobes are harmed by it, facultative anaerobes use it when present, microaerophiles need a little, aerotolerant anaerobes ignore it. Psychrophiles, mesophiles (body temperature) and thermophiles are named by optimum temperature.
  - Needs: MI-3.1.A
  - P2 · drills: mi-oxygen-class, mi-environment-limits
- ● **MI-3.1.C** (asm-micro-2024:MP) Read a growth curve and do the arithmetic of doubling.
  - EK: A batch culture shows lag, exponential (log), stationary and death phases. In exponential growth N = N0 × 2^n with n = time ÷ generation time, so the generation time is t × log 2 ÷ log(N/N0).
  - Needs: MI-3.1.B
  - P1 · drills: mi-doubling-count, mi-generation-time
- ● **MI-3.1.D** (asm-micro-2024:MP) Compare fermentation with respiration.
  - EK: Respiration passes electrons down a transport chain to a terminal acceptor (oxygen in aerobic, nitrate or sulfate in anaerobic respiration) and makes ATP mostly by oxidative phosphorylation. Fermentation has no chain: ATP comes from glycolysis alone, and an organic molecule takes the electrons to regenerate NAD+.
  - Needs: MI-3.1.C
  - P2 · drills: mi-ferment-respire, mi-fermentation-facts

## Unit 4 · Microbial genetics

Big ideas: SMALL

### 4.1 Genes on the move



- ● **MI-4.1.A** (asm-micro-2024:IF) Tell the three routes of horizontal gene transfer apart.
  - EK: Transformation is uptake of free DNA from the surroundings; transduction is transfer by a bacteriophage; conjugation is transfer by cell-to-cell contact through a pilus, usually of a plasmid. All three move genes between cells of the same generation.
  - Needs: MI-3.1.D, BI-6.5.B
  - P2 · drills: mi-hgt-route, mi-hgt-facts
- ● **MI-4.1.B** (asm-micro-2024:IF) Predict whether the lac operon is expressed.
  - EK: The lac repressor binds the operator and blocks transcription unless allolactose (from lactose) removes it. Strong expression also needs low glucose, when cAMP with its activator protein helps RNA polymerase bind. So the operon is fully on only with lactose present and glucose absent.
  - Needs: MI-4.1.A
  - P2 · drills: mi-lac-state, mi-operon-parts
- ● **MI-4.1.C** (asm-micro-2024:IF) Classify mutations and find a mutation frequency.
  - EK: A point mutation may be silent, missense or nonsense; an insertion or deletion not in threes shifts the reading frame. Mutation frequency is mutant colonies over total viable cells plated.
  - Needs: MI-4.1.B
  - P1 · drills: mi-mutation-type, mi-mutation-frequency

## Unit 5 · Microbial ecology

Big ideas: ENV

### 5.1 Communities



- ● **MI-5.1.A** (asm-micro-2024:ME) Describe biofilms and classify symbioses.
  - EK: Most microbes live in biofilms: communities attached to a surface in a self-made matrix, coordinated by quorum sensing and far harder to remove than free cells. In mutualism both partners benefit, in commensalism one benefits and the other is unaffected, in parasitism one benefits at the other's cost.
  - Needs: MI-3.1.D
  - P2 · drills: mi-symbiosis, mi-biofilm
- ● **MI-5.1.B** (asm-micro-2024:ME) Assign microbes their steps in the nitrogen and carbon cycles.
  - EK: Nitrogen fixation turns N2 into ammonia; nitrification oxidises ammonia to nitrite and nitrate; denitrification returns nitrate to N2; decomposers release ammonia from organic matter. Photosynthesisers fix carbon; decomposers and methanogens return it.
  - Needs: MI-5.1.A
  - P2 · drills: mi-nitrogen-step, mi-cycles
- ● **MI-5.1.C** (asm-micro-2024:ME) Describe the human microbiome and what it does for its host.
  - EK: The body carries resident microbes, densest in the large intestine and absent from normally sterile sites such as blood and cerebrospinal fluid. Residents compete with invaders (colonisation resistance), make vitamins, digest fibre and train the immune system; broad antibiotics disturb them.
  - Needs: MI-5.1.B
  - P2 · drills: mi-microbiome-sites, mi-microbiome-roles

## Unit 6 · Microbes and people

Big ideas: ENV, COUNT

### 6.1 Disease, control and use



- ● **MI-6.1.A** (asm-micro-2024:IM) Use the vocabulary of infection and tell endotoxin from exotoxin.
  - EK: Infection is growth of a microbe in a host; disease is damage that results. Koch's postulates tie one organism to one disease by isolating it, growing it in pure culture and reproducing the disease. Exotoxins are secreted proteins; endotoxin is the lipid A of Gram-negative outer membranes, released when cells break up.
  - Needs: MI-4.1.C, MI-5.1.C
  - P2 · drills: mi-toxin-type, mi-infection-terms
- ● **MI-6.1.B** (asm-micro-2024:IM) Tell sterilisation from disinfection and compute a decimal reduction.
  - EK: Sterilisation removes or kills all life including endospores; disinfection reduces microbes on objects; antisepsis does so on living tissue. Death is exponential: each D-value (decimal reduction time) cuts the population tenfold, so survivors = N0 × 10^(−t/D).
  - Needs: MI-6.1.A
  - P1 · drills: mi-control-term, mi-decimal-reduction
- ● **MI-6.1.C** (asm-micro-2024:IM) Match antimicrobial drug classes to their targets and name general resistance mechanisms.
  - EK: Beta-lactams and glycopeptides block cell wall synthesis; aminoglycosides, tetracyclines and macrolides act on the 70S ribosome; fluoroquinolones on DNA gyrase; sulfonamides on folate synthesis. Resistance arises by destroying the drug, altering the target, pumping the drug out or keeping it out.
  - Needs: MI-6.1.B
  - P2 · drills: mi-drug-targets, mi-resistance-mechanism
- ● **MI-6.1.D** (asm-micro-2024:IM) Classify vaccines and explain why antibiotics do not treat viral infections.
  - EK: Live attenuated vaccines replicate weakly and give strong lasting immunity; inactivated vaccines cannot replicate; subunit, toxoid and conjugate vaccines use parts; mRNA vaccines have the host cell make the antigen. Antibiotics target bacterial structures that viruses lack.
  - Needs: MI-6.1.C
  - P2 · drills: mi-vaccine-type, mi-antibiotic-virus
- ● **MI-6.1.E** (asm-micro-2024:IM) Give uses of microbes in food, industry and the environment.
  - EK: Fermentations make bread, beer, wine, yoghurt, cheese and vinegar; engineered microbes make insulin and enzymes; microbes treat sewage and break down pollutants (bioremediation).
  - Needs: MI-6.1.D
  - P2 · drills: mi-food-microbes, mi-industry-microbes

## Unit 7 · Laboratory skills

Big ideas: COUNT

### 7.1 Seeing and counting



- ● **MI-7.1.A** (asm-micro-2024:LAB) Find magnification and the resolution limit of a light microscope.
  - EK: Total magnification is ocular × objective. The smallest resolvable distance is about 0.61 × wavelength ÷ numerical aperture, so shorter wavelengths and oil immersion (higher NA) resolve finer detail; about 0.2 micrometres is the practical limit.
  - Needs: MI-2.1.D
  - P1 · drills: mi-magnification, mi-resolution
- ● **MI-7.1.B** (asm-micro-2024:LAB) Order the Gram stain and choose a stain for a purpose.
  - EK: Crystal violet (primary stain), iodine (mordant), alcohol (decolouriser), safranin (counterstain). The decolouriser step is the one that separates the two groups. Acid-fast staining shows waxy mycolic acid walls; malachite green shows endospores; negative stains show capsules.
  - Needs: MI-7.1.A
  - P2 · drills: mi-gram-steps, mi-stain-choice
- ● **MI-7.1.C** (asm-micro-2024:LAB) Turn a plate count and a dilution series into a concentration.
  - EK: Each colony comes from one viable cell or clump (a colony-forming unit). CFU per mL = colonies ÷ (volume plated × dilution). A serial dilution multiplies the factors of each step. Plates with roughly 30 to 300 colonies are counted.
  - Needs: MI-7.1.B
  - P1 · drills: mi-cfu-per-ml, mi-serial-dilution
- ● **MI-7.1.D** (asm-micro-2024:LAB) Choose a medium and name the principles of aseptic work and containment levels.
  - EK: A selective medium suppresses unwanted organisms; a differential medium makes groups look different; some do both. A streak plate thins cells until single colonies form a pure culture. Laboratories are graded biosafety level 1 to 4 by the risk of the agents handled, with practices and containment rising at each level.
  - Needs: MI-7.1.C
  - P2 · drills: mi-medium-type, mi-aseptic-containment
