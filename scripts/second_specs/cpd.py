"""Computational Protein Design framework (CPD, Nov 2026): structure in UNITS (written to
drills/frameworks/protein-design.yaml by scripts/cpd_framework.py) and two question types per objective in ADD.

Sources read for this (Nov 2026):
  pyrosetta-notebooks  RosettaCommons/PyRosetta.notebooks: the whole table of contents (16 chapters and every
                       notebook title) read from the repository page; the notebooks themselves were not run. Taught
                       as a JHU course for over ten years (Le et al., The Biophysicist 2021).
  rosetta-ref15        Alford et al., "The Rosetta all-atom energy function for macromolecular modeling and design",
                       JCTC 13 (2017) 3031, read from the open core.ac.uk copy: every term, the weight table, the
                       reference energy, units and the guidance on interpreting energies. The later sections (worked
                       protocol captures) were not read.
  dl4proteins          Chungyoun et al., "DL4Proteins Jupyter Notebooks…" (arXiv 2511.02128): the ten workshop
                       titles and what each covers, read in full from the paper.
  kuhlman-bradley      Kuhlman & Bradley, "Advances in protein structure prediction and design", Nat Rev Mol Cell
                       Biol 20 (2019) 681: section outline and key concepts (first half of the PMC text).
  jhu-545614           JHU 545.614 "Computational Protein Structure Prediction and Design" course page: topic list.

The ramp runs vocabulary → representation → energy → sampling → sequence → interfaces → de novo → deep learning →
validation, with the first objective of each unit a recall item. Numbers are recomputed by sympy; facts are standard
textbook or documented content, paraphrased, never copied."""
from opl_dsl import Q

FILE, FRAMEWORK = "cpd-design", "protein-design"
PRACTICE = "P1"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
ST, RP, EN, SA, SQ, IF, DN, ML, VA = ("design.structure", "design.representation", "design.energy", "design.sampling",
    "design.sequence", "design.interfaces", "design.denovo", "design.ml", "design.validation")
PN = lambda *s: [f"pyrosetta-notebooks:{x}" for x in s]
RF = lambda *s: [f"rosetta-ref15:{x}" for x in s]
DL = lambda *s: [f"dl4proteins:{x}" for x in s]
KB = lambda *s: [f"kuhlman-bradley:{x}" for x in s]

IDEAS = [("INVERSE", "Design is folding run backwards",
          "Prediction searches conformations for one sequence; design searches sequences for one conformation. The same energy function and the same samplers serve both."),
         ("ENERGY", "A score is a model, not the truth",
          "Every number is a weighted sum of approximate terms. A design is only as good as what the function leaves out."),
         ("SEARCH", "The space is too big to enumerate",
          "Rotamers and sequences grow combinatorially, so everything rests on sampling: Monte Carlo, annealing, pruning or a learned prior."),
         ("TEST", "A design is a hypothesis until it is expressed",
          "Computational scores rank candidates; folding, stability and function are settled in the laboratory.")]

# unit n: (id, title, std, ideas, {topic n: (title, [(letter, std, do, ek, practice)])})
UNITS = {
 1: ("structure", "Protein geometry and the rotamer picture", PN("2.5") + KB("3"), ["INVERSE"], {
   1: ("Backbone and side-chain degrees of freedom", [
     ("A", PN("2.4", "2.5"), "Name the backbone and side-chain dihedrals and say which are free, which are nearly fixed, and which regions of the Ramachandran plot the common secondary structures occupy.",
      "φ (C−N−Cα−C), ψ (N−Cα−C−N) and ω (nearly planar, about 180° trans); side-chain χ1, χ2…; right-handed α-helix near φ ≈ −60°, ψ ≈ −45°, β-sheet near φ ≈ −120°, ψ ≈ +130°; glycine is permissive and proline restricted.", "P2"),
     ("B", PN("2.5"), "Count the conformational degrees of freedom of a chain and show why enumeration is hopeless.",
      "Two free backbone dihedrals per residue; discretising each into a few states gives states^(2n) conformations, which is Levinthal's paradox in numbers.", "P1")]),
   2: ("Rotamers", [
     ("A", PN("6.1") + RF("fa_dun"), "Explain what a rotamer library is and why side-chain conformations are treated as a discrete, backbone-dependent set.",
      "Side-chain χ angles cluster in a few favoured combinations; the Dunbrack library gives their probabilities as a function of φ/ψ, and fa_dun scores the chosen rotamer's internal energy.", "P2"),
     ("B", PN("6.1"), "Count the rotamer combinations of a set of designable positions and convert a rotamer probability into an energy.",
      "Combinations multiply: Π k_i over positions. A probability p maps to an energy −kT ln p, so a rotamer ten times less likely costs about 1.4 kcal/mol at 298 K.", "P1")]),
 }),
 2: ("representation", "How a structure is represented", PN("2.1", "2.2"), ["INVERSE"], {
   1: ("The Pose and its numbering", [
     ("A", PN("2.1", "2.2"), "Describe what a Pose holds and how residues are addressed, and distinguish pose numbering from PDB numbering.",
      "A Pose carries the sequence, the conformation as internal coordinates, the fold tree and the energies; pose numbering is 1…N over all residues, while PDB numbering carries chains, gaps and insertion codes.", "P2"),
     ("B", PN("2.1"), "Convert between pose and PDB numbering across chains of known length.",
      "Pose index of residue j in chain c is j plus the lengths of the preceding chains, so gaps in PDB numbering do not shift pose indices.", "P1")]),
   2: ("Centroid and full atom", [
     ("A", PN("4.2", "5.1") + KB("3"), "Contrast the centroid and full-atom representations and say which stage of a protocol uses each.",
      "Centroid replaces each side chain with one pseudo-atom and a simple score for fast global search; full atom restores every atom for local refinement and final ranking. Multi-resolution modelling is the standard pattern.", "P2"),
     ("B", PN("4.2"), "Compute how many atoms a representation tracks and the speed-up a coarse-grained model buys.",
      "Pairwise interaction work scales with the square of the number of interacting centres, so a fourfold cut in centres is about a sixteenfold cut in pair work.", "P1")]),
 }),
 3: ("energy", "The all-atom energy function", RF("form", "table", "ref", "units"), ["ENERGY"], {
   1: ("Terms and weights", [
     ("A", RF("form", "table"), "Name the main energy terms and classify each as physics-based or knowledge-based.",
      "Physics-based: fa_atr and fa_rep (Lennard-Jones split at its minimum), fa_sol (Lazaridis–Karplus desolvation), lk_ball_wtd (anisotropic polar solvation), fa_elec (distance-dependent dielectric). Knowledge-based: fa_dun (rotamer), rama_prepro (backbone φ/ψ), p_aa_pp (residue given φ/ψ), the hydrogen-bond and disulfide terms fit to structures.", "P2"),
     ("B", RF("form", "table"), "Compute a total score as the weighted sum of its terms.",
      "Total = Σ w_i E_i. Physics-based terms carry weight 1.0; fa_rep is 0.55, fa_dun 0.7, rama_prepro 0.45, p_aa_pp 0.4, omega 0.6, dslf_fa13 1.25, fa_intra_rep 0.005.", "P1")]),
   2: ("Reference energies and design", [
     ("A", RF("ref"), "Explain what the reference energy does and why design, not scoring, needs it.",
      "ref adds a constant per amino-acid type standing for the unfolded state, fitted to maximise native sequence recovery. For a fixed sequence it is a constant offset; when sequences are compared it removes the composition bias the other terms would impose.", "P2"),
     ("B", RF("ref", "units"), "Compute a stability difference between two candidate sequences including their reference energies.",
      "ΔΔG ≈ (E_folded − Σ ref) for one sequence minus the same for the other; a design that scores better only because of composition bias loses that advantage once ref is included.", "P1")]),
   3: ("Reading an energy", [
     ("A", RF("units", "guidance"), "State what the energy's units mean and how far to trust a computed ΔΔG.",
      "The current function is parameterised in kcal/mol rather than arbitrary Rosetta Energy Units, but the paper's own worked mutation gave −4.95 kcal/mol against −1.11 kcal/mol measured: the sign and the ranking are more reliable than the magnitude.", "P2"),
     ("B", RF("guidance"), "Decompose a score change into terms and name the interaction responsible.",
      "Subtract term by term between two states; per-residue and atom-pair tables locate the contact that changed. A buried polar group shows up in solvation, a clash in fa_rep.", "P1")]),
 }),
 4: ("sampling", "Searching conformations", PN("4.1", "5.1", "6.2") + KB("2"), ["SEARCH"], {
   1: ("Monte Carlo and annealing", [
     ("A", KB("2") + PN("4.1"), "State the Metropolis rule and explain why uphill moves are accepted at all.",
      "A move raising the score by ΔE is accepted with probability exp(−ΔE/kT); uphill steps let the search leave local minima, which gradient descent cannot do.", "P2"),
     ("B", PN("4.1"), "Compute a Metropolis acceptance probability and show how annealing changes it.",
      "P = exp(−ΔE/kT) for ΔE > 0, P = 1 otherwise; lowering the temperature during a run makes the same uphill move far less likely, which is simulated annealing.", "P1")]),
   2: ("Packing and minimisation", [
     ("A", PN("6.2"), "Describe what the packer does, and how packing, minimisation and relax differ.",
      "The packer runs simulated annealing over discrete rotamers at the positions a task allows; minimisation moves continuous degrees of freedom downhill; relax alternates the two so a structure settles without drifting far.", "P2"),
     ("B", PN("6.2") + KB("5"), "Count the entries of a rotamer pair-energy table and explain the cost of precomputing it.",
      "With n positions and k rotamers each, there are n·k one-body terms and k² entries for each of the n(n−1)/2 position pairs, so the table grows as the square of both.", "P1")]),
 }),
 5: ("sequence", "Designing sequence", PN("6.3", "6.4", "6.8") + KB("5"), ["INVERSE", "SEARCH"], {
   1: ("Specifying what may change", [
     ("A", PN("6.3", "6.4"), "Read and write a design specification: which positions repack, which design, and to what alphabet.",
      "A resfile or task operation sets per-position behaviour — repack only, design to all residues, or design to a restricted set; everything else stays fixed. Getting this wrong is the usual cause of a nonsense design.", "P2"),
     ("B", PN("6.3"), "Count the sequence space a design specification opens.",
      "Π a_i over designable positions, where a_i is the alphabet allowed at position i; 20^n for unrestricted design, which is why the space is sampled and never enumerated.", "P1")]),
   2: ("Mutational scans", [
     ("A", PN("6.8") + RF("guidance"), "Plan a point-mutation scan and read its output.",
      "A saturation scan tries 19 substitutions at each chosen position, scoring each after local repacking; the result is a ranked ΔΔG list, not a verdict.", "P2"),
     ("B", PN("6.8"), "Count the jobs and compute the ΔΔG values a scan produces.",
      "19 substitutions per position times the positions, times the independent trials each is run with; ΔΔG = E_mutant − E_wild-type, with a positive value destabilising.", "P1")]),
   3: ("Judging a design protocol", [
     ("A", RF("ref") + KB("5"), "Use native sequence recovery to judge an energy function or protocol.",
      "Redesign a natural protein's positions and count how often the native residue comes back; random choice recovers about 5%, buried positions recover best, and surface positions worst.", "P1"),
     ("B", KB("5"), "Match a sequence-optimisation method to its guarantee: dead-end elimination, mean field, annealing, genetic algorithms.",
      "Dead-end elimination prunes provably non-optimal rotamers and can return the true optimum; annealing and genetic algorithms are stochastic and return good solutions without a proof.", "P2")]),
 }),
 6: ("interfaces", "Interfaces, docking and ligands", PN("7.1", "7.2", "8.1") + KB("5"), ["ENERGY"], {
   1: ("Docking and interface scoring", [
     ("A", PN("7.1", "7.2"), "Describe the two stages of docking and what a funnel plot shows.",
      "A global rigid-body search (often Fourier-based) is followed by local high-resolution refinement; plotting score against RMSD to a reference should funnel toward low RMSD if the function discriminates.", "P2"),
     ("B", PN("7.2") + RF("guidance"), "Compute a binding or interface energy from component scores.",
      "ΔE_interface = E_complex − E_partner A alone − E_partner B alone, each scored in the same function; near-native models gain in van der Waals, electrostatics and side-chain hydrogen bonds.", "P1")]),
   2: ("Designing a binding site", [
     ("A", PN("8.1") + KB("5"), "Lay out how a ligand-binding pocket is designed and why designed enzymes fall short of natural ones.",
      "Place the ligand, design the shell around it, then repack and minimise. Pocket shape and binding are achievable; transition-state stabilisation, and so catalytic efficiency, is not yet.", "P2"),
     ("B", KB("5"), "Choose one-sided or two-sided interface design for a stated problem and say what makes it hard.",
      "Two-sided design redesigns both partners and is easier; a binder against a fixed natural surface is one-sided and much harder, which is also why antibody design remains difficult.", "P2")]),
 }),
 7: ("denovo", "De novo design", PN("6.5", "6.6", "6.7") + KB("5"), ["INVERSE", "SEARCH"], {
   1: ("Building a backbone from nothing", [
     ("A", PN("6.6", "6.7") + KB("5"), "Contrast the routes to a de novo backbone: fragment assembly, distance constraints and parametric equations.",
      "Fragments splice pieces of known structures; constraints specify the contacts wanted; parametric equations generate ideal folds such as coiled coils and β-barrels from a handful of numbers.", "P2"),
     ("B", PN("6.6"), "Compute the geometry of a parametric helical bundle from its parameters.",
      "A coiled-coil's superhelical radius, pitch and the number of residues per repeat fix the backbone; the rise along the axis per residue follows from the pitch and the residues per turn.", "P1")]),
   2: ("Hard cases", [
     ("A", PN("6.5") + KB("5"), "Say why buried hydrogen-bond networks are designed before the rest of the sequence.",
      "A network of buried polar residues is rare and easily broken by later repacking, so it is found first and then held fixed while the surrounding core is designed.", "P2"),
     ("B", KB("5"), "Explain negative and multi-state design and compute the energy gap that must be opened.",
      "Favour the target state by scoring it against competing states and maximising the gap; a conformational switch is a multi-state design where each state's gap is tuned, and a gap of a few kT sets the population ratio.", "P1")]),
 }),
 8: ("ml", "Deep learning for structure and design", DL("WS04", "WS06", "WS07", "WS08", "WS09", "WS10") + KB("4"), ["SEARCH"], {
   1: ("Structure prediction and its confidence", [
     ("A", DL("WS06"), "Name the inputs a modern structure predictor takes and read its confidence metrics.",
      "Sequence, a multiple-sequence alignment and optional templates go in; pLDDT scores per-residue local confidence (higher is better, with roughly 70 and 90 as useful marks) and PAE scores the expected error between residue pairs, which is what judges domain placement.", "P2"),
     ("B", KB("4") + DL("WS06"), "Explain why alignment depth limits prediction and coevolution-based contacts.",
      "Coevolution separates direct couplings from indirect ones only when the alignment is deep; shallow families, including many eukaryote-specific ones, lose that signal, and MSA coverage plots are read for exactly this.", "P2")]),
   2: ("Learned representations and generators", [
     ("A", DL("WS04", "WS05", "WS07"), "Match a representation to its architecture: sequence tokens for language models, residue or atom graphs for message passing.",
      "A protein language model is trained on sequences alone and its embeddings transfer to downstream tasks; a graph network passes messages between residues or atoms, where invariance and equivariance to rotation matter.", "P2"),
     ("B", DL("WS08", "WS09", "WS10"), "Describe the diffusion design pipeline and what each stage contributes.",
      "A diffusion model denoises a backbone (unconditionally, scaffolding a motif, or against a target), an inverse-folding model assigns a sequence to that backbone, and a structure predictor checks that the sequence folds back to it.", "P2")]),
   3: ("Using a pipeline honestly", [
     ("A", DL("WS09"), "Compute the yield of a filtered design funnel.",
      "Multiply the pass fractions of the stages: backbones generated, sequences per backbone, and the fraction whose predicted structure falls within the RMSD and confidence cut-offs.", "P1"),
     ("B", DL("WS09") + KB("6"), "Say what a self-consistency check does and does not establish.",
      "Designing a sequence for a backbone and recovering that backbone from the sequence shows the two models agree; it is not experimental evidence, since both may share the same blind spots.", "P2")]),
 }),
 9: ("validation", "Validation and the bridge to simulation", KB("6", "7") + PN("15.2"), ["TEST", "ENERGY"], {
   1: ("Testing designs", [
     ("A", KB("6"), "Plan the experiments that test a design and say how many candidates to make.",
      "Expression and solubility, then thermal or chemical denaturation for stability, oligomeric state, a high-resolution structure, and a function assay. A stabilisation project may test a handful; a new binder may need thousands, screened by display and sequencing.", "P2"),
     ("B", KB("6"), "Compute the number of designs to order for a target number of successes at an expected hit rate.",
      "Expected successes = N × hit rate, so N = target/hit rate; low rates are why display libraries, not individual clones, are used for binders.", "P1")]),
   2: ("Where a score is not enough", [
     ("A", PN("15.2") + RF("guidance"), "Decide when a score-function ΔΔG is enough and when an alchemical free-energy calculation is warranted.",
      "A score-function scan ranks many mutations cheaply and is right about signs more often than magnitudes; when a few candidates must be quantitative, or when a result must survive review, λ dynamics or another alchemical method gives a statistical-mechanics estimate with an error bar.", "P2"),
     ("B", KB("7"), "Name what current energy functions handle worst and relate it to a failed design.",
      "Balancing polar against nonpolar energetics, solvation, flexible loops and backbone flexibility are the open problems; a design that expresses but is unstructured usually points at one of them.", "P2")]),
 }),
}

RT = "Rational('0.0019872043')*Rational('298.15')"


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC, correct="0", verify="authored", explain=explain)


ADD = [
    ("CPD-1.1.A", facts("cpd-dihedrals", ST, [
        ("Which backbone dihedral is held nearly planar?", "ω, at about 180° in the trans peptide bond", "φ", "ψ", "χ1"),
        ("The right-handed α-helix sits near which backbone angles?", "φ ≈ −60°, ψ ≈ −45°", "φ ≈ +60°, ψ ≈ +45°", "φ ≈ −120°, ψ ≈ +130°", "φ ≈ 180°, ψ ≈ 180°"),
        ("An extended β-strand sits near which backbone angles?", "φ ≈ −120°, ψ ≈ +130°", "φ ≈ −60°, ψ ≈ −45°", "φ ≈ 0°, ψ ≈ 0°", "φ ≈ +60°, ψ ≈ +60°"),
        ("Which residue occupies the widest range of the Ramachandran plot?", "Glycine, which has no side chain beyond its hydrogen", "Tryptophan", "Proline", "Valine"),
        ("Proline is restricted in φ because:", "Its side chain is bonded back to the backbone nitrogen", "It is charged", "It is the largest residue", "It cannot form hydrogen bonds"),
        ("The dihedral φ is defined by which four atoms?", "C(previous)−N−Cα−C", "N−Cα−C−N(next)", "Cα−C−N−Cα", "N−Cα−Cβ−Cγ"),
    ], "Two free backbone dihedrals per residue, one nearly fixed, and side-chain χ angles beyond them")),
    ("CPD-1.1.B", Q("cpd-levinthal", ST, "A chain of {{n}} residues is modelled with {{k}} allowed states for each of its two free backbone dihedrals. How many backbone conformations is that? Give log₁₀ of the count.",
        given={"n": {"pick": [50, 100, 150]}, "k": {"pick": [3, 4]}}, value="2*n*log(k, 10)", tex="\\log_{10}",
        verify="2*n*log(k)/log(10)", explain="Each residue contributes k² conformations, so the count is k^(2n): enumeration is impossible and the search must be guided")),
    ("CPD-1.2.A", facts("cpd-rotamer-lib", ST, [
        ("A rotamer library lists:", "The favoured side-chain χ combinations and their probabilities", "Every possible side-chain conformation on a fine grid", "Backbone fragments from known structures", "Partial charges for each atom"),
        ("A backbone-dependent rotamer library conditions those probabilities on:", "The residue's φ and ψ", "The solvent", "The chain length", "The temperature"),
        ("The energy term that scores the internal strain of the chosen rotamer is:", "fa_dun, from the Dunbrack rotamer probabilities", "fa_atr", "fa_sol", "fa_elec"),
        ("Treating side chains as a discrete rotamer set makes the packing problem:", "A discrete optimisation that can be precomputed as a pair-energy table", "Continuous and smooth", "Exactly solvable in all cases", "Independent of the backbone"),
        ("Which residue has no χ angles at all?", "Glycine", "Alanine", "Serine", "Proline"),
    ], "Discretising side chains is what makes design computationally tractable")),
    ("CPD-1.2.B", Q("cpd-rotamer-energy", ST, "At 298.15 K, a rotamer whose library probability is {{p}} times that of the most favoured rotamer costs how much energy (kcal/mol) in the fa_dun term?",
        given={"p": {"pick": [0.5, 0.1, 0.05, 0.01]}}, value="-0.0019872043*298.15*log(p)", tex="kcal/mol",
        verify=f"-({RT})*log(nsimplify(p))", explain="A probability maps to an energy by −kT ln p, so a tenfold rarer rotamer costs about 1.4 kcal/mol at room temperature")),
    ("CPD-2.1.A", facts("cpd-pose", RP, [
        ("A Pose holds the conformation primarily as:", "Internal coordinates (bond lengths, angles and dihedrals) with a fold tree", "A list of Cartesian coordinates only", "A sequence string only", "An energy value only"),
        ("Pose numbering runs:", "1 to N over every residue in the structure, ignoring chains and gaps", "The same as the PDB numbering", "From 0", "Separately for each chain"),
        ("A PDB file numbers residue 1A then 1B (an insertion code). In pose numbering these are:", "Two consecutive integers", "The same index", "Skipped", "Negative indices"),
        ("A gap in PDB numbering (a missing loop) means pose indices after the gap are:", "Smaller than the PDB numbers, because nothing was inserted for missing residues", "Identical to the PDB numbers", "Negative", "Undefined"),
        ("Before a structure is used, cleaning the PDB file matters because:", "Waters, ligands, alternate conformations and insertion codes can break the numbering or the chemistry", "The file is too large otherwise", "Energies cannot be computed at all", "Chains must be renamed"),
    ], "Pose indices are contiguous; PDB numbering is whatever the depositor chose")),
    ("CPD-2.1.B", Q("cpd-pose-index", RP, "A pose holds three chains of {{c1}}, {{c2}} and {{c3}} residues in that order. What is the pose index of residue {{j}} of chain C?",
        given={"c1": {"pick": [120, 145, 210]}, "c2": {"pick": [86, 99]}, "j": {"pick": [12, 40, 55]}, "c3": {"pick": [60]}},
        value="c1 + c2 + j", tex="index", final=True, verify="c1 + c2 + j",
        explain="Pose numbering is contiguous across chains, so the index is the offset of the preceding chains plus the position within the chain")),
    ("CPD-2.2.A", facts("cpd-centroid", RP, [
        ("In the centroid representation, each side chain is replaced by:", "A single pseudo-atom carrying its size and polarity", "Its Cα only", "Nothing at all", "A full rotamer"),
        ("Centroid mode is used for:", "Fast, aggressive search of conformational space", "Final ranking of near-native models", "Computing hydrogen bonds between side chains", "Scoring disulfides"),
        ("Full-atom mode is used for:", "Local refinement and final discrimination between models", "Global fold search", "Fragment insertion", "Nothing; it is obsolete"),
        ("The usual multi-resolution pattern is:", "Coarse-grained global search, then all-atom refinement", "All-atom search throughout", "Centroid only", "Random sampling then no refinement"),
        ("Side-chain hydrogen bonds cannot be scored in centroid mode because:", "The side-chain atoms are not represented", "The energy function has no hydrogen-bond term", "They do not matter for folding", "They are computed separately by MD"),
    ], "Two resolutions, two jobs: search wide and cheap, then refine and rank")),
    ("CPD-2.2.B", Q("cpd-centroid-speedup", RP, "A {{n}}-residue protein averages {{a}} atoms per residue in full atom and {{b}} interaction centres per residue in centroid. By what factor does the number of pairwise interactions fall?",
        given={"n": {"pick": [100, 150, 200]}, "a": {"pick": [19, 20]}, "b": {"pick": [5, 6]}}, value="(a/b)^2", tex="\\times",
        verify="Rational(a, b)**2", explain="Pair work scales with the square of the number of centres, which is why coarse-grained search is affordable")),
    ("CPD-3.1.A", facts("cpd-terms", EN, [
        ("fa_atr and fa_rep come from:", "The Lennard-Jones potential, split at its minimum into attractive and repulsive parts", "A statistical survey of structures", "The Dunbrack library", "A Coulomb sum"),
        ("fa_sol implements:", "Lazaridis–Karplus Gaussian-exclusion desolvation", "Lennard-Jones attraction", "Rotamer probabilities", "Disulfide geometry"),
        ("lk_ball_wtd adds what the isotropic solvation term misses:", "Direction: it penalises burying a polar atom where its ideal water sites are blocked", "Longer-range attraction", "Backbone torsion preferences", "Disulfide bonding"),
        ("fa_elec uses a distance-dependent dielectric that:", "Rises from a low value in the core toward that of bulk solvent", "Is fixed at 1", "Is fixed at 80", "Depends on the residue type only"),
        ("Which of these is a knowledge-based term fitted to structural statistics?", "p_aa_pp, the propensity of an amino acid at given φ/ψ", "fa_atr", "fa_sol", "fa_elec"),
        ("rama_prepro differs from a plain Ramachandran term by:", "Using a separate map when the next residue is proline", "Ignoring glycine", "Being physics-based", "Scoring side chains"),
        ("The repulsive part of the Lennard-Jones term is softened at very short distances to:", "Keep minimisation stable", "Match experiment exactly", "Speed up scoring", "Allow atom overlap in the final model"),
    ], "Physics-based terms carry weight 1.0; the statistical terms are fitted and weighted down")),
    ("CPD-3.1.B", Q("cpd-weighted-score", EN, "A residue's unweighted term energies are fa_atr {{atr}}, fa_rep {{rep}}, fa_sol {{sol}} and fa_dun {{dun}} kcal/mol. With weights 1.0, 0.55, 1.0 and 0.7, what is the weighted total?",
        given={"atr": {"pick": [-6.4, -8.2, -5.1]}, "rep": {"pick": [1.2, 3.4, 0.8]}, "sol": {"pick": [2.6, 4.1]}, "dun": {"pick": [0.9, 2.2]}},
        value="atr + 0.55*rep + sol + 0.7*dun", tex="kcal/mol",
        verify="nsimplify(atr) + Rational(55,100)*nsimplify(rep) + nsimplify(sol) + Rational(7,10)*nsimplify(dun)",
        explain="The score is a weighted linear sum; fa_rep at 0.55 and fa_dun at 0.7 are the published weights")),
    ("CPD-3.2.A", facts("cpd-ref", EN, [
        ("The reference energy (ref) stands for:", "A constant per amino-acid type approximating its unfolded-state energy", "The energy of the native structure", "A solvation correction", "The lowest score seen so far"),
        ("The reference energies were fitted to:", "Maximise recovery of native sequences in design", "Match gas-phase quantum calculations", "Reproduce melting temperatures", "Minimise run time"),
        ("For a fixed sequence, ref contributes:", "A constant offset that cancels in any comparison of conformations", "A different value per conformation", "Nothing at all", "The dominant term"),
        ("Without reference energies, design would:", "Favour whichever residues the other terms happen to score well, biasing composition", "Produce no sequence at all", "Be exactly correct", "Run faster but identically"),
        ("ref matters for design because design compares:", "Different sequences on the same backbone", "Different backbones with the same sequence", "Different temperatures", "Different force fields"),
    ], "ref is how a fixed-backbone score stands in for a folding free energy")),
    ("CPD-3.2.B", Q("cpd-ref-compare", EN, "Two designs on the same backbone score {{ea}} and {{eb}} kcal/mol before reference energies, with reference sums {{ra}} and {{rb}}. Which is predicted more stable, and by how much (kcal/mol, magnitude)?",
        cases=[{"ea": -310.5, "ra": -120.0, "eb": -305.0, "rb": -118.5},
               {"ea": -288.0, "ra": -101.5, "eb": -292.5, "rb": -108.0},
               {"ea": -415.2, "ra": -160.0, "eb": -410.0, "rb": -158.0},
               {"ea": -250.0, "ra": -95.0, "eb": -256.0, "rb": -96.5}],
        value="abs((ea - ra) - (eb - rb))", tex="kcal/mol",
        verify="Abs((nsimplify(ea) - nsimplify(ra)) - (nsimplify(eb) - nsimplify(rb)))",
        explain="Subtract each design's reference sum before comparing, or composition bias decides the winner")),
    ("CPD-3.3.A", facts("cpd-units", EN, [
        ("The current all-atom energy function is parameterised in:", "kcal/mol, rather than arbitrary Rosetta Energy Units", "Joules", "kT units", "Dimensionless units with no calibration"),
        ("For the paper's worked mutation, the computed stabilisation was about four times the measured value. The lesson:", "Trust the sign and the ranking more than the magnitude", "Energies are meaningless", "The experiment was wrong", "Always multiply by four"),
        ("Comparing total scores between two different proteins is:", "Not meaningful, because the total scales with size and composition", "The standard way to rank designs", "Exact", "Required before design"),
        ("A score of −450 for one structure and −300 for another of the same sequence and length means:", "The first is predicted more favourable under this function", "The first is more stable in reality, certainly", "Nothing can be said", "The second folds faster"),
        ("A large positive fa_rep in one residue usually means:", "A steric clash that should be relieved by repacking or minimisation", "A missing hydrogen bond", "Too much solvation", "A disulfide"),
    ], "The function is calibrated but approximate: rankings survive, absolute magnitudes often do not")),
    ("CPD-3.3.B", Q("cpd-term-decompose", EN, "A mutation changes fa_atr by {{d1}}, fa_rep by {{d2}}, fa_sol by {{d3}} and fa_elec by {{d4}} kcal/mol (unweighted). Using weights 1.0, 0.55, 1.0 and 1.0, what is the weighted ΔΔG?",
        given={"d1": {"pick": [-1.8, 0.9, -0.4]}, "d2": {"pick": [2.0, 0.5, 4.2]}, "d3": {"pick": [-2.2, 1.1]}, "d4": {"pick": [0.3, -0.7]}},
        value="d1 + 0.55*d2 + d3 + d4", tex="kcal/mol",
        verify="nsimplify(d1) + Rational(55,100)*nsimplify(d2) + nsimplify(d3) + nsimplify(d4)",
        explain="Decomposing by term tells you which interaction drove the change, which a single total never does")),
    ("CPD-4.1.A", facts("cpd-metropolis", SA, [
        ("A Monte Carlo move that raises the score by ΔE is accepted with probability:", "exp(−ΔE/kT)", "ΔE/kT", "1 always", "0 always"),
        ("Uphill moves are accepted so that the search can:", "Escape local minima that gradient descent cannot leave", "Raise the final energy", "Run faster", "Avoid computing the energy"),
        ("A move that lowers the score is accepted with probability:", "1", "exp(−ΔE/kT)", "0.5", "0"),
        ("Gradient-based minimisation finds:", "The nearest local minimum, which need not be the global one", "The global minimum always", "A random conformation", "The unfolded state"),
        ("Simulated annealing lowers the temperature during the run so that:", "Early moves explore widely and later moves settle into a minimum", "The energy function changes", "Fewer moves are needed", "The result is deterministic"),
    ], "Metropolis with a falling temperature is the search behind both folding and packing")),
    ("CPD-4.1.B", Q("cpd-accept-ratio", SA, "At {{t1}} K a Monte Carlo move raises the score by {{de}} kcal/mol. By what factor does its acceptance probability fall when the temperature drops to {{t2}} K?",
        given={"de": {"pick": [1.0, 2.0, 3.0]}, "t1": {"pick": [600, 500]}, "t2": {"pick": [300, 250]}},
        value="exp(-de/(0.0019872043*t2))/exp(-de/(0.0019872043*t1))", tex="\\times",
        verify="exp(-nsimplify(de)/(Rational('0.0019872043')*t2))/exp(-nsimplify(de)/(Rational('0.0019872043')*t1))",
        explain="The acceptance ratio is exp(−ΔE/kT); cooling multiplies the exponent, so the same uphill move becomes far less likely")),
    ("CPD-4.2.A", facts("cpd-packer", SA, [
        ("The packer optimises:", "Which rotamer sits at each allowed position, by simulated annealing over the discrete set", "Backbone dihedrals continuously", "The energy-function weights", "The sequence length"),
        ("Minimisation differs from packing in that it:", "Moves continuous degrees of freedom downhill rather than choosing discrete rotamers", "Changes the sequence", "Is stochastic", "Ignores the energy function"),
        ("Relax is used because:", "Alternating packing and minimisation settles a structure without letting it drift far", "It changes the sequence", "It is faster than packing alone", "It guarantees the global minimum"),
        ("A task that accidentally allows every position to design will:", "Change the whole sequence rather than only the intended positions", "Fail with an error", "Repack only", "Have no effect"),
        ("Packing requires a precomputed table of:", "One-body rotamer energies and two-body rotamer pair energies", "Backbone fragments", "Experimental ΔΔG values", "Solvent coordinates"),
    ], "Discrete packing and continuous minimisation do different jobs; relax interleaves them")),
    ("CPD-4.2.B", Q("cpd-pair-table", SA, "Packing {{n}} positions with {{k}} rotamers each needs how many two-body pair-energy entries (all position pairs, all rotamer combinations)?",
        given={"n": {"pick": [8, 10, 12]}, "k": {"pick": [20, 30, 50]}}, value="n*(n-1)/2*k^2", tex="entries", final=True,
        verify="Rational(n*(n-1), 2)*k**2", explain="n(n−1)/2 position pairs times k² rotamer combinations each: the table, not the annealing, is usually the cost")),
    ("CPD-5.1.A", facts("cpd-resfile", SQ, [
        ("A design specification sets, per position:", "Whether it is fixed, repacked only, or designed, and to which residues", "Only the backbone angles", "Only the chain identity", "The temperature"),
        ("'Repack only' at a position means:", "Its rotamer may change but its residue identity may not", "Its identity may change", "It is held completely fixed", "It is deleted"),
        ("Restricting a surface position to polar residues is a way to:", "Encode design intent the energy function would not impose on its own", "Speed up the packer only", "Avoid computing solvation", "Fix the backbone"),
        ("Positions not mentioned in a design specification are usually:", "Left at a default behaviour set by the file's header, which must be checked", "Designed to all 20 residues", "Deleted", "Frozen in all protocols regardless"),
        ("A common cause of a nonsense design is:", "A task that allowed design where repacking was intended", "Too low a temperature", "Using full-atom mode", "Scoring twice"),
    ], "The task specification is the design: it decides what the packer is even allowed to try")),
    ("CPD-5.1.B", Q("cpd-seq-space", SQ, "A design allows all 20 residues at {{n1}} positions and a restricted set of {{a}} residues at {{n2}} positions. How large is the sequence space? Give log₁₀.",
        given={"n1": {"pick": [10, 15, 20]}, "n2": {"pick": [8, 12]}, "a": {"pick": [6, 9]}},
        value="n1*log(20, 10) + n2*log(a, 10)", tex="\\log_{10}",
        verify="n1*log(20)/log(10) + n2*log(a)/log(10)",
        explain="Alphabets multiply across positions; restricting an alphabet is the cheapest way to shrink the search")),
    ("CPD-5.2.A", facts("cpd-scan", SQ, [
        ("A saturation point-mutation scan at one position tries:", "The 19 substitutions other than the wild-type residue", "All 20 residues including wild type twice", "Only conservative substitutions", "One random mutation"),
        ("Each candidate mutation is scored after:", "Local repacking (and usually minimisation) around the site", "No relaxation at all", "A full molecular dynamics run", "Changing the backbone"),
        ("A positive computed ΔΔG for a mutation means it is predicted:", "Destabilising", "Stabilising", "Neutral", "Faster folding"),
        ("The output of a scan should be treated as:", "A ranked shortlist to test, not a verdict", "A measurement", "Proof of stability", "A structure"),
        ("Running each mutation several times with different random seeds is done to:", "Separate a real energy difference from packing noise", "Change the sequence", "Avoid the reference energy", "Speed up the scan"),
    ], "A scan ranks candidates; the laboratory decides")),
    ("CPD-5.2.B", Q("cpd-scan-jobs", SQ, "A saturation scan covers {{n}} positions, with {{r}} independent trials per mutation. How many scoring jobs is that?",
        given={"n": {"pick": [12, 20, 35]}, "r": {"pick": [3, 5, 10]}}, value="19*n*r", tex="jobs", final=True, verify="19*n*r",
        explain="19 substitutions per position times the trials; the wild type is scored separately as the reference")),
    ("CPD-5.3.A", Q("cpd-recovery", SQ, "A redesign of {{n}} positions returns the native residue at {{h}} of them. What is the native sequence recovery (per cent), and how does it compare with the roughly 5 per cent expected by chance?",
        given={"n": {"pick": [120, 160, 200]}, "h": {"pick": [38, 52, 66]}}, value="100*h/n", tex="\\%",
        verify="Rational(100*h, n)", explain="Recovery well above the roughly 1-in-20 chance level is the standard check that an energy function and protocol are working")),
    ("CPD-5.3.B", facts("cpd-search-methods", SQ, [
        ("Dead-end elimination differs from simulated annealing in that it:", "Prunes rotamers that provably cannot be in the optimum, so it can return the true optimum", "Is stochastic", "Needs no energy function", "Is always faster"),
        ("Simulated annealing returns:", "A good solution with no proof of optimality", "The provable global optimum", "Every solution ranked", "The native sequence by construction"),
        ("A genetic algorithm searches by:", "Recombining and mutating a population of candidate sequences", "Pruning provably bad rotamers", "Following the energy gradient", "Enumerating all sequences"),
        ("Mean-field methods approximate the problem by:", "Replacing each position's neighbours with an average, then iterating to self-consistency", "Enumerating all pairs exactly", "Ignoring pair energies", "Using quantum mechanics"),
        ("Why is exact optimisation of the packing problem hard in general?", "It is combinatorial: the rotamer choices couple through pair energies", "The energy function is unknown", "Rotamers are continuous", "It needs more memory than exists for any protein"),
    ], "Know which method gives a guarantee and which gives a good answer fast")),
    ("CPD-6.1.A", facts("cpd-docking", IF, [
        ("The usual docking strategy is:", "A global rigid-body search followed by local high-resolution refinement", "High-resolution refinement only", "A single energy evaluation", "Molecular dynamics only"),
        ("A funnel plot shows:", "Score against RMSD to a reference, which should funnel toward low RMSD", "Score against time", "Energy against temperature", "Sequence against structure"),
        ("Fourier-transform-based docking is used because it:", "Scans translations and rotations of rigid bodies very fast", "Models side-chain flexibility", "Computes solvation exactly", "Guarantees the native pose"),
        ("If a funnel plot is flat, the likely conclusion is:", "The score function does not discriminate near-native from decoy poses here", "The native pose was found", "Sampling was sufficient", "The protein is rigid"),
        ("High-resolution refinement after docking adjusts:", "Side-chain rotamers and small rigid-body and backbone moves at the interface", "The sequence", "The energy-function weights", "The chain order"),
    ], "Search wide, refine locally, then ask whether the score can tell near-native from decoy")),
    ("CPD-6.1.B", Q("cpd-interface-energy", IF, "A complex scores {{ec}} kcal/mol; the two partners alone score {{ea}} and {{eb}}. What is the interface energy?",
        given={"ec": {"pick": [-520.4, -488.0, -605.2]}, "ea": {"pick": [-300.1, -275.5]}, "eb": {"pick": [-210.0, -195.7]}},
        value="ec - ea - eb", tex="kcal/mol", verify="nsimplify(ec) - nsimplify(ea) - nsimplify(eb)",
        explain="Interface energy is the complex minus its separated partners, each scored in the same function; a negative value is favourable binding under the model")),
    ("CPD-6.2.A", facts("cpd-ligand", IF, [
        ("Designing a ligand-binding pocket usually proceeds by:", "Placing the ligand, designing the surrounding shell, then repacking and minimising", "Designing the whole protein first, then adding the ligand", "Docking only", "Random mutation"),
        ("Designed enzymes generally fall short of natural ones in:", "Catalytic efficiency, because transition-state stabilisation is hard to design", "Expression level", "Thermal stability", "Molecular weight"),
        ("A ligand needs parameter files because:", "The energy function must know its atom types, charges and torsions", "The packer cannot read PDB files", "It has no structure", "Ligands are scored by a different program"),
        ("Designing a pocket complementary in shape is:", "Largely achievable with current methods", "Impossible", "Equivalent to designing catalysis", "Only possible with quantum mechanics"),
        ("Catalysis requires stabilising:", "The transition state more than the ground state", "The ground state more than the transition state", "Both equally", "Neither"),
    ], "Binding is designable; catalysis is the open problem")),
    ("CPD-6.2.B", facts("cpd-interface-design", IF, [
        ("One-sided interface design means:", "Designing a binder against a fixed natural surface you cannot change", "Redesigning both partners", "Docking without design", "Designing a monomer"),
        ("Two-sided (symmetric homo-oligomer) design is easier because:", "Both surfaces can be optimised together, and symmetry repeats one solution", "It needs no energy function", "Interfaces are smaller", "There is no backbone flexibility"),
        ("Antibody design remains hard largely because:", "It is one-sided against a chosen epitope and depends on flexible loops", "Antibodies are too small", "Their structures are unknown", "No energy function covers proteins"),
        ("Designed nanocages and higher-order assemblies exploit:", "Symmetry, so a small designed interface repeats into a large structure", "One-sided design", "Negative design only", "Ligand binding"),
    ], "How much of the interface you control decides how hard the problem is")),
    ("CPD-7.1.A", facts("cpd-denovo-backbone", DN, [
        ("Parametric backbone generation builds a fold from:", "A few geometric parameters, such as a coiled coil's radius and pitch", "Fragments of known structures", "A random walk", "An experimental structure"),
        ("Fragment assembly builds a backbone by:", "Monte Carlo insertion of short pieces taken from known structures", "Solving an analytic equation", "Diffusion from noise", "Enumerating all conformations"),
        ("Designing from distance constraints means:", "Specifying the contacts wanted and building a backbone that satisfies them", "Fixing every dihedral", "Using only parametric folds", "Docking two chains"),
        ("Parametric design suits which folds best?", "Regular, repetitive ones such as coiled coils and β-barrels", "Irregular loops", "Intrinsically disordered regions", "Membrane-spanning random coils"),
        ("A de novo designed protein is one whose:", "Sequence and structure were designed rather than taken from a natural protein", "Sequence is natural but refolded", "Structure was solved experimentally first", "Backbone came from a template"),
    ], "Three routes to a backbone: splice, constrain or parameterise")),
    ("CPD-7.1.B", Q("cpd-coiled-coil", DN, "An α-helical bundle has a superhelical pitch of {{pt}} Å and {{nr}} residues per superhelical turn. What is the rise along the superhelical axis per residue (Å)?",
        given={"pt": {"pick": [140, 180, 200]}, "nr": {"pick": [98, 102, 120]}}, value="pt/nr", tex="\\text{Å}",
        verify="Rational(pt, nr)", explain="Rise per residue is the pitch divided by the residues per turn: the parametric handle that sets a bundle's length")),
    ("CPD-7.2.A", facts("cpd-hbnet", DN, [
        ("Buried hydrogen-bond networks are designed before the rest of the core because:", "They are rare and later repacking would break them", "They are easy to find at any stage", "They do not affect the score", "The packer cannot score them"),
        ("A buried polar residue with no hydrogen-bond partner is penalised mainly through:", "The solvation terms, which charge for burying an unsatisfied polar atom", "fa_atr", "The reference energy", "fa_dun"),
        ("Hydrogen-bond networks are used in design to:", "Add specificity, so only the intended partner or conformation fits", "Increase hydrophobic burial", "Replace the energy function", "Reduce the sequence space to one"),
        ("Designs are sensitive to small backbone changes because:", "Side-chain packing and hydrogen bonds depend on geometry at sub-ångström scale", "The sequence changes", "The energy function is stochastic", "Backbones are rigid in reality"),
    ], "Find the rare polar network first, then build the core around it")),
    ("CPD-7.2.B", Q("cpd-gap-population", DN, "A switch is designed so the target conformation lies {{dg}} kcal/mol below the competing one at 298.15 K. What fraction of molecules occupy the target state (two states only)?",
        given={"dg": {"pick": [1.0, 2.0, 3.0, 4.0]}}, value="1/(1 + exp(-dg/(0.0019872043*298.15)))", tex="f",
        verify=f"1/(1 + exp(-nsimplify(dg)/({RT})))",
        explain="Two-state populations follow the Boltzmann factor: negative design is the work of opening this gap, and a few kcal/mol is enough to decide the ratio")),
    ("CPD-8.1.A", facts("cpd-predictor-inputs", ML, [
        ("A modern structure predictor's main inputs are:", "The sequence, a multiple-sequence alignment and optionally templates", "The sequence alone, always", "An experimental structure", "A force field"),
        ("pLDDT measures:", "Per-residue local confidence, higher being better", "Expected error between residue pairs", "Sequence identity to a template", "The energy of the model"),
        ("PAE measures:", "The expected error in the relative position of residue pairs", "Per-residue local confidence", "Alignment depth", "Rotamer probability"),
        ("To judge whether two confidently predicted domains are correctly placed relative to each other, read:", "The PAE map between them", "Their pLDDT values", "The MSA depth", "The sequence length"),
        ("A region with low pLDDT is often:", "Flexible or disordered, not necessarily a modelling failure", "Always a mistake in the sequence", "The best-resolved part", "A crystallisation artefact"),
        ("A shallow MSA usually means:", "Lower confidence, because the coevolution signal is weak", "Higher accuracy", "No effect on accuracy", "A faster, better prediction"),
    ], "Read both confidence metrics: one is local, one is about relative placement")),
    ("CPD-8.1.B", facts("cpd-coevolution", ML, [
        ("Coevolution predicts contacts because:", "Residues in contact tend to vary together across a family's sequences", "Contacts are listed in databases", "Sequence length determines structure", "Alignments encode coordinates"),
        ("Global statistical methods improved contact prediction by:", "Separating direct couplings from indirect, transitive ones", "Using longer sequences", "Ignoring the alignment", "Adding templates"),
        ("Families with few known homologues are hard because:", "The alignment is too shallow to estimate couplings", "Their structures are larger", "They have no contacts", "Templates are forbidden"),
        ("Deep learning changed structure prediction mainly by:", "Predicting inter-residue distances and geometry from alignments, then building and refining models", "Removing the need for sequences", "Replacing experiments entirely", "Making energy functions exact"),
    ], "The signal comes from the alignment, so its depth sets the ceiling")),
    ("CPD-8.2.A", facts("cpd-representations", ML, [
        ("A protein language model is trained on:", "Sequences alone, learning to predict masked or next tokens", "Coordinates only", "Contact maps", "Energies"),
        ("Embeddings from a pretrained language model are useful because:", "They transfer to downstream tasks with little labelled data", "They are the structure", "They replace the MSA entirely in all cases", "They are faster to compute than the sequence"),
        ("A graph neural network over a protein represents:", "Residues or atoms as nodes and their proximity as edges, passing messages along them", "The sequence as a string", "The energy as a scalar", "A 2D image"),
        ("Equivariance to rotation matters because:", "A rotated protein is the same protein, and predictions should transform accordingly", "Proteins never rotate", "It speeds up training only", "It removes the need for data"),
        ("Fine-tuning a large pretrained model with low-rank adapters is used to:", "Adapt it to a task while training far fewer parameters", "Make it larger", "Avoid using embeddings", "Replace the training data"),
    ], "Match the representation to the data: tokens for sequence, graphs for geometry")),
    ("CPD-8.2.B", facts("cpd-diffusion-pipeline", ML, [
        ("In the standard deep-learning design pipeline, the diffusion model produces:", "A backbone, by denoising from noise", "A sequence", "An energy function", "An experimental structure"),
        ("An inverse-folding model's job is to:", "Assign a sequence likely to fold to a given backbone", "Predict the structure of a sequence", "Generate a backbone", "Dock two proteins"),
        ("The structure predictor at the end of the pipeline is used to:", "Check that the designed sequence folds back to the intended backbone", "Generate the backbone", "Design the sequence", "Measure stability experimentally"),
        ("Motif scaffolding means:", "Generating a backbone that holds a specified functional motif in place", "Generating a backbone with no constraints", "Designing a sequence only", "Docking a ligand"),
        ("An all-atom diffusion model extends backbone generation by:", "Handling ligands and side-chain atoms, so small-molecule binders can be designed", "Removing the need for sequence design", "Working without any training data", "Predicting experimental yields"),
    ], "Generate a backbone, give it a sequence, then check the two agree")),
    ("CPD-8.3.A", Q("cpd-funnel-yield", ML, "A pipeline generates {{nb}} backbones, designs {{ns}} sequences for each, and {{p}} per cent of those pass the prediction filter. How many designs pass?",
        given={"nb": {"pick": [100, 250, 500]}, "ns": {"pick": [8, 16]}, "p": {"pick": [4, 12, 25]}},
        value="nb*ns*p/100", tex="designs", final=True, verify="Rational(nb*ns*p, 100)",
        explain="Stage pass fractions multiply, which is why generation is cheap and the filter decides the real cost")),
    ("CPD-8.3.B", facts("cpd-self-consistency", ML, [
        ("A self-consistency check in design means:", "The designed sequence's predicted structure matches the backbone it was designed for", "The design was expressed and folded", "Two laboratories agree", "The energy is negative"),
        ("Passing self-consistency does not establish that the design folds because:", "The design and prediction models can share the same blind spots", "The check is too strict", "RMSD cannot be computed", "Prediction is always wrong"),
        ("A common self-consistency criterion combines:", "Backbone RMSD to the target and the predictor's confidence", "Sequence identity to a natural protein", "Expression yield", "Melting temperature"),
        ("The step that turns a passing design into evidence is:", "Expressing and characterising it in the laboratory", "Running the pipeline again", "Raising the confidence cut-off", "Using a larger model"),
    ], "In silico agreement is a filter, not a result")),
    ("CPD-9.1.A", facts("cpd-experiments", VA, [
        ("The first experimental question about a design is usually:", "Does it express and stay soluble", "What is its catalytic rate", "What is its crystal structure", "What is its binding constant"),
        ("Thermal or chemical denaturation measures:", "Stability, as a melting temperature or a free energy of unfolding", "Binding affinity", "Catalytic efficiency", "Expression yield"),
        ("A high-resolution structure of a design is sought to:", "Confirm the intended fold at atomic detail", "Measure stability", "Measure affinity", "Replace the energy function"),
        ("For a stabilisation project, the number of designs tested is typically:", "A handful", "Thousands", "Millions", "None"),
        ("For a new binder against a chosen target, screening typically uses:", "A library with display and sequencing, because hit rates are low", "A single designed clone", "Only computational filters", "Crystallography first"),
    ], "Express, then stability, then structure, then function: and size the experiment to the hit rate")),
    ("CPD-9.1.B", Q("cpd-designs-needed", VA, "An expected hit rate of {{p}} per cent and a target of {{k}} successful binders means how many designs must be made and screened?",
        given={"p": {"pick": [0.5, 1, 2, 5]}, "k": {"pick": [3, 5, 10]}}, value="k*100/p", tex="designs",
        verify="nsimplify(k)*100/nsimplify(p)", explain="N = target/hit rate; at a fraction of a per cent, display libraries replace individually made clones")),
    ("CPD-9.2.A", facts("cpd-score-vs-alchemical", VA, [
        ("A score-function mutational scan is the right tool when you need:", "A cheap ranking of many candidate mutations", "A quantitative ΔΔG with an error bar", "An experimental measurement", "A binding constant"),
        ("An alchemical free-energy calculation is worth its cost when:", "A few candidates must be quantitative and defensible", "Hundreds must be ranked quickly", "No structure is available", "The sequence is unknown"),
        ("The key thing an alchemical calculation provides that a score does not:", "A statistical-mechanics estimate with a statistical uncertainty", "A faster answer", "A structure", "A sequence"),
        ("λ dynamics is particularly suited to design because it:", "Samples many substitutions at a site in one simulation rather than pairwise", "Needs no force field", "Avoids sampling entirely", "Replaces experiments"),
        ("A sensible division of labour is:", "Score-function scans to shortlist, alchemical calculations on the shortlist, then experiment", "Alchemical calculations on every mutation", "Experiment first, computation never", "Score functions only"),
    ], "Cheap and approximate to shortlist; rigorous and expensive to decide")),
    ("CPD-9.2.B", facts("cpd-open-problems", VA, [
        ("A design that expresses but is unstructured most often points at:", "Mis-balanced polar and nonpolar energetics, or an under-packed core", "A sequencing error, certainly", "The wrong expression host", "A crystallography failure"),
        ("Which is named as an open problem for current energy functions?", "Balancing polar against nonpolar contributions and treating solvation", "Computing Lennard-Jones terms", "Counting atoms", "Reading PDB files"),
        ("Backbone flexibility is a problem for fixed-backbone design because:", "The real protein relaxes away from the designed backbone, and the score assumed it would not", "Backbones never move", "It makes scoring faster", "It only affects prediction"),
        ("Loops are harder than helices and strands to design because:", "They are irregular, flexible and poorly described by regular geometry", "They contain no residues", "They have no energy", "They are always buried"),
    ], "The failures cluster where the model is thinnest: solvation balance and flexibility")),
]

# Second types (Nov 2026): every objective gets a second question in a different form — a scenario, a reverse, a
# scaling, or an ordering — so an objective is learned rather than drilled (the Types column in
# docs/frameworks/README.md is the measure).
ADD += [
    ("CPD-1.1.A", facts("cpd-dihedral-which", ST, [
        ("A design restricts a position to proline. Which backbone dihedral is most restricted as a result?", "φ, which the pyrrolidine ring pins near −60°", "ψ, which becomes free", "ω, which becomes free", "χ1, which is removed"),
        ("A loop residue has φ = +60°, ψ = +40°. The most likely residue is:", "Glycine, which tolerates positive φ", "Valine", "Isoleucine", "Tryptophan"),
        ("A designed helix is reported with ω near 0° at one residue. This means:", "A cis peptide bond, which is rare and worth checking", "A normal trans bond", "A broken chain", "A disulfide"),
        ("Replacing a glycine in a tight turn with alanine often fails because:", "Alanine cannot reach the backbone angles the turn requires", "Alanine is charged", "Alanine is too large to pack", "Alanine cannot hydrogen bond"),
    ], "Read the geometry backwards: the angles tell you which residues can sit there")),
    ("CPD-1.1.B", Q("cpd-levinthal-time", ST, "If a chain could sample {{r}} conformations per second, how many seconds (log₁₀) would it take to try all {{k}}^(2×{{n}}) backbone conformations?",
        given={"n": {"pick": [40, 60]}, "k": {"pick": [3]}, "r": {"pick": [1e12, 1e13]}},
        value="2*n*log(k, 10) - log(r, 10)", tex="\\log_{10} s", verify="2*n*log(k)/log(10) - log(nsimplify(r))/log(10)",
        explain="Even at picosecond sampling the exhaustive time dwarfs the age of the universe (about 10^17.6 s): folding and design must be guided, not exhaustive")),
    ("CPD-1.2.A", facts("cpd-rotamer-apply", ST, [
        ("A buried leucine is modelled in a rotamer that the library gives a low probability. The likely consequence in the score:", "An fa_dun penalty, flagging strain that repacking may relieve", "A lower fa_rep", "A better reference energy", "No effect on any term"),
        ("Two designs differ only in which rotamer a surface lysine takes. The score difference will be:", "Small, because surface side chains are weakly constrained", "Large and decisive", "Exactly zero by construction", "Dominated by the reference energy"),
        ("Increasing the number of rotamers sampled per position (a finer library) mainly costs:", "Time, because the pair-energy table grows with the square of the rotamer count", "Accuracy", "Memory only, with no time cost", "Nothing"),
        ("A residue whose χ angles are badly placed but whose identity is right would be fixed by:", "Repacking that position", "Designing that position", "Changing the backbone", "Lowering the temperature"),
    ], "fa_dun is where a strained side chain shows up, and repacking is the cure")),
    ("CPD-1.2.B", Q("cpd-rotamer-prob", ST, "A rotamer costs {{dg}} kcal/mol in fa_dun relative to the best rotamer at 298.15 K. What is its relative probability?",
        given={"dg": {"pick": [0.5, 1.0, 1.4, 2.0]}}, value="exp(-dg/(0.0019872043*298.15))", tex="p/p_0",
        verify=f"exp(-nsimplify(dg)/({RT}))", explain="The reverse of the energy–probability map: an energy penalty of about 1.4 kcal/mol is a tenfold drop in probability")),
    ("CPD-2.1.A", facts("cpd-pose-apply", RP, [
        ("A script mutates 'residue 45' using a PDB number on a structure with a missing loop. The risk is:", "It mutates the wrong residue, because pose and PDB numbering have diverged", "It raises an error immediately", "Nothing; the numbers always match", "It mutates two residues"),
        ("To select the interface residues of chain B reliably, the safest approach is:", "A residue selector on chain and distance, not hard-coded indices", "Hard-coded pose indices", "Hard-coded PDB numbers", "The sequence string"),
        ("A structure is loaded with its crystallographic waters still present. In the pose these appear as:", "Additional residues that shift the indices of anything after them", "Nothing at all", "Part of the protein chain", "Ligand parameters"),
        ("The fold tree matters because it determines:", "How a change in one dihedral propagates through the rest of the structure", "The energy function weights", "The sequence", "The rotamer library"),
    ], "Hard-coded indices are the classic bug; select by property instead")),
    ("CPD-2.1.B", Q("cpd-pose-reverse", RP, "A pose holds two chains of {{c1}} and {{c2}} residues. Pose index {{idx}} falls in which chain, at which position within it? Give the position within the chain.",
        cases=[{"c1": 120, "c2": 86, "idx": 150}, {"c1": 145, "c2": 99, "idx": 60}, {"c1": 210, "c2": 60, "idx": 240}, {"c1": 98, "c2": 110, "idx": 190}],
        value="idx > c1 ? idx - c1 : idx", tex="position", final=True, verify="idx - c1 if idx > c1 else idx",
        explain="Subtract the preceding chain lengths to go from a pose index back to a chain and position")),
    ("CPD-2.2.A", facts("cpd-resolution-pick", RP, [
        ("A protocol must search widely for a fold from an extended chain. The right representation is:", "Centroid, for speed", "Full atom throughout", "Full atom with a fine rotamer library", "Neither; use docking"),
        ("Near the end of a protocol, two models differ by 1 Å and must be ranked. The right representation is:", "Full atom, which can resolve packing and hydrogen bonds", "Centroid", "Sequence only", "Either; they rank the same"),
        ("A centroid-mode score cannot distinguish two models that differ only in:", "Side-chain rotamer placement", "Overall fold", "Radius of gyration", "Chain breaks"),
        ("Switching from centroid to full atom mid-protocol requires:", "Rebuilding side chains and repacking them", "Nothing; atoms are already there", "A new energy function from scratch", "Changing the sequence"),
    ], "Pick the resolution by what the current step must distinguish")),
    ("CPD-2.2.B", Q("cpd-atom-count", RP, "A {{n}}-residue protein averages {{a}} atoms per residue. How many interacting atom pairs are there (all pairs, no cutoff)?",
        given={"n": {"pick": [100, 150]}, "a": {"pick": [19, 20]}}, value="(n*a)*(n*a - 1)/2", tex="pairs", final=True,
        verify="Rational(n*a*(n*a - 1), 2)", explain="Pair counts grow as the square, which is why cutoffs and coarse-graining exist")),
    ("CPD-3.1.A", facts("cpd-term-diagnose", EN, [
        ("A designed core shows a large positive fa_rep at one position. The diagnosis:", "Two atoms are too close; repack or minimise that region", "A polar group is buried without a partner", "A rotamer is strained", "A disulfide is misgeometried"),
        ("A buried asparagine with no hydrogen-bond partner will be penalised mainly by:", "The solvation terms, including the anisotropic polar term", "fa_atr", "omega", "The reference energy"),
        ("A residue modelled with φ/ψ in a disallowed region will be penalised by:", "rama_prepro", "fa_sol", "fa_elec", "dslf_fa13"),
        ("Two oppositely charged side chains placed in contact at the surface affect which term most?", "fa_elec", "fa_dun", "omega", "pro_close"),
        ("A cysteine pair modelled with poor disulfide geometry is penalised by:", "dslf_fa13", "fa_intra_rep", "p_aa_pp", "yhh_planarity"),
    ], "Each failure mode has a term that reports it: the decomposition is the diagnostic")),
    ("CPD-3.1.B", Q("cpd-weight-change", EN, "A structure has unweighted fa_rep of {{rep}} kcal/mol. A protocol temporarily softens repulsion by scaling the fa_rep weight from 0.55 to {{w}}. By how much (kcal/mol) does the weighted total fall?",
        given={"rep": {"pick": [12.0, 25.0, 40.0]}, "w": {"pick": [0.02, 0.1, 0.275]}}, value="(0.55 - w)*rep", tex="kcal/mol",
        verify="(Rational(55,100) - nsimplify(w))*nsimplify(rep)",
        explain="Ramping the repulsive weight down lets clashed structures relax before the full weight is restored, which is what the relax protocol does")),
    ("CPD-3.2.A", facts("cpd-ref-apply", EN, [
        ("A design returns far more alanines than a natural protein of the same fold. A likely cause:", "The reference energies are mis-balanced for this problem, or packing is too loose", "fa_atr is too weak", "The pose numbering is wrong", "The rotamer library is too fine"),
        ("Changing the reference energy of tryptophan upward (less favourable) would make design:", "Choose tryptophan less often", "Choose tryptophan more often", "Ignore tryptophan's other terms", "Fail to run"),
        ("Two conformations of one fixed sequence are compared. Including ref changes the ranking by:", "Nothing; it is the same constant in both", "Reversing it", "A random amount", "Removing the solvation term"),
        ("Native sequence recovery is the natural objective for fitting ref because:", "It directly measures whether design reproduces sequences nature chose for known folds", "It is easy to compute and unrelated to design", "It measures stability", "It measures binding"),
    ], "ref is a design knob, not a scoring one: it only moves when sequences are compared")),
    ("CPD-3.2.B", Q("cpd-ddg-mutation", EN, "A point mutation changes the folded-state score from {{e1}} to {{e2}} kcal/mol, while the reference sum changes from {{r1}} to {{r2}}. What is the predicted ΔΔG of folding?",
        cases=[{"e1": -310.0, "e2": -306.5, "r1": -120.0, "r2": -118.8},
               {"e1": -288.4, "e2": -291.0, "r1": -101.5, "r2": -102.9},
               {"e1": -415.0, "e2": -413.2, "r1": -160.0, "r2": -159.1},
               {"e1": -250.6, "e2": -254.0, "r1": -95.0, "r2": -96.2}],
        value="(e2 - r2) - (e1 - r1)", tex="kcal/mol",
        verify="(nsimplify(e2) - nsimplify(r2)) - (nsimplify(e1) - nsimplify(r1))",
        explain="Both states move, so subtract each one's reference sum first; a positive result is destabilising")),
    ("CPD-3.3.A", facts("cpd-trust-score", EN, [
        ("A scan predicts ΔΔG values of +4.9, +0.3 and −2.1 kcal/mol. The most defensible statement:", "The third is predicted stabilising and the first destabilising; the ordering is more reliable than the numbers", "All three magnitudes are accurate to 0.1 kcal/mol", "Nothing can be concluded", "The second is exactly neutral"),
        ("Two proteins of different length are scored at −620 and −410. Concluding the first is more stable is:", "Invalid, because totals scale with size and composition", "Valid", "Valid only in centroid mode", "Valid if both are designs"),
        ("To compare a design against its natural parent fairly, you should compare:", "Score differences for the same backbone and length, or a per-residue score", "Raw totals", "Sequence lengths", "Run times"),
        ("A computed ΔΔG four times the measured value is:", "Within the behaviour the energy-function paper itself reports", "Evidence the software is broken", "Impossible", "Proof the experiment was wrong"),
    ], "Compare like with like, and trust rankings over magnitudes")),
    ("CPD-3.3.B", Q("cpd-per-residue", EN, "A {{n}}-residue design totals {{et}} kcal/mol and its natural parent of {{m}} residues totals {{ep}}. What is the difference in score per residue (kcal/mol per residue, design minus parent)?",
        given={"n": {"pick": [96, 120]}, "m": {"pick": [104, 135]}, "et": {"pick": [-290.0, -355.0]}, "ep": {"pick": [-318.0, -402.0]}},
        value="et/n - ep/m", tex="kcal/mol/res", verify="nsimplify(et)/n - nsimplify(ep)/m",
        explain="Normalising by length is the crude way to compare proteins of different size, and it is still only indicative")),
    ("CPD-4.1.A", facts("cpd-mc-apply", SA, [
        ("A Monte Carlo run accepts almost every move. The temperature is:", "Too high: the search is wandering rather than converging", "Too low", "Exactly right", "Irrelevant"),
        ("A Monte Carlo run accepts almost no moves. The temperature is:", "Too low: the search is stuck in one basin", "Too high", "Exactly right", "Irrelevant"),
        ("A protocol reports the lowest-scoring structure it ever visited, not the last one. This is because:", "The last accepted move may be uphill", "The last structure is always the best", "Scoring is stochastic", "Minimisation runs afterwards"),
        ("Running the same Monte Carlo protocol twice with different seeds gives different results. This means:", "The search is stochastic and should be run many times", "The protocol is broken", "The energy function changed", "The structure is wrong"),
    ], "Acceptance rate is the dial that tells you whether the search is working")),
    ("CPD-4.1.B", Q("cpd-metropolis-de", SA, "At {{t}} K, what energy increase (kcal/mol) does a Monte Carlo move need for its acceptance probability to be exactly {{p}}?",
        given={"t": {"pick": [300, 500, 1000]}, "p": {"pick": [0.5, 0.1, 0.05]}}, value="-0.0019872043*t*log(p)", tex="kcal/mol",
        verify="-Rational('0.0019872043')*t*log(nsimplify(p))",
        explain="Invert the Metropolis rule: ΔE = −kT ln P, which is how an annealing schedule is chosen for a given move size")),
    ("CPD-4.2.A", facts("cpd-protocol-order", SA, [
        ("A structure has a steric clash after a mutation. The first step is:", "Repack the neighbourhood, then minimise", "Minimise only, with full repulsive weight", "Design the whole protein", "Dock it to a partner"),
        ("Minimising without repacking after a large mutation tends to:", "Get trapped, because the wrong rotamer cannot be reached by small continuous moves", "Find the global minimum", "Change the sequence", "Be faster and better"),
        ("Relax restrains the structure to its starting coordinates so that:", "It settles without drifting away from the experimental or designed geometry", "It reaches a lower score than any other protocol", "The sequence stays fixed", "Packing is skipped"),
        ("The usual order in a design protocol is:", "Set the task, pack (design), minimise, then rescore", "Minimise, then set the task", "Rescore, then pack", "Design after minimising only"),
    ], "Discrete first, continuous second: the packer can reach what minimisation cannot")),
    ("CPD-4.2.B", Q("cpd-pair-table-growth", SA, "Packing uses {{k1}} rotamers per position. By what factor does the pair-energy table grow if the library is refined to {{k2}} rotamers per position?",
        given={"k1": {"pick": [20, 25]}, "k2": {"pick": [40, 75, 100]}}, value="(k2/k1)^2", tex="\\times",
        verify="Rational(k2, k1)**2", explain="Pair entries go as k², so doubling the rotamers quadruples the table: the scaling that limits how fine a library can be")),
    ("CPD-5.1.A", facts("cpd-task-scenario", SQ, [
        ("You want to redesign only the hydrophobic core and leave the surface untouched. The task should:", "Allow design at the buried positions and repacking at most others", "Allow design everywhere", "Fix every position", "Allow design on the surface only"),
        ("A ligand must stay exactly where it is while the pocket is designed. The ligand should be:", "Fixed, with design allowed in the shell around it", "Designed", "Repacked", "Deleted"),
        ("You want to avoid cysteines anywhere in a design. The right mechanism is:", "A restriction in the task that removes cysteine from the allowed alphabet", "Post-hoc filtering only", "A lower temperature", "A different energy function"),
        ("Interface positions on both partners should be designable, and everything else only repacked. This is:", "Two-sided interface design specified through the task", "One-sided design", "Docking", "A mutational scan"),
    ], "Design intent that the score cannot express belongs in the task")),
    ("CPD-5.1.B", Q("cpd-alphabet-cut", SQ, "A design has {{n}} positions. By what factor (log₁₀) does restricting every position from all 20 residues to {{a}} shrink the sequence space?",
        given={"n": {"pick": [15, 20, 30]}, "a": {"pick": [5, 8, 10]}}, value="n*log(20/a, 10)", tex="\\log_{10}",
        verify="n*log(Rational(20, a))/log(10)",
        explain="Restricting the alphabet cuts the space exponentially in the number of positions: the cheapest lever on search difficulty")),
    ("CPD-5.2.A", facts("cpd-scan-read", SQ, [
        ("A scan ranks a mutation at +0.2 kcal/mol with a run-to-run spread of 0.6 kcal/mol. The honest reading:", "Indistinguishable from neutral given the noise", "Clearly destabilising", "Clearly stabilising", "An error in the protocol"),
        ("Three mutations score −2.4, −2.3 and −2.2 kcal/mol. The right next step:", "Treat them as a tied shortlist and pick by other criteria", "Choose the first as clearly best", "Discard all three", "Rerun only the third"),
        ("A scan is run without repacking the neighbourhood after each mutation. The result will:", "Over-penalise larger residues that would have been accommodated", "Be more accurate", "Be unchanged", "Favour larger residues"),
        ("Mutations at buried positions tend to show:", "Larger score changes than surface positions", "Smaller score changes than surface positions", "No score change", "Only positive changes"),
    ], "Read a scan against its own noise, not as a measurement")),
    ("CPD-5.2.B", Q("cpd-scan-positions", SQ, "A saturation scan produced {{j}} scoring jobs with {{r}} trials per mutation. How many positions were scanned?",
        given={"j": {"pick": [1140, 2280, 3800]}, "r": {"pick": [3, 5, 10]}}, value="j/(19*r)", tex="positions", final=True,
        verify="Rational(j, 19*r)", explain="The reverse of the job count: jobs = 19 × positions × trials")),
    ("CPD-5.3.A", Q("cpd-recovery-compare", SQ, "Protocol A recovers the native residue at {{a}} of {{n}} positions; protocol B at {{b}} of the same {{n}}. What is the difference in recovery (percentage points)?",
        given={"n": {"pick": [150, 200]}, "a": {"pick": [48, 62]}, "b": {"pick": [55, 71, 80]}}, value="100*(b - a)/n", tex="pp",
        verify="Rational(100*(b - a), n)",
        explain="Recovery differences are how energy functions and protocols are compared, with chance at roughly 5 per cent")),
    ("CPD-5.3.B", facts("cpd-method-pick", SQ, [
        ("A benchmark needs the provably optimal rotamer assignment for a small problem. Use:", "Dead-end elimination, which prunes provably non-optimal rotamers", "Simulated annealing", "A genetic algorithm", "Mean field"),
        ("A large design must be run thousands of times within a few hours. Use:", "Simulated annealing, which is fast and good enough", "Exhaustive enumeration", "Dead-end elimination on the full problem", "Quantum mechanics"),
        ("A stochastic optimiser returns a different sequence on each run. The right response:", "Run it many times and look at the consensus and the score distribution", "Trust the first run", "Lower the temperature to zero", "Switch to a single evaluation"),
        ("Dead-end elimination becomes impractical when:", "The problem is large enough that few rotamers can be pruned", "The energy function is physics-based", "Rotamers are discrete", "The backbone is fixed"),
    ], "Choose by whether you need a guarantee or a throughput")),
    ("CPD-6.1.A", facts("cpd-docking-read", IF, [
        ("A docking funnel plot shows the lowest scores at 8 Å RMSD and nothing low near 1 Å. The likely reading:", "Either sampling never reached the native pose or the score prefers a decoy", "The native pose was found", "The protein is rigid", "The partners do not bind"),
        ("Docking two proteins known to bind, the search returns many poses with similar scores. This suggests:", "The score does not discriminate, so other information is needed", "All poses are correct", "The complex is symmetric", "The run was too long"),
        ("Rigid-body docking will miss a complex that requires:", "Substantial backbone change on binding (induced fit)", "Side-chain repacking", "A translation", "A rotation"),
        ("Local refinement is appropriate when:", "An approximate pose is already known", "Nothing is known about the pose", "The partners are unknown", "The sequence is unknown"),
    ], "A funnel is a statement about the score function as much as about the pose")),
    ("CPD-6.1.B", Q("cpd-interface-reverse", IF, "A complex has an interface energy of {{di}} kcal/mol. Its partners alone score {{ea}} and {{eb}}. What does the complex score?",
        given={"di": {"pick": [-18.5, -32.0, -45.2]}, "ea": {"pick": [-300.1, -275.5]}, "eb": {"pick": [-210.0, -195.7]}},
        value="di + ea + eb", tex="kcal/mol", verify="nsimplify(di) + nsimplify(ea) + nsimplify(eb)",
        explain="The reverse of the interface calculation, and the check that the three numbers in a report are consistent")),
    ("CPD-6.2.A", facts("cpd-pocket-scenario", IF, [
        ("A designed pocket binds the ligand but shows no catalysis. The most likely reason:", "The design stabilises the ground state without stabilising the transition state more", "The ligand does not fit", "The protein is unstable", "The pocket is too polar"),
        ("A small-molecule ligand has no parameter file. Before any design you must:", "Generate its parameters (atom types, charges, torsions) for the energy function", "Score it anyway", "Delete it", "Replace it with water"),
        ("A designed pocket buries a charged ligand group with no counter-charge. Expect:", "A large desolvation penalty and probably weak binding", "Stronger binding", "No effect", "A clash only"),
        ("Designing shape complementarity without chemical complementarity usually gives:", "Binding that is weak or non-specific", "Catalysis", "A stable fold", "Nothing at all"),
    ], "Shape is the easy half; chemistry and the transition state are the hard halves")),
    ("CPD-6.2.B", facts("cpd-interface-scenario", IF, [
        ("A project must design a binder to a fixed viral surface protein. This is:", "One-sided design, the harder case", "Two-sided design", "A mutational scan", "Docking only"),
        ("A project designs a new homodimer interface from scratch. This is:", "Two-sided and symmetric, the easier case", "One-sided", "Negative design only", "Ligand design"),
        ("Designing a protein that binds target A but not its close homologue B requires:", "Negative design against B as well as positive design for A", "Positive design for A alone", "A finer rotamer library", "A longer simulation"),
        ("A designed nanocage uses symmetry so that:", "One designed interface repeats into a large assembly", "No interface is needed", "The sequence is shorter", "No energy function is needed"),
    ], "Count how many surfaces you control, and whether you must also design against something")),
    ("CPD-7.1.A", facts("cpd-backbone-pick", DN, [
        ("A project wants an idealised four-helix bundle with a specified radius. The right route:", "Parametric generation from the bundle's geometric parameters", "Fragment assembly", "Diffusion from noise, necessarily", "Template-based modelling"),
        ("A project wants a novel fold with an irregular mixed topology. Parametric equations are:", "Poorly suited, because the fold is not described by a few parameters", "The best choice", "Equivalent to fragments", "Required"),
        ("Fragment assembly biases designs toward:", "Local geometries that occur in known structures", "Entirely novel local geometries", "Extended chains", "Membrane folds"),
        ("A specified set of residue–residue contacts is best imposed by:", "Constraints added to the score during backbone generation", "Parametric equations", "A finer rotamer library", "Negative design"),
    ], "Match the generation method to how regular the target fold is")),
    ("CPD-7.1.B", Q("cpd-coiled-coil-length", DN, "A designed bundle must span {{ln}} Å along its superhelical axis. At a rise of {{ri}} Å per residue, how many residues per helix is that?",
        given={"ln": {"pick": [60, 75, 90]}, "ri": {"pick": [1.45, 1.5]}}, value="ln/ri", tex="residues",
        verify="nsimplify(ln)/nsimplify(ri)",
        explain="The reverse of the parametric calculation: the length you want fixes the helix length you must design")),
    ("CPD-7.2.A", facts("cpd-hbnet-scenario", DN, [
        ("A design with a buried hydrogen-bond network is relaxed afterwards and the network breaks. The fix:", "Constrain or fix the network residues during later steps", "Remove the network", "Lower the repulsive weight permanently", "Redesign the surface"),
        ("A designed core is entirely hydrophobic with no polar network. Expect:", "A stable fold but little conformational specificity between similar folds", "Catalysis", "Instability, necessarily", "No expression"),
        ("Two designs differ by 0.5 Å in backbone geometry and one loses its network. This illustrates:", "How sensitive designed polar networks are to backbone detail", "That backbones are rigid", "That the score function is wrong", "That the sequence changed"),
        ("Buried polar networks add specificity because:", "Only a partner or conformation that completes the network pays no desolvation penalty", "They increase hydrophobic burial", "They stiffen the backbone", "They lower the reference energy"),
    ], "A network is specificity, and it is fragile: protect it through the rest of the protocol")),
    ("CPD-7.2.B", Q("cpd-gap-needed", DN, "A designed switch must keep at least {{f}} per cent of molecules in the target state at 298.15 K (two states). What energy gap (kcal/mol) is needed?",
        given={"f": {"pick": [90, 95, 99]}}, value="0.0019872043*298.15*log(f/(100-f))", tex="kcal/mol",
        verify=f"({RT})*log(Rational(f, 100 - f))",
        explain="Invert the two-state Boltzmann population: 90:10 needs about 1.3 kcal/mol and 99:1 about 2.7, which is why negative design targets a few kcal/mol")),
    ("CPD-8.1.A", facts("cpd-confidence-scenario", ML, [
        ("A prediction has pLDDT above 90 throughout two domains but a high PAE between them. The reading:", "Each domain is confidently modelled but their relative placement is not", "The whole model is wrong", "The whole model is right", "The sequence is wrong"),
        ("A 40-residue terminal segment has pLDDT near 30 while the rest is above 85. The likely reading:", "That segment is probably flexible or disordered", "The whole prediction failed", "The segment is the best part", "The MSA is too deep"),
        ("A designed sequence's prediction returns high pLDDT and low RMSD to the design target. This shows:", "The predictor agrees with the design, which is a filter and not evidence of folding", "The design folds in vitro", "The design is catalytically active", "The design is stable at high temperature"),
        ("Two predictions of a complex disagree about the interface. A useful next check:", "The PAE across the interface in each prediction", "The sequence length", "The pLDDT average only", "The run time"),
    ], "Local confidence and relative-placement confidence answer different questions")),
    ("CPD-8.1.B", facts("cpd-msa-scenario", ML, [
        ("A target protein is from a family with only a handful of known homologues. Expect:", "Lower prediction confidence, because the coevolution signal is weak", "Better predictions", "No effect", "A faster prediction only"),
        ("A deep MSA of thousands of diverse sequences usually gives:", "Stronger contact signals and more confident predictions", "Weaker predictions", "No change", "Only speed benefits"),
        ("Indirect (transitive) couplings in a naive contact analysis cause:", "False contacts between residues that are each coupled to a common third residue", "Missing contacts only", "Perfect accuracy", "No problem"),
        ("A designed de novo sequence has no natural homologues at all. For prediction this means:", "There is no MSA signal, so single-sequence performance is what matters", "Prediction is impossible", "Prediction is more accurate", "The design cannot be scored"),
    ], "Alignment depth is the hidden input, and de novo designs have none")),
    ("CPD-8.2.A", facts("cpd-representation-pick", ML, [
        ("A task must predict a per-residue property from sequence alone with few labels. A good approach:", "Fine-tune or probe a pretrained protein language model's embeddings", "Train a convolutional network from scratch on the labels", "Use a diffusion model", "Use docking"),
        ("A task must score the geometry of residue contacts in a 3D structure. A good approach:", "A graph network over residues or atoms with message passing", "A sequence language model alone", "A diffusion model alone", "A rotamer library"),
        ("Making a model equivariant rather than retraining on rotated copies is preferred because:", "It builds the symmetry in rather than hoping the model learns it", "It is always faster to train", "It needs no data", "It removes the need for validation"),
        ("Attention in a sequence model lets a residue's representation depend on:", "Other residues anywhere in the sequence, weighted by learned relevance", "Only its immediate neighbours", "Its coordinates", "Its rotamer"),
    ], "The representation encodes what you believe matters: order, or geometry")),
    ("CPD-8.2.B", facts("cpd-pipeline-order", ML, [
        ("In the design pipeline, which order is correct?", "Generate a backbone, design a sequence for it, then predict the structure of that sequence", "Design a sequence, generate a backbone, then predict", "Predict, then generate, then design", "Design and predict only"),
        ("You must design a binder that holds a known functional motif in a new scaffold. Use:", "Motif scaffolding in the generative step", "Unconditional generation", "A mutational scan", "Docking alone"),
        ("A small-molecule binder needs atoms of the ligand represented during generation. That requires:", "An all-atom generative model rather than a backbone-only one", "A backbone-only model", "A sequence model", "A rotamer library"),
        ("Designing many sequences per generated backbone is done because:", "Backbone generation is cheap and sequence quality varies, so the filter needs candidates", "Each backbone has exactly one valid sequence", "It is required by the model", "It speeds up generation"),
    ], "Each stage answers a different question, and the order is not interchangeable")),
    ("CPD-8.3.A", Q("cpd-funnel-reverse", ML, "A pipeline must deliver {{k}} designs that pass its filter, designing {{ns}} sequences per backbone with a {{p}} per cent pass rate. How many backbones must be generated?",
        given={"k": {"pick": [20, 50, 96]}, "ns": {"pick": [8, 16]}, "p": {"pick": [4, 10, 25]}},
        value="k*100/(ns*p)", tex="backbones", verify="Rational(k*100, ns*p)",
        explain="Work the funnel backwards from the number of designs you intend to order")),
    ("CPD-8.3.B", facts("cpd-evidence-level", ML, [
        ("Which of these is experimental evidence that a design works?", "It expresses, is soluble, and a measured melting curve shows a folded state", "It passes a self-consistency filter", "Its predicted structure has high pLDDT", "Its score is very negative"),
        ("Two models in a pipeline were trained on overlapping data. Their agreement therefore:", "May reflect shared bias rather than correctness", "Proves correctness", "Is irrelevant", "Means one is redundant"),
        ("A reasonable use of a self-consistency filter is to:", "Reduce thousands of candidates to the ones worth making", "Replace laboratory characterisation", "Measure stability", "Prove function"),
        ("Reporting a design as 'validated' after only computational filters is:", "Overclaiming; the filters rank candidates", "Standard and correct", "Required by the field", "A statement about stability"),
    ], "Computational agreement is a filter; evidence comes from the bench")),
    ("CPD-9.1.A", facts("cpd-experiment-order", VA, [
        ("A design does not express at all. The next step is:", "Revisit solubility and expression (codon usage, tags, host) before concluding the design is wrong", "Measure its melting temperature", "Attempt crystallography", "Measure catalysis"),
        ("A design expresses and is soluble but shows no cooperative unfolding transition. The likely reading:", "It is probably not folded into a well-defined structure", "It is highly stable", "It is catalytically active", "It is a crystallography failure"),
        ("Deciding oligomeric state before interpreting a binding assay matters because:", "An unintended oligomer changes the apparent stoichiometry and affinity", "It is required for expression", "It sets the melting temperature", "It determines the sequence"),
        ("A high-resolution structure is most valuable when:", "You need to know whether the designed geometry was actually achieved", "You only need stability", "You only need expression yield", "You need the sequence"),
    ], "Work up the ladder: expression, fold, state, structure, function")),
    ("CPD-9.1.B", Q("cpd-hit-rate", VA, "A campaign made and screened {{nn}} designs and obtained {{k}} successes. What hit rate (per cent) should the next campaign assume?",
        given={"nn": {"pick": [200, 1000, 5000]}, "k": {"pick": [2, 7, 25]}}, value="100*k/nn", tex="\\%",
        verify="Rational(100*k, nn)",
        explain="The reverse of sizing a campaign: a measured hit rate is the only honest basis for the next one's size")),
    ("CPD-9.2.A", facts("cpd-method-choice-scenario", VA, [
        ("Three hundred candidate mutations must be narrowed down this week. Use:", "A score-function scan", "Alchemical free-energy calculations on all of them", "Experiments on all of them", "A structure prediction of each"),
        ("Four shortlisted mutations must be reported with uncertainties in a paper. Use:", "Alchemical free-energy calculations", "A score-function scan alone", "Docking", "A language model"),
        ("A site must be saturated across all 20 amino acids with rigorous free energies. The method suited to this is:", "λ dynamics, which samples many substituents in one simulation", "Pairwise FEP on all 190 pairs", "A single score evaluation", "A structure prediction"),
        ("A score-function scan and an alchemical calculation disagree on a mutation's sign. The better evidence is:", "The alchemical calculation, if its convergence diagnostics are sound", "The score function, always", "Neither; the question is unanswerable", "Whichever is faster"),
    ], "Cheap methods to shortlist, rigorous methods to decide, experiment to settle")),
    ("CPD-9.2.B", facts("cpd-failure-diagnose", VA, [
        ("A design is stable but binds nothing. The most likely gap:", "The interface chemistry, which is harder than the fold", "The reference energies", "The pose numbering", "The rotamer library"),
        ("A design's crystal structure shows the intended fold but with a shifted helix. This points at:", "Backbone flexibility that fixed-backbone design did not anticipate", "A sequencing error", "A score-function bug", "A failed expression"),
        ("Designs that are over-stabilised and completely rigid may fail at:", "Function, which often needs motion", "Expression", "Folding", "Crystallisation"),
        ("A designed loop is disordered in the structure. The usual explanation:", "Loops are irregular and flexible, and are poorly captured by the score", "Loops are always buried", "Loops have no energy terms", "The loop sequence was wrong"),
    ], "Most design failures sit where the model is thinnest, not where the code is wrong")),
]
