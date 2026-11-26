"""Computational Protein Design unit 10, "Specialised modelling and scale" (Nov 2026): the PyRosetta workshop
chapters that unit 1-9 left unanswered — loop modelling (ch. 9), symmetry (10), density (11), antibodies (12),
membrane proteins (15) and parallel, reproducible runs (16) — plus the refinement protocol (5.2) and Cartesian ligand
docking (8.2). EXISTING adds the jhu-545614 course topics, which were registered as a scope check and never cited.

Sources: the workshop table of contents (read in full, notebooks not run) and Kuhlman & Bradley on antibody and
interface design. Where a chapter's method could not be read beyond its title, the item stays at the level the title
supports — what the method is for and what it must preserve — rather than inventing parameters."""
from opl_dsl import Q

FILE, FRAMEWORK = "cpd-specialised", "protein-design"
PRACTICE = "P2"
MC = ["{{o1}}", "{{o2}}", "{{o3}}", "{{o4}}"]
SA, IF, DN, VA, RP = "design.sampling", "design.interfaces", "design.denovo", "design.validation", "design.representation"
PN = lambda *s: [f"pyrosetta-notebooks:{x}" for x in s]
KB = lambda *s: [f"kuhlman-bradley:{x}" for x in s]
JH = lambda *s: [f"jhu-545614:{x}" for x in s]

UNITS = {"10": ("specialised", "Specialised modelling and scale", ["SEARCH", "TEST"], PN("9.1", "10", "11", "12.1", "12.2", "15.1", "16"))}
TOPICS = {"10.1": "Loops, symmetry and density", "10.2": "Antibodies and membrane proteins", "10.3": "Running at scale, reproducibly"}

# the JHU course topics, cited on the objectives that already answer them
EXISTING = {
    "CPD-4.1.A": JH("T5"), "CPD-4.2.A": JH("T1"), "CPD-6.1.A": JH("T1"), "CPD-6.2.A": JH("T2"),
    "CPD-7.1.A": JH("T3"), "CPD-7.2.A": JH("T3"), "CPD-6.2.B": JH("T4"), "CPD-1.1.A": JH("T5"), "CPD-3.1.A": JH("T5") + PN("3"),
    # the chapter-level workshop items whose sub-items are already cited, plus the Cartesian ligand-docking variant
    "CPD-2.1.A": PN("2"), "CPD-2.2.A": PN("2"), "CPD-6.1.B": PN("8.2"),
}

OBJS = [
    ("CPD-10.1.A", PN("9.1") + KB("5"), "Say what a loop-closure method must guarantee and why loops are modelled separately from the rest of a structure.",
     "A rebuilt loop must still join the fixed flanking residues, so closure is a constraint, not a preference; kinematic closure solves for the dihedrals that close the gap, and loops are irregular and flexible, which is why they are rebuilt rather than threaded."),
    ("CPD-10.1.B", PN("10"), "Describe what a symmetric model fixes and count the independent degrees of freedom symmetry removes.",
     "One asymmetric unit plus a symmetry definition generates the rest, so the energy and the moves apply to the unit and are replicated; n copies of an m-residue chain under exact symmetry leave one chain's degrees of freedom instead of n."),
    ("CPD-10.1.C", PN("11"), "Say what fitting a model into electron density adds to a purely computational score, and what it cannot fix.",
     "Density is experimental evidence that restrains the model, scored alongside the energy function; it cannot rescue a region the map does not resolve, where confidence stays low whatever the score says."),
    ("CPD-10.1.D", PN("5.2"), "Order the stages of a refinement protocol and say what each stage is allowed to move.",
     "Refinement alternates small backbone perturbations, side-chain repacking and minimisation under the all-atom function, usually with the repulsive weight ramped, so the structure settles without escaping the starting fold."),
    ("CPD-10.2.A", PN("12.1") + KB("5"), "Describe how an antibody structure is modelled from its framework and loops, and which loop is the hard one.",
     "The variable domains' frameworks are conserved enough to graft from templates by canonical class; the six complementarity-determining loops are modelled on top, and CDR H3 is the longest, most variable and least predictable."),
    ("CPD-10.2.B", PN("12.2") + KB("5"), "Say what antibody design optimises and why it is a one-sided problem.",
     "Design chooses CDR sequence and length against a chosen epitope on a target that cannot be changed, so it combines one-sided interface design with flexible-loop modelling: the two hardest cases in the field at once."),
    ("CPD-10.2.C", PN("15.1"), "Set up a membrane protein in a bilayer and say what the energy function must change.",
     "The protein is embedded with its hydrophobic span across the membrane and its orientation and depth fixed relative to the bilayer; the solvation term must treat the membrane interior as nonpolar, so a water-based function would misscore buried polar residues."),
    ("CPD-10.3.A", PN("16"), "Distinguish the three ways a design campaign is parallelised and match each to its job.",
     "Independent decoys of one protocol (embarrassingly parallel), one protocol distributed across workers, and many protocols over many inputs; a scan is the first, a large generative pipeline the third."),
    ("CPD-10.3.B", PN("16"), "State what a run must record for a design to be reproducible, and compute the decoy count a campaign needs.",
     "The random seed, the protocol version, the input structure and every option, kept with the output; decoys scale as inputs × protocols × decoys per input, and the lowest-scoring decoy of too small a set is just noise."),
]

MC_ = MC


def facts(name, skill, rows, explain, pace="recall"):
    return Q(name, skill, "{{q}}", pace=pace, cases=[{"q": q, "o1": a, "o2": b, "o3": c, "o4": d} for q, a, b, c, d in rows],
             choice=MC_, correct="0", verify="authored", explain=explain)


ADD = [
    ("CPD-10.1.A", facts("cpd-loop-closure", SA, [
        ("A loop-closure method must guarantee that the rebuilt loop:", "Still connects to the fixed residues at both ends", "Has the lowest possible energy", "Is a helix", "Keeps its original sequence"),
        ("Loops are modelled separately from helices and sheets because they are:", "Irregular and flexible, so regular geometry does not describe them", "Always buried", "Shorter than other elements", "Not scored by the energy function"),
        ("Kinematic closure works by:", "Solving for the dihedrals that close the chain, then sampling the rest", "Minimising from a random start and hoping it closes", "Grafting a loop from a template without changes", "Deleting the loop"),
        ("A designed loop that models well but is disordered in the crystal suggests:", "The loop is genuinely flexible, which the fixed model did not capture", "The sequence was wrong", "The closure failed", "The density was misread"),
    ], "Closure is a hard constraint; flexibility is the reason loops stay hard")),
    ("CPD-10.1.A", Q("cpd-loop-dof", SA, "A {{n}}-residue loop is rebuilt. Its backbone has two free dihedrals per residue, and closure consumes {{c}} of them. How many free backbone degrees of freedom remain?",
        given={"n": {"pick": [6, 8, 12]}, "c": {"pick": [6]}}, value="2*n - c", tex="DOF", final=True, verify="2*n - c",
        explain="Closing a chain at a fixed end point and orientation uses up six degrees of freedom, which is why kinematic closure solves for six torsions and samples the rest")),
    ("CPD-10.1.B", facts("cpd-symmetry", RP, [
        ("In a symmetric model, moves and energies are applied to:", "One asymmetric unit, then replicated by the symmetry definition", "Every chain independently", "Only the largest chain", "The whole assembly atom by atom"),
        ("Exact symmetry is imposed in design because it:", "Cuts the search to one unit and makes one designed interface repeat", "Lowers the energy automatically", "Removes the need for packing", "Guarantees the fold"),
        ("A symmetric homo-oligomer design assumes:", "Every subunit has the same sequence and conformation", "Subunits differ in sequence", "Only the backbone is shared", "There is no interface"),
        ("Designing a nanocage exploits symmetry so that:", "A small designed interface builds a large closed assembly", "No energy function is needed", "The subunits can be different proteins", "Loops need no modelling"),
    ], "Symmetry is a constraint that buys search space and repeats one solution")),
    ("CPD-10.1.B", Q("cpd-symmetry-dof", RP, "An assembly has {{nc}} identical chains of {{m}} residues. Under exact symmetry, how many residues' degrees of freedom does the search actually handle?",
        given={"nc": {"pick": [3, 4, 6, 12]}, "m": {"pick": [60, 95, 120]}}, value="m", tex="residues", final=True, verify="m",
        explain="Exact symmetry reduces the problem to one asymmetric unit, so the search cost is independent of the number of copies")),
    ("CPD-10.1.C", facts("cpd-density", RP, [
        ("Fitting a model into experimental density adds:", "A restraint from evidence, scored alongside the energy function", "A better energy function", "A guarantee of correctness", "A faster search"),
        ("In a region where the map is unresolved, density fitting:", "Cannot settle the conformation, so confidence stays low there", "Resolves the conformation exactly", "Replaces the energy function", "Proves the region is disordered"),
        ("A model that fits the density well but scores badly suggests:", "Either a real strained feature or a modelling error worth inspecting", "The density is wrong", "The energy function is always right", "Nothing"),
        ("Density-guided refinement is valuable mainly because:", "It anchors the model to measurement rather than to the score alone", "It is faster", "It needs no sequence", "It removes the need for refinement"),
    ], "Experimental density is evidence the score does not contain")),
    ("CPD-10.1.D", facts("cpd-refine-stages", SA, [
        ("A refinement protocol alternates:", "Small backbone moves, side-chain repacking and minimisation", "Only minimisation", "Only sequence design", "Only rigid-body moves"),
        ("Ramping the repulsive weight during refinement lets:", "Clashed regions pass through each other before the full weight is restored", "The sequence change", "The backbone stay fixed", "The protocol skip packing"),
        ("Refinement is restrained to the starting structure so that:", "It settles locally instead of drifting to an unrelated conformation", "It reaches the global minimum", "The sequence is preserved", "No energy is computed"),
        ("Refinement should be judged by:", "Whether the score improves without the structure drifting far from the start", "The score alone", "The run time", "The number of decoys"),
    ], "Refinement is local by design: improvement without drift")),
    ("CPD-10.1.D", facts("cpd-refine-diagnose", SA, [
        ("A refinement run ends 6 Å from its starting structure. The likely reading:", "It escaped the intended fold; tighten the restraints", "It refined correctly", "The score function failed", "The loop did not close"),
        ("A refinement run improves the score by 0.2 units over hundreds of steps. The reading:", "The structure was already near a local minimum", "The protocol is broken", "The restraints are too loose", "The sequence is wrong"),
        ("Minimising without first repacking after a backbone move tends to:", "Leave side chains in now-wrong rotamers that minimisation cannot escape", "Give a better result", "Change the sequence", "Close loops"),
    ], "Read refinement by both the score change and the distance moved")),
    ("CPD-10.2.A", facts("cpd-antibody-model", IF, [
        ("Antibody variable domains can be modelled from templates because their:", "Frameworks are structurally conserved across antibodies", "Sequences are identical", "Loops are rigid", "Structures are always known"),
        ("Which complementarity-determining loop is hardest to predict?", "CDR H3, the longest and most variable", "CDR L1", "CDR L2", "CDR H1"),
        ("Most CDR loops other than H3 can be assigned to:", "A small set of canonical conformational classes", "A single universal conformation", "Random conformations", "The framework"),
        ("An antibody model with a confident framework and a poorly resolved H3 should be used:", "With the caveat that the binding loop itself is the least certain part", "As if fully reliable", "Not at all", "Only for the framework"),
    ], "Graft the conserved framework; the variable loops, above all H3, are the uncertainty")),
    ("CPD-10.2.B", facts("cpd-antibody-design", IF, [
        ("Antibody design is a one-sided problem because:", "The epitope on the target cannot be redesigned", "Antibodies have no interface", "Both partners are designed", "The target is unknown"),
        ("Antibody design optimises:", "CDR sequence and loop length against a chosen epitope", "The framework sequence only", "The target's surface", "The constant domains"),
        ("Antibody design is especially hard because it combines:", "One-sided interface design with flexible-loop modelling", "Symmetry with density fitting", "Loop closure with parametric design", "Scoring with minimisation"),
        ("Choosing which epitope to target matters because:", "Binding the wrong surface can give affinity with no function", "Any epitope gives the same result", "Epitopes do not affect design", "The energy function chooses it"),
    ], "The two hardest problems in the field meet in antibody design")),
    ("CPD-10.2.C", facts("cpd-membrane", RP, [
        ("A membrane protein is set up in a bilayer by:", "Embedding it with its hydrophobic span across the membrane and fixing its depth and orientation", "Placing it in water", "Removing its hydrophobic residues", "Scoring it as a soluble protein"),
        ("The energy function must change for a membrane protein because:", "The membrane interior is nonpolar, so burying a polar residue there costs differently than in water", "Lennard-Jones terms do not apply", "Rotamers differ", "Backbones differ"),
        ("Scoring a membrane protein with a water-based solvation model would:", "Misscore residues buried in the bilayer", "Give identical results", "Fail to run", "Be more accurate"),
        ("Predicting the ΔΔG of a point mutation in a membrane protein needs:", "A membrane-aware score, because the residue's environment is the bilayer", "The same protocol as a soluble protein", "No repacking", "Only the sequence"),
    ], "The environment is part of the model: a bilayer is not water")),
    ("CPD-10.3.A", facts("cpd-parallel-kind", VA, [
        ("Running one protocol to produce thousands of independent decoys is:", "Embarrassingly parallel: each job is independent", "A distributed single job", "A multi-protocol sweep", "Serial by necessity"),
        ("Running many different protocols across many inputs is best handled by:", "A job system that tracks which protocol ran on which input", "A single long serial run", "One decoy per input", "Manual bookkeeping"),
        ("A mutational scan parallelises best as:", "Independent jobs, one per mutation and trial", "One distributed job", "A serial loop", "A single decoy"),
        ("The reason a generative design pipeline needs a job system is:", "Its stages differ in cost and each stage's output feeds the next", "It is serial", "It needs no reproducibility", "It uses one protocol"),
    ], "Match the parallel pattern to the shape of the work")),
    ("CPD-10.3.B", Q("cpd-decoys", VA, "A campaign runs {{ni}} input structures through {{np}} protocols with {{nd}} decoys each. How many output models is that?",
        given={"ni": {"pick": [12, 40, 100]}, "np": {"pick": [2, 3]}, "nd": {"pick": [50, 100, 500]}},
        value="ni*np*nd", tex="models", final=True, verify="ni*np*nd",
        explain="Inputs × protocols × decoys; the lowest-scoring model of too small a set is noise, which is why decoy counts are large")),
    ("CPD-10.3.B", facts("cpd-reproducible", VA, [
        ("To reproduce a design run exactly you must record:", "The random seed, the protocol and version, the input and every option", "The output structure only", "The score only", "The date"),
        ("Two runs of the same stochastic protocol with different seeds should:", "Differ, which is why many decoys are run and the set is analysed", "Be identical", "Fail", "Give the same score"),
        ("Reporting only the single best-scoring decoy from a run is misleading because:", "The best of a small stochastic set can be noise rather than signal", "It is always correct", "Scores are deterministic", "Decoys are identical"),
        ("A protocol's version matters to reproducibility because:", "Score-function defaults and movers change between releases", "Versions never change results", "Only the seed matters", "Only the input matters"),
    ], "A result you cannot regenerate is not a result")),
]

ADD += [
    ("CPD-10.1.C", facts("cpd-density-2", RP, [
        ("A model is refined into a 3.5 Å map. At that resolution you can place:", "Backbone and secondary structure reliably, side chains far less so", "Every atom including hydrogens", "Nothing", "Only the ligand"),
        ("Overfitting a model to density means:", "The model reproduces noise in the map rather than real features", "The model ignores the map", "The score is too high", "The map is too sharp"),
        ("Density and the energy function are combined rather than used alone because:", "Each covers what the other misses: evidence and chemistry", "Density is always wrong", "The energy function is exact", "They are the same thing"),
    ], "Resolution sets what the map can decide; the score supplies the chemistry")),
    ("CPD-10.2.A", Q("cpd-cdr-count", IF, "An antibody Fv has how many complementarity-determining loops in total across its heavy and light chains?",
        given={}, cases=[{}], value="6", tex="loops", final=True, verify="Integer(6)",
        explain="Three CDRs per chain (H1-H3 and L1-L3) make six loops; H3 is the longest and hardest to model")),
    ("CPD-10.2.B", facts("cpd-antibody-design-2", IF, [
        ("A designed antibody binds the target with good affinity but also binds a close homologue. The missing step:", "Negative design against the homologue", "More positive design for the target", "A finer rotamer library", "Longer refinement"),
        ("Grafting a CDR with a known binding conformation onto a new framework assumes:", "The framework does not change the loop's conformation much", "The loop is rigid in all contexts", "The target is irrelevant", "Affinity is unchanged by definition"),
        ("Lengthening CDR H3 in a design is a way to:", "Reach into a recessed epitope, at the cost of entropy and predictability", "Increase stability", "Simplify modelling", "Avoid negative design"),
    ], "Specificity needs negative design; loop length buys reach and costs certainty")),
    ("CPD-10.2.C", Q("cpd-tm-span", RP, "A single transmembrane α-helix must cross a hydrophobic core about {{d}} Å thick. At 1.5 Å rise per residue, how many residues is that?",
        given={"d": {"pick": [27, 30, 33]}}, value="d/1.5", tex="residues", verify="nsimplify(d)/Rational(15,10)",
        explain="About 20 residues span a bilayer core, which is why a run of roughly 20 hydrophobic residues flags a membrane span")),
    ("CPD-10.3.A", Q("cpd-parallel-time", VA, "{{nj}} independent jobs of {{tm}} minutes each run on {{nw}} workers. What is the wall-clock time in hours (perfect parallelism)?",
        given={"nj": {"pick": [500, 2000, 9600]}, "tm": {"pick": [6, 15, 40]}, "nw": {"pick": [24, 100, 400]}},
        value="nj*tm/nw/60", tex="hours", verify="Rational(nj*tm, nw*60)",
        explain="Embarrassingly parallel work divides cleanly, so the only questions are worker count and queue time")),
]
